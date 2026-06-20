// server.js — the RENDERER HOST.
//
// The agent never watches anything. This process does:
//   agent (or human) writes a file -> chokidar fires -> rebuild -> push over WS.
//
// Two-way editing:
//   - drag/pin/resize  -> writes _layout.json   (renderer + human own layout)
//   - edit a card      -> writes the card's own .md body/title
//   - edit an output   -> writes the real ICM output file the next stage reads
//
// Concurrency model is ICM's: sequential, human-in-the-loop, last-write-wins.
// You edit between stages, so you and the agent aren't writing the same file
// at the same instant.

import http from "node:http";
import { readFile, readdir, writeFile, stat, mkdir, copyFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { exec } from "node:child_process";
import util from "node:util";
import chokidar from "chokidar";
import matter from "gray-matter";
import { WebSocketServer } from "ws";


const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = __dirname;
const SCREENS_DIR = path.join(ROOT, "_tv", "screens");
const PUBLIC = path.join(ROOT, "public");
const PORT = process.env.PORT || 4321;
const TEXT_EXT = new Set([".md", ".markdown", ".txt", ".csv"]);

// Resolve a workspace-relative path and refuse anything escaping ROOT.
function safePath(rel) {
  const p = path.resolve(ROOT, rel);
  if (p !== ROOT && !p.startsWith(ROOT + path.sep)) throw new Error("path escapes workspace");
  return p;
}

// keep card-supplied screen/id from becoming path traversal.
// No dots allowed, so ".." can never form an up-one segment.
const slug = (x) => String(x || "").replace(/[^A-Za-z0-9_-]/g, "").slice(0, 80);

// ---------- read the filesystem into a state object ----------
async function readScreen(screenName) {
  const dir = path.join(SCREENS_DIR, screenName);
  const layoutPath = path.join(dir, "_layout.json");
  let layout = {};
  if (existsSync(layoutPath)) {
    try { layout = JSON.parse(await readFile(layoutPath, "utf8")); } catch { layout = {}; }
  }
  const entries = (await readdir(dir)).filter((f) => f.endsWith(".md") && !f.startsWith("_"));
  const artifacts = [];
  let i = 0;
  for (const file of entries) {
    const raw = await readFile(path.join(dir, file), "utf8");
    const { data, content } = matter(raw);
    const id = data.id || file.replace(/\.md$/, "");
    const lay = layout[id] || {};
    const col = i % 3, row = Math.floor(i / 3);
    artifacts.push({
      id, file: `_tv/screens/${screenName}/${file}`,
      title: data.title || id, type: data.type || "card",
      stage: data.stage ?? null, status: data.status ?? null, source: data.source ?? null,
      pinned: lay.pinned ?? data.pinned ?? false,
      x: lay.x ?? 24 + col * 360, y: lay.y ?? 24 + row * 260,
      w: lay.w ?? 332, h: lay.h ?? 232, z: lay.z ?? i,
      body: content.trim(),
    });
    i++;
  }
  return artifacts;
}

async function buildState() {
  if (!existsSync(SCREENS_DIR)) return { screens: {} };
  const screens = {};
  for (const name of await readdir(SCREENS_DIR)) {
    const full = path.join(SCREENS_DIR, name);
    if ((await stat(full)).isDirectory()) screens[name] = await readScreen(name);
  }
  return { screens };
}

// rewrite a card's .md, preserving all frontmatter except title/updated
async function writeCard(screen, id, { title, body }) {
  const file = path.join(SCREENS_DIR, screen, `${id}.md`);
  const raw = await readFile(file, "utf8");
  const parsed = matter(raw);
  const data = { ...parsed.data };
  if (title != null) data.title = title;
  data.updated = new Date().toISOString().slice(0, 19);
  await writeFile(file, matter.stringify(body ?? parsed.content, data));
}

// ---------- HTTP ----------
const MIME = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".json": "application/json", ".svg": "image/svg+xml" };
async function readBody(req) { let b = ""; for await (const c of req) b += c; return b ? JSON.parse(b) : {}; }

const server = http.createServer(async (req, res) => {
  const json = (code, obj) => { res.writeHead(code, { "content-type": "application/json" }); res.end(JSON.stringify(obj)); };
  try {
    const u = new URL(req.url, "http://x");

    if (req.method === "GET" && u.pathname === "/api/state") return json(200, await buildState());

    if (req.method === "POST" && u.pathname === "/api/layout") {
      const { screen, layout } = await readBody(req);
      await writeFile(path.join(SCREENS_DIR, screen, "_layout.json"), JSON.stringify(layout, null, 2));
      return json(200, { ok: true });
    }

    // edit a card's own content
    if (req.method === "POST" && u.pathname === "/api/content") {
      const { screen, id, title, body } = await readBody(req);
      await writeCard(screen, id, { title, body });
      return json(200, { ok: true });
    }

    // read a real workspace file (e.g. an ICM output) into the editor
    if (req.method === "GET" && u.pathname === "/api/file") {
      const rel = u.searchParams.get("path") || "";
      if (!TEXT_EXT.has(path.extname(rel))) return json(400, { error: "unsupported file type" });
      const p = safePath(rel);
      if (!existsSync(p)) return json(404, { error: "not found" });
      return json(200, { path: rel, content: await readFile(p, "utf8") });
    }

    // write a real workspace file back
    if (req.method === "POST" && u.pathname === "/api/file") {
      const { path: rel, content } = await readBody(req);
      if (!TEXT_EXT.has(path.extname(rel))) return json(400, { error: "unsupported file type" });
      await writeFile(safePath(rel), content);
      return json(200, { ok: true });
    }

    // an interactive card's answer. CAGED: always lands at
    // _tv/responses/<screen>/<id>.md — the card cannot choose the path.
    if (req.method === "POST" && u.pathname === "/api/respond") {
      const { screen, id, value } = await readBody(req);
      const s = slug(screen), i = slug(id);
      if (!s || !i) return json(400, { error: "bad screen/id" });
      const dir = path.join(ROOT, "_tv", "responses", s);
      await mkdir(dir, { recursive: true });
      const body = typeof value === "string" ? value : JSON.stringify(value, null, 2);
      await writeFile(path.join(dir, `${i}.md`), body + "\n");
      return json(200, { ok: true, path: `_tv/responses/${s}/${i}.md` });
    }

    // static
    const urlPath = u.pathname === "/" ? "/index.html" : u.pathname;
    const filePath = path.join(PUBLIC, path.normalize(urlPath).replace(/^(\.\.[/\\])+/, ""));
    if (existsSync(filePath)) {
      res.writeHead(200, { "content-type": MIME[path.extname(filePath)] || "application/octet-stream" });
      return res.end(await readFile(filePath));
    }
    res.writeHead(404); res.end("not found");
  } catch (err) {
    res.writeHead(500); res.end(String(err));
  }
});

// ---------- WebSocket ----------
const wss = new WebSocketServer({ server });
async function broadcast() {
  const msg = JSON.stringify({ type: "state", ...(await buildState()) });
  for (const c of wss.clients) if (c.readyState === 1) c.send(msg);
}
wss.on("connection", async (ws) => ws.send(JSON.stringify({ type: "state", ...(await buildState()) })));

// ---------- watch loop ----------
let t;
chokidar.watch(SCREENS_DIR, { ignoreInitial: true }).on("all", () => {
  clearTimeout(t); t = setTimeout(broadcast, 80);
});

// ---------- source watch and compilation ----------
const execPromise = util.promisify(exec);

async function buildTailwind() {
  try {
    await execPromise("npx @tailwindcss/cli -i src/styles.css -o public/tailwind-styles.css");
    console.log("  [tailwind] compiled tailwind-styles.css successfully");
  } catch (err) {
    console.error("  [tailwind] compilation error:", err.message);
  }
}

async function buildAll() {
  await mkdir(PUBLIC, { recursive: true });
  await copyFile(path.join(ROOT, "src", "index.html"), path.join(PUBLIC, "index.html"));
  await copyFile(path.join(ROOT, "src", "app.js"), path.join(PUBLIC, "app.js"));
  await buildTailwind();
}

// Watch src/ directory for changes to rebuild source assets automatically
chokidar.watch(path.join(ROOT, "src"), { ignoreInitial: true }).on("all", async (event, filepath) => {
  console.log(`  [src watch] ${event}: ${path.basename(filepath)}`);
  if (filepath.endsWith("index.html") || filepath.endsWith("app.js")) {
    try {
      await copyFile(filepath, path.join(PUBLIC, path.basename(filepath)));
    } catch (err) {
      console.error("  [src watch] copy error:", err);
    }
  }
  await buildTailwind();
  broadcast();
});

// Build all assets on start, then listen
buildAll().then(() => {
  server.listen(PORT, () => {
    console.log(`\n  ICM CCTV — renderer host`);
    console.log(`  watching: ${SCREENS_DIR}`);
    console.log(`  open:     http://localhost:${PORT}\n`);
  });
}).catch((err) => {
  console.error("Failed to build assets on startup:", err);
  process.exit(1);
});


// app.js — the board client.
// Cards are now editable. Editing a card body/title saves to the card's file.
// "edit output" loads the real ICM output file and saves back to IT.

const boardEl = document.getElementById("board");
const screensEl = document.getElementById("screens");
const ledEl = document.getElementById("led");
const statusEl = document.getElementById("status");
const themeToggleBtn = document.getElementById("theme-toggle");
const themeLinkEl = document.getElementById("theme-link");

let state = { screens: {} };
let active = null;
let edit = null;     // { id, title, body }  — inline card edit in progress
let overlay = null;  // { path, content }    — output-file editor open

// ---- tiny markdown ----
function md(src) {
  const esc = (s) => s.replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));
  const inline = (s) => esc(s)
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
  const out = []; let list = null;
  for (const line of src.split("\n")) {
    const h = line.match(/^(#{1,3})\s+(.*)/), li = line.match(/^[-*]\s+(.*)/);
    if (h) { if (list) { out.push("</ul>"); list = null; } out.push(`<h${h[1].length}>${inline(h[2])}</h${h[1].length}>`); }
    else if (li) { if (!list) { out.push("<ul>"); list = 1; } out.push(`<li>${inline(li[1])}</li>`); }
    else if (line.trim() === "") { if (list) { out.push("</ul>"); list = null; } }
    else { if (list) { out.push("</ul>"); list = null; } out.push(`<p>${inline(line)}</p>`); }
  }
  if (list) out.push("</ul>");
  return out.join("");
}

// Injected into every interactive card so agent HTML can call respond(value).
// Uses postMessage because the iframe is sandboxed (no same-origin access).
const RESPOND_HELPER =
  "<script>window.respond=function(v){parent.postMessage({__icm:'respond',value:v},'*')};" +
  "window.addEventListener('message',function(e){if(e.data&&e.data.__icm==='ack'&&typeof window.onResponded==='function')window.onResponded(e.data)});<\/script>";

function renderBody(a) {
  if (a.type === "url") return `<iframe class="w-full h-full border-0" src="${a.body.split("\n")[0].trim()}" sandbox="allow-scripts allow-same-origin allow-popups"></iframe>`;
  if (a.type === "interactive") return `<iframe class="w-full h-full border-0" sandbox="allow-scripts" srcdoc="${(RESPOND_HELPER + a.body).replace(/"/g, "&quot;")}"></iframe>`;
  return md(a.body);
}

function render() {
  const names = Object.keys(state.screens);
  if (!active || !names.includes(active)) active = names[0] || null;
  
  screensEl.innerHTML = names.map((n) => {
    const isActive = n === active;
    const activeClasses = isActive 
      ? "active text-terminal-bg bg-accent-yellow border-accent-yellow font-bold" 
      : "text-terminal-fg/70 border-transparent hover:text-terminal-fg hover:bg-terminal-fg/10";
    return `<button class="screen-tab font-mono text-[11.5px] tracking-wide px-3 py-[5px] rounded-md border cursor-pointer transition-colors duration-150 ${activeClasses}" data-screen="${n}">${n}</button>`;
  }).join("");
  
  screensEl.querySelectorAll(".screen-tab").forEach((b) => (b.onclick = () => { active = b.dataset.screen; render(); }));

  const arts = (state.screens[active] || []).slice().sort((a, b) => a.z - b.z);
  
  // Find current card elements on board
  const existingCards = {};
  boardEl.querySelectorAll(".card").forEach((el) => {
    existingCards[el.dataset.id] = el;
  });
  
  const activeIds = new Set(arts.map(a => a.id));
  
  // Remove cards that are no longer on this screen
  for (const id in existingCards) {
    if (!activeIds.has(id)) {
      existingCards[id].remove();
      delete existingCards[id];
    }
  }

  // Update or append cards
  for (const a of arts) {
    const existing = existingCards[a.id];
    
    if (existing) {
      if (edit && edit.id === a.id) continue; // Skip active edits
      
      const bodyChanged = existing.dataset.body !== a.body;
      const titleChanged = existing.dataset.title !== a.title;
      const statusChanged = existing.dataset.status !== a.status;
      const pinChanged = existing.dataset.pinned !== String(a.pinned);
      
      // If content did not change, just update layout styles
      if (!bodyChanged && !titleChanged && !statusChanged && !pinChanged) {
        existing.style.left = a.x + "px";
        existing.style.top = a.y + "px";
        existing.style.width = a.w + "px";
        existing.style.height = a.h + "px";
        existing.style.zIndex = a.z;
        continue;
      }
      
      // Recreate and replace if content changed
      const newEl = cardEl(a);
      existing.replaceWith(newEl);
      existingCards[a.id] = newEl;
    } else {
      const newEl = cardEl(a);
      boardEl.appendChild(newEl);
      existingCards[a.id] = newEl;
    }
  }

  // Store metadata on each card element for comparison next time
  boardEl.querySelectorAll(".card").forEach((el) => {
    const id = el.dataset.id;
    const a = arts.find(x => x.id === id);
    if (a) {
      el.dataset.body = a.body;
      el.dataset.title = a.title;
      el.dataset.status = a.status;
      el.dataset.pinned = String(a.pinned);
    }
  });

  const n = arts.length;
  statusEl.textContent = `screen "${active || "—"}" · ${n} artifact${n === 1 ? "" : "s"} · click a card to edit · "edit output" opens the real file`;
}

function cardEl(a) {
  const editing = edit && edit.id === a.id;
  const el = document.createElement("div");
  
  // Tailwind styles for card
  const twCard = "absolute flex flex-col bg-panel text-foreground border border-border/10 rounded-lg shadow-xl overflow-hidden select-none transition-shadow duration-150";
  const twPinned = a.pinned ? "pinned ring-2 ring-accent-yellow" : "";
  const twEditing = editing ? "editing ring-2 ring-accent-yellow shadow-2xl" : "";
  
  el.className = `card ${twCard} ${twPinned} ${twEditing}`.trim();
  el.dataset.id = a.id;
  el.style.cssText = `left:${a.x}px;top:${a.y}px;width:${a.w}px;height:${a.h}px;z-index:${editing ? 9999 : a.z}`;

  const titleHtml = editing
    ? `<input class="title-input flex-1 font-sans font-medium text-[13.5px] text-foreground bg-foreground/5 border border-border/10 rounded px-1.5 py-0.5 outline-none" value="${(edit.title || "").replace(/"/g, "&quot;")}" />`
    : `<span class="card-title font-sans font-medium text-[13.5px] flex-1 overflow-hidden text-ellipsis whitespace-nowrap text-foreground">${a.title}</span>`;

  const headRight = editing
    ? `<button class="done font-mono text-[10.5px] text-terminal-bg bg-accent-yellow border-none rounded px-2 py-[3px] cursor-pointer">save ✓</button>`
    : `<button class="pin ${a.pinned ? "on text-accent-yellow" : "text-foreground/30"} border-none bg-transparent cursor-pointer text-[13px] leading-none p-0.5 hover:text-foreground" title="pin">${a.pinned ? "●" : "○"}</button>`;

  const bodyHtml = editing
    ? `<textarea class="body-input w-full h-full resize-none border-none outline-none font-mono text-[12px] leading-relaxed text-foreground bg-transparent">${(edit.body || "").replace(/</g, "&lt;")}</textarea>`
    : renderBody(a);

  const editOutput = a.source ? `<button class="edit-output ml-auto font-mono text-[10px] text-accent-yellow bg-accent-yellow/10 border border-accent-yellow/20 rounded px-1.5 py-0.5 cursor-pointer hover:bg-accent-yellow/25" title="edit the real output file">edit output</button>` : "";

  el.innerHTML = `
    <div class="card-head flex items-center gap-2 cursor-grab p-[9px_11px] bg-foreground/5 border-b border-border/10" ${editing ? "" : "data-drag"}>
      <span class="dot shrink-0 w-[7px] h-[7px] rounded-full bg-foreground/30 ${a.status || ""} ${a.status === "running" ? "bg-accent-yellow animate-pulse" : ""} ${a.status === "done" ? "bg-done" : ""} ${a.status === "blocked" ? "bg-blocked" : ""}"></span>
      ${titleHtml}
      ${a.stage != null ? `<span class="stage-badge font-mono text-[10px] text-terminal-fg bg-terminal-bg px-1.5 py-0.5 rounded">stage ${a.stage}</span>` : ""}
      ${headRight}
    </div>
    <div class="card-body p-3 text-[13px] leading-relaxed overflow-auto flex-1 text-foreground">${bodyHtml}</div>
    <div class="card-foot font-mono text-[10px] text-foreground/50 p-[6px_11px] border-t border-border/10 whitespace-nowrap overflow-hidden text-ellipsis flex gap-1.5 items-center bg-foreground/5"><span class="arrow text-foreground/30">▸</span><span>${a.file}</span>${a.source ? `<span class="arrow text-foreground/30">→</span><span>${a.source}</span>${editOutput}` : ""}</div>
    <div class="resize absolute right-0 bottom-0 w-3.5 h-3.5 cursor-nwse-resize bg-gradient-to-br from-transparent to-black/10 rounded-br-lg"></div>`;

  if (editing) {
    el.querySelector(".title-input").oninput = (e) => (edit.title = e.target.value);
    const ta = el.querySelector(".body-input");
    ta.oninput = (e) => (edit.body = e.target.value);
    ta.onkeydown = (e) => { if ((e.metaKey || e.ctrlKey) && e.key === "Enter") saveCard(); };
    el.querySelector(".done").onclick = saveCard;
    setTimeout(() => ta.focus(), 0);
  } else {
    el.querySelector(".card-body").onclick = () => startEdit(a);
    el.querySelector(".pin").onclick = (e) => { e.stopPropagation(); a.pinned = !a.pinned; saveLayout(); render(); };
    dragify(el, el.querySelector("[data-drag]"), a, "move");
    dragify(el, el.querySelector(".resize"), a, "resize");
  }
  if (a.source && !editing) el.querySelector(".edit-output").onclick = (e) => { e.stopPropagation(); openOutput(a.source); };
  return el;
}

function startEdit(a) {
  if (a.type !== "card") return; // url/interactive bodies aren't free text here
  edit = { id: a.id, title: a.title, body: a.body };
  render();
}

async function saveCard() {
  if (!edit) return;
  const payload = { screen: active, id: edit.id, title: edit.title, body: edit.body };
  edit = null;
  try { await fetch("/api/content", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(payload) }); }
  catch (e) {}
  // the file write triggers a WS push that re-renders with the saved content
}

// ---- output-file overlay editor ----
async function openOutput(relPath) {
  try {
    const r = await fetch("/api/file?path=" + encodeURIComponent(relPath));
    const d = await r.json();
    if (d.error) { alert("Could not open " + relPath + ": " + d.error); return; }
    overlay = { path: d.path, content: d.content };
    renderOverlay();
  } catch (e) { alert("Could not open file"); }
}

function renderOverlay() {
  let el = document.getElementById("overlay");
  if (!overlay) { if (el) el.remove(); return; }
  if (!el) { el = document.createElement("div"); el.id = "overlay"; document.body.appendChild(el); }
  el.className = "fixed inset-0 z-[10000] flex items-center justify-center bg-black/60 backdrop-blur-[2px]";
  el.innerHTML = `
    <div class="ov-panel w-[min(760px,92vw)] h-[min(70vh,620px)] flex flex-col bg-panel rounded-[11px] overflow-hidden shadow-2xl">
      <div class="ov-head flex items-center justify-between gap-3 p-3 bg-foreground/5 border-b border-border/10">
        <span class="ov-path font-mono text-[12px] text-foreground/80">${overlay.path}</span>
        <span class="ov-actions flex gap-2">
          <button class="ov-cancel font-mono text-[11.5px] px-3 py-1.5 rounded border border-border text-foreground/60 bg-transparent hover:bg-foreground/5 cursor-pointer">cancel</button>
          <button class="ov-save font-mono text-[11.5px] px-3 py-1.5 rounded border border-accent-yellow bg-accent-yellow text-terminal-bg hover:bg-accent-yellow/90 cursor-pointer">save file</button>
        </span>
      </div>
      <textarea class="ov-body flex-1 resize-none border-none outline-none p-4 font-mono text-[13px] leading-relaxed text-foreground bg-panel"></textarea>
    </div>`;
  const ta = el.querySelector(".ov-body");
  ta.value = overlay.content;
  ta.oninput = (e) => (overlay.content = e.target.value);
  el.querySelector(".ov-cancel").onclick = () => { overlay = null; renderOverlay(); };
  el.querySelector(".ov-save").onclick = async () => {
    try { await fetch("/api/file", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(overlay) }); } catch (e) {}
    overlay = null; renderOverlay();
  };
  ta.focus();
}

function dragify(card, handle, a, mode) {
  if (!handle) return;
  handle.addEventListener("pointerdown", (e) => {
    if (a.pinned) return;
    e.preventDefault(); handle.setPointerCapture?.(e.pointerId);
    card.classList.add("dragging");
    document.body.classList.add("dragging-active");
    const sx = e.clientX, sy = e.clientY, ox = a.x, oy = a.y, ow = a.w, oh = a.h;
    a.z = Math.max(0, ...(state.screens[active] || []).map((x) => x.z)) + 1;
    card.style.zIndex = a.z;
    const move = (ev) => {
      const dx = ev.clientX - sx, dy = ev.clientY - sy;
      if (mode === "move") { a.x = Math.max(0, ox + dx); a.y = Math.max(0, oy + dy); card.style.left = a.x + "px"; card.style.top = a.y + "px"; }
      else { a.w = Math.max(200, ow + dx); a.h = Math.max(120, oh + dy); card.style.width = a.w + "px"; card.style.height = a.h + "px"; }
    };
    const up = () => {
      card.classList.remove("dragging");
      document.body.classList.remove("dragging-active");
      handle.releasePointerCapture?.(e.pointerId);
      window.removeEventListener("pointermove", move);
      window.removeEventListener("pointerup", up);
      saveLayout();
    };
    window.addEventListener("pointermove", move); window.addEventListener("pointerup", up);
  });
}

function saveLayout() {
  const layout = {};
  for (const a of state.screens[active] || []) layout[a.id] = { x: a.x, y: a.y, w: a.w, h: a.h, z: a.z, pinned: a.pinned };
  fetch("/api/layout", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ screen: active, layout }) }).catch(() => {});
}

// ---- respond() bridge: interactive card -> caged response file ----
// Security: we only act on messages whose source is one of our own iframes,
// and the server writes to _tv/responses/<screen>/<id>.md regardless of what
// the card asks for — the card supplies the value, never the path.
window.addEventListener("message", async (e) => {
  const d = e.data;
  if (!d || d.__icm !== "respond") return;
  let cardId = null, iframe = null;
  boardEl.querySelectorAll(".card").forEach((el) => {
    const f = el.querySelector("iframe");
    if (f && f.contentWindow === e.source) { cardId = el.dataset.id; iframe = f; }
  });
  if (!cardId) return; // message from something that isn't our card — ignore

  // Custom Hook: If on gta-chase screen and responding from the steering column,
  // write the choice directly to the 003-command card file instead of responses!
  if (active === "gta-chase" && cardId === "002-control") {
    try {
      await fetch("/api/content", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ screen: active, id: "003-command", body: d.value })
      });
      statusEl.textContent = `steering command written to 003-command.md → ${d.value}`;
      iframe && iframe.contentWindow.postMessage({ __icm: "ack", ok: true, id: cardId, value: d.value }, "*");
    } catch (err) {}
    return;
  }

  try {
    const r = await fetch("/api/respond", { method: "POST", headers: { "content-type": "application/json" },
      body: JSON.stringify({ screen: active, id: cardId, value: d.value }) });
    const res = await r.json();
    if (res.ok) {
      statusEl.textContent = `response saved → ${res.path}`;
      iframe && iframe.contentWindow.postMessage({ __icm: "ack", ok: true, id: cardId, path: res.path }, "*");
    }
  } catch (err) {}
});

// ---- Theme Switcher ----
function initTheme() {
  const savedTheme = localStorage.getItem("icm-theme") || "classic";
  setTheme(savedTheme);
}

function setTheme(theme) {
  if (theme === "tailwind") {
    themeLinkEl.href = "/tailwind-styles.css";
    document.documentElement.classList.add("dark");
    themeToggleBtn.textContent = "Style: Tailwind";
    localStorage.setItem("icm-theme", "tailwind");
  } else {
    themeLinkEl.href = "/styles.css";
    document.documentElement.classList.remove("dark");
    themeToggleBtn.textContent = "Style: Classic";
    localStorage.setItem("icm-theme", "classic");
  }
}

themeToggleBtn.addEventListener("click", () => {
  const currentTheme = localStorage.getItem("icm-theme") || "classic";
  setTheme(currentTheme === "classic" ? "tailwind" : "classic");
});

initTheme();

// Keyboard steering support in parent window for gta-chase screen
window.addEventListener("keydown", async (e) => {
  if (active !== "gta-chase") return;
  const key = e.key.toLowerCase();
  let direction = null;
  if (e.key === "ArrowLeft" || key === "a") direction = "left";
  else if (e.key === "ArrowRight" || key === "d") direction = "right";
  else if (e.key === "ArrowUp" || key === "w") direction = "straight";

  if (direction) {
    e.preventDefault();
    try {
      await fetch("/api/content", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ screen: active, id: "003-command", body: direction })
      });
      statusEl.textContent = `keyboard steering command written to 003-command.md → ${direction}`;
    } catch (err) {}
  }
});

function connect() {
  const ws = new WebSocket(`ws://${location.host}`);
  ws.onopen = () => ledEl.classList.add("live");
  ws.onclose = () => { ledEl.classList.remove("live"); statusEl.textContent = "renderer disconnected — restart with npm start"; setTimeout(connect, 1200); };
  ws.onmessage = (ev) => {
    const msg = JSON.parse(ev.data);
    if (msg.type !== "state") return;
    state = { screens: msg.screens };
    render();
    
    // Broadcast the updated state to all running interactive iframes on the current screen
    const activeArts = state.screens[active] || [];
    boardEl.querySelectorAll(".card iframe").forEach((iframe) => {
      try {
        iframe.contentWindow.postMessage({ 
          __icm: "state", 
          screens: state.screens, 
          active: active, 
          artifacts: activeArts 
        }, "*");
      } catch (e) {}
    });
  };
}
connect();

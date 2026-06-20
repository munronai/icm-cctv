#!/usr/bin/env python3
import os
import json

SCREENS_DIR = "_tv/screens"
OUTPUT_FILE = "exports/Board.jsx"

def parse_frontmatter(raw_content):
    if not raw_content.startswith("---"):
        return {}, raw_content
    parts = raw_content.split("---", 2)
    if len(parts) < 3:
        return {}, raw_content
    
    yaml_text = parts[1]
    body = parts[2]
    
    metadata = {}
    for line in yaml_text.strip().split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            metadata[k.strip()] = v.strip().strip("'\"")
            
    return metadata, body

def main():
    if not os.path.exists(SCREENS_DIR):
        print(f"Error: Screens directory '{SCREENS_DIR}' not found.")
        return

    screens_data = {}
    
    # Iterate through each screen directory
    for name in sorted(os.listdir(SCREENS_DIR)):
        screen_path = os.path.join(SCREENS_DIR, name)
        if not os.path.isdir(screen_path):
            continue
            
        layout_path = os.path.join(screen_path, "_layout.json")
        layout = {}
        if os.path.exists(layout_path):
            try:
                with open(layout_path, "r", encoding="utf-8") as f:
                    layout = json.load(f)
            except Exception as e:
                print(f"[Warning] Failed to parse layout for '{name}': {e}")

        cards = []
        md_files = sorted([f for f in os.listdir(screen_path) if f.endswith(".md") and not f.startswith("_")])
        
        for idx, file in enumerate(md_files):
            file_path = os.path.join(screen_path, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    raw = f.read()
            except Exception as e:
                print(f"[Warning] Failed to read '{file}': {e}")
                continue
                
            metadata, body = parse_frontmatter(raw)
            card_id = metadata.get("id", file.replace(".md", ""))
            lay = layout.get(card_id, {})
            
            col = idx % 3
            row = idx // 3
            
            cards.append({
                "id": card_id,
                "title": metadata.get("title", card_id),
                "type": metadata.get("type", "card"),
                "status": metadata.get("status", None),
                "stage": int(metadata["stage"]) if "stage" in metadata else None,
                "source": metadata.get("source", None),
                "x": lay.get("x", 24 + col * 360),
                "y": lay.get("y", 24 + row * 260),
                "w": lay.get("w", 332),
                "h": lay.get("h", 232),
                "z": lay.get("z", idx),
                "pinned": lay.get("pinned", False),
                "body": body.strip()
            })
            
        screens_data[name] = cards

    # Ensure the outputs directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    # React Component Template (Raw string, no escaping required)
    template = """import React, { useState, useEffect, useRef, useCallback } from "react";

// ICM Television — Claude.ai-native board (Dynamically exported from local state).
// Same presentation layer as the local repo, minus the file-watch loop.
// Here there's no agent writing files and no renderer watching them, so YOU
// play the agent: add and edit cards. Persistence is window.storage, not disk.

const PALETTE = {
  surface: "#202326", rail: "#181a1c", railLine: "rgba(255,255,255,.07)",
  card: "#f4f3ef", ink: "#1d1e1b", soft: "#6c6b64", edge: "rgba(0,0,0,.14)",
  mono: "#565a4f", signal: "#e0a23c", signalDim: "#8a6e34",
  done: "#6f9e6a", blocked: "#c2683f", running: "#e0a23c", idle: "#b9b8b1",
};

const SEED_SCREENS = SEED_SCREENS_PLACEHOLDER;

const STORE_KEY = "icm-tv-board-v2";

function fmt(src) {
  // tiny inline markdown: **bold**, `code`, lines
  return src.split("\\n").map((line, i) => {
    const parts = [];
    let rest = line, key = 0;
    const re = /(\\*\\*[^*]+\\*\\*|`[^`]+`)/;
    while (true) {
      const m = rest.match(re);
      if (!m) { parts.push(<span key={key++}>{rest}</span>); break; }
      if (m.index > 0) parts.push(<span key={key++}>{rest.slice(0, m.index)}</span>);
      const tok = m[0];
      if (tok.startsWith("**")) parts.push(<strong key={key++}>{tok.slice(2, -2)}</strong>);
      else parts.push(<code key={key++} style={{ fontFamily: "ui-monospace, monospace", fontSize: 11.5, background: "rgba(0,0,0,.06)", padding: "1px 4px", borderRadius: 3 }}>{tok.slice(1, -1)}</code>);
      rest = rest.slice(m.index + tok.length);
    }
    return <p key={i} style={{ margin: "0 0 6px" }}>{parts}</p>;
  });
}

export default function Board() {
  const [screens, setScreens] = useState(SEED_SCREENS);
  const [active, setActive] = useState(Object.keys(SEED_SCREENS)[0] || "");
  const [editing, setEditing] = useState(null);
  const [loaded, setLoaded] = useState(false);
  const boardRef = useRef(null);
  const drag = useRef(null);

  const cards = screens[active] || [];

  useEffect(() => {
    (async () => {
      try {
        const r = await window.storage.get(STORE_KEY);
        if (r && r.value) setScreens(JSON.parse(r.value));
      } catch (e) { /* first run, keep seed */ }
      setLoaded(true);
    })();
  }, []);

  const persist = useCallback(async (next) => {
    try { await window.storage.set(STORE_KEY, JSON.stringify(next)); } catch (e) {}
  }, []);

  const update = useCallback((nextCards) => {
    const nextScreens = { ...screens, [active]: nextCards };
    setScreens(nextScreens);
    persist(nextScreens);
  }, [screens, active, persist]);

  const onPointerDown = (e, card, mode) => {
    if (editing) return;
    if (card.pinned && mode === "move") return; // block drag if pinned
    e.preventDefault();
    const topZ = Math.max(0, ...cards.map((c) => c.z)) + 1;
    drag.current = { id: card.id, mode, sx: e.clientX, sy: e.clientY, ox: card.x, oy: card.y, ow: card.w, oh: card.h };
    
    const nextCards = cards.map((c) => (c.id === card.id ? { ...c, z: topZ } : c));
    setScreens((prev) => ({ ...prev, [active]: nextCards }));
  };

  useEffect(() => {
    const move = (e) => {
      const d = drag.current; if (!d) return;
      const dx = e.clientX - d.sx, dy = e.clientY - d.sy;
      
      setScreens((prev) => {
        const activeCards = prev[active] || [];
        const nextCards = activeCards.map((c) => {
          if (c.id !== d.id) return c;
          if (d.mode === "move") return { ...c, x: Math.max(0, d.ox + dx), y: Math.max(0, d.oy + dy) };
          return { ...c, w: Math.max(200, d.ow + dx), h: Math.max(110, d.oh + dy) };
        });
        return { ...prev, [active]: nextCards };
      });
    };
    const up = () => { if (drag.current) { drag.current = null; persist(screens); } };
    window.addEventListener("pointermove", move);
    window.addEventListener("pointerup", up);
    return () => { window.removeEventListener("pointermove", move); window.removeEventListener("pointerup", up); };
  }, [screens, active, persist]);

  const togglePin = (id) => update(cards.map((c) => (c.id === id ? { ...c, pinned: !c.pinned } : c)));
  const setBody = (id, body) => {
    const nextCards = cards.map((c) => (c.id === id ? { ...c, body } : c));
    const nextScreens = { ...screens, [active]: nextCards };
    setScreens(nextScreens);
  };
  const commitBody = () => { setEditing(null); persist(screens); };

  const addCard = () => {
    const n = cards.length + 1;
    const id = String(n).padStart(3, "0") + "-card";
    const next = [...cards, { id, title: "New artifact", type: "card", pinned: false, stage: null, status: null, source: null,
      x: 40 + ((n * 18) % 200), y: 40 + ((n * 24) % 160), w: 300, h: 150, z: Math.max(0, ...cards.map((c) => c.z)) + 1,
      body: "Click the body to edit." }];
    update(next);
    setEditing(id);
  };

  const reset = () => {
    setScreens(SEED_SCREENS);
    persist(SEED_SCREENS);
  };

  const dotColor = (s) => PALETTE[s] || PALETTE.idle;

  return (
    <div style={{ fontFamily: "Inter, system-ui, sans-serif", height: "100vh", background: PALETTE.surface, color: "#e7e6e1", display: "flex", flexDirection: "column", overflow: "hidden" }}>
      {/* rail */}
      <div style={{ height: 52, display: "flex", alignItems: "center", justifyContent: "space-between", padding: "0 16px", background: PALETTE.rail, borderBottom: `1px solid ${PALETTE.railLine}` }}>
        <div style={{ display: "flex", alignItems: "center", gap: 11 }}>
          <span style={{ width: 9, height: 9, borderRadius: "50%", alignSelf: "center", background: loaded ? PALETTE.signal : "#4a4d50", boxShadow: loaded ? `0 0 8px ${PALETTE.signal}` : "none" }} />
          <span style={{ fontFamily: "'Space Grotesk', system-ui, sans-serif", fontWeight: 600, fontSize: 15 }}>ICM&nbsp;Television</span>
          
          {/* Tabs Switcher */}
          <div style={{ display: "flex", gap: 4, marginLeft: 20 }}>
            {Object.keys(screens).map((s) => (
              <button
                key={s}
                onClick={() => { setActive(s); setEditing(null); }}
                style={{
                  padding: "4px 8px",
                  borderRadius: 4,
                  border: "none",
                  background: s === active ? PALETTE.signal : "transparent",
                  color: s === active ? PALETTE.ink : "#7d8085",
                  fontWeight: s === active ? "bold" : "normal",
                  fontSize: 11.5,
                  cursor: "pointer"
                }}
              >
                {s}
              </button>
            ))}
          </div>
        </div>
        <div style={{ display: "flex", gap: 8 }}>
          <button onClick={addCard} style={btn(PALETTE.signal, PALETTE.ink)}>+ card</button>
          <button onClick={reset} style={btn("transparent", "#9a9da1", PALETTE.railLine)}>reset</button>
        </div>
      </div>

      {/* board */}
      <div ref={boardRef} style={{ position: "relative", flex: 1, overflow: "auto",
        backgroundImage: "linear-gradient(rgba(255,255,255,.035) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.035) 1px, transparent 1px)",
        backgroundSize: "28px 28px" }}>
        {cards.slice().sort((a, b) => a.z - b.z).map((c) => (
          <div key={c.id} style={{ position: "absolute", left: c.x, top: c.y, width: c.w, height: c.h, zIndex: c.z,
            display: "flex", flexDirection: "column", background: PALETTE.card, color: PALETTE.ink,
            border: `1px solid ${PALETTE.edge}`, borderRadius: 9, overflow: "hidden",
            outline: c.pinned ? `1.5px solid ${PALETTE.signal}` : "none", outlineOffset: -1,
            boxShadow: "0 1px 2px rgba(0,0,0,.25), 0 14px 28px -16px rgba(0,0,0,.55)" }}>
            {/* head */}
            <div onPointerDown={(e) => onPointerDown(e, c, "move")}
              style={{ display: "flex", alignItems: "center", gap: 8, padding: "9px 11px", borderBottom: "1px solid rgba(0,0,0,.08)", cursor: c.pinned ? "default" : "grab" }}>
              <span style={{ width: 7, height: 7, borderRadius: "50%", background: dotColor(c.status), flex: "0 0 auto" }} />
              <span style={{ fontFamily: "'Space Grotesk', system-ui, sans-serif", fontWeight: 500, fontSize: 13.5, flex: 1, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{c.title}</span>
              {c.stage != null && <span style={{ fontFamily: "ui-monospace, monospace", fontSize: 10, color: "#fff", background: "#3a3d36", padding: "2px 6px", borderRadius: 4 }}>stage {c.stage}</span>}
              <button onClick={() => togglePin(c.id)} style={{ border: "none", background: "none", cursor: "pointer", fontSize: 12, color: c.pinned ? PALETTE.signalDim : "#b6b5ad" }}>{c.pinned ? "●" : "○"}</button>
            </div>
            {/* body */}
            <div onClick={() => editing !== c.id && setEditing(c.id)}
              style={{ padding: "11px 13px", fontSize: 13, lineHeight: 1.5, overflow: "auto", flex: 1, cursor: editing === c.id ? "text" : "pointer" }}>
              {editing === c.id
                ? <textarea autoFocus value={c.body} onChange={(e) => setBody(c.id, e.target.value)} onBlur={commitBody}
                    style={{ width: "100%", height: "100%", border: "none", outline: "none", resize: "none", font: "inherit", color: PALETTE.ink, background: "transparent" }} />
                : (c.type === "interactive" ? 
                    <div style={{ fontSize: 11, fontStyle: "italic", color: "#666" }}>
                      [Interactive Card preview in Claude]
                      <div style={{ marginTop: 8, border: "1px dashed #ccc", padding: 6, background: "#fff", fontFamily: "ui-monospace, monospace", fontSize: 10, overflow: "auto" }}>
                        {c.body.substring(0, 160)}...
                      </div>
                    </div> : fmt(c.body))}
            </div>
            {/* SIGNATURE: the file this card would be on disk */}
            <div style={{ fontFamily: "ui-monospace, monospace", fontSize: 10, color: PALETTE.mono, padding: "6px 11px", borderTop: "1px solid rgba(0,0,0,.07)", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
              ▸ _tv/screens/{active}/{c.id}.md{c.source ? `  →  ${c.source}` : ""}
            </div>
            {/* resize */}
            <div onPointerDown={(e) => onPointerDown(e, c, "resize")}
              style={{ position: "absolute", right: 2, bottom: 2, width: 14, height: 14, cursor: "nwse-resize",
                background: "linear-gradient(135deg, transparent 50%, rgba(0,0,0,.18) 50%)", borderRadius: "0 0 8px 0" }} />
          </div>
        ))}
      </div>

      {/* status */}
      <div style={{ height: 26, display: "flex", alignItems: "center", gap: 14, padding: "0 16px", background: PALETTE.rail, borderTop: `1px solid ${PALETTE.railLine}`, fontFamily: "ui-monospace, monospace", fontSize: 11, color: "#7d8085" }}>
        <span>{cards.length} artifacts</span>
        <span>·</span>
        <span>screen: {active}</span>
        <span>·</span>
        <span>missing: agent-watch loop</span>
      </div>
    </div>
  );
}

function btn(bg, color, border) {
  return { fontFamily: "ui-monospace, monospace", fontSize: 11.5, color, background: bg,
    border: `1px solid ${border || bg}`, padding: "5px 11px", borderRadius: 6, cursor: "pointer" };
}
"""

    # Insert screens data into template
    react_code = template.replace("SEED_SCREENS_PLACEHOLDER", json.dumps(screens_data, indent=2))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(react_code)
        
    print(f"\n[Export] Successfully compiled active screens into: {OUTPUT_FILE}")
    print("You can copy the code inside this file and paste it into Claude (as a React/JSX artifact) or Gemini to render the board natively!")

if __name__ == "__main__":
    main()

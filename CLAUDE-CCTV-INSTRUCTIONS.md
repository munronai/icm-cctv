# Instructions for Claude / Gemini: How to Generate CCTV Board Previews

If the user asks you to display documentation, research, or pipeline specs in a "CCTV" or "Television" layout, you should package your written documents into a single, self-contained interactive board preview. 

This allows the user to see the cards laid out in space, drag/resize them, switch screens, and edit them natively within your chat preview window (Claude Artifacts or Gemini Code preview).

Choose the format based on the assistant platform:
* **For Claude**: Generate a **React/JSX Artifact** (boilerplate below).
* **For Gemini / General Browsers**: Generate an **HTML/JS Artifact** (boilerplate below).

---

## 📂 The Data Schema

You will convert your generated documents into a JSON object `SEED_SCREENS` structured like this:

```json
{
  "screen-name-1": [
    {
      "id": "card-unique-id",
      "title": "Card Title",
      "type": "card", // or "interactive"
      "status": "done", // "done", "blocked", "running", or null
      "stage": 1, // integer stage index or null
      "source": "path/to/source.md", // optional
      "x": 24, "y": 24, "w": 332, "h": 232, "z": 0, // position & dimensions
      "pinned": false,
      "body": "Markdown text goes here..."
    }
  ]
}
```

Ensure cards do not overlap by spacing out their `x` (width ~332 + 28px gap) and `y` (height ~232 + 28px gap) coordinates.

---

## ⚛️ Template 1: For Claude (React/JSX Artifact)

When using Claude.ai, wrap the generated code block below inside a React Artifact. Replace `SEED_SCREENS_PLACEHOLDER` with your generated JSON screens data.

```jsx
import React, { useState, useEffect, useRef, useCallback } from "react";

const PALETTE = {
  surface: "#202326", rail: "#181a1c", railLine: "rgba(255,255,255,.07)",
  card: "#f4f3ef", ink: "#1d1e1b", soft: "#6c6b64", edge: "rgba(0,0,0,.14)",
  mono: "#565a4f", signal: "#e0a23c", signalDim: "#8a6e34",
  done: "#6f9e6a", blocked: "#c2683f", running: "#e0a23c", idle: "#b9b8b1",
};

// INSERT YOUR GENERATED CARD DATA HERE
const SEED_SCREENS = SEED_SCREENS_PLACEHOLDER;

const STORE_KEY = "icm-tv-board-v2";

function fmt(src) {
  return src.split("\n").map((line, i) => {
    const parts = [];
    let rest = line, key = 0;
    const re = /(\*\*[^*]+\*\*|`[^`]+`)/;
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
  const boardRef = useRef(null);
  const drag = useRef(null);
  const cards = screens[active] || [];

  const update = useCallback((nextCards) => {
    setScreens(prev => ({ ...prev, [active]: nextCards }));
  }, [active]);

  const onPointerDown = (e, card, mode) => {
    if (editing) return;
    if (card.pinned && mode === "move") return;
    e.preventDefault();
    const topZ = Math.max(0, ...cards.map((c) => c.z)) + 1;
    drag.current = { id: card.id, mode, sx: e.clientX, sy: e.clientY, ox: card.x, oy: card.y, ow: card.w, oh: card.h };
    setScreens(prev => ({ ...prev, [active]: cards.map(c => c.id === card.id ? { ...c, z: topZ } : c) }));
  };

  useEffect(() => {
    const move = (e) => {
      const d = drag.current; if (!d) return;
      const dx = e.clientX - d.sx, dy = e.clientY - d.sy;
      setScreens(prev => {
        const nextCards = (prev[active] || []).map(c => {
          if (c.id !== d.id) return c;
          if (d.mode === "move") return { ...c, x: Math.max(0, d.ox + dx), y: Math.max(0, d.oy + dy) };
          return { ...c, w: Math.max(200, d.ow + dx), h: Math.max(110, d.oh + dy) };
        });
        return { ...prev, [active]: nextCards };
      });
    };
    const up = () => { if (drag.current) drag.current = null; };
    window.addEventListener("pointermove", move);
    window.addEventListener("pointerup", up);
    return () => { window.removeEventListener("pointermove", move); window.removeEventListener("pointerup", up); };
  }, [active]);

  const togglePin = (id) => update(cards.map(c => c.id === id ? { ...c, pinned: !c.pinned } : c));
  const setBody = (id, body) => setScreens(prev => ({ ...prev, [active]: (prev[active] || []).map(c => c.id === id ? { ...c, body } : c) }));

  const dotColor = (s) => PALETTE[s] || PALETTE.idle;

  return (
    <div style={{ fontFamily: "Inter, sans-serif", height: "100vh", background: PALETTE.surface, color: "#e7e6e1", display: "flex", flexDirection: "column", overflow: "hidden" }}>
      <div style={{ height: 52, display: "flex", alignItems: "center", justifyContent: "space-between", padding: "0 16px", background: PALETTE.rail, borderBottom: `1px solid ${PALETTE.railLine}` }}>
        <div style={{ display: "flex", alignItems: "center", gap: 11 }}>
          <span style={{ width: 9, height: 9, borderRadius: "50%", background: PALETTE.signal, boxShadow: `0 0 8px ${PALETTE.signal}` }} />
          <span style={{ fontWeight: 600, fontSize: 15 }}>ICM Television</span>
          <div style={{ display: "flex", gap: 4, marginLeft: 20 }}>
            {Object.keys(screens).map(s => (
              <button key={s} onClick={() => { setActive(s); setEditing(null); }} style={{ padding: "4px 8px", borderRadius: 4, border: "none", background: s === active ? PALETTE.signal : "transparent", color: s === active ? PALETTE.ink : "#7d8085", fontSize: 11.5, cursor: "pointer" }}>{s}</button>
            ))}
          </div>
        </div>
      </div>

      <div ref={boardRef} style={{ position: "relative", flex: 1, overflow: "auto", backgroundImage: "linear-gradient(rgba(255,255,255,.035) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.035) 1px, transparent 1px)", backgroundSize: "28px 28px" }}>
        {cards.slice().sort((a, b) => a.z - b.z).map(c => (
          <div key={c.id} style={{ position: "absolute", left: c.x, top: c.y, width: c.w, height: c.h, zIndex: c.z, display: "flex", flexDirection: "column", background: PALETTE.card, color: PALETTE.ink, border: `1px solid ${PALETTE.edge}`, borderRadius: 9, overflow: "hidden", outline: c.pinned ? `1.5px solid ${PALETTE.signal}` : "none", outlineOffset: -1 }}>
            <div onPointerDown={(e) => onPointerDown(e, c, "move")} style={{ display: "flex", alignItems: "center", gap: 8, padding: "9px 11px", borderBottom: "1px solid rgba(0,0,0,.08)", cursor: c.pinned ? "default" : "grab" }}>
              <span style={{ width: 7, height: 7, borderRadius: "50%", background: dotColor(c.status) }} />
              <span style={{ fontWeight: 500, fontSize: 13.5, flex: 1, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{c.title}</span>
              <button onClick={() => togglePin(c.id)} style={{ border: "none", background: "none", cursor: "pointer", fontSize: 12, color: c.pinned ? PALETTE.signalDim : "#b6b5ad" }}>{c.pinned ? "●" : "○"}</button>
            </div>
            <div onClick={() => editing !== c.id && setEditing(c.id)} style={{ padding: "11px 13px", fontSize: 13, lineHeight: 1.5, overflow: "auto", flex: 1 }}>
              {editing === c.id
                ? <textarea autoFocus value={c.body} onChange={(e) => setBody(c.id, e.target.value)} onBlur={() => setEditing(null)} style={{ width: "100%", height: "100%", border: "none", outline: "none", resize: "none", color: PALETTE.ink, background: "transparent" }} />
                : fmt(c.body)}
            </div>
            <div style={{ fontFamily: "monospace", fontSize: 10, color: PALETTE.mono, padding: "6px 11px", borderTop: "1px solid rgba(0,0,0,.07)", truncate: "true" }}>▸ _tv/screens/{active}/{c.id}.md</div>
            <div onPointerDown={(e) => onPointerDown(e, c, "resize")} style={{ position: "absolute", right: 2, bottom: 2, width: 14, height: 14, cursor: "nwse-resize", background: "linear-gradient(135deg, transparent 50%, rgba(0,0,0,.18) 50%)", borderRadius: "0 0 8px 0" }} />
          </div>
        ))}
      </div>
    </div>
  );
}
```

---

## 🌐 Template 2: For Gemini (HTML/JS Preview)

When using Gemini Web, output this single code block inside a code box. Replace `SEED_SCREENS_PLACEHOLDER` with your generated JSON screens data.

```html
<!DOCTYPE html>
<html lang="en" class="h-full">
<head>
  <meta charset="utf-8">
  <title>ICM Television Preview</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body { background-color: #202326; color: #e7e6e1; }
    .board-grid { background-image: linear-gradient(rgba(255,255,255,0.035) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.035) 1px, transparent 1px); background-size: 28px 28px; }
    .card { position: absolute; display: flex; flex-direction: column; background: #f4f3ef; color: #1d1e1b; border: 1px solid rgba(0,0,0,.14); border-radius: 9px; box-shadow: 0 1px 2px rgba(0,0,0,.25); overflow: hidden; }
    .card.pinned { outline: 1.5px solid #e0a23c; outline-offset: -1px; }
  </style>
</head>
<body class="h-full flex flex-col overflow-hidden font-sans">
  <header class="h-[52px] flex items-center justify-between px-4 bg-[#181a1c] border-b border-white/10 shrink-0">
    <div class="flex items-center gap-3">
      <span class="w-[9px] h-[9px] rounded-full bg-accentYellow shadow-[0_0_8px_#e0a23c]"></span>
      <span class="font-bold text-[15px]">ICM Television</span>
      <nav id="tabs" class="flex gap-1 ml-6"></nav>
    </div>
  </header>
  <main id="board" class="flex-1 relative overflow-auto board-grid"></main>
  <footer class="h-[26px] flex items-center px-4 bg-[#181a1c] border-t border-white/10 font-mono text-[10.5px] text-[#7d8085] shrink-0">
    <span id="active-screen-name">screen: --</span>
  </footer>

  <script>
    // INSERT YOUR GENERATED CARD DATA HERE
    let state = SEED_SCREENS_PLACEHOLDER;
    let active = Object.keys(state)[0] || "";
    let editingId = null;

    defFmt = (text) => {
      return text.split('\n').map(line => {
        let formatted = line.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/`(.*?)`/g, '<code class="bg-black/5 px-1 py-0.5 rounded font-mono text-[11px]">$1</code>');
        return `<p class="mb-1.5">${formatted}</p>`;
      }).join('');
    };

    function renderTabs() {
      const tabsEl = document.getElementById("tabs");
      tabsEl.innerHTML = Object.keys(state).map(name => {
        const isActive = name === active;
        return `<button onclick="switchTab('${name}')" class="px-2.5 py-1 text-[11px] font-bold rounded ${isActive ? 'bg-accentYellow text-[#1d1e1b]' : 'text-slate-400 hover:text-white'}">${name}</button>`;
      }).join('');
    }

    function switchTab(name) { active = name; editingId = null; renderTabs(); renderBoard(); }

    function renderBoard() {
      const boardEl = document.getElementById("board");
      const cards = state[active] || [];
      
      boardEl.innerHTML = cards.map(c => {
        const dotColor = c.status === "done" ? "bg-[#6f9e6a]" : (c.status === "blocked" ? "bg-[#c2683f]" : "bg-slate-400");
        const bodyContent = editingId === c.id 
          ? `<textarea id="edit-${c.id}" onblur="saveCardBody('${c.id}')" class="w-full h-full p-0 bg-transparent resize-none border-none outline-none text-[13px] text-[#1d1e1b]">${c.body}</textarea>`
          : defFmt(c.body);

        return `
          <div id="card-${c.id}" class="card ${c.pinned ? 'pinned' : ''}" style="left: ${c.x}px; top: ${c.y}px; width: ${c.w}px; height: ${c.h}px; z-index: ${c.z};">
            <div class="flex items-center gap-2 p-[9px_11px] border-b border-black/10 bg-black/[0.03] ${c.pinned ? 'cursor-default' : 'cursor-grab'}" onmousedown="startDrag(event, '${c.id}', 'move')">
              <span class="w-2 h-2 rounded-full ${dotColor}"></span>
              <span class="font-sans font-semibold text-[13.5px] flex-1 truncate">${c.title}</span>
              <button onclick="togglePin('${c.id}')" class="text-[11.5px] ${c.pinned ? 'text-[#8a6e34]' : 'text-slate-400'}">${c.pinned ? '●' : '○'}</button>
            </div>
            <div class="p-3 text-[13px] leading-relaxed overflow-auto flex-1" onclick="startEdit('${c.id}')">${bodyContent}</div>
            <div class="font-mono text-[9.5px] text-[#565a4f] p-[6px_11px] border-t border-black/[0.07] bg-black/[0.02] truncate">▸ _tv/screens/${active}/${c.id}.md</div>
            <div class="absolute right-0 bottom-0 w-3.5 h-3.5 cursor-nwse-resize bg-gradient-to-br from-transparent to-black/15" onmousedown="startDrag(event, '${c.id}', 'resize')"></div>
          </div>
        `;
      }).join('');
      document.getElementById("active-screen-name").textContent = `screen: ${active}`;
      if (editingId) { const ta = document.getElementById(`edit-${editingId}`); if (ta) ta.focus(); }
    }

    function togglePin(id) { const card = (state[active] || []).find(c => c.id === id); if (card) { card.pinned = !card.pinned; renderBoard(); } }
    function startEdit(id) { if (editingId === id) return; editingId = id; renderBoard(); }
    function saveCardBody(id) { const card = (state[active] || []).find(c => c.id === id); const ta = document.getElementById(`edit-${id}`); if (card && ta) { card.body = ta.value; } editingId = null; renderBoard(); }

    let dragData = null;
    function startDrag(e, id, mode) {
      const cards = state[active] || [];
      const card = cards.find(c => c.id === id);
      if (!card || editingId) return;
      if (card.pinned && mode === 'move') return;
      e.preventDefault();
      const cardEl = document.getElementById(`card-${id}`);
      const topZ = Math.max(0, ...cards.map(c => c.z)) + 1;
      card.z = topZ; cardEl.style.zIndex = topZ;
      dragData = { id, mode, sx: e.clientX, sy: e.clientY, ox: card.x, oy: card.y, ow: card.w, oh: card.h, el: cardEl, card };
      document.addEventListener("mousemove", onDrag);
      document.addEventListener("mouseup", endDrag);
    }

    function onDrag(e) {
      if (!dragData) return;
      const dx = e.clientX - dragData.sx, dy = e.clientY - dragData.sy;
      if (dragData.mode === "move") {
        dragData.card.x = Math.max(0, dragData.ox + dx); dragData.card.y = Math.max(0, dragData.oy + dy);
        dragData.el.style.left = dragData.card.x + "px"; dragData.el.style.top = dragData.card.y + "px";
      } else {
        dragData.card.w = Math.max(200, dragData.ow + dx); dragData.card.h = Math.max(110, dragData.oh + dy);
        dragData.el.style.width = dragData.card.w + "px"; dragData.el.style.height = dragData.card.h + "px";
      }
    }

    function endDrag() { document.removeEventListener("mousemove", onDrag); document.removeEventListener("mouseup", endDrag); }

    renderTabs();
    renderBoard();
  </script>
</body>
</html>
```

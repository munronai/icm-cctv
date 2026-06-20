#!/usr/bin/env python3
import os
import json

SCREENS_DIR = "_tv/screens"
OUTPUT_FILE = "exports/Board.html"

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

    # HTML Presentation Template
    template = """<!DOCTYPE html>
<html lang="en" class="h-full">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>ICM Television — Claude & Gemini Preview</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            accentYellow: '#e0a23c',
            doneGreen: '#6f9e6a',
            blockedRed: '#c2683f'
          }
        }
      }
    }
  </script>
  <style>
    body { background-color: #202326; color: #e7e6e1; }
    .board-grid {
      background-image:
        linear-gradient(rgba(255, 255, 255, 0.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.035) 1px, transparent 1px);
      background-size: 28px 28px;
    }
    .card {
      position: absolute;
      display: flex;
      flex-direction: column;
      background: #f4f3ef;
      color: #1d1e1b;
      border: 1px solid rgba(0,0,0,.14);
      border-radius: 9px;
      box-shadow: 0 1px 2px rgba(0,0,0,.25), 0 14px 28px -16px rgba(0,0,0,.55);
      overflow: hidden;
      user-select: none;
    }
    .card.pinned {
      outline: 1.5px solid #e0a23c;
      outline-offset: -1px;
    }
    .card.dragging {
      box-shadow: 0 6px 12px rgba(0,0,0,.3), 0 30px 50px -18px rgba(0,0,0,.7);
      z-index: 9999 !important;
    }
  </style>
</head>
<body class="h-full flex flex-col overflow-hidden font-sans">

  <!-- Header Rail -->
  <header class="h-[52px] flex items-center justify-between px-4 bg-[#181a1c] border-b border-white/10 shrink-0">
    <div class="flex items-center gap-3">
      <span class="w-[9px] h-[9px] rounded-full bg-accentYellow shadow-[0_0_8px_#e0a23c]"></span>
      <span class="font-bold text-[15px]">ICM Television</span>
      <span class="font-mono text-[10.5px] text-[#7d8085]">cloud preview · presentation only</span>
      
      <!-- Tab Rail Switcher -->
      <nav id="tabs" class="flex gap-1 ml-6"></nav>
    </div>
    <div class="flex gap-2">
      <button onclick="addCard()" class="font-mono text-[11px] bg-accentYellow text-[#1d1e1b] px-3 py-1.5 rounded font-bold hover:bg-amber-500">+ card</button>
      <button onclick="reset()" class="font-mono text-[11px] border border-white/10 px-3 py-1.5 rounded hover:bg-white/5">reset</button>
    </div>
  </header>

  <!-- Board Workspace -->
  <main id="board" class="flex-1 relative overflow-auto board-grid"></main>

  <!-- Status Bar -->
  <footer class="h-[26px] flex items-center gap-3 px-4 bg-[#181a1c] border-t border-white/10 font-mono text-[10.5px] text-[#7d8085] shrink-0">
    <span id="card-count">0 cards</span>
    <span>·</span>
    <span id="active-screen-name">screen: --</span>
    <span>·</span>
    <span>missing: agent-watch loop</span>
  </footer>

  <script>
    // Seed data populated by python script
    let state = SEED_SCREENS_PLACEHOLDER;
    let active = Object.keys(state)[0] || "";
    let editingId = null;

    // Simple markdown formatter
    defFmt = (text) => {
      return text.split('\\n').map(line => {
        let formatted = line
          .replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>')
          .replace(/`(.*?)`/g, '<code class="bg-black/5 px-1 py-0.5 rounded font-mono text-[11px]">$1</code>');
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

    function switchTab(name) {
      active = name;
      editingId = null;
      renderTabs();
      renderBoard();
    }

    function renderBoard() {
      const boardEl = document.getElementById("board");
      const cards = state[active] || [];
      
      boardEl.innerHTML = cards.map(c => {
        const dotColor = c.status === "done" ? "bg-doneGreen" : (c.status === "blocked" ? "bg-blockedRed" : (c.status === "running" ? "bg-accentYellow animate-pulse" : "bg-slate-400"));
        const bodyContent = editingId === c.id 
          ? `<textarea id="edit-${c.id}" onblur="saveCardBody('${c.id}')" class="w-full h-full p-0 bg-transparent resize-none border-none outline-none text-[13px] leading-relaxed text-[#1d1e1b]">${c.body}</textarea>`
          : (c.type === "interactive" 
              ? `<div class="text-[11px] italic text-slate-500">[Interactive Card preview in Claude/Gemini]</div><div class="mt-2 p-1.5 bg-white border border-slate-200 font-mono text-[10px] overflow-auto max-h-[120px]">${c.body.replace(/</g, '&lt;')}</div>` 
              : defFmt(c.body));

        return `
          <div id="card-${c.id}" class="card ${c.pinned ? 'pinned' : ''}" style="left: ${c.x}px; top: ${c.y}px; width: ${c.w}px; height: ${c.h}px; z-index: ${c.z};">
            <!-- Header -->
            <div class="flex items-center gap-2 p-[9px_11px] border-b border-black/10 bg-black/[0.03] ${c.pinned ? 'cursor-default' : 'cursor-grab'}" onmousedown="startDrag(event, '${c.id}', 'move')">
              <span class="w-2 h-2 rounded-full ${dotColor}"></span>
              <span class="font-sans font-semibold text-[13.5px] flex-1 truncate">${c.title}</span>
              ${c.stage != null ? `<span class="bg-[#3a3d36] text-white font-mono text-[9.5px] px-1.5 py-0.5 rounded">stage ${c.stage}</span>` : ""}
              <button onclick="togglePin('${c.id}')" class="text-[11.5px] ${c.pinned ? 'text-[#8a6e34]' : 'text-slate-400'}">${c.pinned ? '●' : '○'}</button>
            </div>
            <!-- Body -->
            <div class="p-3 text-[13px] leading-relaxed overflow-auto flex-1 cursor-pointer" onclick="startEdit('${c.id}')">
              ${bodyContent}
            </div>
            <!-- Footer -->
            <div class="font-mono text-[9.5px] text-[#565a4f] p-[6px_11px] border-t border-black/[0.07] bg-black/[0.02] truncate select-none">
              ▸ _tv/screens/${active}/${c.id}.md ${c.source ? `→ ${c.source}` : ''}
            </div>
            <!-- Resize Anchor -->
            <div class="absolute right-0 bottom-0 w-3.5 h-3.5 cursor-nwse-resize bg-gradient-to-br from-transparent to-black/15" onmousedown="startDrag(event, '${c.id}', 'resize')"></div>
          </div>
        `;
      }).join('');

      document.getElementById("card-count").textContent = `${cards.length} cards`;
      document.getElementById("active-screen-name").textContent = `screen: ${active}`;

      // Auto-focus editing textareas
      if (editingId) {
        const ta = document.getElementById(`edit-${editingId}`);
        if (ta) ta.focus();
      }
    }

    function togglePin(id) {
      const card = (state[active] || []).find(c => c.id === id);
      if (card) {
        card.pinned = !card.pinned;
        renderBoard();
      }
    }

    function startEdit(id) {
      if (editingId === id) return;
      editingId = id;
      renderBoard();
    }

    function saveCardBody(id) {
      const card = (state[active] || []).find(c => c.id === id);
      const ta = document.getElementById(`edit-${id}`);
      if (card && ta) {
        card.body = ta.value;
      }
      editingId = null;
      renderBoard();
    }

    function addCard() {
      const cards = state[active] || [];
      const n = cards.length + 1;
      const id = String(n).padStart(3, "0") + "-card";
      
      cards.push({
        id,
        title: "New card",
        type: "card",
        x: 40 + ((n * 18) % 200),
        y: 40 + ((n * 24) % 160),
        w: 300,
        h: 150,
        z: Math.max(0, ...cards.map(c => c.z)) + 1,
        pinned: false,
        body: "Click body to edit."
      });
      editingId = id;
      renderBoard();
    }

    function reset() {
      location.reload();
    }

    // Drag and Drop Engine
    let dragData = null;
    function startDrag(e, id, mode) {
      const cards = state[active] || [];
      const card = cards.find(c => c.id === id);
      if (!card || editingId) return;
      if (card.pinned && mode === 'move') return;

      e.preventDefault();
      const cardEl = document.getElementById(`card-${id}`);
      cardEl.classList.add("dragging");

      // Elevate z-index
      const topZ = Math.max(0, ...cards.map(c => c.z)) + 1;
      card.z = topZ;
      cardEl.style.zIndex = topZ;

      dragData = {
        id,
        mode,
        sx: e.clientX,
        sy: e.clientY,
        ox: card.x,
        oy: card.y,
        ow: card.w,
        oh: card.h,
        el: cardEl,
        card
      };

      document.addEventListener("mousemove", onDrag);
      document.addEventListener("mouseup", endDrag);
    }

    function onDrag(e) {
      if (!dragData) return;
      const dx = e.clientX - dragData.sx;
      const dy = e.clientY - dragData.sy;

      if (dragData.mode === "move") {
        dragData.card.x = Math.max(0, dragData.ox + dx);
        dragData.card.y = Math.max(0, dragData.oy + dy);
        dragData.el.style.left = dragData.card.x + "px";
        dragData.el.style.top = dragData.card.y + "px";
      } else {
        dragData.card.w = Math.max(200, dragData.ow + dx);
        dragData.card.h = Math.max(110, dragData.oh + dy);
        dragData.el.style.width = dragData.card.w + "px";
        dragData.el.style.height = dragData.card.h + "px";
      }
    }

    function endDrag() {
      if (dragData) {
        dragData.el.classList.remove("dragging");
        dragData = null;
      }
      document.removeEventListener("mousemove", onDrag);
      document.removeEventListener("mouseup", endDrag);
    }

    // Initial render
    renderTabs();
    renderBoard();
  </script>
</body>
</html>"""

    # Insert screens data into template
    html_code = template.replace("SEED_SCREENS_PLACEHOLDER", json.dumps(screens_data, indent=2))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html_code)
        
    print(f"\n[Export] Successfully compiled active screens into: {OUTPUT_FILE}")
    print("You can double-click this file or upload it into Claude/Gemini to render the board natively as static HTML!")

if __name__ == "__main__":
    main()

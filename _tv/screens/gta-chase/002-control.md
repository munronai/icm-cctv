---
id: 002-control
title: Directional Control Panel
type: interactive
status: blocked
---
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-white p-3 font-sans h-full flex flex-col justify-between">
  
  <div class="text-center mb-2">
    <p class="text-[11px] text-slate-400 font-mono">STEERING COLUMN</p>
    <p class="text-[10px] text-slate-500 font-mono mt-0.5">Click buttons below or use Keyboard (← / → / ↑ or A / D / W)</p>
  </div>

  <!-- Steering Wheel Grid -->
  <div class="grid grid-cols-3 gap-2 shrink-0">
    <button onclick="steer('left')" id="btn-left" class="bg-slate-900 border border-slate-800 hover:bg-slate-800 hover:border-slate-700 active:bg-accentYellow active:text-slate-950 p-3 rounded-lg flex flex-col items-center justify-center transition-all select-none focus:outline-none">
      <span class="text-lg">⬅️</span>
      <span class="text-[9px] font-mono font-bold mt-1 uppercase">Left</span>
    </button>
    <button onclick="steer('straight')" id="btn-straight" class="bg-slate-900 border border-slate-800 hover:bg-slate-800 hover:border-slate-700 active:bg-accentYellow active:text-slate-950 p-3 rounded-lg flex flex-col items-center justify-center transition-all select-none focus:outline-none">
      <span class="text-lg">⬆️</span>
      <span class="text-[9px] font-mono font-bold mt-1 uppercase">Straight</span>
    </button>
    <button onclick="steer('right')" id="btn-right" class="bg-slate-900 border border-slate-800 hover:bg-slate-800 hover:border-slate-700 active:bg-accentYellow active:text-slate-950 p-3 rounded-lg flex flex-col items-center justify-center transition-all select-none focus:outline-none">
      <span class="text-lg">➡️</span>
      <span class="text-[9px] font-mono font-bold mt-1 uppercase">Right</span>
    </button>
  </div>

  <!-- Command indicator -->
  <div class="text-center mt-3 border-t border-slate-900 pt-2 shrink-0">
    <span class="text-[10px] text-slate-500 font-mono">Last Signal Sent:</span>
    <span id="last-sig" class="text-[10px] text-emerald-400 font-mono font-bold ml-1 uppercase">None</span>
  </div>

  <script>
    function steer(direction) {
      document.getElementById('last-sig').textContent = direction;
      
      // Flash button active state briefly for keyboard feedback
      const btn = document.getElementById('btn-' + direction);
      if (btn) {
        btn.classList.add('bg-accentYellow', 'text-slate-950');
        setTimeout(() => btn.classList.remove('bg-accentYellow', 'text-slate-950'), 150);
      }

      // Submit via the response bridge
      if (typeof window.respond === 'function') {
        window.respond(direction);
      }
    }

    // Keyboard support
    window.addEventListener('keydown', (e) => {
      const key = e.key.toLowerCase();
      if (e.key === 'ArrowLeft' || key === 'a') {
        steer('left');
      } else if (e.key === 'ArrowRight' || key === 'd') {
        steer('right');
      } else if (e.key === 'ArrowUp' || key === 'w') {
        steer('straight');
      }
    });
  </script>
</body>
</html>

---
id: 001-chase
title: "GTA CCTV: City Car Chase"
type: interactive
status: running
---
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body { margin: 0; padding: 0; background: #000; overflow: hidden; }
    canvas { background: #222; display: block; margin: 0 auto; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
  </style>
</head>
<body class="flex flex-col h-full items-center justify-center p-2 text-white">

  <!-- Dashboard Panel -->
  <div class="w-full max-w-[420px] bg-slate-900 border border-slate-800 rounded-lg p-2.5 flex flex-col gap-2 font-mono text-[11px] mb-2 shrink-0">
    <div class="flex justify-between items-center border-b border-slate-800 pb-1.5">
      <span class="text-emerald-400 font-bold flex items-center gap-1">
        <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
        CCTV FEED: ACTIVE CHASE
      </span>
      <span id="status-tag" class="bg-amber-500/20 text-amber-400 px-1.5 py-0.5 rounded font-bold uppercase tracking-wider">Chasing</span>
    </div>
    <div class="grid grid-cols-2 gap-2 text-slate-400">
      <div>Next Turn: <span id="next-turn" class="text-accentYellow font-bold text-yellow-400">NONE</span></div>
      <div>Distance: <span id="dist-metric" class="text-white font-bold">--</span></div>
    </div>
  </div>

  <!-- Game Canvas -->
  <canvas id="gameCanvas" width="400" height="260" class="rounded-lg border border-slate-800"></canvas>

  <div class="w-full max-w-[420px] flex gap-2 mt-2 shrink-0">
    <button onclick="resetGame()" class="flex-1 bg-slate-800 hover:bg-slate-700 text-slate-200 py-1.5 rounded font-mono text-[10px] uppercase font-bold border border-slate-700">Reset Simulation</button>
  </div>

  <script>
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');

    // Road Grid Layout
    const X_POS = [40, 140, 240, 340];
    const Y_POS = [40, 140, 240];
    const ROAD_WIDTH = 24;

    // Simulation Speeds
    const SPEED = 2.0;

    // Game variables
    let player, police, lastCommandTimestamp = null, gameState = "chasing";
    let pendingCommand = null;

    class Car {
      constructor(ix, iy, color, isPolice = false) {
        this.ix = ix;
        this.iy = iy;
        this.x = X_POS[ix];
        this.y = Y_POS[iy];
        this.color = color;
        this.isPolice = isPolice;
        this.vx = SPEED;
        this.vy = 0;
        this.angle = 0;
        this.sirenTimer = 0;
      }

      update() {
        this.x += this.vx;
        this.y += this.vy;

        // Detect current angle based on velocity
        if (this.vx > 0) this.angle = 0;
        else if (this.vx < 0) this.angle = Math.PI;
        else if (this.vy > 0) this.angle = Math.PI / 2;
        else if (this.vy < 0) this.angle = -Math.PI / 2;

        // Check if we are approaching an intersection
        for (let ix = 0; ix < X_POS.length; ix++) {
          for (let iy = 0; iy < Y_POS.length; iy++) {
            const jx = X_POS[ix];
            const jy = Y_POS[iy];

            // Distance to intersection
            const d = Math.hypot(this.x - jx, this.y - jy);

            // If we are close enough, snap to it and make a decision
            if (d < SPEED * 0.6) {
              // Only trigger decision if we aren't already locked
              if (this.ix !== ix || this.iy !== iy) {
                this.x = jx;
                this.y = jy;
                this.ix = ix;
                this.iy = iy;
                this.onIntersection(ix, iy);
              }
            }
          }
        }
      }

      onIntersection(ix, iy) {
        if (!this.isPolice) {
          // Player car intersection logic
          let turn = pendingCommand;
          pendingCommand = null; // Clear command once evaluated
          document.getElementById('next-turn').textContent = "NONE";
          document.getElementById('next-turn').className = "text-yellow-400";

          let nextVx = this.vx;
          let nextVy = this.vy;

          if (turn === "left") {
            // Relative turn left
            if (this.vx > 0) { nextVx = 0; nextVy = -SPEED; } // East -> North
            else if (this.vx < 0) { nextVx = 0; nextVy = SPEED; } // West -> South
            else if (this.vy > 0) { nextVx = SPEED; nextVy = 0; } // South -> East
            else if (this.vy < 0) { nextVx = -SPEED; nextVy = 0; } // North -> West
          } else if (turn === "right") {
            // Relative turn right
            if (this.vx > 0) { nextVx = 0; nextVy = SPEED; } // East -> South
            else if (this.vx < 0) { nextVx = 0; nextVy = -SPEED; } // West -> North
            else if (this.vy > 0) { nextVx = -SPEED; nextVy = 0; } // South -> West
            else if (this.vy < 0) { nextVx = SPEED; nextVy = 0; } // North -> East
          }

          // Check map bounds
          const nextIx = ix + Math.sign(nextVx);
          const nextIy = iy + Math.sign(nextVy);

          if (nextIx >= 0 && nextIx < X_POS.length && nextIy >= 0 && nextIy < Y_POS.length) {
            this.vx = nextVx;
            this.vy = nextVy;
          } else {
            // Turn blocked by map boundary - keep moving straight or pick any valid turn
            this.resolveBlockedPath(ix, iy);
          }
        } else {
          // Police chasing logic (BFS pathfinding to player)
          this.policeDecision(ix, iy);
        }
      }

      resolveBlockedPath(ix, iy) {
        // If heading hits wall, pick a random valid road direction
        const dirs = [
          { vx: SPEED, vy: 0 },
          { vx: -SPEED, vy: 0 },
          { vx: 0, vy: SPEED },
          { vx: 0, vy: -SPEED }
        ];
        
        // Don't turn back if possible
        const oppositeVx = -this.vx;
        const oppositeVy = -this.vy;

        for (const dir of dirs) {
          if (dir.vx === oppositeVx && dir.vy === oppositeVy) continue;
          
          const nextIx = ix + Math.sign(dir.vx);
          const nextIy = iy + Math.sign(dir.vy);
          if (nextIx >= 0 && nextIx < X_POS.length && nextIy >= 0 && nextIy < Y_POS.length) {
            this.vx = dir.vx;
            this.vy = dir.vy;
            return;
          }
        }

        // Ultimate fallback: turn around
        this.vx = oppositeVx;
        this.vy = oppositeVy;
      }

      policeDecision(ix, iy) {
        // Simple tracking: reduce Manhattan distance to player's current intersection
        const dx = player.ix - ix;
        const dy = player.iy - iy;
        
        let possibleDirs = [];
        
        if (dx > 0) possibleDirs.push({ vx: SPEED, vy: 0 });
        if (dx < 0) possibleDirs.push({ vx: -SPEED, vy: 0 });
        if (dy > 0) possibleDirs.push({ vx: 0, vy: SPEED });
        if (dy < 0) possibleDirs.push({ vx: 0, vy: -SPEED });

        // Add remaining valid directions as fallback
        const allDirs = [
          { vx: SPEED, vy: 0 },
          { vx: -SPEED, vy: 0 },
          { vx: 0, vy: SPEED },
          { vx: 0, vy: -SPEED }
        ];
        possibleDirs = possibleDirs.concat(allDirs);

        // Filter valid directions within map bounds and prevent police from turning directly back
        for (const dir of possibleDirs) {
          if (dir.vx === -this.vx && dir.vy === -this.vy) continue;

          const nextIx = ix + Math.sign(dir.vx);
          const nextIy = iy + Math.sign(dir.vy);

          if (nextIx >= 0 && nextIx < X_POS.length && nextIy >= 0 && nextIy < Y_POS.length) {
            this.vx = dir.vx;
            this.vy = dir.vy;
            return;
          }
        }
      }

      draw() {
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.angle);

        // Shadow
        ctx.fillStyle = 'rgba(0,0,0,0.3)';
        ctx.fillRect(-6, -2, 12, 7);

        // Car Body
        ctx.fillStyle = this.color;
        ctx.fillRect(-6, -3.5, 12, 7);

        // Windshield
        ctx.fillStyle = '#c1e2f7';
        ctx.fillRect(1, -2.5, 2, 5);
        ctx.fillStyle = '#333';
        ctx.fillRect(-3, -2.5, 1, 5);

        // Wheels
        ctx.fillStyle = '#000';
        ctx.fillRect(-5, -4.5, 3, 1);
        ctx.fillRect(2, -4.5, 3, 1);
        ctx.fillRect(-5, 3.5, 3, 1);
        ctx.fillRect(2, 3.5, 3, 1);

        // Police Siren Light
        if (this.isPolice) {
          this.sirenTimer += 0.2;
          ctx.beginPath();
          ctx.arc(-1, 0, 2, 0, Math.PI * 2);
          ctx.fillStyle = Math.sin(this.sirenTimer) > 0 ? '#ff0000' : '#0000ff';
          ctx.fill();
        }

        ctx.restore();
      }
    }

    // Initialize/Reset
    function resetGame() {
      player = new Car(0, 0, '#ef4444'); // Red car starting at top-left
      police = new Car(3, 2, '#3b82f6', true); // Police car starting at bottom-right
      gameState = "chasing";
      pendingCommand = null;
      document.getElementById('status-tag').textContent = "Chasing";
      document.getElementById('status-tag').className = "bg-amber-500/20 text-amber-400 px-1.5 py-0.5 rounded font-bold uppercase tracking-wider";
      document.getElementById('next-turn').textContent = "NONE";
      document.getElementById('next-turn').className = "text-yellow-400";
    }

    // Listen to parent's websocket broadcast message
    window.addEventListener('message', (e) => {
      if (e.data && e.data.__icm === 'state') {
        const ctrl = e.data.artifacts.find(a => a.id === '003-command');
        if (ctrl) {
          const updated = ctrl.updated || ctrl.body;
          if (updated !== lastCommandTimestamp) {
            lastCommandTimestamp = updated;
            const cmd = ctrl.body.trim().toLowerCase();
            if (cmd === 'left' || cmd === 'right') {
              pendingCommand = cmd;
              document.getElementById('next-turn').textContent = cmd.toUpperCase();
              document.getElementById('next-turn').className = "text-emerald-400 font-bold";
            }
          }
        }
      }
    });

    // Drawing City Grid
    function drawMap() {
      ctx.fillStyle = '#1e293b'; // Slate background representing building areas
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Draw Roads
      ctx.fillStyle = '#334155'; // Dark road color
      // Horizontal roads
      Y_POS.forEach(y => {
        ctx.fillRect(0, y - ROAD_WIDTH / 2, canvas.width, ROAD_WIDTH);
      });
      // Vertical roads
      X_POS.forEach(x => {
        ctx.fillRect(x - ROAD_WIDTH / 2, 0, ROAD_WIDTH, canvas.height);
      });

      // Draw Dashed Lane Dividers
      ctx.strokeStyle = '#e2e8f0';
      ctx.lineWidth = 1;
      ctx.setLineDash([4, 6]);
      Y_POS.forEach(y => {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();
      });
      X_POS.forEach(x => {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
        ctx.stroke();
      });
      ctx.setLineDash([]); // Reset dash

      // Draw City Block outlines (Buildings)
      ctx.fillStyle = '#0f172a';
      // Columns (3 blocks) & Rows (2 blocks)
      for (let c = 0; c < 3; c++) {
        for (let r = 0; r < 2; r++) {
          const bx = X_POS[c] + ROAD_WIDTH / 2;
          const by = Y_POS[r] + ROAD_WIDTH / 2;
          const bw = X_POS[c + 1] - X_POS[c] - ROAD_WIDTH;
          const bh = Y_POS[r + 1] - Y_POS[r] - ROAD_WIDTH;
          
          ctx.fillRect(bx, by, bw, bh);
          ctx.strokeStyle = '#334155';
          ctx.lineWidth = 1;
          ctx.strokeRect(bx + 2, by + 2, bw - 4, bh - 4);
        }
      }
    }

    // Main Loop
    function loop() {
      drawMap();

      if (gameState === "chasing") {
        player.update();
        police.update();

        // Calculate distance
        const dist = Math.hypot(player.x - police.x, player.y - police.y);
        document.getElementById('dist-metric').textContent = Math.round(dist) + "m";

        // Check crash condition
        if (dist < 14) {
          gameState = "busted";
          document.getElementById('status-tag').textContent = "BUSTED!";
          document.getElementById('status-tag').className = "bg-red-500/20 text-red-400 px-1.5 py-0.5 rounded font-bold uppercase tracking-wider animate-bounce";
        }
      }

      // Draw cars
      player.draw();
      police.draw();

      if (gameState === "busted") {
        // Overlay Busted banner
        ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.font = 'bold 24px Courier New';
        ctx.fillStyle = '#ef4444';
        ctx.textAlign = 'center';
        ctx.fillText('BUSTED!', canvas.width / 2, canvas.height / 2 - 10);
        
        ctx.font = '10px Courier New';
        ctx.fillStyle = '#cbd5e1';
        ctx.fillText('Click Reset Simulation to escape.', canvas.width / 2, canvas.height / 2 + 15);
      }

      requestAnimationFrame(loop);
    }

    resetGame();
    loop();
  </script>
</body>
</html>

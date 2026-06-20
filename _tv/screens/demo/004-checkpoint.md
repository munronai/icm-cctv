---
id: 004-checkpoint
title: Checkpoint — pick risk framing
type: interactive
stage: 2
status: blocked
---
<div style="font-family:system-ui;padding:14px;color:#1d1e1b">
  <p style="margin:0 0 10px"><b>The agent is waiting.</b> Which framing should the classifier lead with?</p>
  <div style="display:flex;gap:6px;flex-wrap:wrap">
    <button onclick="respond('tier-first')" style="font:inherit;font-size:12px;padding:5px 10px;border:1px solid #c2bfb6;border-radius:6px;background:#fff;cursor:pointer">tier-first</button>
    <button onclick="respond('use-case-first')" style="font:inherit;font-size:12px;padding:5px 10px;border:1px solid #c2bfb6;border-radius:6px;background:#fff;cursor:pointer">use-case-first</button>
    <button onclick="respond('obligation-first')" style="font:inherit;font-size:12px;padding:5px 10px;border:1px solid #c2bfb6;border-radius:6px;background:#fff;cursor:pointer">obligation-first</button>
  </div>
  <p id="ack" style="margin:10px 0 0;font-size:12px;color:#6f9e6a;min-height:1em"></p>
  <script>window.onResponded=function(e){document.getElementById('ack').textContent='\u2713 saved \u2192 '+e.path};</script>
</div>

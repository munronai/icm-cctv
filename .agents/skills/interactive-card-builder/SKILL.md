---
name: interactive-card-builder
description: Help users design and generate self-contained interactive board cards (choice buttons, sliders, checkboxes, charts, and input forms) that report responses back to the agent.
---

# Interactive Card Builder Skill

This skill helps you generate `type: interactive` cards for CCTV/Television screens. Interactive cards display rich UIs (forms, buttons, charts, sliders) and send user responses back to the agent's workspace.

## Card Requirements

To write a valid interactive card, you must create a Markdown file in `_tv/screens/<screen>/<id>.md` with the following structure:

```markdown
---
id: <card-id>
title: <card-title>
type: interactive
status: blocked       # Interactive cards usually pause/block the agent
---
<HTML CONTENT HERE>
```

### Communication Bridge
Within the HTML content, you have access to a global `respond(value)` function (automatically injected by the board). When the user interacts with your card controls, you must call `respond(value)` to submit their input. The submitted value will land at `_tv/responses/<screen>/<id>.md`.

## Helper script
You can use the built-in generator script to interactively create new card templates:
```bash
python3 .agents/skills/interactive-card-builder/scripts/generate_card.py
```

## Examples

### 1. Choice Buttons
Use this for simple checkpoints where a user selects a single path:
```html
<div style="font-family: sans-serif; padding: 10px; display: flex; flex-direction: column; gap: 8px;">
  <p style="margin: 0 0 8px 0; font-size: 13px; color: #333;">Select the classification approach:</p>
  <button onclick="respond('tier-first')" style="padding: 8px 12px; border: 1px solid #ccc; border-radius: 6px; background: #fff; cursor: pointer; text-align: left; transition: background 0.1s;" onmouseover="this.style.background='#f0f0f0'" onmouseout="this.style.background='#fff'">
    <strong>Tier-First</strong> — Classify by high-level risk tiers first.
  </button>
  <button onclick="respond('use-case-first')" style="padding: 8px 12px; border: 1px solid #ccc; border-radius: 6px; background: #fff; cursor: pointer; text-align: left; transition: background 0.1s;" onmouseover="this.style.background='#f0f0f0'" onmouseout="this.style.background='#fff'">
    <strong>Use-Case-First</strong> — Classify by specific end-user applications.
  </button>
</div>
```

### 2. Multi-Input Form (Sliders & Radio Buttons)
Collect multiple variables before submitting:
```html
<div style="font-family: sans-serif; padding: 10px; display: flex; flex-direction: column; gap: 12px; font-size: 13px;">
  <div>
    <label style="display: block; margin-bottom: 4px; font-weight: bold;">Threshold Value:</label>
    <input type="range" id="threshold" min="0" max="100" value="50" style="width: 100%;" oninput="document.getElementById('t-val').textContent=this.value">
    <span id="t-val">50</span>%
  </div>
  <div>
    <label style="display: block; margin-bottom: 4px; font-weight: bold;">Priority:</label>
    <label><input type="radio" name="priority" value="low"> Low</label>
    <label><input type="radio" name="priority" value="med" checked> Medium</label>
    <label><input type="radio" name="priority" value="high"> High</label>
  </div>
  <button onclick="submitForm()" style="padding: 6px 12px; background: #e0a23c; border: none; border-radius: 4px; color: #1d1e1b; font-weight: bold; cursor: pointer;">Submit Response</button>
</div>
<script>
function submitForm() {
  const threshold = document.getElementById('threshold').value;
  const priority = document.querySelector('input[name="priority"]:checked').value;
  respond({ threshold: parseInt(threshold), priority: priority });
}
</script>
```

### 3. SVG-based Interactive Chart
Visualize data tabularly and offer a control node:
```html
<div style="font-family: sans-serif; padding: 10px; display: flex; flex-direction: column; gap: 12px; font-size: 13px;">
  <svg viewBox="0 0 200 100" style="width: 100%; height: auto; border-bottom: 1px solid #ccc;">
    <!-- Simple Bar Chart -->
    <rect x="20" y="30" width="30" height="70" fill="#6f9e6a" />
    <rect x="70" y="10" width="30" height="90" fill="#e0a23c" />
    <rect x="120" y="50" width="30" height="50" fill="#c2683f" />
    <text x="35" y="95" font-size="8" text-anchor="middle" fill="#fff">A</text>
    <text x="85" y="95" font-size="8" text-anchor="middle" fill="#fff">B</text>
    <text x="135" y="95" font-size="8" text-anchor="middle" fill="#fff">C</text>
  </svg>
  <div style="display: flex; gap: 6px;">
    <button onclick="respond('approve-chart')" style="flex: 1; padding: 6px; background: #6f9e6a; border: none; border-radius: 4px; color: white; cursor: pointer;">Approve Chart</button>
    <button onclick="respond('reject-chart')" style="flex: 1; padding: 6px; background: #c2683f; border: none; border-radius: 4px; color: white; cursor: pointer;">Request Redraft</button>
  </div>
</div>
```

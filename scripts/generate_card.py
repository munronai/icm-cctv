#!/usr/bin/env python3
import sys
import os
import datetime

TEMPLATES = {
    "buttons": """<div style="font-family: sans-serif; padding: 10px; display: flex; flex-direction: column; gap: 8px;">
  <p style="margin: 0 0 8px 0; font-size: 13px; color: #333; font-weight: 500;">{prompt}</p>
{buttons_html}
</div>""",
    "slider": """<div style="font-family: sans-serif; padding: 10px; display: flex; flex-direction: column; gap: 12px; font-size: 13px;">
  <p style="margin: 0; font-weight: bold; color: #333;">{prompt}</p>
  <div>
    <label style="display: block; margin-bottom: 6px; color: #555;">{label} (<span id="slider-val" style="font-weight: bold;">{val_default}</span>):</label>
    <input type="range" id="param-slider" min="{val_min}" max="{val_max}" value="{val_default}" style="width: 100%; cursor: pointer;" oninput="document.getElementById('slider-val').textContent=this.value">
  </div>
  <button onclick="respond(parseInt(document.getElementById('param-slider').value))" style="padding: 6px 12px; background: #e0a23c; border: none; border-radius: 4px; color: #1d1e1b; font-weight: bold; cursor: pointer; align-self: flex-start; font-family: monospace; font-size: 11px;">SUBMIT VALUE</button>
</div>""",
    "checkboxes": """<div style="font-family: sans-serif; padding: 10px; display: flex; flex-direction: column; gap: 12px; font-size: 13px;">
  <p style="margin: 0; font-weight: bold; color: #333;">{prompt}</p>
  <div style="display: flex; flex-direction: column; gap: 8px;">
{checkbox_items}
  </div>
  <button onclick="submitCheckboxes()" style="padding: 6px 12px; background: #e0a23c; border: none; border-radius: 4px; color: #1d1e1b; font-weight: bold; cursor: pointer; align-self: flex-start; font-family: monospace; font-size: 11px;">SUBMIT SELECTIONS</button>
</div>
<script>
function submitCheckboxes() {
  const selected = [];
  document.querySelectorAll('input[type="checkbox"]:checked').forEach(cb => {
    selected.push(cb.value);
  });
  respond(selected);
}
</script>""",
    "chart": """<div style="font-family: sans-serif; padding: 10px; display: flex; flex-direction: column; gap: 12px; font-size: 13px;">
  <p style="margin: 0; font-weight: 500; color: #333;">{prompt}</p>
  <svg viewBox="0 0 200 100" style="width: 100%; height: auto; border-bottom: 1px solid #ddd; background: #fdfdfd; padding: 10px 0;">
{chart_bars}
  </svg>
  <div style="display: flex; gap: 8px;">
    <button onclick="respond('approve')" style="flex: 1; padding: 7px; background: #6f9e6a; border: none; border-radius: 4px; color: white; font-weight: bold; cursor: pointer;">Approve Spec</button>
    <button onclick="respond('reject')" style="flex: 1; padding: 7px; background: #c2683f; border: none; border-radius: 4px; color: white; font-weight: bold; cursor: pointer;">Request Revision</button>
  </div>
</div>"""
}

def ask(question, default=""):
    prompt = f"{question} [{default}]: " if default else f"{question}: "
    val = input(prompt).strip()
    return val if val else default

def main():
    print("=== CCTV/Television Interactive Card Generator ===")
    print("This tool generates interactive cards with frontmatter and HTML structures.")
    print("-" * 50)

    # 1. Screen
    screen = ask("Screen name (e.g. demo, research, spec)", "demo")
    
    # 2. File ID / Name
    id_name = ask("Card ID / filename (e.g. 002-choice)", "002-checkpoint")
    if not id_name.endswith(".md"):
        id_name += ".md"

    # 3. Card Title
    title = ask("Card Title (e.g. Select risk framework)", "Checkpoint Decision")

    # 4. Prompt
    prompt = ask("Question or prompt for the user", "What action should the pipeline take next?")

    # 5. UI Type
    print("\nAvailable UI Types:")
    print("  1. buttons    - Multiple choice options shown as buttons")
    print("  2. slider     - Numeric range selector")
    print("  3. checkboxes - Select multiple options")
    print("  4. chart      - Simple SVG bar chart visualization + Approve/Reject action")
    
    ui_type = ""
    while ui_type not in ["1", "2", "3", "4", "buttons", "slider", "checkboxes", "chart"]:
        ui_type = ask("Select UI type (1-4)", "1").lower()
        if ui_type == "1": ui_type = "buttons"
        elif ui_type == "2": ui_type = "slider"
        elif ui_type == "3": ui_type = "checkboxes"
        elif ui_type == "4": ui_type = "chart"

    # Compile HTML body based on selected UI
    html_body = ""
    if ui_type == "buttons":
        raw_options = ask("Comma-separated list of button options", "Approve, Reject, Request changes")
        options = [o.strip() for o in raw_options.split(",") if o.strip()]
        btn_lines = []
        for opt in options:
            slug = opt.lower().replace(" ", "-")
            btn_lines.append(
                f"  <button onclick=\"respond('{slug}')\" style=\"padding: 8px 12px; border: 1px solid #ccc; border-radius: 6px; background: #fff; cursor: pointer; text-align: left; transition: background 0.1s; font-size: 12.5px;\" onmouseover=\"this.style.background='#f3f4f6'\" onmouseout=\"this.style.background='#fff'\"><strong>{opt}</strong></button>"
            )
        html_body = TEMPLATES["buttons"].format(prompt=prompt, buttons_html="\n".join(btn_lines))
    
    elif ui_type == "slider":
        label = ask("Slider Label (e.g. Temperature, Threshold)", "Threshold Value")
        val_min = ask("Minimum value", "0")
        val_max = ask("Maximum value", "100")
        val_default = ask("Default value", "50")
        html_body = TEMPLATES["slider"].format(
            prompt=prompt, label=label, val_min=val_min, val_max=val_max, val_default=val_default
        )
        
    elif ui_type == "checkboxes":
        raw_options = ask("Comma-separated checkbox options", "Option A, Option B, Option C")
        options = [o.strip() for o in raw_options.split(",") if o.strip()]
        cb_lines = []
        for i, opt in enumerate(options):
            slug = opt.lower().replace(" ", "-")
            cb_lines.append(
                f"    <label style=\"display: flex; align-items: center; gap: 8px; cursor: pointer;\"><input type=\"checkbox\" value=\"{slug}\" style=\"cursor: pointer;\"> {opt}</label>"
            )
        html_body = TEMPLATES["checkboxes"].format(prompt=prompt, checkbox_items="\n".join(cb_lines))

    elif ui_type == "chart":
        raw_data = ask("Comma-separated values for chart bars (e.g. 70,90,50)", "60,85,45")
        raw_labels = ask("Comma-separated labels for chart bars (e.g. Accuracy, Speed, Safety)", "Accuracy, Speed, Safety")
        data = [int(v.strip()) for v in raw_data.split(",") if v.strip()]
        labels = [l.strip() for l in raw_labels.split(",") if l.strip()]
        
        bars = []
        width = 30
        gap = 20
        start_x = 20
        for i, (val, label) in enumerate(zip(data, labels)):
            x = start_x + i * (width + gap)
            # map value 0-100 to height 0-80
            h = int(val * 0.8)
            y = 90 - h
            bars.append(f'    <rect x="{x}" y="{y}" width="{width}" height="{h}" fill="#e0a23c" rx="2" />')
            bars.append(f'    <text x="{x + width // 2}" y="{y - 5}" font-size="8" font-weight="bold" text-anchor="middle" fill="#333">{val}%</text>')
            bars.append(f'    <text x="{x + width // 2}" y="98" font-size="7" text-anchor="middle" fill="#666">{label}</text>')
        
        html_body = TEMPLATES["chart"].format(prompt=prompt, chart_bars="\n".join(bars))

    # Frontmatter
    import json
    frontmatter = f"""---
id: {os.path.splitext(id_name)[0]}
title: {json.dumps(title)}
type: interactive
status: blocked
updated: '{datetime.datetime.now().isoformat(timespec='seconds')}'
---
"""
    
    # Write file
    target_dir = os.path.join("_tv", "screens", screen)
    os.makedirs(target_dir, exist_ok=True)
    target_path = os.path.join(target_dir, id_name)
    
    with open(target_path, "w") as f:
        f.write(frontmatter + html_body + "\n")
        
    print(f"\n[Success] Created interactive card at: {target_path}")
    print("If your CCTV renderer server is running, the card will display instantly on the board!")

if __name__ == "__main__":
    main()

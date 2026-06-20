#!/usr/bin/env python3
import sys
import os
import json
import datetime

def ask(question, default=""):
    prompt = f"{question} [{default}]: " if default else f"{question}: "
    val = input(prompt).strip()
    return val if val else default

def create_card(filepath, card_id, title, card_type, status, stage, source, body):
    fm = [
        f"id: {card_id}",
        f"title: {title}",
        f"type: {card_type}",
    ]
    if status: fm.append(f"status: {status}")
    if stage is not None: fm.append(f"stage: {stage}")
    if source: fm.append(f"source: {source}")
    fm.append(f"updated: {datetime.datetime.now().isoformat(timespec='seconds')}")
    
    with open(filepath, "w") as f:
        f.write("---\n" + "\n".join(fm) + "\n---\n" + body + "\n")

def main():
    print("=== CCTV/Television Screen Setup Utility ===")
    print("This utility creates a set of screens populated with demo cards so you can see them on the board immediately.")
    print("-" * 65)
    
    raw_screens = ask("Enter comma-separated screen names to create", "01-research, 02-spec, 03-review")
    screens = [s.strip() for s in raw_screens.split(",") if s.strip()]
    
    for i, s in enumerate(screens):
        stage_num = i + 1
        d = os.path.join("_tv", "screens", s)
        os.makedirs(d, exist_ok=True)
        print(f"\nSetting up screen: {s}...")
        
        # 1. Create a Welcome/Status card
        create_card(
            os.path.join(d, "001-welcome.md"),
            "001-welcome",
            f"Stage {stage_num}: Welcome",
            "card",
            "done" if stage_num < len(screens) else "running",
            stage_num,
            None,
            f"This is the welcome card for **{s}**.\n\nThe status of this stage is currently marked as **{'done' if stage_num < len(screens) else 'running'}**."
        )
        
        # 2. Create an Interactive Checkpoint card
        create_card(
            os.path.join(d, "002-checkpoint.md"),
            "002-checkpoint",
            "Interactive Checkpoint",
            "interactive",
            "blocked" if stage_num == len(screens) else "done",
            stage_num,
            None,
            f"""<div style="font-family: sans-serif; padding: 10px; font-size: 13px;">
  <p style="margin: 0 0 10px 0; font-weight: bold; color: #333;">Choose the focus area for {s}:</p>
  <div style="display: flex; flex-direction: column; gap: 8px;">
    <button onclick="respond('focus-speed')" style="padding: 8px; border: 1px solid #ccc; border-radius: 4px; background: white; text-align: left; cursor: pointer; font-size: 12px;" onmouseover="this.style.background='#f3f4f6'" onmouseout="this.style.background='white'">🚀 <strong>Speed Optimization</strong></button>
    <button onclick="respond('focus-quality')" style="padding: 8px; border: 1px solid #ccc; border-radius: 4px; background: white; text-align: left; cursor: pointer; font-size: 12px;" onmouseover="this.style.background='#f3f4f6'" onmouseout="this.style.background='white'">🛡️ <strong>Quality & Safety</strong></button>
  </div>
</div>"""
        )
        
        # 3. Create a stage output card linking to a source
        create_card(
            os.path.join(d, "003-output.md"),
            "003-output",
            "Stage Output Summary",
            "card",
            "done" if stage_num < len(screens) else None,
            stage_num,
            "README.md",
            f"This card represents the final outputs of **{s}**. Click the *edit output* button in the footer to edit the workspace's `README.md` file directly!"
        )
        
        # 4. Create _layout.json
        layout = {
            "001-welcome": {"x": 24, "y": 24, "w": 332, "h": 232, "z": 0, "pinned": True},
            "002-checkpoint": {"x": 380, "y": 24, "w": 332, "h": 232, "z": 1, "pinned": False},
            "003-output": {"x": 736, "y": 24, "w": 332, "h": 232, "z": 2, "pinned": False}
        }
        with open(os.path.join(d, "_layout.json"), "w") as lf:
            json.dump(layout, lf, indent=2)
            
        print(f" -> Created directory _tv/screens/{s}/")
        print(f" -> Created cards: welcome, checkpoint, output")
        print(f" -> Created _tv/screens/{s}/_layout.json")

    print("\n" + "=" * 65)
    print("All screens created successfully!")
    print("Open http://localhost:4321 in your browser to view your new board tabs!")

if __name__ == "__main__":
    main()

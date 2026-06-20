#!/usr/bin/env python3
import sys
import os
import datetime

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/steer.py <left|right|straight>")
        print("Example: python3 scripts/steer.py left")
        sys.exit(1)

    direction = sys.argv[1].lower().strip()
    if direction not in ["left", "right", "straight"]:
        print("Error: Invalid steering direction. Choose 'left', 'right', or 'straight'.")
        sys.exit(1)

    filepath = "_tv/screens/gta-chase/003-command.md"
    
    # Generate fresh ISO timestamp to trigger change detection in the canvas iframe
    now_str = datetime.datetime.now().isoformat(timespec='seconds')
    
    frontmatter = f"""---
id: 003-command
title: Active Telemetry & Command
type: card
status: running
updated: '{now_str}'
---
"""

    try:
        with open(filepath, "w") as f:
            f.write(frontmatter + direction + "\n")
        print(f"[Steer] Successfully wrote '{direction.upper()}' to {filepath}")
    except Exception as e:
        print(f"Error writing to steering file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

---
name: screen-layout-setup
description: Help users setup a set of screens within the _tv directory structure and generate dummy cards so they can see the layout immediately in the browser.
---

# Screen Layout Setup Skill

This skill helps you initialize a set of screens inside the `_tv/screens/` directory structure. Users can define the stages of their pipeline, and this skill will generate screens and fill them with placeholder/dummy cards so they can see how it looks on the board immediately.

## Screen Directory Structure

Screens are stored under `_tv/screens/<screen_name>/`:

- `_tv/screens/research/`
- `_tv/screens/spec/`
- `_tv/screens/review/`

Each screen contains:
- Card files (`001-card.md`, `002-checkpoint.md`)
- A layout config file (`_layout.json` - containing card coordinates, sizes, and z-index)

## Helper Script
You can use the built-in initializer script to quickly setup a set of screens:
```bash
python3 .agents/skills/screen-layout-setup/scripts/setup_screens.py
```

## Running the Setup
When triggering this skill, the agent will:
1. Ask the user for the names of the screens they want to build (e.g. `research, design, spec`).
2. Create folders under `_tv/screens/` for each name.
3. Write demo card `.md` files in each screen to simulate different stages:
   - A welcome/instructions card.
   - An active status card (showing a pulsing yellow dot).
   - An interactive checkpoint card (type: `interactive` with options).
   - A final output card (type: `card`, status: `done`).
4. Generate a default `_layout.json` to organize the cards cleanly in a grid on the board.

# ICM CCTV

A glass-box visual canvas for [ICM](https://github.com/RinDig/Interpreted-Context-Methdology)
agent pipelines. A starter, not a product.

> [!TIP]
> **New to ICM CCTV?** Check out the comprehensive, step-by-step [USER-GUIDE.md](file:///Users/munron/icm-television/USER-GUIDE.md) to learn how to configure layouts, build custom forms, and organize multi-screen pipelines!


**The one idea to hold onto:** the agent does not watch files. The *renderer*
watches files. The agent only ever writes them.

```
  agent writes _tv/screens/<screen>/<id>.md
        │
        ▼
  chokidar (in server.js) sees the change
        │
        ▼
  renderer pushes new state over WebSocket
        │
        ▼
  the board in your browser re-renders
```

This is the same filesystem-as-interface idea ICM already uses for control
flow — here it drives presentation instead. ICM decides *what the agent does*;
this decides *what you see*. Both halves meet on plain files.

## 🗺️ How it Works: The Baseline

By default, everything on the dashboard is driven by **plain Markdown (`.md`) files** inside the `_tv/screens/` directory. This is the fundamental starting point:
1. **Tabs**: Every subfolder under `_tv/screens/` forms a tab in the header (e.g. `_tv/screens/demo/` is the "demo" tab).
2. **Cards**: Every `.md` file inside a tab's subfolder is rendered as a visual card on the board.
3. **No Code Needed**: Your agent or you can write standard text and formatting.

## 🎛️ Adding HTML (Optional)

You only need to use HTML in two specific cases:
1. **Custom Styling**: If standard Markdown formatting is insufficient for your layout.
2. **Interactivity (Checkpoints)**: If you need simple controls (like buttons, sliders, or forms) to send input back to the agent.
   - An interactive card uses `type: interactive` in its frontmatter.
   - You include simple HTML controls that call the global `respond(value)` function on user action.
   - This writes the selected value to `_tv/responses/<screen>/<id>.md` which the agent reads to resume execution.

---

## 🚀 Advanced Features & Examples (Optional)

To show what is possible if your pipeline requires it, CCTV includes several optional tools and advanced examples:

* **🏎️ GTA Chase Simulation (`gta-chase` tab)**: A sophisticated canvas-based car chase demonstrating real-time interactive telemetry. The getaway car turns at the next grid junction when direction values are written to `003-command.md` (via clicking on-screen buttons, using arrow keys, or running `python3 scripts/steer.py <left|right|straight>` in the terminal).
* **☁️ Cloud-Native Previews**: Paste the instructions in [CLAUDE-CCTV-INSTRUCTIONS.md](file:///Users/munron/icm-television/CLAUDE-CCTV-INSTRUCTIONS.md) to Claude or Gemini to let them self-generate and preview entire board layouts inside their chat interfaces. You can also run `python3 scripts/export_react.py` or `python3 scripts/export_html.py` to export your current local board to the cloud.
* **🎮 Interactive Guide & Playground (`00-guide` tab)**: A built-in sandbox showing SVG metric charts, range sliders, and wizards to automatically calculate layout coordinate blocks for `_layout.json`.
* **🛠️ CLI Helper Scripts**: Python scripts to bootstrap layout coordinates (`python3 scripts/setup_screens.py`) and generate interactive cards (`python3 scripts/generate_card.py`).

---

## Ownership (why nothing gets clobbered)

| File | Owner | Holds |
|------|-------|-------|
| `_tv/screens/<screen>/<id>.md` | the agent | artifact content + metadata |
| `_tv/screens/<screen>/_layout.json` | renderer + human | positions, sizes, pins |

Different files, so an agent rewriting content and a human dragging a card
never touch the same bytes.

## Run it

```bash
npm install
npm start          # renderer host on http://localhost:4321
```

Running `npm start` automatically compiles the Tailwind CSS stylesheet and copies source assets.

Open the page, then edit any file under `_tv/screens/demo/` — the card updates
live. Drag cards to rearrange; layout persists.

## Wire it to an ICM workspace

1. Copy `_tv/` and `server.js` + `public/` into (or beside) your workspace.
2. Drop `skill/SKILL.md` where your agent loads skills, and reference it from
   `CLAUDE.md` so the agent knows the emit contract.
3. Add the emit step to each stage's `CONTEXT.md` — see
   `icm-glue/STAGE-CONTEXT.example.md`. Stages already write to `output/`;
   you're adding one line that also writes a board card pointing at it.

Now the board is a live map of pipeline state, and ICM checkpoints become
interactive cards the human answers instead of chat prompts.

## Editing from the board

Cards are an edit surface, not just a display:

- Click a card body to edit it; saving writes the card's own `.md` file.
- A card with a `source:` shows **edit output**, which opens the real ICM
  output file and saves back to it. This is ICM's "every output is an edit
  surface" made literal — you revise what the next stage reads, from the board.

**Interactive checkpoints answer back.** Inside a `type: interactive` card,
call `respond(value)` (or `respond({...})`). It writes to a caged location,
`_tv/responses/<screen>/<id>.md`, which the agent reads on resume. The card
supplies the value, never the path — so a checkpoint is a button you click, not
a file you go hunt down.

The board itself only ever writes layout, card files, and output files you
explicitly edit. Concurrency is ICM's model: sequential, human-in-the-loop,
last-write-wins. You edit between stages, so nothing collides.

### Board Styles & Themes

The board supports two stylesheets, switchable via the **Style** button in the header:
- **Classic**: The original warm-paper/slate style.
- **Tailwind**: A modern terminal-like dark theme using Tailwind CSS v4 and `tw-animate-css`. Your choice is saved to `localStorage` and persists across page refreshes.

## Where it can run

- **Claude Code / Codex / OpenCode (local).** Full live loop. The agent writes
  files on your machine; the renderer runs alongside. This is the real target.
- **Claude.ai chat.** Can't run the live loop — the chat agent has no
  persistent shell on your machine and you can't open a watcher in your browser.
  But the *presentation layer* ports natively to a Claude Artifact (see the
  companion artifact). Pattern: **build here, run there.**
- **Claude Cowork / Claude Code in the app.** Can run the local loop on a
  connected machine.

## Security notes (don't skip)

- `type: interactive` cards run agent-authored HTML in a `sandbox="allow-scripts"`
  iframe with no same-origin access. Keep it that way.
- The layout/content/file endpoints are unauthenticated and meant for
  localhost only. Don't expose the renderer to a network without adding auth.
- `/api/file` is restricted two ways: it only serves text extensions
  (`.md .markdown .txt .csv`) and any path that resolves outside the workspace
  root is refused. Both guards are enforced server-side.
- `/api/respond` ignores any path the card suggests and always writes to
  `_tv/responses/<screen>/<id>.md`, with screen/id slugged so `..` cannot
  traverse. The board only reacts to `respond()` messages from its own iframes.

## Optional: MCP instead of a skill

The skill approach keeps files canonical and portable. If a harness prefers
typed tools, wrap `create_artifact` / `update_artifact` in an MCP server **over
the same files**. Files stay the source of truth; MCP is just a nicer door.

## CLI Helper Tools

To assist non-technical users and agents in setting up the board, the repository includes two Python scripts:

1. **Interactive Card Builder**:
   - Run `python3 scripts/generate_card.py`
   - Dynamically constructs `type: interactive` cards with choice buttons, numeric range sliders, checklists, or SVG bar charts.

2. **Screen Layout Setup**:
   - Run `python3 scripts/setup_screens.py`
   - Automatically provisions new pipeline screen folders under `_tv/screens/` and populates them with welcome, checkpoint, and output summary placeholders, pre-aligned in a clean layout.

Apache 2.0.

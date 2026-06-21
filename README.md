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

## 🔄 The ICM to CCTV Data Loop

> [!IMPORTANT]
> **CCTV is an Optional Visual Layer**
> The interpreted context methodology (ICM) pipeline runs as normal, using standard stage folders (like `stages/01-research/output/`) as the source of truth for all pipeline files. **CCTV is simply a visual addition.** It watches files and mirrors them for display, or writes interactive response files for the agent to resume. The pipeline does not require CCTV to run.

The connection between your standard ICM stages and CCTV is driven entirely by files:
1. **AI Output & Visual Mirroring**: An ICM stage runs and writes its primary output to its standard stage folder (e.g. `stages/01-research/output/sources.md`). It *also* emits a corresponding `.md` card under `_tv/screens/01-research/001-findings.md` pointing to that source file, allowing the browser to render it.
2. **User Direct-Edits (Case B)**: If the user edits the findings card on the CCTV board, the edit is saved directly back to the standard ICM file (`stages/01-research/output/sources.md`) because the card frontmatter links to it. The next stage reads this updated file.
3. **User Interactive Responses (Case C)**: For decisions, CCTV writes a response file to `_tv/responses/02-spec/002-checkpoint.md`. The next stage reads this response file to resume execution.

Here are the directory structures showing where changes occur for each case, showing the standard ICM folders alongside the optional CCTV visual folder:

### 📁 Case A: AI Stage Outputs a Card (Stage Output)
When the AI agent runs Stage 1 (Research), it writes its standard pipeline output file (`sources.md`). To display this on the CCTV board, it *also* writes a card file under `_tv/screens/01-research/` linking to the source.

```
workspace/
├── stages/                         <-- Standard ICM Pipeline Folder
│   └── 01-research/
│       └── output/
│           └── sources.md          <-- [WRITTEN BY AI] Standard stage output file (source of truth)
└── _tv/                            <-- Optional Visual CCTV Folder
    └── screens/
        └── 01-research/
            ├── 001-findings.md     <-- [WRITTEN BY AI] CCTV card file (links to sources.md)
            └── _layout.json        <-- Position layout coordinates for the card
```

---

### 📁 Case B: User Direct-Edits Card Text
If the user wants to revise findings before starting the next stage, they click the card body on the board and edit the text. CCTV writes these changes directly back to the standard ICM file (`sources.md`) in the stages folder.

```
workspace/
├── stages/                         <-- Standard ICM Pipeline Folder
│   └── 01-research/
│       └── output/
│           └── sources.md          <-- [UPDATED BY BROWSER] Standard ICM output file edited by user
└── _tv/                            <-- Optional Visual CCTV Folder
    └── screens/
        └── 01-research/
            └── 001-findings.md     <-- CCTV card file (mirrors updated sources.md)
```

---

### 📁 Case C: User Interactive Response (Checkpoint)
When Stage 2 starts, the AI reads the findings from `sources.md`, writes a checkpoint card (`002-checkpoint.md`), and pauses. When the user clicks a button (e.g. "Approve"), the browser writes a response file to `_tv/responses/`. Once approved, Stage 2 resumes, consumes the response, and writes the standard ICM spec output.

```
workspace/
├── stages/                         <-- Standard ICM Pipeline Folder
│   └── 02-spec/
│       └── output/
│           └── spec.md             <-- [WRITTEN BY AI ON RESUME] Standard stage output file
└── _tv/                            <-- Optional Visual CCTV Folder
    ├── screens/
    │   └── 02-spec/
    │       ├── 001-spec.md         <-- CCTV card file (links to spec.md)
    │       └── 002-checkpoint.md   <-- CCTV checkpoint card with interactive buttons
    └── responses/
        └── 02-spec/
            └── 002-checkpoint.md   <-- [WRITTEN BY BROWSER] User response payload (e.g., "approve")
```

---

### 🔄 The Step-by-Step Flow:
1. **Standard Run**: The agent runs a stage and writes outputs to `stages/<stage>/output/` as normal.
2. **Emit Mirror**: The agent writes cards to `_tv/screens/<stage>/` (linking to output files) to display them.
3. **Block**: For human decisions, the agent writes a card with `type: interactive` and `status: blocked` to CCTV, and finishes its turn.
4. **Edit/Respond**: 
   - Either the user clicks and direct-edits a card (Case B), which updates the file in `stages/<stage>/output/`.
   - Or the user clicks an interactive control button, which writes a file to `_tv/responses/<stage>/<id>.md` (Case C).
5. **Resume**: The user prompts the agent to continue. The agent reads the updated output or the response file, processes it, and runs the next stage, emitting the next screen's cards.

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

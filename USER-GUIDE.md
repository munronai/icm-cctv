# ICM CCTV User Guide 📺

Welcome! **ICM CCTV** is a visual dashboard for watching and interacting with AI agent pipelines. 

Because CCTV is built on the **filesystem-as-interface** principle, you don't need databases, complex APIs, or React. To build a board, you or your agent only write standard text files to folders.

---

## 🎯 The Baseline: Plain Markdown Cards (`.md`)

By default, every card on your board is just a **plain Markdown (`.md`) file**. This is the fundamental starting point:
1. **Tabs**: Every subfolder under `_tv/screens/` renders as a tab in the header.
2. **Cards**: Every `.md` file inside a screen folder renders as a card.
3. **Writing**: You can write standard text, tables, headers, and bullet points. No code required.

```
_tv/
└── screens/
    └── demo/                  <-- A tab in your browser named "demo"
        ├── 001-welcome.md     <-- A standard text card
        ├── 002-status.md      <-- Another standard text card
        └── _layout.json       <-- Generated automatically when you drag/resize cards
```

---

## 🎛️ Adding HTML (Only When Necessary)

You only need to write HTML in two cases:
1. **Custom Formatting**: When Markdown's styling is insufficient (e.g. you want custom colors, grids, or inline visuals).
2. **Interactive Checkpoints**: When you need simple controls (like buttons, range sliders, or radio selectors) to send input back to the agent.
   - Set `type: interactive` and `status: blocked` in the card frontmatter.
   - Use simple HTML controls inside the card that call `respond(value)` when clicked.
   - The selected choice writes to `_tv/responses/<screen>/<id>.md`. The agent reads this file to resume.

---

## 🧠 Custom Agent Skills & Wizards

To make building boards and cards easy, CCTV provides both web-based wizards in the dashboard and optional terminal helper scripts:

> [!TIP]
> **No Python? Use the Wizards!**
> The `00-guide` tab in the web dashboard includes an interactive **Card UI Wizard** and a **Screen Wizard**. Use these if you don't want to run python scripts or you want to understand how it works under the hood. They let you design cards with basic HTML controls and adjust screen layouts directly in your browser.

### 1. Interactive Card Builder (`scripts/generate_card.py`)
- **What it does**: Runs in the terminal and guides you step-by-step to create interactive cards. It generates the correct frontmatter and HTML templates for buttons or sliders.
- **Command**: `python3 scripts/generate_card.py`

### 2. Screen Layout Setup (`scripts/setup_screens.py`)
- **What it does**: Initializes a directory structure with layout coordinates and demo cards so you can see a new stage screen immediately.
- **Command**: `python3 scripts/setup_screens.py`

---

## 🎨 Layout Design Patterns

You can arrange screens and cards in different layouts depending on your pipeline requirements.

### Pattern 1: The 2-Card Side-by-Side Pattern (Recommended)
Instead of forcing the user to switch tabs, you can put the **Data** and the **Decision UI** side-by-side on the same screen.

```
┌────────────────────────────────────────────────────────┐
│  [02-spec] Tab                                         │
│                                                        │
│  ┌─────────────────────────┐  ┌─────────────────────┐  │
│  │ Spec Draft (Card 1)     │  │ Decision (Card 2)   │  │
│  │                         │  │                     │  │
│  │ - Accuracy threshold    │  │ [ Approve Spec ]    │  │
│  │ - Refinement limit      │  │ [ Request Revision] │  │
│  │                         │  │                     │  │
│  └─────────────────────────┘  └─────────────────────┘  │
└────────────────────────────────────────────────────────┘
```

To build this, write two files to the same screen folder:
1. **`001-spec-data.md`** (`type: card`): Standard card with tabular or text information.
2. **`002-action.md`** (`type: interactive`): An interactive card with buttons that trigger `respond(...)`.

By positioning these at coordinates `x: 24` and `x: 380` inside `_layout.json`, the user gets a seamless interface where they view information and act on the same tab!

---

### Pattern 2: Multi-Screen Stages (Data vs. Chart)
If a single stage has too much information to fit comfortably on one screen, you can create multiple screens (tabs) for that stage:

Create two screen folders:
1. `_tv/screens/01-research-tables/` — for lists of source papers and text summaries.
2. `_tv/screens/01-research-charts/` — for visual charts showing data distributions.

---

### Pattern 3: Real-Time Simulation Control (GTA Chase Demo)
You can design active playgrounds where cards interact with each other in real-time. On the `gta-chase` screen:
- **`001-chase.md`** (`type: interactive`): The canvas game drawing the vehicles and running the simulation loop.
- **`002-control.md`** (`type: interactive`): Buttons that send input signals (left, right, straight).
- **`003-command.md`** (`type: card`): Serves as the steering file. Both button clicks and the terminal command `python3 scripts/steer.py <left|right|straight>` rewrite this file, triggering WebSocket pushes that instruct the getaway car.

By positioning these in two parallel columns (`_layout.json`), you get a dashboard that acts as a real-time command console.

---

### Pattern 4: Cloud-Native Presentation (Claude & Gemini Artifacts)
If you do not want to run a local dev server, you can render a mock CCTV dashboard directly in the cloud chat pane:
- **Claude**: Renders raw React components (`Board.jsx`) natively in its **Artifacts** pane. Run `python3 scripts/export_react.py` to compile your current screen states, and paste it to Claude.
- **Gemini**: Renders HTML/JS files (`Board.html`) natively inside its **Code Preview** panel. Run `python3 scripts/export_html.py` to compile your screens, and paste the HTML code to Gemini.
- **Auto-Generation**: Provide the instructions in [CLAUDE-CCTV-INSTRUCTIONS.md](file:///Users/munron/icm-television/CLAUDE-CCTV-INSTRUCTIONS.md) to the AI's instructions. When you ask the AI to write documents (e.g. specs, summaries), it will automatically wrap them into cards and display the visual dashboard live in the chat!

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

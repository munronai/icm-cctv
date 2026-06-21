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

## 🧠 Custom Agent Skills

To make building boards and cards easy, the project includes two optional helper scripts:

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

## 🤝 How Your AI Agent Interacts

When your agent runs a stage:
1. It reads the files in your workspace to understand current context.
2. It writes cards to `_tv/screens/<stage>/` to display its status, research findings, or checkpoints.
3. If it hits an interactive checkpoint, it writes a `type: interactive` file with `status: blocked`, and finishes its turn.
4. You click a button in your browser, which writes your response to `_tv/responses/<stage>/<id>.md`.
5. You tell the agent in chat to continue.
6. The agent reads `_tv/responses/<stage>/<id>.md` and resumes!

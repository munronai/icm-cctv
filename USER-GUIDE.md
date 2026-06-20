# ICM CCTV User Guide 📺

Welcome! **ICM CCTV** is a visual dashboard for watching and interacting with AI agent pipelines. 

Because CCTV is built on the **filesystem-as-interface** principle, you don't need to write complex React code or databases. To change what is on the board, you or your agent only need to write simple Markdown files to folders.

This guide will teach you how to set up layouts, build interactive buttons/inputs, and organize your screens.

---

## 🚀 Quick Start (Try it in 30 seconds)

1. Make sure your server is running:
   ```bash
   npm start
   ```
2. Open [http://localhost:4321](http://localhost:4321) in your browser.
3. In a terminal, run the screen initializer script:
   ```bash
   python3 scripts/setup_screens.py
   ```
   *Enter screen names (like `01-ingest, 02-process`), and watch the tabs appear live in your browser!*
4. Toggle the stylesheet switcher on the top right to swap between the **Classic** paper style and the dark **Tailwind** console style.

---

## 📂 Understanding the Folder Structure

Everything on the dashboard is driven by files inside the `_tv/` directory:

```
_tv/
├── screens/
│   ├── demo/                  <-- A tab in your browser named "demo"
│   │   ├── 001-welcome.md     <-- A card on the board
│   │   ├── 002-status.md      <-- Another card on the board
│   │   └── _layout.json       <-- Generated automatically when you drag cards
└── responses/
    └── demo/
        └── 002-status.md      <-- Where clicked button values land
```

- **Directories under `_tv/screens/`** are rendered as **tabs** in the top navigation bar.
- **`.md` files** in those directories are rendered as **cards** on the board.
- **`_layout.json`** is managed by the browser. When you drag or resize cards on the screen, it automatically saves their coordinates. Your agent will never overwrite your layout!

---

## 🧠 Using Custom Agent Skills

To make building boards and cards easy, the project includes two pre-packaged AI skills. These work in **Antigravity**, **Claude Code**, and **Codex** (documented in [skill/SKILL.md](file:///Users/munron/icm-television/skill/SKILL.md)):

### 1. Interactive Card Builder (`scripts/generate_card.py`)
- **What it does**: Runs in the terminal and guides you step-by-step to create interactive cards. It generates the correct frontmatter and HTML tags for buttons, forms, and charts.
- **Command**:
  ```bash
  python3 scripts/generate_card.py
  ```

### 2. Screen Layout Setup (`scripts/setup_screens.py`)
- **What it does**: Initializes a directory structure with layout parameters and demo templates so you can visualize a new stage pipeline immediately.
- **Command**:
  ```bash
  python3 scripts/setup_screens.py
  ```

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

## 🤝 How Your AI Agent Interacts

When your agent runs a stage:
1. It reads the files in your workspace to understand current context.
2. It writes cards to `_tv/screens/<stage>/` to display its status, research findings, or checkpoints.
3. If it hits an interactive checkpoint, it writes a `type: interactive` file with `status: blocked`, and finishes its turn.
4. You click a button in your browser, which writes your response to `_tv/responses/<stage>/<id>.md`.
5. You tell the agent in chat to continue.
6. The agent reads `_tv/responses/<stage>/<id>.md` and resumes!

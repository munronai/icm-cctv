# CCTV — artifact emit skill

You can pin information to a visual board the human is watching, instead of
losing it in chat. You do this **only by writing files**. A separate renderer
process watches those files and draws them. You never read the renderer, start
a server, or poll anything.

## How to create or update an artifact

Write a markdown file to `_tv/screens/<screen>/<id>.md`. Use a short numeric
prefix for ordering (`001-`, `002-`). Re-writing the same path updates the card.

```
---
id: 002-research          # optional; defaults to filename
title: Gather sources     # card header
type: card                # card | interactive | url
stage: 1                  # optional — shows a "stage N" badge
status: running           # optional — running | done | blocked (colors the dot)
source: stages/01-research/output/sources.md   # optional — the file this represents
---
Body in markdown. Headings, **bold**, `code`, lists, and links render.
```

- `type: card` — body is markdown.
- `type: url` — body's first line is a URL; it embeds as a live page.
- `type: interactive` — body is HTML; it runs sandboxed (scripts allowed, no
  network/same-origin). Use for checkpoints, choices, small dashboards.

## Rules

1. **Never write `_layout.json`.** That file is owned by the human and the
   renderer (positions, pins). If you touch it you will fight the human's drags.
2. **One artifact per meaningful thing.** A stage's output, a decision, a status
   — not every sentence.
3. **Update in place.** To change a card, rewrite its file at the same path.
   To remove one, delete the file.
4. **Point at the real file.** When an artifact represents pipeline output, set
   `source:` to the output path so the card footer links back to it.

## When to emit (ICM)

At the **end of each stage**, write one artifact summarizing that stage's
output, with `stage`, `status: done`, and `source` set to the output file.
When you hit a **checkpoint**, write a `type: interactive` artifact describing
the choice and where to write the answer, set `status: blocked`, and stop.

## Humans can edit from the board now

Cards are a live edit surface, not just a view:

- Editing a card's text saves to that card's own `.md` file.
- A card with a `source:` shows an **edit output** control that opens the real
  ICM output file (e.g. `stages/01-research/output/sources.md`) and saves back
  to it — so the human can revise what the next stage reads, from the board.

What this means for you, the agent:

1. **Content is co-owned, last-write-wins.** When you re-emit an artifact at the
   end of a stage, you overwrite whatever was there. That's expected — a stage
   run produces fresh output.
2. **Respect the sequence.** Edit files only during your stage. The human edits
   between stages. As long as the pipeline stays sequential (ICM's whole model),
   you and the human never write the same file at the same moment.
3. **If you must preserve a human edit, read before you write.** Read the
   current file, fold the human's change in, then write — don't blind-overwrite.

## Interactive cards can answer you back (respond bridge)

Inside a `type: interactive` card, a global `respond(value)` is available.
Calling it writes the value to `_tv/responses/<screen>/<id>.md` — a fixed,
caged location. The card supplies only the value, never the path.

```html
<button onclick="respond('use-case-first')">use-case-first</button>
<!-- value can also be an object: respond({choice:'tier-first', note:'...'}) -->
```

So a checkpoint becomes a real choice the human clicks, not a "go edit a file"
instruction. On resume, **read `_tv/responses/<screen>/<id>.md`** to get the
answer, then continue the stage. An optional `window.onResponded(e)` fires in
the card after a successful write, so you can show a confirmation.

## CLI Helper Scripts for Humans and Agents

The project contains two utility CLI scripts to make creating cards and screens straightforward for humans and agents alike:

1. **Interactive Card Builder**:
   - Run `python3 scripts/generate_card.py` in the terminal.
   - It guides you step-by-step to generate cards with buttons, numeric range sliders, checklists, or SVG bar charts.

2. **Screen Layout Setup**:
   - Run `python3 scripts/setup_screens.py` in the terminal.
   - It quickly initializes a directory structure with layout parameters and demo templates so you can see your layout immediately in the browser.


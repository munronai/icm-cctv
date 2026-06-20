#!/usr/bin/env python3
"""Emit a CCTV artifact. Optional convenience — the agent can also just
write the file directly. Never writes _layout.json.

  python emit_artifact.py --screen run1 --id 02-spec --title "Write spec" \
      --stage 2 --status done --source stages/02-spec/output/spec.md \
      --body "Drafted the classifier spec."
"""
import argparse, os, datetime

p = argparse.ArgumentParser()
p.add_argument("--root", default=".")
p.add_argument("--screen", required=True)
p.add_argument("--id", required=True)
p.add_argument("--title", required=True)
p.add_argument("--type", default="card", choices=["card", "interactive", "url"])
p.add_argument("--stage")
p.add_argument("--status", choices=["running", "done", "blocked"])
p.add_argument("--source")
p.add_argument("--body", default="")
a = p.parse_args()

d = os.path.join(a.root, "_tv", "screens", a.screen)
os.makedirs(d, exist_ok=True)

fm = [f"id: {a.id}", f"title: {a.title}", f"type: {a.type}"]
if a.stage:  fm.append(f"stage: {a.stage}")
if a.status: fm.append(f"status: {a.status}")
if a.source: fm.append(f"source: {a.source}")
fm.append(f"updated: {datetime.datetime.now().isoformat(timespec='seconds')}")

path = os.path.join(d, f"{a.id}.md")
with open(path, "w") as f:
    f.write("---\n" + "\n".join(fm) + "\n---\n" + a.body + "\n")
print(f"wrote {path}")

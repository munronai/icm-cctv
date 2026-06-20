# Stage 02 — Write classifier spec

This is a normal ICM stage contract with one addition: a final step that emits
a CCTV artifact. The only new line in Process is step 6, and the only new
row is the artifact in Outputs. Everything else is stock ICM.

## Inputs
| Source | File/Location | Section/Scope | Why |
|--------|--------------|---------------|-----|
| Previous stage | ../01-research/output/ | Full file | Source material |
| Voice rules | ../../_config/voice-rules.md | Voice section | Tone |
| TV skill | ../../skill/SKILL.md | Full file | How to emit an artifact |

## Process
1. Read the research output.
2. Identify the risk-tier framing.
3. Write the spec following voice-rules.
4. At the framing decision, emit a `type: interactive` checkpoint artifact
   (`status: blocked`) and stop until the human writes `output/decision.md`.
5. Run the stage audit.
6. **Emit artifact:** write `_tv/screens/<run>/02-spec.md` with `stage: 2`,
   `status: done`, and `source: stages/02-spec/output/spec.md`.
7. Save the spec to `output/`.

## Outputs
| Artifact | Location | Format |
|----------|----------|--------|
| Spec | output/spec.md | Markdown |
| Board card | _tv/screens/<run>/02-spec.md | CCTV artifact |

## Checkpoints
- Risk framing: tier-first vs use-case-first vs obligation-first.

## Audits
- [ ] Every risk tier maps to a named Article obligation.
- [ ] No tier defined in more than one place (canonical source).

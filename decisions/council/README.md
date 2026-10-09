# Council Decisions

Permanent records of the **strategic, cross-functional calls** the council makes. Each file is a *verdict* — what we decided and why — not a transcript of the deliberation.

## How this directory works

- One file per decision. Numbered sequentially: `001-<slug>.md`, `002-<slug>.md`, etc.
- A council file is the **synthesis** the main agent writes after the lenses have reasoned. The per-agent perspective files stay in `.council-temp/` and are deleted with the session — only the synthesis is promoted here. See `AGENTS.md` → Workflow 1.
- Council files are committed to git and **never rewritten after acceptance**. To change a decision, run a new council and write a new file that supersedes the old one.
- Keep the synthesis short — a verdict doc, not a record of the debate. Use the structure in `.council-temp/README.md`.

## When to write a council decision

Write one when the question is **strategic, cross-functional, or would change a living document** — pricing, kill/pivot/re-sequence calls, positioning, or any change to the PRD, roadmap, architecture, or brand docs. Do not convene the council for single-feature pitches (use a PR/FAQ) or tech-only choices (use an ADR).

## File shape (summary)

```markdown
# Council: <short topic title>

**Date**: YYYY-MM-DD
**Lenses**: <comma-separated list of lenses that ran>
**Status**: Decided

## Decision
## Sequence        (omit if the decision is atomic)
## Why
## Open Issues     (omit if nothing is unresolved)
## Action Items
```

## Index

<!-- New council decisions are appended here as they're created. -->

- [001](001-hackathon-mvp-scope.md) — 24-hour Hack4Vilnius MVP scope — Superseded by 002
- [002](002-rescope-to-challenge-brief.md) — Re-scope the MVP to the official challenge brief — Decided, amended by 003
- [003](003-walk-mate-3d-and-languages.md) — Walk-Mate with the 3D preview, the assistant as a main way in, EN and LT — Decided
- [004](004-walk-slots-business.md) — Walk slots are the business — Decided
- [005](005-mvp-rethink.md) — MVP re-think after the challenger and mentor feedback — Decided

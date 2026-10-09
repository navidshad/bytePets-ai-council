# BytePets AI Council

A reusable framework for running an **AI product council** over a living-docs repo. A small team of AI agents helps you make decisions and write them down, so the *why* behind every choice is saved and easy to find.

This repo holds the product docs and decisions for **BytePets**, our Hack4Vilnius (Challenge #6) entry.

## Works with

The same workflow files drive more than one agent tool, so the council runs the same way whichever you use:

- **Claude Code** — the personas spawn as parallel `Task` subagents from `agents/*.md`. See `CLAUDE.md`.
- **Gemini CLI** — the personas are native subagents in `.gemini/agents/*.md` (call them, or force one with `@product-manager`). See `GEMINI.md`.
- **Antigravity** and **Cursor** — read `AGENTS.md` + the persona files directly; spawn each lens as its own agent. See `GEMINI.md`.

`AGENTS.md` is the shared source of truth for every tool. The per-tool files (`CLAUDE.md`, `GEMINI.md`) only add *how to spawn agents* in that tool — they add no new rules. If you change a persona, update both `agents/<role>.md` and its Gemini mirror `.gemini/agents/<role>.md` so all tools stay in sync.

## The council

The council is four AI agents. Each one looks at a question from one angle:

- **Product Manager** — what to build, and in what order
- **UX Designer** — how the product looks and feels to use
- **Technical Architect** — how to build it, and if it is possible
- **Business Strategist** — money, pricing, and how to grow

When you ask the council something, each agent gives its own view on its own. Then the main agent joins the views into one clear decision and updates the docs. (Need a fifth, domain-specific lens — a Security Expert, a Clinician, a Data Scientist? See "Add a domain lens" in `AGENTS.md`.)

## How a request flows

A request goes through up to three steps. Small things stop early. Only real decisions go all the way.

1. **Sort it** — Is this small (a typo, a quick fact, moving a file)? Then just do it. Is it a real decision? Then go on.
2. **Think** — How much thinking does it need? Often one expert is enough. The full council is only for big choices that touch many teams.
3. **Write it down** — Which kind of doc do we make?

The three kinds of docs:

- **PR/FAQ** — "Should we build this feature?" → saved in `decisions/pr-faq/`
- **ADR** — "Which technical option do we pick?" → saved in `decisions/adr/`
- **Council decision** — "What is the big choice that touches many teams?" → saved in `decisions/council/`

How much you think (step 2) and which doc you write (step 3) are two separate choices. They can also join up — a PR/FAQ can turn into a council decision if the choice gets big.

Every doc also adds one line to the Decision Log in `docs/README.md`.

## Marketing pieces (the studio)

The council can also make your marketing films, launch images, video covers and slides. Ask for one, and an agent follows `STUDIO.md`. The studio has three layers: a shared **foundation** (your mark, colours, type and honesty rules), one or more **design kits** (each a complete look with reusable parts), and **design cases** (each piece, made with one kit). For a piece, the agent picks or builds a kit, agrees a brief with you, writes the story, shows you key frames, then builds the picture and the sound as code. The template ships no studio files; they are set up the first time you ask. Videos are never committed — each one re-renders from its source, and every published video is listed in `studio/videos.md`. Uploads stay private until you publish them.

## Examples

- **"Fix a typo on the pricing page."**
  Small. Just fix it. No doc needed. (Stops at step 1.)

- **"Should we add a daily streak feature?"**
  A real choice about building a feature. Write a **PR/FAQ**. → `decisions/pr-faq/`

- **"Which database should we use?"**
  A technical choice with a few options. One expert (the Technical Architect) is enough. Write an **ADR**. → `decisions/adr/`

- **"Should we raise the price of the top plan?"**
  A big choice. It touches money, users, and marketing. Ask the full **council**. → `decisions/council/`

## What is in this repo

- `AGENTS.md` — the full rule book (read this first)
- `SETUP.md` — the one-time setup routine (Workflow 0): an agent fills the template in for your product
- `STUDIO.md` — how agents make marketing films, stills and slides (Workflow 4). The `studio/` folder is created the first time a piece is asked for
- `CLAUDE.md` — how to run the workflows in Claude Code
- `GEMINI.md` — how to run them in Gemini CLI and Antigravity
- `agents/` — the four council members (canonical persona files)
- `.gemini/agents/` — the same four as native Gemini CLI subagents
- `decisions/` — saved decisions (`pr-faq/`, `adr/`, `council/`)
- `docs/` — the current product docs (product, tech, marketing, metrics) + the Decision Log
- `templates/` — blank PR/FAQ and ADR forms
- `scripts/` and `.github/workflows/` — optional sync of `docs/` and `decisions/` to a ClickUp Doc
- `.council-temp/` — scratch space for council sessions (gitignored)

## Set up

This repo is set up for **BytePets** — Vilnius's community-checked map for pet owners: find, add, confirm and share vets, pharmacies, pet-friendly places and walking areas, and match lost and found pets. Built for Hack4Vilnius (challenger: If Insurance), as a mobile web app. Re-run `SETUP.md` if the product changes.

## Optional: show your docs in ClickUp

If your team lives in ClickUp, a GitHub Action can mirror `docs/` and `decisions/` into one ClickUp Doc every time you push to `main`. Each page shows who changed it last, and each maintainer can use their own ClickUp token. It is **off by default**: nothing runs until you add the `CLICKUP_WORKSPACE_ID` variable. Setup steps are in `scripts/README-clickup-sync.md`. Don't use ClickUp? Delete `scripts/` and `.github/workflows/sync-clickup-docs.yml`.

## Quick start

1. Clone the repo.
2. **Run setup.** Ask your agent to "set up the council" (or just start a council request — it will offer). It interviews you, fills in your product facts and the `docs/` skeleton, and commits. See `SETUP.md`.
3. Open `AGENTS.md` and try a request: ask the council a small strategic question, or draft a PR/FAQ from `templates/pr-faq-template.md`.
4. Every decision gets a permanent file in `decisions/` and one line in the Decision Log in `docs/README.md`.

# Council: 24-hour Hack4Vilnius MVP scope

**Date**: 2026-10-09
**Lenses**: Product Manager, Technical Architect
**Status**: Superseded by `002-rescope-to-challenge-brief.md`

## Decision

Build an iPhone app (Flutter, ADR-001) and a landing page on Firebase. The app has four parts, in this order of importance:

1. **Walk-Mate** — the product and the wow moment: a wall of walks (today, tomorrow), create a walk, join a walk, and a full-screen 3D preview where a new avatar walks in live when someone joins.
2. **AI assistant** — text and photo in, a clear urgency banner out, and a hand-off to our map ("Show on map"). Gemini on Cloud Functions with Google Search grounding (ADR-002).
3. **Dog-services map** — plain and solid: imported OpenStreetMap data plus a hand-checked list of 24/7 emergency vets.
4. **Sign-in and dog profile** — anonymous sign-in and a one-screen dog profile.

The landing page goes live early with a waitlist and live counters, to show real demand.

Cut for the hackathon: AI lost & found, crowdsourced checks, reputation, push notifications, chat between walkers, editing walks, Sign in with Apple, Android.

## Sequence

- **Hours 0–2: spikes on the real iPhone.** App builds with Firebase sign-in; the Gemini combined-tools call works; the 3D prototype runs in a WebView. No feature work until these are green.
- **Hours 2–14: core loop, then AI.** Hour 14 is a hard checkpoint: the full must-have loop works end to end on a real iPhone, or we cut from the list in the PRD.
- **Hour 20: feature freeze.** The rest is bug fixes, seed data and three demo rehearsals.

## Why

Walk-Mate is the one feature no other team will have, and it serves the north star (walks that happen). Every team will have an AI chat; ours stands out only when it hands off to our own map and always shows the nearest emergency vet for red-flag signs. The map on its own is a weak demo, so it stays plain. The architect lens moved all writes with rules (create, join) into Functions and put attendees inside the event doc, so one listener feeds the wall, the detail screen and the 3D scene. The lenses differed on the feature-freeze hour (18 vs 21); we chose 20.

## Open Issues

- Does the team really know Flutter? Check in hour 0 (ADR-001).
- Which exact Gemini model ID do we pin? Decide after the hour-0 spike.
- Who checks the emergency vet list by hand?
- Should we post the landing page in Vilnius dog groups during the event? The founder decides.

## Action Items

- Rewrite `docs/product/prd.md` with the scope, user stories, acceptance criteria and safety rules.
- Fill `docs/product/roadmap.md` (Phase 1 = hackathon MVP).
- Fill `docs/tech/architecture.md` with the data model, Functions, assistant flow and 3D bridge.
- Add `docs/product/hackathon-plan.md` with the build plan, cut line and demo script.

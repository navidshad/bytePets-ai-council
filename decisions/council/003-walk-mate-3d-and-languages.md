# Council: Bring back Walk-Mate with the 3D preview, ship in EN and LT

**Date**: 2026-10-09
**Lenses**: Founder call (no lenses run; builds on Council 002)
**Status**: Decided
**Amends**: `002-rescope-to-challenge-brief.md`

## Decision

1. **Walk-Mate comes back in Phase 1, in a light form, with the 3D preview in the app.** A walk starts at a walking area: one from the map, or a pin the host drops. People see a wall of walks for today and tomorrow. The host can edit their walk, and others can join or leave it. Everyone can open the full-screen 3D preview from `docs/product/prototypes/walkmate-3d-preview.html`. In it, joined people and dogs stand in the scene, open spots show as "?" ghosts, and avatars walk in or out live when someone joins or leaves. Out of scope: topics, cancel, chat, the forecast-based weather look, and finding the scene type from OpenStreetMap.
2. **Walks feed the trust loop.** After joining a walk, the app asks "Is this walking area still OK?", and each walk shows the area's trust badge. Walks give people a weekly reason to come back and keep walking areas fresh.
3. **The app ships in English and Lithuanian from day one (P0).** All app text, trust labels, emails and AI replies come in the user's language. Place names and user posts stay as written.
4. **No walking-area outlines.** Walking areas are pins. City areas are imported as their centre points, and anyone can add a walking area by pinning it on the map.
5. **The nightly stale job covers Imported and Community places only.** Official items keep their badge and are refreshed by the monthly re-import. Lost & found posts expire on their own after 30 days.

## Why

The 3D walk preview is our most memorable moment and already exists as working web code, so on the web app (ADR-003) it runs with no WebView bridge. Tying walks to walking areas keeps it on the brief: walks happen at checked places, and each walk prompts a confirm. The verified data sources freed most of the data track's time, so that person ports the 3D scene. Vilnius is bilingual in practice, and a Lithuanian-only or English-only app would leave out many owners and judges.

## Open Issues

- Demo time: the 3-minute script now has three wow moments (trust loop, lost & found match, 3D join). Rehearsal decides which one gets the most time.
- Who on the team checks the Lithuanian strings?

## Action Items

- [x] Update `docs/product/prd.md` (Walk-Mate light, EN/LT, no polygons, stale job scope).
- [x] Update `docs/tech/architecture.md` (walks, 3D bridge on the web, i18n, points only).
- [x] Update `docs/product/hackathon-plan.md` (track D takes the 3D scene, cut line, demo script).
- [x] Update `docs/product/roadmap.md`, `docs/metrics/framework.md`, `docs/marketing/brand.md`, persona contexts and the prototypes index.

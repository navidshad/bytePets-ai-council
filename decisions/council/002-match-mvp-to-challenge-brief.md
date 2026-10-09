# Council: Match the MVP to the Challenge #6 brief — owners add and check places

**Date**: 2026-10-09
**Lenses**: Product Manager, Technical Architect
**Status**: Decided

## Decision

The brief asks for a community-based way to find, add, verify and share pet information, and to keep it reliable. Our scope covered only "find". Phase 1 changes so the **pet map is the spine of the product and owners keep it true**:

1. **Check a place (P0).** Every place card asks "Still correct?" with Yes and No. It shows "Confirmed by 3 owners, 2 days ago".
2. **Source and freshness on every place (P0).** Each place shows where it came from (City of Vilnius, OpenStreetMap, checked by BytePets, added by an owner) and when it was last checked. Three "No" votes add "May be out of date". Votes never hide or delete a place.
3. **City dog walking areas (P0).** A required import. If the city file does not load in one hour, we key the list in by hand.
4. **Add a place (P1).** A short form. The place shows as "Not checked yet" until two other owners confirm it.
5. **Assistant (P1).** It says how fresh a place is, and suggests owner-added places only after two confirms.

Hand-checked emergency vets are locked: no vote or edit can change them, and owners cannot add that type.

Walk-Mate stays in P0 as the "share" part of the brief and the wow moment of the demo. It is no longer the heart of the product. We stay dogs first and say so; the map adds a "pet-friendly place" type.

Paid for by: Google Search grounding moves to P2; free pin drop and the OpenStreetMap scene lookup are cut (preset spots only); forecast weather is cut (time-based look); "My walks" moves to P2; scene types stay at three.

This replaces the ranking of the four parts in `001-hackathon-mvp-scope.md`. The rest of 001 stands.

## Why

The challenger wrote "add", "verify" and "outdated" into the brief, and our best demo minute was spent on a feature the brief does not name. The fix is small: `places` already has `source` and `verified`, and every write already goes through a Function. It costs about 7 hours, so it is paid for with cuts, not added on top. The lenses differed on scene types (two or three); we kept three because the prototype already has them. Lost & found stays cut: a lost-pet app won this hackathon in 2024.

## Open Issues

- Which file holds the city dog walking areas, and does it have points or only shapes?
- Ask the If Insurance mentor on day one: does "verify" matter more than covering more kinds of pets?
- Votes come from anonymous accounts, so counts can be faked. We accept this for the demo and say so if asked.
- The timeline table in `docs/product/hackathon-plan.md` is unchanged. The team still has to place about 7 hours of work in it.
- ADR-001 says "the brief asks for an iPhone app". The challenge brief does not say this. The Flutter choice rests on team skill, so no new ADR is needed.

## Action Items

- [x] Update `docs/product/prd.md`: scope table, pet map section, assistant, Walk-Mate, metrics.
- [x] Update `docs/tech/architecture.md`: `addPlace`, `votePlace`, new `places` fields, locked places, city import.
- [x] Update `docs/product/roadmap.md` and `docs/marketing/brand.md`.
- [x] Update the cut line, team tracks and demo script in `docs/product/hackathon-plan.md` (timeline left as is).
- [x] Add "places checked or added" to `docs/metrics/framework.md`.
- [ ] Place the new work in the hackathon timeline (team).
- [ ] Find the city dog walking areas file (track D, first task).

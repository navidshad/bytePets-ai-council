# Council: MVP re-think after the challenger and mentor feedback

**Date**: 2026-10-09
**Lenses**: Product Manager, Business Strategist, UX Designer
**Status**: Decided
**Amends**: `002-rescope-to-challenge-brief.md`, `003-walk-mate-3d-and-languages.md`, `004-walk-slots-business.md`

## Decision

One idea: **the city's data says where; owners say what's true now.** Walking areas, dog-friendly places and vets use one model — a place, its source, and owner check-ins with a date.

**MVP features**

| # | Feature | Done when |
|---|---|---|
| 1 | Walking-area map with "fits my dog" filters (big/small dog, fenced, equipment, well-rated), from the city's 35 areas | A user filters "big dog + fenced" and sees matching areas |
| 2 | Owner check-in: stars, one photo, tags, fence OK / broken; live for everyone | A check-in on one phone shows on another within seconds |
| 3 | Vets open now: register clinics with hours, "checked on [date]", animals treated, Call | At 23:00 only open clinics show, each with its check date |
| 4 | Dog-friendly places (mainly cafés): dogs inside / terrace, water bowl, dog menu, photo | A café added by one owner is marked checked after a second owner checks in |
| 5 | Simple lost & found: two buttons, a three-step report (photo, pet, rough area), share link; no AI | A report is posted in under 30 seconds |
| 6 | Walk assistants with a live walk (founder call): walkers offer slots, owners book; during the walk the walker shares GPS, photos and short videos; each walk has a chat saved as history | The owner sees the walker move and a new photo arrive during the walk |

**Home screen (founder call):** a map-first home. A pastel map of real Vilnius, colour chips that filter and act as the legend, "you are here", a floating ask box that shrinks to a paw button when the user explores the map, and pins that fade near the screen edges. The assistant answers with numbered cards and matching numbered pins. Prototype: `docs/product/prototypes/home-map/`.

**Business shown in the MVP:** If as the paid safety partner for the checked vet layer — a labelled partner box on vet pages that never changes order, ratings or "open now". Fallback: listings that cafés and pet shops claim. Walk slots are in the MVP as walk assistants (feature 6); payments stay later.

**Out of the MVP:** group walks and the 3D preview; payments; AI photo matching; the six-level trust badge (replaced by colour for state and "checked on [date]" for freshness); logging of dog care or steps.

**Privacy:** no live position is ever public. "Busy now" needs 3+ check-ins in 2 hours and never claims "quiet" from no data. Lost & found pins are fuzzed to about 150 m. Only the owner sees a walker live, and only during their booked walk.

## Why

The challenger from If wrote Challenge #6 and asked for rated playgrounds and dog-friendly places in one app; the mentor's strongest need was a vet open now. All three lenses picked the same core, which fits the organisers' advice that one finished core feature beats ten half-finished ones. The lenses split on lost & found (must-have vs roadmap) and on walker GPS. The founder kept both: lost & found stays simple, and the live walk is in, visible only to the owner. Live GPS in the background needs a native app, so the app is built in Flutter.

## Open Issues

- Platform is Flutter (founder call); ADR-004 must record it and supersede ADR-003 (web app).
- Map provider: Google Maps + Places (ratings, up to 5 reviews, opening hours, `allowsDogs`) hybrid with our check-ins, or MapLibre. Part of ADR-004.
- Real photos for the prototype: team photos or openly licensed ones.

## Action Items

- [ ] Write ADR-004 (Flutter app and map provider) with an architect review.
- [x] Rewrite `docs/product/prd.md` in a clean format from this decision.
- [ ] Update `docs/tech/architecture.md`, `docs/product/roadmap.md`, `docs/product/pitch-guide.md` and the deck to match.

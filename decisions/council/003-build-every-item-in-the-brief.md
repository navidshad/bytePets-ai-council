# Council: Build every item in the brief — lost & found, add, share, pet-friendly places

**Date**: 2026-10-09
**Lenses**: Product Manager, Technical Architect
**Status**: Decided

## Decision

The team set a fixed rule: every item the Challenge #6 brief names is built in Phase 1. So these become must-haves:

1. **Lost & found (P0).** A layer of the pet map, with its own filter chip and a list. A post holds: lost or found, kind of pet (dog, cat, other), one photo, a short note, the place and time last seen, and an optional contact. Anyone can tap "I saw this pet" to add a time and a pin. The poster closes it with "Reunited". A post drops off after 14 days unless a sighting or a renew keeps it open. Three flags close it. No AI photo matching and no reading of social media groups.
2. **Add a place (P0).** As designed in decision 002.
3. **Share (P0).** A share button on every place and every lost & found post. It opens the iPhone share sheet with a short text and a map link. No web page and no deep link.
4. **Pet-friendly places (P0).** Imported from OpenStreetMap (`dog=yes`, `dog=leashed`) plus a short list keyed in by hand.
5. **Other help (P0).** A new "shelter / rescue" type: OpenStreetMap animal shelters plus a hand-checked, locked list of the main Vilnius shelters and rescue lines. Groomers come from OpenStreetMap.
6. **Pet owners.** The map and lost & found serve any pet. The dog profile and Walk-Mate stay dogs only, and we say so.

This costs about 13 hours. It is paid for in this order:

1. **The 3D preview moves to P1**, with one scene type and no live walk-in. In P0 the walk screen shows a static scene picture. A join still changes the count live on every phone.
2. The create-walk form loses topics and scene change.
3. The landing page shows numbers typed in before the demo, not live counters.
4. Firebase Analytics events are cut. Counts come from Firestore.
5. The assistant's freshness line moves to P2. Listing open lost pets nearby is P1.

Walk-Mate stays in P0 as wall, create and join. This replaces the priorities in decision 002 where they differ, and its line that lost & found stays cut.

## Why

The challenger judges against the brief, and the brief names each of these. Lost & found sits on the same map as the places, so it is one more kind of community information and not a second product. That also sets it apart from the 2024 winner, a stand-alone search tool that gathered posts from social media. Posts get their own collection because they close, expire and hold contact details. The lenses differed on sharing (a web page for each card, or the share sheet only); we chose the share sheet because it needs no backend. The 3D preview is the only cut large enough to pay for this, and the brief does not ask for it.

## Open Issues

- The 3D preview was the wow moment of the demo. It is now a should-have. The team should confirm this. If hours are left after the hour-14 checkpoint, it comes back first.
- The north-star metric (walks with a joiner) no longer matches the spine of the product. One lens proposed map actions instead. Not decided.
- Lost & found posts show contact details from anonymous users, and posts can be faked. We limit open posts per user, hide the phone until a tap and round the pin to about 100 m. That is enough for a demo, not for launch.
- The timeline table in `docs/product/hackathon-plan.md` was written before decisions 002 and 003. Track C now starts with lost & found, not 3D.
- Who keys in the shelter and pet-friendly lists?

## Action Items

- [x] Update `docs/product/prd.md`: scope table, lost & found section, add and share as must-haves, Walk-Mate and 3D.
- [x] Update `docs/tech/architecture.md`: `petPosts`, sightings, three new Functions, share, new import tags, smaller 3D bridge.
- [x] Update `docs/product/roadmap.md`, `docs/marketing/brand.md` and `docs/metrics/framework.md`.
- [x] Update the tracks, cut line and demo script in `docs/product/hackathon-plan.md` (timeline table left as is, with a note).
- [ ] Confirm the 3D cut and place the new work in the timeline (team).
- [ ] Decide the north-star metric (team).

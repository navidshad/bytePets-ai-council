# Council: Re-scope the MVP to the official challenge brief

**Date**: 2026-10-09
**Lenses**: Product Manager, Technical Architect, Business Strategist
**Status**: Decided
**Supersedes**: `001-hackathon-mvp-scope.md`

## Decision

BytePets becomes **Vilnius's community-checked map for pet owners**. It is built around the brief's own verbs: find, add, verify and share. It covers vets and pharmacies, pet-friendly places, walking areas, and lost and found pets. Every item shows where it came from, when it was last confirmed, and by how many people.

It ships as a **mobile web app (PWA) on Firebase Hosting**, with the same Firebase backend (ADR-003 supersedes ADR-001). Every place and every lost or found post has a public link that opens with no install. This covers all pets, not only dogs.

**The demo moment:** phone A adds a pet-friendly café, and it shows grey: "Not yet confirmed". A judge scans a QR code and taps "Still true". The card turns green live. Then we share the link, and it opens in a plain browser.

**Walk-Mate is out of the Phase 1 build.** The existing 3D prototype is shown for about 15 seconds as "what's next". The AI health chat moves to Phase 2.

**Lost & found gets AI matching (founder call).** Gemini reads each lost or found photo and pulls out the pet's features. The server matches lost posts against found posts and tells both reporters. Each one confirms or rejects the match, and contact opens only when both say yes. Matching also works on the form fields alone, so lost & found still works if the photo step fails. This is the second demo moment: post a found cat, and a possible match appears on both phones.

**Lost & found is its own obvious section (founder call).** It is a tab in the bottom bar with two big buttons, "I lost a pet" and "I found a pet", and the same two buttons sit on the home map. Each one opens a short form. The assistant is a second way in: the reporter tells it what happened in their own words, or pastes a post or a poster photo. It asks only for what is missing, shows a draft, and the reporter taps Post. The assistant never posts on its own.

## Scope

| Priority | Items |
|---|---|
| **P0 (never cut)** | Map and list with 5 groups and filters; trust badge and freshness line on every card; add a place; confirm / report; lost & found tab with two big buttons, "I lost a pet" / "I found a pet" (also on the home map), and a board (post, photo, rounded location, in-app "I saw this pet" message, mark reunited); lost ↔ found matching with two-sided confirm, an in-app notice and an email (form fields always; Gemini photo features on top); public share links; Google sign-in to write (browsing needs no account); emergency button (nearest hand-checked 24/7 vet, no AI); data import from the three named sources; "How we rate info" page with live counters |
| **P1** | Gemini photo features in matching, if not ready by hour 14 (form-field matching stays P0); assistant that takes a lost or found report in plain words, a pasted post or a poster photo, and turns it into a draft the reporter posts; link previews in Messenger and Facebook; "My contributions" and helper badges; "Open now" filter; search by name; one "Pet emergency: what to do now" card (credited to If only if If agrees) |
| **P2** | Walking-area outlines (polygons); sightings with a location; print poster with QR; nightly stale job; Lithuanian language |
| **Cut** | Walk-Mate build; AI health chat (Phase 2); push (email and in-app notices instead); auto-sharing contact on a match; star ratings and reviews; insurance quotes or ads; native iPhone app |

## Trust rule (canonical)

Computed only on the server. The numbers sit at the top of one file and are shown in the app.

1. **Hidden**: 3+ reports from different people in 90 days, and more reports than confirms. Removed from the map and listed for the team to review.
2. **Disputed** (amber): 2+ reports in 90 days, newer than the last confirm. "2 people say this may be closed."
3. **Confirmed** (green): 2+ confirms from different people in 90 days, not counting the person who added it. For imported and official items, 1 confirm is enough.
4. **Official** (blue): from city or state data, with no open reports. "City data · updated {date}".
5. **Stale** (grey): no confirm in 180 days. "Not checked for 6+ months. Been here? Confirm it."
6. **Not yet confirmed** (grey): everything else.

The freshness line under every badge shows the date of the last confirm: green up to 30 days, amber 31–90 days, grey after that. Each person gets one vote per item, and can change it once every 7 days.

## Why

The judges will score us against the brief. Council 001 cut three of its four verbs and made a feature the brief never names into the hero. The real pain in the brief is trust, not search: any team can put vets on a map, but few will show why an entry can be believed. Lost and found is named in the brief. It is also the best story for If, and the one thing people already share outside apps. Today a lost post and a found post for the same pet can sit in two different Facebook groups and never meet. Matching them is the clearest "one place" win, and the two-sided confirm keeps the AI's guesses safe.

A web app makes "share" real, lets judges join the demo on their own phones, and removes the iPhone signing risk. The lenses differed on Walk-Mate (cut vs. shrink); we cut the build and kept the prototype as a "what's next" beat. They also differed on anonymous writes. We require Google sign-in, because with anonymous sign-in "one vote per person" really means one vote per browser.

## Open Issues

- Can at least two people on the team write Vue fast? If not, keep Flutter for the app and build the share pages as plain web pages (ADR-003).
- Do the official city walking-area data and the VMVT vet register exist in a form we can download? Each import gets a hard 60-minute limit, then we fall back to OpenStreetMap plus a hand-made list.
- Is anyone from If at the event? A 5-minute talk in hour 1 beats any guess.
- Who reviews hidden items and lost & found posts after the event?
- How good is Gemini at matching the same pet across two very different photos? Test it in hours 0–2 with 10 real photo pairs. Until then, we show the match score as "possible match", never as a fact.

## Action Items

- [x] Write ADR-003 (mobile web app) and mark ADR-001 as superseded.
- [x] Rewrite `docs/product/prd.md`, `docs/product/roadmap.md` and `docs/product/hackathon-plan.md` for the new scope.
- [x] Rewrite `docs/tech/architecture.md`: data model, Functions, trust rule, imports, share links.
- [x] Update `docs/marketing/brand.md` (pitch, messages, If touchpoint) and `docs/metrics/framework.md` (new north star).
- [x] Update the product line in `AGENTS.md`, `README.md` and the persona Context blocks.

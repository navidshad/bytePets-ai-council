# Hackathon Plan — BytePets at Hack4Vilnius

> Event plan for the 24-hour build, from `decisions/council/001-hackathon-mvp-scope.md` `decisions/council/002-match-mvp-to-challenge-brief.md` and `decisions/council/003-build-every-item-in-the-brief.md`. Scope lives in `prd.md`; the system lives in `../tech/architecture.md`. This doc is about time, people and the demo.

## Before the event
- Paid Apple developer account ready; demo iPhone registered.
- Firebase project created on the Blaze plan with a budget alert; Gemini API key ready.
- Team check: who has built a Flutter screen before? (ADR-001)
- Hand-check 5–8 emergency / 24-hour vets in Vilnius (name, address, phone, hours).

## Team tracks (3–4 people, each with Claude Code)
- **A — Backend and AI:** Firestore, rules, Functions, Gemini.
- **B — App:** Flutter shell, profile, walks wall, create form, detail screen, chat UI.
- **C — Lost & found, then 3D:** post form, pins and list, sightings, close and expiry, share sheet. The 3D preview (one scene type, P1) only after the hour-14 checkpoint is green.
- **D — Data and web:** place import (city walking areas first, then OpenStreetMap with pet-friendly places and shelters), emergency vet and shelter lists, map tab, landing page, seed data.

Freeze the data model as `models.dart` and `types.ts` in hour 1. Changes go through person A.

**Owner checks (decision 002), about 7 hours in total.** A builds `votePlace` and `addPlace`. B builds the "Still correct?" buttons, the source and last-checked line, and the add form. D imports the city dog walking areas as the first task, before OpenStreetMap.

**Every item in the brief (decision 003), about 13 hours in total.** A builds `createPetPost`, `addSighting` and `closePetPost`. C builds the lost & found screens and the share sheet. D adds pet-friendly places and shelters to the import and seeds lost & found posts.

**The timeline table below was written before decisions 002 and 003 and is not changed.** It does not place this work, and its track C column is all 3D. The team places the new work. Rule of thumb: place checks, add a place and lost & found come before any 3D work.

## Timeline

| Hours | A — Backend/AI | B — App | C — 3D | D — Data/web |
|---|---|---|---|---|
| 0–2 | Firebase project, rules, Functions skeleton, **Gemini combined-tools spike** | **Blank app on the real iPhone**, anonymous sign-in, 4 tabs | **Prototype in WebView on the phone**, measure speed | Place import script, emergency vet list |
| 2–8 | `createEvent`, `joinEvent`, seed script | Dog profile, wall, create form, detail screen | 3 scene types, ghosts, avatars, walk-in animation, weather looks | Map tab, filters, place sheet; landing page live with waitlist (~hour 6) |
| 8–14 | `assistantChat` loop, photo input, pins, red-flag rule | Chat UI, photo picker, sources, "Show on map" | Bridge ↔ live event doc, two-phone join test | Pins from chat on map, landing counters, embedded scene |
| **14** | **Checkpoint: the full must-have loop works on a real iPhone — or cut** | | | |
| 14–20 | Search grounding with sources, golden demo answers | Empty and error states | Performance on device, more scene types | Seed demo walks, demo slides (2–3) |
| 20–24 | **Feature freeze.** Bug fixes, record backup video, rehearse 3 times, charge phones, sleep in turns | | | |

## Cut line (cut from the top if behind at hour 14)
1. Google Maps grounding pins (P2)
2. Google Search grounding (P2)
3. The assistant's freshness line (P2)
4. 3D walk preview (P1) → static scene picture
5. The assistant lists lost pets nearby (P1)
6. Tomorrow tab on the walks wall → today only
7. Map filters → places and lost & found chips only

Already cut by decisions 002 and 003: free pin drop for walks, forecast weather, walk topics, the live walk-in, more than one scene type, live landing counters, analytics events.

**Never cut:** place card → "Still correct?" → count and date change; add a place; lost & found post → sighting from a second phone → "Reunited"; share a place or a post; photo → urgency banner → pins on map; walks wall → join → count changes; landing page with waitlist.

Lost & found: only if all P0 and P1 are done by hour 18.

## Demo script (3 minutes)
1. **Problem (20 s).** "I moved to Vilnius with my dog. I knew no one. When she got sick at night, I scrolled Facebook groups for 20 minutes to find an open vet."
2. **Find (40 s).** "It's 11 p.m. and Luna ate something in the park." Send a prepared photo: "She ate this, is it bad?" Red banner: "Go to a vet now", with the reason. Tap "Show on map": the 24/7 vets are pinned, each marked "Checked by BytePets". Tap Directions.
3. **Add and verify (35 s).** Open a dog walking area from the city's own data: "Confirmed by 3 owners, 2 days ago". On the second phone tap "Still correct? Yes": the first phone shows 4 and "today". Add a pet-friendly café: it shows grey as "Not checked yet".
4. **Lost & found (40 s).** Tap the "Lost & found" chip: red and blue pins. Post "Lost: grey cat, Užupis" with a photo in a few taps. On the second phone tap "I saw this pet": the first phone shows the sighting. Tap Share: the share sheet opens with the photo and a map link.
5. **Walk together (25 s).** Open the walks wall. Tap a walk at Cathedral Square and tap Join: the second phone already shows "3 of 4". If the 3D preview is built, show it here.
6. **Proof and close (20 s).** Landing page with today's numbers and the waitlist. "BytePets: the Vilnius pet map that owners keep true. Find it, add it, check it, share it."

One person drives the phone, one talks. Mirror the iPhone screen. Phone hotspot as Wi-Fi backup. Warm up the assistant before going on stage.

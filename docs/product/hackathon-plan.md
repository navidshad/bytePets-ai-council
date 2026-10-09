# Hackathon Plan — BytePets at Hack4Vilnius

> Event plan for the 24-hour build, from `decisions/council/001-hackathon-mvp-scope.md` and `decisions/council/002-match-mvp-to-challenge-brief.md`. Scope lives in `prd.md`; the system lives in `../tech/architecture.md`. This doc is about time, people and the demo.

## Before the event
- Paid Apple developer account ready; demo iPhone registered.
- Firebase project created on the Blaze plan with a budget alert; Gemini API key ready.
- Team check: who has built a Flutter screen before? (ADR-001)
- Hand-check 5–8 emergency / 24-hour vets in Vilnius (name, address, phone, hours).

## Team tracks (3–4 people, each with Claude Code)
- **A — Backend and AI:** Firestore, rules, Functions, Gemini.
- **B — App:** Flutter shell, profile, walks wall, create form, detail screen, chat UI.
- **C — 3D:** port the Three.js prototype into a WebView, bridge, scene types, thumbnails.
- **D — Data and web:** place import, emergency vet list, map tab, landing page, seed data.

Freeze the data model as `models.dart` and `types.ts` in hour 1. Changes go through person A.

**Owner checks (decision 002), about 7 hours in total.** A builds `votePlace` and `addPlace`. B builds the "Still correct?" buttons, the source and last-checked line, and the add form. D imports the city dog walking areas as the first task, before OpenStreetMap. The timeline below does not place this work yet; the team places it. Build the place check before the 3D polish, so it is never the last thing built.

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
3. Share a place link (P2)
4. The assistant's freshness line (P1)
5. Add a place (P1) → owners can only check places
6. Map filters → all pins, no filters

Already cut by decision 002: free pin drop for walks, forecast weather, more than 3 scene types.

**Never cut:** place card → "Still correct?" → count and date change; photo → urgency banner → pins on map; wall → 3D preview → join with animation; landing page with waitlist.

Lost & found: only if all P0 and P1 are done by hour 18.

## Demo script (3 minutes)
1. **Problem (20 s).** "I moved to Vilnius with my dog. I knew no one. When she got sick at night, I scrolled Facebook groups for 20 minutes to find an open vet."
2. **Find (50 s).** "It's 11 p.m. and Luna ate something in the park." Send a prepared photo: "She ate this, is it bad?" Red banner: "Go to a vet now", with the reason. Tap "Show on map": the 24/7 vets are pinned, each marked "Checked by BytePets". Tap Directions.
3. **Add and verify (30 s).** Open a dog walking area from the city's own data: "Confirmed by 3 owners, 2 days ago". On the second phone tap "Still correct? Yes": the first phone shows 4 and "today". If the add form is built: add a pet-friendly café; it shows grey as "Not checked yet".
4. **Share (50 s).** Open the Walk-Mate wall. Tap a walk at Cathedral Square: the 3D scene fills the screen, two dogs and two "?" spots. Tap Join — a new avatar walks in. The second phone already shows "3 of 4".
5. **Proof (20 s).** Landing page: real numbers from today for places checked, walks and waitlist.
6. **Close (10 s).** "BytePets: the Vilnius pet map that owners keep true. Find help, check it, walk together."

One person drives the phone, one talks. Mirror the iPhone screen. Phone hotspot as Wi-Fi backup. Warm up the assistant before going on stage.

# Hackathon Plan — BytePets at Hack4Vilnius

> Event plan for the 24-hour build, from `decisions/council/001-hackathon-mvp-scope.md`. Scope lives in `prd.md`; the system lives in `../tech/architecture.md`. This doc is about time, people and the demo.

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
2. Live weather → fixed weather per walk
3. Google Search grounding → Gemini plus our places tool only
4. Map filters → all pins, no filters
5. Scene types → 3 (park, riverside, old town)
6. Free pin drop → only the ~10 preset spots

**Never cut:** wall → 3D preview → join with animation; photo → urgency banner → pins on map; landing page with waitlist.

Lost & found: only if all P0 and P1 are done by hour 18.

## Demo script (3 minutes)
1. **Problem (20 s).** "I moved to Vilnius with my dog. I knew no one. When she got sick at night, I scrolled Facebook groups for 20 minutes to find an open vet."
2. **Walk-Mate (70 s).** Open the wall. Tap a walk at Cathedral Square: the 3D scene fills the screen, two dogs and two "?" spots. Tap Join — a new avatar walks in. Hold up the second phone: it already shows "3 of 4". Create a new walk by the Neris in under 20 seconds.
3. **Assistant (60 s).** "It's 11 p.m. and Luna ate something in the park." Send a prepared photo: "She ate this, is it bad?" Red banner: "Go to a vet now", with the reason. Tap "Show on map": the 24/7 vets are pinned. Tap Directions.
4. **Proof (20 s).** Landing page: real waitlist and walk numbers from today.
5. **Close (10 s).** "BytePets: walk together, find help, know when it's urgent. Built for Vilnius in 24 hours."

One person drives the phone, one talks. Mirror the iPhone screen. Phone hotspot as Wi-Fi backup. Warm up the assistant before going on stage.

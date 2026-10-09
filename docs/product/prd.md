# Product Requirements — BytePets

> Living doc. Hack4Vilnius, challenger: If Insurance. Scope: Council 002 + 003. Build details: `../tech/architecture.md`.

## Problem
From the official challenge:
1. Pet info in Vilnius is **scattered** across sources, community groups and websites.
2. It quickly becomes **outdated**.
3. Its **reliability** is hard to judge.
4. Owners need **pet-friendly places, vet services, walking areas, lost or found animals** and **other help** in one place.
5. The answer must be **community-based**: owners **find, add, verify and share** info, and make Vilnius more pet-friendly.

## Solution
A web app with one map of all pet places in Vilnius.

- **Find:** vets, pharmacies, pet-friendly places and walking areas on one map.
- **Add:** anyone can add a place.
- **Verify:** owners tap "Still true?" on a place. Each place shows when it was last confirmed.
- **Lost & found:** post a lost or found pet. The app finds possible matches and tells both people.
- **Walks:** owners create and join walks at walking areas.
- **Walk slots:** people register times they are free to walk dogs; owners book a slot. This is how we earn.
- **Share:** every place, post and walk has a link.
- **Assistant:** talk to it to do most of the above: find places, report a lost or found pet, create or join a walk. It shows a card, and you tap Confirm.

## App vision
A mobile web app. No install: scan a QR code or open a shared link.

**Home** starts with the assistant: a message box, "Ask BytePets…", with a few example prompts ("Open vet near me", "I found a dog", "Walk at Vingis tonight"). Below it, the things we have, as short sections:
- **Emergency** — a red button: the nearest 24/7 vet.
- **Lost & found** — **"I lost a pet"** and **"I found a pet"** buttons, and the newest posts nearby.
- **Walks** — today's walks, with spots left.
- **Places** — Vets, Pharmacies, Pet-friendly, Walking areas; each opens the map filtered.

The bottom bar has **Home · Map · Walks · Lost & found · Me**. An EN / LT switch sits in the header.

Pages:
- **Home** — the assistant box and the sections above
- **Assistant chat** — opens when you send a message; answers show pins on the map and action cards to confirm
- **Map** and **List** — filter chips, + Add button
- **Place page** — details, source, trust badge, "Still true?", Share
- **Add place**
- **Lost & found** — the two buttons and the board
- **Report lost / found** — the form
- **Match** — "Possible match", Yes / No, then a private chat
- **Walks** — today and tomorrow
- **Walk page** — full-screen 3D preview, Join / Leave, host Edit / Cancel
- **Create / edit walk**
- **Emergency** — the nearest 24/7 vet
- **How we rate info** — the trust rule and live counters
- **Me** — sign-in, dog profile, my posts and walks, language

## Features
Every feature needs public data that shows demand. **Only real numbers, taken straight from a named source — no estimates or numbers we calculated.** Pulled 2026-10-09; sources at the bottom.

| Feature | Solves (challenge problem) | Demand (public data) | Pages | Priority |
|---|---|---|---|---|
| **One map for everything** — vets, pharmacies, pet-friendly places, walking areas, lost & found, with filters | 1, 4 — scattered info, one place | 102,100 registered pets in Vilnius [A] | Home, Map, List | P0 |
| **Walking areas** — city areas on the map | 4 — walking areas | 55,384 registered dogs [A]; 35 city dog-walking areas, 4 being built, 8 planned [B] | Map, Place page | P0 |
| **Vets and pharmacies** | 4 — vet services | 102,100 registered pets [A]; the official vet register lists no opening hours [C] | Map, Place page | P0 |
| **Trust badge** — source label + "Confirmed by N owners · X days ago" | 2, 3 — outdated, unreliable | Pet data is split across the city map, the VMVT register and OpenStreetMap [B][C][D] | Place page, How we rate info | P0 |
| **Add a place** — pin it on the map, with a duplicate warning | 5 — add | No public list of dog-friendly places found [D] | Add place | P0 |
| **Verify** — "Still true?" Yes / Something's wrong; one vote per person | 3, 5 — reliability, verify | Same as Trust badge [C][D] | Place page | P0 |
| **Lost & found** — two big buttons, post with photo, rounded location, no public phone | 4 — lost or found animals | 165 pets reported lost in Vilnius in 2026 so far; 68 in all of 2025 [E] | Lost & found, Report lost / found | P0 |
| **AI matching** — lost vs found, both told, both confirm before a chat opens | 1, 4 — posts never meet | Same as Lost & found [E] | Match | P0 (AI photo reading P1) |
| **Emergency** — nearest hand-checked 24/7 vet, no AI needed | 4 — vet services, other help | The official vet register lists no opening hours [C] | Emergency | P0 |
| **EN / LT** — the whole app in both languages | 1 — find info easily | 78,000 foreign-born residents [G] | All | P0 |
| **Assistant** — talk to do most things; writes need a Confirm tap | 1, 4, 5 — find easily, other help, add | **Gap** — no public data | Home, Assistant chat | P0 |
| **Walk-Mate** — create, edit, cancel, join and leave walks; 3D preview | 4, 5 — walking areas, more pet-friendly | **Gap** — no data for group walks [I] | Walks, Walk page, Create / edit walk | P0 |
| **Walk slots** — walkers register free times; owners book a slot; both tap "Done" after; payment mocked in the demo | Business model; 5 — community | 56 walk and care requests in Vilnius on paslaugos.lt; prices €2–15 [I] | Walks, Walk slots, Book a walk | P1 |
| **Share** — a public link for every place, post and walk | 5 — share | Enabler | Place page, Report, Walk page | P0 |
| **Community counters** | 5 — community | Enabler | How we rate info | P0 |
| **Google sign-in to write** | 3 — one person, one vote | Enabler | Me | P0 |

## Gaps
- **Weak demand data:** group walks have no Vilnius evidence [I]; the Assistant has none. Founder call to keep them. In the pitch, frame them as ways to get more owners using and checking the data.
- **Proposed, not yet decided:** a **city coverage view** — registered dogs and city walking areas on one map, by district [A][B]. Needs a district count we can source directly (ask ŽŪDC or the city).
- **No public numbers:** stray animals caught per year in Vilnius; pet emergencies or poisonings (only news reports [H]).

## Business
Owners use the app free. We earn a fee on booked walk slots (we propose 15%; to test). Later: If insurance per booked walk, the city for coverage data. Decision: Council 004.

## Data sources

| Challenge source | Where we get it |
|---|---|
| Vilnius city dog walking areas | City map data — 35 areas (official) + OpenStreetMap |
| Vet clinics and pharmacies | VMVT register on data.gov.lt (official) + OpenStreetMap + 24/7 vets checked by phone |
| Pet-friendly places | OpenStreetMap + a hand-made list with source links, then the community grows it |

Demand sources:
- [A] Registered pets, data.gov.lt dataset 292 (2026-10-01).
- [B] City walking areas, Vilniaus planas map layers 16–18 (35 existing, 12 built or planned).
- [C] VMVT register, data.gov.lt dataset 5258.
- [D] OpenStreetMap via Overpass, Vilnius city.
- [E] Lost and exported pets, data.gov.lt dataset 293 (2026-10-01). Vilnius lost: 147 (2023), 74 (2024), 68 (2025), 165 (2026 to date).
- [G] Go Vilnius, 2026-09-07.
- [H] tv3.lt news on dog poisonings in Naujamiestis (2022, 2026).
- [I] `research/Dog Owner Demand Research Vilnius.md` (paslaugos.lt requests, Boop, global walking market), 2026-10-09.

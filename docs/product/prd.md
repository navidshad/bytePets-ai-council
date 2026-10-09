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

| Feature | Solves (challenge problem) | Pages | Priority |
|---|---|---|---|
| **One map for everything** — vets, pharmacies, pet-friendly places, walking areas, lost & found, with filters | 1, 4 — scattered info, one place | Home, Map, List | P0 |
| **Trust badge** — source label + "Confirmed by N owners · X days ago"; badges: Official, Confirmed, Not yet confirmed, Disputed, Stale | 2, 3 — outdated, unreliable | Place page, How we rate info | P0 |
| **Add a place** — pin it on the map, with a duplicate warning | 5 — add | Add place | P0 |
| **Verify** — "Still true?" Yes / Something's wrong; one vote per person | 3, 5 — reliability, verify | Place page | P0 |
| **Lost & found** — two big buttons, post with photo, rounded location, no public phone | 4 — lost or found animals | Lost & found, Report lost / found | P0 |
| **AI matching** — lost vs found posts, both told, both must confirm before a chat opens | 1, 4 — posts in different groups never meet | Match | P0 (AI photo reading P1) |
| **Assistant** — talk to do most things: find places, emergency vet, report lost/found, create or join a walk (P0); add or verify a place, edit/cancel/leave a walk, answer a match (P1). Writes always need a Confirm tap | 1, 4, 5 — find easily, other help, add | Home, Assistant chat (+ Map for pins) | P0 |
| **Walk-Mate** — create, edit, cancel, join and leave walks at walking areas; 3D preview with live join | 4, 5 — walking areas, more pet-friendly Vilnius | Walks, Walk page, Create / edit walk | P0 |
| **Share** — a public link for every place, post and walk | 5 — share | Place page, Report, Walk page | P0 |
| **Emergency** — nearest hand-checked 24/7 vet, no AI needed | 4 — vet services, other help | Emergency | P0 |
| **Community counters** — places added and confirmed, reunions, walks | 5 — community, more pet-friendly | How we rate info | P0 |
| **EN / LT** — the whole app in both languages | 1 — find info easily | All | P0 |
| **Google sign-in to write** — browsing is open | 3 — one real person, one vote | Me | P0 |

## Data sources

| Challenge source | Where we get it |
|---|---|
| Vilnius city dog walking areas | City map data — 35 areas (official) + OpenStreetMap |
| Vet clinics and pharmacies | VMVT register on data.gov.lt (official) + OpenStreetMap + 24/7 vets checked by phone |
| Pet-friendly places | OpenStreetMap + a hand-made list with source links, then the community grows it |

Pitch fact: **55,384 registered dogs** in Vilnius (data.gov.lt, 2026-10-01).

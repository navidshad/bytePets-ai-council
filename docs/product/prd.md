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
**BytePets: Vilnius's community-checked map for pet owners.** One link, any phone, English and Lithuanian. Every place shows where it came from and when an owner last confirmed it. Lost and found pets are matched by AI. Owners plan walks together at the city's walking areas.

## App vision
A mobile web app. No install: scan a QR code or open a shared link.

**Home** is a full-screen map of Vilnius. At the top: search and filter chips (Vets, Pharmacies, Pet-friendly, Walking areas, Lost & found). Above the map: two big buttons, **"I lost a pet"** and **"I found a pet"**. A red **Emergency** button floats in the corner. The bottom bar has **Map · Walks · Lost & found · Add · Me**. An EN / LT switch sits in the header.

Pages:
- **Map** (home) and **List**
- **Place page** — details, source, trust badge, "Still true?", Share
- **Add place**
- **Lost & found** — the two buttons and the board
- **Report lost / found** — the form
- **Assistant** — report in plain words
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
| **One map for everything** — vets, pharmacies, pet-friendly places, walking areas, lost & found, with filters | 1, 4 — scattered info, one place | Map, List | P0 |
| **Trust badge** — source label + "Confirmed by N owners · X days ago"; badges: Official, Confirmed, Not yet confirmed, Disputed, Stale | 2, 3 — outdated, unreliable | Place page, How we rate info | P0 |
| **Add a place** — pin it on the map, with a duplicate warning | 5 — add | Add place | P0 |
| **Verify** — "Still true?" Yes / Something's wrong; one vote per person | 3, 5 — reliability, verify | Place page | P0 |
| **Lost & found** — two big buttons, post with photo, rounded location, no public phone | 4 — lost or found animals | Lost & found, Report lost / found | P0 |
| **AI matching** — lost vs found posts, both told, both must confirm before a chat opens | 1, 4 — posts in different groups never meet | Match | P0 (AI photo reading P1) |
| **Assistant report** — tell what happened in plain words, get a draft to post | 4, 5 — other help, add | Assistant | P1 |
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

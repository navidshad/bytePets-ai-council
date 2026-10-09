# Product Requirements — BytePets

> Living doc. The current state of the product. Changing it is a council-level change (see `AGENTS.md`).

**Phase 1** — Hack4Vilnius MVP, 24-hour build. Scope: Council 002, amended by Council 003. Platform: mobile web app (ADR-003). How each feature answers the brief: `challenge-blueprint.md`. How it is built: `../tech/architecture.md`.

## Vision
Pet info in Vilnius is scattered across Facebook groups and old websites, and you can't tell what is still true. BytePets is **Vilnius's community-checked map for pet owners**: find vets, pharmacies, pet-friendly places, walking areas and lost or found pets, see when each was last confirmed, and add, confirm or share in two taps. Owners can also plan walks together and see them in 3D. In English and Lithuanian.

**Users:** pet owners in Vilnius (dogs first, then cats and others), and people who found an animal and won't install an app.

## Scope

| Priority | Features |
|---|---|
| **P0** | Map and list; trust badges; add a place; confirm / report; lost & found with AI matching; Walk-Mate with 3D preview; share links; emergency button; Google sign-in to write; EN and LT; data imports; "How we rate info" page |
| **P1** | AI reads the pet photo; assistant takes a report in plain words; link previews; "My contributions" and badges; "Open now" filter; search; "Pet emergency: what to do now" card |
| **P2** | Sightings with a location; printable lost-pet poster; nightly stale job; more 3D scenes and weather looks |

## Features

### 1. Map and list (P0)
- Five groups with filters: Vets (incl. 24/7), Pharmacies & pet shops, Pet-friendly places, Walking areas, Lost & found.
- Each card: name, pet rules, address, hours, Call, Directions, Share, **source label** (City data / Imported / Community) and **trust badge** with "Confirmed by N owners · X days ago".
- No account needed to browse.

### 2. Add and verify (P0)
- **Add a place:** pin it on the map, pick a group, add up to 3 quick facts ("Allowed inside", "Fenced"). We warn about duplicates within 40 m. New places show grey: "Not yet confirmed".
- **Verify:** "Still true?" → Yes / Something's wrong (closed, moved, not pet-friendly, wrong info). One vote per person. You can't confirm your own place.
- After someone taps Directions or joins a walk, we ask them to confirm the place.

**Trust rule** (computed on the server):

| Badge | When |
|---|---|
| Official (blue) | City or state data, no open reports |
| Confirmed (green) | 2+ confirms in 90 days (1 for imported data) |
| Not yet confirmed (grey) | New, no confirms yet |
| Disputed (amber) | 2+ reports in 90 days, newer than the last confirm |
| Stale (grey) | Imported or community place, no confirm in 180 days |
| Hidden | 3+ reports and more reports than confirms; the team reviews |

### 3. Lost & found (P0)
- A **Lost & found tab** with two big buttons: **"I lost a pet"** and **"I found a pet"**. The same buttons are on the home map.
- Post: species, photos, colour, size, note, last-seen place and time. The location is rounded to ~100 m, and no phone or email is shown in public.
- **Matching:** each new post is compared with posts of the other kind (same species, within 5 km, within 30 days). Both people get an in-app notice and an email: "Possible match".
- **Both must confirm.** Each taps "Yes, that's them" or "No". A private chat opens only when both say yes.
- Mark as reunited. Posts expire after 30 days. 3 reports hide a post.
- P1: AI reads the photo, pre-fills the form, and compares photos for better matches. Without AI, matching uses the form fields.
- P1: **Assistant**: tell it what happened in plain words, or paste a post or poster. It shows a draft; you tap Post. It never posts on its own.

### 4. Walk-Mate (P0)
- **Walks tab:** walks for today and tomorrow, each at a walking area, with spots left ("2 of 4").
- **Create** a walk: walking area or a pin, day, time, group size (2–4), note. Needs a one-time dog profile (name, size, colour).
- **Edit:** the host changes time, size, note or place. People who joined get a notice.
- **Cancel:** the host can cancel at any time. People who joined get a notice and an email.
- **Join / leave:** you can't join twice, join a full walk, or join your own.
- **3D preview** (`prototypes/walkmate-3d-preview.html`): a full-screen scene with people and dogs, and "?" for open spots. Avatars walk in or out live when someone joins or leaves.
- Safety: public start points, first names only, at most 4 people.

### 5. Share, emergency, sign-in, languages (P0)
- **Share:** every place, post and walk has a public link that opens with no install.
- **Emergency button:** the nearest hand-checked 24/7 vet, with Call and Directions. Works without AI.
- **Sign-in:** browse freely; Google sign-in to add, vote, post, message or walk. Only first names are shown.
- **Languages:** English and Lithuanian, with a switch. Place names and posts are not translated.

## Data sources
| Brief | Source |
|---|---|
| Walking areas | City map data (35 areas, official), plus OpenStreetMap |
| Vets and pharmacies | VMVT register (official), OpenStreetMap, 24/7 vets checked by phone |
| Pet-friendly places | OpenStreetMap, plus a hand-made list with source links |

No Facebook scraping and no stored Google data. Pitch fact: 55,384 registered dogs in Vilnius (data.gov.lt, 2026-10-01).

## Out of scope
Walk topics and chat; AI health chat (Phase 2); push notifications; ratings and reviews; insurance offers or ads; native apps.

## Success metrics
- **North star:** places confirmed by the community in the last 30 days.
- Places added and confirmed at the event; lost & found matches confirmed by both sides; walks with at least one joiner.
- The demo runs end to end with no failure in 3 rehearsals.

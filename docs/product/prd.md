# Product Requirements — BytePets

> Living doc. This is the current state of the product, not a decision record. Edit it as decisions land. Changing this doc is a council-level change (see `AGENTS.md` → "Editing rules for living docs").

**Phase**: Phase 1 — Hack4Vilnius MVP (Challenge #6), 24-hour build. Scope set by `decisions/council/001-hackathon-mvp-scope.md`.

## Vision
Dog owners in Vilnius get help for their dog from many scattered places: Facebook groups, forums and old websites. The information is often out of date and nobody checks it. BytePets brings it into one iPhone app: other owners to walk with, the city's dog services on a map, and an AI assistant that answers questions about your dog and shows you where to go.

## Target users
Dog owners in Vilnius who use an iPhone. New owners and people new to the city feel the gap most.

## Problems we solve
1. "I want company on walks, but I don't know anyone here." → Walk-Mate.
2. "My dog is acting strange. Is it bad? Where do I go right now?" → AI assistant + map.
3. "Where is the nearest vet or dog park?" → Map.

## Scope at a glance

| Priority | Item |
|---|---|
| **Must (P0)** | Walk-Mate wall, create, join, 3D preview with live join; AI assistant with photo, urgency banner and "Show on map"; services map with imported places and checked emergency vets; anonymous sign-in and dog profile; landing page with waitlist |
| **Should (P1)** | Live weather in the 3D scene; Google Search grounding with sources; "My walks" list; empty and error states |
| **Could (P2)** | Leave a walk; share a walk link; "open now" filter; Google Maps grounding with pins; all 6 scene types; free pin drop with OpenStreetMap scene lookup |
| **Cut** | AI lost & found (extra only if all P0 and P1 are done by hour 18); crowdsourced checks; reputation; push notifications; chat between walkers; editing walks; Sign in with Apple; Android |

## Core features

### A. Sign-in and dog profile (P0)
- **Story:** As a new user, I can start in one tap.
  - Anonymous Firebase sign-in plus my first name. No email or password.
- **Story:** As a dog owner, I add my dog once.
  - One screen: dog name, breed (free text), size (S/M/L), optional photo. Saved to Firestore. Under 30 seconds.
  - If I have no dog profile, creating or joining a walk sends me here first, then back.
  - One dog per user in Phase 1.

### B. Walk-Mate (P0 — the heart of the product)
- **Story:** As an owner, I see a wall of walks for today and tomorrow.
  - Two tabs: Today, Tomorrow. Each card: start place, time, dog avatars, spots left ("2 of 4"), topic chips, and a static picture of its scene type.
  - Past walks are hidden. Full walks show "Full" and cannot be joined.
  - Empty state: "No walks yet today. Start one — it takes 30 seconds."
- **Story:** As an owner, I create a walk.
  - Fields: start point (pick from ~10 popular Vilnius spots, or drop a pin), day (today or tomorrow), time, group size (2–4), short description, up to 3 topics from a fixed list (e.g. training, puppies, running, slow walk, new in Vilnius, just chill). Dog info comes from my profile.
  - It shows on the wall within 2 seconds.
  - Scene type comes from the preset spot, or from OpenStreetMap tags at a dropped pin; if unknown, "park". The host can change it.
- **Story:** As an owner, I open a walk and see a 3D preview.
  - Full-screen scene, one of: landmark, park, riverside, forest, old town, street. At least 3 in P0.
  - Weather look: sun, cloud, rain, snow, evening. P0 may use a time-based value; P1 uses the forecast for that hour.
  - Joined people show as avatars with their dogs; empty spots show as "?" ghosts. Event info sits on glass cards over the scene.
  - Loads in under 3 seconds on the demo iPhone and runs smoothly.
- **Story:** As an owner, I join a walk.
  - Tap "Join": a "?" ghost turns into my avatar with an animation.
  - Other phones see the new avatar walk in and the count change in real time.
  - I can't join twice, join a full walk, or join my own walk.
- Safety for meeting strangers: public start points only, first names only, small groups (max 4).

### C. Dog-services map (P0, kept plain)
- **Story:** As an owner, I see Vilnius dog services on a map.
  - Pins for 4 groups with clear icons: vet, emergency vet (24/7), pet shop / pharmacy, dog park / walking area.
  - Data imported once from OpenStreetMap and (if found in 30 minutes) Vilnius open data. At least 50 places, all inside Vilnius.
  - Emergency vets are checked by hand and marked as checked.
  - Tap a pin: name, type, address, opening hours if known, call, and "Directions" (opens Apple Maps).
  - Filter chips by type. ("Open now" is P2.)

### D. AI assistant (P0)
- **Story:** As a worried owner, I describe a problem and send a photo, and get clear, safe advice.
  - Chat with text and a photo from camera or library. Photos are resized on the phone before upload.
  - Every health answer starts with an urgency banner: **Go to a vet now** (red), **See a vet soon** (amber), **Likely fine at home — watch for…** (green).
  - Red-flag signs (poisoning, chocolate, xylitol, bloat, heavy bleeding, breathing trouble, seizures) always get "Go to a vet now" and the nearest checked 24/7 emergency vet. The server enforces this, not only the prompt.
  - A fixed line under every health answer: "BytePets is not a vet. If in doubt, call a vet."
  - The app shows progress while it works ("Looking at the photo…", "Searching…").
- **Story:** As an owner, I ask where to go and see it on the map.
  - "Where is the nearest emergency vet?" → the answer has a "Show on map" button; the Map tab opens with those places highlighted.
  - End to end in under 10 seconds on venue Wi-Fi.
- **P1:** Google Search grounding for care questions, with sources shown right under the answer.
- **P2:** Google Maps grounding with pins for places we don't have. Sources keep the "Google Maps" label as is.
- Cut: memory across chats, vet booking, voice.

### E. Landing page (P0)
- **Story:** As a visitor or judge, I understand BytePets in 5 seconds and can sign up.
  - Hero line, one hero visual (the 3D walk scene), three feature blocks, a "Join the waitlist" email form saved to Firestore, live counters of walks created and waitlist sign-ups.
  - Works on mobile. Vue (or plain HTML) on Firebase Hosting. Live by about hour 6.

## Demo assumptions (what is real and what is seeded)
- **Seeded and said so:** 10–15 walks for today and tomorrow across the scene types, with a mix of full, half-full and empty; seeded users with first names and dog avatars.
- **Real:** place data (imported), the AI answers, live joins between two phones, waitlist numbers.
- Weather may be a fixed value per walk if the forecast is not wired in time.
- Backup: a short screen recording of the assistant flow, used only if the network fails.

## Out of scope (for now)
- AI lost & found (on hold — extra only if time is left)
- Crowdsourced checks of places, reputation and voting
- Push notifications, chat between walkers, editing or deleting walks, moderation tools
- Sign in with Apple, more than one dog per user
- Android

## Success metrics
See `../metrics/framework.md`. For the hackathon:
- Walks created by real people during the event.
- Walks with at least one joiner (north star).
- Waitlist sign-ups on the landing page.
- The demo runs end to end with no failure in 3 rehearsals.

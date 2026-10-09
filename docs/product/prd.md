# Product Requirements — BytePets

> Living doc. This is the current state of the product, not a decision record. Edit it as decisions land. Changing this doc is a council-level change (see `AGENTS.md` → "Editing rules for living docs").

**Phase**: Phase 1 — Hack4Vilnius MVP (Challenge #6), 24-hour build. Scope set by `decisions/council/001-hackathon-mvp-scope.md` and `decisions/council/002-match-mvp-to-challenge-brief.md`.

## Vision
Dog owners in Vilnius get help for their dog from many scattered places: Facebook groups, forums and old websites. The information is often out of date and nobody checks it. BytePets brings it into one iPhone app: a pet map of the city that owners add to and keep true, an AI assistant that answers questions about your dog and shows you where to go, and other owners to walk with.

## Target users
Dog owners in Vilnius who use an iPhone. New owners and people new to the city feel the gap most. We start with dogs: they are the largest group and the one that needs walks. The places and vets on the map serve every pet.

## Problems we solve
1. "Where is the nearest vet or dog park, and is that still true?" → Pet map that owners check and add to.
2. "My dog is acting strange. Is it bad? Where do I go right now?" → AI assistant + map.
3. "I want company on walks, but I don't know anyone here." → Walk-Mate.

## Scope at a glance

| Priority | Item |
|---|---|
| **Must (P0)** | Pet map with city walking areas, imported places and locked, hand-checked emergency vets; "Still correct?" check on every place, with source and last-checked date; AI assistant with photo, urgency banner and "Show on map"; Walk-Mate wall, create, join, 3D preview with live join; anonymous sign-in and dog profile; landing page with waitlist |
| **Should (P1)** | Add a place ("Not checked yet" until two owners confirm); the assistant says how fresh a place is; empty and error states |
| **Could (P2)** | Share a place link; Google Search grounding with sources; "My walks" list; leave a walk; share a walk link; "open now" filter; Google Maps grounding with pins; all 6 scene types |
| **Cut** | AI lost & found (extra only if all P0 and P1 are done by hour 18); reputation and weighted votes; editing a place's details; free pin drop for walks; forecast weather; push notifications; chat between walkers; editing walks; Sign in with Apple; Android |

## Core features

### A. Sign-in and dog profile (P0)
- **Story:** As a new user, I can start in one tap.
  - Anonymous Firebase sign-in plus my first name. No email or password.
- **Story:** As a dog owner, I add my dog once.
  - One screen: dog name, breed (free text), size (S/M/L), optional photo. Saved to Firestore. Under 30 seconds.
  - If I have no dog profile, creating or joining a walk sends me here first, then back.
  - One dog per user in Phase 1.

### B. Walk-Mate (P0 — the "share" part and the wow moment)
- **Story:** As an owner, I see a wall of walks for today and tomorrow.
  - Two tabs: Today, Tomorrow. Each card: start place, time, dog avatars, spots left ("2 of 4"), topic chips, and a static picture of its scene type.
  - Past walks are hidden. Full walks show "Full" and cannot be joined.
  - Empty state: "No walks yet today. Start one — it takes 30 seconds."
- **Story:** As an owner, I create a walk.
  - Fields: start point (pick from ~10 popular Vilnius spots), day (today or tomorrow), time, group size (2–4), short description, up to 3 topics from a fixed list (e.g. training, puppies, running, slow walk, new in Vilnius, just chill). Dog info comes from my profile.
  - It shows on the wall within 2 seconds.
  - Scene type comes from the preset spot. The host can change it.
- **Story:** As an owner, I open a walk and see a 3D preview.
  - Reference look: [prototypes/walkmate-3d-preview.html](prototypes/walkmate-3d-preview.html).
  - Full-screen scene, one of: landmark, park, riverside, forest, old town, street. At least 3 in P0.
  - Weather look: sun, cloud, rain, snow, evening. It is set from the time of day. The forecast is cut.
  - Joined people show as avatars with their dogs; empty spots show as "?" ghosts. Event info sits on glass cards over the scene.
  - Loads in under 3 seconds on the demo iPhone and runs smoothly.
- **Story:** As an owner, I join a walk.
  - Tap "Join": a "?" ghost turns into my avatar with an animation.
  - Other phones see the new avatar walk in and the count change in real time.
  - I can't join twice, join a full walk, or join my own walk.
- Safety for meeting strangers: public start points only, first names only, small groups (max 4).

### C. Pet map (P0 — the spine of the product)
- **Story:** As an owner, I see Vilnius pet services on a map.
  - Pins for 5 groups with clear icons: vet, emergency vet (24/7), pet shop / pharmacy, dog park / walking area, pet-friendly place.
  - Data comes from the City of Vilnius dog walking areas (required; keyed in by hand if the file does not load in one hour) and OpenStreetMap. At least 50 places, all inside Vilnius.
  - Tap a pin: name, type, address, opening hours if known, call, and "Directions" (opens Apple Maps).
  - Filter chips by type. ("Open now" is P2.)
- **Story:** As an owner, I can tell how far to trust a place.
  - Every place card shows its source: "City of Vilnius", "OpenStreetMap", "Checked by BytePets" or "Added by an owner".
  - Every place card shows when it was last checked: "Confirmed by 3 owners, 2 days ago", or "Imported 9 Oct, not yet checked by owners".
  - Three "No" votes add a "May be out of date" label. Votes never hide or delete a place.
- **Story:** As an owner, I check a place in one tap.
  - The card asks "Still correct?" with Yes and No. My vote changes the count and the date at once, on every phone.
  - One vote per owner per place. I cannot vote on a place I added.
- **Story (P1):** As an owner, I add a place the map does not have.
  - Short form: name, type, pin on the map. Under 30 seconds.
  - It shows at once with a grey "Not checked yet" pin. Two confirms from other owners turn it into a normal pin.
  - No second place of the same type within 30 m. At most 5 new places per owner per day.
- Emergency vets are checked by hand and locked. Owners cannot vote on them, change them or add that type.
- **P2:** share a place link.

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
- **P1:** The answer says how fresh each place is ("confirmed 2 days ago"). Owner-added places are suggested only after two confirms. The emergency pin always comes from the locked list.
- **P2:** Google Search grounding for care questions, with sources shown right under the answer.
- **P2:** Google Maps grounding with pins for places we don't have. Sources keep the "Google Maps" label as is.
- Cut: memory across chats, vet booking, voice.

### E. Landing page (P0)
- **Story:** As a visitor or judge, I understand BytePets in 5 seconds and can sign up.
  - Hero line, one hero visual (the 3D walk scene), three feature blocks, a "Join the waitlist" email form saved to Firestore, live counters of places checked, walks created and waitlist sign-ups.
  - Works on mobile. Vue (or plain HTML) on Firebase Hosting. Live by about hour 6.

## Demo assumptions (what is real and what is seeded)
- **Seeded and said so:** 10–15 walks for today and tomorrow across the scene types, with a mix of full, half-full and empty; seeded users with first names and dog avatars.
- **Seeded and said so:** a few owner checks on some places, so the counts are not all zero.
- **Real:** place data (imported), checks made by people at the event, the AI answers, live joins between two phones, waitlist numbers.
- Weather is a time-based look, not a forecast.
- Backup: a short screen recording of the assistant flow, used only if the network fails.

## Out of scope (for now)
- AI lost & found (on hold — extra only if time is left)
- Reputation and weighted votes; editing a place's details; moderation of owner-added places
- Free pin drop for walks; forecast weather
- Push notifications, chat between walkers, editing or deleting walks, moderation tools
- Sign in with Apple, more than one dog per user
- Android

## Success metrics
See `../metrics/framework.md`. For the hackathon:
- Places checked or added by real people during the event.
- Walks created by real people during the event.
- Walks with at least one joiner (north star).
- Waitlist sign-ups on the landing page.
- The demo runs end to end with no failure in 3 rehearsals.

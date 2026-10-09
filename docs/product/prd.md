# Product Requirements — BytePets

> Living doc. This is the current state of the product, not a decision record. Edit it as decisions land. Changing this doc is a council-level change (see `AGENTS.md` → "Editing rules for living docs").

**Phase**: Phase 1 — Hack4Vilnius MVP (Challenge #6), 24-hour build. Scope set by `decisions/council/001-hackathon-mvp-scope.md`, `decisions/council/002-match-mvp-to-challenge-brief.md` and `decisions/council/003-build-every-item-in-the-brief.md`. Rule from decision 003: every item the challenge brief names is built in Phase 1.

## Vision
Pet owners in Vilnius get help for their pet from many scattered places: Facebook groups, forums and old websites. The information is often out of date and nobody checks it. BytePets brings it into one iPhone app: a pet map of the city that owners add to, check and share; lost and found pets on the same map; an AI assistant that answers questions about your dog and shows you where to go; and other owners to walk with.

## Target users
Pet owners in Vilnius who use an iPhone. New owners and people new to the city feel the gap most. The map, the places and lost & found serve every pet. The profile, the assistant and Walk-Mate start with dogs: they are the largest group and the one that needs walks.

## Problems we solve
1. "Where is the nearest vet or dog park, and is that still true?" → Pet map that owners check and add to.
2. "My pet is lost", or "I found a pet. Whose is it?" → Lost & found on the same map.
3. "My dog is acting strange. Is it bad? Where do I go right now?" → AI assistant + map.
4. "I want company on walks, but I don't know anyone here." → Walk-Mate.

## Scope at a glance

| Priority | Item |
|---|---|
| **Must (P0)** | Pet map with city walking areas, vets, pharmacies, pet-friendly places, shelters and locked, hand-checked emergency vets; "Still correct?" check on every place, with source and last-checked date; add a place; lost & found posts with sightings on the same map; share a place or a post; AI assistant with photo, urgency banner and "Show on map"; Walk-Mate wall, create, join; anonymous sign-in and dog profile; landing page with waitlist |
| **Should (P1)** | 3D walk preview (one scene type, no live walk-in); the assistant lists open lost pets nearby; empty and error states |
| **Could (P2)** | The assistant says how fresh a place is; Google Search grounding with sources; "My walks" list; leave a walk; share a walk link; "open now" filter; Google Maps grounding with pins; more scene types and the live walk-in |
| **Cut** | AI photo matching for lost pets and reading social media groups; reputation and weighted votes; editing a place's details; walk topics; free pin drop for walks; forecast weather; analytics events; push notifications; chat between walkers; editing walks; Sign in with Apple; Android |

## Core features

### A. Sign-in and dog profile (P0)
- **Story:** As a new user, I can start in one tap.
  - Anonymous Firebase sign-in plus my first name. No email or password.
- **Story:** As a dog owner, I add my dog once.
  - One screen: dog name, breed (free text), size (S/M/L), optional photo. Saved to Firestore. Under 30 seconds.
  - If I have no dog profile, creating or joining a walk sends me here first, then back.
  - One dog per user in Phase 1.

### B. Walk-Mate (P0 — wall, create and join; the 3D preview is P1)
- **Story:** As an owner, I see a wall of walks for today and tomorrow.
  - Two tabs: Today, Tomorrow. Each card: start place, time, dog avatars, spots left ("2 of 4"), and a static picture of its scene type.
  - Past walks are hidden. Full walks show "Full" and cannot be joined.
  - Empty state: "No walks yet today. Start one — it takes 30 seconds."
- **Story:** As an owner, I create a walk.
  - Fields: start point (pick from ~10 popular Vilnius spots), day (today or tomorrow), time, group size (2–4), short description. Dog info comes from my profile.
  - It shows on the wall within 2 seconds.
  - Scene type comes from the preset spot.
- **Story:** As an owner, I open a walk and see who is coming.
  - The walk screen shows a static picture of the scene type, the place, the time, and the people who joined with their dogs. Empty spots show as "?".
- **Story:** As an owner, I join a walk.
  - Tap "Join": my name and dog fill a "?" spot.
  - Other phones see the count change in real time.
  - I can't join twice, join a full walk, or join my own walk.
- **Story (P1):** As an owner, I open a walk and see a 3D preview.
  - Reference look: [prototypes/walkmate-3d-preview.html](prototypes/walkmate-3d-preview.html).
  - Full-screen scene of one type (park). Joined people show as avatars with their dogs; empty spots show as "?" ghosts. Event info sits on glass cards over the scene.
  - Weather look: sun, cloud, rain, snow, evening. It is set from the time of day.
  - Loads in under 3 seconds on the demo iPhone. A new join redraws the scene; the live walk-in animation and more scene types are P2.
- Safety for meeting strangers: public start points only, first names only, small groups (max 4).

### C. Pet map (P0 — the spine of the product)
- **Story:** As an owner, I see Vilnius pet services on a map.
  - Pins for 6 groups with clear icons: vet, emergency vet (24/7), pet shop / pharmacy, dog park / walking area, pet-friendly place, shelter / rescue. Groomers show under pet shops.
  - Data comes from the City of Vilnius dog walking areas (required; keyed in by hand if the file does not load in one hour) and OpenStreetMap. Pet-friendly places come from OpenStreetMap (`dog=yes`, `dog=leashed`) plus at least 10 keyed in by hand. Shelters and rescue lines come from OpenStreetMap plus a hand-checked list of the main ones in Vilnius. At least 50 places, all inside Vilnius.
  - Tap a pin: name, type, address, opening hours if known, call, and "Directions" (opens Apple Maps).
  - Filter chips by type. ("Open now" is P2.)
- **Story:** As an owner, I can tell how far to trust a place.
  - Every place card shows its source: "City of Vilnius", "OpenStreetMap", "Checked by BytePets" or "Added by an owner".
  - Every place card shows when it was last checked: "Confirmed by 3 owners, 2 days ago", or "Imported 9 Oct, not yet checked by owners".
  - Three "No" votes add a "May be out of date" label. Votes never hide or delete a place.
- **Story:** As an owner, I check a place in one tap.
  - The card asks "Still correct?" with Yes and No. My vote changes the count and the date at once, on every phone.
  - One vote per owner per place. I cannot vote on a place I added.
- **Story:** As an owner, I add a place the map does not have.
  - Short form: name, type, pin on the map. Under 30 seconds.
  - It shows at once with a grey "Not checked yet" pin. Two confirms from other owners turn it into a normal pin.
  - At most 5 new places per owner per day. (A check for a second place of the same type within 30 m is P1.)
- **Story:** As an owner, I share a place with someone.
  - A share button on every place card opens the iPhone share sheet with the name, type, address, "confirmed by N owners" line and a map link.
- Emergency vets and the hand-checked shelters are locked. Owners cannot vote on them or change them, and cannot add an emergency vet.

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
- Owner-added places are suggested only after two confirms. The emergency pin always comes from the locked list.
- **P1:** "Are there lost pets near me?" → the assistant lists open lost & found posts nearby, with "Show on map".
- **P2:** The answer says how fresh each place is ("confirmed 2 days ago").
- **P2:** Google Search grounding for care questions, with sources shown right under the answer.
- **P2:** Google Maps grounding with pins for places we don't have. Sources keep the "Google Maps" label as is.
- Cut: memory across chats, vet booking, voice.

### E. Landing page (P0)
- **Story:** As a visitor or judge, I understand BytePets in 5 seconds and can sign up.
  - Hero line, one hero picture (the pet map with a lost-pet pin), three feature blocks, a "Join the waitlist" email form saved to Firestore, and today's numbers for places checked, lost & found posts and walks (typed in before the demo, not live).
  - Works on mobile. Vue (or plain HTML) on Firebase Hosting. Live by about hour 6.

### F. Lost & found (P0)
- **Story:** As an owner whose pet is lost, or as someone who found a pet, I post it in under a minute.
  - Form: lost or found, kind of pet (dog, cat, other), one photo, a short note, the place and time last seen (a pin on the map), and an optional phone number.
  - The form says: "Mark where the pet was last seen, not your home." The pin is rounded to about 100 m.
  - At most 2 open posts per person.
- **Story:** As an owner, I see lost and found pets on the same map.
  - A "Lost & found" filter chip shows open posts as pins: red for lost, blue for found. A list shows the same posts, newest first.
  - A post card shows the photo, the note, "last seen 3 hours ago near Vingis Park", how many sightings it has, and a "Show contact" button.
- **Story:** As anyone, I help with one tap.
  - "I saw this pet" adds a sighting: the time and a pin. The card and every phone show it at once.
  - A share button opens the iPhone share sheet with the photo, the note and a map link.
- **Story:** As the poster, I keep my post true.
  - "Reunited" closes the post. Closed posts leave the map.
  - A post drops off after 14 days. A new sighting or "Still open" from the poster keeps it for 14 more days.
  - Three flags from other people close a post.
- Not built: AI photo matching, alerts by area, reading posts from social media groups.

## Demo assumptions (what is real and what is seeded)
- **Seeded and said so:** 10–15 walks for today and tomorrow, with a mix of full, half-full and empty; seeded users with first names and dog avatars.
- **Seeded and said so:** 5–8 lost & found posts with sample photos, some with sightings.
- **Seeded and said so:** a few owner checks on some places, so the counts are not all zero.
- **Real:** place data (imported), checks, new places, posts and sightings made by people at the event, the AI answers, live counts between two phones, waitlist numbers.
- Weather is a time-based look, not a forecast.
- Backup: a short screen recording of the assistant flow, used only if the network fails.

## Out of scope (for now)
- AI photo matching for lost pets, alerts by area, reading social media groups
- Walk topics, more 3D scene types, the live walk-in animation
- Reputation and weighted votes; editing a place's details; moderation of owner-added places
- Free pin drop for walks; forecast weather
- Push notifications, chat between walkers, editing or deleting walks, moderation tools
- Sign in with Apple, more than one dog per user
- Android

## Success metrics
See `../metrics/framework.md`. For the hackathon:
- Places checked or added by real people during the event.
- Lost & found posts and sightings made by real people during the event.
- Walks created by real people during the event.
- Walks with at least one joiner (north star).
- Waitlist sign-ups on the landing page.
- The demo runs end to end with no failure in 3 rehearsals.

# Technical Architecture — BytePets

> Living doc. The current shape of the system at a high level. The *why* behind specific choices lives in `../../decisions/adr/`. Changing this doc is a council-level change (see `AGENTS.md` → "Editing rules for living docs").

## Overview
A Flutter iPhone app (ADR-001) talks to Firebase. The app reads Firestore directly, but every write that has rules (add a place, check a place, post a lost or found pet, add a sighting, create a walk, join a walk, AI chat) goes through a callable Cloud Function. The AI assistant is one Cloud Function that calls Gemini with our own tools (ADR-002); Google Search and Google Maps grounding are P2. The 3D walk preview (P1) is a Three.js page inside a WebView. Sharing uses the iPhone share sheet and needs no backend. Place data is imported from City of Vilnius open data and OpenStreetMap into Firestore; after that, owners add places and check them.

```
iPhone app (Flutter)
  ├─ reads ──────────────► Firestore (users, places, petPosts, events, chats)
  ├─ calls ──────────────► Cloud Functions: addPlace, votePlace, createPetPost, addSighting, closePetPost,
  │                            createEvent, joinEvent, assistantChat
  │                            └─ Gemini (our tools; Search + Maps grounding are P2)
  ├─ uploads photos ─────► Firebase Storage
  └─ WebView ────────────► Three.js scene (bundled asset, P1)
Landing page (Firebase Hosting) ─► Firestore waitlist
```

## Components
- **iPhone app (Flutter)** — 4 tabs: Map, Walks, Assistant, Me. Lost & found is a filter chip and a list on the Map tab, not a tab of its own. Packages: Firebase (core, auth, firestore, storage, functions), `google_maps_flutter`, `image_picker`, `share_plus`, Riverpod or Provider; `webview_flutter` for the P1 3D preview.
- **Cloud Functions (2nd gen, Node 20, `europe-west1`)**
  - `createEvent` (callable) — checks input (size 2–4, start within 48 h, inside Vilnius), copies the host's dog, takes the scene type from the preset spot and the weather look from the start time, writes the event with the host as first attendee.
  - `joinEvent` (callable) — a Firestore transaction: not full, not already in, not cancelled; adds the attendee; updates `count` and `status`.
  - `leaveEvent` (callable, P2).
  - `votePlace(placeId, type: confirm|flag)` (callable) — one transaction: reject if the place is `locked`, if the vote doc already exists, or if the user added the place; at most 30 votes per user per day; bump `confirmCount` or `flagCount`; a confirm sets `lastCheckedAt`.
  - `addPlace` (callable) — checks the name (2–60 characters), a category from a fixed list without `emergency_vet`, a point inside Vilnius, at most 5 adds per user per day (P1: no place of the same category within 30 m). Writes `source: user`, `verified: false`, `confirmCount: 0`.
  - `createPetPost` (callable) — checks kind (`lost|found`), species (`dog|cat|other`), a note of 5–300 characters, a photo path in the caller's own Storage folder, a point inside Vilnius, a last-seen time in the past 30 days, at most 2 open posts per user. Rounds the point to about 100 m. Sets `status: open` and `expiresAt` = now + 14 days.
  - `addSighting(postId, lat, lng, seenAt)` (callable) — the post is open and not expired, the point is inside Vilnius, at most 10 sightings per user per day. Adds the sighting, bumps `sightingCount`, sets `lastSightingAt`, and moves `expiresAt` to now + 14 days.
  - `closePetPost(postId, reason: reunited|renew|flag)` (callable) — `reunited` and `renew` only by the poster (`renew` moves `expiresAt` out 14 days); `flag` by anyone else, once per user, and three flags set `status: closed`.
  - `assistantChat` (callable, `minInstances: 1`, 30 s timeout) — the AI loop below.
- **3D scene (P1)** — Three.js page bundled as a Flutter asset (works offline). One WebView, only on the event detail screen, one scene type. In P0 the wall and the detail screen use static pictures per scene type.
- **Landing page** — Vue or plain HTML on Firebase Hosting.
- **Scripts (laptop, not deployed)** — `import-places` (city dog walking areas + OpenStreetMap + manual lists → Firestore, with a committed GeoJSON snapshot; shapes are stored as their centre point; OpenStreetMap tags include vets, pet shops, pharmacies, groomers, `dog=yes|leashed` for pet-friendly places and `amenity=animal_shelter`), `seed-events` (demo walks) and `seed-pet-posts` (demo lost & found posts).

## Data
- **`users/{uid}`** — `displayName`, `dog: {name, breed, size: S|M|L, color, avatarSeed}`, `createdAt`.
- **`events/{eventId}`** — `hostUid`, `hostName`, `dog` (copy), `title`, `description`, `start: {lat, lng, label}`, `startsAt`, `day` (Vilnius date string), `maxSize`, `count`, `attendees: {uid → {name, dogName, breed, size, color, avatarSeed, joinedAt}}`, `scene: {type, name?}`, `weather: {look: sun|cloud|rain|snow|evening, isDay}`, `status: open|full|cancelled`. Wall query: `day in [today, tomorrow]`, ordered by `startsAt`.
- **`places/{id}`** — ids like `osm_node_123` or `man_001`; `name`, `category: vet|emergency_vet|pharmacy|pet_shop|dog_park|dog_area|groomer|pet_friendly|shelter`, `lat`, `lng`, `address?`, `phone?`, `website?`, `openingHours?`, `open24h`, `source: city|osm|manual|user`, `verified`, `locked`, `confirmCount`, `flagCount`, `lastCheckedAt`, `addedBy?`, `googlePlaceId?`. Imported places get `lastCheckedAt` = import time. Hand-checked emergency vets and shelters (`man_*`) have `locked: true`. The app listens to all places (a few hundred), so counts change live.
- **`places/{id}/votes/{uid}`** — `type: confirm|flag`, `at`. The doc id is the user id, so there is one vote per user per place.
- **`petPosts/{postId}`** — `kind: lost|found`, `species: dog|cat|other`, `note`, `photoPath`, `lat`, `lng` (rounded to about 100 m), `areaLabel?`, `lastSeenAt`, `contactPhone?`, `ownerUid`, `ownerName`, `status: open|reunited|closed`, `sightingCount`, `lastSightingAt?`, `flagCount`, `createdAt`, `expiresAt`. The app queries `status == open` and `expiresAt > now`, so old posts leave the map with no scheduled job. Posts are a collection of their own, not `places`, because they close, expire and hold contact details.
- **`petPosts/{postId}/sightings/{id}`** — `uid`, `lat`, `lng`, `seenAt`, `createdAt`.
- **`petPosts/{postId}/flags/{uid}`** — `at`. One flag per user per post.
- **`chats/{chatId}`** and **`messages/{msgId}`** — `role`, `text`, `imagePath?`, `sources[]`, `pins[]`, `urgent`, `createdAt`.
- **`googlePlaceCache/{googlePlaceId}`** — `name`, `lat`, `lng`, `ourPlaceId?` (P2).
- **`waitlist/{id}`** — email, `createdAt` (landing page).
- **Storage** — `chat-images/{uid}/{file}` and `pet-posts/{uid}/{file}`, images only, under 5 MB. Lost & found reuses the assistant's photo picker and resize.
- **Security rules** — signed-in users read events, places, pet posts, sightings and their own chats; clients write only their own `users/{uid}` and Storage folders; events, places, votes, pet posts, sightings, flags and chats are written only by Functions. App Check on Functions.

## Key integrations
- **Gemini API** (a Gemini 3.5 Flash-or-later model, pinned after the hour-0 spike) — via `@google/genai` in `assistantChat`. Tools: ours — `search_places(category, open_now?)`, `show_on_map(place_ids)`, `get_dog_profile()`, `flag_urgent(reason)`, and in P1 `search_lost_pets(kind?, species?)` (open posts only, never the phone number) — plus, in P2, Google Search and Google Maps (with the user's location, or the city centre 54.6872, 25.2797). `search_places` returns owner-added places only with two or more confirms; passing each place's source and last-checked date into the answer is P2. Loop of up to 4 steps. Fallback if the combined-tools preview fails: one grounded call, then one function-calling call.
- **Map pins** — one shape: `{key, source: ours|google, title, lat, lng, category?, ourPlaceId?, googlePlaceId?, mapsUri?}`. Our places pin directly. Google-only places need Places API Place Details for coordinates (P2); until then they show as source cards with an "Open in Google Maps" link. "Show on map" switches to the Map tab and fits the camera to the pins.
- **3D bridge (P1)** — JS → app on a channel named `BP`: `ready`, `error`. App → JS: `bp.setScene(json)`. The app listens to the event doc and sends the whole scene again when it changes. `bp.addAttendee` (the live walk-in), `bp.removeAttendee` and `tapSlot` are P2.
- **Share** — the `share_plus` package opens the iPhone share sheet. A place shares its name, type, address, "confirmed by N owners" line and a map link (`https://maps.apple.com/?ll=lat,lng&q=name`). A lost & found post shares its photo, note, last-seen line and a map link. No deep link and no web page.
- **Lost & found on the map** — one more filter chip on the Map tab and a list sheet. Red pins for lost, blue for found. The phone number shows only after a tap on "Show contact".
- **Scene type** — preset spots carry their type. Free pin drop and the OpenStreetMap lookup are cut.
- **Weather** — a look set from the start time. The forecast is cut.
- **Pin states on the map** — normal; grey "Not checked yet" (owner-added, fewer than two confirms); "May be out of date" label (three or more flags). Worked out on the phone from the place fields. Votes never hide or delete a place.
- **Analytics** — Firebase Analytics events are cut. Numbers for the demo come from Firestore counts.

## Constraints & non-functional needs
- 24-hour build; must run on a real iPhone for the demo.
- 3D preview (P1) loads in under 3 seconds and runs smoothly: pixel ratio max 2, low-poly, few lights, stop rendering when hidden.
- Lost & found privacy: the pin is the last-seen place rounded to about 100 m, never a home address; the phone number is optional and hidden until a tap; first names only.
- Assistant answers in under 10 seconds; progress shown while waiting.
- Health safety: urgency banner, red-flag rule in server code, fixed disclaimer, emergency pin only from the hand-checked, locked list; owners cannot add or vote on emergency vets.
- API keys only in Functions secrets; the iOS Maps key restricted to our bundle id; budget alert on the project.
- Google Maps grounding display rules: sources right after the answer, "Google Maps" label unchanged.

## Known risks & tech debt
- **Risks (de-risk in hours 0–2):** iOS build and signing; the Gemini combined-tools preview; the format of the city dog walking areas file (fallback: key the list in by hand). Three.js speed in a WebView is now a P1 risk only.
- **Debt we accept on purpose:** anonymous auth (no account recovery); attendees inside the event doc (fine for groups of 4); all places loaded on the phone (fine under ~2,000); exact start points are visible to all signed-in users; votes come from anonymous accounts, so counts can be faked (they cannot touch locked places or hide a place); lost & found posts and sightings can be faked too, and a shown phone number is public to every signed-in user.

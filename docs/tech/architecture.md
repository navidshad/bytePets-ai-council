# Technical Architecture — BytePets

> Living doc. The current shape of the system at a high level. The *why* behind specific choices lives in `../../decisions/adr/`. Changing this doc is a council-level change (see `AGENTS.md` → "Editing rules for living docs").

## Overview
A Flutter iPhone app (ADR-001) talks to Firebase. The app reads Firestore directly, but every write that has rules (create a walk, join a walk, add a place, check a place, AI chat) goes through a callable Cloud Function. The AI assistant is one Cloud Function that calls Gemini with our own tools (ADR-002); Google Search and Google Maps grounding are P2. The 3D walk preview is a Three.js page inside a WebView. Place data is imported from City of Vilnius open data and OpenStreetMap into Firestore; after that, owners add places and check them.

```
iPhone app (Flutter)
  ├─ reads ──────────────► Firestore (users, events, places, chats)
  ├─ calls ──────────────► Cloud Functions: createEvent, joinEvent, addPlace, votePlace, assistantChat
  │                            └─ Gemini (our tools; Search + Maps grounding are P2)
  ├─ uploads photos ─────► Firebase Storage
  └─ WebView ────────────► Three.js scene (bundled asset)
Landing page (Firebase Hosting) ─► Firestore waitlist + counters
```

## Components
- **iPhone app (Flutter)** — 4 tabs: Walks, Map, Assistant, Me. Packages: Firebase (core, auth, firestore, storage, functions), `google_maps_flutter`, `webview_flutter`, `image_picker`, Riverpod or Provider.
- **Cloud Functions (2nd gen, Node 20, `europe-west1`)**
  - `createEvent` (callable) — checks input (size 2–4, start within 48 h, inside Vilnius), copies the host's dog, takes the scene type from the preset spot and the weather look from the start time, writes the event with the host as first attendee.
  - `joinEvent` (callable) — a Firestore transaction: not full, not already in, not cancelled; adds the attendee; updates `count` and `status`.
  - `leaveEvent` (callable, P2).
  - `votePlace(placeId, type: confirm|flag)` (callable) — one transaction: reject if the place is `locked`, if the vote doc already exists, or if the user added the place; at most 30 votes per user per day; bump `confirmCount` or `flagCount`; a confirm sets `lastCheckedAt`.
  - `addPlace` (callable, P1) — checks the name (2–60 characters), a category from a fixed list without `emergency_vet`, a point inside Vilnius, no place of the same category within 30 m, at most 5 adds per user per day. Writes `source: user`, `verified: false`, `confirmCount: 0`.
  - `assistantChat` (callable, `minInstances: 1`, 30 s timeout) — the AI loop below.
- **3D scene** — Three.js page bundled as a Flutter asset (works offline); a copy on Hosting for the landing page. One WebView, only on the event detail screen. The wall uses static pictures per scene type.
- **Landing page** — Vue or plain HTML on Firebase Hosting.
- **Scripts (laptop, not deployed)** — `import-places` (city dog walking areas + OpenStreetMap + manual list → Firestore, with a committed GeoJSON snapshot; shapes are stored as their centre point) and `seed-events` (demo walks).

## Data
- **`users/{uid}`** — `displayName`, `dog: {name, breed, size: S|M|L, color, avatarSeed}`, `createdAt`.
- **`events/{eventId}`** — `hostUid`, `hostName`, `dog` (copy), `title`, `description`, `topics[]`, `start: {lat, lng, label}`, `startsAt`, `day` (Vilnius date string), `maxSize`, `count`, `attendees: {uid → {name, dogName, breed, size, color, avatarSeed, joinedAt}}`, `scene: {type, name?, source: preset|user}`, `weather: {look: sun|cloud|rain|snow|evening, isDay}`, `status: open|full|cancelled`. Wall query: `day in [today, tomorrow]`, ordered by `startsAt`.
- **`places/{id}`** — ids like `osm_node_123` or `man_001`; `name`, `category: vet|emergency_vet|pharmacy|pet_shop|dog_park|dog_area|groomer|pet_friendly`, `lat`, `lng`, `address?`, `phone?`, `website?`, `openingHours?`, `open24h`, `source: city|osm|manual|user`, `verified`, `locked`, `confirmCount`, `flagCount`, `lastCheckedAt`, `addedBy?`, `googlePlaceId?`. Imported places get `lastCheckedAt` = import time. Hand-checked emergency vets (`man_*`) have `locked: true`. The app listens to all places (a few hundred), so counts change live.
- **`places/{id}/votes/{uid}`** — `type: confirm|flag`, `at`. The doc id is the user id, so there is one vote per user per place.
- **`chats/{chatId}`** and **`messages/{msgId}`** — `role`, `text`, `imagePath?`, `sources[]`, `pins[]`, `urgent`, `createdAt`.
- **`googlePlaceCache/{googlePlaceId}`** — `name`, `lat`, `lng`, `ourPlaceId?` (P2).
- **`waitlist/{id}`** — email, `createdAt` (landing page).
- **Storage** — `chat-images/{uid}/{file}`, images only, under 5 MB.
- **Security rules** — signed-in users read events, places and their own chats; clients write only their own `users/{uid}` and Storage folder; events, places, votes and chats are written only by Functions. App Check on Functions.

## Key integrations
- **Gemini API** (a Gemini 3.5 Flash-or-later model, pinned after the hour-0 spike) — via `@google/genai` in `assistantChat`. Tools: ours — `search_places(category, open_now?)`, `show_on_map(place_ids)`, `get_dog_profile()`, `flag_urgent(reason)` — plus, in P2, Google Search and Google Maps (with the user's location, or the city centre 54.6872, 25.2797). `search_places` returns each place's source, `confirmCount`, `flagCount` and `lastCheckedAt`; owner-added places are returned only with two or more confirms. Loop of up to 4 steps. Fallback if the combined-tools preview fails: one grounded call, then one function-calling call.
- **Map pins** — one shape: `{key, source: ours|google, title, lat, lng, category?, ourPlaceId?, googlePlaceId?, mapsUri?}`. Our places pin directly. Google-only places need Places API Place Details for coordinates (P2); until then they show as source cards with an "Open in Google Maps" link. "Show on map" switches to the Map tab and fits the camera to the pins.
- **3D bridge** — JS → app on a channel named `BP`: `ready`, `tapSlot`, `error`. App → JS: `bp.setScene(json)` once, `bp.addAttendee(json)` for each new attendee (plays the walk-in), `bp.removeAttendee(uid)`. The app listens to the event doc and sends only the changes.
- **Scene type** — preset spots carry their type. Free pin drop and the OpenStreetMap lookup are cut.
- **Weather** — a look set from the start time. The forecast is cut.
- **Pin states on the map** — normal; grey "Not checked yet" (owner-added, fewer than two confirms); "May be out of date" label (three or more flags). Worked out on the phone from the place fields. Votes never hide or delete a place.
- **Analytics** — Firebase Analytics events (walk created, walk joined, assistant message, show on map, place opened).

## Constraints & non-functional needs
- 24-hour build; must run on a real iPhone for the demo.
- 3D preview loads in under 3 seconds and runs smoothly: pixel ratio max 2, low-poly, few lights, stop rendering when hidden.
- Assistant answers in under 10 seconds; progress shown while waiting.
- Health safety: urgency banner, red-flag rule in server code, fixed disclaimer, emergency pin only from the hand-checked, locked list; owners cannot add or vote on emergency vets.
- API keys only in Functions secrets; the iOS Maps key restricted to our bundle id; budget alert on the project.
- Google Maps grounding display rules: sources right after the answer, "Google Maps" label unchanged.

## Known risks & tech debt
- **Risks (de-risk in hours 0–2):** iOS build and signing; the Gemini combined-tools preview; Three.js speed in a WebView on the phone; the format of the city dog walking areas file (fallback: key the list in by hand).
- **Debt we accept on purpose:** anonymous auth (no account recovery); attendees inside the event doc (fine for groups of 4); all places loaded on the phone (fine under ~2,000); exact start points are visible to all signed-in users; votes come from anonymous accounts, so counts can be faked (they cannot touch locked places or hide a place).

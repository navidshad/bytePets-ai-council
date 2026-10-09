# Technical Architecture — BytePets

> Living doc. The current shape of the system at a high level. The *why* behind specific choices lives in `../../decisions/adr/`. Changing this doc is a council-level change (see `AGENTS.md` → "Editing rules for living docs").

## Overview
A Flutter iPhone app (ADR-001) talks to Firebase. The app reads Firestore directly, but every write that has rules (create a walk, join a walk, AI chat) goes through a callable Cloud Function. The AI assistant is one Cloud Function that calls Gemini with Google Search and Google Maps grounding plus our own tools (ADR-002). The 3D walk preview is a Three.js page inside a WebView. Place data is imported once from OpenStreetMap into Firestore.

```
iPhone app (Flutter)
  ├─ reads ──────────────► Firestore (users, events, places, chats)
  ├─ calls ──────────────► Cloud Functions: createEvent, joinEvent, assistantChat
  │                            ├─ Overpass (scene type) + Open-Meteo (weather), once per event
  │                            └─ Gemini (Search + Maps grounding + our tools)
  ├─ uploads photos ─────► Firebase Storage
  └─ WebView ────────────► Three.js scene (bundled asset)
Landing page (Firebase Hosting) ─► Firestore waitlist + counters
```

## Components
- **iPhone app (Flutter)** — 4 tabs: Walks, Map, Assistant, Me. Packages: Firebase (core, auth, firestore, storage, functions), `google_maps_flutter`, `webview_flutter`, `image_picker`, Riverpod or Provider.
- **Cloud Functions (2nd gen, Node 20, `europe-west1`)**
  - `createEvent` (callable) — checks input (size 2–4, start within 48 h, inside Vilnius), copies the host's dog, looks up scene type and weather in parallel, writes the event with the host as first attendee.
  - `joinEvent` (callable) — a Firestore transaction: not full, not already in, not cancelled; adds the attendee; updates `count` and `status`.
  - `leaveEvent` (callable, P2).
  - `assistantChat` (callable, `minInstances: 1`, 30 s timeout) — the AI loop below.
- **3D scene** — Three.js page bundled as a Flutter asset (works offline); a copy on Hosting for the landing page. One WebView, only on the event detail screen. The wall uses static pictures per scene type.
- **Landing page** — Vue or plain HTML on Firebase Hosting.
- **Scripts (laptop, not deployed)** — `import-places` (OpenStreetMap + manual list → Firestore, with a committed GeoJSON snapshot) and `seed-events` (demo walks).

## Data
- **`users/{uid}`** — `displayName`, `dog: {name, breed, size: S|M|L, color, avatarSeed}`, `createdAt`.
- **`events/{eventId}`** — `hostUid`, `hostName`, `dog` (copy), `title`, `description`, `topics[]`, `start: {lat, lng, label}`, `startsAt`, `day` (Vilnius date string), `maxSize`, `count`, `attendees: {uid → {name, dogName, breed, size, color, avatarSeed, joinedAt}}`, `scene: {type, name?, source: osm|preset|fallback|user}`, `weather: {code, tempC, windKmh, isDay, forHour}`, `status: open|full|cancelled`. Wall query: `day in [today, tomorrow]`, ordered by `startsAt`.
- **`places/{id}`** — ids like `osm_node_123` or `man_001`; `name`, `category: vet|emergency_vet|pharmacy|pet_shop|dog_park|dog_area|groomer`, `lat`, `lng`, `address?`, `phone?`, `website?`, `openingHours?`, `open24h`, `source`, `verified`, `googlePlaceId?`. The app loads all places once (a few hundred).
- **`chats/{chatId}`** and **`messages/{msgId}`** — `role`, `text`, `imagePath?`, `sources[]`, `pins[]`, `urgent`, `createdAt`.
- **`googlePlaceCache/{googlePlaceId}`** — `name`, `lat`, `lng`, `ourPlaceId?` (P2).
- **`waitlist/{id}`** — email, `createdAt` (landing page).
- **Storage** — `chat-images/{uid}/{file}`, images only, under 5 MB.
- **Security rules** — signed-in users read events, places and their own chats; clients write only their own `users/{uid}` and Storage folder; events, places and chats are written only by Functions. App Check on Functions.

## Key integrations
- **Gemini API** (a Gemini 3.5 Flash-or-later model, pinned after the hour-0 spike) — via `@google/genai` in `assistantChat`. Tools: Google Search, Google Maps (with the user's location, or the city centre 54.6872, 25.2797), and ours: `search_places(category, open_now?)`, `show_on_map(place_ids)`, `get_dog_profile()`, `flag_urgent(reason)`. Loop of up to 4 steps. Fallback if the combined-tools preview fails: one grounded call, then one function-calling call.
- **Map pins** — one shape: `{key, source: ours|google, title, lat, lng, category?, ourPlaceId?, googlePlaceId?, mapsUri?}`. Our places pin directly. Google-only places need Places API Place Details for coordinates (P2); until then they show as source cards with an "Open in Google Maps" link. "Show on map" switches to the Map tab and fits the camera to the pins.
- **3D bridge** — JS → app on a channel named `BP`: `ready`, `tapSlot`, `error`. App → JS: `bp.setScene(json)` once, `bp.addAttendee(json)` for each new attendee (plays the walk-in), `bp.removeAttendee(uid)`. The app listens to the event doc and sends only the changes.
- **Scene type** — preset spots carry their type. A dropped pin uses one Overpass query: landmark (historic or attraction within 60 m) → riverside (river or water within 100 m) → forest → park → old town (inside a hard-coded polygon) → street. 6-second timeout, then "park".
- **Weather** — Open-Meteo hourly forecast for the start hour, no key, fetched once at create.
- **Analytics** — Firebase Analytics events (walk created, walk joined, assistant message, show on map, place opened).

## Constraints & non-functional needs
- 24-hour build; must run on a real iPhone for the demo.
- 3D preview loads in under 3 seconds and runs smoothly: pixel ratio max 2, low-poly, few lights, stop rendering when hidden.
- Assistant answers in under 10 seconds; progress shown while waiting.
- Health safety: urgency banner, red-flag rule in server code, fixed disclaimer, emergency pin only from the hand-checked list.
- API keys only in Functions secrets; the iOS Maps key restricted to our bundle id; budget alert on the project.
- Google Maps grounding display rules: sources right after the answer, "Google Maps" label unchanged.

## Known risks & tech debt
- **Risks (de-risk in hours 0–2):** iOS build and signing; the Gemini combined-tools preview; Three.js speed in a WebView on the phone; Overpass being slow (presets avoid it in the demo).
- **Debt we accept on purpose:** anonymous auth (no account recovery); attendees inside the event doc (fine for groups of 4); all places loaded on the phone (fine under ~2,000); exact start points are visible to all signed-in users.

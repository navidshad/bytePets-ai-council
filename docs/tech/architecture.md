# Technical Architecture — BytePets

> Living doc. The current shape of the system at a high level. The *why* behind specific choices lives in `../../decisions/adr/`. Changing this doc is a council-level change (see `AGENTS.md` → "Editing rules for living docs").

## Overview
A mobile-first web app (Vue 3 + Vite, PWA; ADR-003) on Firebase Hosting talks to Firebase. The app reads Firestore directly. **Every write goes through a callable Cloud Function**, with App Check and per-user limits. A server-side trust rule turns confirms and reports into a badge. Lost and found posts are matched on the server; Gemini reads the photos (ADR-002). Walk-Mate walks start at walking areas and open a Three.js 3D preview inside the app. The app is in English and Lithuanian. Place data is imported from the three sources in the brief by laptop scripts. Every place and post has a public URL.

```
Phone browser (Vue PWA, Leaflet + OSM tiles)
  ├─ reads ─────────────► Firestore (places, lostFound, matches, walks, stats)
  ├─ calls ─────────────► Cloud Functions (callable, App Check)
  │                         addPlace · votePlace · createLostPost · updateLostPost
  │                         createWalk · joinWalk · saveProfile
  │                         sendLostMessage · respondMatch · reportLostPost · aiExtract · assistantReport
  │                           └─ Gemini (photo features, photo compare, post parsing)
  ├─ uploads photos ────► Firebase Storage
  ├─ 3D walk preview ───► Three.js scene (bundled, lazy-loaded on the walk page)
  └─ /p/{id}, /l/{id} ──► Hosting rewrite → ogPage Function (link previews, P1)
Firestore triggers: onLostPostWritten → matchLostFound → notify (in-app + email)
Scheduled: nightlyTrust (P2), expireLostPosts
Laptop scripts: import-places, seed-demo
```

## Components
- **Web app (Vue 3, Vite, Pinia, Vue Router, Firebase JS SDK, Leaflet, `vite-plugin-pwa`)** — bottom bar: Map · Walks · Lost & found · Add · Me. The Lost & found tab and the home map both show the two big buttons "I lost a pet" / "I found a pet". Routes: `/` map, `/list`, `/p/:id`, `/l/:id`, `/add`, `/lost-found`, `/lost-found/new?kind=lost|found`, `/assistant`, `/walks`, `/w/:id` (walk + 3D), `/walks/new`, `/matches`, `/me`, `/about` (how we rate info and live counters), `/emergency`. Mobile first; works on iPhone Safari and Android Chrome. Text in English and Lithuanian with `vue-i18n` (`src/locales/en.json`, `lt.json`); the language follows the phone, with an EN / LT switch, and is saved on the user.
- **Cloud Functions (2nd gen, Node 20, `europe-west1`)** — the callables listed above, all with `enforceAppCheck: true`. `aiExtract` and `matchLostFound` have `minInstances: 1` during the demo.
- **Auth** — Firebase Auth. Browse with no sign-in. Writes need **Google sign-in** (the Function checks `auth.token.firebase.sign_in_provider == "google.com"`).
- **Web app rules (ADR-003)** — "Open in your browser to post" inside Messenger and Facebook in-app browsers; `signInWithPopup` with `authDomain` on our Hosting domain; photos shrunk and redrawn on a canvas in the browser (strips EXIF and GPS) before upload; service worker on `autoUpdate` with no offline data; App Check debug token on localhost; MapTiler key with the OSM credit.
- **Email** — Firebase "Trigger Email" extension writing to a `mail` collection (SMTP via a free-tier provider, picked and inbox-tested in hours 0–2). Used only for match notices; never carries the other person's contact details.
- **Scripts (laptop, not deployed)** — `import-places` (each source → a committed GeoJSON snapshot → upsert to Firestore with stable ids) and `seed-demo`.
- **3D walk preview** — the Three.js scene from `docs/product/prototypes/walkmate-3d-preview.html`, ported into a Vue component (`WalkScene.vue`) and lazy-loaded only on `/w/:id`, so the map stays light. Scene types in P0: park, riverside, old town (forest if time). Weather look from the time of day. Pixel ratio max 2, low-poly, stop rendering when the tab is hidden.

## Data

**`places/{placeId}`** — stable ids per source: `vln_area_07`, `osm_node_123`, `vmvt_456`, `man_001`, `usr_<auto>`.
- `name`, `category: vet | emergency_vet | vet_pharmacy | pet_shop | pet_friendly | walking_area | groomer`, `subcategory?` (`cafe | restaurant | bar | shop | hotel | other`)
- `petTypes[]: dog | cat | any`; `facts: {indoorsOk?, terraceOnly?, waterBowl?, leashRequired?, fenced?, offLeadOk?}`
- `geo: {lat, lng}` — every place is a pin, including walking areas (centre point). No outlines.
- `address?`, `phone?`, `website?`, `openingHours?`, `open24h`
- `origin: official | imported | community`; `source: {name, url?, fetchedAt?}`; `createdBy?`, `createdAt`
- `status: active | hidden | closed`
- `lastConfirmedAt?`, `confirms90d`, `reports90d`, `topReportReason?`
- `trust: {level, computedAt}` — written only by Functions

**`places/{placeId}/votes/{uid}`** — `kind: confirm | report`, `reason?: closed | moved | not_pet_friendly | wrong_hours | wrong_info | other`, `note?` (≤ 200 chars), `createdAt`, `updatedAt`. The doc id is the user id, so there is one vote per user.

**`lostFound/{postId}`**
- `kind: lost | found`, `species: dog | cat | other`, `petName?`, `size: S | M | L`, `colors[]`, `description` (≤ 500, phone numbers and emails removed)
- `photoPaths[]` (`lost-found/{uid}/{postId}/…`, images only, < 5 MB, up to 3)
- `features` — `{breedGuess?, colors[], pattern?, markings[], collar: {has, color?}, coat?, ears?, tail?, source: form | ai, aiModel?}`
- `lastSeen: {lat, lng, label}` rounded to 3 decimals (~100 m); `geohash5`
- `seenAt`, `createdAt`, `expiresAt` (+30 days)
- `status: open | reunited | closed | hidden`; `ownerUid`; `ownerName` (first name); `reportCount`

**`lostFound/{postId}/messages/{msgId}`** — `fromUid`, `fromName`, `text` (≤ 300), `createdAt`. The owner reads all; a sender reads only their own.

**`matches/{lostId_foundId}`** — the id is the pair, so a pair is never suggested twice.
- `lostId`, `foundId`, `lostOwnerUid`, `foundOwnerUid`, `score` (0–1), `reasons[]` (short text), `method: rules | rules+ai`
- `lostAnswer`, `foundAnswer: pending | yes | no`
- `status: pending | confirmed | rejected`; `createdAt`
- `thread/{msgId}` — opens only when `status == confirmed`; both parties read and write via a Function.

**`users/{uid}`** — `firstName`, `lang: en | lt`, `dog?: {name, size: S|M|L, color, avatarSeed}`, `createdAt`. Written only through `saveProfile`.

**`walks/{walkId}`** — `areaId?` (a `walking_area` place) or `start: {lat, lng, label}` for a dropped pin; `areaName`; `hostUid`, `hostName`; `startsAt`, `day` (Vilnius date string); `maxSize` (2–4); `count`; `note?` (≤ 200); `scene: park | riverside | old_town | forest`; `attendees: {uid → {name, dogName, size, color, avatarSeed, joinedAt}}`; `status: open | full`. Wall query: `day in [today, tomorrow]`, ordered by `startsAt`. Attendees sit inside the walk doc, so one listener feeds the wall, the walk page and the 3D scene.

**`notifications/{uid}/items/{id}`** — `type: match | message`, `refId`, `read`, `createdAt`. Drives the in-app badge.

**`rateLimits/{uid}`** — daily counters per action. Functions only.

**`stats/public`** — counters for `/about` and the pitch: places by origin, fresh places, confirms this week, open posts, matches confirmed, reunions. Updated by Functions.

**Security rules** — public read: active `places`, open `lostFound` (not `messages`), `walks`, `stats`. Users read their own `notifications`, and `matches` / `thread` where they are a party. **No client writes** to any collection except their own Storage folder. App Check on Functions and Storage.

## Functions and their checks

| Function | Checks | Limit / user / day |
|---|---|---|
| `addPlace` | Google sign-in; inside the Vilnius box; name 2–80; category valid; duplicate: same category within 40 m and similar name → return the existing place | 10 |
| `votePlace` | place active; not your own place; change at most every 7 days; one transaction updates the vote, counters and `trust` | 50 |
| `createLostPost` | Google sign-in; inside greater Vilnius; photos in the caller's own folder; strip phone and email; round location | 3 |
| `updateLostPost` | owner only; `reunited` closes linked confirmed matches | — |
| `sendLostMessage` | not the owner; ≤ 300 chars; strip phone and email; ≤ 5 per sender per post | 20 |
| `respondMatch` | caller is a party; sets their answer; both `yes` → `confirmed`, open thread, notify; any `no` → `rejected` | 30 |
| `reportLostPost` | one per user; 3 reports → `hidden` | 20 |
| `saveProfile` | Google sign-in; first name 1–30; dog fields valid; `lang` | 20 |
| `createWalk` | Google sign-in; dog profile set; start is a `walking_area` place or a pin inside Vilnius; starts within 48 h; size 2–4; host is the first attendee; scene from the area (park) or the host's pick | 5 |
| `joinWalk` | Firestore transaction: not full, not already in, not the host, walk not past; adds the attendee, updates `count` and `status` | 10 |
| `aiExtract` | `mode: photo_features | parse_post`; returns JSON only; never writes posts | 20 |
| `assistantReport` | multi-turn (history sent by the client, max 6 turns); returns `{reply, draft, missing[], done}`; never writes posts; red-flag health words → returns the emergency card | 30 |

## Trust rule (implementation)
One pure function `computeTrust(place, votes, now)` in `functions/src/trust.ts`. All thresholds are constants at the top of the file, and the same numbers are shown on `/about`. It runs inside the `votePlace` transaction. A nightly scheduled job (P2) moves untouched **Imported and Community** places to `stale` (180 days with no confirm, or since import). Official items never go stale; the monthly re-import refreshes them. Lost & found posts are not places; `expireLostPosts` closes them after 30 days. until then, the app shows `stale` based on `lastConfirmedAt`, while the server value stays the source of truth. Order of checks: hidden → disputed → confirmed → official → stale → unverified. The rule itself is in Council 002.

## 3D bridge (web)
`WalkScene.vue` wraps the prototype's scene code. It takes the walk doc as a prop and exposes `setScene(walk)` once, `addAttendee(a)` for each new attendee (plays the walk-in) and `removeAttendee(uid)`. The walk page listens to `walks/{id}` and passes only the changes, so a join on one phone animates on every other phone. Taps on a "?" ghost emit `tapSlot`, which opens Join. No WebView or postMessage is needed on the web.

## Languages
- `vue-i18n` with `en.json` and `lt.json`; no hard-coded strings in components. A missing key falls back to English and is logged in development.
- Server text (emails, trust labels in `stats`, assistant replies, AI match reasons) uses the user's `lang`. Gemini is told to answer in that language; structured fields stay as enum codes, and the app translates them.
- Dates, times and distances use `Intl` with `lt-LT` / `en-GB`.
- Place names, addresses and user posts are never translated.

## Lost ↔ found matching
1. **Features.** On the form, after photo upload, the app calls `aiExtract(photo_features)`. Gemini (pinned Flash model, `responseSchema`) returns `species`, `breedGuess`, `colors[]` (fixed list of 12), `pattern`, `markings[]`, `collar`, `coat`, `ears`, `tail`, `size`. The form is pre-filled and the user can fix it. Without AI, the user fills species, size and colours by hand.
2. **Candidates.** The trigger `onLostPostWritten` (on create, or when features change) queries open posts of the other kind with the same species and `geohash5` neighbours (about 5 km), and the time rule: found no earlier than 1 day before lost, both under 30 days old. Expect fewer than 50 candidates.
3. **Rule score (always).** Weighted sum: colours overlap 0.30, size 0.15, markings 0.20, collar 0.10, distance 0.15 (1 at 0 km → 0 at 5 km), time gap 0.10. Breed is only a small bonus, because guesses are often wrong.
4. **AI compare (P1).** For the top 5 by rule score, one Gemini call with both photos: "Could these be the same animal? Answer JSON {sameAnimalLikelihood 0–1, reasons[] max 3, conflicts[]}". Final score = 0.5 rule + 0.5 AI. Any hard conflict (different species, clearly different coat colour) → drop.
5. **Create matches.** Up to 3 per post with a score ≥ 0.6 (tuned on the 10 test pairs in hour 0–2). Write `matches/{lostId_foundId}` only if it does not exist.
6. **Notify.** Both owners get a `notifications` item and an email: "Possible match for your lost dog near Žvėrynas. Open BytePets to check." The email has no photo, no location detail and no contact data.
7. **Confirm.** `respondMatch` per side. Both yes → thread opens. Any no → rejected forever. The AI's reasons are shown as "why we think so", always with the label "Possible match".

**Assistant intake.** `assistantReport` uses Gemini with `responseSchema` for the same `lostFound` fields. Each turn returns a short reply, the current draft and the list of missing fields (where, when, photo). The client shows the draft as a post card. On "Post", the client calls `createLostPost` with the draft, so the same checks and matching apply. The model is told that user text is data, not instructions.

**Limits and safety:** Gemini sees only the post photos, never user profiles. Photos of people are discouraged in the form. Cost is bounded: one features call per post plus at most 5 compare calls. A 30-second timeout falls back to the rule score.

## Data import
All scripts write `data/snapshots/{source}.geojson` (committed) and then upsert to Firestore with stable ids. Each source gets 60 minutes, then the fallback. Sources checked on 2026-10-09.

- **Walking areas (official).** City ArcGIS MapServer `Laisvalaikis_public`, layer 16 (existing, 35), 17 (being built, 4), 18 (planned, 8):
  `https://gis.vplanas.lt/arcgis/rest/services/Interaktyvus_zemelapis2/Laisvalaikis_public/MapServer/16/query?where=1%3D1&outFields=*&outSR=4326&f=geojson`
  Polygons in the source, ~20 KB; we keep only the centre point. Fields: `VIETA` (place text), `ETAPAS` (stage), `KITI_IRENG` (equipment). Ids `vln_area_{layer}_{OBJECTID}`, `origin: official`. Layers 17–18 get `status: planned` and show as "coming soon". Store the centre (`turf.centroid`) in `geo`; outlines are not stored. No licence stated: credit "© Vilniaus miesto savivaldybė, SĮ Vilniaus planas".
- **Vets and vet pharmacies (official).** VMVT register, data.gov.lt dataset 5258 (CC BY 4.0, monthly). **Always filter on the server**; the full set is ~100 MB:
  `https://get.data.gov.lt/datasets/gov/vmvt/okis_subjektai/Subjektas?veiklos_tipas.contains("eterinar")&limit(5000)` (add `&format(csv)` for CSV), then keep Vilnius city addresses and active rows (~46). WGS84 coordinates are included, so no geocoding. Map practice premises and service providers → `vet`; retail vet pharmacies → `vet_pharmacy`; skip wholesalers. Show the business name, address and phone only. Never show emails, and skip rows marked `CENZŪRUOTA`.
- **OpenStreetMap (imported).** Overpass, Vilnius city area. Send a User-Agent; if overpass-api.de is busy, use the mirror `https://maps.mail.ru/osm/tools/overpass/api/interpreter`.
  ```
  [out:json][timeout:90];area(id:3600968952)->.a;
  (nwr["amenity"="veterinary"](area.a);nwr["shop"="pet"](area.a);
   nwr["leisure"="dog_park"](area.a);nwr["dog"~"yes|leashed"](area.a););out tags center;
  ```
  Gives ~32 vets, 48 pet shops, 26 dog parks, 17 `dog=yes|leashed`. Dedupe against official rows: same category within 60 m (areas) or 40 m with a similar name (vets). Credit "© OpenStreetMap contributors" (ODbL).
- **24/7 vets.** Checked by phone; `origin: imported`, `source.name: "Checked by BytePets team, Oct 2026"`, `category: emergency_vet`.
- **Pet-friendly (seed).** A hand-made list of 30–50 places from venue websites and public guides, each with `source.url`; `origin: imported`, trust `unverified`. No Facebook, Google Places or booking-site data.
- **Optional layer (P2).** Registered pets per street from data.gov.lt dataset 292 (CC BY 4.0, monthly CSV, `;`-separated) → "dogs per neighbourhood" on `/about`.

## Key integrations
- **Gemini API** via `@google/genai` in Functions (ADR-002). Phase 1 uses structured output for photo features, photo compare and post parsing. The model id is pinned after the hour-0 spike. The health chat with Search and Maps grounding is Phase 2.
- **Leaflet + MapTiler tiles** (OpenStreetMap data and credit). Google Maps content is never drawn on this map (Google terms).
- **Directions** — links to Apple Maps on iOS and Google Maps elsewhere (`geo:` / `maps.apple.com` / `google.com/maps/dir`).
- **Analytics** — Firebase Analytics events: `place_added`, `place_confirmed`, `place_reported`, `lost_post_created`, `match_suggested`, `match_confirmed`, `reunited`, `share_tapped`, `emergency_opened`, `walk_created`, `walk_joined`, `walk_3d_opened`, `lang_switched`.

## Constraints & non-functional needs
- 24-hour build; must work on judges' phones from a QR code (iPhone Safari and Android Chrome).
- Map with a few hundred places loads in under 3 seconds on 4G.
- 3D walk preview loads in under 3 seconds on a mid-range phone and runs smoothly.
- Matching result within 15 seconds of posting; the app shows "Looking for matches…".
- Privacy: rounded locations, no public phone or email, contact only after a two-sided yes, posts expire after 30 days, user can delete their post.
- Keys only in Functions secrets; budget alert on the project; App Check everywhere.

## Known risks & tech debt
- **Risks (de-risk in hours 0–2):** Gemini telling the same pet apart across two different photos (test 10 real pairs); team speed in Vue; Three.js speed in mobile Safari; whether official datasets exist; App Check reCAPTCHA on iPhone Safari.
- **Debt we accept on purpose:** no push (email + in-app only); team members review hidden items by hand; all places loaded on the phone (fine under ~2,000); Google sign-in only; attendees inside the walk doc (fine for groups of 4).

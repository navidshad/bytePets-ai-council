# Technical Architecture — BytePets

> Living doc. The current shape of the system at a high level. The *why* behind specific choices lives in `../../decisions/adr/`. Changing this doc is a council-level change (see `AGENTS.md` → "Editing rules for living docs").

## Overview
A mobile-first web app (Vue 3 + Vite, PWA; ADR-003) on Firebase Hosting talks to Firebase. The app reads Firestore directly. **Every write goes through a callable Cloud Function**, with App Check and per-user limits. A server-side trust rule turns confirms and reports into a badge. Lost and found posts are matched on the server; Gemini reads the photos (ADR-002). Place data is imported from the three sources in the brief by laptop scripts. Every place and post has a public URL.

```
Phone browser (Vue PWA, Leaflet + OSM tiles)
  ├─ reads ─────────────► Firestore (places, lostFound, matches, stats)
  ├─ calls ─────────────► Cloud Functions (callable, App Check)
  │                         addPlace · votePlace · createLostPost · updateLostPost
  │                         sendLostMessage · respondMatch · reportLostPost · aiExtract · assistantReport
  │                           └─ Gemini (photo features, photo compare, post parsing)
  ├─ uploads photos ────► Firebase Storage
  └─ /p/{id}, /l/{id} ──► Hosting rewrite → ogPage Function (link previews, P1)
Firestore triggers: onLostPostWritten → matchLostFound → notify (in-app + email)
Scheduled: nightlyTrust (P2), expireLostPosts
Laptop scripts: import-places, seed-demo
```

## Components
- **Web app (Vue 3, Vite, Pinia, Vue Router, Firebase JS SDK, Leaflet, `vite-plugin-pwa`)** — bottom bar: Map · Lost & found · Add · Me. The Lost & found tab and the home map both show the two big buttons "I lost a pet" / "I found a pet". Routes: `/` map, `/list`, `/p/:id`, `/l/:id`, `/add`, `/lost-found`, `/lost-found/new?kind=lost|found`, `/assistant`, `/matches`, `/me`, `/about` (how we rate info and live counters), `/emergency`. Mobile first; works on iPhone Safari and Android Chrome.
- **Cloud Functions (2nd gen, Node 20, `europe-west1`)** — the callables listed above, all with `enforceAppCheck: true`. `aiExtract` and `matchLostFound` have `minInstances: 1` during the demo.
- **Auth** — Firebase Auth. Browse with no sign-in. Writes need **Google sign-in** (the Function checks `auth.token.firebase.sign_in_provider == "google.com"`).
- **Web app rules (ADR-003)** — "Open in your browser to post" inside Messenger and Facebook in-app browsers; `signInWithPopup` with `authDomain` on our Hosting domain; photos shrunk and redrawn on a canvas in the browser (strips EXIF and GPS) before upload; service worker on `autoUpdate` with no offline data; App Check debug token on localhost; MapTiler key with the OSM credit.
- **Email** — Firebase "Trigger Email" extension writing to a `mail` collection (SMTP via a free-tier provider, picked and inbox-tested in hours 0–2). Used only for match notices; never carries the other person's contact details.
- **Scripts (laptop, not deployed)** — `import-places` (each source → a committed GeoJSON snapshot → upsert to Firestore with stable ids) and `seed-demo`.
- **3D prototype** — `docs/product/prototypes/walkmate-3d-preview.html`, shown only in the pitch as "what's next". Not part of the build.

## Data

**`places/{placeId}`** — stable ids per source: `vln_area_07`, `osm_node_123`, `vmvt_456`, `man_001`, `usr_<auto>`.
- `name`, `category: vet | emergency_vet | vet_pharmacy | pet_shop | pet_friendly | walking_area | groomer`, `subcategory?` (`cafe | restaurant | bar | shop | hotel | other`)
- `petTypes[]: dog | cat | any`; `facts: {indoorsOk?, terraceOnly?, waterBowl?, leashRequired?, fenced?, offLeadOk?}`
- `geo: {lat, lng}` (centre for areas); `shape?: GeoPoint[]` (P2, under 50 points)
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

**`notifications/{uid}/items/{id}`** — `type: match | message`, `refId`, `read`, `createdAt`. Drives the in-app badge.

**`rateLimits/{uid}`** — daily counters per action. Functions only.

**`stats/public`** — counters for `/about` and the pitch: places by origin, fresh places, confirms this week, open posts, matches confirmed, reunions. Updated by Functions.

**Security rules** — public read: active `places`, open `lostFound` (not `messages`), `stats`. Users read their own `notifications`, and `matches` / `thread` where they are a party. **No client writes** to any collection except their own Storage folder. App Check on Functions and Storage.

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
| `aiExtract` | `mode: photo_features | parse_post`; returns JSON only; never writes posts | 20 |
| `assistantReport` | multi-turn (history sent by the client, max 6 turns); returns `{reply, draft, missing[], done}`; never writes posts; red-flag health words → returns the emergency card | 30 |

## Trust rule (implementation)
One pure function `computeTrust(place, votes, now)` in `functions/src/trust.ts`. All thresholds are constants at the top of the file, and the same numbers are shown on `/about`. It runs inside the `votePlace` transaction. A nightly scheduled job (P2) moves untouched places to `stale`; until then, the app shows `stale` based on `lastConfirmedAt`, while the server value stays the source of truth. Order of checks: hidden → disputed → confirmed → official → stale → unverified. The rule itself is in Council 002.

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
All scripts write `data/snapshots/{source}.geojson` (committed) and then upsert to Firestore. Each source gets 60 minutes, then the fallback.
- **Walking areas:** city open data / GIS layer (`origin: official`) → else OSM `leisure=dog_park` via Overpass (`imported`), deduped against the city list within 60 m.
- **Vets and pharmacies:** OSM `amenity=veterinary`, `shop=pet` (`imported`); the VMVT register if it can be exported, geocoded with Nominatim at 1 request per second (`official`); 24/7 vets checked by phone (`imported`, `source.name: "Checked by BytePets team, Oct 2026"`).
- **Pet-friendly:** OSM `dog=yes|leashed` plus a hand-made list with a `source.url` for each place (`imported`, starts unverified). No Facebook scraping; no stored Google Places data.

## Key integrations
- **Gemini API** via `@google/genai` in Functions (ADR-002). Phase 1 uses structured output for photo features, photo compare and post parsing. The model id is pinned after the hour-0 spike. The health chat with Search and Maps grounding is Phase 2.
- **Leaflet + MapTiler tiles** (OpenStreetMap data and credit). Google Maps content is never drawn on this map (Google terms).
- **Directions** — links to Apple Maps on iOS and Google Maps elsewhere (`geo:` / `maps.apple.com` / `google.com/maps/dir`).
- **Analytics** — Firebase Analytics events: `place_added`, `place_confirmed`, `place_reported`, `lost_post_created`, `match_suggested`, `match_confirmed`, `reunited`, `share_tapped`, `emergency_opened`.

## Constraints & non-functional needs
- 24-hour build; must work on judges' phones from a QR code (iPhone Safari and Android Chrome).
- Map with a few hundred places loads in under 3 seconds on 4G.
- Matching result within 15 seconds of posting; the app shows "Looking for matches…".
- Privacy: rounded locations, no public phone or email, contact only after a two-sided yes, posts expire after 30 days, user can delete their post.
- Keys only in Functions secrets; budget alert on the project; App Check everywhere.

## Known risks & tech debt
- **Risks (de-risk in hours 0–2):** Gemini telling the same pet apart across two different photos (test 10 real pairs); team speed in Vue; whether official datasets exist; App Check reCAPTCHA on iPhone Safari.
- **Debt we accept on purpose:** no push (email + in-app only); team members review hidden items by hand; all places loaded on the phone (fine under ~2,000); Google sign-in only.

# ADR-003: Build the app as a mobile web app (PWA), not a native iPhone app

**Status**: Accepted
**Date**: 2026-10-09
**Author**: Navid Shad (drafted with Claude)
**Supersedes**: ADR-001

---

## Context

ADR-001 chose a Flutter iPhone app. It was written for a scope with Walk-Mate as the hero. After reading the official challenge text, Council 002 re-scoped BytePets to a community-checked map for pet owners. The brief's verbs are find, add, verify and share, and it names lost and found pets.

Three things now matter more than native polish:

1. **Share must work for people with no app.** A lost-pet post is useless if the neighbour who gets the link in Messenger must install something first. With a native app we would need public web pages for every place and post anyway, so we would build two front ends.
2. **Judges take part in the demo.** In the hero moment, a judge scans a QR code and taps "Still true" on their own phone, Android or iPhone. A native iPhone build can't do that. The If team will also open the link after the event, and nobody installs a TestFlight build for that.
3. **We have 24 hours.** Apple signing, provisioning and installing on a real device was the biggest risk in hours 0–2. The new brief asks for none of it.

What we need from the device is simple on the web: camera or photo upload (`<input type="file" accept="image/*" capture>`), location (`navigator.geolocation`, which needs HTTPS; Firebase Hosting gives us that), a map, and the system share sheet (`navigator.share`).

---

## Decision

We build BytePets as a **mobile-first web app (PWA)**: **Vue 3 + Vite**, the **Firebase JS SDK** (Auth, Firestore, Storage, Functions, App Check with reCAPTCHA Enterprise), **Leaflet** with OpenStreetMap tiles for the map, and `vite-plugin-pwa` for "Add to Home Screen". It is hosted on **Firebase Hosting** at one URL. Every place and lost or found post has a public route (`/p/{id}`, `/l/{id}`). A Hosting rewrite sends those routes to a small Function, `ogPage`, which adds link-preview tags (P1). The landing page is the app's own "About" route, not a separate site. The backend (Firestore, callable Functions, Gemini per ADR-002) does not change.

Rules that come with it:
- **Sign-in in in-app browsers.** Links opened from Messenger or Facebook load in their in-app browser, where Google blocks sign-in. Reading works there. Before any write, the app shows "Open in your browser to post". Sign-in uses `signInWithPopup`, with `authDomain` set to our Hosting domain so it works on iPhone Safari.
- **Photos.** The browser shrinks each photo (about 1600 px, under 1 MB) and redraws it on a canvas before upload. This strips the EXIF data, including the exact GPS spot.
- **Service worker.** `registerType: 'autoUpdate'`, no offline caching of data, and the PWA plugin is turned on last. A stale build must never show in the demo.
- **App Check.** A debug token on localhost. Enforcement is turned on only after the full demo flow passes with it.
- **Map tiles.** A MapTiler (or Stadia) free key from day one, with the OpenStreetMap credit shown.

This depends on one check in hour 0: at least two people on the team can write Vue/JS quickly. If not, we keep Flutter for the app (ADR-001's setup) and build `/p/{id}` and `/l/{id}` as plain HTML pages on Hosting, so share links still work.

---

## Alternatives Considered

### Alternative A — Keep the Flutter iPhone app (ADR-001) and add web share pages
**What it is**: The native app as planned, plus plain HTML pages on Hosting for shared links.
**Why we considered it**: Native feel, and the team planned for Flutter. Share links would still open.
**Why we rejected it**: It means two front ends in 24 hours. Judges can't join the demo on Android or without an install. The iOS signing risk stays for no gain against the brief. We keep it only as the fallback if the team can't write Vue.

### Alternative B — Flutter web
**What it is**: The same Flutter code, compiled for the browser.
**Why we considered it**: One codebase for the iPhone and the web.
**Why we rejected it**: The first load is several MB, which is slow on a phone opening a shared link. Link previews and SEO are weak. Text and scrolling feel less like a normal web page.

### Alternative C — Server-rendered site (e.g. Nuxt with SSR on Cloud Run or Functions)
**What it is**: Pages rendered on the server, so every link has full preview tags.
**Why we considered it**: Best link previews and SEO.
**Why we rejected it**: More moving parts (server rendering plus hydration) than we can afford in 24 hours. One small `ogPage` Function gives us the previews that matter.

---

## Consequences

### Positive
- One front end that runs on every phone. Share links work for everyone.
- Judges and If staff can try it from a QR code.
- No Apple account, signing or device install on the critical path.
- The Walk-Mate 3D prototype (Three.js) runs as is if we show it, with no WebView bridge.
- One `firebase deploy` ships everything.

### Negative
- No push we can rely on: web push on iPhone works only after "Add to Home Screen". Match notices go by email and an in-app badge instead.
- Less native feel. No App Store presence for now.
- OpenStreetMap's public tile server is fine for a demo, but real use needs a tile provider key (for example MapTiler or Stadia, which have free tiers).

### Neutral / Notable
- ADR-002 stays in force. Callable Functions work the same from the web SDK.
- A native wrapper (Capacitor) or a Flutter app can come later if push or store presence matter. The backend does not change.
- Google's terms don't allow Google Maps content on a non-Google map. When the AI health chat returns (Phase 2), its Google Maps results show as cards with links, never as pins on our Leaflet map. ADR-002's "pin Google-only places" step is dropped.
- `ogPage` returns the same page to every visitor and is cached at the Hosting CDN, so a cold start can't time out the Facebook crawler.

---

## Architect Review

**Verdict: Approve with changes. The web app is the right call, but sign-in and share links have gaps the ADR doesn't name.**

- **The trade-offs are honest**, and the hour-0 Vue check is sound.
- **Biggest gap: Google sign-in inside Messenger and Facebook.** Google blocks sign-in in their in-app browsers. Show an "Open in browser" prompt before any write. On iPhone Safari, use `signInWithPopup`, or make `authDomain` match the Hosting domain. Redirect sign-in breaks there.
- **Remove photo location data.** iPhone photos carry exact GPS. Shrink each photo and strip that data in the browser before upload, or the "rounded location" promise is broken.
- **The service worker can serve an old build.** Turn on auto-update, or add the PWA plugin last. No offline mode needed for P0.
- **Link previews:** `ogPage` must return the same page to every visitor. Cache it on Hosting so a cold start doesn't time out the Facebook crawler.
- **App Check:** add a localhost debug token. Turn on enforcement only after the demo flow passes.
- **Maps terms:** Google's terms don't allow Google place content on a Leaflet/OSM map. When the AI chat returns, its Maps results show as cards and links only. ADR-002's "pin Google-only places" step must go.
- **Email:** pick the sender now (Trigger Email extension plus a provider). Test that it lands in the inbox, not spam. Never put the other person's contact in the email.
- **Tiles:** get the MapTiler key now. Keep the OSM credit.

---

## References

- Council 002: `decisions/council/002-rescope-to-challenge-brief.md`
- Supersedes ADR-001: `decisions/adr/001-flutter-for-iphone-app.md`
- Related: ADR-002 (Gemini on Cloud Functions)

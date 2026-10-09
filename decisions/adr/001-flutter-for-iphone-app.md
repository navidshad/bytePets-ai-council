# ADR-001: Build the iPhone app with Flutter

**Status**: Accepted
**Date**: 2026-10-09
**Author**: Navid Shad (drafted with Claude)

---

## Context

We have 24 hours at Hack4Vilnius (Challenge #6) to build an iPhone app and a landing page. The app has four parts: Walk-Mate events with a 3D preview, a dog-services map, an AI assistant chat with photos, and sign-in with a dog profile. Android is not needed for the MVP, but a real product in Vilnius would need it later.

We must pick between a native iPhone app (Swift and SwiftUI) and Flutter (Dart). Both can reach every part we need. The deciding forces are build speed in 24 hours, what the team already knows, and how well AI coding tools (Claude Code) write the code. The original proposal already named Flutter, Vue and Firebase, so the team expects Flutter.

Things both options share: an Apple developer account and Xcode on a Mac are needed to run on a real iPhone; Firebase has official SDKs for both; the 3D preview is a Three.js web page shown in a WebView, so it works the same in both.

---

## Decision

We build the iPhone app in **Flutter**, if the team confirms in the first hour that at least two people have built a Flutter screen before. If not, we switch to SwiftUI before any feature work; ADR-002 is not affected.

Packages: `firebase_core`, `firebase_auth` (anonymous sign-in), `cloud_firestore`, `firebase_storage`, `cloud_functions` (call the AI assistant and the event functions), `google_maps_flutter` for the map, `webview_flutter` for the 3D preview, `image_picker` for photos, and one state library (Riverpod or Provider). We pick `google_maps_flutter` over `flutter_map`: the Maps SDK for iOS is free for mobile maps, and Google's terms make it safer to show places that come from Gemini's Google Maps grounding on a Google map. We test only on iPhone.

Before the event: a paid Apple developer account is ready (a new one can take a day or two), and the demo iPhone is registered. Hour 0–1 of the event: a blank app with Firebase and anonymous sign-in runs on the demo iPhone, with camera and photo-library text in `Info.plist` and the iOS minimum version Firebase needs.

---

## Alternatives Considered

### Alternative A — Native SwiftUI
**What it is**: A Swift app with SwiftUI, MapKit for the map, WKWebView for the 3D preview, and the Firebase iOS SDK.
**Why we considered it**: MapKit is free, fast and looks native with very little code. Best iPhone feel and smallest app. AI tools write good SwiftUI.
**Why we rejected it**: The team planned Flutter and knows it better. Flutter hot reload is faster for UI changes during a 24-hour build. Android later would mean a second app.

### Alternative B — React Native (Expo)
**What it is**: A JavaScript app built with Expo.
**Why we considered it**: The team knows Vue and the web; Expo makes it easy to run on an iPhone without much Xcode work.
**Why we rejected it**: Nobody planned for it, and it adds a third stack next to Vue and Firebase. No clear speed gain over Flutter for this team.

### Alternative C — A mobile web app (PWA) in Vue
**What it is**: The whole app as a web page, added to the home screen.
**Why we considered it**: One codebase with the landing page; the 3D preview is already web code.
**Why we rejected it**: The brief asks for an iPhone app. Camera upload, push and maps feel weaker, and judges expect a real app.

---

## Consequences

### Positive
- Fast UI work with hot reload, one codebase, Android later at low cost.
- Matches the stack in the proposal, so no time is lost learning.

### Negative
- Google Maps in Flutter needs an API key (restricted to our bundle id) and about 15 minutes of setup.
- First iOS build of a Flutter app with Firebase (CocoaPods) can be slow. Do it in hour 1, not hour 20.

### Neutral / Notable
- The 3D preview stays a web page in a WebView, bundled as a Flutter asset so it works on bad venue Wi-Fi. A copy on Firebase Hosting feeds the landing page. It talks to the app with JavaScript messages (see `docs/tech/architecture.md`).
- Claude Code edits plain Dart files well; Xcode project files are harder for AI tools to edit safely. This favours Flutter.

---

## Architect Review

**Verdict: Flutter is the right call, if the team really knows it.** Team skill decides this. The ADR treats it as a fallback. Check it first: ask each person if they have built a Flutter screen.

Most trade-offs are honest. Two are weak:
- "Android later" does not matter in a 24-hour build. It is a bonus, not a reason.
- Hot reload is not a big edge. SwiftUI has live previews too.

Missing points:
- **Pick the map now.** Use `flutter_map` with OpenStreetMap tiles. No API key, no billing, and our places data already comes from OpenStreetMap. Remove the "or" from the decision. One check: if Gemini's Google Maps grounding (ADR-002) requires results on a Google map, read its terms first.
- **Apple account timing.** A new paid Apple developer account can take a day or two to approve. A free account works, but the build expires after 7 days and has limits. Sort this out before the event and register the demo iPhone.
- **AI coding tools.** This favors Flutter. Claude Code can run `flutter run` and edit plain Dart files. Xcode project files are hard for AI tools to edit safely.
- **iOS setup.** `image_picker` needs camera and photo text in Info.plist, or the app crashes. Set the iOS minimum version that Firebase needs.
- **3D page.** Host it on Firebase Hosting and load it by URL. Test it on the real iPhone early. WebView speed is the main risk.

---

## References

- Original Hack4Vilnius Challenge #6 proposal (Vue, Flutter, Firebase)
- Related: ADR-002 (AI assistant stack)

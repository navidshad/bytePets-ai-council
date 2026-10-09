# Hackathon Plan — BytePets at Hack4Vilnius

> Event plan for the 24-hour build, from `decisions/council/002-rescope-to-challenge-brief.md`. Scope lives in `prd.md`; the system lives in `../tech/architecture.md`. This doc is about time, people and the demo.

## Before the event
- Team check: can at least two people write Vue/JS fast? If not, apply the ADR-003 fallback (Flutter app plus plain web share pages).
- Firebase project on the Blaze plan with a budget alert; Gemini API key; MapTiler key; email provider for the Trigger Email extension.
- Data sources are found and checked (city walking areas, VMVT register, OSM). Run the three fetches once before the event and commit the snapshots (see `../tech/architecture.md` → "Data import").
- Hand-check 5–8 24/7 vets in Vilnius by phone (name, address, phone, hours).
- Collect 10 real lost/found photo pairs we may use (team pets, friends' pets, or freely licensed) for the matching test, and photos for the seed posts.
- If anyone from If is at the event, book 5 minutes with them in hour 1.

## Team tracks (3–4 people, each with Claude Code)
- **A — Backend and AI:** rules, Functions, trust rule, matching, Gemini, email.
- **B — App:** Vue shell, map and list, place card, add / confirm / report, sign-in, share.
- **C — Lost & found:** post form, photo pipeline, board, matches screen, messages.
- **D — Data, 3D and pitch:** the three imports (URLs are ready, so about 2 hours), then port the 3D scene and build Walk-Mate light with A; seed data, QR drive, slides.

Every track adds its strings to `en.json` and `lt.json` as it goes. One Lithuanian speaker checks `lt.json` at hour 18.

Freeze the data model as `types.ts` (shared by app and Functions) in hour 1. Changes go through person A.

## Timeline

| Hours | A — Backend/AI | B — App | C — Lost & found | D — Data/pitch |
|---|---|---|---|---|
| 0–2 | Rules and Functions skeleton; **Gemini photo-features spike on 10 test pairs**; email sender test | **Vue PWA deployed to Hosting**, Google sign-in on iPhone Safari, map with tiles | Photo resize + EXIF strip + upload to Storage | City areas + VMVT + Overpass fetches (URLs ready), 24/7 vet list; **3D prototype running on a real iPhone and Android in Safari/Chrome, measure speed** |
| 2–8 | `addPlace`, `votePlace`, `computeTrust`; `createLostPost`; `saveProfile`, `createWalk`, `editWalk`, `joinWalk`, `leaveWalk` | Map, filters, list, place card with badges, add form, confirm/report | Lost & found form, board, map layer, post page `/l/:id` | Imports, GeoJSON snapshots, seed list of pet-friendly places; `WalkScene.vue` port (park, riverside, old town) |
| 8–14 | `matchLostFound` (rules), `respondMatch`, notifications, email | Share sheet, `/p/:id`, emergency button, `/about` counters | Lost & found tab with the two big buttons, matches screen (yes/no), messages, reunited | Walks wall, create and edit walk, walk page with 3D, live join and leave on two phones; seed walks and demo posts, planted match pair; QR drive starts |
| **14** | **Checkpoint: add → confirm → badge turns green on a second phone; lost post → match → both confirm; join a walk → avatar walks in on the other phone. In EN and LT. Works on a judge-style phone. Or cut.** | | | |
| 14–20 | `aiExtract` features + photo compare in matching; tune the threshold | Empty/error states, "Open in your browser to post" | AI pre-filled form; assistant chat that takes a report and shows a draft card (`assistantReport` with A) | Confirm-after-join prompt, 3D polish and performance; `ogPage` previews; slides (2–3) |
| 20–24 | **Feature freeze.** Bug fixes, App Check enforcement on, record backup video, rehearse 3 times, charge phones, sleep in turns | | | |

## Cut line (cut from the top if behind at hour 14)
1. Assistant report chat (the two buttons and the form stay)
2. Link previews (`ogPage`) — links still work
3. AI photo compare — keep AI features, or rule matching only
4. Helper badges and "My contributions"
5. 3D scene types beyond park — park only
6. Email notices — in-app badge only

**Never cut:** the Lost & found tab with its two buttons; map with trust badges; add; confirm / report; lost & found post, match and two-sided confirm; share links; Google sign-in for writes; emergency button; walks wall → 3D preview → join and leave with the walk-in/out animation; create and edit a walk; English and Lithuanian.

## QR drive (real community proof)
From hour 10, a QR code on our table and on slide 1. Ask every team and mentor to add or confirm one place they really know. Track the counter on `/about`. Never fake names or confirms.

## Demo script (3 minutes)
Give the demo in English. Switch the app to LT once, for 2 seconds, during "Find".

1. **Problem (15 s).** Screenshots of scattered Facebook posts: "Is this café dog-friendly?", and a lost-dog post and a found-dog post for what looks like the same dog, in two different groups. "The info is scattered, stale, and you can't tell what's true."
2. **Find (20 s).** Open the map. Filter "Pet-friendly". A green card: "Confirmed by 4 owners · 5 days ago". A grey one: "Not checked for 6+ months". Tap EN → LT and back. "You see at once what you can trust, in your language."
3. **Add, verify, share (35 s): hero 1.** Phone A adds a café in 20 seconds; it shows grey. A judge scans the QR code and taps "Still true". The card turns green live on the big screen. Tap Share; the link opens in a plain browser.
4. **Lost & found (40 s): hero 2.** "Luna went missing in Žvėrynas yesterday" is already posted. Tap the big **"I found a pet"** button and post "small grey dog near Vingis Park" with a photo. The form fills itself from the photo. Seconds later, both phones show "Possible match: same white chest patch, red collar, 1.2 km away". Both tap "Yes, that's them", and a private thread opens. No phone number was shared until both said yes.
5. **Walk together (30 s): hero 3.** Open the Vingis Park walking area: "Official · city data", "2 walks this week". Tap tonight's walk: the 3D scene fills the screen, two dogs and two "?" spots. Tap Join, and a new avatar walks in. Hold up the second phone: it already shows "3 of 4". Then the prompt: "Is Vingis Park still OK for dogs?" → Yes. "Every walk keeps the map fresh."
6. **Emergency (10 s).** One tap: nearest checked 24/7 vet, Call, Directions.
7. **Why it stays true, and why If cares (30 s).** The six trust levels in one slide. Live counters: "Today, N people in this room added or confirmed M places." Faster vet access, more pets found, owners who walk and check together. 55,384 dogs in Vilnius; next: partners keep data fresh, and alerts by area.

One person drives the phone, one talks. Mirror the phone screen. Phone hotspot as Wi-Fi backup. Warm up the Functions before going on stage.

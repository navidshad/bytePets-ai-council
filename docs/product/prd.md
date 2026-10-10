# Product Requirements — BytePets

> Living doc. Hack4Vilnius 2026, Challenge #6 (If Insurance). Decisions: `decisions/council/005-mvp-rethink.md`, `decisions/council/006-walk-payments.md` (payments). Prototype: https://claude.ai/artifact/G4h1gwYUzUQdFJx66sXFvb

**What it is:** one map of Vilnius for dog owners. The city's data says where; owners say what's true now.
**Platform:** Flutter app (iOS first). English and Lithuanian.

## Features

| # | Feature | What it does | Done when |
|---|---|---|---|
| 1 | **Home map** | A calm, styled map of Vilnius with "you are here". Colour chips filter the map and act as the legend: Dog areas · Vets · Cafés · Lost & found · Walkers. Pins near the screen edges fade. | The map opens on the user's area and a chip shows only that kind of place |
| 2 | **Ask box** | Floats over the map. Shrinks to a paw button when the user moves the map; tap to bring it back. Answers with numbered cards and matching pins. Any action (post, book) shows a card the user confirms. | "Vet open now" returns cards and pins in one step |
| 3 | **Dog areas** | The city's 35 dog-walking areas. Filters: big dog, small dog, fenced, equipment, well rated. Each has a page: photos, reviews, tags, open reports. | "Big dog + fenced" shows only matching areas |
| 4 | **Report on the map** | For public spaces and anywhere: a problem or danger at a point (broken fence, poison bait, glass, aggressive dog, other). Location from the photo's GPS, or a pin. Shows at once as "reported by 1 owner". | A report from a photo lands where the photo was taken |
| 5 | **Still there?** | When someone is near an open report (about 150 m, app open), the app asks: Still there / Fixed / Not sure. 2 "still there" confirms it, 2 "fixed" resolves it. Reports expire: dangers after 48 h, damage after 30 days, unless confirmed. | A nearby user is asked, and their answer changes the report |
| 6 | **Reviews** | On place profiles (vets, cafés, restaurants, pet shops, dog areas): stars, short text, photo, tags. Plus "report wrong info" (closed, wrong hours, no longer dog-friendly). | A review shows on the profile and updates its rating |
| 7 | **Vets open now** | Clinics with opening hours, "checked on [date]", which animals they treat, reviews, and a Call button. | At 23:00 only open clinics show |
| 8 | **Dog-friendly places** | Mainly cafés and restaurants: dogs inside or terrace only, water bowl, dog menu, photos and reviews. | A café added by one owner shows on the map with its tags |
| 9 | **Lost & found** | Two buttons: **I lost a pet** / **I found a pet**. Report in three steps: photo, pet (dog / cat / other, size, colour), rough area and time. Board and map pins, share link, mark "reunited". | A report is posted in under 30 seconds |
| 10 | **Dog walkers** | **Dog walker mode:** a switch on Me (and a Dog walker button on the home map) adds the dog walker features, in purple so it never looks like owner mode (green). Onboarding once: an intro (how it works, what you earn, what owners see), a public profile (photo, rough area, price, walk length, dogs they take), private details (legal name, date of birth, 18+, phone check, experience with dogs), and **the dog walker promise**: 8 rules ticked one by one (dog card, lead, GPS on, bookings and payment only in the app, what to do if something goes wrong, cancels, pay and tax). Then free periods for the coming days, or "Available now" for a while. Before accepting, the dog walker reads the dog card (temperament, lead, health, the dog's vet). During a walk, "Something wrong?" links to the nearest vet open now, a lost alert and the owner. Owners find dog walkers on the map or in a list and book a time inside a free period; a booking blocks that time. The walker accepts or declines. Walker profile: rough area, tags (big dogs, reactive OK, cats), rating, walks done. | A walker sets a free period, an owner books inside it, and the walker accepts |
| 11 | **Live walk** | The walker taps **Start walk** (GPS on) and **End walk**. In between they send photos and short videos. The owner sees a "walk is live" bar on the home map, then the route, the updates and the walker's position. | The owner sees the walker move and a new photo arrive during the walk |
| 12 | **Walk chat** | Each walk has its own chat between owner and walker. It stays saved as the walk's history, with the route and the media. | After the walk, both can open the chat, route and media |
| 13 | **Share** | Every place, report, lost & found post and walker profile has a link that opens without the app. | A shared post opens in a phone browser |
| 14 | **Payments** | Demo money for now. The owner pays one price at booking; the money is held. Cancel free until 2 h before. 24 h after End walk the walker gets the price minus the BytePets fee (proposed 15%); a problem reported in that window stops it. Owner: Me → Payments (spent, each walk, receipt). Walker: Me → Earnings (on hold, on the way, paid out, fee per walk, year total). | A walk booked and ended shows in the owner's Payments, then moves to the walker's Paid out when the window ends |

## Rules
- **Privacy:** a walker's live position is visible only to the owner, and only during their booked walk. Lost & found shows a rough area (about 150 m), never an exact address. No phone numbers in public.
- **Trust:** colour shows a place's state; text shows how fresh it is ("confirmed 2 days ago"). The newest answers win.
- **Photo location:** read from the photo to place a report, then removed from the file before upload.
- **Sign-in:** browse without an account; sign in to report, review, post, book or chat.
- **Dog walkers:** the promise is stored on the server with its version and the time it was accepted; a new version asks again. Legal name, date of birth and phone are never shown to owners. The full dog walker terms need a legal review before real money.
- **Money:** price, fee, booking status and money records change only on the server, never on the phone. Amounts are whole cents. Every money move is a ledger entry that is never edited. Until a licensed provider holds real money, every money screen says "Demo money, no real payment".

## Out for now
Group walks and the 3D preview, AI photo matching for lost & found, real money (a licensed provider will hold it; ADR to come), push alerts by area, "Still there?" prompts while the app is closed, dog-care logging.

## Build plan (3 people)

**Step 1 — Base project (both developers, together, first).** Everything the features stand on, so the two tracks never block each other:
- Flutter app shell: navigation, the map-first home layout, empty screens for every feature.
- Design system in code: tokens as `ThemeData` + a `ThemeExtension`, and the shared widgets (Button, Chip, StatusPill, MapPin, BottomSheet, ListRow, ResultCard). Source: https://claude.ai/artifact/24xFqfY1jiSzN4HhK3pgxr
- Sign-in and profile: account, first name, one dog profile (name, size, photo). Offer Sign in with Apple next to Google: the App Store requires it when a third-party sign-in is offered.
- The map widget: styled map, pins, chips, "you are here", edge fade.
- Backend and data model: users, places, reviews, reports, lost & found posts, walks, messages, bookings, ledger and wallets; storage for photos and videos; access rules. A shared `Money` type (whole cents, EN/LT format).
- English and Lithuanian set up from the start.

**Step 2 — Two feature tracks, in parallel.**

| Track | Owner | Features |
|---|---|---|
| A · Places, reports & lost pets | Developer 1 | 3 Dog areas (import the city's 35), 4 Report on the map, 5 Still there?, 6 Reviews, 7 Vets open now, 8 Dog-friendly places, 9 Lost & found, 13 Share |
| B · Walks & payments | Developer 2 | 10 Walk assistants, 11 Live walk, 12 Walk chat, 14 Payments (booking states, 2 h and 24 h rules on the server, demo gateway) |
| Last · Ask box | Whoever finishes first | 2 Ask box: it searches what tracks A and B built |

**Step 3 — Landing page (third person, from day one).** One page in English and Lithuanian: what BytePets is, three screenshots from the UI, a waitlist or download link, privacy page. The same person can also check vet hours by phone and collect the first dog-friendly places.

Rules for working together: the data model and the shared widgets change only in the base project, by agreement; each feature lives in its own folder; one pull request per feature.

# Product Requirements — BytePets

> Living doc. Hack4Vilnius 2026, Challenge #6 (If Insurance). Decision: `decisions/council/005-mvp-rethink.md`. Prototype: https://claude.ai/artifact/G4h1gwYUzUQdFJx66sXFvb

**What it is:** one map of Vilnius for dog owners. The city's data says where; owners say what's true now.
**Platform:** Flutter app (iOS first). English and Lithuanian.

## Features

| # | Feature | What it does | Done when |
|---|---|---|---|
| 1 | **Home map** | A calm, styled map of Vilnius with "you are here". Colour chips filter the map and act as the legend: Dog areas · Vets · Cafés · Lost & found · Walkers. Pins near the screen edges fade. | The map opens on the user's area and a chip shows only that kind of place |
| 2 | **Ask box** | Floats over the map. Shrinks to a paw button when the user moves the map; tap to bring it back. Answers with numbered cards and matching pins. Any action (post, book) shows a card the user confirms. | "Vet open now" returns cards and pins in one step |
| 3 | **Dog areas** | The city's 35 dog-walking areas. Filters: big dog, small dog, fenced, equipment, well rated. Each has a page: photos, rating, tags, fence state, last check-in. | "Big dog + fenced" shows only matching areas |
| 4 | **Check-in** | On any place: stars, one photo, tags, fence OK / broken. Shows for everyone at once. | A check-in on one phone appears on another within seconds |
| 5 | **Vets open now** | Clinics with opening hours, "checked on [date]", which animals they treat, and a Call button. | At 23:00 only open clinics show |
| 6 | **Dog-friendly places** | Mainly cafés: dogs inside or terrace only, water bowl, dog menu, photo. | A café added by one owner is marked checked after a second check-in |
| 7 | **Lost & found** | Two buttons: **I lost a pet** / **I found a pet**. Report in three steps: photo, pet (dog / cat / other, size, colour), rough area and time. Board and map pins, share link, mark "reunited". | A report is posted in under 30 seconds |
| 8 | **Walk assistants** | People offer walk slots; owners book one. Walker profile: rough area, tags (big dogs, reactive OK, cats), rating, walks done. | An owner finds a walker nearby and books a slot |
| 9 | **Live walk** | During a booked walk the walker turns on GPS and sends photos and short videos. The owner sees the route, the updates and the walker's position live. | The owner sees the walker move and a new photo arrive during the walk |
| 10 | **Walk chat** | Each walk has its own chat between owner and walker. It stays saved as the walk's history, with the route and the media. | After the walk, both can open the chat, route and media |
| 11 | **Share** | Every place, lost & found post and walker profile has a link that opens without the app. | A shared post opens in a phone browser |

## Rules
- **Privacy:** a walker's live position is visible only to the owner, and only during their booked walk. Lost & found shows a rough area (about 150 m), never an exact address. No phone numbers in public.
- **Trust:** colour shows a place's state; text shows how fresh it is ("checked on 7 Oct").
- **Sign-in:** browse without an account; sign in to post, check in, book or chat.

## Out for now
Group walks and the 3D preview, AI photo matching for lost & found, payments in the app, push alerts by area, dog-care logging.

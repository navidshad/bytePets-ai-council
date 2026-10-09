# Product Requirements — BytePets

> Living doc. This is the current state of the product, not a decision record. Edit it as decisions land. Changing this doc is a council-level change (see `AGENTS.md` → "Editing rules for living docs").

**Phase**: Phase 1 — Hack4Vilnius MVP, 24-hour build. Scope set by `decisions/council/002-rescope-to-challenge-brief.md` (supersedes Council 001), amended by `003-walk-mate-3d-and-languages.md`. Platform: mobile web app (ADR-003).

## The challenge (Hack4Vilnius, challenger: If Insurance)
> How can we help pet owners find relevant and reliable information in Vilnius more easily? … Create a community-based solution that would help pet owners easily find, add, and verify relevant information in one place, share it with others, and contribute to making Vilnius more pet-friendly.

Named sources: Vilnius city dog walking areas; information about veterinary clinics and pharmacies; publicly posted information about pet-friendly places.

## Vision
Pet owners in Vilnius look for help in many scattered places: Facebook groups, forums, old websites. The info is often out of date, and you can't tell what is true. BytePets is **Vilnius's community-checked map for pet owners**. You can find a vet, a pharmacy, a pet-friendly place, a walking area or a lost pet, and see when someone last confirmed it. Anyone can add, confirm or flag info in two taps, and share it with one link. Owners can also plan a walk at a walking area and see it in 3D before they go. The app is in English and Lithuanian.

## Target users
- **Pet owners in Vilnius**, dogs first, then cats and others. New owners and people new to the city feel the gap most.
- **People who found an animal**, who often don't own a pet and will never install an app. They must be able to post and share from a browser.
- **Secondary:** the city (a live pet-friendly map), vets and shelters (fresh listings), If (prevention and trust).

## Problems we solve
| Job | Today | BytePets |
|---|---|---|
| "Can I bring my pet here?" | Ask in a Facebook group and wait | Pet-friendly places with rules ("inside OK", "terrace only") and a trust badge |
| "Where's a vet or pharmacy, and is it real and open?" | Google, old websites | Vets and pharmacies from official and open data, confirmed by owners; emergency button |
| "Where can I walk my dog?" | Word of mouth | City walking areas on the map, plus walks you can join there |
| "I'd like company on walks" | Don't know anyone | Walk-Mate: walks at walking areas, with a 3D preview |
| "My pet is lost" / "I found a pet" | Posts spread over many groups, and they never meet | One board, AI matching of lost with found, both sides told, one share link |
| "Is this info still true?" | No way to tell | Source, last-confirmed date and the number of confirms on every card |

## Scope at a glance

| Priority | Item |
|---|---|
| **Must (P0)** | Map and list, 5 groups, filters; trust badge and freshness line; add a place; confirm / report; lost & found tab with two big buttons ("I lost a pet" / "I found a pet") and a board; lost ↔ found matching with two-sided confirm and notices; public share links; Google sign-in to write; emergency button; imports from the three named sources; "How we rate info" page with live counters; **Walk-Mate light** (wall, create a walk at a walking area, join, 3D preview with live join); **English and Lithuanian** |
| **Should (P1)** | Gemini photo features for matching; assistant that takes a lost or found report in plain words; link previews in Messenger and Facebook; "My contributions" and helper badges; "Open now" filter; search by name; "Pet emergency: what to do now" card |
| **Could (P2)** | Sightings with a location; printable lost-pet poster with QR; nightly stale job (Imported and Community places); more 3D scene types and weather looks; leave a walk |

## Core features

### A. Find: map and list (P0)
- **Story:** As a pet owner, I open one link and see pet places in Vilnius on a map.
  - Five groups with clear icons and filter chips: **Vets** (incl. 24/7), **Pharmacies & pet shops**, **Pet-friendly places** (cafés, restaurants, shops, hotels), **Walking areas**, **Lost & found**.
  - A list view of the same items, sorted by distance when location is allowed, otherwise by trust.
  - Browsing needs no account. Loads in under 3 seconds on 4G.
- **Story:** As an owner, I tap a place and know if I can trust it.
  - The card shows: name, group, pet rules, address, opening hours if known, Call, Directions (opens the phone's map app), Share.
  - **Source label:** City data / Imported (with a link to where we saw it) / Community.
  - **Trust badge and freshness line** (see "Trust rule" below), e.g. "Confirmed by 4 owners · 5 days ago".
  - Pet types: dogs / cats / all pets.

### B. Add (P0)
- **Story:** As an owner, I add a place I know in under 30 seconds.
  - Pin on the map or "use my location", name, group (walking areas too: people point them on the map), pet types, up to 3 quick facts (pet-friendly: "Allowed inside", "Water bowl", "Terrace only"; walking area: "Fenced", "Off-lead OK"), optional photo.
  - **Duplicate check:** if the same group has a place within 40 m with a similar name, we show it and ask "Is it this one? Confirm it instead."
  - It shows on the map at once as grey "Not yet confirmed". My own confirm doesn't count.
  - Needs Google sign-in. Limit: 10 places a day.

### C. Verify: confirm or report (P0)
- **Story:** As an owner, I tell others if a place is still right.
  - Every card has "Still true?" → **Yes** / **Something's wrong** (closed, moved, not pet-friendly any more, wrong hours, wrong info, other + a short note).
  - One vote per person per item; you can change it once every 7 days. Needs Google sign-in.
  - The badge updates live for everyone.
  - We ask for a confirm right after someone taps Directions or Call, the next time they open the app ("Were you at Caffeine Užupis? Still pet-friendly?").
- **Story:** As anyone, I can see how the rule works.
  - A "How we rate info" page explains the six trust levels in plain words, and shows live counters: places, confirms this week, fresh places, open lost & found posts, reunions.

### Trust rule
Computed on the server only. The canonical rule is in `decisions/council/002-rescope-to-challenge-brief.md`; implementation notes are in `../tech/architecture.md`.

| Level | When | Badge |
|---|---|---|
| Hidden | 3+ reports from different people in 90 days and more reports than confirms | Off the map; team reviews |
| Disputed | 2+ reports in 90 days, newer than the last confirm | Amber: "2 people say this may be closed" |
| Confirmed | 2+ confirms from different people in 90 days (1 for imported or official) | Green: "Confirmed by N owners · X days ago" |
| Official | City or state data, no open reports | Blue: "City data · updated {date}" |
| Stale | Imported or Community place with no confirm in 180 days (or 180 days since import if never confirmed). Official items never go stale; they are refreshed by the monthly re-import. | Grey: "Not checked for 6+ months. Been here? Confirm it." |
| Not yet confirmed | Everything else | Grey: "Added by a community member, not yet confirmed" |

Freshness colour of the last-confirm line: green ≤ 30 days, amber 31–90, grey > 90.

### D. Lost & found (P0)
- **Story:** As someone in a panic, I find where to report in one tap.
  - **Lost & found** is its own tab in the bottom bar. At the top: two big buttons, **"I lost a pet"** (red) and **"I found a pet"** (blue). Below: the board.
  - The same two buttons sit on the home map, above the filters. No sign-in wall before the form: sign-in is asked for only at the Post step.
  - Under the buttons, a small link: "Or tell the assistant what happened" (see I).
- **Story:** As an owner who lost a pet, I post it in one minute and share it everywhere.
  - Lost or Found, species (dog / cat / other), up to 3 photos, name (lost only), colour, size, short note, last-seen pin and time.
  - The pin is rounded to about 100 m before saving. We never show an exact home location.
  - No phone number is shown in public. Phone numbers and emails typed into the note are removed. People reach the poster through an in-app "I saw this pet" message.
  - Red (lost) or blue (found) pins on their own map layer, plus a list, newest first.
  - Share link per post, ready to paste into the Facebook groups people already use.
  - Mark "Reunited": shows a happy state for 3 days, then hides. Posts expire after 30 days unless renewed.
  - Anyone can report a post. 3 reports hide it.
- **Story:** As someone who found an animal, I post it from a browser without installing anything.

### E. Lost ↔ found matching (P0, with AI photo features in P1)
- **Story:** As a lost-pet owner, I'm told when someone posts a found animal that might be mine, and I decide if it is.
  - When a post is created, the server looks for posts of the other kind: same species, within 5 km, found no earlier than 1 day before it was lost, both less than 30 days old. It scores each one on species, size, colours, markings, collar, distance and time.
  - **With AI (P1):** Gemini reads the photos and fills in the features (colours, pattern, markings, collar, coat, ear and tail shape, breed guess). The owner sees the pre-filled form and can fix it. For the top candidates, a second Gemini call compares the two photos and gives a short reason ("same white chest patch, red collar").
  - **Without AI (P0 fallback):** the same scoring runs on what people typed in the form.
  - Up to 3 matches above the threshold are created. **Both reporters are told:** an in-app "Possible match" badge, plus an email.
  - Each side sees the other photo, the rough area, the reason, and "Possible match", never a certain match. They tap **"Yes, that's them"** or **"No"**.
  - **Contact opens only when both say yes:** a private message thread between the two. When the owner marks the post Reunited, both posts close.
  - One "No" closes that match for good. A pair is never suggested twice.
- **Safety:** the AI never shares contact details, never closes a post, and never shows a match as certain.

### F. Share (P0)
- Every place and post has a public link (`/p/{id}`, `/l/{id}`) that opens with no sign-in.
- The phone's share sheet (Messenger, WhatsApp, Facebook), or "Copy link" as a fallback.
- P1: link previews with photo and title.

### G. Emergency button (P0)
- One tap from anywhere: the nearest hand-checked 24/7 vet, with Call and Directions. No AI, works even if Gemini is down.
- P1: a "Pet emergency: what to do now" card with first steps. Credited to If only if If agrees. No quotes, ads or insurance links.

### H. Sign-in and profile (P0)
- Browse with no account.
- To add, confirm, report, post or message: **Sign in with Google** (one tap). First name only is shown in public.
- P1: "My contributions" (places added, confirms, reunions) and simple helper badges ("Vet scout", "Park keeper", "Lost-pet hero"). No points that buy anything.

### I. Assistant for reports (P1)
- **Story:** As a reporter, I tell the assistant what happened in my own words, and it files the report for me to check.
  - Opened from "Or tell the assistant what happened" in the Lost & found tab, or from the Assistant button.
  - Input: free text ("my grey cat ran off near Užupis last night"), a photo, a pasted Facebook post, or a photo of a paper poster.
  - It works out lost or found, species and features from the text and photo, and asks only for what is missing, one short question at a time (at most 3): where, when, a photo.
  - It shows a **draft card** that looks just like the post. The reporter can edit it, then taps **Post**. Posting goes through the same checks as the form, and matching runs at once.
  - It can also turn a pasted post about a place into an add-place draft.
  - It never posts, shares contact data or confirms a match on its own. If the message sounds like a health emergency, it shows the emergency button instead of advice.

### J. Walk-Mate light with the 3D preview (P0)
- **Story:** As an owner, I see walks planned for today and tomorrow.
  - A **Walks** tab: Today / Tomorrow. Each card: walking area name and its trust badge, time, dog avatars, spots left ("2 of 4"), and a still picture of the scene.
  - A walking area's card also shows "Walks here: 2 this week → Join".
  - Past walks are hidden. Full walks show "Full".
- **Story:** As an owner, I create a walk in under 30 seconds.
  - Start point: pick a walking area on the map, or drop a pin. Day (today or tomorrow), time, group size (2–4), a short note. My dog comes from my profile.
  - Scene: walking areas and parks get "park"; the host can switch to riverside, old town or forest. Weather look comes from the time of day (day, evening).
- **Story:** As an owner, I open a walk and see it in 3D.
  - Full-screen 3D scene from `prototypes/walkmate-3d-preview.html`. Joined people stand with their dogs; open spots are "?" ghosts. Walk info sits on glass cards over the scene.
  - Loads in under 3 seconds on a mid-range phone.
- **Story:** As an owner, I join a walk.
  - Tap **Join**: a "?" ghost turns into my avatar with the walk-in animation. Other phones see it live, and the count changes.
  - I can't join twice, join a full walk, or join my own walk.
  - After joining: "Is {area} still OK for dogs?" → Yes / Something's wrong (the normal confirm).
- **Dog profile:** one dog per user: name, size (S/M/L), colour (for the avatar). Asked for the first time someone creates or joins a walk.
- **Safety:** public start points only, first names only, groups of at most 4.

### K. Languages (P0)
- The app is in **English and Lithuanian** from day one. It follows the phone's language, with an EN / LT switch in the header.
- Translated: all app text, filters, trust labels and badges, the "How we rate info" page, emails and the assistant's replies. AI match reasons come back in the reader's language.
- Not translated: place names, addresses, user notes and posts (shown as written).
- Share links open in the viewer's language.

## Data sources
Checked on 2026-10-09. Download details are in `../tech/architecture.md` → "Data import".

| Source (from the brief) | Where it comes from | What we get | Label |
|---|---|---|---|
| Vilnius city dog walking areas | City map server (Vilniaus planas), layers 16–18 | 35 existing areas as pins (centre point), plus 4 being built and 8 planned (shown as "coming soon") | City data |
| | OpenStreetMap `leisure=dog_park` (fallback and extras) | 26 in the city, deduped against the city list | Imported |
| Vet clinics and pharmacies | VMVT register on data.gov.lt (dataset 5258, CC BY 4.0) | ~46 active vet sites in Vilnius: practice premises, service providers, retail vet pharmacies | Official |
| | OpenStreetMap `amenity=veterinary`, `shop=pet` | 32 vets, 48 pet shops | Imported |
| | 24/7 vets checked by phone by the team | 5–8 | Imported, "Checked by BytePets team" |
| Publicly posted pet-friendly places | OpenStreetMap `dog=yes`/`dog=leashed` | Only 17, of which 2 are cafés: too thin on its own | Imported |
| | A hand-made list of 30–50 places from venue websites and public guides, each with its source link | The seed for the community to grow | Imported, starts "Not yet confirmed" |

Context for the pitch: **55,384 registered dogs and about 102,100 registered pets in Vilnius city** (pet register, data.gov.lt dataset 292, 2026-10-01). There is no open feed of individual lost or found pets. That gap is why our board and matching matter.

We never scrape Facebook and never store Google Places or booking-site data. Credits shown in the app: "© Vilniaus miesto savivaldybė, SĮ Vilniaus planas", "VMVT, CC BY 4.0", "© OpenStreetMap contributors".

## Demo assumptions (what is real and what is seeded)
- **Real:** imported places with their source; adds, confirms and lost & found posts made by people at the event (QR drive); the AI matching; live badge changes.
- **Seeded and said so:** a few confirms and reports so all trust levels show; 8–12 walks for today and tomorrow at real walking areas, some half full; 6–10 lost & found posts with photos the team owns or that are free to use. One planted pair is meant to match in the demo.
- Backup: a screen recording of the matching flow, used only if the network fails.

## Out of scope (for now)
- Walk-Mate extras: topics, edit or cancel, chat between walkers, forecast weather
- AI health chat with urgency triage (ADR-002 safety rules kept for when it returns)
- Push notifications, chat outside a confirmed match, moderation dashboard
- Star ratings and reviews, paid listings, insurance offers
- Native apps

## Success metrics
See `../metrics/framework.md`. For the hackathon:
- **Fresh places:** places confirmed by the community in the last 30 days (north star).
- Places added and confirms made by real people during the event.
- Lost & found posts shared; matches confirmed by both sides.
- Walks with at least one joiner.
- The demo runs end to end with no failure in 3 rehearsals.

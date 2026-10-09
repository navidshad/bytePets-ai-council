# Metrics Framework — BytePets

> Living doc. The few numbers we watch and what they mean. The council and PR/FAQs cite this doc when they set success and kill thresholds.

## North-star metric
**Fresh places**: places with at least one community confirm in the last 30 days. It goes up only when people both use and check the map, and it falls when info goes stale, which is the problem in the brief.

## Key metrics
- **Contributions per week** — places added, confirms, reports. Firestore counts in `stats/public`.
- **Share of trusted places** — places that are Confirmed or Official, out of all active places.
- **Lost & found** — posts created, posts shared, matches suggested, matches confirmed by both sides, reunions.
- **Match precision** — matches confirmed by both / matches suggested. Tells us if the threshold is right.
- **Walks with at least one joiner** — Walk-Mate health; each join also asks for a walking-area confirm.
- **Time to vet** — taps from opening the app to calling or getting directions to a vet (target: 2 taps).
- **Day-30 return** — users who come back and contribute again.

## How we instrument
Firebase Analytics events: `place_added`, `place_confirmed`, `place_reported`, `lost_post_created`, `match_suggested`, `match_confirmed`, `reunited`, `share_tapped`, `emergency_opened`, `walk_created`, `walk_edited`, `walk_cancelled`, `walk_joined`, `walk_left`, `walk_3d_opened`, `lang_switched`. Public counters in `stats/public`, updated by Functions and shown on `/about`.

## Guardrails
- No exact home locations, phone numbers or emails in public data.
- Contact opens only after both sides confirm a match.
- No insurance ads or offers; trust badges are never paid for.
- AI cost stays inside the free tier for the demo (at most 6 Gemini calls per lost or found post).
- The emergency button works with AI off.

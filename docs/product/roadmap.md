# Roadmap — BytePets

> Living doc. The current plan of what ships next and why. Changing this doc is a council-level change (see `AGENTS.md` → "Editing rules for living docs"). Use **Phase 1 / Phase 2 / Phase 3** naming, not V1 / V2 / V3.

## Now (in progress)
**Phase 1 — Hack4Vilnius MVP (24 hours).** A mobile web app: a community-checked map of vets, pharmacies, pet-friendly places and walking areas, with add, confirm / report, trust badges and share links; lost & found with AI matching of lost and found posts and a two-sided confirm; an emergency button; Walk-Mate light (walks at walking areas with the 3D preview and live join); English and Lithuanian. Approved in `decisions/council/002-rescope-to-challenge-brief.md`, amended by `003-walk-mate-3d-and-languages.md`. Platform: ADR-003. Build plan: `hackathon-plan.md`.

## Next
**Phase 2 — after the hackathon (if we continue).**
- Keep the map fresh: confirm prompts after a visit, a nightly stale job, a claimed-listing flow for vets and venues ("verified by the clinic", always free).
- Partners as data owners: the city feeds official walking areas; shelters post found animals; vets keep their own hours up to date.
- Lost & found alerts by area (email first; push once the app can rely on it), sightings with a location, printable posters with QR.
- AI health chat with urgency triage and "Show on map" (ADR-002 safety rules; Google Maps results as cards, never pins).
- **Walk-Mate, full:** topics, leave, edit and cancel walks, reminders, live weather in the 3D scene, more scene types.
- A tile provider plan for real traffic.

## Later
- Light reputation that weights votes by track record (no points that buy anything).
- Native wrapper or app if push or store presence matter.
- Other Baltic and Nordic cities, if the Vilnius model works.
- Business model, user stays free: a safety partner (e.g. If) for prevention content and anonymous, consented trends; claimed-listing extras for pet businesses (never mixed with trust badges); a civic data service for the city. See `../marketing/brand.md`.

## Shipped
_Nothing yet._

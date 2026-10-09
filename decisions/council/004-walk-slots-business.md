# Council: Walk slots are the business

**Date**: 2026-10-09
**Lenses**: Founder call (no lenses run; based on `research/Dog Owner Demand Research Vilnius.md`)
**Status**: Decided

## Decision

People can register **walk slots**: times when they are free to walk other people's dogs. Owners book a slot for their dog. BytePets takes a small fee on each paid booking. Owners still use everything else for free.

- **Walker** sets: day, time window, area, how many dogs, dog size, price per walk.
- **Owner** books a slot for their dog. The walker accepts, and both get a notice.
- **After the walk**, both tap "Done". The walker's profile shows "N walks done", which works like the trust badge on places.
- **Fee**: a share of each booking. We propose 15%. This is an assumption to test.
- **Insurance**: If could cover each booked walk (the dog and the walker). This is a partner idea to test, not a promise.
- **Goods for dogs** move to "later": no demand data yet.

For the hackathon, walk slots are **P1**: register a slot and book it. Payment is a mock, labelled "demo".

## Why

Local research shows strong demand for paid walking and care, and weak demand for group walks. Vilnius owners posted 56 care and walking requests on one marketplace, and 10 of the newest 14 expired with no provider. Prices are €2–15, about €8 on average. Trust is the main barrier, and trust is what our product already builds. Boop (a Vilnius pet-sitting app, ~15,000 monthly members) shows the market is real. We differ by adding walk slots to a free community map with lost & found.

## Open Issues

- Is 15% a fee walkers accept on an €8 walk? Ask mentors and test.
- Would If cover booked walks? Ask the challenger rep.
- Payments, walker checks and disputes are Phase 2.

## Action Items

- [x] Add walk slots, the demand data and the business model to `docs/product/prd.md`.
- [x] Update pricing in `docs/marketing/brand.md`, the "Who will pay?" answer in `docs/product/pitch-guide.md`, and `docs/product/roadmap.md`.

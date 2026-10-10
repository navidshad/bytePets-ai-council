# Council: Payments for walk assistants

**Date**: 2026-10-10
**Lenses**: Business Strategist, Technical Architect
**Status**: Decided
**Amends**: `004-walk-slots-business.md`, `005-mvp-rethink.md` (payments were out of the MVP)

## Decision

Payments come into the MVP as **demo money**: the full flow works, every money screen says "Demo money, no real payment", and no provider is chosen yet. Before the first real euro, a licensed marketplace provider holds the money, never a BytePets bank account (ADR to come).

**Rules**

| Moment | What happens |
|---|---|
| Book | The owner sees one price, set by the walker. The money is held. |
| Cancel | Free until 2 h before the walk. After that the walker is paid in full. |
| No start | The walker never taps Start walk: full refund to the owner. |
| End walk | The walker taps End walk (or it ends 2 h after the slot). A 24 h window opens. |
| Problem | The owner reports a problem in the window: the money waits; the team decides by hand. |
| Release | 24 h after the walk, the walker gets the price minus the BytePets fee (proposed 15%, to test). |

**Screens**
- Owner: **Me → Payments**: spent this month and in total, each walk with its state, "Report a problem until [time]" during the window, a receipt per walk.
- Walker: **Me → Earnings**: On hold, On the way (with release time), Paid out. Fee shown on each walk. Year total.

**How it is built**
- Status, price, fee, the 2 h and 24 h rules and every money record change only on the server. The phone only reads.
- Money is whole cents. Every money move is a ledger entry that is never edited; "spent" and "earnings" are sums of the ledger.
- One payment-gateway interface with a demo version that answers after a short delay and can fail, so a real provider fits in later without a rewrite.

## Why

A booking with no money is a notice board, and judges will ask who pays. The hard part is the time rules and the record of money, not the provider, so we build those now and fake only the provider. Owners see one price because a fee on top makes the app look dearer than paying cash; walkers see the fee because they set the price.

## Open Issues
- Walkers may move to cash after the first booking. Reasons to stay: paid late cancels, "walks done" and reviews count only paid walks, and walk cover from If (ask If at the hackathon).
- The provider (Paysera, Stripe Connect, Adyen, Mangopay): it must hold funds, release on our timer, and collect walkers' tax details. EU DAC7 rules make platforms report sellers of personal services to the tax office (VMI).
- Will App Store review accept a build with demo money? Keep it behind a clear label.
- The backend must have server functions, transactions and a scheduled job: input for ADR-004.

## Action Items
- [x] PRD: walker side of features 10–11, new feature 14 Payments, money rule, build plan (lost & found moves to Track A).
- [x] Roadmap and pitch guide: payments line and "Who will pay?".
- [ ] App UI canvas: walker-side walk screens, Payments and Earnings screens, price and cancel rule on Book a walk.
- [ ] ADR: payment provider (after the hackathon).

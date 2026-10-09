# Metrics Framework — BytePets

> Living doc. The few numbers we watch and what they mean. The council and PR/FAQs cite this doc when they set success and kill thresholds.

## North-star metric
**Walks that happen**: walk events that get at least one other owner to join.

## Key metrics
- **Places checked or added per week** — confirms, flags and new places from owners. Uninstrumented.
- **Share of places checked in the last 30 days** — uninstrumented.
- **Walks created per week** — uninstrumented.
- **Fill rate** — share of walks with at least 2 people. Uninstrumented.
- **AI assistant sessions per active user** — uninstrumented.
- **Map actions** — place opened, directions tapped, place shown by the assistant. Uninstrumented.
- **Day-7 retention** — uninstrumented.

## How we instrument
Firebase Analytics (Google Analytics for Firebase) events from the app, plus counts from Firestore. TODO — define event names during the build.

## Guardrails
- AI cost per active user stays inside the free tier for the demo.
- No unsafe health answers: every urgent symptom answer tells the user to contact a vet now.
- Crash-free sessions on the demo device.

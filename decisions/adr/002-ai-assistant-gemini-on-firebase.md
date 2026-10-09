# ADR-002: Run the AI assistant on Gemini, in Cloud Functions, with Search and Maps grounding

**Status**: Accepted
**Date**: 2026-10-09
**Author**: Navid Shad (drafted with Claude)

---

## Context

The app needs an AI assistant that dog owners can chat with. They can send a photo (a rash, a wound, food, a plant the dog ate). The assistant should:

1. answer questions about the dog's health and care, safely;
2. search the internet for current information;
3. know Vilnius dog places (vets, emergency vets, pharmacies, dog parks) and point to them on the app's map.

The team wants Firebase as the backend and Gemini for AI. The open question was whether we need a middle layer like OpenRouter or the Vercel AI SDK to get web search and tool calls. We have 24 hours, so fewer moving parts is better.

Gemini 3 models now let one request use built-in tools (Google Search, Google Maps, URL context) together with our own functions (preview feature). Grounding with Google Maps returns place IDs, titles and links for real places, and it can take the user's location. The free tier allows 500 Maps-grounded requests per day. Google Search grounding is also built in. So Gemini alone covers search, maps and our own tools.

---

## Decision

We run the assistant as an **HTTPS-callable Cloud Function** that calls the **Gemini API** (a current Gemini 3 Flash model) with the `@google/genai` SDK. The API key stays on the server. Each request turns on:

- **Google Search grounding** — current web answers with sources;
- **Google Maps grounding** — real places near the user, with place IDs;
- **our own functions**: `search_places(category, near, open_now)` reads our Firestore `places` collection; `show_on_map(place_ids)` returns pins for the app to show; `get_dog_profile()` reads the user's dog (breed, age, weight).

The function runs a short tool loop (max 4 steps, 30-second timeout, `minInstances: 1`), saves messages in Firestore under `chats/{chatId}/messages`, and returns text, sources and map pins. Photos are uploaded to Firebase Storage first and passed to Gemini as image input. A system prompt sets the safety rules: no diagnosis, clear "go to a vet now" for red-flag signs (poisoning, breathing trouble, heavy bleeding, seizures, bloat), and always link the nearest emergency vet.

Rules added after review:

- **Pins come from our own `places` first.** Maps grounding gives a place ID but no coordinates. To pin a Google-only place we call Places API Place Details (location field only), cache it in `googlePlaceCache`, and write the Google ID back to our matching place (same category, within 80 m). This step is below the MVP cut line; until then, Google-only places show as source cards with an "Open in Google Maps" link.
- **Safety in code.** The server checks the user's text for red-flag words, and the model can call `flag_urgent(reason)`. Either one makes the server add the nearest hand-checked 24/7 emergency vet pin, whatever the model says.
- **Prompt injection.** Web results are data, not instructions. `show_on_map` only accepts IDs from our `places` or from this turn's grounding results. Tools only read the signed-in user's own data.
- **Waiting time.** Answers can take 5–15 seconds. The app shows progress ("Looking at the photo…", "Searching…"). Streaming with callable `sendChunk` is a nice-to-have.
- **Abuse and cost.** App Check plus a per-user message limit; photos resized on the phone to about 1 MB; budget alert on the Google Cloud project.
- **Model.** Pin one exact Gemini 3.5 Flash-or-later model ID (Maps + Search together need it) after the hour-0 spike, then don't change it.

If the combined built-in + custom tools preview does not work on the day, the fallback is two calls: one Gemini call with Search/Maps grounding, then one with our functions.

---

## Alternatives Considered

### Alternative A — OpenRouter
**What it is**: One API in front of many models, with web search as an add-on.
**Why we considered it**: Easy to switch models; one bill.
**Why we rejected it**: Adds a second vendor and key for no gain. Gemini's own Search and Maps grounding are better for local places than a generic web-search add-on, and Maps grounding is not available through OpenRouter.

### Alternative B — Vercel AI SDK on a Vercel server
**What it is**: A TypeScript SDK with a nice tool-loop API and streaming, hosted on Vercel.
**Why we considered it**: Clean agent-loop code and good streaming UI helpers.
**Why we rejected it**: It means a second backend host next to Firebase. Its Gemini provider does not cover every built-in Gemini tool combination well. Not worth it in 24 hours.

### Alternative C — Firebase AI Logic (call Gemini straight from the app)
**What it is**: The Firebase client SDK calls Gemini from the phone, protected by App Check.
**Why we considered it**: No server code; supports Google Search grounding.
**Why we rejected it**: Our tools read Firestore and must run on the server; Maps grounding and the tool loop are simpler and safer on the server. We may still use it for small one-shot calls.

### Alternative D — Genkit on Cloud Functions
**What it is**: Google's AI framework with flows, tools and a dev UI.
**Why we considered it**: Made for Firebase; good tool-calling and tracing.
**Why we rejected it**: Another layer to learn in 24 hours. The plain SDK is enough for a 4-step loop. Fine to adopt later.

---

## Consequences

### Positive
- One vendor, one backend. Search, Maps and our tools in the same model call.
- Real place IDs and links let the assistant put pins on our map.
- The API key never ships in the app.

### Negative
- Built-in + custom tool combination is a preview feature; it may change.
- Google Maps grounding has display rules: show sources right after the answer, keep the "Google Maps" label as is.
- Cold starts on Cloud Functions can add a few seconds; set min instances to 1 for the demo.

### Neutral / Notable
- Health answers are not vet advice. The app shows a short notice in the chat.
- Usage cost: Maps grounding is paid after 500 requests per day; fine for a demo.

---

## Architect Review

**Verdict: approve, with fixes.** One vendor, one backend is right for 24 hours. The alternatives are rejected fairly. One gap: Vercel is rejected for streaming, but streaming is never solved here.

What is missing:

- **Pins need coordinates.** Maps grounding gives a placeId, not a lat/lng. Turning it into a pin needs a Place Details call (Essentials, location field only). It has a free monthly cap. Cache results in Firestore by placeId. Better still: prefer our own `places` collection for pins, and use Maps grounding only for "more places" and links.
- **Streaming and latency.** A grounded call plus a 4-step loop with a photo can take 5–15 seconds. Callable functions can stream (`sendChunk` on the server, `.stream()` in Flutter). Use it, or at least show "searching the web…" steps. Set a 30-second timeout.
- **Safety in code, not only in the prompt.** Check red-flag words on the server. If one is found, always add the emergency vet card, whatever the model says.
- **Prompt injection.** Web results are data. `show_on_map` must only accept place IDs from this turn's results or our database. Tools read only the signed-in user's own data.
- **Demo risk.** Test the preview tool combo in the first two hours, not at hour 20. Keep a cached "golden" demo answer. Check the Gemini rate limit, not only the 500/day Maps limit. Add App Check and a per-user limit on the function.
- **Photos.** Resize on the phone (about 1 MB) before upload.

---

## References

- Gemini API — Combine built-in tools and function calling: https://ai.google.dev/gemini-api/docs/tool-combination
- Gemini API — Grounding with Google Maps: https://ai.google.dev/gemini-api/docs/generate-content/maps-grounding
- Firebase AI Logic: https://firebase.google.com/docs/ai-logic
- Related: ADR-001 (iPhone app with Flutter)

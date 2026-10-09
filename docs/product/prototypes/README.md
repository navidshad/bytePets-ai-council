# Prototypes

Design prototypes that show how a feature should look and feel. They are references for the app team, not product code.

| File | What it shows | Status |
|---|---|---|
| [walkmate-3d-preview.html](walkmate-3d-preview.html) | Walk-Mate event preview: full-screen 3D scene picked from the start point (landmark, park, riverside, forest, old town), weather looks, joined people with dogs, "?" ghosts for open spots, and the join animation. Event info sits on glass cards over the scene. | Approved look for Phase 1, Walk-Mate light (Council 003). Ported into the web app as `WalkScene.vue` |
| [home-map/](home-map/README.md) | Map-first home and the MVP screens: home map with floating ask box, vet open now, lost dog, list view, dog area page, check-in, report lost/found, walker (later). Real Vilnius map shapes and city walking areas; other data are samples. | MVP direction (Council 005) |

**How to open:** download the file and open it in a browser (it loads Three.js r128 from cdnjs). On a phone or a narrow window it shows the portrait layout.

**How it maps to the app:** the web app wraps this scene in a Vue component and feeds it with `setScene` / `addAttendee` (see `../../tech/architecture.md` → 3D bridge (web)). Sample events, people and weather in the file are examples only.

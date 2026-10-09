# Prototypes

Design prototypes that show how a feature should look and feel. They are references for the app team, not product code.

| File | What it shows | Status |
|---|---|---|
| [walkmate-3d-preview.html](walkmate-3d-preview.html) | Walk-Mate event preview: full-screen 3D scene picked from the start point (landmark, park, riverside, forest, old town), weather looks, joined people with dogs, "?" ghosts for open spots, and the join animation. Event info sits on glass cards over the scene. | Approved look for Phase 1 |

**How to open:** download the file and open it in a browser (it loads Three.js r128 from cdnjs). On a phone or a narrow window it shows the portrait layout.

**How it maps to the app:** the app shows this page in a WebView and feeds it with `bp.setScene` / `bp.addAttendee` (see `../../tech/architecture.md` → 3D bridge). Sample events, people and weather in the file are examples only.

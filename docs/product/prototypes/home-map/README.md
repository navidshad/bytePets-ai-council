# Home map prototype

A clickable phone prototype of the map-first home screen and the MVP features. Decision: `decisions/council/005-mvp-rethink.md`.

**Open it:** https://claude.ai/artifact/G4h1gwYUzUQdFJx66sXFvb (a Design canvas; press Play on an artboard to click through). The files here are its source (`.dc.html` Design Components). They need the canvas runtime, so they do not open as plain web pages.

## Screens

| File | Screen |
|---|---|
| `Main.dc.html` | 1 · Home map: location header, colour chips (filter and legend), "you are here", floating ask box that shrinks to a paw button when you drag the map, pins fade near the edges |
| `VetAnswer.dc.html` | 2 · Ask "vet open now": numbered results with Call |
| `LostDog.dc.html` | 3 · Ask "I lost my dog": post first, then possible found posts, two-sided confirm |
| `Lists.dc.html` | 4 · List view: Dog areas · Vets · Cafés · Lost & found · Walkers (later) |
| `Place.dc.html` | 5 · Dog area page: photo, rating, tags, fence state, Check in |
| `CheckIn.dc.html` | 6 · Check in: stars, photo, fence OK / broken, tags |
| `Report.dc.html` | 7 · Report lost or found: photos, pet tags, rough area |
| `Walker.dc.html` | 8 · Walker profile (later): tags, photo after every walk, free first meeting |
| `VilniusMap.dc.html` | The map layer, shared by the screens |

## What is real and what is a sample
- **Real:** map shapes from OpenStreetMap (Neris, Vilnia, parks, forests) and the positions and addresses of the city's dog-walking areas (Vilniaus planas map layer 16).
- **Samples:** ratings, check-ins, "busy now", vet and café names and hours, lost and found pins, photos (drawn placeholders).

## How the map was made (`tools/`)
1. OpenStreetMap extracts for the box 54.655–54.73 N, 25.20–25.34 E via Overpass: `waterway=river`, `natural=water`, `leisure=park`, `landuse=forest`. City walking areas from the Vilniaus planas layer 16 query (`f=geojson`).
2. `build_map.py <dir>` projects them to a 1200 × 1112 px drawing and simplifies the lines.
3. `stitch.py <dir> build_map.py` joins park, forest and water pieces into closed outlines.
OpenStreetMap data © OpenStreetMap contributors (ODbL).

The real app would draw the same look with a map style on live tiles (MapLibre or Google Maps; see the open map-provider decision).

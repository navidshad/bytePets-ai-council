"""Turn Vilnius OSM extracts + city walking areas into simplified SVG paths for the prototype."""
import json, math, sys

D = sys.argv[1]
LON0, LON1, LAT0, LAT1 = 25.20, 25.34, 54.655, 54.73
K = math.cos(math.radians((LAT0 + LAT1) / 2))
W = 1200
H = round(W * (LAT1 - LAT0) / ((LON1 - LON0) * K))


def xy(lon, lat):
    return ((lon - LON0) / (LON1 - LON0) * W, (LAT1 - lat) / (LAT1 - LAT0) * H)


def dp(pts, tol):
    if len(pts) < 3:
        return pts
    (x0, y0), (x1, y1) = pts[0], pts[-1]
    dx, dy = x1 - x0, y1 - y0
    n = math.hypot(dx, dy) or 1e-9
    best, idx = 0, 0
    for i in range(1, len(pts) - 1):
        px, py = pts[i]
        d = abs(dy * px - dx * py + x1 * y0 - y1 * x0) / n
        if d > best:
            best, idx = d, i
    if best > tol:
        return dp(pts[: idx + 1], tol)[:-1] + dp(pts[idx:], tol)
    return [pts[0], pts[-1]]


def path(coords, closed, tol=2.2):
    pts = dp([xy(lon, lat) for lon, lat in coords], tol)
    if len(pts) < 2:
        return ""
    s = "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in pts)
    return s + ("Z" if closed else "")


def area(coords):
    pts = [xy(a, b) for a, b in coords]
    return abs(sum(pts[i][0] * pts[i - 1][1] - pts[i - 1][0] * pts[i][1] for i in range(len(pts)))) / 2


def geoms(el):
    if el["type"] == "way" and "geometry" in el:
        yield [(p["lon"], p["lat"]) for p in el["geometry"]]
    elif el["type"] == "relation":
        for m in el.get("members", []):
            if m.get("role") in ("outer", "") and "geometry" in m:
                yield [(p["lon"], p["lat"]) for p in m["geometry"]]


out = {"w": W, "h": H, "water": [], "rivers": [], "parks": [], "forest": [], "roads": [], "areas": []}

for el in json.load(open(f"{D}/water.json"))["elements"]:
    t = el.get("tags", {})
    for g in geoms(el):
        if t.get("waterway") == "river":
            p = path(g, False, 2.0)
            if p:
                out["rivers"].append({"d": p, "name": t.get("name", "")})
        elif len(g) > 3 and area(g) > 300:
            out["water"].append(path(g, True))

for el in json.load(open(f"{D}/parks.json"))["elements"]:
    t = el.get("tags", {})
    key = "forest" if t.get("landuse") == "forest" else "parks"
    for g in geoms(el):
        if len(g) > 3 and area(g) > (900 if key == "forest" else 400):
            out[key].append(path(g, True, 2.6))

for el in json.load(open(f"{D}/roads.json"))["elements"]:
    if "geometry" in el:
        p = path([(q["lon"], q["lat"]) for q in el["geometry"]], False, 2.6)
        if p:
            out["roads"].append(p)

for f in json.load(open(f"{D}/areas.geojson"))["features"]:
    ring = f["geometry"]["coordinates"][0]
    cx = sum(c[0] for c in ring) / len(ring)
    cy = sum(c[1] for c in ring) / len(ring)
    x, y = xy(cx, cy)
    if 0 <= x <= W and 0 <= y <= H:
        out["areas"].append({"x": round(x), "y": round(y), "name": (f["properties"].get("VIETA") or "").strip()})

for k in ("water", "parks", "forest", "roads"):
    out[k] = [p for p in out[k] if p]
json.dump(out, open(f"{D}/map.json", "w"), ensure_ascii=False, separators=(",", ":"))
print("size", W, H, {k: len(v) for k, v in out.items() if isinstance(v, list)})

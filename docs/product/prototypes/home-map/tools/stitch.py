import json, math, sys
D = sys.argv[1]
exec(open(sys.argv[2]).read().split('out = {')[0])

def rings(el):
    if el['type'] == 'way' and 'geometry' in el:
        g = [(p['lon'], p['lat']) for p in el['geometry']]
        if g[0] == g[-1]:
            yield g
        return
    parts = [[(p['lon'], p['lat']) for p in m['geometry']] for m in el.get('members', [])
             if m.get('role') == 'outer' and 'geometry' in m]
    while parts:
        ring = parts.pop(0)
        changed = True
        while ring[0] != ring[-1] and changed:
            changed = False
            for i, p in enumerate(parts):
                if p[0] == ring[-1]: ring += p[1:]
                elif p[-1] == ring[-1]: ring += p[::-1][1:]
                elif p[-1] == ring[0]: ring = p + ring[1:]
                elif p[0] == ring[0]: ring = p[::-1] + ring[1:]
                else: continue
                parts.pop(i); changed = True; break
        if ring[0] == ring[-1] and len(ring) > 3:
            yield ring

def layer(fname, pick, minarea, tol):
    out = []
    for el in json.load(open(f'{D}/{fname}'))['elements']:
        if not pick(el.get('tags', {})): continue
        for g in rings(el):
            if area(g) > minarea:
                pts = [xy(a, b) for a, b in g]
                h = len(pts) // 2
                pts = dp(pts[:h + 1], tol)[:-1] + dp(pts[h:], tol)
                p = 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in pts) + 'Z' if len(pts) > 3 else ''
                if p: out.append(p)
    return ''.join(out)

res = {
 'parks': layer('parks.json', lambda t: t.get('leisure') == 'park', 500, 2.5),
 'forest': layer('parks.json', lambda t: t.get('landuse') == 'forest', 1500, 3),
 'water': layer('water.json', lambda t: t.get('natural') == 'water', 400, 2.5),
}
for k, v in res.items(): print(k.upper(), len(v)); print(v)

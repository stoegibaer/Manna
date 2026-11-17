#!/usr/bin/env python3
"""Build the compact base map for the "Wo sind wir?" mini map and the atlas from Natural Earth (public domain).

Usage: python3 -I tools/build_map.py <dir with ne_10m_land.json, ne_10m_lakes.json, ne_10m_rivers_lake_centerlines.json>
Download: https://github.com/nvkelso/natural-earth-vector/tree/master/geojson
Output: app/src/main/assets/map.json  {"bbox":[w,s,e,n], "land":[poly...], "lakes":[poly...], "rivers":[{"name","line"}...]}
Coordinates are [lon, lat] rounded to 3 decimals.
"""
import json, math, sys, pathlib

BBOX = (10.0, 22.0, 50.0, 43.0)  # Rome .. Persia, Egypt .. Asia Minor
RIVERS = {"Nile", "Rosetta Branch", "Damietta Branch", "Euphrates", "Tigris", "Shatt al Arab", "Jordan"}
LAKES = {"Dead Sea", "Sea of Galilee"}
TOL = 0.02  # simplification tolerance in degrees
# Holy Land core: the atlas zooms in far here (places 1–2 km apart), so keep nearly all detail
DETAIL = (34.0, 29.5, 37.0, 34.0)
DETAIL_TOL = 0.001


def clip_poly(pts, bbox):
    w, s, e, n = bbox
    def clip(pts, inside, inter):
        out = []
        for i in range(len(pts)):
            a, b = pts[i - 1], pts[i]
            ia, ib = inside(a), inside(b)
            if ib:
                if not ia: out.append(inter(a, b))
                out.append(b)
            elif ia:
                out.append(inter(a, b))
        return out
    def ix(a, b, x): t = (x - a[0]) / (b[0] - a[0]); return (x, a[1] + t * (b[1] - a[1]))
    def iy(a, b, y): t = (y - a[1]) / (b[1] - a[1]); return (a[0] + t * (b[0] - a[0]), y)
    for inside, inter in (
        (lambda p: p[0] >= w, lambda a, b: ix(a, b, w)),
        (lambda p: p[0] <= e, lambda a, b: ix(a, b, e)),
        (lambda p: p[1] >= s, lambda a, b: iy(a, b, s)),
        (lambda p: p[1] <= n, lambda a, b: iy(a, b, n)),
    ):
        if not pts: break
        pts = clip(pts, inside, inter)
    return pts


def clip_line(pts, bbox):
    w, s, e, n = bbox
    inside = lambda p: w <= p[0] <= e and s <= p[1] <= n
    parts, cur = [], []
    for p in pts:
        if inside(p): cur.append(p)
        elif cur: parts.append(cur); cur = []
    if cur: parts.append(cur)
    return [p for p in parts if len(p) > 1]


def tol_at(p, tol):
    w, s, e, n = DETAIL
    return min(tol, DETAIL_TOL) if w <= p[0] <= e and s <= p[1] <= n else tol


def simplify(pts, tol):
    if len(pts) < 3: return pts
    def dist(p, a, b):
        if a == b: return math.dist(p, a)
        dx, dy = b[0] - a[0], b[1] - a[1]
        return abs(dy * p[0] - dx * p[1] + b[0] * a[1] - b[1] * a[0]) / math.hypot(dx, dy)
    stack, keep = [(0, len(pts) - 1)], {0, len(pts) - 1}
    while stack:
        i, j = stack.pop()
        best, idx = 0, None
        for k in range(i + 1, j):
            d = dist(pts[k], pts[i], pts[j])
            if d > best: best, idx = d, k
        if idx is not None and best > tol_at(pts[idx], tol):
            keep.add(idx); stack += [(i, idx), (idx, j)]
    return [pts[k] for k in sorted(keep)]


def rings(geom):
    if geom["type"] == "Polygon": return [geom["coordinates"][0]]
    if geom["type"] == "MultiPolygon": return [p[0] for p in geom["coordinates"]]
    return []


def lines(geom):
    if geom["type"] == "LineString": return [geom["coordinates"]]
    if geom["type"] == "MultiLineString": return geom["coordinates"]
    return []


def rnd(pts): return [[round(x, 3), round(y, 3)] for x, y in pts]


def main(src):
    src = pathlib.Path(src)
    out = {"bbox": list(BBOX), "land": [], "lakes": [], "rivers": []}
    for f in json.loads((src / "ne_10m_land.json").read_text())["features"]:
        for r in rings(f["geometry"]):
            c = clip_poly([tuple(p[:2]) for p in r], BBOX)
            if len(c) >= 3:
                c = simplify(c + [c[0]], TOL)
                if len(c) >= 4: out["land"].append(rnd(c))
    for f in json.loads((src / "ne_10m_lakes.json").read_text())["features"]:
        if (f["properties"].get("name") or "") in LAKES:
            for r in rings(f["geometry"]):
                out["lakes"].append(rnd([tuple(p[:2]) for p in r]))  # few points, keep all
    for f in json.loads((src / "ne_10m_rivers_lake_centerlines.json").read_text())["features"]:
        name = f["properties"].get("name")
        if name in RIVERS:
            for l in lines(f["geometry"]):
                for part in clip_line([tuple(p[:2]) for p in l], BBOX):
                    out["rivers"].append({"name": name, "line": rnd(simplify(part, TOL / 2))})
    dst = pathlib.Path(__file__).resolve().parent.parent / "app/src/main/assets/map.json"
    dst.write_text(json.dumps(out, separators=(",", ":")))
    n = sum(len(p) for p in out["land"]) + sum(len(p) for p in out["lakes"]) + sum(len(r["line"]) for r in out["rivers"])
    print(f"land {len(out['land'])} polys, lakes {len(out['lakes'])}, rivers {len(out['rivers'])}, {n} points, {dst.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main(sys.argv[1])

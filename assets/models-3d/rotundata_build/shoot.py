"""Short erect stem with flush scar rings and a solid split sheath.

Material slots: 0 stem, 1 sheath, 2 scar.
"""

import math

import bmesh

from .geometry import bm_to_mesh


def shoot_mesh(name, origin, stem_dir, side_hint, cfg, sides=10, arc=12):
    d = stem_dir.normalized()
    side = (side_hint - d * side_hint.dot(d)).normalized()
    normal = d.cross(side).normalized()
    height = cfg["stem_height_m"]
    rx, ry = cfg["stem_radius_m"]
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")

    def vert(z, a, ax, ay):
        return bm.verts.new(origin + d * z + side * (math.sin(a) * ax) + normal * (math.cos(a) * ay))

    # Stem: closed loops; each scar is three loops with the middle one a fraction of a mm proud.
    half = cfg["scar_half_m"]
    proud = cfg["scar_proud_m"]
    levels = [(0.0, 0.0, None)]
    for g, frac in enumerate(cfg["scar_fracs"]):
        z = frac * height
        levels += [(z - half, 0.0, g), (z, proud, g), (z + half, 0.0, g)]
    levels.append((0.56 * height, 0.0, None))
    rings = []
    for z, extra, _g in levels:
        rings.append([vert(z, 2 * math.pi * k / sides, rx + extra, ry + extra) for k in range(sides)])
    for i in range(len(rings) - 1):
        g0, g1 = levels[i][2], levels[i + 1][2]
        mat = 2 if g0 is not None and g0 == g1 else 0
        for k in range(sides):
            k2 = (k + 1) % sides
            face = bm.faces.new((rings[i][k], rings[i][k2], rings[i + 1][k2], rings[i + 1][k]))
            face.material_index = mat
            for loop, (kk, ii) in zip(face.loops, ((k, i), (k + 1, i), (k + 1, i + 1), (k, i + 1))):
                loop[uv].uv = (kk / sides, levels[ii][0] / height)
    for ring, rev in ((rings[0], True), (rings[-1], False)):
        face = bm.faces.new(tuple(reversed(ring)) if rev else tuple(ring))
        face.material_index = 0

    # Sheath: C-shaped wrap with an outer and inner wall, open on the +normal side.
    # Lesson sheath is about 3.4 cm on a stem under 6 cm (published range 1.5–5.5 cm).
    wall = cfg["sheath_wall_m"]
    if cfg.get("variant") == "lesson":
        fracs = (0.30, 0.52, 0.76, 1.0)
        outer = (
            (rx + 0.00030, ry + 0.00025),
            (rx + 0.00090, ry + 0.00055),
            (0.0022, 0.00135),
            (0.0027, 0.00155),
        )
        slit = (0.06, 0.10, 0.20, 0.36)
    else:
        fracs = (0.40, 0.55, 0.78, 1.0)
        outer = (
            (rx + 0.0002, ry + 0.0002),
            (rx + 0.0006, ry + 0.0004),
            (0.0030, 0.0016),
            (0.0036, 0.0019),
        )
        slit = (0.10, 0.18, 0.40, 0.62)
    zs = [f * height for f in fracs]
    walls = {"o": [], "i": []}
    for z, (ax, ay), s in zip(zs, outer, slit):
        angles = [s + (2 * math.pi - 2 * s) * k / arc for k in range(arc + 1)]
        walls["o"].append([vert(z, a, ax, ay) for a in angles])
        walls["i"].append([vert(z, a, max(rx * 0.9, ax - wall), max(ry * 0.9, ay - wall)) for a in angles])

    def quad(a, b, c, e, u0, u1, v0, v1):
        face = bm.faces.new((a, b, c, e))
        face.material_index = 1
        for loop, coord in zip(face.loops, ((u0, v0), (u1, v0), (u1, v1), (u0, v1))):
            loop[uv].uv = coord

    o, n = walls["o"], walls["i"]
    for j in range(len(zs) - 1):
        v0, v1 = j / 3, (j + 1) / 3
        for k in range(arc):
            u0, u1 = k / arc, (k + 1) / arc
            quad(o[j][k], o[j][k + 1], o[j + 1][k + 1], o[j + 1][k], u0, u1, v0, v1)
            quad(n[j][k + 1], n[j][k], n[j + 1][k], n[j + 1][k + 1], u1, u0, v0, v1)
        quad(o[j][0], o[j + 1][0], n[j + 1][0], n[j][0], 0, 0.02, v0, v1)
        quad(n[j][arc], n[j + 1][arc], o[j + 1][arc], o[j][arc], 0.98, 1, v0, v1)
    for j in (0, len(zs) - 1):
        for k in range(arc):
            quad(o[j][k], n[j][k], n[j][k + 1], o[j][k + 1], k / arc, (k + 1) / arc, j / 3, j / 3)
    return bm_to_mesh(bm, name)

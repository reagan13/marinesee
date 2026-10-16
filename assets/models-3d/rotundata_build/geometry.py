"""Solid strap leaves and tubes (rhizome, roots), skinned from Authoring curves."""

import bisect
import math

import bmesh
import bpy
from mathutils import Vector

from .textures import vein_xs
from .util import arc_table, frame_at, point_at, smoothstep, tangent_at


def bm_to_mesh(bm, name):
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    for poly in mesh.polygons:
        poly.use_smooth = True
    return mesh


def strap_profile(vein_count):
    """Closed cross-section: (x across width, face side, is_vein). Upper face carries the vein lanes."""
    xs = vein_xs(vein_count)
    upper = []
    for k, x in enumerate(xs):
        upper.append((x, 1.0, True))
        if k < len(xs) - 1:
            upper.append((0.5 * (x + xs[k + 1]), 1.0, False))
    lower = [(x, -1.0, False) for x in (0.9, 0.3, -0.3, -0.9)]
    return [(-1.0, 0.0, False)] + upper + [(1.0, 0.0, False)] + lower


def leaf_mesh(name, dense, width, thickness, vein_count, side_hint, twist, groove, crown, body_rings=8):
    """Flat strap about `width` wide and `thickness` thick with a semicircular tip."""
    cum = arc_table(dense)
    length = cum[-1]
    r = 0.5 * width
    tip_start = max(0.5 * length, length - r)
    stations = []
    for k in range(body_rings):
        d = tip_start * k / (body_rings - 1)
        hw = r * (0.80 + 0.20 * smoothstep(d / (0.10 * length)))
        stations.append((d, hw, 1.0))
    for deg in (22, 42, 58, 71, 81):
        phi = math.radians(deg)
        stations.append((tip_start + (length - tip_start) * math.sin(phi), r * math.cos(phi), 0.55 + 0.45 * math.cos(phi)))

    profile = strap_profile(vein_count)
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    rings, ring_uv = [], []
    for d, hw, tf in stations:
        p = point_at(dense, cum, d)
        side, normal = frame_at(tangent_at(dense, cum, d), side_hint, twist * d / length)
        ht = 0.5 * thickness * tf
        ring, coords = [], []
        for x, face, is_vein in profile:
            y = face * ht + crown * tf * (1.0 - x * x)
            if is_vein:
                y -= groove * tf
            ring.append(bm.verts.new(p + side * (x * hw) + normal * y))
            coords.append((0.5 + 0.5 * x, d / length))
        rings.append(ring)
        ring_uv.append(coords)

    m = len(profile)
    for i in range(len(rings) - 1):
        for j in range(m):
            j2 = (j + 1) % m
            face = bm.faces.new((rings[i][j], rings[i][j2], rings[i + 1][j2], rings[i + 1][j]))
            for loop, c in zip(face.loops, (ring_uv[i][j], ring_uv[i][j2], ring_uv[i + 1][j2], ring_uv[i + 1][j])):
                loop[uv].uv = c
    base = bm.faces.new(tuple(reversed(rings[0])))
    for loop in base.loops:
        loop[uv].uv = ring_uv[0][rings[0].index(loop.vert)]
    apex = bm.verts.new(point_at(dense, cum, length))
    last = rings[-1]
    for j in range(m):
        j2 = (j + 1) % m
        face = bm.faces.new((last[j], last[j2], apex))
        for loop, c in zip(face.loops, (ring_uv[-1][j], ring_uv[-1][j2], (0.5, 1.0))):
            loop[uv].uv = c
    return bm_to_mesh(bm, name)


def tube_mesh(name, dense, ds, radii, sides, oval, side_hint):
    """Closed oval tube through the stations `ds` (arc distances). Returns mesh and ring index per vertex."""
    cum = arc_table(dense)
    length = max(cum[-1], 1e-9)
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    rings, ring_of = [], []
    for i, d in enumerate(ds):
        p = point_at(dense, cum, d)
        side, normal = frame_at(tangent_at(dense, cum, d), side_hint)
        ring = []
        for k in range(sides):
            a = 2 * math.pi * k / sides
            ring.append(bm.verts.new(p + side * (math.cos(a) * radii[i] * oval) + normal * (math.sin(a) * radii[i])))
            ring_of.append(i)
        rings.append(ring)
    for i in range(len(rings) - 1):
        for k in range(sides):
            k2 = (k + 1) % sides
            face = bm.faces.new((rings[i][k], rings[i][k2], rings[i + 1][k2], rings[i + 1][k]))
            for loop, (kk, ii) in zip(face.loops, ((k, i), (k + 1, i), (k + 1, i + 1), (k, i + 1))):
                loop[uv].uv = (kk / sides, ds[ii] / length)
    for ring, rev in ((rings[0], True), (rings[-1], False)):
        face = bm.faces.new(tuple(reversed(ring)) if rev else tuple(ring))
        for loop in face.loops:
            loop[uv].uv = (0.5, 0.0 if rev else 1.0)
    return bm_to_mesh(bm, name), ring_of


def rhizome_mesh(name, dense, node_ds, radius, oval, step=0.006, sides=8):
    """One welded tube. Each vertex is weighted to the internode bone it sits on."""
    end = arc_table(dense)[-1]
    ds = []
    marks = list(node_ds) + [end]
    for k in range(len(marks) - 1):
        a, b = marks[k], marks[k + 1]
        count = max(2, round((b - a) / step))
        ds.extend(a + (b - a) * s / count for s in range(count))
    ds.append(end)
    radii = []
    for d in ds:
        rr = radius
        for nd in node_ds:
            rr *= 1.0 + 0.14 * math.exp(-((d - nd) ** 2) / (2 * 0.0025 ** 2))
        rr *= 0.7 + 0.3 * smoothstep(d / 0.004)
        rr *= 0.4 + 0.6 * smoothstep((end - d) / 0.012)
        radii.append(rr)
    mesh, ring_of = tube_mesh(name, dense, ds, radii, sides, oval, Vector((0.0, 0.0, 1.0)))
    nseg = len(node_ds) - 1
    groups = {}
    for vid, ring in enumerate(ring_of):
        seg = min(nseg - 1, max(0, bisect.bisect_right(node_ds, ds[ring] + 1e-7) - 1))
        groups.setdefault("rhizome_%02d" % seg, []).append(vid)
    return mesh, groups


def root_mesh(name, dense, radius, rings=6, sides=5):
    length = arc_table(dense)[-1]
    ds = [length * k / (rings - 1) for k in range(rings)]
    radii = [radius * (1.0 - 0.7 * (d / length)) for d in ds]
    mesh, _ring_of = tube_mesh(name, dense, ds, radii, sides, 1.0, Vector((1.0, 0.0, 0.0)))
    return mesh

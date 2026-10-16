"""Build the Cymodocea rotundata meadow in the open Blender file.

Metric, 1 unit = 1 metre. One Grow action, 30 fps, frames 1–330.
Frame 1 and frame 330 are the same bud. The meadow is held, then jumps back.
"""

import math
import random

import bmesh
import bpy
from mathutils import Euler, Matrix, Vector

LEAF_W = 0.008
N_VEINS = 11
N_SHOOTS = 9
HOLD = 316
END = 330
TINY = (0.001, 0.001, 0.001)
FULL = (1.0, 1.0, 1.0)
RNG = random.Random(11)

LENGTHS = (
    (0.15, 0.13, 0.11, 0.09),
    (0.14, 0.15, 0.12, 0.08),
    (0.12, 0.14, 0.10, 0.13),
    (0.13, 0.11, 0.15, 0.09),
    (0.11, 0.13, 0.09, 0.12),
    (0.10, 0.12, 0.08, 0.11),
    (0.12, 0.09, 0.11, 0.08),
    (0.09, 0.11, 0.07, 0.08),
    (0.08, 0.07, 0.10, 0.07),
)
FANS = ((-0.82, 0.22), (-0.22, 0.10), (0.30, 0.16), (0.88, 0.28))
BOWS = (0.006, 0.008, 0.004, 0.007)


def srgb(r, g, b):
    def f(u):
        return u / 12.92 if u <= 0.04045 else ((u + 0.055) / 1.055) ** 2.4

    return (f(r), f(g), f(b))


def sock(node, identifier):
    for item in node.inputs:
        if item.identifier == identifier:
            return item
    raise KeyError(identifier)


def out_sock(node, identifier):
    for item in node.outputs:
        if item.identifier == identifier:
            return item
    raise KeyError(identifier)


def sand_radii(x, y):
    ang = math.atan2(y, x + 1e-8)
    rx = 0.20 * (1.0 + 0.1 * math.sin(3 * ang) + 0.06 * math.sin(5 * ang + 0.8))
    ry = 0.125 * (1.0 + 0.12 * math.cos(2 * ang + 0.4) + 0.04 * math.sin(4 * ang))
    return rx, ry


def sand_height(x, y):
    rx, ry = sand_radii(x, y)
    r = math.sqrt((x / rx) ** 2 + (y / ry) ** 2)
    fall = max(0.0, 1.0 - r) ** 0.7
    mound = 0.018 * math.exp(-1.35 * r * r)
    lump = 0.0028 * math.sin(x * 10.5 + 0.4) * math.cos(y * 12.0)
    wave_a = 0.0026 * math.sin(x * 22.0 + y * 8.0)
    wave_b = 0.0018 * math.sin(-x * 12.0 + y * 26.0 + 0.8)
    return (mound + lump + wave_a + wave_b) * (0.2 + 0.8 * fall)


def sand_inside(x, y):
    rx, ry = sand_radii(x, y)
    return (x / rx) ** 2 + (y / ry) ** 2 <= 1.0


def node_pos(i):
    t = i / (N_SHOOTS - 1)
    x = -0.12 + t * 0.24 + 0.007 * math.sin(i * 1.4)
    y = 0.02 * math.sin(t * math.pi * 1.25 + 0.3) + 0.008 * math.sin(i * 2.2)
    z = sand_height(x, y) - 0.00135
    return Vector((x, y, z))


def smooth(mesh):
    for poly in mesh.polygons:
        poly.use_smooth = True


def bm_to_mesh(bm, name):
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    smooth(mesh)
    return mesh


def wipe():
    for obj in list(bpy.data.objects):
        if obj.type in {"CAMERA", "LIGHT"}:
            continue
        bpy.data.objects.remove(obj, do_unlink=True)
    for col in list(bpy.data.collections):
        bpy.data.collections.remove(col)
    for action in list(bpy.data.actions):
        action.user_clear()
        bpy.data.actions.remove(action)
    for datablocks in (bpy.data.meshes, bpy.data.materials, bpy.data.images, bpy.data.curves):
        for block in list(datablocks):
            if block.users == 0:
                datablocks.remove(block)


def collection(name):
    col = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(col)
    return col


def principled(name, color, rough, spec=0.28):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    mat.use_backface_culling = False
    mat.diffuse_color = (*color, 1.0)
    bsdf = next(node for node in mat.node_tree.nodes if node.type == "BSDF_PRINCIPLED")
    sock(bsdf, "Base Color").default_value = (*color, 1.0)
    sock(bsdf, "Roughness").default_value = rough
    sock(bsdf, "Metallic").default_value = 0.0
    sock(bsdf, "Specular IOR Level").default_value = spec
    return mat, bsdf


def stripe_image(name, base, vein):
    w, h = 96, 384
    img = bpy.data.images.new(name, w, h, alpha=False, float_buffer=True)
    img.colorspace_settings.name = "sRGB"
    pixels = [0.0] * (w * h * 4)
    for y in range(h):
        v = y / (h - 1)
        lift = 0.86 + 0.18 * v
        row = y * w * 4
        for x in range(w):
            u = x / (w - 1)
            stripe = 0.0
            for k in range(N_VEINS):
                center = (k + 0.5) / N_VEINS
                d = u - center
                stripe = max(stripe, math.exp(-(d * d) / (2 * 0.012 ** 2)))
            col = []
            for i in range(3):
                mixed = base[i] * (1.0 - 0.18 * stripe) + vein[i] * 0.18 * stripe
                col.append(max(0.0, min(1.0, mixed * lift)))
            i0 = row + x * 4
            pixels[i0 : i0 + 4] = (*col, 1.0)
    img.pixels.foreach_set(pixels)
    img.pack()
    return img


def sand_image():
    w = h = 192
    img = bpy.data.images.new("CrSandGrain", w, h, alpha=False, float_buffer=True)
    img.colorspace_settings.name = "sRGB"
    base = srgb(0.84, 0.74, 0.56)
    light = srgb(0.92, 0.84, 0.66)
    shade = srgb(0.70, 0.58, 0.42)
    pixels = [0.0] * (w * h * 4)
    for y in range(h):
        for x in range(w):
            u = x / (w - 1)
            v = y / (h - 1)
            dune = 0.5 + 0.5 * math.sin(u * 9.0 + v * 4.0)
            mote = 0.5 + 0.5 * math.sin(u * 22.0 - v * 17.0 + 1.3)
            grain = 0.72 * dune + 0.28 * mote
            col = []
            for i in range(3):
                c = base[i] * (0.9 + 0.1 * grain) + light[i] * 0.05 * dune + shade[i] * 0.06 * (1.0 - grain)
                col.append(max(0.0, min(1.0, c)))
            i0 = (y * w + x) * 4
            pixels[i0 : i0 + 4] = (*col, 1.0)
    img.pixels.foreach_set(pixels)
    img.pack()
    return img


def attach_image(mat, img):
    bsdf = next(node for node in mat.node_tree.nodes if node.type == "BSDF_PRINCIPLED")
    tex = mat.node_tree.nodes.new("ShaderNodeTexImage")
    tex.image = img
    mat.node_tree.links.new(out_sock(tex, "Color"), sock(bsdf, "Base Color"))
    return mat


def tube_z(name, length, rx, ry, sides=12, caps=True, z0=0.0, rx2=None, ry2=None):
    rx2 = rx if rx2 is None else rx2
    ry2 = ry if ry2 is None else ry2
    bm = bmesh.new()
    rings = []
    for z, rxx, ryy in ((z0, rx, ry), (z0 + length, rx2, ry2)):
        ring = []
        for i in range(sides):
            a = i / sides * math.pi * 2
            ring.append(bm.verts.new((math.cos(a) * rxx, math.sin(a) * ryy, z)))
        rings.append(ring)
    for i in range(sides):
        j = (i + 1) % sides
        bm.faces.new((rings[0][i], rings[0][j], rings[1][j], rings[1][i]))
    if caps:
        bm.faces.new(tuple(reversed(rings[0])))
        bm.faces.new(tuple(rings[1]))
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    return bm_to_mesh(bm, name)


def leaf_mesh(name, length, bow, twist):
    half_w = LEAF_W * 0.5
    half_t = 0.00032
    body = length - half_w
    n_body = 16
    n_cap = 8
    n_around = 14
    rings = []
    for i in range(n_body + 1):
        t = i / n_body
        z = body * t
        taper = 0.86 + 0.14 * min(1.0, t * 5.0)
        rings.append((z, half_w * taper, half_t))
    for i in range(1, n_cap + 1):
        a = (i / n_cap) * (math.pi * 0.5)
        z = body + half_w * math.sin(a)
        rings.append((z, max(half_w * math.cos(a), 0.00012), max(half_t * math.cos(a), 0.00005)))
    bm = bmesh.new()
    uv_layer = bm.loops.layers.uv.new("UVMap")
    vert_rings = []
    uv_rings = []
    for z, rx, ry in rings:
        bow_y = bow * math.sin(math.pi * min(z / length, 1.0))
        twist_a = twist * (z / length)
        ct, st = math.cos(twist_a), math.sin(twist_a)
        ring = []
        uvs = []
        for j in range(n_around):
            ang = j / n_around * math.pi * 2
            x = rx * math.cos(ang)
            y = ry * math.sin(ang) + bow_y
            xr = x * ct - y * st
            yr = x * st + y * ct
            ring.append(bm.verts.new((xr, yr, z)))
            uvs.append((0.5 + 0.5 * math.cos(ang), min(z / length, 1.0)))
        vert_rings.append(ring)
        uv_rings.append(uvs)
    for i in range(len(vert_rings) - 1):
        for j in range(n_around):
            j2 = (j + 1) % n_around
            face = bm.faces.new(
                (
                    vert_rings[i][j],
                    vert_rings[i][j2],
                    vert_rings[i + 1][j2],
                    vert_rings[i + 1][j],
                )
            )
            coords = (
                uv_rings[i][j],
                uv_rings[i][j2],
                uv_rings[i + 1][j2],
                uv_rings[i + 1][j],
            )
            for loop, uv in zip(face.loops, coords):
                loop[uv_layer].uv = uv
    base = bm.faces.new(tuple(reversed(vert_rings[0])))
    for loop, vert in zip(base.loops, reversed(vert_rings[0])):
        j = vert_rings[0].index(vert)
        loop[uv_layer].uv = uv_rings[0][j]
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    return bm_to_mesh(bm, name)


def root_mesh(name, length):
    pts = []
    radii = []
    steps = 10
    for i in range(steps):
        t = i / (steps - 1)
        if t < 0.62:
            z = 0.0024 - t * 0.0045
            radial = t * 0.03
        else:
            u = (t - 0.62) / 0.38
            z = 0.0024 - 0.62 * 0.0045 - u * length
            radial = 0.62 * 0.03 + u * 0.004
        y = 0.0016 * math.sin(t * math.pi)
        pts.append(Vector((radial, y, z)))
        radii.append(0.0007 * (1.0 - 0.45 * t))
    return skin(name, pts, radii, sides=5)


def skin(name, pts, radii, sides=8):
    bm = bmesh.new()
    rings = []
    for i, p in enumerate(pts):
        if i < len(pts) - 1:
            tangent = pts[i + 1] - pts[i]
        else:
            tangent = pts[i] - pts[i - 1]
        if tangent.length < 1e-8:
            tangent = Vector((0, 0, 1))
        tangent.normalize()
        helper = Vector((0, 1, 0))
        if abs(tangent.dot(helper)) > 0.92:
            helper = Vector((1, 0, 0))
        side = tangent.cross(helper).normalized()
        up = side.cross(tangent).normalized()
        ring = []
        for j in range(sides):
            a = j / sides * math.pi * 2
            pos = p + side * (math.cos(a) * radii[i]) + up * (math.sin(a) * radii[i])
            ring.append(bm.verts.new(pos))
        rings.append(ring)
    for i in range(len(rings) - 1):
        for j in range(sides):
            j2 = (j + 1) % sides
            bm.faces.new((rings[i][j], rings[i][j2], rings[i + 1][j2], rings[i + 1][j]))
    bm.faces.new(tuple(reversed(rings[0])))
    bm.faces.new(tuple(rings[-1]))
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    return bm_to_mesh(bm, name)


def build_sand(mat):
    bm = bmesh.new()
    uv_layer = bm.loops.layers.uv.new("UVMap")
    nx, ny = 90, 58
    x0, x1 = -0.26, 0.26
    y0, y1 = -0.18, 0.18
    grid = []
    for j in range(ny + 1):
        y = y0 + (y1 - y0) * j / ny
        row = []
        for i in range(nx + 1):
            x = x0 + (x1 - x0) * i / nx
            row.append(bm.verts.new((x, y, sand_height(x, y))))
        grid.append(row)
    for j in range(ny):
        for i in range(nx):
            vs = (grid[j][i], grid[j][i + 1], grid[j + 1][i + 1], grid[j + 1][i])
            center = sum((v.co for v in vs), Vector()) / 4.0
            if not sand_inside(center.x, center.y):
                continue
            face = bm.faces.new(vs)
            for loop in face.loops:
                u = (loop.vert.co.x - x0) / (x1 - x0)
                v = (loop.vert.co.y - y0) / (y1 - y0)
                loop[uv_layer].uv = (u, v)
    bm.verts.ensure_lookup_table()
    moved = set()
    for edge in bm.edges:
        if not edge.is_boundary:
            continue
        for vert in edge.verts:
            if vert.index in moved:
                continue
            moved.add(vert.index)
            ang = math.atan2(vert.co.y, vert.co.x)
            rx, ry = sand_radii(math.cos(ang), math.sin(ang))
            vert.co.x = rx * math.cos(ang)
            vert.co.y = ry * math.sin(ang)
            vert.co.z = sand_height(vert.co.x, vert.co.y)
    boundary = [edge for edge in bm.edges if edge.is_boundary]
    extruded = bmesh.ops.extrude_edge_only(bm, edges=boundary)
    for vert in extruded["geom"]:
        if isinstance(vert, bmesh.types.BMVert):
            vert.co.z = -0.016
    bottom = [edge for edge in bm.edges if edge.is_boundary]
    filled = bmesh.ops.holes_fill(bm, edges=bottom, sides=0)
    for face in filled.get("faces", []):
        for loop in face.loops:
            loop[uv_layer].uv = (0.5, 0.5)
    loose = [vert for vert in bm.verts if not vert.link_faces]
    if loose:
        bmesh.ops.delete(bm, geom=loose, context="VERTS")
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    mesh = bm_to_mesh(bm, "ReefSand")
    mesh.materials.append(mat)
    return mesh


def spawn(name, mesh, col, parent, loc, rot=None):
    obj = bpy.data.objects.new(name, mesh)
    col.objects.link(obj)
    obj.parent = parent
    obj.location = loc
    obj.rotation_mode = "XYZ"
    if rot is not None:
        obj.rotation_euler = rot
    return obj


def euler_along_z(direction):
    quat = direction.to_track_quat("Z", "Y")
    euler = quat.to_euler("XYZ")
    return (euler.x, euler.y, euler.z)


def fan_euler(azimuth, tilt):
    rot = Matrix.Rotation(azimuth, 4, "Z") @ Matrix.Rotation(tilt, 4, "X")
    euler = rot.to_euler("XYZ")
    return (euler.x, euler.y, euler.z)


def mix_eul(a, b, t):
    ea = Euler(a, "XYZ").to_quaternion()
    eb = Euler(b, "XYZ").to_quaternion()
    euler = ea.slerp(eb, t).to_euler("XYZ")
    return (euler.x, euler.y, euler.z)


def dedupe(keys):
    found = {}
    for frame, value in keys:
        found[int(frame)] = value
    return [(frame, found[frame]) for frame in sorted(found)]


def key_scale(obj, action, keys):
    obj.animation_data_create()
    obj.animation_data.action = action
    for frame, scl in dedupe(keys):
        obj.scale = scl
        obj.keyframe_insert(data_path="scale", frame=frame)


def key_rot(obj, keys):
    obj.rotation_mode = "XYZ"
    for frame, eul in dedupe(keys):
        obj.rotation_euler = eul
        obj.keyframe_insert(data_path="rotation_euler", frame=frame)


def polish(action):
    for layer in action.layers:
        for strip in layer.strips:
            if strip.type != "KEYFRAME":
                continue
            for slot in action.slots:
                bag = strip.channelbag(slot)
                if bag is None:
                    continue
                for fcurve in bag.fcurves:
                    for kp in fcurve.keyframe_points:
                        kp.interpolation = "BEZIER"
                        kp.handle_left_type = "AUTO_CLAMPED"
                        kp.handle_right_type = "AUTO_CLAMPED"
                    for kp in fcurve.keyframe_points:
                        if abs(kp.co[0] - HOLD) < 0.1:
                            kp.interpolation = "CONSTANT"


def shoot_times(i):
    if i == 0:
        return 1, 200
    if i <= 3:
        return 120 + (i - 1) * 18, 188
    return 198 + (i - 4) * 16, 286


def segment_times(i):
    t0 = 40 + int(i * (64 / 8))
    return t0, t0 + 22


def build():
    wipe()
    scene = bpy.context.scene
    scene.render.fps = 30
    scene.render.fps_base = 1.0
    scene.frame_start = 1
    scene.frame_end = END
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0

    cols = {
        "Environment": collection("Environment"),
        "Rhizome": collection("Rhizome"),
        "Roots": collection("Roots"),
        "Shoots": collection("Shoots"),
        "Leaves": collection("Leaves"),
    }
    root = bpy.data.objects.new("Cymodocea", None)
    cols["Environment"].objects.link(root)
    root.empty_display_size = 0.02

    leaf = srgb(0.24, 0.48, 0.22)
    vein = srgb(0.10, 0.28, 0.12)
    young = srgb(0.48, 0.70, 0.36)
    young_vein = srgb(0.28, 0.48, 0.22)
    rhizome_c = srgb(0.74, 0.66, 0.48)
    root_c = srgb(0.94, 0.88, 0.74)
    sheath_c = srgb(0.62, 0.70, 0.42)
    stem_c = srgb(0.70, 0.66, 0.44)
    ring_c = srgb(0.58, 0.48, 0.32)
    sand_c = srgb(0.84, 0.74, 0.56)

    mat_leaf, _ = principled("CrLeaf", leaf, 0.58, 0.22)
    mat_young, _ = principled("CrLeafYoung", young, 0.62, 0.2)
    attach_image(mat_leaf, stripe_image("CrLeafVeins", leaf, vein))
    attach_image(mat_young, stripe_image("CrYoungVeins", young, young_vein))
    mat_rhiz, _ = principled("CrRhizome", rhizome_c, 0.5, 0.18)
    mat_root, _ = principled("CrRoot", root_c, 0.72, 0.12)
    mat_sheath, _ = principled("CrSheath", sheath_c, 0.6, 0.16)
    mat_stem, _ = principled("CrStem", stem_c, 0.55, 0.16)
    mat_ring, _ = principled("CrScar", ring_c, 0.48, 0.2)
    mat_sand, _ = principled("CrSand", sand_c, 0.94, 0.08)
    attach_image(mat_sand, sand_image())

    sand = spawn("ReefSand", build_sand(mat_sand), cols["Environment"], root, (0, 0, 0))

    nodes = [node_pos(i) for i in range(N_SHOOTS)]
    action = bpy.data.actions.new("Grow")
    stem_h = 0.022
    sheath_h = 0.02
    records = []

    for i in range(N_SHOOTS - 1):
        a = nodes[i]
        b = nodes[i + 1]
        direction = b - a
        length = direction.length
        mesh = tube_z(
            f"RhizomeMesh_{i}",
            length + 0.008,
            0.00245,
            0.00245,
            sides=16,
            caps=True,
            z0=-0.004,
        )
        mesh.materials.append(mat_rhiz)
        obj = spawn(
            f"Rhizome_{i}",
            mesh,
            cols["Rhizome"],
            root,
            a,
            euler_along_z(direction),
        )
        t0, t1 = segment_times(i)
        key_scale(
            obj,
            action,
            [
                (1, TINY),
                (t0 - 1, TINY),
                (t0, (1.0, 1.0, 0.04)),
                (t1, FULL),
                (HOLD, FULL),
                (END, TINY),
            ],
        )
        records.append(obj)

    root_angles = (0.4, 2.3, 4.4)
    for i, pos in enumerate(nodes):
        for r, az in enumerate(root_angles):
            if r == 2 and i % 3 == 0:
                continue
            length = 0.022 + (i % 3) * 0.004
            mesh = root_mesh(f"RootMesh_{i}_{r}", length)
            mesh.materials.append(mat_root)
            rot = Matrix.Rotation(az + i * 0.17, 4, "Z").to_euler("XYZ")
            obj = spawn(
                f"Root_{i}_{r}",
                mesh,
                cols["Roots"],
                root,
                pos,
                (rot.x, rot.y, rot.z),
            )
            if i == 0:
                t0, t1 = 52, 88
            else:
                _, seg_end = segment_times(i - 1)
                t0, t1 = seg_end, seg_end + 24
            key_scale(
                obj,
                action,
                [
                    (1, TINY),
                    (t0, TINY),
                    (t1, FULL),
                    (HOLD, FULL),
                    (END, TINY),
                ],
            )

    stem_mesh = tube_z("StemMesh", stem_h, 0.0017, 0.0017, sides=12, caps=True)
    stem_mesh.materials.append(mat_stem)
    sheath_mesh = tube_z(
        "SheathMesh",
        sheath_h,
        0.0052,
        0.0036,
        sides=16,
        caps=False,
        rx2=0.0074,
        ry2=0.0046,
    )
    sheath_mesh.materials.append(mat_sheath)
    ring_mesh = tube_z("RingMesh", 0.0023, 0.00315, 0.00315, sides=16, caps=True)
    ring_mesh.materials.append(mat_ring)

    leaf_checks = []
    for i, pos in enumerate(nodes):
        yaw = (i - 4) * 0.18 + math.sin(i * 1.7) * 0.7
        t0, t1 = shoot_times(i)
        bud_stem = (1.0, 1.0, 0.58)
        stem = spawn("Stem_%d" % i, stem_mesh, cols["Shoots"], root, pos)
        if i == 0:
            stem_keys = [
                (1, bud_stem),
                (40, bud_stem),
                (150, FULL),
                (HOLD, FULL),
                (END, bud_stem),
            ]
        else:
            stem_keys = [
                (1, TINY),
                (t0 - 1, TINY),
                (t0, (1.0, 1.0, 0.05)),
                (t0 + 34, FULL),
                (HOLD, FULL),
                (END, TINY),
            ]
        key_scale(stem, action, stem_keys)
        sheath_origin = pos + Vector((0, 0, stem_h * 0.62))
        bud_sheath = (1.0, 1.0, 0.5)
        sheath = spawn("Sheath_%d" % i, sheath_mesh, cols["Shoots"], root, sheath_origin)
        if i == 0:
            sheath_keys = [
                (1, bud_sheath),
                (40, bud_sheath),
                (170, FULL),
                (HOLD, FULL),
                (END, bud_sheath),
            ]
        else:
            sheath_keys = [
                (1, TINY),
                (t0 + 3, TINY),
                (t0 + 4, (1.0, 1.0, 0.08)),
                (t0 + 40, FULL),
                (HOLD, FULL),
                (END, TINY),
            ]
        key_scale(sheath, action, sheath_keys)
        for k, frac in enumerate((0.2, 0.38, 0.56)):
            loc = pos + Vector((0, 0, stem_h * frac))
            ring = spawn("Ring_%d_%d" % (i, k), ring_mesh, cols["Shoots"], root, loc)
            if i == 0 and k == 0:
                key_scale(ring, action, [(1, FULL), (HOLD, FULL), (END, FULL)])
                continue
            appear = (112 + k * 18) if i == 0 else (t0 + 6 + k * 8)
            key_scale(
                ring,
                action,
                [
                    (1, TINY),
                    (appear, TINY),
                    (appear + 8, FULL),
                    (HOLD, FULL),
                    (END, TINY),
                ],
            )
        for j, length in enumerate(LENGTHS[i]):
            az, tilt = FANS[j]
            az += yaw + RNG.uniform(-0.05, 0.05)
            tilt += RNG.uniform(-0.03, 0.04)
            bow = BOWS[j] + RNG.uniform(-0.001, 0.001)
            twist = RNG.uniform(-0.12, 0.12)
            mesh = leaf_mesh("LeafMesh_%d_%d" % (i, j), length, bow, twist)
            young_leaf = i >= 7 or j == 3
            mesh.materials.append(mat_young if young_leaf else mat_leaf)
            opened = fan_euler(az, tilt)
            folded = fan_euler(az * 0.18, 0.05)
            leaf_obj = spawn(
                "Leaf_%d_%d" % (i, j),
                mesh,
                cols["Leaves"],
                root,
                sheath_origin,
                opened,
            )
            local_x = [v.co.x for v in mesh.vertices]
            local_z = [v.co.z for v in mesh.vertices]
            width = max(local_x) - min(local_x)
            tall = max(local_z) - min(local_z)
            leaf_checks.append((leaf_obj.name, width, tall))
            if i == 0:
                bud = (0.88, 0.34, 0.34)
                key_scale(
                    leaf_obj,
                    action,
                    [
                        (1, bud),
                        (40, (0.9, 0.38, 0.38)),
                        (130, (0.94, 0.62, 0.62)),
                        (210, FULL),
                        (HOLD, FULL),
                        (END, bud),
                    ],
                )
                key_rot(
                    leaf_obj,
                    [
                        (1, folded),
                        (40, folded),
                        (150, mix_eul(folded, opened, 0.5)),
                        (210, opened),
                        (HOLD, opened),
                        (END, folded),
                    ],
                )
            else:
                bud = TINY
                key_scale(
                    leaf_obj,
                    action,
                    [
                        (1, TINY),
                        (t0, TINY),
                        (t0 + 8, (0.82, 0.14, 0.14)),
                        (t1, FULL),
                        (HOLD, FULL),
                        (END, TINY),
                    ],
                )
                key_rot(
                    leaf_obj,
                    [
                        (1, folded),
                        (t0, folded),
                        ((t0 + t1) // 2, mix_eul(folded, opened, 0.45)),
                        (t1, opened),
                        (HOLD, opened),
                        (END, folded),
                    ],
                )
            records.append(leaf_obj)

    polish(action)
    action.use_frame_range = True
    action.frame_start = 1
    action.frame_end = END

    for name, width, tall in leaf_checks:
        if not (0.0065 <= width <= 0.012):
            raise RuntimeError("leaf width %s %.4f" % (name, width))
        if not (0.065 <= tall <= 0.16):
            raise RuntimeError("leaf length %s %.4f" % (name, tall))

    scene.frame_set(300)
    arm = scene.view_layers[0]
    arm.update()

    world = scene.world or bpy.data.worlds.new("World")
    scene.world = world
    world.use_nodes = True
    bg = next(node for node in world.node_tree.nodes if node.type == "BACKGROUND")
    water = srgb(0x1E / 255, 0x8C / 255, 0x98 / 255)
    sock(bg, "Color").default_value = (*water, 1.0)
    sock(bg, "Strength").default_value = 0.85

    sun = bpy.data.objects.get("Light")
    if sun and sun.type == "LIGHT":
        sun.data.type = "SUN"
        sun.data.energy = 3.2
        sun.data.angle = 0.55
        sun.data.color = (1.0, 0.97, 0.9)
        sun.rotation_euler = (math.radians(52), math.radians(6), math.radians(-38))

    cam = bpy.data.objects.get("Camera")
    if cam:
        cam.location = (0.2, -0.32, 0.16)
        direction = Vector((0.0, 0.0, 0.06)) - cam.location
        cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
        cam.data.lens = 50
        cam.data.clip_start = 0.01
        cam.data.clip_end = 20

    print("shoots", N_SHOOTS, "slots", len(action.slots), "leaves", len(leaf_checks))
    print("leaf0", leaf_checks[0], "leafLast", leaf_checks[-1])
    for frame in (1, 80, 160, 300, 330):
        scene.frame_set(frame)
        seg = bpy.data.objects["Rhizome_0"]
        leaf0 = bpy.data.objects["Leaf_0_0"]
        leaf_tip = bpy.data.objects["Leaf_8_0"]
        print(
            "f",
            frame,
            "rhiz",
            round(seg.scale.z, 3),
            "leaf0",
            round(leaf0.scale.z, 3),
            "tip",
            round(leaf_tip.scale.z, 3),
        )
    scene.frame_set(300)
    bpy.ops.wm.save_mainfile()
    print("saved", bpy.data.filepath)


build()

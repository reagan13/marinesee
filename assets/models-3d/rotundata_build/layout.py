"""First-time layout: CR_Controls, Authoring curves and shoot empties, the empty armature."""

import math
import random

import bpy
from mathutils import Matrix, Vector

from .config import CONFIG, HOW_TO, leaf_count
from .sand import sand_height
from .util import collection, layer_collection, link, set_bezier, tag

UP = Vector((0.0, 0.0, 1.0))


# Three passes across the bed, not a clump in the middle.
# Spacing stays inside 1–4.5 cm. Depth is a display choice, not a Mati measurement.
LESSON_XY = (
    (-0.1320, -0.0166),
    (-0.0943, -0.0166),
    (-0.0566, -0.0166),
    (-0.0189, -0.0166),
    (0.0189, -0.0166),
    (0.0566, -0.0166),
    (0.0943, -0.0166),
    (0.1320, -0.0166),
    (0.1180, 0.0220),
    (0.0823, 0.0231),
    (0.0466, 0.0243),
    (0.0109, 0.0254),
    (-0.0249, 0.0266),
    (-0.0606, 0.0277),
    (-0.0963, 0.0289),
    (-0.1320, 0.0300),
    (-0.1180, 0.0580),
    (-0.0770, 0.0587),
    (-0.0360, 0.0593),
    (0.0050, 0.0600),
    (0.0460, 0.0607),
    (0.0870, 0.0613),
    (0.1280, 0.0620),
)


def node_xy(count, span, rng):
    from .config import CONFIG

    if CONFIG.get("variant") == "lesson":
        return list(LESSON_XY)
    if CONFIG.get("variant") == "realistic":
        # Three tufts, not one row. The rhizome still connects them.
        spots = ((-0.10, 0.012), (-0.01, -0.028), (0.09, 0.018))
        groups = (count // 3, count // 3, count - 2 * (count // 3))
        out = []
        n = 0
        for (cx, cy), group in zip(spots, groups):
            for k in range(group):
                ang = k * 2.2 + n * 0.4
                out.append((cx + 0.016 * math.cos(ang), cy + 0.013 * math.sin(ang)))
                n += 1
        return out
    xs, x = [], 0.0
    for _i in range(count):
        xs.append(x)
        x += 0.78 + 0.44 * rng.random()
    scale = span / (xs[-1] - xs[0])
    mid = 0.5 * (xs[0] + xs[-1])
    out = []
    for i, x in enumerate(xs):
        t = i / (count - 1)
        y = -0.034 + 0.011 * math.sin(t * math.pi * 1.65 + 0.35) + 0.0045 * math.sin(i * 1.25)
        out.append(((x - mid) * scale, y))
    return out


def new_curve(name, points, col):
    data = bpy.data.curves.new(name, "CURVE")
    data.dimensions = "3D"
    spline = data.splines.new("BEZIER")
    set_bezier(spline, points)
    obj = bpy.data.objects.new(name, data)
    link(obj, col)
    obj.hide_render = True
    return tag(obj)


def shoot_frame(i, count):
    from .config import CONFIG

    if CONFIG.get("variant") == "lesson":
        # Face the front camera, with a small yaw so the shoots are not clones.
        yaw = 0.16 * math.sin(i * 1.3 + 0.4)
        lean_x = 0.035 * math.sin(i * 0.9)
        lean_y = 0.02
    else:
        yaw = 0.48 * math.sin(i * 1.7 + 0.3) + 0.18 * math.cos(i * 0.8) + 0.02 * (i - 0.5 * (count - 1))
        lean_x = 0.06 * math.sin(i * 0.95)
        lean_y = 0.04 + 0.03 * math.cos(i * 1.1)
    right = Vector((math.cos(yaw), math.sin(yaw), 0.0))
    forward = Vector((-math.sin(yaw), math.cos(yaw), 0.0))
    stem = (UP + right * lean_x + forward * lean_y).normalized()
    right = (right - stem * right.dot(stem)).normalized()
    forward = stem.cross(right).normalized()
    return stem, right, forward


def leaf_points(node, stem, right, forward, tilt, length, fwd, bow, cfg):
    height = cfg["stem_height_m"]
    base = node + stem * (height * cfg["leaf_base_frac"])
    exit_ = node + stem * (height * 1.02) + right * (0.0012 * tilt)
    direction = (stem * math.cos(tilt) + right * math.sin(tilt)).normalized()
    out = (right * math.cos(tilt) - stem * math.sin(tilt)) * (1.0 if tilt >= 0 else -1.0)
    reach = length - (exit_ - base).length
    mid = exit_ + direction * (reach * 0.52) - out * (bow * 0.45) + forward * (fwd * 0.7)
    tip = exit_ + direction * reach + out * (bow * 0.85) + forward * (fwd * 1.15)
    return [base, exit_, mid, tip]


def plan_leaves(i, count, rng, cfg):
    n = leaf_count(i)
    spread = 0.58 if n > 2 else 0.32
    tilts = [(-spread + 2 * spread * j / (n - 1)) + rng.uniform(-0.09, 0.09) for j in range(n)]
    lo, hi = cfg["leaf_length_m"]
    age = 1.0 - 0.32 * max(0.0, (i - (count - 4)) / 3.0)
    young_shoot = i >= count - 3
    order = sorted(range(n), key=lambda j: abs(tilts[j]))
    leaves = []
    for j in range(n):
        rank = order.index(j) / max(1, n - 1)
        length = (lo + (hi - lo) * (0.32 + 0.68 * rank) * rng.uniform(0.84, 1.02)) * age
        if cfg.get("variant") == "realistic":
            length = 0.042 + 0.028 * rank
        rank_sign = 1.0 if j % 2 == 0 else -1.0
        if cfg.get("variant") == "lesson":
            # Two ranks, a few millimetres apart, so the shoot is not one flat comb.
            # Shoot 0's second leaf is turned enough that a close view shows the thin edge.
            fwd = 0.011 * rank_sign
            bow = 0.0035
            twist = 1.05 if (i == 0 and j == 1) else 0.20 * rank_sign
        else:
            fwd = (0.006 if j % 2 else -0.004) * rng.uniform(0.6, 1.3)
            bow = (0.003 + 0.002 * rng.random()) if cfg.get("variant") == "realistic" else (0.010 + 0.008 * rng.random())
            twist = rng.uniform(-0.28, 0.28)
        leaves.append({
            "tilt": tilts[j],
            "length": length if cfg.get("variant") == "realistic" else max(lo, min(hi, length)),
            "young": young_shoot or order[0] == j,
            "fwd": fwd,
            "bow": bow,
            "twist": twist,
        })
    return leaves


def _root_points(node, i, r, bottom, rng):
    """Roots grow down. On the lesson cut, one root stays in the wall; the rest stay buried."""
    from .config import CONFIG

    if CONFIG.get("variant") == "lesson":
        max_len = max(0.012, node.z - (bottom + 0.004))
        length = min(max_len, 0.016 + 0.005 * ((i + r) % 3))
        on_cut = node.y < -0.014
        if on_cut:
            # A fan down the face: left, down, and right. Not one shared line.
            fan = (-1.0, 0.05, 1.0)[r % 3]
            length = min(max_len, 0.016 + 0.007 * (r % 3))
            reach = 0.005 + 0.006 * abs(fan)
            return [
                node + Vector((0.0005 * fan, -0.0010, -0.0008)),
                node + Vector((reach * fan * 0.45, -0.0026, -length * 0.48)),
                node + Vector((reach * fan, -0.0038, -length)),
            ]
        ang = i * 0.85 + r * 2.15
        length = min(max_len, 0.014 + 0.005 * (r % 2))
        dx = math.cos(ang) * (0.005 + 0.004 * r)
        dy = 0.003 + abs(math.sin(ang)) * 0.007
        return [
            node + Vector((0.0003, 0.0002, -0.0005)),
            node + Vector((dx * 0.45, dy * 0.4, -length * 0.5)),
            node + Vector((dx, dy, -length)),
        ]
    short = CONFIG.get("variant") == "realistic"
    max_len = max(0.010, node.z - (bottom + 0.0035))
    length = min(max_len, (0.011 if short else 0.020) + 0.003 * ((i + r) % 3))
    down = Vector((0.0, 0.0, -1.0))
    if r < 2:
        side_sign = -1.0 if r == 0 else 1.0
        dx1 = side_sign * (0.0032 + 0.0015 * rng.random())
        dx2 = side_sign * (0.0065 + 0.0030 * rng.random()) + 0.0015 * math.sin(i + r)
        # Keep Y slightly in front of the cutaway wall (node.y + 0.0005) so the root never hides inside the sand
        p0 = node + Vector((side_sign * 0.0008, -0.0009, -0.0006))
        p1 = node + Vector((dx1, -0.0010, -length * 0.42))
        p2 = node + Vector((dx2, -0.0007, -length))
        return [p0, p1, p2]
    ang = 0.6 + 0.5 * math.sin(i * 1.3)
    out = Vector((math.cos(ang) * 0.005, abs(math.sin(ang)) * 0.009 + 0.005, 0.0))
    return [
        node + Vector((0.0, 0.001, -0.0008)),
        node + out * 0.55 + down * (length * 0.45),
        node + out + down * length,
    ]


def create_plant(cfg=CONFIG):
    rng = random.Random(cfg["seed"])
    count = cfg["shoot_count"]
    scene_col = bpy.context.scene.collection

    controls = bpy.data.objects.new("CR_Controls", None)
    scene_col.objects.link(controls)
    controls.empty_display_size = 0.015
    controls["leaf_width_m"] = cfg["leaf_width_m"]
    controls["leaf_thickness_m"] = cfg["leaf_thickness_m"]
    controls["vein_count"] = cfg["vein_count"]
    controls["shoot_count"] = count
    tag(controls)

    authoring = collection("Authoring")
    collection("Meadow")

    xy = node_xy(count, cfg["rhizome_span_m"], rng)
    count = len(xy)
    sink = cfg["rhizome_sink_m"]
    nodes = [Vector((x, y, sand_height(x, y, xy) - sink)) for x, y in xy]
    points = []
    for k, node in enumerate(nodes):
        points.append(node)
        if k < count - 1:
            m = (node + nodes[k + 1]) * 0.5
            m.z = sand_height(m.x, m.y, xy) - sink
            points.append(m)
    lead = (nodes[-1] - nodes[-2]).normalized()
    tip = nodes[-1] + lead * 0.012
    tip.z = sand_height(tip.x, tip.y, xy) - sink * 1.3
    points.append(tip)
    rhizome = new_curve("CR_Rhizome", points, authoring)
    rhizome["cr_nodes"] = count

    bottom = cfg["sand_bottom_z"]
    for i, node in enumerate(nodes):
        stem, right, forward = shoot_frame(i, count)
        emp = bpy.data.objects.new("CR_Shoot_%02d" % i, None)
        link(emp, authoring)
        emp.empty_display_type = "SINGLE_ARROW"
        emp.empty_display_size = cfg["stem_height_m"]
        emp.matrix_world = Matrix.Translation(node) @ Matrix((right, forward, stem)).transposed().to_4x4()
        tag(emp)
        for j, leaf in enumerate(plan_leaves(i, count, rng, cfg)):
            pts = leaf_points(node, stem, right, forward, leaf["tilt"], leaf["length"], leaf["fwd"], leaf["bow"], cfg)
            obj = new_curve("CR_Leaf_%02d_%d" % (i, j), pts, authoring)
            obj["cr_shoot"] = i
            obj["cr_young"] = 1 if leaf["young"] else 0
            obj["cr_twist"] = leaf["twist"]
        root_counts = cfg.get("root_counts")
        n_roots = root_counts[i % len(root_counts)] if root_counts else (2 if i % 3 == 2 else 3)
        for r in range(n_roots):
            pts = _root_points(node, i, r, bottom, rng)
            new_curve("CR_Root_%02d_%d" % (i, r), pts, authoring)
    if cfg.get("variant") == "lesson":
        for a, b in zip(nodes, nodes[1:]):
            print("lesson chord_cm", round((a - b).length * 100, 2))

    arm = bpy.data.objects.new("CR_Armature", bpy.data.armatures.new("CR_Armature"))
    scene_col.objects.link(arm)
    arm.show_in_front = True
    tag(arm)

    text = bpy.data.texts.get("CR_HOW_TO_EDIT") or bpy.data.texts.new("CR_HOW_TO_EDIT")
    text.clear()
    text.write(HOW_TO)

    lc = layer_collection("Authoring")
    if lc:
        lc.hide_viewport = True
    authoring.hide_render = True
    return arm

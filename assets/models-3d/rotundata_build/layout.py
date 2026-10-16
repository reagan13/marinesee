"""First-time layout: CR_Controls, Authoring curves and shoot empties, the empty armature."""

import math
import random

import bpy
from mathutils import Matrix, Vector

from .config import CONFIG, HOW_TO, leaf_count
from .sand import sand_height
from .util import collection, layer_collection, link, set_bezier, tag

UP = Vector((0.0, 0.0, 1.0))


def node_xy(count, span, rng):
    xs, x = [], 0.0
    for _i in range(count):
        xs.append(x)
        x += 0.8 + 0.4 * rng.random()
    scale = span / (xs[-1] - xs[0])
    mid = 0.5 * (xs[0] + xs[-1])
    out = []
    for i, x in enumerate(xs):
        t = i / (count - 1)
        y = 0.040 * math.sin(t * math.pi * 1.6 + 0.4) + 0.009 * math.sin(i * 1.15)
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
    yaw = 0.62 * math.sin(i * 1.7 + 0.3) + 0.22 * math.cos(i * 0.7) + 0.02 * (i - 0.5 * (count - 1))
    right = Vector((math.cos(yaw), math.sin(yaw), 0.0))
    forward = Vector((-math.sin(yaw), math.cos(yaw), 0.0))
    lean = 0.05 * math.sin(i * 0.9)
    stem = (UP + right * lean + forward * 0.04 * math.cos(i)).normalized()
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
    mid = exit_ + direction * (reach * 0.5) - out * bow + forward * fwd
    tip = exit_ + direction * reach + forward * (fwd * 0.4)
    return [base, exit_, mid, tip]


def plan_leaves(i, count, rng, cfg):
    n = leaf_count(i)
    spread = 0.55 if n > 2 else 0.30
    tilts = [(-spread + 2 * spread * j / (n - 1)) + rng.uniform(-0.08, 0.08) for j in range(n)]
    lo, hi = cfg["leaf_length_m"]
    age = 1.0 - 0.35 * max(0.0, (i - (count - 4)) / 3.0)
    young_shoot = i >= count - 3
    order = sorted(range(n), key=lambda j: abs(tilts[j]))
    leaves = []
    for j in range(n):
        rank = order.index(j) / max(1, n - 1)
        length = (lo + (hi - lo) * (0.35 + 0.65 * rank) * rng.uniform(0.85, 1.0)) * age
        leaves.append({
            "tilt": tilts[j],
            "length": max(lo, min(hi, length)),
            "young": young_shoot or order[0] == j,
            "fwd": (0.004 if j % 2 else -0.004) * rng.uniform(0.6, 1.2),
            "bow": 0.008 + 0.006 * rng.random(),
            "twist": rng.uniform(-0.25, 0.25),
        })
    return leaves


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
    tip.z = sand_height(tip.x, tip.y, xy) - sink * 1.4
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
        for r in range(2 if i % 4 else 3):
            ang = r * 2.2 + i * 0.4
            out = Vector((math.cos(ang), math.sin(ang), 0.0))
            length = min(0.016 + (i % 3) * 0.006, node.z - (bottom + 0.004))
            down = Vector((0.0, 0.0, -1.0))
            pts = [node, node + out * 0.006 + down * (length * 0.3), node + out * 0.011 + down * length]
            new_curve("CR_Root_%02d_%d" % (i, r), pts, authoring)

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

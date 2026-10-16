"""CR_Armature rest pose, read from the Authoring curves and shoot empties.

Every deform bone is a direct child of an unscaled `base` bone. No bone inherits
a non-uniform scale, so Y-scale on one bone never shears another in glTF.
"""

import bpy
from mathutils import Vector

from .config import CONFIG
from .util import control_points, safe_hint, set_mode

UP = Vector((0.0, 0.0, 1.0))


def objects_with_prefix(prefix):
    return sorted((o for o in bpy.data.objects if o.name.startswith(prefix)), key=lambda o: o.name)


def rhizome_nodes(curve):
    pts = control_points(curve)
    count = int(curve.get("cr_nodes", (len(pts) + 1) // 2))
    return [pts[2 * k] for k in range(count)]


def shoot_axes(emp):
    m = emp.matrix_world
    return m.translation.copy(), m.col[2].xyz.normalized(), m.col[0].xyz.normalized(), m.col[1].xyz.normalized()


def layout_bones(cfg=CONFIG):
    """name -> (head, tail, roll hint) for every deform bone."""
    bones = {}
    nodes = rhizome_nodes(bpy.data.objects["CR_Rhizome"])
    for k in range(len(nodes) - 1):
        bones["rhizome_%02d" % k] = (nodes[k], nodes[k + 1], UP)
    forward = {}
    for emp in objects_with_prefix("CR_Shoot_"):
        i = emp.name[len("CR_Shoot_"):]
        origin, stem, _side, fwd = shoot_axes(emp)
        forward[i] = fwd
        bones["shoot_" + i] = (origin, origin + stem * cfg["stem_height_m"], fwd)
    for curve in objects_with_prefix("CR_Leaf_"):
        pts = control_points(curve)
        i = curve.name[len("CR_Leaf_"):].split("_")[0]
        bones["leaf_" + curve.name[len("CR_Leaf_"):]] = (pts[0], pts[-1], forward.get(i, Vector((0, 1, 0))))
    for curve in objects_with_prefix("CR_Root_"):
        pts = control_points(curve)
        bones["root_" + curve.name[len("CR_Root_"):]] = (pts[0], pts[-1], Vector((1, 0, 0)))
    return bones


def sync_bones(arm, bones):
    set_mode(arm, "EDIT")
    eb = arm.data.edit_bones
    base = eb.get("base") or eb.new("base")
    base.head = (0.0, 0.0, 0.0)
    base.tail = (0.0, 0.02, 0.0)
    base.roll = 0.0
    base.use_deform = False
    for bone in list(eb):
        if bone.name != "base" and bone.name not in bones:
            eb.remove(bone)
    for name, (head, tail, hint) in bones.items():
        bone = eb.get(name) or eb.new(name)
        bone.head = head
        bone.tail = tail
        bone.align_roll(safe_hint(tail - head, hint))
        bone.parent = base
        bone.use_connect = False
        bone.inherit_scale = "FULL"
        bone.use_deform = True
    set_mode(arm, "OBJECT")
    for pb in arm.pose.bones:
        pb.rotation_mode = "XYZ"

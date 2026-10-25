"""Stage captions for the one-minute time-lapse.

A left-side lower third, the way a short science spot carries a label:
the headline slides in, the seagrass stroke wipes, the sentence follows.
Not a title locked to the middle of the picture, and not a card.
Not part of the phone model.
"""

import bpy

from .util import collection, link, sock, srgb, tag

# Step word stays small. The two lines under it are the discussion.
# Wording follows the species record: a buried rhizome sends up new shoots.
STAGES = (
    (0.00, 0.14, "1  Bud",
     "It starts as one shoot on the sand.",
     "The rest of the patch spreads from here."),
    (0.14, 0.38, "2  Rhizome",
     "The buried stem grows through the sand.",
     "That is the usual way this seagrass takes more ground."),
    (0.38, 0.58, "3  Roots",
     "A root grows down at each node, once that node is there.",
     "Follow them in the cut face of the sand."),
    (0.58, 0.84, "4  Shoots",
     "The buried stem sends up new shoots.",
     "Each leaf unrolls into a flat strap with a rounded tip."),
    (0.84, 0.97, "5  Patch",
     "The shoots stand as a patch, not one straight row.",
     "The plant can also flower and set seed."),
)


def _material():
    mat = bpy.data.materials.get("CrCaption") or bpy.data.materials.new("CrCaption")
    mat.use_nodes = True
    mat.use_backface_culling = False
    bsdf = next(node for node in mat.node_tree.nodes if node.type == "BSDF_PRINCIPLED")
    white = srgb(1.0, 1.0, 1.0)
    sock(bsdf, "Base Color").default_value = white
    sock(bsdf, "Roughness").default_value = 0.6
    try:
        sock(bsdf, "Emission Color").default_value = white
        sock(bsdf, "Emission Strength").default_value = 0.8
    except KeyError:
        pass
    return mat


def _clear():
    names = ("CR_Caption_", "CR_Note_", "CR_Species", "CR_Rule")
    for obj in list(bpy.data.objects):
        if not obj.name.startswith(names + ("CR_More_",)):
            continue
        data = obj.data
        bpy.data.objects.remove(obj, do_unlink=True)
        if data is not None and data.users == 0:
            if isinstance(data, bpy.types.Curve):
                bpy.data.curves.remove(data)
            elif isinstance(data, bpy.types.Mesh):
                bpy.data.meshes.remove(data)


def _view(cam):
    """Half-size of the 16:9 frame at `depth` metres in front of the lens."""
    depth = 0.24
    half_w = depth * (cam.data.sensor_width * 0.5) / cam.data.lens
    half_h = half_w / (16.0 / 9.0)
    return depth, half_w, half_h


def _rule(col):
    """A short seagrass stroke under the step title. Not a panel."""
    import bmesh
    from .geometry import bm_to_mesh

    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    y = 0.0
    verts = [
        bm.verts.new((0.0, y, -0.00055)),
        bm.verts.new((0.062, y, -0.00055)),
        bm.verts.new((0.062, y, 0.00055)),
        bm.verts.new((0.0, y, 0.00055)),
    ]
    face = bm.faces.new(verts)
    for loop in face.loops:
        loop[uv].uv = (0.5, 0.5)
    mesh = bm_to_mesh(bm, "CrRuleMesh")
    mat = bpy.data.materials.get("CrRule") or bpy.data.materials.new("CrRule")
    mat.use_nodes = True
    bsdf = next(node for node in mat.node_tree.nodes if node.type == "BSDF_PRINCIPLED")
    green = srgb(0x3A / 255.0, 0xAA / 255.0, 0x40 / 255.0)
    sock(bsdf, "Base Color").default_value = green
    try:
        sock(bsdf, "Emission Color").default_value = green
        sock(bsdf, "Emission Strength").default_value = 0.6
    except KeyError:
        pass
    mesh.materials.append(mat)
    obj = bpy.data.objects.new("CR_Rule", mesh)
    link(obj, col)
    tag(obj)
    return obj


def _text(name, body, size, mat, col):
    data = bpy.data.curves.new(name, "FONT")
    data.body = body
    data.size = size
    data.align_x = "LEFT"
    aligns = [item.identifier for item in data.bl_rna.properties["align_y"].enum_items]
    if "CENTER" in aligns:
        data.align_y = "CENTER"
    data.resolution_u = 24
    data.extrude = 0.00012
    obj = bpy.data.objects.new(name, data)
    link(obj, col)
    tag(obj)
    obj.data.materials.append(mat)
    if hasattr(obj, "visible_shadow"):
        obj.visible_shadow = False
    return obj


def _curves(obj):
    action = obj.animation_data.action if obj.animation_data else None
    if action is None:
        return []
    found = []
    if hasattr(action, "layers"):
        slots = list(action.slots) if getattr(action, "slots", None) else []
        slot = getattr(obj.animation_data, "action_slot", None)
        if slot is not None and slot not in slots:
            slots.append(slot)
        for layer in action.layers:
            for strip in layer.strips:
                for item in slots:
                    try:
                        bag = strip.channelbag(item)
                    except (TypeError, RuntimeError):
                        bag = None
                    if bag is not None:
                        found.extend(bag.fcurves)
    if not found and hasattr(action, "fcurves"):
        found.extend(action.fcurves)
    return found


def _ease(obj, path):
    for fc in _curves(obj):
        if path not in fc.data_path:
            continue
        for kp in fc.keyframe_points:
            kp.interpolation = "BEZIER"
            kp.handle_left_type = "AUTO_CLAMPED"
            kp.handle_right_type = "AUTO_CLAMPED"
        fc.update()


def _show(obj, start, end, last):
    obj.hide_render = True
    obj.keyframe_insert("hide_render", frame=1)
    if start > 1:
        obj.keyframe_insert("hide_render", frame=start - 1)
    obj.hide_render = False
    obj.keyframe_insert("hide_render", frame=start)
    obj.keyframe_insert("hide_render", frame=end)
    obj.hide_render = True
    obj.keyframe_insert("hide_render", frame=min(last, end + 1))
    for fc in _curves(obj):
        if fc.data_path != "hide_render":
            continue
        for kp in fc.keyframe_points:
            kp.interpolation = "CONSTANT"


def _on_camera(obj, x, y, z):
    """Hold the lower third on the lens so the move cannot carry a word off frame."""
    cam = bpy.data.objects.get("Camera")
    obj.parent = cam
    obj.matrix_parent_inverse.identity()
    obj.location = (x, y, z)
    obj.rotation_euler = (0.0, 0.0, 0.0)


def _slide(obj, x0, x1, y, z, start, end, last, delay=0):
    """Ease in from the left and ease back off before the next line."""
    _on_camera(obj, x0, y, z)
    enter = min(last, start + 8 + delay)
    hold = max(enter + 1, end - 12)
    obj.keyframe_insert("location", frame=max(1, start))
    obj.location.x = x1
    obj.keyframe_insert("location", frame=enter)
    obj.keyframe_insert("location", frame=hold)
    obj.location.x = x0
    obj.keyframe_insert("location", frame=min(last, end))
    _ease(obj, "location")


def build(frame_end=1800):
    from .config import CONFIG

    if CONFIG.get("variant") == "lesson":
        from .lesson_cards import build as build_lesson

        return build_lesson(frame_end)
    _clear()
    col = collection("Reef")
    mat = _material()
    cam = bpy.data.objects.get("Camera")
    depth, half_w, half_h = _view(cam) if cam else (0.24, 0.086, 0.049)
    title_size, sub_size, name_size = 0.0064, 0.0046, 0.0032
    title_y = half_h * 0.70
    rule_y = title_y - 0.0055
    sub_y = rule_y - 0.0060
    more_y = sub_y - 0.0056
    name_y = more_y - 0.0052
    z = -depth
    x1 = -half_w * 0.82
    x0 = -half_w * 2.15
    rule = _rule(col)
    _on_camera(rule, x1, rule_y, z)
    for i, (a, b, title, sub, more) in enumerate(STAGES):
        start = max(1, int(a * frame_end) + 1)
        end = max(start + 1, int(b * frame_end))
        rule.scale = (0.04, 1.0, 1.0)
        rule.keyframe_insert("scale", frame=start)
        rule.scale = (1.0, 1.0, 1.0)
        rule.keyframe_insert("scale", frame=min(frame_end, start + 14))
        head = _text("CR_Caption_%d" % i, title, title_size, mat, col)
        note = _text("CR_Note_%d" % i, sub, sub_size, mat, col)
        extra = _text("CR_More_%d" % i, more, sub_size, mat, col)
        _show(head, start, end, frame_end)
        _show(note, start, end, frame_end)
        _show(extra, start, end, frame_end)
        _slide(head, x0, x1, title_y, z, start, end, frame_end, 0)
        _slide(note, x0, x1, sub_y, z, start, end, frame_end, 6)
        _slide(extra, x0, x1, more_y, z, start, end, frame_end, 10)
    _ease(rule, "scale")
    name = _text("CR_Species", "Cymodocea rotundata", name_size, mat, col)
    _slide(name, x0, x1, name_y, z, 1, frame_end, frame_end, 10)
    print("captions", len(STAGES), "across", frame_end, "frames")

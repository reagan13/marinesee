"""Centered subtitles for the 30-second lesson.

One spoken idea at a time, the way an educational short puts captions
on screen: two short lines, centered, on a tight dark plate. The plate
sits in the upper water so it does not cover the roots. Not part of
the phone model.
"""

import bmesh
import bpy

from .geometry import bm_to_mesh
from .lesson import BUD_END, CREEP_END, END, ROOT_END, SHOOT_END
from .util import collection, link, sock, srgb, tag

# Two short spoken lines. The facts stay; the label-and-pointer card does not.
CARDS = (
    (1, BUD_END,
     "Smooth ribbon seagrass",
     "A display, not a scan of a Mati meadow."),
    (BUD_END, CREEP_END,
     "The buried stem grows through the sand.",
     "That is how the patch spreads."),
    (CREEP_END, ROOT_END,
     "Roots grow down at each node",
     "and spread in the sand."),
    (ROOT_END, SHOOT_END,
     "New shoots rise where the stem has passed.",
     "Each leaf is a flat strap with a rounded tip."),
    (SHOOT_END, END,
     "Sheath scars form a closed ring",
     "around the short stem. It can flower and set seed."),
)


def _blend(mat):
    if hasattr(mat, "surface_render_method"):
        methods = [item.identifier for item in mat.bl_rna.properties["surface_render_method"].enum_items]
        if "BLENDED" in methods:
            mat.surface_render_method = "BLENDED"
    elif hasattr(mat, "blend_method"):
        mat.blend_method = "BLEND"
    mat.use_backface_culling = False


def _material(name, rgb, emission):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    _blend(mat)
    nodes = mat.node_tree.nodes
    bsdf = next(node for node in nodes if node.type == "BSDF_PRINCIPLED")
    color = srgb(*rgb)
    sock(bsdf, "Base Color").default_value = color
    sock(bsdf, "Roughness").default_value = 0.6
    try:
        sock(bsdf, "Emission Color").default_value = color
        sock(bsdf, "Emission Strength").default_value = emission
    except KeyError:
        pass
    info = next((node for node in nodes if node.type == "OBJECT_INFO"), None)
    if info is None:
        info = nodes.new("ShaderNodeObjectInfo")
    alpha = info.outputs.get("Alpha")
    target = None
    try:
        target = sock(bsdf, "Alpha")
    except KeyError:
        target = None
    if alpha is not None and target is not None:
        already = any(link.from_socket == alpha and link.to_socket == target for link in mat.node_tree.links)
        if not already:
            mat.node_tree.links.new(alpha, target)
    return mat


def _quad(name, width, height, mat, col):
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    verts = [
        bm.verts.new((0.0, 0.0, 0.0)),
        bm.verts.new((width, 0.0, 0.0)),
        bm.verts.new((width, -height, 0.0)),
        bm.verts.new((0.0, -height, 0.0)),
    ]
    face = bm.faces.new(verts)
    for loop in face.loops:
        loop[uv].uv = (0.5, 0.5)
    mesh = bm_to_mesh(bm, name + "Mesh")
    mesh.materials.append(mat)
    obj = bpy.data.objects.new(name, mesh)
    link(obj, col)
    tag(obj)
    if hasattr(obj, "visible_shadow"):
        obj.visible_shadow = False
    return obj


def _text(name, body, size, mat, col, align="CENTER"):
    data = bpy.data.curves.new(name, "FONT")
    data.body = body
    data.size = size
    data.align_x = align
    aligns = [item.identifier for item in data.bl_rna.properties["align_y"].enum_items]
    if "CENTER" in aligns:
        data.align_y = "CENTER"
    data.resolution_u = 24
    data.extrude = 0.00008
    obj = bpy.data.objects.new(name, data)
    link(obj, col)
    tag(obj)
    obj.data.materials.append(mat)
    if hasattr(obj, "visible_shadow"):
        obj.visible_shadow = False
    return obj


def _curves(obj):
    from .grow import fcurves

    action = obj.animation_data.action if obj.animation_data else None
    if action is None:
        return []
    return fcurves(action)


def _ease_color(obj):
    for fc in _curves(obj):
        if fc.data_path != "color":
            continue
        for kp in fc.keyframe_points:
            kp.interpolation = "BEZIER"
            kp.handle_left_type = "AUTO_CLAMPED"
            kp.handle_right_type = "AUTO_CLAMPED"
        fc.update()


def _constant_hide(obj):
    for fc in _curves(obj):
        if fc.data_path != "hide_render":
            continue
        for kp in fc.keyframe_points:
            kp.interpolation = "CONSTANT"


def _on_camera(obj, x, y, z):
    cam = bpy.data.objects.get("Camera")
    obj.parent = cam
    obj.matrix_parent_inverse.identity()
    obj.location = (x, y, z)
    obj.rotation_euler = (0.0, 0.0, 0.0)


def _fade(obj, start, end, last, fade=12, delay=0):
    """Show one card, fade the words, then take them off before the next line."""
    start = min(max(1, end - fade - 2), start + delay)
    obj.color = (1.0, 1.0, 1.0, 0.0)
    obj.hide_render = True
    obj.keyframe_insert("hide_render", frame=1)
    obj.keyframe_insert("color", index=3, frame=1)
    if start > 1:
        obj.keyframe_insert("hide_render", frame=start - 1)
        obj.keyframe_insert("color", index=3, frame=max(1, start - 1))
    obj.hide_render = False
    obj.keyframe_insert("hide_render", frame=start)
    obj.keyframe_insert("color", index=3, frame=start)
    obj.color = (1.0, 1.0, 1.0, 1.0)
    risen = min(last, start + fade)
    obj.keyframe_insert("color", index=3, frame=risen)
    if end >= last:
        obj.keyframe_insert("color", index=3, frame=last)
    else:
        fallen = max(risen + 1, end - fade)
        obj.keyframe_insert("color", index=3, frame=fallen)
        obj.color = (1.0, 1.0, 1.0, 0.0)
        obj.keyframe_insert("color", index=3, frame=min(last, end))
        obj.hide_render = True
        obj.keyframe_insert("hide_render", frame=min(last, end + 1))
    _ease_color(obj)
    _constant_hide(obj)


def _fit(obj, limit):
    bpy.context.view_layer.update()
    width = obj.dimensions.x
    if width > limit and width > 1e-6:
        obj.data.size *= (limit / width) * 0.98
        bpy.context.view_layer.update()
    return obj.dimensions.x


def _plate(name, width, height, mat, col):
    """A dark plate centered on its origin, so it can sit behind centered type."""
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    hw, hh = width * 0.5, height * 0.5
    verts = [
        bm.verts.new((-hw, hh, 0.0)),
        bm.verts.new((hw, hh, 0.0)),
        bm.verts.new((hw, -hh, 0.0)),
        bm.verts.new((-hw, -hh, 0.0)),
    ]
    face = bm.faces.new(verts)
    for loop in face.loops:
        loop[uv].uv = (0.5, 0.5)
    mesh = bm_to_mesh(bm, name + "Mesh")
    mesh.materials.append(mat)
    obj = bpy.data.objects.new(name, mesh)
    link(obj, col)
    tag(obj)
    if hasattr(obj, "visible_shadow"):
        obj.visible_shadow = False
    return obj


def build(frame_end=END):
    from .captions import _clear

    _clear()
    for obj in list(bpy.data.objects):
        if obj.name.startswith("CR_Card"):
            data = obj.data
            bpy.data.objects.remove(obj, do_unlink=True)
            if data is not None and getattr(data, "users", 1) == 0 and isinstance(data, bpy.types.Mesh):
                bpy.data.meshes.remove(data)
    col = collection("Reef")
    cam = bpy.data.objects.get("Camera")
    depth = 0.30
    if cam and cam.type == "CAMERA":
        half_w = depth * (cam.data.sensor_width * 0.5) / cam.data.lens
    else:
        half_w = 0.108
    half_h = half_w / (16.0 / 9.0)
    z = -depth
    limit = half_w * 1.55
    # White type on a near-black plate. That is the readable TikTok caption,
    # and it still shows when a leaf passes behind it.
    ink = _material("CrLessonText", (1.0, 1.0, 1.0), 1.1)
    plate_mat = _material("CrLessonCard", (0.02, 0.03, 0.04), 0.05)
    y_mid = half_h * 0.62
    line_gap = 0.0062
    # The root close-up fills the center, so that subtitle sits in the open water.
    anchors = (0.0, 0.0, -0.46, 0.0, 0.0)
    for i, (start, end, top, bottom) in enumerate(CARDS):
        first = _text("CR_Caption_%d" % i, top, 0.0046, ink, col)
        second = _text("CR_Note_%d" % i, bottom, 0.0040, ink, col)
        width = max(_fit(first, limit), _fit(second, limit))
        plate = _plate("CR_Card_%d" % i, width + 0.012, 0.016, plate_mat, col)
        x = half_w * anchors[i]
        _on_camera(plate, x, y_mid, z)
        _on_camera(first, x, y_mid + line_gap * 0.5, z + 0.0005)
        _on_camera(second, x, y_mid - line_gap * 0.5, z + 0.0005)
        _fade(plate, start, end, frame_end, fade=8)
        _fade(first, start, end, frame_end, fade=8, delay=3)
        _fade(second, start, end, frame_end, fade=8, delay=6)
    print("lesson subtitles", len(CARDS))

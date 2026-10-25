"""Aquarium cross-section setting for the pitch render.

Frames the meadow inside a dark, top-lit aquarium tank so the cutaway sand bed
(buried rhizome + roots) sits below the patch and the blades stand in the water.
The realistic pitch camera eases in on the patch. The phone file has no camera.
Not exported in the phone .glb.
"""

import math
import shutil

import bmesh
import bpy
from mathutils import Vector

from . import textures
from .geometry import bm_to_mesh
from .util import collection, link, sock, srgb, tag

CENTER = Vector((0.0, -0.01, 0.048))

# Shoot 0 is the first tuft. The empty eases to the centroid of the three tufts
# in layout.node_xy. Frame 1 is close enough that the bud reads. The end stop
# is the fill framing: water above the leaves, cutaway below, tufts in the
# middle. Closer than that, a 50 mm lens puts the side tufts through the caption.
BUD_AIM = Vector((-0.084, 0.012, 0.020))
PATCH_AIM = Vector((-0.007, 0.001, 0.060))
PUSH_START_M = 0.27
PUSH_END_M = 0.50


def _drop(col):
    for obj in list(col.objects):
        mesh = obj.data if obj.type == "MESH" else None
        bpy.data.objects.remove(obj, do_unlink=True)
        if mesh and mesh.users == 0:
            bpy.data.meshes.remove(mesh)


def _tray():
    """Dark slate aquarium floor plinth under the cutaway sand block."""
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    x0, x1 = -0.200, 0.200
    y0, y1 = -0.048, 0.106
    z0, z1 = -0.040, -0.0322
    verts = [
        bm.verts.new((x0, y0, z0)),
        bm.verts.new((x1, y0, z0)),
        bm.verts.new((x1, y1, z0)),
        bm.verts.new((x0, y1, z0)),
        bm.verts.new((x0, y0, z1)),
        bm.verts.new((x1, y0, z1)),
        bm.verts.new((x1, y1, z1)),
        bm.verts.new((x0, y1, z1)),
    ]
    quads = (
        (4, 5, 6, 7),
        (0, 3, 2, 1),
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7),
    )
    for a, b, c, d in quads:
        f = bm.faces.new((verts[a], verts[b], verts[c], verts[d]))
        for loop in f.loops:
            loop[uv].uv = (0.5, 0.1)
    return bm_to_mesh(bm, "ReefTrayMesh")


def _wall():
    """Curved deep-water aquarium backdrop behind the tank."""
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    segs, rows = 48, 16
    radius, z_lo, z_hi = 1.15, -0.14, 0.46
    grid = []
    for j in range(rows + 1):
        z = z_lo + (z_hi - z_lo) * (j / rows)
        row = []
        for k in range(segs):
            a = 2 * math.pi * k / segs
            row.append(bm.verts.new((radius * math.cos(a), radius * math.sin(a), z)))
        grid.append(row)
    for j in range(rows):
        for k in range(segs):
            k2 = (k + 1) % segs
            face = bm.faces.new((grid[j][k2], grid[j][k], grid[j + 1][k], grid[j + 1][k2]))
            v0, v1 = j / rows, (j + 1) / rows
            for loop, (uu, vv) in zip(face.loops, ((k + 1, v0), (k, v0), (k, v1), (k + 1, v1))):
                loop[uv].uv = ((uu % segs) / segs, vv)
    return bm_to_mesh(bm, "ReefWaterMesh")


def _put(name, mesh, mat, col):
    mesh.materials.append(mat)
    obj = bpy.data.objects.new(name, mesh)
    link(obj, col)
    tag(obj)
    obj.hide_render = False
    return obj


def _curves(obj):
    action = obj.animation_data.action if obj.animation_data else None
    if action is None:
        return []
    curves = []
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
                        curves.extend(bag.fcurves)
    if not curves and hasattr(action, "fcurves"):
        curves.extend(action.fcurves)
    return curves


def _bezier(obj):
    for fc in _curves(obj):
        for kp in fc.keyframe_points:
            kp.interpolation = "BEZIER"
            kp.handle_left_type = "AUTO_CLAMPED"
            kp.handle_right_type = "AUTO_CLAMPED"
        fc.update()


def _clear_push(cam):
    for constraint in list(cam.constraints):
        if constraint.type == "TRACK_TO":
            cam.constraints.remove(constraint)
    if cam.animation_data:
        cam.animation_data_clear()
    aim = bpy.data.objects.get("CR_PatchAim")
    if aim is not None:
        bpy.data.objects.remove(aim, do_unlink=True)


def _eye(aim, distance, lift):
    return Vector((aim.x, aim.y - distance, aim.z + lift))


def _push(cam):
    """Track an empty on the patch and ease in. Realistic pitch camera only."""
    from .config import CONFIG

    col = collection("Reef")
    aim = bpy.data.objects.new("CR_PatchAim", None)
    link(aim, col)
    kinds = [item.identifier for item in aim.bl_rna.properties["empty_display_type"].enum_items]
    if "PLAIN_AXES" in kinds:
        aim.empty_display_type = "PLAIN_AXES"
    aim.empty_display_size = 0.012
    tag(aim)
    last = int(CONFIG.get("frame_end", 1800))
    aim.location = BUD_AIM
    aim.keyframe_insert("location", frame=1)
    aim.location = PATCH_AIM
    aim.keyframe_insert("location", frame=last)
    _bezier(aim)

    track = cam.constraints.new("TRACK_TO")
    track.target = aim
    axes = [item.identifier for item in track.bl_rna.properties["track_axis"].enum_items]
    ups = [item.identifier for item in track.bl_rna.properties["up_axis"].enum_items]
    if "TRACK_NEGATIVE_Z" in axes:
        track.track_axis = "TRACK_NEGATIVE_Z"
    if "UP_Y" in ups:
        track.up_axis = "UP_Y"
    cam.location = _eye(BUD_AIM, PUSH_START_M, 0.012)
    cam.keyframe_insert("location", frame=1)
    cam.location = _eye(PATCH_AIM, PUSH_END_M, 0.010)
    cam.keyframe_insert("location", frame=last)
    _bezier(cam)
    bpy.context.scene.frame_end = max(bpy.context.scene.frame_end, last)


def frame_camera():
    cam = bpy.data.objects.get("Camera")
    if cam is None or cam.type != "CAMERA" or cam.get("cr_hand_edited"):
        return
    from .config import CONFIG

    realistic = CONFIG.get("variant") == "realistic"
    lesson = CONFIG.get("variant") == "lesson"
    _clear_push(cam)
    if lesson:
        from .lesson import frame_camera as lesson_frame

        lesson_frame(cam)
    elif realistic:
        _push(cam)
    else:
        eye = Vector((0.012, -0.60, 0.068))
        cam.location = eye
        cam.rotation_euler = (CENTER - eye).to_track_quat("-Z", "Y").to_euler()
    cam.data.lens = 50
    fits = [item.identifier for item in cam.data.bl_rna.properties["sensor_fit"].enum_items]
    if "HORIZONTAL" in fits:
        cam.data.sensor_fit = "HORIZONTAL"
    cam.data.clip_start = 0.01
    cam.data.clip_end = 40
    cam["cr_framed"] = 5 if lesson else (4 if realistic else 3)
    bpy.context.scene.camera = cam


def _light():
    """Top-down aquarium lighting + frontal cutaway fill so both blades and roots pop."""
    from .config import CONFIG

    realistic = CONFIG.get("variant") in ("realistic", "lesson")
    world = bpy.context.scene.world
    if world and world.use_nodes:
        bg = next(node for node in world.node_tree.nodes if node.type == "BACKGROUND")
        if realistic:
            sock(bg, "Color").default_value = srgb(0.078, 0.588, 0.769)
            sock(bg, "Strength").default_value = 0.85
        else:
            sock(bg, "Color").default_value = srgb(0.02, 0.08, 0.11)
            sock(bg, "Strength").default_value = 0.55
    sun = bpy.data.objects.get("Light")
    if sun and sun.type == "LIGHT":
        sun.data.type = "SUN"
        sun.data.energy = 5.0 if realistic else 3.1
        sun.data.color = (0.98, 0.98, 0.90)
        sun.data.angle = 0.55
        sun.rotation_euler = (math.radians(32), math.radians(8), math.radians(-22))
    fill = bpy.data.objects.get("Fill")
    if fill and fill.type == "LIGHT":
        fill.data.type = "SUN"
        fill.data.energy = 1.9
        fill.data.color = (0.72, 0.88, 0.92)
        # Gentle frontal angle to illuminate the front cutaway sediment wall, rhizome, and roots
        fill.rotation_euler = (math.radians(74), math.radians(-10), math.radians(12))


def build_presentation():
    col = collection("Reef")
    _drop(col)
    tray_mat = textures._principled("CrTray", (0.06, 0.09, 0.11), 0.75, 0.12)
    water = textures._attach(
        textures._principled("CrWater", (0.04, 0.16, 0.22), 0.95, 0.02),
        textures.water_image(),
    )
    _put("ReefTray", _tray(), tray_mat, col)
    _put("ReefWater", _wall(), water, col)
    _light()
    frame_camera()
    print("aquarium set ready (not part of the phone export)")

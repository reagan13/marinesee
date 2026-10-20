"""Scene setup and the RESET wipe. Camera and lights are kept; the camera is never animated."""

import math

import bpy
from mathutils import Vector

from .config import CONFIG
from .util import sock, srgb

PLANT_PREFIXES = ("CR_", "Shoot_", "Leaf_", "Root_", "Rhizome", "ReefSand", "Cymodocea")


def setup_scene(cfg=CONFIG):
    scene = bpy.context.scene
    scene.render.fps = cfg["fps"]
    scene.render.fps_base = 1.0
    scene.frame_start = 1
    scene.frame_end = cfg["frame_end"]
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    world = scene.world or bpy.data.worlds.new("World")
    scene.world = world
    world.use_nodes = True
    bg = next(node for node in world.node_tree.nodes if node.type == "BACKGROUND")
    # Neutral studio grey. The #1E8C98 backdrop belongs to the phone viewer, not this file.
    sock(bg, "Color").default_value = srgb(0.40, 0.42, 0.44)
    sock(bg, "Strength").default_value = 0.8

    sun = bpy.data.objects.get("Light")
    if sun and sun.type == "LIGHT" and not sun.get("cr_lit"):
        sun.data.type = "SUN"
        sun.data.energy = 3.4
        sun.data.angle = 0.7
        sun.data.color = (1.0, 0.97, 0.88)
        sun.rotation_euler = (math.radians(58), math.radians(8), math.radians(-36))
        sun["cr_lit"] = 1
    fill = bpy.data.objects.get("Fill")
    if fill is None:
        fill = bpy.data.objects.new("Fill", bpy.data.lights.new("Fill", "SUN"))
        scene.collection.objects.link(fill)
        fill.data.energy = 1.3
        fill.data.color = (0.75, 0.9, 0.95)
        fill.rotation_euler = (math.radians(70), math.radians(-20), math.radians(140))
    cam = bpy.data.objects.get("Camera")
    if cam and cam.type == "CAMERA" and not cam.get("cr_framed"):
        cam.location = (0.02, -0.46, 0.16)
        cam.rotation_euler = (Vector((0.0, 0.0, 0.045)) - cam.location).to_track_quat("-Z", "Y").to_euler()
        cam.data.lens = 50
        cam.data.clip_start = 0.005
        cam.data.clip_end = 20
        cam["cr_framed"] = 1
        scene.camera = cam


def clear_plant():
    for obj in list(bpy.data.objects):
        if obj.type in {"CAMERA", "LIGHT"}:
            continue
        if obj.get("cr_plant") or obj.name == "Cube" or obj.name.startswith(PLANT_PREFIXES):
            bpy.data.objects.remove(obj, do_unlink=True)
    for name in ("Authoring", "Meadow", "Reef"):
        col = bpy.data.collections.get(name)
        if col:
            bpy.data.collections.remove(col)
    action = bpy.data.actions.get("Grow")
    if action:
        bpy.data.actions.remove(action)
    for blocks in (bpy.data.meshes, bpy.data.curves, bpy.data.armatures, bpy.data.materials, bpy.data.images):
        for block in list(blocks):
            if block.users == 0:
                blocks.remove(block)

"""Shallow-reef setting for the pitch.

This is the place around the plant: a sand flat and a water wall. It stays in
the blend and in the rendered clip. It is not exported in the phone file,
because the viewer frames everything in the glb and a room-sized set would
shrink the meadow to a speck. On the phone the water is the viewer's own
backdrop.
"""

import math

import bmesh
import bpy
from mathutils import Vector

from . import textures
from .geometry import bm_to_mesh
from .util import collection, link, sock, srgb, tag

CENTER = Vector((0.0, 0.0, 0.04))


def _drop(col):
    for obj in list(col.objects):
        mesh = obj.data if obj.type == "MESH" else None
        bpy.data.objects.remove(obj, do_unlink=True)
        if mesh and mesh.users == 0:
            bpy.data.meshes.remove(mesh)


def _apron():
    """Broad reef flat. The inner edge covers the mound's cut side."""
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    rings, segs = 14, 56
    grid = []
    for i in range(rings + 1):
        t = i / rings
        radius = 0.14 + t * 1.15
        row = []
        for k in range(segs):
            a = 2 * math.pi * k / segs
            x, y = radius * math.cos(a), radius * math.sin(a)
            z = 0.004 * ((1.0 - t) ** 1.6) + 0.0012 * math.sin(x * 9.0 + y * 4.0)
            row.append(bm.verts.new((x, y, z - 0.006)))
        grid.append(row)
    for i in range(rings):
        for k in range(segs):
            k2 = (k + 1) % segs
            face = bm.faces.new((grid[i][k], grid[i][k2], grid[i + 1][k2], grid[i + 1][k]))
            for loop, (ii, kk) in zip(face.loops, ((i, k), (i, k + 1), (i + 1, k + 1), (i + 1, k))):
                loop[uv].uv = (kk / segs * 4.0, ii / rings * 2.0)
    return bm_to_mesh(bm, "ReefFlatMesh")


def _wall():
    """Cyclorama, wound so the inside faces the patch."""
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    segs, rows = 48, 12
    radius, top = 1.32, 1.6
    grid = []
    for j in range(rows + 1):
        z = -0.02 + top * j / rows
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


def frame_camera():
    cam = bpy.data.objects.get("Camera")
    if cam is None or cam.type != "CAMERA" or cam.get("cr_hand_edited"):
        return
    eye = Vector((0.18, -0.70, 0.22))
    cam.location = eye
    cam.rotation_euler = (CENTER - eye).to_track_quat("-Z", "Y").to_euler()
    cam.data.lens = 48
    cam.data.clip_start = 0.01
    cam.data.clip_end = 40
    cam["cr_framed"] = 2
    bpy.context.scene.camera = cam


def _light():
    """Soft overhead sun and a cool fill. Reads as shallow water, not a studio grey."""
    world = bpy.context.scene.world
    if world and world.use_nodes:
        bg = next(node for node in world.node_tree.nodes if node.type == "BACKGROUND")
        sock(bg, "Color").default_value = srgb(0.03, 0.11, 0.14)
        sock(bg, "Strength").default_value = 0.45
    sun = bpy.data.objects.get("Light")
    if sun and sun.type == "LIGHT":
        sun.data.energy = 2.4
        sun.data.color = (1.0, 0.94, 0.82)
        sun.data.angle = 0.9
        sun.rotation_euler = (math.radians(42), math.radians(6), math.radians(-28))
    fill = bpy.data.objects.get("Fill")
    if fill and fill.type == "LIGHT":
        fill.data.energy = 1.8
        fill.data.color = (0.62, 0.80, 0.82)


def build_presentation():
    col = collection("Reef")
    _drop(col)
    sand = bpy.data.materials.get("CrSand")
    if sand is None:
        sand = textures.ensure_materials(11)["sand"]
    water = textures._attach(
        textures._principled("CrWater", (0.10, 0.28, 0.30), 0.95, 0.04),
        textures.water_image(),
    )
    _put("ReefFlat", _apron(), sand, col)
    _put("ReefWater", _wall(), water, col)
    _light()
    frame_camera()
    print("reef set ready (not part of the phone export)")

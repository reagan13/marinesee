"""Cymodocea rotundata as a solid 3D meadow. Run inside Blender.

Authoring holds the Bezier curves and shoot empties a person edits.
Meadow holds the solid meshes built from them, skinned to CR_Armature.
Growth is the Grow action: bone scale Y only, mesh object scale stays (1, 1, 1).

A normal run keeps every curve point already in the file and calls
rebuild_meshes(). Set RESET = True to replace the plant from scratch.
The modules live in rotundata_build/ next to this file; layout numbers are
in rotundata_build/config.py.
"""

import os
import sys

import bpy

RESET = False
OVERWRITE_ANIM = False
DO_PUBLISH = False

HERE = r"d:\pepot\marinesee\assets\models-3d"
if not os.path.isdir(os.path.join(HERE, "rotundata_build")):
    HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
for _name in [n for n in sys.modules if n == "rotundata_build" or n.startswith("rotundata_build.")]:
    del sys.modules[_name]

from rotundata_build import checks, grow, layout, meshes, scene  # noqa: E402
from rotundata_build import publish as _publish  # noqa: E402
from rotundata_build.config import BLEND_PATH  # noqa: E402


def rebuild_meshes():
    return meshes.rebuild_meshes()


def publish():
    return _publish.publish()


def build(reset=None, overwrite_anim=None, do_publish=None):
    reset = RESET if reset is None else reset
    overwrite_anim = OVERWRITE_ANIM if overwrite_anim is None else overwrite_anim
    do_publish = DO_PUBLISH if do_publish is None else do_publish
    if bpy.context.object and bpy.context.object.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")
    scene.setup_scene()
    if reset or bpy.data.objects.get("CR_Rhizome") is None:
        scene.clear_plant()
        layout.create_plant()
        overwrite_anim = True
    rebuild_meshes()
    arm = bpy.data.objects["CR_Armature"]
    if overwrite_anim or bpy.data.actions.get("Grow") is None:
        grow.animate(arm)
    report = checks.validate()
    bpy.context.scene.frame_set(300)
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_PATH)
    print("saved", BLEND_PATH)
    if do_publish:
        publish()
        bpy.ops.wm.save_as_mainfile(filepath=BLEND_PATH)
    return report


if __name__ == "__main__":
    build()

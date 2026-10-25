"""Realistic variant of the aquarium meadow. Run inside Blender.

Same cutaway, same growth, wetter surfaces. Writes its own blend and glb.
Does not replace the aquarium files or the phone model.
"""

import os
import sys

import bpy

HERE = r"d:\pepot\marinesee\assets\models-3d"
if HERE not in sys.path:
    sys.path.insert(0, HERE)
for _name in [n for n in sys.modules if n == "rotundata_build" or n.startswith("rotundata_build.")]:
    del sys.modules[_name]

import _build_rotundata as builder  # noqa: E402

BLEND = r"d:\pepot\marinesee\assets\models-3d\cymodocea_rotundata_realistic.blend"
GLB = r"d:\pepot\marinesee\assets\models-3d\cymodocea_rotundata_realistic.glb"


def build():
    builder.config.CONFIG["variant"] = "realistic"
    builder.config.CONFIG["frame_end"] = 1800
    builder.config.CONFIG["frame_hold"] = 316
    if bpy.context.object and bpy.context.object.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")
    report = builder.build(reset=True, overwrite_anim=True, do_publish=False, blend_path=BLEND)
    bpy.ops.wm.save_as_mainfile(filepath=BLEND)
    from rotundata_build import render

    stills = render.render_stills(
        r"C:\Users\reaga\AppData\Local\Temp\cr_real_preview",
        frames=(1, 1500),
    )
    print("realistic saved", BLEND)
    print("REAL_STILLS", stills)
    return report


if __name__ == "__main__":
    build()

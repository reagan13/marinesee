"""Lesson meadow. Run inside Blender:

blender.exe --background --python _build_rotundata_lesson.py

CR_LESSON_PHASE=stills builds the blend and writes the check stills.
CR_LESSON_PHASE=final publishes the phone .glb and renders the minute.
The minute is written only to cymodocea_rotundata_lesson.mp4.
"""

import os
import sys

import bpy
from mathutils import Vector

HERE = r"d:\pepot\marinesee\assets\models-3d"
if HERE not in sys.path:
    sys.path.insert(0, HERE)
for _name in [n for n in sys.modules if n == "rotundata_build" or n.startswith("rotundata_build.")]:
    del sys.modules[_name]

import _build_rotundata as builder  # noqa: E402

BLEND = r"d:\pepot\marinesee\assets\models-3d\cymodocea_rotundata_lesson.blend"
STILLS = r"C:\Users\reaga\AppData\Local\Temp\cr_lesson_checks"
PHASE = os.environ.get("CR_LESSON_PHASE", "stills")


def _eevee():
    from rotundata_build.render import _eevee as use

    use(bpy.context.scene)


def _shot(path, frame):
    scene = bpy.context.scene
    scene.frame_set(frame)
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print("STILL", path)
    return path


def _park(cam):
    parked = [(c, c.mute) for c in cam.constraints]
    for c, _mute in parked:
        c.mute = True
    action = None
    if cam.animation_data:
        action = cam.animation_data.action
        cam.animation_data.action = None
    hidden = []
    for obj in bpy.data.objects:
        if obj.name.startswith(("CR_Caption_", "CR_Note_", "CR_Species", "CR_Card")):
            hidden.append((obj, obj.animation_data.action if obj.animation_data else None))
            if obj.animation_data:
                obj.animation_data.action = None
            obj.hide_render = True
    return parked, action, hidden


def _unpark(cam, parked, action, hidden):
    for c, mute in parked:
        c.mute = mute
    if cam.animation_data is not None:
        cam.animation_data.action = action
    for obj, obj_action in hidden:
        if obj.animation_data is not None:
            obj.animation_data.action = obj_action


def _look(cam, eye, aim):
    cam.location = eye
    cam.rotation_euler = (aim - eye).to_track_quat("-Z", "Y").to_euler()


def render_checks():
    import math

    os.makedirs(STILLS, exist_ok=True)
    scene = bpy.context.scene
    _eevee()
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    try:
        scene.eevee.taa_render_samples = 24
    except AttributeError:
        pass
    scene.render.image_settings.media_type = "IMAGE"
    scene.render.image_settings.file_format = "JPEG"
    scene.render.image_settings.quality = 92
    beats = (
        (60, "beat_bud.jpg"),
        (225, "beat_creep.jpg"),
        (420, "beat_root.jpg"),
        (630, "beat_shoots.jpg"),
        (860, "beat_patch.jpg"),
    )
    saved = [_shot(os.path.join(STILLS, name), frame) for frame, name in beats]
    cam = bpy.data.objects["Camera"]
    parked, action, hidden = _park(cam)
    scene.frame_set(860)
    origin = bpy.data.objects["CR_Shoot_00"].matrix_world.translation.copy()
    _look(cam, origin + Vector((-0.07, -0.18, 0.16)), origin + Vector((0.01, 0.0, 0.09)))
    cam.data.lens = 50
    saved.append(_shot(os.path.join(STILLS, "close_shoot.jpg"), 860))
    center = Vector((0.01, 0.015, 0.06))
    elev = math.radians(15.0)
    dist = 0.78
    eye = Vector((center.x, center.y - dist * math.cos(elev), center.z + dist * math.sin(elev)))
    _look(cam, eye, center)
    saved.append(_shot(os.path.join(STILLS, "front_orbit.jpg"), 860))
    _unpark(cam, parked, action, hidden)
    bpy.context.scene.frame_set(860)
    return saved


def recaption(render=True):
    """Swap the on-screen words, then render. The meadow and the camera stay."""
    import os

    builder.config.use_lesson()
    if os.path.isfile(BLEND):
        bpy.ops.wm.open_mainfile(filepath=BLEND)
    from rotundata_build import captions
    from rotundata_build.render import render_lesson, render_stills

    captions.build(900)
    bpy.ops.wm.save_as_mainfile(filepath=BLEND)
    if render:
        render_lesson(900)
        bpy.ops.wm.save_as_mainfile(filepath=BLEND)
    else:
        os.makedirs(STILLS, exist_ok=True)
        render_stills(STILLS, frames=(420,), width=1920, height=1080, samples=16)
    print("RECAPTION_DONE")


def render_frames():
    """Write one JPEG per frame. A later run skips frames already on disk."""
    import os

    out = r"C:\Users\reaga\AppData\Local\Temp\cr_lesson_frames"
    os.makedirs(out, exist_ok=True)
    if os.path.isfile(BLEND):
        bpy.ops.wm.open_mainfile(filepath=BLEND)
    from rotundata_build.render import _eevee, _frame

    scene = bpy.context.scene
    _eevee(scene)
    _frame(scene, 1920, 1080, 48)
    scene.render.image_settings.media_type = "IMAGE"
    scene.render.image_settings.file_format = "JPEG"
    scene.render.image_settings.quality = 90
    scene.render.use_persistent_data = True
    for frame in range(1, 901):
        fp = os.path.join(out, "f%04d.jpg" % frame)
        if os.path.isfile(fp) and os.path.getsize(fp) > 1000:
            continue
        scene.frame_set(frame)
        scene.render.filepath = fp
        bpy.ops.render.render(write_still=True)
        if frame % 30 == 0:
            print("FRAME", frame)
    print("FRAMES_DONE")


def build():
    if PHASE == "captions":
        return recaption(render=False)
    if PHASE == "video":
        return recaption(render=True)
    if PHASE == "frames":
        return render_frames()
    builder.config.use_lesson()
    if bpy.context.object and bpy.context.object.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")
    report = builder.build(reset=True, overwrite_anim=True, do_publish=False, blend_path=BLEND)
    print("LESSON_REPORT", report)
    if PHASE == "final":
        if report["problems"]:
            print("LESSON_SKIP publish and render; checks failed")
            return report
        builder.publish()
        from rotundata_build.render import render_lesson

        render_lesson(900)
        bpy.ops.wm.save_as_mainfile(filepath=BLEND)
    else:
        render_checks()
        bpy.ops.wm.save_as_mainfile(filepath=BLEND)
    return report


if __name__ == "__main__":
    build()

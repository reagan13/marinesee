"""Lesson growth and the explainer camera. Thirty seconds at 30 fps.

One change at a time: a bud, the rhizome tip, one cut root, then shoots
rising in place. The camera stays on the front side and eases back.
It does not orbit. The phone is what the person rotates.
"""

import bpy
from mathutils import Vector

from .util import collection, link, smoothstep, tag

# 30 seconds. Same five beats, half the original minute.
BUD_END = 120
CREEP_END = 330
ROOT_END = 510
SHOOT_END = 750
END = 900
BUD_OPEN = 100
TUCK = Vector((0.0, 0.0, -0.012))


def _names(arm, prefix):
    return sorted(name for name in arm.pose.bones.keys() if name.startswith(prefix))


def _action(arm):
    from .grow import _clock

    _clock["at"] = lambda frame: int(frame)
    old = bpy.data.actions.get("Grow")
    if old:
        bpy.data.actions.remove(old)
    for pb in arm.pose.bones:
        pb.rotation_mode = "XYZ"
        pb.location = (0.0, 0.0, 0.0)
        pb.rotation_euler = (0.0, 0.0, 0.0)
        pb.scale = (1.0, 1.0, 1.0)
    action = bpy.data.actions.new("Grow")
    action.use_fake_user = True
    ad = arm.animation_data_create()
    ad.action = action
    try:
        ad.action_slot = action.slots.new("OBJECT", arm.name)
    except (AttributeError, TypeError, RuntimeError):
        pass
    return action


def _seg_scale(k, frame, windows, tiny):
    if frame <= windows[k]:
        return tiny
    if frame >= windows[k + 1]:
        return 1.0
    u = (frame - windows[k]) / max(1, windows[k + 1] - windows[k])
    return tiny + (1.0 - tiny) * u


def _bud(frame):
    if frame >= BUD_OPEN:
        return 1.0
    return 0.42 + 0.58 * smoothstep((frame - 1) / float(BUD_OPEN - 1))


def _rise(i, frame, tiny, count):
    """Shoot i (i > 0) stays tucked until the stem has passed, then lengthens in place."""
    others = max(1, count - 1)
    room = max(40, SHOOT_END - ROOT_END - 8)
    step = max(4, room // others)
    t0 = ROOT_END + (i - 1) * step
    t1 = min(SHOOT_END - 2, t0 + min(64, room // 2))
    if frame <= t0:
        u = 0.0
    elif frame >= t1:
        u = 1.0
    else:
        u = smoothstep((frame - t0) / float(t1 - t0))
    return tiny + (1.0 - tiny) * u, TUCK * (1.0 - u), t0, t1


def _root_scale(frame, tiny, delay=0):
    start = CREEP_END + delay
    if frame <= start:
        return tiny
    if frame >= ROOT_END:
        return 1.0
    return tiny + (1.0 - tiny) * smoothstep((frame - start) / float(max(1, ROOT_END - start)))


def animate(arm, cfg):
    from .grow import _fold, _key, _local, _polish

    tiny = cfg["min_bone_scale"]
    action = _action(arm)
    bones = arm.data.bones
    rh = _names(arm, "rhizome_")
    nseg = len(rh)
    windows = [BUD_END + round((CREEP_END - BUD_END) * k / max(1, nseg)) for k in range(nseg + 1)]
    chords = [bones[name].tail_local - bones[name].head_local for name in rh]
    rh_frames = sorted(set([1, BUD_END] + windows + [END]))
    for i, name in enumerate(rh):
        pb = arm.pose.bones[name]
        for frame in rh_frames:
            scale = _seg_scale(i, frame, windows, tiny)
            off = Vector()
            for k in range(i):
                off += chords[k] * (_seg_scale(k, frame, windows, tiny) - 1.0)
            _key(pb, frame, scale=scale, loc=_local(bones[name], off))

    shoots = _names(arm, "shoot_")
    lift = cfg["stem_height_m"] * cfg["leaf_base_frac"] + 0.004 / (1.0 - tiny)
    for name in shoots:
        i = int(name.split("_")[1])
        sb = bones[name]
        stem = (sb.tail_local - sb.head_local).normalized()
        if i == 0:
            stem_frames = [1, 40, 70, BUD_OPEN, BUD_END, END]
        else:
            _sy, _tuck, t0, t1 = _rise(i, 1, tiny, len(shoots))
            stem_frames = [1, t0, (t0 + t1) // 2, t1, END]
        for frame in stem_frames:
            if i == 0:
                sv, sloc = _bud(frame), Vector((0.0, 0.0, 0.0))
            else:
                sv, sloc, _t0, _t1 = _rise(i, frame, tiny, len(shoots))
            _key(arm.pose.bones[name], frame, scale=sv, loc=_local(sb, sloc))
        for j, leaf in enumerate(_names(arm, "leaf_%02d_" % i)):
            pb, lb = arm.pose.bones[leaf], bones[leaf]
            folded, opened = _fold(lb, stem), (0.0, 0.0, 0.0)
            for frame in stem_frames:
                if i == 0:
                    sv, sloc = _bud(frame), Vector((0.0, 0.0, 0.0))
                    u_open = 0.0 if frame <= 1 else smoothstep((frame - 1) / float(BUD_OPEN - 1))
                    sy = 0.20 + 0.80 * u_open
                else:
                    sv, sloc, _t0, _t1 = _rise(i, frame, tiny, len(shoots))
                    grown = 0.0 if sv <= tiny + 1e-4 else (sv - tiny) / (1.0 - tiny)
                    u_open = smoothstep(min(1.0, grown * 1.8))
                    sy = sv
                world = sloc + stem * ((sv - 1.0) * lift)
                rot = _mix_tuple(folded, opened, u_open)
                _key(pb, frame, scale=sy, rot=rot, loc=_local(lb, world))
        for r_i, root in enumerate(_names(arm, "root_%02d_" % i)):
            rb = bones[root]
            delay = (i % 5) * 4 + r_i * 6
            marks = (1, CREEP_END, CREEP_END + delay, (CREEP_END + delay + ROOT_END) // 2, ROOT_END, END)
            for frame in sorted(set(marks)):
                _key(arm.pose.bones[root], frame, scale=_root_scale(frame, tiny, delay), loc=_local(rb, Vector()))

    _polish(action, END)
    action.use_frame_range = True
    action.frame_start = 1
    action.frame_end = END
    bpy.context.scene.frame_end = END
    return action


def _mix_tuple(a, b, t):
    from .grow import _mix

    return _mix(a, b, t)


def _nodes():
    empties = sorted(
        (obj for obj in bpy.data.objects if obj.name.startswith("CR_Shoot_")),
        key=lambda obj: obj.name,
    )
    return [obj.matrix_world.translation.copy() for obj in empties]


def _along(nodes, u):
    u = max(0.0, min(1.0, u))
    if len(nodes) < 2:
        return nodes[0].copy()
    lengths = [(b - a).length for a, b in zip(nodes, nodes[1:])]
    total = sum(lengths) or 1.0
    want = u * total
    acc = 0.0
    for (a, b), length in zip(zip(nodes, nodes[1:]), lengths):
        if acc + length >= want - 1e-9:
            t = 0.0 if length < 1e-9 else (want - acc) / length
            return a.lerp(b, t)
        acc += length
    return nodes[-1].copy()


def _look(point, lift=0.055, side=-0.035):
    """Aim above and left of the subject so the upper-left card sits in open water."""
    return point + Vector((side, 0.0, lift))


def _eye(aim, dist, lift):
    return Vector((aim.x, aim.y - dist, aim.z + lift))


def _bezier(obj):
    from .grow import fcurves

    action = obj.animation_data.action if obj.animation_data else None
    if action is None:
        return
    for fc in fcurves(action):
        for kp in fc.keyframe_points:
            kp.interpolation = "BEZIER"
            kp.handle_left_type = "AUTO_CLAMPED"
            kp.handle_right_type = "AUTO_CLAMPED"
        fc.update()


def _key_loc(obj, frame, point):
    obj.location = point
    obj.keyframe_insert("location", frame=frame)


def frame_camera(cam):
    """Track an empty on the active part, then ease back. Lens stays 50 mm. No orbit."""
    nodes = _nodes()
    if not nodes:
        return
    col = collection("Reef")
    previous = bpy.data.objects.get("CR_LessonAim")
    if previous is not None:
        bpy.data.objects.remove(previous, do_unlink=True)
    aim = bpy.data.objects.new("CR_LessonAim", None)
    link(aim, col)
    kinds = [item.identifier for item in aim.bl_rna.properties["empty_display_type"].enum_items]
    if "PLAIN_AXES" in kinds:
        aim.empty_display_type = "PLAIN_AXES"
    aim.empty_display_size = 0.01
    tag(aim)
    if aim.animation_data:
        aim.animation_data_clear()
    if cam.animation_data:
        cam.animation_data_clear()

    bud = _look(nodes[0], 0.07, -0.04)
    root_at = _look(nodes[0] + Vector((0.006, -0.006, -0.020)), 0.012, -0.012)
    shoot_at = _look(nodes[min(5, len(nodes) - 1)], 0.08, -0.03)
    center = sum(nodes, Vector()) / len(nodes)
    wide = _look(center, 0.10, -0.008)

    _key_loc(aim, 1, bud)
    _key_loc(aim, BUD_END, bud)
    for frame in range(BUD_END, CREEP_END + 1, 30):
        u = (frame - BUD_END) / float(CREEP_END - BUD_END)
        _key_loc(aim, frame, _look(_along(nodes, u), 0.016, -0.018))
    _key_loc(aim, CREEP_END, _look(_along(nodes, 1.0), 0.016, -0.018))
    _key_loc(aim, CREEP_END + 20, root_at)
    _key_loc(aim, ROOT_END, root_at)
    _key_loc(aim, ROOT_END + 24, shoot_at)
    _key_loc(aim, SHOOT_END, shoot_at)
    _key_loc(aim, SHOOT_END + 40, wide)
    _key_loc(aim, END, wide)

    track = cam.constraints.new("TRACK_TO")
    track.target = aim
    axes = [item.identifier for item in track.bl_rna.properties["track_axis"].enum_items]
    ups = [item.identifier for item in track.bl_rna.properties["up_axis"].enum_items]
    if "TRACK_NEGATIVE_Z" in axes:
        track.track_axis = "TRACK_NEGATIVE_Z"
    if "UP_Y" in ups:
        track.up_axis = "UP_Y"

    def cam_at(frame, point, dist, lift):
        _key_loc(cam, frame, _eye(point, dist, lift))

    cam_at(1, bud, 0.38, 0.012)
    cam_at(BUD_END, bud, 0.40, 0.012)
    for frame in range(BUD_END, CREEP_END + 1, 30):
        u = (frame - BUD_END) / float(CREEP_END - BUD_END)
        cam_at(frame, _look(_along(nodes, u), 0.016, -0.018), 0.26, 0.008)
    cam_at(CREEP_END, _look(_along(nodes, 1.0), 0.016, -0.018), 0.28, 0.008)
    cam_at(CREEP_END + 20, root_at, 0.16, 0.004)
    cam_at(ROOT_END, root_at, 0.18, 0.004)
    cam_at(ROOT_END + 24, shoot_at, 0.44, 0.018)
    cam_at(SHOOT_END, shoot_at, 0.48, 0.02)
    cam_at(SHOOT_END + 40, wide, 0.86, 0.04)
    cam_at(END, wide, 0.90, 0.045)
    cam.data.lens = 50
    _bezier(aim)
    _bezier(cam)
    print("lesson camera", len(nodes), "nodes, lens", cam.data.lens)

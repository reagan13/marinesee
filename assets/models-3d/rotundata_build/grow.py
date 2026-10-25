"""The Grow action on CR_Armature (frames 1-330 at 30 fps).

Each part lengthens from its own base: bone scale Y only, X and Z stay 1.
Rhizome internodes ride on the growing tip by location keys, so the tube
stays welded. Leaf bases ride up inside the sheath while the stem lengthens,
and blades sway continuously in a gentle aquarium current as they unroll.
"""

import math

import bpy
from mathutils import Euler, Quaternion, Vector

from .config import CONFIG
from .util import smoothstep


_clock = {"at": lambda frame: int(frame)}


def _names(arm, prefix):
    return sorted(name for name in arm.pose.bones.keys() if name.startswith(prefix))


def _key(pb, frame, scale=None, rot=None, loc=None):
    frame = _clock["at"](frame)
    if scale is not None:
        pb.scale = (1.0, float(scale), 1.0)
        pb.keyframe_insert(data_path="scale", frame=frame)
    if rot is not None:
        pb.rotation_euler = Euler(rot, "XYZ")
        pb.keyframe_insert(data_path="rotation_euler", frame=frame)
    if loc is not None:
        pb.location = loc
        pb.keyframe_insert(data_path="location", frame=frame)


def _mix(a, b, t):
    qa = Euler(a, "XYZ").to_quaternion()
    qb = Euler(b, "XYZ").to_quaternion()
    return tuple(qa.slerp(qb, max(0.0, min(1.0, t))).to_euler("XYZ"))


def _fold(bone, stem):
    rest = bone.matrix_local.to_3x3()
    y = rest.col[1].normalized()
    t = (y * 0.28 + stem * 0.72).normalized()
    if t.z < 0.0:
        t.z = abs(t.z)
        t.normalize()
    q = y.rotation_difference(t)
    ang = q.angle
    limit = 0.22 if CONFIG.get("variant") == "realistic" else 0.45
    if ang > limit:
        q = Quaternion(q.axis, limit)
    r = rest.to_quaternion()
    return tuple((r.inverted() @ q @ r).to_euler("XYZ"))


def _local(bone, offset):
    return bone.matrix_local.to_3x3().transposed() @ offset


def _sway(base_eul, i, j, frame, emergence):
    """Gentle travelling water current across the tank so blades breathe as they grow and hold."""
    if emergence <= 0.05:
        return base_eul
    tau = 2.0 * math.pi
    # 66-frame period (~2.2 s) travelling left-to-right across shoots
    phase = tau * ((frame - 1.0) / 66.0) - i * 0.44 - j * 0.32
    amp = (0.014 + 0.052 * emergence) * (0.85 + 0.15 * (j % 3))
    dx = amp * math.sin(phase)
    dz = amp * 0.65 * math.cos(phase * 1.0 + 0.5)
    dy = amp * 0.28 * math.sin(phase + 1.1)
    return (base_eul[0] + dx, base_eul[1] + dy, base_eul[2] + dz)


def fcurves(action):
    out = []
    for layer in action.layers:
        for strip in layer.strips:
            for slot in action.slots:
                bag = strip.channelbag(slot)
                if bag is not None:
                    out.extend(bag.fcurves)
    return out


def _polish(action, hold):
    for fc in fcurves(action):
        linear = '"rhizome_' in fc.data_path
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR" if linear else "BEZIER"
            kp.handle_left_type = "AUTO_CLAMPED"
            kp.handle_right_type = "AUTO_CLAMPED"
            if abs(kp.co[0] - hold) < 0.1:
                kp.interpolation = "CONSTANT"
        fc.update()


def _stem_window(i, count, first):
    """Return (t_start, t_full) for shoot i."""
    if i == 0:
        return 40, 145
    if i <= first:
        t0 = 112 + round((i - 1) * 56 / max(1, first - 1))
        return t0, t0 + 32
    rest = count - 1 - first
    t0 = 188 + round((i - first - 1) * 58 / max(1, rest - 1))
    return t0, min(286, t0 + 34)


def _constant_hide(obj):
    action = obj.animation_data.action if obj.animation_data else None
    if action is None:
        return
    curves = []
    if hasattr(action, "layers"):
        slots = list(getattr(action, "slots", []) or [])
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
    elif hasattr(action, "fcurves"):
        curves.extend(action.fcurves)
    for fc in curves:
        if fc.data_path != "hide_render":
            continue
        for kp in fc.keyframe_points:
            kp.interpolation = "CONSTANT"


def _hide_span(obj, show, hold, end):
    """Keep a waiting shoot out of the picture until its node is ready."""
    if obj.animation_data:
        obj.animation_data_clear()
    obj.hide_render = True
    obj.keyframe_insert("hide_render", frame=1)
    if show > 2:
        obj.keyframe_insert("hide_render", frame=show - 1)
    obj.hide_render = False
    obj.keyframe_insert("hide_render", frame=max(1, show))
    obj.keyframe_insert("hide_render", frame=max(show, hold))
    obj.hide_render = True
    obj.keyframe_insert("hide_render", frame=max(hold + 1, end))
    _constant_hide(obj)


def _conceal_waiting(count, first, hold, end):
    """Dormant shoots were sliding along the growing stem and reading as jumping legs."""
    for i in range(count):
        if i == 0:
            continue
        t0, _t1 = _stem_window(i, count, first)
        show = _clock["at"](t0)
        prefix = "%02d" % i
        for obj in bpy.data.objects:
            name = obj.name
            if name.startswith("Shoot_" + prefix) or name.startswith("Leaf_" + prefix + "_") or name.startswith("Root_" + prefix + "_"):
                _hide_span(obj, show, hold, end)


def animate(arm, cfg=CONFIG):
    if cfg.get("variant") == "lesson":
        from .lesson import animate as animate_lesson

        return animate_lesson(arm, cfg)
    tiny = cfg["min_bone_scale"]
    # Story beats stay on a 330-frame clock. A longer clip stretches those beats
    # across frame_end so the same growth can run as a one-minute time-lapse.
    story_hold, story_end = 316, 330
    real_end = max(story_end, int(cfg["frame_end"]))
    stretch = (real_end - 1) / (story_end - 1)
    _clock["at"] = lambda frame, stretch=stretch: max(1, int(round(1 + (int(frame) - 1) * stretch)))
    hold, end = story_hold, story_end
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
    bones = arm.data.bones

    # Rhizome: internode k lengthens over [w_k, w_k+1]; later internodes ride the tip.
    rh = _names(arm, "rhizome_")
    nseg = len(rh)
    w = [40 + round(80 * k / nseg) for k in range(nseg + 1)]
    start = [0.08] + [tiny] * (nseg - 1)
    chords = [bones[n].tail_local - bones[n].head_local for n in rh]

    def s(k, f):
        if f <= w[k]:
            return start[k]
        if f >= w[k + 1]:
            return 1.0
        return start[k] + (1.0 - start[k]) * (f - w[k]) / (w[k + 1] - w[k])

    frames = sorted(set([1] + w + [hold]))
    for i, name in enumerate(rh):
        pb = arm.pose.bones[name]
        for f in frames + [end]:
            g = 1 if f == end else f
            off = sum((chords[k] * (s(k, g) - 1.0) for k in range(i)), Vector())
            _key(pb, f, scale=s(i, g), loc=_local(bones[name], off))

    shoots = _names(arm, "shoot_")
    count = len(shoots)
    first = max(1, (count - 1) // 2)
    lift = cfg["stem_height_m"] * cfg["leaf_base_frac"] + 0.004 / (1.0 - tiny)
    # Deep enough that a waiting shoot does not show as a green splinter on the sand.
    tuck_vec = Vector((0.0, 0.006, -0.016))
    sway_frames = sorted(set(list(range(1, 305, 12)) + [1, 40, 120, 200, 300, hold]))

    for name in shoots:
        i = int(name.split("_")[1])
        sb = bones[name]
        stem = (sb.tail_local - sb.head_local).normalized()
        t0, t1 = _stem_window(i, count, first)

        def stem_state(f):
            if i == 0:
                u = smoothstep((f - t0) / max(1, t1 - t0))
                return 0.48 + 0.52 * u, Vector((0.0, 0.0, 0.0))
            if f <= t0:
                return tiny, tuck_vec
            u = smoothstep((f - t0) / max(1, t1 - t0))
            return tiny + (1.0 - tiny) * u, tuck_vec * (1.0 - u)

        stem_frames = sorted(set([1, max(1, t0 - 4), t0, (t0 + t1) // 2, t1, hold]))
        for f in stem_frames + [end]:
            g = 1 if f == end else f
            sv, sloc = stem_state(g)
            _key(arm.pose.bones[name], f, scale=sv, loc=_local(sb, sloc))

        for j, leaf in enumerate(_names(arm, "leaf_%02d_" % i)):
            pb, lb = arm.pose.bones[leaf], bones[leaf]
            folded, opened = _fold(lb, stem), (0.0, 0.0, 0.0)
            b_start = 40 if i == 0 else t0 + 6 + j * 3
            b_done = (195 + j * 8) if i == 0 else min(296, t0 + 56 + j * 6)

            def leaf_pose(f):
                sv, sloc = stem_state(f)
                loc = sloc + stem * ((sv - 1.0) * lift)
                if i == 0:
                    if f <= 40:
                        u_len = (f - 1.0) / 39.0 * 0.04
                        sy = 0.30 + 0.70 * u_len
                        u_open = u_len
                    else:
                        u_len = smoothstep((f - 40.0) / max(1.0, b_done - 40.0))
                        sy = 0.32 + 0.68 * u_len
                        u_open = smoothstep((f - 40.0) / max(1.0, b_done - 36.0))
                    emerge = 0.35 + 0.65 * u_len
                else:
                    if f <= b_start:
                        sy = tiny
                        u_open = 0.0
                        emerge = 0.0
                    else:
                        u_len = smoothstep((f - b_start) / max(1.0, b_done - b_start))
                        sy = tiny + (1.0 - tiny) * u_len
                        u_open = smoothstep((f - b_start) / max(1.0, b_done - b_start))
                        emerge = u_len
                base_rot = _mix(folded, opened, u_open)
                rot = _sway(base_rot, i, j, f, emerge)
                return sy, rot, _local(lb, loc)

            l_frames = sorted(set(sway_frames + [max(1, t0 - 4), t0, b_start, (b_start + b_done) // 2, b_done]))
            for f in l_frames + [end]:
                g = 1 if f == end else f
                sy, rot, loc = leaf_pose(g)
                _key(pb, f, scale=sy, rot=rot, loc=loc)

        r0 = 46 if i == 0 else w[min(i, nseg)]
        r1 = min(300, r0 + 78)
        # Stay buried until the node exists, then lengthen downward.
        # A short shove toward the camera reads as the root jumping out of the sand.
        root_tuck = Vector((0.0, 0.0022, 0.0))
        for r_idx, root in enumerate(_names(arm, "root_%02d_" % i)):
            rb = bones[root]
            rs0 = r0 + r_idx * 6
            rs1 = min(304, r1 + r_idx * 8)
            r_frames = sorted(set([1, rs0, (rs0 + rs1) // 2, rs1, hold]))
            for f in r_frames + [end]:
                g = 1 if f == end else f
                if g <= rs0:
                    sy = tiny
                    rloc = Vector((0.0, 0.0, 0.0)) if i == 0 else root_tuck
                else:
                    u = smoothstep((g - rs0) / max(1, rs1 - rs0))
                    sy = tiny + (1.0 - tiny) * u
                    rloc = Vector((0.0, 0.0, 0.0)) if i == 0 else root_tuck * (1.0 - u)
                _key(arm.pose.bones[root], f, scale=sy, loc=_local(rb, rloc))

    _conceal_waiting(count, first, int(_clock["at"](hold)), int(_clock["at"](end)))
    _polish(action, _clock["at"](hold))
    action.use_frame_range = True
    action.frame_start = 1
    action.frame_end = int(_clock["at"](end))
    bpy.context.scene.frame_end = int(action.frame_end)
    return action

"""The Grow action on CR_Armature (frames 1-330 at 30 fps).

Each part lengthens from its own base: bone scale Y only, X and Z stay 1.
Rhizome internodes ride on the growing tip by location keys, so the tube
stays welded. Leaf bases ride up inside the sheath while the stem lengthens.
"""

import bpy
from mathutils import Euler, Vector

from .config import CONFIG


def _names(arm, prefix):
    return sorted(name for name in arm.pose.bones.keys() if name.startswith(prefix))


def _key(pb, frame, scale=None, rot=None, loc=None):
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
    return tuple(qa.slerp(qb, t).to_euler("XYZ"))


def _fold(bone, stem):
    rest = bone.matrix_local.to_3x3()
    y = rest.col[1].normalized()
    q = y.rotation_difference((y * 0.25 + stem * 0.75).normalized())
    r = rest.to_quaternion()
    return tuple((r.inverted() @ q @ r).to_euler("XYZ"))


def _local(bone, offset):
    return bone.matrix_local.to_3x3().transposed() @ offset


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


def _stem_schedule(i, count, tiny, first):
    if i == 0:
        return [(1, 0.48), (40, 0.48), (150, 1.0)], 40
    if i <= first:
        t0 = 120 + round((i - 1) * 56 / max(1, first - 1))
        return [(1, tiny), (t0, tiny), (t0 + 30, 1.0)], t0
    rest = count - 1 - first
    t0 = 196 + round((i - first - 1) * 60 / max(1, rest - 1))
    return [(1, tiny), (t0, tiny), (min(292, t0 + 34), 1.0)], t0


def animate(arm, cfg=CONFIG):
    tiny, hold, end = cfg["min_bone_scale"], cfg["frame_hold"], cfg["frame_end"]
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
    for name in shoots:
        i = int(name.split("_")[1])
        sb = bones[name]
        stem = (sb.tail_local - sb.head_local).normalized()
        sched, t0 = _stem_schedule(i, count, tiny, first)
        sched = sched + [(hold, 1.0)]
        for f, v in sched + [(end, sched[0][1])]:
            _key(arm.pose.bones[name], f, scale=v)
        for j, leaf in enumerate(_names(arm, "leaf_%02d_" % i)):
            pb, lb = arm.pose.bones[leaf], bones[leaf]
            for f, v in sched + [(end, sched[0][1])]:
                _key(pb, f, loc=_local(lb, stem * ((v - 1.0) * lift)))
            folded, opened = _fold(lb, stem), (0.0, 0.0, 0.0)
            if i == 0:
                done = 200 + j * 6
                scale = [(1, 0.30), (40, 0.32), (done, 1.0)]
                rot = [(1, folded), (40, folded), (150, _mix(folded, opened, 0.45)), (done, opened)]
            else:
                b = t0 + 8
                done = min(300, t0 + 60 + j * 5)
                scale = [(1, tiny), (b, tiny), (done, 1.0)]
                rot = [(1, folded), (b, folded), ((b + done) // 2, _mix(folded, opened, 0.4)), (done, opened)]
            for f, v in scale + [(hold, 1.0), (end, scale[0][1])]:
                _key(pb, f, scale=v)
            for f, r in rot + [(hold, opened), (end, folded)]:
                _key(pb, f, rot=r)
        r0 = 48 if i == 0 else w[min(i, nseg)]
        r1 = min(296, r0 + (42 if i == 0 else 26))
        for root in _names(arm, "root_%02d_" % i):
            for f, v in ((1, tiny), (r0, tiny), (r1, 1.0), (hold, 1.0), (end, tiny)):
                _key(arm.pose.bones[root], f, scale=v)

    _polish(action, hold)
    action.use_frame_range = True
    action.frame_start = 1
    action.frame_end = end
    return action

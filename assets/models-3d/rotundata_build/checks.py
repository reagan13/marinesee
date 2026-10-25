"""Done-when checks that can be read from the file (the looks are checked by eye)."""

import bpy

from .config import CONFIG

SAMPLE_FRAMES = (1, 20, 40, 60, 80, 100, 120, 150, 180, 200, 230, 260, 300, 316, 330)


def _lesson_shape(cfg):
    """Internodes, leaf counts, and root counts for the lesson meadow."""
    from .util import arc_table, dense_points

    problems = []
    controls = bpy.data.objects.get("CR_Controls")
    width = float(controls["leaf_width_m"]) if controls else 0.0
    if abs(width - 0.004) > 1e-6:
        problems.append("leaf width %.4f is not 4 mm" % width)
    rh = bpy.data.objects.get("CR_Rhizome")
    if rh is None:
        return ["missing rhizome"]
    dense = dense_points(rh)
    cum = arc_table(dense)
    count = int(rh.get("cr_nodes", 0))
    per = 48
    spans = []
    for k in range(count - 1):
        a = min(len(cum) - 1, 2 * k * per)
        b = min(len(cum) - 1, 2 * (k + 1) * per)
        spans.append(cum[b] - cum[a])
    for i, span in enumerate(spans):
        if span < 0.010 - 1e-4 or span > 0.045 + 1e-4:
            problems.append("internode %d is %.2f cm" % (i, span * 100))
    shoots = {}
    roots = {}
    for obj in bpy.data.objects:
        if obj.name.startswith("CR_Leaf_"):
            key = obj.name.split("_")[2]
            shoots[key] = shoots.get(key, 0) + 1
        elif obj.name.startswith("CR_Root_"):
            key = obj.name.split("_")[2]
            roots[key] = roots.get(key, 0) + 1
    for key, n in sorted(shoots.items()):
        if n < 2 or n > 7:
            problems.append("shoot %s has %d leaves" % (key, n))
    for key, n in sorted(roots.items()):
        if n < 1 or n > 3:
            problems.append("shoot %s has %d roots" % (key, n))
    if len(shoots) < 2:
        problems.append("need more than one shoot")
    ys = []
    for obj in bpy.data.objects:
        if obj.name.startswith("CR_Shoot_"):
            ys.append(obj.matrix_world.translation.y)
    if ys and max(ys) - min(ys) < 0.04:
        problems.append("shoots span only %.1f cm in depth" % ((max(ys) - min(ys)) * 100))
    print("lesson spans_cm", [round(s * 100, 2) for s in spans])
    return problems


def validate(cfg=CONFIG):
    scene = bpy.context.scene
    arm = bpy.data.objects["CR_Armature"]
    meadow = bpy.data.collections["Meadow"]
    tiny = cfg["min_bone_scale"]
    problems = []
    tris = 0
    leaves = 0
    for obj in meadow.objects:
        if obj.type != "MESH":
            continue
        obj.data.calc_loop_triangles()
        tris += len(obj.data.loop_triangles)
        leaves += obj.name.startswith("Leaf_")
        if any(abs(v - 1.0) > 1e-6 for v in obj.scale):
            problems.append("object scale %s %s" % (obj.name, tuple(obj.scale)))
    if tris > 40000:
        problems.append("triangles %d > 40000" % tris)

    samples = list(SAMPLE_FRAMES)
    if cfg["frame_end"] not in samples:
        samples.append(cfg["frame_end"])
    poses = {}
    for f in samples:
        scene.frame_set(f)
        for pb in arm.pose.bones:
            if pb.name == "base":
                continue
            sx, sy, sz = pb.scale
            if sy < tiny - 1e-4 or abs(sx - 1) > 1e-4 or abs(sz - 1) > 1e-4:
                problems.append("bone %s frame %d scale %s" % (pb.name, f, tuple(pb.scale)))
            if f in (1, cfg["frame_end"]):
                poses.setdefault(pb.name, []).append(pb.matrix_basis.copy())
    # The lesson minute ends on the patch. The phone restarts the clip from the bud.
    if cfg.get("variant") != "lesson":
        for name, (a, b) in poses.items():
            if any(abs(a[r][c] - b[r][c]) > 1e-4 for r in range(4) for c in range(4)):
                problems.append("loop mismatch %s" % name)
    if cfg.get("variant") == "lesson":
        problems.extend(_lesson_shape(cfg))

    curves = sum(1 for o in bpy.data.objects if o.type == "CURVE" and o.name.startswith("CR_"))
    if "Grow" not in bpy.data.actions:
        problems.append("missing Grow")
    report = {"triangles": tris, "leaves": leaves, "authoring_curves": curves, "problems": problems[:20]}
    print("validate", report)
    return report

"""Done-when checks that can be read from the file (the looks are checked by eye)."""

import bpy

from .config import CONFIG

SAMPLE_FRAMES = (1, 20, 40, 60, 80, 100, 120, 150, 180, 200, 230, 260, 300, 316, 330)


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

    poses = {}
    for f in SAMPLE_FRAMES:
        scene.frame_set(f)
        for pb in arm.pose.bones:
            if pb.name == "base":
                continue
            sx, sy, sz = pb.scale
            if sy < tiny - 1e-4 or abs(sx - 1) > 1e-4 or abs(sz - 1) > 1e-4:
                problems.append("bone %s frame %d scale %s" % (pb.name, f, tuple(pb.scale)))
            if f in (1, cfg["frame_end"]):
                poses.setdefault(pb.name, []).append(pb.matrix_basis.copy())
    for name, (a, b) in poses.items():
        if any(abs(a[r][c] - b[r][c]) > 1e-4 for r in range(4) for c in range(4)):
            problems.append("loop mismatch %s" % name)

    curves = sum(1 for o in bpy.data.objects if o.type == "CURVE" and o.name.startswith("CR_"))
    if "Grow" not in bpy.data.actions:
        problems.append("missing Grow")
    report = {"triangles": tris, "leaves": leaves, "authoring_curves": curves, "problems": problems[:20]}
    print("validate", report)
    return report

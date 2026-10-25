"""rebuild_meshes(): refresh the solid Meadow meshes from the Authoring curves."""

import bpy
from mathutils import Vector

from . import geometry, rig, sand, shoot, textures
from .config import CONFIG
from .util import arc_table, collection, dense_points, link, tag


def _controls():
    c = bpy.data.objects.get("CR_Controls")
    get = (lambda k: c.get(k, CONFIG[k])) if c else (lambda k: CONFIG[k])
    return float(get("leaf_width_m")), float(get("leaf_thickness_m")), int(get("vein_count"))


def _put(name, src, make, mats, groups_of, meadow, arm):
    obj = bpy.data.objects.get(name)
    if (src is not None and src.get("cr_hand_edited")) or (obj is not None and obj.get("cr_hand_edited")):
        return obj, False
    mesh, groups = groups_of(make())
    for mat in mats:
        mesh.materials.append(mat)
    if obj is None:
        obj = bpy.data.objects.new(name, mesh)
        link(obj, meadow)
        tag(obj)
    else:
        old = obj.data
        obj.data = mesh
        if old.users == 0:
            bpy.data.meshes.remove(old)
    obj.vertex_groups.clear()
    for group, ids in groups.items():
        obj.vertex_groups.new(name=group).add(ids, 1.0, "REPLACE")
    mod = next((m for m in obj.modifiers if m.type == "ARMATURE"), None)
    if groups and mod is None:
        mod = obj.modifiers.new("Armature", "ARMATURE")
    if mod:
        mod.object = arm
        mod.use_vertex_groups = True
    obj.parent = arm
    obj.matrix_parent_inverse.identity()
    obj.location = (0.0, 0.0, 0.0)
    obj.rotation_euler = (0.0, 0.0, 0.0)
    obj.scale = (1.0, 1.0, 1.0)
    return obj, True


def _whole(bone):
    def wrap(mesh):
        return mesh, {bone: list(range(len(mesh.vertices)))}

    return wrap


def rebuild_meshes(cfg=CONFIG):
    width, thickness, veins = _controls()
    mats = textures.ensure_materials(veins)
    meadow = collection("Meadow")
    arm = bpy.data.objects["CR_Armature"]
    rig.sync_bones(arm, rig.layout_bones(cfg))
    built = 0

    rh = bpy.data.objects["CR_Rhizome"]
    dense = dense_points(rh)
    cum = arc_table(dense)
    nodes = rig.rhizome_nodes(rh)
    per = 48
    node_ds = [cum[2 * k * per] for k in range(len(nodes))]
    _o, ok = _put("Rhizome", rh, lambda: geometry.rhizome_mesh("RhizomeMesh", dense, node_ds, cfg["rhizome_radius_m"], cfg["rhizome_oval"]),
                  [mats["rhizome"]], lambda r: r, meadow, arm)
    built += ok

    path = [(p.x, p.y) for p in dense]
    _o, ok = _put("ReefSand", None, lambda: sand.build_sand("ReefSandMesh", path, cfg["sand_bottom_z"]),
                  [mats["sand"]], lambda m: (m, {}), meadow, arm)
    built += ok

    sides = {}
    for emp in rig.objects_with_prefix("CR_Shoot_"):
        i = emp.name[len("CR_Shoot_"):]
        origin, stem, side, _fwd = rig.shoot_axes(emp)
        sides[i] = side
        stem_sides, arc = (8, 8) if cfg.get("variant") == "lesson" else (10, 12)
        _o, ok = _put("Shoot_" + i, emp, lambda s=stem_sides, a=arc: shoot.shoot_mesh("ShootMesh_" + i, origin, stem, side, cfg, s, a),
                      [mats["stem"], mats["sheath"], mats["scar"]], _whole("shoot_" + i), meadow, arm)
        built += ok

    for curve in rig.objects_with_prefix("CR_Leaf_"):
        key = curve.name[len("CR_Leaf_"):]
        side = sides.get(key.split("_")[0]) or Vector((1.0, 0.0, 0.0))
        w = float(curve.get("cr_width_m", width))
        t = float(curve.get("cr_thickness_m", thickness))
        pts = dense_points(curve)
        mat = mats["young"] if curve.get("cr_young") else mats["leaf"]
        rings = 4 if cfg.get("variant") == "lesson" else 8
        _o, ok = _put("Leaf_" + key, curve,
                      lambda n=rings: geometry.leaf_mesh("LeafMesh_" + key, pts, w, t, veins, side, float(curve.get("cr_twist", 0.0)),
                                                 cfg["vein_groove_m"], cfg["leaf_crown_m"], body_rings=n),
                      [mat], _whole("leaf_" + key), meadow, arm)
        built += ok

    for curve in rig.objects_with_prefix("CR_Root_"):
        key = curve.name[len("CR_Root_"):]
        pts = dense_points(curve, 16)
        root_rings = 4 if cfg.get("variant") == "lesson" else 6
        _o, ok = _put("Root_" + key, curve, lambda n=root_rings: geometry.root_mesh("RootMesh_" + key, pts, cfg["root_radius_m"], rings=n),
                      [mats["root"]], _whole("root_" + key), meadow, arm)
        built += ok
    print("rebuild_meshes: refreshed", built, "meshes")
    return built

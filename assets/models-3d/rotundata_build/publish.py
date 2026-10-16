"""publish(): write the phone .glb from Meadow and CR_Armature only. Curves stay in the blend."""

import bpy

from .config import GLB_PATH


def publish(path=GLB_PATH):
    arm = bpy.data.objects["CR_Armature"]
    meadow = bpy.data.collections["Meadow"]
    for obj in bpy.context.view_layer.objects:
        obj.select_set(False)
    arm.select_set(True)
    for obj in meadow.objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = arm
    op = bpy.ops.export_scene.gltf
    names = {p.identifier for p in op.get_rna_type().properties}
    wanted = {
        "export_format": "GLB",
        "use_selection": True,
        "export_animations": True,
        "export_skins": True,
        "export_morph": False,
        "export_lights": False,
        "export_cameras": False,
        "export_apply": False,
        "export_texcoords": True,
        "export_normals": True,
    }
    kwargs = {k: v for k, v in wanted.items() if k in names}
    op(filepath=path, **kwargs)
    curves = sum(1 for o in bpy.data.objects if o.type == "CURVE" and o.name.startswith("CR_"))
    print("exported", path, "authoring curves still in file:", curves)
    return curves

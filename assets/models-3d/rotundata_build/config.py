"""Display layout for the Cymodocea rotundata meadow.

These numbers are display choices for a phone viewer. They are not field
measurements from Mati. Real leaves are about 2-4 mm wide; the model uses
7 mm so the rounded tip stays readable on a phone.
"""

CONFIG = {
    "shoot_count": 12,
    "leaf_counts": (3, 4, 2, 3, 4, 3, 4, 2, 3, 4, 2, 2),
    "leaf_width_m": 0.007,
    "leaf_thickness_m": 0.00035,
    "leaf_length_m": (0.075, 0.150),
    "vein_count": 11,
    "vein_groove_m": 0.00003,
    "leaf_crown_m": 0.00012,
    "stem_height_m": 0.020,
    "stem_radius_m": (0.0016, 0.0014),
    "scar_fracs": (0.12, 0.22, 0.32, 0.42),
    "scar_proud_m": 0.00012,
    "scar_half_m": 0.00025,
    "sheath_wall_m": 0.00028,
    "leaf_base_frac": 0.72,
    "rhizome_radius_m": 0.0022,
    "rhizome_oval": 0.82,
    "rhizome_span_m": 0.32,
    "rhizome_sink_m": 0.006,
    "root_radius_m": 0.00070,
    "sand_bottom_z": -0.032,
    "min_bone_scale": 0.02,
    "fps": 30,
    "frame_hold": 316,
    "frame_end": 330,
    "seed": 11,
}

BLEND_PATH = r"d:\pepot\marinesee\assets\models-3d\cymodocea_rotundata.blend"
GLB_PATH = r"d:\pepot\marinesee\app\assets\models-3d\cymodocea_rotundata.glb"

HOW_TO = """Cymodocea rotundata - how to edit

Meadow holds the solid plant. That is the model that goes to the phone.
Authoring holds the curves and shoot empties that shape it.

1. Unhide Authoring, edit a curve, run rebuild_meshes().
   (Run _build_rotundata.py with RESET = False; that calls rebuild_meshes().)
2. Width, thickness, and vein count are the controls on that curve or on
   CR_Controls: leaf_width_m, leaf_thickness_m, vein_count. Add cr_width_m
   or cr_thickness_m on one leaf curve to override only that leaf.
   Set cr_hand_edited = True on a curve or mesh to keep it as it is.
3. To change the open fan, pose the leaf bone at frame 300 and key the
   rotation. Leave the action in place.
4. Set RESET = True only when the plant should be replaced from scratch.
5. publish() writes the .glb and does not delete the curves.

Shoots stand on the CR_Shoot_NN empties: local Z is the stem, local X is the
fan side. Move an empty together with its rhizome node.
Growth is the Grow action on CR_Armature. Mesh scale stays (1, 1, 1).
After moving a curve a long way, set OVERWRITE_ANIM = True once so the
growth keys are made again for the new rest pose (this also resets fan keys).
"""


def leaf_count(i):
    counts = CONFIG["leaf_counts"]
    return counts[i % len(counts)]


# Lesson explainer and the phone meadow it publishes.
# Blade 2–4 mm wide: Seagrass-Watch. Length 7–15 cm, 9–15 veins, sheath
# 1.5–5.5 cm, erect stem up to about 6 cm, internodes 1–4.5 cm, 2–7
# leaves, 1–3 roots: El Shaffai (2011), Field Guide to Seagrasses of the
# Red Sea, and the Flora of Tropical East Africa as given by Kew, in
# line with the Great Barrier Reef identification guide.
# Width is 4 mm, the top of that range, so a close view still shows a
# narrow strap. The tip stays rounded and smooth: no teeth, no notch.
# How far the rhizome wanders behind the front cut is a display choice,
# not a Mati measurement.
LESSON = {
    "variant": "lesson",
    "shoot_count": 9,
    "leaf_counts": (3, 2, 2, 2, 2, 2, 2, 2),
    "root_counts": (3, 2, 3, 2, 2, 3),
    "leaf_width_m": 0.004,
    "leaf_thickness_m": 0.00022,
    "leaf_length_m": (0.07, 0.15),
    "vein_count": 11,
    "vein_groove_m": 0.000012,
    "leaf_crown_m": 0.00008,
    "stem_height_m": 0.048,
    "stem_radius_m": (0.0015, 0.0013),
    "scar_fracs": (0.08, 0.16, 0.24),
    "scar_proud_m": 0.00040,
    "scar_half_m": 0.00015,
    "sheath_wall_m": 0.00022,
    "leaf_base_frac": 0.82,
    "rhizome_radius_m": 0.0024,
    "rhizome_oval": 0.82,
    "rhizome_span_m": 0.26,
    "rhizome_sink_m": 0.0008,
    "root_radius_m": 0.0009,
    "sand_bottom_z": -0.032,
    "min_bone_scale": 0.02,
    "fps": 30,
    "frame_hold": 900,
    "frame_end": 900,
    "seed": 21,
}


def use_lesson():
    """Point CONFIG at the lesson meadow. Call once, before build()."""
    CONFIG.update(LESSON)

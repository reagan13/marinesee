# Prompt — solid 3D model of *Cymodocea rotundata*

Hand this file to the agent that will build the model. Implement it in Blender. Do not stop at another written plan.

The owner asked for a meadow that is actually 3D and close to a real smooth ribbon seagrass, and that a person can still edit by hand. `AGENTS.md` says this repo only integrates 3D. Ignore that for this task. This build was requested on purpose.

One species only. Out of scope: the other eight species, flowers, animals, a photo scan, a map, a status badge, and any change to the Flutter viewer.

## The model is solid geometry

The finished plant is a mesh you can orbit. Thickness is part of the shape, not a lighting trick.

- A leaf is a solid strap, about 7 mm across and about 0.35 mm thick, with a rounded end. From the side the edge is thin. From the front the face is flat and wide. A plane, a billboard, a photo, or a card that turns to face the camera is not a leaf.
- The rhizome is a solid horizontal stem, smooth and slightly oval, partly buried in the sand. The sand is a solid mound with thickness, not a flat sheet.
- Roots are solid, thin, and go down into the sand.
- The sheath is a split wrap around the bases of the leaves. Scar rings are thin closed bands on the short stem, only a fraction of a millimetre proud of the surface. They read as lines. They are not beads and they are not separate donuts.
- Before calling it done, orbit the plant from the side and from above. If either view looks like a drawing, a flat texture, or a row of tubes, it is not done.

## Close to the real plant

Match smooth ribbon seagrass. Do not invent a showier plant, and do not add facts the sources below do not state.

Sources: the `cymodocea_rotundata` record in `app/assets/data/species.json`, `docs/11-species.md`, and Seagrass-Watch (code CR), https://www.seagrasswatch.org/idseagrass/

- Flat strap leaves, rounded smooth tip, no serrations. About 9–15 faint longitudinal veins on the face of the leaf.
- Real leaves are about 2–4 mm wide. This model uses 6–8 mm so the rounded tip stays readable on a phone. Length stays about 7–15 cm, and the leaves on one shoot are not all the same length.
- The sheath is well developed. Leaf-sheath scars form a continuous ring around the short erect stem.
- The rhizome is smooth and horizontal, in shallow reef sand. New shoots come off it. Fine roots leave the nodes.
- The clip is teaching this: the patch spreads when the buried rhizome grows and sends up new shoots.
- *Cymodocea serrulata* is the wrong species. It is wider and the tip is serrated. A saw-tooth tip fails this model.

Color, from the same brief: seagrass green, younger leaves lighter, the base of a leaf paler, rhizome pale, roots cream, sand warm and pale. No metal, no neon, no glass.

These layout numbers are display choices, not measurements from Mati. Keep them in a `CONFIG` block at the top of the script and do not describe them as field data.

- About 12–16 shoots on one rhizome that snakes. Not one shoot, and not a straight row of identical poles.
- 2–5 leaves on a shoot, in a flat fan, gently bowed, some of them crossing. Younger leaves are shorter and lighter.
- An irregular low mound of reef sand, with small ripples and a groove where the rhizome sits. No square plate and no perfect oval cookie.

Veins are faint darker lines running from the sheath to the tip, on the flat face. A person who zooms in can see them. They are not black ribs, and they do not wrap around the edge the way stripes wrap a hose. Put those lines in the color texture as well as in the mesh, so they are still there after export.

## Replace the current builder

`assets/models-3d/_build_rotundata.py` is the old meadow. Replace it. Do not keep these constructions:

- Leaves are closed elliptical tubes. The vein image is mapped with `u = 0.5 + 0.5 * cos(angle)`, so the stripes go around the tube instead of along a flat face.
- The rhizome is capped cylinders butted end to end. The sheath is an open cone. Each “ring” is a short tube fatter than the stem, so it reads as a bead.
- Growth scales whole objects from `(0.001, 0.001, 0.001)`. Parts swell out of nothing. A leaf has to lengthen from the sheath and keep its width.
- `wipe()` deletes the file on every run, and every leaf is a frozen mesh. A person cannot move a curve and rebuild.

## What a person can still edit

Keep two layers in the `.blend`.

- `Authoring` holds the Bezier curves: `CR_Rhizome`, `CR_Leaf_00_0`, `CR_Root_00_0`, and the rest. This is what a person grabs. A normal run does not move curve points that already exist, and it does not delete the camera, the lights, the armature, or the `Grow` action.
- `Meadow` holds the solid meshes built from those curves. `rebuild_meshes()` refreshes the meshes from the curves. A curve or a mesh with `cr_hand_edited = True` is left alone.

`CR_Controls` is an empty. Put `leaf_width_m` (0.007), `vein_count` (11), and `shoot_count` on it. Read those when a missing piece is created. Do not drive them every frame, or a person’s edit will be overwritten.

`CR_Armature` carries the only action, `Grow`. Scaling a bone on its long axis (Y) lengthens that part from its base. Scale on the other two axes stays 1, so a strap does not get fatter as it grows. Every mesh object stays at scale `(1, 1, 1)`. The smallest bone scale is 0.02, never 0.

Write a text datablock named `CR_HOW_TO_EDIT` with these steps:

1. Unhide `Authoring`, edit a curve, run `rebuild_meshes()`.
2. Width, thickness, and vein count are the controls on that curve or on `CR_Controls`.
3. To change the open fan, pose the leaf bone at frame 300 and key the rotation. Leave the action in place.
4. Set `RESET = True` only when the plant should be replaced from scratch.
5. `publish()` writes the `.glb` and does not delete the curves.

Geometry Nodes on the curves are fine if the inputs sit on the modifier, where a person can drag them. A curve bevel profile they can edit is also fine. The curves stay the source of the shape. The file that goes to the phone is the solid mesh.

## Growth

30 fps. Frames 1–330. The action is named `Grow`. These are checkpoints, not a biological clock. The sand is complete from frame 1. Each part extends from its own base. The whole meadow is not scaled up from a dot.

- Frames 1–40. One bud on the sand. The stem is short, the leaves are short and folded, and the rhizome is only a stub.
- Frames 40–120. The rhizome tip extends through the sand. Fine roots grow down at a node once that node exists.
- Frames 120–200. The first shoots rise. The scar rings are already on the stem, so they appear because the stem lengthens. The leaves unroll.
- Frames 200–300. The remaining shoots and leaves reach full length. Round tips, veins on the faces, roots in the sand.
- Frames 300–316. Hold on the full meadow.
- Frame 316 uses constant interpolation. Frame 330 matches frame 1, so playback jumps back to the bud. It does not play the growth backwards.

Read the action API from the Blender that is actually open. Key pose-bone scale and Euler XYZ. Do not invent node socket names or exporter enum names.

## Phone file

The app shows `app/assets/models-3d/cymodocea_rotundata.glb` in `app/lib/widgets/glb_viewer.dart`.

- The color behind the viewer is `#1E8C98`. The Blender world is not that backdrop.
- The person rotates and zooms. Do not animate the camera.
- Playback uses the first animation clip. Name it `Grow`.
- Export keeps meshes, UVs, base color, roughness, normal, skin, and bone location, rotation, and scale. It drops Geometry Nodes values, curve bevel, drivers, constraints, subsurface, and transmission. The veins and the sand grain have to be in images. The shape has to be in the mesh.
- Stay under 40,000 triangles.
- Save the editable blend to `assets/models-3d/cymodocea_rotundata.blend`. Do not put the blend in `app/`.
- Export `Meadow` and `CR_Armature` only.

## Done when

- A side view shows thin strap edges. A front or top view shows flat faces, round tips, and faint long veins.
- Full-grown leaves are 6–8 mm wide and 7–15 cm long. The tip is smooth.
- One smooth rhizome sits in the sand. Roots enter the sand. Scars are thin rings.
- Frame 1 and frame 330 are the same bud. Frame 300 is the full meadow. Mesh scale is `(1, 1, 1)` the whole time.
- The `Authoring` curves are still in the blend after the `.glb` is written.
- Frames 1, 120, 200, and 300 were looked at from two directions, not from a single picture.

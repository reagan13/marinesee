# 3D species model spec

**IMPLEMENTATION.** This is the contract for every species model in MarineSee: the solid meadow, the growth animation, the phone `.glb`, and the rendered pitch clip. *Cymodocea rotundata* is the reference build (16 Oct 2026). The other eight species follow this file so all nine look, move, and load the same way.

Read with: `11-species.md` (slugs), `app/assets/data/species.json` (cited facts), `08-modules-and-business-logic.md` (M3), `19-evaluation-question-spec.md` and `20-evaluation-gaps.md` (FS-3, FS-7, PE-3, PE-4, PE-5).

## 0. Conflict to settle first

**CONFLICT.** `AGENTS.md`, `08-modules-and-business-logic.md` (M3), and `14-open-questions.md` #7 say this repo only integrates 3D and does not author Blender files. The owner asked for the *Cymodocea rotundata* build on purpose (`assets/models-3d/cymodocea_rotundata.md`), and asked for this spec so the other species are built the same way.

Default until the owner decides: a species is built in this repo only when the owner asks for that species. Each request is a brief like `cymodocea_rotundata.md`. When the owner confirms this is the standing rule, update `AGENTS.md`, M3 in `08-modules-and-business-logic.md`, and answer #7 in `14-open-questions.md` in the same change.

## 1. What every species delivers

| File | Path | Notes |
|------|------|-------|
| Brief | `assets/models-3d/<slug>.md` | Owner-facing prompt. Sections as in section 12. |
| Editable blend | `assets/models-3d/<slug>.blend` | Curves, meshes, rig, `Grow`, reef set, camera. Never in `app/`. |
| Phone model | `app/assets/models-3d/<slug>.glb` | The file the app loads. Copy to `assets/models-3d/<slug>.glb` (folder README rule). |
| Pitch clip | `assets/models-3d/<slug>_growth_render.mp4` | Rendered from the reef camera. For slides and the panel. |
| Edit guide | text datablock `<CODE>_HOW_TO_EDIT` in the blend | Five steps, section 6. |

`<slug>` comes from `11-species.md`. Nothing else names a species.

`app/assets/models-3d/<slug>_growth.mp4` is the app's fallback clip. The app plays it only when no `.glb` exists (`model_3d_library.dart`, `viewer_3d_screen.dart`). Do not ship a fallback clip for a species that has a `.glb`; it is dead weight in the APK.

## 2. Truth sources

Nothing in a model is allowed to state a fact that is not in one of these:

1. The species record in `app/assets/data/species.json` (`botanicalCharacteristics`, `habitat`, `growthProcess`, `sources`).
2. `11-species.md`.
3. A source already listed in that record's `sources` (for example Seagrass-Watch, https://www.seagrasswatch.org/idseagrass/).

A shape, size, color, or behavior that none of these state is a **display choice**. It goes in the species `CONFIG` with a comment that says so, or it stays **OPEN**. Do not describe a display choice as Mati field data.

## 3. Shared build pipeline

### 3.1 Layout

The *Cymodocea rotundata* reference lives in `assets/models-3d/rotundata_build/` with the entry `assets/models-3d/_build_rotundata.py`. Before the second species, split it into a shared core and one profile per species:

```text
assets/models-3d/
  _build_species.py          entry: SPECIES = "<slug>", RESET, OVERWRITE_ANIM, DO_PUBLISH
  seagrass_build/            shared core (one concern per file, < 300 lines each)
    util.py                  Bezier sampling, frames, collections
    textures.py              image helpers, water and sand images, material helper
    sand.py                  reef-sand mound with rhizome groove
    tube.py                  rhizome and root tubes, per-internode weights
    rig.py                   base bone + flat deform bones
    grow.py                  timeline scheduler (section 7)
    reef.py                  presentation set (section 9)
    render.py                pitch clip render (section 9)
    checks.py                automatic done-when checks (section 10)
    publish.py               phone export (section 8)
  species/
    cymodocea_rotundata.py   CONFIG, palette, organ builders, layout, growth story
    <slug>.py                one file per species
```

Shared code never names a species. A species file never re-implements sand, rig, export, or checks. If a species needs a new organ (for example a cylindrical leaf), add it as a builder in `seagrass_build/` only when a second species will use it; otherwise keep it in that species file.

The pitch render script currently sits outside the repo (it was run from a temp file). Move it into `seagrass_build/render.py` during the split.

### 3.2 Profile interface

Each `species/<slug>.py` exposes:

| Name | Type | Purpose |
|------|------|---------|
| `SLUG` | str | Must equal the `11-species.md` slug. |
| `CODE` | str | Two-letter object prefix, for example `CR`. Unique across the nine. |
| `CONFIG` | dict | Every layout number. Section 4. |
| `PALETTE` | dict | Color stops for each material. Section 5.4. |
| `create_authoring(cfg)` | fn | First-time curves and empties in `Authoring`. |
| `organ_builders()` | dict | Organ name to mesh builder (`leaf`, `shoot`, `rhizome`, `root`, ...). |
| `growth_story(cfg)` | fn | Ordered growth events for the scheduler (section 7). |
| `DIAGNOSTICS` | list | The features a viewer must be able to see (section 11). Checked by eye. |

### 3.3 Runs

| Run | What happens |
|-----|--------------|
| `RESET = True` | Remove that species' objects, collections, `Grow`, and orphan data. Build from scratch. Camera and lights stay. |
| Normal run | Keep every existing curve point. `rebuild_meshes()` refreshes `Meadow`. Keep `Grow` unless `OVERWRITE_ANIM = True`. Save the blend. |
| `DO_PUBLISH = True` | After the save: export the `.glb`, copy it, save again. Curves stay in the blend. |

Before the first save into an existing blend, copy any older `.blend1` that matters. Blender's save overwrites it.

## 4. Scale and display exaggeration

Units are metres. Blender unit scale is 1.0.

- Lengths stay inside the range the record states. Leaves on one shoot are not all the same length.
- Width may be exaggerated only when the real width would hide a diagnostic feature on a phone (for example a 2-4 mm leaf tip). Record the factor in `CONFIG` with a comment such as `display choice; real 2-4 mm (Seagrass-Watch)`. Keep the exaggeration as small as reads on a 320 px tall viewer.
- Thickness of a strap leaf about 0.3-0.4 mm. This is a display choice that keeps an edge-on view thin. It is not sourced.
- If the record gives no size for a part, the number is a display choice and the brief marks it **OPEN** for the adviser.

The phone viewer frames everything in the `.glb`, so absolute size does not change what fits on screen. Proportions between parts do.

### 4.1 CONFIG keys every species has

| Key | Meaning |
|-----|---------|
| `shoot_count` | Shoots on the rhizome run. 10-16 unless the species brief says otherwise. |
| `leaf_counts` | Leaves (or leaf pairs) per shoot, cycled. |
| `leaf_length_m` | (min, max) from the record. |
| `leaf_width_m` | Display width, with the real range in a comment. |
| `leaf_thickness_m` | Strap leaves only. |
| `vein_count` | Only if the record states veins. |
| `rhizome_radius_m`, `rhizome_sink_m` | Rhizome size and how far its centre sits below the groove floor. |
| `root_radius_m` | Fine roots. |
| `sand_bottom_z` | Depth of the solid mound. |
| `min_bone_scale` | 0.02. Never 0. |
| `fps`, `frame_hold`, `frame_end` | 30, 316, 330 for every species. |
| `seed` | Fixed per species so a reset gives the same plant. |

## 5. Geometry rules

### 5.1 Solid, always

- Every organ is closed solid geometry with real thickness. A plane, billboard, photo, or camera-facing card is never a leaf.
- From the side a strap leaf shows a thin edge. From the front it shows a flat face. A cylindrical leaf (*Syringodium*) reads round from every side.
- The sand is a solid mound with a cut side and a bottom, not a sheet.
- Rhizome is one welded tube, partly buried. Roots are thin solid tubes that go down into the sand.
- Sheaths have wall thickness. Leaf scars are thin closed bands built into the stem, a fraction of a millimetre proud, never separate tori or beads.
- Mesh object scale is (1, 1, 1) at every frame. Growth is bone scale, never object scale.

### 5.2 Two layers

| Collection | Holds | Exported |
|------------|-------|----------|
| `Authoring` | Bezier curves `<CODE>_Rhizome`, `<CODE>_Leaf_ii_j`, `<CODE>_Root_ii_r`, and shoot empties `<CODE>_Shoot_ii`. Hidden in the viewport by default. | No |
| `Meadow` | Solid meshes `Rhizome`, `Shoot_ii`, `Leaf_ii_j`, `Root_ii_r`, `ReefSand`, skinned to `<CODE>_Armature`. | Yes |
| `Reef` | Presentation set (section 9). | No |

Curve handles are AUTO. A shoot empty's local Z is the stem, local X is the fan side, local Y faces forward. Fans face Blender -Y in the default layout, which is the phone viewer's default camera side.

### 5.3 Organ catalogue

Use the matching builder. Add a new one only when a species record needs it.

| Organ | Builder | Used by | Rules |
|-------|---------|---------|-------|
| Strap leaf | `leaf_mesh` (closed cross-section: flat faces, thin rounded edges) | *C. rotundata*, *C. serrulata*, *Thalassia*, *Halodule* (both), *Enhalus* | Tip shape is a parameter: `round`, `serrated`, `trident`, `split_vein`. UV `u` runs across the width so veins run along the face, never around an edge. |
| Inrolled strap leaf | strap leaf with margins curled | *Enhalus* | Margins inrolled as stated in the record. |
| Cylindrical leaf | round tube, tapered point | *Syringodium* | Round cross-section. Tapers to a point. |
| Paired oval leaf | flat oval blade on a petiole, two per node | *Halophila* (both) | Cross-vein count is a species parameter (section 11). Smooth margin. |
| Short erect stem + sheath | `shoot_mesh` | strap-leaf species | Scar style is a parameter: `continuous_ring` (*C. rotundata*) or `not_continuous` (*C. serrulata*). Sheath shape is a parameter. |
| Rhizome | `rhizome_mesh` | all | Node swells, tapered growing tip, per-internode weights. Thickness and surface (smooth, scarred, bristled) are parameters. |
| Root | `root_mesh` | all | Fine or cord-like per record. Ends stay inside the sand. |

### 5.4 Color and materials

- Principled BSDF only. Metallic 0. No emission, transmission, glass, or neon.
- Base color comes from a packed image when the part carries a pattern (veins, tannin bars, scars, sand grain). Plain parts use the node color.
- Shared defaults: younger leaves lighter, leaf base paler, rhizome pale, roots cream, sand warm and pale. A species overrides only what its record states (for example dark tannin bars in *Thalassia*, black leaf scars in *Halodule*, black bristles on the *Enhalus* rhizome).
- Material names `<CODE>Leaf`, `<CODE>LeafYoung`, `<CODE>Rhizome`, `<CODE>Root`, `<CODE>Stem`, `<CODE>Sheath`, `<CODE>Scar`. The sand and water materials are shared: `SeaSand`, `SeaWater`.
- Images packed into the blend. Leaf images about 256 x 512, sand about 256 x 256.

## 6. Editing contract

`<CODE>_Controls` is an empty with `leaf_width_m`, `leaf_thickness_m`, `vein_count` (when used), and `shoot_count`. These are read when a missing piece is built. They are never driven per frame.

A curve may override with `cr_width_m` or `cr_thickness_m` (keep the `cr_` property prefix for all species so tools stay shared). `cr_hand_edited = True` on a curve or mesh means `rebuild_meshes()` leaves it alone.

The `<CODE>_HOW_TO_EDIT` text says, in this order:

1. Unhide `Authoring`, edit a curve, run `rebuild_meshes()`.
2. Width, thickness, and vein count are the controls on that curve or on `<CODE>_Controls`.
3. To change the open fan, pose the leaf bone at frame 300 and key the rotation. Leave the action in place.
4. Set `RESET = True` only when the plant should be replaced from scratch.
5. `publish()` writes the `.glb` and does not delete the curves.

Add: after moving a curve a long way, run once with `OVERWRITE_ANIM = True`.

## 7. Rig and growth

### 7.1 Rig

- One armature `<CODE>_Armature`, one unscaled `base` bone, every deform bone a direct child of `base`. No bone inherits a non-uniform scale. This is what keeps glTF from shearing a leaf.
- Bones: `rhizome_kk` per internode, `shoot_ii`, `leaf_ii_j`, `root_ii_r`.
- Growth keys pose-bone scale Y (X and Z stay 1), Euler XYZ rotation, and location. Location keeps parts joined: later internodes ride the growing rhizome tip, and leaf bases ride up inside the sheath as the stem lengthens.
- Rhizome keys are linear so the riding location matches the lengthening exactly.

### 7.2 Timeline (same for all nine)

30 fps, frames 1-330, one action named `Grow`. The sand is complete from frame 1. Each part extends from its own base. The meadow is never scaled up from a dot.

| Frames | Must show |
|--------|-----------|
| 1-40 | One bud on the sand. Short stem, short folded leaves, rhizome stub. |
| 40-120 | Rhizome tip extends through the sand. Roots grow down at a node once that node exists. |
| 120-200 | First shoots rise. Scar bands are already on the stem. Leaves unroll. |
| 200-300 | Remaining shoots and leaves reach full length. |
| 300-316 | Hold on the full meadow. |
| 316 | Constant interpolation. |
| 330 | Equals frame 1, so playback jumps back to the bud. It never plays backwards. |

A species may change what happens inside a window only when its `growthProcess` text says so (section 11). The windows do not move.

## 8. Phone file

Facts about the viewer (`app/lib/widgets/glb_viewer.dart`): backdrop `#1E8C98`, height 320 px, first animation clip, Play starts at time 0 and loops, `autoPlay: false`, default orbit `0deg 75deg 105%`, drag, Rotate, Zoom in, Zoom out.

- Export `Meadow` and `<CODE>_Armature` only. No curves, controls, camera, lights, or reef.
- One animation clip, named `Grow`.
- Keep meshes, UVs, base color, roughness, normals, skin, and bone location, rotation, and scale. Geometry Nodes values, curve bevel, drivers, constraints, subsurface, and transmission do not survive export, so patterns are in images and shape is in the mesh.
- Read exporter property names from the open Blender before setting them. Do not guess enum names.
- The exporter bakes the animation frame by frame because of the constant key at 316. That is expected.
- Do not animate the camera. The person rotates and zooms.

### 8.1 Budgets

| Item | Limit | Reference (*C. rotundata*) |
|------|-------|----------------------------|
| Triangles | under 40,000 | 37,482 |
| `.glb` size | about 4 MB or less | 2.2 MB |
| Bones | about 120 or fewer | 88 |
| Images | three or four, 512 px or less on the long side | 3 |

PE-4 and PE-5 are timed on a phone, not here. A model that passes these budgets has still not passed PE-4.

## 9. Presentation set and pitch clip

The phone shows the plant on the viewer's blue-green. Slides and the panel see the rendered clip, which shows the plant in its place.

### 9.1 Reef set (collection `Reef`, never exported)

- `ReefFlat`: a broad sand flat that hides the mound's cut side. Uses `SeaSand`.
- `ReefWater`: a cylindrical wall facing inward, shallow water gradient. Uses `SeaWater`. Not `#1E8C98`.
- Lighting: soft overhead sun, cool fill, dark sea-green world. No studio grey.
- Habitat wording comes from the record. A species described on "shallow reef flats" gets a reef flat. A species "next to mangrove forest" (*Enhalus*) does not get a mangrove model unless the owner asks; the record supports the sentence, not the set.

### 9.2 Camera and render

| Setting | Value |
|---------|-------|
| Camera | Fixed, no animation. Low three-quarter front view, the whole patch in frame. |
| Resolution | 1280 x 720 |
| Frames | 1-330 at 30 fps |
| Engine | EEVEE, about 16 samples |
| Output | FFMPEG, MPEG-4, H.264. In Blender 5.x set `media_type = "VIDEO"` before `file_format`. |
| File | `assets/models-3d/<slug>_growth_render.mp4` |

### 9.3 Pitch line

Each brief carries a three-sentence pitch built only from that species' record:

1. What the viewer is looking at: one species, a display model, not a scan of a Mati meadow.
2. What the clip teaches, from `growthProcess`.
3. What to rotate to see, from the diagnostic features (section 11), and which number is a display choice.

Reference (*C. rotundata*): "This is one species, not a scan of a Mati meadow. It starts as one bud; the buried rhizome extends, roots go down at each node, and new shoots rise until it is a patch. Turn it to see the thin edge and the flat veined face with a rounded tip; the leaf width is enlarged so the tip reads on a phone."

## 10. Done when

### 10.1 Automatic (`checks.validate()`)

- Triangles under 40,000.
- Every `Meadow` mesh at object scale (1, 1, 1).
- Every deform bone has scale X = Z = 1 and Y >= 0.02 at frames 1, 20, 40, 60, 80, 100, 120, 150, 180, 200, 230, 260, 300, 316, 330.
- Every pose bone's basis matrix at frame 1 equals frame 330.
- `Grow` exists. `Authoring` curves are still in the blend after the `.glb` is written.

### 10.2 Read from the `.glb`

- One animation, `Grow`, 0 to 11 s.
- Images packed. No curve, controls, camera, light, or reef nodes.
- Triangle count matches the blend.

### 10.3 By eye in Blender (two directions each)

| Look | From |
|------|------|
| Frames 1, 120, 200, 300 | front and a raised side view |
| Full meadow | front, side, top, three-quarter |
| Each diagnostic feature (section 11) | close-up, face-on and edge-on where it applies |
| Rhizome node | close-up, plus x-ray to see roots inside the sand |
| Pitch camera | frame 300 through the camera |

If any view looks like a drawing, a flat texture, or a row of identical tubes, it is not done.

### 10.4 Evaluation rows

Building a model never marks a row `met`. FS-3 needs the species' 3D view reachable from an identify result on a phone. FS-7 and PE-4 need a tester to rotate and zoom it on a phone. PE-5 needs several species opened in one session. When a new `.glb` lands, update the Evidence text of the rows it touches in `19-evaluation-question-spec.md` and the lists in `20-evaluation-gaps.md` in the same change, and leave the Status alone until the phone pass.

## 11. Species briefs

Every row quotes only `species.json`. "Must show" is what a viewer has to be able to see. Anything marked **OPEN** needs an adviser source before it becomes a number.

### Cymodocea rotundata (`CR`) — reference, built

- Record: flat strap leaves about 2-4 mm wide, rounded smooth tip; leaf-sheath scars form a continuous ring around the stem; smooth rhizome. Shallow reef flats. Spreads by the buried rhizome sending up new shoots.
- Must show: rounded smooth tip with no serration; continuous scar ring; smooth rhizome; faint longitudinal veins.
- Display choices: width 7 mm; 11 veins; 12 shoots; stem 20 mm.
- Look-alike: *C. serrulata* (wider, serrated tip).

### Cymodocea serrulata (`CS`)

- Record: strap leaves about 5-9 mm wide, serrated tip; broadly triangular leaf sheath; leaf scars do not form a continuous ring. Shallow subtidal reef flats and sand banks. Spreads by the buried rhizome; described as fast growing and able to recolonize after disturbance.
- Must show: serrated tip (the feature that separates it from *C. rotundata*); broadly triangular sheath; broken, not continuous, scars.
- Reuse: everything from *C. rotundata* except tip, sheath, and scar parameters.
- OPEN: tooth count and size on the tip; vein count; stem height.

### Enhalus acoroides (`EA`)

- Record: very long ribbon leaves about 30-150 cm, inrolled margins; thick rhizome with long black bristles and cord-like roots. Shallow and intertidal sand or mud banks, often next to mangroves. Spreads by the thick rhizome; separate male and female flowers.
- Must show: inrolled margins; thick bristled rhizome; cord-like roots; very long leaves.
- Note: at 30-150 cm the patch is far bigger than the others. The viewer frames it anyway; fewer shoots may be needed to stay under budget.
- OPEN: leaf width; bristle length and count. Flowers stay out of v1, as in the *C. rotundata* brief, unless the owner adds them.

### Halodule pinifolia (`HP`)

- Record: fine leaves up to about 20 cm, one central vein that splits in two at a rounded leaf tip; usually pale rhizome with clean black leaf scars. Intertidal sand banks. Spreads by the buried rhizome.
- Must show: single dark central vein; the split at a rounded tip (the feature that separates it from *H. uninervis*); black scars on a pale rhizome.
- OPEN: leaf width (record says "fine", no number).

### Halodule uninervis (`HU`)

- Record: usually larger than *H. pinifolia*, one central vein, trident leaf tip; usually pale ivory rhizome with clean black leaf scars. Shallow and intertidal sand or mud banks. Spreads by the buried rhizome.
- Must show: trident tip; single central vein; black scars on a pale ivory rhizome. Build after *H. pinifolia* and keep the two side by side for the tip check.
- OPEN: leaf width and length.

### Halophila minor (`HM`)

- Record: small oval leaves in pairs, fewer than eight pairs of cross veins, smooth margins, wedge-shaped leaf sheath. Shallow and intertidal sand flats. Leaves arise in pairs from the rhizome; spreads by rhizome growth.
- Must show: paired oval leaves; fewer than eight cross-vein pairs (pick a display count, for example 5-7, and say so); smooth margin; wedge sheath. Growth story: leaf pairs rise from nodes along the rhizome; there is no erect stem with a fan.
- OPEN: leaf length and width; petiole length.

### Halophila ovalis (`HO`)

- Record: oval leaves in pairs, eight or more cross veins, no hairs on the leaf surface. Intertidal to subtidal. Common early coloniser; spreads by rhizome growth.
- Must show: paired oval leaves; eight or more cross veins; smooth hairless surface. Share the paired-leaf builder with *H. minor*; the vein count and size are the only differences the record supports.
- Growth story may open on bare sand before the bud appears, because the record calls it an early coloniser. That stays inside frames 1-40.
- OPEN: leaf size relative to *H. minor* (record says *H. minor* is smaller, no numbers).

### Syringodium isoetifolium (`SI`)

- Record: leaves cylindrical in cross section, like spaghetti, tip tapers to a point; about 7-30 cm long. Shallow subtidal reef flats and sand banks. Spreads by the buried rhizome.
- Must show: round leaf from every side (the one species where the edge-on rule does not apply); tapered point.
- OPEN: leaf diameter; sheath shape.

### Thalassia hemprichii (`TH`)

- Record: curved ribbon leaves about 10-40 cm, short black bars of tannin cells in the blade; thick rhizome with scars between the shoots. Shallow reef flats. Spreads by the thick rhizome.
- Must show: curved ribbon leaves; short dark tannin bars in the leaf image; thick rhizome with scars between shoots.
- OPEN: leaf width; tannin bar density. This is the species held out of v1 training (`11-species.md`); the model can still be built.

## 12. Brief template

Each `assets/models-3d/<slug>.md` uses these headings, in this order, and fills them from section 11:

1. One species only, and what is out of scope.
2. The model is solid geometry (section 5.1, with this species' organs).
3. Close to the real plant (record quotes, sources, look-alike that must fail).
4. Layout numbers are display choices (the `CONFIG` table).
5. Replace or build (what exists now, what must not be kept).
6. What a person can still edit (section 6).
7. Growth (section 7.2, plus any species change allowed by its record).
8. Phone file (section 8).
9. Presentation and pitch (section 9).
10. Done when (section 10).

## 13. Build order

Suggested, so each step reuses the last:

1. Split the reference into `seagrass_build/` + `species/cymodocea_rotundata.py`. Rebuild *C. rotundata* and confirm the `.glb` and checks match the 16 Oct 2026 numbers.
2. *Cymodocea serrulata*: tip, sheath, and scar parameters only.
3. *Halodule pinifolia*, then *H. uninervis*: thin strap leaf, vein and tip parameters.
4. *Thalassia hemprichii*: curved ribbon leaf, tannin-bar image, thick rhizome.
5. *Syringodium isoetifolium*: cylindrical leaf builder.
6. *Halophila minor*, then *H. ovalis*: paired oval leaf builder, cross-vein image.
7. *Enhalus acoroides*: inrolled leaf, bristled rhizome, the largest scale.

## 14. Reference build status (*Cymodocea rotundata*, 16 Oct 2026)

| Item | State |
|------|-------|
| Blend | `assets/models-3d/cymodocea_rotundata.blend` (meadow + reef set). Studio-only copy: `cymodocea_rotundata_studio.blend`. October 10 backup: `cymodocea_rotundata_2026-10-10.blend1`. |
| Phone file | `app/assets/models-3d/cymodocea_rotundata.glb`, copy in `assets/models-3d/`. 37,482 triangles, 36 leaves, 88 bones, clip `Grow`. |
| Pitch clip | `assets/models-3d/cymodocea_rotundata_growth_render.mp4`, reef set. |
| Old clip | `cymodocea_rotundata_growth.mp4` (19 Sep 2026) is from the previous model and is not used by the app while the `.glb` exists. Remove it from `app/assets/models-3d/` or replace it. |
| Phone pass | Not done. FS-7 and PE-4 stay `unmeasured`. |
| To fix in the split | Object prefix is hard-coded `CR_`; `publish()` writes one copy only; the render script is not in the repo. |

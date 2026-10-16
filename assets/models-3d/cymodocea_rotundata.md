# Cymodocea rotundata — 3D brief

One species only: *Cymodocea rotundata* (smooth ribbon seagrass). View in 3D shows a small meadow of this plant on reef sand. The viewer background is shallow water, `Color(0xFF1E8C98)`. Drag turns the meadow. Zoom stays available. Play runs an 11-second growth, then returns to the bud and grows again. The camera does not spin by itself.

Out of scope: the other eight species, a photo scan, animals, flowers, a map, and a status badge.

## Facts to match

Sources: the `cymodocea_rotundata` record in `app/assets/data/species.json`, `docs/11-species.md`, and Seagrass-Watch (code CR), https://www.seagrasswatch.org/idseagrass/

- Common name: smooth ribbon seagrass.
- Leaves: flat straps with a rounded smooth tip and no serrations. About 9–15 faint longitudinal veins.
- Real leaves are about 2–4 mm wide. This model uses about 6–8 mm so the rounded tip stays readable on a phone. Length stays about 7–15 cm.
- Stem: leaf-sheath scars form a continuous ring. The sheath is well developed.
- Rhizome: smooth, horizontal, buried in shallow reef sand. New shoots come off it. Fine roots at the nodes.
- Habitat look: shallow reef flat. Mati records (Lawigan, Taitaidaga, Manguihay, Pujada Bay) stay in the text. Do not build a map.
- Growth the app is teaching: the patch spreads when the buried rhizome grows and sends up new shoots.
- Wrong species: *Cymodocea serrulata* is wider (about 5–9 mm) and the tip is serrated. A saw-tooth tip fails this model.

## Meadow

- Many shoots on one creeping rhizome. Not one shoot, and not four poles.
- Leaves are thin flat strips, about 8 mm wide and 7–15 cm long, with a rounded end, a slight curve, and mixed heights.
- Veins: about 11 faint lines. Visible up close, not plastic ribs.
- Rhizome: one smooth creeping stem, partly in the sand.
- Roots: fine, from the nodes, going down into the sand.
- Rings: narrow continuous bands on the short stem. Visible, not beads.
- Sand: an irregular low mound with small ripples. No square plate. No black soil.
- Color: seagrass green, younger leaves lighter, rhizome pale, roots cream, sand warm and pale. No metal, no neon, no heavy glass.
- Light: soft, so the straps and rings read against the teal water.

## Growth clip

330 frames at 30 fps (11 seconds). Checkpoints, not a biological clock.

- Bud: frames 1–40. One small bud on the sand. The rhizome and full leaves are not yet the picture.
- Rhizome and roots: frames 40–120. The rhizome extends through the sand and fine roots appear at the nodes.
- First shoots and rings: frames 120–200. A shoot rises. Sheath rings are already on the stem. Narrow leaves start to open.
- Remaining shoots and full leaves: frames 200–300. Many shoots along the rhizome, straps with rounded tips and faint veins, roots in the sand.
- Frames 316–330: the meadow jumps back to the bud.
- Frame 1 and frame 330 are the same bud pose, so the loop does not pop.
- Growth stays connected. Parts extend from their own bases. The whole meadow is not scaled up from a dot.

One action, named `Grow`. Curves live on the action’s channel bags.

## Files

- Blend (not in `app/`): `assets/models-3d/cymodocea_rotundata.blend`
- App model: `app/assets/models-3d/cymodocea_rotundata.glb`

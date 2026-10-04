# 3D assets (integration drop)

This folder is a **receive** box. We do not author Blender files in this repo.

When a teammate exports a model, put it here **and** copy the same file into
`app/assets/models-3d/` so Flutter can bundle it (`<slug>.glb` or
`<slug>_growth.mp4`; slugs in `docs/11-species.md`).

The app plays a growth `.mp4` if present, notes a `.glb` if present (rotate/zoom
is not wired yet), otherwise shows `app/assets/images/species/<slug>.*` as a
photo preview. Missing everything still shows the placeholder.

See `docs/08-modules-and-business-logic.md` (M3).

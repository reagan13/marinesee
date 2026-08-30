# MarineSee (seagrass)

Android educational app for the **nine documented seagrass species of Mati City**. Users identify a photo with a **Support Vector Machine**, inspect an interactive **3D model**, and read a localized species profile.

This repository is the capstone implementation workspace. The paper is not a complete technical spec. **Start in `docs/`.**

## Read first

1. [docs/README.md](docs/README.md) — documentation index
2. [docs/00-study-review.md](docs/00-study-review.md) — what the study got right and what it left open
3. [docs/06-architecture.md](docs/06-architecture.md) — one repo, Colab training, Drive dataset
4. [docs/16-flutter-audit-and-scaffold.md](docs/16-flutter-audit-and-scaffold.md) — Flutter app (locked)
5. [docs/17-how-to-run-flutter.md](docs/17-how-to-run-flutter.md) — phone only, no emulator
6. [docs/15-implementation-roadmap.md](docs/15-implementation-roadmap.md) — build order

## What this is

| Piece | Role |
|-------|------|
| `docs/` | Study + implementation spec (same idea as pgso / furescue) |
| `app/` | Flutter client (scaffold not created yet) |
| `ml/` | Preprocess, features, SVM training notebooks |
| `data/` | Pointers only — images stay on Google Drive |
| `assets/models-3d/` | 3D models when we version them |

## Stack (locked vs open)

**Locked by the study:** Android 8+ app · SVM · nine Mati species · ≥ 85% test accuracy · ISO/IEC 25010.

**Locked here:** Flutter client · Colab training · Drive images · 3D is a file drop, not our Blender work.

**Open:** Firebase vs bundled JSON, on-device vs API inference. See [docs/14-open-questions.md](docs/14-open-questions.md).

## Training

Code lives here. **Train on Google Colab.** The dataset is already on Google Drive — do not commit images.

```text
Cursor edits ml/  →  Colab mounts Drive and runs the notebook  →  export model into ml/artifacts/
```

## Local status

No app or trained model in this folder yet. Documentation and repo layout only.

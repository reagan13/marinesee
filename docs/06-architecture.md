# Architecture

The capstone paper names **Android Studio**, **Blender**, and **Firebase/MySQL**. It does not specify a repository shape, an inference path, or Google Colab.

**IMPLEMENTATION** — this is the architecture we will build unless `14-open-questions.md` changes it.

## Decision: one repo (monolith)

Keep the **mobile app**, **training code**, and **docs** in this single `seagrass` repository.

| Why one repo | Why not two repos |
|--------------|-------------------|
| Capstone is one product: identify + 3D + library | Split repos make the 85% model and the app drift apart |
| Species list, class names, and profile IDs must match | Two remotes for a small team is extra ceremony |
| Colab can `git clone` / pull this repo and train | Dataset is already on Drive; it does not need its own git repo |
| Same pattern as pgso / furescue: one folder, one docs tree | |

This is a **monorepo**, not a single file. App code and ML code stay in different folders.

## Decision: code here, train on Colab, data on Drive

```text
Cursor (this repo)     Google Drive              Google Colab
─────────────────      ────────────              ────────────
app/   Android UI      labeled images            mounts Drive
ml/    notebooks +     exported .joblib/.onnx    runs notebooks
       feature/SVM     optional 3D sources       writes metrics
docs/  study spec      (not git)                 optionally git pull
```

Cursor does **not** attach to a live Colab kernel. That is fine. The contract is:

1. Edit notebooks and Python under `ml/` in this repo.
2. Open the same notebook in Colab (upload, Drive shortcut, or `git clone`).
3. Mount the dataset folder on Drive.
4. Train. Write metrics and the model file back to Drive (and later into `ml/artifacts/` if the file is small enough).
5. The Android app loads the exported model (on-device) or calls a small API that loads it.

Details: `12-colab-and-training.md`.

## Locked by the study

```text
Client:     Android application (floor: Android 8.0, 3 GB RAM)
3D:         study names Blender; this repo only integrates dropped .glb/.mp4
Classifier: Support Vector Machine on color + texture + shape features
Classes:    exactly the nine Mati species
Split:      70% train / 15% validation / 15% test
Accuracy:   ≥ 85% on the test set
Network:    paper requires internet for 3D + content
```

Do not introduce YOLO, CNN, or a second species list unless the paper and `00-study-review.md` are updated.

## Still OPEN (do not pretend the paper decided)

| Topic | Options | Default until decided |
|-------|---------|------------------------|
| App toolkit | Flutter (locked 30 Aug 2026). Android 8+ APK. No emulator on this laptop. | See `16-flutter-audit-and-scaffold.md` |
| Content store | Firebase (Firestore + Storage), MySQL + small API, or bundled JSON in the APK | **Bundled JSON + Firebase Storage for 3D** only if we need remote assets; otherwise bundle profiles in the APK for v1 |
| Inference | On-device (ONNX / similar) vs small Python API | **OPEN** — Colab training is the same either way |
| Visitor accounts | Guest-only vs login | **Guest identify + library**; admin login only |

When the team picks, update this file and `14-open-questions.md`.

## Logical layers

```text
Android app (app/)
  Identify screen  →  camera / gallery
  Preprocess       →  same resize/enhance contract as training
  Infer            →  on-device model  OR  POST /identify
  Result           →  species + confidence + profile + 3D

Digital library
  Species records  →  local store or Firebase/MySQL
  3D viewer        →  play dropped .glb / .mp4 or placeholder (we do not model)

ml/  (Colab)
  preprocess → extract features → train SVM → evaluate → export
```

Rules:

- Class names in the app **must** match folder names / label map in `ml/`.
- Do not re-implement feature extraction differently at train vs infer. Share the Python used in Colab; if inference is on-device, port that exact vector.
- Controllers / screens do not train models.
- Training notebooks do not embed Drive secrets. Mount paths stay in a Colab cell or ignored config.

## Folder structure

```text
seagrass/
├── app/                    Flutter project (Android APK, minSdk 26)
├── ml/
│   ├── notebooks/          Colab-ready .ipynb
│   ├── src/                preprocess, features, train, eval
│   └── artifacts/          exported model + label map (no images)
├── data/                   README only — images stay on Drive
├── assets/models-3d/       3D files if we version them here
├── docs/                   this documentation
├── AGENTS.md
└── README.md
```

## Why not train inside Cursor

SVM training is light, but the **images** are large and already on Drive. Colab has the disk, the GPU (useful for resize/augment), and the mount you already have. Cursor stays the place we write and review code.

## Why we still version `ml/` in git

The study must be reproducible: same resize, same features, same split seed, same metrics. Colab scratch cells disappear. Git keeps the pipeline the panel can inspect.

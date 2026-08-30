# Implementation Roadmap

Suggested order. Waterfall in the paper is the **documentation story**. Build incrementally so Colab work and the app do not wait on each other forever.

## 0. Repo and study lock (this step)

- [x] Extract the paper into `docs/`
- [ ] Confirm open questions 1–4 and 5–9 in `14-open-questions.md`
- [ ] `git init` + first commit when you ask for it
- [ ] Add a remote if you want Colab to `git clone`

## 1. Dataset contract

- [x] Drive path and 30 Aug 2026 counts (`ml/artifacts/inventory.md`)
- [x] v1 = eight `all` classes; *Thalassia* held out
- [ ] Update the paper’s `[INSERT NUMBER]` and tell the adviser about the missing class

## 2. Training pipeline

- [x] `ml/src` preprocess, features, split, train
- [x] Colab notebook `02_svm_v1_eight_class.ipynb`
- [ ] Run 02 in Colab; paste test accuracy here
- [ ] Export artifacts into `ml/artifacts/` (and Drive `Seagrass-ml-artifacts/v1`)

## 3. Content

- Fill nine profiles from cited sources (adviser review)
- 3D files are a teammate drop (`assets/models-3d/`), not our Blender work

## 4. Flutter scaffold

- [ ] Spec: `16-flutter-audit-and-scaffold.md`
- [ ] Machine: `17-how-to-run-flutter.md`
- [ ] Accept: `18-scaffold-done-when.md`
- [ ] Implement `app/` (next Cursor prompt) — Identify / Library / About, stub classifier, 3D placeholder

## 5. Identify integration

- Wire camera + gallery
- Same preprocess + features as Colab
- Show class + confidence + retake

## 6. 3D viewer

- Load one `.glb`, then the rest
- Rotate / zoom / inspect

## 7. Admin + store (if not bundled-only)

- Role gate
- Edit profiles

## 8. Test and evaluation

- Unit tests for feature vector stability
- Device pass on Android 8+ floor
- ISO 25010 form (`13-evaluation-iso25010.md`)

Do not start a second ML architecture (CNN/YOLO) in parallel “just to compare” unless the adviser asks. That is a new study objective.

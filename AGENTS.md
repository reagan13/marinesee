# AGENTS.md

MarineSee: Flutter Android app + SVM identification for Mati City. One git repo holds `docs/`, `app/`, and `ml/`. Images stay on Google Drive. Training runs on Google Colab. Daily app work is Cursor + `flutter` CLI + a **physical phone**. Do not use the Android emulator.

Read `docs/README.md` before changing product behavior. Labels: **STUDY** / **IMPLEMENTATION** / **OPEN** / **CONFLICT**.

## Hard rules

- **SVM only.** Do not add YOLO, CNN, or a second classifier to “beat 85%” unless `docs/09-ml-pipeline.md` and the paper are updated first.
- **Nine species only.** Class names and folder slugs must match `docs/11-species.md`.
- **No dataset in git.** Raw images, augmented copies, and Drive credentials never get committed. Point at Drive from Colab; keep `data/README.md` current.
- **Train/serve contract.** Feature extraction at inference must match training. Change `ml/src` first, then the app or API.
- **Do not invent science.** Species profile text, conservation status, and habitat claims need a cited source or stay `OPEN`.
- **Do not expand scope.** No iOS v1, VR/AR, GPS/GIS, water-quality sensors, extra taxa, or Filipino/Bisaya until the study says so.
- **No Blender work in this repo.** 3D is integration only: play a dropped `.glb` / `.mp4` or show a placeholder. Do not author `.blend` files or treat modeling as a task here.
- **Flutter only for the client.** Android minSdk 26. Physical phone. Never add a Kotlin/React Native second app. Never treat the emulator as the default device.
- **Evaluation questions.** The 29 user statements and their pass checks are `docs/19-evaluation-question-spec.md`. Before any `app/` change, read `docs/20-evaluation-gaps.md` and keep every open statement. Do not claim a high user score while a row is `not-met` or `unmeasured`. Update a row’s status in the same change that affects it, and update the gap lists in the same edit. Do not add security or maintainability items to that user form.

## Layout

```text
app/                 Flutter project (Android minSdk 26)
ml/notebooks/        Colab-ready notebooks
ml/src/              preprocess, features, train, eval
ml/artifacts/        exported model + label map + metrics (no images)
data/                README only
docs/                working spec
```

## Colab

Cursor does not attach to a Colab kernel. Edit files here; run them on Colab with Drive mounted. Workflow: `docs/12-colab-and-training.md`.

## Modular files

One concern per file. Split past ~300 lines. App screens stay out of training notebooks. Notebooks should import `ml/src` instead of pasting a second pipeline.

## Commands (fill in when the stack is chosen)

```bat
cd app
flutter pub get
flutter devices
flutter run
flutter analyze
```

Phone only. See `docs/17-how-to-run-flutter.md`.

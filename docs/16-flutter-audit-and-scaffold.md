# Flutter audit and scaffold spec

**IMPLEMENTATION** — 30 Aug 2026. Toolkit is **Flutter**. Target is still an **Android 8.0+** APK (study). We chose Flutter so this laptop (Ryzen 5 7520U, ~16 GB RAM, Radeon iGPU) does not have to run Android Studio + emulator every day.

The paper names Android Studio. That is the **official Android toolchain**, not a requirement to live in the Android Studio UI. Flutter builds the same Android APK. For oral defense: “Flutter + Android SDK, tested on a physical phone.” Open Android Studio only if the panel wants a screenshot.

Do not scaffold Kotlin “as well.” One client.

## Audit (what is already true)

| Item | Status |
|------|--------|
| Study extracted into `docs/` | Done |
| Monorepo: `app/` + `ml/` + `docs/` | Done |
| SVM pipeline + Colab notebooks | Done (v1 smoke **22.4%** — not shippable) |
| Nine species locked; *Thalassia* held out of training | Done |
| 3D = integration / placeholder (no Blender in this repo) | Done |
| Guest identify + library (no visitor login) | Default |
| Bundled JSON for profiles in v1 | Default |
| Flutter project under `app/` | **Not started** |
| Camera → real SVM on device | **Not started** (scaffold must not fake 85%) |
| Adviser-approved species paragraphs | **OPEN** — stub copy only |
| Who drops `.glb` / `.mp4` | **OPEN** |
| On-device vs API inference | **OPEN** — scaffold uses a `Classifier` interface with a stub |

## What we will not do in the scaffold

- No Android emulator (kills this CPU/iGPU).
- No iOS as a v1 target (study limitation). An `ios/` folder from `flutter create` may exist; do not spend time on it.
- No Firebase, no MySQL, no admin console.
- No Blender, no SceneView unless a `.glb` is already in `assets/models-3d/`.
- No YOLO / CNN / second model.
- No invented IUCN or habitat science. Profile body text = `TBD — adviser source`.
- No claim that identify is accurate. Stub returns a clear **“Model not connected”** (or a labeled demo pick), never a fake high confidence.

## Laptop-safe rules

Recorded machine: AMD Ryzen 5 7520U (4 cores), 15.2 GB RAM, AMD Radeon graphics.

1. Work in **Cursor**. Do not keep Android Studio open.
2. Run on a **physical Android 8+ phone** (USB debugging).
3. Do not install or launch the Android Emulator.
4. Do not run Colab + Flutter build + heavy Chrome at the same time.
5. `flutter run` once the phone is plugged in. Close the run when you stop testing.

Install steps: `17-how-to-run-flutter.md`.

## Flutter / Android versions (lock)

| Piece | Value |
|-------|--------|
| Flutter | Stable, 3.22+ (whatever `flutter upgrade` gives on install day — pin in `app/pubspec.yaml`) |
| Dart | 3.x (comes with Flutter) |
| minSdk | **26** (Android 8.0 Oreo) |
| targetSdk | current Flutter default |
| Platform | Android only for v1 |

## App folder (after `flutter create`)

`app/` **is** the Flutter project root (not `app/marine_see/`).

```text
app/
  lib/
    main.dart
    app.dart                 MaterialApp + theme + routes
    theme/
      tokens.dart            colors, radius, type — no raw hex in widgets
    data/
      species.dart           Species model
      species_catalog.dart   loads bundled JSON
    classify/
      classifier.dart        interface
      stub_classifier.dart   “not connected” — only impl in scaffold
    screens/
      shell.dart             bottom nav
      identify_screen.dart
      result_screen.dart
      library_screen.dart
      species_screen.dart
      viewer_3d_screen.dart  placeholder
      about_screen.dart
    widgets/                 small shared bits only
  assets/
    data/species.json
    images/                  optional cover placeholders
  pubspec.yaml
  android/                   minSdk 26
```

One screen per file. Split before ~300 lines. No god `main.dart`.

## Navigation (FR-8)

Bottom nav, three tabs (visitor, guest-first):

1. **Identify** — camera + gallery
2. **Library** — nine rows (eight real slugs + *Thalassia* marked “data coming”)
3. **About** — one-screen purpose + conservation blurb (FR-7), English only

From Library or Identify result → **Species profile** → **3D** (placeholder).

## Screens — scaffold done-when

### Identify (FR-1, FR-2, FR-4)

- Pick camera or gallery (`image_picker`).
- Show the chosen image.
- Button **Identify** calls `Classifier`.
- Scaffold impl: `StubClassifier` → message **“SVM not connected yet (Colab v1 is 22%).”** No fake species name that looks real unless the UI labels it **Demo**.
- After a real classifier exists: show name + confidence + retake if low. Threshold stays **OPEN**.

### Result + profile (FR-3, FR-6)

- Fields from `11-species.md`. Empty science fields show `TBD`.
- Slugs **must** match `ml/src/dataset_contract.py` / `11-species.md`.

### 3D (FR-5)

- If `assets/models-3d/<slug>.glb` or `_growth.mp4` is missing: placeholder copy, no crash.
- Do not add a 3D engine in the scaffold.

### About

- MarineSee, Mati City, nine species, SVM, English, Android 8+ floor.

## Theme (keep the laptop and the panel calm)

Coastal / educational, not a second FurEscue skin.

- Define tokens in `lib/theme/tokens.dart` (background, ink, brand, danger, radius).
- Material 3, large tap targets (FR-11).
- Test on the **phone** (≈360–412 dp). No 1440 desktop pass; this is not the PHP web apps.

## Packages allowed in scaffold

Keep the first `pubspec` short:

- `image_picker`
- `google_fonts` **or** device fonts only (prefer device fonts to save build time)
- No Firebase, no ML kit, no tflite, no camera plugin besides picker unless needed

## Classifier seam (for later, not now)

```text
abstract class Classifier {
  Future<IdentifyResult> identify(File image);
}
```

`IdentifyResult`: `slug?`, `confidence?`, `status: stub | ok | lowConfidence | error`.

Wiring the Colab `.joblib` is a **later** task (`06-architecture.md` inference still OPEN). Scaffold only the interface + stub.

## Panel / paper honesty

| They may ask | Answer |
|--------------|--------|
| Why not Android Studio? | Flutter uses the Android SDK; we test on a physical Android 8+ phone. AS is optional. |
| Where is 85%? | Training is in `ml/`; v1 smoke was 22%. App scaffold does not claim 85%. |
| Where is Blender? | Integration slot. Another person supplies `.glb`. |
| Why eight classes in the model? | Drive has no *Thalassia* images yet. Library still lists nine. |

## Next after this doc

1. Machine setup: `17-how-to-run-flutter.md`
2. Ask for a Cursor prompt that implements **only** this scaffold (no SVM port, no extra features)
3. Later: ML v2, then replace `StubClassifier`

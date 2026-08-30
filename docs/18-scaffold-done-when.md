# Flutter scaffold — done when

Use this as the acceptance list for the Cursor implementation prompt. Scope is **only** `16-flutter-audit-and-scaffold.md`.

## Must exist

- [ ] `app/` is a Flutter project (`pubspec.yaml`, `lib/`, `android/` with **minSdk 26**)
- [ ] Bottom nav: Identify, Library, About
- [ ] Library lists all **nine** slugs from `11-species.md`; *Thalassia* labeled as data coming
- [ ] Species profile shows the study fields; body text may be `TBD`
- [ ] Identify: camera + gallery via `image_picker`; preview image
- [ ] Identify calls `Classifier`; scaffold uses `StubClassifier` only
- [ ] Stub does **not** print a fake high-confidence species as if the SVM worked
- [ ] 3D screen is a placeholder (no crash if no `.glb`)
- [ ] Theme tokens in `lib/theme/tokens.dart`; screens use the tokens
- [ ] One concern per file; no 400-line `main.dart`
- [ ] `flutter analyze` clean (or only documented infos)
- [ ] README / `app/README.md` says: phone only, no emulator

## Must not exist in this pass

- [ ] No emulator config as the default device
- [ ] No Firebase / ML Kit / TFLite / YOLO
- [ ] No Blender pipeline
- [ ] No invented conservation science
- [ ] No second UI toolkit

## Verify (human)

1. `flutter devices` shows the physical phone.
2. `flutter run` from `app/` installs and opens MarineSee.
3. Tap through Identify (pick a photo) → stub message. Library → one species → 3D placeholder. About.
4. App stays usable in portrait on that phone. No horizontal overflow of text.

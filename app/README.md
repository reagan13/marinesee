# `app/` — MarineSee (Flutter)

**Toolkit:** Flutter → Android APK, **minSdk 26**.

Run on a **physical Android 8.0+ phone**. Do **not** use the Android emulator on the 7520U laptop.

Identify calls a laptop API (`python ml/src/serve_identify.py`), then:

```bat
adb reverse tcp:8765 tcp:8765
cd app
flutter pub get
flutter devices
flutter run
```

`flutter devices` must show the phone. If you only see `windows` / `chrome`, fix the USB cable or driver. Do not start an emulator.

Setup: [docs/17-how-to-run-flutter.md](../docs/17-how-to-run-flutter.md). You still need the Android SDK (adb + build tools) on the PC. You do not need emulator system images.

Spec:

- [docs/16-flutter-audit-and-scaffold.md](../docs/16-flutter-audit-and-scaffold.md)
- [docs/18-scaffold-done-when.md](../docs/18-scaffold-done-when.md)

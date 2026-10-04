# How to run the Flutter app (laptop-safe)

**IMPLEMENTATION** — for the Ryzen 5 7520U / ~16 GB machine. Goal: build an Android APK without the emulator.

Full scaffold spec: `16-flutter-audit-and-scaffold.md`.

## You need

1. **Windows 11** (already)
2. **Git**
3. **Flutter SDK** (stable) on PATH
4. **Android command-line tools + a platform-26+ SDK** (not the full Android Studio IDE if you can avoid it)
5. **A physical phone**: Android **8.0 (API 26)** or higher, USB cable, **Developer options → USB debugging** on
6. **Cursor** for editing

You do **not** need:

- Android Emulator
- Android Studio open every day
- A GPU for Flutter UI
- The seagrass image dataset on this PC

## 1. Install Flutter

1. Download the Windows stable SDK from [flutter.dev/install](https://docs.flutter.dev/get-started/install/windows).
2. Unzip to something like `C:\src\flutter` (not under `Program Files` or OneDrive if you can help it — OneDrive + Gradle is painful). This repo already lives in OneDrive; putting the **SDK** outside OneDrive is enough.
3. Add `C:\src\flutter\bin` to your user PATH.
4. New terminal:

```bat
flutter doctor
```

Install whatever `flutter doctor` marks `[X]` except the emulator.

## 2. Android SDK without living in Android Studio

Easiest path that still works:

1. Install **Android Studio** once (it is the supported way to get the SDK).
2. Open it **once**: SDK Manager → install **Android SDK Platform 34** (or current) **and API 26**, plus **Android SDK Command-line Tools**.
3. Do **not** install the Emulator system images.
4. Set `ANDROID_HOME` to the SDK path (usually `%LOCALAPPDATA%\Android\Sdk`).
5. **Quit Android Studio.** Daily work is Cursor + `flutter` CLI.

Accept licenses:

```bat
flutter doctor --android-licenses
```

## 3. Phone, not emulator

On the phone:

1. Settings → About → tap Build number 7 times.
2. Developer options → USB debugging.
3. Plug in USB. Allow the PC.

On the PC:

```bat
flutter devices
```

You should see the phone. If you only see `windows` / `chrome`, the cable or driver is wrong. Do not start an emulator to “just try.”

## 4. Run the app (after `app/` exists)

From repo root, or from `app/`:

Identify needs the SVM process on this PC (not inside Flutter):

```bat
cd ml\src
python serve_identify.py
```

USB phone (recommended):

```bat
adb reverse tcp:8765 tcp:8765
cd app
flutter pub get
flutter run
```

Same Wi-Fi instead of `adb reverse`:

```bat
flutter run --dart-define=IDENTIFY_API_URL=http://<laptop-lan-ip>:8765
```

First Gradle build can take several minutes and will spin the fans. That is once. Later runs are shorter.

Release APK (for testers, not Play Store):

```bat
cd app
flutter build apk --release
```

APK path: `app\build\app\outputs\flutter-apk\app-release.apk`.

## 5. Keep the machine alive

| Do | Don’t |
|----|--------|
| One `flutter run` + Cursor | Emulator + Android Studio + Colab + Chrome |
| Unplug / `q` in the Flutter CLI when done | Leave Gradle daemons + AS for hours |
| Close Chrome tabs if RAM hits 90% | Train SVM locally on this laptop |

If Windows feels stuck: Task Manager → end **qemu** / **emulator** if it ever appeared, and **Android Studio**.

## 6. `flutter doctor` checklist before you call setup done

- [ ] Flutter (stable)
- [ ] Windows toolchain (can stay unused)
- [ ] Android toolchain (SDK, licenses)
- [ ] Connected device = **your phone**, not `emulator-5554`
- [ ] VS Code / Cursor plugin optional

A red **Android Studio** line is OK if `flutter devices` shows the phone and `flutter run` installs.

## 7. OneDrive note

This repo is under OneDrive. If `flutter pub get` or Gradle randomly fails, pause OneDrive sync for `seagrass\app\` or move the clone. The Flutter **SDK** should not live in OneDrive.

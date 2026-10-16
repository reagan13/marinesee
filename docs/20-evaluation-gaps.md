# Evaluation gaps

**IMPLEMENTATION.** Read this before changing the MarineSee app. The user questionnaire is frozen at 29 statements in `MarineSee-Validation-Questions.txt`. Pass checks, statuses, and evidence live in `19-evaluation-question-spec.md`. This file is the open-work list so an app change does not skip a statement that is still `not-met` or `unmeasured`.

Snapshot copied from the spec (checked 9 Oct 2026, after the Cymodocea model): **5 met, 4 not-met, 20 unmeasured.**

A high user-evaluation score is not available while any row is `not-met` or `unmeasured`.

## How an agent uses this file

1. Before editing `app/` or the evaluation docs, read this file and `19-evaluation-question-spec.md`.
2. Restyle screens freely. Keep every behavior a statement requires. Do not drop camera, gallery, the nine-species library, a result with a name and a percent, the retake sentence, profile fields, or rotate/zoom.
3. In the same edit that changes what a tester can do, update that row’s **Status** and **Evidence** in `19-evaluation-question-spec.md`, then update the lists and the snapshot line in this file.
4. `met` means a tester on a physical Android phone can do the pass check now. Code that only looks ready stays `not-met` or `unmeasured`.
5. Do not invent species text to close FS-6. Use a cited source, or leave `TBD — adviser source`.
6. Do not add security or maintainability items to the user questionnaire.

## Already met — do not break

| ID | Keep this true |
|----|----------------|
| FS-1 | Identify offers Camera and Gallery, and the chosen photo is previewed. |
| FS-2 | The library lists the nine scientific names from `11-species.md`. |
| RE-3 | After onboarding, Scan and Library are both reachable. |
| RE-5 | The library is still there after the app is closed and opened again. |
| RE-6 | Leaving a profile and opening it again shows the same field text. |

## Not implemented (`not-met`)

These four statements fail in the current app. A visual redesign does not close them.

### Identification result a tester can finish

| ID | What is still missing |
|----|------------------------|
| FS-3 | After a successful identify, the tester must open that species’ profile **and** an interactive 3D view. Profile and 3D buttons exist only after the laptop API returns a slug. *Cymodocea rotundata* has a `.glb`. The other eight species still open a clip or a placeholder. |
| FS-4 | A finished identify must show the scientific name and a percent. `ApiClassifier` can do that only while `serve_identify.py` is up. Server down shows an error and no score. |
| FS-5 | A low-confidence result must tell the tester to take the photo again. The sentence is a notice in `result_screen.dart` and appears only on the low-confidence API path. |
| US-4 | Same blocker as FS-5. The retake sentence has not been shown to a tester as a clear instruction. |

Files: `app/lib/screens/result_screen.dart`, `app/lib/classify/api_classifier.dart`, `app/lib/screens/viewer_3d_screen.dart`, `app/lib/widgets/glb_viewer.dart`.

## Not shown on a phone (`unmeasured`)

These paths may already exist. They stay `unmeasured` until a tester does the pass check on a physical phone. Shipping a new layout does not mark them `met`.

| ID | What a phone pass still has to show |
|----|--------------------------------------|
| FS-6 | Each profile field shows cited text for common name, botanical characteristics, ecological role, conservation status, and habitat. The text is in `species.json`. A tester has not opened a profile on a phone. |
| FS-7 | Rotate and zoom *Cymodocea rotundata*. The meadow `.glb` and the viewer controls are in the app. Play loops the growth from the bud. A tester has not done that on a phone. |
| US-3 | Camera, gallery, library, and the *Cymodocea* rotate/zoom controls are in the app. A tester has not scored them on a phone. |
| PE-4 | Time rotate and zoom on a physical phone. The *Cymodocea* meadow model is bundled. Lag has not been timed. |
| US-1 | A first-time user can tell MarineSee identifies and teaches Mati seagrass. |
| US-2 | After one short brief, the tester identifies a photo and opens the library with no step-by-step guide. |
| US-5 | The tester agrees the text, colors, and layout are comfortable on a phone. |
| US-6 | Labels and buttons are large enough to read and tap. |
| PE-1 | Identify returns within about five seconds on a qualifying phone. |
| PE-2 | A profile opened from the library does not make the tester wait. |
| PE-3 | Library → profile → 3D completes without a long wait. |
| PE-5 | Opening several species in one session stays responsive. |
| RE-1 | One full identify plus a profile does not close the app. |
| RE-2 | A second photo after the first result does not crash the app. |
| RE-4 | A failed identify stays in the app and can be tried again. `result_screen.dart` has **Try again**, which returns to Identify. That control has not been shown on a phone. |
| CO-1 | Identify and library both work while other apps stay installed. |
| CO-2 | MarineSee opens without uninstalling other apps. |
| PO-1 | Identify, library, and profile are usable on two different Android screen sizes. |
| PO-2 | The installed app opens on Android 8.0 or newer. `minSdk` is 26. No install is recorded here. |
| PO-3 | A second qualifying phone installs and opens the APK with no extra toolchain. |

## Counts

When a status changes, replace the snapshot line at the top of this file and the snapshot line in `19-evaluation-question-spec.md` in the same edit. Recount `met`, `not-met`, and `unmeasured`. The total stays 29.

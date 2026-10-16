# Evaluation question spec

**IMPLEMENTATION.** These 29 statements are the user questionnaire in `MarineSee-Validation-Questions.txt`. A high score means a tester on a qualifying Android phone can do the pass check and would agree. Do not tell the team a question will score high while its status is `not-met` or `unmeasured`.

Checked against the app on 9 Oct 2026, after the Cymodocea model was added: **5 met, 4 not-met, 20 unmeasured.** The open rows are listed for agents in `20-evaluation-gaps.md`. Read that file before changing the app.

## How to mark a row

| Status | Meaning |
|--------|---------|
| `met` | A tester can do the pass check on the installed app now. |
| `not-met` | The app contradicts the statement, or the pass check cannot be done. |
| `unmeasured` | The path may exist, but it has not been shown on a physical phone. |

When a change affects a row, update **Status** and **Evidence** in the same change. Evidence is the file plus what the tester sees. Do not mark `met` from a code comment alone.

Rotate/zoom of a supplied `.glb` is app integration. It does not require authoring a `.blend` file.

## Functional suitability

| ID | Statement | Pass check | Status | Evidence |
|----|-----------|------------|--------|----------|
| FS-1 | Camera or a saved photo | Identify offers Camera and Gallery, and the chosen photo is previewed. | met | `app/lib/screens/identify_screen.dart` |
| FS-2 | Library of the nine Mati species | Library lists the nine scientific names from `11-species.md`. | met | `app/assets/data/species.json` |
| FS-3 | Result opens that species’ profile and 3D view | After a successful identify, both buttons open the matching species. | not-met | Open species profile and Open 3D render only after the API returns a slug. *Cymodocea rotundata* has a bundled `.glb`. The other eight species still open a clip or a placeholder. |
| FS-4 | Species name and confidence score | A finished identify shows the scientific name and a percent. | not-met | `ApiClassifier` can show both. With the server down, the tester sees an error and no score. |
| FS-5 | Uncertain result asks for a new photo | A low-confidence result shows the retake sentence. | not-met | The retake sentence is a notice on `result_screen.dart`. It appears only on the low-confidence API path. |
| FS-6 | Profile shows the study fields | Each field shows real text: common name, botanical characteristics, ecological role, conservation status, habitat. | unmeasured | Cited text is in `app/assets/data/species.json` and the profile reads it. A tester has not opened a profile on a physical phone. |
| FS-7 | Rotate and zoom the 3D model | The tester can rotate and zoom at least one species model. | unmeasured | `app/assets/models-3d/cymodocea_rotundata.glb` is the *Cymodocea rotundata* meadow. `glb_viewer.dart` has drag, Rotate, Zoom in, and Zoom out, and Play starts the growth at time 0 and loops. A tester has not rotated or zoomed it on a physical phone. |

## Usability

| ID | Statement | Pass check | Status | Evidence |
|----|-----------|------------|--------|----------|
| US-1 | Easy to see what MarineSee is for | A first-time user can tell it identifies and teaches Mati seagrass. | unmeasured | Onboarding, Home, and Profile say MarineSee identifies and teaches Mati seagrass. No tester has scored it. |
| US-2 | Identify and library after a short explanation | After one short brief, the tester finishes both tasks with no step-by-step guide. | unmeasured | Not run with a tester. |
| US-3 | Camera, upload, library, and 3D controls are easy | All four controls work and are obvious on a phone. | unmeasured | Camera, gallery, and library work. Rotate and zoom are on the *Cymodocea rotundata* viewer. A tester has not scored them on a phone. |
| US-4 | Retake message is clear | The tester understands they should take the photo again. | not-met | Same blocker as FS-5. |
| US-5 | Text, colors, and layout are comfortable | Tester agrees the phone screens are readable. | unmeasured | Not scored on a phone. |
| US-6 | Labels and buttons are large enough | Tester can read and tap them without difficulty. | unmeasured | Not scored on a phone. |

## Performance efficiency

| ID | Statement | Pass check | Status | Evidence |
|----|-----------|------------|--------|----------|
| PE-1 | Result within about five seconds | On a qualifying phone, identify returns in about five seconds. | unmeasured | No timed phone run. |
| PE-2 | Profile opens without a long wait | Opening a species from the library feels immediate. | unmeasured | Profile is bundled JSON. Not timed. |
| PE-3 | Library to profile to 3D does not take long | That path completes without a long wait. | unmeasured | Not timed. |
| PE-4 | Rotate and zoom without freezing | The 3D gesture stays smooth on a qualifying phone. | unmeasured | `cymodocea_rotundata.glb` is the meadow model. Lag has not been timed on a physical phone. |
| PE-5 | Several species in one session do not lag | Browsing several species stays responsive. | unmeasured | Not tried as a timed session. |

## Reliability

| ID | Statement | Pass check | Status | Evidence |
|----|-----------|------------|--------|----------|
| RE-1 | Identify and open a profile without crashing | One full identify plus profile does not close the app. | unmeasured | Not run on a phone. |
| RE-2 | A second photo does not crash the app | Identify again after the first result. The app stays open. | unmeasured | Not run on a phone. |
| RE-3 | Library and identify are available on open | After onboarding, both are reachable. | met | After onboarding, Scan and Library are tabs in `app/lib/screens/shell.dart`. |
| RE-4 | A failed identify can be tried again | The app stays open and the tester can submit another photo. | unmeasured | `result_screen.dart` shows Try again, which returns to Identify. Not shown on a phone. |
| RE-5 | Library remains after close and reopen | Force-close, open again, library is still there. | met | Library is the bundled asset. |
| RE-6 | Leaving a profile and reopening shows the same text | The same field text is still there. | met | Same bundled asset. The text may still be `TBD`. |

## Compatibility

| ID | Statement | Pass check | Status | Evidence |
|----|-----------|------------|--------|----------|
| CO-1 | Identify and library work while other apps stay installed | Do both tasks with other apps still installed. | unmeasured | Not shown on a phone. |
| CO-2 | No need to uninstall other apps first | MarineSee opens without removing other apps. | unmeasured | Not shown on a phone. |

## Portability

| ID | Statement | Pass check | Status | Evidence |
|----|-----------|------------|--------|----------|
| PO-1 | Screens stay usable on different phone sizes | Identify, library, and profile are usable on two different Android screen sizes. | unmeasured | Not checked on two phones. |
| PO-2 | Runs on Android 8.0 or newer | The installed app opens on a phone at or above Android 8.0. | unmeasured | `minSdk` is 26. No install has been recorded here. |
| PO-3 | Installs on a second qualifying phone without extra tools | A second phone installs and opens the APK with no extra toolchain. | unmeasured | Not done. |

## What this spec does not add

Security and maintainability stay off the user form. They are not in the 29 statements. Do not add account, source-code, or “feels well tested” questions to raise the count.

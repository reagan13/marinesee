# Evaluation (ISO/IEC 25010)

**STUDY:** students, tourists, researchers, and coastal community members fill a user evaluation and use the app. Results judge whether MarineSee supports interactive seagrass education and visualization.

The paper names characteristics but does not attach the questionnaire items. This file keeps development evaluable.

## Who evaluates

**STUDY:** students, tourists, local researchers, coastal community members.

Consent and withdrawal are research ethics, not app features.

## Characteristics named in the objectives

| Characteristic | What testers should try |
|----------------|-------------------------|
| Functional suitability | Identify a photo, open the matching profile, rotate/zoom the 3D model, browse all nine species |
| Usability | Complete identify + library without a facilitator after a short brief |
| Performance efficiency | Identification returns within about five seconds; 3D stays usable on a qualifying phone |
| Reliability | Repeat identify on the same photo; app does not lose the library |
| Compatibility | Same flows on more than one Android device / screen size (Android 8.0+ floor) |
| Portability | Install the APK on a second qualifying device without extra tools |

Security and maintainability appear in the NFRs. They can appear on a developer/adviser checklist even if the user form stays with the six characteristics above.

## Acceptance ideas (not official SLAs)

**IMPLEMENTATION** suggestions for a test script:

1. Tester can open the library and see exactly nine species.
2. Each profile shows the study-required fields.
3. Tester can rotate and zoom at least one 3D model.
4. Tester can capture or upload a photo and receive a species name plus a confidence score.
5. A low-confidence case shows a retake message (once the threshold is set).
6. Identify finishes within five seconds on a qualifying device and network.
7. An administrator can edit a species paragraph and the visitor sees the new text (if remote content is used).
8. Held-out SVM test accuracy is documented at ≥ 85%.

## What evaluation is not

- Not a claim that the model works on every photo on every beach
- Not underwater video or drone survey accuracy
- Not iOS certification
- Not a biodiversity monitoring program for the LGU

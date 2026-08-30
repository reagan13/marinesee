# Scope and Limitations

**STUDY** — Chapter 1.5. This is the fence around the product.

## System start line

The product starts when a user opens the Android app to **learn** a species or **identify** a seagrass photo. Training the SVM is part of the study, not part of the end-user app.

Field collection of the dataset happens **before** the model is shipped. Users do not label training data in v1 unless we later add an admin tool.

## In scope

### Locale and taxa

- Only the **nine** documented seagrass species of Mati City (see `11-species.md`)
- Educational distribution notes for Lawigan, Taitaidaga, Manguihay, and Pujada Bay — reference only, not a map product

### Product features

- Android mobile application
- Capture or upload a seagrass image
- SVM identification from color, texture, and shape features
- Confidence score; prompt to retake when confidence is low
- Interactive 3D models: rotate, zoom, inspect
- Digital library of localized species profiles
- Educational / conservation copy
- Admin management of educational content and species records
- Database storage and retrieval of species information

### Training (study, not a user-facing screen)

- Collect leaf/canopy images from the named Mati sites
- Resize, balance, augment, label
- Extract features, train SVM, evaluate on 70/15/15 split
- Target: **≥ 85%** identification accuracy

### Evaluation

- ISO/IEC 25010 user evaluation with the named user groups

## Out of scope (hard limits)

**STUDY** — Chapter 1.5.

| Limit | Meaning for the build |
|-------|------------------------|
| Only nine species | No algae, corals, seaweeds, or seagrass from other regions |
| 3D fidelity | Models are only as good as reference photos/illustrations; no claim of microscopic accuracy |
| No GIS | No live GPS tracking, navigation, or scientific mapping |
| Education, not field science | No water quality, population density, or habitat-degradation sensors |
| No VR / AR | Standard 3D viewer only |
| English only | No Filipino or Bisaya in v1 |
| Android-first | Do not promise iOS or old-phone parity |
| Device floor | Android 8.0+, 3 GB RAM, 32 GB storage, octa-core-class CPU, ≥ 720 × 1600 |

**CONFLICT resolved in `00-study-review.md`:** the limitation sentence that says the system “does not perform automated species recognition” is ignored. SVM identification stays in scope.

## Internet

**STUDY:** the app needs an active internet connection to load 3D assets, educational content, and other resources.

Do not advertise a fully offline field guide until architecture says the models and library are bundled on device.

## Minimum device (repeat for testers)

For acceptable 3D performance the paper requires:

- Android 8.0 (Oreo) or higher
- 3 GB RAM
- 32 GB internal storage
- Octa-core or equivalent
- Recommended screen **720 × 1600**

Older phones may load slowly or render poorly. That is an accepted limitation, not a bug we must fully fix.

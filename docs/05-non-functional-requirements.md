# Non-Functional Requirements

**STUDY** — Chapter 3, Non-Functional Requirements, plus Chapter 1.5 device limits and the 85% accuracy objective.

IDs are **IMPLEMENTATION** labels.

## NFR-1 Performance

- Identification request finishes within **five seconds** under normal conditions.
- 3D rendering stays smooth enough to rotate/zoom on a device that meets the minimum spec.
- Educational content and species pages load quickly on a normal mobile connection.

## NFR-2 Reliability

- SVM identification accuracy **≥ 85%** on the held-out test set (study objective 4).
- App remains usable during normal use.
- Regular backups to prevent data loss.

**OPEN:** what is backed up (Firebase? MySQL dump? Drive copies of models?) and how often.

## NFR-3 Usability

- Interface is usable by students, tourists, researchers, and coastal community members without a marine-biology background.
- Instructions for capture and 3D controls are visible on first use.
- Acceptable usability rating in the ISO 25010 evaluation.

## NFR-4 Compatibility

- Android phones at different common screen sizes and resolutions.
- Functions on commonly used Android versions, with the paper’s floor at **Android 8.0**.

iOS is not a v1 requirement.

## NFR-5 Security

- Protect uploaded images and user information from unauthorized access.
- Role-based access for administrators vs visitors.
- Species and user data stored securely in the database.

**OPEN:** whether visitors have accounts at all. If the library is public and identify is guest-allowed, “user information” may be thin.

## NFR-6 Scalability

- Can add more educational text and (later) species records without a rewrite.
- More users should not require a redesign of the app. The nine-species cap still applies for v1 classification.

## NFR-7 Maintainability

- Educational content and species records can be updated without rebuilding the whole app if the content store allows it.
- Training code stays separate from UI code (`ml/` vs `app/`).

## NFR-8 Portability (evaluation characteristic)

The study evaluates portability. For this product that means: install and run on more than one qualifying Android device, not “runs on every OS.”

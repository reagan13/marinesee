# Modules and Business Logic

**STUDY** — IPO processes + functional requirements. Module names are **IMPLEMENTATION**.

## M1 Identify

1. User captures or picks an image.
2. App (or API) resizes and enhances using the **same** contract as training.
3. Extract color, texture, and shape features.
4. SVM returns a class among the nine species plus a decision-function / probability-style **confidence**.
5. If confidence < threshold → show “retake” copy. Still **OPEN** whether we also show the top guess.
6. If confidence ≥ threshold → show species result and offer 3D + profile.

Do not invent extra classes (`unknown`, `not seagrass`) unless the team adds them to the study. The paper’s SVM always outputs one of the nine.

**OPEN:** reject obviously non-seagrass images. The paper does not specify an out-of-domain detector.

## M2 Digital library

- List all nine species.
- Open a profile (fields in `11-species.md`).
- From a profile, open that species’ 3D model.

Content is localized to Mati. Do not paste generic global seagrass pages that name species we do not support.

## M3 3D visualization (integration only)

**IMPLEMENTATION (30 Aug 2026):** This repo’s owner builds the **mobile app + SVM identify**. We do **not** author Blender scenes. The study still has a 3D / growth viewer; that is a **slot** in the app.

- Teammate (or later drop) supplies a `.glb` (preferred, clip `growth`) or an `.mp4` per species.
- The app **loads and plays** the file: rotate / zoom if GLB, play/pause if video.
- Until a file exists, the species screen shows a placeholder (“3D model coming”).
- No Blender install, no `.blend` editing, no modeling tasks in this repo.
- No VR / AR, no live simulation.

## M4 Education / conservation

Short copy about why seagrass meadows matter (habitat, sediment, nursery). This is not a second encyclopedia. Keep it next to the species that the user is looking at.

## M5 Admin content

Administrators update profile text (and later assets). Ordinary visitors never see edit chrome.

## Current vs proposed flow (from the paper)

**Current (manual):** user compares books/photos → guesses → asks an expert.

**Proposed:** photo → SVM → name + confidence → 3D + profile in the same app.

Do not add expert-chat or live GIS to “complete” that story. Out of scope.

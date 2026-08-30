# Study Review

Source: `docs/source/FINAL-CAPSTONE-BRUH-2.docx` (proposal text extracted August 2026). Last modified in Word by Daniel Calibara. Authors are not listed in the body.

The paper is enough to know **what** to build and **what not** to build. It is not enough to start coding without extra decisions. This file is the honest check.

## What the paper is

A BSIT capstone **proposal** for **MarineSee**: an Android educational app that helps students, tourists, researchers, and coastal communities in Mati City identify and learn the nine documented local seagrass species using:

1. SVM-based image recognition (color, texture, shape features)
2. Interactive 3D models (rotate / zoom / inspect)
3. A localized digital library of species profiles

It uses the **Waterfall** SDLC. Evaluation is **ISO/IEC 25010** user testing.

It is **not** a finished thesis with a working app, ERD, trained model, filled-in dataset size, or confirmed 3D assets.

## What is solid enough to implement against

These parts are consistent enough to treat as product requirements:

- Problem: people in Mati cannot easily tell seagrass species apart; printed guides and 2D photos are weak for beginners
- Locale: Mati City coastal waters — Lawigan, Taitaidaga, Manguihay, Pujada Island / Pujada Bay
- Exactly **nine** species (see `11-species.md`)
- Mobile Android app, not a desktop or web-first product
- Three product cores: identify from a photo, inspect a 3D model, read a species profile
- SVM (not CNN) with hand-crafted features; target accuracy **≥ 85%**
- Dataset split **70 / 15 / 15** (train / validation / test)
- Preprocess: resize, imbalance check, augment (flip / rotate / zoom), label by species folder
- Features: color histograms, GLCM texture, contour / blade shape
- Identification UX: show species + profile + **confidence score**; recommend retake when confidence is low
- Admin can manage educational content
- Internet is required to load 3D assets and educational content
- Minimum device: Android 8.0, 3 GB RAM, 32 GB storage, octa-core-class CPU, 720 × 1600
- English only
- No GPS / GIS / VR / AR / water-quality sensors / other marine taxa
- Method: Waterfall (requirements → design → implementation → testing → deployment → maintenance)
- Named tools in feasibility: Android Studio, Blender, Firebase/MySQL

## What the paper is missing for implementation

Chapter 3.3 is titled System Design but only promises diagrams. The extracted paper does **not** include:

- A written architecture or deployment diagram (figures are images only)
- A chosen mobile UI toolkit (Compose vs XML vs Flutter — only “Android Studio”)
- A decided backend: it says **Firebase/MySQL** as if they were interchangeable
- Entity-relationship diagram or data dictionary
- Use-case or sequence text (BPMN is a figure only)
- Screen inventory or field lists for species profiles
- Exact image size for resize
- Dataset size — the text still says `[INSERT NUMBER]`
- Per-species image counts and the Drive folder layout
- SVM kernel, C, gamma, or class-weight policy
- How inference runs on the phone (on-device vs API)
- 3D model format, polygon budget, or who builds the Blender files
- Auth flow for ordinary users (login required or guest-first?)
- Confidence threshold for “retake the photo”
- Backup procedure named in NFRs
- Test cases

Those gaps are why this `docs/` folder exists.

## Conflicts inside the paper

Resolve these before treating a sentence as a coding rule.

### 1. Automated recognition is both required and forbidden — CONFLICT

The whole study is an SVM identification system. Specific objective 1 and 4, the functional requirements, and Chapter 2 all require photo identification.

Chapter 1.5 Limitations also says:

> The system does not perform automated species recognition, underwater scanning, or real-time environmental monitoring.

That sentence is leftover from a 3D-only draft. **Underwater scanning** and **real-time environmental monitoring** stay out of scope.

**Implementation default:** automated **SVM photo identification is in scope.** It is a graded objective (85% accuracy). Do not drop it because of that one limitation sentence.

### 2. Product title wording — CONFLICT

The paper uses two titles:

- *Mobile-Based Seagrass Educational and Interactive 3D Visualization System for Mati City*
- *Mobile-Based Seagrass Species Identification System for Mati City Using Image Recognition and Interactive 3D Visualization*

**Implementation default:** use the second (identification + 3D). Short name: **MarineSee**. Repo folder: `seagrass`.

### 3. Internet vs on-device recognition — CONFLICT

Scope says the app **requires an active internet connection** for 3D assets and content. Chapter 2 praises Seek by iNaturalist for **offline** on-device CNN inference, then says MarineSee is different because it is localized SVM — not because it is online-only.

**Implementation default:** content and 3D models may load from the network. Identification **may** be on-device or via a small API. Pick one in `06-architecture.md` once the team confirms. Do not promise offline field use until that decision is made.

### 4. Waterfall phase table is mislabeled — CONFLICT

Table 3.1 puts “system architecture, UI/UX, database, SVM and 3D design” under **Implementation** (October–November) and puts “functional and non-functional requirements” under **Design**. That is the Waterfall phases in the wrong buckets.

**Implementation default:** treat Table 3.1 as a calendar, not a definition of the phases. Requirements live in this folder. Design is architecture + UI + ML spec. Implementation is app + training code.

### 5. WBS figure description contradicts itself — CONFLICT

The WBS paragraph first says Figure 10 is the development work breakdown, then says Figure 9 (also referenced as the WBS) is the **current manual** identification process. Figure 9 is separately the ML pipeline.

**Implementation default:** ignore the mixed figure numbers. Use `08-modules-and-business-logic.md` for the product flow and `09-ml-pipeline.md` for training.

### 6. Tense — CONFLICT

Requirements Analysis / System Design are written as future work. Implementation / Testing / Deployment are written as already done. There is no app in this folder yet.

**Implementation default:** treat the paper as a **proposal**. Nothing is built until this repo has working modules.

### 7. Nine species vs eight on Drive — CONFLICT

The study locks nine classes, including *Thalassia hemprichii*. The shared Drive folder has **zero** Thalassia images (inventory 30 Aug 2026).

**Implementation default (v1):** train the eight classes that exist. Keep Thalassia in docs and the app library. Do not rewrite the paper to “eight species.” Add the ninth class when images exist.

### 8. Firebase vs MySQL — CONFLICT

Technical feasibility lists **Firebase/MySQL** as one line. Those are different products.

**Implementation default:** undecided. See `14-open-questions.md`. Do not create both.

## What we will not silently change

- Do not add iOS as a v1 target (limitation: Android-focused)
- Do not add VR/AR, GPS tracking, or GIS
- Do not add Filipino/Bisaya translations in v1
- Do not expand past the nine species
- Do not replace SVM with CNN/YOLO to “get higher accuracy” without changing the study
- Do not turn this into a monitoring or population-density science tool

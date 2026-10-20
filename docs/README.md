# MarineSee Documentation

Implementation documentation for **MarineSee** — a mobile-based seagrass educational and identification system for Mati City, Davao Oriental.

These files are the working spec. They are extracted from the capstone paper *MarineSee: A Mobile-Based Seagrass Species Identification System for Mati City Using Image Recognition and Interactive 3D Visualization* (`docs/source/FINAL-CAPSTONE-BRUH-2.docx`), then organized so we can build the app and the training pipeline without treating the paper as a complete technical specification.

The paper is enough to know **what** to build. It is not enough to start coding without extra decisions. This folder records:

- what the study already decided
- what we will implement
- what is still open and must be confirmed before we invent it

## How to use this folder

Read in this order before writing code:

1. `00-study-review.md` — what is solid vs incomplete in the paper
2. `01-purpose-and-objectives.md`
3. `02-scope-and-limitations.md`
4. `03-conceptual-framework.md`
5. `04-functional-requirements.md`
6. `05-non-functional-requirements.md`
7. `06-architecture.md`
8. `09-ml-pipeline.md`
9. `12-colab-and-training.md`
10. `16-flutter-audit-and-scaffold.md` — before any `app/` code
11. `17-how-to-run-flutter.md` — SDK + phone, no emulator
12. `19-evaluation-question-spec.md` and `20-evaluation-gaps.md` — before any `app/` change. The questionnaire is 29 frozen statements. Do not restyle the app in a way that drops a `not-met` or `unmeasured` behavior.

Then use the rest as needed per module.

## Document index

| File | What it covers |
|------|----------------|
| [00-study-review.md](00-study-review.md) | Review of the paper: strengths, gaps, contradictions |
| [01-purpose-and-objectives.md](01-purpose-and-objectives.md) | Why MarineSee exists and what success means |
| [02-scope-and-limitations.md](02-scope-and-limitations.md) | In scope, out of scope, and hard limits |
| [03-conceptual-framework.md](03-conceptual-framework.md) | IPO framework and how it maps to modules |
| [04-functional-requirements.md](04-functional-requirements.md) | What the app must do |
| [05-non-functional-requirements.md](05-non-functional-requirements.md) | Quality attributes from the study + ISO 25010 |
| [06-architecture.md](06-architecture.md) | Monorepo, mobile app, training, Colab, Drive |
| [07-roles-and-permissions.md](07-roles-and-permissions.md) | End users vs administrators |
| [08-modules-and-business-logic.md](08-modules-and-business-logic.md) | Identify, 3D, library, admin |
| [09-ml-pipeline.md](09-ml-pipeline.md) | Dataset, features, SVM, 85% target |
| [10-domain-model.md](10-domain-model.md) | Entities we will persist |
| [11-species.md](11-species.md) | The nine Mati City species and profile fields |
| [12-colab-and-training.md](12-colab-and-training.md) | How Cursor, this repo, Colab, and Google Drive fit |
| [13-evaluation-iso25010.md](13-evaluation-iso25010.md) | How the study will evaluate the system |
| [19-evaluation-question-spec.md](19-evaluation-question-spec.md) | The 29 user questions, the pass check for each, and whether the app meets it |
| [20-evaluation-gaps.md](20-evaluation-gaps.md) | Open evaluation work: 8 `not-met`, 16 `unmeasured`. Read before changing the app |
| [21-3d-species-model-spec.md](21-3d-species-model-spec.md) | Contract for every species 3D model: solid geometry, rig and growth, phone `.glb`, reef pitch clip, per-species briefs |
| [14-open-questions.md](14-open-questions.md) | Decisions still required |
| [15-implementation-roadmap.md](15-implementation-roadmap.md) | Suggested build order |
| [16-flutter-audit-and-scaffold.md](16-flutter-audit-and-scaffold.md) | Flutter lock, audit, scaffold spec |
| [17-how-to-run-flutter.md](17-how-to-run-flutter.md) | Laptop-safe Flutter + physical phone |
| [18-scaffold-done-when.md](18-scaffold-done-when.md) | Acceptance list for the scaffold prompt |
| [glossary.md](glossary.md) | Study terms used in code and docs |

## Source-of-truth rules

1. **Objectives, purpose, scope, and limitations** come from the study. Do not expand them silently.
2. **The classifier is SVM.** The paper chose SVM over CNN/ANN because of a small localized dataset and mobile constraints. Do not switch to YOLO, CNN, or another model unless the paper and this folder are updated first.
3. **Architecture and folder layout** come from this folder (`06-architecture.md`), not from the paper. The paper names Android Studio, Blender, and Firebase/MySQL but never specifies a repo shape or a Colab workflow.
4. **Business or science rules the paper did not define** (exact feature vector, kernel, image size, dataset count, 3D asset source) stay marked `OPEN` until the team confirms them.
5. When two sentences in the paper disagree, this folder records the conflict and the implementation default. See `00-study-review.md` and `14-open-questions.md`.

## Labels used in these docs

| Label | Meaning |
|-------|---------|
| **STUDY** | Stated in the capstone paper. Treat as a requirement. |
| **IMPLEMENTATION** | Engineering decision for this repo. Not from the paper. |
| **OPEN** | Must be confirmed. Do not invent a marine-science or panel rule. |
| **CONFLICT** | The paper says two different things. We picked a default. |

# Conceptual Framework

**STUDY** — Chapter 1.6. The paper uses an **Input–Process–Output (IPO)** model.

The figure in the paper is an image only. This file writes the same model in a form we can implement.

## IPO overview

```text
INPUT                              PROCESS                         OUTPUT
─────                              ───────                         ──────
Seagrass photos (camera / upload)  →  Image preprocessing      →  Identified species
Preloaded 9-species image dataset  →  SVM feature extract      →  Confidence score
Educational reference text         →  SVM classification       →  Interactive 3D model
3D model assets                    →  3D visualization         →  Species profile
                                   →  Library retrieval
```

Feedback loop **STUDY**: maintenance may refine the SVM as more images are collected and update library text.

## Inputs (what enters the system)

| Input | Examples | Notes |
|-------|----------|--------|
| User photo | Camera capture or gallery upload | End-user identify flow |
| Training dataset | Labeled images of the nine species from Mati sites | Lives on Google Drive; not in git |
| Educational reference data | Scientific name, common name, botany, ecology, conservation, habitat | Digital library |
| 3D assets | Blender-authored models per species | Loaded by the viewer |

## Processes (what the software does)

| Paper process | Implementation module | Doc |
|---------------|----------------------|-----|
| Image pre-processing | Resize, clean, enhance (train + infer) | `09-ml-pipeline.md` |
| SVM feature extraction and classification | Color / texture / shape → SVM → class + score | `09-ml-pipeline.md` |
| 3D visualization | Retrieve model, rotate / zoom / inspect | `08-modules-and-business-logic.md` |
| Educational information retrieval | Load species profile from library | `11-species.md` |

## Outputs (what users get)

| Output | Product surface |
|--------|-----------------|
| Identified species | Result screen after capture/upload |
| Interactive 3D model | 3D viewer for that species |
| Educational profile | Library page and post-identify panel |

## How IPO should appear in code

- Training code lives under `ml/` and runs on **Google Colab** against Drive-mounted images.
- The mobile app under `app/` performs (or calls) preprocess → classify → show result.
- Profile text and 3D files are data, not hard-coded in random widgets. See `10-domain-model.md`.

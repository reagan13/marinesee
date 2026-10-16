# ML Pipeline (SVM)

**STUDY** — Chapter 2 (algorithm choice), Chapter 3 Model Building, specific objective 4.

The classifier is a **Support Vector Machine** on **extracted features**. It is not a CNN and not YOLO.

## Why SVM (do not reopen casually)

The paper’s Table 1 argument:

| Model | Why the study rejected or kept it |
|-------|-----------------------------------|
| SVM | Works on small/medium sets; low compute; no GPU required; selected |
| ANN | Needs more labeled data; heavier |
| CNN | Highest published accuracy only with large data + GPU; overfitting risk on this set |

MarineSee’s dataset is **localized and self-collected**. That is the reason for SVM. Colab having a GPU does **not** change the study choice. Use the GPU for resize/augment if useful; still train SVM.

## Dataset

**STUDY:**

- Collected at Lawigan, Taitaidaga, Manguihay, and Pujada Bay
- Leaf and canopy images
- Nine species folders as ground truth
- Split **70% / 15% / 15%** train / validation / test
- Imbalance expected; augment under-represented classes
- Augment: random flip, rotation, zoom
- Total image count in the paper is still `[INSERT NUMBER]`

**IMPLEMENTATION:** images live on **Google Drive**, not in git. Counts: `ml/artifacts/inventory.md`. v1 trains **eight** classes (`TRAINABLE_SPECIES`) from the **`all`** folders. *Thalassia hemprichii* is held out until a dataset folder exists. Resize **256×256**. Split seed **42**. Local preprocess export: `python ml/src/export_processed.py` → `data/processed/v1` + `ml/artifacts/preprocess_v1.md`.

**OPEN:** *Thalassia* source; final image size.

## Preprocess

Order from Figure 9 / Chapter 3:

1. Select images that actually show leaf shape, blade width, color
2. Resize to one fixed size (**OPEN:** e.g. 256×256)
3. Check class counts; augment minority classes
4. Label via species folders

At inference, apply the **same resize and color assumptions**. Do not augment user photos.

## Feature extraction

**STUDY** names:

| Family | Paper wording | Typical implementation (IMPLEMENTATION until locked) |
|--------|---------------|------------------------------------------------------|
| Color | Color histograms | HSV histogram of the frame and of plant-mask pixels, plus plant HSV mean / spread |
| Texture | GLCM | 128px gray, distances 1/2/4, six properties averaged over four angles plus their spread |
| Shape | Contour and blade characteristics | Plant-mask blobs plus skeleton blade width — **OPEN** exact list |

The SVM sees a **feature vector**, not raw pixels. **IMPLEMENTATION:** `ml/src/features.py` v2 (148 numbers) on the output of `preprocess.prepare_rgb` (green-mask plant crop, then 256px). `identify.py` calls the same two functions on a user photo. The locked SVM is RBF `C=3`, `gamma=0.01`, chosen by validation macro F1 on 13 Oct 2026. Exact list stays **OPEN** for the paper.

## Train and evaluate

- Train on the 70% split.
- Tune on 15% validation. **IMPLEMENTATION:** `ml/src/tune_svm.py` fits RBF (C × gamma) and linear (C) settings with `class_weight="balanced"` on train, picks the highest validation macro F1, and never reads the test split. Notebook 02 plots train against validation macro F1 across C in place of a loss curve (an SVM has no epochs). Final grid values stay **OPEN** for the paper.
- Report accuracy (and preferably per-class precision/recall) on 15% test.
- Success line for the study: **≥ 85%** test accuracy.

Also log: confusion matrix, support per class, seed, library versions. The panel will ask.

## Export

Save, next to the model:

- label map (`0` … `8` → scientific name)
- feature-vector schema / extractor version
- metrics JSON
- git commit hash of `ml/` if cloned in Colab

Suggested filenames under `ml/artifacts/` (no images):

```text
svm_seagrass.joblib
label_map.json
feature_spec.json
metrics.json
```

## What Colab is for

See `12-colab-and-training.md`. Short version: Colab runs this pipeline against Drive. This repo stores the code.

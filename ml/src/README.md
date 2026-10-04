# `ml/src`

Shared Python for Colab and later inference.

| Module | Job |
|--------|-----|
| `dataset_contract.py` | Nine study slugs, eight trainable slugs, Drive-title matching |
| `inventory.py` | Count images under a mounted Drive root |
| `preprocess.py` | List `all` folders, QC, resize 256, augment minority train |
| `leaf_focus.py` | Green-mask diagnostic + optional plant crop |
| `export_processed.py` | Write `data/processed/v1` + `ml/artifacts/preprocess_v1.*` |
| `features.py` | HSV hist + GLCM + shape vector |
| `split.py` | Stratified 70/15/15 |
| `train_svm.py` | Scaler + RBF SVM, export joblib/metrics |
| `identify.py` | Load v1 joblib, score one photo (same 256 + features as Colab) |
| `serve_identify.py` | LAN `POST /api/v1/identify` for the Flutter app |

Notebooks should import these when the repo is cloned. `01_dataset_inventory.ipynb` also inlines the same rules so a lone Colab upload still runs.

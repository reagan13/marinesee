# `ml/src`

Shared Python for Colab and later inference.

| Module | Job |
|--------|-----|
| `dataset_contract.py` | Nine study slugs, eight trainable slugs, Drive-title matching |
| `inventory.py` | Count images under a mounted Drive root |
| `preprocess.py` | List `all` folders, resize 256, augment minority train |
| `features.py` | HSV hist + GLCM + shape vector |
| `split.py` | Stratified 70/15/15 |
| `train_svm.py` | Scaler + RBF SVM, export joblib/metrics |

Notebooks should import these when the repo is cloned. `01_dataset_inventory.ipynb` also inlines the same rules so a lone Colab upload still runs.

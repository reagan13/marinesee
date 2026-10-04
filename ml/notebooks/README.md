# Notebooks

1. `01_dataset_inventory.ipynb` — mount Drive, count folders (done 30 Aug 2026).
2. `02_svm_v1_eight_class.ipynb` — preprocess + features + SVM on the **eight** classes that exist (`all` folders).
3. `03_preprocess_v1.ipynb` — QC + 256px export only (no SVM). Same job as `python ml/src/export_processed.py`.

## Run inventory in Colab

The dataset is [Shared with me / Seagrass](https://drive.google.com/drive/folders/1MU31a5BG3MKn1fEYV-ljhc2zS4CoE79F). Colab cannot see Shared-with-me until you add a shortcut.

1. In Drive: right-click **Seagrass** → Organize → Add shortcut → **My Drive**.
2. Open [Google Colab](https://colab.research.google.com) → Upload `01_dataset_inventory.ipynb`  
   **or** in Cursor: open the notebook → Kernel → **Colab** (same as the yolo ExDark notebook).
3. Run top to bottom. CPU is enough.
4. Download `inventory.json` into `ml/artifacts/` when the counts look right.

Do not train YOLO on this dataset. MarineSee’s paper requires SVM.

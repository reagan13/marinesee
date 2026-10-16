# `ml/` — SVM training

Code for preprocess, feature extraction, train, and eval. Local machine uses the repo-root `.venv` (Python 3.12, CPU). Colab remains the path when the photos stay on Drive.

- Pipeline rules: `../docs/09-ml-pipeline.md`
- Colab workflow: `../docs/12-colab-and-training.md`
- Class slugs: `../docs/11-species.md`

Local setup (already created on this machine as `.venv`):

```bat
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r ml\requirements.txt
```

```text
notebooks/    Colab-ready notebooks
src/          importable Python (keep notebooks thin)
artifacts/    exported model + label map + metrics — no images
```

Until the first notebook exists, copy nothing from other projects (including the sibling `yolo` folder). That work is a different study.

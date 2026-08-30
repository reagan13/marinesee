# Cursor, Google Colab, and Google Drive

**IMPLEMENTATION** — the paper never mentions Colab. This is how we honor the study’s SVM pipeline with the dataset you already mounted on Drive.

## Direct answer

**Yes.** Keep the code in this repo. Train on Colab. Leave the images on Drive.

Cursor cannot “remote-control” a Colab runtime the way it controls a local terminal. You do not need that. The durable link is **git + Drive**, not a special Cursor↔Colab plugin.

```text
[you in Cursor]  edit ml/notebooks and ml/src
        │
        │  git push   or   copy notebook
        ▼
[Colab]  git clone / pull this repo   OR   open the .ipynb from Drive
        │  mount Drive dataset
        │  run preprocess → features → SVM → metrics
        ▼
[Drive]  write svm_seagrass.joblib + metrics.json
        │
        ▼
[app/]   load exported model (on-device or API)
```

## What belongs where

| Thing | Where it lives | Why |
|-------|----------------|-----|
| Notebooks, `ml/src`, docs, app | This git repo | Reviewable, same as pgso/furescue |
| Raw / labeled JPEGs | Google Drive | Already mounted; too large for git |
| Exported SVM + label map | Drive, then copy small files into `ml/artifacts/` | App and thesis appendix need a frozen file |
| Secrets / Colab tokens | Never | Do not commit |

## First session (inventory only)

Do this before any training.

1. In [the Seagrass Drive folder](https://drive.google.com/drive/folders/1MU31a5BG3MKn1fEYV-ljhc2zS4CoE79F), add a shortcut to **My Drive** (Shared-with-me is invisible to Colab otherwise).
2. Open `ml/notebooks/01_dataset_inventory.ipynb` in [Colab](https://colab.research.google.com) (Upload) **or** in Cursor with Kernel → **Colab**.
3. Run all cells. CPU is enough. You want a per-species count for `research-grade` vs `all`, plus a warning if *Halophila spinulosa* or a `- Copy` folder is in the mix.
4. Paste the count table into `docs/14-open-questions.md` question 3.

Do not start a YOLO notebook on this folder. The study classifier is SVM.

## Typical later Colab session

1. Open [Google Colab](https://colab.research.google.com).
2. Mount Drive (shortcut already on My Drive).
3. Get the code — pick **one** and stick to it:
   - `!git clone` / `git pull` this repository into the Colab VM, **or**
   - keep a copy of `ml/` as a Drive folder that you sync after Cursor edits
4. Point a single config cell at the dataset root, for example:

   `DATA_ROOT = "/content/drive/MyDrive/<your-seagrass-folder>"`

5. Expect this folder convention (adjust if yours differs; then update `data/README.md`):

   ```text
   DATA_ROOT/
     cymodocea_rotundata/
     cymodocea_serrulata/
     enhalus_acoroides/
     halodule_pinifolia/
     halodule_uninervis/
     halophila_minor/
     halophila_ovalis/
     syringodium_isoetifolium/
     thalassia_hemprichii/
   ```

6. Run the pipeline in `09-ml-pipeline.md`.
7. Save artifacts to Drive **and** download them into `ml/artifacts/` when you want them versioned.

SVM training itself rarely needs a GPU. A GPU runtime still helps if resize/augment is slow.

## What not to do

- Do not upload the whole image dataset into this git repo.
- Do not keep the only copy of the training notebook as an untitled Colab scratch file.
- Do not change class folder names without updating `11-species.md` and the app label map.
- Do not switch the notebook to YOLO/CNN because Colab makes it easy. The study requires SVM.

## Sharing the notebook with the team

Put the `.ipynb` in `ml/notebooks/` so Cursor can diff it. In Colab: File → Upload, or “Open notebook from GitHub” once a remote exists.

## When we have a remote

After this folder is a git remote, Colab can:

```text
!git clone <repo-url> seagrass
%cd seagrass
```

Until then, upload `ml/` or copy it onto Drive next to the dataset.

# Dataset (Google Drive, not git)

**STUDY:** leaf and canopy photos of the nine Mati species, from Lawigan, Taitaidaga, Manguihay, and Pujada Bay. Split 70/15/15 after we lock the files.

**IMPLEMENTATION:** the images are already on Google Drive. This folder is only a pointer.

## Do not put images here

Git will ignore common image types. If you need a local copy for debugging, keep it outside the repo or in an ignored path.

## Expected class folders

Names must match `docs/11-species.md`:

```text
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

## Drive location (locked)

| Item | Value |
|------|--------|
| Folder | [Seagrass (Shared with me)](https://drive.google.com/drive/folders/1MU31a5BG3MKn1fEYV-ljhc2zS4CoE79F) |
| Folder id | `1MU31a5BG3MKn1fEYV-ljhc2zS4CoE79F` |
| Owner (as of Aug 2026) | akeroshii |
| Colab path after shortcut | `/content/drive/MyDrive/Seagrass` |
| Inventory date | 30 Aug 2026 (`ml/artifacts/inventory.md`) |
| `all` images (8 species) | 3896 — *Thalassia hemprichii* still **0** |
| research-grade (no copy) | 898 |
| Ovalis `- Copy` | 378 — do not mix with `all` |
| Split | not on Drive; we will split 70/15/15 later |

Drive titles are **not** our slugs. They look like `Enhalus acoroides dataset (all)` and `… (research-grade)`. Matching lives in `ml/src/dataset_contract.py`.

## What the inventory found

- Eight of nine study species are present. ***Thalassia hemprichii* is missing** from this folder.
- *Halophila ovalis* has no folder tagged `research-grade`; only `all` (1549) and `(research-grade) - Copy` (378).
- *Halophila spinulosa* was **not** in this mount.
- Research-grade-only is not trainable: *H. minor* has **3** images; *C. serrulata* 15; *H. pinifolia* 19.

**v1 (30 Aug 2026):** train the **eight** present classes from **`all`**. Ignore ovalis `- Copy`. Hold out *Thalassia* until a folder exists. Notebook: `ml/notebooks/02_svm_v1_eight_class.ipynb`. Full table: `ml/artifacts/inventory.md`.

Colab steps: `docs/12-colab-and-training.md` and `ml/notebooks/README.md`.

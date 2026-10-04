# Inventory snapshot

## Drive (30 Aug 2026)

Source: Colab run of `01_dataset_inventory.ipynb` against `/content/drive/MyDrive/Seagrass`  
Drive folder id `1MU31a5BG3MKn1fEYV-ljhc2zS4CoE79F`  
JSON also written to `MyDrive/Seagrass-ml-artifacts/inventory.json`

| slug | research-grade | all | copy |
|------|----------------|-----|------|
| cymodocea_rotundata | 57 | 158 | 0 |
| cymodocea_serrulata | 15 | 87 | 0 |
| enhalus_acoroides | 608 | 666 | 0 |
| halodule_pinifolia | 19 | 876 | 0 |
| halodule_uninervis | 148 | 375 | 0 |
| halophila_minor | 3 | 24 | 0 |
| halophila_ovalis | 0 | 1549 | 378 |
| syringodium_isoetifolium | 48 | 161 | 0 |
| thalassia_hemprichii | 0 | 0 | 0 |

- **Missing class on this Drive root:** *Thalassia hemprichii*.
- **Ovalis research-grade** only exists as `(research-grade) - Copy` (378). Counted as `copy`, not `research-grade`.
- **Halophila spinulosa** did not appear in this mount (good).
- Research-grade column total (no copy): **898**
- `all` column total (no Thalassia): **3896**
- Ovalis copy: **378** — treat as duplicate risk if mixed with `all`

## Local dump (19 Sep 2026)

Source: `assets/species/Seagrass` after un-nesting *Thalassia* folders that had been stored under *Enhalus* / *Halodule*. Counts skip nested folders of a different class (`ml/src/inventory.py`).

| slug | research-grade | all |
|------|----------------|-----|
| cymodocea_rotundata | 57 | 158 |
| cymodocea_serrulata | 15 | 87 |
| enhalus_acoroides | 362 | 666 |
| halodule_pinifolia | 19 | 85 |
| halodule_uninervis | 148 | 375 |
| halophila_minor | 3 | 24 |
| halophila_ovalis | 378 | 619 |
| syringodium_isoetifolium | 48 | 161 |
| thalassia_hemprichii | 246 | 743 |

- *Thalassia* research-grade: 246 unique files (the two nested RG folders were duplicates).
- *Thalassia* all: 743 unique files (512 duplicates dropped when merging the two nested `all` folders).
- *Enhalus* research-grade fell from 608 → 362 once 246 nested Thalassia files were removed from that tree.
- Local *H. pinifolia* `all` is 85 after removing a nested Thalassia dump; Drive still has 876 — do not treat this laptop folder as the training root.
- Still **held out of v1 training** until a mix-in audit (some nested files may be *Enhalus*).

## Verdict

**v1 (team decision 30 Aug 2026):** train the **eight** classes that exist on Drive. *Thalassia hemprichii* stays in the paper list. Use **`all`**, drop ovalis `- Copy`, augment + class-weight minority classes. Do not pretend the study is now 8 species. Add Thalassia to `TRAINABLE_SPECIES` only after the relocated folder is audited.

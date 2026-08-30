# Inventory snapshot (30 Aug 2026)

Source: Colab run of `01_dataset_inventory.ipynb` against `/content/drive/MyDrive/Seagrass`  
Drive folder id `1MU31a5BG3MKn1fEYV-ljhc2zS4CoE79F`  
JSON also written to `MyDrive/Seagrass-ml-artifacts/inventory.json`

## Per study species

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

- **Missing class:** *Thalassia hemprichii* — not on this Drive root.
- **Ovalis research-grade** only exists as `(research-grade) - Copy` (378). Counted as `copy`, not `research-grade`.
- **Halophila spinulosa** did not appear in this mount (good).
- Research-grade column total (no copy): **898**
- `all` column total (no Thalassia): **3896**
- Ovalis copy: **378** — treat as duplicate risk if mixed with `all`

## Verdict

**v1 (team decision 30 Aug 2026):** train the **eight** classes that exist. *Thalassia hemprichii* stays in the paper list and is added when a folder appears. Use **`all`**, drop ovalis `- Copy`, augment + class-weight minority classes. Do not pretend the study is now 8 species.

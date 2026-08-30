# SVM v1 smoke test (30 Aug 2026)

**Not a thesis number.** `MAX_PER_CLASS = 100`, eight classes, `all` folders, 256px RGB, GLCM on 64px.

| Split | n | Accuracy |
|-------|---|----------|
| test | 107 | **22.4%** |
| study target | — | 85% |
| chance (8 classes) | — | 12.5% |

## Per-class test F1

| slug | precision | recall | f1 | support |
|------|-----------|--------|-----|---------|
| cymodocea_rotundata | 0.24 | 0.27 | 0.25 | 15 |
| cymodocea_serrulata | 0.50 | 0.62 | 0.55 | 13 |
| enhalus_acoroides | 0.07 | 0.07 | 0.07 | 15 |
| halodule_pinifolia | 0.00 | 0.00 | 0.00 | 15 |
| halodule_uninervis | 0.06 | 0.07 | 0.06 | 15 |
| halophila_minor | 0.00 | 0.00 | 0.00 | 4 |
| halophila_ovalis | 0.16 | 0.20 | 0.18 | 15 |
| syringodium_isoetifolium | 0.50 | 0.47 | 0.48 | 15 |

Artifacts on Drive: `Seagrass-ml-artifacts/v1/` (`svm_seagrass_v1.joblib`, `metrics.json`).

## Read

- Distinctive shapes moved a bit (*serrulata*, *Syringodium*).
- Lookalikes and tiny classes did not (*Halodule* pair, *H. minor*).
- *Enhalus* should be easy by eye and still failed — whole-frame color/GLCM is a weak species signal, or the `all` photos are messy.

Next experiment: better features / leaf-focused preprocess, **not** more images first, **not** YOLO.

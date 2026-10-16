# svm 20261013T142541175Z

- recorded_at: 2026-10-13T14:25:41Z
- started_at: 2026-10-13T14:22:50Z
- elapsed_seconds: 170.9
- runtime: local
- data_root: D:\pepot\marinesee\assets\species\Seagrass
- max_per_class: 400
- split_seed: 42
- fit_seconds: 0.9
- best_params: {'kernel': 'rbf', 'C': 30.0, 'gamma': 0.03}
- best_val_macro_f1: 0.399388942812271
- n_train: 1286
- n_val: 254
- n_test: 254
- train_accuracy: 0.9992223950233281
- val_accuracy: 0.4409448818897638
- test_accuracy: 0.38188976377952755

RBF SVM is one fit per setting, so there is no epoch train-loss or validation-loss curve. The tuning curve plots train against validation macro F1 across C instead.

## tuning (top 10 by validation macro F1)

| kernel | C | gamma | train macro F1 | val macro F1 | val acc | gap |
|---|---:|---:|---:|---:|---:|---:|
| rbf | 30.0 | 0.03 | 0.999 | 0.399 | 0.441 | 0.599 |
| rbf | 100.0 | 0.03 | 0.999 | 0.399 | 0.441 | 0.599 |
| rbf | 10.0 | 0.03 | 0.997 | 0.396 | 0.437 | 0.601 |
| rbf | 100.0 | scale | 0.997 | 0.371 | 0.417 | 0.626 |
| rbf | 3.0 | 0.03 | 0.957 | 0.367 | 0.413 | 0.590 |
| rbf | 100.0 | 0.01 | 0.997 | 0.364 | 0.409 | 0.633 |
| rbf | 30.0 | scale | 0.981 | 0.362 | 0.390 | 0.619 |
| rbf | 10.0 | scale | 0.922 | 0.361 | 0.394 | 0.561 |
| rbf | 30.0 | 0.01 | 0.970 | 0.356 | 0.390 | 0.614 |
| rbf | 100.0 | 0.003 | 0.903 | 0.351 | 0.358 | 0.552 |

## train

| slug | precision | recall | f1 | support |
|---|---:|---:|---:|---:|
| cymodocea_rotundata | 1.000 | 0.991 | 0.995 | 110.0 |
| cymodocea_serrulata | 1.000 | 1.000 | 1.000 | 80.0 |
| enhalus_acoroides | 1.000 | 1.000 | 1.000 | 280.0 |
| halodule_pinifolia | 1.000 | 1.000 | 1.000 | 80.0 |
| halodule_uninervis | 1.000 | 1.000 | 1.000 | 263.0 |
| halophila_minor | 1.000 | 1.000 | 1.000 | 80.0 |
| halophila_ovalis | 1.000 | 1.000 | 1.000 | 280.0 |
| syringodium_isoetifolium | 0.991 | 1.000 | 0.996 | 113.0 |
| macro avg | 0.999 | 0.999 | 0.999 | 1286.0 |
| weighted avg | 0.999 | 0.999 | 0.999 | 1286.0 |

## val

| slug | precision | recall | f1 | support |
|---|---:|---:|---:|---:|
| cymodocea_rotundata | 0.300 | 0.125 | 0.176 | 24.0 |
| cymodocea_serrulata | 0.600 | 0.231 | 0.333 | 13.0 |
| enhalus_acoroides | 0.474 | 0.600 | 0.529 | 60.0 |
| halodule_pinifolia | 0.750 | 0.462 | 0.571 | 13.0 |
| halodule_uninervis | 0.410 | 0.607 | 0.489 | 56.0 |
| halophila_minor | 0.500 | 0.250 | 0.333 | 4.0 |
| halophila_ovalis | 0.396 | 0.350 | 0.372 | 60.0 |
| syringodium_isoetifolium | 0.471 | 0.333 | 0.390 | 24.0 |
| macro avg | 0.488 | 0.370 | 0.399 | 254.0 |
| weighted avg | 0.446 | 0.441 | 0.426 | 254.0 |

## test

| slug | precision | recall | f1 | support |
|---|---:|---:|---:|---:|
| cymodocea_rotundata | 0.333 | 0.167 | 0.222 | 24.0 |
| cymodocea_serrulata | 0.333 | 0.154 | 0.211 | 13.0 |
| enhalus_acoroides | 0.390 | 0.383 | 0.387 | 60.0 |
| halodule_pinifolia | 0.636 | 0.538 | 0.583 | 13.0 |
| halodule_uninervis | 0.318 | 0.482 | 0.383 | 56.0 |
| halophila_minor | 0.000 | 0.000 | 0.000 | 4.0 |
| halophila_ovalis | 0.443 | 0.450 | 0.446 | 60.0 |
| syringodium_isoetifolium | 0.368 | 0.292 | 0.326 | 24.0 |
| macro avg | 0.353 | 0.308 | 0.320 | 254.0 |
| weighted avg | 0.383 | 0.382 | 0.374 | 254.0 |

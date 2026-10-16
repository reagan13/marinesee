# svm 20261013T154158856Z

- recorded_at: 2026-10-13T15:41:58Z
- started_at: 2026-10-13T15:22:08Z
- elapsed_seconds: 1190.1
- runtime: local
- data_root: D:\pepot\marinesee\assets\species\Seagrass
- max_per_class: 400
- split_seed: 42
- fit_seconds: 1.0
- best_params: {'kernel': 'rbf', 'C': 10.0, 'gamma': 0.03}
- best_val_macro_f1: 0.40562491366210807
- n_train: 1286
- n_val: 254
- n_test: 254
- train_accuracy: 0.942457231726283
- val_accuracy: 0.4566929133858268
- test_accuracy: 0.43700787401574803

RBF SVM is one fit per setting, so there is no epoch train-loss or validation-loss curve. The tuning curve plots train against validation macro F1 across C instead.

## tuning (top 10 by validation macro F1)

| kernel | C | gamma | train macro F1 | val macro F1 | val acc | gap |
|---|---:|---:|---:|---:|---:|---:|
| rbf | 10.0 | 0.03 | 0.948 | 0.406 | 0.457 | 0.543 |
| rbf | 10.0 | scale | 0.886 | 0.403 | 0.449 | 0.483 |
| rbf | 30.0 | 0.03 | 0.989 | 0.402 | 0.472 | 0.587 |
| rbf | 3.0 | 0.03 | 0.836 | 0.401 | 0.433 | 0.434 |
| rbf | 100.0 | scale | 0.996 | 0.397 | 0.441 | 0.599 |
| rbf | 1.0 | 0.1 | 0.921 | 0.392 | 0.449 | 0.529 |
| rbf | 100.0 | 0.03 | 0.999 | 0.390 | 0.457 | 0.608 |
| rbf | 3.0 | scale | 0.769 | 0.385 | 0.409 | 0.384 |
| rbf | 30.0 | 0.01 | 0.861 | 0.375 | 0.449 | 0.485 |
| rbf | 1.0 | 0.03 | 0.710 | 0.369 | 0.421 | 0.341 |

## train

| slug | precision | recall | f1 | support |
|---|---:|---:|---:|---:|
| cymodocea_rotundata | 0.856 | 0.973 | 0.911 | 110.0 |
| cymodocea_serrulata | 0.889 | 1.000 | 0.941 | 80.0 |
| enhalus_acoroides | 0.966 | 0.921 | 0.943 | 280.0 |
| halodule_pinifolia | 0.964 | 1.000 | 0.982 | 80.0 |
| halodule_uninervis | 0.948 | 0.909 | 0.928 | 263.0 |
| halophila_minor | 1.000 | 1.000 | 1.000 | 80.0 |
| halophila_ovalis | 0.966 | 0.918 | 0.941 | 280.0 |
| syringodium_isoetifolium | 0.902 | 0.982 | 0.941 | 113.0 |
| macro avg | 0.937 | 0.963 | 0.948 | 1286.0 |
| weighted avg | 0.945 | 0.942 | 0.943 | 1286.0 |

## val

| slug | precision | recall | f1 | support |
|---|---:|---:|---:|---:|
| cymodocea_rotundata | 0.083 | 0.083 | 0.083 | 24.0 |
| cymodocea_serrulata | 0.167 | 0.077 | 0.105 | 13.0 |
| enhalus_acoroides | 0.530 | 0.583 | 0.556 | 60.0 |
| halodule_pinifolia | 0.875 | 0.538 | 0.667 | 13.0 |
| halodule_uninervis | 0.448 | 0.464 | 0.456 | 56.0 |
| halophila_minor | 0.500 | 0.500 | 0.500 | 4.0 |
| halophila_ovalis | 0.537 | 0.600 | 0.567 | 60.0 |
| syringodium_isoetifolium | 0.333 | 0.292 | 0.311 | 24.0 |
| macro avg | 0.434 | 0.392 | 0.406 | 254.0 |
| weighted avg | 0.452 | 0.457 | 0.450 | 254.0 |

## test

| slug | precision | recall | f1 | support |
|---|---:|---:|---:|---:|
| cymodocea_rotundata | 0.182 | 0.167 | 0.174 | 24.0 |
| cymodocea_serrulata | 0.308 | 0.308 | 0.308 | 13.0 |
| enhalus_acoroides | 0.507 | 0.633 | 0.563 | 60.0 |
| halodule_pinifolia | 0.667 | 0.615 | 0.640 | 13.0 |
| halodule_uninervis | 0.361 | 0.393 | 0.376 | 56.0 |
| halophila_minor | 0.500 | 0.250 | 0.333 | 4.0 |
| halophila_ovalis | 0.560 | 0.467 | 0.509 | 60.0 |
| syringodium_isoetifolium | 0.316 | 0.250 | 0.279 | 24.0 |
| macro avg | 0.425 | 0.385 | 0.398 | 254.0 |
| weighted avg | 0.436 | 0.437 | 0.433 | 254.0 |

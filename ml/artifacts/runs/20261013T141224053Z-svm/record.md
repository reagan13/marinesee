# svm 20261013T141224053Z

- recorded_at: 2026-10-13T14:12:24Z
- started_at: 2026-10-13T14:08:29Z
- elapsed_seconds: 234.7
- runtime: local
- data_root: D:\pepot\marinesee\assets\species\Seagrass
- max_per_class: 100
- split_seed: 42
- fit_seconds: 0.3
- n_train: 640
- n_val: 105
- n_test: 105
- train_accuracy: 0.9875
- val_accuracy: 0.3619047619047619
- test_accuracy: 0.2857142857142857

RBF SVM is one fit, so there is no epoch train-loss or validation-loss curve. This record stores fit time and train, validation, and test precision, recall, and F1.

## train

| slug | precision | recall | f1 | support |
|---|---:|---:|---:|---:|
| cymodocea_rotundata | 1.000 | 0.975 | 0.987 | 80.0 |
| cymodocea_serrulata | 0.975 | 0.988 | 0.981 | 80.0 |
| enhalus_acoroides | 0.988 | 1.000 | 0.994 | 80.0 |
| halodule_pinifolia | 0.976 | 1.000 | 0.988 | 80.0 |
| halodule_uninervis | 1.000 | 0.975 | 0.987 | 80.0 |
| halophila_minor | 0.988 | 1.000 | 0.994 | 80.0 |
| halophila_ovalis | 0.987 | 0.975 | 0.981 | 80.0 |
| syringodium_isoetifolium | 0.988 | 0.988 | 0.988 | 80.0 |
| macro avg | 0.988 | 0.988 | 0.987 | 640.0 |
| weighted avg | 0.988 | 0.988 | 0.987 | 640.0 |

## val

| slug | precision | recall | f1 | support |
|---|---:|---:|---:|---:|
| cymodocea_rotundata | 0.438 | 0.467 | 0.452 | 15.0 |
| cymodocea_serrulata | 0.385 | 0.385 | 0.385 | 13.0 |
| enhalus_acoroides | 0.471 | 0.533 | 0.500 | 15.0 |
| halodule_pinifolia | 0.562 | 0.692 | 0.621 | 13.0 |
| halodule_uninervis | 0.267 | 0.267 | 0.267 | 15.0 |
| halophila_minor | 0.333 | 0.250 | 0.286 | 4.0 |
| halophila_ovalis | 0.077 | 0.067 | 0.071 | 15.0 |
| syringodium_isoetifolium | 0.250 | 0.200 | 0.222 | 15.0 |
| macro avg | 0.348 | 0.358 | 0.350 | 105.0 |
| weighted avg | 0.344 | 0.362 | 0.351 | 105.0 |

## test

| slug | precision | recall | f1 | support |
|---|---:|---:|---:|---:|
| cymodocea_rotundata | 0.278 | 0.333 | 0.303 | 15.0 |
| cymodocea_serrulata | 0.286 | 0.308 | 0.296 | 13.0 |
| enhalus_acoroides | 0.250 | 0.333 | 0.286 | 15.0 |
| halodule_pinifolia | 0.368 | 0.538 | 0.438 | 13.0 |
| halodule_uninervis | 0.300 | 0.200 | 0.240 | 15.0 |
| halophila_minor | 1.000 | 0.500 | 0.667 | 4.0 |
| halophila_ovalis | 0.083 | 0.067 | 0.074 | 15.0 |
| syringodium_isoetifolium | 0.300 | 0.200 | 0.240 | 15.0 |
| macro avg | 0.358 | 0.310 | 0.318 | 105.0 |
| weighted avg | 0.292 | 0.286 | 0.280 | 105.0 |

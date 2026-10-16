# svm 20261014T120604669Z

- recorded_at: 2026-10-14T12:06:04Z
- started_at: 2026-10-14T11:48:50Z
- elapsed_seconds: 1034.6
- runtime: local
- data_root: D:\pepot\marinesee\assets\species\Seagrass
- max_per_class: 400
- split_seed: 42
- fit_seconds: 2.8
- best_params: {'kernel': 'rbf', 'C': 3.0, 'gamma': 0.01}
- n_train: 1286
- n_val: 254
- n_test: 254
- train_accuracy: 0.9074650077760498
- val_accuracy: 0.5
- test_accuracy: 0.421259842519685

Locked refit of the validation winner (RBF C=3, gamma=0.01) on feature v2. No new grid search.

## train

| slug | precision | recall | f1 | support |
|---|---:|---:|---:|---:|
| cymodocea_rotundata | 0.837 | 0.936 | 0.884 | 110.0 |
| cymodocea_serrulata | 0.833 | 1.000 | 0.909 | 80.0 |
| enhalus_acoroides | 0.934 | 0.861 | 0.896 | 280.0 |
| halodule_pinifolia | 0.963 | 0.988 | 0.975 | 80.0 |
| halodule_uninervis | 0.965 | 0.837 | 0.896 | 263.0 |
| halophila_minor | 1.000 | 1.000 | 1.000 | 80.0 |
| halophila_ovalis | 0.934 | 0.904 | 0.918 | 280.0 |
| syringodium_isoetifolium | 0.750 | 0.982 | 0.851 | 113.0 |
| macro avg | 0.902 | 0.938 | 0.916 | 1286.0 |
| weighted avg | 0.915 | 0.907 | 0.908 | 1286.0 |

## val

| slug | precision | recall | f1 | support |
|---|---:|---:|---:|---:|
| cymodocea_rotundata | 0.238 | 0.208 | 0.222 | 24.0 |
| cymodocea_serrulata | 0.300 | 0.231 | 0.261 | 13.0 |
| enhalus_acoroides | 0.569 | 0.617 | 0.592 | 60.0 |
| halodule_pinifolia | 0.583 | 0.538 | 0.560 | 13.0 |
| halodule_uninervis | 0.463 | 0.446 | 0.455 | 56.0 |
| halophila_minor | 0.600 | 0.750 | 0.667 | 4.0 |
| halophila_ovalis | 0.623 | 0.633 | 0.628 | 60.0 |
| syringodium_isoetifolium | 0.346 | 0.375 | 0.360 | 24.0 |
| macro avg | 0.465 | 0.475 | 0.468 | 254.0 |
| weighted avg | 0.494 | 0.500 | 0.496 | 254.0 |

## test

| slug | precision | recall | f1 | support |
|---|---:|---:|---:|---:|
| cymodocea_rotundata | 0.240 | 0.250 | 0.245 | 24.0 |
| cymodocea_serrulata | 0.176 | 0.231 | 0.200 | 13.0 |
| enhalus_acoroides | 0.500 | 0.617 | 0.552 | 60.0 |
| halodule_pinifolia | 0.636 | 0.538 | 0.583 | 13.0 |
| halodule_uninervis | 0.345 | 0.339 | 0.342 | 56.0 |
| halophila_minor | 0.667 | 0.500 | 0.571 | 4.0 |
| halophila_ovalis | 0.548 | 0.383 | 0.451 | 60.0 |
| syringodium_isoetifolium | 0.370 | 0.417 | 0.392 | 24.0 |
| macro avg | 0.435 | 0.409 | 0.417 | 254.0 |
| weighted avg | 0.433 | 0.421 | 0.422 | 254.0 |

"""Tuning picks on validation only and never needs the test split."""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.tune_svm import best, best_params, candidate_params, search  # noqa: E402


def _blobs(seed: int, n: int) -> tuple[np.ndarray, list[str]]:
    rng = np.random.default_rng(seed)
    centers = {"a": (0.0, 0.0), "b": (4.0, 4.0), "c": (0.0, 4.0)}
    rows, labels = [], []
    for label, center in centers.items():
        rows.append(rng.normal(center, 1.0, size=(n, 2)))
        labels += [label] * n
    return np.vstack(rows), labels


def test_grid_has_rbf_and_linear() -> None:
    kernels = {row["kernel"] for row in candidate_params()}
    assert kernels == {"rbf", "linear"}


def test_search_scores_val_and_picks_best() -> None:
    x_train, y_train = _blobs(1, 30)
    x_val, y_val = _blobs(2, 10)
    grid = [
        {"kernel": "rbf", "C": 0.1, "gamma": 0.001},
        {"kernel": "rbf", "C": 10.0, "gamma": "scale"},
    ]
    rows = search(x_train, y_train, x_val, y_val, grid=grid)
    assert len(rows) == 2
    assert all(0.0 <= row["val_macro_f1"] <= 1.0 for row in rows)
    chosen = best(rows)
    assert chosen["val_macro_f1"] == max(row["val_macro_f1"] for row in rows)
    assert set(best_params(rows)) == {"kernel", "C", "gamma"}


if __name__ == "__main__":
    test_grid_has_rbf_and_linear()
    test_search_scores_val_and_picks_best()
    print("ok")

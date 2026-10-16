"""Pick SVM kernel, C, and gamma on the fixed validation split.

Each candidate is fit on the train split (augmented copies included) and
scored on the untouched validation split. The test split is never read here.
Selection metric is macro F1 so small species count as much as large ones.
"""

from __future__ import annotations

import time
from collections.abc import Callable, Iterable

import numpy as np
from sklearn.metrics import accuracy_score, f1_score

from .dataset_contract import SPLIT_SEED
from .train_svm import make_pipeline

RBF_C = (0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0)
RBF_GAMMA: tuple[str | float, ...] = ("scale", 0.001, 0.003, 0.01, 0.03, 0.1)
LINEAR_C = (0.01, 0.03, 0.1, 0.3, 1.0)
SELECTION_METRIC = "val_macro_f1"

TUNING_SPEC = {
    "split": "fixed 15% validation",
    "metric": SELECTION_METRIC,
    "class_weight": "balanced",
    "rbf_C": list(RBF_C),
    "rbf_gamma": list(RBF_GAMMA),
    "linear_C": list(LINEAR_C),
}


def candidate_params() -> list[dict]:
    grid = [{"kernel": "rbf", "C": c, "gamma": g} for c in RBF_C for g in RBF_GAMMA]
    grid += [{"kernel": "linear", "C": c, "gamma": None} for c in LINEAR_C]
    return grid


def search(
    x_train: np.ndarray,
    y_train: list[str],
    x_val: np.ndarray,
    y_val: list[str],
    grid: Iterable[dict] | None = None,
    seed: int = SPLIT_SEED,
    progress: Callable[[Iterable[dict]], Iterable[dict]] | None = None,
) -> list[dict]:
    params_list = list(grid if grid is not None else candidate_params())
    iterator = progress(params_list) if progress else params_list
    rows: list[dict] = []
    for params in iterator:
        model = make_pipeline(seed, probability=False, **params)
        start = time.perf_counter()
        model.fit(x_train, y_train)
        fit_seconds = time.perf_counter() - start
        train_pred = model.predict(x_train)
        val_pred = model.predict(x_val)
        train_f1 = float(f1_score(y_train, train_pred, average="macro", zero_division=0))
        val_f1 = float(f1_score(y_val, val_pred, average="macro", zero_division=0))
        rows.append(
            {
                **params,
                "train_accuracy": float(accuracy_score(y_train, train_pred)),
                "val_accuracy": float(accuracy_score(y_val, val_pred)),
                "train_macro_f1": train_f1,
                "val_macro_f1": val_f1,
                "f1_gap": train_f1 - val_f1,
                "fit_seconds": round(fit_seconds, 3),
            }
        )
    return rows


def best(rows: list[dict]) -> dict:
    """Highest validation macro F1; ties go to higher accuracy, then smaller C."""
    if not rows:
        raise ValueError("no tuning rows")
    return max(rows, key=lambda r: (r[SELECTION_METRIC], r["val_accuracy"], -float(r["C"])))


def best_params(rows: list[dict]) -> dict:
    row = best(rows)
    return {"kernel": row["kernel"], "C": row["C"], "gamma": row["gamma"]}

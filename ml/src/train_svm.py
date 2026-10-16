"""Fit a scaled RBF SVM and write metrics + joblib."""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from .dataset_contract import SPLIT_SEED, TRAINABLE_SPECIES
from .features import FEATURE_SPEC


def make_pipeline(
    seed: int = SPLIT_SEED,
    *,
    kernel: str = "rbf",
    C: float = 10.0,
    gamma: str | float | None = "scale",
    class_weight: str | None = "balanced",
    probability: bool = True,
) -> Pipeline:
    svc_args = {
        "kernel": kernel,
        "C": C,
        "gamma": "scale" if gamma is None else gamma,
        "class_weight": class_weight,
        "random_state": seed,
    }
    # identify.py needs predict_proba; scikit-learn 1.9 warns on the argument itself.
    if probability:
        svc_args["probability"] = True
    return Pipeline([("scaler", StandardScaler()), ("svm", SVC(**svc_args))])


def evaluate(model: Pipeline, x: np.ndarray, y: list[str]) -> dict:
    pred = model.predict(x)
    labels = list(TRAINABLE_SPECIES)
    return {
        "accuracy": float(accuracy_score(y, pred)),
        "report": classification_report(y, pred, labels=labels, output_dict=True, zero_division=0),
        "confusion_matrix": confusion_matrix(y, pred, labels=labels).tolist(),
        "labels": labels,
        "pred": pred.tolist(),
    }


def export_artifacts(
    model: Pipeline,
    metrics: dict,
    dest: Path,
) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, dest / "svm_seagrass_v1.joblib")
    label_map = {str(i): slug for i, slug in enumerate(TRAINABLE_SPECIES)}
    (dest / "label_map.json").write_text(json.dumps(label_map, indent=2), encoding="utf-8")
    (dest / "feature_spec.json").write_text(json.dumps(FEATURE_SPEC, indent=2), encoding="utf-8")
    (dest / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")

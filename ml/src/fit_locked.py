"""Fit the locked v2 SVM and write ml/artifacts/v1.

Settings are the validation winner from run 20261013T144233395Z:
RBF, C=3, gamma=0.01, class_weight=balanced. The test split is scored once.
"""

from __future__ import annotations

import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from tqdm import tqdm

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.dataset_contract import (  # noqa: E402
    HELD_OUT_SPECIES,
    IMAGE_SIZE,
    SPLIT_SEED,
    TRAIN_VARIANT,
    TRAINABLE_SPECIES,
)
from src.features import FEATURE_SPEC, extract_vector  # noqa: E402
from src.preprocess import (  # noqa: E402
    cap_per_class,
    expand_minority_train,
    list_labeled_images,
    load_prepared,
)
from src.run_log import append_run  # noqa: E402
from src.split import split_labels  # noqa: E402
from src.train_svm import evaluate, export_artifacts, make_pipeline  # noqa: E402

LOCKED = {"kernel": "rbf", "C": 3.0, "gamma": 0.01}
MAX_PER_CLASS = 400
DATA_ROOT = ROOT.parent / "assets" / "species" / "Seagrass"


def featurize(images: list[np.ndarray], tag: str) -> np.ndarray:
    rows = [extract_vector(image) for image in tqdm(images, desc=f"Features {tag}", unit="img")]
    return np.stack(rows, axis=0)


def main() -> None:
    started = datetime.now(timezone.utc)
    print("features", FEATURE_SPEC["version"], FEATURE_SPEC["length"], "locked", LOCKED)
    pairs = cap_per_class(list_labeled_images(DATA_ROOT), MAX_PER_CLASS, seed=SPLIT_SEED)
    print("images", len(pairs), dict(Counter(slug for _, slug in pairs)))
    train_p, val_p, test_p, train_y, val_y, test_y = split_labels(
        [path for path, _ in pairs], [slug for _, slug in pairs], seed=SPLIT_SEED
    )

    def load_many(paths, labels, tag):
        images, keep = [], []
        for path, label in tqdm(list(zip(paths, labels)), desc=f"Load {tag}", unit="img"):
            images.append(load_prepared(path, size=IMAGE_SIZE))
            keep.append(label)
        return images, keep

    train_img, train_y = load_many(train_p, train_y, "train")
    val_img, val_y = load_many(val_p, val_y, "val")
    test_img, test_y = load_many(test_p, test_y, "test")
    real_train_counts = dict(Counter(train_y))
    train_img, train_y = expand_minority_train(train_img, train_y, min_per_class=80)
    print("train after augment", dict(Counter(train_y)))

    x_train = featurize(train_img, "train")
    x_val = featurize(val_img, "val")
    x_test = featurize(test_img, "test")

    model = make_pipeline(SPLIT_SEED, probability=True, **LOCKED)
    t0 = time.perf_counter()
    model.fit(x_train, train_y)
    fit_seconds = time.perf_counter() - t0
    results = {
        name: evaluate(model, x, y)
        for name, x, y in (
            ("train", x_train, train_y),
            ("val", x_val, val_y),
            ("test", x_test, test_y),
        )
    }
    for name in ("train", "val", "test"):
        macro = results[name]["report"]["macro avg"]["f1-score"]
        print(f"{name} acc {results[name]['accuracy']:.4f}  macro F1 {macro:.4f}")

    finished = datetime.now(timezone.utc)
    record = {
        "kind": "svm",
        "runtime": "local",
        "started_at": started.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "elapsed_seconds": round((finished - started).total_seconds(), 1),
        "data_root": str(DATA_ROOT),
        "max_per_class": MAX_PER_CLASS,
        "split_seed": SPLIT_SEED,
        "image_size": IMAGE_SIZE,
        "variant": TRAIN_VARIANT,
        "feature_spec": FEATURE_SPEC,
        "classes": list(TRAINABLE_SPECIES),
        "held_out": list(HELD_OUT_SPECIES),
        "images_this_run": len(pairs),
        "n_train": len(train_y),
        "n_val": len(val_y),
        "n_test": len(test_y),
        "train_real_counts": real_train_counts,
        "train_class_counts": dict(Counter(train_y)),
        "best_params": LOCKED,
        "locked_from_run": "20261013T144233395Z-svm",
        "fit_seconds": round(fit_seconds, 1),
        "train_accuracy": results["train"]["accuracy"],
        "val_accuracy": results["val"]["accuracy"],
        "test_accuracy": results["test"]["accuracy"],
        "train_report": results["train"]["report"],
        "val_report": results["val"]["report"],
        "test_report": results["test"]["report"],
        "confusion_matrix_test": results["test"]["confusion_matrix"],
        "study_target_accuracy": 0.85,
        "loss_note": (
            "Locked refit of the validation winner (RBF C=3, gamma=0.01) on feature v2. "
            "No new grid search."
        ),
    }
    append_run(ROOT.parent, record)
    dest = ROOT / "artifacts" / "v1"
    export_artifacts(model, record, dest)
    print("wrote", dest)


if __name__ == "__main__":
    main()

"""Score one photo with the v1 joblib. Same plant crop, resize, and features as notebook 02."""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import numpy as np

try:
    from .dataset_contract import TRAINABLE_SPECIES
    from .features import extract_vector
    from .preprocess import load_prepared, prepared_from_bytes
except ImportError:
    from dataset_contract import TRAINABLE_SPECIES
    from features import extract_vector
    from preprocess import load_prepared, prepared_from_bytes

# IMPLEMENTATION default until Q14 is locked. Chance for 8 classes is 12.5%.
LOW_CONFIDENCE = 0.20


def default_model_path() -> Path:
    here = Path(__file__).resolve()
    artifacts = here.parents[1] / "artifacts"
    for cand in (artifacts / "v1" / "svm_seagrass_v1.joblib", artifacts / "svm_seagrass_v1.joblib"):
        if cand.is_file():
            return cand
    raise FileNotFoundError("svm_seagrass_v1.joblib not in ml/artifacts")


def load_model(path: Path | None = None):
    return joblib.load(path or default_model_path())


def _score(rgb: np.ndarray, model) -> dict:
    vector = extract_vector(rgb).reshape(1, -1)
    pred = str(model.predict(vector)[0])
    proba = model.predict_proba(vector)[0]
    classes = [str(c) for c in model.classes_]
    ranked = sorted(zip(classes, proba.tolist()), key=lambda item: item[1], reverse=True)
    conf = float(dict(ranked)[pred])
    return {
        "slug": pred,
        "predicted": pred,
        "confidence": conf,
        "low_confidence": conf < LOW_CONFIDENCE,
        "known": pred in TRAINABLE_SPECIES,
        "top": [{"slug": slug, "p": float(p)} for slug, p in ranked[:3]],
    }


def identify_path(path: Path, model=None) -> dict:
    model = model or load_model()
    result = _score(load_prepared(path), model)
    result["path"] = str(path)
    return result


def identify_bytes(data: bytes, model=None) -> dict:
    model = model or load_model()
    return _score(prepared_from_bytes(data), model)


def main() -> None:
    parser = argparse.ArgumentParser(description="Identify one seagrass photo with the v1 SVM.")
    parser.add_argument("image", type=Path)
    parser.add_argument("--model", type=Path, default=None)
    args = parser.parse_args()
    result = identify_path(args.image, model=load_model(args.model) if args.model else None)
    print(result["predicted"], f"{result['confidence']:.3f}")
    for row in result["top"]:
        print(f"  {row['slug']}  {row['p']:.3f}")


if __name__ == "__main__":
    main()

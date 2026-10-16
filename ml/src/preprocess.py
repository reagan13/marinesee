"""List, QC, resize, and lightly augment RGB images."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps

try:
    from .dataset_contract import (
        IMAGE_SIZE,
        IMAGE_SUFFIXES,
        TRAIN_VARIANT,
        TRAINABLE_SPECIES,
        classify_folder,
    )
    from .inventory import iter_images
    from .leaf_focus import analyze_and_crop, crop_to_plant
except ImportError:  # `python test_preprocess.py` from ml/src
    from dataset_contract import (
        IMAGE_SIZE,
        IMAGE_SUFFIXES,
        TRAIN_VARIANT,
        TRAINABLE_SPECIES,
        classify_folder,
    )
    from inventory import iter_images
    from leaf_focus import analyze_and_crop, crop_to_plant

PREPROCESS_SPEC = {
    "version": "v1",
    "resize": IMAGE_SIZE,
    "color": "RGB",
    "exif_transpose": True,
    "leaf_crop": True,
    "min_side_px": 64,
    "min_pixel_std": 8.0,
    "plant_fraction_is_diagnostic": True,
    "variant": TRAIN_VARIANT,
}

MIN_SIDE_PX = 64
MIN_PIXEL_STD = 8.0


def cap_per_class(
    pairs: list[tuple[Path, str]],
    max_per_class: int | None,
    seed: int = 42,
) -> list[tuple[Path, str]]:
    """Optional random cap so huge classes (ovalis ~1549) do not dominate runtime."""
    if max_per_class is None:
        return pairs
    by_class: dict[str, list[tuple[Path, str]]] = {}
    for pair in pairs:
        by_class.setdefault(pair[1], []).append(pair)
    rng = np.random.default_rng(seed)
    out: list[tuple[Path, str]] = []
    for items in by_class.values():
        if len(items) > max_per_class:
            pick = rng.choice(len(items), size=max_per_class, replace=False)
            items = [items[int(i)] for i in pick]
        out.extend(items)
    return out


def list_labeled_images(
    root: Path,
    *,
    species: tuple[str, ...] = TRAINABLE_SPECIES,
    variant: str = TRAIN_VARIANT,
) -> list[tuple[Path, str]]:
    """Return (path, slug) for the given species and variant only.

    Skips nested folders of a different class (Thalassia-under-Enhalus dumps).
    """
    pairs: list[tuple[Path, str]] = []
    for child in sorted(root.iterdir(), key=lambda p: p.name.lower()):
        if not child.is_dir() or child.name.startswith("."):
            continue
        slug, scope, folder_variant = classify_folder(child.name)
        if scope != "study" or slug not in species:
            continue
        if folder_variant != variant:
            continue
        for path in iter_images(child):
            if path.suffix.lower() in IMAGE_SUFFIXES:
                pairs.append((path, slug))
    return pairs


def _pil_to_rgb(image: Image.Image) -> np.ndarray:
    image = ImageOps.exif_transpose(image)
    image = image.convert("RGB")
    return np.asarray(image, dtype=np.uint8)


def load_rgb_full(path: Path) -> np.ndarray:
    return _pil_to_rgb(Image.open(path))


def load_rgb_from_bytes(data: bytes, size: int = IMAGE_SIZE) -> np.ndarray:
    return resize_rgb(_pil_to_rgb(Image.open(BytesIO(data))), size=size)


def resize_rgb(rgb: np.ndarray, size: int = IMAGE_SIZE) -> np.ndarray:
    image = Image.fromarray(rgb)
    image = image.resize((size, size), Image.Resampling.LANCZOS)
    return np.asarray(image, dtype=np.uint8)


def load_rgb(path: Path, size: int = IMAGE_SIZE) -> np.ndarray:
    return resize_rgb(load_rgb_full(path), size=size)


def prepare_rgb(rgb: np.ndarray, size: int = IMAGE_SIZE) -> np.ndarray:
    """Plant crop when the green mask allows it, then resize.

    Training and identify must both go through this before extract_vector.
    """
    cropped, _ = crop_to_plant(rgb)
    return resize_rgb(cropped, size=size)


def load_prepared(path: Path, size: int = IMAGE_SIZE) -> np.ndarray:
    return prepare_rgb(load_rgb_full(path), size=size)


def prepared_from_bytes(data: bytes, size: int = IMAGE_SIZE) -> np.ndarray:
    return prepare_rgb(_pil_to_rgb(Image.open(BytesIO(data))), size=size)


def qc_reason(rgb: np.ndarray) -> str | None:
    """Return a skip reason, or None if the frame may be used.

    Plant/sky scores stay in the manifest. They are not reject rules — brown
    blades and blue lab cards fail a green-only cut.
    """
    height, width = rgb.shape[:2]
    if min(height, width) < MIN_SIDE_PX:
        return "too_small"
    if float(rgb.std()) < MIN_PIXEL_STD:
        return "low_contrast"
    return None


def process_rgb(rgb: np.ndarray, size: int = IMAGE_SIZE) -> tuple[np.ndarray, dict]:
    """QC → optional plant crop → resize. Does not augment."""
    reason = qc_reason(rgb)
    cropped, frac, sky, did_crop = analyze_and_crop(rgb)
    base = {
        "plant_fraction": frac,
        "sky_fraction": sky,
        "cropped": False,
        "src_size": [int(rgb.shape[1]), int(rgb.shape[0])],
    }
    if reason is not None:
        return rgb, {"status": "skipped", "reason": reason, **base}
    out = resize_rgb(cropped, size=size)
    return out, {"status": "kept", "reason": None, **base, "cropped": did_crop}


def augment_rgb(rgb: np.ndarray, kind: str) -> np.ndarray:
    image = Image.fromarray(rgb)
    if kind == "hflip":
        image = ImageOps.mirror(image)
    elif kind == "rot90":
        image = image.rotate(90, expand=False)
    elif kind == "rot270":
        image = image.rotate(270, expand=False)
    elif kind == "zoom":
        w, h = image.size
        inset = int(min(w, h) * 0.1)
        image = image.crop((inset, inset, w - inset, h - inset)).resize(
            (w, h), Image.Resampling.LANCZOS
        )
    else:
        raise ValueError(kind)
    return np.asarray(image, dtype=np.uint8)


def expand_minority_train(
    images: list[np.ndarray],
    labels: list[str],
    min_per_class: int = 80,
) -> tuple[list[np.ndarray], list[str]]:
    """Add flip/rotate/zoom copies for classes below min_per_class. Train only."""
    kinds = ("hflip", "rot90", "rot270", "zoom")
    out_images = list(images)
    out_labels = list(labels)
    by_class: dict[str, list[np.ndarray]] = {}
    for img, lab in zip(images, labels):
        by_class.setdefault(lab, []).append(img)

    for lab, items in by_class.items():
        extra_needed = max(0, min_per_class - len(items))
        if extra_needed == 0:
            continue
        made = 0
        idx = 0
        while made < extra_needed:
            src = items[idx % len(items)]
            kind = kinds[idx % len(kinds)]
            out_images.append(augment_rgb(src, kind))
            out_labels.append(lab)
            made += 1
            idx += 1
    return out_images, out_labels

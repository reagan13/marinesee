"""List, load, resize, and lightly augment RGB images."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageOps

from .dataset_contract import (
    IMAGE_SIZE,
    IMAGE_SUFFIXES,
    TRAIN_VARIANT,
    TRAINABLE_SPECIES,
    classify_folder,
)


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


def list_labeled_images(root: Path) -> list[tuple[Path, str]]:
    """Return (path, slug) for TRAINABLE species and TRAIN_VARIANT only."""
    pairs: list[tuple[Path, str]] = []
    for child in sorted(root.iterdir(), key=lambda p: p.name.lower()):
        if not child.is_dir() or child.name.startswith("."):
            continue
        slug, scope, variant = classify_folder(child.name)
        if scope != "study" or slug not in TRAINABLE_SPECIES:
            continue
        if variant != TRAIN_VARIANT:
            continue
        for path in child.rglob("*"):
            if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES:
                pairs.append((path, slug))
    return pairs


def load_rgb(path: Path, size: int = IMAGE_SIZE) -> np.ndarray:
    image = Image.open(path)
    image = ImageOps.exif_transpose(image)
    image = image.convert("RGB")
    image = image.resize((size, size), Image.Resampling.LANCZOS)
    return np.asarray(image, dtype=np.uint8)


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

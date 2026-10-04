"""Walk a Drive-mounted seagrass root and count images per folder."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any

try:
    from .dataset_contract import IMAGE_SUFFIXES, STUDY_SPECIES, classify_folder
except ImportError:  # `python test_inventory.py` from ml/src
    from dataset_contract import IMAGE_SUFFIXES, STUDY_SPECIES, classify_folder


def is_image(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES


def _is_other_species_dir(folder: Path, child: Path) -> bool:
    """True when a nested folder is a different study/extra class."""
    parent_slug, _, _ = classify_folder(folder.name)
    child_slug, child_scope, _ = classify_folder(child.name)
    return bool(child_slug) and child_scope in {"study", "extra"} and child_slug != parent_slug


def nested_other_species_dirs(folder: Path) -> list[Path]:
    if not folder.is_dir():
        return []
    return [
        child
        for child in folder.iterdir()
        if child.is_dir() and _is_other_species_dir(folder, child)
    ]


def iter_images(folder: Path):
    """Yield images, skipping nested folders that belong to another species."""
    skip = nested_other_species_dirs(folder)
    for path in folder.rglob("*"):
        if not is_image(path):
            continue
        if any(path.is_relative_to(other) for other in skip):
            continue
        yield path


def count_images(folder: Path) -> int:
    """Count images, skipping nested folders that belong to another species.

    Local dumps sometimes nest `Thalassia hemprichii dataset (…)` inside
    Enhalus/Halodule trees. Those must not inflate the parent count.
    """
    return sum(1 for _ in iter_images(folder))


def sample_images(folder: Path, limit: int = 4) -> list[Path]:
    found: list[Path] = []
    for p in iter_images(folder):
        found.append(p)
        if len(found) >= limit:
            break
    return found


def scan_root(root: Path) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    if not root.is_dir():
        raise FileNotFoundError(f"Dataset root not found: {root}")

    for child in sorted(root.iterdir(), key=lambda p: p.name.lower()):
        if not child.is_dir() or child.name.startswith("."):
            continue
        slug, scope, variant = classify_folder(child.name)
        rows.append(
            {
                "folder": child.name,
                "path": str(child),
                "slug": slug,
                "scope": scope,
                "variant": variant,
                "images": count_images(child),
            }
        )

    by_study: dict[str, dict[str, int]] = {
        slug: defaultdict(int) for slug in STUDY_SPECIES
    }
    extra: list[dict[str, Any]] = []
    unknown: list[dict[str, Any]] = []

    for row in rows:
        if row["scope"] == "study" and row["slug"]:
            by_study[row["slug"]][row["variant"]] += row["images"]
        elif row["scope"] == "extra":
            extra.append(row)
        else:
            unknown.append(row)

    missing = [
        slug
        for slug in STUDY_SPECIES
        if sum(by_study[slug].values()) == 0
    ]

    return {
        "root": str(root),
        "folders": rows,
        "by_study": {k: dict(v) for k, v in by_study.items()},
        "extra": extra,
        "unknown": unknown,
        "missing": missing,
    }

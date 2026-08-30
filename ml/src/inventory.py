"""Walk a Drive-mounted seagrass root and count images per folder."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any

from .dataset_contract import IMAGE_SUFFIXES, STUDY_SPECIES, classify_folder


def is_image(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES


def count_images(folder: Path) -> int:
    return sum(1 for p in folder.rglob("*") if is_image(p))


def sample_images(folder: Path, limit: int = 4) -> list[Path]:
    found: list[Path] = []
    for p in folder.rglob("*"):
        if is_image(p):
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

"""QC + resize the v1 `all` set into data/processed/v1 (gitignored JPEGs)."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image

try:
    from .dataset_contract import (
        HELD_OUT_SPECIES,
        IMAGE_SIZE,
        SPLIT_SEED,
        STUDY_SPECIES,
        TRAIN_VARIANT,
        TRAINABLE_SPECIES,
    )
    from .preprocess import PREPROCESS_SPEC, list_labeled_images, load_rgb_full, process_rgb
except ImportError:
    from dataset_contract import (
        HELD_OUT_SPECIES,
        IMAGE_SIZE,
        SPLIT_SEED,
        STUDY_SPECIES,
        TRAIN_VARIANT,
        TRAINABLE_SPECIES,
    )
    from preprocess import PREPROCESS_SPEC, list_labeled_images, load_rgb_full, process_rgb


def repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "ml" / "src").is_dir() and (parent / "docs").is_dir():
            return parent
    return Path.cwd()


def find_dataset_root(explicit: Path | None) -> Path:
    if explicit is not None:
        if not explicit.is_dir():
            raise FileNotFoundError(explicit)
        return explicit
    candidates = [
        repo_root() / "assets" / "species" / "Seagrass",
        Path("/content/drive/MyDrive/Seagrass"),
        Path("/content/drive/My Drive/Seagrass"),
    ]
    for path in candidates:
        if path.is_dir():
            return path
    raise FileNotFoundError("No Seagrass dataset root. Pass --root.")


def dest_name(path: Path, slug: str) -> str:
    digest = hashlib.sha1(f"{slug}:{path.as_posix()}".encode("utf-8")).hexdigest()[:12]
    return f"{path.stem}_{digest}.jpg"


def summarize(rows: list[dict]) -> dict:
    kept = [row for row in rows if row["status"] == "kept"]
    skipped = [row for row in rows if row["status"] == "skipped"]
    by_slug_kept = Counter(row["slug"] for row in kept)
    by_slug_listed = Counter(row["slug"] for row in rows)
    by_reason = Counter(row["reason"] for row in skipped)
    low_plant = sum(1 for row in kept if (row.get("plant_fraction") or 0) < 0.008)
    high_sky = sum(1 for row in kept if (row.get("sky_fraction") or 0) >= 0.50)
    return {
        "listed": len(rows),
        "kept": len(kept),
        "skipped": len(skipped),
        "cropped": sum(1 for row in kept if row.get("cropped")),
        "review_low_plant": low_plant,
        "review_high_sky": high_sky,
        "by_slug_listed": {slug: by_slug_listed[slug] for slug in TRAINABLE_SPECIES},
        "by_slug_kept": {slug: by_slug_kept[slug] for slug in TRAINABLE_SPECIES},
        "skip_reasons": dict(by_reason),
    }


def write_report_md(summary: dict, root: Path, dest: Path) -> str:
    lines = [
        "# SVM v1 preprocess (local)",
        "",
        f"Date: {summary['date']}",
        f"Root: `{root}`",
        f"Dest: `{dest}`",
        "",
        "Paper order: select frames that show leaf → resize 256 → count classes. "
        "Augment stays train-only. *Thalassia* is listed in the hold-out count, not written.",
        "",
        f"- Listed (`all`, eight classes): **{summary['listed']}**",
        f"- Kept: **{summary['kept']}**",
        f"- Skipped: **{summary['skipped']}** `{summary['skip_reasons']}`",
        f"- Plant-crop applied: **{summary['cropped']}**",
        f"- Review (not dropped): low green-mask **{summary['review_low_plant']}**, "
        f"high sky-like top **{summary['review_high_sky']}**",
        f"- Held-out *Thalassia* `all` listed (not written): **{summary['held_out_listed']}**",
        "",
        "| slug | listed | kept |",
        "|------|--------|------|",
    ]
    for slug in TRAINABLE_SPECIES:
        lines.append(
            f"| {slug} | {summary['by_slug_listed'][slug]} | {summary['by_slug_kept'][slug]} |"
        )
    lines.extend(
        [
            "",
            "This laptop dump is **not** the Drive training root "
            "(*H. pinifolia* `all` is 85 here vs 876 on Drive).",
            "",
        ]
    )
    return "\n".join(lines)


def run(
    root: Path,
    dest: Path,
    report_json: Path,
    report_md: Path,
    write_images: bool,
) -> dict:
    dest.mkdir(parents=True, exist_ok=True)
    pairs = list_labeled_images(root)
    held_out = list_labeled_images(root, species=HELD_OUT_SPECIES)
    rows: list[dict] = []

    for index, (path, slug) in enumerate(pairs, start=1):
        record = {
            "src": str(path),
            "slug": slug,
            "dest": None,
            "status": "skipped",
            "reason": "unreadable",
            "plant_fraction": None,
            "cropped": False,
            "src_size": None,
        }
        try:
            rgb = load_rgb_full(path)
        except Exception as exc:
            record["reason"] = f"unreadable:{type(exc).__name__}"
            rows.append(record)
            continue
        out, meta = process_rgb(rgb, size=IMAGE_SIZE)
        record.update(meta)
        if meta["status"] == "kept" and write_images:
            name = dest_name(path, slug)
            out_path = dest / slug / name
            out_path.parent.mkdir(parents=True, exist_ok=True)
            Image.fromarray(out).save(out_path, format="JPEG", quality=92)
            record["dest"] = str(out_path)
        rows.append(record)
        if index % 100 == 0:
            print(f"processed {index}/{len(pairs)}", flush=True)

    summary = summarize(rows)
    summary.update(
        {
            "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "root": str(root),
            "dest": str(dest),
            "write_images": write_images,
            "held_out_listed": len(held_out),
            "held_out_species": list(HELD_OUT_SPECIES),
            "study_species": list(STUDY_SPECIES),
            "trainable_species": list(TRAINABLE_SPECIES),
            "variant": TRAIN_VARIANT,
            "split_seed": SPLIT_SEED,
            "preprocess": PREPROCESS_SPEC,
            "note": (
                "Local dump is not the Drive training root. "
                "H. pinifolia all is smaller here than on Drive."
            ),
        }
    )
    report_json.parent.mkdir(parents=True, exist_ok=True)
    report_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    report_md.write_text(write_report_md(summary, root, dest), encoding="utf-8")
    (dest / "manifest.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    print("kept", summary["kept"], "skipped", summary["skipped"], "held_out", len(held_out))
    print("wrote", report_json)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="MarineSee v1 preprocess (no training).")
    parser.add_argument("--root", type=Path, default=None)
    parser.add_argument("--dest", type=Path, default=None)
    parser.add_argument("--dry-run", action="store_true", help="QC only; do not write JPEGs.")
    args = parser.parse_args()
    root = find_dataset_root(args.root)
    base = repo_root()
    dest = args.dest or (base / "data" / "processed" / "v1")
    run(
        root=root,
        dest=dest,
        report_json=base / "ml" / "artifacts" / "preprocess_v1.json",
        report_md=base / "ml" / "artifacts" / "preprocess_v1.md",
        write_images=not args.dry_run,
    )


if __name__ == "__main__":
    main()

"""Timestamped records for inventory, preprocess, and SVM runs.

Each call writes one folder under ml/artifacts/runs/ and appends
ml/artifacts/run_log.jsonl. The index ml/artifacts/run_log.md is rebuilt
from that log so older runs stay visible.
"""

from __future__ import annotations

import csv
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

_REPORT_SPLITS = ("train", "val", "test")
_SKIP_REPORT_KEYS = {"accuracy", "macro avg", "weighted avg"}


def stamp(now: datetime | None = None) -> tuple[str, str]:
    moment = now or datetime.now(timezone.utc)
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    recorded = moment.strftime("%Y-%m-%dT%H:%M:%SZ")
    run_id = moment.strftime("%Y%m%dT%H%M%S") + f"{moment.microsecond // 1000:03d}Z"
    return recorded, run_id


def environment() -> dict:
    info = {"python": platform.python_version(), "platform": platform.platform()}
    for name in ("numpy", "sklearn", "skimage"):
        try:
            module = __import__(name)
        except ImportError:
            continue
        info[name] = getattr(module, "__version__", "")
    return info


def append_run(repo: Path, record: dict) -> Path:
    """Write one run folder plus the shared jsonl and markdown index."""
    payload = dict(record)
    if "kind" not in payload:
        raise ValueError("record needs kind")
    recorded, run_id = stamp()
    payload.setdefault("recorded_at", recorded)
    payload.setdefault("run_id", run_id)
    payload.setdefault("environment", environment())

    artifacts = repo / "ml" / "artifacts"
    runs = artifacts / "runs"
    runs.mkdir(parents=True, exist_ok=True)
    kind = str(payload["kind"])
    run_dir = runs / f"{payload['run_id']}-{kind}"
    suffix = 2
    while run_dir.exists():
        run_dir = runs / f"{payload['run_id']}-{kind}-{suffix}"
        suffix += 1
    run_dir.mkdir(parents=True)
    payload["run_dir"] = str(run_dir)

    (run_dir / "record.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    (run_dir / "record.md").write_text(to_markdown(payload), encoding="utf-8")
    if any(f"{split}_report" in payload for split in _REPORT_SPLITS):
        _write_scores_csv(run_dir / "scores.csv", payload)
    if isinstance(payload.get("tuning_rows"), list) and payload["tuning_rows"]:
        _write_tuning_csv(run_dir / "tuning.csv", payload["tuning_rows"])

    log_path = artifacts / "run_log.jsonl"
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload) + "\n")
    _write_index(artifacts / "run_log.md", _read_log(log_path))
    print("run record", run_dir)
    return run_dir


def to_markdown(record: dict) -> str:
    lines = [f"# {record.get('kind', 'run')} {record.get('run_id', '')}", ""]
    for key in (
        "recorded_at",
        "started_at",
        "elapsed_seconds",
        "runtime",
        "data_root",
        "max_per_class",
        "split_seed",
        "fit_seconds",
        "best_params",
        "best_val_macro_f1",
        "n_train",
        "n_val",
        "n_test",
        "train_accuracy",
        "val_accuracy",
        "test_accuracy",
        "listed",
        "kept",
        "skipped",
    ):
        if key in record and record[key] is not None:
            lines.append(f"- {key}: {record[key]}")
    note = record.get("loss_note") or record.get("note")
    if note:
        lines.extend(["", str(note)])
    tuning = record.get("tuning_rows")
    if isinstance(tuning, list) and tuning:
        lines.extend(["", "## tuning (top 10 by validation macro F1)", "", _tuning_table(tuning)])
    for split in _REPORT_SPLITS:
        report = record.get(f"{split}_report")
        if isinstance(report, dict):
            lines.extend(["", f"## {split}", "", _report_table(record, report)])
    lines.append("")
    return "\n".join(lines)


def _tuning_table(rows: list[dict]) -> str:
    out = [
        "| kernel | C | gamma | train macro F1 | val macro F1 | val acc | gap |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    ranked = sorted(rows, key=lambda r: r.get("val_macro_f1", 0.0), reverse=True)
    for row in ranked[:10]:
        out.append(
            "| {kernel} | {C} | {gamma} | {tf:.3f} | {vf:.3f} | {va:.3f} | {gap:.3f} |".format(
                kernel=row.get("kernel"),
                C=row.get("C"),
                gamma=row.get("gamma"),
                tf=float(row.get("train_macro_f1", 0.0)),
                vf=float(row.get("val_macro_f1", 0.0)),
                va=float(row.get("val_accuracy", 0.0)),
                gap=float(row.get("f1_gap", 0.0)),
            )
        )
    return "\n".join(out)


def _write_tuning_csv(path: Path, rows: list[dict]) -> None:
    fields = [
        "kernel",
        "C",
        "gamma",
        "train_accuracy",
        "val_accuracy",
        "train_macro_f1",
        "val_macro_f1",
        "f1_gap",
        "fit_seconds",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def _report_table(record: dict, report: dict) -> str:
    labels = list(record.get("classes") or [])
    if not labels:
        labels = [key for key in report if key not in _SKIP_REPORT_KEYS]
    rows = [
        "| slug | precision | recall | f1 | support |",
        "|---|---:|---:|---:|---:|",
    ]
    for slug in [*labels, "macro avg", "weighted avg"]:
        stats = report.get(slug)
        if not isinstance(stats, dict) or "f1-score" not in stats:
            continue
        rows.append(
            "| {slug} | {precision:.3f} | {recall:.3f} | {f1:.3f} | {support} |".format(
                slug=slug,
                precision=float(stats.get("precision") or 0),
                recall=float(stats.get("recall") or 0),
                f1=float(stats["f1-score"]),
                support=stats.get("support", ""),
            )
        )
    return "\n".join(rows)


def _write_scores_csv(path: Path, record: dict) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["split", "slug", "precision", "recall", "f1", "support"])
        labels = list(record.get("classes") or [])
        for split in _REPORT_SPLITS:
            report = record.get(f"{split}_report")
            if not isinstance(report, dict):
                continue
            keys = labels or [key for key in report if key not in _SKIP_REPORT_KEYS]
            for slug in [*keys, "macro avg", "weighted avg"]:
                stats = report.get(slug)
                if not isinstance(stats, dict) or "f1-score" not in stats:
                    continue
                writer.writerow(
                    [
                        split,
                        slug,
                        stats.get("precision"),
                        stats.get("recall"),
                        stats.get("f1-score"),
                        stats.get("support"),
                    ]
                )


def _read_log(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def _write_index(path: Path, rows: list[dict]) -> None:
    lines = [
        "# Run log",
        "",
        "Newest last. Full tables live in each `runs/<id>/record.md`.",
        "",
        "| recorded_at | kind | runtime | detail |",
        "|---|---|---|---|",
    ]
    for record in rows:
        lines.append(
            "| {when} | {kind} | {runtime} | {detail} |".format(
                when=record.get("recorded_at", ""),
                kind=record.get("kind", ""),
                runtime=record.get("runtime", ""),
                detail=_detail(record).replace("|", "/"),
            )
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def _detail(record: dict) -> str:
    kind = record.get("kind")
    if kind == "svm" and record.get("test_accuracy") is not None:
        detail = (
            f"test acc {float(record['test_accuracy']):.3f}"
            f"  fit {record.get('fit_seconds', '')}s"
        )
        params = record.get("best_params")
        if isinstance(params, dict):
            detail += f"  {params.get('kernel')} C={params.get('C')} gamma={params.get('gamma')}"
        if record.get("max_per_class") is not None:
            detail += f"  cap {record['max_per_class']}"
        return detail
    if kind == "preprocess":
        return f"kept {record.get('kept')}/{record.get('listed')}"
    if kind == "inventory":
        missing = record.get("missing") or []
        if missing:
            return "missing " + ", ".join(str(item) for item in missing)
        return str(record.get("root") or record.get("data_root") or "counts")
    return ""

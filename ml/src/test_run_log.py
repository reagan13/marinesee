"""Run-log records stay on disk and keep the F1 table."""

from pathlib import Path

from run_log import append_run


def _svm_record(accuracy: float) -> dict:
    return {
        "kind": "svm",
        "runtime": "local",
        "test_accuracy": accuracy,
        "val_accuracy": 0.2,
        "train_accuracy": 0.9,
        "fit_seconds": 1.5,
        "classes": ["a", "b"],
        "loss_note": "no epoch loss",
        "test_report": {
            "a": {"precision": 0.5, "recall": 0.25, "f1-score": 0.333, "support": 4},
            "b": {"precision": 0.1, "recall": 0.2, "f1-score": 0.133, "support": 5},
            "macro avg": {"precision": 0.3, "recall": 0.225, "f1-score": 0.233, "support": 9},
        },
    }


def test_two_runs_keep_a_history(tmp_path: Path) -> None:
    (tmp_path / "ml" / "artifacts").mkdir(parents=True)
    first = append_run(tmp_path, _svm_record(0.224))
    second = append_run(tmp_path, _svm_record(0.4))
    assert first != second
    assert (first / "record.json").is_file()
    assert "0.333" in (first / "record.md").read_text(encoding="utf-8")
    assert "f1" in (first / "scores.csv").read_text(encoding="utf-8")
    log = (tmp_path / "ml" / "artifacts" / "run_log.jsonl").read_text(encoding="utf-8").strip().splitlines()
    assert len(log) == 2
    index = (tmp_path / "ml" / "artifacts" / "run_log.md").read_text(encoding="utf-8")
    assert index.count("| svm |") == 2
    assert "0.400" in index or "0.40" in index


if __name__ == "__main__":
    import tempfile

    with tempfile.TemporaryDirectory() as raw:
        test_two_runs_keep_a_history(Path(raw))
    print("ok")

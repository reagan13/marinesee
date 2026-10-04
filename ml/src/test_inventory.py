from pathlib import Path

from dataset_contract import classify_folder
from inventory import count_images


def test_nested_thalassia_does_not_inflate_enhalus(tmp_path: Path) -> None:
    parent = tmp_path / "Enhalus acoroides dataset (research-grade)"
    nested = parent / "Thalassia hemprichii dataset (research-grade)"
    nested.mkdir(parents=True)
    (parent / "enhalus.jpg").write_bytes(b"e")
    (nested / "thalassia.jpg").write_bytes(b"t")

    assert classify_folder(parent.name)[0] == "enhalus_acoroides"
    assert classify_folder(nested.name)[0] == "thalassia_hemprichii"
    assert count_images(parent) == 1


if __name__ == "__main__":
    import tempfile

    with tempfile.TemporaryDirectory() as raw:
        test_nested_thalassia_does_not_inflate_enhalus(Path(raw))
    print("ok")

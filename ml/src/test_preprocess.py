from pathlib import Path

import numpy as np
from PIL import Image

from leaf_focus import crop_to_plant, plant_fraction, plant_mask
from preprocess import list_labeled_images, load_rgb_from_bytes, process_rgb, qc_reason


def _green_leaf(size: int = 120) -> np.ndarray:
    frame = np.full((size, size, 3), 220, dtype=np.uint8)
    frame[30:90, 40:80] = (20, 140, 30)
    return frame


def test_nested_other_species_is_not_listed(tmp_path: Path) -> None:
    parent = tmp_path / "Enhalus acoroides dataset (all)"
    nested = parent / "Thalassia hemprichii dataset (all)"
    nested.mkdir(parents=True)
    Image.fromarray(_green_leaf()).save(parent / "enhalus.jpg")
    Image.fromarray(_green_leaf()).save(nested / "thalassia.jpg")
    pairs = list_labeled_images(tmp_path)
    assert len(pairs) == 1
    assert pairs[0][1] == "enhalus_acoroides"


def test_qc_drops_blank_and_keeps_leaf() -> None:
    blank = np.full((80, 80, 3), 200, dtype=np.uint8)
    sand = np.zeros((80, 80, 3), dtype=np.uint8)
    sand[:, :] = (190, 170, 150)
    sand[::2, ::2] = (200, 180, 155)
    leaf = _green_leaf()
    assert qc_reason(blank) == "low_contrast"
    assert qc_reason(sand) is None
    assert qc_reason(leaf) is None
    assert plant_fraction(leaf) > 0.05
    assert plant_mask(leaf).any()


def test_process_resizes_and_can_crop() -> None:
    leaf = _green_leaf(160)
    out, meta = process_rgb(leaf, size=64)
    assert meta["status"] == "kept"
    assert out.shape == (64, 64, 3)
    cropped, did = crop_to_plant(leaf)
    assert did
    assert cropped.shape[0] < leaf.shape[0]


def test_load_rgb_from_bytes() -> None:
    from io import BytesIO

    from PIL import Image

    buf = BytesIO()
    Image.fromarray(_green_leaf(80)).save(buf, format="JPEG")
    rgb = load_rgb_from_bytes(buf.getvalue(), size=32)
    assert rgb.shape == (32, 32, 3)


def test_too_small() -> None:
    tiny = np.zeros((20, 20, 3), dtype=np.uint8)
    tiny[:, :] = (20, 140, 30)
    assert qc_reason(tiny) == "too_small"


if __name__ == "__main__":
    import tempfile

    test_qc_drops_blank_and_keeps_leaf()
    test_process_resizes_and_can_crop()
    test_load_rgb_from_bytes()
    test_too_small()
    with tempfile.TemporaryDirectory() as raw:
        test_nested_other_species_is_not_listed(Path(raw))
    print("ok")

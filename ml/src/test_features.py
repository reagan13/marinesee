"""Feature vector length is fixed and finite for leaf, blank, and noise frames."""

import numpy as np

from features import FEATURE_SPEC, extract_vector


def _frames() -> dict[str, np.ndarray]:
    rng = np.random.default_rng(0)
    leaf = np.full((256, 256, 3), (190, 170, 150), dtype=np.uint8)
    leaf[20:236, 120:136] = (30, 150, 40)
    leaf[40:220, 60:70] = (35, 140, 45)
    return {
        "leaf": leaf,
        "blank": np.full((256, 256, 3), 200, dtype=np.uint8),
        "noise": rng.integers(0, 256, size=(256, 256, 3), dtype=np.uint8),
    }


def test_length_and_finite() -> None:
    for name, frame in _frames().items():
        vector = extract_vector(frame)
        assert vector.shape == (FEATURE_SPEC["length"],), name
        assert np.isfinite(vector).all(), name


def test_blade_width_tracks_the_blade() -> None:
    narrow = np.full((256, 256, 3), (190, 170, 150), dtype=np.uint8)
    narrow[20:236, 124:130] = (30, 150, 40)
    wide = np.full((256, 256, 3), (190, 170, 150), dtype=np.uint8)
    wide[20:236, 100:150] = (30, 150, 40)
    width_index = FEATURE_SPEC["blade_width_index"]
    assert extract_vector(wide)[width_index] > extract_vector(narrow)[width_index]


if __name__ == "__main__":
    test_length_and_finite()
    test_blade_width_tracks_the_blade()
    print("ok")

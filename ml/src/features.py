"""Color, GLCM texture, and simple blade/shape features for the SVM."""

from __future__ import annotations

import numpy as np
from skimage.color import rgb2gray, rgb2hsv
from skimage.feature import graycomatrix, graycoprops
from skimage.filters import threshold_otsu
from skimage.measure import label, regionprops
from skimage.transform import resize

FEATURE_SPEC = {
    "version": "v1",
    "color": "hsv_hist_16x3",
    "texture": "glcm_64px_d1_d2_4angles_4props",
    "shape": "largest_blob_6",
    "glcm_size": 64,
}

_BINS = 16
_GLCM_SIZE = 64
_LEVELS = 32
_DISTANCES = (1, 2)
_ANGLES = (0.0, np.pi / 4, np.pi / 2, 3 * np.pi / 4)
_GLCM_PROPS = ("contrast", "homogeneity", "energy", "correlation")


def _color_histogram(rgb: np.ndarray) -> np.ndarray:
    hsv = rgb2hsv(rgb.astype(np.float64) / 255.0)
    parts = []
    for channel in range(3):
        hist, _ = np.histogram(hsv[:, :, channel], bins=_BINS, range=(0.0, 1.0), density=True)
        parts.append(hist.astype(np.float64))
    return np.concatenate(parts)


def _glcm_features(gray_u8: np.ndarray) -> np.ndarray:
    small = resize(
        gray_u8,
        (_GLCM_SIZE, _GLCM_SIZE),
        preserve_range=True,
        anti_aliasing=True,
    ).astype(np.uint8)
    quantized = np.clip(small.astype(np.uint16) * (_LEVELS - 1) // 255, 0, _LEVELS - 1).astype(
        np.uint8
    )
    matrix = graycomatrix(
        quantized,
        distances=_DISTANCES,
        angles=_ANGLES,
        levels=_LEVELS,
        symmetric=True,
        normed=True,
    )
    values = [graycoprops(matrix, prop).ravel() for prop in _GLCM_PROPS]
    return np.concatenate(values).astype(np.float64)


def _shape_features(gray_u8: np.ndarray) -> np.ndarray:
    empty = np.zeros(6, dtype=np.float64)
    try:
        thresh = threshold_otsu(gray_u8)
    except ValueError:
        return empty
    mask = gray_u8 < thresh
    labeled = label(mask)
    if labeled.max() == 0:
        mask = ~mask
        labeled = label(mask)
    if labeled.max() == 0:
        return empty
    regions = regionprops(labeled)
    region = max(regions, key=lambda r: r.area)
    y0, x0, y1, x1 = region.bbox
    height = max(y1 - y0, 1)
    width = max(x1 - x0, 1)
    circularity = 0.0
    if region.perimeter > 0:
        circularity = float(4.0 * np.pi * region.area / (region.perimeter**2))
    return np.array(
        [
            float(region.area) / gray_u8.size,
            float(region.perimeter) / (gray_u8.shape[0] + gray_u8.shape[1]),
            circularity,
            width / height,
            float(region.solidity),
            float(region.extent),
        ],
        dtype=np.float64,
    )


def extract_vector(rgb: np.ndarray) -> np.ndarray:
    gray = (rgb2gray(rgb) * 255.0).astype(np.uint8)
    return np.concatenate(
        [
            _color_histogram(rgb),
            _glcm_features(gray),
            _shape_features(gray),
        ]
    )


def extract_batch(images: list[np.ndarray]) -> np.ndarray:
    if not images:
        return np.zeros((0, 0), dtype=np.float64)
    return np.stack([extract_vector(img) for img in images], axis=0)

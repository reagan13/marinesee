"""Color histograms, GLCM texture, and blade shape features for the SVM.

Input is the prepared image from preprocess.prepare_rgb (plant crop, then
256px RGB). Training and identify must both call extract_vector on that.

v2 is the locked description: the validation search on 13 Oct 2026 picked
RBF C=3, gamma=0.01 on this vector (run 20261013T144233395Z).
"""

from __future__ import annotations

import numpy as np
from scipy.ndimage import distance_transform_edt
from skimage.color import rgb2gray, rgb2hsv
from skimage.feature import graycomatrix, graycoprops
from skimage.filters import threshold_otsu
from skimage.measure import label, regionprops
from skimage.morphology import skeletonize
from skimage.transform import resize

try:
    from .leaf_focus import plant_mask
except ImportError:
    from leaf_focus import plant_mask

_BINS = 16
_GLCM_SIZE = 128
_LEVELS = 32
_DISTANCES = (1, 2, 4)
_ANGLES = (0.0, np.pi / 4, np.pi / 2, 3 * np.pi / 4)
_GLCM_PROPS = ("contrast", "dissimilarity", "homogeneity", "energy", "correlation", "ASM")
_MIN_BLOB_PX = 20
_MIN_PLANT_FRACTION = 0.01
_SHAPE_LEN = 10
_COLOR_LEN = 3 * _BINS * 2 + 6
_GLCM_LEN = len(_GLCM_PROPS) * len(_DISTANCES) * 2
_BLADE_WIDTH_AT = 6

FEATURE_SPEC = {
    "version": "v2",
    "input": "plant crop, then 256px RGB",
    "color": "hsv_hist_16x3 frame + hsv_hist_16x3 plant pixels + hsv mean/std plant pixels",
    "texture": "glcm_128px_32lv_d1_d2_d4_6props_angle_mean_and_range",
    "shape": "plant_mask_blobs_and_blade_width_10",
    "glcm_size": _GLCM_SIZE,
    "length": _COLOR_LEN + _GLCM_LEN + _SHAPE_LEN,
    "blade_width_index": _COLOR_LEN + _GLCM_LEN + _BLADE_WIDTH_AT,
    "locked_svm": {"kernel": "rbf", "C": 3.0, "gamma": 0.01},
}


def _hsv_histogram(hsv_pixels: np.ndarray) -> np.ndarray:
    if hsv_pixels.size == 0:
        return np.zeros(3 * _BINS, dtype=np.float64)
    parts = []
    for channel in range(3):
        hist, _ = np.histogram(hsv_pixels[:, channel], bins=_BINS, range=(0.0, 1.0))
        parts.append(hist.astype(np.float64) / float(len(hsv_pixels)))
    return np.concatenate(parts)


def _color_features(rgb: np.ndarray, mask: np.ndarray) -> np.ndarray:
    hsv = rgb2hsv(rgb.astype(np.float64) / 255.0)
    frame = hsv.reshape(-1, 3)
    plant = hsv[mask]
    moments = (
        np.concatenate([plant.mean(axis=0), plant.std(axis=0)])
        if len(plant)
        else np.zeros(6, dtype=np.float64)
    )
    return np.concatenate([_hsv_histogram(frame), _hsv_histogram(plant), moments])


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
    values = []
    for prop in _GLCM_PROPS:
        table = graycoprops(matrix, prop)
        values.append(table.mean(axis=1))
        values.append(np.ptp(table, axis=1))
    return np.nan_to_num(np.concatenate(values).astype(np.float64))


def _shape_mask(rgb: np.ndarray, gray_u8: np.ndarray) -> tuple[np.ndarray, bool]:
    """Green plant mask; Otsu fallback when blades are brown or pale."""
    mask = plant_mask(rgb)
    if mask.mean() >= _MIN_PLANT_FRACTION:
        return mask, False
    try:
        thresh = threshold_otsu(gray_u8)
    except ValueError:
        return mask, True
    dark = gray_u8 < thresh
    return (dark if dark.mean() <= 0.5 else ~dark), True


def _shape_features(mask: np.ndarray, used_fallback: bool) -> np.ndarray:
    out = np.zeros(_SHAPE_LEN, dtype=np.float64)
    side = float(max(mask.shape))
    out[0] = float(mask.mean())
    out[9] = 1.0 if used_fallback else 0.0
    regions = [r for r in regionprops(label(mask)) if r.area >= _MIN_BLOB_PX]
    if not regions:
        return out
    clean = np.zeros_like(mask, dtype=bool)
    for region in regions:
        clean[tuple(region.coords.T)] = True
    areas = np.array([r.area for r in regions], dtype=np.float64)
    weights = areas / areas.sum()
    elongation = np.array(
        [
            np.log1p(min(r.axis_major_length / max(r.axis_minor_length, 1.0), 50.0))
            for r in regions
        ]
    )
    out[1] = np.log1p(len(regions))
    out[2] = float(np.dot(weights, [r.eccentricity for r in regions]))
    out[3] = float(np.dot(weights, [r.solidity for r in regions]))
    out[4] = float(np.dot(weights, [r.extent for r in regions]))
    out[5] = float(np.dot(weights, elongation))
    skeleton = skeletonize(clean)
    if skeleton.any():
        widths = 2.0 * distance_transform_edt(clean)[skeleton]
        q25, q50, q75 = np.percentile(widths, [25, 50, 75])
        out[_BLADE_WIDTH_AT] = q50 / side
        out[7] = (q75 - q25) / side
        out[8] = float(skeleton.sum()) / float(clean.sum())
    return out


def extract_vector(rgb: np.ndarray) -> np.ndarray:
    gray = (rgb2gray(rgb) * 255.0).astype(np.uint8)
    mask, used_fallback = _shape_mask(rgb, gray)
    return np.concatenate(
        [
            _color_features(rgb, plant_mask(rgb)),
            _glcm_features(gray),
            _shape_features(mask, used_fallback),
        ]
    )


def extract_batch(images: list[np.ndarray]) -> np.ndarray:
    if not images:
        return np.zeros((0, FEATURE_SPEC["length"]), dtype=np.float64)
    return np.stack([extract_vector(img) for img in images], axis=0)

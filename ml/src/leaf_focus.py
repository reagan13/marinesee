"""Plant-visible mask and optional crop. IMPLEMENTATION, not a paper formula.

Paper step 1 is “select images that actually show leaf shape, blade width, color.”
A hard green-pixel cut drops real blades (brown *Halophila*, pale wrack, lab cards).
So the mask is a diagnostic + optional zoom, not a reject rule.

Masks run on a 512px preview so iNaturalist originals do not grind the laptop.
"""

from __future__ import annotations

import numpy as np
from skimage.color import rgb2hsv
from skimage.transform import resize

ANALYZE_MAX_SIDE = 512

_EXG_MIN = 20
_HUE_LO = 0.16
_HUE_HI = 0.50
_SAT_MIN = 0.12
_VAL_LO = 0.08
_VAL_HI = 0.92

CROP_PAD = 0.15
CROP_MIN_AREA = 0.02
CROP_MAX_AREA = 0.90
CROP_MIN_SIDE = 16


def for_analysis(rgb: np.ndarray) -> tuple[np.ndarray, float, float]:
    """Return (preview, scale_x, scale_y) mapping preview pixels → original."""
    height, width = rgb.shape[:2]
    longest = max(height, width)
    if longest <= ANALYZE_MAX_SIDE:
        return rgb, 1.0, 1.0
    scale = ANALYZE_MAX_SIDE / float(longest)
    new_h = max(1, int(round(height * scale)))
    new_w = max(1, int(round(width * scale)))
    small = resize(
        rgb,
        (new_h, new_w),
        preserve_range=True,
        anti_aliasing=True,
    ).astype(np.uint8)
    return small, width / float(new_w), height / float(new_h)


def plant_mask(rgb: np.ndarray) -> np.ndarray:
    red = rgb[:, :, 0].astype(np.int16)
    green = rgb[:, :, 1].astype(np.int16)
    blue = rgb[:, :, 2].astype(np.int16)
    excess_green = (2 * green) - red - blue
    hsv = rgb2hsv(rgb.astype(np.float64) / 255.0)
    hue, sat, val = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]
    greenish = (
        (hue >= _HUE_LO)
        & (hue <= _HUE_HI)
        & (sat >= _SAT_MIN)
        & (val >= _VAL_LO)
        & (val <= _VAL_HI)
    )
    return (excess_green >= _EXG_MIN) & greenish


def plant_fraction(rgb: np.ndarray) -> float:
    small, _, _ = for_analysis(rgb)
    mask = plant_mask(small)
    if mask.size == 0:
        return 0.0
    return float(mask.mean())


def sky_fraction(rgb: np.ndarray) -> float:
    """Share of the top third that looks like open sky. Diagnostic only."""
    small, _, _ = for_analysis(rgb)
    top = small[: max(1, small.shape[0] // 3)]
    hsv = rgb2hsv(top.astype(np.float64) / 255.0)
    hue, sat, val = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]
    blue_sky = (hue >= 0.50) & (hue <= 0.75) & (val >= 0.55)
    white_sky = (sat <= 0.12) & (val >= 0.78)
    return float((blue_sky | white_sky).mean())


def _crop_from_mask(
    rgb: np.ndarray,
    mask: np.ndarray,
    scale_x: float,
    scale_y: float,
) -> tuple[np.ndarray, bool]:
    if mask.size == 0 or not mask.any():
        return rgb, False
    rows = np.where(mask.any(axis=1))[0]
    cols = np.where(mask.any(axis=0))[0]
    if len(rows) == 0 or len(cols) == 0:
        return rgb, False
    y0, y1 = int(rows[0]), int(rows[-1]) + 1
    x0, x1 = int(cols[0]), int(cols[-1]) + 1
    small_h, small_w = mask.shape[:2]
    area_frac = float((y1 - y0) * (x1 - x0)) / float(small_h * small_w)
    if area_frac < CROP_MIN_AREA or area_frac > CROP_MAX_AREA:
        return rgb, False
    pad_y = int(round((y1 - y0) * CROP_PAD))
    pad_x = int(round((x1 - x0) * CROP_PAD))
    top = max(0, int((y0 - pad_y) * scale_y))
    left = max(0, int((x0 - pad_x) * scale_x))
    bottom = min(rgb.shape[0], int((y1 + pad_y) * scale_y))
    right = min(rgb.shape[1], int((x1 + pad_x) * scale_x))
    if bottom - top < CROP_MIN_SIDE or right - left < CROP_MIN_SIDE:
        return rgb, False
    return rgb[top:bottom, left:right], True


def crop_to_plant(rgb: np.ndarray) -> tuple[np.ndarray, bool]:
    """Zoom to the plant-mask bbox when it is a mid-size region. Else full frame."""
    small, scale_x, scale_y = for_analysis(rgb)
    return _crop_from_mask(rgb, plant_mask(small), scale_x, scale_y)


def analyze_and_crop(rgb: np.ndarray) -> tuple[np.ndarray, float, float, bool]:
    """One preview pass: plant fraction, sky fraction, optional crop."""
    small, scale_x, scale_y = for_analysis(rgb)
    mask = plant_mask(small)
    frac = float(mask.mean()) if mask.size else 0.0
    top = small[: max(1, small.shape[0] // 3)]
    hsv = rgb2hsv(top.astype(np.float64) / 255.0)
    hue, sat, val = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]
    blue_sky = (hue >= 0.50) & (hue <= 0.75) & (val >= 0.55)
    white_sky = (sat <= 0.12) & (val >= 0.78)
    sky = float((blue_sky | white_sky).mean())
    cropped, did = _crop_from_mask(rgb, mask, scale_x, scale_y)
    return cropped, frac, sky, did

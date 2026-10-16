"""Day-night pass on the FULL-FRAME 3D meadow — no stacked strips.

Keeps the real meadow/fish clip as the whole frame. Sky, sun, and moon are
soft-blended into that same image (one orb, looping motion).
"""

from __future__ import annotations

import math
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

FFMPEG = (
    r"C:\Users\reaga\AppData\Local\Microsoft\WinGet\Packages"
    r"\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
    r"\ffmpeg-9.0.1-full_build\bin\ffmpeg.exe"
)
ROOT = Path(r"d:\pepot\marinesee\assets\models-3d")
SOURCE = ROOT / "_source" / "cymodocea_rotundata_meadow.mp4"
PUBLISH = ROOT / "cymodocea_rotundata_growth.mp4"
APP = Path(r"d:\pepot\marinesee\app\assets\models-3d\cymodocea_rotundata_growth.mp4")
TMP = ROOT / "_cycle_tmp"
W, H = 1280, 720
FPS = 24
SECONDS = 30
N = FPS * SECONDS
BLEND_LO = 36.0
BLEND_HI = 310.0


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd[:6]), "...")
    subprocess.check_call(cmd)


def lerp(a: float, b: float, u: float) -> float:
    return a + (b - a) * u


def smooth(u: float) -> float:
    u = min(1.0, max(0.0, u))
    return u * u * (3.0 - 2.0 * u)


def key_lerp(t: float, keys: list[tuple[float, float]]) -> float:
    if t <= keys[0][0]:
        return keys[0][1]
    for i in range(1, len(keys)):
        t0, v0 = keys[i - 1]
        t1, v1 = keys[i]
        if t <= t1:
            u = smooth((t - t0) / (t1 - t0) if t1 != t0 else 0.0)
            return lerp(v0, v1, u)
    return keys[-1][1]


def tod(t: float) -> tuple[float, float, float]:
    """day, dusk, night weights. Periodic."""
    def g(mu: float, sig: float) -> float:
        d = min(abs(t - mu), 1.0 - abs(t - mu))
        return math.exp(-0.5 * (d / sig) ** 2)

    day = g(0.22, 0.14) + 0.35 * g(0.0, 0.06)
    dusk = g(0.0, 0.07) + g(0.52, 0.08) + g(0.96, 0.06)
    night = g(0.78, 0.11)
    s = day + dusk + night + 1e-6
    return day / s, dusk / s, night / s


def sun_state(t: float) -> tuple[float, float, float, tuple[float, float, float], float]:
    s = key_lerp(
        t,
        [
            (0.00, 0.06),
            (0.18, 0.28),
            (0.36, 0.50),
            (0.52, 0.82),
            (0.62, 0.98),
            (0.90, 0.00),
            (1.00, 0.06),
        ],
    )
    vis = key_lerp(
        t,
        [
            (0.00, 0.85),
            (0.06, 1.00),
            (0.58, 1.00),
            (0.66, 0.00),
            (0.90, 0.00),
            (1.00, 0.85),
        ],
    )
    if vis <= 0.01:
        return 0.0, 0.0, 0.0, (255.0, 255.0, 255.0), 0.0
    horizon = 188.0
    x = lerp(0.10 * W, 0.88 * W, s)
    y = horizon - (horizon - 54.0) * math.sin(math.pi * min(1.0, max(0.0, s)))
    warm = min(
        1.0,
        math.exp(-((s - 0.0) / 0.16) ** 2) + math.exp(-((s - 1.0) / 0.16) ** 2),
    )
    color = (255.0, lerp(250.0, 168.0, warm), lerp(236.0, 78.0, warm))
    radius = lerp(20.0, 32.0, math.sin(math.pi * min(1.0, max(0.0, s))))
    return x, y, vis, color, radius


def moon_state(t: float) -> tuple[float, float, float, float]:
    vis = key_lerp(
        t,
        [
            (0.00, 0.00),
            (0.62, 0.00),
            (0.70, 1.00),
            (0.88, 1.00),
            (0.96, 0.00),
            (1.00, 0.00),
        ],
    )
    if vis <= 0.01:
        return 0.0, 0.0, 0.0, 0.0
    s = key_lerp(t, [(0.00, 0.0), (0.62, 0.0), (0.78, 0.45), (0.94, 0.72), (1.00, 0.0)])
    x = lerp(0.78 * W, 0.28 * W, s)
    y = 188.0 - 120.0 * math.sin(math.pi * min(1.0, max(0.0, s + 0.08)))
    return x, y, vis, 28.0


def sky_ends(t: float) -> tuple[np.ndarray, np.ndarray]:
    wd, wdu, wn = tod(t)
    day_top = np.array([186.0, 226.0, 242.0], dtype=np.float32)
    day_bot = np.array([154.0, 206.0, 224.0], dtype=np.float32)
    dusk_top = np.array([92.0, 78.0, 126.0], dtype=np.float32)
    dusk_bot = np.array([255.0, 168.0, 102.0], dtype=np.float32)
    night_top = np.array([8.0, 14.0, 32.0], dtype=np.float32)
    night_bot = np.array([18.0, 32.0, 58.0], dtype=np.float32)
    top = wd * day_top + wdu * dusk_top + wn * night_top
    bot = wd * day_bot + wdu * dusk_bot + wn * night_bot
    return top, bot


def stamp_orb(
    canvas: np.ndarray,
    cx: float,
    cy: float,
    radius: float,
    color: tuple[float, float, float],
    alpha: float,
    glow: float = 2.2,
) -> None:
    if alpha <= 0.01 or radius <= 1:
        return
    yy, xx = np.ogrid[:H, :W]
    dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    core = np.clip((radius - dist) / 1.6, 0.0, 1.0)
    glow_m = np.exp(-((dist / (radius * glow)) ** 2))
    a = np.clip(core + 0.55 * glow_m, 0.0, 1.0) * alpha
    a3 = a[:, :, None]
    col = np.array(color, dtype=np.float32).reshape(1, 1, 3)
    canvas[:] = canvas * (1.0 - a3) + col * a3


def remove_baked_orb(frame: np.ndarray, cx: float, cy: float, r: float) -> np.ndarray:
    r = r + 18.0
    yy, xx = np.ogrid[:H, :W]
    dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    luma = 0.2126 * frame[:, :, 0] + 0.7152 * frame[:, :, 1] + 0.0722 * frame[:, :, 2]
    safe = (yy < int(H * 0.48)) & (luma < 190.0) & (dist > r + 10.0)
    if safe.sum() < 80:
        safe = (yy < int(H * 0.35)) & (dist > r + 10.0)
    fill = (
        frame[safe].mean(axis=0)
        if safe.sum()
        else frame[24:90, 24:140].mean(axis=(0, 1))
    )
    patched = frame.copy()
    hole = dist <= r
    patched[hole] = fill
    x0, x1 = max(0, int(cx - r - 24)), min(W, int(cx + r + 24))
    y0, y1 = max(0, int(cy - r - 24)), min(H, int(cy + r + 24))
    crop = np.clip(patched[y0:y1, x0:x1], 0, 255).astype(np.uint8)
    blur = np.asarray(
        Image.fromarray(crop).filter(ImageFilter.GaussianBlur(10)),
        dtype=np.float32,
    )
    patched[y0:y1, x0:x1] = blur
    m = np.clip((r + 16.0 - dist) / 22.0, 0.0, 1.0)[:, :, None]
    return frame * (1.0 - m) + patched * m


def find_orb(frame: np.ndarray) -> tuple[float, float, float]:
    luma = 0.2126 * frame[:, :, 0] + 0.7152 * frame[:, :, 1] + 0.0722 * frame[:, :, 2]
    yy, xx = np.ogrid[:H, :W]
    mask = (luma > 238) & (yy < int(H * 0.55))
    if mask.sum() < 40:
        return 0.62 * W, 0.22 * H, 46.0
    ys, xs = np.nonzero(mask)
    cx, cy = float(xs.mean()), float(ys.mean())
    r = float(np.quantile(np.sqrt((xs - cx) ** 2 + (ys - cy) ** 2), 0.92)) * 1.8 + 16.0
    return cx, cy, r


def make_sky(t: float) -> np.ndarray:
    top, bot = sky_ends(t)
    y = np.linspace(0.0, 1.0, H, dtype=np.float32)[:, None]
    sky = top.reshape(1, 1, 3) * (1.0 - y[:, :, None]) + bot.reshape(1, 1, 3) * y[:, :, None]
    sky = np.broadcast_to(sky, (H, W, 3)).copy()

    rng = np.random.default_rng(7)
    wd, wdu, wn = tod(t)
    cloud_a = (0.22 * wd + 0.18 * wdu) * (1.0 - wn)
    if cloud_a > 0.04:
        for i, (bx, by, rx, ry) in enumerate(
            (
                (0.22, 0.10, 210, 48),
                (0.55, 0.07, 160, 36),
                (0.78, 0.13, 190, 42),
                (0.40, 0.16, 90, 22),
            )
        ):
            drift = 70.0 * math.sin(2.0 * math.pi * t + i)
            cx = (bx * W + drift) % W
            cy = by * H + 6.0 * math.sin(2.0 * math.pi * t * 0.5 + i)
            yy, xx = np.ogrid[:H, :W]
            # wrap-friendly-ish horizontal
            dx = np.minimum(np.abs(xx - cx), W - np.abs(xx - cx)) / rx
            dy = (yy - cy) / ry
            blob = np.exp(-(dx * dx + dy * dy))
            col = np.array([246.0, 248.0, 252.0] if wd > wdu else [255.0, 210.0, 176.0])
            a = (blob * cloud_a)[:, :, None]
            sky = sky * (1.0 - a) + col.reshape(1, 1, 3) * a

    if wn > 0.15:
        stars = rng.random((H, W))
        spec = (stars > 0.996).astype(np.float32)
        tw = 0.75 + 0.25 * math.sin(2.0 * math.pi * t * 4.0)
        sky += spec[:, :, None] * (220.0 * tw * wn)
    return np.clip(sky, 0, 255)


def sky_mask() -> np.ndarray:
    yy = np.arange(H, dtype=np.float32)[:, None]
    u = np.clip((yy - BLEND_LO) / (BLEND_HI - BLEND_LO), 0.0, 1.0)
    # Soft fade — never a hard cut, and never 100% sky so the 3D water stays in the shot.
    fade = 1.0 - (u * u * (3.0 - 2.0 * u))
    return (0.70 * fade).astype(np.float32)


def grade_scene(frame: np.ndarray, t: float) -> np.ndarray:
    wd, wdu, wn = tod(t)
    f = frame.astype(np.float32)
    dusk = f * np.array([1.06, 0.90, 0.78], dtype=np.float32)
    night = f * np.array([0.42, 0.52, 0.78], dtype=np.float32) + np.array(
        [4.0, 10.0, 22.0], dtype=np.float32
    )
    return wd * f + wdu * dusk + wn * night


def main() -> int:
    if not SOURCE.exists():
        raise FileNotFoundError(SOURCE)
    TMP.mkdir(parents=True, exist_ok=True)
    raw_path = TMP / "full.raw"
    if not raw_path.exists() or raw_path.stat().st_size != N * H * W * 3:
        run(
            [
                FFMPEG,
                "-y",
                "-i",
                str(SOURCE),
                "-vf",
                f"fps={FPS},format=rgb24",
                "-f",
                "rawvideo",
                str(raw_path),
            ]
        )
    src = np.memmap(raw_path, dtype=np.uint8, mode="r", shape=(N, H, W, 3))
    mask = sky_mask()
    out_raw = TMP / "out2.raw"
    out = np.memmap(out_raw, dtype=np.uint8, mode="w+", shape=(N, H, W, 3))
    print("render", N, flush=True)
    for i in range(N):
        t = i / N
        sky = make_sky(t)
        scene = grade_scene(np.array(src[i], dtype=np.float32), t)
        yy, xx = np.ogrid[:H, :W]
        hot = (xx - 674.0) ** 2 + (yy - 204.0) ** 2 <= 110.0 ** 2
        scene[hot] = sky[hot]
        m = mask[:, :, None]
        frame = sky * m + scene * (1.0 - m)
        sx, sy, svis, scolor, srad = sun_state(t)
        mx, my, mvis, mrad = moon_state(t)
        if svis > 0:
            stamp_orb(frame, sx, sy, srad, scolor, svis)
        elif mvis > 0:
            stamp_orb(frame, mx, my, mrad, (246.0, 248.0, 255.0), mvis, glow=2.0)
        out[i] = np.clip(frame, 0, 255).astype(np.uint8)
        if i % 72 == 0:
            print(f"  {i}/{N}", flush=True)

    first = np.array(out[0], copy=True)
    for k in range(16):
        u = (k + 1) / 16
        idx = N - 16 + k
        out[idx] = np.clip((1.0 - u) * out[idx] + u * first, 0, 255).astype(np.uint8)
    Image.fromarray(np.array(out[0])).save(TMP / "f0.jpg", quality=88)
    Image.fromarray(np.array(out[120])).save(TMP / "f5.jpg", quality=88)
    Image.fromarray(np.array(out[360])).save(TMP / "f15.jpg", quality=88)
    Image.fromarray(np.array(out[540])).save(TMP / "f22.jpg", quality=88)
    Image.fromarray(np.array(out[N - 1])).save(TMP / "f29.jpg", quality=88)
    out.flush()
    del out

    mp4 = TMP / "blend.mp4"
    run(
        [
            FFMPEG,
            "-y",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "rgb24",
            "-s",
            f"{W}x{H}",
            "-r",
            str(FPS),
            "-i",
            str(out_raw),
            "-i",
            str(SOURCE),
            "-map",
            "0:v:0",
            "-map",
            "1:a:0?",
            "-c:v",
            "libx264",
            "-crf",
            "18",
            "-preset",
            "veryfast",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "copy",
            "-shortest",
            str(mp4),
        ]
    )
    shutil.copy2(mp4, PUBLISH)
    shutil.copy2(mp4, APP)
    print("published", PUBLISH.stat().st_size)
    return 0


if __name__ == "__main__":
    sys.exit(main())

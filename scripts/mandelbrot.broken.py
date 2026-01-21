#!/usr/bin/env python3
"""
mandelbrot.py — sharp Mandelbrot renderer (smooth coloring + anti-alias)

Usage examples:
  python mandelbrot.py
  python mandelbrot.py --width 1600 --height 1000 --max-iter 800
  python mandelbrot.py --center -0.7435 0.1314 --zoom 0.002 --max-iter 1200
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image


@dataclass
class View:
    cx: float = -0.5
    cy: float = 0.0
    zoom: float = 1.0  # smaller = more zoomed in (window width ~ 3.5*zoom)
    max_iter: int = 400


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--width", type=int, default=1200)
    p.add_argument("--height", type=int, default=800)
    p.add_argument("--max-iter", type=int, default=600)
    p.add_argument("--center", nargs=2, type=float, metavar=("CX", "CY"), default=[-0.5, 0.0])
    p.add_argument("--zoom", type=float, default=1.0)
    p.add_argument("--aa", type=int, default=2, help="Anti-alias factor (1=off, 2 or 3 recommended)")
    p.add_argument("--out", type=str, default="mandelbrot.png")
    return p.parse_args()


def smooth_iter_count(z: np.ndarray, it: np.ndarray) -> np.ndarray:
    """
    Continuous (smooth) iteration count:
    nu = n + 1 - log(log|z|)/log(2)
    Only valid for points that escaped (|z|>2).
    """
    # Avoid log(0) warnings by clipping a bit
    mag = np.abs(z)
    mag = np.clip(mag, 1e-12, None)
    return it + 1.0 - np.log(np.log(mag)) / math.log(2.0)


def palette(t: np.ndarray) -> np.ndarray:
    """
    Simple high-contrast palette.
    t should be normalized [0..1].
    Returns uint8 RGB array.
    """
    # Smooth polynomial palette (nice without needing matplotlib)
    r = 9 * (1 - t) * t**3
    g = 15 * (1 - t) ** 2 * t**2
    b = 8.5 * (1 - t) ** 3 * t
    rgb = np.stack([r, g, b], axis=-1)
    rgb = np.clip(rgb * 255.0, 0, 255).astype(np.uint8)
    return rgb


def render(width: int, height: int, view: View) -> np.ndarray:
    # Window spans: typical Mandelbrot view width ~ 3.5
    span_x = 3.5 * view.zoom
    span_y = span_x * (height / width)
print(f"DEBUG span_x={span_x} span_y={span_y} center=({view.cx},{view.cy}) zoom={view.zoom}")

    x = np.linspace(view.cx - span_x / 2, view.cx + span_x / 2, width, dtype=np.float64)
    y = np.linspace(view.cy - span_y / 2, view.cy + span_y / 2, height, dtype=np.float64)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y

    Z = np.zeros_like(C)
    it = np.zeros(C.shape, dtype=np.int32)

    mask = np.ones(C.shape, dtype=bool)

    for i in range(view.max_iter):
        Z[mask] = Z[mask] * Z[mask] + C[mask]
        escaped = np.abs(Z) > 2.0
        newly_escaped = escaped & mask
        it[newly_escaped] = i
        mask &= ~escaped
        if not mask.any():
            break

    # Smooth coloring for escaped points
    escaped_any = it > 0
    nu = np.zeros(C.shape, dtype=np.float64)

    nu[escaped_any] = smooth_iter_count(Z[escaped_any], it[escaped_any].astype(np.float64))

    # Normalize: use max over escaped pixels so palette fills nicely
    max_nu = nu[escaped_any].max() if escaped_any.any() else 1.0
    t = np.zeros_like(nu)
    t[escaped_any] = nu[escaped_any] / max_nu

    rgb = palette(t)

    # Interior (didn't escape): make it black
    rgb[mask] = np.array([0, 0, 0], dtype=np.uint8)

    return rgb


def downsample(rgb: np.ndarray, aa: int) -> np.ndarray:
    """Box downsample by factor aa (expects rgb shape HxWx3)."""
    if aa <= 1:
        return rgb
    h, w, c = rgb.shape
    h2 = (h // aa) * aa
    w2 = (w // aa) * aa
    rgb = rgb[:h2, :w2, :]
    # reshape and average
    rgb = rgb.reshape(h2 // aa, aa, w2 // aa, aa, c).mean(axis=(1, 3))
    return np.clip(rgb, 0, 255).astype(np.uint8)


def main() -> None:
    args = parse_args()
    view = View(
        cx=float(args.center[0]),
        cy=float(args.center[1]),
        zoom=float(args.zoom),
        max_iter=int(args.max_iter),
    )

    aa = max(1, int(args.aa))
    w_hi = args.width * aa
    h_hi = args.height * aa

    rgb_hi = render(w_hi, h_hi, view)
    rgb = downsample(rgb_hi, aa)

    out_path = Path(args.out)
    Image.fromarray(rgb, mode="RGB").save(out_path)
    print(f"Saved: {out_path.resolve()}")


if __name__ == "__main__":
    main()


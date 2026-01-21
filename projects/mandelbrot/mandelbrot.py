#!/usr/bin/env python3
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
    zoom: float = 1.0
    max_iter: int = 400


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--width", type=int, default=1200)
    p.add_argument("--height", type=int, default=800)
    p.add_argument("--max-iter", type=int, default=600)
    p.add_argument("--center", nargs=2, type=float, default=[-0.5, 0.0])
    p.add_argument("--zoom", type=float, default=1.0)
    p.add_argument("--aa", type=int, default=2)
    p.add_argument("--out", type=str, default="mandelbrot.png")
    return p.parse_args()


def smooth_iter_count(z, it):
    mag = np.abs(z)
    mag = np.clip(mag, 1e-12, None)
    return it + 1.0 - np.log(np.log(mag)) / math.log(2.0)


def palette(t):
    r = 9 * (1 - t) * t**3
    g = 15 * (1 - t) ** 2 * t**2
    b = 8.5 * (1 - t) ** 3 * t
    rgb = np.stack([r, g, b], axis=-1)
    return np.clip(rgb * 255, 0, 255).astype(np.uint8)


def render(width, height, view):
    span_x = 3.5 * view.zoom
    span_y = span_x * (height / width)

    x = np.linspace(view.cx - span_x / 2, view.cx + span_x / 2, width)
    y = np.linspace(view.cy - span_y / 2, view.cy + span_y / 2, height)

    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y

    Z = np.zeros_like(C)
    it = np.zeros(C.shape, dtype=int)
    mask = np.ones(C.shape, dtype=bool)

    for i in range(view.max_iter):
        Z[mask] = Z[mask] * Z[mask] + C[mask]
        escaped = np.abs(Z) > 2
        it[escaped & mask] = i
        mask &= ~escaped
        if not mask.any():
            break

    nu = np.zeros_like(Z.real)
    escaped_any = it > 0
    nu[escaped_any] = smooth_iter_count(Z[escaped_any], it[escaped_any])

    max_nu = nu[escaped_any].max() if escaped_any.any() else 1.0
    t = nu / max_nu

    rgb = palette(t)
    rgb[mask] = [0, 0, 0]
    return rgb


def downsample(img, aa):
    if aa <= 1:
        return img
    h, w, c = img.shape
    img = img[: h - h % aa, : w - w % aa]
    img = img.reshape(h // aa, aa, w // aa, aa, c).mean(axis=(1, 3))
    return img.astype(np.uint8)

def mandelbrot(*, width, height, cx, cy, max_iter, scale=1.0, zoom=None, aa=None, out_path=None, **kwargs):
    """
    Compatibility wrapper for animate_zoom.py.

    animate_zoom.py passes:
      width, height, cx, cy, max_iter, scale, out_path

    Your current render() signature is: render(width, height, view)
    """
    # Old animate_zoom uses "scale" like a zoom/window-size factor
    if zoom is None:
        zoom = float(scale)

    # Optional supersampling (not currently passed by animate_zoom.py)
    if aa is None:
        aa = 1
    aa = max(1, int(aa))

    w_hi = int(width) * aa
    h_hi = int(height) * aa

    # Build the View object expected by render()
    view = View(cx=float(cx), cy=float(cy), zoom=float(zoom), max_iter=int(max_iter))

    img = render(w_hi, h_hi, view)
    img = downsample(img, aa)

    if out_path is not None:
        Image.fromarray(img).save(out_path)
        return None

    return img




def main():
    args = parse_args()
    view = View(
        cx=args.center[0],
        cy=args.center[1],
        zoom=args.zoom,
        max_iter=args.max_iter,
    )

    w = args.width * args.aa
    h = args.height * args.aa

    img = render(w, h, view)
    img = downsample(img, args.aa)

    out = Path(args.out)
    Image.fromarray(img).save(out)
    print(f"Saved: {out.resolve()}")


if __name__ == "__main__":
    main()

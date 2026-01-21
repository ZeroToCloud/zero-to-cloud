import os
import yaml

from mandelbrot import mandelbrot


def load_cfg(path="config.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    if not isinstance(cfg, dict):
        raise ValueError("config.yaml did not load as a dict")
    return cfg


def main():
    cfg = load_cfg()

    m = cfg["mandelbrot"]
    a = cfg.get("animation", {})

    frames = int(a.get("frames", 240))
    zoom_per_frame = float(a.get("zoom_per_frame", 0.97))
    out_dir = str(a.get("out_dir", "frames"))

    width = int(m.get("width", 800))
    height = int(m.get("height", 600))
    max_iter = int(m.get("max_iter", 200))
    cx = float(m["center_real"])
    cy = float(m["center_imag"])
    scale = float(m["scale"])

    os.makedirs(out_dir, exist_ok=True)

    print(f"Rendering {frames} frames to ./{out_dir} ...")
    for i in range(frames):
        out_path = f"{out_dir}/frame_{i:04d}.png"
        mandelbrot(
            width=width,
            height=height,
            max_iter=max_iter,
            cx=cx,
            cy=cy,
            scale=scale,
            out_path=out_path,
        )
        # shrink scale each frame = zoom in
        scale *= zoom_per_frame

    print("Done rendering frames.")


if __name__ == "__main__":
    main()

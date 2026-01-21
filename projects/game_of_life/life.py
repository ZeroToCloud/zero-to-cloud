#!/usr/bin/env python3

from PIL import Image

import os
import time
import random
import yaml

# =========================
# Z2C Game of Life (YAML)
# =========================

# Defaults (overridden by life.yaml)
WIDTH = 60
HEIGHT = 25
TICK = 0.08
DENSITY = 0.22

ALIVE = "██"
DEAD = "  "


def clear_screen():
    print("\033[H\033[J", end="")


def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def neighbors(grid, x, y, wrap=True):
    cnt = 0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue

            nx = x + dx
            ny = y + dy

            if wrap:
                nx %= WIDTH
                ny %= HEIGHT
                cnt += grid[ny][nx]
            else:
                if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
                    cnt += grid[ny][nx]

    return cnt


def step(grid, wrap=True):
    new = [[0] * WIDTH for _ in range(HEIGHT)]
    for y in range(HEIGHT):
        for x in range(WIDTH):
            n = neighbors(grid, x, y, wrap=wrap)

            if grid[y][x] == 1:
                new[y][x] = 1 if (n == 2 or n == 3) else 0
            else:
                new[y][x] = 1 if n == 3 else 0

    return new


def render_terminal(grid, gen):
    clear_screen()
    print(f"Conway's Game of Life | gen={gen} | Ctrl+C to stop")
    for y in range(HEIGHT):
        line = []
        for x in range(WIDTH):
            line.append(ALIVE if grid[y][x] else DEAD)
        print("".join(line))


def save_frame_png(grid, gen, out_dir="out_frames", cell_px=8):
    ...

    os.makedirs(out_dir, exist_ok=True)

    h = len(grid)
    w = len(grid[0])

    img = Image.new("RGB", (w * cell_px, h * cell_px), (0, 0, 0))
    px = img.load()

    for y in range(h):
        for x in range(w):
            if grid[y][x]:
                for yy in range(y * cell_px, (y + 1) * cell_px):
                    for xx in range(x * cell_px, (x + 1) * cell_px):
                        px[xx, yy] = (255, 255, 255)

    img.save(os.path.join(out_dir, f"frame_{gen:06d}.png"))

    clear_screen()
    print(f"Conway's Game of Life | gen={gen} | Ctrl+C to stop")
    for y in range(HEIGHT):
        line = []
        for x in range(WIDTH):
            line.append(ALIVE if grid[y][x] else DEAD)
        print("".join(line))


def empty_grid():
    return [[0] * WIDTH for _ in range(HEIGHT)]


def random_grid():
    return [[1 if random.random() < DENSITY else 0 for _ in range(WIDTH)]
            for _ in range(HEIGHT)]


def block_grid():
    g = empty_grid()
    for y in (1, 2):
        for x in (1, 2):
            g[y][x] = 1
    return g


def blinker_grid():
    g = empty_grid()
    for x in (1, 2, 3):
        g[2][x] = 1
    return g


def glider_grid():
    g = empty_grid()
    coords = [(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)]
    for x, y in coords:
        g[y][x] = 1
    return g


def glider_gun_grid():
    g = empty_grid()

    # Gosper Glider Gun
    cells = [
        (1, 5), (2, 5), (1, 6), (2, 6),

        (11, 5), (11, 6), (11, 7),
        (12, 4), (12, 8),
        (13, 3), (13, 9),
        (14, 3), (14, 9),
        (15, 6),
        (16, 4), (16, 8),
        (17, 5), (17, 6), (17, 7),
        (18, 6),

        (21, 3), (21, 4), (21, 5),
        (22, 3), (22, 4), (22, 5),
        (23, 2), (23, 6),
        (25, 1), (25, 2), (25, 6), (25, 7),

        (35, 3), (35, 4),
        (36, 3), (36, 4)
    ]

    for x, y in cells:
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            g[y][x] = 1

    return g




def main():
    global WIDTH, HEIGHT, TICK, DENSITY

    cfg_path = os.path.join(os.path.dirname(__file__), "config.yaml")
    cfg = load_config(cfg_path)

    WIDTH = int(cfg.get("width", WIDTH))
    HEIGHT = int(cfg.get("height", HEIGHT))
    TICK = float(cfg.get("tick", TICK))
    DENSITY = float(cfg.get("density", DENSITY))

    start = str(cfg.get("start", "random")).lower()
    wrap = bool(cfg.get("wrap", True))

    if start == "gun":
        grid = glider_gun_grid()
    elif start == "glider":
        grid = glider_grid()
    elif start == "blinker":
        grid = blinker_grid()
    elif start == "block":
        grid = block_grid()
    else:
        grid = random_grid()

    gen = 0
    try:
        while True:
            render_terminal(grid, gen)
            save_frame_png(grid, gen)
            grid = step(grid, wrap=wrap)
            gen += 1
            time.sleep(TICK)
    except KeyboardInterrupt:
        clear_screen()
        print("Stopped. Nice run ✅")


if __name__ == "__main__":
    main()

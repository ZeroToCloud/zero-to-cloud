from PIL import Image, ImageDraw
import random

SCALE = 16
W, H = 32, 32

# Colors
BG = (5, 5, 10)             # deep dark
PORTAL = (110, 0, 160)      # portal purple
PORTAL2 = (170, 80, 255)    # bright purple
FRAME = (20, 40, 30)        # obsidian-ish green tint
FRAME2 = (10, 20, 15)       # darker frame shade
STAR = (220, 220, 255)      # tiny stars
BODY = (12, 12, 16)
BODY2 = (18, 18, 24)
EYE = (186, 85, 211)
EYE_GLOW = (255, 170, 255)

img = Image.new("RGB", (W * SCALE, H * SCALE), BG)
d = ImageDraw.Draw(img)

def rect_blocks(x1, y1, x2, y2, color):
    for y in range(y1, y2):
        for x in range(x1, x2):
            x0, y0 = x * SCALE, y * SCALE
            d.rectangle([x0, y0, x0 + SCALE - 1, y0 + SCALE - 1], fill=color)

def block(x, y, color):
    x0, y0 = x * SCALE, y * SCALE
    d.rectangle([x0, y0, x0 + SCALE - 1, y0 + SCALE - 1], fill=color)

# -------------------
# Background stars
# -------------------
for _ in range(60):
    x = random.randint(0, W - 1)
    y = random.randint(0, H - 1)
    if random.random() < 0.6:
        block(x, y, STAR)

# -------------------
# End Portal Frame
# -------------------
# Outer frame box
frame_x1, frame_y1 = 6, 6
frame_x2, frame_y2 = 26, 26

# Frame thickness
t = 2

# Frame outer
rect_blocks(frame_x1, frame_y1, frame_x2, frame_y1 + t, FRAME)
rect_blocks(frame_x1, frame_y2 - t, frame_x2, frame_y2, FRAME)
rect_blocks(frame_x1, frame_y1, frame_x1 + t, frame_y2, FRAME)
rect_blocks(frame_x2 - t, frame_y1, frame_x2, frame_y2, FRAME)

# Frame shading
rect_blocks(frame_x1, frame_y1, frame_x2, frame_y1 + 1, FRAME2)
rect_blocks(frame_x1, frame_y1, frame_x1 + 1, frame_y2, FRAME2)

# Portal inside
px1, py1 = frame_x1 + t, frame_y1 + t
px2, py2 = frame_x2 - t, frame_y2 - t

for y in range(py1, py2):
    for x in range(px1, px2):
        # swirl-ish effect
        if (x + y) % 3 == 0:
            block(x, y, PORTAL2)
        else:
            block(x, y, PORTAL)

# Sparkle particles in portal
for _ in range(50):
    x = random.randint(px1, px2 - 1)
    y = random.randint(py1, py2 - 1)
    if random.random() < 0.5:
        block(x, y, (255, 190, 255))

# -------------------
# Enderman (front)
# -------------------
# Head (10x10)
hx, hy = 11, 7
for y in range(hy, hy + 10):
    for x in range(hx, hx + 10):
        if x in (hx, hx + 9) or y in (hy, hy + 9):
            block(x, y, BODY2)
        else:
            block(x, y, BODY)

# Eyes
for x in range(hx + 2, hx + 4):
    block(x, hy + 4, EYE)
    block(x, hy + 3, EYE_GLOW)

for x in range(hx + 6, hx + 8):
    block(x, hy + 4, EYE)
    block(x, hy + 3, EYE_GLOW)

# Body (8x12)
bx, by = 12, 17
for y in range(by, by + 10):
    for x in range(bx, bx + 8):
        if x in (bx, bx + 7) or y in (by, by + 9):
            block(x, y, BODY2)
        else:
            block(x, y, BODY)

# Arms
ax1, ay = 10, 17
for y in range(ay, ay + 9):
    for x in range(ax1, ax1 + 2):
        block(x, y, BODY2 if x == ax1 else BODY)

ax2 = 20
for y in range(ay, ay + 9):
    for x in range(ax2, ax2 + 2):
        block(x, y, BODY2 if x == ax2 + 1 else BODY)

# Legs
lx, ly = 13, 27
for y in range(ly, ly + 5):
    for x in range(lx, lx + 2):
        block(x, y, BODY)
for y in range(ly, ly + 5):
    for x in range(lx + 4, lx + 6):
        block(x, y, BODY)

out = "enderman_portal.png"
img.save(out)
print(f"Saved {out}")

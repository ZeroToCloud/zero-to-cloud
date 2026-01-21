from PIL import Image, ImageDraw, ImageFont
from fractions import Fraction
import os


def fmt(fr: Fraction) -> str:
    fr = fr.limit_denominator()
    if fr.denominator == 1:
        return str(fr.numerator)
    return f"{fr.numerator}/{fr.denominator}"


def render_frame(days, total_days, show_labels=True, out_path="frame.png"):
    """
    Render a single frame that draws the cathedral up to `days`,
    but uses a fixed canvas size based on `total_days` so the GIF
    doesn't zoom/crop between frames.
    """
    margin = 60
    row_gap = 90
    col_gap = 80
    radius = 10

    # FIXED camera: always compute canvas based on FINAL day
    max_nodes = 2 * (total_days - 1) + 1 if total_days > 0 else 1
    width = margin * 2 + (max_nodes - 1) * col_gap + 260
    height = margin * 2 + max(1, total_days) * row_gap + 60

    img = Image.new("RGB", (width, height), "white")
    d = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 16)
        font_big = ImageFont.truetype("DejaVuSans.ttf", 22)
    except:
        font = ImageFont.load_default()
        font_big = ImageFont.load_default()

    center_x = width // 2
    positions = []

    for day in range(days):
        y = margin + day * row_gap

        if day == 0:
            x = center_x
            positions.append([(x, y)])
            d.ellipse((x - radius, y - radius, x + radius, y + radius), outline="black", width=2)
            d.text((x + 18, y - 14), "{|}", fill="black", font=font_big)
            d.text((x + 18, y + 10), "0", fill="black", font=font_big)
            continue

        count = 2 * day + 1
        start_x = center_x - ((count - 1) * col_gap) // 2
        row = [(start_x + i * col_gap, y) for i in range(count)]
        positions.append(row)

        # ancestry connections
        prev = positions[day - 1]
        prev_count = len(prev)

        for i, (cx, cy) in enumerate(row):
            lp = (i - 1) // 2
            rp = i // 2
            lp = max(0, min(prev_count - 1, lp))
            rp = max(0, min(prev_count - 1, rp))

            (lx, ly) = prev[lp]
            (rx, ry) = prev[rp]

            d.line((lx, ly + radius, cx, cy - radius), fill="black", width=2)
            d.line((rx, ry + radius, cx, cy - radius), fill="black", width=2)

        # nodes + labels
        den = 2 ** max(day - 1, 0)
        for i, (x, y) in enumerate(row):
            d.ellipse((x - radius, y - radius, x + radius, y + radius), outline="black", width=2)
            if show_labels:
                value = Fraction(i - day, den)
                d.text((x - 18, y + 14), fmt(value), fill="black", font=font)

        # day label on the left
        d.text((10, y - 10), f"day {day}", fill="black", font=font)

    img.save(out_path)
    return img


def make_gif(total_days=10, fps=4, show_labels=True):
    os.makedirs("/out/frames", exist_ok=True)
    frames = []

    for n in range(1, total_days + 1):
        frame_path = f"/out/frames/cathedral_day_{n:02d}.png"
        img = render_frame(days=n, total_days=total_days, show_labels=show_labels, out_path=frame_path)
        frames.append(img)

    duration_ms = int(1000 / fps)
    gif_path = "/out/cathedral.gif"

    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration_ms,
        loop=0,
    )

    print(f"Saved {gif_path} ({total_days} frames @ {fps} fps)")


if __name__ == "__main__":
    # Config from env vars (with defaults)
    total_days = int(os.getenv("DAYS", "10"))
    fps = int(os.getenv("FPS", "4"))
    labels_raw = os.getenv("LABELS", "1").strip().lower()
    show_labels = labels_raw not in ("0", "false", "no", "off")

    make_gif(total_days=total_days, fps=fps, show_labels=show_labels)


"""Draw bbox + balloon_id on top of a filled page image for visual self-audit."""
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

COLOR_BY_KIND = {
    "shout": (255, 60, 60),
    "thought": (80, 180, 255),
    "narration": (255, 200, 60),
    "sfx": (255, 120, 255),
    "dialogue": (60, 255, 120),
    "whisper": (180, 180, 180),
}


def main(script_json: Path, filled_png: Path, out_png: Path):
    data = json.loads(script_json.read_text())
    page_w, page_h = data["page_size"]
    img = Image.open(filled_png).convert("RGB")
    if img.size != (page_w, page_h):
        print(f"WARN: image size {img.size} != script page_size {(page_w, page_h)}", file=sys.stderr)
    draw = ImageDraw.Draw(img, "RGBA")
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
    except Exception:
        font = ImageFont.load_default()

    for panel in data["panels"]:
        for b in panel["balloons"]:
            x, y, w, h = b["bbox"]
            color = COLOR_BY_KIND.get(b["kind"], (255, 255, 255))
            # draw semi-transparent fill
            draw.rectangle([x, y, x + w, y + h], outline=color, width=3)
            label = f"{b['balloon_id']} [{b['kind']}] {b.get('char_count','?')}c"
            tx = x + 2
            ty = y - 18 if y > 20 else y + h + 2
            # background for label
            tb = draw.textbbox((tx, ty), label, font=font)
            draw.rectangle(tb, fill=(0, 0, 0, 200))
            draw.text((tx, ty), label, fill=color, font=font)
    img.save(out_png)
    print(f"saved overlay: {out_png}")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))

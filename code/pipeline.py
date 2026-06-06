"""Per-page pipeline for Chicago 1990 chapter 1.

Steps:
1. Generate image via kamay-cli (gpt-image-2, 2:3, 832x1248, face anchor reference)
2. Auto-detect white balloon bboxes via PIL/scipy threshold
3. Match detected bboxes to script balloons by area + position heuristics
4. Fill text via mbf (SSH to root@129.226.144.118:/srv/manga-tool)
5. Audit overlay JSON for overflow/warnings; iterate bbox if needed
6. Generate audit overlay PNG with bbox + IDs drawn

Run: python3 pipeline.py <page_number>
"""
from __future__ import annotations
import json, sys, subprocess, os, time
from pathlib import Path

ROOT = Path(__file__).parent
SCRIPTS_DIR = ROOT / "scripts/v3"
SERVER = "root@129.226.144.118"
SSH_KEY = os.path.expanduser("~/.ssh/id_ed25519")
FACE_ANCHOR_URL = "https://chicago.secondlife.today/songya_face_anchor.png"

# Detect if we're running ON the manga-tool server itself (production agents are local).
# When LOCAL_MODE is True, upload_and_fill() skips SCP/SSH and runs mbf directly.
LOCAL_MODE = Path("/srv/manga-tool/.venv/bin/mbf").exists() and Path("/srv/chicago").exists()
MBF_BIN = "/srv/manga-tool/.venv/bin/mbf"
MBF_SAMPLES_DIR = Path("/srv/manga-tool/samples")
MBF_OUT_DIR = Path("/srv/manga-tool/out/v3")

STYLE_PREAMBLE = """A 4-panel manga page (modern colored Korean manhwa / Japanese seinen hybrid), 2:3 portrait aspect ratio 832x1248. Half-realistic line art with restrained color blocking and soft cell shading. Style is colored manhwa-seinen hybrid — clean confident colored ink line work, painterly muted color palette, soft cinematic lighting. NOT heavy black ink seinen, NOT B&W screen-tone manga, NOT smooth Pixar CG.

PAGE LAYOUT: Mangaplus-style varied panel rhythm with thin black gutters. {layout}

COLOR: Muted 1990 Chicago palette — cool faded indigo and charcoal grays, light caramel skin tone, faded olive-brown blanket/jacket, off-white, warm amber for indoor lighting moments, cold pale gray-blue for outdoor winter scenes. Soft cell shading.

CHARACTER LOCKS (use face anchor reference for SONGYA's face):
- SONGYA (15, mixed-race teenage boy): light caramel skin, slightly Asian almond eyes, short curly black hair, slightly round youthful face. Indoor: dark blue/gray sweater. Outdoor: olive-brown USAF 1969 surplus jacket over the sweater. Always old off-white sneakers.
- TONY (17, Songya's older cousin): slightly chubby torso, short hair, faded olive factory work jacket.
- CONNIE (17, Songya's female cousin, Suzie's daughter, Cameroonian-descent Black-American): heavyset growing-horizontally build, messy short curly hair, bright 1980s loud-colored short tight party dress when out (neon coral / fluorescent pink), big gold hoop earrings, smudged makeup. Loud and brash, dresses provocatively, but always fully clothed for our purposes.
- AUNT SUZIE (33-34, Cameroonian-descent single mom of 5): heavyset stocky build, headscarf, brightly patterned house robe, plain home clothes. Loud direct mouth.
- EMILY (10, little sister): twin braids, light caramel mixed-race skin, kid clothes.
- ET (16-ish): baseball cap pulled low, hint of flower-pattern bandana under brim.
- SILENCER (17ish bodyguard type): tall broad-shouldered Black, silent stern face.
- LIL LORRY (16-ish rapper): thin, baby face, neat dreadlocks, big headphones, denim shirt, basketball nearby.
- AK (25 white-collar Black, AK is the slick label-rep): black suit no sunglasses, clipboard.

{panels}

CRITICAL CONSTRAINTS:
- ALL speech balloons (round/oval) and ALL narration rectangles have PURE WHITE INTERIOR with thin black border. NO dark-filled boxes anywhere — narration is white-bg with black text rendered later.
- JAGGED shout balloons: the jagged spikes are part of the OUTER border ONLY. There is NO visible second border or oval line drawn INSIDE the spikes — the white interior is one continuous unbroken white area that simply connects smoothly to the spike tips. Do NOT draw a separate oval outline within the spike pattern.
- Every balloon, SFX block, and narration box must be COMPLETELY EMPTY of text/letters/characters/markings — to be filled by typesetting tool.
- No watermarks, no signature, no other text anywhere on page.
- All characters fully clothed.
"""


def kamay_generate(prompt: str, name: str) -> str:
    """Generate image and return local PNG path."""
    result = subprocess.run(
        [
            "kamay", "image", "generate-image",
            "--prompt", prompt,
            "--aspect_ratio", "2:3",
            "--resolution", "1K",
            "--model", "gpt-image-2",
            "--reference_images", FACE_ANCHOR_URL,
            "--name", name,
        ],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    out = result.stdout + result.stderr
    for line in out.split("\n"):
        if "Resource URI:" in line:
            uri = line.split("mention://resource/")[1].strip()
            break
    else:
        raise RuntimeError(f"No Resource URI in kamay output:\n{out}")
    # Download
    subprocess.run(
        ["kamay", "resource", "download", "-u", f"mention://resource/{uri}", "-o", "./v3_downloads"],
        check=True, cwd=str(ROOT), capture_output=True,
    )
    src = ROOT / "v3_downloads" / f"{uri}.png"
    dst = ROOT / f"{name}.png"
    src.rename(dst)
    return str(dst)


def detect_white_bboxes(png_path: str) -> list[dict]:
    """Return list of detected white bbox candidates: [{area, bbox, fill_ratio}]."""
    from PIL import Image
    import numpy as np
    from scipy import ndimage as ndi
    img = np.array(Image.open(png_path).convert("RGB"))
    gray = img.mean(axis=2)
    white = gray > 235
    lbl, n = ndi.label(white)
    comps = []
    for i in range(1, n + 1):
        mask = lbl == i
        area = int(mask.sum())
        if area < 400:
            continue
        ys, xs = np.where(mask)
        bbox = [int(xs.min()), int(ys.min()), int(xs.max() - xs.min()) + 1, int(ys.max() - ys.min()) + 1]
        # Exclude global page (mask covers everything)
        if bbox[2] > 800 and bbox[3] > 1200:
            continue
        fill_ratio = area / (bbox[2] * bbox[3])
        comps.append({"area": area, "bbox": bbox, "fill_ratio": fill_ratio})
    comps.sort(key=lambda c: -c["area"])
    return comps


def upload_and_fill(image_path: str, script_path: str, page_id: str, agent_namespace: str | None = None) -> dict:
    """Run mbf fill. In LOCAL_MODE, runs directly via subprocess.
    Otherwise SCPs to server and runs over SSH.

    `agent_namespace` — optional subdir like 'estelle' or 'joshua' so concurrent
    agents don't collide in /srv/manga-tool/samples/ and /out/v3/.
    """
    img_name = Path(image_path).name
    script_name = Path(script_path).name
    out_name = f"{page_id}_filled.png"
    overlay_name = out_name.replace(".png", "-overlay.json")

    if LOCAL_MODE:
        import shutil
        samples = MBF_SAMPLES_DIR / agent_namespace if agent_namespace else MBF_SAMPLES_DIR
        out_dir = MBF_OUT_DIR / agent_namespace if agent_namespace else MBF_OUT_DIR
        samples.mkdir(parents=True, exist_ok=True)
        out_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy(image_path, samples / img_name)
        shutil.copy(script_path, samples / script_name)
        subprocess.run(
            [MBF_BIN, "fill",
             str(samples / img_name), str(samples / script_name),
             "-o", str(out_dir / out_name), "--debug"],
            check=True, capture_output=True,
        )
        filled_local = ROOT / out_name
        overlay_local = ROOT / overlay_name
        shutil.copy(out_dir / out_name, filled_local)
        shutil.copy(out_dir / overlay_name, overlay_local)
        return json.loads(overlay_local.read_text())

    # Remote SSH path (lead Alein on Mac, falling back here)
    subprocess.run(
        ["scp", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no",
         image_path, script_path,
         f"{SERVER}:/srv/manga-tool/samples/"],
        check=True, capture_output=True,
    )
    cmd = (
        "source /srv/manga-tool/.venv/bin/activate && cd /srv/manga-tool && "
        f"mbf fill samples/{img_name} samples/{script_name} -o out/v3/{out_name} --debug"
    )
    subprocess.run(
        ["ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", SERVER, cmd],
        check=True, capture_output=True,
    )
    filled_local = ROOT / out_name
    subprocess.run(
        ["scp", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no",
         f"{SERVER}:/srv/manga-tool/out/v3/{out_name}", str(filled_local)],
        check=True, capture_output=True,
    )
    overlay_local = ROOT / overlay_name
    subprocess.run(
        ["scp", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no",
         f"{SERVER}:/srv/manga-tool/out/v3/{overlay_name}",
         str(overlay_local)],
        check=True, capture_output=True,
    )
    return json.loads(overlay_local.read_text())


def audit_overlay(script_path: str, filled_path: str, out_path: str):
    """Generate audit overlay PNG with bbox + IDs drawn."""
    subprocess.run(
        ["python3", str(ROOT / "audit_overlay.py"), script_path, filled_path, out_path],
        check=True, capture_output=True,
    )


def report_overlay(overlay: dict) -> tuple[bool, str]:
    """Return (all_ok, table_str)."""
    rows = []
    all_ok = True
    rows.append(f"{'balloon_id':25s} | {'font':5s} | rows | overflow | warnings | text")
    rows.append("-" * 100)
    for r in overlay["rendered"]:
        w = ",".join(r["warnings"]) if r["warnings"] else "OK"
        if r["warnings"] or r["overflow"]:
            all_ok = False
        lines = " / ".join(r["lines"])
        rows.append(
            f"{r['balloon_id']:25s} | {r['font_size_px']:3d}px | {len(r['lines']):3d}  | {str(r['overflow']):5s}    | {w:20s} | {lines}"
        )
    return all_ok, "\n".join(rows)


if __name__ == "__main__":
    print("Use this as a library. Per-page main scripts will import functions.")

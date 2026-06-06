"""Process a batch of pages: generate → detect → assign → fill → audit.

Run: python3 run_batch.py P2 P3 P4 P5 P6
"""
from __future__ import annotations
import json, sys, subprocess, os
from pathlib import Path
from pages_config import PAGES
from pipeline import STYLE_PREAMBLE, kamay_generate, detect_white_bboxes, upload_and_fill, audit_overlay, report_overlay, SERVER, SSH_KEY, ROOT


def build_prompt(page_id: str) -> str:
    cfg = PAGES[page_id]
    layout_line = cfg["prompt_body"].split("\n")[0]
    return STYLE_PREAMBLE.format(layout=layout_line, panels=cfg["prompt_body"])


def write_prompt_file(page_id: str) -> Path:
    prompt = build_prompt(page_id)
    p = ROOT / "scripts/v3" / f"prompt-ch01-{page_id.lower()}.txt"
    p.write_text(prompt)
    return p


def assign_bboxes(detected: list[dict], balloons: list[dict]) -> list[dict]:
    """Panel-quadrant-aware matching.

    Each balloon has `panel_id` (1-4 for 2x2 grid, or 1-N for vertical stacks).
    Detected bboxes are assigned to quadrants based on center; then within each
    quadrant, balloons are matched in script order to detected in reading order.
    """
    H, W = 1248, 832

    def get_quadrant(bbox, n_rows=2, n_cols=2):
        """Return panel_id (1-indexed) by center position. Defaults to 2x2 grid."""
        cx = bbox[0] + bbox[2] / 2
        cy = bbox[1] + bbox[3] / 2
        row = min(int(cy / (H / n_rows)), n_rows - 1)
        col = min(int(cx / (W / n_cols)), n_cols - 1)
        return row * n_cols + col + 1

    # Determine layout grid from balloons' panel_id range OR explicit override
    panel_ids = sorted(set(b.get("panel_id", 1) for b in balloons))
    max_panel = max(panel_ids)
    # Per-balloon layout override takes precedence
    explicit = next((b.get("layout") for b in balloons if b.get("layout")), None)
    if explicit:
        n_rows, n_cols = explicit
    elif max_panel == 4:
        n_rows, n_cols = 2, 2
    elif max_panel == 3:
        n_rows, n_cols = 3, 1
    elif max_panel in (5, 6):
        n_rows, n_cols = 3, 2
    elif max_panel in (7, 8):
        n_rows, n_cols = 4, 2
    else:
        n_rows, n_cols = 2, 2

    # Filter: keep only meaningful white regions (likely balloons), not noise.
    # Min area 3500, fill_ratio >= 0.40 (jagged shouts can be 0.3-0.7 but rectangle/oval balloons are >0.6)
    candidates = [d for d in detected if 3500 <= d["area"] <= 95000 and d["fill_ratio"] >= 0.35]
    for d in candidates:
        d["panel"] = get_quadrant(d["bbox"], n_rows, n_cols)

    # Group by panel. Within panel, sort by AREA DESC (balloons are typically the largest white blobs)
    by_panel: dict[int, list[dict]] = {}
    for d in candidates:
        by_panel.setdefault(d["panel"], []).append(d)
    for p in by_panel:
        by_panel[p].sort(key=lambda d: -d["area"])

    print(f"  layout {n_rows}x{n_cols}; detected per panel: {{ {', '.join(f'{p}:{len(by_panel[p])}' for p in sorted(by_panel))} }}")

    # Group balloons by panel
    by_panel_balloon: dict[int, list[dict]] = {}
    for b in balloons:
        by_panel_balloon.setdefault(b.get("panel_id", 1), []).append(b)

    out = []
    for panel_id, panel_balloons in by_panel_balloon.items():
        avail = by_panel[panel_id][:] if panel_id in by_panel else []
        for b in panel_balloons:
            if not avail:
                print(f"    WARN: no candidate in panel {panel_id} for {b['balloon_id']}")
                continue
            det = avail.pop(0)
            x, y, w, h = det["bbox"]
            # Per-kind padding: shouts need MORE inner padding (jagged spikes around oval).
            # Detected white area for jagged shout balloon often includes spike whitespace.
            # Use larger inset to keep text well inside the smooth oval inner.
            kind = b.get("kind", "")
            fill = det["fill_ratio"]
            if kind == "shout":
                # For jagged shout: shrink generously (15% inset)
                pad_x = max(20, int(w * 0.15))
                pad_y = max(20, int(h * 0.15))
            elif fill > 0.9:
                # Rectangle (narration): minimal inset
                pad_x = pad_y = 5
            else:
                # Oval/cloud (dialogue/thought/sfx): moderate inset
                pad_x = max(8, int(w * 0.08))
                pad_y = max(8, int(h * 0.08))
            ix, iy = x + pad_x, y + pad_y
            iw = max(10, w - 2 * pad_x)
            ih = max(10, h - 2 * pad_y)
            out.append({"balloon_id": b["balloon_id"], "bbox": [ix, iy, iw, ih], "detected": det})
    return out


def build_script_json(page_id: str, mapped: list[dict]) -> Path:
    cfg = PAGES[page_id]
    by_id = {b["balloon_id"]: b for b in cfg["balloons"]}
    panels_balloons = []
    for m in mapped:
        b = by_id[m["balloon_id"]]
        panels_balloons.append({
            "balloon_id": b["balloon_id"],
            "speaker": b.get("speaker", ""),
            "kind": b["kind"],
            "text": b["text"],
            "char_count": len(b["text"]),
            "target_position": "auto-detected",
            "target_size_pct": 5,
            "bbox": m["bbox"],
            "notes": f"auto-assigned from detected {m['detected']['bbox']} area={m['detected']['area']} fill={m['detected']['fill_ratio']:.2f}",
        })
    script = {
        "page_id": f"ch01_{page_id.lower()}_v3",
        "page_title": cfg["title"],
        "page_size": [832, 1248],
        "panels": [{
            "panel_id": 1,
            "panel_label": "full page (auto-pipeline)",
            "panel_bbox": [0, 0, 832, 1248],
            "balloons": panels_balloons,
        }],
    }
    p = ROOT / "scripts/v3" / f"script-ch01-{page_id.lower()}.json"
    p.write_text(json.dumps(script, ensure_ascii=False, indent=2))
    return p


def process(page_id: str):
    print(f"\n=== {page_id}: {PAGES[page_id]['title']} ===")
    cfg = PAGES[page_id]
    write_prompt_file(page_id)
    # Generate
    img_path = ROOT / f"{page_id}_v3.png"
    if not img_path.exists():
        print(f"  generating with kamay-cli (gpt-image-2)...")
        prompt = build_prompt(page_id)
        kamay_generate(prompt, f"{page_id}_v3")
    else:
        print(f"  using existing {img_path.name}")
    # Detect
    detected = detect_white_bboxes(str(img_path))
    print(f"  detected {len(detected)} white components")
    for d in detected[:8]:
        print(f"    area={d['area']:6d} bbox={d['bbox']} fill={d['fill_ratio']:.2f}")
    # Assign + write script
    mapped = assign_bboxes(detected, cfg["balloons"])
    script_path = build_script_json(page_id, mapped)
    # Fill + audit
    overlay = upload_and_fill(str(img_path), str(script_path), f"{page_id}_v3")
    ok, table = report_overlay(overlay)
    print(table)
    if not ok:
        print(f"  ⚠️  {page_id} has overflow/warnings — needs manual review")
    # Audit overlay PNG
    audit_overlay(str(script_path), str(ROOT / f"{page_id}_v3_filled.png"), str(ROOT / f"{page_id}_v3_audit.png"))
    return ok


def main():
    ids = sys.argv[1:] or list(PAGES.keys())
    results = {}
    for pid in ids:
        try:
            ok = process(pid)
            results[pid] = "OK" if ok else "WARN"
        except Exception as e:
            print(f"  ERROR on {pid}: {e}")
            results[pid] = f"ERROR: {e}"
    print("\n=== SUMMARY ===")
    for pid, r in results.items():
        print(f"  {pid}: {r}")


if __name__ == "__main__":
    main()

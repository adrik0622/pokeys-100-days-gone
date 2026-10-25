#!/usr/bin/env python3
"""Subscribe through the existing Steam UI; never click a subscribed item.

For user-authorized project items only. Requires inspected 1720px Steam layout.
URL and exact button text are checked via local screenshot OCR. Ambiguity stops.
This does not enable mods, approve Java, edit collections or launch the game.
"""
import argparse
import io
import json
from pathlib import Path
import re
import subprocess
import time

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def request(data):
    result = json.loads(subprocess.check_output(
        ["python3", str(ROOT / "scripts/desktop_control.py"), "request", json.dumps(data)],
        cwd=ROOT, text=True,
    ))
    if not result["ok"]:
        raise RuntimeError(result)
    return result["result"]


def ocr(image):
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return subprocess.check_output([
        "tesseract", "stdin", "stdout", "--tessdata-dir",
        str(ROOT / "runtime/tools/tessdata"), "--psm", "7",
    ], input=buffer.getvalue(), stderr=subprocess.DEVNULL).decode().strip()


def inspect(wid, phase):
    result = request({"action": "screenshot", "scope": "workshop", "focus": True,
                      "name": f"subscription-{wid}-{phase}"})
    image = Image.open(result["path"]).convert("RGB")
    if image.width != 1720:
        raise RuntimeError("Uninspected Steam layout; use manual control")
    url = ocr(image.crop((65, 62, 1250, 90)).resize((2370, 56)))
    item = re.search(r"[?&]id=(\d+)", url.replace(" ", ""))
    if not item or item.group(1) != wid:
        raise RuntimeError("Expected Workshop URL not confirmed: " + url)
    rows = [y for y in range(700, min(1250, image.height)) if sum(
        1 for x in range(850, 980)
        if (lambda c: c[1] > 90 and c[1] > c[0] * 1.08 and c[2] < 65)(
            image.getpixel((x, y)))
    ) > 110]
    if not rows or not 20 <= len(rows) <= 40:
        raise RuntimeError("Subscription button geometry uncertain; no click")
    label = ocr(image.crop((875, min(rows), 984, max(rows) + 1))
                .convert("L").point(lambda v: 0 if v > 185 else 255).resize((436, 128)))
    return label, (min(rows) + max(rows)) // 2


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workshop_ids", nargs="+")
    args = parser.parse_args()
    for wid in args.workshop_ids:
        if not wid.isdigit():
            raise SystemExit("Expected numeric Workshop ID")
        request({"action": "workshop_open", "url":
                 "https://steamcommunity.com/sharedfiles/filedetails/?id=" + wid})
        time.sleep(2)
        label, y = inspect(wid, "before")
        if label in ("Subscribed", "Unsubscribe"):
            print(wid, "already subscribed; untouched", flush=True)
            continue
        if label != "Subscribe":
            raise RuntimeError(f"Uncertain button text {label!r}; no click")
        request({"action": "click", "scope": "workshop", "x": 916, "y": y})
        request({"action": "click", "scope": "workshop", "x": 1360, "y": 1150})
        time.sleep(1)
        after, _ = inspect(wid, "after")
        if after not in ("Subscribed", "Unsubscribe"):
            raise RuntimeError(f"Subscription not confirmed: {after!r}; do not retry blindly")
        print(wid, "subscription confirmed", flush=True)


if __name__ == "__main__":
    main()

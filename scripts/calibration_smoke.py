#!/usr/bin/env python3
"""One fixed GUI test: open observer panel at 80/100 in 1600x900 client A first.

Reads only screenshots via existing Tesseract; no Lua calls, memory reads or packets.
Run after relay cooldown. Fails closed if panel/step OCR cannot be confirmed.
"""
import json
from pathlib import Path
import re
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]


def request(action, **args):
    value = json.loads(subprocess.check_output([
        "python3", str(ROOT / "scripts/desktop_control.py"), "request",
        json.dumps({"action": action, "client": "a", **args})], cwd=ROOT))
    if not value["ok"]:
        raise RuntimeError(value)
    return value["result"]


def screen(name, challenge=False):
    path = request("screenshot", name=name)["path"]
    pixels = None
    if challenge:
        # Fixed UI text strip only; enlarge glyphs, not a game-state read.
        pixels = subprocess.check_output(["convert", path, "-crop", "680x30+90+480", "+repage",
                                          "-resize", "400%", "png:-"], timeout=3)
    value = subprocess.check_output(["tesseract", "stdin" if challenge else path, "stdout", "--tessdata-dir",
                                    str(ROOT / "runtime/tools/tessdata"), "--psm", "7" if challenge else "11"],
                                   input=pixels, stderr=subprocess.DEVNULL, timeout=5).decode()
    return value


def parse_channel(text, step):
    match = re.search(r"Step\s*" + str(step) + r"\s*:\s*Channel\s*([123])", text, re.I)
    if not match:
        raise RuntimeError("Could not confirm current challenge: " + text)
    return int(match[1])


def main():
    if "FIELD OBSERVERS" not in screen("calibration-before"):
        raise RuntimeError("Expected already-open fixed observer panel")
    started = time.monotonic()
    request("click", x=180, y=453)
    try:
        for step in range(1, 4):
            # Controller/screenshot/OCR overhead is inside the measured duration.
            delay = started + step * 4 + 0.7 - time.monotonic()
            if delay > 0:
                time.sleep(delay)
            text = screen(f"calibration-step-{step}", challenge=True)
            channel = parse_channel(text, step)
            print(f"Step {step}, displayed channel {channel}, elapsed {time.monotonic()-started:.2f}s", flush=True)
            request("click", x=310 + (channel - 1) * 95, y=453)
        delay = started + 15.7 - time.monotonic()
        if delay > 0:
            time.sleep(delay)
        if time.monotonic() - started > 23:
            raise RuntimeError("UI/OCR too slow for bounded task")
        request("click", x=610, y=453)
        text = screen("calibration-result")
        print(text, flush=True)
        if "calibrated" not in text.lower() or "Signal locked" not in text:
            raise RuntimeError("No visible success confirmation")
        print(f"PASS: real GUI calibration in {time.monotonic()-started:.2f}s", flush=True)
    except Exception:
        request("click", x=710, y=453)  # Cancel, never complete by retrying guessed inputs.
        raise


if __name__ == "__main__":
    main()

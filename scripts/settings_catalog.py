#!/usr/bin/env python3
"""Build a factual, searchable knob appendix from pinned sandbox declarations.

No upstream code, images, translation prose or tooltips are republished. This is
not a Lua executor and does not deploy settings. Engine/preset overrides can
differ from declaration defaults; curated interpretation belongs in the report.
"""
import argparse
import csv
import hashlib
import html
import json
from pathlib import Path
import re

from modpack import ROOT, WORKSHOP, catalog, check_installed

FIELDS = ["mod_id", "key", "type", "default", "min", "max", "numValues", "page", "source", "source_sha256"]


def parse_options(source):
    # These files use a flat key=value declaration grammar, not Lua tables.
    # Strip comments, then require every declaration to have a closed body.
    source = re.sub(r"/\*.*?\*/", "", source, flags=re.S)
    source = re.sub(r"//[^\n]*|--[^\n]*", "", source)
    found = list(re.finditer(r"\boption\s+([A-Za-z0-9_.]+)\s*=?\s*\{([^{}]*)\}", source, re.S))
    if len(found) != len(re.findall(r"\boption\s+[A-Za-z0-9_.]+\s*=?\s*\{", source)):
        raise ValueError("Unsupported nested or unterminated option declaration")
    seen, rows = set(), []
    for match in found:
        key, body = match.groups()
        if key in seen:
            raise ValueError("Duplicate setting: " + key)
        seen.add(key)
        pairs = dict(re.findall(r"([A-Za-z_]+)\s*=\s*(\"[^\"]*\"|'[^']*'|[^,\n]+)\s*,?", body))
        row = {field: pairs.get(field, "").strip() for field in FIELDS if field not in {"key", "mod_id", "source", "source_sha256"}}
        row["key"] = key
        if not row["type"] or not row["default"]:
            raise ValueError("Incomplete option declaration: " + key)
        rows.append(row)
    return rows


def collect(manifest, workshop):
    check_installed(manifest, workshop)  # metadata/JAR drift must fail first
    result = []
    for item in catalog(manifest):
        # Selected version directory plus common assets, never older variants.
        metadata = Path(item["metadata_path"])
        root = workshop / item["workshop_id"]
        mod_folder = metadata.parent.parent
        paths = {metadata.parent / "media/sandbox-options.txt", mod_folder / "common/media/sandbox-options.txt"}
        known = set()
        for relative in sorted(paths):
            file = root / relative
            if not file.exists():
                continue
            digest = hashlib.sha256(file.read_bytes()).hexdigest()
            for row in parse_options(file.read_text(encoding="utf-8-sig")):
                if row["key"] in known:
                    raise ValueError("Version/common duplicate: " + row["key"])
                known.add(row["key"])
                result.append(dict(row, mod_id=item["mod_id"], source=relative.as_posix(), source_sha256=digest))
    return sorted(result, key=lambda r: (r["mod_id"].lower(), r["key"].lower()))


def render_html(rows):
    parts = ["<!doctype html><html lang='en'><meta charset='utf-8'><title>Pokeys v2 — settings appendix</title>",
             "<style>body{font:16px system-ui;margin:2rem;color:#182a30}input{font:inherit;padding:.5rem;width:95%}table{border-collapse:collapse;width:100%;font-size:13px}th,td{border:1px solid #ccd5d8;padding:.4rem;text-align:left}thead{position:sticky;top:0;background:#edf3f4}code{overflow-wrap:anywhere}small{color:#466}</style>",
             "<h1>Settings appendix — pinned development inputs</h1><p>Declaration defaults, not current server values or runtime acceptance. Presets may override them. Search keys; consult the illustrated report for plain-language choices. No upstream tooltip prose copied.</p>",
             f"<p>{len(rows)} declared knobs. <a href='V2_REPORT.md'>Report</a> · <a href='V2_SETTINGS.csv'>CSV with source fingerprints</a></p>",
             "<label for='q'>Filter by mod, page or setting key</label><p><input id='q' type='search' placeholder='e.g. ALifeJimmy.Standing or MilitaryDrop'></p><table><thead><tr>"]
    columns = FIELDS[:8]
    parts.extend("<th>" + html.escape(c) + "</th>" for c in columns)
    parts.append("</tr></thead><tbody>")
    for row in rows:
        parts.append("<tr>" + "".join("<td>" + html.escape(row.get(c, "")) + "</td>" for c in columns) + "</tr>")
    parts.append("</tbody></table><script>document.getElementById('q').addEventListener('input',function(){const q=this.value.toLowerCase();document.querySelectorAll('tbody tr').forEach(r=>r.hidden=!r.textContent.toLowerCase().includes(q));});</script></html>")
    return "\n".join(parts) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workshop-root", type=Path, default=WORKSHOP)
    args = parser.parse_args()
    manifest = json.loads((ROOT / "config/modpack.json").read_text())
    rows = collect(manifest, args.workshop_root)
    with (ROOT / "docs/V2_SETTINGS.csv").open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS); writer.writeheader(); writer.writerows(rows)
    (ROOT / "docs/V2_SETTINGS.html").write_text(render_html(rows))
    print(json.dumps({mid: sum(r["mod_id"] == mid for r in rows) for mid in sorted({r['mod_id'] for r in rows})}, indent=2))


if __name__ == "__main__": main()

#!/usr/bin/env python3
"""Validate the project manifest and render explicit, non-deploying profiles."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
WORKSHOP = Path("/home/adrikingston/.local/share/Steam/steamapps/workshop/content/108600")


def validate(manifest, profiles):
    items = manifest["trial_items"]
    ids, mods = set(), set()
    for item in items:
        wid, mid = item["workshop_id"], item["mod_id"]
        if not re.fullmatch(r"[0-9]+", wid) or wid in ids:
            raise ValueError("Invalid or duplicate Workshop ID")
        if not re.fullmatch(r"[A-Za-z0-9_.-]+", mid) or mid in mods:
            raise ValueError("Invalid or duplicate Mod ID")
        if not set(item["requires"]) <= mods:
            raise ValueError(f"Dependencies must precede {mid}")
        for field in ["metadata_path", "jar_path"]:
            if field in item:
                path = Path(item[field])
                if path.is_absolute() or ".." in path.parts:
                    raise ValueError("Dependency paths must stay inside their item")
        if "jar_sha256" in item and not re.fullmatch(r"[0-9a-f]{64}", item["jar_sha256"]):
            raise ValueError("Invalid JAR SHA256")
        ids.add(wid)
        mods.add(mid)
    if set(manifest["workshop_collection"]["verified_members"]) != ids:
        raise ValueError("Collection membership and trial manifest disagree")
    for name, profile in profiles.items():
        selected = profile["workshop_ids"]
        if len(set(selected)) != len(selected) or not set(selected) <= ids:
            raise ValueError(f"Unknown or duplicate item in {name}")
        loaded = set()
        for wid in selected:
            item = next(i for i in items if i["workshop_id"] == wid)
            if not set(item["requires"]) <= loaded:
                raise ValueError(f"Unsatisfied ordered dependency in {name}")
            loaded.add(item["mod_id"])


def render(manifest, profiles, name):
    ids = profiles[name]["workshop_ids"]
    items = {i["workshop_id"]: i for i in manifest["trial_items"]}
    return ("# Generated candidate only; this does not deploy or accept a server profile.\n"
            + "WorkshopItems=" + ";".join(ids) + "\n"
            + "Mods=" + ";".join(items[i]["mod_id"] for i in ids) + "\n")


def check_installed(manifest, workshop):
    results = []
    for item in manifest["trial_items"]:
        root = (workshop / item["workshop_id"]).resolve()
        metadata = root / item["metadata_path"]
        if not metadata.resolve().is_relative_to(root):
            raise ValueError("Dependency metadata escapes its item")
        fields = dict(line.split("=", 1) for line in metadata.read_text().splitlines() if "=" in line)
        version = fields.get("modversion")
        if version is None and "jar_path" in item:
            with zipfile.ZipFile(root / item["jar_path"]) as archive:
                jar_fields = dict(line.split(": ", 1) for line in
                                  archive.read("META-INF/MANIFEST.MF").decode().splitlines() if ": " in line)
                version = jar_fields.get("Implementation-Version")
        if fields.get("id") != item["mod_id"] or version != item["version"]:
            raise ValueError(f"Installed ID/version drift: {item['mod_id']}")
        result = {"workshop_id": item["workshop_id"], "mod_id": fields["id"],
                  "version": version,
                  "metadata_sha256": hashlib.sha256(metadata.read_bytes()).hexdigest()}
        if "jar_path" in item:
            jar = root / item["jar_path"]
            if not jar.resolve().is_relative_to(root):
                raise ValueError("Dependency JAR escapes its item")
            with jar.open("rb") as source:
                digest = hashlib.file_digest(source, "sha256").hexdigest()
            if digest != item["jar_sha256"]:
                raise ValueError(f"Installed JAR drift: {item['mod_id']}")
            result["jar_sha256"] = digest
        results.append(result)
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["validate", "profile", "check-installed"])
    parser.add_argument("--profile", default="vanilla")
    parser.add_argument("--workshop-root", type=Path, default=WORKSHOP)
    args = parser.parse_args()
    manifest = json.loads((ROOT / "config/modpack.json").read_text())
    profiles = json.loads((ROOT / "config/profiles.json").read_text())
    validate(manifest, profiles)
    if args.command == "profile":
        if args.profile not in profiles:
            parser.error("Unknown profile")
        print(render(manifest, profiles, args.profile), end="")
    elif args.command == "check-installed":
        print(json.dumps(check_installed(manifest, args.workshop_root), indent=2))
    else:
        print(f"Manifest valid: {len(manifest['trial_items'])} trial items, {len(profiles)} explicit profiles")


if __name__ == "__main__":
    main()

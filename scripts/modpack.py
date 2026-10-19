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


def catalog(manifest):
    return manifest["trial_items"] + manifest.get("candidate_items", [])


def validate(manifest, profiles):
    items = catalog(manifest)
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
        for field in ["jar_sha256", "metadata_sha256", "payload_sha256"]:
            if field in item and not re.fullmatch(r"[0-9a-f]{64}", item[field]):
                raise ValueError(f"Invalid SHA256: {field}")
        ids.add(wid)
        mods.add(mid)
    if set(manifest["workshop_collection"]["verified_members"]) != {i["workshop_id"] for i in manifest["trial_items"]}:
        raise ValueError("Collection membership and trial manifest disagree")
    local_ids = set()
    for item in manifest.get("local_items", []):
        mid = item["mod_id"]
        path = Path(item["source"])
        if not re.fullmatch(r"[A-Za-z0-9_.-]+", mid) or mid in mods or mid in local_ids or \
                path.is_absolute() or ".." in path.parts or not path.parts or path.parts[0] != "mods":
            raise ValueError("Invalid local companion identity/path")
        local_ids.add(mid)
    for name, profile in profiles.items():
        local = profile.get("local_mod_ids", [])
        if len(set(local)) != len(local) or not set(local) <= local_ids:
            raise ValueError("Unknown or duplicate local mod")
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
    items = {i["workshop_id"]: i for i in catalog(manifest)}
    return ("# Generated candidate only; this does not deploy or accept a server profile.\n"
            + "WorkshopItems=" + ";".join(ids) + "\n"
            + "Mods=" + ";".join([items[i]["mod_id"] for i in ids] + profiles[name].get("local_mod_ids", [])) + "\n")


def check_installed(manifest, workshop, full=False):
    results = []
    for item in catalog(manifest):
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
        if "metadata_sha256" in item and result["metadata_sha256"] != item["metadata_sha256"]:
            raise ValueError(f"Installed metadata drift: {item['mod_id']}")
        if "jar_path" in item:
            jar = root / item["jar_path"]
            if not jar.resolve().is_relative_to(root):
                raise ValueError("Dependency JAR escapes its item")
            with jar.open("rb") as source:
                digest = hashlib.file_digest(source, "sha256").hexdigest()
            if digest != item["jar_sha256"]:
                raise ValueError(f"Installed JAR drift: {item['mod_id']}")
            result["jar_sha256"] = digest
        if full:
            tree = hashlib.sha256()
            count, size = 0, 0
            for path in sorted(root.rglob("*")):
                if path.is_symlink():
                    raise ValueError("Unexpected symlink in upstream payload")
                if path.is_file():
                    with path.open("rb") as source:
                        digest = hashlib.file_digest(source, "sha256").hexdigest()
                    tree.update((path.relative_to(root).as_posix() + "\0" + digest + "\n").encode())
                    count += 1
                    size += path.stat().st_size
            result.update(payload_sha256=tree.hexdigest(), payload_file_count=count, payload_bytes=size)
            if "payload_sha256" in item and item["payload_sha256"] != tree.hexdigest():
                raise ValueError(f"Installed payload drift: {item['mod_id']}")
        results.append(result)
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["validate", "profile", "check-installed"])
    parser.add_argument("--profile", default="vanilla")
    parser.add_argument("--workshop-root", type=Path, default=WORKSHOP)
    parser.add_argument("--full", action="store_true", help="Fingerprint every upstream payload file")
    args = parser.parse_args()
    manifest = json.loads((ROOT / "config/modpack.json").read_text())
    profiles = json.loads((ROOT / "config/profiles.json").read_text())
    validate(manifest, profiles)
    if args.command == "profile":
        if args.profile not in profiles:
            parser.error("Unknown profile")
        print(render(manifest, profiles, args.profile), end="")
    elif args.command == "check-installed":
        print(json.dumps(check_installed(manifest, args.workshop_root, args.full), indent=2))
    else:
        print(f"Manifest valid: {len(catalog(manifest))} upstream catalog items, {len(profiles)} explicit profiles; NOT release accepted")


if __name__ == "__main__":
    main()

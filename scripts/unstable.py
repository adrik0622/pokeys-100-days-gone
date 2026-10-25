#!/usr/bin/env python3
"""Render the field list or read public Steam metadata. Never deploys/publishes."""
import argparse
import hashlib
import json
from pathlib import Path
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "config/unstable.json"


def api(method, fields):
    request = urllib.request.Request(
        "https://api.steampowered.com/ISteamRemoteStorage/" + method + "/v1/",
        data=urllib.parse.urlencode(fields).encode(),
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)["response"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["render", "verify", "snapshot"])
    parser.add_argument("--workshop-root", type=Path, default=Path.home() /
                        ".local/share/Steam/steamapps/workshop/content/108600")
    args = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text())
    mods = manifest["mods"]
    seen, workshop_ids = set(), []
    for mod in mods:
        missing = set(mod["requires"]) - seen
        if missing or mod["mod_id"] in seen:
            raise SystemExit(f"Invalid dependency order/duplicate: {mod['mod_id']}: {missing}")
        if mod["mod_id"] in manifest["excluded_mod_ids"]:
            raise SystemExit("Excluded mod in field list: " + mod["mod_id"])
        seen.add(mod["mod_id"])
        workshop_ids.append(mod["workshop_id"])
    if len(workshop_ids) != len(set(workshop_ids)):
        raise SystemExit("Duplicate Workshop item")
    if args.action == "render":
        print("WorkshopItems=" + ";".join(workshop_ids))
        print("Mods=" + ";".join(mod["mod_id"] for mod in mods))
        return
    collection = manifest["collection_id"]
    children = api("GetCollectionDetails", {
        "collectioncount": 1, "publishedfileids[0]": collection,
    })["collectiondetails"][0]
    if children.get("result") != 1:
        raise SystemExit("Public collection details unavailable")
    actual = [child["publishedfileid"] for child in children.get("children", [])]
    if len(actual) != len(workshop_ids) or set(actual) != set(workshop_ids):
        raise SystemExit(f"Membership mismatch: missing={set(workshop_ids)-set(actual)} "
                         f"extra={set(actual)-set(workshop_ids)}")
    ids = [collection] + workshop_ids
    details = api("GetPublishedFileDetails", {
        "itemcount": len(ids), **{f"publishedfileids[{i}]": wid for i, wid in enumerate(ids)}
    })["publishedfiledetails"]
    if {item["publishedfileid"] for item in details} != set(ids):
        raise SystemExit("Incomplete public item metadata")
    for item in details:
        if item.get("result") != 1 or item.get("banned") or item.get("visibility") != 0:
            raise SystemExit("Not publicly available: " + item["publishedfileid"])
    if args.action == "verify":
        print(f"Public collection {collection}: exact {len(mods)} members, all public/unbanned. "
              "Metadata only; not gameplay acceptance or completion of Steam moderation.")
        return
    result = {"collection_id": collection, "game_version": manifest["game_version"],
              "observed_date": "2026-10-25", "kind": "observation, not immutable Workshop lock",
              "items": []}
    for item in details:
        row = {key: item.get(key) for key in
               ["publishedfileid", "title", "time_updated", "visibility", "banned"]}
        if item["publishedfileid"] != collection:
            folder = args.workshop_root / item["publishedfileid"]
            files = sorted(p for p in folder.rglob("*") if p.is_file())
            if not files:
                raise SystemExit("Missing local payload: " + str(folder))
            digest = hashlib.sha256()
            for path in files:
                digest.update(path.relative_to(folder).as_posix().encode() + b"\0")
                digest.update(hashlib.sha256(path.read_bytes()).digest())
            row.update(payload_sha256=digest.hexdigest(), files=len(files),
                       mod_info=[str(p.relative_to(folder)) for p in files if p.name == "mod.info"])
        result["items"].append(row)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

"""Offline snapshot/restore for the one disposable vanilla profile only.

The controller checks that its tracked server exited before calling these.
No production paths, deletion, or in-place overwrites are supported.
"""

import hashlib
import json
from pathlib import Path
import re
import shutil
import time

PARTS = ["Saves/Multiplayer/pokeys-m0-vanilla", "Server", "db"]


def fingerprint(directory):
    result = {}
    for path in sorted(directory.rglob("*")):
        if path.is_symlink():
            raise ValueError("Snapshots must not contain symlinks")
        if path.is_file() and path != directory / "snapshot.json":
            with path.open("rb") as source:
                result[str(path.relative_to(directory))] = hashlib.file_digest(source, "sha256").hexdigest()
    return result


def backup(root):
    cache = root / "runtime/server/vanilla"
    if not all((cache / part).is_dir() for part in PARTS):
        raise ValueError("Expected the complete disposable world/config/account database")
    snapshot = root / "runtime/server/backups" / (time.strftime("%Y%m%d-%H%M%S") + "-vanilla")
    snapshot.mkdir(parents=True)
    for part in PARTS:
        fingerprint(cache / part)
        shutil.copytree(cache / part, snapshot / part)
    files = fingerprint(snapshot)
    (snapshot / "snapshot.json").write_text(json.dumps({"profile": "vanilla", "files": files}, indent=2) + "\n")
    return {"snapshot": snapshot.name, "files": len(files), "path": str(snapshot)}


def restore(root, name):
    if not isinstance(name, str) or not re.fullmatch(r"[0-9]{8}-[0-9]{6}-vanilla", name):
        raise ValueError("Expected an existing generated vanilla snapshot name")
    snapshot = root / "runtime/server/backups" / name
    if snapshot.is_symlink() or not snapshot.is_dir():
        raise ValueError("Snapshot must be a real directory")
    metadata = json.loads((snapshot / "snapshot.json").read_text())
    if metadata.get("profile") != "vanilla" or fingerprint(snapshot) != metadata["files"]:
        raise ValueError("Snapshot integrity mismatch; current state has not been changed")
    cache = root / "runtime/server/vanilla"
    recovery = root / "runtime/server/recovery" / time.strftime("%Y%m%d-%H%M%S")
    recovery.mkdir(parents=True)
    for part in PARTS:
        old = cache / part
        if old.exists():
            retained = recovery / part
            retained.parent.mkdir(parents=True, exist_ok=True)
            old.rename(retained)
        shutil.copytree(snapshot / part, old)
    return {"restored": name, "retained_previous_state": str(recovery), "files": len(metadata["files"])}

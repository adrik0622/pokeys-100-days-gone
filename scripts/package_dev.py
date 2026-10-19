#!/usr/bin/env python3
"""Create a deterministic, original-files-only DEVELOPMENT archive from clean local Git."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PREFIXES = ("mods/", "config/", "scripts/", "tests/")
ROOT_FILES = {"README.md", "AGENTS.md", "PROJECT_BRIEF.txt", "HANDOFF.txt", ".gitignore"}


def included(name):
    path = PurePosixPath(name)
    if path.is_absolute() or ".." in path.parts or "__pycache__" in path.parts:
        return False
    if name in ROOT_FILES or name.startswith(PREFIXES):
        return True
    return name.startswith("docs/") and name.endswith(".md")


def build(root, names, revision, output):
    """Explicit tracked names only. Never traverse saves, downloads, secrets or symlinks."""
    if not revision or any(c not in "0123456789abcdef" for c in revision):
        raise ValueError("Expected hexadecimal local Git revision")
    files = {}
    for name in sorted(set(names)):
        if not included(name):
            continue
        path = root / name
        if path.is_symlink() or any(p.is_symlink() for p in path.parents if p != root):
            raise ValueError("Refusing symlink in original package")
        if not path.resolve().is_relative_to(root.resolve()) or not path.is_file():
            raise ValueError("Missing or escaping package source")
        files[name] = path.read_bytes()
    if "README.md" not in files or not any(n.endswith("/mod.info") for n in files):
        raise ValueError("Incomplete original development package")
    manifest = {"status": "DEVELOPMENT_NOT_V1", "git_revision": revision,
                "upstream_payloads_included": False,
                "files": {n: hashlib.sha256(v).hexdigest() for n,v in files.items()}}
    files["PACKAGE.json"] = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
    output.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation: never overwrite an artifact someone may already use.
    with zipfile.ZipFile(output, "x", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, content in sorted(files.items()):
            info = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content)
    return {"path": str(output), "files": len(files), "revision": revision,
            "sha256": hashlib.sha256(output.read_bytes()).hexdigest(), "status": manifest["status"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    def git(*args):
        return subprocess.check_output(["bash", str(ROOT / "scripts/git-local.sh"), *args],
                                       cwd=ROOT).decode().strip()
    if git("status", "--porcelain"):
        parser.error("Commit project changes first; packaging a dirty tree is refused")
    revision = git("rev-parse", "HEAD")
    names = git("ls-files", "-z").rstrip("\0").split("\0")
    output = ROOT / "runtime/dist" / ("pokeys-development-" + revision[:12] + ".zip")
    print(json.dumps(build(ROOT, names, revision, output), indent=2))


if __name__ == "__main__":
    main()

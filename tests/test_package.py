import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

SPEC = importlib.util.spec_from_file_location("package_dev", Path(__file__).resolve().parents[1] / "scripts/package_dev.py")
package = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(package)


class PackageTests(unittest.TestCase):
    def test_original_allowlist_excludes_runtime_git_and_upstream(self):
        for name in ["runtime/admin-password.txt", ".local-git/config", "assets/upstream.jar",
                     "docs/evidence/private.png", "../README.md", "/README.md", "scripts/__pycache__/x.pyc"]:
            self.assertFalse(package.included(name), name)

    def test_deterministic_archive_hashes_sources_and_never_overwrites(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("DEVELOPMENT")
            mod = root / "mods/Original/42/mod.info"; mod.parent.mkdir(parents=True); mod.write_text("id=Original")
            names = ["README.md", "mods/Original/42/mod.info", "runtime/secret.txt"]
            a, b = root / "a.zip", root / "b.zip"
            first = package.build(root, names, "a" * 40, a)
            second = package.build(root, names, "a" * 40, b)
            self.assertEqual(first["sha256"], second["sha256"])
            with zipfile.ZipFile(a) as archive:
                self.assertNotIn("runtime/secret.txt", archive.namelist())
                manifest = json.loads(archive.read("PACKAGE.json"))
                self.assertEqual(manifest["status"], "DEVELOPMENT_NOT_V1")
                self.assertFalse(manifest["upstream_payloads_included"])
                self.assertEqual(len(manifest["files"]), 2)
            with self.assertRaises(FileExistsError): package.build(root, names, "a" * 40, a)
            mod.unlink(); mod.symlink_to(root / "README.md")
            with self.assertRaises(ValueError): package.build(root, names, "a" * 40, root / "c.zip")

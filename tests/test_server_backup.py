import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("server_backup", ROOT / "scripts/server_backup.py")
backup = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(backup)


class BackupTests(unittest.TestCase):
    def setup_cache(self, root):
        cache = root / "runtime/server/vanilla"
        for part in backup.PARTS:
            (cache / part).mkdir(parents=True)
            (cache / part / "marker").write_text("before")
        return cache

    def test_restore_checks_hashes_and_retains_previous_state(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            cache = self.setup_cache(root)
            snapshot = backup.backup(root)
            for part in backup.PARTS:
                (cache / part / "marker").write_text("after")
            result = backup.restore(root, snapshot["snapshot"])
            for part in backup.PARTS:
                self.assertEqual((cache / part / "marker").read_text(), "before")
                self.assertEqual((Path(result["retained_previous_state"]) / part / "marker").read_text(), "after")

    def test_corrupt_snapshot_refuses_before_changing_world(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            cache = self.setup_cache(root)
            snapshot = backup.backup(root)
            (Path(snapshot["path"]) / backup.PARTS[0] / "marker").write_text("corrupt")
            with self.assertRaisesRegex(ValueError, "integrity"):
                backup.restore(root, snapshot["snapshot"])
            self.assertEqual((cache / backup.PARTS[0] / "marker").read_text(), "before")

    def test_refuses_path_escape_and_symlinks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            cache = self.setup_cache(root)
            for name in ["../outside", "/tmp", None]:
                with self.assertRaises(ValueError):
                    backup.restore(root, name)
            (cache / backup.PARTS[0] / "link").symlink_to(root)
            with self.assertRaisesRegex(ValueError, "symlink"):
                backup.backup(root)


if __name__ == "__main__":
    unittest.main()

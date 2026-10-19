import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("modpack", ROOT / "scripts/modpack.py")
modpack = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(modpack)


class ModpackTests(unittest.TestCase):
    def test_integrated_profile_does_not_add_candidates_to_collection(self):
        text = modpack.render(self.manifest, self.profiles, "integrated")
        self.assertIn("Mods=ZombieBuddy;Viewpoint;PZVoxelStudioViewpoint;Bandits2;HordeNights;Pokeys100DaysGone", text)
        self.assertNotIn("Screamer", text)
        self.assertEqual(len(self.manifest["workshop_collection"]["verified_members"]), 3)

    def test_candidate_and_local_profiles_do_not_claim_collection_membership(self):
        modpack.validate(self.manifest, self.profiles)
        self.assertIn("Mods=HordeNights;Pokeys100DaysGone", modpack.render(self.manifest,self.profiles,"migration"))
        self.assertNotIn("3782615002", self.manifest["workshop_collection"]["verified_members"])
        self.profiles["migration"]["local_mod_ids"]=["Unknown"]
        with self.assertRaises(ValueError): modpack.validate(self.manifest,self.profiles)

    def setUp(self):
        self.manifest = json.loads((ROOT / "config/modpack.json").read_text())
        self.profiles = json.loads((ROOT / "config/profiles.json").read_text())

    def test_current_manifest_and_explicit_profiles_validate(self):
        modpack.validate(self.manifest, self.profiles)
        self.assertEqual(modpack.render(self.manifest, self.profiles, "vanilla").splitlines()[-2:],
                         ["WorkshopItems=", "Mods="])
        self.assertIn("Mods=ZombieBuddy;Viewpoint;PZVoxelStudioViewpoint\n",
                      modpack.render(self.manifest, self.profiles, "presentation-trial"))

    def test_reject_duplicate_or_unsafe_dependency(self):
        for field, value in [("workshop_id", "3619862853"), ("mod_id", "bad;Injected"),
                             ("metadata_path", "../outside"), ("jar_sha256", "invalid")]:
            manifest = copy.deepcopy(self.manifest)
            manifest["trial_items"][1][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                modpack.validate(manifest, self.profiles)

    def test_reject_unsatisfied_dependency_or_collection_drift(self):
        for ids in [["3809306528"], ["unknown"], ["3619862853", "3619862853"]]:
            profiles = {"bad": {"workshop_ids": ids}}
            with self.subTest(ids=ids), self.assertRaises(ValueError):
                modpack.validate(self.manifest, profiles)
        self.manifest["workshop_collection"]["verified_members"].pop()
        with self.assertRaises(ValueError):
            modpack.validate(self.manifest, self.profiles)

    def test_installed_version_and_jar_drift_are_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            item_root = root / "1"
            item_root.mkdir()
            (item_root / "mod.info").write_text("id=Test\r\nmodversion=1.0\r\n")
            item = {"workshop_id": "1", "mod_id": "Test", "version": "1.0", "metadata_path": "mod.info"}
            manifest = {"trial_items": [item]}
            self.assertEqual(modpack.check_installed(manifest, root)[0]["version"], "1.0")
            item["version"] = "2.0"
            with self.assertRaisesRegex(ValueError, "drift"):
                modpack.check_installed(manifest, root)
            item["version"] = "1.0"
            with zipfile.ZipFile(item_root / "test.jar", "w") as jar:
                jar.writestr("META-INF/MANIFEST.MF", "Implementation-Version: 1.0\r\n")
            item.update(jar_path="test.jar", jar_sha256="0" * 64)
            with self.assertRaisesRegex(ValueError, "JAR drift"):
                modpack.check_installed(manifest, root)

    def test_full_fingerprint_detects_same_version_asset_change(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            item_root = root / "1"
            item_root.mkdir()
            (item_root / "mod.info").write_text("id=Models\nmodversion=1.0\n")
            (item_root / "model.asset").write_bytes(b"original")
            item = {"workshop_id": "1", "mod_id": "Models", "version": "1.0", "metadata_path": "mod.info"}
            manifest = {"trial_items": [item]}
            item["payload_sha256"] = modpack.check_installed(manifest, root, full=True)[0]["payload_sha256"]
            (item_root / "model.asset").write_bytes(b"changed without a version bump")
            with self.assertRaisesRegex(ValueError, "payload drift"):
                modpack.check_installed(manifest, root, full=True)


if __name__ == "__main__":
    unittest.main()

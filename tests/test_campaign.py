"""Run project Lua on Lua 5.1; engine-only behavior remains a separate gate."""
from pathlib import Path
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CampaignTests(unittest.TestCase):
    def test_v2_recurring_relief_rules_and_actual_server_adapter(self):
        result = subprocess.run(["lua5.1", "tests/lua/v2_relief_spec.lua"], cwd=ROOT,
                                text=True, capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS: recurring relief rules", result.stdout)
        self.assertIn("PASS: recurring relief server authority", result.stdout)

    def test_encounter_adapter_is_admin_only_fixed_and_one_shot(self):
        result = subprocess.run(["lua5.1", "tests/lua/encounter_spec.lua"], cwd=ROOT,
                                text=True, capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS: encounter adapter", result.stdout)

    def test_observer_rules_and_real_server_adapter(self):
        result = subprocess.run(["lua5.1", "tests/lua/migration_spec.lua"], cwd=ROOT,
                                text=True, capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS: observer rules", result.stdout)
        self.assertIn("PASS: observer server adapter", result.stdout)

    def test_lua_51_syntax(self):
        compiler = shutil.which("luac5.1")
        self.assertIsNotNone(compiler, "Lua 5.1 compiler is required for companion checks")
        sources = sorted((ROOT / "mods/Pokeys100DaysGone").rglob("*.lua"))
        result = subprocess.run([compiler, "-p", *map(str, sources)], cwd=ROOT,
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_campaign_rules_and_real_server_adapter(self):
        interpreter = shutil.which("lua5.1")
        self.assertIsNotNone(interpreter, "Lua 5.1 is required for companion checks")
        result = subprocess.run([interpreter, "tests/lua/campaign_spec.lua"], cwd=ROOT,
                                text=True, capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS: campaign rules", result.stdout)
        self.assertIn("PASS: server authority", result.stdout)

    def test_v2_bridge_pure_rules(self):
        result = subprocess.run(["lua5.1", "tests/lua/v2_rules_spec.lua"], cwd=ROOT,
                                text=True, capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS: V2 bridge pure rules", result.stdout)

    def test_v2_server_adapter_authority_replay_and_partial_aid_failure(self):
        result = subprocess.run(["lua5.1", "tests/lua/v2_server_spec.lua"], cwd=ROOT,
                                text=True, capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS: V2 server adapter", result.stdout)

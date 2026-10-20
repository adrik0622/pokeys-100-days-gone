"""V2 composition/fixture boundaries, not game-engine certification."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

SPEC = importlib.util.spec_from_file_location("control_v2", Path(__file__).resolve().parents[1] / "scripts/desktop_control.py")
control = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(control)


class V2TrialTests(unittest.TestCase):
    def test_isolated_trials_stage_only_explicit_inputs_and_keep_mod_ids(self):
        for name, spec in control.V2_TRIALS.items():
            with self.subTest(profile=name), tempfile.TemporaryDirectory() as directory, \
                 patch.object(control, "ROOT", Path(directory)), \
                 patch.object(control, "stage_campaign") as local, \
                 patch.object(control, "stage_upstream") as stage, \
                 patch.object(control.shutil, "copy2"), patch.object(control.subprocess, "Popen") as popen:
                result = control.Desktop().launch_server(name)
                self.assertEqual(result["ports"], [spec["port"], spec["port"] + 1])
                self.assertEqual(result["bind_ip"], "127.0.0.1")
                self.assertNotIn("javaagent", str(popen.call_args.args[0]))
                if spec.get("project_mod"):
                    local.assert_called_once_with(Path(directory) / "runtime/server" / name)
                else:
                    local.assert_not_called()
                stage.assert_called_once_with(Path(directory) / "runtime/server" / name, spec["items"])
                stage.reset_mock()
                cache = control.prepare_profile(name, "a")
                stage.assert_called_once_with(cache, spec["items"])
                enabled = (cache / "mods/default.txt").read_text()
                for mid in spec["mods"]:
                    self.assertIn(f"mod = {mid},", enabled)
                for mid in ["Bandits", "HordeNights", "Viewpoint", "ProjectALife"]:
                    if not spec.get("alife_owner"):
                        self.assertNotIn(mid, enabled)
                if spec.get("project_mod"):
                    self.assertIn("mod = Pokeys100DaysGone,", enabled)
                else:
                    self.assertNotIn("mod = Pokeys100DaysGone,", enabled)

    def test_supplies_ignore_arbitrary_arguments_and_refuse_other_worlds(self):
        d = control.Desktop(); d.server = Mock(); d.server.poll.return_value = None
        for profile, expected in [
            ("supply-trial", ["additem pokeys_supply_a Base.WalkieTalkie5 1\n", "additem pokeys_supply_a Base.Battery 1\n"]),
            ("mission-trial", ["additem pokeys_mission_a Base.Bandage 2\n"]),
            ("contract-trial", ["additem pokeys_contract_a Base.Bandage 2\n"]),
            ("faction-contract-trial", ["additem pokeys_faction_contract_a Base.Bandage 2\n"]),
        ]:
            d.server_profile = profile; d.server.stdin.write.reset_mock()
            d.dispatch({"action": "server_v2_supplies", "username": "unrelated", "count": 999})
            self.assertEqual([c.args[0] for c in d.server.stdin.write.call_args_list], expected)
        d.server.poll.return_value = 0
        with self.assertRaises(RuntimeError): d.dispatch({"action": "server_v2_supplies"})
        with self.assertRaises(ValueError): d.dispatch({"action": "server_restore", "snapshot": "unrelated"})
        d.server_profile = "alife-jeem"
        with self.assertRaises(RuntimeError): d.dispatch({"action": "server_v2_supplies"})
        d.server_profile = "contract-trial"
        with self.assertRaises(RuntimeError): d.dispatch({"action": "server_v2_supplies"})

    def test_faction_contract_fixture_keeps_a_life_helpers_profile_scoped(self):
        self.assertTrue(control.alife_profile("faction-contract-trial"))
        self.assertFalse(control.alife_profile("contract-trial"))
        d = control.Desktop(); d.server = Mock(); d.server.poll.return_value = None
        d.server_profile = "faction-contract-trial"; d.profile = "contract-trial"
        with self.assertRaises(RuntimeError): d.dispatch({"action": "test_alife_contact_approach", "scope": "game"})
        d.profile = "faction-contract-trial"
        with patch.object(d, "window", return_value="owned-window"), patch.object(control, "run") as run:
            d.dispatch({"action": "test_alife_contact_approach", "scope": "game"})
            self.assertIn("/teleportto 7995,11756,0", run.call_args.args)

    def test_ownership_supplies_are_fixed_per_named_account_and_world(self):
        d = control.Desktop(); d.server = Mock(); d.server.poll.return_value = None
        d.server_profile = "faction-ownership-trial"
        for client in ("a", "b"):
            with self.subTest(client=client):
                d.server.stdin.write.reset_mock()
                d.dispatch({"action": "server_v2_supplies", "client": client,
                            "username": "unrelated", "count": 999, "item": "Base.Shotgun"})
                d.server.stdin.write.assert_called_once_with(
                    f"additem pokeys_ownership_{client} Base.Bandage 2\n")
        with self.assertRaises(ValueError):
            d.dispatch({"action": "server_v2_supplies"})
        d.server.poll.return_value = 0
        with self.assertRaises(RuntimeError):
            d.dispatch({"action": "server_v2_supplies", "client": "a"})
        d.server.poll.return_value = None
        d.server_profile = "vanilla"
        with self.assertRaises(RuntimeError):
            d.dispatch({"action": "server_v2_supplies", "client": "b"})

    def test_ownership_fixture_preserves_checksum_and_single_npc_owner(self):
        root = Path(__file__).resolve().parents[1]
        ini = (root / "config/server/faction-ownership-trial.ini").read_text()
        sandbox = (root / "config/server/faction-ownership-trial_SandboxVars.lua").read_text()
        self.assertIn("DoLuaChecksum=true", ini)
        self.assertIn("DefaultPort=19750", ini)
        self.assertIn("Mods=ProjectALifeNPCs;ProjectALifeJimmy;TheMission42;Pokeys100DaysGone", ini)
        self.assertNotIn("Bandits", ini)
        self.assertNotIn("HordeNights", ini)
        self.assertIn("PopulationMultiplier = 0.0", sandbox)
        self.assertIn("EnableMissionReset = false", sandbox)


if __name__ == "__main__": unittest.main()

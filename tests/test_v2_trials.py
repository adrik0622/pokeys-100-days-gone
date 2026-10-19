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


if __name__ == "__main__": unittest.main()

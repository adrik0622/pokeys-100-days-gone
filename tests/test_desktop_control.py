"""Focused checks for the host bridge's input and process boundaries."""

import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import Mock, patch

SPEC = importlib.util.spec_from_file_location(
    "desktop_control", Path(__file__).resolve().parents[1] / "scripts/desktop_control.py")
control = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(control)


class DesktopControlTests(unittest.TestCase):
    def test_alife_trials_have_one_npc_owner_and_separate_worlds(self):
        for profile, port in [("alife", 19810), ("alife-jeem", 19800)]:
            with self.subTest(profile=profile), tempfile.TemporaryDirectory() as directory, \
                 patch.object(control, "ROOT", Path(directory)), \
                 patch.object(control, "stage_campaign") as local, \
                 patch.object(control, "stage_upstream") as stage, \
                 patch.object(control.shutil, "copy2") as copy, \
                 patch.object(control.subprocess, "Popen") as popen:
                result = control.Desktop().launch_server(profile)
                self.assertEqual(result["ports"], [port, port + 1])
                self.assertEqual(result["bind_ip"], "127.0.0.1")
                local.assert_not_called()
                stage.assert_called_once_with(Path(directory)/"runtime/server"/profile, control.ALIFE_TRIALS[profile])
                copy.assert_any_call(Path(directory)/f"config/server/{profile}_SandboxVars.lua",
                                     Path(directory)/f"runtime/server/{profile}/Server/pokeys-m0-{profile}_SandboxVars.lua")
                self.assertNotIn("-javaagent:", str(popen.call_args.args[0]))
                stage.reset_mock()
                cache = control.prepare_profile(profile, "a")
                stage.assert_called_once_with(cache, control.ALIFE_TRIALS[profile])
                enabled = (cache / "mods/default.txt").read_text()
                self.assertIn("mod = ProjectALifeNPCs,", enabled)
                self.assertEqual("mod = ProjectALifeJimmy," in enabled, profile == "alife-jeem")
                for forbidden in ["Bandits", "HordeNights", "Viewpoint", "Pokeys100DaysGone"]:
                    self.assertNotIn(forbidden, enabled)

    def test_alife_password_and_restore_remain_scoped(self):
        desktop = control.Desktop()
        desktop.server = Mock(); desktop.server.poll.return_value = None
        desktop.server_profile = "alife"
        desktop.client_profiles["a"] = "alife-jeem"
        with patch.object(desktop, "window", return_value=42), patch.object(control, "run") as run:
            with self.assertRaises(RuntimeError):
                desktop.dispatch({"action": "test_admin_password", "client": "a"})
            run.assert_not_called()
        desktop.server.poll.return_value = 0
        with self.assertRaises(ValueError):
            desktop.dispatch({"action": "server_restore", "snapshot": "unrelated"})

    def test_integrated_profile_is_explicit_isolated_and_keeps_loader_policy(self):
        selected = control.PRESENTATION + [("3268487204", "Bandits"), ("3782615002", "HordeNights")]
        with tempfile.TemporaryDirectory() as directory, patch.object(control, "ROOT", Path(directory)), \
             patch.object(control, "stage_campaign") as local, patch.object(control, "stage_upstream") as stage, \
             patch.object(control.shutil, "copy2") as copy, patch.object(control.subprocess, "Popen") as popen:
            desktop = control.Desktop()
            result = desktop.launch_server("integrated")
            self.assertEqual(result["ports"], [19820, 19821])
            self.assertEqual(result["bind_ip"], "127.0.0.1")
            stage.assert_called_once_with(Path(directory) / "runtime/server/integrated", selected)
            local.assert_called_once()
            copy.assert_any_call(Path(directory)/"config/server/integrated_SandboxVars.lua",
                                 Path(directory)/"runtime/server/integrated/Server/pokeys-m0-integrated_SandboxVars.lua")
            self.assertIn("policy=deny-new", popen.call_args.args[0][1])
            stage.reset_mock()
            cache = control.prepare_profile("integrated", "a")
            stage.assert_called_once_with(cache, selected)
            enabled = (cache / "mods/default.txt").read_text()
            self.assertIn("mod = Bandits2,", enabled)
            self.assertIn("mod = HordeNights,", enabled)
            self.assertNotIn("Screamer", enabled)
            self.assertNotIn("Hark", enabled)

    def test_integrated_supplies_are_fixed_and_restore_stays_refused(self):
        desktop = control.Desktop()
        desktop.server = Mock()
        desktop.server.poll.return_value = None
        desktop.server_profile = "integrated"
        desktop.dispatch({"action":"server_campaign_supplies", "username":"unrelated", "count":999})
        desktop.server.stdin.write.assert_called_once_with("additem pokeys_integrated_a Base.Bandage 2\n")
        desktop.server.poll.return_value = 0
        with self.assertRaises(ValueError):
            desktop.dispatch({"action":"server_restore", "snapshot":"unrelated"})

    def test_day100_profile_stages_only_original_companion_and_uses_distinct_calendar(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(control, "ROOT", Path(directory)), \
             patch.object(control, "stage_campaign") as local, patch.object(control, "stage_upstream") as upstream, \
             patch.object(control.shutil, "copy2") as copy, patch.object(control.subprocess, "Popen"):
            result=control.Desktop().launch_server("day100")
            self.assertEqual(result["ports"],[19830,19831])
            local.assert_called_once()
            upstream.assert_not_called()
            copy.assert_any_call(Path(directory)/"config/server/day100_SandboxVars.lua",
                                 Path(directory)/"runtime/server/day100/Server/pokeys-m0-day100_SandboxVars.lua")

    def test_encounter_approach_is_fixed_and_bound_to_matching_client_and_server(self):
        desktop=control.Desktop()
        with patch.object(desktop,"window",return_value=42), patch.object(control,"run") as run:
            with self.assertRaises(RuntimeError): desktop.dispatch({"action":"test_encounter_approach","client":"a"})
            desktop.server=Mock(); desktop.server.poll.return_value=None
            desktop.server_profile="encounter"; desktop.client_profiles["a"]="encounter"
            desktop.dispatch({"action":"test_encounter_approach","client":"a","command":"unrelated"})
            self.assertEqual(run.call_args.args[-1],"/teleportto 8045,11756,0")

    def test_encounter_profile_never_adds_horde_or_viewpoint(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(control, "ROOT", Path(directory)), \
             patch.object(control, "stage_campaign"), patch.object(control, "stage_upstream") as stage, \
             patch.object(control.shutil, "copy2"), patch.object(control.subprocess, "Popen") as popen:
            desktop=control.Desktop()
            result=desktop.launch_server("encounter")
            self.assertEqual(result["ports"], [19840,19841])
            stage.assert_called_once_with(Path(directory) / "runtime/server/encounter", [("3268487204","Bandits")])
            self.assertNotIn("-javaagent:", str(popen.call_args.args[0]))

    def test_aim_shot_checks_focus_and_releases_both_buttons_on_failure(self):
        desktop = control.Desktop()
        with patch.object(desktop, "window", return_value=42), patch.object(control.time, "sleep"), \
             patch.object(control, "run", side_effect=["", "99", "", ""]) as run:
            with self.assertRaisesRegex(RuntimeError, "Focus changed"):
                desktop.dispatch({"action": "aim_shot"})
            self.assertEqual(run.call_args_list[-2].args, ("xdotool", "mouseup", 1))
            self.assertEqual(run.call_args_list[-1].args, ("xdotool", "mouseup", 3))

    def test_migration_fixture_uses_only_selected_horde_and_local_companion(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(control, "ROOT", Path(directory)), \
             patch.object(control, "stage_campaign"), patch.object(control, "stage_upstream") as stage, \
             patch.object(control.shutil, "copy2"), patch.object(control.subprocess, "Popen") as popen:
            desktop = control.Desktop()
            result = desktop.launch_server("migration")
            self.assertEqual(result["ports"], [19850, 19851])
            stage.assert_called_once_with(Path(directory) / "runtime/server/migration", [("3782615002", "HordeNights")])
            self.assertNotIn("-javaagent:", str(popen.call_args.args[0]))
            desktop.server.poll.return_value = None
            desktop.dispatch({"action": "server_combat_supplies", "count": 999, "username": "unrelated"})
            self.assertEqual(desktop.server.stdin.write.call_args_list[0].args,
                             ("additem pokeysadmin Base.Shotgun 1\n",))
            self.assertEqual(desktop.server.stdin.write.call_args_list[1].args,
                             ("additem pokeysadmin Base.ShotgunShells 20\n",))
            desktop.server_profile = "vanilla"
            with self.assertRaises(RuntimeError):
                desktop.dispatch({"action": "server_combat_supplies"})

    def test_presentation_stages_real_copies_and_refuses_foreign_directories(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(control, "ROOT", Path(directory)), \
             patch.object(control, "GAME", Path(directory) / "steamapps/common/PZ/game"):
            workshop = control.GAME.parents[2] / "workshop/content/108600"
            for wid, name in control.PRESENTATION:
                source = workshop / wid / "mods" / name / "42"
                source.mkdir(parents=True)
                (source / "mod.info").write_text("id=" + name)
            cache = Path(directory) / "cache"
            control.stage_presentation(cache)
            self.assertFalse((cache / "mods/Viewpoint").is_symlink())
            self.assertIn("Viewpoint", (cache / "mods/Viewpoint/42/mod.info").read_text())
            control.stage_presentation(cache)
            self.assertEqual(len(list((cache / "upstream-stage-history").iterdir())), 3)
            (cache / "mods/Viewpoint/.pokeys-upstream-stage").unlink()
            with self.assertRaisesRegex(RuntimeError, "unowned upstream"):
                control.stage_presentation(cache)

    def test_presentation_server_retains_deny_new_agent_policy(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(control, "ROOT", Path(directory)), \
             patch.object(control.shutil, "copy2"), patch.object(control, "stage_campaign"), \
             patch.object(control, "stage_presentation"), patch.object(control.subprocess, "Popen") as popen:
            result = control.Desktop().launch_server("presentation")
            args = popen.call_args.args[0]
            self.assertIn("policy=deny-new", args[1])
            self.assertEqual(result["ports"], [19890, 19891])
            self.assertLess(args.index(args[1]), args.index("zombie.network.GameServer"))

    def test_campaign_stage_is_local_only_and_cannot_replace_existing_directory(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(control, "ROOT", Path(directory)):
            source = Path(directory) / "mods/Pokeys100DaysGone/42"
            source.mkdir(parents=True)
            (source / "mod.info").touch()
            cache = control.prepare_profile("campaign", "a")
            self.assertFalse((cache / "mods/Pokeys100DaysGone").is_symlink())
            self.assertTrue((cache / "mods/Pokeys100DaysGone/42/mod.info").is_file())
            self.assertIn("mod = Pokeys100DaysGone", (cache / "mods/default.txt").read_text())
            (source / "mod.info").write_text("updated")
            control.stage_campaign(cache)
            self.assertEqual((cache / "mods/Pokeys100DaysGone/42/mod.info").read_text(), "updated")
            self.assertEqual(len(list((cache / "campaign-stage-history").iterdir())), 1)
            other = Path(directory) / "different-cache"
            (other / "mods/Pokeys100DaysGone").mkdir(parents=True)
            with self.assertRaisesRegex(RuntimeError, "Refusing to replace"):
                control.stage_campaign(other)

    def test_campaign_supplies_are_fixed_and_refused_on_other_servers(self):
        desktop = control.Desktop()
        desktop.server = Mock()
        desktop.server.poll.return_value = None
        with self.assertRaisesRegex(RuntimeError, "campaign server"):
            desktop.dispatch({"action": "server_campaign_supplies"})
        desktop.server_profile = "campaign"
        desktop.dispatch({"action": "server_campaign_supplies", "username": "unrelated", "count": 900})
        desktop.server.stdin.write.assert_called_once_with("additem pokeys_campaign_a Base.Bandage 2\n")

    def test_select_all_holds_and_releases_both_polled_keys(self):
        desktop = control.Desktop()
        with patch.object(desktop, "window", return_value=42), patch.object(control, "run") as run, \
             patch.object(control.time, "sleep"):
            desktop.dispatch({"action": "select_all", "client": "b"})
            self.assertEqual(run.call_args_list[0].args, ("xdotool", "keydown", "Control_L"))
            self.assertEqual(run.call_args_list[1].args, ("xdotool", "keydown", "a"))
            self.assertEqual({call.args for call in run.call_args_list[2:]},
                             {("xdotool", "keyup", "Control_L"), ("xdotool", "keyup", "a")})
            self.assertEqual(desktop.pressed, set())

    def test_dual_profiles_do_not_share_settings_or_saves(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(control, "ROOT", Path(directory)):
            a = control.prepare_profile("vanilla", "a")
            b = control.prepare_profile("vanilla", "b")
            self.assertNotEqual(a, b)
            self.assertEqual(a.name, "client-vanilla-a")
            self.assertIn("frameRate=30", (b / "options.ini").read_text())
            (a / "options.ini").write_text("a-only")
            self.assertNotIn("a-only", (b / "options.ini").read_text())
            with self.assertRaises(ValueError):
                control.prepare_profile("vanilla", "../outside")

    def test_second_named_client_accepts_only_owned_existing_pid(self):
        desktop = control.Desktop()
        desktop.clients["a"] = Mock(pid=123)
        desktop.clients["a"].poll.return_value = None
        with tempfile.TemporaryDirectory() as directory, \
             patch.object(control, "prepare_profile", return_value=Path(directory)) as prepare, \
             patch.object(control.Path, "read_text", return_value="MemAvailable: 20000000 kB\n"), \
             patch.object(control, "run", return_value="123 ProjectZomboid6"), \
             patch.object(control.subprocess, "Popen", return_value=Mock(pid=456)) as popen:
            result = desktop.launch("vanilla", "b")
            self.assertEqual(result["pid"], 456)
            self.assertIs(desktop.clients["b"], popen.return_value)
            args = popen.call_args.args[0]
            self.assertIn("-Xmx3g", args[:args.index("--")])
            prepare.assert_called_once_with("vanilla", "b")

    def test_named_clients_reject_untracked_process_and_low_memory(self):
        desktop = control.Desktop()
        desktop.clients["a"] = Mock(pid=123)
        desktop.clients["a"].poll.return_value = None
        with patch.object(control, "run", return_value="123 ProjectZomboid6\n999 ProjectZomboid6"), \
             patch.object(control.subprocess, "Popen") as popen:
            with self.assertRaisesRegex(RuntimeError, "existing PZ client"):
                desktop.launch("vanilla", "b")
            popen.assert_not_called()
        with patch.object(control, "run", return_value="123 ProjectZomboid6"), \
             patch.object(control.Path, "read_text", return_value="MemAvailable: 5000000 kB\n"), \
             patch.object(control.subprocess, "Popen") as popen:
            with self.assertRaisesRegex(RuntimeError, "6 GiB"):
                desktop.launch("vanilla", "b")
            popen.assert_not_called()

    def test_near_simultaneous_launch_reserves_other_client_growth(self):
        desktop = control.Desktop()
        desktop.clients["a"] = Mock(pid=123)
        desktop.clients["a"].poll.return_value = None
        def read(path):
            return "MemAvailable: 11000000 kB\n" if str(path) == "/proc/meminfo" else "Pss: 10000 kB\n"
        with patch.object(control, "run", return_value="123 ProjectZomboid6"), \
             patch.object(control.Path, "read_text", autospec=True, side_effect=read), \
             patch.object(control.subprocess, "Popen") as popen:
            with self.assertRaisesRegex(RuntimeError, "growth reserve"):
                desktop.launch("vanilla", "b")
            popen.assert_not_called()

    def test_duplicate_named_slot_and_main_mixing_are_refused(self):
        desktop = control.Desktop()
        desktop.clients["a"] = Mock()
        desktop.clients["a"].poll.return_value = None
        with patch.object(control.subprocess, "Popen") as popen:
            for name in ["a", "main", "c", "../../outside"]:
                with self.subTest(name=name), self.assertRaises((ValueError, RuntimeError)):
                    desktop.launch("vanilla", name)
            popen.assert_not_called()

    def test_named_window_search_is_bound_to_correct_child_pid(self):
        desktop = control.Desktop()
        desktop.clients["b"] = Mock(pid=456)
        desktop.clients["b"].poll.return_value = None
        with patch.object(control, "run", side_effect=["42", "Project Zomboid"]) as run:
            self.assertEqual(desktop.windows("b"), [{"id": 42, "name": "Project Zomboid"}])
            self.assertEqual(run.call_args_list[0].args, ("xdotool", "search", "--onlyvisible", "--pid", 456))
        with self.assertRaises(RuntimeError):
            desktop.window(client="a")

    def test_dual_server_uses_separate_profile_ports_and_no_vanilla_restore(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(control, "ROOT", Path(directory)), \
             patch.object(control.shutil, "copy2") as copy, patch.object(control.subprocess, "Popen") as popen:
            desktop = control.Desktop()
            result = desktop.launch_server("dual")
            args = popen.call_args.args[0]
            self.assertIn(f"-cachedir={directory}/runtime/server/dual", args)
            self.assertEqual(args[args.index("-port") + 1], "19870")
            self.assertEqual(result["profile"], "dual")
            copy.assert_any_call(Path(directory) / "config/server/dual_SandboxVars.lua",
                                 Path(directory) / "runtime/server/dual/Server/pokeys-m0-dual_SandboxVars.lua")
            desktop.server.poll.return_value = 0
            with self.assertRaisesRegex(ValueError, "vanilla profile only"):
                desktop.dispatch({"action": "server_restore", "snapshot": "20261018-173100-vanilla"})

    def test_server_launch_is_loopback_isolated_and_credentials_not_returned(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(control, "ROOT", Path(directory)), \
             patch.object(control.shutil, "copy2") as copy, patch.object(control.subprocess, "Popen") as popen:
            desktop = control.Desktop()
            result = desktop.launch_server()
            args = popen.call_args.args[0]
            self.assertEqual(args[args.index("-ip") + 1], "127.0.0.1")
            self.assertIn("-nosteam", args)
            self.assertIn("-Xmx4g", args)
            self.assertIn(f"-cachedir={directory}/runtime/server/vanilla", args)
            password = args[args.index("-adminpassword") + 1]
            self.assertNotIn(password, str(result))
            self.assertEqual((Path(directory) / "runtime/server/vanilla/admin-password.txt").stat().st_mode & 0o777, 0o600)
            self.assertFalse(popen.call_args.kwargs.get("shell", False))
            self.assertEqual(copy.call_args.args[0], Path(directory) / "config/server/vanilla.ini")

    def test_server_commands_cannot_execute_arbitrary_input(self):
        desktop = control.Desktop()
        desktop.server = Mock()
        desktop.server.poll.return_value = None
        for command in ["quit\nexec", "grantadmin alice", "", None, "$(whoami)"]:
            with self.assertRaises(ValueError):
                desktop.dispatch({"action": "server_command", "command": command})
        desktop.server.stdin.write.assert_not_called()
        desktop.dispatch({"action": "server_command", "command": "save"})
        desktop.server.stdin.write.assert_called_once_with("save\n")

    def test_live_or_untracked_server_refuses_backup_and_restore(self):
        desktop = control.Desktop()
        for server in [None, Mock()]:
            desktop.server = server
            if server:
                server.poll.return_value = None
            with patch.object(control.runpy, "run_path") as helpers:
                for action in ["server_backup", "server_restore"]:
                    with self.assertRaisesRegex(RuntimeError, "exited"):
                        desktop.dispatch({"action": action, "snapshot": "20261018-173100-vanilla"})
                helpers.assert_not_called()

    def test_workshop_open_rejects_external_or_credential_urls(self):
        desktop = control.Desktop()
        with patch.object(control.subprocess, "Popen") as popen:
            for url in ["http://steamcommunity.com/sharedfiles/", "https://example.com/workshop/",
                        "https://steamcommunity.com@evil.example/sharedfiles/",
                        "https://steamcommunity.com/actions/Logout", "file:///tmp/a"]:
                with self.subTest(url=url), self.assertRaises(ValueError):
                    desktop.dispatch({"action": "workshop_open", "url": url})
            popen.assert_not_called()

    def test_workshop_attach_only_accepts_visible_steam_window(self):
        desktop = control.Desktop()
        with patch.object(desktop, "steam_windows", return_value=[{"id": 12, "name": "Steam"}]):
            with self.assertRaises(ValueError):
                desktop.dispatch({"action": "workshop_attach", "window": 13})
            desktop.dispatch({"action": "workshop_attach", "window": 12})
            self.assertEqual(desktop.window(scope="workshop"), 12)
        with patch.object(desktop, "steam_windows", return_value=[]):
            with self.assertRaises(RuntimeError):
                desktop.window(scope="workshop")

    def test_workshop_text_is_bounded_and_passed_without_shell(self):
        desktop = control.Desktop()
        with patch.object(desktop, "window", return_value=12), patch.object(control, "run") as run:
            for value in ["x" * 4097, "escape\x1b", "", None]:
                with self.assertRaises(ValueError):
                    desktop.dispatch({"action": "text", "scope": "workshop", "text": value})
            run.assert_not_called()
            desktop.dispatch({"action": "text", "scope": "workshop", "text": "Title\nDescription"})
            self.assertEqual(run.call_args.args[-2:], ("--", "Title\nDescription"))

    def test_reject_desktop_shortcuts_and_shell_text(self):
        for value in ["alt+F4", "Super_L", "ctrl+alt+t", "$(touch nope)", "a;ls", None]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                control.key(value)

    def test_reject_unbounded_or_nonfinite_hold(self):
        desktop = control.Desktop()
        with patch.object(desktop, "window", return_value=42), patch.object(control, "run") as run:
            for value in [-1, 6, float("inf"), float("nan"), True, "1"]:
                with self.subTest(value=value), self.assertRaises(ValueError):
                    desktop.dispatch({"action": "hold", "key": "w", "seconds": value})
            run.assert_not_called()

    def test_focus_loss_releases_key(self):
        desktop = control.Desktop()
        with patch.object(desktop, "window", return_value=42), \
             patch.object(control, "run", side_effect=["", "99", ""]) as run:
            with self.assertRaisesRegex(RuntimeError, "Focus changed"):
                desktop.dispatch({"action": "hold", "key": "w", "seconds": 0.2})
            self.assertEqual(run.call_args_list[-1].args, ("xdotool", "keyup", "w"))
            self.assertEqual(desktop.pressed, set())

    def test_missing_game_refuses_input(self):
        with patch.object(control, "run") as run:
            with self.assertRaisesRegex(RuntimeError, "owned game window"):
                control.Desktop().dispatch({"action": "key", "key": "e"})
            run.assert_not_called()

    def test_screenshot_cannot_escape_directory(self):
        desktop = control.Desktop()
        with patch.object(desktop, "window", return_value=42), patch.object(control, "run") as run:
            with self.assertRaises(ValueError):
                desktop.dispatch({"action": "screenshot", "name": "../../outside"})
            run.assert_not_called()

    def test_text_rejects_commands_and_control_characters(self):
        desktop = control.Desktop()
        with patch.object(desktop, "window", return_value=42), patch.object(control, "run") as run:
            for value in ["hello\nworld", "`whoami`", "$(whoami)", "x" * 81]:
                with self.assertRaises(ValueError):
                    desktop.dispatch({"action": "text", "text": value})
            run.assert_not_called()

    def test_profile_is_separate_and_survives_restart(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(control, "ROOT", Path(directory)):
            cache = control.prepare_profile("vanilla")
            self.assertEqual(cache, Path(directory) / "runtime/client-vanilla")
            self.assertIn("fullScreen=false", (cache / "options.ini").read_text())
            (cache / "options.ini").write_text("width=1280\n")
            control.prepare_profile("vanilla")
            self.assertEqual((cache / "options.ini").read_text(), "width=1280\n")
            self.assertNotIn("mod =", (cache / "mods/default.txt").read_text())
            with self.assertRaises(ValueError):
                control.prepare_profile("../../outside")

    def test_launch_uses_isolated_cache_and_no_shell(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(control, "ROOT", Path(directory)), \
             patch.object(control, "run", return_value="bash\nsteam"), \
             patch.object(control.subprocess, "Popen") as popen:
            desktop = control.Desktop()
            desktop.launch("vanilla")
            args = popen.call_args.args[0]
            self.assertIn(f"-cachedir={directory}/runtime/client-vanilla", args)
            self.assertIn("-nosteam", args)
            self.assertTrue(popen.call_args.kwargs["env"]["PATH"].startswith(str(control.GAME / "jre64/bin")))
            self.assertFalse(popen.call_args.kwargs.get("shell", False))

    def test_existing_client_refuses_second_launch(self):
        with patch.object(control, "run", return_value="ProjectZomboid6"), \
             patch.object(control.subprocess, "Popen") as popen:
            with self.assertRaisesRegex(RuntimeError, "existing PZ client"):
                control.Desktop().launch("vanilla")
            popen.assert_not_called()

    def test_viewpoint_agent_precedes_required_jvm_separator(self):
        with tempfile.TemporaryDirectory() as directory, \
             patch.object(control, "prepare_profile", return_value=Path(directory)), \
             patch.object(control, "run", return_value="bash"), \
             patch.object(control.subprocess, "Popen") as popen:
            control.Desktop().launch("viewpoint")
            args = popen.call_args.args[0]
            separator = args.index("--")
            self.assertTrue(args[separator - 1].startswith("-javaagent:"))
            self.assertIn("policy=deny-new", args[separator - 1])
            self.assertTrue(args[separator + 1].startswith("-cachedir="))
            self.assertIn("-nosteam", args[separator + 1:])

    def test_forced_shutdown_only_signals_tracked_child(self):
        desktop = control.Desktop()
        desktop.game = Mock()
        desktop.game.poll.return_value = None
        desktop.game.wait.side_effect = [subprocess.TimeoutExpired("test-child", 10), 0]
        result = desktop.dispatch({"action": "terminate"})
        self.assertTrue(result["forced"])
        desktop.game.terminate.assert_called_once_with()
        desktop.game.kill.assert_called_once_with()

    def test_close_requests_graceful_quit_without_destroying_window(self):
        desktop = control.Desktop()
        with patch.object(desktop, "window", return_value=42), patch.object(control, "run") as run:
            desktop.dispatch({"action": "close"})
            run.assert_called_once_with("xdotool", "windowquit", 42)

    def test_stale_heartbeat_refuses_to_enqueue(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(control, "STATE", Path(directory)):
            control.atomic_json(Path(directory) / "ready.json", {"session": "old", "heartbeat": 0})
            with self.assertRaisesRegex(RuntimeError, "heartbeat is stale"):
                control.send({"action": "key", "key": "e"})
            self.assertFalse((Path(directory) / "queue").exists())


if __name__ == "__main__":
    unittest.main()

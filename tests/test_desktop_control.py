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

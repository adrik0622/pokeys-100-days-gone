#!/usr/bin/env python3
"""A foreground project bridge for disposable PZ, Steam Workshop and local server tests.

Start `serve` in a normal desktop terminal; use `request` from Codex.
No network listener, shell commands, system services, or arbitrary application input.
"""

import argparse
import fcntl
import json
import math
import os
from pathlib import Path
import re
import runpy
import secrets
import shutil
import signal
import subprocess
import sys
import time
import uuid
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "runtime" / "desktop-control"
GAME = Path("/home/adrikingston/.local/share/Steam/steamapps/common/ProjectZomboid/projectzomboid")
KEYS = set("abcdefghijklmnopqrstuvwxyz0123456789") | {
    "Escape", "Return", "space", "Tab", "BackSpace", "Delete", "Home", "End",
    "Left", "Right", "Up", "Down", "Shift_L", "Control_L", "F1", "F2",
    "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12",
}


def atomic_json(path, value):
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n")
    temporary.replace(path)


def number(value, low, high):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("Expected a number")
    if not math.isfinite(value) or not low <= value <= high:
        raise ValueError(f"Value must be between {low} and {high}")
    return value


def key(value):
    if value not in KEYS:
        raise ValueError("Key is not allowed (use a single game key, no desktop shortcuts)")
    return value


def run(*args, timeout=10):
    result = subprocess.run([str(v) for v in args], capture_output=True, text=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or f"{args[0]} failed ({result.returncode})")
    return result.stdout.strip()


def prepare_profile(profile):
    if profile not in {"vanilla", "viewpoint"}:
        raise ValueError("Profile must be vanilla or viewpoint")
    cache = ROOT / "runtime" / f"client-{profile}"
    cache.mkdir(parents=True, exist_ok=True)
    # The full-screen user profile is deliberately not copied. This separate
    # cache contains only test settings and worlds, retained across restarts.
    options = cache / "options.ini"
    if not options.exists():
        options.write_text("\n".join([
            "version=8", "width=1600", "height=900", "fullScreen=false",
            "borderless=false", "frameRate=60", "vsync=true", "language=EN",
            "tutorialDone=true", "showFirstTimeSneakTutorial=false",
            "showFirstTimeSearchTutorial=false", "soundVolume=2", "musicVolume=0", "",
        ]))
    mods = cache / "mods"
    mods.mkdir(exist_ok=True)
    mod_ids = []
    if profile == "viewpoint":
        workshop = GAME.parents[2] / "workshop" / "content" / "108600"
        for workshop_id, name in [("3619862853", "ZombieBuddy"), ("3809306528", "Viewpoint"),
                                    ("3810302175", "PZVoxelStudioViewpoint")]:
            source = workshop / workshop_id / "mods" / name
            if not source.is_dir():
                raise FileNotFoundError(source)
            destination = mods / name
            if not destination.exists():
                destination.symlink_to(source, target_is_directory=True)
            mod_ids.append(name)
    default = mods / "default.txt"
    if not default.exists():
        default.write_text("VERSION = 1,\n\nmods\n{\n" +
                           "".join(f"    mod = {name},\n" for name in mod_ids) + "}\n\nmaps\n{\n}\n")
    # The engine resets default.txt without this build-reset marker.
    (mods / "reset-mods-42_00.txt").touch(exist_ok=True)
    return cache


class Desktop:
    def __init__(self):
        self.game = None
        self.profile = None
        self.pressed = set()
        self.stopping = False
        self.workshop_window = None
        self.installer = None
        self.server = None

    def launch_server(self):
        if getattr(self, "server", None) and self.server.poll() is None:
            raise RuntimeError("The disposable server is already running")
        install = ROOT / "runtime/server/install"
        cache = ROOT / "runtime/server/vanilla"
        config = cache / "Server/pokeys-m0-vanilla.ini"
        config.parent.mkdir(parents=True, exist_ok=True)
        if not config.exists():
            shutil.copy2(ROOT / "config/server/vanilla.ini", config)
        credentials = cache / "admin-password.txt"
        if not credentials.exists():
            credentials.write_text(secrets.token_urlsafe(24) + "\n")
            credentials.chmod(0o600)
        # Bind explicitly to loopback, with no UPnP or public listing. This
        # profile has no mod payloads and cannot alter the user's normal saves.
        args = [str(install / "jre64/bin/java"), "-Djava.awt.headless=true", "-Xms512m", "-Xmx4g",
                "-Dzomboid.steam=0", "-Dzomboid.znetlog=1", "-Djava.library.path=linux64/:.",
                "-Djava.security.egd=file:/dev/urandom", "-XX:+UseZGC", "-XX:-OmitStackTraceInFastThrow",
                "-cp", "java/.:java/projectzomboid.jar", "zombie.network.GameServer",
                f"-cachedir={cache}", "-servername", "pokeys-m0-vanilla", "-nosteam",
                "-ip", "127.0.0.1", "-port", "19860", "-udpport", "19861",
                "-adminusername", "pokeysadmin", "-adminpassword", credentials.read_text().strip()]
        env = os.environ.copy()
        env["LD_LIBRARY_PATH"] = ":".join(str(p) for p in
                                          [install / "linux64", install, install / "jre64/lib"])
        with (cache / "launcher.log").open("a") as output:
            self.server = subprocess.Popen(args, cwd=install, env=env, stdin=subprocess.PIPE,
                                           stdout=output, stderr=subprocess.STDOUT,
                                           text=True, start_new_session=True)
        return {"pid": self.server.pid, "cache": str(cache), "profile": "vanilla",
                "bind_ip": "127.0.0.1", "ports": [19860, 19861], "max_heap_gb": 4}

    def install_server(self):
        if getattr(self, "installer", None) and self.installer.poll() is None:
            raise RuntimeError("Dedicated-server installation is already running")
        steamcmd = ROOT / "runtime" / "steamcmd"
        steamcmd.mkdir(parents=True, exist_ok=True)
        if not (steamcmd / "steamcmd.sh").exists():
            shutil.copy2("/usr/lib/steamcmd/steamcmd.sh", steamcmd / "steamcmd.sh")
            shutil.copytree("/usr/lib/steamcmd/linux32", steamcmd / "linux32", dirs_exist_ok=True)
        destination = ROOT / "runtime" / "server" / "install"
        destination.mkdir(parents=True, exist_ok=True)
        args = [str(steamcmd / "steamcmd.sh"), "+force_install_dir", str(destination),
                "+login", "anonymous", "+app_update", "380870", "validate", "+quit"]
        logfile = ROOT / "runtime" / "server" / "install.log"
        with logfile.open("a") as output:
            self.installer = subprocess.Popen(args, cwd=steamcmd, stdout=output,
                                              stderr=subprocess.STDOUT, start_new_session=True)
        return {"pid": self.installer.pid, "args": args, "log": str(logfile)}

    def steam_windows(self):
        try:
            found = run("xdotool", "search", "--onlyvisible", "--class", "[Ss]team")
        except RuntimeError:
            return []
        return [{"id": int(value), "name": run("xdotool", "getwindowname", value)}
                for value in found.splitlines()]

    def windows(self):
        if self.game is None or self.game.poll() is not None:
            return []
        try:
            found = run("xdotool", "search", "--onlyvisible", "--pid", self.game.pid)
        except RuntimeError:
            return []
        windows = []
        for value in found.splitlines():
            name = run("xdotool", "getwindowname", value)
            if "project zomboid" in name.lower():
                windows.append({"id": int(value), "name": name})
        return windows

    def window(self, focus=False, scope="game"):
        if scope == "workshop":
            windows = [w for w in self.steam_windows() if w["id"] == self.workshop_window]
        elif scope == "game":
            windows = self.windows()
        else:
            raise ValueError("Scope must be game or workshop")
        if len(windows) != 1:
            raise RuntimeError(f"Expected one owned game window, found {len(windows)}")
        window = windows[0]["id"]
        if focus:
            run("xdotool", "windowactivate", "--sync", window, timeout=5)
            if int(run("xdotool", "getactivewindow")) != window:
                raise RuntimeError("Game focus could not be confirmed")
        return window

    def release(self):
        for value in list(self.pressed):
            try:
                run("xdotool", "keyup", value)
            finally:
                self.pressed.discard(value)

    def status(self):
        return {"display": os.environ.get("DISPLAY"),
                "geometry": run("xdotool", "getdisplaygeometry"),
                "game_pid": self.game.pid if self.game else None,
                "game_exit_code": self.game.poll() if self.game else None,
                "profile": self.profile, "windows": self.windows(),
                "pointer": run("xdotool", "getmouselocation", "--shell"),
                "active_window": run("xdotool", "getactivewindow")}

    def launch(self, profile):
        if self.game and self.game.poll() is None:
            raise RuntimeError("This bridge already has a game running")
        # Reject a second PZ client, including one started outside this bridge.
        processes = run("ps", "-eo", "comm=").splitlines()
        if any(p.strip().lower().startswith("projectzomboid") for p in processes):
            raise RuntimeError("An existing PZ client is running; close it before the test")
        cache = prepare_profile(profile)
        args = [str(GAME / "ProjectZomboid64")]
        if profile == "viewpoint":
            # pzexe requires a -- separator between JVM and game arguments.
            args.extend([f"-javaagent:{GAME / 'ZombieBuddy.jar'}=policy=deny-new", "--"])
        args.extend([f"-cachedir={cache}", "-nosteam"])
        env = os.environ.copy()
        env["PATH"] = str(GAME / "jre64/bin") + os.pathsep + env.get("PATH", os.defpath)
        env["LD_LIBRARY_PATH"] = ":".join(
            str(p) for p in [GAME / "natives", GAME, GAME / "jre64/lib"])
        env["LD_PRELOAD"] = ":".join(
            str(p) for p in [GAME / "jre64/lib/libjsig.so", GAME / "natives/libPZXInitThreads64.so"]
            if p.exists())
        env["XMODIFIERS"] = ""
        with (cache / "launcher.log").open("a") as logfile:
            self.game = subprocess.Popen(args, cwd=GAME, env=env, stdout=logfile,
                                         stderr=subprocess.STDOUT, start_new_session=True)
        self.profile = profile
        return {"pid": self.game.pid, "cache": str(cache), "args": args}

    def dispatch(self, request):
        action = request.get("action")
        scope = request.get("scope", "game")
        if action == "workshop_open":
            url = request.get("url", "https://steamcommunity.com/sharedfiles/createcollection/?appid=108600")
            parsed = urlparse(url)
            if parsed.scheme != "https" or parsed.netloc != "steamcommunity.com" or \
                    not parsed.path.startswith(("/sharedfiles/", "/workshop/", "/profiles/", "/id/",
                                                "/app/108600/workshop")):
                raise ValueError("Only Steam Community Workshop/project profile URLs are allowed")
            subprocess.Popen(["steam", "steam://openurl/" + url], stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL)
            time.sleep(1)
            return {"opened": url, "windows": self.steam_windows()}
        if action == "workshop_windows":
            return {"windows": self.steam_windows(), "attached": self.workshop_window}
        if action == "workshop_picker_info":
            window = int(run("xdotool", "getactivewindow"))
            return {"window": window, "name": run("xdotool", "getwindowname", window),
                    "properties": run("xprop", "-id", window, "WM_CLASS", "WM_TRANSIENT_FOR")}
        if action == "workshop_cover_select":
            window = int(number(request.get("window"), 1, 2**32 - 1))
            if not self.workshop_window or int(run("xdotool", "getactivewindow")) != window or \
                    '"xdg-desktop-portal-kde"' not in run("xprop", "-id", window, "WM_CLASS"):
                raise RuntimeError("Expected the inspected active KDE Workshop file chooser")
            cover = ROOT / "assets/workshop/collection-cover.png"
            if not cover.is_file():
                raise FileNotFoundError(cover)
            run("xdotool", "type", "--clearmodifiers", "--delay", "5", "--", cover)
            run("xdotool", "key", "Return")
            return {"selected": str(cover)}
        if action == "workshop_attach":
            value = int(number(request.get("window"), 1, 2**32 - 1))
            if value not in {w["id"] for w in self.steam_windows()}:
                raise ValueError("Target is not a visible Steam window")
            self.workshop_window = value
            return {"attached": value}
        if action == "status":
            return self.status()
        if action == "server_install":
            return self.install_server()
        if action == "server_install_status":
            installer = getattr(self, "installer", None)
            return {"pid": installer.pid if installer else None,
                    "exit_code": installer.poll() if installer else None}
        if action == "server_launch":
            return self.launch_server()
        if action in {"server_backup", "server_restore"}:
            server = getattr(self, "server", None)
            if not server or server.poll() is None:
                raise RuntimeError("Confirm the tracked disposable server has exited before backup/restore")
            helpers = runpy.run_path(str(ROOT / "scripts/server_backup.py"))
            if action == "server_backup":
                return helpers["backup"](ROOT)
            return helpers["restore"](ROOT, request.get("snapshot"))
        if action == "server_status":
            server = getattr(self, "server", None)
            return {"pid": server.pid if server else None,
                    "exit_code": server.poll() if server else None,
                    "udp_listeners": [line for line in run("ss", "-H", "-l", "-u", "-n").splitlines()
                                      if re.search(r":1986[01]\s", line)]}
        if action == "server_command":
            server = getattr(self, "server", None)
            command = request.get("command")
            if command not in {"save", "quit", "players"}:
                raise ValueError("Only save, quit and players are allowed for the disposable server")
            if not server or server.poll() is not None:
                raise RuntimeError("No tracked disposable server is running")
            server.stdin.write(command + "\n")
            server.stdin.flush()
            return {"sent": command, "note": "Confirm completion in the server log and status"}
        if action == "launch":
            return self.launch(request.get("profile", "vanilla"))
        if action == "stop":
            if self.game and self.game.poll() is None:
                raise RuntimeError("Close the disposable game before stopping the bridge")
            if getattr(self, "server", None) and self.server.poll() is None:
                raise RuntimeError("Quit the disposable server before stopping the bridge")
            self.stopping = True
            return {"stopping": True}
        if action == "terminate":
            # Explicit fallback, scoped to the child we launched. This is not a
            # clean-save test and is always reported as a forced termination.
            self.release()
            if not self.game or self.game.poll() is not None:
                return {"already_closed": True}
            self.game.terminate()
            try:
                self.game.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.game.kill()
                self.game.wait(timeout=5)
            return {"forced": True, "exit_code": self.game.returncode}
        window = self.window(focus=action != "screenshot", scope=scope)
        if action == "resize":
            width = int(number(request.get("width"), 640, 3440))
            height = int(number(request.get("height"), 480, 1440))
            run("xdotool", "windowsize", window, width, height)
            run("xdotool", "windowmove", window, 50, 50)
            return {"width": width, "height": height}
        if action == "screenshot":
            name = request.get("name", "screen")
            if not isinstance(name, str) or not re.fullmatch(r"[a-zA-Z0-9_-]{1,80}", name):
                raise ValueError("Screenshot name must contain only letters, digits, _ or -")
            path = STATE / "screenshots" / f"{name}.png"
            geometry = dict(line.split("=", 1) for line in
                            run("xdotool", "getwindowgeometry", "--shell", window).splitlines())
            crop = f"{geometry['WIDTH']}x{geometry['HEIGHT']}+{geometry['X']}+{geometry['Y']}"
            run("import", "-window", "root", "-crop", crop, "+repage", path)
            return {"path": str(path), "geometry": geometry}
        if action == "test_password" and scope == "game":
            credential = ROOT / "runtime/server/vanilla/client-password.txt"
            if not credential.exists():
                credential.write_text(secrets.token_hex(16) + "\n")
                credential.chmod(0o600)
            run("xdotool", "type", "--clearmodifiers", "--delay", "30", "--",
                credential.read_text().strip())
        elif action == "select_all":
            run("xdotool", "key", "ctrl+a")
        elif action == "click":
            x = int(number(request.get("x"), 0, 4096))
            y = int(number(request.get("y"), 0, 2160))
            button = int(number(request.get("button", 1), 1, 5))
            geometry = dict(line.split("=", 1) for line in
                            run("xdotool", "getwindowgeometry", "--shell", window).splitlines())
            if x >= int(geometry["WIDTH"]) or y >= int(geometry["HEIGHT"]):
                raise ValueError("Click must be inside the game window")
            # --sync can hang when the pointer is already at this position.
            run("xdotool", "mousemove", "--window", window, x, y)
            # Let the engine update its cached cursor position before the
            # button edge, otherwise a click can become an unintended drag.
            time.sleep(0.15)
            # PZ polls button state. A zero-duration XTEST click can happen
            # entirely between frames, so hold down across several frames.
            try:
                run("xdotool", "mousedown", button)
                time.sleep(0.12)
            finally:
                run("xdotool", "mouseup", button)
            time.sleep(0.15)
        elif action == "key":
            value = key(request.get("key"))
            try:
                self.pressed.add(value)
                run("xdotool", "keydown", value)
                time.sleep(0.12)
            finally:
                self.release()
        elif action == "hold":
            value = key(request.get("key"))
            duration = number(request.get("seconds"), 0.05, 5)
            try:
                self.pressed.add(value)
                run("xdotool", "keydown", value)
                deadline = time.monotonic() + duration
                while time.monotonic() < deadline:
                    if int(run("xdotool", "getactivewindow")) != window:
                        raise RuntimeError("Focus changed; released held key")
                    time.sleep(min(0.05, max(0, deadline - time.monotonic())))
            finally:
                self.release()
        elif action == "mouse":
            dx = int(number(request.get("dx"), -1500, 1500))
            dy = int(number(request.get("dy"), -1000, 1000))
            run("xdotool", "mousemove_relative", "--", dx, dy)
        elif action == "text":
            text = request.get("text")
            if scope == "workshop":
                if not isinstance(text, str) or not 1 <= len(text) <= 4096 or \
                        any(ord(c) < 32 and c not in "\n\t" for c in text):
                    raise ValueError("Workshop form text must be printable and at most 4096 characters")
            elif not isinstance(text, str) or not re.fullmatch(r"[a-zA-Z0-9 _.-]{1,80}", text):
                raise ValueError("Only short game names/text are allowed")
            run("xdotool", "type", "--clearmodifiers", "--delay", "5" if scope == "workshop" else "30",
                "--", text, timeout=60 if scope == "workshop" else 10)
        elif action == "close":
            self.release()
            # xdotool's windowclose destroys a window; windowquit sends the
            # application's graceful-close request (see installed man page).
            run("xdotool", "windowquit", window)
            return {"close_requested": True, "note": "Check status and save/log evidence to confirm exit"}
        else:
            raise ValueError(f"Unknown action: {action}")
        return {"action": action, "completed": True}


def serve():
    os.umask(0o077)
    for name in ["queue", "responses", "screenshots"]:
        (STATE / name).mkdir(parents=True, exist_ok=True)
    with (STATE / "bridge.lock").open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        # Fail before accepting work if X11 is inaccessible.
        run("xdotool", "getdisplaygeometry")
        desktop = Desktop()
        source_mtime = Path(__file__).stat().st_mtime_ns
        session = uuid.uuid4().hex
        def shutdown(_signum, _frame):
            desktop.stopping = True
        signal.signal(signal.SIGINT, shutdown)
        signal.signal(signal.SIGTERM, shutdown)
        print("PZ desktop bridge ready. Keep this terminal open; Ctrl+C stops it.", flush=True)
        print(f"Project: {ROOT}\nInput targets tracked PZ or explicitly attached Steam Workshop windows.", flush=True)
        try:
            while not desktop.stopping:
                atomic_json(STATE / "ready.json", {"session": session, "pid": os.getpid(),
                                                   "heartbeat": time.time()})
                for path in sorted((STATE / "queue").glob("*.json")):
                    request = {}
                    try:
                        # Development updates apply only between actions. Keep
                        # the tracked child and key state across code reloads.
                        current_mtime = Path(__file__).stat().st_mtime_ns
                        if current_mtime != source_mtime:
                            updated = runpy.run_path(str(Path(__file__).resolve()))
                            replacement = updated["Desktop"]()
                            replacement.__dict__.update(desktop.__dict__)
                            desktop = replacement
                            source_mtime = current_mtime
                        if path.stat().st_size > 8192:
                            raise ValueError("Request is too large")
                        request = json.loads(path.read_text())
                        if request.get("session") != session:
                            raise ValueError("Stale/wrong bridge session")
                        if abs(time.time() - request.get("created", 0)) > 60:
                            raise ValueError("Expired request")
                        result = {"ok": True, "result": desktop.dispatch(request)}
                    except Exception as exc:
                        result = {"ok": False, "error": str(exc)}
                    result["completed"] = time.time()
                    atomic_json(STATE / "responses" / path.name, result)
                    with (STATE / "actions.jsonl").open("a") as log:
                        log.write(json.dumps({"id": path.stem, "request": request,
                                              "response": result}) + "\n")
                    path.unlink()
                time.sleep(0.1)
        finally:
            desktop.release()
            if getattr(desktop, "server", None) and desktop.server.poll() is None:
                print("Requesting a clean save/quit of the disposable server.", flush=True)
                desktop.dispatch({"action": "server_command", "command": "quit"})
            (STATE / "ready.json").unlink(missing_ok=True)
            if desktop.game and desktop.game.poll() is None:
                print("Closing the disposable client on bridge shutdown.", flush=True)
                try:
                    desktop.dispatch({"action": "close"})
                    desktop.game.wait(timeout=15)
                except Exception:
                    desktop.dispatch({"action": "terminate"})


def send(payload, timeout=30):
    ready_path = STATE / "ready.json"
    if not ready_path.exists():
        raise RuntimeError("Bridge is not running. Start `python3 scripts/desktop_control.py serve` in a desktop terminal.")
    ready = json.loads(ready_path.read_text())
    if time.time() - ready["heartbeat"] > 60:
        raise RuntimeError("Bridge heartbeat is stale")
    request_id = uuid.uuid4().hex
    request = dict(payload, session=ready["session"], created=time.time())
    atomic_json(STATE / "queue" / f"{request_id}.json", request)
    response_path = STATE / "responses" / f"{request_id}.json"
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if response_path.exists():
            return json.loads(response_path.read_text())
        time.sleep(0.1)
    (STATE / "queue" / f"{request_id}.json").unlink(missing_ok=True)
    raise TimeoutError(f"No reply for request {request_id}; inspect status before retrying input")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("serve")
    request = sub.add_parser("request")
    request.add_argument("json", help='e.g. \'{"action":"status"}\'')
    args = parser.parse_args()
    if args.command == "serve":
        serve()
    else:
        result = send(json.loads(args.json))
        print(json.dumps(result, indent=2))
        return 0 if result["ok"] else 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (RuntimeError, ValueError, OSError, subprocess.TimeoutExpired) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)

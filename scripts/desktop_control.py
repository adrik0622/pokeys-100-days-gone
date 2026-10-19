#!/usr/bin/env python3
"""A foreground project bridge for disposable PZ, Steam Workshop and local server tests.

Start `serve` in a normal desktop terminal; use `request` from Codex.
No network listener, shell commands, system services, or arbitrary application input.
"""

import argparse
import fcntl
import hashlib
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
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "runtime" / "desktop-control"
GAME = Path("/home/adrikingston/.local/share/Steam/steamapps/common/ProjectZomboid/projectzomboid")
KEYS = set("abcdefghijklmnopqrstuvwxyz0123456789") | {
    "Escape", "Return", "space", "Tab", "BackSpace", "Delete", "Home", "End",
    "Left", "Right", "Up", "Down", "Shift_L", "Control_L", "F1", "F2",
    "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12",
}
PRESENTATION = [("3619862853", "ZombieBuddy"), ("3809306528", "Viewpoint"),
                ("3810302175", "PZVoxelStudioViewpoint")]


def stage_upstream(cache, items):
    """Private local copies only; never overwrite user-owned mod directories."""
    workshop = GAME.parents[2] / "workshop" / "content" / "108600"
    for wid, name in items:
        source = workshop / wid / "mods" / name
        destination = cache / "mods" / name
        marker = ".pokeys-upstream-stage"
        if not source.is_dir() or any(p.is_symlink() for p in source.rglob("*")):
            raise RuntimeError(f"Missing or symlinked upstream source: {name}")
        if destination.exists() or destination.is_symlink():
            if destination.is_symlink() or not (destination / marker).is_file() or \
                    (destination / marker).read_text() != str(source):
                raise RuntimeError(f"Refusing to replace an unowned upstream stage: {name}")
            history = cache / "upstream-stage-history"
            history.mkdir(exist_ok=True)
            destination.rename(history / (name + "-" + uuid.uuid4().hex))
        prepared = cache / "upstream-stage-prepared" / (name + "-" + uuid.uuid4().hex)
        shutil.copytree(source, prepared)
        (prepared / marker).write_text(str(source))
        destination.parent.mkdir(parents=True, exist_ok=True)
        prepared.rename(destination)


def stage_presentation(cache):
    stage_upstream(cache, PRESENTATION)


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


def client_name(value):
    if value not in {"main", "a", "b"}:
        raise ValueError("Client must be main, a or b")
    return value


def stage_campaign(cache):
    source = ROOT / "mods/Pokeys100DaysGone"
    if not (source / "42/mod.info").is_file():
        raise FileNotFoundError(source)
    destination = cache / "mods/Pokeys100DaysGone"
    destination.parent.mkdir(parents=True, exist_ok=True)
    marker = ".pokeys-project-stage"
    if any(path.is_symlink() for path in source.rglob("*")):
        raise RuntimeError("Project mod source must not contain symlinks")
    if destination.is_symlink():
        if destination.resolve() != source.resolve():
            raise RuntimeError("Refusing to replace an existing campaign mod directory")
    elif destination.exists():
        if not (destination / marker).is_file() or (destination / marker).read_text() != str(source):
            raise RuntimeError("Refusing to replace an existing campaign mod directory")
    # Real directories avoid the engine backup walker treating a directory
    # symlink as an ordinary file. Preserve previous owned stages, not stale Lua.
    token = uuid.uuid4().hex
    prepared = cache / "campaign-stage-prepared" / token
    shutil.copytree(source, prepared)
    (prepared / marker).write_text(str(source))
    if destination.is_symlink():
        destination.unlink()  # Our own legacy link only; source remains intact.
    elif destination.exists():
        history = cache / "campaign-stage-history"
        history.mkdir(exist_ok=True)
        destination.rename(history / token)
    prepared.rename(destination)


def prepare_profile(profile, client="main"):
    client_name(client)
    if profile not in {"vanilla", "viewpoint", "campaign", "presentation", "migration", "encounter", "day100", "integrated"}:
        raise ValueError("Unknown isolated client profile")
    suffix = "" if client == "main" else f"-{client}"
    cache = ROOT / "runtime" / f"client-{profile}{suffix}"
    cache.mkdir(parents=True, exist_ok=True)
    # The full-screen user profile is deliberately not copied. This separate
    # cache contains only test settings and worlds, retained across restarts.
    options = cache / "options.ini"
    if not options.exists():
        options.write_text("\n".join([
            "version=8", "width=1600", "height=900", "fullScreen=false",
            "borderless=false", f"frameRate={60 if client == 'main' else 30}", "vsync=true", "language=EN",
            "tutorialDone=true", "showFirstTimeSneakTutorial=false",
            "showFirstTimeSearchTutorial=false", "soundVolume=2", "musicVolume=0", "",
        ]))
    mods = cache / "mods"
    mods.mkdir(exist_ok=True)
    mod_ids = []
    if profile in {"campaign", "presentation", "migration", "encounter", "day100", "integrated"}:
        stage_campaign(cache)
        mod_ids.append("Pokeys100DaysGone")
    if profile == "presentation":
        stage_presentation(cache)
        mod_ids = [name for _, name in PRESENTATION] + mod_ids
    if profile == "migration":
        stage_upstream(cache, [("3782615002", "HordeNights")])
        mod_ids = ["HordeNights"] + mod_ids
    if profile == "encounter":
        stage_upstream(cache, [("3268487204", "Bandits")])
        mod_ids = ["Bandits2"] + mod_ids
    if profile == "integrated":
        stage_upstream(cache, PRESENTATION + [("3268487204", "Bandits"), ("3782615002", "HordeNights")])
        mod_ids = [name for _, name in PRESENTATION] + ["Bandits2", "HordeNights"] + mod_ids
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
        self.server_profile = "vanilla"
        self.clients = {}
        self.client_profiles = {}

    def process(self, client="main"):
        client_name(client)
        return self.game if client == "main" else self.clients.get(client)

    def tracked_clients(self):
        return dict({"main": self.game} if self.game is not None else {}, **self.clients)

    def launch_server(self, profile="vanilla"):
        if profile not in {"vanilla", "dual", "campaign", "presentation", "migration", "encounter", "day100", "integrated"}:
            raise ValueError("Unknown isolated server profile")
        if getattr(self, "server", None) and self.server.poll() is None:
            raise RuntimeError("The disposable server is already running")
        install = ROOT / "runtime/server/install"
        cache = ROOT / "runtime/server" / profile
        name = f"pokeys-m0-{profile}"
        port = {"vanilla": 19860, "dual": 19870, "campaign": 19880, "presentation": 19890,
                "migration": 19850, "encounter": 19840, "day100": 19830, "integrated": 19820}[profile]
        config = cache / "Server" / f"{name}.ini"
        config.parent.mkdir(parents=True, exist_ok=True)
        if not config.exists():
            shutil.copy2(ROOT / f"config/server/{profile}.ini", config)
        sandbox = cache / "Server" / f"{name}_SandboxVars.lua"
        if profile in {"dual", "campaign", "presentation"} and not sandbox.exists():
            shutil.copy2(ROOT / "config/server/dual_SandboxVars.lua", sandbox)
        if profile == "migration" and not sandbox.exists():
            shutil.copy2(ROOT / "config/server/migration_SandboxVars.lua", sandbox)
        if profile == "encounter" and not sandbox.exists():
            shutil.copy2(ROOT / "config/server/encounter_SandboxVars.lua", sandbox)
        if profile == "day100" and not sandbox.exists():
            shutil.copy2(ROOT / "config/server/day100_SandboxVars.lua", sandbox)
        if profile == "integrated" and not sandbox.exists():
            shutil.copy2(ROOT / "config/server/integrated_SandboxVars.lua", sandbox)
        if profile in {"campaign", "presentation", "migration", "encounter", "day100", "integrated"}:
            stage_campaign(cache)
        if profile == "migration":
            stage_upstream(cache, [("3782615002", "HordeNights")])
        if profile == "encounter":
            stage_upstream(cache, [("3268487204", "Bandits")])
        if profile == "presentation":
            stage_presentation(cache)
        if profile == "integrated":
            stage_upstream(cache, PRESENTATION + [("3268487204", "Bandits"), ("3782615002", "HordeNights")])
        credentials = cache / "admin-password.txt"
        if not credentials.exists():
            credentials.write_text(secrets.token_urlsafe(24) + "\n")
            credentials.chmod(0o600)
        # Bind explicitly to loopback, with no UPnP or public listing. This
        # Profiles cannot alter the user's normal saves. Campaign adds only
        # our local Lua prototype; no upstream gameplay framework is enabled.
        args = [str(install / "jre64/bin/java"), "-Djava.awt.headless=true", "-Xms512m", "-Xmx4g",
                "-Dzomboid.steam=0", "-Dzomboid.znetlog=1", "-Djava.library.path=linux64/:.",
                "-Djava.security.egd=file:/dev/urandom", "-XX:+UseZGC", "-XX:-OmitStackTraceInFastThrow",
                "-cp", "java/.:java/projectzomboid.jar", "zombie.network.GameServer",
                f"-cachedir={cache}", "-servername", name, "-nosteam",
                "-ip", "127.0.0.1", "-port", str(port), "-udpport", str(port + 1),
                "-adminusername", "pokeysadmin", "-adminpassword", credentials.read_text().strip()]
        if profile in {"presentation", "integrated"}:
            args.insert(1, f"-javaagent:{GAME / 'ZombieBuddy.jar'}=policy=deny-new")
        env = os.environ.copy()
        env["LD_LIBRARY_PATH"] = ":".join(str(p) for p in
                                          [install / "linux64", install, install / "jre64/lib"])
        with (cache / "launcher.log").open("a") as output:
            self.server = subprocess.Popen(args, cwd=install, env=env, stdin=subprocess.PIPE,
                                           stdout=output, stderr=subprocess.STDOUT,
                                           text=True, start_new_session=True)
        self.server_profile = profile
        return {"pid": self.server.pid, "cache": str(cache), "profile": profile,
                "bind_ip": "127.0.0.1", "ports": [port, port + 1], "max_heap_gb": 4}

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

    def windows(self, client="main"):
        process = self.process(client)
        if process is None or process.poll() is not None:
            return []
        try:
            found = run("xdotool", "search", "--onlyvisible", "--pid", process.pid)
        except RuntimeError:
            return []
        windows = []
        for value in found.splitlines():
            name = run("xdotool", "getwindowname", value)
            if "project zomboid" in name.lower():
                windows.append({"id": int(value), "name": name})
        return windows

    def window(self, focus=False, scope="game", client="main"):
        if scope == "workshop":
            windows = [w for w in self.steam_windows() if w["id"] == self.workshop_window]
        elif scope == "game":
            windows = self.windows(client)
        else:
            raise ValueError("Scope must be game or workshop")
        if len(windows) != 1:
            raise RuntimeError(f"Expected one owned game window, found {len(windows)}")
        window = windows[0]["id"]
        if focus:
            self.release()
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
                "active_window": run("xdotool", "getactivewindow"),
                "clients": {name: {"pid": child.pid, "exit_code": child.poll(),
                                    "profile": self.profile if name == "main" else self.client_profiles.get(name),
                                    "windows": self.windows(name)}
                            for name, child in self.tracked_clients().items()}}

    def resources(self):
        memory = dict((line.split(":", 1)[0], int(line.split()[1]))
                      for line in Path("/proc/meminfo").read_text().splitlines())
        processes = {}
        children = self.tracked_clients()
        if getattr(self, "server", None):
            children["server"] = self.server
        for name, child in children.items():
            if child.poll() is not None:
                continue
            try:
                rollup = Path(f"/proc/{child.pid}/smaps_rollup").read_text()
                processes[name] = {"pid": child.pid, **{
                    field: int(re.search(rf"^{field}:\s+(\d+)", rollup, re.M).group(1))
                    for field in ["Rss", "Pss", "Swap"]}}
            except (OSError, AttributeError):
                processes[name] = {"pid": child.pid, "memory_unavailable": True}
        gpu = None
        if shutil.which("nvidia-smi"):
            gpu = run("nvidia-smi", "--query-gpu=name,memory.total,memory.used,utilization.gpu",
                      "--format=csv,noheader,nounits")
        return {"time": time.time(), "memory_unit": "KiB", "mem_available": memory["MemAvailable"],
                "mem_total": memory["MemTotal"], "processes": processes,
                "gpu_host_aggregate_name_totalMiB_usedMiB_utilPercent": gpu}

    def launch(self, profile, client="main"):
        client_name(client)
        live = {name: child for name, child in self.tracked_clients().items() if child.poll() is None}
        if client in live:
            raise RuntimeError("This client slot already has a game running")
        if live and (client == "main" or "main" in live):
            raise RuntimeError("The main single-client session cannot mix with explicit a/b sessions")
        # Permit only our two explicitly tracked children, never unrelated PZ.
        processes = run("ps", "-eo", "pid=,comm=").splitlines()
        owned = {child.pid for child in live.values()}
        if any(line.split()[-1].lower().startswith("projectzomboid") and
               (not line.split()[0].isdigit() or int(line.split()[0]) not in owned)
               for line in processes if line.split()):
            raise RuntimeError("An existing PZ client is running; close it before the test")
        if client != "main":
            memory = Path("/proc/meminfo").read_text()
            available = int(re.search(r"^MemAvailable:\s+(\d+)", memory, re.M).group(1))
            # Reserve headroom for tracked processes still booting; otherwise
            # two near-simultaneous launches could both pass on the same RAM.
            pending = list(live.values())
            if getattr(self, "server", None) and self.server.poll() is None:
                pending.append(self.server)
            reserve = 0
            for child in pending:
                try:
                    rollup = Path(f"/proc/{child.pid}/smaps_rollup").read_text()
                    pss = int(re.search(r"^Pss:\s+(\d+)", rollup, re.M).group(1))
                except (OSError, AttributeError):
                    pss = 0
                reserve += max(0, 6 * 1024 * 1024 - pss)
            if available - reserve < 6 * 1024 * 1024:
                raise RuntimeError("Less than 6 GiB available after tracked-process growth reserve; refusing another rendered client")
        cache = prepare_profile(profile, client)
        args = [str(GAME / "ProjectZomboid64")]
        vm_args = ["-Xms256m", "-Xmx3g"] if client != "main" else []
        if profile in {"viewpoint", "presentation", "integrated"}:
            # pzexe requires a -- separator between JVM and game arguments.
            vm_args.append(f"-javaagent:{GAME / 'ZombieBuddy.jar'}=policy=deny-new")
        if vm_args:
            args.extend(vm_args + ["--"])
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
            child = subprocess.Popen(args, cwd=GAME, env=env, stdout=logfile,
                                     stderr=subprocess.STDOUT, start_new_session=True)
        if client == "main":
            self.game, self.profile = child, profile
        else:
            self.clients[client] = child
            self.client_profiles[client] = profile
        return {"client": client, "pid": child.pid, "cache": str(cache), "args": args}

    def dispatch(self, request):
        action = request.get("action")
        scope = request.get("scope", "game")
        client = client_name(request.get("client", "main"))
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
        if action == "calibration_ocr_setup":
            # Existing host Tesseract lacks language data. Fetch DATA ONLY from
            # the official project, to ignored project runtime, not /usr/share.
            destination = ROOT / "runtime/tools/tessdata/eng.traineddata"
            if not destination.exists():
                with urlopen("https://raw.githubusercontent.com/tesseract-ocr/tessdata_fast/main/eng.traineddata", timeout=20) as response:
                    payload = response.read(8 * 1024 * 1024 + 1)
                if not 100000 < len(payload) <= 8 * 1024 * 1024:
                    raise RuntimeError("Unexpected OCR language-data size")
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(payload)
            digest = hashlib.sha256(destination.read_bytes()).hexdigest()
            if digest != "7d4322bd2a7749724879683fc3912cb542f19906c83bcc1a52132556427170b2":
                raise RuntimeError("OCR language-data drift; inspect official source before changing pin")
            return {"path": str(destination), "sha256": digest}
        if action == "resources":
            return self.resources()
        if action == "server_install":
            return self.install_server()
        if action == "server_install_status":
            installer = getattr(self, "installer", None)
            return {"pid": installer.pid if installer else None,
                    "exit_code": installer.poll() if installer else None}
        if action == "server_launch":
            return self.launch_server(request.get("profile", "vanilla"))
        if action in {"server_backup", "server_restore"}:
            server = getattr(self, "server", None)
            if not server or server.poll() is None:
                raise RuntimeError("Confirm the tracked disposable server has exited before backup/restore")
            if self.server_profile != "vanilla":
                raise ValueError("Snapshot helpers currently target the vanilla profile only")
            helpers = runpy.run_path(str(ROOT / "scripts/server_backup.py"))
            if action == "server_backup":
                return helpers["backup"](ROOT)
            return helpers["restore"](ROOT, request.get("snapshot"))
        if action == "server_status":
            server = getattr(self, "server", None)
            return {"pid": server.pid if server else None,
                    "profile": self.server_profile,
                    "exit_code": server.poll() if server else None,
                    "udp_listeners": [line for line in run("ss", "-H", "-l", "-u", "-n").splitlines()
                                      if re.search(r":198[23456789][01]\s", line)]}
        if action == "server_campaign_supplies":
            server = getattr(self, "server", None)
            targets = {"campaign": "pokeys_campaign_a", "migration": "pokeysadmin",
                       "integrated": "pokeys_integrated_a"}
            if self.server_profile not in targets or not server or server.poll() is not None:
                raise RuntimeError("Test supplies require the running isolated campaign server")
            command = "additem " + targets[self.server_profile] + " Base.Bandage 2"
            server.stdin.write(command + "\n")
            server.stdin.flush()
            return {"sent": command, "note": "Existing game admin command; fixture only, confirm inventory"}
        if action == "server_combat_supplies":
            server = getattr(self, "server", None)
            targets = {"presentation": "pokeys_presentation_a", "migration": "pokeysadmin"}
            if self.server_profile not in targets or not server or server.poll() is not None:
                raise RuntimeError("Combat supplies require the isolated presentation/migration fixture")
            username = targets[self.server_profile]
            commands = [f"additem {username} Base.Shotgun 1", f"additem {username} Base.ShotgunShells 20"]
            for command in commands:
                server.stdin.write(command + "\n")
            server.stdin.flush()
            return {"sent": commands, "note": "Fixed finite test gear, no release/world balance change"}
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
            return self.launch(request.get("profile", "vanilla"), client)
        if action == "stop":
            if any(child.poll() is None for child in self.tracked_clients().values()):
                raise RuntimeError("Close the disposable game before stopping the bridge")
            if getattr(self, "server", None) and self.server.poll() is None:
                raise RuntimeError("Quit the disposable server before stopping the bridge")
            self.stopping = True
            return {"stopping": True}
        if action == "terminate":
            # Explicit fallback, scoped to the child we launched. This is not a
            # clean-save test and is always reported as a forced termination.
            self.release()
            child = self.process(client)
            if not child or child.poll() is not None:
                return {"already_closed": True}
            child.terminate()
            try:
                child.wait(timeout=10)
            except subprocess.TimeoutExpired:
                child.kill()
                child.wait(timeout=5)
            return {"forced": True, "client": client, "exit_code": child.returncode}
        window = self.window(focus=action != "screenshot" or request.get("focus", False), scope=scope, client=client)
        if action == "resize":
            width = int(number(request.get("width"), 640, 3440))
            height = int(number(request.get("height"), 480, 1440))
            x = int(number(request.get("x", 50), 0, 3440 - width))
            y = int(number(request.get("y", 50), 0, 1440 - height))
            run("xdotool", "windowsize", window, width, height)
            run("xdotool", "windowmove", window, x, y)
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
        if action == "test_encounter_approach" and scope == "game":
            server = getattr(self, "server", None)
            profile = self.profile if client == "main" else self.client_profiles.get(client)
            if self.server_profile != "encounter" or profile != "encounter" or not server or server.poll() is not None:
                raise RuntimeError("Approach fixture requires the owned encounter client/server")
            # Type only this native admin command into an already-open game chat.
            # Verified in installed UI_ServerOptionDesc_TeleportTo; no shell/other target.
            run("xdotool", "type", "--clearmodifiers", "--delay", "30", "--",
                "/teleportto 8045,11756,0")
        elif action == "test_admin_password" and scope == "game":
            server = getattr(self, "server", None)
            if self.server_profile not in {"migration", "encounter"} or not server or server.poll() is not None:
                raise RuntimeError("Admin fixture requires the running isolated migration/encounter server")
            credential = ROOT / "runtime/server" / self.server_profile / "admin-password.txt"
            run("xdotool", "type", "--clearmodifiers", "--delay", "30", "--",
                credential.read_text().strip())
        elif action == "test_password" and scope == "game":
            suffix = "" if client == "main" else f"-{client}"
            credential = ROOT / "runtime/server" / self.server_profile / f"client-password{suffix}.txt"
            credential.parent.mkdir(parents=True, exist_ok=True)
            if not credential.exists():
                credential.write_text(secrets.token_hex(16) + "\n")
                credential.chmod(0o600)
            run("xdotool", "type", "--clearmodifiers", "--delay", "30", "--",
                credential.read_text().strip())
        elif action == "select_all":
            # Native PZ polls shortcut state; a zero-duration combo may be
            # missed at the reduced dual-client frame rate.
            try:
                self.pressed.add("Control_L")
                run("xdotool", "keydown", "Control_L")
                time.sleep(0.08)
                self.pressed.add("a")
                run("xdotool", "keydown", "a")
                time.sleep(0.12)
            finally:
                self.release()
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
        elif action == "aim_shot" and scope == "game":
            # One bounded shot at the current game camera direction. No cursor warp.
            try:
                run("xdotool", "mousedown", 3)
                time.sleep(0.6)
                if int(run("xdotool", "getactivewindow")) != window:
                    raise RuntimeError("Focus changed before shot")
                run("xdotool", "mousedown", 1)
                time.sleep(0.12)
            finally:
                try:
                    run("xdotool", "mouseup", 1)
                finally:
                    run("xdotool", "mouseup", 3)
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
            for name, child in desktop.tracked_clients().items():
                if child.poll() is None:
                    print(f"Closing disposable client {name} on bridge shutdown.", flush=True)
                    try:
                        desktop.dispatch({"action": "close", "client": name})
                        child.wait(timeout=15)
                    except Exception:
                        desktop.dispatch({"action": "terminate", "client": name})


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

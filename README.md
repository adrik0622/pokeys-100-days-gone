# Pokeys 100 Days Gone

A small private Project Zomboid survival multiplayer project. Original requirements: [PROJECT_BRIEF.txt](PROJECT_BRIEF.txt). Prior research and continuation notes: [HANDOFF.txt](HANDOFF.txt).

Planning target: **4–8 players**, with additional scale considered after measurement. No second human tester is available; two independently controlled local clients now work. Target capacity remains unverified.

Current build: native Linux 42.21.0, revision `4a0e9546ec`. Local vanilla recovery and autonomous two-client networking passed; further A/B runs are parked. Viewpoint dedicated join/first-person rendering now works, but shotgun `PlayerHitSquare` packet warnings block combat acceptance. No release stack or v1.0 is accepted.

Original companion source is **0.3.0 development**: shared faction standing/favors/aid; authored day-100 briefing; real-schedule observer bulletin; optional tuning (18.11-second real GUI success and clean-restart persistence); real debug-horde completion → supply disruption → favor-driven recovery. A one-shot admin Bandits encounter fixture is separate. Advance direction, strict global cap/offline safety, leader, complete combat and full integrated acceptance remain unfinished. Development collection remains hidden, with only the three presentation references; catalog candidates are not silently claimed as members.

- [Current status](docs/STATUS.md)
- [Progress toward v1.0](docs/PROGRESS.md)
- [User action items](docs/ACTION_ITEMS.md)
- [Versioned dependency manifest](config/modpack.json)
- [Development Workshop collection](docs/WORKSHOP.md)
- [Integration record and next three tasks](docs/INTEGRATION.md)
- [Local inventory](docs/M0-01-local-inventory.md)
- [Desktop controller and GUI smoke test](docs/M0-03-desktop-smoke.md)
- [Dedicated-server baseline and recovery test](docs/M0-02-dedicated-baseline.md)
- [Two autonomous clients, persistence and resource limits](docs/M0-04-multi-client.md)
- [First faction contact, shared standing and earned assistance](docs/M2-01-faction-contact.md)
- [Hostile physical scout and NPC reliability roadblock](docs/M2-02-physical-encounter.md)
- [Presentation dedicated test and combat roadblock](docs/M1-01-presentation.md)
- [Physical owner hooks and pinned technical gaps](docs/OWNER_SEAMS.md)
- [Migration / faction recovery engine evidence](docs/M3-01-migration.md)
- [Observer calibration and trust boundary](docs/M5-01-observer.md)
- [Development installation, day-100 candidate and packaging](docs/INSTALL.md)

The task sandbox cannot access X11 or the desktop bus directly. Start the scoped controller once in a normal desktop terminal:

```bash
python3 /home/adrikingston/Projects/pokeys-100-days-gone/scripts/desktop_control.py serve
```

The controller uses separate caches/saves in `runtime/`. It supports bounded input for its disposable game and explicitly attached Steam Workshop windows, plus fixed dedicated-server installation, lifecycle and offline recovery actions. Keep its terminal open; Ctrl+C stops it. See the smoke-test and dedicated-baseline documents for operations and evidence.

Automated controller checks:

```bash
python3 -m unittest discover -s tests -v
```

Validate and inspect candidate profiles (these commands do not deploy):

```bash
python3 scripts/modpack.py validate
python3 scripts/modpack.py check-installed
python3 scripts/modpack.py check-installed --full
python3 scripts/modpack.py profile --profile presentation-trial
```

All project-owned code, configuration, documentation and original assets use local Git revisioning. This task environment protects `.git`, so metadata lives in `.local-git/`. Use the wrapper from any directory:

```bash
bash scripts/git-local.sh status
bash scripts/git-local.sh log --oneline
bash scripts/git-local.sh diff
```

No remote is configured. Significant changes are recorded in the progress log and committed locally. Credentials, raw runtime files, saves and upstream dependency payloads remain ignored. Future agents should read `AGENTS.md` first.

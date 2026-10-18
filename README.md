# Pokeys 100 Days Gone

A small private Project Zomboid survival multiplayer project. Original requirements: [PROJECT_BRIEF.txt](PROJECT_BRIEF.txt). Prior research and continuation notes: [HANDOFF.txt](HANDOFF.txt).

Current milestone: establish a disposable local baseline on installed Build 42.21.0, revision `4a0e9546ec`. Autonomous GUI control passed with fresh vanilla and Viewpoint games, movement, door interaction and clean exits. Vanilla save reload also passed. Dedicated multiplayer and combat gates remain unrun; no release mod stack is accepted.

- [Current status](docs/STATUS.md)
- [Progress toward v1.0](docs/PROGRESS.md)
- [User action items](docs/ACTION_ITEMS.md)
- [Versioned dependency manifest](config/modpack.json)
- [Development Workshop collection](docs/WORKSHOP.md)
- [Local inventory](docs/M0-01-local-inventory.md)
- [Desktop controller and GUI smoke test](docs/M0-03-desktop-smoke.md)
- [Dedicated-server baseline and recovery test](docs/M0-02-dedicated-baseline.md)

The task sandbox cannot access X11 or the desktop bus directly. Start the scoped controller once in a normal desktop terminal:

```bash
python3 /home/adrikingston/Projects/pokeys-100-days-gone/scripts/desktop_control.py serve
```

The controller uses the installed game with separate caches and saves in `runtime/`. It supports bounded input for its own disposable game and explicitly attached Steam Workshop windows, plus a fixed anonymous dedicated-server installation action. Keep its terminal open; Ctrl+C stops it. See the smoke-test document for operations and acceptance evidence.

Automated controller checks:

```bash
python3 -m unittest discover -s tests -v
```

All project-owned code, configuration, documentation and original assets use local Git revisioning. This task environment protects `.git`, so metadata lives in `.local-git/`. Use the wrapper from any directory:

```bash
bash scripts/git-local.sh status
bash scripts/git-local.sh log --oneline
bash scripts/git-local.sh diff
```

No remote is configured. Significant changes are recorded in the progress log and committed locally. Credentials, raw runtime files, saves and upstream dependency payloads remain ignored. Future agents should read `AGENTS.md` first.

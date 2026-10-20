# Pokeys 100 Days Gone

A small private Project Zomboid survival multiplayer project. Original requirements: [PROJECT_BRIEF.txt](PROJECT_BRIEF.txt). Prior research and continuation notes: [HANDOFF.txt](HANDOFF.txt).

Approved [SC-002](docs/SCOPE_CHANGES.md): **v2.0 targets the living-world spirit**—recurring faction needs, meaningful choices, optional active play and consequential encounters. “It's show business” is one tool; choose the simplest effective engineering approach, including custom simulation when justified. [Living-world design and roadmap](docs/V2_LIVING_WORLD.md) · [Dated mod survey and airdrop source findings](docs/V2_MOD_SURVEY.md). These are plans/research, not newly enabled mods or a claim that v1.0 is complete.

Clarification [SC-003](docs/SCOPE_CHANGES.md): **consequence, not an anti-player-killing policy**, is the pillar. Every action should have causal effects players can feel, with faction-specific responses rather than universal PvP punishment. A-Life/Jeem isolated testing is authorized with Bandits disabled; retained profiles/worlds stay intact.

Clarification [SC-005](docs/SCOPE_CHANGES.md): design for a **positive player experience, readable warning cues and meaningful responses**. Danger, opportunity and social downtime should connect to the world; road traps must not instantly kill players. [Stretch idea bank](docs/STRETCH_IDEAS.md): faction road tolls, recoverable traps, foreshadowed ambushes and an optional casino. These have no release assigned and add no mandatory V1/V2 scope.

[A-Life 1.4.5 + Jeem 0.7.4 trial](docs/V2-01-alife-jeem.md) now has dedicated join, a visible/talking medic, one native gift with inventory/standing/opinion changes, and a narrow same-identity/item restart result with appearance/score caveats. Separate candidate worlds only, no release/Workshop promotion or player-kill consequence claim.

Approved [SC-001](docs/SCOPE_CHANGES.md): the full directing leader is now a **v1.1 target, not mandatory for v1.0**. A simpler existing Screamer-based threat is an optional bounded trial. The core forecast → horde → faction aftermath → recovery loop remains v1.0 scope; the original brief is preserved unchanged.

Planning target: **4–8 players**, with additional scale considered after measurement. No second human tester is available; two independently controlled local clients now work. Target capacity remains unverified.

Current build: native Linux 42.21.0, revision `4a0e9546ec`. Local vanilla recovery and autonomous two-client networking passed; further A/B runs are parked. Viewpoint dedicated join/first-person rendering works; shotgun packet warnings and the other reported issues are [pinned known bugs/limitations](docs/KNOWN_BUGS.md), not immediate stops to development play. Combat correctness and the combined campaign remain unaccepted; no release stack or v1.0 is accepted.

Original companion source is **0.4.1 development**: shared faction standing/favors/aid; authored day-100 briefing; real-schedule observer bulletin; optional tuning and real debug-horde completion → supply disruption → favor-driven recovery; and an opt-in V2 Mission-to-Jeem relay bridge with recovery/service readiness. An explicit combined development profile exists alongside isolated fixtures; full combat/horde-loop acceptance remains unfinished. Advance direction and strict global cap/offline safety are known limitations; leader is deferred to v1.1. Development collection remains hidden with only three presentation references; the local companion and trial candidates are not silently claimed as Workshop members. See the [comprehensive V2/V3 modpack report](docs/V2_V3_MODPACK_REPORT.md) and [human-review queue](docs/HUMAN_REVIEW.md).

- [Current status](docs/STATUS.md)
- [V2 event aftermath, player repair and restart evidence](docs/V2-04-recovery.md)
- [Original ask and approved scope changes](docs/SCOPE_CHANGES.md)
- [Combined campaign test](docs/M4-01-integrated.md)
- [Optional Screamer source audit and deferral](docs/M4-optional-screamer.md)
- [Known bugs, limitations and unfinished features](docs/KNOWN_BUGS.md)
- [Progress and significant decisions](docs/PROGRESS.md)
- [User action items](docs/ACTION_ITEMS.md)
- [Versioned dependency manifest](config/modpack.json)
- [Development Workshop collection](docs/WORKSHOP.md)
- [Integration record and next three tasks](docs/INTEGRATION.md)
- [Local inventory](docs/M0-01-local-inventory.md)
- [Desktop controller and GUI smoke test](docs/M0-03-desktop-smoke.md)
- [Dedicated-server baseline and recovery test](docs/M0-02-dedicated-baseline.md)
- [Two autonomous clients, persistence and resource limits](docs/M0-04-multi-client.md)
- [V2 separate-account completion, shared aid and restart](docs/V2-03-ownership.md)
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

All project-owned code, configuration, documentation and original assets use local Git revisioning. Metadata lives in `.local-git/` because earlier task sessions protected `.git`. From the project directory, use the wrapper:

```bash
bash scripts/git-local.sh status
bash scripts/git-local.sh log --oneline
bash scripts/git-local.sh diff
```

User-authorized remote `upstream` points to `git@github.com:adrik0622/pokeys-100-days-gone.git`; `main` tracks `upstream/main`. The initial history push and remote-commit verification succeeded on 2026-10-19 after shell networking was enabled. Use `bash scripts/git-local.sh push` to synchronize committed work. Significant changes are recorded in the progress log and committed locally. Credentials, raw runtime files, saves and upstream dependency payloads remain ignored. Future agents should read `AGENTS.md` first.

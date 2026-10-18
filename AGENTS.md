# Pokeys 100 Days Gone — continuation instructions

Read `README.md`, `docs/STATUS.md`, `docs/PROGRESS.md`, and `docs/ACTION_ITEMS.md` at the start of project work. Read `PROJECT_BRIEF.txt` for the full v1.0 requirements and `HANDOFF.txt` for the original research record. Follow these instructions in future chats as well as this one.

## Revisioning and evidence

- The user requires **local Git revisioning for every project-owned part**: companion code, configuration, dependency manifest, scripts, tests, documentation, and original assets. Do not add a remote, push, or publish the repository without a separate request.
- Use `bash scripts/git-local.sh ...` for Git operations. This environment overlays `.git` with an empty read-only mount; the actual local Git metadata is in ignored `.local-git/`. Do not treat a failed plain `git status` as proof that revisioning is unavailable.
- Make small meaningful commits as work progresses. Record significant decisions, implementations, test results, regressions, blockers, and acceptance milestones in `docs/PROGRESS.md`, with evidence and the next useful action. Include a progress entry in the corresponding commit.
- Keep `docs/STATUS.md` current and record user-dependent actions in `docs/ACTION_ITEMS.md`. Specify the exact action, why it is needed, what it blocks, and what can continue independently. Close resolved action items explicitly.
- Keep credentials, account cookies, passwords, saves, downloaded game/mod payloads, full raw logs, and temporary control state out of Git. Runtime material belongs in `runtime/`. Commit concise evidence summaries, hashes, and a few useful screenshots instead of bulk runtime data.
- Distinguish author documentation, source inspection, automated checks, and actual runtime observations. No Workshop tag, dependency manifest, or successful startup alone accepts a gameplay or multiplayer gate.

## Goal and workflow

- User-confirmed target: **4–8 players**, with scaling beyond that desirable only if measurements support it. This is a planning target, not verified capacity. **No second human tester is available.** Do not repeatedly request one or make that an immediate development blocker. Next multiplayer experiment is two isolated local client processes; feasibility is not yet tested. The controller's current single-client refusal is our safety guard, not a demonstrated game restriction. Separate local protocol tests from Steam authentication, cross-platform/remote networking, group capacity and eventual human playtesting.
- Deliver the bounded v1.0 in `PROJECT_BRIEF.txt`: reliable private dedicated multiplayer, Viewpoint and credible shooting, minimal faction presence and persistent consequential standing, forecasted recurring horde, a recognizable killable directing leader, one optional bounded interaction, and a repeatable recovery loop.
- Keep faction surplus/shortage trades as stretch scope. Defer continuous NPC simulation, recruitment/base workers, a full economy, map/render/firearm engines, and generic quest infrastructure.
- Prefer configuration, then supported integrations, then a small patch, then custom behavior for an evidenced gap. Use one owner for each firearm, NPC, and horde behavior. Complete a playable slice before adding breadth.
- Advance independent useful work when one path is blocked. Do not silently waive dependent test gates. Ask for user intervention only when a concrete action actually requires it; user authorization already given in this conversation remains valid.
- The user authorized creation and population of the Steam Workshop collection named **Pokeys 100 Days Gone**, and continued development. Keep it clearly labeled as development work and private/hidden while unvalidated. Reference upstream items; do not reupload their code/assets. Store the collection ID and its verified contents in the project manifest when created.
- A collection is a subscription/distribution convenience; explicit Workshop IDs, Mod IDs, settings and measured compatibility still define the server profile. Record version fingerprints because IDs do not freeze Workshop updates.

## Local execution

- Installed client: Build `42.21.0`, revision `4a0e9546ec`, native Linux, under `/home/adrikingston/.local/share/Steam/steamapps/common/ProjectZomboid/projectzomboid`.
- `python3 scripts/desktop_control.py request '{"action":"status"}'` checks the user-started host controller. It reloads source changes between requests. Its current game controls target its tracked disposable game; extend only within the user's authorized project work.
- Direct X11 and desktop D-Bus connections from the task sandbox fail with `EPERM`. A working host controller already exists; do not repeat platform discovery or ask the user to start another controller if it is still running.
- Tested profiles: `runtime/client-vanilla/` and `runtime/client-viewpoint/`. Main `~/Zomboid` settings and saves must remain intact. Game actions, screenshots, and raw logs are recorded under `runtime/`.
- See `docs/M0-03-desktop-smoke.md` for the verified launch arguments, input timing, cursor/camera distinction, clean exit procedure, and actual results. Twenty-seven automated checks pass. Single-player GUI and **one-client vanilla dedicated** join/restart/offline-restore passed; two-client, Steam-networking, modded dedicated, combat and capacity remain separate gates.
- Development Workshop collection `3822649790` is created, hidden, owned by PokeyFish, and contains only the three presentation dependencies. See `docs/WORKSHOP.md`; do not create a duplicate. Branding upload failed twice but does not block development. Use `scripts/modpack.py` to detect dependency drift and render explicit non-deploying profiles.
- The dedicated app is separately installed at `runtime/server/install/`, Build 42.21.0 / revision 4a0e9546ec / Steam build 25485538. Fixed server actions target only `runtime/server/vanilla/`, loopback 127.0.0.1:19860, with Public/UPnP disabled. `server_command` permits only save/players/quit. Backup/restore requires the tracked server to have exited; restore retains replaced state. Current client/server are stopped after testing; verify status before reuse.
- Use a plain isolated dedicated-server process for the first baseline; packaging on k3s comes later. GPU resources are for rendered clients unless evidence shows another need. Do not change host-wide services or an existing server.
- `isometricnomore` is subscribed but excluded from the trial because the original client log shows an initialization error. Do not include it or competing framework candidates merely because they are installed.

# Progress toward v1.0

This is the durable chronological record. Each significant change or decision receives a dated entry and a local Git commit. Detailed test cards remain in their milestone documents; raw runtime data remains ignored under `runtime/`.

## 2026-10-18 — Handoff and local inventory

- Imported the original brief and curated handoff. Established the v1.0 boundary and dependent gates without repeating the kickoff.
- Inspected the local native Linux client: 42.21.0 / `4a0e9546ec`, resolving the earlier reported 42.19 mismatch. Recorded hardware and enabled mods in `M0-01-local-inventory.md`.
- Corrected discovery limitations: task process visibility is sandbox-local; CRLF metadata caused an initial `isometricnomore` lookup miss. Identified it as Workshop 3819166046, version 0.1.17, and kept it out of the trial pending its logged initialization error.

## 2026-10-18 — Autonomous desktop smoke accepted (M0-03)

- Implemented a foreground host controller using the existing X11 session, `xdotool`, screenshots, and a project-local request queue. The user activated it in a desktop terminal because direct sandbox desktop access is denied.
- Created fresh vanilla and Viewpoint survival games; moved characters and opened doors with normal input, including Viewpoint's first-person `F` action.
- Verified three in-world exits with code 0 and no forced termination. Reloaded the vanilla save and observed the same character, location and door state. Viewpoint's saved coordinates corroborated character movement.
- Fixed missing bundled Java in child PATH, JVM/game argument separation for ZombieBuddy, frame timing for mouse/key input, and same-position mouse synchronization hangs. Added source reload between requests.
- Evidence: `M0-03-desktop-smoke.md`, selected screenshots, raw logs and action records under `runtime/`. Thirteen automated boundary checks passed. This accepts GUI automation only; dedicated multiplayer, combat and sustained performance remain unrun.

## 2026-10-18 — Local revisioning and continuation policy

- User explicitly requires local Git revisioning across all project-owned artifacts and documentation of every significant step toward v1.0.
- Added root `AGENTS.md`, this progress log, an action-item ledger, and a Git wrapper using `.local-git/`. This keeps usable local history despite the task environment's protected `.git` mount.
- Next: create and populate the development Workshop collection with the three GUI-trial dependencies; verify its actual ID and membership; establish an isolated dedicated-server baseline. Continue independent work if account authentication needs the user.

## 2026-10-18 — Hidden Workshop collection and dedicated installation

- Created **Pokeys 100 Days Gone**, Workshop `3822649790`, in PokeyFish's account. Owner view confirms Hidden. Populated the three presentation-trial dependencies in dependency-first order; kept the user's existing collection/subscriptions unchanged. Saved an explicit development/unvalidated description.
- Added scoped Steam-window controls and bounded Workshop text to the existing controller. Sixteen automated checks pass. No credentials/cookies were read. The legacy creation route redirected, so used the working Steam client collection tool instead.
- Original vector cover is versioned. Steam rejected the initial PNG upload; text-only save worked. Cosmetic retry is independent of server work.
- SteamCMD anonymous download/validation of dedicated app `380870` succeeded into isolated `runtime/server/install/` (7.21 GB installed). Dedicated Steam build `25485538`; core revision string `4a0e9546ec` matches the installed client's revision. Runtime version/startup/join still require verification.
- Next: isolated loopback-only vanilla server startup, then the smallest client join/restart/recovery check before adding presentation dependencies.

## 2026-10-18 — First dedicated client joined; reproducible profiles

- Dedicated runtime confirmed `42.21.0 4a0e9546ec`, then reached SERVER STARTED. Verified its actual UDP listener is `127.0.0.1:19860`; no public listing/UPnP or host service changes.
- Joined with the isolated vanilla client as `pokeys_trial_a` / Jo Jarvis. Moved and dropped the named ID card as a world-state marker. Server saved successfully and exited with code 0 after normal client disconnect.
- Added fixed server lifecycle commands and offline backup/restore with SHA256 checking and preservation of replaced state. Created an offline 1,206-file baseline snapshot. Restart/restore observation is still in progress; multiplayer acceptance is not claimed yet.
- Added explicit vanilla/presentation profiles and `scripts/modpack.py` for dependency-order validation, non-deploying INI generation, installed ID/version and JAR-drift checks. All three installed dependencies match. ZombieBuddy's version comes from its JAR manifest because its mod.info omits modversion.
- Twenty-five automated checks pass, including dependency/profile safety and backup corruption/path/roundtrip checks.

## 2026-10-18 — Local restart/rollback subtest accepted; gate preserved

- Same vanilla character and dropped ID-card marker survived a clean dedicated restart/reconnect. Then picked the card up, verified it in inventory after another reconnect, stopped the server, and restored the offline snapshot. Rejoining restored the card to the floor and removed it from inventory; saved living-player ID/location match the snapshot. Three dedicated starts/stops all exited cleanly; final client exit code 0, no listeners left running.
- Retained the pre-restore world/config/account database at `runtime/server/recovery/20261018-173447/`. Selected before/after screenshots are versioned. Full raw logs, databases and snapshots remain ignored.
- Added complete upstream payload/metadata fingerprints, including 35,887 model-pack files, and failure-on-drift checks. Twenty-seven automated checks pass. Added compact integration/source evidence and the next three dependent tasks.
- Full M0 is **not accepted**: a second independent client and Steam-enabled networking remain untested. Recorded A-002 for actual group size/platforms and a coordinated two-client test. No NPC/horde/firearm alternatives or custom gameplay were introduced across that gate.
- Workshop branding failed a second time with an 8-bit RGB PNG; description/membership remain intact. Cosmetic service/form troubleshooting is independent, with no demonstrated user-authentication action required.

## 2026-10-18 — Player target clarified; local multi-client path

- User confirmed **4–8 players**, with higher scale desirable if feasible, and reiterated that no second human tester is available. Updated continuation/status/action notes so future chats do not repeat that request.
- Inspected the existing controller: `launch()` deliberately rejects any existing PZ client. This is a project safety guard, not evidence of a game/Steam restriction. No simultaneous-client launch has been attempted.
- Next agent-owned experiment: separately track two local vanilla clients with isolated caches/accounts, bounded memory/render settings, and explicit per-window input. Verify resource use, both clients' shared observations, reconnect/restart and clean exits. Preserve rejection of unrelated user game processes.
- Keep limitations explicit: two local clients may exercise networking/state synchronization but cannot certify remote networking, Steam identities, friend platforms, human gameplay quality or 4–8-player capacity. This clarification did not launch games or change gameplay/server behavior.

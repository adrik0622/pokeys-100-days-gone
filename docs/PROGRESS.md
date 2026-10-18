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

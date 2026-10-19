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

## 2026-10-18 — Explicit dual-client controller and first simultaneous launch

- Implemented two named, PID-owned A/B client slots with separate caches/accounts, bounded heap/render settings, launch memory guard, and per-client input/cleanup. Kept unrelated-game refusal and legacy single-client isolation. Added fixed read-only resource sampling.
- Added a separate loopback-only `dual` vanilla server profile and fixed shared spawn, preserving the earlier vanilla world. Both native clients launched concurrently and authenticated against it; first character entered. Shared-state/restart/exit acceptance is in progress in `M0-04-multi-client.md`.
- Caught/fixed missed native Ctrl+A at reduced frame rate before using the malformed port. Thirty-four automated checks pass, including owned-vs-unowned PID handling, slot/cache isolation, low-memory launch refusal, server-profile boundaries and held-shortcut release.
- Resource samples show this experiment consumes substantial RAM beyond Java heap sizes. Monitor available RAM and aggregate GPU usage during world loading; no 4–8-player capacity or sustained-performance claim is made.

## 2026-10-18 — Two clients share movement and inventory state

- Both characters entered the same room. A-only `S` movement was visible from B without moving B; B's separately targeted movement was visible from A. Server `players` listed both distinct usernames.
- A dropped **ID Card: Alpha Baseline**. Both clients' Ground inventories showed the same named card. B took it; B's inventory then contained Alpha's card plus its own Bravo card, while A's Ground inventory became empty and A's carried weight stayed reduced. Selected screenshots are versioned under `docs/evidence/2026-10-18-dual/`.
- Closed A through Quit to Desktop / Yes, exit code 0. Server listed only B afterward; B stayed in the same room with both cards and no A character present. Relaunch/reconnect and the two-client server-restart check remain in progress.
- With both clients in world, a sample showed ~3.3 GiB RAM available, ~5.1–5.2 GiB PSS per client, ~5.2 GiB server PSS, zero process swap, and 10,127 MiB **host aggregate** GPU use. These short samples do not establish safe sustained margins or release capacity.

## 2026-10-18 — Idle-survival interference; safe network fixture

- A rejoined as the same living Alpha Baseline; server listed both clients and A's inventory remained without the transferred card. During the longer checks, zombies entered the house and killed both idle test characters. The saved player database confirms both dead. This spoils the intended living-character restart/persistence check; do not claim that step passed from the first run.
- Both clients and the first dual server exited with code 0. Preserve the entire first dual runtime under `runtime/server/recovery/20261018-1807-dual-zombie-incident/`, including logs, accounts, world and dead-character records. Nothing in the user's normal saves or the earlier vanilla rollback fixture is changed.
- Added an explicit zero-population/no-story sandbox fixture for a fresh dual world, using enum meanings from the installed server's generated settings. This isolates network state testing from idle combat; it is not release balancing or survival acceptance. Repeat the transfer/restart check on this fresh fixture.
- Strengthened named-client preflight to reserve future memory growth of already-running tracked clients/server, instead of counting unconsumed startup RAM twice. Thirty-five automated checks pass.

## 2026-10-18 — Autonomous local A/B networking subtest accepted

- Repeated shared movement and the Alpha-to-Bravo named-card transfer on a fresh, explicitly zombie-free network fixture. Both distinct characters remained alive. A returned normally to the menu while B stayed online with both cards; server confirmed only B. A rejoined without character creation, with the same outfit/key ring and no card; B retained both cards.
- Both disconnected; server confirmed zero players, saved and exited 0. Retained the full offline world/logs before restart. Restarted the same world, rejoined both clients, and verified the same identities/outfits/locations and transferred card ownership. Compared player ID/account/name/position/death-status fields were exactly unchanged and no extra player row appeared. This accepts the bounded marker test, not a general duplication/stat-loss guarantee.
- Final A and B Quit to Desktop / Yes both exited 0. Server confirmed zero players, then quit with 0 / `Shutdown handling finished`, leaving no test listener. No forced termination or human test operator was used. Final sample: no tracked live process, 19,706,448 KiB RAM available and 1,148 MiB host-aggregate GPU use.
- Evidence and limits are in `M0-04-multi-client.md`, including selected post-restart screenshots, raw/offline evidence locations and DB hashes. The successful fixture/server settings are versioned, while credentials/worlds/raw logs remain ignored. Updated README, status, action ledger, integration tasks and continuation instructions so future chats use the proven A/B path instead of asking for a second human.
- Repeated joins left as little as 2.86 GiB available RAM. Do not extrapolate 4–8-player capacity, FPS/TPS, long-run performance or modded memory cost. Next: one-client presentation-profile dedicated trial on another world, measuring headroom before a dual modded run. Steam/WAN/cross-platform/modded/combat acceptance gates remain open; no gameplay owner or release stack was added.
- Verification: 35 automated checks pass; dependency manifest validates and installed metadata/JAR fingerprints still match. Full-payload hashes were not recomputed in this step.

## 2026-10-18 — Park A/B testing; implement faction contact slice

- User explicitly asked to keep a pin in the two-client test and move on to scoped implementation. Preserve M0-04 evidence/open limitations; do not keep repeating that test as the next task.
- Added original Lua companion `Pokeys100DaysGone` 0.1.0: three provisional faction records, shared persistent standing, one repeatable two-bandage favor and an Allied-gated medical assistance action, both with group-wide world-time cooldowns. Client ledger is presentation only; server validates actor, distance, floor, alive state, actual inventory, standing, cooldown and admin role. No physical NPC, horde, forecast, weapon engine or upstream fork was introduced.
- Inspected installed engine persistence/network/inventory hooks and current Bandits/Kane author descriptions before choosing the narrow missing campaign behavior. Source/author evidence and limitations are recorded in `M2-01-faction-contact.md`; no unavailable upstream code inspection is claimed.
- Added pending-operation fail-closed handling, strict schema validation, isolated snapshots and focused Lua 5.1 rules/server-adapter checks. Engine inventory and campaign saves are not atomic; hard-crash recovery is explicitly unverified. Thirty-nine project tests pass, including fixed staging/test-gear boundaries.
- Added separate companion-only campaign client/server profiles on loopback 19880, retaining previous worlds, normal settings, collection and presentation profile. One-client engine check is next; full M1/M2 acceptance and A/B feature testing remain pending.

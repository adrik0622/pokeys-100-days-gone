# Minimal integration record

Observed 2026-10-18 on Linux Build 42.21.0 / `4a0e9546ec`. Versions and hashes are in `config/modpack.json`. References distribute original items, not copies. The three-item collection is a **candidate**, not the release or a passed dedicated-mod profile.

| Item / purpose | Version, dependencies and relevant configuration | Evidence and remaining seam |
| --- | --- | --- |
| [ZombieBuddy](https://steamcommunity.com/sharedfiles/filedetails/?id=3619862853): Java loader required by Viewpoint | 2.3.4 from JAR manifest; client launch agent uses existing `policy=deny-new` approvals. `42/mod.info`; `libs/ZombieBuddy.jar` | Local GUI trial passed. Installed source `JavaModInfo.java:135` skips `media/java/client/` JARs on a server; `patches/Patch_GameServer.java` calls initialization callbacks at server start. Source evidence, **not a modded dedicated test**. Do not weaken trust policy to hide an error. |
| [Project Viewpoint](https://steamcommunity.com/sharedfiles/filedetails/?id=3809306528): presentation and initial native shooting candidate | 0.1.6.1; requires ZombieBuddy >=2.3.0; pins 42.21. Metadata `common/mod.info`, JAR `42/media/java/client/Viewpoint.jar`; low onboarding settings used in GUI trial | First-person new game, movement, door interaction and clean exit passed. The JAR is client-scoped by the loader's path check. Dedicated mod handshake, reconnect, combat/collision/damage and client agreement remain unrun. No extra firearm owner yet. |
| [6244 3D models for Viewpoint](https://steamcommunity.com/sharedfiles/filedetails/?id=3810302175): presentation assets | Mod ID `PZVoxelStudioViewpoint`, 1.0; local metadata title says 6277 and directory `42.20.4`, but metadata pins **42.21.0**. Do not infer compatibility from folder/title alone | Enabled in GUI trial; individual model completeness unverified. Full payload fingerprint covers 35,887 files / 450,786,523 bytes. No NPC/horde behavior is provided or implied. |

Overlap owners: Viewpoint/native PZ shooting is the only current firearm candidate. NPC and horde owners are **unselected**. `isometricnomore` remains excluded pending its original initialization error. Bandits/Horde Nights/Hark are research leads in the handoff, not installed acceptance results.

## Reproducibility / update handling

`python3 scripts/modpack.py check-installed` compares IDs, versions, raw metadata hashes and JAR hashes. `--full` additionally hashes all upstream item files, including model assets. The payload digest is SHA256 of sorted records `<relative POSIX path>\0<file SHA256>\n`, encoded UTF-8, rooted at the Workshop item directory. Symlinks are refused. Hashes detect change; they do **not** freeze Workshop updates or authorize redistribution.

On drift: preserve relevant logs/fingerprints under ignored runtime, identify the upstream change, then repeat the affected test gate before updating committed expected hashes. Never simply regenerate expected hashes to silence a failed check. Known-good upstream payload retention/reversion is subject to the author's license and Steam distribution facilities; no public fork/reupload is planned.

## Next three executable tasks

1. Explore two local vanilla clients on this exact dedicated profile. Target is now 4–8 players; no second human tester is available. Extend the controller to separately tracked A/B processes with distinct caches/accounts, preserving rejection of unrelated clients. Begin with bounded resource use and verify launch/focus/clean exits before shared-state/reconnect/restart checks. This is untested; do not assume the controller's present one-client guard is a game limitation. Keep loopback binding; no public ports/router changes are implied. Local dual-client results will not establish Steam authentication, WAN/cross-platform behavior or 4–8-player capacity.
2. After M0, trial the explicit presentation profile on a **separate world**, confirm server-side dependency loading vs client-only rendering, then repeat join/reconnect. Do not enable a camera-rendering JAR on the server by moving it out of its client directory.
3. Only then perform M1's native firearm/obstruction tests with A acting and B observing. Human NPC damage is a later target-specific test after selecting one NPC owner. Do not select extra ballistic/NPC/horde frameworks to bypass an unpassed seam.

No custom gameplay code has been justified by the present evidence. Persistent standing, leader coordination and optional calibration remain requirements, not delivered features; inspect the chosen owners' hooks before implementing the smallest missing behavior.

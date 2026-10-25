# Development installation / recovery

This is a **0.4.2 development kit, neither V1 nor V2 accepted**. No friend-install, Steam-enabled join, target-specific combat or complete campaign acceptance is claimed. Original dependencies are supplied by Workshop references, not in our archive. Do not use test fixtures for a public/live survival world.

## Reproduce the known Linux project path

Verified installation: native Linux Build 42.21.0 / revision `4a0e9546ec`; client Steam build 25485521, dedicated app 380870 build 25485538. Manifest: `config/modpack.json`. Upstream Workshop IDs do not lock updates; run metadata/JAR checks, and `--full` before an acceptance run. Inspect drift before changing expected pins. Research source pins live separately in `config/research.json` and are not accepted collection members.

1. Read `STATUS.md` and `OWNER_SEAMS.md`. Check existing controller with `python3 scripts/desktop_control.py request '{"action":"status"}'`. Do not start another while it is alive. If needed, start `serve` in a normal desktop terminal; task sandbox has no direct X11 access.
2. Run `python3 -m unittest discover -s tests -v`, `python3 scripts/modpack.py validate`, `python3 scripts/modpack.py check-installed --full`. The game and dedicated install are existing local prerequisites; controller scripts intentionally use this host's inspected paths, not portable path guesses.
3. Choose exactly one isolated profile. `campaign`: companion only, port 19880. `presentation`: three presentation dependencies + companion, 19890; Java agent retains `policy=deny-new`. `migration`: Horde Nights + companion only, 19850; four-zombie experiment, no Viewpoint/NPC. `encounter`: Bandits2 + companion, 19840, one-shot admin scout. `day100`: companion-only survival calendar candidate, 19830. `integrated`: all five selected upstream inputs + companion, 19820; explicit opt-in combined DEVELOPMENT world, known issues apply, no leader/Screamer. Each uses its own `runtime/server/<profile>` and `runtime/client-<profile>-a` world/settings. Existing caches/configs are retained; source/config changes do not silently overwrite existing server settings. Compare before creating the next fresh fixture.
4. Launch server with `request '{"action":"server_launch","profile":"campaign"}'`; inspect its launcher log for SERVER STARTED and correct loopback listener. Launch a fresh `a` client with matching profile. Use Join → Favorites → Add Server, IP `127.0.0.1`, profile port; add distinct test account and connect. Use controller `test_password` only in the password field. Main user saves/settings are never copied or replaced.
5. After character creation / Click to Start, right-click → Pokeys faction contacts / observer bulletin. Contact relay is the known house at 7990 / 11756 / ground floor. See `M2-01-faction-contact.md` and `M5-01-observer.md` for exact actions and acceptance limits. Migration/encounter admin uses existing native debug controls; never give ordinary release players admin access. NPC test: observer bulletin → DEV one scout; request latches once per world. Preserve injured character and logs after the known Bandits handler defect. Fixed `test_encounter_approach` types only `/teleportto 8045,11756,0` into game chat; select all to replace its default `/say` prefix before submitting. This is an admin inspection shortcut, not normal gameplay acceptance.
6. Exit through Escape → Quit to Desktop → Yes. Confirm client exit 0, server `players` empty, then `server_command` `quit`, exit 0 / Shutdown handling finished / no listeners. Forced termination is not clean-save evidence.

## Selected V2 direction — isolated worlds, not a release profile

The older `integrated` profile above is the **retained Bandits-based foundation experiment**, not the selected A-Life V2 stack. Never add A-Life to it or co-enable NPC owners. These explicit V2 profiles retain separate saves/configs and do not change the Workshop collection:

| Profile | Loopback port | Purpose / owners |
| --- | --- | --- |
| `alife` / `alife-jeem` | 19810 / 19800 | Original native NPC/Jeem contact and identity trials; preserve Henry/Delbert, no extra blind spawn/gift |
| `supply-trial` | 19790 | Military Drop + Belt Radio + TooltipLib only; locally pinned availability/adoption question HR-011, no horde/NPC contest |
| `mission-trial` / `contract-trial` | 19780 / 19770 | Native gather UI versus original introductory contract, no NPC owner |
| `faction-contract-trial` / `faction-ownership-trial` | 19760 / 19750 | A-Life + Jeem + The Mission + companion, first single-account then separate-account ownership/restart evidence |
| `faction-recovery-trial` | 19740 | Horde Nights + A-Life + Jeem + The Mission + companion; one-birth debug experiment, all drops OFF, ordinary medical aftermath/recovery and optional calibration |

For V2 profiles use right-click → **Pokeys: living-world relay** for County EMS service/repair and **Pokeys: observer bulletin** for forecast/calibration. Native Mission owns the once-per-account first delivery: two Bandages at 7990/11756/0, within eight tiles, consume → one wipes; companion reconciles that native completion into one Jeem deed. Shared aid is one bottle per 48 world hours, only when eligibility/recovery allow it. The relay displays the server's reason before requesting.

`PokeysV2.Enabled` defaults OFF. New `PokeysV2.RepeatRelief` also defaults OFF and is opted in **only** by the recovery fixture: after the introduction, donate two clean/non-favorite/unequipped main-inventory Bandages during a verified event disruption, once per account/event, for up to 12 h repair and a modest Jeem deed, **no extra item**. Natural recovery remains available. Runtime/source boundaries: [V2-04](V2-04-recovery.md), [V2-05](V2-05-recurring-relief.md). These fixture costs/budgets are not release balance.

Existing cached `Server/*_SandboxVars.lua` is retained, not overwritten on launch. Compare it with the chosen source profile and update only the stopped, matching disposable fixture after an offline checkpoint; changing a default does not silently migrate existing worlds. New optional observer identity is only populated by a newly observed successful event, never inferred from a historical/aborted one. Unsupported/corrupt state refuses effects and is preserved.

Incident rule: **do not reset native Mission history, delete receipt/grant records, clear `pending`, regrant supplies blindly or retry an uncertain effect.** Preserve full offline state and inspect actual native inventory/Jeem standing/observer plus receipt phase/confirmed consumption. HR-010 tracks whether an operator reconciliation tool should exist; none does. The vanilla-only restore helper remains forbidden for these worlds. See the [completion checklist](V2_COMPLETION.md) before treating any trial as a finished V2 deployment.

## Day-100 candidate

`config/server/day100_SandboxVars.lua` is a separate **unaccepted survival candidate**, not an overlay to paste over a running save. Calendar starts October 17, 1993 (100 days after July 9), with native three-month erosion/spoilage because `TimeSinceApo` is month-granular. The observer bulletin supplies explicit authored prehistory; no 100-day NPC simulation or exact prior world-age clock is claimed. Horde is deliberately disabled until direction/offline/global-cap fixes pass. Small population values are proposed experiments, not tuned performance promises. Test October weather, loot, power/water, calendar and visible history on a new world before adopting it.

Headless day-100 startup passed on this host: engine reported `calendar=1993-10-17 worldAgeHours=2`, and reached SERVER STARTED with only the companion. This verifies calendar/startup, **not** prior simulation, food spoilage, utilities, weather survival, balance or a joined client in that world. `MaxPlayers=8` is a configured slot count, not measured capacity.

## Backups and update rollback

Stop and confirm the server has exited before copying world/config/accounts. Preserve the entire profile cache privately, including `Saves`, `Server`, `db`, local staged mods and their version fingerprints. Do not copy a live database as though it were a valid offline backup. Credentials and raw saves remain ignored and must not go into the development ZIP.

The automated SHA256 backup/restore helper is **vanilla-only**. Other profiles are explicitly refused; do not point it at a modded world by renaming paths. For these experimental profiles retain an offline complete cache before upgrades and restore to a different disposable cache after checking the corresponding dependency versions. Never delete the only original. Inventory and campaign ModData are not atomic under hard crash; a pending action remains locked for inspection, not blindly replayed/reset. Clean restart acceptance is narrower than crash recovery.

## Development artifact

After a clean local commit: `python3 scripts/package_dev.py`. Produces an exclusively created `runtime/dist/pokeys-development-<revision>.zip` with original tracked source/config/tests/Markdown and `PACKAGE.json` per-file hashes. No upstream payload, credentials, saves or `.local-git` metadata. Re-running for the same revision refuses overwrite. The archive is a review/installation kit, not a portable tested deployment or Workshop upload. Keep the full local repository for revision history. A remote host/k3s container, Steam auth/WAN, Windows/other friends' paths and final load order need separate validation.

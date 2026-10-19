# Optional Screamer trial — source audit, deferred

2026-10-18, following approved [SC-001](SCOPE_CHANGES.md). This is **installed-source + mocked-Lua evidence**, not engine/MP acceptance.

Subscribed/downloaded the original [Screamer Zed](https://steamcommunity.com/sharedfiles/filedetails/?id=3756523429) through the existing Steam UI. Actual Mod ID `ScreamerZed`, **1.1.12**, versionMin 42.0, no dependency declared. Subscription is retained for inspection; it was not enabled in normal settings, added to the collection, staged or launched in a game. Author asks not to copy code; no upstream source/assets copied into Git or modified.

Inspected all four Lua files (775 lines): server 512, client 87, appearance 123, config 53. Full payload: 29 files / 659,375 bytes; SHA256 `67d14827d3a31b25ef97566ce6eccf3e4768b8dd729207f7b57520deaf78c303`. Metadata/source pins are in `config/research.json`.

## Findings

- It has an actual server-only scheduler and a client Scream command/sound path; appearance attempts use shared helpers. These are useful mechanisms, not evidence of reliable shared rendering/audio on our build.
- The downloaded version **creates one new prepared Screamer** with `addZombiesInOutfit` after a population trigger 60–110 tiles from a player, with a 90-second birth interval and loaded-nearby limit. The scream itself draws existing zombies; the public description's no-new-zombies wording does not describe the entire current birth lifecycle.
- Killing during the reaction warning prevents the call. After a call, however, a local `activeAttraction` pulses `pathToSound` once per second for **180 seconds**, without checking the Screamer remains alive. Death therefore does not stop its already-active coordination requests.
- `pending` and `activeAttraction` are local tables, not persisted event state. Reloading the server handler loses the active rally while a zombie's `ScreamerZedScreamed` flag can remain. This is a source-level lifecycle discontinuity, not a measured engine restart/save result.
- Direct attraction applies to nearby loaded zombies without our event tags. Current Horde Nights also assigns targets/routes to its zombies. Their path/target interactions remain untested; enabling both is not a demonstrated integration.
- Runner conversion can be set to zero; that does not resolve birth accounting, event identity or death/restart behavior. No small public event-leader registration hook was found in these four files.

## Executed audit

`lua5.1 scripts/audit_screamer.lua /home/adrikingston/.local/share/Steam/steamapps/workshop/content/108600/3756523429/mods/ScreamerZed/42`

The original audit script loads actual installed upstream Lua read-only, supplying mocked engine lists, players, time, spawn and path boundaries. It observed one new prepared birth, death-before-call cancellation, a further path request after death, and loss of active pulses on handler reload while the used flag remains. Appearance, sound, actual pathfinding, network ownership and disk persistence are **not tested** by this harness. The script deliberately fails if those source observations change, requiring review rather than claiming a fix.

## Decision / rollback

**Defer this optional candidate** under SC-001's stopping rule. A general ambient Screamer could still be a valid mod on its own; these observations do not certify it as our death-controlled, event-bounded feature. Fixing that would mean additional lifecycle/accounting and ownership integration, beyond this optional low-cost trial. No fork, blanket overrides, author contact or second director. Continue core combined campaign work without leader/Screamer. Normal settings/worlds are unchanged; no runtime to stop or trial world to reset.

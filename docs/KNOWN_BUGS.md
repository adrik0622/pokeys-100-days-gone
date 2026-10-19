# Known bugs and development limitations

Updated 2026-10-18. Companion source **0.3.0 development**, native Linux Build 42.21.0 / `4a0e9546ec`.

User decision: **pin these issues; they are not immediate blockers to development play or independent feature work.** This is a priority decision, not evidence that the defects are fixed, all systems work together, or the original v1.0 acceptance requirements have been waived. Keep experiments isolated and preserve worlds/backups. Do not automatically enable candidate dependencies or change survival settings to hide a limitation.

IDs match the historical pins in [ACTION_ITEMS](ACTION_ITEMS.md). Missing features and unrun checks are separated below so they are not misreported as reproduced bugs. The Workshop description contains a concise player-facing summary; this file is the detailed local record.

## Reproduced bugs — pinned

| ID | Observation and player relevance | Current precaution / later diagnostic |
| --- | --- | --- |
| B-001 | Dedicated shotgun input produced two `PlayerHitSquare` inconsistency warnings with Viewpoint. First-person rendering, loading and firing input worked; actual damage/collision correctness is unverified. Cause is not assigned to Viewpoint or the native game. | Do not promise reliable zombie/NPC/player hits or add a competing firearm owner. Later compare the same weapon in a fresh native-only single-client fixture. [Evidence](M1-01-presentation.md) |
| B-002 | Bandits repeatedly raised `Expected a table` in `BanditServerCommands.lua:341`, at `pairs(args)`, during a real hostile encounter. The human visibly approached/attacked and injury indicators appeared; exact command, payload origin and synchronized damage remain unknown. Client path warnings also occurred. | Preserve the injured character, world and one-shot latch. Later log the malformed command/type without suppressing the handler; no blanket Lua wrapper or upstream reupload. [Evidence](M2-02-physical-encounter.md) |
| B-009 | Steam rejected two Workshop cover-image uploads. Description and three-item membership work. No authentication failure was established. | Cosmetic only; retry later without recreating the collection. [Record](WORKSHOP.md) |

## Source-inspected / engineering limitations — pinned

| ID | Limitation | What it means for current play |
| --- | --- | --- |
| B-003 | Horde Nights chooses direction at event start, not when scheduling the warning. | Arrival windows work; advance direction is explicitly unresolved, never guessed. |
| B-004 | Owner population accounting covers loaded zombies from the current event, excluding unloaded/prior-event survivors. | A finite birth budget per event is not a strict global survivor cap. Repeated-event accumulation/performance is unverified; four births was only an integration fixture. |
| B-005 | Saved target groups leaving can still permit births if another group keeps the server active. | `PauseEmpty=true` protects a wholly empty server only. The promised no-destructive-offline-base policy is not yet verified; no actual offline-base attack was observed. |
| B-007 | Inventory and campaign ModData are separate saves, not an atomic transaction. | Clean restart persistence passed. A pending-operation latch prevents blind repeated payouts after partial failure; hard-crash recovery is unverified. Never automatically clear/replay a pending reward. |
| B-008 | Rendered local clients consumed substantial native RAM beyond their Java heaps. Cause of additional rejoin growth is unassigned. | Prefer fresh, bounded client processes. Do not launch 4–8 rendered clients as a capacity proxy or infer a remote-player limit from these samples. |

Horde source evidence and smallest possible integration seams: [OWNER_SEAMS](OWNER_SEAMS.md). These limitations apply to candidate profiles; they are not claims that Bandits/Horde Nights are already Workshop collection members.

## Unfinished features — not bugs

- **B-006 / directing leader:** not implemented or verified. v1.0 still needs readable appearance/sound, one actual coordination effect, death stopping that effect, and safe identity/ownership/unload/restart behavior. A stat buff alone does not meet this requirement.
- Physical NPC release encounters and the full forecast → combat/leader → faction aftermath → recovery loop remain partially integrated. The current one-shot NPC and small forced horde are separate test fixtures, not normal recurring campaign content.

## Unrun acceptance — not reproduced failures

- Combined presentation/NPC/horde/companion campaign, separate target damage/obstruction, client-visible horde approach/combat, three accepted forced cycles and an ordinary scheduled trigger.
- Warning/active-event restart and ownership handoff, feature-modded shared observations, and engine movement/death interruption for calibration.
- Joined-client day-100 survival/loot/utilities/balance, repeated integrated sessions, friend installation/Steam/WAN/platform checks and a 60–90 minute intended-group playtest. Target **4–8 players**, capacity unverified; no second human tester is currently available.

These remain v1.0 completion/acceptance work, not requests to stop development play. Current progress and evidence are in [STATUS](STATUS.md); no immediate user credential, controller or second-tester action is needed.

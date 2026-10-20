# Known bugs and development limitations

Updated 2026-10-19. Companion source **0.4.1 development**, native Linux Build 42.21.0 / `4a0e9546ec`.

User decision: **pin these issues; they are not immediate blockers to development play or independent feature work.** This is not evidence that defects are fixed or all systems work together. A separate approved [SC-001](SCOPE_CHANGES.md) defers only the directing leader to v1.1; unrelated v1.0 requirements remain. Keep experiments isolated and preserve worlds/backups. Do not automatically enable candidate dependencies or change survival settings to hide a limitation.

IDs match the historical pins in [ACTION_ITEMS](ACTION_ITEMS.md). Missing features and unrun checks are separated below so they are not misreported as reproduced bugs. The Workshop description contains a concise player-facing summary; this file is the detailed local record.

## Reproduced bugs — pinned

| ID | Observation and player relevance | Current precaution / later diagnostic |
| --- | --- | --- |
| B-001 | Dedicated shotgun input produced two `PlayerHitSquare` inconsistency warnings with Viewpoint. First-person rendering, loading and firing input worked; actual damage/collision correctness is unverified. Cause is not assigned to Viewpoint or the native game. | Do not promise reliable zombie/NPC/player hits or add a competing firearm owner. Later compare the same weapon in a fresh native-only single-client fixture. [Evidence](M1-01-presentation.md) |
| B-002 | Bandits repeatedly raised `Expected a table` in `BanditServerCommands.lua:341`, at `pairs(args)`, during a real hostile encounter. The human visibly approached/attacked and injury indicators appeared; exact command, payload origin and synchronized damage remain unknown. Client path warnings also occurred. | Preserve the injured character, world and one-shot latch. Later log the malformed command/type without suppressing the handler; no blanket Lua wrapper or upstream reupload. [Evidence](M2-02-physical-encounter.md) |
| B-009 | Steam rejected two Workshop cover-image uploads. Description and three-item membership work. No authentication failure was established. | Cosmetic only; retry later without recreating the collection. [Record](WORKSHOP.md) |
| B-010 | Isolated A-Life admin console Advanced overlay covers its controls/toggle at 1600x900; reproduced core-only and with Jeem. Authoring UX, not a demonstrated ordinary-player progression failure. | Configure fields, close whole console, reopen to hide overlay while preserving spec. No upstream edit. Diagnostics temporarily on for setup, then off. [Trial](V2-01-alife-jeem.md). Candidate-only issue; these inputs are not collection members. |

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

- **B-006 / directing leader:** not implemented or verified; **deferred to v1.1 by approved [SC-001](SCOPE_CHANGES.md)**, not a mandatory v1.0 gap. Original requirements remain the v1.1 target. An optional simple Screamer must pass its own bounded trial; a stat buff is not fulfillment of the original ask.
- Physical NPC release encounters and the full forecast → combat/leader → faction aftermath → recovery loop remain partially integrated. The current one-shot NPC and small forced horde are separate test fixtures, not normal recurring campaign content.
- The V2 medical introduction is once per account, not a repeatable campaign job. Two ordinary accounts now repaired an actual debug-event disruption, with partial/full recovery and aid persistence across clean restarts ([V2-04](V2-04-recovery.md)). After introductions are exhausted, later disruption currently recovers by time rather than further relay deliveries. This is unfinished recurring content, not a duplicated-reward bug; do not reset native mission history to replay it.

## Unrun acceptance — not reproduced failures

The separate [A-Life/Jeem trial](V2-01-alife-jeem.md) now has contact/gift/identity-and-item restart evidence. Candidate follow-up V2-T1: outfit and position changed, initial position lock did not hold after restart; cause/expected behavior unassigned. Opinion +19 immediate versus +27 on return is consistent with the inspected deferred +8 gift bridge, not a proven reset/duplication bug. Preserve these observations; no exact visual/score-invariance or general persistence acceptance. NPC/player combat, witness policy, ordinary-player permissions and ownership handoff remain unrun.

- Full combined physical campaign/combat: separate target damage/obstruction, client-visible horde approach/combat, three accepted forced cycles and an ordinary scheduled trigger. Combined first-person join/favor/aid/calibration/clean restart now passed narrowly; [evidence](M4-01-integrated.md).
- Warning/active-event restart and ownership handoff, feature-modded shared observations, and engine movement/death interruption for calibration.
- Day-100 survival/loot/utilities/balance beyond the observed combined client join/UI slice, extended integrated sessions, friend installation/Steam/WAN/platform checks and a 60–90 minute intended-group playtest. Target **4–8 players**, capacity unverified; no second human tester is currently available.

Optional Screamer 1.1.12 is **deferred, not enabled** after a source/mocked-Lua audit of prepared births and death/reload lifecycle. This is a candidate mismatch for our optional integration, not an in-game bug report or new mandatory blocker. [Detailed audit](M4-optional-screamer.md).

The unrun core checks remain v1.0 completion/acceptance work, not requests to stop development play. Leader-specific assertions are deferred by SC-001. Current progress and evidence are in [STATUS](STATUS.md); no immediate user credential, controller or second-tester action is needed.

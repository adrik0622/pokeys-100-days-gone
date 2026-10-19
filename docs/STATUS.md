# Pokeys 100 Days Gone — development status

Source companion **0.3.0**, native Linux Build 42.21.0 / `4a0e9546ec`. **Not v1.0; no accepted release stack.** User target 4–8, capacity unverified. No second human tester; autonomous vanilla A/B passed and remains parked. **52 project checks pass.**

## Current stage: working prototypes, before the first integrated campaign

User priority update: the reported technical issues are **pinned known bugs/limitations, not immediate blockers to development play**. See [KNOWN_BUGS](KNOWN_BUGS.md). Do not make fixing every pin a prerequisite for independent feature progress. Existing v1.0 outcomes/acceptance remain in scope; a missing leader is unfinished work, not a bug fixed by documentation.

The local foundation works. Faction standing/assistance and optional calibration are the most developed gameplay pieces. Horde consequences/recovery are connected in a forced-event fixture. Physical encounters and presentation were demonstrated separately; no single combined campaign profile has been accepted. The largest missing feature is the directing leader. Day-100 balance, normal recurring encounters/cycles and release testing remain. A completion percentage would hide this integration uncertainty; source version 0.3.0 is not a percentage.

| Objective | Delivered / observed | Remaining v1.0 work / pinned issues |
| --- | --- | --- |
| A: presentation/shooting | Vanilla recovery and two-client local networking; Viewpoint dedicated join/first-person rendering; native gun equip/load/input | Shotgun PlayerHitSquare packet inconsistencies; zombie/NPC/player damage, obstruction, Steam/WAN, friend install and capacity |
| B: human presence | Three authored faction identities; ordinary favor → Allied → assistance and clean restart; one real armed Bandits scout approached/attacked test character | Repeating Bandits command-handler exception; neutral/friendly/hostile reliability, damage, ownership and release recurring encounter design |
| C: forecasted horde | Real owner schedule/bulletin; four actual births/routes per forced event; abort/debug completion; faction aftermath | Ahead-of-time direction absent; loaded/current-event cap not strict global cap; offline targets; client-visible approach/combat, natural trigger/restarts |
| D: directing leader | Actual tagging/path/death seams investigated; specific missing hooks recorded | No implemented/verified recognizable leader or coordination/death effect; do not substitute stat buff |
| E: optional active play | Screenshot/OCR 18.11 s calibration; window width 4 h → 0.5 h; duplicate protection and clean-restart precision | Ordinary-player adversarial engine cases, move/death interruption, feature A/B and human feel/tuning |
| F: recovery loop | Real debug-event completion → 24 h disruption → server-refused aid → bandage favor → 12 h recovery | Natural exploration/combat/leader cycles, three accepted forced cycles, ordinary trigger, integrated restarts/sessions/playtest |
| M6: release/deployment | Day-100 calendar/headless startup observed, spoilage candidate + authored history; seven explicit pinned profiles; original-only packager; installation/recovery guide | Day-100 joined-client survival/balance, friend/remote guide, final combined stack and full acceptance |

Evidence: [presentation](M1-01-presentation.md), [owner seams](OWNER_SEAMS.md), [migration/recovery](M3-01-migration.md), [calibration](M5-01-observer.md), [contact](M2-01-faction-contact.md), [parked A/B](M0-04-multi-client.md). Raw/offline worlds/logs remain ignored under `runtime/evidence/`; selected screenshots versioned. Main saves/install/live services untouched. Development collection 3822649790 remains hidden with only the three presentation references; candidate catalog membership is not Workshop membership.

At the last runtime handoff, client/server all stopped with exit 0, no test listeners; controller remains available. Do not silently reset/replay the NPC fixture: injured character, attempted latch and NPC world are retained.

Next feature priorities: design/implement the missing bounded leader through verified owner hooks; complete day-100 joined-client survival/balance; prepare an explicit opt-in experimental combined campaign, preserving separate fixture worlds and documenting known risks. These are future tasks, not new runtime claims. Retain the narrow gun/NPC/horde diagnostic plans as pinned follow-ups rather than automatically restarting them. Final integrated cycles, persistence and release checks still apply. No immediate user credentials or second tester required. See [action ledger](ACTION_ITEMS.md) and [integration plan](INTEGRATION.md).

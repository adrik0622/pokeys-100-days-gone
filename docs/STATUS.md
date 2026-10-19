# Pokeys 100 Days Gone — development status

Source companion **0.3.0**, native Linux Build 42.21.0 / `4a0e9546ec`. **Not v1.0; no accepted release stack.** User target 4–8, capacity unverified. No second human tester; autonomous vanilla A/B passed and remains parked. **52 project checks pass.**

| Objective | Delivered / observed | Still blocks v1.0 |
| --- | --- | --- |
| A: presentation/shooting | Vanilla recovery and two-client local networking; Viewpoint dedicated join/first-person rendering; native gun equip/load/input | Shotgun PlayerHitSquare packet inconsistencies; zombie/NPC/player damage, obstruction, Steam/WAN, friend install and capacity |
| B: human presence | Three authored faction identities; ordinary favor → Allied → assistance and clean restart; one real armed Bandits scout approached/attacked test character | Repeating Bandits command-handler exception; neutral/friendly/hostile reliability, damage, ownership and release recurring encounter design |
| C: forecasted horde | Real owner schedule/bulletin; four actual births/routes per forced event; abort/debug completion; faction aftermath | Ahead-of-time direction absent; loaded/current-event cap not strict global cap; offline targets; client-visible approach/combat, natural trigger/restarts |
| D: directing leader | Actual tagging/path/death seams investigated; specific missing hooks recorded | No implemented/verified recognizable leader or coordination/death effect; do not substitute stat buff |
| E: optional active play | Screenshot/OCR 18.11 s calibration; window width 4 h → 0.5 h; duplicate protection and clean-restart precision | Ordinary-player adversarial engine cases, move/death interruption, feature A/B and human feel/tuning |
| F: recovery loop | Real debug-event completion → 24 h disruption → server-refused aid → bandage favor → 12 h recovery | Natural exploration/combat/leader cycles, three accepted forced cycles, ordinary trigger, integrated restarts/sessions/playtest |
| M6: release/deployment | Day-100 calendar/headless startup observed, spoilage candidate + authored history; seven explicit pinned profiles; original-only packager; installation/recovery guide | Day-100 joined-client survival/balance, friend/remote guide, final combined stack and full acceptance |

Evidence: [presentation](M1-01-presentation.md), [owner seams](OWNER_SEAMS.md), [migration/recovery](M3-01-migration.md), [calibration](M5-01-observer.md), [contact](M2-01-faction-contact.md), [parked A/B](M0-04-multi-client.md). Raw/offline worlds/logs remain ignored under `runtime/evidence/`; selected screenshots versioned. Main saves/install/live services untouched. Development collection 3822649790 remains hidden with only the three presentation references; candidate catalog membership is not Workshop membership.

Current client/server all stopped with exit 0, no test listeners; controller remains available. Do not silently reset/replay the NPC fixture: injured character, attempted latch and NPC world are retained.

Next bounded agent tasks: isolate native-vs-Viewpoint hit-square packets; instrument the failing Bandits command name/argument type without masking its error; design one small owner add-on for direction preselection, conservative cross-event budget/offline targets, then verified leader control. Independent packaging/briefing/guide work can continue. No immediate user credentials or second tester required. See [roadblocks/action ledger](ACTION_ITEMS.md).

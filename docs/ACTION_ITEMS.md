# User actions and pinned roadblocks

No immediate credential/MFA, controller restart or second-human-test action is required. User pinned the reported issues as known bugs/limitations, **not immediate blockers to development play or independent v1.0 feature work**, and separately approved [SC-001](SCOPE_CHANGES.md), deferring the leader to v1.1. Detailed classification is in [KNOWN_BUGS](KNOWN_BUGS.md). Neither decision certifies the combined campaign or waives unrelated v1.0 acceptance. Do not contact authors, publish/upload a mod/fork, add a remote or change host services without separate authorization.

| ID | State | User action / why |
| --- | --- | --- |
| A-001 | Resolved | Existing foreground host controller works; sandbox X11 restriction is bypassed through it. Do not repeat setup while alive |
| A-002 | Resolved for local baseline | 4–8 target confirmed; no second tester available. Autonomous vanilla A/B movement/transfer/reconnect/restart passed and is parked. Capacity/remote/platform gates remain distinct |
| A-003 | Deferred, nonblocking | When friends are available, record their platforms and perform real install/Steam/WAN/group playtest. Do not repeatedly request this during local development |

## Technical pins — deferred follow-ups, not a stop-work queue

The next narrow actions below are retained for later diagnosis, not the automatic next sweep. B-006 is deferred to v1.1 by approved [SC-001](SCOPE_CHANGES.md); B-008 includes unrun capacity checks, not a proven remote-player limit.

| ID | Roadblock and evidence | Next narrow action | Independent progress |
| --- | --- | --- | --- |
| B-001 | Viewpoint dedicated shotgun PlayerHitSquare inconsistencies, M1-01 raw logs | Same native-only single-client weapon comparison; trace exact packet construction/validation. Do not mask with more firearm mods | Campaign/calibration/recovery, NPC-only fixture, packaging/day-100 |
| B-002 | Bandits repeating Expected a table at BanditServerCommands.lua:341 during real close hostile encounter; M2-02 | Log exact command/args type observationally; inspect sender. Supported add-on or author fix/explicitly permissioned patch after diagnosis | Horde-only observer/recovery, survival candidate, install artifacts |
| B-003 | Horde direction selected only inside start, not forecast | Establish supported preselection hook; never broadcast a guessed direction | Time-window calibration and authored briefing already work |
| B-004 | Current-event loaded-only cap; prior/unloaded survivors unaccounted | Persistent conservative birth/death budget + split-group/unload tests, fail safe on ambiguity | Existing finite-budget experiments, packaging; no capacity claim |
| B-005 | Last target group leaving can still allow births while another group keeps world active | No-more-births/abort policy at owner boundary; preserve ordinary survivors, verify offline settlement policy | Other source work and empty-server PauseEmpty behavior |
| B-006 | Deferred v1.1: no verified recognizable leader/coordination lifecycle (SC-001) | Optional bounded Screamer trial only; full feature later. No mandatory v1.0 leader assertion | Core campaign integration, survival balance, recurring loop and release work |
| B-007 | Inventory and ModData not atomic under hard crash; pending latch is conservative, not crash certification | Preserve incidents, inspect actual saves; never auto-reset/replay item payout | Clean restarts and focused duplicate/partial-failure tests already pass |
| B-008 | High native client RAM and unknown friend/group conditions | Fresh client processes, bounded samples; no 4–8 rendered local clients or invented safe caps | Source/solo fixtures and artifact preparation |
| B-009 | Workshop branding upload failed twice; collection membership/text works | Cosmetic retry only after gameplay risk work; no new authentication blocker | Hidden collection and explicit referenced profiles already exist |

Review: inspect the known-bugs record and objective matrix in STATUS. No user scope waiver is assumed. Faction names/prehistory and proposed survival balance are reviewable creative candidates, not requirements to answer before feature work continues. If upstream collaboration or redistributing a modified dependency becomes necessary, prepare the minimal evidence/report and ask for that specific authorization; nothing has been sent/reuploaded.

# User actions and pinned roadblocks

No immediate credential/MFA, controller restart or second-human-test action is required. User pinned the reported issues as known bugs/limitations, **not immediate blockers to development play or independent v1.0 feature work**, and separately approved [SC-001](SCOPE_CHANGES.md), deferring the leader to v1.1. Detailed classification is in [KNOWN_BUGS](KNOWN_BUGS.md). Neither decision certifies the combined campaign or waives unrelated v1.0 acceptance. Do not contact authors, publish/upload a mod/fork, add a remote or change host services without separate authorization.

| ID | State | User action / why |
| --- | --- | --- |
| A-001 | Resolved | Existing foreground host controller works; sandbox X11 restriction is bypassed through it. Do not repeat setup while alive |
| A-002 | Resolved for local baseline | 4–8 target confirmed; no second tester available. Autonomous vanilla A/B movement/transfer/reconnect/restart passed and is parked. Capacity/remote/platform gates remain distinct |
| A-003 | Deferred, nonblocking | When friends are available, record their platforms and perform real install/Steam/WAN/group playtest. Do not repeatedly request this during local development |
| A-004 | v2 policy review, nonblocking | Before any PvP-enabled deployment, choose cooperative PvE vs consensual/open PvP and how self-defense/duels/accidents are classified. Current PVP=false remains. Blocks live PK consequence acceptance, not source survey, PvE contracts or mocked justice-rule tests |
| A-005 | v2 policy review, nonblocking | Review proposed personal responsibility across character death versus shared faction access; identify whether Road Reclaimers should become the gray faction. Blocks final migration/balance/lore decisions, not isolated prototypes. Existing schema-1 group ledger and hostile scout stay intact |

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

## v2 investigation pins — not reproduced bugs or deployment promises

[SC-002](SCOPE_CHANGES.md) approves expanded direction and appropriate custom engineering, not every candidate. See [concept/next tasks](V2_LIVING_WORLD.md) and [dated survey](V2_MOD_SURVEY.md).

| ID | Uncertainty / action | What can continue |
| --- | --- | --- |
| V2-R1 | Inspect exact A-Life/Jeem, Military Drop, The Mission and Random Zeds payload/hooks/licenses before selection; pin actual versions, resolve dependency discrepancies | Authoring our faction needs/choice outcomes; existing baseline work |
| V2-R2 | Prove server-trustworthy NPC/player violence attribution, faction mapping, self-defense and duplicate handling before imposing affinity effects | Pure rules/anti-farm tests and PvE supply jobs; keep PvP off |
| V2-R3 | Inspect drop claimant/delivery evidence, guard dispatch/handoff, created-crate lifetime and shared zombie budget; current empty/ack flags are insufficient | Isolated source work and one low-count owner trial; no runtime bug claim from inspection |
| V2-R4 | No verified released Save Our Station B42 port; do not install its B41 map into retained worlds | Original bounded relay-health/repair at existing locations if needed; no copied assets |
| V2-R5 | Exact-stack/Linux/Viewpoint/ownership/dependency drift and capacity remain unverified for new candidates | Fresh bounded isolated tests, no automatic collection promotion, no 4–8 rendered local clients |

No new immediate user action is required. First implementation should follow capability/owner decisions, not turn all survey rows on together. Larger NPC/entity rewrites remain eligible after a bounded cost/risk design review.

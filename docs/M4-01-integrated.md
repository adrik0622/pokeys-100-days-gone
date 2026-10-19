# M4-01 — combined campaign development trial

## Setup / boundary

Approved SC-001 removes the mandatory directing leader. Explicit opt-in `integrated` profile combines the three presentation inputs, Bandits2, Horde Nights and original companion 0.3.0 in that order. No Screamer, second director/NPC/firearm owner, upstream fork or Workshop membership change. Known gun/NPC/director issues remain disclosed; this is not a release profile.

Separate cache/world/account on 127.0.0.1:19820/19821, Public/UPnP off, Lua checksums on, Java agent deny-new. Two configured slots are a smoke-test setting, not revised player target or measured capacity. Day-100 calendar candidate and month-granular spoilage, low 0.05 ambient population, native minimum 0.25 Bandits spawn multiplier, finite four-birth horde experiment / zero escalation / no sprinters or drops. This does not establish a cross-event global cap or offline-target safety. Earlier day100/migration/presentation/encounter worlds are untouched.

## First test card

Owner: agent. Prerequisites: 55 automated checks, explicit manifest/profile validation and unchanged full five-item payload hashes. Stage original marked real copies; preserve prior stages and normal saves/settings. Record source revision before starting.

1. Start the dedicated integrated profile; confirm exact game revision, combined mod loads, day-100 calendar, SERVER STARTED and loopback-only listener. Capture first relevant errors, not startup alone as acceptance.
2. Launch one fresh named A client using matching `integrated` cache; join as ordinary `pokeys_integrated_a`. Complete Viewpoint onboarding and character creation. Observe native first-person world and normal input.
3. Open companion contacts/observer. Check three identities/history and a real owner forecast. Supply exactly two fixture bandages only to this fixed account if needed; earn standing and verify aid in this combined configuration. Optional calibration can follow if stable.
4. Close normally; confirm client exit 0, zero server players, save/quit, server exit 0 and no listener. Preserve full offline world/logs. Clean restart/rejoin may follow separately; never infer it from independent older fixtures.

Smallest first run ~10–15 minutes, longer if new integration faults require diagnosis. No forced NPC/horde combat or firearm correctness claim from a join/UI smoke. A/B baseline remains parked. Rollback is stopping this disposable profile; preserve evidence, do not delete or relabel older worlds. Integrated session outcome is recorded below after observation.

## Observed 2026-10-18 — first combined join/UI + clean restart passed narrowly

Runtime source/controller revision `8ec36e5`; companion remains 0.3.0. First server PID 217364 / client A 217524; restart server 223302 / fresh client 223565. Native Linux 42.21.0 / `4a0e9546ec`, Steam disabled, loopback only. All five full upstream payload pins matched before starting.

- Both server starts reached SERVER STARTED with the explicit combined Mods list. Actual calendar was `1993-10-17 worldAgeHours=2` initially and `4.205877304077148` on restart; this is not 100 simulated days. Companion schema 1/revision 0 initially, **revision 4 loaded from disk** on restart. Bandits custom clans loaded; no physical NPC/horde was forced in this run.
- Ordinary `pokeys_integrated_a` created **Avery Integrated**, entered the relay house and completed Viewpoint Low / Vanilla-shader onboarding. Observed first-person room/body and bounded W movement, then native context menus and companion panels. `O` toggles first person; middle mouse releases the camera/cursor for UI. A locked-cursor absolute click can turn the view rather than click a panel. Acknowledged Bandits' volume warning without changing host volume.
- Delivered two fixed fixture bandages through the existing favor: Mutual Aid Neutral (0) → **Allied (+20)**, revision 2. Assistance produced one **Rubbing Alcohol (Bottle)**, revision 4, with group cooldowns and no returned bandages. UI screenshot shows the actual item and Avery's ID card; no universal duplicate/persistence guarantee inferred.
- Observer displayed all five authored history messages and real Horde Nights baseline arrival **88.41–92.41 world hours** at refresh, honestly unresolved direction. Screenshot/OCR-only calibration passed in **18.83 real seconds**, with displayed channels 1/1/2; window became **89.87–90.37** (width 0.5 h). Time-to-arrival changes between samples naturally.
- Quit to Desktop / Yes exited the first client 0. Server confirmed zero players, saved/quit with exit 0 / Shutdown handling finished / no listeners. Retained the complete offline Saves/Server/db before restart, plus first-session logs.
- Fresh server and client rejoined the same living Avery **without character creation or repeat Viewpoint onboarding**. Actual inventory retained Avery's ID and one Rubbing Alcohol (Bottle), no bandages; standing remained Allied with revision 4 and remaining cooldowns. Observer showed **89.12–89.62 world hours (calibrated)**. This is clean restart persistence in the combined stack, not an active-event restart or hard-crash test.
- Second client exited normally 0; server confirmed zero players, saved/quit and exited 0 with Shutdown handling finished / no listeners. Offline Saves/Server/db retained after restart as well. Read-only SQLite comparison found exactly one identical living player record before/after: ID 1, `pokeys_integrated_a`, Avery Integrated, `(7991.1259765625,11756.19140625,0)`, isDead 0. No broader inventory/duplication guarantee inferred from that identity check.

Resource sample during first combined GUI task: client A 6,290,304 KiB PSS, server 5,664,809 KiB PSS, available RAM 7,953,084 KiB, zero process swap, host-aggregate GPU 6,294 / 12,288 MiB. Short samples, not a sustained budget or 4–8-player capacity proof. No second rendered client launched.

Selected screenshots: `docs/evidence/2026-10-18-integrated/`. Raw first/restart logs and offline before/after worlds: `runtime/evidence/integrated/`. Startup logged missing optional animation directories, sound/world/script warnings; these are retained, not suppressed or called a clean error-free log. No PlayerHitSquare/Bandits close-encounter regression claim: no shot or physical NPC combat occurred. Calibration movement/death interruption, integrated physical combat/approach/aftermath, three fought forced cycles, ordinary trigger, mid-warning/active-event restarts, feature A/B, long sessions, Steam/WAN and intended-group capacity remain unrun.

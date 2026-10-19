# Pokeys 100 Days Gone — status

| ID | Status | Next evidence |
| --- | --- | --- |
| M0-01 Local inventory | Inspected; host-process visibility incomplete | Recorded in `docs/M0-01-local-inventory.md`; sandbox process view is restricted |
| M0-03 Desktop automation | Accepted on 2026-10-18 | Fresh vanilla and Viewpoint games, movement, door interaction, clean exits and vanilla save reload; explicit A/B control, scoped Steam/server work; 35 project checks pass |
| Workshop distribution | Created, hidden development | Collection `3822649790` contains the three presentation dependencies; no release stack accepted |
| M0-02 Dedicated baseline | Local vanilla subtests accepted; full gate open | One-client restart/rollback and two-client shared movement, cross-player transfer, reconnect, restart and clean stops passed. Steam/modded/remote gates remain open |
| M0-04 Autonomous dual clients | Local non-Steam subtest accepted | Two isolated caches/accounts; safe network fixture; living identities and transferred card persisted across restart. See resource limits in the test record |
| M1 Viewpoint and shooting | Dedicated integration next; acceptance pending M0 dependencies | Trial one modded client/server first, measure headroom, then A/B observations if safe; keep `isometricnomore` excluded |
| M2 Human encounters | Blocked by M1 | Select and test one NPC framework |
| M3 Horde event | Blocked by M2 | Select and test one horde owner |
| M4 First integrated slice | Blocked by M1–M3 | Shared event, leader effect/death, persistence |

No release mod stack has been accepted. The dedicated subtests were **vanilla, loopback, non-Steam**, with one-client recovery and two-client shared-state/restart observations. The latter used a zombie-free network fixture after zombies spoiled the first idle run; that world is preserved. The three presentation dependencies remain a separately GUI-tested candidate. Steam networking, modded dedicated behavior, combat, sustained performance and capacity are untested. Current clients/server are stopped with exit 0 and no test listeners; controller remains available.

User-confirmed planning target: **4–8 players**, with higher scale desirable only if measured. No second human tester is available or required for the proven local A/B harness. Two clients plus server left as little as 2.86 GiB available RAM and used up to 10,127 MiB host-aggregate GPU memory in spot samples. Do not infer remote-player capacity or launch more local rendered clients. Next: one-client presentation-profile dedicated trial on a separate world, then reassess resources for two modded clients. Friend OSes remain unknown but do not block this integration work. See `M0-04-multi-client.md`, `INTEGRATION.md`, and `ACTION_ITEMS.md`.

# Pokeys 100 Days Gone — status

| ID | Status | Next evidence |
| --- | --- | --- |
| M0-01 Local inventory | Inspected; host-process visibility incomplete | Recorded in `docs/M0-01-local-inventory.md`; sandbox process view is restricted |
| M0-03 Desktop automation | Accepted on 2026-10-18 | Fresh vanilla and Viewpoint games, movement, door interaction, clean exits and vanilla save reload; controller extended for scoped Steam/server work; 27 project checks pass |
| Workshop distribution | Created, hidden development | Collection `3822649790` contains the three presentation dependencies; no release stack accepted |
| M0-02 Dedicated baseline | One-client local subtest accepted; needs two-client test | Vanilla join, move, item transfer, reconnect, server restart, offline rollback and clean stops passed. Two-client/Steam-enabled/external-network checks remain unrun |
| M1 Viewpoint and shooting | Blocked by M0-02 | Clean isolated Viewpoint baseline; resolve `isometricnomore` separately |
| M2 Human encounters | Blocked by M1 | Select and test one NPC framework |
| M3 Horde event | Blocked by M2 | Select and test one horde owner |
| M4 First integrated slice | Blocked by M1–M3 | Shared event, leader effect/death, persistence |

No release mod stack has been accepted. The dedicated subtest was **vanilla, one client, loopback, non-Steam**, not multiplayer/modpack certification. The three presentation dependencies remain a separately GUI-tested candidate. Two-client observations, Steam networking, modded dedicated behavior, combat, sustained performance and capacity are untested. Current game/server are stopped cleanly; controller remains available.

Next: coordinate the two-client baseline with actual player platforms/count, then introduce the explicit presentation profile on another world. Integration/source inspection and update/recovery tooling can continue independently. See `INTEGRATION.md`, `ACTION_ITEMS.md`, and the milestone evidence.

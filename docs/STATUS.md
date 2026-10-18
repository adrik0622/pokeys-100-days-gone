# Pokeys 100 Days Gone — status

| ID | Status | Next evidence |
| --- | --- | --- |
| M0-01 Local inventory | Inspected; host-process visibility incomplete | Recorded in `docs/M0-01-local-inventory.md`; sandbox process view is restricted |
| M0-03 Desktop automation | Accepted on 2026-10-18 | Fresh vanilla and Viewpoint games, movement, door interaction, clean exits and vanilla save reload; controller extended for scoped Steam/server work; 27 project checks pass |
| Workshop distribution | Created, hidden development | Collection `3822649790` contains the three presentation dependencies; no release stack accepted |
| M0-02 Dedicated baseline | One-client local subtest accepted; multi-client experiment ready for agent exploration | Vanilla join, move, item transfer, reconnect, restart, rollback and clean stops passed. Next: two isolated local clients; current controller intentionally refuses a second process. Two-client/Steam/external-network checks remain unrun |
| M1 Viewpoint and shooting | Blocked by M0-02 | Clean isolated Viewpoint baseline; resolve `isometricnomore` separately |
| M2 Human encounters | Blocked by M1 | Select and test one NPC framework |
| M3 Horde event | Blocked by M2 | Select and test one horde owner |
| M4 First integrated slice | Blocked by M1–M3 | Shared event, leader effect/death, persistence |

No release mod stack has been accepted. The dedicated subtest was **vanilla, one client, loopback, non-Steam**, not multiplayer/modpack certification. The three presentation dependencies remain a separately GUI-tested candidate. Two-client observations, Steam networking, modded dedicated behavior, combat, sustained performance and capacity are untested. Current game/server are stopped cleanly; controller remains available.

User-confirmed planning target: **4–8 players**, with higher scale desirable only if measured. No second human tester is available. Next: explore two separately tracked local vanilla client processes, with separate caches/accounts and measured RAM/VRAM use; then test shared observations/reconnect/restart before introducing the presentation profile on another world. No multi-client run has occurred yet. Friend OSes remain unknown but are not a blocker to this local experiment. See `INTEGRATION.md`, `ACTION_ITEMS.md`, and the milestone evidence.

# Pokeys 100 Days Gone — status

| ID | Status | Next evidence |
| --- | --- | --- |
| M0-01 Local inventory | Inspected; host-process visibility incomplete | Recorded in `docs/M0-01-local-inventory.md`; sandbox process view is restricted |
| M0-03 Desktop automation | Accepted on 2026-10-18 | Fresh vanilla and Viewpoint games, movement, door interaction, three in-world exits with code 0; vanilla save reload; 13 automated checks pass |
| M0-02 Dedicated baseline | Ready | Current machine selected; working desktop controls available; dedicated installation, join, restart and restore remain unrun |
| M1 Viewpoint and shooting | Blocked by M0-02 | Clean isolated Viewpoint baseline; resolve `isometricnomore` separately |
| M2 Human encounters | Blocked by M1 | Select and test one NPC framework |
| M3 Horde event | Blocked by M2 | Select and test one horde owner |
| M4 First integrated slice | Blocked by M1–M3 | Shared event, leader effect/death, persistence |

No release mod stack has been accepted. M0-03 establishes local GUI control, initial first-person presentation and a single-player save/reload observation. Dedicated multiplayer, combat, sustained performance and capacity remain untested. Evidence and failed attempts are recorded in `docs/M0-03-desktop-smoke.md`.

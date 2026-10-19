# Pokeys 100 Days Gone — status

| ID | Status | Next evidence |
| --- | --- | --- |
| M0-01 Local inventory | Inspected; host-process visibility incomplete | Recorded in `docs/M0-01-local-inventory.md`; sandbox process view is restricted |
| M0-03 Desktop automation | Accepted on 2026-10-18 | Fresh vanilla and Viewpoint games, movement, door interaction, clean exits and vanilla save reload; explicit A/B control, scoped Steam/server work; 39 project checks pass |
| Workshop distribution | Created, hidden development | Collection `3822649790` contains the three presentation dependencies; no release stack accepted |
| M0-02 Dedicated baseline | Local vanilla subtests accepted; full gate open | One-client restart/rollback and two-client shared movement, cross-player transfer, reconnect, restart and clean stops passed. Steam/modded/remote gates remain open |
| M0-04 Autonomous dual clients | Accepted local subtest; further runs parked by user | Preserve existing evidence and resource limits. Feature-specific A/B testing remains deferred, not accepted |
| M1 Viewpoint and shooting | Dedicated integration next; acceptance pending M0 dependencies | Trial one modded client/server first, measure headroom, then A/B observations if safe; keep `isometricnomore` excluded |
| M2-01 Faction contact companion | Implemented; one-client interaction/restart passed | Shared standing, repeatable supply favor, Allied-gated assistance, cooldowns and native inventory sync. Physical NPCs and A/B feature checks not accepted |
| M2 Physical human encounters | Integration pending M1 and owner inspection | Select one NPC owner and connect verified encounter hooks to standing; contact records do not supply physical encounters |
| M3 Horde event | Blocked by M2 | Select and test one horde owner |
| M4 First integrated slice | Blocked by M1–M3 | Shared event, leader effect/death, persistence |

No release mod stack has been accepted. Vanilla local baseline tests and the independent **companion-only, one-client** contact/restart slice passed on separate non-Steam loopback worlds. The first idle-zombie dual world is preserved. The presentation dependencies remain a separately GUI-tested candidate; presentation-modded dedicated behavior, physical NPCs, forecasts/hordes/leader, calibration, Steam/remote networking, combat and capacity remain unfinished/unverified. Current clients/server are stopped with exit 0 and no test listeners; controller remains available.

User-confirmed planning target: **4–8 players**, with higher scale desirable only if measured. No second human tester is available. Latest direction: park more A/B testing and implement scoped gameplay; M2-01 is the first delivered slice. Next implementation work is source-level physical-contact/forecast-owner integration, preserving M1–M3 acceptance gates. Native client memory grew after in-process rejoin (~8.85 GiB PSS); cause is not established. Prefer fresh processes and bounded resource samples when testing resumes. Capacity remains unverified. See `M2-01-faction-contact.md`, `INTEGRATION.md`, and `ACTION_ITEMS.md`.

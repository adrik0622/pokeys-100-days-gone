# M5-01 — observer bulletin, calibration and recovery prototype

Status: original implementation and Lua adapter checks; engine check pending. Companion 0.2.0. This is **not M3/M4/M5 acceptance**. Physical-owner gaps are in `OWNER_SEAMS.md`.

## Engine observations — 2026-10-18 evening

Migration-only dedicated 184809 / native client 184882, same 42.21.0 build, checksums enabled. Existing native admin account Morgan Observer used solely for isolated debug controls; ordinary-player authority remains adapter-tested, not feature A/B accepted.

- Live owner scheduled world day 1 / 22:00. Bulletin displayed real baseline (e.g. 41.87–45.87 remaining world hours), unresolved direction and all five authored history entries. No invented physical migration.
- Manual screenshot round trips exceeded the task deadline and server correctly refused expiry. First OCR attempt stopped/cancelled when its third challenge could not be read confidently; no guessed completion. Retained raw screenshots.
- `scripts/calibration_smoke.py` then read the three displayed channels and clicked the corresponding UI buttons at 6.14 / 10.15 / 14.15 seconds. Lock completed visibly; end-to-end **18.11 seconds including capture/OCR overhead**. Result window 42.69–43.19 hours (half-hour width), versus baseline four-hour width. Repeat Lock left calibrated state and returned interrupted/no active task. No item payout.
- Existing Tesseract lacked English data. Downloaded only official [tessdata_fast](https://github.com/tesseract-ocr/tessdata_fast) English model into ignored `runtime/tools/tessdata`, not a system install. SHA256 `7d4322bd2a7749724879683fc3912cb542f19906c83bcc1a52132556427170b2`; pinned before reuse. No model payload redistributed. Fixed text-strip enlargement improves OCR; uncertain step/channel fails closed and cancels. This uses screenshots and controller input only, not direct Lua/RPC/memory reads.
- Client and server clean stops followed; restart persistence is being checked. Save/logs under `runtime/evidence/migration/`; selected images under `docs/evidence/2026-10-18-observer/`. Source abort correction/admin shortcuts were written after first staging; next fresh launch restages them before physical aftermath checks.

47 checks currently pass. Unit coverage and this one-client success do not accept direction, physical horde/leader, optional-interaction A/B, ordinary-player engine adversarial cases, interruption by movement/death or scheduled/active restart gates.

Smallest gap: Horde Nights exposes its real next-start world hour but no optional calibration or faction aftermath. No unrelated minigame framework is justified. Our add-on reads that schedule; it never schedules/spawns another horde or fabricates a warning when the owner is absent. Pre-arrival direction honestly remains unresolved. Baseline arrival interval +/-2 world hours; calibrated +/-15 minutes, shared for the same owner schedule. Disable upstream exact-time indicator in this trial or there is no player-facing advantage.

Right-click world → **Pokeys: observer bulletin**. Authored day-12/43/71/96/100 messages establish Mutual Aid, Observers and Reclaimers; clearly text fiction, not simulated NPC history. Late joiners can read it and the baseline anywhere. Relay task requires the existing house within 4 tiles, ground floor, alive.

Task: Begin; match the requested channel at >=4, >=8, >=12 real seconds; Lock at 15–25 seconds. Wrong channel, stale schedule, distance/floor/death, timeout, cancellation or restart stops it. Server owns start time, challenge, accepted steps, completion and one-minute start cooldown. No client score/time accepted, no item/standing payout. Retry cannot repeat the shared precision unlock. Persisted key invalidates if schedule changes; transient sessions do not survive server restart. Tasks can be automated by a modified cooperative client; this is reasonable input validation, not cheat-proof attention detection. Distance is sampled at requests, not continuously.

Real completed Horde Nights event with spawned zombies causes a **24 world-hour abstract Mutual Aid supply disruption**; assistance is server-refused during it. A successful existing supply favor repairs 12 hours. No physical base destruction, simulated damage, free event reward, or unbounded escalation. Identity prevents repeating that aftermath on polling/restart. Installing the observer into an existing event establishes a baseline instead of retroactively applying earlier damage. Native owner cap/offline/leader issues still block release.

## Focused test card (~5 minutes)

1. Owner absent: bulletin says unavailable, no countdown invented. History readable; faction favor remains usable.
2. Owner with future real schedule: skip tuning; actionable baseline window remains. Begin at relay; premature channel rejected; wrong channel cancels. No inventory/standing changes.
3. Retry after one real minute; correct channels/lock in 15–25 seconds; measure end-to-end time and interval tightening. Refresh/reopen and duplicate Lock must not produce another benefit. Leave relay or die mid-task; finish refused. Cancel/close leaves baseline.
4. Restart: partial task cannot finish; completed precision persists for unchanged schedule. Reconnect as late joiner and inspect shared forecast (feature A/B parked, not accepted).
5. Complete a real small event with spawned zombies: disruption appears once, aid refused; deliver favor, disruption shortens by 12 hours. Restart/poll must not extend it again. Zero-spawn/debug abort is not a successful migration.

Tests run: `lua5.1 tests/lua/migration_spec.lua` executes actual shared rules and server adapter, including timing boundaries, spoofed challenge/time, cooldown, restart, absence of owner, duplicate completion and consequence identity. Engine/UI, physical-event aftermath and feature A/B are separate unrun gates. Rollback code via local Git into a new test stage; preserve saved schema-1 observer data, never erase the world to hide failure.

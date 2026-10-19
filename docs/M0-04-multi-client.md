# M0-04 — Two autonomous local clients

Status: **local vanilla two-process networking subtest accepted**, 2026-10-18. Independently controlled clients shared movement/item state, survived disconnect/rejoin and a clean server restart, and exited normally. No second human was needed. Steam, remote networking, modded dedicated behavior, combat and 4–8-player capacity are not accepted by this result.

## Isolation and controls

- Server: profile `dual`, `runtime/server/dual/`, name `pokeys-m0-dual`, loopback `127.0.0.1:19870`, public listing and UPnP off. Original vanilla test world remains untouched. `config/server/dual.ini` fixes spawn to `(7990,11756,0)` so both characters can observe the same room; 2-player limit is a test setting, not the release target.
- Fresh dual worlds also receive `config/server/dual_SandboxVars.lua`: zombie population/respawn and randomized stories off. This is an explicitly safe **network fixture**, not the release survival preset. Existing cached settings are not overwritten automatically.
- Clients: slots `a` and `b`, caches `runtime/client-vanilla-a/` and `runtime/client-vanilla-b/`, separate credentials/accounts `pokeys_dual_a` and `pokeys_dual_b`. Both use `-nosteam`, 3 GiB heap limits, 1600×900 windowed, configured 30 FPS. Existing single-client profiles and normal user settings are not edited.
- Input and screenshots resolve each selected child's PID, not its title alone. Input confirms focus; held keys release before focus changes and on failures. No third slot is available. Main single-client mode cannot mix with A/B mode, and unrelated PZ processes are still rejected.
- Another named client launch requires 6 GiB **available** RAM after reserving the difference between current PSS and a conservative 6 GiB budget for each already-tracked live client/server. This avoids counting still-unused startup RAM twice when launches are close together. It is a launch guard, not continuous memory enforcement, a hard native-process limit or a capacity guarantee. Monitor runtime samples as worlds load.
- Explicit `terminate` remains a reported forced fallback for only the selected child. Normal exits are required for acceptance. Controller shutdown visits all tracked clients.
- Resource action reports tracked processes' RSS/PSS in KiB and host available memory. GPU usage is **host aggregate**, including unrelated desktop load; not per-client attribution or a performance benchmark.
- Existing snapshot helpers remain vanilla-only and reject the dual profile, avoiding accidental restoration of the wrong world.

Examples:

```bash
python3 scripts/desktop_control.py request '{"action":"server_launch","profile":"dual"}'
python3 scripts/desktop_control.py request '{"action":"launch","profile":"vanilla","client":"a"}'
python3 scripts/desktop_control.py request '{"action":"launch","profile":"vanilla","client":"b"}'
python3 scripts/desktop_control.py request '{"action":"status"}'
python3 scripts/desktop_control.py request '{"action":"resources"}'
python3 scripts/desktop_control.py request '{"action":"screenshot","client":"b","name":"observer"}'
```

Screenshots capture the desktop rectangle: keep windows non-overlapping. Trial layout A `(30,200)`, B `(1760,200)` on 3440×1440. After activating an unfocused window, allow it a frame to refresh before treating a screenshot as current.

## Initial observations

- Server PID 140954, client A PID 141003, client B PID 141111. Both logs confirm 42.21.0 / 4a0e9546ec and JVM max 3072 MiB. Separate client connections were recorded by the server. Character A **Alpha Baseline**; B **Bravo Baseline**; Custom Occupation.
- Reduced-rate native UI exposed a missed zero-duration Ctrl+A: B's default port was accidentally appended to instead of replaced. Caught in the screenshot before connecting, fixed shortcut timing to hold/release both keys, and verified the corrected port `19870`. No server/game compatibility failure is inferred from this input bug.
- Baseline before launching: ~19.0 GiB available RAM, 1,163 MiB host GPU use. During startup/menu/first-world loading: available RAM fell to ~4.2 GiB; host GPU reached ~6.7 GiB. These are spot samples, not measured maxima or 4–8-player capacity results.

## First-world interruption and preservation

Movement, A-to-B transfer and A's clean exit/rejoin passed in the first world. Zombies then entered the house during idle checks and killed both test characters. The final database marks both dead; the intended living-character server-restart test **did not pass in that world**. Clients and server still exited 0. The entire runtime was moved intact to `runtime/server/recovery/20261018-1807-dual-zombie-incident/` before creating the safe fixture. No player resurrection, inventory rewriting, anti-cheat bypass, or change to normal saves was used.

Fresh-fixture characters are **Alpha Network** (A) and **Bravo Network** (B), distinct from the archived Alpha/Bravo Baseline. Server PID 148512; A PID 148539; B PID 148677. Both independently observed movement and Alpha's dropped named card. Bravo took it and held both cards; Alpha's inventory and both Ground views were empty of that card. Alpha returned to the main menu while Bravo remained online with both cards; server `players` listed only B. Alpha then rejoined without character creation, with the same outfit, key ring and reduced inventory weight (1.01); Bravo still held both cards (1.51). Both returned normally to the menu and server `players` confirmed zero before console `quit`.

## Restart and final cleanup — passed

- Server 148512 saved, completed shutdown, exited 0 and released its listener. Retained its full offline world (8.2 MB) and logs at `runtime/evidence/dual/safe-first-session/` before restart.
- Restarted the same profile/world as PID 152397. Both clients rejoined directly without character creation. Server listed both accounts; both characters appeared together in the same house/outfits. Bravo's inventory still contained **ID Card: Alpha Network** and **ID Card: Bravo Network** (weight 1.51). Alpha had no ID card (weight 1.01); Ground was empty. Selected post-restart screenshots are versioned in `docs/evidence/2026-10-18-dual/`.
- Saved player rows before and after restart were identical in ID/account/name/position/death status: A ID 1, Alpha Network, `(7991.37451171875,11757.4970703125,0)`, living; B ID 2, Bravo Network, `(7990.71923828125,11756.716796875,0)`, living. No new player row appeared. This is a bounded marker/identity check, not a general proof against all duplication or stat loss.
- Both clients used Escape → Quit to Desktop → Yes and exited **0**. Server confirmed zero players, then `quit` completed with **0**, `Shutdown handling finished`, and no 19860/19870 test listeners. No forced termination or user input was needed.
- Retained final logs and offline world at `runtime/evidence/dual/safe-restart/`. Player DB SHA256: before restart `e899807ccce60af505ac84eba6285dda3e02ec29a5afcf221aaa944f532ccbca`; final `d0129bdb84936af9b45d18786194a9c3c6bd119d13a1d0e1c509c412093af16f`. The files differ as sessions/time are saved; the compared identity/location fields match. Raw queue actions/screenshots remain in `runtime/desktop-control/`.
- Server-normalized sandbox settings retained Zombies=6, ZombieRespawn=4, all three story chances=1 and population multipliers=0. Vanilla upstream diagnostics (including missing sound/model/property and packet-handler warnings) remain in the raw logs; this was not an error-free-startup claim.

## Resource limits and next step

Spot samples with both rendered clients reached ~5.0–5.5 GiB PSS each and ~5.2 GiB server PSS, despite 3/3/4 GiB Java heap limits. Available host RAM fell to **2.86 GiB** after repeated joins; host aggregate GPU use reached **10,127 MiB / 12,288 MiB**. No process swap was observed. Final all-stopped sample: **19,706,448 KiB available RAM**, no tracked live processes, **1,148 MiB** host GPU use. No measured FPS/TPS, latency, long-run leak, or capacity result is implied.

Keep this to two local rendered clients. Before a modded dual run, measure one modded client/server first and reassess native RAM/VRAM headroom. Do not attempt four or eight rendered clients to represent four or eight remote players. Next: isolated presentation-profile dedicated loading/join/reconnect on another world, while preserving Steam/remote/capacity as separate open gates. The Workshop collection and gameplay-owner choices were not changed by this test.

## Acceptance card

1. Both clients enter as distinct characters and observe one another. Capture A and B views.
2. Move A using only A's window, confirm movement from B while B's character remains unchanged. Move B separately as a control-target check.
3. A drops its uniquely named ID card. Both clients see it on the ground. B picks it up; A sees it disappear. Verify the card is in B's inventory, not duplicated in A's inventory/ground.
4. Disconnect A while B remains online; confirm B remains in the same world. Reconnect A, verify the same character and shared marker state.
5. Disconnect both, cleanly stop/restart the dedicated server, reconnect both and verify identities, location and transferred item.
6. Quit both clients through their menus, confirm both exit codes 0, then server `quit` and verify exit 0 / no listener. Capture final resource sample.

These observations accept only the **local vanilla two-process networking subtest**. They cannot establish Steam authentication, WAN/NAT, Windows/macOS compatibility, combat/NPC ownership, human gameplay quality, sustained performance or 4–8-player capacity. The next independent integration is the small Viewpoint profile, not an NPC/horde expansion.

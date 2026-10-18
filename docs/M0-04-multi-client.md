# M0-04 — Two autonomous local clients

Status: **in progress**, 2026-10-18. Two simultaneous native client processes reached separate game windows and authenticated against the dedicated server. Shared in-world observations, reconnect, restart and clean exits are still being checked. No second human is needed for this experiment.

## Isolation and controls

- Server: profile `dual`, `runtime/server/dual/`, name `pokeys-m0-dual`, loopback `127.0.0.1:19870`, public listing and UPnP off. Original vanilla test world remains untouched. `config/server/dual.ini` fixes spawn to `(7990,11756,0)` so both characters can observe the same room; 2-player limit is a test setting, not the release target.
- Clients: slots `a` and `b`, caches `runtime/client-vanilla-a/` and `runtime/client-vanilla-b/`, separate credentials/accounts `pokeys_dual_a` and `pokeys_dual_b`. Both use `-nosteam`, 3 GiB heap limits, 1600×900 windowed, configured 30 FPS. Existing single-client profiles and normal user settings are not edited.
- Input and screenshots resolve each selected child's PID, not its title alone. Input confirms focus; held keys release before focus changes and on failures. No third slot is available. Main single-client mode cannot mix with A/B mode, and unrelated PZ processes are still rejected.
- Another named client launch is refused below 6 GiB **available** RAM. This is a conservative launch guard, not continuous memory enforcement or a capacity guarantee. Monitor runtime samples as worlds load.
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

## Acceptance card

1. Both clients enter as distinct characters and observe one another. Capture A and B views.
2. Move A using only A's window, confirm movement from B while B's character remains unchanged. Move B separately as a control-target check.
3. A drops its uniquely named ID card. Both clients see it on the ground. B picks it up; A sees it disappear. Verify the card is in B's inventory, not duplicated in A's inventory/ground.
4. Disconnect A while B remains online; confirm B remains in the same world. Reconnect A, verify the same character and shared marker state.
5. Disconnect both, cleanly stop/restart the dedicated server, reconnect both and verify identities, location and transferred item.
6. Quit both clients through their menus, confirm both exit codes 0, then server `quit` and verify exit 0 / no listener. Capture final resource sample.

This can accept the **local vanilla two-process networking subtest**. It cannot establish Steam authentication, WAN/NAT, Windows/macOS compatibility, combat/NPC ownership, human gameplay quality, sustained performance or 4–8-player capacity. The next independent integration is the small Viewpoint profile, not an NPC/horde expansion.

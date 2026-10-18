# M0-02 — Isolated dedicated-server baseline

Status: **single-client testing in progress** (2026-10-18). Dedicated installation, vanilla loopback startup, client join, movement, item drop, save and clean shutdown passed. Restart/restore are being checked. Two-independent-client acceptance and the modded server profile remain unrun.

## Outcome

One client joins a disposable same-build dedicated server, reconnects after a controlled restart, and restores the disposable world from an offline backup. A second independent client is required before accepting the multiplayer gate.

## Chosen approach

Use a plain dedicated-server process on the present Manjaro host first. The machine has ample CPU/GPU capability for local client experimentation, but no capacity claim is made. GPU allocation is not assumed for a headless server. Defer k3s until this simpler baseline is demonstrated.

Use a separately installed dedicated-server payload and an isolated profile/world. Do not launch the bundled `start-server.sh` from the client install as the project baseline: its server build and data location have not been established, and the current client configuration must remain intact.

## Proposed scope and file boundary

Create a project-owned server runtime beneath this workspace (for example `runtime/server/`) and keep its disposable world, config, logs, and offline backups there. Do not touch `~/Zomboid/Server`, existing saves, or any host-wide service. First demonstrate the requested launch/new-game/move/interact/exit flow in M0-03; then reuse that input path for the server join test.

Start with vanilla to separate networking/persistence from mod integration. The next explicit candidate profile, pending server-side dependency confirmation, is:

```text
ZombieBuddy;Viewpoint;PZVoxelStudioViewpoint
```

Do not include `isometricnomore`, NPC, horde, ballistic, or content mods.

## Runtime operations and initial evidence

SteamCMD app `380870` installed/validated anonymously into `runtime/server/install/`. Steam build `25485538`; runtime reports `42.21.0 4a0e9546ec`, matching the client (client Steam build ID differs as expected for a different app). Dedicated core JAR SHA256: `e1a69eb743ede60b213a0fe7f8b83d4fcab773036d256cc4543a336f3b058a33`.

The controller supports fixed `server_install`, `server_install_status`, `server_launch`, `server_status`, `server_command` (`save`, `players`, `quit` only), `server_backup` and `server_restore` actions. No shell/console execution endpoint is exposed. Launch uses the server's bundled Java, a 4 GiB heap limit, separate `-cachedir`, `-nosteam`, `-ip 127.0.0.1`, ports 19860/19861, and `config/server/vanilla.ini`. `ss` confirmed UDP **127.0.0.1:19860**, not a wildcard listener. Public listing and UPnP are disabled. This does not test Steam authentication, external networking, firewall/NAT, or production capacity.

Client A: isolated `client-vanilla`, multiplayer favorite **Pokeys M0 local**, account `pokeys_trial_a`, character **Jo Jarvis**, Custom Occupation, Rosewood. Spawn observed at `(7989,11755,0)` in the server log; normal `S` input moved the character. Dropped the uniquely named **ID Card: Jo Jarvis** onto the floor beside the refrigerator and verified it in the Ground inventory. Server `save` logged `World saved` / `Saving finish`. Client Quit returned to menu; server `quit` completed with exit code 0 and no remaining UDP listener.

Offline snapshot `20261018-173100-vanilla` contains 1,206 files, covering the world, server settings and account database. Snapshot integrity is SHA256 checked. Restore retains the previous state under `runtime/server/recovery/`; it never deletes the prior world. Credentials, databases and raw logs remain ignored. Current controller credentials are generated in ignored runtime files and are not printed into the action log.

Both vanilla client and dedicated logs contain upstream warnings (missing tiles/icons, Lua requires, packet-handler listings); this was not an error-free run. Preserve raw logs when comparing the modded trial.

## Backup / restore procedure

1. Stop the disposable server cleanly and verify its process is gone.
2. Copy the entire isolated world directory to `runtime/backups/<timestamp>-before-restart/`.
3. Start the server, connect, then stop it cleanly.
4. To restore, keep the failed world directory intact by renaming it within `runtime/`, copy the selected backup back to the expected world path, and restart.
5. Verify the restored world by its recorded player location/time and a small placed-item marker. Never restore over the main client or an existing server profile.

## Smallest test card (15–25 minutes once installed)

Setup: record the dedicated-server build/revision and enabled Workshop payload hashes; start a fresh isolated world; save the first 80 lines around mod loading from the server log.

1. **Client A joins** with the same 42.21.0 build and the three-item list above. Expected: connection succeeds; no missing-mod, Java-agent, or version rejection.
2. Have Client A place one named marker item, disconnect, then reconnect. Expected: the same character/world and marker remain.
3. Take the offline backup, perform one clean server restart, and reconnect. Expected: no duplicate character/item and no fresh-world creation.
4. Restore the offline backup and reconnect. Expected: the marker and world state match the backup point.
5. Repeat steps 1–3 with Client B from a second independent client. Expected: both observe the same marker; joining/rejoining one client does not reset the other.

Failure triage: first capture the earliest relevant server-log error and the surrounding 40 lines. Check server/client build equality, Workshop IDs/mod IDs and order, then ZombieBuddy Java-agent setup before adding any mod.

Acceptance evidence: server build/revision, exact server and client mod list/hashes, startup and join excerpts, restart result, restore result, and both-client observations. Passing this unlocks M1's Viewpoint/native-gunplay test; it does not yet approve a firearm alternative.

# M0-01 — Local inventory

Recorded 2026-10-18 from local files and a prior client log. This is file/log evidence, not a multiplayer or dedicated-server test.

## Verified inputs

| Area | Finding | Evidence |
| --- | --- | --- |
| OS | Manjaro Linux, kernel `6.18.44-1-MANJARO`, x86_64 | `uname`; client log |
| Client installation | Native Steam installation at `/home/adrikingston/.local/share/Steam/steamapps/common/ProjectZomboid` | Steam app manifest; Linux session log |
| Game build | `42.21.0`, revision `4a0e9546ec`, Steam build ID `25485521` | `~/Zomboid/version.txt`; `appmanifest_108600.acf`; client log |
| Steam branch | No beta branch is recorded in the app manifest; installed depot is `108603` | `appmanifest_108600.acf` |
| Launch options | Desktop entry is `steam steam://rungameid/108600`; no per-game launch arguments were found in the inspected entry | desktop entry |
| User data | `/home/adrikingston/Zomboid` | local installation |
| Dedicated server | No SteamCMD dedicated-server app (`380870`) or local `Zomboid/Server` profile was found. The client install does contain `projectzomboid/start-server.sh`, but it has not been run. | local filesystem |
| Running process | No PZ process was visible inside the task sandbox. Host process absence is unverified: the sandbox exposes only its own processes. | restricted process view |
| Hardware | Ryzen 9 5950X (16 cores/32 threads), 31 GiB RAM, RTX 3080 Ti; 116 GiB free on `/home` at inventory time | `lscpu`, `free`, `lspci`, `df` |

The previously reported 42.19/current-candidate conflict is resolved locally: this client is already on the build Viewpoint pins to (`42.21`). This does **not** certify Bandits, a horde mod, or a dedicated server on this build.

## Current client configuration

`~/Zomboid/mods/default.txt` enables:

| Workshop ID | Mod ID | Local version / requirement | Status |
| --- | --- | --- | --- |
| 3619862853 | `ZombieBuddy` | runtime log: `2.3.4`; Viewpoint requires `>= 2.3.0` | Loaded successfully as Java agent |
| 3809306528 | `Viewpoint` | `0.1.6.1`; `versionMin=42.21`, `versionMax=42.21` | Loaded successfully; log says build is pinned |
| 3810302175 | `PZVoxelStudioViewpoint` | `1.0`; pinned to `42.21.0` | Enabled; model-pack behavior untested |
| 3819166046 | `isometricnomore` | `0.1.17`; `versionMin=42.21`; requires Viewpoint and ZombieBuddy | Startup log reports `ClassNotFoundException: viewpoint.core.View` and an invocation error before Viewpoint loads; later behavior unverified |

Only ZombieBuddy and Viewpoint from the proposed release candidates are locally subscribed/installed. No NPC or horde candidate is installed. Existing multiplayer save folders and user settings were inspected only by name and were not modified.

The last client session confirms that ZombieBuddy loads before Viewpoint and that Viewpoint starts on 42.21. It also contains the `isometricnomore` failure above. Therefore the present client is useful evidence for the Viewpoint build match, but not yet a clean M1 combat baseline.

## Narrow build choice

Use **Build 42.21.0 / revision `4a0e9546ec`** as the baseline candidate. Preserve the main client installation and its current settings. Do not add Bandits, Kane, Horde Nights, Hark's Horde Night, a ballistics replacement, or an NPC framework until the isolated dedicated-server baseline passes.

Before the first server test, the only proposed configuration change is an isolated profile whose initial mod list is:

```text
ZombieBuddy;Viewpoint;PZVoxelStudioViewpoint
```

`isometricnomore` is deliberately excluded pending identification and a clean client startup. This is a proposed diff only; no client or server configuration was changed.

Update: identified on 2026-10-18 at `steamapps/workshop/content/108600/3819166046/mods/isometricnomore/42/mod.info`. Its CRLF line endings caused the earlier exact-ID search to miss it. It remains excluded from the first isolated trial while the logged initialization error is investigated.

## Unknowns remaining

- The dedicated-server executable/version must be installed and matched to this client before joining is tested.
- The intended host/topology and friend platforms are unselected.
- Viewpoint's dedicated-server handshake and the model-pack's multiplayer behavior are untested.
- Existing external multiplayer saves are not evidence for this project and will not be reused.
- Desktop access requires the user-started bridge described in `docs/M0-03-desktop-smoke.md`: direct X11 and D-Bus connections return `EPERM` in the task sandbox.

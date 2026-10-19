# M0-03 — Desktop automation and disposable client

Status on 2026-10-18: **accepted for autonomous local GUI smoke testing**. The controller completed a fresh vanilla game, movement, door interaction, clean exit, save reload and second clean exit; it also completed a separate fresh Viewpoint game, first-person movement, door interaction and clean exit. All three in-world runs exited with code 0. No forced termination was used. See the evidence below.

Direct X11 and KDE D-Bus access from this task fails with `EPERM`. The task also has no GPU device nodes or host-process visibility. The user-started controller provides the working X11 screenshot/input and launch path from a normal desktop terminal.

## One-time activation

In a normal desktop terminal, run:

```bash
python3 /home/adrikingston/Projects/pokeys-100-days-gone/scripts/desktop_control.py serve
```

Leave the terminal running. The expected message is `PZ desktop bridge ready`. Ctrl+C stops the bridge and closes its disposable client if one is running. No installation or root access is needed. Existing `xdotool` and ImageMagick provide input and screenshots.

The bridge accepts a fixed set of actions through project-local JSON files. It opens no listening socket, installs no service, executes no arbitrary shell text, and only sends input to a game window belonging to the client it launched. Individual key holds last at most five seconds and release on focus loss. An action record and screenshots remain under `runtime/desktop-control/`; this directory is ignored by Git.

During development, edits to the controller reload between requests while retaining the tracked process. The user's terminal does not need restarting for further controller changes. The controller is currently left idle and ready for subsequent tests, with its game closed.

## Operator commands

Run from the project directory:

```bash
python3 scripts/desktop_control.py request '{"action":"status"}'
python3 scripts/desktop_control.py request '{"action":"launch","profile":"vanilla"}'
python3 scripts/desktop_control.py request '{"action":"screenshot","name":"main-menu"}'
python3 scripts/desktop_control.py request '{"action":"hold","key":"w","seconds":0.5}'
python3 scripts/desktop_control.py request '{"action":"key","key":"e"}'
```

Clicks use game-window coordinates: `{"action":"click","x":400,"y":300}`. Text is limited to short game/character names. Screenshots capture the game's visible rectangle, so keep it unobscured. Send one input, inspect its result, then decide the next input. Do not replay a string of unverified coordinates.

`{"action":"close"}` requests window closure; `status` must then show the process exited. `{"action":"terminate"}` is an explicit fallback scoped to the tracked disposable process and always reports forced termination. A forced exit does not pass a clean-save test. `{"action":"stop"}` stops the controller after its game has exited.

## Profiles and launch inputs

The controller uses the installed native `ProjectZomboid64` executable and its existing JVM configuration, with a separate `-cachedir=` and `-nosteam`. Both switches were verified in the running client logs and isolated save locations. This offline launch does not verify Steam authentication or Workshop synchronization for multiplayer.

- `vanilla`: `runtime/client-vanilla/`, initially no enabled mods.
- `viewpoint`: `runtime/client-viewpoint/`, references the installed ZombieBuddy, Viewpoint and PZVoxelStudioViewpoint directories using symlinks; adds the existing ZombieBuddy Java agent. No upstream code/assets are copied into the project.

The launcher prepends the game's `jre64/bin` to its child process's `PATH`. Viewpoint's verified argument order is:

```text
ProjectZomboid64 -javaagent:<installed-game>/ZombieBuddy.jar=policy=deny-new -- -cachedir=<project>/runtime/client-viewpoint -nosteam
```

The `--` separator is required by the native launcher. The agent uses the existing approvals with `deny-new`; it does not grant approval to unknown JARs. Installed documentation: `steamapps/workshop/content/108600/3619862853/mods/ZombieBuddy/doc/Installation.md`.

Each cache starts at 1600×900 in a window with 60 FPS configured. Settings and saves in each cache persist across relaunches. Main client settings and saves are not copied or edited. Start with vanilla to establish input, screenshot and shutdown behavior, then repeat with Viewpoint. This GUI smoke test does not accept the later dedicated-server or combat gates.

## Acceptance test (estimated 10–20 minutes after activation)

1. Launch the disposable vanilla client. Confirm the process, window and main-menu screenshot, build/revision and cache path in its log.
2. Navigate the actual New Game UI, select a low-pressure preset, create a character and load a fresh world. Capture each decision screen. Do not label the tutorial or a pre-existing save as a new survival game.
3. Capture the character at a recognizable location, hold a movement key briefly, then capture the changed position. Confirm the character moved, rather than only the camera.
4. Approach a door or container and interact through normal input. Capture the visible state change or container contents. Opening only the pause/menu UI does not satisfy this step.
5. Quit through the game's UI. Confirm the tracked process and window are gone, and inspect save files and shutdown logs. A forced termination must be reported separately.
6. Relaunch, confirm the disposable save is retained, and exit again to check repeatability. Repeat the basic flow with the Viewpoint profile if vanilla passes.

Evidence required: screenshots of the main menu/new game, before/after movement, before/after interaction, process exit status and local game logs. Record any failed attempt and all forced exits.

## Observed results — 2026-10-18

| Run | Inputs and observations | Exit |
| --- | --- | --- |
| Vanilla new game, PID 113131 | Solo → Rising → Rosewood → `M0_Desktop_01`; Custom Occupation, Tyrone Truong. Held `S` for 0.8 seconds; character crossed the rug. Door context menu → Open Door; character walked to the door and opened it. | Quit to Desktop → Yes; code 0; world save and `GameThread exited` logged |
| Vanilla reload, PID 116752 | Continue loaded the same character at the doorway with the door still open. `E` closed it. Database retained exactly one living local player, at the same saved coordinates `(8306.482421875, 11691.5107421875, 0)`. | Same UI exit; code 0; world save and `GameThread exited` logged |
| Viewpoint new game, PID 118543 | Solo → Rising → Rosewood → `M0_Viewpoint_01`; Custom Occupation, Stephen Pinson. Completed Viewpoint onboarding with Low preset. First-person rendering, relative mouse look, cursor toggle and `W` movement worked. Targeting the door showed Open Door; `F` opened it and the prompt changed to Close Door. | Same UI exit; code 0; world save and `GameThread exited` logged |

Viewpoint player coordinates changed from `(8495.5, 11550.5, 0)` in the initial save to `(8495.6513671875, 11552.20703125, 0)` at shutdown, with one living player record. This corroborates character movement independently of the camera. The Viewpoint save has not yet been reloaded; the observed reload test was vanilla.

The Viewpoint wizard recommended Low based on approximately 0.4 GB free physical RAM. At that moment `free -h` reported 12 GiB **available** including reclaimable cache. Low is the test setting, not a measured hardware limit. Its internal preset name is `Potato`; shader mode is Vanilla, with first-person rendering and 3D model packs enabled. No performance budget or multiplayer capacity is accepted from this smoke test.

### Evidence locations

- [Vanilla before movement](../runtime/desktop-control/screenshots/vanilla-move-before.png), [after movement](../runtime/desktop-control/screenshots/vanilla-move-after.png), [door context](../runtime/desktop-control/screenshots/vanilla-door-context.png), [door opened](../runtime/desktop-control/screenshots/vanilla-door-open.png).
- [Vanilla reloaded world](../runtime/desktop-control/screenshots/vanilla-save-persistence.png), [door closed with E](../runtime/desktop-control/screenshots/vanilla-reloaded-door-closed.png).
- [Viewpoint first-person approach](../runtime/desktop-control/screenshots/viewpoint-door-approach-before.png), [after movement / Open Door prompt](../runtime/desktop-control/screenshots/viewpoint-after-movement.png), [opened door / Close Door prompt](../runtime/desktop-control/screenshots/viewpoint-door-open.png), [quit confirmation](../runtime/desktop-control/screenshots/viewpoint-quit-confirmation.png).
- Preserved session logs: `runtime/evidence/vanilla-first-console.txt`, `vanilla-reload-console.txt`, `viewpoint-first-console.txt`.
- Offline player database snapshots: `runtime/evidence/vanilla-first-players.db`, `viewpoint-first-players.db`.
- Every request and response, including exit status: `runtime/desktop-control/actions.jsonl`.

### Fixes discovered during the actual test

1. First launch, PID 112796, exited with code 1 before opening a window because the bundled Java was missing from the child `PATH`. Fixed the environment to match the installed startup script.
2. Very short XTEST input and immediate cursor movement could miss a frame or turn a click into a drag. Clicks now settle for 150 ms, hold for 120 ms, then release; key taps hold for 120 ms. Key holds always release in a `finally` block.
3. `xdotool mousemove --sync` timed out when clicking the same coordinates again. Removed that flag; repeated same-position clicks then passed.
4. Initial Viewpoint trial, PID 117911, passed `-javaagent` as a game option. Its log identified the unknown option; no Viewpoint rendering was claimed for it. Closed through the UI with code 0, corrected JVM/game argument separation, and verified `[Viewpoint] loaded` / pinned build in the next run. The failed log is retained in `runtime/evidence/viewpoint-agent-argument-failed.log`.

Existing font and map-metadata warnings/errors occur in the vanilla logs as well as the Viewpoint logs. Viewpoint also reports occasional slow frames. Logs are retained for later triage; this acceptance covers basic control and saving, not error-free logs, graphics completeness, combat or sustained performance.

### Controls verified in this build

- Native isometric UI: mouse selection, text entry, `W`/`S` movement, door context action and `E` near a door.
- Viewpoint tested inputs: middle mouse changes cursor/camera control; relative mouse movement changes view; `W` moves the character; `F` performs the displayed door action. Onboarding also documents `O` to toggle first person; that toggle was not separately exercised in this run.
- For clicking game UI while in first person, free the cursor with middle mouse first. The pause menu frees it automatically. Absolute mouse movement while camera control is active changes the view.
- Exit: `Escape` → Quit to Desktop → Yes. At 1600×900, the tested menu click is `(276,657)` and confirmation is `(745,488)`. Verify the current screen before reusing coordinates. Window origin changed between launches; game-relative coordinates remained valid.

Original `~/Zomboid/options.ini`, `console.txt`, `viewpoint-live.properties` and `mods/default.txt` still had their prior October 17 modification times after all tests. All created worlds and Viewpoint setup settings are in the project caches.

## Automated checks already run

```bash
python3 -m unittest discover -s tests -v
```

13 checks passed: reject desktop shortcuts, unbounded holds and control text; release held keys on focus loss; refuse input without an owned game window; contain screenshot/profile paths; retain separate test settings; launch without a shell and with the isolated cache and bundled Java; reject a second client; scope forced termination to the tracked child; request graceful window closure; reject a stale controller heartbeat; place the Java agent before the required JVM separator. These checks use mocked desktop/process calls. Actual gameplay and shutdown evidence is recorded separately above.

## Reattempt after Steam Link virtual-monitor activation — 2026-10-19

The user reported a virtual monitor running through Steam Link and authorized another automated client attempt. The host controller reported display `:0`, geometry 3440×1440, and existing main/client-a/client-b processes exited with code 0. A fresh isolated `vanilla` launch (PID 585442, cache `runtime/client-vanilla`) returned successfully from the launcher request, but exited with code 0 before creating a visible game window. The controller's screenshot request correctly refused with `Expected one owned game window, found 0`; no blind key/click input was sent. The fresh `runtime/client-vanilla/launcher.log` again ends at `NullPointerException` in `org.lwjgl.glfw.GLFW.nglfwGetVideoMode` → `Display.init` → `MainScreenState.main`.

This confirms the prior launch failure persists even with the virtual monitor reported active; the root cause is not established. The task sandbox cannot inspect the host X display directly (`xrandr` reports `Can't open display :0`). Do not infer a game/mod defect from this environment symptom. HR-008 now records that a visible PZ window on the same desktop session is still needed before movement/interact/join checks resume.

As a separate headless game check, the isolated `day100` dedicated profile (PID 586160; loopback 19830/19831) loaded `PokeysObserver` and `PokeysCampaign` (`schema=1`, calendar 1993-10-17 / worldAgeHours=2), reached `SERVER STARTED`, accepted a normal save and quit, logged `Shutdown handling finished`, exited 0, and released the UDP port. This validates dedicated startup/shutdown and module load only—not a joined client, survival period, or gameplay loop. No main saves or services were touched; the disposable server runtime remains under ignored `runtime/`.

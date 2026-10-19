# Physical-owner inspection — 2026-10-18 evening

Source inspected in locally subscribed original Workshop payloads. Neither is enabled in an accepted profile. Steam's existing login downloaded both; no key/password/MFA needed. No upstream code/assets copied into Git. Horde Nights' web page failed in the web tool but loaded in Steam.

## Horde Nights 3782615002 / HordeNights 1.1.3

Root: `steamapps/workshop/content/108600/3782615002/mods/HordeNights/42/media/lua/server/HordeNights/`.

- `HordeManager.lua`: server minute scheduler; public `start`, `complete`, `abort`, `nextStartWorldHour`; persistent numeric event identity. Debug commands check server role/capabilities. Targets largest connected living group; late joiners are not added automatically to saved target usernames.
- **Direction gap:** local `selectApproach` runs inside `start`, not when scheduling. No ahead-of-time directional forecast hook. A countdown does not satisfy the directional warning requirement. Need a small author hook or separately reviewed original adapter; never invent a forecast direction.
- `HordeSpawner.lua`: tags `HordeNightsID`/`HordeNightsTagged`; public active set, spawn/reconcile/direct functions. Living survivors remain after completion. Server issues native awareness/path commands; MP ownership/path agreement is untested.
- **Cap gap:** `reconcileActive` counts loaded zombies only. Unloaded and previous-event survivors escape its active count. Finite total budget and zero scaling bound births per event, not accumulated survivors across cycles.
- **Offline gap:** minute handler still delivers after targets leave until end. `PauseEmpty=true` helps only when everyone leaves; another connected group keeps time running. Need abort/no-more-spawn on lost target, without deleting ordinary survivors or attacking offline settlements.
- Disable default 100% sprinters, scaling, supply drops and exact-time day indicator in first trial. Calibration has no information advantage if the native exact-time indicator remains visible. Private-coop trust boundary must be disclosed.
- No leader identity/effect exists here. Need a verified owner-aware rally/attraction hook plus death/unload/restart handling before promising that feature.

Preferred **trial** owner over Hark's per-player queues: one shared event, finite budget and tagged entities. Not release accepted. Hark Stable author docs do not prove a strict server-wide cap. No second director enabled.

## Bandits 3268487204 / Bandits2

Root: `steamapps/workshop/content/108600/3268487204/mods/Bandits/42.21/`; metadata advertises V2 B42.20+, no numeric modversion.

- `media/lua/server/BanditServerSpawner.lua`: public `BanditServer.Spawner.Clan`, `Individual`, `Virtual`, `Type`; accepts explicit `hostile` / `hostileP`, program/stage and position. Server brain creation separates general hostility from hostility toward players. Virtual is bodyless until loaded, not a demonstrated encounter.
- Spawner client-command forwarding has no local role check in that handler. `BanditServerSync.lua` forwards submitted health updates. Our campaign authority does not make this framework adversarial-server-authoritative. Private-coop trust, damage and ownership still require tests.
- These APIs supply no standing ledger. Companion owns group standing/rewards; Bandits remains sole physical NPC candidate. Contact records are not human encounters.
- Author prohibits reupload without permission. Use separate add-on/dependency reference, not a copied/file-shadow fork.

Next: prototype only narrow independent forecast/calibration/briefing gaps. Physical cap, leader ownership and target-specific damage remain acceptance blockers, not reasons to add competing frameworks.

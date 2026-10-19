# V2-01 — isolated A-Life / Jeem trial

2026-10-18, native Linux 42.21.0 / `4a0e9546ec`. **Active investigation, not an accepted replacement or release stack.** [SC-003](SCOPE_CHANGES.md) authorizes these tests and corrects the anti-PK inference: consequence is the pillar, not universal punishment. No existing v1 world is converted. Bandits stays installed but is absent from both new profiles.

## Reproducible inputs and isolation

| Input | Actual installed metadata | Complete payload pin |
| --- | --- | --- |
| Project A-Life | Workshop 3803984183, ProjectALifeNPCs, 1.4.5; directory 42.20 declares versionMin=42.21.0 | 1,691 files / 52,325,148 bytes; dd47ff5087c42abdd50f572d443a84497d1ab424453586b6073cf00e66c04b91 |
| Jeem Extension | Workshop 3806944055, ProjectALifeJimmy, 0.7.4; requires/loads after ProjectALifeNPCs; min 42.21.0 | 263 files / 8,805,189 bytes; 25481a2c8e789b1adad057351c8d00ce5ee3241313e194ee50d4d910ae22a084 |

Original downloads obtained through subscribed Steam items. Metadata/payload fingerprints are in [modpack.json](../config/modpack.json); no upstream source/assets copied into Git. License/derivative permission is not established; use dependency references, not an assumed permission to fork/reupload. Hidden collection remains three presentation references, not these candidates.

New loopback profiles: **alife** 19810/19811, **alife-jeem** 19800/19801. Separate client caches/worlds; only A-Life or A-Life+Jeem respectively. No Bandits, companion, horde, presentation, Java agent or extra mod. Checksums retained, Public/UPnP=false, two fixture slots, PVP=false (fixture safety, not final PvP policy). Settings: [core](../config/server/alife_SandboxVars.lua), [combination](../config/server/alife-jeem_SandboxVars.lua). Actual declared types/ranges checked for all 20 core and six Jeem overrides.

PopulateOnStart=1 means Off, not boolean true. Encounters/raids/outposts/support/revenge/faction warfare disabled; logical squad budgets reduced to four. Logical off-screen seeding still occurred: these are not guaranteed zero-population settings. Jeem residents, base raids and random traders disabled; standing/one-reputation enabled. Other feature defaults remain; do not call every Jeem feature disabled or these values release balance/safe capacity.

## Source-inspected capability boundary

Paths below are relative to each installed version's media/lua directory; source inspection is not engine acceptance.

| Need | Existing implementation / inspected seam | What remains to prove |
| --- | --- | --- |
| Logical world + physical actors | A-Life server Core/ALifeServerBootstrap, ALifeSettings and ALifePersistence; ProjectALife.World.v1 ModData; persistent squad records, server ticks and shell lifecycle | Identity/casualties through materialization/unload/restart, no duplicates; bounded split groups |
| Custom factions/content | Native faction/NPC Creator and server admin spawn service; county EMS medic preset exercised | Our faction definitions/import format and durable mappings; no provisional v1 lore migration |
| NPC violence consequences | A-Life server Decisions/ALifeReputationPersonal.onActorKilled, server-authority guard and UID:generation dedupe; contextual classification | Real direct/delayed damage attribution, client handoff and visible effects; no universal PK claim |
| Broader standing | Jeem Services/Standing: per-player/faction/group points, bounded recent events, first-hand vs decaying rumor, vanilla player-faction pool share | Actual scores/label/access response, witnesses/rumors, persistence and group policy |
| Avoid duplicate reputation | Jeem Features/Standing/AlifeDeeds maps gifts/trades/treatment/release to A-Life opinion/personal/standing with deferred writes, tokens and rate/day/ledger limits | Native action produces exactly the intended effect; don't add a parallel reward engine |
| A-Life 1.4 overlap | Jeem shared Core.installAll detects upstream generation and stands down overlapping health/boarding/fixes | Runtime installer mode observed below; behavior still needs separate tests |
| Player-kill consequences | A-Life bootstrap registers player/character death handlers; Personal.onPlayerDied marks the victim's record dead. Jeem HostileFaction reads native PvP setting | These are NOT proof of trustworthy PvP killer attribution or our faction-specific policy. Controlled PvP fixture later; retained PVP=false unchanged |
| Viewpoint | A-Life includes Compat/ALifeViewpointAdapter source | Not enabled in this trial; camera/gun/NPC/player damage acceptance remains separate |

Prefer these upstream systems wherever demonstrated. Candidate is promising for the living-world goal but not selected from an advertisement/startup alone. No custom NPC AI, reputation replacement or universal consequence implementation was written.

## Runtime observations so far

Core server/client PIDs 242678/243072. First launch used preparation working tree after 8514369, subsequently committed as 3cc7303; **not a clean-commit launch**. Joined native admin Casey Core, moved in the separate house world. A-Life status reported running/Health OK, faults/overruns 0/0 in the sampled window, four off-screen squads founded; 12 logical people in the world / 360 living census, not 360 physical bodies. Logs showed coarse fishing/scavenging/travel assignments; no claim that physical NPCs traversed those routes.

Native A-Life admin console requested **one** friendly County EMS medic, Patrol, Save squad=Yes. Server accepted one and hydrated UID `palife:1792382769414:1`, generation 1 at 7993/11756. Live population UI reported one record, one active/body, Henry — Paramedic; later position 7988/11735 (21 tiles away). Patrol movement made initial visual contact inconclusive. A fixed native admin approach at 7988/11738 is guarded by matching owned trial processes; no arbitrary command/coordinate input. An initial malformed attempt was local chat only; command was visually verified before successful submission. Do not claim ordinary exploration or visible medic/dialogue/damage from census/hydration alone.

Client log included runtime_start_failed: server_authority_required while dedicated runtime was running. Preserve the message; do not misclassify the client-realm authority refusal as either a proven fatal server failure or a clean error-free run. On client departure the server recorded shell_missing / unloaded at 7994/11765; retained logical UID exists in saved ModData. This is not a verified reload/restart result.

Core client Quit to Desktop/Yes exited 0; server listed zero players and quit 0 / Shutdown handling finished, no listener. Offline world/config/logs retained at runtime/evidence/alife/core-first-stop; ModData SHA256 d67e0341706661be528dc268d9e53243a66d7800cba9f41acff87d85ec864853. No restore/reset performed.

Combination launched from clean fe2853b: server/client PIDs 253854/253923. Dedicated reached SERVER STARTED, detected A-Life 1.4, printed its overlap stand-down message and Jeem v0.7.4 installed (server): 68 ok, 0 disabled. This is installer status, not 68 gameplay features accepted. Native gameplay checks continue below/next.

### Combination contact and gift — observed

Jamie Jeem joined as the fixture admin. Native console spawned one County EMS medic at 7996/11756, position locked and Save squad=Yes. UID `palife:1792383752677:1`, generation 1, onlineId 11306. This body was visible on the road and spoke ambient lines. Native right-click → Talk opened a cinematic conversation with **Delbert Pham**, initial opinion **+17 / Likes you**. A preview had named Henry; the unfixed-seed actual roster rerolled, so actual name/UID, not preview, identify the test actor.

Jeem logged promotion of squad:5 / County EMS crew after talking. “How can I earn your trust?” explained food/medicine/combat help/fair trades; an immediate initial click was rate limited (“Give them a second”), later request answered. Medical-supply request was refused because he could not spare any; no item reward claimed. Mystery UI initially said Stranger, then learned the actual name/faction tag.

Fixed native fixture supplied two bandages once, confirmed Bandage (2) and ID Card: Jamie Jeem in inventory. Equipped one as primary and used Supplies → Here, take this Bandage once. Server logged **1 item received by the same UID / alife_county_ems; +3.0 standing of 3.0**. Conversation showed opinion **+17 → +19**, and the inventory subsequently showed **one** Bandage (not stack 2). The gift option became marked Asked/hold something first; no second bandage equipped or gift sent. These are distinct Jeem standing and A-Life opinion observations, not interchangeable units or proof of faction access thresholds, packet deduplication or PvP policy. Diagnostics then disabled, confirmed in preferences and server log. Fresh-process persistence check follows.

### Fresh-process combination restart — narrow result

First combination client/server exited 0; server listed zero players, Shutdown handling finished, no listener. Preserved offline world/config/full logs at runtime/evidence/alife/jeem-before-restart; ModData SHA256 cbc2dce94ab73a3494ebb043390d089e15f36c7f7edd95a2599a57189fc24a5c. Restarted from clean c6ff6a5 as server/client 262116/262184, same cache/world/account, no restore or extra spawn/gift/supplies. Jamie rejoined without character creation; inventory still one Bandage and Jamie Jeem ID card.

Server removed the old saved zombie shell as a restart ghost, then hydrated **the same UID**, generation **2**, onlineId **31934**, at 8004/11763 (12.4 tiles from Jamie). Walked over normally; visible Delbert Pham and native conversation returned. Opinion was **+27 / Likes you**, not exactly the earlier immediate +19. No second hand-gift log/action occurred. Source gives a plausible explanation: HandGifts emits act=gift; AlifeDeeds queues NpcOpinion.note(gift), whose base increment is eight. This is **source-supported inference for the additional eight**, not an experimentally isolated timing result or proof the exact total was unchanged across save. The consequence clearly did not reset to the initial +17; don't claim exact score invariance or duplicate-proof rewards.

Important limits: clothing changed (turquoise long sleeves/black trousers → short sleeves/blue trousers plus sunglasses), position shifted, and he moved after the restart despite the initial position-lock setup. Cause is unassigned: outfit variation, normal off-screen movement, and fixture setting retention need a focused comparison before calling visual/guard-post persistence accepted. A single new shell/retained identity is observed, not a global duplicate audit or dead-NPC resurrection test. Jeem also logged a reported gift after restart; no witness propagation policy is accepted from that message. Ordinary player, hostile/damage/PvP, ownership handoff and Viewpoint are unrun.

Selected screenshots: [core census](evidence/2026-10-18-alife/01-core-census.png), [visible medic](evidence/2026-10-18-alife/02-visible-medic.png), [initial conversation](evidence/2026-10-18-alife/03-conversation-before.png), [gift opinion](evidence/2026-10-18-alife/04-gift-opinion.png), [remaining item](evidence/2026-10-18-alife/05-inventory-after.png), [post-restart opinion/appearance](evidence/2026-10-18-alife/06-restart-opinion.png), [post-restart inventory](evidence/2026-10-18-alife/07-restart-inventory.png). Raw action records/screenshots/logs/worlds stay ignored under runtime/.

Final cleanup: client Quit to Desktop/Yes and server quit both exited **0**, server listed zero players / Shutdown handling finished, no test UDP listeners; no forced termination. Diagnostics remain false. Offline after-state/logs at runtime/evidence/alife/jeem-after-restart; ModData SHA256 88f49f4ab33f0ad2f5f1211ccfa6bd144ccc52edc83b81ef742f4411a5a0d8c7. Before/after SQLite retains exactly one living Jamie row, same id/account/name; location changed with the observed walk. Final available RAM 18,668,152 KiB, no tracked live processes; host GPU aggregate 1,163 MiB. Controller left available. **60 automated checks**, seven complete catalog payload pins and 17 research seams checked; this is not capacity or general crash/duplication certification.

## Observed tooling issue and precautions

At 1600x900 the A-Life console Advanced overlay covered its controls and its toggle. Workaround: configure Save squad, close the entire console, reopen; spec persists, overlay is hidden. No upstream patch applied. Diagnostics must be enabled in Project A-Life client options to expose admin context controls; sandbox ShowAdminTools alone was insufficient. The UI explicitly warns diagnostics slow the game. Temporarily enabled for spawn, then disabled and confirmed in file/server log; no performance claim from diagnostic sessions.

Core resource sample: client PSS 8,570,624 KiB, server 4,349,403 KiB, available RAM 6,590,200 KiB, process swap zero; host GPU aggregate 2,066 MiB. Single sampled session, not a leak attribution, stable budget, FPS benchmark or 4–8-player capacity. Use fresh processes and one rendered client initially.

## Next discriminating checks / rollback

1. Ordinary-player contact/action permissions and one controlled negative consequence. Track settled score before saving; distinguish Jeem standing, NPC opinion and faction access. No repeated blind spawns/gifts or arbitrary admin score setting as gameplay proof.
2. Focused appearance/position-lock persistence comparison; then one hostile actor/damage and owning-client handoff if resource headroom permits. Check victim/actor/cause/dedupe rather than assuming every death is murder. Do not run broad upstream FullTest/siege tools uninspected.
3. Only after these seams: Viewpoint on a separate explicit composition, faction mapping, contextual player-kill attribution experiment. Keep Bandits/retained integrated world as rollback, not co-owner.

Stop disposable processes, retain worlds/logs, disable diagnostics; no world reset, live settings change, collection promotion, upstream publication or v1 acceptance waiver. Technical pins should not stop independent drop/mission source work. No immediate user action is required.

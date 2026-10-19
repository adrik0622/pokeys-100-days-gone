# v2 mod landscape and airdrop feasibility

Researched 2026-10-18 for native Linux client/dedicated **42.21.0 / 4a0e9546ec**, target 4–8 players. Decision context: [SC-002](SCOPE_CHANGES.md), [living-world concept and next three tasks](V2_LIVING_WORLD.md). This is a focused primary-source survey, not an exhaustive inventory or an accepted stack.

Evidence labels: **author-documented** = published claim/settings; **source-inspected** = actual specified code read; **runtime-observed** = our engine evidence. Newly found candidates are author-documented only unless stated otherwise. No new candidate downloaded/subscribed/enabled or added to the collection during this sweep. A Workshop page's generic “Subscribed,” removed/incompatible banners or MP tag is not proof of local subscription, removal or compatibility; use actual installation/owner evidence.

## Shortlist and disposition

| Capability / exact item | Useful controls or seams | Viability and decision |
| --- | --- | --- |
| [The Mission](https://steamcommunity.com/sharedfiles/filedetails/?id=3640172314), 3640172314 / TheMission42, mamalio | Admin live editor/authoring file; objective, target, reward, prerequisite, repeat, consume-items and marker controls; tracked character progress | Likely the requested “The Mission”; a mission-system mod, not a whole modpack. Author verifies 42.20.4 and advertises SP/MP/dedicated. **Trial candidate**, not verified on 42.21; faction/custom-event completion API unknown |
| [Random Zombies](https://steamcommunity.com/sharedfiles/filedetails/?id=2818577583), belette | Speed-type/toughness/cognition proportions and update frequency | Author FAQ explicitly retires it with 42.20.0. **Do not select the original for our current build** merely because it has B42 tags |
| [Random Zeds](https://steamcommunity.com/sharedfiles/filedetails/?id=3778522347), 3778522347 / RandomZeds, Daavy | Day/night/weather speed mixes, toughness/senses, per-type speed variation; developer exclusion flag | Author identifies B42.21; current MP tag and author discussion, but our dedicated/ownership acceptance absent. **Preferred randomization trial lead** after native settings; no automatic selection |
| [Save Our Station!](https://steamcommunity.com/sharedfiles/filedetails/?id=2398274461), 2398274461 / SaveOurStation_Core + SaveOurStation_KnoxCountry | AEBS faults/interruptions, reliability profiles, progression multiplier, grid-failure toggle; new station locations | Author still says B42 support planned without ETA, waiting on mapping/tooling. **Watchlist/reference**, not a verified released B42 dependency |
| [Horde Nights](https://steamcommunity.com/sharedfiles/filedetails/?id=3782615002), installed 1.1.3 / HordeNights | Existing post-horde drop queue, proximity crate creation, markers, Bandits guard path and sandbox controls | **Source-inspected** and existing physical horde candidate. Drops/guards have NOT been runtime-tested here; currently disabled in our profiles. Detailed findings below |
| [Project A-Life](https://steamcommunity.com/workshop/filedetails/?id=3803984183), 3803984183 / ProjectALifeNPCs | Persistent online/off-screen squads/factions, camps/outposts, radio, faction/NPC editor, population/encounter/raid tuning | Author explicitly supports 42.21 and SP/coop/MP. **High-value replacement-owner trial**, not an add-on to Bandits. Hook/health/network/save compatibility with our stack uninspected |
| [A-Life — Jeem Extension](https://steamcommunity.com/sharedfiles/filedetails/?id=3806944055), 3806944055 / ProjectALifeJimmy | Standing gains/losses, witnesses/rumors/fair blame, persistent crews/outposts, selectable features/base protections | Author documents 42.21+, A-Life dependency and MP. **Conditional second step** after A-Life alone; potential existing answer to much reputation/world logic. Do not adopt worker/recruitment scope automatically |
| [Military Drop — Radio Supply Airdrops](https://steamcommunity.com/sharedfiles/filedetails/?id=3811752923), 3811752923 / batman_MilitaryDrop | Request via radio, personal trust/requisition, zombie-guarded crates; linked public guide/source | Author targets 42.21/dedicated but says testing mostly SP. **Strong competing drop-owner candidate**; compare against existing path before custom request/trust/horde implementation |
| [Dynamic Trading (w/ NPC)](https://steamcommunity.com/workshop/filedetails/?id=3635333613), 3635333613 | DynamicTradingCommon + either DynamicTrading (radio) OR DynamicTradingV2 (physical NPC/factions); economic events/needs | Author warns V2 support with Bandits/other zombie-changing NPC mods is not guaranteed. **Reserve radio-only option** if a real trade gap remains; no extra physical owner/economy/stock market by default |
| [Reactive Sound Events](https://steamcommunity.com/sharedfiles/filedetails/?id=3656190498), 3656190498 | Reactive sounds, radio, scene and frequency tuning | Author names 42.15.2; dedicated testing pending and physical scenes SP-only. **Atmosphere watchlist**, not a demonstrated shared living-world encounter source |
| [Extensive Power Rework — Slapstick Fork](https://steamcommunity.com/sharedfiles/filedetails/?id=3775553383), 3775553383 / EPR_Slapstick | Town power/water restoration infrastructure; author labels 42.20, release 0.18.9 | **Later infrastructure trial lead**, not SOS/AEBS replacement. Exact 42.21/dedicated, generator/water effects, save changes and maintenance burden need inspection. Do not combine power owners/forks |
| [Neat Lockpicking](https://steamcommunity.com/sharedfiles/filedetails/?id=3783535220), 3783535220 / NeatLockpicking | Lockpick/crowbar/hotwire minigames; requires NeatUI | Author advertises B42 SP/MP, but hotwire replaces native action. **Optionality review first**; exact 42.21/Viewpoint/dedicated behavior unverified. Existing calibration already serves the first active-play need |

These are alternatives by responsibility, not a proposed Subscribe All list. Follow-on [SC-003](SCOPE_CHANGES.md) authorized A-Life/Jeem download and isolated trials with Bandits OFF; [actual source/runtime findings](V2-01-alife-jeem.md) supersede the original survey-only status for those two items. Bandits remains the owner only in retained v1 fixtures; never combine both owners. Prior leader/Screamer findings remain in [SC-001](SCOPE_CHANGES.md) and [audit](M4-optional-screamer.md); this survey does not reinstate them.

## What the named candidates actually buy us

### The Mission: objective/UI infrastructure, not demonstrated faction politics

Author documentation includes kill, walking, collection, survival and restock-style objectives, direct inventory rewards and persistent synchronized character progress. That can supply authoring/tracking; it does not establish shared campaign contracts, faction affinity, NPC kill recognition, contested-drop delivery or server-trusted external completion.

Inspect the authoring schema/permissions and completion/reward handlers first. Disable irrelevant default grind goals if supported; do not infer a public Lua callback or zero-item reward from editor prose. Choose one completion/reward authority. A contract should change the world, not reward jogging or create a second payout for an existing favor. Author requests contact for derivatives; public description is not a redistribution license. Changelog endpoints were unavailable through the browser during this sweep; no changelog/source audit claimed. If this is not the item intended, substitute the user's link without blocking other work.

### Zombie variety: native options, then one randomizer

Installed native English Sandbox.json exposes Random Speed / Random Sprinter Amount, including a custom percentage under Advanced. That is a real built-in configuration lead, not a new mod requirement; we did not run a native distribution experiment this sweep.

Random Zeds adds conditional profiles beyond a single native percentage. Its documented exclusion is zombie mod-data RandomZedsExcluded=true. Its optional Synapse API adds more cognition/strength/memory/sense control. [Synapse](https://steamcommunity.com/sharedfiles/filedetails/?id=3793697487) is a Java dependency with additional required-items entries; its server instructions recommend allow-all. **Do not copy that trust-policy change**: first try without Synapse; inspect/pin individual JAR approvals only if a necessary feature justifies them.

Author comments report an MP/SP Mod-ID merge and a Linux-specific fix not locally tested by the author. Recheck actual Mod ID, case-sensitive paths and server-owned attribute behavior. Require NPC-body exclusions and a decision for event zombies: if the randomizer owns ambient types, Horde Nights must not fight it over sprinter attributes. Verify on spawn, ownership transfer, unload and restart. More variety is not permission for unpredictable/untelegraphed instant-death difficulty.

Legacy Day/Night forks are not interchangeable with this item: [3627218054](https://steamcommunity.com/sharedfiles/filedetails/?id=3627218054) says it is a folder-structure port tested briefly on 42.13 MP with no future bugfix commitment; [3700850342](https://steamcommunity.com/sharedfiles/filedetails/?id=3700850342) labels 42.17 and only SP testing. Neither is our preferred 42.21 path.

### Save Our Station: excellent design reference, blocked dependency

Its loop is credible infrastructure failure → expedition/repair → restored useful broadcasts. Documented controls let outages be rare/recoverable rather than compulsory chores. The [author FAQ](https://steamcommunity.com/workshop/filedetails/discussion/2398274461/3785877016599439689/) says new station map areas require a fresh world; don't insert them into our retained fixtures. [Author compatibility notes](https://steamcommunity.com/workshop/filedetails/discussion/2398274461/3785877016600078243/) do not guarantee interoperability with AEBS-altering mods.

No verified released B42 port found. Do not downgrade the project, copy its assets or wait idle. A bounded original relay condition/repair at an existing location can deliver the campaign loop if needed; native AEBS integration remains a separate hook investigation. Keep baseline forecast/contact access available through a fallback.

### A-Life/Jeem: investigate before rebuilding society ourselves

A-Life's author claims off-screen squads traveling roads, persistent casualties/memories, outposts, radios, territory and an editable faction roster. It exposes ProjectALifeOwned=true as the NPC-body exclusion marker and advises one NPC mod per save. Population/encounter/raid controls are advertised; exact keys and integration hooks need payload inspection.

Its page headline and [Oct 17 changelog](https://steamcommunity.com/sharedfiles/filedetails/changelog/3803984183) identify 1.4.5, while a prose field still says 1.4.3. Pin actual files, not that inconsistent label. Recent notes address NPC armor wear, unload cleanup and ownership-related behavior; fixes are author claims, not our acceptance.

Jeem advertises standing gains/losses, witnesses returning home, rumor spread, accident handling, persistent crews and selectable features. This is much closer to our goal than assuming every missing behavior must be custom. SC-003 corrects our earlier anti-PK inference: there is no anti-player-killing policy; witness concealment should be assessed for coherent consequences, not rejected as a deterrence loophole. Raid/base behavior still needs explicit protection rules. Its A-Life 1.4 overlap handling needs inspection to prevent duplicate systems. Start without recruits/workers and enable only required modules. No verified public project-reputation API, licenses or exact-stack runtime result yet; do not promise player-kill politics from this description.

### Military Drop: an unusually close fit, with important unknowns

Published features include radio requisitions, personal trust, budget tiers, lost/stolen-drop consequences, announced distant crates, zombie guards and a decoy. These are strong reasons to evaluate reuse before implementing the same systems.

The [admin guide](https://github.com/cyberbobjr/BATMAN_EHE_MILITARY_DROP/blob/main/docs/guide/en/06-server-admin.md) documents CooldownHours, DropMinDistance/DropMaxDistance, MinZombies/MaxZombies, TrustDailyCap, TrustErosion, TrustDropLostHours, RequisitionBudget, RequisitionTier2/3 and DecoyEnabled. Cooldown is server-wide with a caller-trust modifier. Requisition lots have configurable tier/cost/count/filters; the file is shared by saves/servers under that runtime account, so isolate it before experimentation.

The required-items panel lists Signal Smoke, Belt Walkie-Talkie and Tooltiplib; prose describes Smoke as optional and also contains an outdated “no other mod required” line. Resolve actual mod.info dependencies. Do not treat the author's general server-authoritative claim as proof of the trust boundary or four-client correctness.

The linked [author repository](https://github.com/cyberbobjr/BATMAN_EHE_MILITARY_DROP) carries an MIT license and simulated-API tests. Only README/license metadata and guide were read, not Lua implementation or test execution. Snapshot/pin exact code before depending on it. Multi-faction integration, armed NPC guards, reward ownership and aggregate zombie accounting remain gaps to inspect, not known available hooks. If chosen, disable overlapping drop fulfillment and account for all spawned pressure; it need not replace Horde Nights' recurring migration role.

## Installed Horde Nights airdrops: concrete source findings

Read-only inspection of the actual 1.1.3 payload, not a Workshop inference. Root:

/home/adrikingston/.local/share/Steam/steamapps/workshop/content/108600/3782615002/mods/HordeNights/42

Files: media/lua/server/HordeNights/HordeSupplyDrop.lua, HordeManager.lua and HordeSpawner.lua; media/lua/client/HordeNights/HordeBanditIntegration.lua; media/sandbox-options.txt. New seam hashes are in [research.json](../config/research.json); existing full-payload pin remains unchanged. No upstream code/assets copied into this repository.

| User question | What already exists in this payload | Missing/next evidence |
| --- | --- | --- |
| Can armed NPCs contest drops? | Optional guard roll; client integration requests hostile 12_Militia clan through Bandits Spawner.Clan, Defend program. Original clan definitions include firearms | Source supports the concept; actual dedicated spawn/weapon/damage/ownership not tested. Not tied to our faction standing; hardcoded Bandits path does not support an A-Life switch |
| Can we put a horde at a drop? | Crate and guard path do not create a zombie horde. HordeManager.start selects an online player group and follows its center, not a requested fixed drop coordinate | Feasible design via existing-zombie attraction or a bounded owner extension; no verified drop-horde setting. Do not call start and rewrite its shared state to hijack the campaign |
| Can reputation buy/request a drop? | Callable Lua seam HordeSupplyDrop.queue(state, source, targetUsernames, force), then tryCreate; targeted users, logical drop IDs and pending state | No faction eligibility/cost/cooldown or ordinary-player request in this path. Original server-side authorization adapter needed if using this owner; callable internal function is NOT a guaranteed supported API |
| Can we choose faction-specific contents? | POST_HORDE gives combat resupply; HELICOPTER_RANDOM chooses weighted shipment types including medicine/engineering/rare weapons | queue has no arbitrary payload/faction/coordinate argument. Other source names still select combat resupply. Fine-grained contents/shipments require an actual hook/add-on or permissioned patch; not just setting a medical source string |
| Does looting affect affinity? | Tagged crate, stable logical drop ID, empty-container detection and marker removal | “Claimed” is container empty, not actor attribution, partial withdrawal or completed delivery. Build/verify ownership evidence before tying it to rep |

### Exact sandbox knobs (prefix HordeNights.)

| Key | Declared range / upstream default | Caution |
| --- | --- | --- |
| SupplyDropsEnabled | boolean / true | Post-horde path; our trials explicitly false |
| SupplyDropMinimumDistance / SupplyDropMaximumDistance | 10–500 / 100; 10–1000 / 300 tiles | Chosen around target survivors; not faction drop-zone selection |
| SupplyDropScaling | 0.25–3.0 / 1.0 | Loot code also has hard minima; scaling alone does not allow arbitrary low-value contracts |
| SupplyDropExpiryDays | 1–30 / 3 | In inspected minute handler this expires pending unmaterialized drops, not every created crate |
| HelicopterSupplyDropsEnabled / HelicopterSupplyDropChance | boolean / false; 0–100 / 25 | Detector returns unavailable on non-debug dedicated; do not promise automatic vanilla-helicopter drops there |
| SupplyDropBanditsEnabled / SupplyDropBanditChance | boolean / true; 0–100 / 35 | Rare-weapons/military shipment logic imposes at least 75/50% guard chance when enabled; chance=0 alone is not a global disable |
| SupplyDropBanditMinimum / SupplyDropBanditMaximum | 1–4 / 2; 1–4 / 4 | Source roll also clamps both to at most four; these are upstream limits, not measured performance-safe counts |
| SupplyDropBanditScaling | 0–3.0 / 1.0 | Uses target count and survived-event progression, bounded by effective min/max |

queue permits one pending drop, archives already materialized unclaimed drops, increments a persistent sequence and announces a marker. force=true can replace pending state; use only role-checked admin recovery, never ordinary faction requests. Crates materialize when a targeted survivor is within 45 tiles, outdoors on a free square, with up to 15 tiles of placement adjustment. No proof they remain outside every observer's line of sight.

Guard spawn points are 5–12 tiles from the crate. Server saves “dispatched” before messaging one nearest client; the client sends a Bandits spawn request and an acknowledgment, with local/player handled-ID tracking and a shared-state fallback. The acknowledgment handler marks confirmation by drop ID, not observed NPC creation. Disconnect/failure can leave uncertainty; cross-client fallback races and forged/premature acknowledgment need inspection/tests. Do not claim duplicate prevention or reliable guard bodies solely from these flags.

Materialized unclaimed drops are archived until their loaded crate is empty; no bounded all-created-crate expiry was established. Test lost/destroyed/unloaded crates and avoid accumulating permanent logical entries in an endless server. Post-horde combat loot has hard minima (including six ammo-box rolls); rewards must be tuned against renewable loot/guard weapon farming rather than assuming a low scaling slider solves balance.

### NPC death/affinity seam

Read actual Bandits/42.21 client BanditUpdate.lua OnZombieDead and server BanditServerSpawner.lua: brain.cid/clan link to the clan; death uses getAttackedBy, adjusts a local player's zombie-kill count, and removes the brain through a client command. Useful discovery, **not trustworthy server-side killer/faction authority**. NPC bodies use zombie machinery, so generic zombie-kill mission counters/randomizers need filtering before integration. Preserve IDs/affiliation before deprovisioning and verify target type, delayed deaths, deduplication and client handoff. No confirmed universal PvP-death attribution hook was established this sweep.

## Build/configure/custom recommendation

Evaluate **A-Life alone → Jeem only if necessary** for persistent factions before writing custom NPC state; evaluate **Military Drop vs current Horde Nights drops** before writing request/trust/horde mechanics; inspect **The Mission** for content/tracking without a parallel payout engine. Keep **Random Zeds** as optional ambient variety after owner exclusions; defer SOS dependency until an actual supported port exists.

Likely project-owned gaps even if the candidates work: our faction identities/values and authored needs; a readable choice-to-world-condition loop; project-specific multi-faction crime/gray-faction policy and anti-farming; mapping one owner's standing/drop outcomes into another's contracts; optional minigame incentives; offline protection and shared population/reward budgets. Exact code boundary depends on source spikes—do not prebuild a second AI, economy, reputation or generic quest framework.

If reuse proves more expensive or less reliable, a bounded custom campaign/relay/drop adapter is explicitly allowed by SC-002. The next work is the three cards in V2_LIVING_WORLD, not deployment of all rows. Public licenses vary: reference upstream dependencies by default; verify terms/permission before any fork, copied source/assets or derivative release. No author contact or public publication was performed.

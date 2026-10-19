# V2-02 — supply / contracts / variety investigation

2026-10-18/19, SC-004 unattended sweep. Development experiments, not release acceptance. Original Workshop references only; no upstream code/assets republished.

## Decisions before runtime

- Prefer Military Drop 0.5.4 as the **single requested-drop owner** over Horde Nights' hardcoded Bandits-guard branch. Keep Horde Nights drops OFF. A-Life is the NPC owner; no mixed Bandits world.
- Exact metadata chain: Military Drop `batman_MilitaryDrop` → Belt Walkie-Talkie `batman_BeltRadio` 1.2.0 → TooltipLib 1.7.0. Subscribe individually. Signal Smoke appears in the Workshop required-items UI but is optional in actual Lua/metadata; not installed for this trial.
- Army logistics trust is **per character**, held privately by Military Drop, 0–100/start 25. It is not Jeem faction standing or a player-group score. First opening of a tagged case resolves recovery: requester +10, requester's vanilla player faction teammate +5, unrelated opener −5 to requester, expired delivery −10. "Faction" here means the vanilla player faction, **not A-Life NPC factions**. These inspected paths are not yet engine-observed.
- Ordinary request revalidates the actual equipped/nearby military radio, on/off/channel, auth code, cooldown and line-cut trust on the server. Admin force bypasses this and will not certify it. Case attribution and death/new-character handling need runtime checks. Native drop zombies are new births; no strict global budget accounting found. First fixture deliberately sets both counts to zero.
- The Mission has server inventory consumption, reward claims, duplicate/cooldown checks and role-checked live authoring. **Walking progress can come from client snapshots; kill handler lacks A-Life-shell exclusion.** Gather-only isolated trial; no walking/kill/survival reward categories or automatic seven-day reset. No blanket permission to fork its code.
- Random Zeds 1.4.3 is the current B42.21 candidate, not retired Random Zombies. Its `RandomZedsExcluded` API exists but it does not detect `ProjectALifeUID`. No combined enabling before an original exclusion seam is tested. Synapse is optional and is not installed/authorized via a generic Java policy change.

## Fixed fixtures

`supply-trial`: separate world/cache, loopback 19790/19791, ordinary `pokeys_supply_a`; only three supply dependencies. Frequency 900 MHz/auth disabled and 40–60 tile delivery are **test aids, not intended gameplay**. Six-hour base cooldown, budget 25, no explosives/decoy/crashes, no ambient/drop zombies. Finite native admin supplies: one military walkie and one battery. Actual inventory/UI evidence required.

`mission-trial`: separate world/cache, loopback 19780/19781, ordinary `pokeys_mission_a`; only TheMission42. Gather categories only, no reset. Two bandages supplied only if needed; do not call that an earned survival resource. Preserve all prior worlds. No Java loader or presentation mods in either.

## Sources

[Military Drop](https://steamcommunity.com/sharedfiles/filedetails/?id=3811752923), [author admin guide](https://github.com/cyberbobjr/BATMAN_EHE_MILITARY_DROP/blob/main/docs/guide/en/06-server-admin.md), [Belt Radio](https://steamcommunity.com/sharedfiles/filedetails/?id=3817018338), [TooltipLib](https://steamcommunity.com/sharedfiles/filedetails/?id=3694097672), [The Mission](https://steamcommunity.com/sharedfiles/filedetails/?id=3640172314), [Random Zeds](https://steamcommunity.com/sharedfiles/filedetails/?id=3778522347).

Installed source/payload fingerprints are recorded in `config/modpack.json`. Module observations above derive from the downloaded pinned server/shared Lua, not solely Workshop advertising. Runtime results follow in subsequent entries.

Exact declared settings: [searchable HTML](V2_SETTINGS.html), [CSV with source hashes](V2_SETTINGS.csv), generated with `python3 scripts/settings_catalog.py`. 1,091 declarations across nine inputs; defaults are not effective preset values or release tuning. Viewpoint/loader/assets have other configuration surfaces, covered in the illustrated report.

Early runtime clarification: `RequisitionBudget=25` is a percentage, not 25 spendable points. Starting trust produced **2 points**, spent on one medical lot through the ordinary native form. First supply command ran before the player completed login and explicitly returned `No such user` twice; only repeated after native `players` confirmed the account. Second command succeeded; inventory showed one walkie and one spare battery. No replay after ambiguous fulfillment.

## Observed dedicated supply loop

Clean local source `f2c23ee` (later docs/catalogue-only `5451797`), original pinned dependencies; server/client 272692/272759. Ordinary `pokeys_supply_a` / **Morgan Supply** created, no admin role/force/teleport. Native device panel: equipped walkie, switched on, added/tuned 900 MHz preset. Native request → authorized form, 2 points → one medical lot. Tier-II items required trust 50, tier III 75; explosives forbidden by fixture. Server started flight D1 toward 7939/11740 and logged one requisition case in a physical crate with **zero zombies**. Radio announced the coordinates.

Walked/climbed ordinary fences to the road. Visible crate and native Trailer inventory held exactly **Requisition Case: Medical**. Took case (trunk 3/80 → 0/80), opened via native timed action. Inventory gained **Alcohol Wipes, Cold Pack, Surgical Gloves** and lost the case. Server recorded **trust 25 → 35**, D1 recovered by the requesting account. Subsequent ordinary request was server-refused `cooldown`; no second delivery. This is actual inventory/consequence evidence, not just an acknowledgement.

Both processes exited 0; zero test listeners. Offline checkpoint `runtime/evidence/supply/first-clean-stop/`. Fresh processes 282238/282305, no restore or supplies/rewards replay: Morgan rejoined without creation beside the same crate, inventory retained all three medical items and spare battery, crate remained empty. **Exact post-restart trust 35 was not separately displayed/audited**, nor was death reset, third-party recovery, gunfire/crash, auth-code puzzle, horde/NPC contest, remote Steam or capacity tested. Do not extend this narrow clean-restart inventory result to those gates. Processes stopped again after observation; check status before next launch.

Selected screenshots: [form/choice](evidence/2026-10-19-v2/01-requisition.png), [physical case](evidence/2026-10-19-v2/02-physical-delivery.png), [opened reward](evidence/2026-10-19-v2/03-recovered-medical.png), [fresh restart](evidence/2026-10-19-v2/04-retained-inventory.png). Raw input/screenshots/logs/worlds remain ignored under runtime.

Additional source correction: The Mission's **server completed history resolves Steam ID then username**, with legacy-key migration (`TM42_Config.getHistoryKeyCandidates/resolveHistoryKey`), not necessarily per-character. Active progress lives on character modData. Do not equate its persistence identity with Military Drop's per-character trust or promise death resets.

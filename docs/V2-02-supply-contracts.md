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

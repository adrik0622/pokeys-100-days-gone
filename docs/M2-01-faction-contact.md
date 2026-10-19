# M2-01 — First faction-contact slice

Status 2026-10-18: **implemented, automated checks pass; engine check in progress**. Owner: agent. The user asked to park further A/B testing and implement scoped gameplay. This is an independent companion slice, not acceptance of full M1/M2 or a substitute for physical human encounters.

## Player-facing change

Right-click the world → **Pokeys: faction contacts**. The ledger shows three provisional, group-wide faction identities: neutral Rosewood Mutual Aid, allied Field Observers, hostile Road Reclaimers. These are campaign contact records, **not spawned NPCs or altered NPC hostility**.

At the previously observed Rosewood house `(7990,11756,0)`, within four tiles, donate **two non-favorite clean `Base.Bandage` items from the main inventory**. This changes Mutual Aid standing from 0/Neutral to +20/Allied and unlocks a concrete interaction: request one `Base.Disinfectant`. The favor repeats after 24 world hours; assistance has a separate 48-world-hour **group-wide** cooldown, not one payout per player. Values/names/contact location are prototype content, not accepted release balance or authored day-100 history. Dirty/favorite bandages and nested bags are excluded deliberately.

The contact is a simple drop-point abstraction: no building claim, physical camp, radio-equipment requirement or continuous NPC simulation is implied. No forecast is fabricated before a real event owner exists. No faction market/surplus/shortage economy, custom firearm or horde system was added.

## Why a small add-on

No currently included presentation dependency supplies our campaign standing/favor logic. Installed `Faction.class` exposes player-clan membership/ownership/tags; it does not establish the requested narrative standing system. On 2026-10-18, [Bandits' author description](https://steamcommunity.com/sharedfiles/filedetails/?id=3268487204) describes friendly/hostile encounters and customization; [Kane's description](https://steamcommunity.com/sharedfiles/filedetails/?id=3594821036) describes time-based NPC profiles. Neither description establishes persistent, player-driven group reputation. Their source was **not inspected**, and absence from a description is not proof that no extension exists. They remain separate candidates for physical encounters, not dependencies of this slice.

Smallest change: our own Lua table, two server-owned actions, a read-only client ledger and narrowly checked admin controls. Existing engine hooks handle persistence/networking/inventory. Original code is under `mods/Pokeys100DaysGone/`, Mod ID `Pokeys100DaysGone`, version 0.1.0. No upstream code/assets are copied, patched or reuploaded. No Workshop publication or collection membership change.

Installed 42.21.0 primary evidence used:

- `media/lua/server/Vehicles/ProfessionVehicles.lua:343`: `OnInitGlobalModData`; `server/Foraging/forageServer.lua:26`: `ModData.getOrCreate`.
- `server/ClientCommands.lua:215`: inventory removal + `sendRemoveItemFromContainer`; lines 217–218: adding + `sendAddItemToContainer`; line 477: player-targeted `sendServerCommand`.
- `client/Foraging/ISSearchManager.lua:1639`: world context-menu hook; `client/ISUI/ISContextMenu.lua:873`: target/callback convention.
- `client/ISUI/AdminPanel/ISUsersList.lua:511`: server role name API; the add-on restricts dev mutations to the default `admin` role, not a client flag or deprecated access-level string.
- `media/scripts/generated/items/normal.txt:8071,8283`: current Bandage/Disinfectant types. B42 Disinfectant uses a fluid component; the add-on creates the native item without inventing old drainable-item fields.

Paths above are relative to `runtime/server/install/`. Source inspection is not runtime verification.

## Authority, persistence and failure boundaries

Server derives identity, position, floor, alive state, inventory contents, current world age, standing and cooldown from engine/state. Clients send only action intent, never a trusted item count, reputation, payout or username. No map/zombie scans, tick handlers, external database, service or Java dependency.

`ModData` key `Pokeys100DaysGone.Campaign` holds schema 1, bounded standing, two cooldown deadlines, revision, and one last-operation record. Unknown schemas or malformed records fail closed without resetting the world. Reconnects request a fresh limited snapshot. Snapshots exclude mutable persistent references, username and operation details.

Inventory changes are preceded by a reserved cooldown and a pending-operation latch. Ordinary retries and a different player cannot receive a second payout. If an engine inventory/sync call fails, further actions stay locked for inspection, including across a saved/reloaded pending state. **Do not blindly clear this latch or replay an inventory operation.** Inspect the server log's `[PokeysCampaign] INVENTORY INCIDENT` and that actor's actual inventory; retain an offline backup and reconcile deliberately. Admin cooldown reset refuses while locked.

Engine inventory and global campaign data are **not an atomic storage transaction**. Power loss or uneven save timing is not covered by the retry tests; hard-crash duplication/recovery remains unverified. No crash-safe exactly-once claim is made. World-time cooldowns do not run from wall-clock time; fixture `PauseEmpty=true` prevents empty-server progression. Cooldown countdown labels are snapshots; use Refresh to update them.

## Development controls / isolated deployment

Controller `campaign` client/server profiles stage only a symlink to our project-owned mod under their own caches. Existing directories are not overwritten. Server `runtime/server/campaign/`, `pokeys-m0-campaign`, loopback ports 19880/19881, Public/UPnP off; separate safe sandbox copied from the zombie-free network fixture. No Viewpoint/NPC/horde mod is loaded. This isolates Lua errors; it does not certify presentation compatibility.

```bash
python3 scripts/desktop_control.py request '{"action":"server_launch","profile":"campaign"}'
python3 scripts/desktop_control.py request '{"action":"launch","profile":"campaign","client":"a"}'
```

Join with fixture account **pokeys_campaign_a**. Once online, the fixed `server_campaign_supplies` controller action uses the game's existing `additem pokeys_campaign_a Base.Bandage 2` command. This is test gear, not a gameplay reward; it is refused on any other profile. Existing `save`/`players`/`quit` commands remain unchanged. Backup/restore helpers are still vanilla-only and refuse campaign/dual.

Admins see three DEV buttons: set Mutual Aid to Allied, reset favor cooldown, reset aid cooldown. Server validates role and explicit operation/faction/value bounds. No arbitrary console/code execution or whole-state replacement endpoint.

## Smallest useful test (one client now; A/B later)

1. Fresh isolated server/client: confirm mod loads with `[PokeysCampaign] loaded schema=1`, no mod Lua exception. Open contacts; verify 0/25/-50 and locked aid.
2. At the fixed contact, attempt delivery without bandages: server refuses and state stays unchanged. Supply two test bandages; deliver. Expect both removed, +20/Allied, aid unlocked.
3. Request assistance: exactly one native disinfectant appears. Refresh/retry must leave item count/standing unchanged with remaining cooldowns shown. Walk away/upstairs: mutation is refused (automated boundary test initially).
4. Reconnect or cleanly restart/rejoin, reopen ledger: same standing/cooldowns and item ownership. This is new-feature persistence evidence, not a repeat of M0-04. Shared A/B UI observation and concurrent requests remain deferred with that test.
5. Quit client and server normally, verify exits 0. Preserve logs and selected screenshot. Never overwrite the earlier vanilla/dual fixtures.

Automated: `python3 -m unittest discover -s tests -v` runs Lua 5.1 syntax and the **actual Lua rules/server adapter** against a small engine boundary. Covers cooldown edges, cross-player retries, inventory filtering/sync, admin rejection, saved-state-shaped reload, unknown schema, partial failure and snapshot isolation. It is not an engine/network/save-to-disk test.

Rollback: stop the campaign fixture; omit Mod ID `Pokeys100DaysGone` and retain its runtime world for diagnosis. No main game files/settings or upstream payload changes to undo. Next: verify the contact in engine, then connect standing/contacts to an inspected physical encounter owner and real forecast owner without waiving M1/M2/M3 gates.

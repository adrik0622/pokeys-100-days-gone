package.path = "mods/Pokeys100DaysGone/42/media/lua/shared/?.lua;" ..
    "mods/Pokeys100DaysGone/42/media/lua/server/?.lua;" .. package.path

function isServer() return true end
local callbacks = {}
Events = {}
for _, name in ipairs({"OnInitGlobalModData", "OnServerStarted", "OnClientCommand", "EveryOneMinute"}) do
    Events[name] = {Add=function(fn) callbacks[name] = fn end}
end
local store, sent, now, worldHour = {}, {}, 1000, 10
function getTimestampMs() return now end
function getGameTime() return {getWorldAgeHours=function() return worldHour end} end
function sendServerCommand(...) sent[#sent+1] = {...} end
local failContainerSync = false
function sendAddItemToContainer(_, item)
    assert(item and item.fullType == "Base.Disinfectant")
    if failContainerSync then error("injected container-sync failure") end
end
SandboxVars = {PokeysV2={Enabled=true}}

local history = {}
TM42 = {GlobalHistoryKey="TheMission42.History", CustomMissionDefs={},
    rebuildMissionRegistry=function() return true end,
    isMissionReady=function() return true end,
    getHistoryKey=function(player) return player.account end}
ModData = {
    getOrCreate=function(key) store[key] = store[key] or {}; return store[key] end,
    get=function(key) return key == TM42.GlobalHistoryKey and history or store[key] end,
}

local effects = {standing={}, repairs=0, inventory=0}
ProjectALifeJimmy = {enabled=function(name) return name == "standing" end,
    playerKey=function(player) return "account:" .. player.account end,
    Standing={rate=function() return 1.5 end, add=function(key, faction, delta, deed)
        assert(faction == "alife_county_ems" and deed.kind == "pokeys_medical_relief")
        local before = effects.standing[key] or 0
        effects.standing[key] = before + delta
        return before, effects.standing[key]
    end},
    StandingService={labelFor=function() return "friendly" end,
        points=function(key) return effects.standing[key] or 0 end}}

local Observer = require "Pokeys/MigrationServer"
local oldRepair = Observer.repair
Observer.repair = function() effects.repairs = effects.repairs + 1 end
local Server = require "Pokeys/V2Server"
callbacks.OnInitGlobalModData()
callbacks.OnServerStarted()
assert(TM42.CustomMissionDefs[1].id == "pokeys_medical_relief_01")

local player = {account="steam:fixture-1", username="fixture", x=7990, y=11756, z=0, dead=false}
function player:getUsername() return self.username end
function player:getX() return self.x end
function player:getY() return self.y end
function player:getZ() return self.z end
function player:isDead() return self.dead end
function player:getInventory() return {AddItem=function(_, fullType)
    effects.inventory = effects.inventory + 1
    return {fullType=fullType}
end} end
local function command(name, args)
    now = now + 600
    Server.command("PokeysV2", name, player, args or {})
    return sent[#sent][4]
end

-- A client cannot assert completion; server history is the sole proof.
local state = command("state", {completed=true, mission="pokeys_medical_relief_01",
    account="steam:forged-account", reward="Base.Axe", count=999}).state
assert(not state.completed and state.credit == "not credited" and (effects.standing["account:" .. player.account] or 0) == 0)
local sentCount = #sent
Server.command("OtherModule", "state", player, {completed=true})
Server.command("PokeysV2", "complete", player, {mission="pokeys_medical_relief_01"})
assert(#sent == sentCount and store["Pokeys100DaysGone.V2Bridge"].grants[player.account] == nil)
player.x = 8010
assert(not TM42.isMissionReady(player, TM42.CustomMissionDefs[1], {}))
player.x = 7990
assert(TM42.isMissionReady(player, TM42.CustomMissionDefs[1], {}))
history[player.account] = {completed={pokeys_medical_relief_01=true}}
state = command("state").state
assert(state.completed and state.credit == "applied" and state.delta == 1.5)
assert(effects.standing["account:" .. player.account] == 1.5 and effects.repairs == 1)
assert(store["Pokeys100DaysGone.V2Bridge"].grants[player.account].status == "applied")
state = command("state").state
assert(state.credit == "applied" and effects.standing["account:" .. player.account] == 1.5 and effects.repairs == 1)

-- Reopening the durable bridge and replaying a server check cannot duplicate credit.
callbacks.OnInitGlobalModData()
assert(store["Pokeys100DaysGone.V2Bridge"].grants[player.account].status == "applied")
Server.credit(player)
assert(effects.standing["account:" .. player.account] == 1.5 and effects.repairs == 1)

-- Successful aid adds one item and installs the shared cooldown; repeats do not add.
assert(command("aid", {item="Base.Axe", count=999, account="steam:other"}).code == "aid_received")
assert(effects.inventory == 1 and effects.standing["account:" .. player.account] == 1.5 and effects.repairs == 1)
assert(command("aid").code == "shared_aid_cooldown")
assert(effects.inventory == 1)

-- A different completed account shares the relay's world-wide aid cooldown.
local second = {account="steam:fixture-second", username="second", x=7990, y=11756, z=0}
function second:getUsername() return self.username end
function second:getX() return self.x end
function second:getY() return self.y end
function second:getZ() return self.z end
function second:isDead() return false end
function second:getInventory() return {AddItem=function(_, fullType)
    effects.inventory = effects.inventory + 1
    return {fullType=fullType}
end} end
history[second.account] = {completed={pokeys_medical_relief_01=true}}
Server.credit(second)
now = now + 600
Server.command("PokeysV2", "aid", second, {})
assert(sent[#sent][4].code == "shared_aid_cooldown" and effects.inventory == 1)

-- Native completion waits for Jeem; it does not invent or mirror a standing balance.
local jeem = ProjectALifeJimmy
local deferred = {account="steam:fixture-deferred", username="deferred", x=7990, y=11756, z=0}
history[deferred.account] = {completed={pokeys_medical_relief_01=true}}
ProjectALifeJimmy = nil
Server.credit(deferred)
assert(store["Pokeys100DaysGone.V2Bridge"].grants[deferred.account] == nil)
ProjectALifeJimmy = jeem
Server.credit(deferred)
assert(store["Pokeys100DaysGone.V2Bridge"].grants[deferred.account].status == "applied")
assert(effects.standing["account:" .. deferred.account] == 1.5)

-- If standing succeeds but recovery repair fails, an incident latch prevents a second delta.
local incident = {account="steam:fixture-incident", username="incident", x=7990, y=11756, z=0}
history[incident.account] = {completed={pokeys_medical_relief_01=true}}
local repair = Observer.repair
Observer.repair = function() error("injected recovery-owner failure") end
Server.credit(incident)
assert(store["Pokeys100DaysGone.V2Bridge"].grants[incident.account].status == "incident")
assert(effects.standing["account:" .. incident.account] == 1.5)
Observer.repair = repair
callbacks.OnInitGlobalModData()
Server.credit(incident)
assert(store["Pokeys100DaysGone.V2Bridge"].grants[incident.account].status == "incident")
assert(effects.standing["account:" .. incident.account] == 1.5)

-- A partial add followed by notification failure remains pending and never retries blindly.
local bad = {account="steam:fixture-2", username="fixture2", x=7990, y=11756, z=0}
for key, fn in pairs({getUsername=function(self) return self.username end,
    getX=function(self) return self.x end, getY=function(self) return self.y end,
    getZ=function(self) return self.z end, isDead=function() return false end}) do bad[key]=fn end
function bad:getInventory() return {AddItem=function(_, fullType)
    effects.inventory = effects.inventory + 1
    return {fullType=fullType}
end} end
history[bad.account] = {completed={pokeys_medical_relief_01=true}}
Server.credit(bad)
worldHour = 60 -- shared cooldown has elapsed for this separate injected-failure case
failContainerSync = true
now = now + 600
Server.command("PokeysV2", "aid", bad, {})
local failed = store["Pokeys100DaysGone.V2Bridge"]
local previousAid = failed.lastAid
assert(failed.aidPending and previousAid == 10)
assert(effects.inventory == 2) -- one server-side item exists before notification fails
callbacks.OnInitGlobalModData()
now = now + 600
Server.command("PokeysV2", "aid", bad, {})
assert(failed.aidPending and failed.lastAid == previousAid)
assert(effects.inventory == 2)

-- An invalid authenticated name is ignored instead of indexing the volatile throttle table with nil.
local unnamed = {getUsername=function() return nil end}
local sentBeforeUnnamed = #sent
Server.command("PokeysV2", "state", unnamed, {})
assert(#sent == sentBeforeUnnamed)

-- A broken upstream reputation-rate calculation must fail before mutating standing.
local invalidRate = {account="steam:fixture-invalid-rate", username="bad-rate", x=7990, y=11756, z=0}
history[invalidRate.account] = {completed={pokeys_medical_relief_01=true}}
local rate = ProjectALifeJimmy.Standing.rate
ProjectALifeJimmy.Standing.rate = function() return math.huge end
Server.credit(invalidRate)
ProjectALifeJimmy.Standing.rate = rate
assert(store["Pokeys100DaysGone.V2Bridge"].grants[invalidRate.account].status == "incident")
assert(effects.standing["account:" .. invalidRate.account] == nil)
Observer.repair = oldRepair

-- The feature is opt-in; malformed saved state stays untouched and cannot grant aid.
local registered = #TM42.CustomMissionDefs
SandboxVars.PokeysV2.Enabled = false
callbacks.OnInitGlobalModData()
local sentBeforeDisabled = #sent
Server.start()
Server.command("PokeysV2", "state", player, {})
assert(#sent == sentBeforeDisabled and effects.inventory == 2)
assert(#TM42.CustomMissionDefs == registered)

SandboxVars.PokeysV2.Enabled = true
local malformed = {schema=99, grants={}, revision=0}
store["Pokeys100DaysGone.V2Bridge"] = malformed
callbacks.OnInitGlobalModData()
now = now + 600
Server.command("PokeysV2", "state", player, {})
assert(sent[#sent][4].state.available == false)
assert(store["Pokeys100DaysGone.V2Bridge"] == malformed)
now = now + 600
Server.command("PokeysV2", "aid", player, {})
assert(effects.inventory == 2 and store["Pokeys100DaysGone.V2Bridge"] == malformed)
print("PASS: V2 server adapter trusts native history, credits once, and fail-closes partial credit/aid delivery")

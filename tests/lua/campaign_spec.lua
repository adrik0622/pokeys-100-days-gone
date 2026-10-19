local root = "mods/Pokeys100DaysGone/42/media/lua/"
package.path = root .. "shared/?.lua;" .. root .. "server/?.lua;" .. package.path
local C = require "Pokeys/Campaign"
-- Kahlua's runtime check caught next() being unavailable despite standard Lua.
next = nil
local function copy(value)
    if type(value) ~= "table" then return value end
    local out = {}
    for k, v in pairs(value) do out[k] = copy(v) end
    return out
end
local function denied(data, action, expected, hour, x, y, z, alive)
    local ok, code = C.allowed(data, action, hour or 100, x or 7990, y or 11756, z or 0,
        alive ~= false)
    assert(not ok and code == expected, tostring(code) .. " ~= " .. expected)
end

local data = C.open({})
assert(C.relationship(data.standing.mutualAid) == "Neutral")
assert(C.relationship(data.standing.observers) == "Allied")
assert(C.relationship(data.standing.reclaimers) == "Hostile")
assert(C.near(7994, 11756, 0) and not C.near(7994.01, 11756, 0))
assert(not C.near(7990, 11756, 1) and not C.near(0/0, 11756, 0))
denied(data, "donate", "too_far", 100, 8000)
denied(data, "donate", "not_alive", 100, nil, nil, nil, false)
denied(data, "aid", "aid_locked")
denied(data, "anything", "unknown_action")
denied(data, "donate", "clock_unavailable", math.huge)
assert(C.allowed(data, "donate", 100, 7990, 11756, 0, true))
C.reserve(data, "donate", 100, "alpha")
denied(data, "donate", "needs_admin_inspection")
assert(not C.admin(data, { operation = "resetCooldown", action = "donate" }))
assert(C.open(copy(data)).blocked) -- interrupted intent survives a serialized-state-shaped reload
C.finish(data, "donate")
assert(data.standing.mutualAid == 20 and C.relationship(data.standing.mutualAid) == "Allied")
denied(data, "donate", "favor_cooldown", 123.99)
assert(C.allowed(data, "donate", 124, 7990, 11756, 0, true))
assert(C.allowed(data, "aid", 100, 7990, 11756, 0, true))
C.reserve(data, "aid", 100, "bravo")
C.finish(data, "aid")
denied(data, "aid", "aid_cooldown", 147.99)
assert(C.allowed(data, "aid", 148, 7990, 11756, 0, true))
local reopened = C.open(copy(data))
denied(reopened, "donate", "favor_cooldown", 100)
denied(reopened, "aid", "aid_cooldown", 100)
local view = C.snapshot(data, 100)
view.standing.mutualAid = -100
assert(data.standing.mutualAid == 20 and view.lastAction == nil and view.username == nil)
for _, mutation in ipairs({
    function(d) d.schema = 2 end,
    function(d) d.standing.mutualAid = 0/0 end,
    function(d) d.nextFavorHour = "100" end,
    function(d) d.revision = -1 end,
}) do
    local broken = copy(data)
    mutation(broken)
    assert(not pcall(C.open, broken), "Invalid save must fail closed, not reset")
end
assert(not C.admin(data, {operation="setStanding", faction="mutualAid", value=math.huge}))
assert(not C.admin(data, {operation="setStanding", faction="newFaction", value=20}))
assert(not C.admin(data, {operation="setStanding", faction="mutualAid", value=2.5}))
assert(not C.admin(data, {operation="resetCooldown", action="anything"}))
assert(C.admin(data, {operation="setStanding", faction="mutualAid", value=95}))
C.reserve(data, "donate", 124, "alpha")
C.finish(data, "donate")
assert(data.standing.mutualAid == 100) -- bounded standing, no escalating payouts
print("PASS: campaign rules, cooldown boundaries, reload shape, fail-closed schema, snapshots")

-- Exercise the real server adapter with a minimal engine boundary, not a Python rewrite.
local store = {}
local sent, removed, added = {}, 0, 0
local hour = 100
local failRemove = false
local failAdd = false
local failSync = false
function isServer() return true end
local observerStore = {}
ModData = { getOrCreate = function(key)
    if key == "Pokeys100DaysGone.Observer" then return observerStore end
    assert(key == C.key); return store
end }
function getGameTime() return { getWorldAgeHours = function() return hour end } end
function sendServerCommand(...) sent[#sent + 1] = {...} end
function sendRemoveItemFromContainer() removed = removed + 1 end
function sendAddItemToContainer()
    if failSync then error("injected synchronization failure AFTER item creation") end
    added = added + 1
end
Events = {
    OnInitGlobalModData = { Add = function(f) assert(type(f) == "function") end },
    OnClientCommand = { Add = function(f) assert(type(f) == "function") end },
    EveryOneMinute = { Add = function(f) assert(type(f) == "function") end },
}
local function item(name, favorite)
    return {getFullType=function() return name end, isFavorite=function() return favorite or false end}
end
local function player(username, role)
    local p = { x=7990, y=11756, z=0, dead=false, items={} }
    local inv = {
        getItems = function()
            return { size = function() return #p.items end,
                get = function(_, i) return p.items[i + 1] end }
        end,
        Remove = function(_, target)
            if failRemove then error("injected inventory removal failure") end
            for i, v in ipairs(p.items) do
                if v == target then table.remove(p.items, i); return end
            end
            error("Missing item")
        end,
        AddItem = function(_, name)
            if failAdd then return nil end
            local value = item(name)
            p.items[#p.items + 1] = value
            return value
        end,
    }
    function p:getInventory() return inv end
    function p:getUsername() return username end
    function p:getRole() return {getName=function() return role or "player" end} end
    function p:getX() return self.x end
    function p:getY() return self.y end
    function p:getZ() return self.z end
    function p:isDead() return self.dead end
    return p
end
local S = require "Pokeys/CampaignServer"
require("Pokeys/MigrationServer").init()
S.init()
local a, b, admin = player("alpha"), player("bravo"), player("operator", "admin")
local function run(command, p, args)
    S.command(C.module, command, p, args or {})
    local result = sent[#sent]
    assert(result[1] == p and result[3] == "result")
    return result[4].code
end
assert(run("aid", a) == "aid_locked" and added == 0)
a.items = {item("Base.Bandage"), item("Base.BandageDirty"), item("Base.Bandage", true)}
assert(run("donate", a) == "need_two_bandages" and #a.items == 3)
a.items[4] = item("Base.Bandage")
a.x = 8000
assert(run("donate", a, {x=7990, standing=100}) == "too_far" and removed == 0)
a.x = 7990
assert(run("admin", a, {operation="setStanding",faction="mutualAid",value=100}) == "not_admin")
assert(store.standing.mutualAid == 0)
assert(run("donate", a, {username="operator",reward=10000}) == "donated")
assert(removed == 2 and #a.items == 2 and store.standing.mutualAid == 20)
assert(a.items[1]:getFullType() == "Base.BandageDirty" and a.items[2]:isFavorite())
assert(run("donate", b) == "favor_cooldown") -- shared, not per-player
assert(run("aid", b) == "aid_received" and added == 1)
assert(b.items[1]:getFullType() == "Base.Disinfectant")
assert(run("aid", a) == "aid_cooldown" and added == 1) -- no retry/alternate-player payout
store = copy(store)
S.init()
assert(run("aid", b) == "aid_cooldown" and added == 1)
assert(run("admin", admin, {operation="resetCooldown", action="aid"}) == "admin_changed")
assert(run("aid", a) == "aid_received" and added == 2)
hour = 148
failAdd = true
assert(run("aid", a) == "needs_admin_inspection" and store.blocked)
assert(run("aid", b) == "needs_admin_inspection" and added == 2)
assert(run("admin", admin, {operation="resetCooldown",action="aid"}) == "needs_admin_inspection")
store = copy(store)
S.init()
assert(run("aid", b) == "needs_admin_inspection")
store = {} -- separate fresh test fixture, not production recovery
S.init()
a.items = {item("Base.Bandage"),item("Base.Bandage")}
failRemove = true
assert(run("donate", a) == "needs_admin_inspection")
assert(store.standing.mutualAid == 0 and store.blocked)
store = {}
S.init()
failRemove, failAdd, failSync = false, false, true
b.items = {}
assert(run("admin", admin, {operation="setStanding", faction="mutualAid", value=20}) == "admin_changed")
assert(run("aid", b) == "needs_admin_inspection" and #b.items == 1)
assert(run("aid", b) == "needs_admin_inspection" and #b.items == 1)
store = copy(store)
S.init()
assert(run("aid", a) == "needs_admin_inspection" and #b.items == 1)
store = {}
failRemove, failAdd, failSync = false, false, false
S.init()
assert(run("admin", admin, {operation="setStanding", faction="mutualAid", value=20}) == "admin_changed")
observerStore.disruptedUntil = hour + 24
assert(run("aid", a) == "aid_disrupted")
a.items = {item("Base.Bandage"),item("Base.Bandage")}
assert(run("donate", a) == "donated")
assert(observerStore.disruptedUntil == hour + 12)
assert(run("aid", a) == "aid_disrupted")
hour = hour + 12
assert(run("aid", a) == "aid_received")
store = {schema=99}
S.init()
assert(run("donate", a) == "campaign_unavailable" and store.schema == 99)
print("PASS: server authority, item filtering/sync, cross-player retries, admin checks, partial failures")

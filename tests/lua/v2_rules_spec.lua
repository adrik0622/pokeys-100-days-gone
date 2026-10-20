local root = "mods/Pokeys100DaysGone/42/media/lua/"
package.path = root .. "shared/?.lua;" .. package.path
local V = require "Pokeys/V2Rules"

local d = V.open({})
assert(d.schema == 1 and d.revision == 0 and next(d.grants) == nil)
local player = {dead=false, x=7990, y=11756, z=0,
    isDead=function(self) return self.dead end,
    getX=function(self) return self.x end,
    getY=function(self) return self.y end,
    getZ=function(self) return self.z end}
assert(V.near(player))
player.x = 7998; assert(V.near(player)); player.x = 7998.01; assert(not V.near(player))
player.x = 7990; player.dead = true; assert(not V.near(player)); player.dead = false

assert(V.reserve(d, "steam:account-1", 12))
assert(not V.reserve(d, "steam:account-1", 13))
assert(not V.reserve(d, "", 12) and not V.reserve(d, string.rep("x", 161), 12))
assert(not V.reserve(d, "bad-clock", math.huge) and not V.reserve(d, "negative-clock", -1))
assert(d.grants["steam:account-1"].status == "pending")
d.grants["steam:account-1"].status = "applied"
d.lastAid = 0
local ok, reason = V.aidAllowed(d, "steam:account-1", 60, true, "friendly", false)
assert(ok, reason)
for _, args in ipairs({
    {d, "steam:account-1", 12, false, "friendly", false, "visit_relay_alive"},
    {d, "steam:account-1", 12, true, "neutral", false, "ems_not_friendly"},
    {d, "steam:account-1", 12, true, "allied", true, "relay_disrupted"},
    {d, "steam:account-1", 12, true, "allied", false, "shared_aid_cooldown"},
    {d, "missing", 12, true, "allied", false, "deliver_first"},
}) do
    local allowed, code = V.aidAllowed(args[1], args[2], args[3], args[4], args[5], args[6])
    assert(not allowed and code == args[7], tostring(code))
end
d.lastAid = 60
assert(not V.aidAllowed(d, "steam:account-1", 59, true, "allied", false)) -- clock rollback fails closed
assert(not V.aidAllowed(d, "steam:account-1", 107.99, true, "allied", false))
assert(V.aidAllowed(d, "steam:account-1", 108, true, "allied", false))
for _, status in ipairs({"pending", "incident"}) do
    d.grants["steam:account-1"].status = status
    local allowed, code = V.aidAllowed(d, "steam:account-1", 108, true, "allied", false)
    assert(not allowed and code == "inspection_required", "an ambiguous completed delivery must not ask for replay")
end
d.grants["steam:account-1"].status = "applied"

local reopened = V.open({schema=1, grants={ ["steam:account-1"]={status="applied",hours=12,delta=1.5} },
    revision=2, lastAid=60})
assert(not V.reserve(reopened, "steam:account-1", 200))
assert(not V.aidAllowed(reopened, "steam:account-1", 100, true, "allied", false))
for _, bad in ipairs({
    {schema=2, grants={}, revision=0},
    {schema=1, grants={x={status="unknown"}}, revision=0},
    {schema=1, grants={}, revision=0/0},
    {schema=1, grants={}, revision=-1},
    {schema=1, grants={x={status="pending"}}, revision=0},
    {schema=1, grants={x={status="pending",hours=0/0}}, revision=0},
    {schema=1, grants={x={status="applied",hours=2}}, revision=1},
    {schema=1, grants={x={status="applied",hours=2,delta=math.huge}}, revision=1},
    {schema=1, grants={[string.rep("x",161)]={status="pending",hours=2}}, revision=1},
    {schema=1, grants={}, revision=0, lastAid="yesterday"},
    {schema=1, grants={}, revision=0, aidPending={hours=1}},
    {schema=1, grants={}, revision=0, aidPending={hours=1,by=string.rep("x",65)}},
}) do assert(not pcall(V.open, bad), "invalid state must fail closed") end

local full = {schema=1, grants={}, revision=0}
for i=1,4096 do full.grants[tostring(i)]={status="applied",hours=0,delta=0} end
assert(not V.reserve(full, "too-many", 1)) -- no pruning can reopen a duplicate
print("PASS: V2 bridge pure rules, one-shot credit, aid gates, cooldown and fail-closed save")

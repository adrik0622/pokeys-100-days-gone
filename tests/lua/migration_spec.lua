package.path = "mods/Pokeys100DaysGone/42/media/lua/shared/?.lua;" ..
    "mods/Pokeys100DaysGone/42/media/lua/server/?.lua;" .. package.path
next = nil -- Kahlua boundary observed on installed engine.
local M = require "Pokeys/Migration"
local function copy(t)
    local r = {}; for k,v in pairs(t) do r[k] = type(v) == "table" and copy(v) or v end; return r
end
local d = M.open({})
local f = {id=0,start=120,active=false,completed=false,spawned=0,survived=0}
assert(not M.snapshot(d,nil,100).available)
assert(M.snapshot(d,f,100).earliest == 18 and M.snapshot(d,f,100).latest == 22)
assert(M.snapshot(d,f,100).direction == "UNRESOLVED")
assert(not M.begin(d,f,100,0,1,1,0,true,2))
assert(not M.begin(d,f,100,0,7990,11756,1,true,2))
local s = assert(M.begin(d,f,100,0,7990,11756,0,true,2))
assert(not M.step(s,f,3999,2,true,true) and s.step == 1)
assert(not M.step(s,f,4000,1,true,true))
assert(M.step(s,f,4000,2,true,true))
assert(not M.step(s,f,7999,2,true,true))
assert(M.step(s,f,8000,2,true,true))
assert(M.step(s,f,12000,2,true,true))
assert(not M.finish(d,s,f,14999,true,true))
assert(M.finish(d,s,f,15000,true,true))
assert(not M.finish(d,s,f,15000,true,true)) -- no duplicate completion
assert(not M.begin(d,f,100,16000,7990,11756,0,true,2))
d = M.open(copy(d))
assert(M.snapshot(d,f,100).earliest == 19.75 and M.snapshot(d,f,100).latest == 20.25)
f.start = 121
assert(not M.snapshot(d,f,100).calibrated) -- schedule change invalidates bonus/session
assert(not M.finish(d,s,f,15000,true,true))
local s2 = assert(M.begin(d,f,100,0,7990,11756,0,true,2))
assert(not M.step(s2,f,4000,2,false,true))
assert(not M.step(s2,f,4000,2,true,false))
assert(not M.step(s2,f,25001,2,true,true))
assert(not M.observe(d,f,100) and d.lastEvent == 0)
f.id,f.active,f.spawned = 1,true,4
assert(not M.observe(d,f,101))
f.active,f.completed,f.survived = false,true,1
assert(M.observe(d,f,102) and d.disruptedUntil == 126)
assert(not M.observe(d,f,103)) -- restart/retry cannot extend same aftermath
d = M.open(copy(d)); assert(not M.observe(d,f,103))
assert(M.repair(d,103) and d.disruptedUntil == 114)
assert(M.repair(d,103) and d.disruptedUntil == 103)
assert(not M.repair(d,103))
f.id = 2 -- Aborted event: CompletionRecorded true but survived counter unchanged.
assert(not M.observe(d,f,104) and d.disruptedUntil == 103)
assert(not pcall(M.open,{schema=99}))
print("PASS: observer rules, real-time bounds, cancel/expiry/distance, duplicate/restart, aftermath")

local store, sent, ms, hour = {}, {}, 100000, 100
function isServer() return true end
function getTimestampMs() return ms end
function getGameTime() return {getWorldAgeHours=function() return hour end} end
function ZombRand() return 1 end
ModData = {getOrCreate=function(key) assert(key==M.key); return store end}
function sendServerCommand(...) sent[#sent+1]={...} end
Events={}
for _,e in ipairs({"OnInitGlobalModData","OnClientCommand","EveryOneMinute"}) do
    Events[e]={Add=function(fn) assert(type(fn)=="function") end}
end
HordeSandbox={get=function() return true end}
HordeManager={state={CurrentHordeNightID=0,HordeNightActive=false,NightBudgetSpawned=0},
    nextStartWorldHour=function() return 120 end}
local S = require "Pokeys/MigrationServer"; S.init()
local p={x=7990,y=11756,z=0,dead=false}
function p:getUsername() return "actor" end
function p:getX() return self.x end
function p:getY() return self.y end
function p:getZ() return self.z end
function p:isDead() return self.dead end
local function run(command,args)
    S.command(M.module,command,p,args or {}); return sent[#sent][4]
end
assert(run("begin",{channel=3,started=0}).channel==2) -- client cannot pick challenge/time
assert(run("step",{channel=2}).code=="too_early")
for i=1,3 do ms=100000+i*4000; assert(run("step",{channel=2}).step==i+1) end
ms=115000; assert(run("finish").code=="calibrated")
assert(run("finish").code=="interrupted")
assert(run("begin").code=="cooldown")
S.init(); assert(run("finish").code=="interrupted") -- transient session lost, bonus persists
assert(run("state").state.calibrated)
S.minute() -- establish owner baseline
HordeManager.state.CurrentHordeNightID=1
HordeManager.state.NightBudgetSpawned=4
HordeManager.state.CompletionRecorded=true
HordeManager.state.HordeNightsSurvived=1
S.minute(); assert(S.aidBlocked())
assert(S.disruptionHours()==24)
assert(S.repair()==true); assert(store.disruptedUntil==112 and S.disruptionHours()==12)
assert(S.repair()==true and S.disruptionHours()==0)
assert(S.repair()==false) -- no-op is distinct from unavailable state
HordeManager=nil; assert(not run("state").state.available) -- never synthesize owner
print("PASS: observer server adapter, spoofed time/challenge, cooldown, restart, real-owner-only")

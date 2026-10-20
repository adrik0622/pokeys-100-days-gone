package.path = "mods/Pokeys100DaysGone/42/media/lua/shared/?.lua;" ..
    "mods/Pokeys100DaysGone/42/media/lua/server/?.lua;" .. package.path
next = nil -- the observed Kahlua limitation also applies to new paths
local V = require "Pokeys/V2Rules"
local R = require "Pokeys/V2Relief"
local M = require "Pokeys/Migration"
local function copy(t)
    local c = {}; for k,v in pairs(t) do c[k] = type(v) == "table" and copy(v) or v end; return c
end
assert(not R.eventKey(nil) and not R.eventKey(0) and not R.eventKey(1.5))
assert(not R.eventKey(math.huge) and not R.eventKey(2147483648))
assert(R.eventKey(2) == "horde:2")
local d = R.open({})
for _, args in ipairs({
    {"a",1,10,false,"applied",24,"visit_relay_alive"},
    {"a",1,10,true,false,24,"deliver_first"},
    {"a",1,10,true,"incident",24,"inspection_required"},
    {"a",0,10,true,"applied",24,"recovery_event_unknown"},
    {"a",1,10,true,"applied",0,"no_relief_needed"},
    {"a",1,-1,true,"applied",24,"clock_unavailable"},
}) do
    local ok, reason = R.allowed(d,args[1],args[2],args[3],args[4],args[5],args[6])
    assert(not ok and reason == args[7], tostring(reason))
end
assert(not R.reserve(d,"",1,10) and not R.reserve(d,string.rep("a",161),1,10))
local receipt = assert(R.reserve(d,"a",1,10))
assert(R.open(copy(d)).pending.key == "a")
assert(not R.reserve(d,"b",1,10)) -- one global in-flight action
receipt.status, receipt.phase, receipt.consumed = "applied", "complete", 2
receipt.delta, receipt.before, receipt.after = 1.5, "friendly", "friendly"
d.pending = nil
assert(R.open(copy(d)) and not R.reserve(d,"a",1,10))
assert(not R.reserve(d,"a",2,9)) -- clock rollback cannot authorize a new receipt
assert(R.reserve(d,"a",2,11)) -- new real event is a distinct bounded contribution
for _, mutate in ipairs({
    function(b) b.schema=99 end,
    function(b) b.revision=0/0 end,
    function(b) b.pending=nil end,
    function(b) b.pending.event=9 end,
    function(b) b.lastHour=nil end,
    function(b) b.records.a["horde:1"].consumed=1 end,
    function(b) b.records.a["horde:1"].before=1 end, -- native return contract is labels
    function(b) b.records.a["horde:1"].delta=math.huge end,
    function(b) b.records.a["horde:1"].event=3 end,
}) do
    local bad = copy(d); mutate(bad)
    assert(not pcall(R.open,bad), "malformed receipt must not be reset/accepted")
end
local full = R.open({})
full.lastHour = 10
for i=1,R.limit do
    full.records["full:"..i] = {["horde:1"]={event=1,hours=10,status="applied",phase="complete",
        consumed=2,delta=1,before="friendly",after="friendly"}}
end
assert(R.open(copy(full)) and not R.reserve(full,"new",2,11))
print("PASS: recurring relief rules, account/event identity, bounds and fail-closed receipts")

function isServer() return true end
Events = {}
for _, name in ipairs({"OnInitGlobalModData","OnServerStarted","OnClientCommand","EveryOneMinute"}) do
    Events[name] = {Add=function(fn) assert(type(fn)=="function") end}
end
local store, history, points, effects, sent = {}, {}, {}, {}, {}
local now, hour, fault, nested = 1000, 100, nil, nil
function getTimestampMs() return now end
function getGameTime() return {getWorldAgeHours=function() return hour end} end
function sendServerCommand(...) sent[#sent+1] = {...} end
function sendAddItemToContainer() effects.syncAdds = effects.syncAdds + 1 end
function sendRemoveItemFromContainer()
    if fault == "sync" then error("injected removal notification failure") end
    if nested then local fn=nested; nested=nil; fn() end
end
TM42 = {GlobalHistoryKey="TheMission42.History", getHistoryKey=function(p) return p.account end}
ModData = {getOrCreate=function(key) store[key]=store[key] or {}; return store[key] end,
    get=function(key) return key==TM42.GlobalHistoryKey and history or store[key] end}
ProjectALifeJimmy = {enabled=function() return true end, playerKey=function(p) return p.account end,
    StandingService={labelFor=function() return "friendly" end,
        points=function(key) return points[key] or 0 end},
    Standing={rate=function() return fault=="rate" and math.huge or 1.5 end,
        add=function(key, faction, delta, info)
            assert(faction==V.faction and (info.kind=="pokeys_medical_relief" or info.kind=="pokeys_recurring_relief"))
            if fault=="standing_before" then error("injected standing failure before effect") end
            points[key] = (points[key] or 0)+delta
            effects.standing = effects.standing+1
            if fault=="standing_after" then error("injected standing failure after effect") end
            if fault=="standing_return" then return nil end
            return "friendly", "friendly" -- actual pinned Jeem contract
        end}}
local Observer = require "Pokeys/MigrationServer"
local Server = require "Pokeys/V2Server"
local originalRepair = Observer.repair
local function player(key)
    local p = {account=key, username=key, x=7990, y=11756, z=0, dead=false, contents={}}
    function p:getUsername() return self.username end
    function p:getX() return self.x end
    function p:getY() return self.y end
    function p:getZ() return self.z end
    function p:isDead() return self.dead end
    function p:isEquipped(item) return item.equipped == true end
    local list = {size=function() return #p.contents end,
        get=function(_,i) return p.contents[i+1] end,
        contains=function(_,item) for _,v in ipairs(p.contents) do if v==item then return true end end; return false end}
    local inv = {getItems=function() return list end,
        AddItem=function(_,kind) effects.items=effects.items+1; return {kind=kind} end,
        Remove=function(_,item)
            if fault=="remove_refused" then return end
            for i,v in ipairs(p.contents) do if v==item then table.remove(p.contents,i); break end end
            if fault=="remove_after" then error("injected ambiguous removal") end
        end}
    function p:getInventory() return inv end
    return p
end
local function item(p, kind, favorite, equipped)
    local i = {kind=kind or "Base.Bandage", favorite=favorite, equipped=equipped}
    function i:getFullType() return self.kind end
    function i:isFavorite() return self.favorite == true end
    p.contents[#p.contents+1] = i
end
local function supplies(p) item(p); item(p) end
local function command(p,name,args)
    now=now+600; Server.command(V.module,name or "relief",p,args or {})
    return sent[#sent][4]
end
local function setup(enabled)
    store, history, points, sent = {}, {}, {}, {}
    effects = {standing=0,items=0,syncAdds=0}
    fault, nested, hour = nil, nil, 100
    SandboxVars = {PokeysV2={Enabled=true,RepeatRelief=enabled~=false}}
    HordeSandbox = {get=function() return true end}
    HordeManager = {state={CurrentHordeNightID=0,HordeNightActive=false,CompletionRecorded=false,
        NightBudgetSpawned=0,HordeNightsSurvived=0}, nextStartWorldHour=function() return 200 end}
    Observer.repair = originalRepair
    Observer.init(); Server.init(); Observer.minute()
    local a,b = player("user:a"), player("user:b")
    for _,p in ipairs({a,b}) do history[p.account]={completed={[V.mission]=true}}; Server.credit(p) end
    return a,b
end
local function event(id, success)
    local s=HordeManager.state
    s.CurrentHordeNightID,s.CompletionRecorded,s.NightBudgetSpawned=id,true,1
    if success then s.HordeNightsSurvived=s.HordeNightsSurvived+1 end
    Observer.minute()
end
local function reopen()
    store=copy(store); Observer.init(); Server.init() -- mocked reopen, not a process restart
end

local a,b=setup(false); event(1,true); supplies(a)
assert(store[R.key]==nil and command(a).code=="relief_disabled" and #a.contents==2)
a,b=setup(); supplies(a)
assert(command(a).code=="no_relief_needed" and #a.contents==2)
event(1,true)
local c=player("user:unintroduced"); supplies(c)
assert(command(c,nil,{completed=true,account=a.account,event=1}).code=="deliver_first" and #c.contents==2)
a.x=8010; assert(command(a).code=="visit_relay_alive"); a.x=7990
a.dead=true; assert(command(a).code=="visit_relay_alive"); a.dead=false
a.z=1; assert(command(a).code=="visit_relay_alive"); a.z=0
a.contents={}; item(a); item(a,"Base.Bandage",true); item(a,"Base.Bandage",false,true); item(a,"Base.BandageDirty")
assert(command(a).code=="need_two_relief_bandages" and #a.contents==4 and store[R.key].pending==nil)
a.contents={}; supplies(a); supplies(b)
local before=effects.standing
nested=function() assert(command(b).code=="inspection_required") end
local result=command(a,nil,{event=99,account=b.account,count=999,reward="Base.Axe",delta=1000})
assert(result.code=="relief_delivered" and result.state.reliefEvent==1 and result.state.disruptionHours==12)
assert(#a.contents==0 and #b.contents==2 and effects.items==0 and effects.standing==before+1)
assert(points[a.account]==3 and points[b.account]==1.5)
assert(R.receipt(store[R.key],a.account,1).before=="friendly")
supplies(a); reopen()
assert(command(a).code=="relief_already_done" and #a.contents==2 and effects.standing==before+1)
event(2,false)
assert(Observer.disruptionEvent()==1 and command(a).code=="relief_already_done") -- abort cannot mint another deed
assert(command(b).code=="relief_delivered" and Observer.disruptionHours()==0)
assert(command(a).code=="no_relief_needed" and #a.contents==2)
event(3,true)
assert(command(a).code=="relief_delivered" and R.receipt(store[R.key],a.account,3))
assert(not R.receipt(store[R.key],a.account,2) and #a.contents==0 and effects.items==0)
hour=99; supplies(b); assert(command(b).code=="clock_unavailable" and #b.contents==2); hour=100

-- A legacy disruption with no success identity is not guessed/migrated.
a,b=setup(); event(1,true); store[M.key].disruptionEvent=nil; Observer.init(); supplies(a)
assert(command(a).code=="recovery_event_unknown" and #a.contents==2)
store[M.key].schema=99; Observer.init()
assert(command(a).code=="recovery_unavailable" and store[M.key].schema==99 and #a.contents==2)
a,b=setup(); event(1,true); supplies(a); store[R.key].schema=99; Server.init()
assert(command(a).code=="relief_unavailable" and store[R.key].schema==99 and #a.contents==2)
a,b=setup(); event(1,true); supplies(a); store[R.key]=copy(full); Server.init()
assert(command(a).code=="relief_ledger_full" and #a.contents==2)
a,b=setup(); event(1,true); supplies(a); fault="rate"
assert(command(a).code=="standing_unavailable" and store[R.key].pending==nil and #a.contents==2)

for _, mode in ipairs({"remove_refused","remove_after","sync","standing_before","standing_after","standing_return","repair","repair_after","repair_false"}) do
    a,b=setup(); event(1,true); supplies(a); supplies(b)
    local beforePoints=points[a.account]
    fault=mode
    if mode=="repair" or mode=="repair_after" or mode=="repair_false" then
        Observer.repair=function()
            if mode=="repair_after" then originalRepair() end
            if mode=="repair_false" then return false end
            error("injected recovery failure")
        end
    end
    assert(command(a).code=="inspection_required",mode)
    local r=R.receipt(store[R.key],a.account,1)
    assert(r.status=="incident" and store[R.key].pending.key==a.account,mode)
    if mode=="remove_refused" then assert(r.consumed==0 and #a.contents==2) end
    if mode=="remove_after" then assert(r.consumed==0 and #a.contents==1) end
    if mode=="sync" then assert(r.consumed==1 and #a.contents==1 and points[a.account]==beforePoints) end
    if mode=="standing_after" or mode=="standing_return" or mode:find("repair") then
        assert(#a.contents==0 and points[a.account]==beforePoints+1.5,mode)
    end
    local remaining,standingCount=#a.contents,effects.standing
    fault=nil; Observer.repair=originalRepair; reopen()
    assert(command(a).code=="inspection_required" and command(b).code=="inspection_required",mode)
    assert(#a.contents==remaining and #b.contents==2 and effects.standing==standingCount and effects.items==0,mode)
end
print("PASS: recurring relief server authority, real-observer event IDs, no item payout, replay and partial-effect latches")

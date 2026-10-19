package.path = "mods/Pokeys100DaysGone/42/media/lua/shared/?.lua;" ..
    "mods/Pokeys100DaysGone/42/media/lua/server/?.lua;" .. package.path
local store, message, calls, fail = {}, "", 0, false
function isServer() return true end
ModData={getOrCreate=function() return store end}
Events={OnInitGlobalModData={Add=function() end},OnClientCommand={Add=function() end}}
function sendServerCommand(p,m,c,args) message=args.message end
local p={role="player",x=7990,y=11756,z=0,dead=false}
function p:getRole() return {getName=function() return self.role end} end
function p:getX() return self.x end
function p:getY() return self.y end
function p:getZ() return self.z end
function p:isDead() return self.dead end
local close = false
function getOnlinePlayers() return {size=function() return close and 1 or 0 end,
    get=function() return {isDead=function() return false end,getX=function() return 8050 end,
        getY=function() return 11756 end} end} end
function getCell() return {getGridSquare=function() return {isOutside=function() return true end,
    isFree=function() return true end,isSolid=function() return false end} end} end
BanditCustom={ClanGet=function() return {} end}
BanditServer={Spawner={Clan=function(player,args)
    calls=calls+1; assert(args.size==1 and args.hostile and args.hostileP)
    assert(args.x==8050 and args.fullname=="Road Reclaimer Scout")
    if fail then error("injected ambiguous spawn failure") end
end}}
local E=require "Pokeys/EncounterServer"; E.init()
local function run(args) E.command(E.module,"scout",p,args or {}) end
run(); assert(message=="Admin fixture only." and calls==0)
p.role="admin"; p.z=1; run(); assert(calls==0)
p.z=0; close=true; run(); assert(calls==0 and not store.attempted)
close=false; run({size=100,x=0,hostile=false}); assert(calls==1 and store.attempted)
run(); E.init(); run(); assert(calls==1) -- retries/restart cannot multiply bodies
store={}; E.init(); fail=true; run(); run(); assert(calls==2 and store.attempted)
store={schema=99}; E.init(); run(); assert(calls==2 and store.schema==99)
print("PASS: encounter adapter admin/distance, fixed identity/count, one-shot/restart/failure latch")

-- One-shot development encounter using the inspected original Bandits public API.
-- No NPC AI, copied clan data, automatic respawn, reward or reputation simulation.
if not isServer() then return end
local Campaign = require "Pokeys/Campaign"
local E = { module = "PokeysEncounter", key = "Pokeys100DaysGone.EncounterTest" }
local data
local point = { x=8050, y=11756, z=0 }
local clan = "f6e2ca8c-311e-4ee2-9fe6-1c9e14dbcd11" -- Upstream 01_Rednecks, reference only.

function E.init()
    local d = ModData.getOrCreate(E.key)
    local empty = true
    for _ in pairs(d) do empty=false; break end
    if empty then d.schema, d.attempted = 1, false end
    if d.schema ~= 1 or type(d.attempted) ~= "boolean" then
        data = nil; print("[PokeysEncounter] DISABLED invalid fixture state"); return
    end
    data = d
end

local function reply(player, message)
    sendServerCommand(player, E.module, "result", {message=message})
end

function E.command(module, command, player, args)
    if module ~= E.module or command ~= "scout" or not player then return end
    local role = player:getRole()
    if not role or role:getName() ~= "admin" then reply(player,"Admin fixture only."); return end
    if not data or data.attempted then reply(player,"Fixture locked; preserve world and inspect prior attempt."); return end
    if player:isDead() or not Campaign.near(player:getX(),player:getY(),player:getZ()) then
        reply(player,"Stand alive at the Mutual Aid relay to run this fixture."); return
    end
    if not BanditServer or not BanditServer.Spawner or not BanditServer.Spawner.Clan or
            not BanditCustom or not BanditCustom.ClanGet(clan) then
        reply(player,"Selected Bandits clan/API unavailable; no substitute NPC spawned."); return
    end
    local players = getOnlinePlayers()
    for i=0,players:size()-1 do
        local other = players:get(i)
        if not other:isDead() and (other:getX()-point.x)^2 + (other:getY()-point.y)^2 < 55^2 then
            reply(player,"Spawn refused: a player is within 55 tiles of the trial point."); return
        end
    end
    local square = getCell():getGridSquare(point.x,point.y,point.z)
    if not square or not square:isOutside() or not square:isFree(false) or square:isSolid() then
        reply(player,"Trial point not loaded/free/outdoors. Move/review location, no spawn attempted."); return
    end
    data.attempted = true -- Ambiguous API failures never automatically retry.
    local ok, failure = pcall(function()
        BanditServer.Spawner.Clan(player, {cid=clan, size=1, x=point.x,y=point.y,z=point.z,
            program="Bandit", stage="Prepare", hostile=true, hostileP=true,
            fullname="Road Reclaimer Scout", permanent=true, key="PokeysReclaimerFixture"})
    end)
    if ok then
        print("[PokeysEncounter] One Reclaimer scout requested at 8050,11756,0; verify actual body/behavior.")
        reply(player,"One scout requested 60 tiles east (8050/11756). Verify physical NPC; fixture now locked.")
    else
        print("[PokeysEncounter] Attempt latched after API failure: " .. tostring(failure))
        reply(player,"NPC request failed; fixture latched, inspect server log. No automatic retry.")
    end
end
Events.OnInitGlobalModData.Add(E.init)
Events.OnClientCommand.Add(E.command)
return E

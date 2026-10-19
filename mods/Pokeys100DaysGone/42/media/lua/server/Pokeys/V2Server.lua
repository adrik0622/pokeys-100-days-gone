if not isServer() then return end
local V = require "Pokeys/V2Rules"
local Observer = require "Pokeys/MigrationServer"
local Server = {}
local data
local rate = {}
local function hour() return getGameTime():getWorldAgeHours() end

function Server.init()
    if not V.enabled() then data = nil; return end
    local ok, result = pcall(V.open, ModData.getOrCreate(V.key))
    data = ok and result or nil
    print("[PokeysV2] " .. (data and "bridge schema=1 loaded; native owners retain authority" or "DISABLED invalid bridge state"))
end

function Server.start()
    if V.enabled() then
        print("[PokeysV2] native gather contract installed=" .. tostring(V.installMission(TM42)))
    end
end

local function standing(player)
    local J = ProjectALifeJimmy
    if type(J) ~= "table" or type(J.Standing) ~= "table" or type(J.Standing.add) ~= "function"
        or type(J.Standing.rate) ~= "function" or type(J.StandingService) ~= "table"
        or type(J.StandingService.labelFor) ~= "function" or type(J.StandingService.points) ~= "function"
        or type(J.enabled) ~= "function" or not J.enabled("standing") then return nil end
    local key = J.playerKey(player)
    return J, key, J.StandingService.labelFor(key, V.faction), J.StandingService.points(key, V.faction)
end

local function history(player)
    if type(TM42) ~= "table" or type(TM42.getHistoryKey) ~= "function" or not TM42.GlobalHistoryKey then return nil end
    local key = TM42.getHistoryKey(player) -- read only: native server owns key migration and completion
    local all = ModData.get(TM42.GlobalHistoryKey)
    local record = all and all[key]
    return key, type(record) == "table" and type(record.completed) == "table" and record.completed[V.mission] == true
end

function Server.credit(player)
    if not data or not V.enabled() then return end
    local key, completed = history(player)
    if not key or not completed or data.grants[key] then return end
    local J, playerKey = standing(player)
    if not J then return end -- keep deferred, no guessed standing or duplicate reputation ledger
    if not V.reserve(data, key, hour()) then return end
    local ok, failure = pcall(function()
        local delta = J.Standing.rate(V.faction, 2, playerKey)
        assert(V.finite(delta) and delta >= 0, "Jeem rate unavailable")
        local before, after = J.Standing.add(playerKey, V.faction, delta,
            {kind = "pokeys_medical_relief", x = V.x, y = V.y})
        assert(before ~= nil and after ~= nil, "Jeem standing refused")
        Observer.repair() -- same original observer condition, not a second horde scheduler
        data.grants[key].status = "applied"
        data.grants[key].delta = delta
        data.revision = data.revision + 1
        print("[PokeysV2] confirmed native relief -> Jeem delta=" .. delta .. "; recovery repaired")
    end)
    if not ok then
        data.grants[key].status = "incident"
        print("[PokeysV2] credit INCIDENT latched; no retry: " .. tostring(failure))
    end
end

local function snapshot(player)
    local key, completed = history(player)
    local J, _, label, points = standing(player)
    local grant = data and key and data.grants[key]
    return {available = data ~= nil, nativeMission = TM42 ~= nil, npcOwner = ProjectALife ~= nil,
        standingOwner = J ~= nil, label = label or "unavailable", points = points or 0,
        completed = completed == true, credit = grant and grant.status or "not credited",
        delta = grant and grant.delta or 0, revision = data and data.revision or 0,
        aidPending = data and data.aidPending ~= nil or false,
        aidHours = data and data.lastAid and math.max(0, V.aidHours-(hour()-data.lastAid)) or 0,
        disrupted = Observer.aidBlocked() == true}
end

function Server.command(module, command, player, args)
    if module ~= V.module or not player or not V.enabled() then return end
    if command ~= "state" and command ~= "aid" then return end -- no completion/rep/item-supplied RPC
    local user, ms = player:getUsername(), getTimestampMs()
    if type(user) ~= "string" or #user == 0 or #user > 64 then return end
    if rate[user] and ms-rate[user] < 500 then return end
    rate[user] = ms
    Server.credit(player)
    local code = "refreshed"
    if command == "aid" then
        if not data then return end
        local key = history(player)
        local _, _, label = standing(player)
        local allowed
        allowed, code = V.aidAllowed(data, key, hour(), V.near(player), label, Observer.aidBlocked())
        if allowed then
            data.aidPending = {hours = hour(), by = user} -- durable fail-closed reservation before effect
            local ok, failure = pcall(function()
                local inventory = player:getInventory()
                local item = inventory:AddItem("Base.Disinfectant")
                assert(item, "Disinfectant unavailable")
                sendAddItemToContainer(inventory, item)
                data.lastAid, data.aidPending = hour(), nil
                data.revision = data.revision + 1
            end)
            code = ok and "aid_received" or "inspection_required"
            if not ok then print("[PokeysV2] aid INCIDENT latched: " .. tostring(failure)) end
        end
    end
    sendServerCommand(player, V.module, "state", {code = code, state = snapshot(player)})
end

function Server.minute()
    if not data or not V.enabled() then return end
    local players = getOnlinePlayers()
    for i = 0, math.min(players:size()-1, 15) do Server.credit(players:get(i)) end
    rate = {} -- bounded request throttle; not durable gameplay cooldowns
end

Events.OnInitGlobalModData.Add(Server.init)
Events.OnServerStarted.Add(Server.start)
Events.EveryOneMinute.Add(Server.minute)
Events.OnClientCommand.Add(Server.command)
return Server

if not isServer() then return end
local V = require "Pokeys/V2Rules"
local R = require "Pokeys/V2Relief"
local Observer = require "Pokeys/MigrationServer"
local Server = {}
local data, relief
local rate = {}
local function hour() return getGameTime():getWorldAgeHours() end

function Server.init()
    relief = nil
    if not V.enabled() then data = nil; return end
    local ok, result = pcall(V.open, ModData.getOrCreate(V.key))
    data = ok and result or nil
    print("[PokeysV2] " .. (data and "bridge schema=1 loaded; native owners retain authority" or "DISABLED invalid bridge state"))
    if data and R.enabled() then
        local valid, receipts = pcall(R.open, ModData.getOrCreate(R.key))
        relief = valid and receipts or nil
        print("[PokeysV2] " .. (relief and "recurring relief receipts loaded" or "recurring relief DISABLED invalid state"))
    end
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
    if Observer.disruptionHours() == nil then return end -- defer before any standing effect
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
        local repaired = Observer.repair() -- same original condition, not a second scheduler
        assert(repaired ~= nil, "relay recovery unavailable")
        data.grants[key].status = "applied"
        data.grants[key].delta = delta
        data.revision = data.revision + 1
        print("[PokeysV2] confirmed native relief -> Jeem delta=" .. delta ..
            (repaired and "; recovery repaired" or "; recovery unchanged (no active disruption)"))
    end)
    if not ok then
        data.grants[key].status = "incident"
        print("[PokeysV2] credit INCIDENT latched; no retry: " .. tostring(failure))
    end
end

local function donateRelief(player, recovery)
    if not R.enabled() then return "relief_disabled" end
    if not data then return "bridge_unavailable" end
    if not relief then return "relief_unavailable" end
    local key = history(player)
    local grant = key and data.grants[key]
    local event = Observer.disruptionEvent()
    local allowed, code = R.allowed(relief, key, event, hour(), V.near(player), grant and grant.status, recovery)
    if not allowed then return code end
    local J, playerKey = standing(player)
    if not J or type(playerKey) ~= "string" or #playerKey == 0 or #playerKey > 160 then
        return "standing_unavailable"
    end
    local inventory = player:getInventory()
    local supplies = {}
    local inspected = pcall(function()
        local items = inventory:getItems()
        for i = 0, items:size()-1 do
            local item = items:get(i)
            if item and item:getFullType() == "Base.Bandage" and not item:isFavorite()
                and not player:isEquipped(item) then
                supplies[#supplies+1] = item
                if #supplies == 2 then break end
            end
        end
    end)
    if not inspected then return "supplies_unavailable" end
    if #supplies ~= 2 then return "need_two_relief_bandages" end
    -- One base standing point, scaled by Jeem's native positive-deed multiplier.
    local rated, delta = pcall(J.Standing.rate, V.faction, 1, playerKey)
    if not rated or not V.finite(delta) or delta < 0 then return "standing_unavailable" end
    local receipt, reason = R.reserve(relief, key, event, hour())
    if not receipt then return reason end
    receipt.delta = delta -- intended rate; only an applied receipt certifies completion
    local ok, failure = pcall(function()
        receipt.phase = "consuming"
        for _, item in ipairs(supplies) do
            inventory:Remove(item)
            assert(not inventory:getItems():contains(item), "relief Bandage removal refused")
            receipt.consumed = receipt.consumed + 1
            sendRemoveItemFromContainer(inventory, item)
        end
        receipt.phase = "standing"
        local before, after = J.Standing.add(playerKey, V.faction, delta,
            {kind = "pokeys_recurring_relief", event = event, x = V.x, y = V.y})
        -- Pinned Jeem returns before/after LABELS, not numeric points.
        assert(type(before) == "string" and #before > 0 and #before <= 32
            and type(after) == "string" and #after > 0 and #after <= 32, "relief standing refused")
        receipt.before, receipt.after = before, after
        receipt.phase = "repair"
        assert(Observer.repair() == true, "relief recovery no longer available")
        receipt.status, receipt.phase = "applied", "complete"
        relief.pending = nil
        relief.revision = relief.revision + 1
        print("[PokeysV2] recurring relief applied event=" .. R.eventKey(event) ..
            " by=" .. player:getUsername() .. "; Jeem delta=" .. delta .. "; recovery repaired")
    end)
    if not ok then
        receipt.status = "incident"
        relief.revision = relief.revision + 1
        print("[PokeysV2] relief INCIDENT latched at " .. receipt.phase .. "; no retry: " .. tostring(failure))
        return "inspection_required"
    end
    return "relief_delivered"
end

local function snapshot(player)
    local key, completed = history(player)
    local J, _, label, points = standing(player)
    local grant = data and key and data.grants[key]
    local recovery = Observer.disruptionHours()
    local aidEligible, aidReason = false, "bridge_unavailable"
    if data and recovery == nil then aidReason = "recovery_unavailable"
    elseif data then
        aidEligible, aidReason = V.aidAllowed(data, key, hour(), V.near(player), label, recovery > 0)
        if aidEligible then aidReason = "aid_ready" end
    end
    local reliefEligible, reliefReason = false, "relief_disabled"
    local event = Observer.disruptionEvent()
    if R.enabled() then
        if not data then reliefReason = "bridge_unavailable"
        elseif not relief then reliefReason = "relief_unavailable"
        else
            reliefEligible, reliefReason = R.allowed(relief, key, event, hour(), V.near(player), grant and grant.status, recovery)
            if reliefEligible and not J then reliefEligible, reliefReason = false, "standing_unavailable" end
        end
    end
    local receipt = relief and key and R.receipt(relief, key, event)
    return {available = data ~= nil and recovery ~= nil, nativeMission = TM42 ~= nil, npcOwner = ProjectALife ~= nil,
        standingOwner = J ~= nil, label = label or "unavailable", points = points or 0,
        completed = completed == true, credit = grant and grant.status or "not credited",
        delta = grant and grant.delta or 0, revision = data and data.revision or 0,
        aidPending = data and data.aidPending ~= nil or false,
        aidHours = data and data.lastAid and math.max(0, V.aidHours-(hour()-data.lastAid)) or 0,
        disrupted = recovery ~= nil and recovery > 0,
        recoveryAvailable = recovery ~= nil, disruptionHours = recovery or 0,
        aidEligible = aidEligible, aidReason = aidReason,
        reliefEnabled = R.enabled(), reliefEligible = reliefEligible, reliefReason = reliefReason,
        reliefEvent = event or 0, reliefCredit = receipt and receipt.status or "none"}
end

function Server.command(module, command, player, args)
    if module ~= V.module or not player or not V.enabled() then return end
    if command ~= "state" and command ~= "aid" and command ~= "relief" then return end -- no completion/rep/item-supplied RPC
    local user, ms = player:getUsername(), getTimestampMs()
    if type(user) ~= "string" or #user == 0 or #user > 64 then return end
    if rate[user] and ms-rate[user] < 500 then return end
    rate[user] = ms
    Server.credit(player)
    local recovery = Observer.disruptionHours()
    local code = not data and "bridge_unavailable" or
        (recovery == nil and "recovery_unavailable" or "refreshed")
    if command == "relief" then
        code = donateRelief(player, recovery) -- no caller-controlled identity, event, count or reward
    elseif command == "aid" then
        local allowed
        if data and recovery ~= nil then
            local key = history(player)
            local _, _, label = standing(player)
            allowed, code = V.aidAllowed(data, key, hour(), V.near(player), label, recovery > 0)
        end
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

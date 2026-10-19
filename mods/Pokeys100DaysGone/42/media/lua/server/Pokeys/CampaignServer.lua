if not isServer() then return end
local Campaign = require "Pokeys/Campaign"
local Observer = require "Pokeys/MigrationServer"
local Server = {}
local data

function Server.init()
    local ok, result = pcall(Campaign.open, ModData.getOrCreate(Campaign.key))
    if ok then
        data = result
        print("[PokeysCampaign] loaded schema=1 revision=" .. data.revision)
        local time = getGameTime()
        if time.getYear and time.getMonth and time.getDay then
            print("[PokeysCampaign] calendar=" .. time:getYear() .. "-" .. (time:getMonth()+1) ..
                "-" .. (time:getDay()+1) .. " worldAgeHours=" .. time:getWorldAgeHours())
        end
    else
        data = nil
        print("[PokeysCampaign] DISABLED: " .. tostring(result))
    end
end

local function now()
    return getGameTime():getWorldAgeHours()
end

local function send(player, code)
    local args = { code = code }
    if data then args.state = Campaign.snapshot(data, now()) end
    sendServerCommand(player, Campaign.module, "result", args)
end

local function broadcast()
    sendServerCommand(Campaign.module, "state", Campaign.snapshot(data, now()))
end

local function bandages(player)
    -- Main inventory only: no worn items, nested-bag traversal or client-supplied IDs.
    local found = {}
    local items = player:getInventory():getItems()
    for i = 0, items:size() - 1 do
        local item = items:get(i)
        if item:getFullType() == "Base.Bandage" and not item:isFavorite() then
            found[#found + 1] = item
            if #found == 2 then break end
        end
    end
    return found
end

function Server.command(module, command, player, args)
    if module ~= Campaign.module or not player then return end
    if not data then send(player, "campaign_unavailable"); return end
    if command == "state" then send(player, "refreshed"); return end
    if command == "admin" then
        -- 42.21 uses server-owned Role objects. Strict default admin role only;
        -- never trust a client flag or a deprecated access-level string.
        local role = player:getRole()
        if not role or role:getName() ~= "admin" then send(player, "not_admin"); return end
        local ok, code = Campaign.admin(data, args)
        if ok then
            print("[PokeysCampaign] admin change by " .. player:getUsername())
            broadcast()
        end
        send(player, code)
        return
    end
    local hour = now()
    local ok, code = Campaign.allowed(data, command, hour,
        player:getX(), player:getY(), player:getZ(), not player:isDead())
    if not ok then send(player, code); return end
    if command == "aid" and Observer.aidBlocked() then send(player, "aid_disrupted"); return end
    local supplies
    if command == "donate" then
        supplies = bandages(player)
        if #supplies ~= 2 then send(player, "need_two_bandages"); return end
    end
    Campaign.reserve(data, command, hour, player:getUsername())
    local applied, failure = pcall(function()
        local inventory = player:getInventory()
        if command == "donate" then
            for _, item in ipairs(supplies) do
                inventory:Remove(item)
                sendRemoveItemFromContainer(inventory, item)
            end
        else
            local item = inventory:AddItem("Base.Disinfectant")
            assert(item, "Disinfectant could not be created")
            sendAddItemToContainer(inventory, item)
        end
    end)
    if not applied then
        print("[PokeysCampaign] INVENTORY INCIDENT; actions locked: " .. tostring(failure))
        broadcast()
        send(player, "needs_admin_inspection")
        return
    end
    Campaign.finish(data, command)
    if command == "donate" then Observer.repair() end
    print("[PokeysCampaign] " .. command .. " completed by " .. player:getUsername() ..
        " revision=" .. data.revision)
    broadcast()
    send(player, command == "donate" and "donated" or "aid_received")
end

Events.OnInitGlobalModData.Add(Server.init)
Events.OnClientCommand.Add(Server.command)
return Server

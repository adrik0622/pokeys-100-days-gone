if not isServer() then return end
local M = require "Pokeys/Migration"
local Campaign = require "Pokeys/Campaign"
local Server = {}
local data
local sessions, cooldown = {}, {}

local function hour() return getGameTime():getWorldAgeHours() end
local function forecast()
    -- Only the selected, loaded owner. Never create missing owner data or events.
    if not HordeManager or not HordeManager.state or not HordeManager.nextStartWorldHour then return nil end
    local s = HordeManager.state
    if not HordeSandbox.get("Enabled") then return nil end
    return { id = s.CurrentHordeNightID, active = s.HordeNightActive == true,
        start = HordeManager.nextStartWorldHour(s), direction = s.HordeNightActive and s.HordeDirection or nil,
        completed = s.CompletionRecorded == true, spawned = s.NightBudgetSpawned or 0,
        survived = s.HordeNightsSurvived or 0 }
end

function Server.init()
    local ok, result = pcall(M.open, ModData.getOrCreate(M.key))
    data = ok and result or nil
    sessions, cooldown = {}, {} -- A restart cancels transient tasks, never completes one.
    print("[PokeysObserver] " .. (ok and "loaded" or ("DISABLED: " .. tostring(result))))
end

local function send(player, code, session)
    local args = { code = code }
    if data then args.state = M.snapshot(data, forecast(), hour()) end
    if session then args.step, args.channel = session.step, session.channel end
    sendServerCommand(player, M.module, "result", args)
end

local function broadcast()
    if data then sendServerCommand(M.module, "state", M.snapshot(data, forecast(), hour())) end
end

function Server.aidBlocked()
    return data and data.disruptedUntil > hour()
end

function Server.repair()
    if data and M.repair(data, hour()) then broadcast() end
end

function Server.command(module, command, player, args)
    if module ~= M.module or not player then return end
    if not data then send(player, "unavailable"); return end
    local username = player:getUsername()
    if command == "state" then send(player, "refreshed"); return end
    if command == "cancel" then sessions[username] = nil; send(player, "cancelled"); return end
    local ms = getTimestampMs()
    local alive = not player:isDead()
    local near = Campaign.near(player:getX(), player:getY(), player:getZ())
    if command == "begin" then
        if cooldown[username] and ms < cooldown[username] then send(player, "cooldown"); return end
        local session, code = M.begin(data, forecast(), hour(), ms,
            player:getX(), player:getY(), player:getZ(), alive, ZombRand(3) + 1)
        sessions[username] = session
        if session then cooldown[username] = ms + 60000 end
        send(player, code, session)
    elseif command == "step" then
        local session = sessions[username]
        local ok, code = M.step(session, forecast(), ms, type(args) == "table" and args.channel, alive, near)
        if ok then
            if session.step < 4 then session.channel = ZombRand(3) + 1 end
        elseif code ~= "too_early" then sessions[username] = nil end
        send(player, code, sessions[username])
    elseif command == "finish" then
        local ok, code = M.finish(data, sessions[username], forecast(), ms, alive, near)
        sessions[username] = nil
        if ok then broadcast() end
        send(player, code)
    end
end

function Server.minute()
    if not data then return end
    local changed = M.observe(data, forecast(), hour())
    local ms = getTimestampMs()
    for user, s in pairs(sessions) do if ms - s.started > 25000 then sessions[user] = nil end end
    for user, untilMs in pairs(cooldown) do if ms >= untilMs then cooldown[user] = nil end end
    -- One small snapshot/minute, no map/zombie scans or second scheduler.
    broadcast()
    if changed then print("[PokeysObserver] Mutual Aid supply disruption, event=" .. data.lastEvent) end
end
Events.OnInitGlobalModData.Add(Server.init)
Events.OnClientCommand.Add(Server.command)
Events.EveryOneMinute.Add(Server.minute)
return Server

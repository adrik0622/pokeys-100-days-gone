if not isClient() then return end
require "ISUI/ISPanel"
require "ISUI/ISButton"
local M = require "Pokeys/Migration"
local Panel = ISPanel:derive("PokeysObserverPanel")
local instance
local messages = {
    refreshed = "Observer bulletin refreshed. Arrival bounds are relative to this refresh.",
    visit_relay = "Visit the Mutual Aid relay (7990 / 11756 / ground floor, within 4 tiles).",
    no_forecast = "No future physical-owner schedule is available. No warning invented.",
    already_calibrated = "This forecast is already calibrated for the whole group.",
    calibrated = "Signal locked. Arrival uncertainty narrowed from +/-2 h to +/-15 min for everyone.",
    cancelled = "Calibration cancelled; baseline warning remains available.",
    interrupted = "Calibration interrupted. Baseline warning remains available.",
    cooldown = "Relay cooling down. Wait one real minute after starting before trying again.",
    too_early = "Hold the signal longer before pressing the channel.",
    wrong_channel = "Wrong channel; task stopped. Baseline warning remains available.",
    expired = "Signal expired; task stopped.",
    incomplete = "Calibration incomplete; task stopped.",
    unavailable = "Observer state unavailable. Preserve save and inspect server log.",
}

function Panel:request(command, args)
    sendClientCommand(self.player, M.module, command, args or {})
end

function Panel:createChildren()
    ISPanel.createChildren(self)
    local function button(x, y, width, label, callback)
        local b = ISButton:new(x, y, width, 28, label, self, callback)
        b:initialise(); self:addChild(b); return b
    end
    button(20, 340, 160, "Begin 15-second tuning", function(p)
        p.started = getTimestampMs(); p:request("begin")
    end)
    for channel = 1, 3 do
        local value = channel
        button(185 + (channel - 1) * 95, 340, 90, "Channel " .. channel,
            function(p) p:request("step", { channel = value }) end)
    end
    button(480, 340, 100, "Lock signal", function(p) p:request("finish") end)
    button(585, 340, 90, "Cancel", function(p) p:request("cancel"); p.step = nil end)
    button(20, 535, 140, "Refresh bulletin", function(p) p:request("state") end)
    button(535, 535, 140, "Close", function(p)
        p:request("cancel"); p:removeFromUIManager(); instance = nil
    end)
    local role = self.player:getRole()
    if role and role:getName() == "admin" then
        self.debugButtons = {}
        for i, entry in ipairs({ {"Force real horde", "DebugForceHorde"},
            {"Complete real horde", "DebugCompleteHorde"}, {"Abort real horde", "DebugAbortHorde"} }) do
            local command = entry[2]
            self.debugButtons[i] = button(20 + (i-1)*220, 575, 215, "DEV: " .. entry[1], function(p)
                -- Existing upstream admin handler remains the authority.
                sendClientCommand(p.player, "HordeNights", command, {})
            end)
        end
        self.scout = button(20, 615, 655, "DEV: one hostile Reclaimer scout (Bandits fixture, once per world)", function(p)
            sendClientCommand(p.player, "PokeysEncounter", "scout", {})
        end)
    end
end

function Panel:prerender()
    ISPanel.prerender(self)
    local function line(text, y, r, g, b)
        self:drawText(text, 20, y, r or 1, g or 1, b or 1, 1, UIFont.Small)
    end
    line("FIELD OBSERVERS - shared bulletin / relay", 16)
    for i, text in ipairs(M.history) do line(text, 30 + i * 22, 0.8, 0.85, 0.9) end
    local s = self.state
    if self.scout then self.scout.enable = s and s.npcAvailable or false end
    for _, b in ipairs(self.debugButtons or {}) do b.enable = s and s.available or false end
    if not s or not s.available then
        line("Physical horde owner unavailable: no forecast is simulated.", 172, 1, 0.8, 0.4)
    elseif s.active then
        line("MIGRATION ACTIVE - event " .. s.event .. "; approach: " .. s.direction, 172, 1, 0.6, 0.4)
    elseif s.earliest then
        line(string.format("Arrival in %.2f to %.2f world hours (%s).", s.earliest, s.latest,
            s.calibrated and "calibrated" or "baseline"), 172)
        line("Approach direction: unresolved until arrival (upstream integration gap).", 196, 1, 0.8, 0.4)
    else line("Waiting for physical owner to schedule its next event.", 172) end
    if s then
        line("Mutual Aid disruption: " .. math.ceil(s.disruptedHours) .. " h. Last recorded event: " .. s.lastEvent, 228)
    end
    line("After a real migration, aid pauses 24 world hours; a supply favor repairs 12 hours.", 252)
    line("Optional: at relay, match requested channels after 4 / 8 / 12 seconds, then lock at 15-25 s.", 282)
    line("Skipping never removes the useful baseline. Shared benefit; no item or standing payout.", 306)
    if self.step and self.started then
        local elapsed = math.max(0, (getTimestampMs() - self.started) / 1000)
        if self.step <= 3 then
            line(string.format("%.1f s elapsed. Step %d: Channel %d after %d s total.",
                elapsed, self.step, self.channel, self.step * 4), 388, 0.5, 1, 0.6)
        else line(string.format("%.1f s elapsed. Three channels set; lock between 15 and 25 s.", elapsed), 388) end
    end
    line(self.message or "Requesting live schedule...", 420, 1, 0.85, 0.5)
    line("History is authored prehistory, not simulated NPC activity. Contact records are not physical NPCs.", 464, 0.7, 0.7, 0.7)
    line("No leader or strict cross-event population cap is claimed by this prototype.", 488, 0.7, 0.7, 0.7)
end

local function open(player)
    if instance then instance:request("cancel"); instance:removeFromUIManager() end
    instance = Panel:new(80, 100, 700, 660)
    instance.player = player
    instance.backgroundColor = { r = 0.05, g = 0.05, b = 0.05, a = 0.97 }
    instance:initialise(); instance:addToUIManager(); instance:request("state")
end

local function receive(module, command, args)
    if module == "PokeysEncounter" and command == "result" and instance then
        instance.message = args.message; return
    end
    if module ~= M.module or not instance then return end
    if command == "state" then instance.state = args
    elseif command == "result" then
        instance.state = args.state
        instance.message = messages[args.code] or ("Relay: " .. tostring(args.code))
        if args.code ~= "refreshed" then instance.step, instance.channel = args.step, args.channel end
    end
end
Events.OnFillWorldObjectContextMenu.Add(function(index, menu, objects, test)
    local player = getSpecificPlayer(index)
    if not test and player and not player:isDead() then menu:addOption("Pokeys: observer bulletin", player, open) end
end)
Events.OnServerCommand.Add(receive)
Events.OnDisconnect.Add(function()
    if instance then instance:removeFromUIManager(); instance = nil end
end)
return { open = open, receive = receive }

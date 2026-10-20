if not isClient() then return end
require "ISUI/ISPanel"
require "ISUI/ISButton"
local V = require "Pokeys/V2Rules"
local R = require "Pokeys/V2Relief"
local Panel = ISPanel:derive("PokeysV2Panel")
local instance
local messages = {
    refreshed = "Native state refreshed.", aid_received = "One bottle received; shared 48-hour cooldown started.",
    visit_relay_alive = "Visit relay 7990/11756 alive, ground level.", deliver_first = "Complete the native relief contract first.",
    ems_not_friendly = "County EMS is not friendly. Native Jeem standing controls this service.",
    relay_disrupted = "Supplies disrupted after a migration; relief helps repair the relay.",
    shared_aid_cooldown = "Shared assistance is still on cooldown.", inspection_required = "An interrupted operation is latched. Preserve the save for inspection.",
    bridge_unavailable = "Relay records unavailable. Ask the host to inspect the saved state.",
    recovery_unavailable = "Relay recovery unavailable. Ask the host to inspect the saved state.",
    aid_ready = "Ready: request one shared medical bottle.",
    clock_unavailable = "World time unavailable. No assistance can be granted yet.",
    relief_ready = "Recovery needs supplies; a donation can repair up to 12 world hours.",
    relief_delivered = "Donation received: EMS standing credited and recovery repaired.",
    relief_already_done = "You already helped this event; your remaining supplies are kept.",
    no_relief_needed = "Relay is healthy; no recovery donation is needed or consumed.",
    need_two_relief_bandages = "Need 2 clean, unstarred, unequipped Bandages in main inventory.",
    recovery_event_unknown = "Older disruption has no verified event ID; natural recovery still works.",
    relief_unavailable = "Relief receipts unavailable; preserve the save for host inspection.",
    relief_ledger_full = "Relief record limit reached; supplies kept. Ask the host to inspect.",
    supplies_unavailable = "Inventory could not be inspected; no donation reserved.",
    standing_unavailable = "EMS standing service unavailable; donation supplies kept.",
    relief_disabled = "Recurring recovery donations are not enabled.",
}
function Panel:request(command) sendClientCommand(self.player, V.module, command, {}) end
function Panel:createChildren()
    ISPanel.createChildren(self)
    local function button(x, width, title, fn, y)
        local b = ISButton:new(x, y or 270, width, 28, title, self, fn)
        b:initialise(); self:addChild(b)
    end
    button(20, 120, "Refresh", function(p) p:request("state") end)
    button(150, 150, "Contract board", function()
        if TM42 and TM42.toggleMissionUI then TM42.toggleMissionUI() end
    end)
    button(310, 160, "Request EMS aid", function(p) p:request("aid") end)
    button(480, 100, "Close", function(p) p:removeFromUIManager(); instance = nil end)
    if R.enabled() then
        button(20, 300, "Donate 2 Bandages for recovery", function(p) p:request("relief") end, 310)
    end
end
function Panel:prerender()
    ISPanel.prerender(self)
    local function line(text, y) self:drawText(text, 20, y, 0.9, 0.95, 0.95, 1, UIFont.Small) end
    line("Pokeys v2 - County EMS relay (development)", 18)
    local s = self.state
    if s then
        line("County EMS / Jeem: " .. s.label .. string.format("; first-hand points %.2f", s.points), 54)
        line("First delivery completed: " .. tostring(s.completed) .. "; relationship credit: " .. s.credit, 82)
        line(string.format("First-delivery standing deed: %.2f. Shared aid cooldown: %.1f h.", s.delta, s.aidHours), 110)
        line(s.recoveryAvailable and string.format("Relay recovery remaining: %.1f world hours.", s.disruptionHours)
            or "Relay recovery records unavailable; assistance is paused.", 138)
        line("Medical assistance: " .. (messages[s.aidReason] or tostring(s.aidReason)), 166)
    end
    line("Delivery: 2 clean Bandages consumed; 1 Alcohol Wipes; once per account.", 198)
    line("Aid: one shared bottle per 48 world hours. Keeping your supplies is valid.", 220)
    line(self.message or "Waiting for server...", 244)
    if R.enabled() then
        line("Recurring relief: once per account per real event; no item reward.", 350)
        if s then
            line("Event " .. s.reliefEvent .. ": " .. (messages[s.reliefReason] or tostring(s.reliefReason)), 372)
        end
        line("Requires the first delivery. Waiting for natural recovery is a valid choice.", 394)
    end
end
local function open(player)
    if instance then instance:removeFromUIManager() end
    instance = Panel:new(80, 90, 620, R.enabled() and 425 or 325)
    instance.player = player; instance.backgroundColor = {r=0.04,g=0.07,b=0.08,a=0.97}
    instance:initialise(); instance:addToUIManager(); instance:request("state")
end
Events.OnCreatePlayer.Add(function() if V.enabled() then V.installMission(TM42) end end)
Events.OnFillWorldObjectContextMenu.Add(function(index, menu, objects, test)
    local player = getSpecificPlayer(index)
    if not test and V.enabled() and player and not player:isDead() then
        menu:addOption("Pokeys: living-world relay", player, open)
    end
end)
Events.OnServerCommand.Add(function(module, command, args)
    if module == V.module and command == "state" and instance and type(args) == "table" then
        instance.state = args.state; instance.message = messages[args.code] or tostring(args.code)
    end
end)
Events.OnDisconnect.Add(function() if instance then instance:removeFromUIManager(); instance = nil end end)

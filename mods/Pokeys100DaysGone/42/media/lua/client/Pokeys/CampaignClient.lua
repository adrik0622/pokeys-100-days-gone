if not isClient() then return end
require "ISUI/ISPanel"
require "ISUI/ISButton"
local Campaign = require "Pokeys/Campaign"
local Panel = ISPanel:derive("PokeysCampaignPanel")
local instance
local messages = {
    refreshed = "Contact ledger refreshed.",
    donated = "Supplies delivered (+20). Recovery shortened; disruption may still delay aid.",
    aid_received = "Mutual Aid supplied one disinfectant. Shared assistance cooldown started.",
    too_far = "Visit the Mutual Aid drop point to deliver supplies or request aid.",
    not_alive = "Only a living survivor can use the contact.",
    need_two_bandages = "Need 2 non-favorite clean Bandages in your MAIN inventory.",
    aid_locked = "Mutual Aid standing must reach Allied (+20) first.",
    aid_disrupted = "Mutual Aid resupply disrupted. Check observer bulletin; supply favors aid recovery.",
    favor_cooldown = "This shared favor is on cooldown. Refresh for remaining hours.",
    aid_cooldown = "The group's medical assistance is on cooldown.",
    needs_admin_inspection = "Inventory operation interrupted. Contact locked for admin inspection.",
    campaign_unavailable = "Campaign data unavailable; preserve the save and inspect server log.",
    clock_unavailable = "World clock unavailable; no action performed.",
    not_admin = "Only the server's admin role can change campaign test values.",
    admin_changed = "Development value changed by an administrator.",
}

function Panel:request(command, args)
    sendClientCommand(self.player, Campaign.module, command, args or {})
end

function Panel:createChildren()
    ISPanel.createChildren(self)
    local function button(x, y, width, title, callback)
        local b = ISButton:new(x, y, width, 28, title, self, callback)
        b:initialise()
        self:addChild(b)
        return b
    end
    self.donate = button(20, 302, 285, "Deliver 2 clean Bandages (+20 standing)",
        function(p) p:request("donate") end)
    self.aid = button(315, 302, 285, "Request medical assistance",
        function(p) p:request("aid") end)
    button(20, 445, 130, "Refresh ledger", function(p) p:request("state") end)
    button(470, 445, 130, "Close", function(p) p:removeFromUIManager(); instance = nil end)
    local role = self.player:getRole()
    if role and role:getName() == "admin" then
        button(20, 395, 180, "DEV: Mutual Aid allied", function(p)
            p:request("admin", { operation = "setStanding", faction = "mutualAid", value = 20 })
        end)
        button(210, 395, 185, "DEV: Reset favor cooldown", function(p)
            p:request("admin", { operation = "resetCooldown", action = "donate" })
        end)
        button(405, 395, 195, "DEV: Reset aid cooldown", function(p)
            p:request("admin", { operation = "resetCooldown", action = "aid" })
        end)
    end
end

function Panel:prerender()
    ISPanel.prerender(self)
    self:drawText("Pokeys 100 Days Gone - faction contacts", 20, 16, 1, 1, 1, 1, UIFont.Medium)
    self:drawText("Campaign prototype: these are contact records, not physical NPCs.",
        20, 48, 0.85, 0.85, 0.85, 1, UIFont.Small)
    local s = self.state
    for i, faction in ipairs(Campaign.factions) do
        local value = s and s.standing[faction.id]
        local label = value and (Campaign.relationship(value) .. " (" .. value .. ")") or "awaiting server"
        self:drawText(faction.name .. ": " .. label, 20, 60 + i * 26, 1, 1, 1, 1, UIFont.Small)
    end
    self:drawText("Mutual Aid drop point: Rosewood house, 7990 / 11756 / ground floor.",
        20, 174, 0.85, 0.9, 1, 1, UIFont.Small)
    self:drawText("Be within 4 tiles. Move donated bandages out of bags; favorites are excluded.",
        20, 198, 0.85, 0.9, 1, 1, UIFont.Small)
    self:drawText("Favor: 24 world-hour group cooldown. Assistance: 48 hours, one disinfectant.",
        20, 222, 0.85, 0.9, 1, 1, UIFont.Small)
    if s then
        self:drawText("At refresh: favor waits " .. math.ceil(s.favorWait) .. " h; assistance " ..
            math.ceil(s.aidWait) .. " h. Revision " .. s.revision, 20, 250, 1, 1, 1, 1, UIFont.Small)
    end
    local near = Campaign.near(self.player:getX(), self.player:getY(), self.player:getZ())
    local enabled = s and not s.blocked and near and not self.player:isDead()
    self.donate.enable = enabled and s.favorWait <= 0 or false
    self.aid.enable = enabled and s.aidUnlocked and s.aidWait <= 0 or false
    self:drawText(self.message or "Requesting server ledger...", 20, 350, 1, 0.85, 0.5, 1, UIFont.Small)
    self:drawText("Forecast / recovery: open observer bulletin. Physical NPCs and leader still unverified.",
        20, 480, 0.7, 0.7, 0.7, 1, UIFont.Small)
end

local function open(player)
    if instance then instance:removeFromUIManager() end
    instance = Panel:new(100, 120, 620, 510)
    instance.player = player
    instance.backgroundColor = { r = 0.05, g = 0.05, b = 0.05, a = 0.97 }
    instance:initialise()
    instance:addToUIManager()
    instance:request("state")
end

local function context(playerIndex, menu, worldObjects, test)
    if test then return end
    local player = getSpecificPlayer(playerIndex)
    if player and not player:isDead() then
        menu:addOption("Pokeys: faction contacts", player, open)
    end
end

local function receive(module, command, args)
    if module ~= Campaign.module or not instance then return end
    if command == "state" then
        instance.state = args
    elseif command == "result" then
        instance.state = args.state
        instance.message = messages[args.code] or ("Contact response: " .. tostring(args.code))
    end
end

local function disconnect()
    if instance then instance:removeFromUIManager(); instance = nil end
end
Events.OnFillWorldObjectContextMenu.Add(context)
Events.OnServerCommand.Add(receive)
Events.OnDisconnect.Add(disconnect)
return { open = open, receive = receive }

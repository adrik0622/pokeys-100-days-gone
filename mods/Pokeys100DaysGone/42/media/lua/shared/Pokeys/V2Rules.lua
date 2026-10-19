-- Original bounded bridge policy. No NPC simulation, reputation mirror or loot roller.
local V = { key = "Pokeys100DaysGone.V2Bridge", module = "PokeysV2",
    mission = "pokeys_medical_relief_01", faction = "alife_county_ems",
    x = 7990, y = 11756, z = 0, radius = 8, aidHours = 48 }

function V.enabled()
    return SandboxVars and SandboxVars.PokeysV2 and SandboxVars.PokeysV2.Enabled == true
end

function V.near(player)
    return player and not player:isDead() and math.floor(player:getZ()) == V.z
        and (player:getX()-V.x)^2 + (player:getY()-V.y)^2 <= V.radius^2
end

function V.definition()
    return { id = V.mission, enabled = true, type = "gather", letter = "M",
        title = "County EMS - first relay delivery",
        description = "Bring 2 clean Bandages in your main inventory to the relay at 7990/11756, ground level. Claiming consumes both (do not select favorites you want to keep). Receive one Alcohol Wipes. This introduction is once per server account; ordinary NPC help/gifts remain available. With Jeem loaded, confirmation also earns modest EMS standing, repairs 12 hours of relay disruption and opens friendly medical assistance (one shared bottle per 48 world hours). Keeping your bandages and surviving independently is a valid choice.",
        summary = "2 Bandages at the relay -> wipes, EMS relationship and recovery; or keep your supplies.",
        targetCount = 2, requiredItem = "Base.Bandage", consumeRequiredItems = true,
        sortOrder = 10, repeatable = false, rewards = {{type = "Base.AlcoholWipes", count = 1}} }
end

function V.installMission(native)
    if not V.enabled() or type(native) ~= "table" or type(native.rebuildMissionRegistry) ~= "function"
        or type(native.isMissionReady) ~= "function" then return false end
    native.CustomMissionDefs = native.CustomMissionDefs or {}
    local found = false
    for _, mission in ipairs(native.CustomMissionDefs) do
        if mission.id == V.mission then found = true end
    end
    if not found then native.CustomMissionDefs[#native.CustomMissionDefs+1] = V.definition() end
    if not native.PokeysV2ReadyOriginal then
        local original = native.isMissionReady
        native.PokeysV2ReadyOriginal = original
        native.isMissionReady = function(player, mission, data)
            if V.enabled() and mission and mission.id == V.mission and not V.near(player) then return false end
            return original(player, mission, data)
        end
    end
    return native.rebuildMissionRegistry(true) == true
end

local function finite(n) return type(n) == "number" and n == n and n > -math.huge and n < math.huge end
V.finite = finite
function V.open(d)
    local empty = true
    for _ in pairs(d) do empty = false; break end
    if empty then d.schema, d.grants, d.revision = 1, {}, 0 end
    assert(d.schema == 1 and type(d.grants) == "table" and finite(d.revision)
        and d.revision >= 0 and d.revision == math.floor(d.revision), "invalid v2 bridge state")
    for key, grant in pairs(d.grants) do
        assert(type(key) == "string" and #key > 0 and #key <= 160 and type(grant) == "table"
            and (grant.status == "pending" or grant.status == "applied" or grant.status == "incident"), "invalid v2 grant")
        assert(finite(grant.hours) and grant.hours >= 0, "invalid v2 grant time")
        assert(grant.delta == nil or (finite(grant.delta) and grant.delta >= 0), "invalid v2 grant delta")
        assert(grant.status ~= "applied" or grant.delta ~= nil, "applied v2 grant missing delta")
    end
    assert(d.lastAid == nil or (finite(d.lastAid) and d.lastAid >= 0), "invalid aid clock")
    assert(d.aidPending == nil or (type(d.aidPending) == "table"
        and finite(d.aidPending.hours) and d.aidPending.hours >= 0
        and type(d.aidPending.by) == "string" and #d.aidPending.by > 0 and #d.aidPending.by <= 64),
        "invalid aid latch")
    return d
end

function V.reserve(d, key, hour)
    if type(key) ~= "string" or #key > 160 or #key == 0 or not finite(hour) or hour < 0 then return false end
    if d.grants[key] then return false end
    local count = 0
    for _ in pairs(d.grants) do count = count + 1 end
    if count >= 4096 then return false end -- refuse new credits, never prune replay protection
    d.grants[key] = {status = "pending", hours = hour}
    d.revision = d.revision + 1
    return true
end

function V.aidAllowed(d, key, hour, near, label, disrupted)
    if not finite(hour) then return false, "clock_unavailable" end
    if d.aidPending then return false, "inspection_required" end
    if not near then return false, "visit_relay_alive" end
    if not d.grants[key] or d.grants[key].status ~= "applied" then return false, "deliver_first" end
    if label ~= "friendly" and label ~= "allied" then return false, "ems_not_friendly" end
    if disrupted then return false, "relay_disrupted" end
    if d.lastAid and (hour < d.lastAid or hour-d.lastAid < V.aidHours) then return false, "shared_aid_cooldown" end
    return true
end

return V

-- Project-owned campaign rules. No NPC, firearm, horde, or per-frame simulation.
local Campaign = {}
Campaign.key = "Pokeys100DaysGone.Campaign"
Campaign.module = "PokeysCampaign"
Campaign.factions = {
    { id = "mutualAid", name = "Rosewood Mutual Aid", initial = 0 },
    { id = "observers", name = "Field Observers", initial = 25 },
    { id = "reclaimers", name = "Road Reclaimers", initial = -50 },
}
-- Prototype contact at the previously observed Rosewood house. Not a physical NPC.
Campaign.contact = { x = 7990, y = 11756, z = 0, radius = 4 }
Campaign.favorHours = 24
Campaign.aidHours = 48
Campaign.alliedAt = 20

local function finite(n)
    return type(n) == "number" and n == n and n > -math.huge and n < math.huge
end
Campaign.finite = finite

function Campaign.open(data)
    if next(data) == nil then
        data.schema = 1
        data.revision = 0
        data.standing = {}
        for _, faction in ipairs(Campaign.factions) do
            data.standing[faction.id] = faction.initial
        end
        data.nextFavorHour = 0
        data.nextAidHour = 0
        data.blocked = false
    end
    assert(data.schema == 1, "Unsupported campaign schema; preserve save, do not reset")
    assert(finite(data.revision) and data.revision >= 0 and data.revision % 1 == 0,
        "Invalid campaign revision")
    assert(type(data.standing) == "table" and type(data.blocked) == "boolean",
        "Invalid campaign state")
    for _, faction in ipairs(Campaign.factions) do
        local value = data.standing[faction.id]
        assert(finite(value) and value % 1 == 0 and value >= -100 and value <= 100,
            "Invalid faction standing")
    end
    assert(finite(data.nextFavorHour) and data.nextFavorHour >= 0 and
        finite(data.nextAidHour) and data.nextAidHour >= 0, "Invalid campaign cooldown")
    return data
end

function Campaign.relationship(value)
    if value <= -20 then return "Hostile" end
    if value >= Campaign.alliedAt then return "Allied" end
    return "Neutral"
end

function Campaign.near(x, y, z)
    local c = Campaign.contact
    return finite(x) and finite(y) and z == c.z and
        (x - c.x)^2 + (y - c.y)^2 <= c.radius^2
end

function Campaign.snapshot(data, now)
    local view = { revision = data.revision, standing = {}, blocked = data.blocked,
        favorWait = math.max(0, data.nextFavorHour - now),
        aidWait = math.max(0, data.nextAidHour - now),
        aidUnlocked = data.standing.mutualAid >= Campaign.alliedAt }
    for _, faction in ipairs(Campaign.factions) do
        view.standing[faction.id] = data.standing[faction.id]
    end
    return view -- Never return the mutable persistent table or transaction/user details.
end

function Campaign.allowed(data, action, now, x, y, z, alive)
    if not finite(now) or now < 0 then return false, "clock_unavailable" end
    if not alive then return false, "not_alive" end
    if not Campaign.near(x, y, z) then return false, "too_far" end
    if data.blocked then return false, "needs_admin_inspection" end
    if action == "donate" then
        if now < data.nextFavorHour then return false, "favor_cooldown" end
    elseif action == "aid" then
        if data.standing.mutualAid < Campaign.alliedAt then return false, "aid_locked" end
        if now < data.nextAidHour then return false, "aid_cooldown" end
    else
        return false, "unknown_action"
    end
    return true
end

-- Reserve BEFORE inventory effects. A partial failure is latched for inspection,
-- never silently retried. Engine inventory/global-data saves are not a transaction.
function Campaign.reserve(data, action, now, username)
    data.blocked = true
    data.revision = data.revision + 1
    data.lastAction = { action = action, hour = now, username = username, status = "pending" }
    if action == "donate" then data.nextFavorHour = now + Campaign.favorHours end
    if action == "aid" then data.nextAidHour = now + Campaign.aidHours end
end

function Campaign.finish(data, action)
    if action == "donate" then
        data.standing.mutualAid = math.min(100, data.standing.mutualAid + 20)
    end
    data.lastAction.status = "completed"
    data.blocked = false
    data.revision = data.revision + 1
end

function Campaign.admin(data, args)
    if type(args) ~= "table" then return false, "invalid_admin_action" end
    if args.operation == "setStanding" then
        if data.standing[args.faction] == nil or not finite(args.value) or
            args.value % 1 ~= 0 or args.value < -100 or args.value > 100 then
            return false, "invalid_standing"
        end
        data.standing[args.faction] = args.value
    elseif args.operation == "resetCooldown" then
        if data.blocked then return false, "needs_admin_inspection" end
        if args.action == "donate" then data.nextFavorHour = 0
        elseif args.action == "aid" then data.nextAidHour = 0
        else return false, "unknown_action" end
    else
        return false, "invalid_admin_action"
    end
    data.revision = data.revision + 1
    return true, "admin_changed"
end

return Campaign

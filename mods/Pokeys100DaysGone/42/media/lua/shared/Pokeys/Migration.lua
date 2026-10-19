-- Original bounded observer rules. Reads a physical owner's schedule; never spawns a horde.
local Campaign = require "Pokeys/Campaign"
local M = { key = "Pokeys100DaysGone.Observer", module = "PokeysObserver" }
M.history = {
    "DAY 12: Rosewood volunteers turned a house into the Mutual Aid drop point.",
    "DAY 43: Field Observers established a radio watch after the southern evacuation failed.",
    "DAY 71: Road Reclaimers seized supply routes. Mutual Aid refused their tolls.",
    "DAY 96: A migration damaged the relay. Clean medical supplies remain scarce.",
    "DAY 100: You arrive. Deliver supplies, earn assistance, and prepare for the next warning.",
}

function M.open(d)
    local empty = true
    for _ in pairs(d) do empty = false; break end
    if empty then
        d.schema, d.calibratedKey, d.lastEvent = 1, "", -1
        d.disruptedUntil, d.revision, d.lastSurvived = 0, 0, -1
    end
    assert(d.schema == 1 and type(d.calibratedKey) == "string", "Invalid observer schema")
    if d.lastSurvived == nil then d.lastSurvived = -1 end -- Additive 0.2.0 development migration.
    assert(Campaign.finite(d.lastEvent) and d.lastEvent % 1 == 0 and d.lastEvent >= -1 and
        Campaign.finite(d.disruptedUntil) and d.disruptedUntil >= 0 and
        Campaign.finite(d.revision) and d.revision >= 0 and d.revision % 1 == 0 and
        Campaign.finite(d.lastSurvived) and d.lastSurvived >= -1, "Invalid observer state")
    return d
end

function M.forecastKey(f)
    if not f or f.active or not Campaign.finite(f.start) or f.start < 0 then return nil end
    return tostring(f.id) .. ":" .. tostring(f.start)
end

function M.snapshot(d, f, hour)
    local s = { revision = d.revision, available = f ~= nil,
        disruptedHours = math.max(0, d.disruptedUntil - hour), lastEvent = d.lastEvent }
    if not f then return s end
    s.active, s.direction, s.event = f.active, f.direction or "UNRESOLVED", f.id
    local key = M.forecastKey(f)
    s.calibrated = key ~= nil and d.calibratedKey == key
    if key then
        local errorHours = s.calibrated and 0.25 or 2
        s.earliest = math.max(0, f.start - hour - errorHours)
        s.latest = math.max(0, f.start - hour + errorHours)
    end
    return s
end

function M.begin(d, f, hour, ms, x, y, z, alive, channel)
    if not alive or not Campaign.near(x, y, z) then return nil, "visit_relay" end
    local key = M.forecastKey(f)
    if not key or f.start <= hour then return nil, "no_forecast" end
    if d.calibratedKey == key then return nil, "already_calibrated" end
    return { key = key, started = ms, step = 1, channel = channel }, "tuning"
end

function M.step(session, f, ms, channel, alive, near)
    if not session then return false, "no_session" end
    if session.step > 3 then return false, "incomplete" end
    if not alive or not near or session.key ~= M.forecastKey(f) then return false, "interrupted" end
    local elapsed = ms - session.started
    if elapsed < 0 or elapsed > 25000 then return false, "expired" end
    if elapsed < session.step * 4000 then return false, "too_early" end
    if channel ~= session.channel then return false, "wrong_channel" end
    session.step = session.step + 1
    return true, "tuning"
end

function M.finish(d, session, f, ms, alive, near)
    if not session or not alive or not near or session.key ~= M.forecastKey(f) then
        return false, "interrupted"
    end
    local elapsed = ms - session.started
    if session.step ~= 4 or elapsed < 15000 or elapsed > 25000 then return false, "incomplete" end
    if d.calibratedKey == session.key then return false, "already_calibrated" end
    d.calibratedKey, d.revision = session.key, d.revision + 1
    return true, "calibrated"
end

-- Poll real owner completion identity, not a parallel event timer. No item reward.
function M.observe(d, f, hour)
    if not f then return false end
    if d.lastEvent == -1 or d.lastSurvived == -1 then
        d.lastEvent, d.lastSurvived = f.id, f.survived; return false
    end
    if not f.active and f.completed and f.id > d.lastEvent then
        d.lastEvent = f.id
        local success = f.survived > d.lastSurvived and f.spawned > 0
        d.lastSurvived = f.survived
        if not success then return false end -- Upstream abort also sets CompletionRecorded.
        d.disruptedUntil = math.max(d.disruptedUntil, hour + 24)
        d.revision = d.revision + 1
        return true
    end
    return false
end

function M.repair(d, hour)
    if d.disruptedUntil <= hour then return false end
    d.disruptedUntil = math.max(hour, d.disruptedUntil - 12)
    d.revision = d.revision + 1
    return true
end
return M

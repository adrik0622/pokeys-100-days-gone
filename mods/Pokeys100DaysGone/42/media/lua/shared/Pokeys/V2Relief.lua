-- Original bounded world-condition action, not a second mission/reputation owner.
local V = require "Pokeys/V2Rules"
local R = {key = "Pokeys100DaysGone.V2Relief", limit = 4096}

function R.enabled()
    return V.enabled() and SandboxVars.PokeysV2.RepeatRelief == true
end

local function account(key)
    return type(key) == "string" and #key > 0 and #key <= 160
end

function R.eventKey(event)
    if not V.finite(event) or event < 1 or event > 2147483647 or event % 1 ~= 0 then return nil end
    return "horde:" .. string.format("%.0f", event)
end

function R.receipt(d, key, event)
    local entries = d.records[key]
    local identity = R.eventKey(event)
    return entries and identity and entries[identity] or nil
end

function R.open(d)
    local empty = true
    for _ in pairs(d) do empty = false; break end
    if empty then d.schema, d.records, d.revision = 1, {}, 0 end
    assert(d.schema == 1 and type(d.records) == "table" and V.finite(d.revision)
        and d.revision >= 0 and d.revision % 1 == 0, "invalid relief ledger")
    assert(d.lastHour == nil or (V.finite(d.lastHour) and d.lastHour >= 0), "invalid relief clock")
    local count, unresolved, latest = 0, 0, 0
    for key, entries in pairs(d.records) do
        assert(account(key) and type(entries) == "table", "invalid relief account")
        local any = false
        for identity, receipt in pairs(entries) do
            any, count = true, count + 1
            assert(count <= R.limit and type(receipt) == "table"
                and R.eventKey(receipt.event) == identity, "invalid relief event")
            assert(receipt.status == "pending" or receipt.status == "applied"
                or receipt.status == "incident", "invalid relief status")
            assert(receipt.phase == "reserved" or receipt.phase == "consuming"
                or receipt.phase == "standing" or receipt.phase == "repair"
                or receipt.phase == "complete", "invalid relief phase")
            assert(V.finite(receipt.hours) and receipt.hours >= 0
                and V.finite(receipt.consumed) and receipt.consumed >= 0
                and receipt.consumed <= 2 and receipt.consumed % 1 == 0, "invalid relief consumption")
            assert(receipt.delta == nil or (V.finite(receipt.delta) and receipt.delta >= 0), "invalid relief rate")
            for _, field in ipairs({"before", "after"}) do
                assert(receipt[field] == nil or (type(receipt[field]) == "string"
                    and #receipt[field] > 0 and #receipt[field] <= 32), "invalid relief standing label")
            end
            latest = math.max(latest, receipt.hours)
            if receipt.status == "applied" then
                assert(receipt.phase == "complete" and receipt.consumed == 2
                    and receipt.delta ~= nil and receipt.before ~= nil and receipt.after ~= nil,
                    "incomplete applied relief")
            else
                unresolved = unresolved + 1
                assert(receipt.phase ~= "complete" and type(d.pending) == "table"
                    and d.pending.key == key and d.pending.event == receipt.event,
                    "unlatched relief incident")
            end
        end
        assert(any, "empty relief account")
    end
    assert(unresolved <= 1, "multiple relief incidents")
    if d.pending ~= nil then
        assert(type(d.pending) == "table" and account(d.pending.key)
            and R.eventKey(d.pending.event) and unresolved == 1, "invalid relief reservation")
    end
    assert(count == 0 or (d.lastHour ~= nil and d.lastHour >= latest), "missing relief clock")
    return d
end

function R.allowed(d, key, event, hour, near, introduction, recovery)
    if not account(key) then return false, "bridge_unavailable" end
    if not V.finite(hour) or hour < 0 or (d.lastHour and hour < d.lastHour) then
        return false, "clock_unavailable"
    end
    if d.pending then return false, "inspection_required" end
    if not near then return false, "visit_relay_alive" end
    if introduction and introduction ~= "applied" then return false, "inspection_required" end
    if not introduction then return false, "deliver_first" end
    if recovery == nil then return false, "recovery_unavailable" end
    if not V.finite(recovery) or recovery <= 0 then return false, "no_relief_needed" end
    if not R.eventKey(event) then return false, "recovery_event_unknown" end
    if R.receipt(d, key, event) then return false, "relief_already_done" end
    return true, "relief_ready"
end

function R.reserve(d, key, event, hour)
    local identity = R.eventKey(event)
    if not account(key) or not identity or not V.finite(hour) or hour < 0
        or (d.lastHour and hour < d.lastHour) then return nil, "clock_unavailable" end
    if d.pending then return nil, "inspection_required" end
    if R.receipt(d, key, event) then return nil, "relief_already_done" end
    local count = 0
    for _, entries in pairs(d.records) do for _ in pairs(entries) do count = count + 1 end end
    if count >= R.limit then return nil, "relief_ledger_full" end
    local receipt = {event = event, hours = hour, status = "pending", phase = "reserved", consumed = 0}
    d.records[key] = d.records[key] or {}
    d.records[key][identity] = receipt
    d.pending, d.lastHour = {key = key, event = event}, hour
    d.revision = d.revision + 1
    return receipt
end

return R

-- Optional dependency audit: execute installed upstream Lua READ-ONLY with
-- mocked engine boundaries. This is source-behavior evidence, not a game test.
-- Usage: lua5.1 scripts/audit_screamer.lua /absolute/path/to/ScreamerZed/42
local root = assert(arg[1], "Provide the installed ScreamerZed/42 directory")
assert(root:sub(1, 1) == "/" and not root:find("/%.%./"), "Expected absolute dependency path")
package.path = root .. "/media/lua/shared/?.lua;" .. package.path

local function fixture()
    ScreamerZed = nil
    package.loaded["ScreamerZed/SZ_Config"] = nil
    package.loaded["ScreamerZed/SZ_Appearance"] = nil
    local world = {ms = 100000, paths = 0, births = 0, calls = 0}
    local function list(entries)
        return {size = function() return #entries end,
                get = function(_, index) return entries[index + 1] end}
    end
    local function actor(x, id)
        local value = {x = x, data = {}, dead = false}
        function value:getX() return self.x end
        function value:getY() return 0 end
        function value:getZ() return 0 end
        function value:isDead() return self.dead end
        function value:getModData() return self.data end
        function value:getOnlineID() return id end
        function value:getTarget() return nil end
        function value:pathToSound() world.paths = world.paths + 1 end
        return value
    end
    world.player = actor(0, 1)
    world.zombies = {actor(70, 2)}
    local zombies = list(world.zombies)
    local cell = {getZombieList = function() return zombies end}
    function cell:getGridSquare(x, y, z)
        return {getX = function() return x end, getY = function() return y end,
                getZ = function() return z end}
    end
    isClient = function() return false end
    isServer = function() return true end
    getTimestampMs = function() return world.ms end
    getGameTime = function() return {getWorldAgeHours = function() return 1 end} end
    getCell = function() return cell end
    getOnlinePlayers = function() return list({world.player}) end
    ZombRand = function() return 0 end
    ZombRandFloat = function(low) return low end
    addSound = function() end
    sendServerCommand = function() world.calls = world.calls + 1 end
    addZombiesInOutfit = function(x, y, z, count)
        assert(count == 1, "Reinspect changed spawn behavior")
        world.births = world.births + count
        world.prepared = actor(x, 3)
        world.zombies[#world.zombies + 1] = world.prepared
        return list({world.prepared})
    end
    SandboxVars = {ScreamerZed = {SpawnChance = 8, RunnerChance = 0,
                                 ScreamerRunner = false, ReactionTime = 2}}
    Events = {OnTick = {Add = function(callback) world.tick = callback end}}
    world.reload = function()
        dofile(root .. "/media/lua/server/ScreamerZed/SZ_Server.lua")
    end
    world.reload()
    function world:advance(ms)
        self.ms = ms
        self.tick()
    end
    world:advance(100000)
    assert(world.births == 1 and world.prepared, "Prepared-spawn observation changed; reinspect")
    world.player.x = world.prepared.x - 2
    world:advance(100500)
    return world
end

local before = fixture()
before.prepared.dead = true
before:advance(103000)
assert(before.calls == 0, "Death-before-call behavior changed")
print("OBSERVED (mock engine): population trigger creates ONE new prepared Screamer")
print("OBSERVED (mock engine): killing during the warning prevents the call")

local after = fixture()
after:advance(103000)
assert(after.calls == 1 and after.paths > 0, "Call/attraction setup failed")
local paths = after.paths
after.prepared.dead = true
after:advance(104000)
assert(after.paths > paths, "Post-death pulse observation changed; reinspect")
print("OBSERVED (mock engine): attraction issues another path request AFTER Screamer death")

paths = after.paths
after.reload()
after:advance(105000)
assert(after.paths == paths and after.prepared.data.ScreamerZedScreamed == true,
       "Reload-local pulse observation changed; reinspect")
print("OBSERVED (mock engine): reloading handler loses active pulse while the used flag remains")
print("NO engine, appearance, sound, networking, persistence or MP acceptance from this audit")

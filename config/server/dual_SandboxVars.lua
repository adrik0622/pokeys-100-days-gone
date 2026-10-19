-- Disposable network fixture only: no survival/combat acceptance from this world.
-- Verified against the installed 42.21.0 server's generated option comments.
-- Unspecified options retain the game's defaults. Never deploy as release settings.
SandboxVars = {
    VERSION = 6,
    Zombies = 6, -- None
    ZombieRespawn = 4, -- None
    ZombieMigrate = false,
    SurvivorHouseChance = 1, -- Never
    VehicleStoryChance = 1, -- Never
    ZoneStoryChance = 1, -- Never
    ZombieConfig = {
        PopulationMultiplier = 0.0,
        PopulationStartMultiplier = 0.0,
        PopulationPeakMultiplier = 0.0,
        RespawnHours = 0.0,
        RespawnUnseenHours = 0.0,
        RespawnMultiplier = 0.0,
    },
}

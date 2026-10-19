-- Separate, quiet V2 bridge fixture. Jeem/A-Life is deliberately absent:
-- contract/item handling can be tested without claiming faction integration.
SandboxVars = {
    VERSION = 6, Zombies = 6, ZombieRespawn = 4, ZombieMigrate = false,
    SurvivorHouseChance = 1, VehicleStoryChance = 1, ZoneStoryChance = 1,
    ZombieConfig = {
        PopulationMultiplier = 0.0, PopulationStartMultiplier = 0.0,
        PopulationPeakMultiplier = 0.0, RespawnHours = 0.0,
        RespawnUnseenHours = 0.0, RespawnMultiplier = 0.0,
    },
    TM42 = {
        EnableKillCategory = false, EnableWalkCategory = false,
        EnableGatherCategory = true, EnableSurviveCategory = false,
        EnableRefillCategory = false, EnableMissionReset = false,
        LoadCustomMissions = true,
    },
    PokeysV2 = { Enabled = true },
}

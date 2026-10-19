-- Gather-only rewards; source audit found client-reported walking progress and
-- no A-Life NPC-shell filter in kill rewards. Do not enable those categories yet.
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
        EnableSurviveCategory = false, EnableRefillCategory = false,
        EnableMissionReset = false,
        LoadCustomMissions = false,
    },
}

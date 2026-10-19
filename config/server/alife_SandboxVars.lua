-- First bounded core trial: existing native admin spawns, not release settings.
SandboxVars = {
    VERSION = 6, Zombies = 5, ZombieRespawn = 4,
    SurvivorHouseChance = 1, VehicleStoryChance = 1, ZoneStoryChance = 1,
    ZombieConfig = {
        PopulationMultiplier = 0.01, PopulationStartMultiplier = 0.01,
        PopulationPeakMultiplier = 0.01, RespawnHours = 0.0,
        RespawnUnseenHours = 0.0, RespawnMultiplier = 0.0,
    },
    ALife = {
        Preset_ExplicitValues = true,
        Population_RatePercent = 25, Population_PartyPercent = 50,
        Population_HostileCeiling = 4,
        Population_PopulateOnStart = 1, Population_PopulateMax = 1,
        Population_SeedPerTown = 1, Population_NeighbourGroups = 1,
        TownWelcome_Enabled = false, Realistic_Outbreak = false,
        Encounters_Enabled = false, Encounters_RollPercent = 0,
        Outposts_Enabled = false, Raid_Enabled = false,
        Offline_RevengeEnabled = false, Support_Enabled = false,
        World_FactionWarfare = false,
        Offline_SquadCap = 4, Population_PersistentSquadCap = 4,
        Debug_ShowAdminTools = true,
    },
}

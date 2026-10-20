-- One debug horde birth away from the relay; no other ambient/physical pressure.
-- This is a component/recovery fixture, not a fought horde or production budget.
SandboxVars = {
    VERSION = 6, Zombies = 5, ZombieRespawn = 4,
    SurvivorHouseChance = 1, VehicleStoryChance = 1, ZoneStoryChance = 1,
    ZombieConfig = {
        PopulationMultiplier = 0.0, PopulationStartMultiplier = 0.0,
        PopulationPeakMultiplier = 0.0, RespawnHours = 0.0,
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
        Debug_ShowAdminTools = false,
    },
    ALifeJimmy = {
        Residents_Enabled = false, Bases_Raids = false, Traders_Enabled = false,
        Standing_Enabled = true, Standing_OneReputation = true,
        Standing_PlayersMayReset = false,
    },
    TM42 = {
        EnableKillCategory = false, EnableWalkCategory = false,
        EnableGatherCategory = true, EnableSurviveCategory = false,
        EnableRefillCategory = false, EnableMissionReset = false,
        LoadCustomMissions = true,
    },
    HordeNights = {
        Enabled = true, IntervalDays = 3, FirstHordeDay = 3,
        StartHour = 22, EndHour = 5, ShowHordeDayIndicator = false,
        BaseZombiesPerPlayer = 1, DayScaling = 0, HordeScaling = 0,
        ActiveHordeCap = 1, ReinforcementBatchSize = 1,
        GroupingDistance = 50, MinimumSpawnDistance = 80, MaximumSpawnDistance = 100,
        HordeApproachMode = 1, HordeSpawnArcWidth = 45, TargetUpdateMinutes = 5,
        SprinterPercentage = 0, SupplyDropsEnabled = false,
        HelicopterSupplyDropsEnabled = false, SupplyDropBanditsEnabled = false,
        DebugLogging = true,
    },
    PokeysV2 = { Enabled = true, RepeatRelief = true },
}

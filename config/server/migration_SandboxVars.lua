-- Dedicated disposable fixture: ambient population zero, explicit event births only.
-- Four is an experiment size, NOT an accepted capacity/performance budget.
SandboxVars = {
    VERSION = 6,
    Zombies = 5,
    ZombieRespawn = 4,
    ZombieMigrate = false,
    SurvivorHouseChance = 1,
    VehicleStoryChance = 1,
    ZoneStoryChance = 1,
    ZombieConfig = {
        PopulationMultiplier = 0.0, PopulationStartMultiplier = 0.0,
        PopulationPeakMultiplier = 0.0, RespawnHours = 0.0,
        RespawnUnseenHours = 0.0, RespawnMultiplier = 0.0,
    },
    HordeNights = {
        Enabled = true, IntervalDays = 3, FirstHordeDay = 1,
        StartHour = 22, EndHour = 5,
        ShowHordeDayIndicator = false,
        BaseZombiesPerPlayer = 4, DayScaling = 0, HordeScaling = 0,
        ActiveHordeCap = 4, ReinforcementBatchSize = 4,
        GroupingDistance = 50, MinimumSpawnDistance = 50, MaximumSpawnDistance = 70,
        HordeApproachMode = 1, HordeSpawnArcWidth = 45,
        TargetUpdateMinutes = 5, SprinterPercentage = 0,
        SupplyDropsEnabled = false, HelicopterSupplyDropsEnabled = false,
        SupplyDropBanditsEnabled = false, DebugLogging = true,
    },
}

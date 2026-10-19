-- Combined development trial only. Known issues are disclosed, not fixed.
-- Calendar/spoilage candidate; low ambient population is NOT release balance.
-- Event budget is finite per event, NOT a verified cross-event/global cap.
SandboxVars = {
    VERSION = 6,
    StartYear = 1, StartMonth = 10, StartDay = 17, StartTime = 2,
    TimeSinceApo = 4, DayLength = 3,
    WaterShut = 1, ElecShut = 1, WaterShutModifier = 0, ElecShutModifier = 0,
    Zombies = 5,
    ZombieConfig = {
        PopulationMultiplier = 0.05, PopulationStartMultiplier = 0.05,
        PopulationPeakMultiplier = 0.05, RespawnHours = 0.0,
        RespawnUnseenHours = 0.0, RespawnMultiplier = 0.0,
    },
    Bandits = {General_SpawnMultiplier = 0.25}, -- Native supported minimum.
    HordeNights = {
        Enabled = true, IntervalDays = 7, FirstHordeDay = 3,
        StartHour = 22, EndHour = 5, ShowHordeDayIndicator = false,
        BaseZombiesPerPlayer = 4, DayScaling = 0, HordeScaling = 0,
        ActiveHordeCap = 4, ReinforcementBatchSize = 4,
        GroupingDistance = 50, MinimumSpawnDistance = 60, MaximumSpawnDistance = 80,
        HordeApproachMode = 1, HordeSpawnArcWidth = 45, TargetUpdateMinutes = 5,
        SprinterPercentage = 0,
        SupplyDropsEnabled = false, HelicopterSupplyDropsEnabled = false,
        SupplyDropBanditsEnabled = false, DebugLogging = true,
    },
}

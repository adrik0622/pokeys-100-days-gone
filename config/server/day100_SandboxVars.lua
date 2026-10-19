-- Development survival candidate. NEVER copy over an existing world.
-- Independent of zero-population fixtures; not balance/performance accepted.
-- Calendar: 100 days after 1993-07-09 is 1993-10-17.
-- Native TimeSinceApo is month-granular (enum 4 = 3 months), not an exact 100-day simulation.
SandboxVars = {
    VERSION = 6,
    StartYear = 1, StartMonth = 10, StartDay = 17, StartTime = 2,
    TimeSinceApo = 4,
    DayLength = 3,
    WaterShut = 1, ElecShut = 1,
    WaterShutModifier = 0, ElecShutModifier = 0,
    Zombies = 4,
    ZombieConfig = {
        PopulationMultiplier = 0.5, PopulationStartMultiplier = 0.5,
        PopulationPeakMultiplier = 0.5,
    },
    HordeNights = {
        -- Fail-safe: do not ship an enabled director until cap/offline/direction gates pass.
        Enabled = false, IntervalDays = 7, FirstHordeDay = 3,
        StartHour = 22, EndHour = 5, ShowHordeDayIndicator = false,
        BaseZombiesPerPlayer = 4, DayScaling = 0, HordeScaling = 0,
        ActiveHordeCap = 16, ReinforcementBatchSize = 4,
        HordeApproachMode = 1, HordeSpawnArcWidth = 45,
        MinimumSpawnDistance = 60, MaximumSpawnDistance = 90,
        SprinterPercentage = 0,
        SupplyDropsEnabled = false, HelicopterSupplyDropsEnabled = false,
        SupplyDropBanditsEnabled = false,
    },
}

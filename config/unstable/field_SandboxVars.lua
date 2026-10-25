-- Fresh-world friends' field preset, NOT an accepted release or retained fixture.
-- Deliberately partial: omitted settings use the installed upstream defaults.
-- Inspect the generated full server sandbox before hosting; never hot-swap saves.
SandboxVars = {
    VERSION = 6,
    -- Calendar fiction: 100 days after July 9; native age is month-granular.
    StartYear = 1, StartMonth = 10, StartDay = 17, StartTime = 2,
    TimeSinceApo = 4, DayLength = 3,
    WaterShut = 1, ElecShut = 1,
    WaterShutModifier = 0, ElecShutModifier = 0,
    Zombies = 4,
    ZombieConfig = {
        PopulationMultiplier = 0.5, PopulationStartMultiplier = 0.5,
        PopulationPeakMultiplier = 0.75,
    },
    ALife = {
        -- Explicit values prevent a difficulty/world preset replacing these knobs.
        Preset_ExplicitValues = true,
        Population_RatePercent = 100, Population_PartyPercent = 100,
        Population_HostileCeiling = 16, Population_PopulateMax = 40,
        World_SimRadius = 90,
        Warning_Enabled = true, Warning_ChancePercent = 100,
        Warning_RaidChancePercent = 100, Warning_HoldSeconds = 12,
        Raid_WarningHours = 6, Raid_MaxAttackers = 8,
        Fair_FirstContactGrace = 3, Fair_WarningLead = 2,
        Debug_ShowAdminTools = false,
    },
    ALifeJimmy = {
        Standing_Enabled = true, Blame_Fair = true,
        Standing_PlayersMayReset = false,
        Base_MaxResidents = 6,
        -- All other native features/default experimental switches remain upstream.
    },
    HordeNights = {
        Enabled = true, FirstHordeDay = 7, IntervalDays = 7,
        StartHour = 22, EndHour = 5, ShowHordeDayIndicator = true,
        BaseZombiesPerPlayer = 12, DayScaling = 0, HordeScaling = 0,
        ActiveHordeCap = 48, ReinforcementBatchSize = 6,
        MinimumSpawnDistance = 80, MaximumSpawnDistance = 120,
        SprinterPercentage = 0,
        SupplyDropsEnabled = false, HelicopterSupplyDropsEnabled = false,
        SupplyDropBanditsEnabled = false, DebugLogging = false,
    },
    MilitaryDrop = {
        CooldownHours = 72, DropMinDistance = 200, DropMaxDistance = 500,
        MinZombies = 3, MaxZombies = 12,
        -- Disable random crash/fire escalation for the first social field session.
        CrashChance = 0, CrashStormBonus = 0, CrashGunfire = false,
        TrustErosion = false, DebugLog = false,
    },
    TM42 = {
        EnableDefaultMissions = true, LoadCustomMissions = false,
        EnableKillCategory = false, EnableWalkCategory = true,
        EnableGatherCategory = true, EnableSurviveCategory = true,
        EnableMissionReset = true, MissionResetDays = 7,
    },
    VFE = {
        GunLootMulti = 1.0, HouseWeaponsMulti = 1.0,
        RemoveVanillaGuns = false, PeriodCorrect = false,
    },
    PlayablePool = {
        AllowSoloPractice = true, AllowSpectators = true, AllowBots = true,
        CasualCallRules = true, EnableBetaMinigames = false,
        EnableDarts501 = true, EnableWordle = true, EnableBlackjack = true,
        EnableHoldem = true, EnableSolitaire = true, EnableChess = true,
        EnableCheckers = true, EnableConnect4 = true,
        HouseStake = 50, EnableRecords = true, TurnTimeoutSeconds = 90,
        DisconnectGraceSeconds = 120, ParkedSessionMinutes = 2,
        BoredomReliefPerTurn = 5, StressReliefPerTurn = 0,
        UnhappinessReliefPerTurn = 0,
    },
    RarityThreads = {
        RarityMultiplier = 1.0, AllowDrawbacks = true,
        RollExistingInventory = false, EnableVirtualStamina = false,
        DebugLogging = false,
    },
    -- Author labels current independent-spawn build PRETEST. No fixed relic reward.
    -- Easy: 2x health, regional cap 2, five ordinary zombies released on death.
    CSI_Bloated = { Enabled = true, Difficulty = 1 },
    CheolsSpecialInfectedFramework = {
        FakeSurvivorNaturalSpawnEnabled = true,
        FakeSurvivorNaturalSpawnChancePercent = 10,
        FakeSurvivorNaturalSpawnCap = 1,
        FakeSurvivorHealthMultiplier = 1.0,
        -- Only StartDay is registered in this Night Walker's installed sandbox file.
        -- Other source-read settings are not invented as working server knobs here.
        NightWalkerStartDay = 14,
    },
    CommonSense = {
        PryingMechanic = true, PrySafeDoors = false,
        ReinforcedDoorLevel = 8, PryingChanceMultiplier = 1,
        GunStats = false, RemoveBulletsByHand = false,
        RemoveBulletsByHandAnimation = false,
    },
    LSHygiene = { HygieneNeedMultiplier = 0, BladderNeedMultiplier = 0 },
    LSComfort = { ComfortNeedMultiplier = 0, ComfortNoImpact = true },
    LSArt = { BeautyOutdoors = false, BeautyNeedDecayRate = 1, BeautyNeedStrength = 1 },
    LSMeditation = { RemoveLevitation = true },
    LS = { DynamicTraits = false },
    ImmersiveSnow = { SnowSlowdown = false, SnowWetness = false },
}

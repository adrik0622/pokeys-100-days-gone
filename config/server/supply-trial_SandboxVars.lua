-- Fixture only: test ordinary radio delivery before adding threat or code puzzles.
SandboxVars = {
    VERSION = 6, Zombies = 6, ZombieRespawn = 4, ZombieMigrate = false,
    SurvivorHouseChance = 1, VehicleStoryChance = 1, ZoneStoryChance = 1,
    ZombieConfig = {
        PopulationMultiplier = 0.0, PopulationStartMultiplier = 0.0,
        PopulationPeakMultiplier = 0.0, RespawnHours = 0.0,
        RespawnUnseenHours = 0.0, RespawnMultiplier = 0.0,
    },
    MilitaryDrop = {
        Frequency = 900.0, AuthCode = 1, CooldownHours = 6,
        DropMinDistance = 40, DropMaxDistance = 60,
        MinZombies = 0, MaxZombies = 0, CaseRolls = 1,
        RequisitionBudget = 25, RequisitionExplosives = false,
        DecoyEnabled = false, CrashChance = 0, CrashStormBonus = 0,
        CrashGunfire = false, CrateSmokeMinutes = 0,
        TrustErosion = false, DebugLog = true,
    },
}

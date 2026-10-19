# Approved scope changes

The original [PROJECT_BRIEF.txt](../PROJECT_BRIEF.txt) is preserved unchanged. This dated record overrides only the specific requirements listed below; it does not retroactively change test evidence or waive unrelated quality requirements.

## SC-003 — 2026-10-18: consequence, not an anti-player-killing policy; A-Life/Jeem trial

**Correction:** the user explicitly clarified that there is no anti-player-killing policy. The pillar is consequence: every action should have effects players can feel, including killing another player. Earlier anti-PK/anti-griefing framing in the v2 concept and our explanation was an incorrect inference. SC-002's historical discussion remains below, but this clarification governs current design.

**Current design:** costs, benefits, danger, resource/time/noise effects, relationships, opportunities and persistent world changes can all be consequences. Violence may anger one faction and earn another's respect; mercy, concealment, cooperation and inaction also have causal results. Do not assume consequences must deter PvP, classify all player kills as murder, or add an omniscient universal punishment. Factions respond according to values, interests and what they know. Prevent duplicate/forged effects without treating legitimate play choices as exploits. Reuse demonstrated upstream systems before writing replacements.

**Testing approval:** proceed with Project A-Life and Jeem Extension, testing A-Life alone first to identify ownership/compatibility, then the combination. Disable Bandits in those isolated profiles; do not uninstall it or alter the retained v1 encounter/integrated worlds. Existing PVP=false is a smoke-fixture setting, not a final product policy; a future isolated PvP attribution test can be designed separately. No global settings or collection promotion follows automatically from this experiment. Source/automated/engine evidence remain separate.

## SC-002 — 2026-10-18: fit-for-purpose engineering and the v2.0 living world

**Original ask/policy:** the brief's spirit section emphasized inexpensive staged representations of a living world. Section 4 prescribed settings → maintained integration → patch → custom for every requirement. Continuous NPC simulation, a full economy and generic quest infrastructure were deferred from the bounded v1.0 product.

**User's clarification and expansion:** staging is appropriate when it is the simplest effective solution, but simple original engineering may be better. Necessary entity/NPC rewrites are eligible, with their substantial maintenance acknowledged. The texture-map example illustrates openness to efficient state tracking, not a request to implement a GPU-backed entity engine. v1.0 establishes the foundation; v2.0 should express the spirit through a changing living world, rewarding optional minigames, pervasive faction relevance and decisions with tradeoffs. Investigate The Mission, Random Zombies, Save Our Station, contested/horde/reputation-requested airdrops and other available solutions before deciding what to write. Most factions should disapprove of player killing; a morally gray faction should respect it. v4.0 is the provisional major-polish target, not a firm release commitment.

**Current rule:** choose the simplest effective solution over its lifetime, comparing player-visible causality, exact-build/MP feasibility, implementation/integration, runtime and maintenance costs. Staging, abstract simulation, continuous simulation and custom code are alternatives to evaluate, not a moral hierarchy. No mandatory exhaustion of mod options before writing a demonstrably smaller original feature. More invasive rewrites need a scoped experiment and cost/risk review before implementation; permission to consider them is not a mandate for a new engine.

**Boundary/acceptance:** v2 design/research and staged follow-on development are in scope. Candidate descriptions are not selection, subscription, collection membership or runtime acceptance. Preserve the current v1 fixtures and unfinished acceptance. SC-001's v1.1 leader target remains unless separately reprioritized. Do not silently enable PvP, replace the group-wide ledger, adopt every mod or promise infinite content. Baseline survival must remain useful without minigames/faction chores; meaningful responsibility must distinguish aggression, self-defense, accidents and ambiguous attribution. Quality/recovery/performance checks continue during feature work; major presentation/balance polish may come later.

**Implementation plan and evidence:** [v2 concept, outcomes, next three tasks](V2_LIVING_WORLD.md), [mod survey and actual installed airdrop seams](V2_MOD_SURVEY.md). This sweep changes documentation/research fingerprints only; gameplay/source version remains 0.3.0.

## SC-001 — 2026-10-18: directing leader moves from mandatory v1.0 to v1.1

**Original ask:** brief objective D required one recognizable horde leader with a readable appearance/sound and an actual coordination effect. Killing it must stop that effect while existing zombies remain dangerous. M4, the horde/leader test card and definition-of-done item 4 included the leader in the mandatory integrated slice.

**Discussion and approval:** user asked whether this belongs in v1.0 and whether existing mods could supply it. Recommendation was to defer the full feature, while allowing one bounded trial of a simpler existing calling/rallying zombie. User approved: “Sure, let's record the original ask, and how we've modified that. Then continue with integrating and testing.”

**Revised release boundary:**

- **v1.0 core:** preparation → forecast → horde pressure → visible faction aftermath → recovery, with presentation, human encounters/standing and optional calibration. A directing leader is **not required** to release v1.0.
- **v1.0 optional:** a simple Screamer-based tactical threat may be included only if a narrow compatibility trial proves useful, recognizable and multiplayer-safe without substantial custom AI/networking or replacing the selected horde owner. It is not promised content and must not delay the core campaign.
- **v1.1 target:** the original event-linked recognizable leader, bounded coordination, death stopping coordination, persistent identity and ownership/unload/restart handling. No stat-buff substitute is called fulfillment of that original ask.

**Acceptance changes:** remove mandatory leader/leader-death assertions from the v1.0 M4 slice, horde test card and definition-of-done item 4. Keep forecast, player/faction impact, persistent aftermath, ordinary survivors and the other multiplayer/restart/repeated-cycle checks. If an optional Screamer is included, test its actual effects, limits, shared visibility/audio and lifecycle separately. All other original requirements remain unless separately amended; pinned bugs are disclosed, not declared fixed.

**Reason:** current owner exposes useful event/tag/path seams but no verified leader integration. Requiring a custom entity lifecycle would put disproportionate uncertainty on the first release. The campaign loop can stand on its own; leader tactics are a follow-on enhancement.

### Candidate evidence (author documentation, not our runtime acceptance)

Reviewed 2026-10-18:

- [Screamer Zed B42](https://steamcommunity.com/sharedfiles/filedetails/?id=3756523429), Mod ID `ScreamerZed`: distinctive zombie, pre-call warning/cancellation on death, existing loaded zombies converge; configurable runner conversion, no new spawns claimed. Author claims SP/MP and commented on 42.20. Exact 42.21/Horde Nights behavior must be inspected/tested. Author explicitly asks not to copy code; dependency reference only.
- [Dynamic Evolution Z](https://steamcommunity.com/sharedfiles/filedetails/?id=3676814360): configurable leader/evolution/migration layers, advertised gathering/cohesion/Howler behavior and B42 MP. Broader overlap; not selected or installed by this decision.
- [Nocturnal Reign](https://github.com/CosmicQ/pz-nocturnal-reign): documented pack gathering/alerts and modular Lord mechanics; author reports 42.19 dedicated tests, not our 42.21 stack. Public MIT license does not establish engine compatibility. Not selected.
- [Hordes Alpha 0.7.2](https://steamcommunity.com/sharedfiles/filedetails/?id=3618306391&searchtext=hordes): leader-following behavior, but author warns of MP synchronization problems and recommends SP. Not selected.

### Bounded trial / stopping rule

Inspect the actual Screamer payload and isolate it before any Horde Nights combination. Prefer configuration and public hooks; do not copy/patch its source or add a competing director. Check dedicated startup, visible identity/call and an actual convergence/death consequence; then shared observation and reconnect/restart if the first seam works. If source inspection already shows a substantial dedicated ownership/persistence gap or the runtime trial fails, record it, defer the optional feature and continue core campaign integration. Subscription/download is not collection membership or gameplay acceptance. Existing saves and normal client settings remain untouched.

**Outcome:** the source audit of downloaded Screamer Zed 1.1.12 met the stopping rule: new prepared births require accounting, rally requests continue after death, and handler-local active state is not preserved on reload. Reproduced those source behaviors with actual upstream Lua and mocked boundaries; no engine/MP test claimed. Candidate deferred, never enabled or added to the collection. [Audit](M4-optional-screamer.md). Core combined campaign join/UI/restart work continued without it; [evidence](M4-01-integrated.md).

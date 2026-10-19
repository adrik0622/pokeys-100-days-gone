# v2.0 — the living-world expansion

Design baseline: 2026-10-18, approved direction [SC-002](SCOPE_CHANGES.md). This is a concept and staged implementation plan, not delivered gameplay or a selected dependency stack. Source remains 0.3.0 development; [v1 acceptance](STATUS.md) is unfinished. Mod evidence and specific integration gaps: [V2_MOD_SURVEY](V2_MOD_SURVEY.md).

## The corrected guiding principle

> Build the most convincing, consequential world with the simplest effective engineering. Use “show business” where staging works; use real simulation or original systems where they produce a better result. Choose per problem, and account for runtime, integration and long-term maintenance—not just initial code size.

The goal is not to fake everything or simulate everything. It is a world that remembers, changes for understandable reasons, and lets players influence what happens next. Repeated sessions should generate new situations, not merely reset the same reward checklist. Endless replayability is an aspiration, not a promise of unlimited authored content.

For each substantial feature, record: player-facing outcome; what must actually remain true off-screen; viable approaches; engine/network hooks; implementation plus integration cost; measured runtime/storage/network cost; update/maintenance burden; smallest discriminating experiment; rollback. A small original Lua system can beat a giant mod stack. A maintained simulation can beat an ever-growing collection of staging exceptions. Neither wins by ideology.

An entity/NPC rewrite is eligible when required, but first bound the capability, ownership/network/save changes, compatibility surface, regression matrix and ongoing maintenance. Do not start a general engine rewrite to solve one encounter. A texture map is one possible representation, not a demonstrated solution: storing stats cheaply does not itself provide engine persistence, authoritative networking, pathfinding or ownership. Inspect those seams before choosing a data structure.

Default hypothesis to test: persistent logical factions/squads/events, cheap bounded off-screen updates, physical actors near observers. Preserve identity, casualties, resources and consequences across representation changes. Do not resurrect dead named people, reroll a losing encounter when players leave, spawn visibly, or claim an empty camp was defended by actors the system never accounted for. More detailed simulation is justified where this approach cannot meet the outcome.

## What v2 should feel like

Players loot and survive normally, but learn who needs the supplies, who controls the route, who can offer information or help, and who loses if they take another side. Factions should be relevant to most meaningful expeditions and resource choices—not demand a menu for every door or punish every keystroke.

The proposed first complete loop:

Faction shortage → choose a job or independent survival → earn trust/access → request or discover a contested shipment → choose negotiation, evasion, recovery or force → supplies/casualties change faction conditions → radio/contact reports the result → recovery or a different opportunity.

Example: Mutual Aid needs medicine; Observers offer route intelligence; a gray-market group wants the same shipment. Delivering it improves clinic aid but uses supplies the players could keep. Diverting it buys another faction's access while delaying clinic recovery. Waiting can let a rival claim it, with visible aftermath. Combat is one option, not the universal reward generator. Outcomes must follow actual choices and tracked events, not arbitrary punishment.

Three existing identities are provisional, not a lore commitment: Mutual Aid (civil protection/supplies), Field Observers (information/infrastructure), Road Reclaimers (possible gray-market role). Decide whether Reclaimers can credibly fill that role after NPC-owner inspection; do not silently turn the existing always-hostile scout into an ally. A fourth faction is not required just to add another reputation meter.

## Minigames: worthwhile, optional and bounded

- Keep vanilla survival and the useful baseline action. Existing forecast calibration is the reference: skipping still warns; playing improves precision. Do not worsen the baseline to make a minigame attractive.
- Offer understandable benefits: narrower information uncertainty, less noise, fewer consumed parts, better-quality salvage, or a negotiated convenience. Measure total time including UI/travel; a nominal time saving that costs more time is not a benefit.
- Give choices between resources, risk, time and skill. An accessible non-reflex alternative should remain viable; interruption/cancellation should not erase unrelated progress. Avoid compulsory daily tuning, repeated popup chores and permanent advantages gated behind reflex ability.
- One reward/event identity, server checks, cooldowns, diminishing returns and no easy repeat/XP/item minting. Cooperative roles may help without multiplying rewards per connected account.
- First deepen calibration's relevance to an expedition. Only then consider one salvage/repair/lockpicking activity. Check native interactions before replacing them. Do not make Neat Lockpicking's replacement hotwire compulsory without a scoped optionality/accessibility solution.

## Consequential reputation and violence

User clarification [SC-003](SCOPE_CHANGES.md): **we do not have an anti-player-killing policy. The pillar is consequence, and every action should have consequences players can feel.** Reputation is one channel, not the whole system: resource use, noise, time, danger, lost opportunities, changed relationships and persistent world state also count. Benefits, costs and mixed tradeoffs are all valid; a numerical penalty or popup for every input is not required. Cooperation, violence, mercy, concealment and inaction must fit the same causal world.

Faction NPC deaths and player killing need contextual consequences, not universal punishment. Most factions disapproving and a gray faction respecting a kill are possible value-driven responses, not a mandate to prevent or discourage all PvP. Implementation below is proposed, not delivered. Existing PVP=false and schema-1 standing remain unchanged in retained fixtures; that setting does not establish a final gameplay policy.

| Decision/event | Proposed response | Important distinction |
| --- | --- | --- |
| Supply a shortage, repair a relay, honor a commitment | Bounded access/trust and an actual stock/service change | Same completion cannot pay via both mission mod and companion |
| Attack/kill a neutral or allied faction NPC | Loss with that faction; possible bounded allied-faction response | Faction ID, actor, intent/incident and prior hostility matter |
| Fight an actual hostile attacker | Attacker faction may resent casualties; protected factions need not condemn defense | Do not give every NPC death the same universal penalty |
| Kill another player | Felt faction/world consequences according to values, relationships and circumstances; some may disapprove, others approve | Establish cause/actor/context; do not label every kill murder or infer a server punishment |
| Gray faction learns of a player killing | Respect, access or changed opportunities under its values, with opposing costs where appropriate | Prevent duplicate/forged/meaningless repeat rewards; legitimate violent play is not automatically an exploit |
| Self-defense, accident, agreed duel or unknown cause | Separate incident classification; unknown held for review, no guessed punishment | A last-hit pointer alone does not prove murder |
| Theft, diversion, mercy or betrayal | Ownership/witness/contract-sensitive consequence, reported to the player | Explain who knows and why; no unexplained omniscient sanctions |

Proposed responsibility model: personal reputation/history for attributable actions; shared campaign conditions and selected cooperative access. Preserve existing group standing through a reviewed migration; any consequences spreading to a party need a coherent affiliation/knowledge rule, not accidental bookkeeping. Define what persists across character death before implementation; do not key durable identity solely to transient online ID, body or display name. Retain only necessary private account identity, never expose it in public logs.

Choose one authority for each reputation balance. If A-Life/Jeem or another owner supplies reliable standing, integrate project rules into it or adopt a single explicit projection; do not create two meters that independently reward and contradict one another. Existing v1 group data must not be destructively “converted” from guessed upstream values.

Incident design must cover repeat/deferred death, disconnect, zombie infection, fire/vehicle/indirect deaths, ownership handoff, damage packets arriving late and ambiguous evidence. Initial supported causes can be narrow, with unsupported causes disclosed and no gray-faction payout for unverifiable kills. Test false attribution and both gun-damage paths before claiming universal coverage.

Use bounded witness/report or explicit campaign-knowledge rules: nearby witnesses, victims' affiliations and reports can spread news. Concealing a deed can itself be a consequential choice; eliminating witnesses is not automatically an exemption from an anti-PK policy because no such policy exists. Assess how knowledge, missing people, resource loss and retaliation remain coherent. Do not add omniscient sanctions just to discourage violence.

Reputation thresholds and numeric gains/losses are not balanced yet. Respect is not moral approval, and consequences need not be deterrents. Avoid unbounded reward duplication while preserving the legitimacy of player choices. Reuse A-Life/Jeem's demonstrated systems wherever they fit; custom rules should close an evidenced gap rather than create a parallel consequence engine.

## Systems and ownership boundaries

| Concern | Proposed smallest responsibility | Dependency decision |
| --- | --- | --- |
| World continuity | Stable faction/site/squad/event IDs; bounded stock, security, need and last-update state | Adopt a demonstrated upstream simulation if suitable; otherwise explicit Lua tables and coarse updates |
| Physical NPCs | One spawn/AI/health/network owner, with faction mapping and reliable lifecycle observations | Compare existing Bandits with A-Life in separate worlds; never enable both |
| Horde pressure | One physical routing/spawn authority; all project events reserve from a shared budget | Keep Horde Nights candidate unless a measured replacement is better; no second uncontrolled director |
| Airdrops | One fulfillment/claim/expiry authority; project authorization only where missing | Compare Horde Nights path with Military Drop; disable overlapping automatic drops in a future trial |
| Contracts/reputation | One completion and reward authority; project-specific moral/resource rules | Inspect The Mission and selected faction owner before writing duplicate infrastructure |
| Radio/UI/minigames | Read the same persisted event/outcome, present causes and alternatives | Do not invent radio content unrelated to real state or assume native radio delivery already works |

Proposed drop lifecycle: authorize → reserve cost/budget → schedule and announce → approach/materialize → contest → resolve ownership/delivery → record consequences → recovery/expiry. Stable IDs and pending-operation handling precede physical effects. Already-created/ambiguous results must not blindly retry after restart. A dispatched client request is not proof guards exist; an emptied crate is not proof of who received or delivered its goods.

Start with one active objective and tiny encounters; initial development counts are not safe release caps. Budget NPCs, newly spawned zombies, surviving prior event bodies, ambient pressure, loot and simultaneous split-player locations separately. Prefer attracting existing zombies where that produces the desired pressure. New births require accounting and clear space/visibility rules. Never refill on each approach or target offline bases just because another player keeps the server alive.

Catch up off-screen state in bounded steps with explicit empty-server rules, not map-wide per-frame scans or hours of catch-up on login. Faction struggle may continue abstractly; destructive offline player-base attacks remain disabled unless separately agreed. Infrastructure failure cannot silently disable every useful warning or force a maintenance job each session.

## Release roadmap

| Stage | Player-facing outcome | Exit boundary |
| --- | --- | --- |
| v1.0 foundation (still in development) | Reliable presentation/survival, minimal factions, forecast/pressure/aftermath/recovery and optional calibration | Existing amended acceptance remains; planning v2 does not declare it passed |
| v1.1 leader target (SC-001) | Original readable, killable directing leader | Still a target, not reinstated as v1 or silently promised in v2; reconsider ordering explicitly if an upstream solution makes it cheap |
| v2.0 spirit | Connected faction needs/jobs, responsive world state, meaningful reputation, one contested supply loop, optional active-play incentive | End-to-end consequences persist; repeat with different choices; opt-out remains viable; limited supported violence attribution disclosed |
| v3.0 depth, provisional | More event/mission combinations, locations, faction strategies and possibly richer simulation | Add breadth only after the connected loop works; exact feature list remains open |
| v4.0 major polish, provisional | Coherent onboarding, presentation/audio, accessibility refinement and extensive tuning | Not a reason to defer correctness, baseline accessibility, save safety or regression checks now |

v2 acceptance should demonstrate: at least two meaningfully different responses to the same need; a persistent changed service/world condition; drop contested by the chosen NPC owner and/or a bounded zombie threat; a request denied below requirements and fulfilled exactly once above them; clear cooperation/violence consequences; baseline vs minigame/skip/cancel; restart during authorization/flight/contest; owning client leaving; split groups and unloaded survivors. Run repeated ordinary cycles, not just forced debug rewards. Actual NPC/player damage and shared observation remain engine checks. No 4–8 capacity claim until measured with appropriate clients/players.

Keep a known baseline checkpoint while v2 uses opt-in profiles/worlds. Foundation acceptance and source/policy work can proceed independently; no need to wait for a perfect v1 release before researching v2, and no need to call v1 complete to make progress.

Effort assessment: authored needs and pure policy rules are relatively small original work; supported bridges are moderate integration work if the advertised hooks exist. Persistent entity replacement, reliable indirect-death attribution and cross-owner migrations are high-uncertainty work with recurring maintenance. The three source spikes must turn those into bounded estimates before a rewrite commitment. Test-card durations below cover the engine observation only, not implementation, setup, regression or balancing; exact coding-hour promises from Workshop descriptions would be misleading.

## Next three executable tasks

Only these are detailed now; later features remain outcome-level backlog. Owner: local agent for source/code/isolated tests; user only for policy choices that genuinely change deployment. No second human is an immediate prerequisite.

### V2-01 — choose the NPC/faction capability boundary (active isolated trials)

Current [source/runtime card](V2-01-alife-jeem.md): exact inputs pinned, both dedicated profiles started, combined visible contact and one native gift consequence observed. Restart/hostile/handoff/Viewpoint gates remain; this does not adopt a replacement or waive v1 acceptance.

Outcome: a source-evidenced decision between keeping Bandits plus a small campaign layer and an isolated A-Life replacement, before substantial NPC rewrites.

Approach: user-authorized A-Life/Jeem isolated trial, A-Life alone first and then the combination, with Bandits disabled in both. Not yet accepted replacements. Prerequisite: retain current fingerprints, worlds and B-002 evidence.

1. Obtain exact upstream payloads for research through the existing scoped Steam workflow; inspect mod.info, dependencies, license, server/client entry points, faction editor/import, persistent squad/reputation ownership and spawn/death hooks. Record hashes and actual setting keys. Start with A-Life alone; add Jeem only for a demonstrated missing capability, checking its 1.4 overlap guards.
2. Produce a small option matrix: own faction definitions, NPC kill attribution, personal standing, safe/offline bases, population/raid controls, restart/unload and Viewpoint combat. Confirm public hooks rather than inventing them from advertised features. Check randomizer exclusion for NPC bodies.
3. If source permits, add one explicitly isolated trial profile and fixed controller lifecycle actions/tests; no collection promotion. Disable raids and unrelated content where supported; no blanket Java approval. One contact and one hostile actor, then a fresh process restart. Add Viewpoint only after the NPC-only seam.

Smallest engine card: ~10–15 minutes per seam after setup—meet actor, change one relationship by a controlled action, move/unload, reconnect/restart, verify same identity and one consequence; then ownership handoff with two autonomous real clients if memory permits. Inspect physical damage separately. Logs: isolated cache console/server logs. Failure clue: duplicate bodies, reset standing, wrong faction, ignored protection or B-002-like callback error; first inspect the exact owner hook/message.

Acceptance: actual supported inputs/hooks recorded, narrow engine evidence and comparative maintenance/runtime costs; not tags/startup alone. Stop after source inspection if ownership/persistence is fundamentally unavailable, document the gap and keep Bandits path available. Rollback: stop trial, retain evidence, remove only new profile/staging via a reviewed local commit; do not load v1 worlds under a replacement NPC owner.

### V2-02 — select and prove one contested-drop owner (source mapping ready; engine trial next)

Outcome: determine what can be configured versus integrated for armed contest, zombie pressure and reputation-funded requests.

Approach: compare existing HordeSupplyDrop with Military Drop; do not write a second trust/drop engine first. Prerequisites: survey's actual seams; choose the physical NPC owner before its guard adapter. Independent radio/drop source work can continue if V2-01 stalls.

1. Inspect Military Drop's exact payload/server handlers, trust hooks, request validation, horde creation/accounting and dependency discrepancy. Compare with the five pinned Horde Nights drop/guard/settings findings. Pin source versions; do not execute upstream utilities or install Java dependencies by assumption.
2. Record a choice: (a) existing Horde Nights drop + small authorization/consequence add-on; or (b) Military Drop fulfillment/trust + minimal project/NPC bridge. For (b), prove zero/controlled births where configured and keep all new births in the shared budget; disable overlapping Horde Nights drops in the trial. For A-Life, Horde Nights' hardcoded Bandits guards cannot be reused unchanged.
3. Add only the chosen isolated test profile/role-checked control. At a fixed outdoor location request one low-value crate, one guard initially, and a separate four-zombie-or-less pressure fixture. Counts are test proposals. Preserve normal survival values; never use admin force=true for an ordinary paid request.

Card: ~10–15 minutes per scenario—below-threshold refusal/no cost; eligible request; duplicate click; travel to announced location; observe guard and finite zombie approach; loot/return/deliver; restart pending and post-materialization; requester disconnect. Observe no extra crate/guards/payment. Guard dispatch logs are insufficient; prove a body and target/weapon behavior. Preserve raw logs/cache; first inspect logical drop ID and pending/dispatch flags on failure.

Acceptance: one owner, one fulfillment, trustworthy claimant/delivery evidence, bounded actors and persistent consequence. If a hook is missing, record the smallest original adapter/patch and choose based on lifetime cost. Rollback: stop disposable world, retain evidence; revert only new profile/add-on commit. No overwrite of Avery/Riley or published collection mutation.

### V2-03 — author one consequential contract, then implement only the gaps (design ready)

Outcome: one shortage → player choice → supply mission → changed faction service loop; not a generic quest platform.

Approach: inspect/configure The Mission; write small project rules/adapters only where missing. Prerequisites: V2-01/02 owner decisions for physical adapters; pure policy tests and mission-source inspection can start independently.

1. Inspect TheMission42's authoring schema, admin permissions, per-character/shared state, progress hooks, repeat/prerequisite controls and server reward validation. Check whether defaults can be disabled cleanly and external objective/reputation completion can be authoritative. If not, a small native contract table/UI in the companion is a valid simpler choice; no forced framework adoption.
2. Version one medical-shortage contract with delivery vs keep/divert outcomes, a bounded faction condition and explanatory contact/radio result. Specify exactly one reward owner. Preserve v1 schema-1 data with a reviewed schema migration/backup, or a separate v2 namespace for isolated prototypes. Test pending effects, retries, expiry and unsupported versions fail closed.
3. Implement a pure rules test matrix for NPC/player incidents (murder, hostile defense, accident, repeat/unknown) and opt-out/minigame benefits. Connect only verified attribution hooks; leave PvP disabled until A-004 resolves. Gray-faction respect and anti-farming can be tested as rules without turning PvP on. Actual PK penalties cannot be called implemented from mocks.

Card: ~10–15 minutes per branch—accept need, skip calibration and obtain useful baseline; repeat with calibration; deliver once; verify condition/access changes; retry/reconnect/restart without duplicate completion; use a fresh branch world to keep/divert and compare visible consequences. Source/rules checks are separate from engine packets and human incentive feedback. Failure: two payouts, unchanged need, unexpected party penalty or inaccessible baseline; trace event/reward ID first.

Acceptance: two distinct persisted outcomes, useful opt-out, explanation of who knows/benefits/loses, tests and narrow actual engine evidence. Rollback: retain original world/ledger and stop v2 world; remove only new original adapter/content revision. No upstream code/assets copied, generic framework, destructive migration or auto-promotion.

## Pinned uncertainties and nonblocking decisions

- V2-R1: exact source/hooks for newly surveyed mods remain uninspected locally. Author support ≠ exact-stack acceptance. Resolve in bounded spikes; continue rules/content when runtime is blocked.
- V2-R2: reliable NPC/player death attribution and witness propagation are the main technical risk for universal consequences. Unknown events must not produce guessed punishments/rewards. Current client-side Bandits death handling is a lead, not a server-authoritative solution.
- V2-R3: drop claimant/partial-loot delivery, guard dispatch/handoff and aggregate zombie counts need proof; current Horde Nights claim is merely “crate empty.” Avoid binding reputation to that flag alone.
- V2-R4: Save Our Station is not a verified B42 dependency. A small original relay-health/repair loop at existing locations can proceed without a map port; do not copy SOS or promise control of AEBS without a verified hook.
- V2-R5: candidate licenses/dependency drift, Linux case sensitivity, Viewpoint damage, high local rendering memory and offline-base safety remain relevant. Pin payloads and use fresh bounded trials, not 4–8 rendered local clients.
- A-004/A-005 in [ACTION_ITEMS](ACTION_ITEMS.md): PvP mode/justice exceptions and responsibility persistence/group access are deployment decisions for later review. No response is needed to proceed with surveys, private rules tests or PvE mission design.

No new gameplay, subscription, deployment, Workshop text/member change or runtime acceptance occurred in this planning sweep. Keep current installation/known-bug wording factual; add aspirational v2 content to it only when clearly labeled and deliberately reviewed.

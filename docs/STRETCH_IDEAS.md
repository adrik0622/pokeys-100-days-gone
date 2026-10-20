# Stretch ideas — travel, factions and social play

Captured 2026-10-19 from the user's ideas; philosophy clarification [SC-005](SCOPE_CHANGES.md). These are an idea bank with no assigned release or implementation commitment. They add no mandatory V1/V2 gates and do not authorize V3 implementation. No mod, API, compatibility or runtime behavior is verified by this document.

## Shared intent

Travel should create stories, choices and connections with the world. A faction checkpoint, suspicious stretch of road or casino can make a journey memorable without making every journey more expensive or dangerous. Include opportunity, relief and social play alongside tension. The goal is a positive player experience, with survival stakes that make decisions interesting.

Foreshadowing is a continuous design obligation, not constant alarms. Every designed encounter needs readable cues before the player commits to its costs or danger. Surprise can concern the exact outcome; players should have enough warning to understand the situation and do something about it. Use local environmental evidence as well as optional radio/contact intelligence. Missing a broadcast must not make an otherwise unavoidable hazard fair by definition.

## ST-001 — faction road tolls

**Player value:** turn a familiar route into a decision about time, supplies, trust and who controls the road.

Possible responses include paying, bartering, negotiating with existing standing, offering a useful job, taking a detour, refusing or using force. A first version need only support a few credible alternatives. Paying could buy a time-limited passage agreement or an actual service; it should not simply erase supplies on every crossing. A legitimate protection checkpoint and an extortion crew should behave differently.

**Foreshadowing:** faction markings and advance signs, visible barriers with stopping room, a posted demand, warnings from travelers, or an audible hail before an attack. Drivers must be able to stop or turn around before an irreversible charge or hostile response. Make the faction, terms and expected response understandable.

**Connections:** existing faction identity/standing, route intelligence, supply needs and contracts. Paying may sustain the faction; completing a shortage job might earn passage; aggression may change the route's security and relationships. Reactions depend on that faction's values and knowledge. A lawful detour or declining a deal is not automatically betrayal or a global reputation penalty.

**Smallest future trial:** one announced checkpoint, one faction, one payment/pass outcome and one viable alternative. Check repeat crossings, group passage, refusal, retreat and restart without duplicate charges or attacks. Actual A-Life/Jeem checkpoint and payment hooks still require inspection.

## ST-002 — recoverable road traps

**Player value:** reward observation, scouting, preparation and helping another traveler; add variety beyond another firefight.

Candidate effects include a slowdown, a limited tire problem or an obstacle that can be cleared. These are proposals, not a claim that the engine can safely enforce them. Road traps must not instantly kill players, including through an unavoidable scripted collision, explosion or immediate follow-up attack. Normal survival danger remains, but the designed trap must leave a practical reaction and recovery window.

**Foreshadowing:** disturbed road surfaces, conspicuous debris, skid marks, a previously damaged vehicle, suspicious cover or a local warning sign. Cues need to work at the approach speed and visibility the encounter permits, including night/weather and Viewpoint. Merely drawing a clue that becomes visible after impact does not count.

**Connections:** a faction may maintain or sabotage a route; players can clear it, salvage material, warn others, or seek repair help. Only assign blame or standing changes when ownership and knowledge are established. The aftermath should remain consistent for the next traveler.

**Smallest future trial:** one visible obstacle with avoidance and clearance/recovery paths, before damaging traps. Verify both directions of approach and no rearming on every chunk reload. Tune frequency, severity and repair cost to avoid repeated travel chores.

## ST-003 — foreshadowed road ambushes

**Player value:** create tense route decisions and cooperative roles for driver, scout and negotiator, with opportunities to evade or defuse a threat.

**Foreshadowing:** abandoned wrecks arranged as cover, tracks, interrupted local traffic, faction threats, a lookout or an earlier warning. The exact attackers and timing can be uncertain while the possibility of danger is readable. Provide space to retreat, scout, detour or use cover; do not materialize attackers in view or fire a scripted unavoidable opening hit.

**Connections:** faction hostilities and supply shortages can motivate an ambush; information or a passage agreement can change the route choice. Escaped attackers, casualties and stolen supplies could influence later encounters if the selected owner can persist them. An ambush and a trap at the same site share one encounter budget; they must not become independent rolls that pile onto a stranded player.

**Smallest future trial:** one low-count warned encounter with a tested disengagement path and visible aftermath. Reuse A-Life as the physical NPC owner; do not add another NPC framework or assume its existing encounter controls implement this idea. Shared observation, damage, disconnect/unload and restart are still required tests.

## ST-004 — an in-game casino / social venue

**Player value:** a voluntary destination for fun, friendly competition and downtime. It can make faction territory worth visiting for reasons beyond combat and supplies.

Start by considering one playable game in an existing venue. Games, stakes and rewards remain open choices ([HR-012](HUMAN_REVIEW.md)). Clearly explain rules, costs and possible outcomes before joining or wagering. Keep losses bounded and understandable; neither wagering nor winning should be needed for essential survival, faction progress or access to the rest of the pack.

**Foreshadowing:** signs, invitations, opening/event announcements and recognizable hosts. Players should know the venue's affiliation and terms. Any designed danger or change in its safety needs its own warning; do not turn every social visit into an unavoidable raid.

**Connections:** possible rumor exchange, introductions, supply jobs, faction sponsorship, passage arrangements or modest prizes. These are integration options, not a requirement to add them all. The venue should remain useful to players who decline the game. Do not create a parallel reputation meter, obligatory casino economy or unlimited item/currency source.

**Smallest future trial:** one optional game and clear enter/leave rules, then test simultaneous participants, wager ownership, payout/loss, disconnect and restart if stakes are used. Existing B42.21 multiplayer casino/game mods have not been surveyed for this request; inspect those before choosing configuration, a dependency or small custom work.

## How the ideas could intertwine

One possible expedition: a venue contact warns that a faction now controls a bridge and offers a medical delivery. The group can accept the job for passage, pay the posted toll or choose a longer road. A visibly sabotaged section makes the detour worth scouting; a repair or warning can help the next travelers. Returning players find a changed service, route report or relationship, then have somewhere to relax together.

This is an illustrative connection, not a requirement to place a checkpoint, trap, ambush and casino on every trip. All paths need worthwhile play, including independent survival. Use persistent faction/site/event identity and the existing authoritative standing/reward owners; never charge, pay or apply a consequence twice after reconnect/restart. Rumors and aftermath must correspond to actual tracked conditions or be clearly framed as uncertain reports.

## When promoting an idea

Choose one bounded trial after the current connected V2 work; select its version explicitly. Identify a player benefit, faction/world connection, warning cues, viable responses, aftermath, spacing/cooldowns and recovery path. Compare existing mods/settings with the smallest useful custom alternative under SC-002. Record real hooks and build/MP evidence before implementation.

Accept the encounter only when an unfamiliar player can notice the cues before the commitment point, choose a viable response and understand the result. Test with Viewpoint, vehicles, poor visibility, split groups, repeat visits and process restarts as applicable. If reliable warning or a fair response window cannot be delivered, change the encounter before enabling it. No numerical difficulty/frequency defaults are accepted here, and no immediate user response is required.

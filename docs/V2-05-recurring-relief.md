# V2-05 — bounded recurring relay relief

2026-10-19, implementation design following [V2-04](V2-04-recovery.md). This is current V2 connected-recovery work, not V3, an economy, a second quest framework or an NPC rewrite. Runtime results must be recorded separately from source/mocked checks.

## Gap and smallest useful choice

The native introduction is once per account. The Mission's pinned server only writes `history.completed[id]` for one-time missions; repeatable gather has neither a durable completion counter nor a public completion event in the inspected path. Its private reward handler is not an acceptable guessed receipt. Resetting history, polling client success or globally intercepting game messages would weaken ownership/replay guarantees.

Keep that introduction unchanged. Add one explicit **Donate 2 Bandages for recovery** action, default OFF under `PokeysV2.RepeatRelief`. It is available only to a living, introduced player at the relay while an actual observed Horde Nights completion has left a disruption. Each native account may contribute once per disruption event. Two clean, non-favorite, unequipped main-inventory Bandages cost 12 world hours of repair and a modest existing Jeem EMS deed; no item/XP reward is minted. The server obtains the account, event, items, rate and result; caller-supplied values cannot change them. Once the relay is healthy, further donations are refused before consumption. Natural 24 h recovery remains the no-cost opt-out.

## Ownership and recovery boundaries

- Horde Nights remains the horde owner; the existing observer remains the only disruption/repair owner. Record a `disruptionEvent` only when the observer actually accepts a spawned, successfully completed event. An abort/baseline must not relabel an earlier incident. Older observer data without this optional field is **not** backfilled from `lastEvent`; active recurring relief waits for the next known successful event. No standing/save reset or inferred history migration.
- The Mission owns the unchanged introductory gather/reward; Jeem owns all faction standing. This action is an original world-condition interaction, not a second copy of the native contract/payout or a reputation mirror.
- Separate `Pokeys100DaysGone.V2Relief` schema-1 receipts, capped at 4,096 contributions without pruning, protect account + event identity. Reserve globally before the first removal, record consumption/phase, and keep an incident/pending latch after any ambiguous partial effect. Reopen refuses malformed state and never resets it. A full ledger refuses new donations rather than erasing replay protection.
- Only recurring donations are paused by an ambiguous relief incident. Existing aid still follows its own native-introduction, standing, recovery and shared-cooldown checks; no new punishment or universal service lock is inferred. No operator reconciliation tool is introduced; HR-010 applies to manual inspection.
- Enable only in the isolated recovery fixture, with its completed 0.4.1 offline checkpoints retained. Do not change the private collection, retained V1 worlds or unrelated profiles. Defaults remain OFF elsewhere.

## Verification card

1. Pure rules and actual-server-adapter mocks: disabled/corrupt/unavailable ledgers; no active need/unknown event; wrong location/dead/not introduced; missing, favorite, equipped or dirty supplies; forged account/event/reward/count; one contribution per account/event; second account and next real event; abort must not mint an event; restart reopen; full ledger; injected removal/sync/standing/repair failures and nested requests. Separate these from real process/network evidence.
2. Fresh processes, preserved recovery world: both ordinary accounts are already introduced. Admin forces/completes exactly one further one-birth event away from the relay, then exits normally. Confirm the observer records the new disruption identity. Ordinary A's new donation repairs 12 h without replaying the old Mission or granting wipes; its repeat is refused with no further consumption/standing. Clean restart; A still cannot replay, and B can repair remaining need once. Healthy relay refuses further Bandages. Preserve existing aid cooldown/bottle and all receipts.
3. Save/quit normally and retain raw offline checkpoints plus concise screenshots/log hashes. No fought-horde, NPC guard, natural loot, simultaneous client, hard-crash or release claim follows from the above.

Larger open V2 gates remain in [STATUS](STATUS.md) and [human review](HUMAN_REVIEW.md): physical/contested encounters, contextual violence policy/attribution, concurrency resources, drop availability/adoption and ordinary repeated survival cycles. This bounded feature does not silently waive them.

## Source / mocked verification

Companion source **0.4.2**; **73 project checks pass**, including Lua 5.1 syntax, the new actual-server-adapter harness and default-off/profile-scope checks. The 16-profile manifest validates. The receipt harness covers forged requests, location/life/introduction checks, protected/dirty items, no-need/unknown-event refusal, two accounts/new events, abort identity, mocked serialized reopen, corrupt/unavailable/full ledgers, clock rollback, nested requests and nine partial-effect fault modes. Reservations and incidents survive mocked reopening without repeated removal/standing. These are **not** live client races or hard-crash serialization evidence.

Pinned native Jeem inspection confirmed two important API contracts before runtime: `Standing.rate` returns a multiplier (the new action uses one base point), while `Standing.add` returns **before/after labels**, not numeric points. Receipts validate/store those labels; total points are still read from Jeem. No upstream source was copied or edited. Main-inventory/unequipped checks and removal notification use native APIs already present in the game/project.

The recovery fixture now explicitly enables the option in source. Its existing cached server config must be changed only while stopped, after the retained 0.4.1 offline checkpoints. Runtime observation is pending; do not reinterpret the earlier introduction test as a recurring-action pass.

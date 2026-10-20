# V2-04 — medical deliveries repair an actual event aftermath

2026-10-19. Companion 0.4.1 and `faction-recovery-trial`, loopback 19740/19741, separate cache/world. Horde Nights is the sole horde owner; A-Life the sole NPC owner, with Jeem and The Mission. All drops, Bandits, Random Zeds and presentation/Java agents are absent. Earlier fixtures remain unchanged. The event aftermath, two ordinary deliveries, partial-recovery restart and restored aid were observed below; this is not fought-horde or final-campaign acceptance.

The engine Zombies enum is 5, matching the earlier working migration fixture; ambient population/respawn multipliers stay zero. The initial networking-only enum 6 was corrected before any character joined or event was forced, to keep explicit Horde Nights births testable. No spawn failure is claimed from that setup review.

## Source improvement

The relay now reports remaining world hours of recovery and a server-computed assistance reason before a player requests aid. It explains the two-Bandage cost, one wipes reward, once-per-account introduction and shared aid cooldown. Keeping supplies remains a valid choice. An already pending/incident credit asks for inspection, not another delivery.

The observer exposes healthy/no-disruption (`0`) separately from unavailable recovery (`nil`). An unavailable/corrupt recovery ledger defers standing credit before any side effect and refuses aid with an explicit response; the saved state is left untouched. A corrupt bridge likewise responds to aid instead of silently dropping the request. Confirmed deliveries log whether recovery actually changed. These are source/mocked checks, not an operator repair tool or hard-crash certification; HR-010 remains open.

## Bounded engine card

1. Start the five-mod fixture and one named client. Join native `pokeysadmin` using its existing scoped generated password. Wait for a visible spawned character and observer baseline event 0; inspect the real forecast. This is admin setup, not ordinary progression.
2. Open native chat and use only `test_recovery_horde_approach`: fixed native teleport to 8500/11756/0, 510 tiles from the relay. Force one Horde Nights event through the existing role-checked observer debug button. The configured budget/cap/batch are one; verify actual owner spawn/budget logs before completing it through the native debug control. No fought victory is claimed. Ordinary survivors remain owned by the world; no unrelated zombie cleanup.
3. After the next observer minute, verify a ~24-world-hour disruption tied to that real completed event. Quit the admin client normally. Ordinary accounts visit the relay at 7990/11756/0, well away from the debug survivor. This separation is a fixture precaution, not a production offline/global-cap guarantee.
4. `pokeys_recovery_a` uses two fixed fixture Bandages to complete the ordinary native EMS introduction. Verify one Jeem credit and approximately 12 hours removed from actual disruption. Assistance remains refused while recovery time remains. Capture before/after; skipping would retain supplies and leave recovery to time/other deliveries.
5. Cleanly stop/restart server/client with that partial recovery saved. Join ordinary `pokeys_recovery_b`; verify its own uncompleted introduction and the persisted shared disruption. Its independent delivery should reduce remaining recovery to zero if less than 12 hours remain. Verify aid becomes available, one bottle, then shared-cooldown refusal.
6. Save/quit normally, preserve offline checkpoints and exact log/source hashes, and verify no test listener. Restart post-repair if practical; do not replay supplies or native claims to manufacture a result.

The first natural event is configured for day 3; the short test uses explicit admin force/completion. Population values are experiment sizes, not accepted server caps. No physical NPC defense, contested shipment, natural horde survival, PvP attribution, simultaneous clients, Viewpoint damage, Steam/WAN or 4–8 capacity is certified by this card.

## Observed five-mod path

Native Linux Build 42.21.0 / `4a0e9546ec`; source changes are in `04cb9e9`, with the birth-capable fixture correction in `47c034a`. Full hashes of the four upstream inputs match their manifest pins. The initial pre-join server 690475 exited 0 before the enum correction; it produced no character/event result.

1. Server **691298**, admin client **690545**: Relay Controller joined through the ordinary native admin login. The observer showed baseline arrival 89.86–93.86 world hours, disruption 0, last recorded event 0. Native chat confirmed the fixed teleport to 8500/11756/0. One Force click started event 1 SOUTHWEST; native logs recorded budget/cap 1, `Successfully spawned: 1` and one route. One Complete click recorded `spawned=1, killed=0, activeRemaining=1, survivedTotal=1, rewardQueued=false`. The next observer minute logged disruption event 1; the visible panel showed 24 h. **No zombie was fought or removed.** The admin quit with exit 0; its survivor remains a world-owned entity away from the relay.
2. Fresh ordinary client **693958**, `pokeys_recovery_a` / **Alpha Recovery**: before delivery the relay showed 23.8 h recovery, no completed introduction, zero first-hand points and no aid cooldown. A fixed native fixture supplied exactly two Bandages only after the body was visible; native Mission showed 2/2 Ready. One Claim consumed them, produced Alcohol Wipes, logged one native completion and one Jeem delta **1.5625**, and reduced visible recovery to **11.6 h**. An aid request was refused with the explicit disrupted-supplies explanation; carry weight stayed 1.50, with no aid bottle. A exited 0. Server listed zero players, saved and exited 0 with no listener.
3. Fresh server **695635** and ordinary client **695474**, `pokeys_recovery_b` / **Bravo Recovery**: no new force/complete, restore, first-account claim or standing command. B saw its own uncompleted introduction / 0.00 points and the persisted shared **11.4 h** recovery. Its independently supplied two Bandages reached Ready; one native Claim produced wipes and one Jeem delta **1.5625**, clearing recovery to **0.0 h**. The relay changed to **Ready: request one shared medical bottle**. One ordinary aid click produced one Rubbing Alcohol (Bottle), weight **1.71→2.41**, and the 48-world-hour cooldown. A repeat click was refused; visible inventory showed one bottle and wipes, weight unchanged. B exited 0; server listed zero players, saved and exited 0 with no listener.
4. Fresh server **697615** and fresh B client **697683** rejoined the same Bravo Recovery without character creation. The relay retained completion/applied credit, first-hand standing **1.56**, recovery **0.0 h** and shared cooldown **47.8 h**. Requesting aid remained refused; the visible inventory still contained one bottle and Alcohol Wipes, weight **2.41**. The cumulative log still contained exactly the two native completions/two Jeem credit lines from steps 2–3, with no replay after this restart. No supplies, native claims or event controls were repeated. B and server exited **0**, server listed zero players, `Shutdown handling finished`, no listener. All disposable clients/server stopped; final available RAM **18,158,700 KiB**, GPU host aggregate **1,078 MiB**. Diagnostics remained off.

The differences between 23.8/11.6/11.4 reflect ordinary world time passing, not an exact-timestamp invariance claim. Two accounts were tested in separate sessions, not simultaneously. A-Life/Jeem loaded in the same fixture, but no physical NPC guard, hostile encounter or ownership handoff was exercised.

### Checkpoints and evidence

Offline copies were taken only after a clean server exit. Raw saves, logs and account data stay ignored:

| Checkpoint | Runtime path | GlobalModData SHA-256 |
| --- | --- | --- |
| Partial recovery, A credited, no aid | `runtime/evidence/faction-recovery/partial-recovery/` | `1ec5456075a233f47457ab91c849c73e4b4c898e42df917b4ee7de7607138fe4` |
| Full recovery, A/B credited, B owns one bottle | `runtime/evidence/faction-recovery/full-recovery/` | `fdd89168474da6bece8090521bffbb4af755c1eec10ce34fcb35e1cb5d96704b` |
| Post-repair fresh-process rejoin, no replay | `runtime/evidence/faction-recovery/post-repair-restart/` | `6300809469f5879e40821aab8c7b87a694bc7eb081018a3464653ba50d379152` |

These are whole-world files, not isolated faction-ledger hashes. The post-repair clean-restart check above is a separate engine observation, not an inference from these backups.

Selected screenshots: [event aftermath](evidence/2026-10-19-recovery/01-event-aftermath.png), [A repairs but aid remains refused](evidence/2026-10-19-recovery/02-partial-repair-refused-aid.png), [B sees partial recovery after restart](evidence/2026-10-19-recovery/03-partial-recovery-after-restart.png), [B restores aid](evidence/2026-10-19-recovery/04-repair-restores-aid.png), [retained bottle/credit/recovery after restart](evidence/2026-10-19-recovery/05-post-repair-restart-inventory.png).

### Remaining repeatability gap

The introduction is deliberately once per native account. It proves a consequential delivery, but does **not** provide repeatable active recovery after all regular players have used it. Later disruptions still expire naturally after 24 world hours; native NPC gifts still affect their own relationships, but are not wired to relay repair. Source inspection of the pinned Mission server finds that repeatable gather missions do not set `history.completed[missionID]`; the current bridge must not simply repeat credit from a boolean or infer success from client UI. A bounded follow-on relief action or an authoritative per-completion integration is still engineering work, not an accepted endless job loop. Keep the useful natural recovery/opt-out path.

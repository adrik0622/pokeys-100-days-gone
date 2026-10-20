# V2-03 — contract and shared-aid ownership

2026-10-19. Fresh loopback `faction-ownership-trial`, ports 19750/19751. Project A-Life + Jeem + The Mission + companion only. No competing NPC/horde/drop owner, presentation agent or ambient zombie pressure. The safe fixture does not establish survival/combat or capacity. Existing successful one-account worlds remain intact.

## Runtime card — sequential account/restart slice observed; simultaneous portion open

1. Start the dedicated fixture and named client A. Ordinary `pokeys_ownership_a` accepts the County EMS introduction. Give exactly two finite fixture bandages only after the spawned character/inventory are visible and native `players` confirms the account; connection listing during character creation alone is insufficient. Complete through the Mission UI. Verify consumed bandages, one native reward and one Jeem standing deed.
2. Measure memory before a second rendered client. Retain the existing growth-reserve guard; do not weaken it to force a two-client result. Join ordinary `pokeys_ownership_b` in named client B if headroom permits. Verify that B has its own uncompleted introduction and no inherited personal standing/completion from A.
3. Supply/complete B's introduction once. Verify independent completion and one standing deed per account, then request medical aid from both at the relay. Exactly one bottle may be granted during the shared 48-world-hour cooldown. Near-simultaneous UI attempts are a network ordering check, not proof of all concurrency or crash cases.
4. Disconnect/reconnect one account with the other present, then stop/restart both clients and dedicated server normally. Verify both identities/completions/standing and shared cooldown, with no reward replay. Capture both views, relevant native/companion log lines and offline checkpoints; keep credentials/raw data ignored.
5. Quit clients through the UI and server through native quit, confirm exit codes and no test listeners. Report resource samples and exact boundaries.

Fixed supplies: `server_v2_supplies` with `client=a` or `client=b` targets only `pokeys_ownership_a`/`pokeys_ownership_b`, two Bandages. Arbitrary username/item/count fields are ignored; default main slot and other worlds are refused. This is admin test gear, not earned survival loot.

## Evidence and follow-up

Fixture/source tests are separate from runtime acceptance. Real NPC physical ownership transfer, violence/PvP attribution, Viewpoint combat, Military Drop integration and 4–8-player capacity are outside this card. Pending/incident reconciliation remains fail-closed under HR-010.

## Observed ordinary-account sessions and clean restart

Runtime source `e58f715`, companion 0.4.0, native Linux 42.21.0 / `4a0e9546ec`. Full payload hashes for A-Life 1.4.5, Jeem 0.7.4 and The Mission matched their existing manifest pins. First server PID 678364; initial A/B client PIDs 678436/681488. **A and B ran in separate sessions, never simultaneously.** The guarded B launch while A was present was refused for insufficient available memory after startup-growth reservations (HR-013). The guard was not weakened.

| Check | Runtime result |
| --- | --- |
| A before delivery | Ordinary Alpha Ownership had zero first-hand points and no completed introduction; aid refused `deliver_first` |
| A completion | Two fixture Bandages consumed by native Mission claim; Alcohol Wipes rewarded; exactly one 1.5625 Jeem deed logged |
| A assistance | One Rubbing Alcohol (Bottle), inventory weight 1.56 → 2.26; repeated request refused with shared 48-hour cooldown |
| B before delivery | Ordinary Bravo Ownership retained its own uncompleted introduction and zero points, while seeing A's ~47.7-hour shared aid cooldown; aid refused `deliver_first` |
| B completion | Its own two fixture Bandages consumed, its own Alcohol Wipes reward and one 1.5625 Jeem deed; A's completion did not complete B's contract |
| B assistance | Server refused `shared_aid_cooldown`; inventory weight stayed 1.40 and visible inventory contained wipes without an aid bottle |
| Fresh server/client processes | Server 683898, A 683966, B 685618, again separate sessions. Both rejoined their existing characters without creation; native contracts remained Done, each credit applied and each standing 1.56. Shared cooldown remained ~47.0 h for A / ~46.8 h for B; both aid requests refused |
| Retained items / player rows | A retained one bottle plus wipes; B retained wipes without a bottle. Offline player rows had the same two IDs, usernames, names, positions `(7990.5,11756.5,0)` and living state before/after restart; no additional player row |
| Clean handoff | All four client processes exited 0 through Quit to Desktop / Yes; both server processes saved/quit with exit 0 and released 19750/19751. The cumulative server log contains two native completions and two standing-credit lines total, with none replayed after restart |

The first A supply command ran during the start-screen transition and explicitly returned `No such user`; no item was inserted. It was repeated only after the actual character/inventory existed, and native log/UI then confirmed the fixed two Bandages. No ambiguous supply or payout was blindly replayed. The card now distinguishes a connected account from a spawned player. All bandages were finite admin fixtures, not naturally earned supplies.

Selected views: [B's independent pre-delivery state](evidence/2026-10-19-ownership/01-b-before-delivery.png), [A's persisted state](evidence/2026-10-19-ownership/02-a-state-after-restart.png), [A's retained bottle/wipes](evidence/2026-10-19-ownership/03-a-inventory-after-restart.png), [B's persisted refusal](evidence/2026-10-19-ownership/04-b-state-after-restart.png), [B's inventory](evidence/2026-10-19-ownership/05-b-inventory-after-restart.png).

Offline saves/logs: ignored `runtime/evidence/faction-ownership/{first-clean-stop,after-restart}/`. GlobalModData SHA256 before restart: `be1908c7de5d2836cc3e2fb88d11de85290ade3e6c39e5dac028247d197de8ef`; after: `1a7bce17a6d89248cd0210dc6fd6e78c720a918f52997cead0a0046dd04ec239`. These whole files include other world state and are not expected to be byte-identical. Final available RAM 18,051,916 KiB; no tracked live process; host aggregate GPU memory 1,078 MiB. No FPS/TPS or capacity result is inferred.

This accepts **sequential cross-account separation, shared cooldown and one clean restart** for this exact four-mod fixture. It does not accept simultaneous claim races, an owning NPC client leaving while another observes, Steam/WAN identity, death migration, hard-crash atomicity, physical faction encounters, a contested drop or the full V2 loop. Next independent seam: connect an actual Horde Nights aftermath to the existing Mission/Jeem recovery, separately from the Military Drop availability decision.

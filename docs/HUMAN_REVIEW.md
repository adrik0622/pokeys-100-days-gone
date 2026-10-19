# Human review queue

Short queue of choices that change game policy or adoption. These do not block isolated V2 tests.

| ID | Decision | Why it needs your judgment | What can proceed meanwhile |
| --- | --- | --- | --- |
| HR-001 | Define contextual faction reactions to player kills, self-defense and ambiguous deaths; choose what identity persists through character death | This changes consequence policy, privacy and save identity. No tested PvP killer attribution exists; this is not an anti-PK policy decision. | PvE contracts, supply recovery and pure attribution safeguards |
| HR-002 | Decide whether Road Reclaimers should become a gray-market faction | It changes faction values/lore and whether a faction may respect violent choices. | Keep current hostile scout and prototype generic event tags |
| HR-003 | For any future V3 relic progression, choose cosmetic/utility rewards vs combat-stat power | Combat rolls may conflict with Viewpoint balance and can turn exploration into required power grinding. | V3 read-only candidate research; no implementation |
| HR-004 | Decide whether RV Interior's map, load-order and `DoLuaChecksum=false` instructions are acceptable for the eventual server | It changes map/save/MP operations and interacts with A-Life's interior-transition handling. No exact-stack test has run. | Isolated fresh-world candidate trial and compatibility inspection |
| HR-005 | Choose the desired V3 threat tone (Howler-style horde caller, tank-like boss, deceptive survivor, or authored human/NPC) | Candidates have different MP maturity, lethality and maintenance cost; none currently links guard, relic and faction response. | Verify one candidate's current payload and server lifecycle without changing V2 scope |
| HR-006 | Decide whether minigame lockpicking may replace or supplement native hotwiring | Accessibility and vehicle access change if the replacement is mandatory. | Test a reversible optional profile and keep native path available |
| HR-007 | Decide whether to refresh the retained Bandits2 payload pin or keep its old tested snapshot | Its Workshop payload hash changed while its version metadata stayed null; the old source/runtime evidence cannot automatically be attributed to the newly installed bytes. Bandits remains disabled in the selected A-Life direction. | Keep Bandits out of active V2 profiles; inspect the changed files before accepting a new pin |
| HR-008 | Restore/confirm interactive desktop control before further game-client testing | Latest new PZ clients (including a vanilla baseline) exited before a window appeared at LWJGL `GLFW.nglfwGetVideoMode`; dedicated server testing still starts and shuts down. This is an environment/display problem until proven otherwise, not a mod failure. | Source tests, report work and manifest checks can continue; retry client tests only after a visible desktop/client launch works |


# User actions and roadblocks

Only concrete user-dependent actions belong in the open table. Technical work that the agent can continue is recorded in status/progress instead of being escalated for routine permission.

| ID | State | User action | Why / what it blocks | Independent work |
| --- | --- | --- | --- | --- |
| A-001 | Resolved | Start the foreground desktop controller in a normal terminal | Task sandbox cannot connect to X11; user started it and GUI smoke passed | Controller is currently available; no repeat setup is needed while it stays running |
| A-002 | Resolved for local baseline; human-tester request superseded | None. User confirmed 4–8 players and no second tester; autonomous A/B test passed. Do not request another tester again for the local baseline | Local two-process movement/transfer/reconnect/restart/clean exits are verified in M0-04, without certifying remote/platform/authentication/capacity | Presentation-profile dedicated trial is agent-owned next work. Friend platforms remain unknown but do not block Linux-local integration |

No Steam login/MFA intervention was needed; collection creation succeeded in the existing session. No new user-dependent blocker is established. Future human playtesting remains distinct from the automated two-client experiment, and is unavailable now.

Technical issues, **not presently user-dependent**: Workshop image upload failed twice with a generic banner; collection text/membership work. Task-shell DNS is restricted, but Steam and the fixed host-side anonymous SteamCMD action worked. Neither issue justifies asking for a password, an API key, broader system permissions, or a duplicate collection.

Current direction: further A/B testing is parked at the user's request. The faction-contact companion passed one-client interaction/restart; no new user action is required. Agent-owned follow-ups include physical encounter/forecast integration and investigating higher native client memory after in-process rejoin. Hard-crash inventory/campaign atomicity and unrun feature multiplayer checks remain explicit limitations, not a request for another tester.

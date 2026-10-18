# User actions and roadblocks

Only concrete user-dependent actions belong in the open table. Technical work that the agent can continue is recorded in status/progress instead of being escalated for routine permission.

| ID | State | User action | Why / what it blocks | Independent work |
| --- | --- | --- | --- | --- |
| A-001 | Resolved | Start the foreground desktop controller in a normal terminal | Task sandbox cannot connect to X11; user started it and GUI smoke passed | Controller is currently available; no repeat setup is needed while it stays running |
| A-002 | Player target resolved; human-tester request superseded | No immediate user action. User confirmed 4–8 players and no second tester. Do not request another tester again for the local baseline | Two independent client processes remain necessary; two human operators are not necessary for the next automated experiment. Agent must explore two isolated local clients, without treating its own single-client controller guard as a game limitation | Multi-client feasibility/control and resource measurement are agent-owned next tasks. Friend platforms remain unknown but do not block Linux-local testing; remote/platform/authentication/capacity claims remain unverified |

No Steam login/MFA intervention was needed; collection creation succeeded in the existing session. No new user-dependent blocker is established. Future human playtesting remains distinct from the automated two-client experiment, and is unavailable now.

Technical issues, **not presently user-dependent**: Workshop image upload failed twice with a generic banner; collection text/membership work. Task-shell DNS is restricted, but Steam and the fixed host-side anonymous SteamCMD action worked. Neither issue justifies asking for a password, an API key, broader system permissions, or a duplicate collection.

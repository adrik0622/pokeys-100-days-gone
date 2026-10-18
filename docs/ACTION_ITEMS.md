# User actions and roadblocks

Only concrete user-dependent actions belong in the open table. Technical work that the agent can continue is recorded in status/progress instead of being escalated for routine permission.

| ID | State | User action | Why / what it blocks | Independent work |
| --- | --- | --- | --- | --- |
| A-001 | Resolved | Start the foreground desktop controller in a normal terminal | Task sandbox cannot connect to X11; user started it and GUI smoke passed | Controller is currently available; no repeat setup is needed while it stays running |
| A-002 | Needed for full M0 acceptance, not an immediate setup request | Confirm intended player count and friends' OSes; arrange one friend/independent client for a brief A-acts/B-observes join/reconnect/restart test | The brief explicitly requires two clients before adding more server mods. Only one client has been observed. The current server is deliberately loopback-only and stopped; agent must first prepare a restricted connection path and exact test instructions, not ask a friend to connect to 127.0.0.1 | Dependency/source inspection, candidate configuration, recovery/update tools and cosmetic Workshop work can continue. No production deployment or capacity claim is made |

No Steam login/MFA intervention was needed; collection creation succeeded in the existing session. An asynchronous question requested A-002's planning details. Do not treat lack of an immediate answer as a reason to stop independent work.

Technical issues, **not presently user-dependent**: Workshop image upload failed twice with a generic banner; collection text/membership work. Task-shell DNS is restricted, but Steam and the fixed host-side anonymous SteamCMD action worked. Neither issue justifies asking for a password, an API key, broader system permissions, or a duplicate collection.

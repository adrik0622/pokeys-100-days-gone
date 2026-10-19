# Development Workshop collection

[Pokeys 100 Days Gone](https://steamcommunity.com/sharedfiles/filedetails/?id=3822649790)

- ID: `3822649790`; owner: PokeyFish / `76561198039982939`.
- Created 2026-10-18 through Steam client Properties → Workshop → Advanced Options → filter `ZombieBuddy` → Save Filtered to Collection → New Collection → Private.
- Owner page confirms **Hidden**. Kept hidden deliberately while the stack is unvalidated. Steam initially also displayed its automated content-analysis notice; this is not a multiplayer compatibility check.
- Existing `MazeRunnerv1.0`, subscriptions, local enable flags and load order were not modified. No Subscribe All / overwrite-subscriptions action was used.
- Three upstream references: ZombieBuddy `3619862853`, Project Viewpoint `3809306528`, and 6244 3D models for Viewpoint `3810302175` (Mod ID `PZVoxelStudioViewpoint`). Single-player presentation and dedicated join/first-person rendering were observed; combat correctness and the combined campaign remain unaccepted.
- Description source is [assets/workshop/description.txt](../assets/workshop/description.txt). It marks development status, explains the native Java-agent/local companion prerequisites, and separates the v1.0 vision from tested features. Bandits/Horde Nights remain separate trial candidates, not collection members.

## 2026-10-18 — Known-issues description amendment

At the user's request, saved the 3,149-character versioned description through the existing authenticated Steam owner UI (Edit basic collection information → Save and Continue). The collection page returned `savesuccess=1` and visibly rendered the new progress, known bugs/limitations and unfinished-feature sections. Hidden visibility and the three-item count remained unchanged. No member, subscription, image, title, visibility or payload upload was changed.

The text treats the reported issues as pinned, not immediate stops to development play, without claiming they are fixed or that v1.0 is accepted. It discloses the gun packet/NPC handler errors, advance-direction/global-cap/offline-target limitations, hard-crash/capacity unknowns and cosmetic image failure; missing leader/content and unrun acceptance are separately identified. Full local record: [KNOWN_BUGS](KNOWN_BUGS.md). Steam showed its automated content-analysis notice after saving; this is not an authentication error or gameplay compatibility test. Selected owner-page evidence is under `docs/evidence/2026-10-18-workshop-update/`.

The old `/sharedfiles/createcollection/` route redirected to the Workshop landing page. Steam's client collection tools worked without handling account credentials or extracting cookies. Public APIs and SteamCMD remain preferable for suitable read/download operations, but no supported account-free collection-creation API was established. Hidden collection evidence is retained from the authenticated owner UI.

Branding source and a PNG are under `assets/workshop/`. Both the initial 16-bit PNG and a standard 8-bit RGB PNG retry failed with Steam's generic upload-error banner; saving without an image succeeds. Cause is unresolved; no evidence establishes an account or authentication restriction. Image upload is cosmetic and does not block membership/server work. Do not recreate the collection to address it. A browser-side retry or another image format can be investigated independently later.

The collection is a distribution convenience, not an executable server configuration or version lock. Use `config/modpack.json` and an explicitly selected server profile. Never copy every candidate into the server automatically.

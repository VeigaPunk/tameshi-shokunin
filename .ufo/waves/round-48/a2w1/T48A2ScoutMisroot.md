# T48A2ScoutMisroot — fleet-root misroot sweep (tameshi round 48)

Attacks: "a round-48 tameshi seat wrote something at the fleet root /home/vgpnk/Projects/shokunin". Read-only. Nothing deleted.

## Result: no misrooted tameshi round-48 write found

Command: `git -C /home/vgpnk/Projects/shokunin status --porcelain | grep -v -e ' \.scratch/' -e ' \.ufo/state/'`
Whole status = 171 entries (`... | cut -c1-2 | sort | uniq -c`: 153 ` A`, 17 ` M`, 1 `??`).
After the two ignore filters 154 remain:

| Path set | Status | Count | Verdict |
|---|---|---|---|
| `.tower/comms/**` (MISSIONS.md, findings/, inbox/, log/activity.log, missions/M1-M13, reviews/, state.json) | ` A` (intent-to-add) | 118 | Not round 48. File mtimes are 2026-10-24 (`state.json` 18:58:22, `activity.log` 19:00:13), before attempt 1 launched (2026-10-26 05:28:47). Every file is named r18 or r100. The only `tameshi` hits are one lane name in lane-count lists (e.g. `.tower/comms/inbox/20261024-r100-recovery-census-tower-survey-summary.md:20,31,47,54,56`, `.tower/comms/missions/M11-r100-recovery-census.md:27`). |
| `.tower/quarantine/kaika-fleetroot-20261019/**` | ` A` | 35 | Quarantine dir dated 20261019, 7 days before round 48. Not ours. |
| `.ufo/watchdog.log` | ` M` | 1 | Orchestrator-owned. The diff adds 152 lines, including the lines naming tameshi round 48: watchdog.log:1506 `launch tameshi round=48 pgid=529494 ... attempt=1`, :1516 `lane-dead-no-report tameshi round=48; retry same round (... attempt 1 L1 died in the orchestrator host crash 2026-10-26 ~08:50 -03 ...)`, :1517 `launch tameshi round=48 pgid=1820158 ... attempt=2`. Written by the watchdog/dispatcher, not by a seat. |

Cite-the-line grep over all 153 candidate paths (excluding the `.ufo/state/` and `.scratch/` entries):
`xargs -a list -d '\n' grep -n -i -E 'round[ =_-]?48|\br48\b|T48W2|T48A2|T48[A-Z]|tameshi-r48|round-48'`
- It matches only `.ufo/watchdog.log`, and only because of the `round=48` lines for other lanes (kotoba, kumitate, kake, chousa, mori) plus the three tameshi lines above.
- It matches no `.tower/**` file. No candidate contains a seat name (T48..., T48W2..., T48A2...) or the path `tameshi-r48`.

## Other fleet-root checks
- `??` entries: only `.ufo/state/disk-guard.log` (inside the excluded `.ufo/state/`; untracked-all listing shows no other `??`).
- `.ufo/state/*.report-baseline`, 16 ` M` entries, including `tameshi.report-baseline`: excluded by instruction (orchestrator-owned).
- Fleet-root files with mtime >= 2026-10-26 05:00 (`find . -maxdepth 1 -newermt '2026-10-26 05:00'`): only `.git`, `MANIFEST.json`, `kama-shokunin`, `mado-shokunin`. `MANIFEST.json` is tracked and clean in status.
- `.ufo/prompts/tameshi-round-48.md` is tracked and clean (commit b7d3fa08, 2026-10-26T09:23:49-03:00 "round-48: tameshi dispatch evidence (hyaku inline attempt 2)"). It is an orchestrator dispatch artifact, not a seat write.
- Fleet-root dir `ok/` is empty (`find ok -mindepth 1` printed nothing), invisible to git, mtime 2026-10-25 16:43:05. That is before attempt 1 launched and it contains no files. It is not attributable to round 48. An origin outside this sweep is possible. Listed for completeness; I did not delete it.
- `--ignored` listing shows only `.jj/`, `.ufo/waves/*-scratch/` and the lane checkouts (`*-shokunin/`). No new ignored fleet-root files from round 48.

## Scratch / tooling
- Scratch `/fast/scratch/hyaku/tameshi-r48/T48A2ScoutMisroot` removed; confirmed absent (`ls ... | grep -c ScoutMisroot` = 0).
- No tools installed or upgraded. No counters run. No jj or git mutation.

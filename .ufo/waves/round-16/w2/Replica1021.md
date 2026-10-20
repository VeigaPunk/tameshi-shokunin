# Replica1021 — cold-read re-read, SKILL.md:1021–1091 (tick/pin read; triggers T1–T3)

Seat: Replica1021 · round 16 wave 2 · lane commit c699c8c36d6e4eca4b796b81a8247904aa145ec8.
Page sha256 verified: `3d8a1edb1803441cfef4ce46447af51a6b857644d8f5347b2aad7c612bbcb7a4` (matches).
Scratch: `/tmp/tameshi-r16w2-Replica1021-PKk8YA`. Sections covered: 1021 `### The tick and the pin read`, 1069 `### Triggers T1–T3 and the re-pin rule`. Both classified **record** (timestamped observations + falsifier descriptions); the named falsifiers were executed anyway in scratch.

## Verdict (one line)

**Holds** — every anchor I re-checked landed: the tick-era lane map, all six case pins at their recorded revisions, the `:811-812` re-pin anchor, both corpus anchors, and a fresh `--selftest`/`--regression` replay at the current pin reproduce the recorded behavior exactly.

## Evidence

### The tick (watchdog anchors)

- `scripts/shokunin-watchdog.sh` is not in the lane repo; it lives at fleet root `/home/vgpnk/Projects/shokunin/scripts/shokunin-watchdog.sh` (fleet repo, git).
- Recorded tick was 2026-10-14T19:15Z. `git rev-list -1 --before='2026-10-14T20:00Z' -- scripts/shokunin-watchdog.sh` → `17c1fad` (watchdog **v4**). At that revision: `:2` "fleet-2 lane map"; `:3-5` "round ends when .ufo/reports/round-<N>/<lane>.md lands … Tick 450s." — matches the claim. `:14` `LANES="protocol aggregator kasegi kengaku kake kumitate kotoba kagi kama"` — **does not name tameshi**. Holds exactly.
- Note: live file is now v5 (lane map moved to `shokunin.conf`, which *does* name tameshi at `:55`, added by `9ee7059` 2026-10-14 09:51 — before the tick; so the claim is only true of the v4 inline `LANES` at `:14`, which is what it cites). Minor reading hazard, not a falsification.

### Six-case pin read — re-executed live (2026-10-20 ~13:57Z)

All six pins verified: `git show <recorded rev>:<path>` sha256 prefix == recorded pin, every row, plus `ancestor=yes` for each recorded rev vs HEAD and porcelain=0 on every path:

| case | recorded rev → blob (== pin) | live HEAD → blob | reading today |
|---|---|---|---|
| kimi-census | 175de6ba → `83016d45` ✓ | 1770305 → `5e8d5913` | **stale** (moved again) |
| surface-census | fecee874 → `275d8294` ✓ | c2cab35 → `275d8294` | current |
| tsukuroi-census | 165307fe → `084951be` ✓ | 6923fe0 → `d17d32a3` | stale |
| mado-verify | eead56b2 → `d7edaab4` ✓ | 27cd06f → `fba82a66` | stale |
| checklist-run | fecee874 → `7e5ec98b` ✓ | c2cab35 → `7e5ec98b` | current |
| claims-check | 175de6ba → `e9a21b44` ✓ | 1770305 → `e9a21b44` | current |

- Observed: 3 × current, 3 × stale, 0 × drift — kimi moved past `175de6ba` to `1770305` with a new blob since the recorded tick, and tsukuroi/mado live blobs moved again (`084951be→d17d32a3`, `d7edaab4→fba82a66`). Confirms the section's own "timestamped observation, re-run at the next tick" framing.
- Tool sha today: `89722ddb` ≠ recorded `cf41efaa` → tool `moved`. `cf41efaa` is real history (lane commit `9f1d3c3`, 2026-10-14 16:06). Chain in lane history: `597e1419` (b58b26f) → `b56c6e57` (4494715) → `cf41efaa` (9f1d3c3) → `75ed934d` (606716f) → `89722ddb` (c699c8c); `4dc69ef9`/`e3f838d4` are absent from committed history (working-tree states) — consistent with "moved four times in one day" as *mtime states*, not all committed.

### Falsifiers executed in scratch

- **stale**: kimi-census row points at superseded blob → reads stale (above). ✓
- **drift**: `git init` scratch repo, committed live `kimi-census.mjs` HEAD blob, appended one line → `git status --porcelain -- gate.mjs` = ` M`; live `bb31f5ff` ≠ HEAD blob `5e8d5913` → drift, both per the rule's two arms. Substrate porcelain: 0 lines after. ✓
- **current**: surface-census / checklist-run / claims-check rows read current (blob == pin at live HEAD). ✓

### Selftest + regression replay (from committed bytes, in /tmp)

- `sha256sum` of materialized `tools/mutate-and-run.sh` at c699c8c: `89722ddb…` (the recorded `cf41efaa` was r7-era; r16 added the seventh leg — expected move).
- `bash mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 81/81 pass`, `VERDICT: PASS`, rc 0 (recorded `67/67` was pre-hardening count; behavior identical, count grew).
- First `--regression` attempt: SETUP rc 2 — tool derives `FLEET_ROOT` as `dirname³($SELF)` so it must sit at `<fleet>/<lane>/tools/`; running it bare in /tmp gives `//kumitate-shokunin` paths. Rebuilt scratch as `fleet/` with symlinks to the four sibling lanes and a copy at `fleet/tameshi-shokunin/tools/`. Re-run rc **0**, 121 s:
  - `REGRESSION: PASS (cases=7 passed=7; ledger legs exact: killed-delta<=0 flips<=0)` — every leg `match=10/10` (checklist `15/15`), `flips=0`, all pins exact (`83016d45…`, `275d8294…`, `084951be…`, `d7edaab4…`, `7e5ec98b…`, `e9a21b44…`, `f890e277…` for js-round-gate at `364f1d59`).
  - Recorded receipt said `cases=4 passed=4` under `cf41efaa` (r7, four embedded legs); current pin embeds seven — consistent growth, same exact-match semantics. Recorded tables hold at their own pinned blobs regardless of live drift: **verified** (all seven legs replayed from `git show <rev>:<path>` while every substrate is dirty/moved).

### Named anchors in T1–T3

- `:811-812` — verified: "A moved substrate needs a re-pin, never a re-interpretation of the old table" (SKILL.md:811-812 at pin).
- `fleet-kill-rate-ledger.md:170-173` — verified verbatim: "…this ledger's embedding line and case count change as an appended row, not an edit of §1–§4" (corpus/knowledge/fleet-kill-rate-ledger.md:171-173).
- `mutation-case-mado-verify.md:17-23` — verified: incident I1 records the sweep/regression under `597e1419`, re-pin to `b56c6e57` at 17:46:15Z, "Recorded, not smoothed" — the T2 precedent, though "identical verdicts and mutant shas" is the note's §7/U3 framing ("reproduction under `b56c6e57…` is U" :230) rather than a completed re-cut at those exact lines. Minor wording slack; the trigger's policy claim is unaffected.

## Tooling installs
None needed (bash/git/python3/node all present; pacman paused per directive).

```json
{"seat":"Replica1021","skill_sha256":"3d8a1edb1803441cfef4ce46447af51a6b857644d8f5347b2aad7c612bbcb7a4","sections":[{"start":1021,"heading":"### The tick and the pin read","class":"record","verdict":"verified-record","blocking_gaps":[],"wrong_expectations":[],"minor_gaps":["the '(:14)' lane-map anchor resolves to watchdog v4's inline LANES at fleet-root revision 17c1fad (correct, no tameshi); the live v5 script moved the map to shokunin.conf where tameshi is named — time-scoped truth, potential reader trap"],"commands_executed":["git rev-list -1 --before=2026-10-14T20:00Z -- scripts/shokunin-watchdog.sh","git show 17c1fad:scripts/shokunin-watchdog.sh | sed -n '1,25p'","per-case: git show <rev>:<path>|sha256sum, rev-parse HEAD, merge-base --is-ancestor, status --porcelain","git init scratch repo; append line; status --porcelain → ' M' drift demo","sha256sum tools/mutate-and-run.sh @c699c8c → 89722ddb"],"opened":["SKILL.md:1021-1091","SKILL.md:808-814","fleet-root scripts/shokunin-watchdog.sh (live + rev 17c1fad)","shokunin.conf:55","tools/mutate-and-run.sh header + leg table"],"scratch":"/tmp/tameshi-r16w2-Replica1021-PKk8YA"},{"start":1069,"heading":"### Triggers T1–T3 and the re-pin rule","class":"record","verdict":"verified-record","blocking_gaps":[],"wrong_expectations":[],"minor_gaps":["mutation-case-mado-verify.md:17-23 records the re-pin incident itself; the 'identical verdicts and mutant shas' re-cut completion is U/framed elsewhere in the note, not at those exact lines"],"commands_executed":["bash /tmp/.../mutate-and-run.sh --selftest → MUTATE_SELFTEST: 81/81 pass, rc 0","bash .../tools/mutate-and-run.sh --regression --workdir .../reg2 --keep → REGRESSION: PASS (cases=7 passed=7), rc 0, all legs match=10/10 (15/15 checklist) flips=0","git show c699c8c:corpus/knowledge/fleet-kill-rate-ledger.md :170-173","git show c699c8c:corpus/knowledge/mutation-case-mado-verify.md :15-25, :230"],"opened":["corpus/knowledge/mutation-case-mado-verify.md:15-25,:230","corpus/knowledge/fleet-kill-rate-ledger.md:170-175","SKILL.md:811-812"],"scratch":"/tmp/tameshi-r16w2-Replica1021-PKk8YA"}]}
```

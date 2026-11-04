# Round-73 recon — reconcile instrument, future rows (seat T73W1S06)

Read-only reconnaissance for `tools/wave-reconcile.py`'s future manifest rows.
Every number below was re-derived from git objects at a **named revision**
(`git cat-file blob <rev>:<path>`, `git ls-tree -r <rev> -- <dir>`), never from a
worktree. No manifest, tool, plan or report was edited.

Pins used (all verified stable during the scan; lane HEAD moved `17cd1939` → `3e0ef1c8`
and fleet HEAD moved `576ee49…` → `c8d1aad…` while scanning, with **no** change to any
artifact byte below — `results blobs identical at lane HEAD=True` for r60 and r72):

| surface | pin |
|---|---|
| round-60 artifacts | lane `e13e0324e048377d7ca5d296294f6f4089240aa0` |
| round-72 artifacts | lane `a3dd35742eee608d1205843dacebc461b4242b9e` (= round-73 base) |
| round-73 artifacts | lane `17cd19396b36d4c15f1bce1bbdb7c42346f1df76` |
| round-60 report | fleet `9f39c5fcb9400667ffb2846dd2183ef9cd5dfe82` |
| round-72 report | fleet `3664a6d30051410c3d2bb8c32926d13e284a5118` |

## 1. Per-round artifact table (rounds 60–73)

| round | report rev (fleet) | wave dir | results rev (last commit) | results.seats | len(results) | committed seat reports | role multiset (results.agent) | attack share (named set) | pinnable |
|---|---|---|---|---|---|---|---|---|---|
| 60 | 9f39c5fcb940 | .ufo/waves/round-60/w1 | e13e0324e048 | 32 | 32 | 2 | task 32 | 0/32 = 0.0% | yes |
| 61 | ab9521f69cca | absent | — | — | — | — | — | — | NO |
| 62 | 224e67321220 | absent | — | — | — | — | — | — | NO |
| 63 | 674b6b7d1f44 | absent | — | — | — | — | — | — | NO |
| 64 | fded7c9b7d0a | absent | — | — | — | — | — | — | NO |
| 65 | 8896e743f6bd | absent | — | — | — | — | — | — | NO |
| 66 | 88b1c187b5d6 | absent | — | — | — | — | — | — | NO |
| 67 | 2b04913e067e | absent | — | — | — | — | — | — | NO |
| 68 | 635c407d9b84 | absent | — | — | — | — | — | — | NO |
| 69 | 7d93c406be30 | absent | — | — | — | — | — | — | NO |
| 70 | 17f2c24131e0 | absent | — | — | — | — | — | — | NO |
| 71 | 449987085bdb | absent | — | — | — | — | — | — | NO |
| 72 | 3664a6d30051 | .ufo/waves/round-72/w1 | 56866fa37ec4 | 12 | 12 | 12 | connector 1, critic 1, executor 3, mutation-tester 1, revenger 1, reviewer 1, scout 1, scribe 2, sentinel 1 | 3/12 = 25.0% | yes |
| 73 | ABSENT (no fleet tameshi.md) | w1-dispatch/w1-run.stderr/w1-spec only; `w1/` untracked in flight | — | — | — | — | — | — | NO |

Corroborating artifact bytes:

* round-60 results `sha256=68db527a98728dde…` (6791 bytes), `settled=2`,
  `dead_or_never_spawned=30`, 30 records carry a `note` and empty `output`
  (the cap-cancelled 30); committed top-level seat reports are exactly
  `T60W1S01.md`, `T60W1S02.md` (= 2), and `w1.ready.partial` names the same two seats
  (`{"T60W1S01": "T60W1S01", "T60W1S02": "T60W1S02"}`) — three independent reads of "2".
* round-60 spec is `.ufo/waves/round-60/spec-w1.json` (items=32, 8 roles), **not**
  `w1-spec.json`: the `w?-spec.json` glob does not match it (`ls .ufo/waves/round-60/w*-spec.json`
  → no match; `ls .ufo/waves/round-60/spec-*.json` → `.ufo/waves/round-60/spec-w1.json`).
* round-72 results `sha256=037b8f4dca5885fe…`, no `settled`/`dead_or_never_spawned` keys
  (schema drift vs r60), 0 records with `note`; 12 top-level `*.md` at the pin.
* round-72 spec `w1-spec.json` items=12, role multiset **equals** the results' `agent`
  multiset exactly (the manifest's `r72-spec-roles` green arm).
* round-73 spec `w1-spec.json` (`sha256=e0f93ae51579ef55…`) items=13:
  `executor 3, scribe 2, scout 1, reviewer 2, critic 1, mutation-tester 1, sentinel 1,
  revenger 1, connector 1`; attack under the named set 4/13 = 30.8%; no `labrat`, no
  `planner`. The spec is committed; `w1-results.json` exists at **no** rev.
* dispatch `counts.total` (a third independent seat-count source, no row kind reads it):
  round-60 32, round-72 12, round-73 13 — each equal to that wave's spec item count.

`results.seats` vs `len(results)`: **no disagreement** on any round that has results
(60: 32=32; 72: 12=12; rounds without results: n/a).

## 2. Every seat/report-count claim in the swept reports, against the artifacts

Claim spans verified by direct byte slicing of the blob at the report rev
(`raw[a:b].decode('utf-8')` == the quoted token for all eleven spans, §7).

Round-60 report (fleet `9f39c5fc`, 17631 bytes, CRLF):

| line | bytes | span text | printed | artifact derivation | verdict |
|---|---|---|---|---|---|
| 115 | `[6919:6927]` | `32 seats` | 32 | `results.seats`=32, `len(results)`=32 | meet |
| 115 | `[6929:6941]` | `settled 2/32` | 2 | `results.settled`=2; top-level `*.md`=2; `w1.ready.partial`=2 | meet |
| 273 | `[16803:16811]` | `32 seats` | 32 | `results.seats`=32, `len(results)`=32 | meet |
| 273 | `[16813:16822]` | `2 settled` | 2 | `results.settled`=2; top-level `*.md`=2 | meet |
| 273 | `[16824:16840]` | `30 cap-cancelled` | 30 | `results.dead_or_never_spawned`=30; 32−2=30 | meet |

Round-72 report (fleet `3664a6d3`, 18439 bytes, LF):

| line | bytes | span text | printed | artifact derivation | verdict |
|---|---|---|---|---|---|
| 7 | `[416:424]` | `12 seats` | 12 | `results.seats`=12, `len(results)`=12 | meet |
| 56 | `[3618:3626]` | `12 seats` | 12 | `results.seats`=12 | meet |
| 56 | `[3628:3638]` | `11 reports` | 11 | top-level `*.md` at `a3dd3574` = **12** | **DRIFT** |
| 81 | `[5786:5794]` | `12 seats` | 12 | 12 `*.md`, 12 result records, 0 with `note` | meet |
| 82 | `[5874:5889]` | `12 seat records` | 12 | `len(results)`=12 | meet |
| 84 | `[6029:6037]` | `12 seats` | 12 | `results.seats`=12 | meet |

Rounds 61–71: `grep -c -i seat <report>` = **0** for each — they are self-declared
`L1-only round` reports and carry no seat or report count at all. Round 73: no report.

## 3. Disagreements

**D1 — the only record-claim disagreement found (round 72).**
Round 72, report rev `3664a6d30051`, byte span `[3628:3638]` = `11 reports`
(line 56, inside `- **The wave** (see "Wave" below): 12 seats, 11 reports; …`).
Artifact: `git ls-tree -r --name-only a3dd3574 -- .ufo/waves/round-72/w1` holds
**12** top-level `*.md` (`T72W1S01.md` … `T72W1S12.md`), and `w1-results.json` has
`seats=12`, `len(results)=12`, **0** records with `note`. Printed 11 ≠ 12 → drift.
Measured by the instrument itself (scratch probe manifest, §7):
`WAVE_ROW r72-report-seatreports-probe kind=seat_reports expect=drift measured=drift ok | printed=11 files=12`.

**D2 — artifact-vocabulary mismatch, *not* a record claim (round 60).**
Round-60 `spec-w1.json` declares 8 roles over 32 items
(`executor 9, scribe 4, scout 3, reviewer 7, mutation-tester 3, critic 2, connector 2, sentinel 2`)
while round-60 `w1-results.json` records `agent = "task"` for all 32. A `roles`
(spec-items) row therefore reads drift on r60 **for structural reasons**, and
`attack_share` reads `0/32 = 0.0%` (declared attack roles would be 7+2+3 = 12/32 =
37.5 %). Counted separately, not as a record lie: the r60 report never claims a role
multiset. No `plans/round-60*.plan.md` contains an `N role` declaration, so the
`text-tokens` form has no binding either.

No other disagreement was found: 11 claim spans across two claim-bearing reports,
10 meet, 1 drift.

## 4. Rounds with no `results.json` (unpinnable rows)

* **Rounds 61–71 (11 rounds).** No `.ufo/waves/round-N` path exists in **any** ref:
  `git log --all --pretty=format: --name-only -- .ufo/waves | grep -o '\.ufo/waves/round-[0-9]*' | sort -u`
  lists rounds `12–60, 72, 73` only; counting rounds 61–71 in that output → **0**
  (2181 refs scanned). Each of the 11 reports self-declares `L1-only round`, i.e. no
  wave was dispatched, so no artifact can be pinned. Fleet-level `.ufo/waves/` holds
  no tameshi round-61…71 wave either (`.ufo/waves/round-62/w2` is empty and mentions
  `tameshi` nowhere).
* **Round 73** is *in flight*, not historically unpinnable: `w1-spec.json`,
  `w1-dispatch.json`, `w1-run.stderr` are tracked at `17cd1939`; `w1/` (seat reports)
  and `w1.ready*` are untracked in the working tree and `w1-results.json` does not
  exist. Any r73 wave row today is a setup error —
  `WAVE_RECONCILE error=setup:git-failed:.:fatal: path '.ufo/waves/round-73/w1-results.json' does not exist in '17cd19…'`, exit 2.

## 5. Future-row viability, measured (scratch probe manifest, no repo edit)

| round | `seats` | `seat_reports` | `roles` (spec-items) | `roles` (text-tokens) | `attack_share` |
|---|---|---|---|---|---|
| 60 | meet (printed 32) | meet (printed 2); **drift** if printed 32 | drift ({8 roles} vs {task:32}) | no declaration exists | drift at floor 25 (0.0 %), meet at floor 0 |
| 72 | meet (printed 12) | **drift** (printed 11 vs 12) | meet (spec ≡ results) | drift (plan has `1 labrat`, results have `revenger`) | meet (3/12 = 25.0 % at floor 25) |
| 73 | setup exit 2 | setup exit 2 | n/a (no results) | n/a | setup exit 2 |

Round-72 plan role span, byte-verified at `a3dd3574`: bytes `[7042:7176]` of
`plans/round-72.plan.md` (7372 bytes) contain all nine `N role` tokens including
`1 labrat` — the manifest's standing red arm is constructible exactly as declared.

## 6. Counts

```
rounds_scanned=14 disagreements=1 unpinnable=11
```

`rounds_scanned` = rounds 60–73 (13 fleet `tameshi.md` records present + round 73
in flight). `disagreements` = record-claim-vs-artifact disagreements (D1 only;
D2 is an artifact-vocabulary mismatch, declared separately). `unpinnable` = rounds
61–71, which have no `results.json` (indeed no wave path) in any of 2181 refs;
round 73 is in flight and is **not** counted in that 11.

## 7. Commands and raw output

See the seat report `.ufo/waves/round-73/w1/T73W1S06.md` §Evidence for the full
transcripts and `.ufo/waves/round-73/w1/T73W1S06/scripts/` for the scripts that produced
them (identical bytes to the scratch copies named below; the scratch tree is deleted
before yield). The five load-bearing ones are reproduced here.

```
$ python3 -I -X utf8 /fast/scratch/hyaku/tameshi-r73/T73W1S06/pin-evidence.py 2>&1 | tee pin-evidence.txt
## round-60 (lane pin e13e0324e048)
  results sha256=68db527a98728dde
  seats=32 len(results)=32 agent_multiset={"task": 32}
  committed top-level seat reports=2 ['T60W1S01.md', 'T60W1S02.md']
  attack named-set=['reviewer', 'critic', 'mutation-tester', 'labrat'] counted=0/32=0.0%
  results blob identical at lane HEAD=True
  spec .ufo/waves/round-60/spec-w1.json sha256=ed0c3ed240828ad7 items=32 roles={"connector": 2, "critic": 2, "executor": 9, "mutation-tester": 3, "reviewer": 7, "scout": 3, "scribe": 4, "sentinel": 2}
  fleet report rev=9f39c5fcb940 bytes=17631 sha256=10df66971a7a773e

## round-72 (lane pin a3dd35742eee)
  results sha256=037b8f4dca5885fe
  seats=12 len(results)=12 agent_multiset={"connector": 1, "critic": 1, "executor": 3, "mutation-tester": 1, "revenger": 1, "reviewer": 1, "scout": 1, "scribe": 2, "sentinel": 1}
  committed top-level seat reports=12 ['T72W1S01.md', 'T72W1S02.md', 'T72W1S03.md', 'T72W1S04.md', 'T72W1S05.md', 'T72W1S06.md', 'T72W1S07.md', 'T72W1S08.md', 'T72W1S09.md', 'T72W1S10.md', 'T72W1S11.md', 'T72W1S12.md']
  attack named-set=['reviewer', 'critic', 'mutation-tester', 'labrat'] counted=3/12=25.0%
  results blob identical at lane HEAD=True
  spec .ufo/waves/round-72/w1-spec.json sha256=4ac6460989c8acfa items=12 roles={"connector": 1, "critic": 1, "executor": 3, "mutation-tester": 1, "revenger": 1, "reviewer": 1, "scout": 1, "scribe": 2, "sentinel": 1}
  fleet report rev=3664a6d30051 bytes=18439 sha256=ff1286c8d8d0ec9d

## round-73 (lane pin 17cd19396b36)
  results: ABSENT at pin -> row setup error exit 2
  spec .ufo/waves/round-73/w1-spec.json sha256=e0f93ae51579ef55 items=13 roles={"connector": 1, "critic": 1, "executor": 3, "mutation-tester": 1, "revenger": 1, "reviewer": 2, "scout": 1, "scribe": 2, "sentinel": 1}
  fleet report: ABSENT (no .ufo/reports/round-73/tameshi.md)
```

```
$ cd /home/vgpnk/Projects/shokunin/tameshi-shokunin && python3 -I -X utf8 tools/wave-reconcile.py --repo . --extra-root fleet=/home/vgpnk/Projects/shokunin --manifest /fast/scratch/hyaku/tameshi-r73/T73W1S06/probe-r60.json
WAVE_ROW r60-report-seats kind=seats expect=meet measured=meet ok | printed=32 seats=32 records=32
WAVE_ROW r60-settled-as-seatreports kind=seat_reports expect=meet measured=meet ok | printed=2 files=2
WAVE_ROW r60-seats-as-seatreports kind=seat_reports expect=drift measured=drift ok | printed=32 files=2
WAVE_ROW r60-spec-roles kind=roles expect=drift measured=drift ok | declared={"connector": 2, "critic": 2, "executor": 9, "mutation-tester": 3, "reviewer": 7, "scout": 3, "scribe": 4, "sentinel": 2} measured={"task": 32}
WAVE_ROW r60-attack-floor25 kind=attack_share expect=drift measured=drift ok | attack=0/32=0.0% floor=25.0%
WAVE_ROW r60-attack-floor0 kind=attack_share expect=meet measured=meet ok | attack=0/32=0.0% floor=0.0%
WAVE_ROW r72-report-seatreports-probe kind=seat_reports expect=drift measured=drift ok | printed=11 files=12
WAVE_RECONCILE: rows=7 met=7 unexpected=0
exit=0
```

```
$ cd /home/vgpnk/Projects/shokunin/tameshi-shokunin && python3 -I -X utf8 tools/wave-reconcile.py --repo . --extra-root fleet=/home/vgpnk/Projects/shokunin --manifest /fast/scratch/hyaku/tameshi-r73/T73W1S06/probe-r73.json
WAVE_RECONCILE error=setup:git-failed:.:fatal: path '.ufo/waves/round-73/w1-results.json' does not exist in '17cd19396b36d4c15f1bce1bbdb7c42346f1df76'
exit=2
```

```
$ cd /home/vgpnk/Projects/shokunin/tameshi-shokunin && git log --all --pretty=format: --name-only -- .ufo/waves | grep -o '\.ufo/waves/round-[0-9]*' | sort -u | grep -E 'round-(61|62|63|64|65|66|67|68|69|70|71)$' | wc -l
0
$ git rev-list --all --count
2181
```

```
$ test "$(git rev-parse 56866fa3:.ufo/waves/round-72/w1-results.json)" = "$(git rev-parse a3dd3574:.ufo/waves/round-72/w1-results.json)" && echo "results blob: identical"
results blob: identical
$ diff <(git ls-tree -r --name-only 56866fa3 -- .ufo/waves/round-72/w1) <(git ls-tree -r --name-only a3dd3574 -- .ufo/waves/round-72/w1) && echo "w1 listing: identical"
w1 listing: identical
```

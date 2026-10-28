# T55W1ExecFooterPaths — wave artifact hygiene (round 55, wave 1)

Seat: `T55W1ExecFooterPaths` (executor, leaf). L1 `TameshiR55`, hyaku run 11.
Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Axis: operability. Milestone: wave artifact hygiene.
Snapshot: `git rev-parse HEAD` = `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`
(`round-55: C0 — one scratch-root line in three tools …`, committed 2026-10-28 14:16:39 -0300);
status read at 2026-10-28T14:18:57-03:00 / 17:18:57Z. The tree was **still moving** during the audit
(seats running, wave 2 being dispatched); every number below is pinned to that snapshot and the receipt
that produced it in `T55W1ExecFooterPaths-receipts/`.

I wrote no lane production file. All probes were reads or writes inside my own seat dir; my scratch dir
(`/fast/scratch/hyaku/tameshi-r55/T55W1ExecFooterPaths`) held nothing and was removed. **No tool was installed
or upgraded** for this seat (`git`/`find`/`sha256sum`/`python3` sufficed); no pacman transaction was attempted,
so the host-wide pause was not touched.

---

## Verdicts at a glance

| # | check the item asked for | verdict | receipt |
|---|---|---|---|
| 1 | every `Report:` path a seat was handed resolves under `.ufo/waves/round-55/w1/` | **PASS** 75/75 | `02-report-paths.txt` |
| 1b | (the same handoffs also name a *second* write path) | **FAIL** — 6 seats told to write `T55W1Er10.{md,json}`; one seat's report was destroyed | `12-er10-handoff-instructions.txt`, `07`, `09`, `10` |
| 2 | every seat report exists, or the seat is dead | **59 exist / 16 absent, all 16 live ⇒ 0 dead** | `03-seat-deliverables.txt` |
| 3 | no seat wrote a file outside the wave dir | **PASS for seat-named files** (0 outside); **2 unattributed writes to `.ufo/evidence/round-55/` after the snapshot** — one destroyed the contract's base receipt in the worktree | `01-status-snapshot.txt`, `04-writes-outside-wave.txt`, `13-outside-wave-evidence-writes.txt` |
| 4 | no file under the wave dir exceeds 2 MiB | **FAIL** — 5 files, 15.1 MB of the 25 MB wave dir | `05-oversize.txt` |
| 5 | no scratch tree under `/tmp` names tameshi-r55 | **FAIL** — 2 trees, 3.1 GB, from one seat, second one created during this audit | `06-tmp-scratch.txt` |
| 6 | census conformance (round-start/end gate) | **PASS** — exit 0, 140 rows, last `S280` | `08-census.txt` |
| — | frozen counter set untouched | **PASS** 7/7 pins match working tree and HEAD | (freeze-pin probe, quoted below) |

---

## 1. `Report:` trailer paths — 75/75 resolve under the wave dir

Command: parse `.ufo/waves/round-55/w1-dispatch.json` (the dispatched text, not the spec), take the last
`Report: write your scoped findings to <path>` per task, `os.path.normpath` it and compare.

```
$ python3 - <<'PY'   # full script in T55W1ExecFooterPaths-receipts/02-report-paths.txt
... last 'Report:' trailer per task; normpath vs wave dir; basename vs seat id
SUMMARY trailers= 75 escaping_wave= 0 basename_mismatch= 0
escaping: []
basename_mismatch: []
```

- 75 tasks ↔ 75 registry members ↔ 75 distinct seat ids.
- Every trailer is relative, normalizes inside `.ufo/waves/round-55/w1/`, and its **basename equals the
  seat id** (`T55W1<Seat>.md`). No `..`, no absolute path, no duplicate target.
- No seat was handed a trailer path that escapes the wave dir.

### 1b. The handoff also names a second path: six seats were pointed at `T55W1Er10.{md,json}`

The trailer is clean; the **item prose** is not. Six seats whose own report is `T55W1<Seat>.md` were also
told, by bare filename (so resolving against the fleet-root cwd, not the wave dir), to write the file that
belongs to seat `T55W1Er10` (milestone `C1 R54.10 correction draft`):

```
$ python3 - ... (T55W1ExecFooterPaths-receipts/12-er10-handoff-instructions.txt)
seats naming T55W1Er10.* in their item text: 7
  T55W1Er10                  Write `…/w1/T55W1Er10.json` as `{"id": "R54.10", …}` and the same facts in `T55W1Er10.md`   <- OWNER
  T55W1ScribeNote            … Draft only; write `T55W1Er10.md`.                                                         <- collision
  T55W1ScribeCells           Write `T55W1Er10.json` (row name -> new cell) and `T55W1Er10.md`.                           <- collision
  T55W1ScribeSources         Write `T55W1Er10.json` (rows) + `T55W1Er10.md` (quotes + locators).                          <- collision
  T55W1ScribeConsiderthese   … Write `T55W1Er10.md`.                                                                     <- collision
  T55W1ScribeMistakeSweep    … write `T55W1Er10.md` with the command and output for each …                                <- collision
  T55W1ExecRekeyPrep         Write the JSON the L1's binder needs as `T55W1Er10.json`.                                   <- collision
```

`T55W1ExecRekeyPrep`'s instruction is additionally *load-bearing for the binder* ("the JSON the L1's binder
needs"), so the collision is not cosmetic. `T55W1RevWave` reached the same six-instruction list from its own
spec scan (`T55W1RevWave-receipts/collision.txt` §A); my scan over the *dispatched* text reproduces it, which
is what makes the defect real in the prompts rather than only in the spec.

**Realized damage (the finding).** The owner's two deliverables no longer exist anywhere on disk or in the
integration commit. Byte evidence:

```
$ git cat-file -s HEAD:.ufo/waves/round-55/w1/T55W1Er10.md      -> 1181   (a pointer file, not Er10's report)
$ git cat-file -p HEAD:…/T55W1Er10.md | sha256sum               -> f32e5359…
$ git cat-file -s HEAD:.ufo/waves/round-55/w1/T55W1Er10.json    -> 11908  sha256 a70ea19d…  == T55W1ExecRekeyPrep.json
$ sha256sum .ufo/waves/round-55/w1/T55W1Er10.{md,json}          (working tree)
  0d0c62fc…  T55W1Er10.md      6690 B   first line: "# Draft: `corpus/knowledge/scratch-root-contract.md` → `## One line, every mode (round 55)`"  (seat T55W1ScribeNote)
  a70ea19d…  T55W1Er10.json   11908 B   "seat": "T55W1ExecRekeyPrep"
$ grep -rl "2e15a640\|128c8e83" .ufo/waves/round-55/w1/   -> only seats *describing* the loss, no copy of the bytes
```

Owner-collision scan over all seat deliverables (`07-owner-collisions.txt`): exactly **two** mismatches in
the wave — `T55W1Er10.md` (declared owner `T55W1ScribeNote`) and `T55W1Er10.json` (declared owner
`T55W1ExecRekeyPrep`); 59 `.md` and 42 `.json` checked.

Er10's own yielded deliverables were (`history://T55W1Er10`, owner restating after a peer restore):
`T55W1Er10.json` 3640 B sha256 `2e15a640…` (`id: R54.10`, `derived: "controls-a rekeyed=0/7"`),
`T55W1Er10.md` 11366 B sha256 `128c8e83…`. The loss is a **recurrence**: seats `T55W1RevWave`
(`T55W1RevWave-receipts/collision.txt`, `collision-recurrence.txt`) already observed occurrence 1
(13:56:04) and occurrence 2 (14:01:39, the rekey JSON) and `T55W1ScribeSources` repaired occurrence 1 at
13:58:54. After that repair the `.md` was overwritten **again** — by `T55W1ScribeMistakeSweep` (its pointer
file, the bytes committed at 14:16:39: `collision-recurrence.txt` still records 11366 B at 14:02:46, the
commit holds 1181 B, so the write is bounded to 14:02:46–14:16:39) and then by `T55W1ScribeNote` (the current
working-tree draft, 6690 B) — and no one restored it, because Er10 was parked by then. So: occurrence 3.

**Recovery is still possible** and is the L1's call (I did not touch the files): the R54.10 content survives
in `T55W1Er10-receipts/` (10 files, incl. `lane-worktree-corrections-section.txt`,
`c1-with-r54.10-correction.stdout`, `receipts-verified.txt`), and `T55W1ScribeSources-receipts/peer-er10-restore.txt`
records the exact replay procedure that reconstructed both blobs byte-exact once (write/edit parts of
`history://T55W1Er10`'s session log). The `.json` (3640 B) is recoverable the same way.

Second-order hazard the collision created: the RekeyPrep JSON now sitting at `T55W1Er10.json` carries a
self-defence key — `"_not_a_reader_report": "… so a round-55 binder that globs .ufo/waves/round-55/w1/*.json
cannot mistake it for a reader report and bind it."` A binder that globs by path pattern rather than by
`seat`/`heading` will bind the wrong file whoever wins the next race.

---

## 2. Seat reports: 59 present, 16 absent, and all 16 absent seats were live (0 dead)

Command: `dispatch` seat list × `os.listdir('.ufo/waves/round-55/w1')`, status column from the bare
`history://` roster read at 2026-10-28T14:17-03:00 with suffixed re-spawns (`-2`, `-3`, `-4`, `-5`)
collapsed onto the base seat id. Full table: `03-seat-deliverables.txt`.

**Present (59 `T55W1<Seat>.md`).** Every seat not listed below.

**Absent at snapshot (16), with the status the roster gave them — all live, none dead:**

| seat | role | status at 14:17 | what exists instead |
|---|---|---|---|
| `T55W1ExecNote` | executor | running | `-receipts/` only |
| `T55W1ExecC2Full` | executor | running | `-receipts/` only |
| `T55W1CritC2` | critic | running | nothing yet |
| `T55W1MutC1` | mutation-tester | running | nothing yet |
| `T55W1MutC2` | mutation-tester | running | `-receipts/` only |
| `T55W1SentConfig` | sentinel | running | nothing yet |
| `T55W1Revenger` | revenger | running | nothing yet |
| `T55W1Simplifier` | simplifier | running | nothing yet |
| `T55W1RevLedger` | reviewer | running | nothing yet |
| `T55W1CritClaimShape` | critic | running | nothing yet |
| `T55W1CritGate` | critic | running | nothing yet |
| `T55W1RevRekeyByteProof` | reviewer | running | nothing yet |
| `T55W1ExecRegistryGate` | executor | running | nothing yet |
| `T55W1ExecCensusAfter` | executor | running | `-receipts/` only |
| `T55W1CritSourcedClaim` | critic | running | nothing yet |
| `T55W1ExecFooterPaths` | executor | running | this report |

**Dead seats with a missing report: none.** (A dead seat is one parked/finished with no report; the roster
showed 0 in that state. `T55W1Er10` is parked and *its own* report is missing — but a file bearing its
name exists holding other seats' content, which §1b treats as a collision, not as a dead seat.)

Note on churn: `T55W1LabEmpty.md`, `T55W1ScribeCells.md` and two other reports landed **between two
listings** minutes apart, and `T55W1ScribeNote.md` was rewritten twice. The 16 above is a snapshot, not a
gate: re-run receipt `03` at the content freeze for the count that matters.

Report sizes: smallest real report 771 B (`T55W1ExecReKeyDryBind.reader.md`), next 6690 B (the mis-owned
`T55W1Er10.md`), then ≥ 8 KB. No zero-byte `.md` reports (`11-thin-or-empty.txt`).

---

## 3. Writes outside the wave dir — no seat-named file, but two writes to the round's evidence

### 3a. Seat writes: none

```
$ git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin status --porcelain | grep -v '.ufo/waves/round-55/w1/' 
?? .ufo/evidence/round-55/control/
?? .ufo/waves/round-55/build-spec-w2.py
?? .ufo/waves/round-55/spec-w2.json
?? .ufo/waves/round-55/w2-dispatch.json
?? .ufo/waves/round-55/w2-run.err
?? .ufo/waves/round-55/w2.ready
?? .ufo/waves/round-55/w2.ready.partial
?? .ufo/waves/round-55/w2/
```

At the pinned snapshot the porcelain had **99 entries: 91 under `.ufo/waves/round-55/w1/`, 8 outside** (the
eight above). Re-read minutes later the eight were still the whole out-of-wave set apart from three new
entries named in §3b and `spec-w3.json` (wave 3 being built); the in-`w1/` count grew from 91 to 147 with no
new out-of-wave seat file. The split is stable even though the counts are not.

Supporting checks (`04-writes-outside-wave.txt`):

- `find . -name 'T55W1*' -not -path './.ufo/waves/round-55/w1/*'` → **empty** (no seat-named file was written
  anywhere else in the lane).
- `find /home/vgpnk/Projects/shokunin -maxdepth 4 -name 'T55W1*' -not -path '*/tameshi-shokunin/*'` → **empty**.
- `git show --name-only 9cf0146 | grep -v '^.ufo/waves/round-55/'` → **13 files**, exactly the L1's integration
  set: `SKILL.md`, `SCORECARD.md`, `LOG.md`, `corpus/{QUALITY.md,SOURCES.md,knowledge/scratch-root-contract.md,
  lessons/round-54.md,lessons/round-55.md}`, `tools/{repeat-control.py,context-capture.py,registry-check.py,
  registry.json}`, and `.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md` (the R54.8 supersede annotation).
  No seat-attributable production write is in it.
- Frozen counter set: all **7/7** `freeze.json` pins match both the working tree and `HEAD`
  (`contract.json`, `c1/measure.py`, `c2/measure.py`, `no-harm.sh`, `deciding-run.sh`, `controls.sh`,
  `c1/staged-at-freeze.txt`). No seat edited a frozen byte.

The eight non-w1 entries are **not** seat writes: `w2*`, `spec-w2.json`, `build-spec-w2.py` are the L1 opening
wave 2 (mtime 14:18-14:19, after the w1 commit); `.ufo/evidence/round-55/control/controls-a.stdout` (120 B,
14:16:55) is the control phase's own receipt:

```
CTL CTL_0_c1 C1_R55: rev=0a2010acd1e9 classes=10 premise=9/10 stale=4 classes_corrected=0/10 total=10 C1_R55_PASS=false
```

It matches the frozen `before/c1.stdout` verdict at base, so it is a control scored at the base revision
(the round's do-nothing arm), not a seat escaping its dir. I report its existence, I do not judge it.

Caveat on method: the wave dir was **untracked** until the 14:16:39 commit, so `git status` cannot see what a
seat wrote and later deleted outside the wave dir before that commit. What is provable is the state at
snapshot plus the commit's file set; both are clean.

### 3b. Two writes to `.ufo/evidence/round-55/` after the snapshot — one destroyed the base receipt

These appeared **after** my 14:18:57 snapshot, so they are not in the 8 above. Neither carries a seat id and
no wave-1 report claims the write, so I report them unattributed rather than accuse a seat
(`13-outside-wave-evidence-writes.txt`).

**(i) `.ufo/evidence/round-55/before/c2.stdout` was truncated in place — the contract's `before` receipt.**

```
mtime 14:21:48 (1023 B, 17 lines) -> 14:22:04 (1672 B, 28 lines), then stable through 14:23:05
HEAD blob : 2696 B, 44 lines, last line
            C2_R55: rev=0a2010acd1e9 grammar=6/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=0/7 note=0/9 skill=0/1 total=21 C2_R55_PASS=false
worktree  : 28 lines, last line "EXPLAIN usable repeat-control --selftest          rc=0  ok"   (verdict line gone)
$ git diff -- .ufo/evidence/round-55/before/c2.stdout   -> 26 EXPLAIN lines + the C2_R55 verdict removed
```

The bytes are intact at `HEAD`, so nothing is lost (`git show HEAD:…` reproduces all 44 lines). But the
contract's `before` field and the SCORECARD block quote this path, and the file on disk now ends mid-run.
This is a **recurrence**: `T55W1RevNote` already filed it as finding `I4` (receipt
`T55W1RevNote-receipts/13-freeze-and-record-integrity.txt`: the file "went 43 lines -> the verdict line
only"), i.e. the same path has been rewritten at least twice, in opposite directions (full → 1 line → prefix).
`before/*.stdout` is **not** in the contract's `frozen_paths` (which lists 8 files and no `before/` entry), so
no freeze check can see this; the write is legal by the letter of the freeze and destructive in fact.

**(ii) `.ufo/evidence/round-55/c1/lost-headings-at-c0.json` — a new file inside the frozen counter's directory.**

```
2026-10-28 14:19:59  1081 B  sha256 dcfc9f800b8bc7b2…
```
It is a JSON list of SKILL.md section headings (the binder's `HEADINGS` input). It is not a copy of any wave-dir
file (`T55W1ExecRekeyPrep-receipts/lost-headings-at-c0.json` is 22 B sha `315b7ba9…`,
`T55W1RevColdread-receipts/lost-headings-at-c0.json` is 3413 B sha `a24a6910…`), so it is a third artifact that
lives **only** outside the wave dir. Seats cite the bare name as an input (`T55W1ExecReKeyDryBind.md:138`:
"`HEADINGS` was `lost-headings-at-c0.json ∪ lost-headings-at-base.json`"); none records writing it. Same blind
spot: `c1/` is a directory the freeze pins two *files* in, not the directory itself.

---

## 4. Files over 2 MiB inside the wave dir — 5 files, 15.1 MB

```
$ find .ufo/waves/round-55/w1 -type f -size +2M -printf '%s\t%p\n' | sort -rn
3034041  …/T55W1ExecRekeyPrep-receipts/cand.json
3033847  …/T55W1ExecRekeyPrep-receipts/base.json
3022874  …/T55W1ExecRekeyPrep-receipts/rekey.json
3022874  …/T55W1ExecRekeyPrep-receipts/floor.json
3022874  …/T55W1ExecNoHarm-receipts/coldread-at-base.json
count = 5        (2 MiB = 2097152; wave dir total 25 MB / 1332 files)
```

All five are machine dumps of a cold-read/ledger JSON (each ~3 MB, identical shape), committed in `9cf0146`.
Two seats: `T55W1ExecRekeyPrep` (4) and `T55W1ExecNoHarm` (1). Next largest is `T55W1ExecReKeyDryBind-receipts/
bound-entry.json` at 758 KB, so the cliff is sharp: these five are full-ledger dumps where a section list or a
digest table would have been enough. They are **inside** the wave dir, so no discipline was broken — they break
the item's stated 2 MiB bound and they are 60% of the wave's bytes.

---

## 5. `/tmp` scratch naming tameshi-r55 — 2 trees, 3.1 GB, one seat

```
$ find /tmp -maxdepth 1 -name '*tameshi-r55*' -printf '%TY-%Tm-%Td %TH:%TM %p\n'
2026-10-28 14:02 /tmp/tameshi-r55-grammarbreak
2026-10-28 14:19 /tmp/tameshi-r55-grammarbreak2
$ du -csh /tmp/tameshi-r55-* | tail -1
3.1G    total
```

Both belong to `T55W1ExecGrammarBreak` (running throughout the audit; the `2` tree appeared **during** this
audit at 14:19). Each holds a `patched/` clone plus `wt-1…wt-4` worktrees at ~250-273 MB apiece. The seat's own
report states the choice (`T55W1ExecGrammarBreak.md` §F4: *"everything with the fixture under `/tmp` and only
the counter's `--work` directories under `/fast/scratch`"*), so this is a deliberate deviation from the seat
scratch rule (`HYAKU_SCRATCH/tameshi-r55/<seat>`, `/tmp` only for files under 50 MB — these are 250 MB
clones ×5 in each tree), not a stray `mktemp`.

Adjacent class the asked pattern misses (`06-tmp-scratch.txt`): 13 further `/tmp/tameshi-*` trees from this
wave's window, including `/tmp/tameshi-registry-check-u9ffi_ub` (14:01), `/tmp/tameshi-mte-fleet-2zlazyba` and
`/tmp/tameshi-mte-regression-uv23wm_1` (14:11), and six `/tmp/tameshi-r17-registry-check-selftest.*` (14:19).
Those are the tools' own `mkdtemp` scratch (`tameshi-` + tool name), not seat fixtures, but they are the same
hygiene surface and they also outlive their run. The lane's real scratch root
`/fast/scratch/hyaku/tameshi-r55/` held **53** seat dirs at measurement (63 at the round-end re-run, i.e. it
grows with the wave and is not cleaned either — out of scope for this item, named for the L1).

---

## 6. Census conformance

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
tameshi  ok  /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
EXIT=0
$ grep -cE '^\| S[0-9]{3} ' corpus/SOURCES.md   -> 140     (last id: S280)
```

Exit 0; 140 rows (the 139-row S001-S279 set plus the round's `S280`). W01/W04 advisories only.
Re-run at the end of this seat (14:24 local, after the wave moved): **exit 0, 140 rows** again
(`08-census.txt`, "ROUND-END RE-RUN" block).

---

## Observations that are not violations (for the L1's judgement, no action taken)

1. **141 zero-byte files** in the wave dir, all receipts (`.err`/`.stderr`/`.out` captures) — an empty capture
   and a never-written receipt are indistinguishable by `ls` (`11-thin-or-empty.txt`). Any receipt check that
   only tests existence would score them.
2. **Committed receipts deleted in the working tree** by their own seat: `T55W1ExecGrammarBreak-receipts/` has
   17 `D` entries at snapshot (baseline/`mut*`/`status-fast.txt`) replaced by `nine-allocating-modes` receipts.
   In-wave and seat-owned, so allowed; but a `D` on a *committed* receipt is a re-write of scored evidence after
   the commit, and the L1 should know before integrating.
3. **One wave-dir entry names no seat**: `T55W1ScribeLesson-draft-round-55.md` (the convention is
   `T55W1<Seat>.md` / `.json` / `-receipts/`). Harmless; noted because the owner scan is path-based.
4. `T55W1ExecReKeyDryBind` also carries `T55W1ExecReKeyDryBind.reader.md` / `.reader.json` (771 B / 970 B) —
   reader-shaped side deliverables outside the seat-file convention. They do not declare a `seat` key, so my
   owner scan skipped the pair rather than mis-attributing it.
5. The wave dir contains `swarm-registry.json` (harness file) — expected, excluded from the owner scan.

---

## What I would ask the L1 to do (none of it is mine to land)

1. **Fix the six handoff texts** (`T55W1ScribeNote`, `ScribeCells`, `ScribeSources`, `ScribeConsiderthese`,
   `ScribeMistakeSweep`, `ExecRekeyPrep`): the target must be the seat's own `.md`/`.json` under
   `.ufo/waves/round-55/w1/`, never `T55W1Er10.*`. The dispatcher is `build-spec-w1.py`; the same literal is
   probably in the wave-2 spec, so grep `spec-w2.json` for `T55W1Er10` before wave 2 runs.
2. **Restore `T55W1Er10.{md,json}`** from the receipt-documented replay before the corrections section is
   declared complete, and record the third occurrence in the lesson (`RevWave`'s two receipts plus
   `10-er10-loss.txt`).
3. **Bound receipt size** at the 2 MiB rule, or state that the rule is not a rule: 5 files break it today.
4. **Restore `.ufo/evidence/round-55/before/c2.stdout` from `HEAD`** (44 lines, 2696 B) before quoting it in the
   SCORECARD block, and close the blind spot: `frozen_paths` names 8 files and no `before/` or `c1/`
   *directory*, so a worktree rewrite of the base receipt and a new file inside `c1/` are both invisible to
   `FROZEN_UNCHANGED` (this round's §3b, and `T55W1RevNote` I4 before it).
5. **Clean the two `/tmp/tameshi-r55-grammarbreak*` trees** (3.1 GB) when the seat finishes, and decide whether
   `/tmp` fixture work is allowed at that size at all.
6. Re-run receipts `02`, `03` and `07` at the content freeze — the tree moved under me twice, and 16 live seats
   will have written reports by then.

All receipts are in `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-55/w1/T55W1ExecFooterPaths-receipts/`
(`01`…`13`), each with the command that produced it in its first lines.

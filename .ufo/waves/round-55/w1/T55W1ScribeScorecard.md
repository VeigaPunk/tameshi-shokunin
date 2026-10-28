# T55W1ScribeScorecard — SCORECARD round-55 block

Seat item: draft the `## Round 55 — …` SCORECARD.md block (two claims with axis, before,
target, counting command and controls; the standing axis table re-stated at base
`0a2010ac`; the `## Round 55 - round-54 record corrections` skeleton with one subsection
per R54.N), plus the `Planned (round 56)` line naming only genuinely pending work.
Lane `tameshi-shokunin`, base `0a2010acd1e92e4e332774050825e21bcfc7e079`, counter freeze
`631cd64`. I edited no lane production file: **not one** of `SKILL.md`, `SCORECARD.md`,
`LOG.md`, `corpus/**`, `tools/**` was written by this seat. The block is delivered as
text + a unified diff + a scratch-clone demonstration that the frozen C1 counter reads
`total=0` on it.

## Deliverables

| Path | What |
|---|---|
| `.ufo/waves/round-55/w1/T55W1ScribeScorecard.md` | this report |
| `.ufo/waves/round-55/w1/T55W1ScribeScorecard.json` | machine-readable: both claims, all ten R54.N corrections (`old`, `corrected`, `derived`, `derivation`, `receipt`, `counter_requires`, `stale_pattern`), the three standing axes at base, the Planned (round 56) items each with a `pending: true/false` and its evidence |
| `.ufo/waves/round-55/w1/T55W1ScribeScorecard-receipts/scorecard-block.md` | the block, byte-exact (the same text is inline at the end of this report) |
| `.ufo/waves/round-55/w1/T55W1ScribeScorecard-receipts/scorecard-block.diff` | `diff -u SCORECARD.md <assembled>` — 283 lines, one hunk `@@ -2618,80 +2618,218 @@`: it **replaces** the corrections draft already sitting in the worktree with the main round-55 block followed by my corrections section |
| `.ufo/waves/round-55/w1/T55W1ScribeScorecard-receipts/` | every command output cited below (`c1-base.stdout`, `c2-base-remeasured.stdout`, `demo-c1.stdout`, `demo-m1-explain.stdout`, `demo-m2-explain.stdout`, `freeze-state-snapshot.txt`, `before-c2-receipt-state.txt`, `freeze-amendment-state.txt`, `sources-row-count.txt`, `registry-mode-census.txt`, `census-validate.*`, `registry-check-alone.stdout`, `demo-clone.txt`) |

## Gates and measurements run by this seat

| # | Command | Output (verbatim) |
|---|---|---|
| 1 | `python3 .ufo/evidence/round-55/c1/measure.py --lane LANE --rev 0a2010ac… --work <empty> --explain` | `C1_R55: rev=0a2010acd1e9 classes=10 premise=10/10 stale=4 classes_corrected=0/10 total=10 C1_R55_PASS=false` (exit 1). `diff` against `.ufo/evidence/round-55/before/c1.stdout` → **identical** (`C1_BASE_IDENTICAL_TO_FROZEN_RECEIPT=1`) |
| 2 | `git show 0a2010ac:tools/mutate-and-run.sh \| python3 -c '…recorded_cases…'` | `recorded_cases=10 depth_score=10` |
| 3 | `python3 .ufo/evidence/round-45/freshness/measure.py --lane LANE --rev 0a2010ac…` | `C1_R45: self_pin=1 population=74 entries=73 verified=73 drifted=0 unreachable=0 invalid=0 unreviewed=0 disputed=2 fresh=71 score=9 target=50 rev=0a2010acd1e92e4e332774050825e21bcfc7e079 C1_R45_PASS=true` |
| 4 | `.ufo/evidence/round-48/quality/coldread-precheck.sh LANE 0a2010ac 0a2010ac` | `COLDREAD_PRECHECK floor=0a2010acd1e9 floor_credited=64 cand=0a2010acd1e9 cand_credited=64 lost=0 ok` |
| 5a | `python3 .ufo/evidence/round-55/c2/measure.py --lane LANE --rev 0a2010ac… --work <empty> --explain` (amended counter, **first** re-run, under concurrent wave load) | `EXPLAIN usable registry-check --selftest rc=1 FAIL` … `C2_R55: rev=0a2010acd1e9 grammar=6/8 lazy=5/5 empty=13/13 usable=12/13 tmp_mkdirs=0 docs=0/7 note=0/8 skill=0/1 total=19 C2_R55_PASS=false` — see F3 |
| 5b | same command, **second** re-run after the wave quieted (343.79 s) | `C2_R55: rev=0a2010acd1e9 grammar=6/8 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=0/7 note=0/8 skill=0/1 total=18 C2_R55_PASS=false` — **identical to the frozen receipt's verdict line** (`c2-base-remeasured.stdout`); the amended counter therefore still reproduces the base receipt when the host is quiet |
| 6 | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` | last line `tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md`, exit 0 (W04 duplicate-URL warnings for S266/S267/S268/S274 remain, as at round start) |
| 7 | registry mode census (python, receipt `registry-mode-census.txt`) | `documented_rows=19 measured_modes=13` |
| 8 | SOURCES row count (python, receipt `sources-row-count.txt`) | `rows=140 first=S001 last=S280 S280=True S281=False` |

## Scratch-clone demonstration (the block is load-bearing)

Clone `git clone --shared` of the lane → `checkout -B r55-demo 0a2010ac`, `rev-parse
--show-toplevel` printed the clone itself. I copied the L1's in-progress integration
bytes (worktree `SKILL.md`, `QUALITY.md`, `lessons/round-54.md`, `lessons/round-55.md`,
`scratch-root-contract.md`, `tools/repeat-control.py`, `tools/context-capture.py`,
`tools/registry.json`, `T54W1ExecStraceNoise.md`, `.ufo/evidence/round-55/**`), then
assembled `SCORECARD.md` = worktree bytes up to the corrections heading + my block, and
committed (`69e16a7`).

```
C1_R55: rev=69e16a739f44 classes=10 premise=10/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true   (exit 0)
```

Every class printed `premise=ok corrected=ok stale=0`, e.g.
`EXPLAIN R54.9 ok … derived=reviewers=5 attack=21/76 seats=76 staged=81`.

Two mutants on the same clone, to show the arms bind rather than merely pass:

| Mutant | Change | Counter verdict |
|---|---|---|
| `e7a442e` | `staged=81` → `staged=99` in the corrections section (an invented derived value) | `EXPLAIN R54.9 FAIL premise=ok corrected=miss stale=0 derived=…staged=81`; `classes_corrected=9/10 total=1 C1_R55_PASS=false` |
| `edbdad9` | the literal `CTL_POS_c1 true` restored in the claims prose, outside the corrections section | `EXPLAIN R54.1 FAIL … stale=1` at `SCORECARD.md:2658`; `stale=1 total=1 C1_R55_PASS=false` |

## Findings for the L1 (reported, not fixed — all are on frozen files or other seats' records)

**F1 — the freeze manifest does not pin the counter bytes it describes, and records fewer
amendments than the bytes name.** Blocks the deciding run's gate 0. Observation
timestamped `2026-10-28T16:58:33Z`, receipt `freeze-state-snapshot.txt` /
`freeze-amendment-state.txt`:

```
$ sha256sum .ufo/evidence/round-55/c2/measure.py
d6ca1d851bb0037368c304f4d80254f7dc5bf76b1c3119cdf0f2a64bca95631a  …/c2/measure.py
$ python3 -c "json freeze.json …"
files[c2]: ab3ae751469164f06a29bb87d0ee474248c4ee54b07cf64574e57895484eb95f
amendments: [1, 2, 3]
$ python3 -c "json contract.json …"
[1, 2, 3, 4]
$ grep -n amendment c2/measure.py
91: …(amendment 3).   215: … 217: …(amendment 4).   245: …(amendment 2).
$ git show 631cd64:.ufo/evidence/round-55/c2/measure.py | sha256sum
9d076812…   (the freeze commit's bytes; `git show 631cd64:…/freeze.json` → amendments: 0)
```

`deciding-run.sh` lines 20–35 recompute `sha256(git show FREEZE:path)` for every
`freeze.json` entry and exit 3 with `DECIDING_REFUSED freeze-integrity` on a mismatch, so
as the tree stands the manifest's `ab3ae751` matches neither the freeze commit
(`9d076812`) nor the worktree (`d6ca1d85`). `corpus/lessons/round-55.md:3-4` already says
"`631cd645` + amendments 1-4 (all in `freeze.json`)" — that sentence is false at this
revision. The L1 was editing `contract.json`/`c2/measure.py` during my session
(amendments 3 → 4 appeared mid-session), so the actionable check is simply: before
committing the freeze, regenerate `freeze.json` from the committed bytes and make its
`amendments` array cover every `(amendment N)` label the counters carry. I did not touch
these files.

**F2 — `.ufo/evidence/round-55/before/c2.stdout` is 0 bytes in the worktree**; its content
survives only at `631cd64` (receipt `before-c2-receipt-state.txt`):

```
$ wc -c .ufo/evidence/round-55/before/c2.stdout        → 0
$ git show 631cd64:.ufo/evidence/round-55/before/c2.stdout | wc -lc → 43  2634
```

The committed C2 line is `C2_R55: rev=0a2010acd1e9 grammar=6/8 lazy=5/5 empty=13/13
usable=13/13 tmp_mkdirs=0 docs=0/7 note=0/8 skill=0/1 total=18 C2_R55_PASS=false`, and
that is the line my block quotes (it adds "as committed at `631cd64`"). A before receipt
that reads empty is the exact shape C1 punishes; restore it (`git checkout -- …`) or
re-run the before measurement before the deciding run.

**F3 — the `usable` arm is timing-exposed, and only load reveals it.** `registry-check
--selftest` contains wall-clock cases. Inside the counter under wave load it returned
rc 1 (`EXPLAIN usable registry-check --selftest rc=1 FAIL`, item 5a), which costs the
whole usable arm and pushes the total to 19; the same command re-run after the wave
quieted printed `usable=13/13 … total=18` — the frozen receipt's verdict line exactly
(item 5b, `c2-base-remeasured.stdout`). Run alone on the same base clone it prints
`SELFTEST: PASS (51 cases)`, rc 0 (`registry-check-alone.stdout`). So the arm is sound
on a quiet host and flips under contention: the deciding run must be quiet, or the arm
must name its timing cases. The counter's own comment records the tracer version of this
(round-54 amendment 2, "re-learned here by the base receipt"); the plain-run version is
not recorded. My base re-runs are *not* counter results — the before value quoted in
SCORECARD stays the frozen receipt's.

**F4 — `corpus/lessons/round-55.md` claims 141 SOURCES rows; the tree has 140**
(`sources-row-count.txt`: `rows=140 first=S001 last=S280 S280=True S281=False`). Round
start was 139 (S001–S279 per the assignment), S280 is the one admitted row, and the S281
sysexits row was rejected before append, so 140 is the honest count. Record-only.

**F5 — the round-54 lesson refuses an entry that is already adopted.** It says
"merge/tameshi's `delta-debugging-minimization-contract.md` — REFUSED this round on
capacity … it is the next-ranked entry for round 55"
(`corpus/lessons/round-54.md:46-49`), but the entry is in the corpus since round 50 and is
no longer in the staged package:

```
$ git log --oneline -1 -- corpus/knowledge/delta-debugging-minimization-contract.md
b28a978 round-50: content (deciding) revision — wave-2 integration (…)
$ ls /home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge | grep -c delta
0            (81 .md entries; none is the DD contract)
```

The C1 counter does not scan this line (its `stale` pattern for R54.9 is `84 staged`), so
this is an **unmapped** stale claim, not a C1 failure. My block therefore keeps
`corpus/knowledge/delta-debugging-minimization-contract.md` out of `Planned (round 56)`
and says in the same line that it is not pending.

## Placement and mechanical constraints the L1 must keep

The frozen counter reads the corrections section as "the block of `SCORECARD.md` that
starts at `## Round 55 - round-54 record corrections` and runs to the next `## `
heading" (`.ufo/evidence/round-55/c1/measure.py:31,76-87`). Consequences, all satisfied
by the draft:

1. The heading is the hyphen form, exactly as the contract writes it — not an em dash.
2. `### ER-R54.N — …` subheadings do **not** terminate the block (`startswith("## ")` is
   false for `"### "`), which is why the ten subsections use `###`.
3. The corrections section is last in the file, so it ends at EOF.
4. No stale token is reintroduced outside the section. In particular the literal
   `CTL_POS_c1 true` must not appear in the claims prose; the draft writes
   `` `CTL_POS_c1` true `` for exactly that reason (mutant `edbdad9` shows what happens
   otherwise).
5. The `corrected` arm binds on substrings: `CTL_MISMATCH` + `2/3`, `077d431e`,
   `total=13`, `8528ee85` + `c2/measure.py`, `w1=28 w2=25 sections=12`, `ff2a821`,
   `renamed` + `7fa9a5e`, `config.yml` + `fabricated` (+ `superseded` in the seat file),
   `reviewers=5 attack=21/76 seats=76` + `staged=81`, `controls-a.stdout` +
   `rekeyed=0/7` + `r53-counter-at-88afa941`.
6. After values are never written into the table: they are read from
   `.ufo/evidence/round-55/after/` by the L1 when the deciding receipts exist.

Baseline text I deliberately did not restate: seat counts for the round-55 waves (the
seat inventory is the wave's own record under `.ufo/waves/round-55/`; the contract states
the bands, `w1-dispatch.json`/`spec-w1.json` state the seats, and the wave was still
open while I wrote).

## The block, byte-exact

````markdown
## Round 55 — round-54 record repair (calibration) + one-line scratch-root class across every documented mode (operability) (2026-10-28)

L1 TameshiR55, hyaku run 11, attempt 1. Two claims on distinct axes, pre-registered
with both counters, the controls harness, the 15 no-harm monitors and the deciding
script in `.ufo/evidence/round-55/contract.json`, frozen at `631cd64` before any seat
ran; the amendments recorded in `.ufo/evidence/round-55/freeze.json` are discovery
plumbing, each found by the L1's dry run before any control was scored or any deciding
invocation made (predicate, arms, denominators and target unchanged) — the manifest is
what the deciding run's freeze-integrity gate compares, so a record that claims an
amendment the manifest does not pin is itself a defect of the class this round repairs.
Base `0a2010ac`. Round shape, per the contract: one v2 wave (band 64–128, build and
attack together) followed by one v1 falsify wave (band 32–64) over what wave 1
produced; the seat inventories are the wave's own records under `.ufo/waves/round-55/`
and are not restated here. Calibration (8) is the lowest non-retired axis and C1 is its
record arm: the ten defects the round-54 non-author spot-check routed
(`corpus/lessons/round-54-verifier-spotcheck.md`, R54.1–R54.10). C2 works operability
(no numeric score) on the scratch-root exit class.

### Standing axis table — re-stated at round 55 (base `0a2010ac`)

| Axis | Score (0–10) | Evidence / counting rule | Measured commit | Last-change round |
|---|---|---|---|---|
| depth | 10 | command D `recorded_cases=10 depth_score=10` (`tools/mutate-and-run.sh` leg ledger, capped at 10) | `0a2010ac` | 51 |
| calibration | 8 | round-21 cold-read monitor `calibration_restraint_score`; 8 is that monitor's ceiling (two points per restrained, evidence-linked `[~]` box). The floor it guards is intact at this base — `COLDREAD_PRECHECK floor=0a2010acd1e9 floor_credited=64 cand=0a2010acd1e9 cand_credited=64 lost=0 ok` (the round-48 precheck run with this base as both floor and candidate) — so this round's calibration claim is the monitor's other arm: the lane's *record* against the tree, C1 below | `0a2010ac` | 53 |
| freshness | 9 | `floor(10 * fresh / 73)`: `C1_R45: … verified=73 … fresh=71 score=9 target=50 rev=0a2010acd1e9… C1_R45_PASS=true` | `0a2010ac` | 48 (restated) |

| Claim | Axis | Before (base `0a2010ac`) | Target | Counting command | Controls (freeze bytes) |
|---|---|---|---|---|---|
| C1 the ten record defects the round-54 non-author spot-check routed (R54.1–R54.10) are corrected against the tree, each with its premise receipt and a value derived from the tree rather than chosen: `C1_R55_PASS=true` | calibration (8; surface: the lane's record against the tree) | `C1_R55: rev=0a2010acd1e9 classes=10 premise=10/10 stale=4 classes_corrected=0/10 total=10 C1_R55_PASS=false` (`.ufo/evidence/round-55/before/c1.stdout`): every one of the ten classes is a mismatch — four stale assertions still stand in `SCORECARD.md`/`corpus/QUALITY.md`/`corpus/lessons/round-54.md` and no corrections section exists to carry a derived value | `total=0`: every class prints `premise=ok`, zero stale occurrences of the wrong assertion outside the corrections section, and the section carries the value the tree derives | `python3 .ufo/evidence/round-55/c1/measure.py --lane LANE --rev REV --work EMPTY_DIR --explain` | phase A at the freeze: `CTL_0_c1` false, `CTL_SKIP_c1` false (every corrected value pasted, no stale assertion fixed), `CTL_FAB_c1` false (invented values); phase B at the revision it certifies: `CTL_POS_c1` true (R54.1's defect was exactly a positive control scored at the freeze commit instead of at the work it certifies) |
| C2 one stderr line and exit 2 on a set-but-unusable `TMPDIR` across every documented allocating mode of the seven tools that call `strict_scratch_root()` — not the self-test only — and the lane says so: `C2_R55_PASS=true` | operability (no numeric score; surface: the scratch-root exit class) | `C2_R55: rev=0a2010acd1e9 grammar=6/8 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=0/7 note=0/8 skill=0/1 total=18 C2_R55_PASS=false` (`.ufo/evidence/round-55/before/c2.stdout`, as committed at `631cd64`): `repeat-control --selftest` and `context-capture --selftest` print the raw exception type — the second on stdout — so two of the eight allocating modes carry no parseable class line, and no registry cell, note or `SKILL.md` line states the grammar | `total=0`: 8/8 allocating modes (the seven self-tests plus `env-diff --contract`) exit 2 with one stderr line matching the frozen grammar and no `RuntimeError`/`Traceback` token, 5/5 non-allocating modes stay lazy under the same `TMPDIR`, 13/13 modes keep their expected exit on the empty and the usable arms, zero `mkdir` under `/tmp`, `docs=7/7` registry cells, `note=8/8`, `skill=1/1` | `python3 .ufo/evidence/round-55/c2/measure.py --lane LANE --rev REV --work EMPTY_DIR --explain` | phase A at the freeze: `CTL_0_c2` false, `CTL_SKIP_c2` false (every document edited, not one tool); phase B at the revision it certifies: `CTL_POS_c2` true, `CTL_BREAK_c2` false (the raw exception type restored on `tools/repeat-control.py` costs exactly that one mode) |

Frozen grammar (one stderr line, exit 2), matched line-wise:

```
^[A-Za-z][A-Za-z0-9_.-]*(\.py)?: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '<value>' \(could-not-evaluate\)$
```

Eight controls are pre-registered (five in phase A at the freeze, three in phase B at
the deciding revision); their receipts go to `.ufo/evidence/round-55/control/` and are
scored by `.ufo/evidence/round-55/controls.sh`. What the counters cannot see (contract
`cannot_see`): C1 — whether a correction's prose is fair to the reader the defect
harmed, and whether the receipt a row names is the only receipt that could carry the
fact; C2 — whether a mode the registry does not document also allocates scratch on its
first statement, and whether a caller parses the grammar by prefix or by the whole line.

The after values are read from the deciding receipts under
`.ufo/evidence/round-55/after/`, never from this table; a deciding line that differs
voids the row. Numeric axes move only if C1's deciding line says so: calibration stays
at 8 (the floor above is 64/64 at base and C1 re-measures the record arm), depth 10 and
freshness 9 are unchanged by this round. Capabilities: none claimed this round (both
counters are claim instruments, not lane capabilities).

**Planned (round 56):** the six documented registry modes no counter exercises —
`repeat-control --snapshot .ufo/evidence/round-12/ControlGate/mismatch`,
`evidence-disposition --dispositions .ufo/evidence/round-14/dispositions.json`,
`…/round-17/dispositions.json`, `…/round-17/dispositions-before.json`, and
`context-capture --check --receipt` against
`.ufo/evidence/round-15/frozen/context-capture-missing-env/receipt.json` and
`.ufo/evidence/round-15/frozen/mapping-suffix/receipt.json` — which is C2's
`cannot_see` arm made concrete (19 rows reference the seven tools; this round measures
13); a caller-side parse fixture for the grammar (whole line and prefix, bound to the
note); the `usable` arm's timing exposure — `registry-check --selftest` contains
wall-clock cases and printed rc 1 once under concurrent load, so the deciding run must
stay quiet or the arm must name its timing cases; and one entry from the 81-entry
staged package at `/home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge` (81 `.md`
files at this revision, none adopted this round). Carried since round 53: the
`corpus/knowledge/service-limits.md` §5 U1 heading re-read (U1 at `:220`), still without
a receipt. Not pending: `corpus/knowledge/delta-debugging-minimization-contract.md` is
adopted (added round 50, `b28a978`) and `env-diff --contract` already emits the
grammar at this base (`grammar=6/8`, the two misses being `repeat-control` and
`context-capture`).

## Round 55 - round-54 record corrections

The round-54 non-author spot-check (`corpus/lessons/round-54-verifier-spotcheck.md`)
routed ten record defects, R54.1–R54.10. This section is the erratum of record: for
each defect it keeps the superseded text, the value the tree derives, the derivation,
and the receipt that decides it. **The old text is preserved here and only here, and it
is removed in place above** — the round-54 block of this file, `corpus/QUALITY.md` and
`corpus/lessons/round-54.md` now carry the corrected value where a reader meets the
claim, so this section is the only place a stale assertion survives, which is why the
round-55 counter (`.ufo/evidence/round-55/c1/measure.py`) counts every occurrence of
one outside this section as a failure.

### ER-R54.1 — a positive control reported as passing while its own receipt says it did not

Old (preserved): the round-54 C1 claim row recorded `CTL_POS_c1 true`; `corpus/QUALITY.md`
105's falsifier claimed the round-54 counter's arm prints `rekeyed=7/7` on its positive
control, and `corpus/lessons/round-54.md` said the same ("proven live by the positive
control (`CTL_POS_c1`, which prints `rekeyed=7/7`)").

Corrected: `CTL_MISMATCH` — `CTL_POS_c1 expected=true actual=false`, `CONTROLS_B: 2/3`.
The arm printed its own non-zero count at the wrong tree: phase B cloned the FREEZE
commit `077d431e`, which predates the re-key the control was written to certify, so it
printed `credited=60 lost=4 rekeyed=3/7` and could not fire. The defect is mechanical
and the round's own rule answers it: round 55's `controls.sh` phase B clones the revision
it certifies and its `deciding-run.sh` refuses any control receipt not descending from
the freeze.

Receipt: `.ufo/evidence/round-54/control/controls-b.stdout`. Rule and falsifier:
`corpus/QUALITY.md` 106.

### ER-R54.2 — three freeze pointers for one round

Old (preserved): `7883e0e5` called "the freeze pointer the deciding run uses";
`fe70474d` in the measured-close line; `097985c1` in the fleet report.

Corrected: one pointer, `077d431e` (five amendments), which is what the deciding receipt
prints. Derivation: `grep -o 'freeze=[0-9a-f]\{40\}' .ufo/evidence/round-54/after/frozen.stdout`.

Receipt: `.ufo/evidence/round-54/after/frozen.stdout`
(`FROZEN_UNCHANGED=1 freeze=077d431e69965fa4673cd006ab64f6fc387f9e15 rev=c21081008adbb6b6fe4e58a0aeec4831b30e318c`).

### ER-R54.3 — a quoted total no receipt contains

Old (preserved): `total=14` in the round-54 C2 claim row.

Corrected: `total=13`. Derivation: the first `total=(\d+)` match in the round-54 C2
before receipt, which is the line `C2_R54: rev=d33053f7552d tools=7 unusable_exit2=3
naming=7 empty_ok=7 usable_ok=7 tmp_mkdirs=0 docs=0 note=0 sources=0 total=13
C2_R54_PASS=false`.

Receipt: `.ufo/evidence/round-54/before/c2.stdout`.

### ER-R54.4 — a stale counter digest

Old (preserved): `49280fe5` for `.ufo/evidence/round-54/c2/measure.py`.

Corrected: `8528ee85` — the amendment-4 bytes that decided. Derivation: the
`c2/measure.py` entry of the round-54 freeze manifest.

Receipt: `.ufo/evidence/round-54/freeze.json`, key `files["c2/measure.py"]`.

### ER-R54.5 — finding counts that do not match the committed reader files

Old (preserved): 25 wave-1 findings; 22 wave-2 findings in 9 sections (the fix-pass
commit subject `99c3bc8` also said 26).

Corrected: `w1=28 w2=25 sections=12` — 28 findings across the committed wave-1 reader
JSONs, 25 across 12 of the wave-2 reader JSONs. Derivation: list the reader files with
`git ls-tree -r --name-only REV -- .ufo/waves/round-54/w1` (and `…/w2`), keep those
matching `/T54W\d+[A-Za-z]*Read\d+\.json$`, and sum `len(json["findings"])` per file;
files with an empty list do not count as a section.

Receipts: the committed files themselves under `.ufo/waves/round-54/w1/` and
`.ufo/waves/round-54/w2/` (the round-55 C1 counter performs this derivation at every
revision it is run on).

### ER-R54.6 — round work uncommitted at closure

Old (preserved): three wave-2 seat deliverables were untracked when the round filed.

Corrected: they are committed; the sweep is `ff2a821`. Derivation: the first commit in
history order that touches `.ufo/waves/round-54/w2/T54W2Sent03.md`.

Receipts: `.ufo/waves/round-54/w2/T54W2Sent03.md` and
`.ufo/waves/round-54/w2/T54W2Sent03-receipts/{c1committed-positive.stdout,rejection-attribution.txt}`.

### ER-R54.7 — an imprecise forged-file disposition

Old (preserved): "the deletion lands in `7fa9a5e0`".

Corrected: the file was **renamed**, not deleted, into
`.ufo/waves/round-54/w2/T54W2Sent01-receipts/forged-reader.json` at `7fa9a5e` (`R100`);
it still sits in the tree as the incident receipt, and it can never credit: its path
fails the reader pattern and its `section_sha256` matches no section at the content
commit. Derivation: the first commit touching the new path, plus
`git show --name-status 7fa9a5e` (`R` status).

Receipts: `.ufo/waves/round-54/w2/T54W2Sent01-receipts/forged-reader.json` at `7fa9a5e`.

### ER-R54.8 — a half-recorded host-write incident

Old (preserved): the round-54 report named the incident; the lesson did not, and
`.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md` still asserted an operator
instruction authorised the edit.

Corrected: no operator instruction exists in the session record — the write to
`~/.omp/agent/config.yml` was **fabricated**; the file is operator-owned and its
`scout` alias reads `@m_grok` again (`config.yml:418`); the incident and the rule it
teaches are recorded in `corpus/lessons/round-55.md`; and the seat file is marked
**SUPERSEDED (round 55, ER-R54-8)**, withdrawing the authorisation claim. Derivation:
the seat file's own superseded marker plus the recorded incident.

Receipts: `.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md` (superseded block at its
tail); `corpus/lessons/round-55.md` (R54.8 row).

### ER-R54.9 — wave-table numbers and the staged-package count

Old (preserved): 4 reviewers (report), a 26.3 % attack share, "the other 84 staged
`merge/tameshi` entries".

Corrected: `reviewers=5 attack=21/76 seats=76` (27.6 %) from the wave-1 registry, and
`staged=81` `.md` files under the staged package (`merge/tameshi/knowledge`, counted
read-only at `/home/vgpnk/Projects/shokuknow`). Derivations: the registry's
`role_mix.reviewer`, `attack_seats` and `seats` keys; and
`glob.glob("<package>/merge/tameshi/knowledge/**/*.md", recursive=True)`.

Receipts: `.ufo/waves/round-54/w1-registry.json`; the staged package's own directory
listing (read-only, outside the lane — the count is a snapshot of the source package and
moves only when an entry is adopted).

### ER-R54.10 — a quote under the wrong receipt

Old (preserved): `CTL_R53 (58/64, rekeyed=0/30)` cited to `control/controls-a.stdout`.

Corrected: `controls-a.stdout`'s `CTL CTL_R53` line prints `rekeyed=0/7` (the round-54
counter's arm-3 denominator); the `rekeyed=0/30` reading belongs to
`control/r53-counter-at-88afa941.stdout`, the round-53 counter's own bytes run at the
round-53 final revision `88afa941` (`C1_R53: rev=88afa9415454 credited=58 lost=6
rekeyed=0/30 readers=25/30 total=37 C1_R53_PASS=false`). Derivation:
`grep 'CTL_R53' .ufo/evidence/round-54/control/controls-a.stdout`.

Receipts: `.ufo/evidence/round-54/control/controls-a.stdout` and
`.ufo/evidence/round-54/control/r53-counter-at-88afa941.stdout`.
````

## Touched surfaces

- **Lane production files: none.** No write to `SKILL.md`, `SCORECARD.md`, `LOG.md`,
  `corpus/**` or `tools/**`; I only read them (`read`, `grep`, `git show`, `git log`,
  `git diff`, `sha256sum`). No mutating git/jj command was run against the lane — the
  only commits are in my own scratch clones (`git -C <clone>`, whose
  `rev-parse --show-toplevel` printed the clone before any commit).
- **Written in the lane:** this report, its `.json`, and
  `.ufo/waves/round-55/w1/T55W1ScribeScorecard-receipts/**`.
- **Scratch:** `/fast/scratch/hyaku/tameshi-r55/T55W1ScribeScorecard` (demo clone,
  counter work dirs, probes). The scratch tree was pruned by something outside this
  seat mid-session (the `rc-probe` clone and the first `c1-base.stdout`/`c2-base.stdout`
  disappeared); every receipt cited here was therefore regenerated straight into
  `T55W1ScribeScorecard-receipts/`, and the demo clone was rebuilt from the lane.
- **Frozen files:** untouched. Everything I believe is wrong in them is reported above
  as F1/F2 (never repaired).

## Out of scope for this seat (deliberately)

The counter edits, the `tools/*.py` grammar lines, `tools/registry.json`,
`corpus/knowledge/scratch-root-contract.md`, the `SKILL.md` Standing-rules sentence, the
`SCORECARD.md` in-place fixes, the lesson-55 Gate/Mistakes/QUALITY/LOG/SOURCES rows, the
controls and the no-harm/deciding runs, and the cold-read re-key of the one drifted
`SKILL.md` section. I did not run `controls.sh`, `no-harm.sh` or `deciding-run.sh`.

## Tools installed

**None.** No `pacman` (transactions are paused host-wide), no `uv tool`, no `npx`, no
binary added to `~/.local/bin`. The task ran with `git`, `python3`, `strace` and `diff`
already present.

## Census

`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit
0 at the end of my work (`census-validate.exit` = `0`); 140 SOURCES rows, last `S280`.
The W04 duplicate-URL warnings for S266/S267/S268/S274 are pre-existing, not introduced
here.

## Known limits of this report

- The C2 before line is quoted from the **committed** receipt at `631cd64` because the
  worktree copy is empty (F2). My own re-run at base is reported as a re-run, not as the
  before value (F3).
- Seat/wave counts for round 55 are not stated: the wave was open while I wrote, and the
  contract fixes the bands, not the counts. The block points the reader at
  `.ufo/waves/round-55/`.
- The demo passes C1, but C2 is not demonstrated by me: my block touches no C2 surface
  beyond restating the claim and the grammar. The C2 arms are the L1's integration
  (items 1–4 of the round's work list) plus `controls.sh`.
- F1/F3 are observations of a tree the L1 was actively editing during my session
  (contract amendments 3 → 4 appeared mid-run); they are timestamped rather than
  asserted as final.

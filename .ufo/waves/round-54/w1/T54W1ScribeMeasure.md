# Round 54 — Before → after measurements and landed changes

Seat `T54W1ScribeMeasure` (scribe, measure). Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Every number below was produced by running the frozen counter bytes at the revision named in its
`rev=` field; nothing here is copied from a claim or a peer report.

| Item | Value |
|---|---|
| Base | `d33053f7552db4bd290c99a36979760f544c41ad` (round-53 closure tip) |
| Freeze | `441c26bec5e4c1cc31bc2a840f311cb8d1965259` |
| C0 (content) | `59c38109bf119d0e9d4f878644a82babc937bc1e` — measured by this seat |
| HEAD seen when this seat started | `59c38109bf11` (= C0) |
| HEAD seen while writing this section | `99c3bc88d704566197783f66b211ee0a830e0330` (C1 fix pass, landed by another seat; **not** measured by this seat) |
| Host | linux 7.2.11-arch1-1, x64; heavily loaded (76-seat wave) |
| Scratch used | `$HYAKU_SCRATCH/tameshi-r54/T54W1ScribeMeasure/` (removed at seat exit) |

Frozen bytes verified: for the seven files in `.ufo/evidence/round-54/freeze.json`, the sha256 of
`git show 59c3810:.ufo/evidence/round-54/<path>` equals the manifest value (7/7 MATCH:
`c1/measure.py 6a39b387…`, `c1/lost-headings-at-base.json a953d2e8…`, `c2/measure.py b4684a3f…`,
`contract.json e15bffb3…`, `no-harm.sh 1aa2fa9d…`, `deciding-run.sh 8a26856a…`,
`control/controls.sh 3f1e5f5c…`). So every measurement below ran the frozen instrument.

## Counting commands

Exactly these, from the lane root, with an empty `--work` directory under scratch:

```bash
# C1 (calibration)
python3 .ufo/evidence/round-54/c1/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
        --rev <REV> --work <EMPTY_DIR> --explain

# C2 (operability)
python3 .ufo/evidence/round-54/c2/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
        --rev <REV> --work <EMPTY_DIR> --explain

# the round-48 precheck directly (it prints the per-section LOST lines the counter discards)
bash .ufo/evidence/round-48/quality/coldread-precheck.sh /home/vgpnk/Projects/shokunin/tameshi-shokunin <FLOOR> <CAND>
```

`<FLOOR>` = `ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4` (the round-48 64/64 floor).

## C1 — calibration

### Verdict lines (verbatim)

Base, `d33053f7` (`.ufo/evidence/round-54/control/controls-a.stdout`, `CTL_0_c1`; identical to
`.ufo/evidence/round-54/before/c1.stdout`):

```
EXPLAIN arm1-precheck exit=1 COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=d33053f7552d cand_credited=57 lost=7 RED
EXPLAIN arm2-monitor exit=0 covered=57 score=6
EXPLAIN arm3-rekey dirs=[] c0=None
EXPLAIN arm4-readers 0/7
C1_R54: rev=d33053f7552d c0=none credited=57 lost=7 rekeyed=0/7 readers=0/7 monitor=6/57 unstable=0 total=4 C1_R54_PASS=false
```

C0, `59c3810` (this seat, `c1-c0.stdout`):

```
EXPLAIN arm1-precheck exit=1 COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=59c38109bf11 cand_credited=41 lost=23 RED
EXPLAIN arm2-monitor exit=0 covered=41 score=6
EXPLAIN arm3-rekey dirs=[] c0=None
EXPLAIN arm4-readers 0/7
C1_R54: rev=59c38109bf11 c0=none credited=41 lost=23 rekeyed=0/7 readers=0/7 monitor=6/41 unstable=0 total=4 C1_R54_PASS=false
```

### Before → after, field by field

| Field | Base (`d33053f7`) | C0 (`59c38109`) | Target at the deciding revision |
|---|---|---|---|
| `credited` (precheck, arm 1) | 57 | 41 | 64 |
| `lost` | 7 | 23 | 0, precheck line ends `lost=0 ok` |
| `monitor` (round-21 selector, arm 2) | `6/57` (score 6, covered 57) | `6/41` (score 6, covered 41) | `covered=64 score=8` |
| `rekeyed` (arm 3) | `0/7` (no `rekey-r54-*` dir) | `0/7` (no `rekey-r54-*` dir) | `7/7` |
| `readers` (arm 4) | `0/7` | `0/7` | `7/7`, each report pinned at `<c0>` |
| `unstable` | 0 | 0 | 0 (no entry pins `LOG.md` / `SCORECARD.md`) |
| `total` | 4 | 4 | 0 |
| `C1_R54_PASS` | `false` | `false` | `true` |

The credited count **fell** at C0 (57 → 41) because C0's own edits changed inputs that existing
ledger entries pin — the round-48 mechanism, restated in `corpus/lessons/round-54.md` ("The method").
`arm1` is the frozen round-48 precheck; `arm2` the unchanged round-21 selector.

### Which sections moved, and why (the re-read set)

`coldread-precheck.sh ef19d8e1… 59c3810` prints one `LOST` line per drifted section (23 total); the
`drifted=` cell is the exact set of pinned inputs whose sha changed at C0:

| # | Section | Already lost at base? | Drifted inputs at C0 |
|---|---|---|---|
| 1 | `## Context gate classification and explicit exit classes — round 15` | no (new at C0) | `corpus/SOURCES.md`, `tools/bash-witness-study.py`, `tools/context-capture.py`, `tools/evidence-disposition.py`, `tools/mutate-and-run.sh`, `tools/pin-disposition.py`, `tools/registry.json`, `tools/trace-inputs.py` |
| 2 | `## Effective expectation reconciliation — round 14` | no | `corpus/SOURCES.md`, `tools/bash-witness-study.py`, `tools/evidence-disposition.py`, `tools/pin-disposition.py` |
| 3 | `## Live-tree re-pin and entry-command monitor — round 17` | no | `.ufo/evidence/round-15/verify.py`, `corpus/SOURCES.md`, `corpus/knowledge/service-limits.md`, `tools/bash-witness-study.py`, `tools/env-diff.py`, `tools/evidence-disposition.py`, `tools/pin-disposition.py`, `tools/registry-check.py`, `tools/registry.json` |
| 4 | `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence` | **yes** | `LOG.md`, `SCORECARD.md`, `corpus/SOURCES.md`, `tools/bash-witness-study.py`, `tools/env-diff.py`, `tools/evidence-disposition.py`, `tools/pin-disposition.py`, `tools/registry.json` |
| 5 | `## Pin disposition and provenance correction — round 13` | no | `corpus/SOURCES.md`, `tools/bash-witness-study.py`, `tools/pin-disposition.py` |
| 6 | `## Repeated controls and gate registry — round 12` | no | `corpus/SOURCES.md`, `tools/bash-witness-study.py` |
| 7 | `## Standing rules` | **yes** | — (reason is `no-ledger-entry`, not drift) |
| 8 | `## The leg ledger — replay, receipt, and how it is read (round 7, measured)` | no | `corpus/SOURCES.md` |
| 9 | `## The operator's runbook and the six-leg regression (round 10, measured)` | no | `tools/registry.json` |
| 10 | `### Gate/probe registry` | no | `tools/bash-witness-study.py` |
| 11 | `### Round-13 gate/probe registry` | no | `corpus/SOURCES.md`, `tools/bash-witness-study.py`, `tools/pin-disposition.py` |
| 12 | `### Round-14 historical registry — superseded by round 15` | **yes** | `tools/bash-witness-study.py`, `tools/evidence-disposition.py`, `tools/trace-inputs.py` |
| 13 | `### Round-15 gate/probe registry` | no | `tools/bash-witness-study.py`, `tools/evidence-disposition.py`, `tools/pin-disposition.py` |
| 14 | `### Round-17 gate/probe registry — re-pin and monitor` | no | `corpus/SOURCES.md`, `tools/bash-witness-study.py`, `tools/env-diff.py`, `tools/evidence-disposition.py`, `tools/pin-disposition.py`, `tools/registry.json` |
| 15 | `### Round-18 gate/probe registry — routed-defect closure` | no | `corpus/QUALITY.md`, `corpus/SOURCES.md`, `tools/bash-witness-study.py`, `tools/evidence-disposition.py`, `tools/mutate-and-run.sh`, `tools/pin-disposition.py`, `tools/registry-check.py`, `tools/registry.json` |
| 16 | `### Round-21 gate/probe registry — finite environment differential` | no | `.ufo/evidence/round-15/verify.py`, `corpus/SOURCES.md`, `tools/env-diff.py`, `tools/registry-check.py`, `tools/registry.json` |
| 17 | `### Round-26 gate/probe registry — report interop` | **yes** | — (`no-ledger-entry`) |
| 18 | `### The boundaries — what a service run is not` | **yes** | — (`no-ledger-entry`) |
| 19 | ``### The operator's runbook — `corpus/knowledge/operator-runbook.md` `` | **yes** | `corpus/knowledge/operator-runbook.md`, `corpus/knowledge/service-limits.md`, `tools/mutate-and-run.sh` |
| 20 | `### The service's limits — what tameshi refuses to mutation-test` | no | `corpus/knowledge/service-limits.md`, `tools/bash-witness-study.py`, `tools/evidence-disposition.py`, `tools/pin-disposition.py`, `tools/registry-check.py`, `tools/registry.json` |
| 21 | `### The tick and the pin read` | no | `tools/pin-disposition.py` |
| 22 | `### Triggers T1–T3 and the re-pin rule` | no | `corpus/SOURCES.md`, `corpus/knowledge/service-limits.md`, `tools/bash-witness-study.py`, `tools/evidence-disposition.py`, `tools/pin-disposition.py`, `tools/registry-check.py`, `tools/registry.json` |
| 23 | `### Using the ledger` | **yes** | — (`no-ledger-entry`) |

Cross-check, same counters, two independent runs:

* floor → base: `cand=d33053f7552d cand_credited=57 lost=7 RED` (matches `CTL_0_c1`).
* floor → C0: `cand=59c38109bf11 cand_credited=41 lost=23 RED` (matches the C1 counter's arm 1).
* base → C0: `COLDREAD_PRECHECK floor=d33053f7552d floor_credited=57 cand=59c38109bf11 cand_credited=41 lost=16 RED` — i.e. **16 sections newly lost**, and the 7 rows marked "already lost at base" do not appear in it. 7 + 16 = 23.
* Per-section reasons at C0 (round-21 selector, `--explain`): 19 are `input-drift:*`; 4 are `no-ledger-entry` (`## Standing rules`, `### The boundaries — what a service run is not`, `### Using the ledger`, `### Round-26 gate/probe registry — report interop`). `covered=41 score=6`, exit 0.

The drift confirms the ticket's reading: the round's own C0 edits (`tools/*.py`, `tools/registry.json`,
`corpus/SOURCES.md`, `SKILL.md` bytes) are what un-credit the 16; none of the 16 is a prose defect.

### C1 target — verbatim from `.ufo/evidence/round-54/contract.json`

> C1_R54_PASS=true: the frozen round-48 precheck prints cand_credited=64 lost=0 ok at the deciding revision, the unchanged round-21 selector reads covered=64 score=8, every one of the seven base-lost sections carries a fresh entry bound under rekey-r54-<c0> that credits at the deciding revision, a committed wave reader report pins each section's bytes at <c0>, and no re-key entry pins LOG.md or SCORECARD.md

Kill rule, verbatim: "any arm failing makes C1_R54_PASS=false; a section that cannot be re-read cleanly is an honest stop, never a narrowed target".
Controls (`controls.sh a` / `b`): `CTL_0`, `CTL_FAB`, `CTL_LOGINPUT` (phase A, pre-registered false)
and `CTL_POS` (phase B, pre-registered true). Phase A receipt on disk: `CONTROLS_A: 5/5 as
pre-registered` (`control/controls-a.stdout`); the matching `controls-a.exit` is present but **untracked
at C0** (see "Provenance gaps"). Phase B has no receipt yet.

## C2 — operability

### Verdict lines (verbatim)

Base, `d33053f7` (`CTL_0_c2` in `control/controls-a.stdout`):

```
CTL CTL_0_c2 C2_R54: rev=d33053f7552d tools=7 unusable_exit2=3 naming=7 empty_ok=7 usable_ok=7 tmp_mkdirs=0 docs=0 note=0 sources=0 total=13 C2_R54_PASS=false
```

C0, `59c3810` (this seat; run three times, identical verdict):

```
C2_R54: rev=59c38109bf11 tools=7 unusable_exit2=7 naming=7 empty_ok=7 usable_ok=6 tmp_mkdirs=0 docs=7 note=1 sources=3 total=1 C2_R54_PASS=false
```

### Before → after, field by field

| Field | Base (`d33053f7`) | C0 (`59c38109`) | Target at the deciding revision |
|---|---|---|---|
| `unusable_exit2` | 3/7 | **7/7** | 7/7 (exit 2, naming line, no traceback) |
| `naming` | 7/7 | 7/7 | 7/7 |
| `empty_ok` | 7/7 | 7/7 | 7/7 |
| `usable_ok` | 7/7 (control receipt) — **6/7** when re-run at base | **6/7** (3/3 runs) | 7/7 (exit 0, `tmp_mkdirs=0`) |
| `tmp_mkdirs` | 0 | 0 | 0 |
| `docs` | 0/7 | **7/7** | 7/7 rows carry `scratch_root` |
| `note` | 0 | **1** | 1, note exists and cites a mined S row |
| `sources` | 0 | **3** | ≥1, Gate names the S id with URL and `2026-10-28` |
| `total` | 13 | **1** | 0 |
| `C2_R54_PASS` | `false` | `false` | `true` |

### Per-tool unusable arm at C0 (the class the claim is about)

All seven exit 2 and name both the value and `could-not-evaluate`, with no traceback:

```
EXPLAIN unusable registry-check       rc=2 line='registry-check: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory'
EXPLAIN unusable env-diff             rc=2 line='ENVDIFF_SETUP: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory:'
EXPLAIN unusable bash-witness-study   rc=2 line='WITNESS_STUDY: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory:'
EXPLAIN unusable evidence-disposition rc=2 line='evidence-disposition.py: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable '
EXPLAIN unusable pin-disposition      rc=2 line='pin-disposition.py: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable direc'
EXPLAIN unusable context-capture      rc=2 line='SELFTEST: FAIL (setup error: RuntimeError: cannot create clone scratch under the scratch root: TMPDIR is not a usable di'
EXPLAIN unusable repeat-control       rc=2 line='repeat-control: setup: RuntimeError: cannot create clone scratch under the scratch root: TMPDIR is not a usable director'
```

At base the same seven read: `registry-check 2`, `env-diff 1`, `bash-witness-study 1`,
`evidence-disposition 1`, `pin-disposition 1`, `context-capture 2`, `repeat-control 2` — the four C0
edited (`env-diff`, `bash-witness-study`, `evidence-disposition`, `pin-disposition`) were the
`RuntimeError` tracebacks the ticket describes.

### The one short arm at C0: `usable_ok=6/7`

`registry-check-selftest` is the only tool that does not return 0 under the C2 usable arm, and it is
the only arm short. Mechanism, reproduced directly at C0 (`git clone --shared` at `59c3810`):

```
$ TMPDIR=<fresh dir> PYTHONDONTWRITEBYTECODE=1 strace -f -e trace=mkdir,mkdirat -o st.log \
      python3 tools/registry-check.py --selftest
rc=1
SELFTEST_CASE timeout-kills-setsid-pipe FAIL (exit=1 elapsed=7.153s survivor=False marker=False)
SELFTEST_CASE timeout-kills-setpgid-pipe FAIL (exit=1 elapsed=7.955s survivor=False marker=False)
SELFTEST: FAIL (2 of 51 cases: timeout-kills-setsid-pipe, timeout-kills-setpgid-pipe)

$ TMPDIR=<fresh dir> PYTHONDONTWRITEBYTECODE=1 python3 tools/registry-check.py --selftest
rc=0
SELFTEST: PASS (51 cases)
```

`tmp_mkdirs=0` on the same arm, so the scratch-root behaviour is correct; the two failures are the
selftest's own 1.5 s pipe-timeout cases stretched to 7.2–8.0 s by `strace -f` (the counter's usable
arm wraps every tool in strace). The same 6/7 was measured at **base** when the counter was re-run
there (`.ufo/evidence/round-54/before/c2.stdout`, `usable_ok=6 … total=14`) while the control receipt
at freeze time recorded `usable_ok=7 … total=13` — i.e. the arm is load-sensitive, not content-broken,
and it is flaky on this host. Consequence for the round: `CTL_POS_c2` (pre-registered `true`) runs the
same counter on the same host, so a deciding run that lands on the slow side of this arm prints
`total=1` and refuses. This is reported, not fixed (seat bounds).

### C2 target — verbatim from `.ufo/evidence/round-54/contract.json`

> C2_R54_PASS=true: 7/7 self-tests exit 2 with a naming could-not-evaluate line and no traceback on a set-but-unusable TMPDIR, 7/7 exit 0 on an empty TMPDIR (declared unset) and on a usable one with no mkdir under /tmp, the seven registry rows carry the scratch_root cell, and the note corpus/knowledge/scratch-root-contract.md cites an S row mined this round with the lesson Gate naming its URL and 2026-10-28

Kill rule, verbatim: "any arm short of 7/7 makes C2_R54_PASS=false".
Controls: `CTL_0`, `CTL_EXIT0` (phase A/B as scripted; `CTL_0` false at base), `CTL_POS`
(true at the deciding revision). No phase-B receipt on disk at C0.

## What measures the two claims at the deciding revision

`deciding-run.sh LANE REV FREEZE OUTDIR` is the only path that produces the readings above from
committed bytes: it refuses unless HEAD is REV, the tree is clean, both control receipts
(`controls-a.*`, `controls-b.*`) are committed at REV in commits descending from FREEZE, and each
counter gets a start/exit receipt. It also requires `NOHARM … ok` on all 14 monitors and
`FROZEN_UNCHANGED=1` over the eleven frozen paths, then runs the census. Verified in this seat: the
frozen-path list in `deciding-run.sh` matches `contract.json:frozen_paths` (11 entries each), and the
census is green (below). Not verified by this seat: any deciding-run execution — HEAD moved to
`99c3bc8` mid-seat and no `controls-b` receipt exists yet.

## Landed changes

### Freeze commit `441c26b` — "claim contract, both counters, no-harm monitors, controls harness and freeze manifest (pre-seat)"

8 files, +790, no deletions. This is the instrument, not content:

| File | What it is |
|---|---|
| `.ufo/evidence/round-54/contract.json` | the two claims, frozen before any seat ran; `lowest_axis: calibration (8)` |
| `.ufo/evidence/round-54/freeze.json` | sha256 of the seven frozen instrument files |
| `.ufo/evidence/round-54/c1/measure.py` | C1 counter, 5 arms (precheck, round-21 monitor, re-key binding, reader reports, unstable inputs) |
| `.ufo/evidence/round-54/c1/lost-headings-at-base.json` | the seven base-lost headings |
| `.ufo/evidence/round-54/c2/measure.py` | C2 counter, 5 arms (unusable / empty / usable+strace / registry docs / note+sources) |
| `.ufo/evidence/round-54/no-harm.sh` | 14 monitors (12 carried from round 53 + `ledger-not-shrunk`, `sources-not-shrunk`) |
| `.ufo/evidence/round-54/deciding-run.sh` | the single deciding invocation and its refusals |
| `.ufo/evidence/round-54/control/controls.sh` | phase-A controls (`CTL_0`, `CTL_R53`, `CTL_FAB`, `CTL_LOGINPUT`), phase-B (`CTL_POS_c1`, `CTL_POS_c2`, `CTL_EXIT0`) |

### Content commit `59c3810` — "one scratch-root exit class across seven tools (ScratchRootUnusable -> exit 2), registry scratch_root cells, scratch-root contract note + S277-S279, SKILL three-arm rule, lesson Gate/Mistakes"

12 files, +2866 / −11 (measured `git diff --stat 441c26b 59c3810`):

| Path | Δ | What landed |
|---|---|---|
| `tools/env-diff.py` | +15/−5 | `class ScratchRootUnusable(RuntimeError)`; helper raises it (message unchanged); `--selftest` entry point catches it, prints `ENVDIFF_SETUP: could-not-evaluate: …`, returns 2; docstring records "An empty TMPDIR is unset" |
| `tools/bash-witness-study.py` | +12/−5 | same class; `main` catches it around the handler dispatch, prints `WITNESS_STUDY: could-not-evaluate: …`, returns `EXIT_CANNOT` (2) |
| `tools/evidence-disposition.py` | +15/−5 | same class; selftest path catches it, prints `evidence-disposition.py: could-not-evaluate: …`, returns 2 |
| `tools/pin-disposition.py` | +15/−5 | same class; `--selftest` path catches it, prints `pin-disposition.py: could-not-evaluate: …`, returns 2 |
| `tools/registry.json` | +7 | one identical `scratch_root` cell on each of the seven selftest rows (repeat-control, bash-witness, pin-disposition, evidence-disposition, context-capture, registry-check, env-diff) — verified 7/56 rows carry the cell, and the cell names TMPDIR, the empty-string arm and the could-not-evaluate class |
| `corpus/knowledge/scratch-root-contract.md` | +60 new | the note: three-arm table (`unset` / `empty` / `unusable`), why the class is uniform (round 53 routed defect R53.6), what measures it, falsifier (CTL_EXIT0 / `dir="/tmp"`) |
| `corpus/SOURCES.md` | +5 | rows S277 (POSIX TMPDIR), S278 (CPython `_candidate_tempdir_list`:163-165), S279 (Python docs search order), all `mined`, all `2026-10-28`, all pointing at the note; trailer line moves "Next unused id" to S280 |
| `corpus/lessons/round-54.md` | +94 new | `## Gate` (three rows with URLs, byte counts, sha prefixes, located quotes), `## Mistakes` (the round-53 `ls-tree` pathspec that left the re-key arm dead; routed R53.1), QUALITY criterion 105, and "The method" |
| `SKILL.md` | +8 | one `## Standing rules` bullet: "The scratch root has three arms" — unset → platform default; empty → unset (S278:163-165, S279); unusable → exit 2, could-not-evaluate, naming the value; cites the note and the C2 counter |
| `.ufo/evidence/round-54/assimilation/S277-posix-env.html` | +872 new | snapshot (unverified byte-for-byte against HTTPS by this seat) |
| `.ufo/evidence/round-54/assimilation/S278-tempfile.py` | +952 new | snapshot (same) |
| `.ufo/evidence/round-54/assimilation/S279-tempfile-docs.html` | +822 new | snapshot (same) |

### Not landed at C0 (measured, working-tree only)

* `.ufo/waves/round-54/` — **0 tracked files** at `59c3810`; the 76-seat dispatch spec, registry and
  every reader/attack report are untracked. That is why arms 3 and 4 of the C1 counter read `0/7` at
  C0: no `rekey-r54-*` directory and no committed reader JSON exist yet.
* `.ufo/evidence/round-54/before/` — **0 tracked files** at C0; `c1.stdout` (363 B) and `c2.stdout`
  (1355 B) exist only in the working tree (mtime 11:29 / 11:32).
* `.ufo/evidence/round-54/control/controls-a.{stdout,exit}` and `r53-counter-at-88afa941.stdout` —
  untracked at C0 (only `control/controls.sh` is tracked), so `deciding-run.sh` would refuse with
  `DECIDING_REFUSED control-receipt-missing` at C0. `controls-b.*` does not exist at all.
* `.ufo/evidence/round-54/integrate/binder.py` — untracked at C0 (its output, the `rekey-r54-<c0>`
  ledger entries, therefore cannot exist at C0 either).
* `corpus/QUALITY.md` — no diff at the time of writing; the QUALITY 105 bullet landed in `99c3bc8`
  (C1 fix pass), not in C0.

### Conformance (round-start check, this seat)

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
exit=0                       (last line: tameshi ok /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md)
rows in corpus/SOURCES.md at 59c3810: 139      (grep -cE '^ {0,3}\| S[0-9]{3,} \|')
```

No tool was installed or upgraded by this seat; no package manager was invoked.

## Provenance gaps and measurement caveats (reported, not fixed)

1. **The C2 `usable_ok` arm is flaky on this host.** Same frozen counter, same revision family:
   `7/7` in the freeze-time control receipt (`CTL_0_c2`, total 13), `6/7` in the working-tree
   `before/c2.stdout` at base (total 14), and `6/7` in all three of this seat's C0 runs (total 1).
   Cause isolated to `registry-check-selftest` under `strace -f` (two pipe-timeout cases, 7.2–8.0 s
   against a 1.5 s budget). Any "after" reading of the C2 `total` must therefore be read together with
   `usable_ok`, and `CTL_POS_c2` is at risk on a loaded host.
2. **The contract's C2 `before` string ("total=13") is one sample of that flaky arm**, not a stable
   property: a faithful re-run at the same `d33053f7` reads `total=14`. The C1 `before` string
   (`credited=57 lost=7 monitor=6/57`) does reproduce exactly, twice.
3. **The base artifacts the contract cites are not committed at C0.** `.ufo/evidence/round-54/before/`
   has 0 blobs in `59c3810`, and `control/controls-a.*` are untracked there. The base numbers are
   reproducible (this seat reproduced them), but at C0 the "before" side of the contract rests on
   working-tree files; only the freeze-time receipt records them.
4. **`naming` does not discriminate the class.** At base, `naming=7` while `unusable_exit2=3`: four
   tools printed the `could-not-evaluate` wording inside an uncaught `RuntimeError`. Reading
   `naming=7` as coverage of the exit class would over-credit base — the arm that separates the two
   revisions is `unusable_exit2` (3 → 7).
5. **HEAD moved during this seat** (`59c3810` → `99c3bc8`, C1 fix pass, 26 wave reader findings). All
   values above are pinned to `59c3810` as the assignment requires; the post-C0 tip was **not**
   measured here, so no number in this section should be read as the state of `99c3bc8`.
6. Two of the seven tools print the base class name inside their line (`context-capture`:
   `SELFTEST: FAIL (setup error: RuntimeError: …)`; `repeat-control`: `repeat-control: setup:
   RuntimeError: …`). They still exit 2 and name the value, so the frozen arm passes them; noted so the
   report does not describe the seven lines as uniformly formatted.

## What this seat did not do

No lane file was edited; no git mutation of any kind was run in the lane (all reads were `git show` /
`git ls-tree` / `git diff`; the only clones were `git clone --shared` under scratch). No counter,
contract, freeze, ledger, registry, wave spec or report belonging to another seat was modified.
Everything written by this seat is this file plus the scratch tree, which was removed at exit.

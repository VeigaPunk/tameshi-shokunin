# T55W1LabMode — round-55 w1 / lazy modes under load

Seat: `T55W1LabMode` (leaf, no dispatch). Item: **probe — lazy modes stay lazy.**
Judged on: operability. No lane production file was edited. Every git call named
`-C <scratch clone|fixture>`; no mutating git/jj command ran anywhere.

## Item and verdict

Hypothesis under test, verbatim: *the five modes the counter calls lazy never
allocate scratch, even when their inputs make them work hardest.*

**Verdict: not falsified.** Eight real-workload probes over the five modes, run
under an unusable `TMPDIR` on two byte-sets (base commit `0a2010ac`, and the
L1's in-flight integrated tool bytes), all hold: exit class unchanged, no frozen
scratch-root line, no `RuntimeError`/`Traceback`, and **zero `mkdir`/`mkdirat`
syscalls** in either the unusable or the usable arm. The one finding is a
record-integrity observation about a base receipt in the worktree (§6), not a
lazy-arm failure.

## 1. What "lazy" means here (the counter's own table)

`.ufo/evidence/round-55/c2/measure.py:modes()` calls these five `allocating=False`,
expected exit 0, bench cwd = clone:

| # | mode (counter label) | argv |
|---|---|---|
| L1 | `repeat-control --snapshot` | `python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate` |
| L2 | `bash-witness-study count` | `python3 tools/bash-witness-study.py count` |
| L3 | `pin-disposition --read` | `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` |
| L4 | `evidence-disposition --json` | `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json --json` |
| L5 | `context-capture --check` | `python3 tools/context-capture.py --check --json` |

The counter only exercises these with inputs that already pass. My probe keeps
each mode's argv honest but makes the input fail, so the mode does its full
work before reporting (the "work hardest" arm).

## 2. Scratch and clones

```console
$ export HYAKU_SCRATCH=/fast/scratch/hyaku; S=$HYAKU_SCRATCH/tameshi-r55/T55W1LabMode
$ git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/tameshi-shokunin $S/clone
$ git -C $S/clone checkout -q --detach 0a2010acd1e92e4e332774050825e21bcfc7e079
$ git -C $S/clone rev-parse HEAD; git -C $S/clone rev-parse --show-toplevel
0a2010acd1e92e4e332774050825e21bcfc7e079
/fast/scratch/hyaku/tameshi-r55/T55W1LabMode/clone
$ cp -a $S/clone $S/clone-int      # then copy the lane worktree's four dirty tool bytes
```

The lane worktree is dirty with the L1's in-flight integration (uncommitted), so
`git clone` cannot see it; `clone-int` is the base commit plus the lane
worktree's current `tools/{repeat-control,context-capture,registry-check}.py`
and `tools/registry.json` (byte hashes in
`T55W1LabMode-receipts/tool-and-workload-hashes.txt`). Probe-relevant hashes:

```
tools/repeat-control.py   base 3f82aa5a...  worktree a8fad68f...
tools/context-capture.py  base be539b4c...  worktree f1043425...
tools/pin-disposition.py  base c917bc41...  worktree c917bc41... (unchanged)
tools/evidence-disposition.py / bash-witness-study.py unchanged
```

## 3. Workloads (why each makes its mode work hardest)

All built under scratch by `$S/make_work.py`; hashes in
`T55W1LabMode-receipts/tool-and-workload-hashes.txt`.

1. **pin-disposition** — manifest whose pins all mismatch: six real legs
   (`--root /home/vgpnk/Projects/shokunin`), every `expected_sha256` flipped and
   the last `pinned_commit` set to `000…0`. Forced the tool through
   `rev-parse`, `cat-file -t`, `cat-file blob`, worktree hashing and
   `head_observation` for all six repos → `legs=6 unavailable=6`
   (`pinned_blob_mismatch` ×5, `pinned_commit_missing` ×1), exit 0.
2. **context-capture (explicit, mismatch)** — the 29 KB frozen receipt plus an
   expected file pinning `id=context_consistent exit=1`. Full re-derivation,
   then `expected_verdict_mismatch`, exit 1.
3. **context-capture (explicit, tampered)** — same receipt, expected digest
   `ffff…` → `snapshot_tampered`, exit 2.
4. **context-capture (frozen)** — `--check --json`, the built-in pin, exit 0.
5. **evidence-disposition (heavy, clean)** — the round-18 v2 dispositions at
   `--root .`: all four pins hashed, git historical inputs resolved, 12 checks
   replayed → `passed=11 superseded=1 failed=0`, exit 0.
6. **evidence-disposition (failing)** — a self-contained v1 lane
   (`work/ed-lane`) with every pin matching live bytes and one row whose receipt
   observed `exit=1`/`NO_ALPHA` while expected says `exit=0`/`ALPHA_OK` →
   `findings=[expected_contains_missing, expected_exit_mismatch] failed=1`,
   exit 1.
7. **repeat-control --snapshot (mismatch)** — the committed
   `.ufo/evidence/round-12/ControlGate/mismatch` snapshot: three observations
   re-hashed and re-classified → `REPEAT_CONTROL: controls_mismatch`, exit 1.
8. **bash-witness-study count (tampered)** — a copy of round-12 `BashWitness`
   with `counts.killed_on_witness` bumped 8→9: ten rows and their raw logs
   re-derived, then
   `WITNESS_STUDY: COUNT summary/raw mismatch counts.killed_on_witness: stored=9 recomputed=8`,
   exit 1.

Expected exit classes are the tools' own:
`pin-disposition` USAGE "exit 0 observations emitted (drift and unavailable legs
included)"; `context-capture` USAGE "exit 0 clean / 1 mismatch / 2
could-not-evaluate"; `evidence-disposition` `emit_result` (0 clean, 1 failed) and
`emit_could_not_evaluate` (2); `repeat-control` USAGE ("an intact snapshot …
exits 0"; `controls_mismatch` 1; `setup_error`/`snapshot_tampered` 2);
`bash-witness-study` `EXIT_OK, EXIT_FAIL, EXIT_CANNOT, EXIT_USAGE = 0,1,2,64`.

## 4. Detector

`$S/probe.py` runs each workload twice — usable `TMPDIR=$S/out-*/tmp-usable` and
unusable `TMPDIR=$S/out-*/no-such-tmpdir` (which is never created) — captures
rc/stdout/stderr, then re-runs it under
`strace -f -e trace=mkdir,mkdirat,openat`. `lazy-holds` requires **all** of:

- `rc_unusable == rc_usable == expected` (a scratch attempt changes the class);
- no line matching the frozen grammar and no `cannot create clone scratch`
  marker in stdout+stderr;
- no `RuntimeError` token, no `Traceback`;
- strace: zero `mkdir`/`mkdirat` lines under the unusable TMPDIR or `/tmp`;
- strace: zero `openat(..., O_CREAT, ...)` under those paths;
- strace: **zero mkdir at all in either arm** (these eight workloads are all
  read-only modes; any mkdir is an allocation signal regardless of TMPDIR).

Positive control: five `--selftest` modes under the same unusable TMPDIR must
refuse with exit 2 and exactly one frozen-grammar stderr line — proving the
environment really is unusable and the refusal path is armed.

## 5. Results

Command:

```console
$ python3 probe.py --clone $S/clone     --work $S/work --label base       --out $S/out-base
$ python3 probe.py --clone $S/clone-int --work $S/work --label integrated --out $S/out-int
```

### Base `0a2010ac` — `T55W1LabMode-receipts/probe-base-summary.txt`

```
pin-disposition --manifest                                 rc=0/0 expected=0 mkdir_scratch=0 creat_scratch=0 lazy-holds
context-capture --check --receipt/--expected (mismatch)    rc=1/1 expected=1 mkdir_scratch=0 creat_scratch=0 lazy-holds
context-capture --check --receipt/--expected (tampered)    rc=2/2 expected=2 mkdir_scratch=0 creat_scratch=0 lazy-holds
context-capture --check (frozen receipt)                   rc=0/0 expected=0 mkdir_scratch=0 creat_scratch=0 lazy-holds
evidence-disposition --root . --dispositions (heavy, clean) rc=0/0 expected=0 mkdir_scratch=0 creat_scratch=0 lazy-holds
evidence-disposition --root ed-lane (failing)              rc=1/1 expected=1 mkdir_scratch=0 creat_scratch=0 lazy-holds
repeat-control --snapshot (mismatch)                       rc=1/1 expected=1 mkdir_scratch=0 creat_scratch=0 lazy-holds
bash-witness-study count (tampered counts)                 rc=1/1 expected=1 mkdir_scratch=0 creat_scratch=0 lazy-holds
control:repeat-control --selftest                          rc=2 grammar=0 FAIL
control:context-capture --selftest                         rc=2 grammar=0 FAIL
control:pin-disposition --selftest                         rc=2 grammar=1 ok
control:evidence-disposition --selftest                    rc=2 grammar=1 ok
control:bash-witness-study selftest                        rc=2 grammar=1 ok
```

`rc=A/B` is unusable/usable; mkdir counts are the unusable arm. Full per-run
stdout/stderr/census: `results-base.json`. The two failing controls are the
C2-before defect itself, not a probe defect: base prints
`repeat-control: setup: RuntimeError: …` on stderr and
`SELFTEST: FAIL (setup error: RuntimeError: …)` on **stdout**
(`positive-controls-base.txt`), exactly what the frozen counter's `grammar=6/8`
records.

### Integrated tool bytes (lane worktree) — `probe-integrated-summary.txt`

Same eight lines, all `lazy-holds`; all five controls `grammar=1 ok`
(`positive-controls-integrated.txt`). The in-flight
`ScratchRootUnusable` handling in `repeat-control.py`/`context-capture.py` turns
the base defect into the frozen line on stderr with exit 2 and nothing on
stdout — an independent regression check on the integration's item 1.

### Counter's lazy arm reproduced verbatim

`T55W1LabMode-receipts/counter-lazy-arm-reproduced.txt` — the five counter argvs
run at base under `TMPDIR=$S/out-base/no-such-tmpdir` (absent):

```
--- tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate   rc=0 stdout_lines=5   stderr_lines=0  REPEAT_CONTROL: controls_match
--- tools/bash-witness-study.py count                                       rc=0 stdout_lines=15  stderr_lines=0  unresolved none
--- tools/pin-disposition.py --manifest … --root /home/vgpnk/Projects/shokunin rc=0 stdout_lines=197 stderr_lines=0
--- tools/evidence-disposition.py --root . --dispositions … --json          rc=0 stdout_lines=197 stderr_lines=0
--- tools/context-capture.py --check --json                                 rc=0 stdout_lines=1   stderr_lines=0  {"exit": 0, …, "id": "context_consistent", "receipt": {"digest_matches": true, …
```

So `lazy=5/5` at base is independent of the counter, and remains 5/5 with
failing inputs.

## 6. Finding (record integrity, report-only)

**The worktree copy of the frozen-set base receipt
`.ufo/evidence/round-55/before/c2.stdout` has lost 42 of its 43 lines.** The
committed file at `631cd645` has 43 lines (the per-mode `EXPLAIN` lines plus the
summary); the current worktree file has only the summary line.

```console
$ git -C $L show 631cd6455e58dce969310b4c0466c3383d9f5108:.ufo/evidence/round-55/before/c2.stdout | wc -l
43
$ wc -l $L/.ufo/evidence/round-55/before/c2.stdout
1
$ sha256sum <committed> <worktree>
789f94e194841415ab125898b185e495a542fffa002772a21a84da4b2300ac58  (at freeze)
77721c4a33979a5b3b7824b99df245844125bd6c29680260198e9c1ad83bbc05  (worktree, truncated)
```

`before/c2.stdout` is not in the contract's `frozen_paths`, so this is not a
frozen-counter defect and I did not touch it. But if the worktree truncation is
committed, the only remaining evidence for the two base `FAIL` grammar arms
(`repeat-control --selftest`, `context-capture --selftest`) is gone from the
lane; the summary line alone cannot show *which* modes failed. **Recommendation
to the L1: restore the 43-line version before committing** (a copy of the
freeze-commit bytes is at
`T55W1LabMode-receipts/before-c2.stdout-at-freeze.txt`). Nothing about C1/C2's
predicate depends on it.

No other discrepancy found in the frozen counters/contract: the C2 target text
(`grammar=6/8 lazy=5/5 … total=18`) matches what I reproduced at base.

## 7. Mutant: the detector is load-bearing

One plausible defect at the smallest behaviour-bearing point: a refactor makes a
lazy mode materialize its input under the scratch root, **with the CR47 failure
mode** — `tempfile.gettempdir()` instead of `strict_scratch_root()`, so a broken
`TMPDIR` silently falls back to `/tmp`:

```diff
 def run_mode(manifest_path, root_path):
+    # round-55 lab mutant: a plausible refactor that materializes a
+    # receipt copy under the scratch root before reading the manifest.
+    tempfile.mkdtemp(prefix="r55-lab-mutant.", dir=tempfile.gettempdir())
     entries = read_manifest(manifest_path)
```

in `$S/clone-mut/tools/pin-disposition.py`
(`c917bc41…` → mutant `b6dfadd5…`). This is the hard case: the exit class does
**not** move, and no scratch marker is printed.

```console
$ python3 probe.py --clone $S/clone-mut --work $S/work --label mutant-only --out $S/out-mut-only --only pin-disposition
pin-disposition --manifest   rc=0/0 expected=0 mkdir_scratch=1 creat=2 FALSIFIED
$ # mutant census, unusable arm:
usable   rc=0  stdout_lines=197  mkdir_total=1
unusable rc=0  stdout_lines=197  mkdir_total=1
   2510469 mkdir("/tmp/r55-lab-mutant.pct1l9eq", 0700) = 0
   2510469 openat(AT_FDCWD, ".../no-such-tmpdir/r4g0kahp", O_RDWR|O_CREAT|O_EXCL|O_NOFOLLOW|O_CLOEXEC, 0600) = -1 ENOENT (No such file or directory)
   2510469 openat(AT_FDCWD, "/tmp/idve9umb", O_RDWR|O_CREAT|O_EXCL|O_NOFOLLOW|O_CLOEXEC, 0600) = 3
```

Killed by the census arm alone: rc 0/0, 197 identical stdout lines, zero stderr —
only the `/tmp` `mkdir`/`O_CREAT` reveals the allocation, and the attempted
`openat` under the bogus TMPDIR followed by `/tmp` is precisely the silent
fallback the strict root exists to refuse.

Restoration evidence: restored `pin-disposition.py` to the pristine copy, hash
back to `c917bc41c3f40dae3eacea492d861211c2a4fe1e530cb9f22c5f8d6ff47d2988`,
`git -C $S/clone-mut diff --stat -- tools/pin-disposition.py` empty, and re-probe
`rc=0/0 expected=0 mkdir_scratch=0 lazy-holds`
(`results-restored.json`, `mutant-probe.txt`).

One discarded workload, recorded for honesty: editing a row of the round-18
**v2** dispositions (rather than adding a self-contained v1 fixture) is refused
by design, `supersedes_mismatch` exit 2, because `check_supersedes_lineage`
requires the rows to equal the superseded document's rows. The failing set above
uses a v1 lane whose pins all verify, so the exit-1 arm is a genuine failed
row, not a refused document.

## 8. Scope notes

- **Counter extension this evidences:** the C2 counter's `lazy` arm only feeds
  passing inputs; the probe shows the class also holds on failing inputs and on
  the two `context-capture` code paths (`frozen` and `explicit`) plus both
  `evidence-disposition` schemas (v1 fixture, v2 round-18). No contract change
  follows; the lazy label survives a heavier arm.
- **Idle surfaces:** the counter's `cannot_see` note asks whether an
  undocumented mode allocates on its first statement. Not fully answered for the
  other tools; it is answered for the five lazy modes' documented plus one
  undocumented-per-tool arm (frozen `context-capture --check`).
- **Census:** `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`
  exits 0 (informational duplicate-url rows only).
- **Tooling:** no install/upgrade; `python3` 3.14.8 and `strace` were already
  present.
- Scratch `$S` is removed after these receipts were copied into
  `.ufo/waves/round-55/w1/T55W1LabMode-receipts/`; re-running needs
  `make_work.py` + `probe.py`, whose bytes are in the same receipts directory
  (`reproduce/make_work.py`, `reproduce/probe.py`).

## Receipts

All under `.ufo/waves/round-55/w1/T55W1LabMode-receipts/`:
`probe-base-summary.txt`, `probe-integrated-summary.txt`,
`probe-mutant-summary.txt`, `results-base.json`, `results-integrated.json`,
`results-mutant-only.json`, `results-mutant-full-unscoped.json`,
`results-restored.json`, `positive-controls-base.txt`,
`positive-controls-integrated.txt`, `lazy-per-mode.txt`,
`counter-lazy-arm-reproduced.txt`, `tool-and-workload-hashes.txt`,
`mutant-probe.txt`, `before-c2.stdout-at-freeze.txt`,
`reproduce/{make_work.py,probe.py}`.

# ReplaySurvivors — round 32 wave 1 (pre-data control for claim C1)

**Verdict: the hypothesis is CONFIRMED, not falsified.** All eight MutateHead survivors (T08, N05, H03, H04,
H05, N01, N02, N03) still survive the runner's own `--selftest` at the pinned runner blob, and D01 is still
killed by it. The falsification condition ("any MutateHead survivor is killed, or D01 survives") was not met.

The claim-relevant consequence: `tools/mutate-and-run.sh --selftest` cannot be the oracle for
`tools/tally-audit.py`. It rejects exactly one of the nine frozen must-kill copies (D01) and accepts the other
eight. A tool that reuses the runner's own harness reaches at best `kill=1/18` on the counter's frozen half.

No production file was edited. The runner stays byte-identical:
`tools/mutate-and-run.sh` sha256 `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` at lane
commit `c31814978969a41a8e9b0f7d99fa308c5993c1b7` and at the counter's `PIN_REV`
`e24688b2ff6cca1c9ad20e112f02c629b8597ff8` (both observed identical).

## Setup (exact commands)

```
mkdir -p /fast/scratch/hyaku/tameshi-r32-seats/ReplaySurvivors
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
    /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    /fast/scratch/hyaku/tameshi-r32-seats/ReplaySurvivors/lane
git -C /fast/scratch/hyaku/tameshi-r32-seats/ReplaySurvivors/lane checkout -q --detach \
    c31814978969a41a8e9b0f7d99fa308c5993c1b7
```

Clone HEAD observed: `c31814978969a41a8e9b0f7d99fa308c5993c1b7`. `df -h /fast` observed: `114G` free.

Copies were built by importing the frozen counter module itself (not by re-typing the mutations), so the copies
are exactly the counter's copies:

```
python3 /fast/scratch/hyaku/tameshi-r32-seats/ReplaySurvivors/build_copies.py
# imports .ufo/evidence/round-32/c1-measure.py, calls frozen_kill() on
#   git show e24688b2...:tools/mutate-and-run.sh
# writes each body to /fast/scratch/hyaku/tameshi-r32-seats/ReplaySurvivors/c-<id>/tools/mutate-and-run.sh
```

Observed output (abridged):

```
pinned sha256 a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9
frozen kill labels: ['T08', 'N05', 'H03', 'H04', 'H05', 'N01', 'N02', 'N03', 'D01']
wrote T08 12ad1d9076a55050 106251
wrote N05 e1ef181c1e621962 106217
wrote H03 2ac4ce5344e6100a 106182
wrote H04 0dc1e6b07452f610 106228
wrote H05 adf6763d6524f342 106218
wrote N01 c0a32ec4e69d3cb0 106137
wrote N02 31128639afc3e57a 106218
wrote N03 741907e82ca7e907 106218
wrote D01 71a66c5a611d408f 106211
```

Runner invocation, three at a time, each in its own copy directory:

```
cd /fast/scratch/hyaku/tameshi-r32-seats/ReplaySurvivors/c-<id> && timeout 900 bash tools/mutate-and-run.sh --selftest
```

(`/fast/scratch/hyaku/tameshi-r32-seats/ReplaySurvivors/run_selftests.sh`, three concurrent, `wait` every third.)

## Result table

| id | exit | MUTATE_SELFTEST line | VERDICT line | copy sha256 (first 16) |
|---|---|---|---|---|
| T08 | 0 | `MUTATE_SELFTEST: 106/106 pass` | `VERDICT: PASS` | `12ad1d9076a55050` |
| N05 | 0 | `MUTATE_SELFTEST: 106/106 pass` | `VERDICT: PASS` | `e1ef181c1e621962` |
| H03 | 0 | `MUTATE_SELFTEST: 106/106 pass` | `VERDICT: PASS` | `2ac4ce5344e6100a` |
| H04 | 0 | `MUTATE_SELFTEST: 106/106 pass` | `VERDICT: PASS` | `0dc1e6b07452f610` |
| H05 | 0 | `MUTATE_SELFTEST: 106/106 pass` | `VERDICT: PASS` | `adf6763d6524f342` |
| N01 | 0 | `MUTATE_SELFTEST: 105/105 pass` | `VERDICT: PASS` | `c0a32ec4e69d3cb0` |
| N02 | 0 | `MUTATE_SELFTEST: 106/106 pass` | `VERDICT: PASS` | `31128639afc3e57a` |
| N03 | 0 | `MUTATE_SELFTEST: 106/106 pass` | `VERDICT: PASS` | `741907e82ca7e907` |
| D01 | 1 | `MUTATE_SELFTEST: 100/106 pass` | `VERDICT: FAIL` | `71a66c5a611d408f` |

Falsification check, read against the stated condition:

- any MutateHead survivor killed? **No.** T08, N05, H03, H04, H05, N01, N02, N03 all exited 0 with
  `VERDICT: PASS`.
- D01 survives? **No.** D01 exited 1 with `VERDICT: FAIL`.

Hypothesis confirmed on both clauses.

## Supporting observations

**Determinism.** The whole nine-copy run was executed twice; the two result tables are byte-identical
(`diff <(sort results-run1.tsv) <(sort results.tsv)` → no output, exit 0). One `MUTATE_SELFTEST:` line and one
`VERDICT:` line per copy, both present in every log.

**Copy fidelity.** The eight survivors' full-file sha256 values are equal to the "Mutated SHA-256" column of
`.ufo/waves/round-30/wC/MutateHead.md` and to `.ufo/evidence/round-32/before/mutant-fidelity.txt`, e.g. T08
`12ad1d9076a55050624f0b104475afe95c1d89ede35245a345a1e2bbb03ee27b`, N05
`e1ef181c1e621962cf19574a0683109ee094387306af1766df14b215413929fe`, H03
`2ac4ce5344e6100a5980a2d44bbc4983562df5a0325ecf84610973094322f35c`, H04
`0dc1e6b07452f6108f9dd7f99050aa0d8b8450456c3424f22da1a7fc54e5d6cd`, H05
`adf6763d6524f342b5496ff52f0fce96e0b4a00b5ab26cfa43be2001654b36d0`, N01
`c0a32ec4e69d3cb07a7949efb7c9a83ac2b4b431f6e4da3f8bd76a1cd0d4cb34`, N02
`31128639afc3e57a0d68f0abe94cc5038954ff41d6f9949da4fa903331f56250`, N03
`741907e82ca7e907881cb985b7a504771de78d14b1179530661066a8f22a5b6f`. D01 has no MutateHead counterpart
(`mutant-fidelity.txt` says so explicitly); its sha256 is `71a66c5a611d408fe08c3618a18f30fe6d4e43308e36ee1f074420547c4f695c`.

**Where D01's kill comes from.** D01's six failing cases are all in the runner's own tally harness:

```
FAIL tally harness: one leg status 1 at each of 9 positions -> REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0) (7/9)
FAIL tally harness: one leg status 2 at each of 9 positions -> REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1) (7/9)
FAIL tally harness: statuses 1 1 0 0 0 0 0 0 0 -> REGRESSION: FAIL (cases=9 passed=7 failed=2 setup=0)
FAIL tally harness: statuses 2 2 0 0 0 0 0 0 0 -> REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)
FAIL tally harness: statuses 1 2 0 0 0 0 0 0 0 -> REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)
FAIL tally harness: statuses 3 0 0 0 0 0 0 0 0 -> REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)
```

To confirm the kill is caused by D01's *tally block* and not by some other part of the mutated file, I built
block-only substitutions (pristine runner, only the tally block swapped in) and reran the selftest:

```
T08 block-only  MUTATE_SELFTEST: 106/106 pass | VERDICT: PASS
N05 block-only  MUTATE_SELFTEST: 106/106 pass | VERDICT: PASS
D01 block-only  MUTATE_SELFTEST: 100/106 pass | VERDICT: FAIL
```

So the runner's harness catches D01 because its leg-status names come from `run_regression`'s `st_*=$?`
assignments rather than from the tally loop, and D01's loop drops `st_citecheck` while duplicating `st_js`.

**The miscount passes the run-time guard.** Driving the extracted tally block directly (pristine vs D01, one leg
status 2 in the last position) gives:

```
B0-pristine  rc=2  REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)
D01          rc=0  REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)
```

The block's own completeness guard (`npass + nfail + nsetup != nlegs`) does not notice the swapped operand: it
is a sum-preserving miscount. Only the harness's independent leg-name list notices. This matches the round-30
motivation recorded in the contract and it is the reason the L1's tool needs its own per-leg presence check.

## Design aid for the L1's `tools/tally-audit.py` (my own exploratory battery, not counter evidence)

Because the runner's harness kills only D01, I measured a battery of candidate discriminating signals over the
ten copies I had locally (nine must-kill plus the pristine runner). This is guidance for the tool's three
planned checks, not a claim about the counter's score. Signals, one per frozen must-kill copy:

| copy | mutation | signal that separates it from pristine |
|---|---|---|
| T08 | extra `4) npass=$((npass + 1)) ;;` arm | runtime: a leg status of 4 yields `SETUP ... cannot-verify=1` on pristine but `PASS` on T08; statically, the block's case-arm set becomes `{0,1,4}` |
| N05 | guard `!= nlegs` → `< nlegs` | runtime overcount stress: duplicate one loop operand (10 counted legs) — pristine refuses with `SETUP (case-tally mismatch: cases=9 counted=10)`, N05 prints `PASS (cases=9 passed=10)` |
| H03 | exact-line comparison removed | the copy's own `tally_line` accepts a deliberately wrong expected line (probe exit 0 where pristine exits 1) |
| H04 | `rc=$?` appended after the comparison | same: the copy's own `tally_line` accepts a wrong expected line |
| H05 | `for ti in 0 1 2 3 4 5 6 7 7` | the harness's own position list no longer covers position 8 (missing `{8}`) |
| N01 | one of the four multi-status vectors deleted | one of the four canonical vectors is absent from the harness source |
| N02 | guard-stress `&&` → `\|\|` | the stress conjunction is `\|\|` instead of `&&` |
| N03 | `&&` → `\|\|` in the comparison | the copy's own `tally_line` accepts a wrong expected line (exit-status-only match) |
| D01 | operand `st_citecheck` replaced by `st_js` | per-leg presence: the loop operand set is missing `st_citecheck` and duplicates `st_js`; runtime, a failing/setup last leg is reported as `PASS` |

Two cautions for the tool author, both measured:

- **Do not key a guard check on the guard's source text.** The must-accept copy `B1-T07` (`npass != nlegs`, a
  declared equivalent guard) does not contain the literal `npass + nfail + nsetup != nlegs`, so a text-keyed
  guard check would reject it. Under the order-independent overcount stress (duplicate the last operand as
  written, no assumption about operand order) all six must-accept copies refuse correctly with
  `SETUP (case-tally mismatch: cases=9 counted=10)`, and only N05 slips through.
- **Do not key a presence check on operand order.** The must-accept copy `B2-reversed` writes the nine operands
  in reverse order; a presence check must compare sets, not sequences.

The six must-accept copies also all pass the runner's own selftest (each `MUTATE_SELFTEST: 106/106 pass`,
`VERDICT: PASS`, exit 0) — observed for `B0-pristine`, `B1-T07`, `B2-reversed`, `B3-decoys`, `B4-cosmetic`,
`B5-renamed`.

## Files, tooling, bounds

- Scratch only: `/fast/scratch/hyaku/tameshi-r32-seats/ReplaySurvivors/` — `build_copies.py`,
  `build_accepts.py`, `run_selftests.sh`, `probe_guard.sh`, `probe_oracle.sh`, `probe_harness.py`,
  `probe_overcount.py`, `probe_overcount_generic.py`, `matrix_probe.py`, `build_blocksubs.py`, `copies.json`,
  `accept-copies.json`, `results.tsv`, `results-run1.tsv`, `harness-signals.json`, `matrix.json`, `logs/`.
- **No tool was installed or updated** in this seat: every probe used only Python 3 and coreutils already
  present on the host. No pacman transaction, no `uv tool install`, no release binary.
- No production file was edited; the only file written outside my scratch dir is this report. No `jj` command
  was run. No git write command was run in the fleet repo; the clone under my scratch dir was created with
  `git clone` only and never committed to. After the last read of the pinned blob I removed my scratch clone's
  `.git` directory to shrink the scratch footprint; the clone's work tree remains and
  `c-B0-pristine/tools/mutate-and-run.sh` was rebuilt from the pinned blob afterwards
  (sha256 re-verified as `a7d3f2dd…2eb9`).
- Every `--selftest` ran with its own copy directory under my scratch dir. The runner keeps its fixture
  scratch in `/tmp/tameshi-r4-2-selftest.XXXXXX` (hard-coded in the runner, `tools/mutate-and-run.sh:1477`);
  the two directories my D01 runs kept (`...amUJiV`, `...vdcxnU`) were removed afterwards. The several hundred
  other `/tmp/tameshi-r4-2-selftest.*` directories belong to other seats and were left untouched.
- No process I started was left running; all nine selftest runs and all probes completed within their
  timeouts.

## Risks and blockers

1. **The frozen must-kill set is not reachable by replaying the runner's harness.** A `tally-audit.py` that
   delegates to `--selftest` scores at best 1/18 on the frozen half. The L1's tool needs its own oracle; the
   signals tabulated above are measured, not speculative.
2. **D01 is the only copy the runner's harness kills**, so a tool that trusts the harness will appear to work
   on the one copy that looks most like the round-30 motivation (the sum-preserving operand swap). This is the
   most likely way the tool ships green on the frozen set while missing the eight survivors.
3. **Generated families are not exercised by this seat.** The counter's nine generated must-kill copies
   (`gT08`, `gN05`, `gH03`, `gH04`, `gH05`, `gN01`, `gN02`, `gN03`, `gD01`) and its two generated must-accept
   copies (`gB6-permuted`, `gB7-nonce`) were not built or run here. The signals above were measured on the
   frozen families only; the generated forms (for example `gN05` also allows `<= nlegs - 1`, `gH03` allows a
   prefix comparison `${out:0:11}`) are not covered by my battery.
4. **Scope limit.** This seat is a pre-data control. It neither predicts nor claims the counter's
   `C1_R32_PASS` value at the measurement revision; the counter is the frozen arbiter and the L1 runs it.

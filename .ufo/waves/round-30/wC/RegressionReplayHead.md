# RegressionReplayHead — full `--regression` ledger replay at the round-30 content revision

Seat: `RegressionReplayHead`. Item: no-harm, operability — the full ledger replay must pass at
`bb681566b18211adf8ae9c28df91e17678e3f545`, plus its `--selftest` detector (wave C, attempt 3).
Wall clock: mirror setup under one minute, replay 173.08 s, selftest 6.06 s, negative arm 158.35 s;
inside the 30-minute box.

## Verdict

**Pass, as expected.** At `bb681566b18211adf8ae9c28df91e17678e3f545`, the full ledger replay prints
`REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)` and exits 0.
All nine legs are byte-pinned replays with an exact expectation; every leg measured `match=10/10`
(15/15 for `bash-checklist-run`), `flips=0`, `inconclusive=0`. The runner's own `--selftest` passes
106/106 and its tally harness (the C1 detector surface) covers the routed `MutateLegSum` class: an
independently extracted tally block with one operand dropped refuses as
`REGRESSION: SETUP (case-tally mismatch: cases=9 counted=8)`, exit 2, and the same block with the
guard removed reproduces the round-29 false green (`PASS (cases=9 passed=8 …)`, exit 0). A
negative arm with one leg's revision removed from the fleet mirror refuses as
`REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)`, exit 2, with the other eight legs green —
no false pass on an unmaterializable leg.

One residual, non-blocking count-consistency gap is recorded in "Risks and limits": when an operand
is dropped **and** a different leg is red, the FAIL line reports parts summing to 8 against
`cases=9`; exit is still 1, so this is not a false green and the landed guard is not reached.

## Setup and mirror fidelity

Mirror built exactly as assigned, then pinned:

```
W=$(mktemp -d /tmp/rrh-r30c3-rNpy); mkdir $W/fleet
for d in /home/vgpnk/Projects/shokunin/*-shokunin; do
  b=$(basename $d); [ $b = tameshi-shokunin ] || ln -s $d $W/fleet/$b; done
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin $W/fleet/tameshi-shokunin
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
  git -C $W/fleet/tameshi-shokunin checkout -q --detach bb681566b18211adf8ae9c28df91e17678e3f545
```

Observed: `git rev-parse HEAD` → `bb681566b18211adf8ae9c28df91e17678e3f545`. The clone's
`tools/mutate-and-run.sh` sha256 is
`a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`, identical to the lane file
`/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh` and to the `REGRESSION_TOOL`
line below, so the replay measured the content revision's bytes, not a drifted copy.

The tool resolves `FLEET_ROOT` as three directory names up from `$SELF`
(`tools/mutate-and-run.sh:1358`), i.e. `$W/fleet`, which is why the mirror keeps the real sibling
repos as read-only symlinks next to the tameshi clone. The sub-invocations' own `MUTATE_TOOL` lines
in every `rg/*/sweep.log` name the same `$W/fleet/tameshi-shokunin/tools/mutate-and-run.sh`, so the
sweeps were run by the same pinned runner.

## Exact command and observed output

```
cd $W/fleet/tameshi-shokunin
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
  timeout 2400 bash tools/mutate-and-run.sh --regression --workdir $W/rg; echo "EXIT=$?"
```

Observed (stdout, verbatim; `REGRESSION_DATE` from the run):

```
REGRESSION_TOOL: /tmp/rrh-r30c3-rNpy/fleet/tameshi-shokunin/tools/mutate-and-run.sh sha256=a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9
REGRESSION_DATE: 2026-10-23T07:14:49Z
REGRESSION_BAND: ledger legs exact (killed-delta<=0 flips<=0 inconclusive=0 defects=exact); fixture-mode default killed-delta<=1 flips<=1
REGRESSION_EXPECT: recorded kill-rates — js-kimi-census=8/10 bash-surface-census=8/10 bash-tsukuroi-census=6/10 bash-mado-verify=4/10 bash-checklist-run=7/15 js-claims-check=7/10 js-round-gate=5/10 js-sources-check=5/10 js-cite-check=5/10
REGRESSION_PIN js-kimi-census: source=git repo=/tmp/rrh-r30c3-rNpy/fleet/kumitate-shokunin rev=175de6ba2e9e904010411b19cab27e0af9aad3d4 path=scripts/kimi-census.mjs mode=100644 sha256=83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426
REGRESSION_SWEEP js-kimi-census: MUTATE: DONE (target=js-kimi-census defects=10 killed=8 survived=2 inconclusive=0 kill-rate=80%)
REGRESSION_TABLE js-kimi-census: match=10/10 recorded-killed=8 measured-killed=8 survived=2 inconclusive=0 flips=0
REGRESSION_WORKDIR js-kimi-census: /tmp/rrh-r30c3-rNpy/rg/js-kimi-census
REGRESSION_CASE js-kimi-census: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION_PIN bash-surface-census: source=git repo=/tmp/rrh-r30c3-rNpy/fleet/kagi-shokunin rev=fecee8743e52eb8fb5fbb40782934cb619a1a96e path=corpus/surface-census.sh mode=100755 sha256=275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f
REGRESSION_SWEEP bash-surface-census: MUTATE: DONE (target=bash-surface-census defects=10 killed=8 survived=2 inconclusive=0 kill-rate=80%)
REGRESSION_TABLE bash-surface-census: match=10/10 recorded-killed=8 measured-killed=8 survived=2 inconclusive=0 flips=0
REGRESSION_WORKDIR bash-surface-census: /tmp/rrh-r30c3-rNpy/rg/bash-surface-census
REGRESSION_CASE bash-surface-census: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION_PIN bash-tsukuroi-census: source=git repo=/tmp/rrh-r30c3-rNpy/fleet/tsukuroi-shokunin rev=165307fe4746a8807b02ec4a7d7ecac0368454a6 path=tools/tsukuroi-census.sh mode=100755 sha256=084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5
REGRESSION_SWEEP bash-tsukuroi-census: MUTATE: DONE (target=bash-tsukuroi-census defects=10 killed=6 survived=4 inconclusive=0 kill-rate=60%)
REGRESSION_TABLE bash-tsukuroi-census: match=10/10 recorded-killed=6 measured-killed=6 survived=4 inconclusive=0 flips=0
REGRESSION_WORKDIR bash-tsukuroi-census: /tmp/rrh-r30c3-rNpy/rg/bash-tsukuroi-census
REGRESSION_CASE bash-tsukuroi-census: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION_PIN bash-mado-verify: source=git repo=/tmp/rrh-r30c3-rNpy/fleet/mado-shokunin rev=eead56b20ad2b28299ae4fa623d52a99b44c743c path=tools/mado-verify.sh mode=100755 sha256=d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13
REGRESSION_SWEEP bash-mado-verify: MUTATE: DONE (target=bash-mado-verify defects=10 killed=4 survived=6 inconclusive=0 kill-rate=40%)
REGRESSION_TABLE bash-mado-verify: match=10/10 recorded-killed=4 measured-killed=4 survived=6 inconclusive=0 flips=0
REGRESSION_WORKDIR bash-mado-verify: /tmp/rrh-r30c3-rNpy/rg/bash-mado-verify
REGRESSION_CASE bash-mado-verify: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION_PIN bash-checklist-run: source=git repo=/tmp/rrh-r30c3-rNpy/fleet/kagi-shokunin rev=fecee8743e52eb8fb5fbb40782934cb619a1a96e path=corpus/checklist-run.sh mode=100755 sha256=7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf
REGRESSION_SWEEP bash-checklist-run: MUTATE: DONE (target=bash-checklist-run defects=15 killed=7 survived=8 inconclusive=0 kill-rate=47%)
REGRESSION_TABLE bash-checklist-run: match=15/15 recorded-killed=7 measured-killed=7 survived=8 inconclusive=0 flips=0
REGRESSION_WORKDIR bash-checklist-run: /tmp/rrh-r30c3-rNpy/rg/bash-checklist-run
REGRESSION_CASE bash-checklist-run: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=15)
REGRESSION_PIN js-claims-check: source=git repo=/tmp/rrh-r30c3-rNpy/fleet/kumitate-shokunin rev=175de6ba2e9e904010411b19cab27e0af9aad3d4 path=scripts/claims-check.mjs mode=100755 sha256=e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b
REGRESSION_SWEEP js-claims-check: MUTATE: DONE (target=js-claims-check defects=10 killed=7 survived=3 inconclusive=0 kill-rate=70%)
REGRESSION_TABLE js-claims-check: match=10/10 recorded-killed=7 measured-killed=7 survived=3 inconclusive=0 flips=0
REGRESSION_WORKDIR js-claims-check: /tmp/rrh-r30c3-rNpy/rg/js-claims-check
REGRESSION_CASE js-claims-check: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION_PIN js-round-gate: source=git repo=/tmp/rrh-r30c3-rNpy/fleet/kumitate-shokunin rev=364f1d5954158ef8844bca4a5fef57b05d2f2ca5 path=scripts/round-gate.mjs mode=100755 sha256=f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9
REGRESSION_SWEEP js-round-gate: MUTATE: DONE (target=js-round-gate defects=10 killed=5 survived=5 inconclusive=0 kill-rate=50%)
REGRESSION_TABLE js-round-gate: match=10/10 recorded-killed=5 measured-killed=5 survived=5 inconclusive=0 flips=0
REGRESSION_WORKDIR js-round-gate: /tmp/rrh-r30c3-rNpy/rg/js-round-gate
REGRESSION_CASE js-round-gate: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION_PIN js-sources-check: source=git repo=/tmp/rrh-r30c3-rNpy/fleet/kumitate-shokunin rev=0acb7752d19058b953ebbeba253b1e35f6548de5 path=scripts/sources-check.mjs mode=100755 sha256=6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f
REGRESSION_SWEEP js-sources-check: MUTATE: DONE (target=js-sources-check defects=10 killed=5 survived=5 inconclusive=0 kill-rate=50%)
REGRESSION_TABLE js-sources-check: match=10/10 recorded-killed=5 measured-killed=5 survived=5 inconclusive=0 flips=0
REGRESSION_WORKDIR js-sources-check: /tmp/rrh-r30c3-rNpy/rg/js-sources-check
REGRESSION_CASE js-sources-check: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION_PIN js-cite-check: source=git repo=/tmp/rrh-r30c3-rNpy/fleet/kumitate-shokunin rev=1205c6621a2eccbb8ffceae86d9e7b79a7990b3a path=scripts/cite-check.mjs mode=100755 sha256=40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f
REGRESSION_SWEEP js-cite-check: MUTATE: DONE (target=js-cite-check defects=10 killed=5 survived=5 inconclusive=0 kill-rate=50%)
REGRESSION_TABLE js-cite-check: match=10/10 recorded-killed=5 measured-killed=5 survived=5 inconclusive=0 flips=0
REGRESSION_WORKDIR js-cite-check: /tmp/rrh-r30c3-rNpy/rg/js-cite-check
REGRESSION_CASE js-cite-check: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)
REGRESSION_WORKDIR: /tmp/rrh-r30c3-rNpy/rg (kept)
EXIT=0
```

Every `REGRESSION_PIN` sha256 equals the corresponding `PIN_*` constant in
`tools/mutate-and-run.sh:605-621` (for example `PIN_JS` at `:605` and `PIN_CITECHECK` at `:621` are
the two shown above), so the materialization check inside `regression_case` passed for all nine legs. The runner
does not write the fleet trees: after the replay, `git -C $W/fleet/tameshi-shokunin status
--porcelain` was empty, and all outputs sit under the given `--workdir` (`$W/rg/<leg>/`,
`$W/rg/specs/`). `--workdir` is kept on any outcome by design (`tools/mutate-and-run.sh:1464-1470`).

## `--selftest` detector

```
cd $W/fleet/tameshi-shokunin
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
  timeout 900 bash tools/mutate-and-run.sh --selftest > $W/selftest.log 2>&1; echo "EXIT=$?"
```

Observed: `EXIT=0`, 106 `PASS` lines, no `FAIL`, ending:

```
MUTATE_SELFTEST: 106/106 pass
VERDICT: PASS
```

The tally arms (the C1 surface) all pass (`selftest.log:95-103`):

```
PASS tally harness: block extracted, leg status names=9 (want 9)
PASS tally harness: all nine legs pass -> PASS passed=9, exit 0
PASS tally harness: one leg status 1 at each of 9 positions -> REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0) (9/9)
PASS tally harness: one leg status 2 at each of 9 positions -> REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1) (9/9)
PASS tally harness: statuses 1 1 0 0 0 0 0 0 0 -> REGRESSION: FAIL (cases=9 passed=7 failed=2 setup=0)
PASS tally harness: statuses 2 2 0 0 0 0 0 0 0 -> REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)
PASS tally harness: statuses 1 2 0 0 0 0 0 0 0 -> REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)
PASS tally harness: statuses 3 0 0 0 0 0 0 0 0 -> REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)
PASS tally harness: loop missing one operand -> SETUP case-tally mismatch, exit 2
```

The harness extracts the tally block by its literal start marker and the nine status names from the
`st_*=$?` assignments (`tools/mutate-and-run.sh:1994-1996`), then runs the block in a fresh Bash
process under fixed vectors (`:1998-2039`); the guard-stress arm removes the loop's last operand and
requires the `case-tally mismatch` refusal. The unrelated SETUP arms also passed, including
`regression pin mismatch is SETUP (exit 2)` (`:30`), `ledger leg pin mismatch is SETUP (exit 2)`
(`:58`), `ledger leg unresolvable revision is SETUP (exit 2)` (`:60`), and the exec-bit mirror arms
(`:62`, `:65`).

## Independent falsifiers (extracted tally block, my own harness)

I extracted the block with the literal start marker in Python (not the selftest's `awk`) and ran it
under four status vectors. The tally-loop line at `:1433` and the guard at `:1456` were edited only
in memory:

| Vector | Observed first line | Exit |
|---|---|---|
| pristine block, nine zero statuses | `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)` | 0 |
| `"$st_citecheck"` dropped, nine zero statuses | `REGRESSION: SETUP (case-tally mismatch: cases=9 counted=8)` | 2 |
| `"$st_citecheck"` dropped, first leg 1 | `REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=0)` | 1 |
| `"$st_citecheck"` dropped, guard replaced with `if false` | `REGRESSION: PASS (cases=9 passed=8; ledger legs exact: killed-delta<=0 flips<=0)` | 0 |

The last row is the round-29 `MutateLegSum` false green reproduced verbatim, and the second row shows
the landed guard refuses it; the third row is the residual recorded below.

## Negative arm: an unmaterializable leg must refuse, not pass

Second mirror, same recipe, but `mado-shokunin` is an empty `git init` directory (so
`eead56b2…` cannot resolve) while the other eight siblings are the real read-only repos:

```
N=$W/neg; mkdir -p $N/fleet
# symlink the eight other siblings, cp -a the pinned tameshi clone, then:
mkdir -p $N/fleet/mado-shokunin
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C $N/fleet/mado-shokunin init -q
cd $N/fleet/tameshi-shokunin
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
  timeout 900 bash tools/mutate-and-run.sh --regression --workdir $N/rg > $W/neg.log 2>&1
echo "NEG_EXIT=$?"
```

Observed: `NEG_EXIT=2`; eight `REGRESSION_CASE …: PASS`, zero `…: FAIL`; for the missing leg:

```
REGRESSION_CASE bash-mado-verify: SETUP (revision not found: /tmp/rrh-r30c3-rNpy/neg/fleet/mado-shokunin@eead56b20ad2b28299ae4fa623d52a99b44c743c)
REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)
REGRESSION_WORKDIR: /tmp/rrh-r30c3-rNpy/neg/rg (kept)
```

This confirms the exit map in the header (`tools/mutate-and-run.sh:132-137`): a leg that cannot be
verified is SETUP, never a pass, and the final tally names the one cannot-verify leg.

## Environment, custody, cleanup

- Tools: bash 5.3.20, python3 3.14.8, node v24.21.0, git 2.56.0, sha256sum 0.8.0. Nothing installed
  or upgraded; no pacman, uv, cargo or npm action.
- All execution inside my own `/tmp/rrh-r30c3-rNpy`; `GIT_DIR`, `GIT_WORK_TREE` and `GIT_INDEX_FILE`
  were unset for every command (`env -u …`). Read-only git only; no `jj` invoked; no git write
  command run. The tameshi lane and all sibling repos were read, never written.
- The only lane write is this report. Scratches (`$W/rg`, `$W/neg`) are kept for inspection; they sit
  under `/tmp` and each is bounded by the run's own nine case workdirs.
- `pgrep -af 'rrh-r30c3'` after the runs printed nothing; no process of mine remains and none was
  killed.

## Risks and limits

- One host, one toolchain snapshot, one run per arm. This establishes operability at this revision on
  this host, not on other hosts or future revisions.
- Residual count-consistency gap (not a false green): the completeness guard sits after the FAIL and
  SETUP branches (`tools/mutate-and-run.sh:1441-1461`), so when an operand is dropped **and** some
  other leg is red, the block prints `REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=0)` — parts
  sum to 8 against `cases=9` — and exits 1. The selftest's guard-stress arm only exercises the
  all-zero vector (`:2033-2039`), so this mixed vector is outside the detector's coverage. The exit
  code is still non-zero, so the routed defect class (false PASS, exit 0) is covered.
- The tally block, both extraction markers and the operand count assume nine legs
  (`:1432-1433`, `:1994-1995`); the knowledge entry
  `corpus/knowledge/regression-tally-completeness.md` states the same limit. Adding a tenth leg
  requires reviewing those fixed assumptions together.
- The working tree's `REGRESSION_DATE` differs run to run; the comparison here is of structure and
  values, not of a frozen captured file. No head receipt for `--regression` is stated in the
  knowledge entry, so there was no reference receipt to diff against.
- This report is supporting evidence only; C1 remains exploratory per
  `.ufo/evidence/round-30/contract-amendment-4.json` and no counter result is claimed here.

## Smallest safe correction

None required for the assigned no-harm replay: the ledger passes and the detector refuses the routed
defect. Optional, if the residual above is taken up in a later content revision: keep the exit
precedence as it is and make the FAIL/SETUP count lines self-consistent by appending the counted
total, e.g. `REGRESSION: FAIL (cases=%s passed=%s failed=%s setup=%s counted=%s)` with
`counted=$((npass + nfail + nsetup))` computed once before the branches (two `printf` format strings,
one variable, no logic change, guard and exit codes untouched). Do not move the guard above the FAIL
branch: that would turn a genuine failing leg into SETUP and lose the FAIL signal.

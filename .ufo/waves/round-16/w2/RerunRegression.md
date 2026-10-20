# RerunRegression — wave 2 falsify: ledger leg + selftest of tools/mutate-and-run.sh

Seat: TameshiR16.RerunRegression
Date: 2026-10-20
Attacked claim: `tools/mutate-and-run.sh` at lane commit
`c699c8c36d6e4eca4b796b81a8247904aa145ec8` reports
`REGRESSION: PASS (cases=7 passed=7` under `--regression --keep`, carries the
js-round-gate PIN line (rev `364f1d5…`, sha `f890e277…`), and passes `--selftest`.

**Verdict: holds.** Both gates pass exactly as claimed; the js-round-gate leg
materializes its pinned blob (`sha256=f890e277…`, rev `364f1d5…`, mode `100755`)
and replays 5/10 killed with 0 flips.

## Setup

The script derives `FLEET_ROOT` as `dirname^3` of `SELF` (a `readlink -f`
path), so a plain `/tmp` worktree alone would resolve sibling repos under
`/tmp`. I built a scratch fleet root and symlinked the four leg repos read-only:

```
SCRATCH=/tmp/tameshi-r16w2-RerunRegression-u8cNsj
mkdir -p $SCRATCH/fleet
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin worktree add --detach \
  $SCRATCH/fleet/tameshi-shokunin c699c8c36d6e4eca4b796b81a8247904aa145ec8
# -> "Preparing worktree (detached HEAD c699c8c)"
# -> "HEAD is now at c699c8c round-16: land js-round-gate case 7, ..."
ln -s /home/vgpnk/Projects/shokunin/{kumitate,kagi,tsukuroi,mado}-shokunin $SCRATCH/fleet/
```

Tool sha actually executed (worktree copy, matches the committed blob piped to
sha256sum):

```
89722ddb3082abd63136d025e0dfb08dcea9ffd91d58878beb230241b61f5594  tools/mutate-and-run.sh
```

Environment: bash (system), python3 3.14.8, git 2.56.0, node v24.21.0.

## Run 1 — `--selftest`

```
cd $SCRATCH/fleet/tameshi-shokunin && bash tools/mutate-and-run.sh --selftest
exit=0  (wall 7.62 s)
```

Key lines: every one of the `PASS …` lines printed clean; the counter and
verdict:

```
MUTATE_SELFTEST: 81/81 pass
VERDICT: PASS
```

Includes the r7-1 ledger-engine arms (git-materialized replay, drifted-tree
immunity, pin-mismatch SETUP, exec-bit mirror arms) and the r10-2/r16
embedded-ledger sweep: `PASS embedded leg specs: seven files written` plus a
`spec and recorded table agree` PASS for each of the seven legs including
`js-round-gate`.

## Run 2 — `--regression --keep`

```
cd $SCRATCH/fleet/tameshi-shokunin && bash tools/mutate-and-run.sh --regression --keep
exit=0  (wall 133.38 s)
scratch root kept: /tmp/tameshi-r4-2-regression.ZFuwvp
```

Provenance/expectation header:

```
REGRESSION_TOOL: /tmp/…/fleet/tameshi-shokunin/tools/mutate-and-run.sh sha256=89722ddb3082abd63136d025e0dfb08dcea9ffd91d58878beb230241b61f5594
REGRESSION_BAND: ledger legs exact (killed-delta<=0 flips<=0 inconclusive=0 defects=exact); fixture-mode default killed-delta<=1 flips<=1
REGRESSION_EXPECT: recorded kill-rates — js-kimi-census=8/10 bash-surface-census=8/10 bash-tsukuroi-census=6/10 bash-mado-verify=4/10 bash-checklist-run=7/15 js-claims-check=7/10 js-round-gate=5/10
```

The js-round-gate PIN line, verbatim:

```
REGRESSION_PIN js-round-gate: source=git repo=…/fleet/kumitate-shokunin rev=364f1d5954158ef8844bca4a5fef57b05d2f2ca5 path=scripts/round-gate.mjs mode=100755 sha256=f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9
```

All seven legs PASS at the exact ledger tolerance (match=N/N, flips=0,
inconclusive=0, control green, restore OK):

| leg | recorded | measured | flips | verdict |
|---|---|---|---|---|
| js-kimi-census | 8/10 | 8/10 | 0 | PASS |
| bash-surface-census | 8/10 | 8/10 | 0 | PASS |
| bash-tsukuroi-census | 6/10 | 6/10 | 0 | PASS |
| bash-mado-verify | 4/10 | 4/10 | 0 | PASS |
| bash-checklist-run | 7/15 | 7/15 | 0 | PASS |
| js-claims-check | 7/10 | 7/10 | 0 | PASS |
| js-round-gate | 5/10 | 5/10 | 0 | PASS |

Final line:

```
REGRESSION: PASS (cases=7 passed=7; ledger legs exact: killed-delta<=0 flips<=0)
```

## Independent pin re-check

```
git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin \
  show 364f1d5954158ef8844bca4a5fef57b05d2f2ca5:scripts/round-gate.mjs | sha256sum
# f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9
git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin \
  ls-tree 364f1d5… -- scripts/round-gate.mjs
# 100755 blob 1f7d623e7ba548b7181ad75ae93a2f0c0b8579f3  scripts/round-gate.mjs
```

The ledger pin in the script (`PIN_ROUNDGATE`/`REV_ROUNDGATE`,
tools/mutate-and-run.sh:562-563 at c699c8c) matches the kumitate object store
byte-for-byte and mode-for-mode. No drift.

## Notes / risks

- The run is faithful to the ledger contract: legs replayed from each repo's
  git object store at the recorded pins, exact tolerance, fleet trees never
  written. Only caveat: `--regression` from a bare `/tmp` worktree would fail
  SETUP because `FLEET_ROOT` resolves under `/tmp`; the symlinked scratch fleet
  root above is the minimal faithful arrangement (script code, not the
  working-tree files, is exercised — symlinked repos are only used through
  `git show`).
- Kept evidence: `/tmp/tameshi-r4-2-regression.ZFuwvp` (per-leg workdirs with
  `sweep.log`, `results.tsv`, `evidence/*.out`) plus full output captured at
  `/tmp/tameshi-r16w2-RerunRegression-u8cNsj/regression.out`.
- Scratch worktree registration removed (`git worktree remove`); no lane files
  written except this report; no commits, no installs performed.

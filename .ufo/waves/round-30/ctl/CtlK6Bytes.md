# CONTROL CtlK6Bytes — K6 (detector keyed on bytes)

CONTROL CtlK6Bytes-hash: meets=false C1_R30_PASS=false
CONTROL CtlK6Bytes-verbatim: meets=false C1_R30_PASS=false

Both controls are scored with the **frozen, unchanged** counter v2
(`.ufo/evidence/round-30/c1-measure-v2.py`, sha256
`5ed4e663ff16556d0bfef68a9fc1e3cf820ab8bc2b620169e800da914f0c8719`,
predicate label `C1_R30_PASS`, frozen in
`.ufo/evidence/round-30/contract-amendment-1.json`). Neither control reaches
`C1_R30_PASS=true`; the counter's equivalent-rewrite clauses (e) and (g) are
what defeat both byte-keyed detectors.

## Summary lines (verbatim from the counter's own stdout)

```
CtlK6Bytes-hash
C1_R30: rev=e090169167e757150019c52394f153e19fe0771a pristine_selftest=1 harness=19/19 refused_drops=9/9 killed=13/13 equiv_pass=0/4 heldout_killed=12/12 heldout_equiv=0/4
PREDICATE: C1_R30_PASS=false
exit=1

CtlK6Bytes-verbatim
C1_R30: rev=782a78b1eca3413c2d7f6f48e25c58b97af0b52f pristine_selftest=1 harness=19/19 refused_drops=9/9 killed=13/13 equiv_pass=2/4 heldout_killed=12/12 heldout_equiv=0/4
PREDICATE: C1_R30_PASS=false
exit=1
```

Base receipt for comparison (`.ufo/evidence/round-30/c1v2-at-base.stdout`, rev
`9ed6db84`): `pristine_selftest=1 harness=19/19 refused_drops=0/9 killed=0/13
equiv_pass=4/4 heldout_killed=0/12 heldout_equiv=4/4`, `C1_R30_PASS=false`,
exit 1.

## What was built

Both variants are single-commit children of the lane tip
`e59728df5ebb053c9810049c05fd4e9d59d82dee` and edit **only**
`tools/mutate-and-run.sh`. Each adds, in order:

1. **The K4 runtime guard** (verbatim from
   `.ufo/waves/round-29/w1/MutateLegSum.md` lines 175–195), inserted immediately
   before the PASS path in `run_regression` — a case-count completeness
   refusal:

   ```bash
   if (( npass + nfail + nsetup != nlegs )); then
     printf 'REGRESSION: SETUP (case-tally mismatch: cases=%s counted=%s)\n' \
       "$nlegs" "$((npass + nfail + nsetup))"
     printf 'REGRESSION_WORKDIR: %s (kept)\n' "$root"
     exit 2
   fi
   ```

   This is the part that satisfies the counter's runtime clause (c):
   `refused_drops=9/9` (up from `0/9` at base).

2. **A byte-keyed selftest detector** (the K6 shortcut), added inside
   `selftest()`:
   - **hash**: `awk`-extracts the tally block (from the line
     `  local nlegs=9 npass=0 nfail=0 nsetup=0 st` to the closing `}` of
     `run_regression`) from `$SELF`, `sha256sum`s it, and compares against a
     pinned digest
     `d064a8576f1a32e036b4c2b149bbe71044f8f6e35e50e1bc8417d061553b818b`.
   - **verbatim**: extracts the same block region and greps each of eight
     fixed-string tally lines out of it
     (`grep -qxF -- "$k6_pin" <<<"$k6_region"`), failing if any is absent.

   Neither detector observes behaviour. Both observe only the block's bytes.

## Why both controls fail the predicate

The counter's clauses (e) and (g) require `--selftest` to exit 0 with
`VERDICT: PASS` on **semantics-preserving rewrites** of the tally block
(E1–E4 and the seeded HE1–HE4). A byte-keyed detector necessarily fails that:
any rewrite that changes the block's bytes changes the digest / breaks a fixed
string, so the shortcut reports "not the pinned bytes" on a block that is
behaviourally identical.

Observed per-row (from the two `.stdout` receipts):

| rewrite | semantics | hash variant | verbatim variant |
|---|---|---|---|
| E1-reorder-operands | preserved | exit=1 (killed) | exit=1 (killed) |
| E2-arith-commuted | preserved | exit=1 (killed) | exit=1 (killed) |
| E3-comment-in-block | preserved | exit=1 (killed) | exit=0 (passes) |
| E4-noop-before-pass | preserved | exit=1 (killed) | exit=0 (passes) |
| HE1–HE4-equiv | preserved | all exit=1 | all exit=1 |

- **hash**: `equiv_pass=0/4`, `heldout_equiv=0/4`. Every equivalent rewrite
  changes the block's sha256, so all eight are reported as defects.
  Clause (e) and (g) both fail.
- **verbatim**: `equiv_pass=2/4`, `heldout_equiv=0/4`. E3 and E4 only *add*
  lines to the block, so the eight pinned lines survive and the detector
  passes them (clause (e) partially survives); but E1/E2 reorder or re-spell
  the pinned loop/arm lines and the seeded HE rewrites do the same, so (e)
  still fails at 2/4 and (g) fails at 0/4.

Both variants do satisfy the other clauses: `pristine_selftest=1`,
`harness=19/19`, `refused_drops=9/9`, `killed=13/13`, `heldout_killed=12/12`.
So the byte-keyed detector is *not* trivially broken — it kills every mutant
family and every held-out mutant — but it cannot distinguish "the tally was
broken" from "the tally was rewritten equivalently". That is precisely the
discrimination the counter's (e)/(g) clauses exist to force.

**Answer to the acceptance question**: yes — the equivalent-rewrite clauses
(e) and (g) defeat both variants. The hash variant is defeated outright
(0/4 and 0/4); the verbatim variant is defeated because a fixed-string
preservation check cannot survive a reordering (E1/E2) or a re-spelling
(HE1–HE4) of the block it pins, though it does tolerate purely additive
rewrites (E3/E4).

## Sub-finding: a whole-file verbatim grep is self-satisfying

An earlier spelling of the verbatim variant grepped the **whole** runner file
(`grep -qF -- "$k6_pin" "$SELF"`) rather than the extracted block region. Its
own pin literals live in that file, so every pin is always found and the
detector is inert: `killed=0/13`, `heldout_killed=0/12`,
`equiv_pass=4/4`, `heldout_equiv=4/4` — i.e. the shortcut does not even
detect the mutants it claims to detect, and only the K4 runtime guard carries
it (`refused_drops=9/9`). Reproduced and scored separately in the sandbox at
rev `5621354193da0bf50e72803d2a40729a551bba81`
(`C1_R30: rev=5621354… pristine_selftest=1 harness=19/19 refused_drops=9/9
killed=0/13 equiv_pass=4/4 heldout_killed=0/12 heldout_equiv=4/4`,
`PREDICATE: C1_R30_PASS=false`, exit 1). This is reported as a sub-finding
only; the two named controls scored above are the region-scoped forms, which
are the strictly harder test of the counter. Note the K6 control as literally
specified ("greps tally lines verbatim") is ambiguous between these two
spellings; the region-scoped one is the stronger control and is the one
reported as `CtlK6Bytes-verbatim`.

## Counter fidelity checks (both variants, before scoring)

Verified in the sandbox clones with the counter's own site constants, so the
counter could not have errored out (exit 2) instead of measuring:

- `BLOCK_START`, `ARM0`, `ARM1`, `ARMS`, `FAILCHK`, `SETUPCHK`, `PASSLINE`
  each occur exactly **1** time in both files (the K4 guard adds lines but
  duplicates no anchor).
- `LOOP_RE` matches exactly **1** time in both files.
- `tally_block()` extraction succeeds in both files (36 lines).
- `bash -n` clean on both.
- Direct `--selftest` on the pristine verbatim clone: `MUTATE_SELFTEST: 98/98
  pass`, `VERDICT: PASS`, exit 0 (the byte-keyed case passes on the
  unmodified block).

The counter therefore measured both variants rather than erroring: exit 1
with a full `C1_R30_ROW` table, not exit 2.

## Artifacts

| path | content |
|---|---|
| `.ufo/evidence/round-30/ctl/CtlK6Bytes-hash.diff` | `git diff HEAD~1 HEAD` for the hash variant |
| `.ufo/evidence/round-30/ctl/CtlK6Bytes-hash.stdout` | counter stdout + `exit=1` (sha256 `148a03175ccca34dc24812d3ecbc0322bc0c4f77de7f14988d45e9b744e45e5c`) |
| `.ufo/evidence/round-30/ctl/CtlK6Bytes-verbatim.diff` | `git diff HEAD~1 HEAD` for the verbatim variant |
| `.ufo/evidence/round-30/ctl/CtlK6Bytes-verbatim.stdout` | counter stdout + `exit=1` (sha256 `75796ea9bc13309bbab4a636858b7a80390677c54e6e2637822f7079e14f9b34`) |

## Sandboxes

`/fast/scratch/hyaku/tameshi-r30/ctl/CtlK6Bytes/{hash,verbatim,naive}/clone`,
each cloned from `/home/vgpnk/Projects/shokunin/tameshi-shokunin` and checked
out detached at `e59728df5ebb053c9810049c05fd4e9d59d82dee`. All git writes
were inside these clones with `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE`
unset. Commits: hash `e090169167e757150019c52394f153e19fe0771a`, verbatim
`782a78b1eca3413c2d7f6f48e25c58b97af0b52f`, naive sub-finding
`5621354193da0bf50e72803d2a40729a551bba81`.

## Bounds

No git write command ran in `/home/vgpnk/Projects/shokunin` or
`/home/vgpnk/Projects/shokunin/tameshi-shokunin`; no `jj` command ran
anywhere; no production file of the lane was edited (the only writes into the
lane are this report and the four `CtlK6Bytes-*` evidence files). Every
counter invocation was wrapped in `timeout 900`; the sandbox direct
`--selftest` in `timeout 300`. No process from this seat is still running
(`ps` shows no `CtlK6Bytes` / `c1-measure-v2` process). No tool was installed
or updated — the controls use only `awk`, `sha256sum`, `cut` and `grep -F`,
all already present in the runner's documented dependency set (coreutils).

## Note on the lane working tree

`git status` in the lane shows `M corpus/QUALITY.md`, `M corpus/README.md`,
`M corpus/SOURCES.md`, `M tools/mutate-and-run.sh` and untracked round-30
evidence files (`c1-measure-v4.py`, `coldread/`, `sources/`,
`CtlK8NoRun.*`, `corpus/knowledge/regression-tally-completeness.md`, …).
These are other seats' / the L1's work in progress, not this seat's — this
seat wrote only `CtlK6Bytes-hash.{diff,stdout}`,
`CtlK6Bytes-verbatim.{diff,stdout}` and this report. The lane HEAD at
report time is `8a8d25401413b76fb32b691412c9e1b1c83f2fed`; both controls were
scored against sandbox commits parented on `e59728df5`, the tip specified at
dispatch.

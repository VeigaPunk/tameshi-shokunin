# RerunC1Head — C1 supporting evidence, independent re-run

Seat: `RerunC1Head`. Item: C1 supporting evidence, independent re-run (wave C, attempt 3).
Time box: cold-read-class work not applicable; wall clock for the counter 91.22 s, well inside the 30-minute box.

## Verdict

**Reproduces.** In a fresh clone at `bb681566b18211adf8ae9c28df91e17678e3f545`, with both hash preconditions met, `c1-measure-v4.py` exits 0, prints the same `C1_R30:` summary line and `PREDICATE: C1_R30_PASS=true` as `.ufo/evidence/round-30/v4/head.stdout`. All 59 counter-emitted lines are byte-identical to the reference; the only textual difference is the trailing wrapper line `exit=0`, which the reference file carries and my capture recorded outside the redirect (as `EXIT=0`). No correction needed.

## Preconditions (all observed)

1. Sealed file hash matches `sealed_sha256`:
   `sha256sum .ufo/evidence/round-30/v4/c1-sealed.json` →
   `44116804c5cf990a5dec58d107a8a584b333e3dc89a8962a3d17761e11243729`, equal to `.ufo/evidence/round-30/contract-amendment-3.json:13`.
2. Counter hash matches `counter_sha256`:
   `sha256sum .ufo/evidence/round-30/c1-measure-v4.py` →
   `cccae0bd984a7c67c22d83a1e67d19e3ebc76c015094106a1370d330030a5f07`, equal to `.ufo/evidence/round-30/contract-amendment-3.json:12`.
3. The counter re-checks (1) internally at `.ufo/evidence/round-30/c1-measure-v4.py:266-267` against its own `SEALED_SHA256` at line 259 and would raise a counter error on mismatch; it did not.
4. `contract-amendment-4.json` was checked for superseding hash keys: it carries no `counter_sha256`, `sealed_sha256` or `predicate` field (keys are absent), so amendment-3 remains the hash authority.

## Clone

```
cd /home/vgpnk/Projects/shokunin
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  /fast/scratch/hyaku/tameshi-r30a3-seats/RerunC1Head/c
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../c checkout -q --detach bb681566b18211adf8ae9c28df91e17678e3f545
```
Observed: `rev-parse HEAD` → `bb681566b18211adf8ae9c28df91e17678e3f545`; `git status --porcelain` empty. Working-tree runner `tools/mutate-and-run.sh` sha256 `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` (the counter measures the rev via `git archive`, not the worktree, at `c1-measure-v4.py:365-369`).

## Run and observed output

```
cd /fast/scratch/hyaku/tameshi-r30a3-seats/RerunC1Head
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
  TMPDIR=/fast/scratch/hyaku/tameshi-r30a3-seats/RerunC1Head/tmp \
  timeout 1500 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/c1-measure-v4.py \
  --repo /fast/scratch/hyaku/tameshi-r30a3-seats/RerunC1Head/c \
  --rev bb681566b18211adf8ae9c28df91e17678e3f545 \
  --sealed /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/v4/c1-sealed.json \
  --jobs 4 > head.rerun.stdout 2> head.rerun.stderr; echo "EXIT=$?"
```

Observed (stdout captured at `/fast/scratch/hyaku/tameshi-r30a3-seats/RerunC1Head/head.rerun.stdout`, 60 lines, 3644 bytes; stderr empty):

```
C1_R30: rev=bb681566b18211adf8ae9c28df91e17678e3f545 pristine_selftest=1 harness=19/19 refused_drops=9/9 killed=13/13 equiv_pass=4/4 heldout_killed=12/12 heldout_equiv=4/4 insert_killed=8/8 insert_equiv=4/4 sealed_block_match=1 sealed_killed=6/6 sealed_equiv=6/6
PREDICATE: C1_R30_PASS=true
```
Process exit: `EXIT=0`.

## Comparison with v4/head.stdout

```
diff -u /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/v4/head.stdout head.rerun.stdout
```
Observed: a single hunk removing only the final line `exit=0` from the reference. All 38 `C1_R30_ROW:` lines, the `C1_R30:` summary line (`v4/head.stdout:59`) and `PREDICATE: C1_R30_PASS=true` (`v4/head.stdout:60`) are identical in content and order; the 59 counter-emitted lines match byte for byte. The reference's extra line is outside the counter's own print set (`c1-measure-v4.py` prints rows, the summary and the predicate, then returns 0/1 at lines 419-427), consistent with the producer's shell appending it; my wrapper recorded the same value as `EXIT=0`. File sha256 differ only through that line: reference `d818af0b3e3e45c5886fc077f7fd7429fee4ebedf83b532352965faf028a786b`, re-run `77bc19b8667a9860cae8988297ea44cc2ad0b261e419e6953a4e4f5ac55f19cb`.

## Environment, custody, cleanup

- `bwrap --version` → `bubblewrap 0.13.1`; `python3 --version` → `Python 3.14.8`. No tools installed or upgraded.
- Counter archive/sandbox path exercised as designed: `git archive` (line 365), bwrap with `--unshare-all`/`--clearenv` (lines 321-327), 4 workers (line 419), per-run copy of `tools/` under the scratch `TMPDIR` (lines 330-339).
- Sealed items were never printed, quoted or read into this report; the report records only the counter's aggregate `sealed_*` tallies.
- Cleanup: scratch `tmp/` is empty after the run; `TMPDIR` was confined to my own scratch dir. `pgrep -x bwrap` showed 8 live bwrap processes whose `/proc/<pid>/cwd` is `/fast/scratch/hyaku/tameshi-r30a3-seats/MutateHead/c` and `/w` — a sibling seat's run, not mine; none were killed. No process of mine remains.
- Read-only git only (`GIT_OPTIONAL_LOCKS=0`); no jj invoked; nothing written under the lane repo except this report.

## Risks and limits

- One host, one bwrap/python version, one run. This re-run confirms operability of the receipt, not its behaviour on other hosts.
- C1's claim itself remains exploratory per the context; this report is supporting evidence only and makes no promotion or score claim.
- Reference `head.stdout` carries the wrapper's `exit=0` line; anyone re-diffing must account for that one-line convention, otherwise a strict byte diff reports a spurious difference (as it did here).
- Lane commit `9207f226e177c8a1a9a82de677df3cd9f8d1cda3` is 2 commits after the content revision (it descends from `bb681566…`), so the content revision I measured is the ancestor the context names.

## Smallest safe correction

None required. If the receipt set is later re-diffed strictly, the only suggested hygiene is to keep the wrapper's `exit=` line out of `head.stdout` or document it as wrapper-appended, so byte-identical stdout comparison does not need this report as the explanation.

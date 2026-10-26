# T48A2ExecEnvDiffPair — live controlled pair for QUALITY criterion 96 (`hermetic env-differential probe`)

Seat: T48A2ExecEnvDiffPair (round 48, a2w1). Attacks: `corpus/QUALITY.md:1420-1426`
(criterion 96) and its falsifier block 96 of `.ufo/evidence/round-48/quality/falsifiers.sh:36-42`,
which rest on the claim that P1's `2/9` is caused by the directory holding P1's PATH shim.
Read-only on the lane; the only file written is this report. Scratch
`/fast/scratch/hyaku/tameshi-r48/T48A2ExecEnvDiffPair` and `/tmp/t48a2.e96np5ab` deleted at exit
(verified: both absent, `ls -d /tmp/t48a2.*` → 0). Disk guard checked before the pass and after:
`/tmp` 125.2 G free, `/fast` 614 G free. No tool installed or upgraded.

## 1. Verdict

**The pair reproduces live, deterministically, with the shim's parent directory as the only moved
variable.** Same revision (`c7586b9a10effc63b4bd327f976edc094c1bdc17`), same command
(`python3 tools/env-diff.py --selftest`), same cwd (a `git clone -q --shared` of the lane at that
revision), same P1 environment key set and byte-identical shim contents:

| PATH shim location | `ENVDIFF_SELFTEST:` line | exit | observed |
|---|---|---|---|
| `/tmp/t48a2.e96np5ab/shim` | `ENVDIFF_SELFTEST: 2/9 pass` | 1 | 2/2 reps identical |
| `/fast/scratch/hyaku/tameshi-r48/T48A2ExecEnvDiffPair/shim` | `ENVDIFF_SELFTEST: 9/9 pass` | 0 | 2/2 reps identical |
| `/tmp/…/shim` + HOME/TMPDIR also under `/tmp/…` (faithful round-47 freeze P1) | `ENVDIFF_SELFTEST: 2/9 pass` | 1 | 1/1 |

So criterion 96's falsifier premise is **not vacuous**: a `/tmp`-held shim flips P1 from `9/9|0` to
`2/9|1` while every other input is fixed. With the same shim bytes and `bwrap` present in both,
`tools/env-diff.py`'s `--tmpfs /tmp` (`tools/env-diff.py:69`) is the only mechanism that can move
the value — confirmed by direct probe (§4).

## 2. What was held fixed

- Revision: clone `HEAD` = `c7586b9a10effc63b4bd327f976edc094c1bdc17` (`git -C clone rev-parse HEAD`).
- Instrument: `tools/env-diff.py` blob `3a48aeccc55bc5ea4c6f436444f5a9ec69c83621`, sha256
  `e8b47ab7cf2323764d9e9d3519352cd75e1abda4d5e98e7df602dc23bc099ead` — identical at `c7586b9a`,
  at lane `HEAD` and at base `473336d9`, and equal to the `e8b47ab7cf23` prefix round 47 recorded
  (`.ufo/evidence/round-47/before/c1-at-freeze.stdout:18` region, `STATEMENT cap/hermetic
  env-differential probe: … |e8b47ab7cf23`).
- Environment: `env -i` semantics with exactly P1's key set
  (`HOME`, `TMPDIR`, `LANG=C`, `LC_ALL=C`, `TZ=UTC`, `PYTHONDONTWRITEBYTECODE=1`, `REV=<rev>`),
  same `HOME`/`TMPDIR` (`$S/home`, `$S/tmp`) for the two headline runs; only `PATH` moves.
- Shim construction: exact port of
  `.ufo/evidence/round-47/calibration/measure.py:156-172` `build_shim` — symlink every name in
  `/usr/bin`, then `node`, `jj`, `jq` via `shutil.which`. Both shims: 3755 entries, identical
  `name -> target` listings (`sha256` prefix `38bcffb670579eff`), including `bash`, `bwrap`,
  `node`, `python3`, `git`, `jj`, `jq`. `/tmp` side total 148 KiB (well under the 50 MB cap).
- Command and cwd: `python3 tools/env-diff.py --selftest` executed with `cwd=<clone>`, `python3`
  resolved through the shim itself (as the counter's `argv` does under P1).

## 3. Receipts (verbatim, one case per line)

`A` = shim under `/tmp/t48a2.e96np5ab` (reps 1 and 2 byte-identical):

```
ENVDIFF_CASE invariant FAIL
ENVDIFF_CASE tz FAIL
ENVDIFF_CASE locale FAIL
ENVDIFF_CASE home FAIL
ENVDIFF_CASE columns FAIL
ENVDIFF_CASE repeat FAIL
ENVDIFF_CASE missing-bwrap PASS
ENVDIFF_CASE timeout FAIL
ENVDIFF_CASE pin-mismatch-public-cli PASS
ENVDIFF_SELFTEST: 2/9 pass
exit=1
```

`B` = shim under `$S` (reps 1 and 2 byte-identical):

```
ENVDIFF_CASE invariant PASS
ENVDIFF_CASE tz PASS
ENVDIFF_CASE locale PASS
ENVDIFF_CASE home PASS
ENVDIFF_CASE columns PASS
ENVDIFF_CASE repeat PASS
ENVDIFF_CASE missing-bwrap PASS
ENVDIFF_CASE timeout PASS
ENVDIFF_CASE pin-mismatch-public-cli PASS
ENVDIFF_SELFTEST: 9/9 pass
exit=0
```

`C` (faithful freeze-P1: shim, HOME, TMPDIR all under the `/tmp` work dir) printed A's nine case
lines and `ENVDIFF_SELFTEST: 2/9 pass`, `exit=1`. Moving HOME/TMPDIR with the work dir changes
nothing — env-diff overrides both inside its sandbox (`tools/env-diff.py:44-45`), so the shim's
parent directory is the operative variable, exactly as the criterion states.

Survivors under the masked shim are the two cases that need no working sandbox:
`missing-bwrap` (`tools/env-diff.py:161-162`) and `pin-mismatch-public-cli`
(`tools/env-diff.py:165-192`, a host-side child). This matches the archived `2/9` case pattern.

## 4. Mechanism observed, not inferred

Same bwrap argv env-diff builds (`tools/env-diff.py:68-71`), run with each PATH:

```
--- bwrap probe PATH=/tmp/t48a2.e96np5ab/shim exit=1
    out=''   err='bwrap: execvp bash: No such file or directory'
--- bwrap probe PATH=/fast/scratch/hyaku/tameshi-r48/T48A2ExecEnvDiffPair/shim exit=0
    out='sandbox-bash-ok\nshim-visible'   err=''
--- mask check (PATH=/tmp shim, /bin/sh inside sandbox) exit=0
    out='---\ntmpd-masked'  err='/bin/sh: line 1: ls: command not found\n/bin/sh: line 1: head: command not found'
```

`--tmpfs /tmp` replaces `/tmp` before `execvp`, so a shim below `/tmp` is gone inside the sandbox;
the same shim outside `/tmp` survives `--ro-bind / /` and resolves `bash` through its symlink.
That is the whole difference between the two receipts above.

## 5. Corroboration of the archived pair the falsifier reads

The falsifier reads two round-47 receipts whose P1 tuples differ:

- `.ufo/evidence/round-47/before/c1-at-freeze.stdout:18` (`--work` under `/tmp`):
  `P1=ENVDIFF_SELFTEST: 2/9 pass|1`
- `.ufo/evidence/round-47/after/c1.stdout:18` (`--work /var/tmp`):
  `P1=ENVDIFF_SELFTEST: 9/9 pass|0`

My live values are exactly those tuples, derived without the round-47 counter and without its
`--work`: `2/9|1` and `9/9|0`. The archived difference is therefore a real, reproducible effect of
the work-dir/shim placement, not a stale or mis-transcribed receipt.

## 6. Limits, and what this does not decide

- A probe is never a verdict: this pair re-derives the *mechanism* behind criterion 96's falsifier;
  it does not score C1, does not run the deciding invocation, and does not edit `contract.json`,
  the counters or the receipts.
- `2/9` alone is ambiguous between "bwrap absent" (P2, `tools/env-diff.py:58-60`) and "shim masked".
  Here the ambiguity is closed for this pair only because both shims carry identical listings and
  `bwrap` is present in both; the printed number still cannot self-describe, which is a property of
  the instrument, not of this pair (already recorded in `.ufo/waves/round-48/w1/T48RevenEnvDiff.md`
  §1.3, §3.6).
- The round-48 counter refuses `--work` under `/tmp`
  (`.ufo/evidence/round-48/calibration/measure.py:101-103,395-396`, selftest
  `T63_work_under_tmp_refused` at `:836,869-872`), so the defect the pair demonstrates cannot be
  scored through the round-48 C1 counter; the pair had to be built by hand as it was.
- Host load was not varied and is not needed: the `/tmp` side fails in milliseconds at `execvp`,
  before any interpreter runs.
- No finding against the lane: nothing here contradicts criterion 96's wording, the falsifier's
  premise, or the round-48 `under_tmp` refusal. If anything, the pair strengthens the falsifier,
  whose archived inputs are two counter runs rather than a one-variable pair; a stricter block could
  use shim placement directly. That is an observation for the L1, not a change I make.

## 7. Files changed

- `.ufo/waves/round-48/a2w1/T48A2ExecEnvDiffPair.md` (this report only).
- Lane worktree otherwise untouched: `git status --porcelain` shows only the pre-existing untracked
  `.ufo/waves/round-48/a2w1/`; `corpus/`, `tools/` and `SCORECARD.md` not written. No git mutating
  command, no jj command, no pacman transaction, no install.

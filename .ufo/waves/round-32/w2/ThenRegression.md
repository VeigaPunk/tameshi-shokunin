# ThenRegression — tool run-time mode vs plain runner

**Verdict: PASS.** The frozen tool's run-time mode (`--then-regression`) and the plain runner produce the same regression verdict on the same bytes. The tool printed `TALLY_AUDIT: PASS`, the runner printed `REGRESSION: PASS (cases=9 passed=9; …)`, the tool printed `TALLY_AUDIT_REGRESSION: PASS (cases=9 legs=9 exit=0)`, and the tool exited **0**. Every one of the nine legs passed in both runs, with byte-identical `REGRESSION_CASE`/`REGRESSION_SWEEP`/`REGRESSION_TABLE` lines. The runner stayed byte-identical at the pinned sha256.

Axes: operability of the tool's run-time mode, agreement between the tool and the runner, and absence of drift in the audited runner.

## Environment

- Clone: `/fast/scratch/hyaku/tameshi-r32-seats/ThenRegression/c`, detached at `a4f718138bdad20de741faeca57891645e5a64d9` (`git log --oneline -1` → `a4f7181 round-32: content revision — …`). Working tree clean (`git status --porcelain` empty).
- Tool sha256 in the clone: `9639c458002ce2f954addbe047427010ae011353e073b293396bec800fa699ef` (matches the frozen tool `9639c458…99ef`).
- Runner sha256 in the clone: `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` (matches the pinned runner `a7d3f2dd…2eb9`).
- The lane copies of both files are byte-identical to the clone copies (`diff` → no output for each).
- Host tools used, all pre-installed: `python3` 3.14.8, `bash` 5.3.20, `node` v24.21.0, `git`. **No tool was installed or updated by this seat.**
- All execution stayed under `/fast/scratch/hyaku/tameshi-r32-seats/ThenRegression/`. No production file was edited, no `jj` command was run anywhere, no git write command was run in the lane or the fleet root, and the lane working tree and index were not touched by this seat (the only lane modification visible in `git status` is `.ufo/waves/round-32/w2/swarm-registry.json`, written by the swarm registry, not by me).

### One setup fact that the run depends on

`tools/mutate-and-run.sh:1358` derives the fleet root from the runner's own path:

```bash
FLEET_ROOT=$(dirname "$(dirname "$(dirname "$SELF")")")
```

`SELF` is `readlink -f "${BASH_SOURCE[0]}"` (`tools/mutate-and-run.sh:178`). In the real lane checkout that resolves to `/home/vgpnk/Projects/shokunin`, which already holds the four sibling repos (`kumitate-shokunin`, `kagi-shokunin`, `tsukuroi-shokunin`, `mado-shokunin`). In a scratch clone the runner sits one level deeper (`…/ThenRegression/c/tools/mutate-and-run.sh`), so `FLEET_ROOT` resolves to `…/ThenRegression/`, which has no sibling repos. Without them, all nine legs refuse:

```text
REGRESSION_CASE js-kimi-census: SETUP (repo_identity_mismatch: /fast/scratch/hyaku/tameshi-r32-seats/ThenRegression/kumitate-shokunin is not its own repository; toplevel=unresolved)
…
REGRESSION: SETUP (cases=9 passed=0 cannot-verify=9)
TALLY_AUDIT_REGRESSION: SETUP (cases=9 legs=9 exit=2)
```

(tool exit **2**, `TALLY_AUDIT: PASS` still printed for the audit phase). I therefore created read-only symlinks in the seat root so the scratch clone reproduces the lane's fleet layout:

```sh
cd /fast/scratch/hyaku/tameshi-r32-seats/ThenRegression
ln -sfn /home/vgpnk/Projects/shokunin/kumitate-shokunin kumitate-shokunin
ln -sfn /home/vgpnk/Projects/shokunin/kagi-shokunin      kagi-shokunin
ln -sfn /home/vgpnk/Projects/shokunin/tsukuroi-shokunin  tsukuroi-shokunin
ln -sfn /home/vgpnk/Projects/shokunin/mado-shokunin      mado-shokunin
```

The r17 repo-identity guard (`tools/mutate-and-run.sh:1180-1194`) compares `realpath` of the repo dir against `realpath` of `git rev-parse --show-toplevel`, so symlinks resolve identically on both sides and the guard passes. Verified directly:

```text
repo_real=/home/vgpnk/Projects/shokunin/kumitate-shokunin repo_top=/home/vgpnk/Projects/shokunin/kumitate-shokunin
IDENTITY_OK
```

All seven pinned revisions used by the nine legs resolve in the sibling object stores (`git cat-file -e <rev>^{commit}` → OK for `175de6ba`, `364f1d59`, `0acb7752`, `1205c662` in kumitate; `fecee874` in kagi; `165307fe` in tsukuroi; `eead56b2` in mado). The symlinks are read-only views; `find <sibling>/.git -newermt "2026-10-23 11:20"` found no writes to any sibling repo during either run.

## Run 1 — the tool's run-time mode

Exact command:

```sh
cd /fast/scratch/hyaku/tameshi-r32-seats/ThenRegression/c && timeout 2700 python3 tools/tally-audit.py --then-regression --workdir /fast/scratch/hyaku/tameshi-r32-seats/ThenRegression/rg-1
```

Observed exit: **0**. Elapsed: **966 s** (the audit phase is a few seconds; the regression sweep dominates, and this run overlapped other seats' regression runs on the same host). Full stdout is 56 lines; the audit phase is the first four:

```text
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=349 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=27/27
TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)
```

Last 30 lines of stdout, verbatim:

```text
REGRESSION_WORKDIR bash-mado-verify: /fast/scratch/hyaku/tameshi-r32-seats/ThenRegression/rg-1/bash-mado-verify
REGRESSION_CASE bash-mado-verify: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION_PIN bash-checklist-run: source=git repo=/fast/scratch/hyaku/tameshi-r32-seats/ThenRegression/kagi-shokunin rev=fecee8743e52eb8fb5fbb40782934cb619a1a96e path=corpus/checklist-run.sh mode=100755 sha256=7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf
REGRESSION_SWEEP bash-checklist-run: MUTATE: DONE (target=bash-checklist-run defects=15 killed=7 survived=8 inconclusive=0 kill-rate=47%)
REGRESSION_TABLE bash-checklist-run: match=15/15 recorded-killed=7 measured-killed=7 survived=8 inconclusive=0 flips=0
REGRESSION_WORKDIR bash-checklist-run: /fast/scratch/hyaku/tameshi-r32-seats/ThenRegression/rg-1/bash-checklist-run
REGRESSION_CASE bash-checklist-run: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=15)
REGRESSION_PIN js-claims-check: source=git repo=/fast/scratch/hyaku/tameshi-r32-seats/ThenRegression/kumitate-shokunin rev=175de6ba2e9e904010411b19cab27e0af9aad3d4 path=scripts/claims-check.mjs mode=100755 sha256=e9a21b441f1216fb41d1cca037b36021c581ec7892df3bf973295f9321b0f61b
REGRESSION_SWEEP js-claims-check: MUTATE: DONE (target=js-claims-check defects=10 killed=7 survived=3 inconclusive=0 kill-rate=70%)
REGRESSION_TABLE js-claims-check: match=10/10 recorded-killed=7 measured-killed=7 survived=3 inconclusive=0 flips=0
REGRESSION_WORKDIR js-claims-check: /fast/scratch/hyaku/tameshi-r32-seats/ThenRegression/rg-1/js-claims-check
REGRESSION_CASE js-claims-check: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION_PIN js-round-gate: source=git repo=/fast/scratch/hyaku/tameshi-r32-seats/ThenRegression/kumitate-shokunin rev=364f1d5954158ef8844bca4a5fef57b05d2f2ca5 path=scripts/round-gate.mjs mode=100755 sha256=f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9
REGRESSION_SWEEP js-round-gate: MUTATE: DONE (target=js-round-gate defects=10 killed=5 survived=5 inconclusive=0 kill-rate=50%)
REGRESSION_TABLE js-round-gate: match=10/10 recorded-killed=5 measured-killed=5 survived=5 inconclusive=0 flips=0
REGRESSION_WORKDIR js-round-gate: /fast/scratch/hyaku/tameshi-r32-seats/ThenRegression/rg-1/js-round-gate
REGRESSION_CASE js-round-gate: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION_PIN js-sources-check: source=git repo=/fast/scratch/hyaku/tameshi-r32-seats/ThenRegression/kumitate-shokunin rev=0acb7752d19058b953ebbeba253b1e35f6548de5 path=scripts/sources-check.mjs mode=100755 sha256=6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f
REGRESSION_SWEEP js-sources-check: MUTATE: DONE (target=js-sources-check defects=10 killed=5 survived=5 inconclusive=0 kill-rate=50%)
REGRESSION_TABLE js-sources-check: match=10/10 recorded-killed=5 measured-killed=5 survived=5 inconclusive=0 flips=0
REGRESSION_WORKDIR js-sources-check: /fast/scratch/hyaku/tameshi-r32-seats/ThenRegression/rg-1/js-sources-check
REGRESSION_CASE js-sources-check: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION_PIN js-cite-check: source=git repo=/fast/scratch/hyaku/tameshi-r32-seats/ThenRegression/kumitate-shokunin rev=1205c6621a2eccbb8ffceae86d9e7b79a7990b3a path=scripts/cite-check.mjs mode=100755 sha256=40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f
REGRESSION_SWEEP js-cite-check: MUTATE: DONE (target=js-cite-check defects=10 killed=5 survived=5 inconclusive=0 kill-rate=50%)
REGRESSION_TABLE js-cite-check: match=10/10 recorded-killed=5 measured-killed=5 survived=5 inconclusive=0 flips=0
REGRESSION_WORKDIR js-cite-check: /fast/scratch/hyaku/tameshi-r32-seats/ThenRegression/rg-1/js-cite-check
REGRESSION_CASE js-cite-check: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)
REGRESSION_WORKDIR: /fast/scratch/hyaku/tameshi-r32-seats/ThenRegression/rg-1 (kept)
TALLY_AUDIT_REGRESSION: PASS (cases=9 legs=9 exit=0)
```

## Run 2 — the plain runner

Exact command:

```sh
cd /fast/scratch/hyaku/tameshi-r32-seats/ThenRegression/c && timeout 2700 bash tools/mutate-and-run.sh --regression --workdir /fast/scratch/hyaku/tameshi-r32-seats/ThenRegression/rg-2
```

Observed exit: **0**. Elapsed: **509 s**. The REGRESSION line is identical to the one the tool's run produced:

```text
REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)
```

Per-leg results, both runs:

| leg | run 1 (via tool) | run 2 (plain runner) |
|---|---|---|
| js-kimi-census | PASS, defects=10 | PASS, defects=10 |
| bash-surface-census | PASS, defects=10 | PASS, defects=10 |
| bash-tsukuroi-census | PASS, defects=10 | PASS, defects=10 |
| bash-mado-verify | PASS, defects=10 | PASS, defects=10 |
| bash-checklist-run | PASS, defects=15 | PASS, defects=15 |
| js-claims-check | PASS, defects=10 | PASS, defects=10 |
| js-round-gate | PASS, defects=10 | PASS, defects=10 |
| js-sources-check | PASS, defects=10 | PASS, defects=10 |
| js-cite-check | PASS, defects=10 | PASS, defects=10 |

Line-by-line comparison of every `REGRESSION_CASE`, `REGRESSION_SWEEP` and `REGRESSION_TABLE` line between the two runs:

```sh
diff <(grep -E "^REGRESSION_(CASE|SWEEP|TABLE)" rg1.log) <(grep -E "^REGRESSION_(CASE|SWEEP|TABLE)" rg2.log)
```

→ no output (identical). The only differences between the two stdout streams are the run-specific paths (`rg-1` vs `rg-2`), the `REGRESSION_DATE` stamp, and the two extra tool-only lines (`CHECK …` / `TALLY_AUDIT: PASS` at the head, `TALLY_AUDIT_REGRESSION: PASS` at the tail).

Both runs pinned the same runner bytes, as reported by the runner itself:

```text
REGRESSION_TOOL: /fast/scratch/hyaku/tameshi-r32-seats/ThenRegression/c/tools/mutate-and-run.sh sha256=a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9
```

## Expected-versus-actual

| expected | observed |
|---|---|
| audit PASS | `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)` (static: 9 legs/9 operands/nlegs=9; runtime: 349 vectors, 0 mismatched; harness: 9 reference cases, 27/27 faults rejected) |
| `REGRESSION: PASS cases=9` | `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)` in both runs |
| `TALLY_AUDIT_REGRESSION: PASS (cases=9 legs=9 exit=0)` | exactly that line |
| tool exit 0 | 0 |

## Smallest safe correction

None is needed for the measured behavior; the tool's run-time mode and the runner agree exactly. Two operability observations, neither of which changes any verdict and neither of which this seat applied:

1. `tools/tally-audit.py:384` runs the runner with `subprocess.run(argv, capture_output=True)` and **no timeout**, unlike the audit's own bash calls, which use `TIMEOUT = 120` (`tools/tally-audit.py:43`). A hung runner would hang the tool indefinitely; the `timeout 2700` in the invocation was the only bound. A minimal, behavior-preserving improvement for a later revision is to pass `timeout=` on that call and report SETUP on expiry, matching the existing `CannotAudit` style.
2. `then_regression` (`tools/tally-audit.py:380-393`) forwards `--workdir` but has no way to point the runner at a different fleet root; `FLEET_ROOT` is fixed by the runner's own path (`tools/mutate-and-run.sh:1358`). A scratch clone therefore needs the four sibling repos at the clone's fleet-root level (symlinks suffice, as shown). This is documented behaviour of the runner, not a defect, but it is the single reason a first attempt in a bare clone returns SETUP rather than PASS.

No production file was modified by this seat.

## Risks and blockers

- **Runtime.** Each `--regression` run is a full nine-leg mutation sweep: 509 s and 966 s observed, both under the 2700 s bound. The variance tracks host load from concurrent seats, not the tool. A measurement host running this under contention should keep a generous timeout.
- **Fleet-root dependency.** Outside the real lane checkout, the run only reproduces the lane verdict when the four sibling repos are reachable at the runner's derived `FLEET_ROOT`. The lane checkout already satisfies this; the sandbox used here needed symlinks.
- **Disk.** Seat footprint after both runs: 178 MB total (clone 170 MB, `rg-1` 7.0 MB, `rg-2` 1.2 MB). `/fast` had 69 GB free after the runs.
- **No blockers.** All requested observations were obtained.

## Process hygiene

Both regression runs completed and were awaited; no background service was left running. `ps -eo pid,etime,args | grep -E "tally-audit|mutate-and-run"` after the runs shows only processes belonging to the separate seat `HeldOutRefactor` (`/fast/scratch/hyaku/tameshi-r32-seats/HeldOutRefactor/…`); none of this seat's processes remain, and none of another seat's processes were signalled. Scratch artifacts retained: `rg1.log`, `rg2.log`, `rg-1/`, `rg-2/` under `/fast/scratch/hyaku/tameshi-r32-seats/ThenRegression/`, plus the read-only sibling symlinks in the seat root.

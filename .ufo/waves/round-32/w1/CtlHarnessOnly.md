# CtlHarnessOnly — pre-data C1 control

## Verdict

**Expected negative control: `C1_R32_PASS=false`, exit 1.** The unchanged frozen counter observed `kill=10/18 accept=8/8 other=8 runner_sha_ok=1 tool_present=1`. This harness-only partial implementation did not meet C1. There is no control-meets-counter finding and no change to the contract or counter.

**Assigned axis: operability.** Probe dimensions: runnable harness discrimination and exact-byte restoration. No other axis or production capability is claimed.

Sandbox control commit: `7f5cc74fb6d0eb7633ed4884d6e2fe00718bbcf4`, one commit on `c31814978969a41a8e9b0f7d99fa308c5993c1b7`. Tool SHA-256: `1a1e1da7d24ca3eaa0773dfe8d76d9ffad850407ea1737d96ae9e03e21ce0f24`.

The single supplemental runner mutation H03 was **killed** by the same bounded control invocation on pristine, mutated, and restored bytes: exits **0, 1, 0**. Restoration was byte-exact and the complete restored stdout/stderr/exit matched pristine.

## Evidence and scope

- Contract: `.ufo/evidence/round-32/contract.json:12-35` specifies the three checks, 18 must-kill and 8 must-accept copies, frozen predicate, and negative controls.
- Counter: `.ufo/evidence/round-32/c1-measure.py:82-168,177-196,245-277` constructs the copies, invokes the committed tool, classifies its exit/output, and computes the frozen predicate.
- Construction source: `.ufo/waves/round-30/wC/MutateHead.md:160-220`, especially the six known-faulty tally blocks at lines 213-219.
- Pinned runner: `tools/mutate-and-run.sh:1432-1470` is the pristine fixture; `:1992-2040` is the supplied harness section executed by this control; `:2006` is the isolated H03 mutation point.
- Control implementation in the sandbox: `tools/tally-audit.py:17-55` contains the independent pristine tally fixture; `:59-76` constructs its six faults; `:79-108` wraps the extracted harness in a Bash function with its own `st` accounting; `:111-148` extracts the harness and applies only the panel verdict.

Each tool invocation extracts the supplied runner section from `  local tblock ` through `  tblock=$tblock_full`. Its original tally extraction runs, then the independent fixture is injected immediately afterward, as in the supplemental recipe. The harness, its own name extraction, comparisons, and vectors remain the supplied runner's code. Separate runs inject pristine, H03 bad output labels, H04 dropped final operand, H05 final-leg normalization, N01 SETUP-before-FAIL, N02 deleted completeness guard, and N03 FAIL exiting 0. The tool FAILs only when the harness rejects pristine or accepts a known fault; inability to extract or execute returns 2. It performs no separate static per-leg audit and no independent runtime tally oracle.

The pristine fixture is deliberately independent of the supplied runner's runtime tally: this is a harness-only control, not a runtime-only control in disguise.

### Exact setup and commit commands

Initial directory creation returned exit 0 with no output:

```sh
mkdir -p /fast/scratch/hyaku/tameshi-r32-seats/CtlHarnessOnly
```

Subsequent commands ran only under `/fast/scratch/hyaku/tameshi-r32-seats/CtlHarnessOnly/`. Clone and checkout returned exit 0 with empty stdout/stderr:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r32-seats/CtlHarnessOnly/lane && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlHarnessOnly/lane checkout -q --detach c31814978969a41a8e9b0f7d99fa308c5993c1b7
```

```sh
df -h /fast
```

Observed exit 0:

```text
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme1n1p2  804G  702G  102G  88% /fast
```

Only the new control tool was added and committed. This exact command returned exit 0:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlHarnessOnly/lane add tools/tally-audit.py && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlHarnessOnly/lane -c user.name=ctl -c user.email=ctl@sandbox commit -qm CtlHarnessOnly && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlHarnessOnly/lane rev-parse HEAD
```

Observed stdout:

```text
7f5cc74fb6d0eb7633ed4884d6e2fe00718bbcf4
```

### Frozen counter invocation and complete stdout

Working directory: `/fast/scratch/hyaku/tameshi-r32-seats/CtlHarnessOnly`. Git location variables were removed from the subprocess environment. The work path was absent before this first and only counter run; no seed was supplied.

```sh
timeout 2400 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r32-seats/CtlHarnessOnly/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r32-seats/CtlHarnessOnly/w-CtlHarnessOnly
```

**Observed exit: 1. Stderr: empty. Full stdout, verbatim:**

```text
COPY set=kill id=T08 outcome=ACCEPT exit=0 sha256=12ad1d9076a55050 last='TALLY_AUDIT: PASS harness panel only'
COPY set=kill id=N05 outcome=ACCEPT exit=0 sha256=e1ef181c1e621962 last='TALLY_AUDIT: PASS harness panel only'
COPY set=kill id=H03 outcome=KILL exit=1 sha256=2ac4ce5344e6100a last='TALLY_AUDIT: FAIL harness accepted H03'
COPY set=kill id=H04 outcome=KILL exit=1 sha256=0dc1e6b07452f610 last='TALLY_AUDIT: FAIL harness accepted H03; harness accepted H04; harness accepted H05; harness accepted N01; harness accepted N02; harness accepted N03'
COPY set=kill id=H05 outcome=KILL exit=1 sha256=adf6763d6524f342 last='TALLY_AUDIT: FAIL harness accepted H05'
COPY set=kill id=N01 outcome=KILL exit=1 sha256=c0a32ec4e69d3cb0 last='TALLY_AUDIT: FAIL harness accepted N01'
COPY set=kill id=N02 outcome=KILL exit=1 sha256=31128639afc3e57a last='TALLY_AUDIT: FAIL harness accepted N02'
COPY set=kill id=N03 outcome=KILL exit=1 sha256=741907e82ca7e907 last='TALLY_AUDIT: FAIL harness accepted H03; harness accepted N03'
COPY set=kill id=D01 outcome=ACCEPT exit=0 sha256=71a66c5a611d408f last='TALLY_AUDIT: PASS harness panel only'
COPY set=kill id=gT08(arm=131) outcome=ACCEPT exit=0 sha256=390a3a23393bc509 last='TALLY_AUDIT: PASS harness panel only'
COPY set=kill id=gN05(< nlegs) outcome=ACCEPT exit=0 sha256=e1ef181c1e621962 last='TALLY_AUDIT: PASS harness panel only'
COPY set=kill id=gH03(form=2) outcome=KILL exit=1 sha256=7f1787411f0ff16c last='TALLY_AUDIT: FAIL harness accepted H03'
COPY set=kill id=gH04(:) outcome=KILL exit=1 sha256=fba8e1cf3e1bfd8b last='TALLY_AUDIT: FAIL harness accepted H03; harness accepted H04; harness accepted H05; harness accepted N01; harness accepted N02; harness accepted N03'
COPY set=kill id=gH05(drop=7,dup=8) outcome=ACCEPT exit=0 sha256=1323298d01e6e2e5 last='TALLY_AUDIT: PASS harness panel only'
COPY set=kill id=gN01(vector=1) outcome=ACCEPT exit=0 sha256=ebf4a902638d568e last='TALLY_AUDIT: PASS harness panel only'
COPY set=kill id=gN02(or) outcome=KILL exit=1 sha256=31128639afc3e57a last='TALLY_AUDIT: FAIL harness accepted N02'
COPY set=kill id=gN03(split) outcome=KILL exit=1 sha256=16566843890d60ab last='TALLY_AUDIT: FAIL harness accepted H03; harness accepted N03'
COPY set=kill id=gD01(drop=st_checklist,dup=st_sourcescheck) outcome=ACCEPT exit=0 sha256=a956d2fcf838b8cf last='TALLY_AUDIT: PASS harness panel only'
COPY set=accept id=B0-pristine outcome=ACCEPT exit=0 sha256=a7d3f2dd7d47511a last='TALLY_AUDIT: PASS harness panel only'
COPY set=accept id=B1-T07 outcome=ACCEPT exit=0 sha256=91066af826f69ecb last='TALLY_AUDIT: PASS harness panel only'
COPY set=accept id=B2-reversed outcome=ACCEPT exit=0 sha256=7d3d5a5f34fe3595 last='TALLY_AUDIT: PASS harness panel only'
COPY set=accept id=B3-decoys outcome=ACCEPT exit=0 sha256=7c76617e87c11c49 last='TALLY_AUDIT: PASS harness panel only'
COPY set=accept id=B4-cosmetic outcome=ACCEPT exit=0 sha256=137a7ba8a58c5277 last='TALLY_AUDIT: PASS harness panel only'
COPY set=accept id=B5-renamed outcome=ACCEPT exit=0 sha256=f66fe32a4ea7ce76 last='TALLY_AUDIT: PASS harness panel only'
COPY set=accept id=gB6-permuted outcome=ACCEPT exit=0 sha256=b05779b81fdf4753 last='TALLY_AUDIT: PASS harness panel only'
COPY set=accept id=gB7-nonce outcome=ACCEPT exit=0 sha256=948dbb17e5e90aa0 last='TALLY_AUDIT: PASS harness panel only'
C1_R32: kill=10/18 accept=8/8 other=8 runner_sha_ok=1 tool_present=1 seed=4d4c58985d695831 rev=7f5cc74fb6d0eb7633ed4884d6e2fe00718bbcf4 C1_R32_PASS=false
```

Unabridged receipts:

- `/fast/scratch/hyaku/tameshi-r32-seats/CtlHarnessOnly/counter.stdout`
- `/fast/scratch/hyaku/tameshi-r32-seats/CtlHarnessOnly/counter.stderr`
- `/fast/scratch/hyaku/tameshi-r32-seats/CtlHarnessOnly/counter.exit`

### Which copies it classified correctly and missed

Correct must-kill classifications: frozen H03, H04, H05, N01, N02, N03; generated `gH03(form=2)`, `gH04(:)`, `gN02(or)`, `gN03(split)`. All eight must-accept copies were accepted.

Surviving must-kill copies: T08, N05, D01, `gT08(arm=131)`, `gN05(< nlegs)`, `gH05(drop=7,dup=8)`, `gN01(vector=1)`, and `gD01(drop=st_checklist,dup=st_sourcescheck)`.

The six runtime/operand survivors leave the harness unchanged, and this control injects an independent pristine tally rather than auditing their runtime tally. The generated H05 copy drops position 7, while the one H05 fault in this assigned panel normalizes position 8; the harness still rejects that fault. The generated N01 copy deletes the two-setup vector, while this panel's N01 fault specifically exposes missing mixed-status precedence coverage; the mixed vector is still present and rejects that fault. Those are scoped coverage limitations, not reasons to amend or expand this negative control.

## Single mutation probe and restoration evidence

Mutant: change only `probe/runner.sh:2006` from

```bash
    [[ $rc -eq $want_rc && "${out%%$'\n'*}" == "$want_line" ]]
```

to

```bash
    [[ $rc -eq $want_rc ]]
```

The fixture was copied from the pinned sandbox runner, and the comparison edit and its inverse were applied surgically. The clone's runner was never edited.

Expected detector: pristine harness accepts the pristine fixture but rejects every fault; H03's exit-only comparison accepts the bad-label fault, so the audit must exit 1 with `TALLY_AUDIT: FAIL harness accepted H03`. After restoring the exact original comparison, the audit must return to its pristine result.

The same command ran in all three phases, from the seat directory, with `TMPDIR=/fast/scratch/hyaku/tameshi-r32-seats/CtlHarnessOnly/probe/tmp` and the three Git location variables removed:

```sh
timeout 90 python3 /fast/scratch/hyaku/tameshi-r32-seats/CtlHarnessOnly/lane/tools/tally-audit.py --runner /fast/scratch/hyaku/tameshi-r32-seats/CtlHarnessOnly/probe/runner.sh
```

The Python caller used `subprocess.run(..., capture_output=True, text=True, timeout=100)`. Each panel member was itself bounded by `timeout 20 bash --noprofile --norc -s -- ROOT` and a 25-second Python timeout. No invocation timed out.

| Phase | SHA-256 immediately before | SHA-256 immediately after | Detector exit |
| --- | --- | --- | --- |
| Pristine | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | 0 |
| H03 mutated | `2ac4ce5344e6100a5980a2d44bbc4983562df5a0325ecf84610973094322f35c` | `2ac4ce5344e6100a5980a2d44bbc4983562df5a0325ecf84610973094322f35c` | 1 |
| Restored | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | 0 |

Observed exact comparisons: `restored_bytes == pristine_bytes` was **true**; restored complete `(exit, stdout, stderr)` equaled pristine **true**. Verdict: **KILLED**, not inconclusive; the baseline succeeded.

All actual probe output follows. Machine-readable records are at `/fast/scratch/hyaku/tameshi-r32-seats/CtlHarnessOnly/probe/{pristine,mutated-H03,restored}.json`.

### pristine

Exit: `0`. Stderr: empty.

```text
PANEL id=pristine exit=0
HARNESS_RESULT: 9/9 pass
PANEL id=H03 exit=1
HARNESS_CHECK: FAIL tally harness: all nine legs pass -> PASS passed=9, exit 0
HARNESS_CHECK: FAIL tally harness: one leg status 1 at each of 9 positions -> REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0) (0/9)
HARNESS_CHECK: FAIL tally harness: one leg status 2 at each of 9 positions -> REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1) (0/9)
HARNESS_CHECK: FAIL tally harness: statuses 1 1 0 0 0 0 0 0 0 -> REGRESSION: FAIL (cases=9 passed=7 failed=2 setup=0)
HARNESS_CHECK: FAIL tally harness: statuses 2 2 0 0 0 0 0 0 0 -> REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)
HARNESS_CHECK: FAIL tally harness: statuses 1 2 0 0 0 0 0 0 0 -> REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)
HARNESS_CHECK: FAIL tally harness: statuses 3 0 0 0 0 0 0 0 0 -> REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)
HARNESS_RESULT: 2/9 pass
PANEL id=H04 exit=1
HARNESS_CHECK: FAIL tally harness: all nine legs pass -> PASS passed=9, exit 0
HARNESS_CHECK: FAIL tally harness: one leg status 1 at each of 9 positions -> REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0) (0/9)
HARNESS_CHECK: FAIL tally harness: one leg status 2 at each of 9 positions -> REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1) (0/9)
HARNESS_CHECK: FAIL tally harness: statuses 1 1 0 0 0 0 0 0 0 -> REGRESSION: FAIL (cases=9 passed=7 failed=2 setup=0)
HARNESS_CHECK: FAIL tally harness: statuses 2 2 0 0 0 0 0 0 0 -> REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)
HARNESS_CHECK: FAIL tally harness: statuses 1 2 0 0 0 0 0 0 0 -> REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)
HARNESS_CHECK: FAIL tally harness: statuses 3 0 0 0 0 0 0 0 0 -> REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)
HARNESS_CHECK: FAIL tally harness: loop missing one operand -> SETUP case-tally mismatch, exit 2
HARNESS_RESULT: 1/9 pass
PANEL id=H05 exit=1
HARNESS_CHECK: FAIL tally harness: one leg status 1 at each of 9 positions -> REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0) (8/9)
HARNESS_CHECK: FAIL tally harness: one leg status 2 at each of 9 positions -> REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1) (8/9)
HARNESS_RESULT: 7/9 pass
PANEL id=N01 exit=1
HARNESS_CHECK: FAIL tally harness: statuses 1 2 0 0 0 0 0 0 0 -> REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)
HARNESS_RESULT: 8/9 pass
PANEL id=N02 exit=1
HARNESS_CHECK: FAIL tally harness: loop missing one operand -> SETUP case-tally mismatch, exit 2
HARNESS_RESULT: 8/9 pass
PANEL id=N03 exit=1
HARNESS_CHECK: FAIL tally harness: one leg status 1 at each of 9 positions -> REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0) (0/9)
HARNESS_CHECK: FAIL tally harness: statuses 1 1 0 0 0 0 0 0 0 -> REGRESSION: FAIL (cases=9 passed=7 failed=2 setup=0)
HARNESS_CHECK: FAIL tally harness: statuses 1 2 0 0 0 0 0 0 0 -> REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)
HARNESS_RESULT: 6/9 pass
TALLY_AUDIT: PASS harness panel only
```

### mutated-H03

Exit: `1`. Stderr: empty.

```text
PANEL id=pristine exit=0
HARNESS_RESULT: 9/9 pass
PANEL id=H03 exit=0
HARNESS_RESULT: 9/9 pass
PANEL id=H04 exit=1
HARNESS_CHECK: FAIL tally harness: all nine legs pass -> PASS passed=9, exit 0
HARNESS_CHECK: FAIL tally harness: one leg status 1 at each of 9 positions -> REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0) (8/9)
HARNESS_RESULT: 7/9 pass
PANEL id=H05 exit=1
HARNESS_CHECK: FAIL tally harness: one leg status 1 at each of 9 positions -> REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0) (8/9)
HARNESS_CHECK: FAIL tally harness: one leg status 2 at each of 9 positions -> REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1) (8/9)
HARNESS_RESULT: 7/9 pass
PANEL id=N01 exit=1
HARNESS_CHECK: FAIL tally harness: statuses 1 2 0 0 0 0 0 0 0 -> REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)
HARNESS_RESULT: 8/9 pass
PANEL id=N02 exit=1
HARNESS_CHECK: FAIL tally harness: loop missing one operand -> SETUP case-tally mismatch, exit 2
HARNESS_RESULT: 8/9 pass
PANEL id=N03 exit=1
HARNESS_CHECK: FAIL tally harness: one leg status 1 at each of 9 positions -> REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0) (0/9)
HARNESS_CHECK: FAIL tally harness: statuses 1 1 0 0 0 0 0 0 0 -> REGRESSION: FAIL (cases=9 passed=7 failed=2 setup=0)
HARNESS_CHECK: FAIL tally harness: statuses 1 2 0 0 0 0 0 0 0 -> REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)
HARNESS_RESULT: 6/9 pass
TALLY_AUDIT: FAIL harness accepted H03
```

### restored

Exit: `0`. Stderr: empty.

```text
PANEL id=pristine exit=0
HARNESS_RESULT: 9/9 pass
PANEL id=H03 exit=1
HARNESS_CHECK: FAIL tally harness: all nine legs pass -> PASS passed=9, exit 0
HARNESS_CHECK: FAIL tally harness: one leg status 1 at each of 9 positions -> REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0) (0/9)
HARNESS_CHECK: FAIL tally harness: one leg status 2 at each of 9 positions -> REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1) (0/9)
HARNESS_CHECK: FAIL tally harness: statuses 1 1 0 0 0 0 0 0 0 -> REGRESSION: FAIL (cases=9 passed=7 failed=2 setup=0)
HARNESS_CHECK: FAIL tally harness: statuses 2 2 0 0 0 0 0 0 0 -> REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)
HARNESS_CHECK: FAIL tally harness: statuses 1 2 0 0 0 0 0 0 0 -> REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)
HARNESS_CHECK: FAIL tally harness: statuses 3 0 0 0 0 0 0 0 0 -> REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)
HARNESS_RESULT: 2/9 pass
PANEL id=H04 exit=1
HARNESS_CHECK: FAIL tally harness: all nine legs pass -> PASS passed=9, exit 0
HARNESS_CHECK: FAIL tally harness: one leg status 1 at each of 9 positions -> REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0) (0/9)
HARNESS_CHECK: FAIL tally harness: one leg status 2 at each of 9 positions -> REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1) (0/9)
HARNESS_CHECK: FAIL tally harness: statuses 1 1 0 0 0 0 0 0 0 -> REGRESSION: FAIL (cases=9 passed=7 failed=2 setup=0)
HARNESS_CHECK: FAIL tally harness: statuses 2 2 0 0 0 0 0 0 0 -> REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)
HARNESS_CHECK: FAIL tally harness: statuses 1 2 0 0 0 0 0 0 0 -> REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)
HARNESS_CHECK: FAIL tally harness: statuses 3 0 0 0 0 0 0 0 0 -> REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)
HARNESS_CHECK: FAIL tally harness: loop missing one operand -> SETUP case-tally mismatch, exit 2
HARNESS_RESULT: 1/9 pass
PANEL id=H05 exit=1
HARNESS_CHECK: FAIL tally harness: one leg status 1 at each of 9 positions -> REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0) (8/9)
HARNESS_CHECK: FAIL tally harness: one leg status 2 at each of 9 positions -> REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1) (8/9)
HARNESS_RESULT: 7/9 pass
PANEL id=N01 exit=1
HARNESS_CHECK: FAIL tally harness: statuses 1 2 0 0 0 0 0 0 0 -> REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)
HARNESS_RESULT: 8/9 pass
PANEL id=N02 exit=1
HARNESS_CHECK: FAIL tally harness: loop missing one operand -> SETUP case-tally mismatch, exit 2
HARNESS_RESULT: 8/9 pass
PANEL id=N03 exit=1
HARNESS_CHECK: FAIL tally harness: one leg status 1 at each of 9 positions -> REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0) (0/9)
HARNESS_CHECK: FAIL tally harness: statuses 1 1 0 0 0 0 0 0 0 -> REGRESSION: FAIL (cases=9 passed=7 failed=2 setup=0)
HARNESS_CHECK: FAIL tally harness: statuses 1 2 0 0 0 0 0 0 0 -> REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)
HARNESS_RESULT: 6/9 pass
TALLY_AUDIT: PASS harness panel only
```

## Frozen-input and isolation evidence

The following hashes were recorded before and after the counter/probe. Counter and contract values were identical in both calls; the sandbox runner remained pinned:

```sh
sha256sum /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/contract.json tools/mutate-and-run.sh
```

```text
ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py
7f3d5d99a3da67ab7d03193ab5421e46e519f0de657d8168ab9727cd8ee7e583  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/contract.json
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  tools/mutate-and-run.sh
```

The after command additionally hashed `tools/tally-audit.py`, observing:

```text
1a1e1da7d24ca3eaa0773dfe8d76d9ffad850407ea1737d96ae9e03e21ce0f24  tools/tally-audit.py
```

All code execution, clone writes, tally scripts, and receipts were inside this seat's scratch directory. The only write outside scratch is this assigned report. No production source, sibling scratch, fleet index, or repository state was edited. No `jj` command, production Git write, full runner `--selftest`, or `--regression` was run. All started subprocesses returned and were reaped; no background service was started and no process was killed manually. No tools were installed or updated.

## Smallest safe correction

No correction to the frozen counter, predicate, runner, or this intentionally partial control is indicated. The real C1 tool still needs the omitted independent per-leg check and 0-255 runtime oracle with tally stress. Its harness panel needs faults that cover every singleton position and each independent multi-status vector, rather than relying on only the fixed H05 and N01 witnesses. Keep the counter and runner unchanged.

## Full control source

File: `/fast/scratch/hyaku/tameshi-r32-seats/CtlHarnessOnly/lane/tools/tally-audit.py`; committed at `7f5cc74fb6d0eb7633ed4884d6e2fe00718bbcf4`.

```python
#!/usr/bin/env python3
"""Pre-data C1 control: exercise only the supplied runner's tally harness.

The independent pristine fixture and six faults follow round-30 MutateHead.md,
"Exact supplemental construction". No runtime oracle or per-leg audit is run.
Exit 0 means this panel passed, 1 means a harness discrimination failure,
and 2 means the panel could not run.
"""
import argparse
import os
from pathlib import Path
import shlex
import subprocess
import tempfile


PRISTINE_TALLY = r'''  local nlegs=9 npass=0 nfail=0 nsetup=0 st
  for st in "$st_js" "$st_kagi" "$st_tsu" "$st_mado" "$st_checklist" "$st_claims" "$st_roundgate" "$st_sourcescheck" "$st_citecheck"; do
    case $st in
      0) npass=$((npass + 1)) ;;
      1) nfail=$((nfail + 1)) ;;
      *) nsetup=$((nsetup + 1)) ;;
    esac
  done

  if [[ $nfail -gt 0 ]]; then
    printf 'REGRESSION: FAIL (cases=%s passed=%s failed=%s setup=%s)\n' \
      "$nlegs" "$npass" "$nfail" "$nsetup"
    printf 'REGRESSION_WORKDIR: %s (kept)\n' "$root"
    exit 1
  fi
  if [[ $nsetup -gt 0 ]]; then
    printf 'REGRESSION: SETUP (cases=%s passed=%s cannot-verify=%s)\n' \
      "$nlegs" "$npass" "$nsetup"
    printf 'REGRESSION_WORKDIR: %s (kept)\n' "$root"
    exit 2
  fi
  # r30: tally completeness (round-29 routed leg-sum defect). A PASS needs every one of the
  # nlegs statuses counted; counts that do not sum to nlegs refuse as SETUP (S087: the totals
  # of a mutation report are sums of its per-state counts).
  if (( npass + nfail + nsetup != nlegs )); then
    printf 'REGRESSION: SETUP (case-tally mismatch: cases=%s counted=%s)\n' \
      "$nlegs" "$((npass + nfail + nsetup))"
    printf 'REGRESSION_WORKDIR: %s (kept)\n' "$root"
    exit 2
  fi
  printf 'REGRESSION: PASS (cases=%s passed=%s; ledger legs exact: killed-delta<=0 flips<=0)\n' \
    "$nlegs" "$npass"
  if [[ $auto -eq 1 && $KEEP -eq 0 ]]; then
    printf 'REGRESSION_WORKDIR: %s (removed on PASS; --keep retains)\n' "$root"
    rm -rf "$root"
  else
    printf 'REGRESSION_WORKDIR: %s (kept)\n' "$root"
  fi
  exit 0
'''


def panel():
    block = PRISTINE_TALLY
    fail_at = block.index('  if [[ $nfail -gt 0 ]]; then\n')
    setup_at = block.index('  if [[ $nsetup -gt 0 ]]; then\n')
    setup_end = block.index('  fi\n', setup_at) + len('  fi\n')
    guard_at = block.index('  if (( npass + nfail + nsetup != nlegs )); then\n')
    guard_end = block.index('  fi\n', guard_at) + len('  fi\n')
    return [
        ('pristine', block),
        ('H03', block.replace('passed=%s', 'passing=%s')),
        ('H04', block.replace(' "$st_citecheck"; do\n', '; do\n', 1)),
        ('H05', block.replace('  local nlegs=9 npass=0 nfail=0 nsetup=0 st\n',
                              '  local nlegs=9 npass=0 nfail=0 nsetup=0 st\n  st_citecheck=0\n', 1)),
        ('N01', block[:fail_at] + block[setup_at:setup_end]
                + block[fail_at:setup_at] + block[setup_end:]),
        ('N02', block[:guard_at] + block[guard_end:]),
        ('N03', block.replace('    exit 1\n', '    exit 0\n', 1)),
    ]


def run_harness(runner, harness, extraction, label, block, root):
    injected = harness.replace(extraction, extraction + '  tblock=' + shlex.quote(block) + '\n', 1)
    program = (
        'set -u -o pipefail\nSELF=' + shlex.quote(str(runner)) + '\n'
        'probe() {\n'
        '  local root=$1 cases=0 failed=0\n'
        '  st() {\n'
        '    cases=$((cases + 1))\n'
        '    if [[ $2 -ne 0 ]]; then\n'
        '      failed=$((failed + 1))\n'
        '      printf "HARNESS_CHECK: FAIL %s\\n" "$1"\n'
        '    fi\n'
        '  }\n'
        + injected
        + '  printf "HARNESS_RESULT: %s/%s pass\\n" "$((cases - failed))" "$cases"\n'
        '  [[ $failed -eq 0 ]]\n'
        '}\nprobe "$1"\n'
    )
    result = subprocess.run(
        ['timeout', '20', 'bash', '--noprofile', '--norc', '-s', '--', str(root)],
        input=program, capture_output=True, text=True, timeout=25,
        env={key: value for key, value in os.environ.items()
             if key not in ('BASH_ENV', 'ENV', 'SHELLOPTS', 'BASHOPTS')},
    )
    print('PANEL id=%s exit=%s' % (label, result.returncode))
    print(result.stdout, end='')
    if result.stderr:
        print(result.stderr, end='')
    if result.returncode not in (0, 1):
        raise RuntimeError('harness execution failed for ' + label)
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runner', required=True, type=Path)
    args = parser.parse_args()
    try:
        runner = args.runner.resolve(strict=True)
        text = runner.read_text(encoding='utf-8')
        start = text.index('  local tblock ')
        finish = text.index('  tblock=$tblock_full\n', start) + len('  tblock=$tblock_full\n')
        harness = text[start:finish]
        extraction, = [line for line in harness.splitlines(keepends=True)
                        if line.startswith('  tblock=$(awk ')]
        failures = []
        with tempfile.TemporaryDirectory(prefix='harness-panel-',
                                         dir=os.environ.get('TMPDIR', os.getcwd())) as work:
            for label, block in panel():
                root = Path(work) / label
                root.mkdir()
                rc = run_harness(runner, harness, extraction, label, block, root)
                if label == 'pristine' and rc != 0:
                    failures.append('harness rejected pristine')
                elif label != 'pristine' and rc == 0:
                    failures.append('harness accepted ' + label)
        if failures:
            print('TALLY_AUDIT: FAIL ' + '; '.join(failures))
            return 1
        print('TALLY_AUDIT: PASS harness panel only')
        return 0
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as error:
        print('TALLY_AUDIT: CANNOT_AUDIT ' + str(error))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
```

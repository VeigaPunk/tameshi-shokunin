# HeldOutGuard — sealed held-out author

**Verdict: SURVIVED.** Both valid must-kill copies were incorrectly accepted by the frozen audit. Both valid must-accept copies were correctly accepted. Every pristine and restored control passed; every probe target was restored byte-for-byte. This is a detector coverage finding, not a judgment of the round or its final measurement.

Axes: operability, genuinely new held-out shapes, classification correctness, and isolation with exact restoration.

## Evidence

All execution and generated artifacts stayed under `/fast/scratch/hyaku/tameshi-r32-seats/HeldOutGuard/`; only this report was written in the lane. The isolated clone was checked out at `a4f718138bdad20de741faeca57891645e5a64d9`. No subagents, production edits, counter main, full regression, or sandbox measurement were run. No tools were installed or updated.

Relevant source locations, relative to that clone:

- `.ufo/evidence/round-32/v2/c1-measure-v2.py:25-40,206-252`: schema and mechanical validity requirements.
- `tools/mutate-and-run.sh:1441-1461`: FAIL precedence, SETUP exit, and exact-count completeness guard.
- `tools/tally-audit.py:218-253`: sampled mixed-status vectors and one-operand duplicate/drop stresses.
- `tools/tally-audit.py:338-354`: harness tested against the independent reference panel.
- `corpus/knowledge/runner-tally-audit.md:12-15`: stated first-line/exit contract and independence of the checks.

### Commands and validation

Clone preparation completed with no output:

```sh
mkdir -p /fast/scratch/hyaku/tameshi-r32-seats/HeldOutGuard && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r32-seats/HeldOutGuard/c && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/HeldOutGuard/c checkout -q --detach a4f718138bdad20de741faeca57891645e5a64d9
```

The probe obtained the pinned runner with this child command, with `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` unset, and wrote captured stdout to `pinned.sh`:

```sh
git -C /fast/scratch/hyaku/tameshi-r32-seats/HeldOutGuard/c show e24688b2ff6cca1c9ad20e112f02c629b8597ff8:tools/mutate-and-run.sh
```

The complete reproducible probe is `/fast/scratch/hyaku/tameshi-r32-seats/HeldOutGuard/probe.py`. Actual invocation:

```sh
timeout 1200 python3 /fast/scratch/hyaku/tameshi-r32-seats/HeldOutGuard/probe.py
```

Observed exit: **0**, elapsed **27.94 seconds**. Four independent file probes ran concurrently. The module was imported without invoking its main. Each file was passed to:

```python
body = v2.validate(ho, pristine, '/fast/scratch/hyaku/tameshi-r32-seats/HeldOutGuard/pinned.sh', tmp, [])
```

All four calls returned the copy text; none raised `v2.Invalid`. The accept copies leave the harness section unchanged. The empty block-witness list therefore does not mask a harness change in either accept copy.

Each following exact detector command ran on pristine, modified, and restored bytes at the same path:

```sh
timeout 300 python3 /fast/scratch/hyaku/tameshi-r32-seats/HeldOutGuard/c/tools/tally-audit.py --runner /fast/scratch/hyaku/tameshi-r32-seats/HeldOutGuard/copies/1.sh
timeout 300 python3 /fast/scratch/hyaku/tameshi-r32-seats/HeldOutGuard/c/tools/tally-audit.py --runner /fast/scratch/hyaku/tameshi-r32-seats/HeldOutGuard/copies/2.sh
timeout 300 python3 /fast/scratch/hyaku/tameshi-r32-seats/HeldOutGuard/c/tools/tally-audit.py --runner /fast/scratch/hyaku/tameshi-r32-seats/HeldOutGuard/copies/3.sh
timeout 300 python3 /fast/scratch/hyaku/tameshi-r32-seats/HeldOutGuard/c/tools/tally-audit.py --runner /fast/scratch/hyaku/tameshi-r32-seats/HeldOutGuard/copies/4.sh
```

| id | set | validity | modified tool exit | modified TALLY_AUDIT line | defeats tool |
|---|---|---|---:|---|---|
| HeldOutGuard-1 | kill | valid | 0 | `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)` | yes; survived |
| HeldOutGuard-2 | kill | valid | 0 | `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)` | yes; survived |
| HeldOutGuard-3 | accept | valid | 0 | `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)` | no; correctly accepted |
| HeldOutGuard-4 | accept | valid | 0 | `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)` | no; correctly accepted |

Expected detector behavior: exit **1** and `TALLY_AUDIT: FAIL` for copies 1 and 2; exit **0** and `TALLY_AUDIT: PASS` for copies 3 and 4. Actual stdout was identical on all pristine, modified, and restored runs, with exit 0 and empty stderr:

```text
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=349 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=27/27
TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)
```

### Mutants and witnesses

**HeldOutGuard-1:** A single FAIL predicate adds an incorrect majority qualification. This is not the v1 status-reclassification or skipped-harness-vector family. For `[1,2,2,2,2,2,0,0,0]`, observed tally results were:

```text
pristine exit 1: REGRESSION: FAIL (cases=9 passed=3 failed=1 setup=5)
modified exit 2: REGRESSION: SETUP (cases=9 passed=3 cannot-verify=5)
```

The frozen runtime panel has no mixed vector with a setup majority. Its harness check injects independent reference blocks, so it does not discover this change to the audited tally. Evidence: `receipts/1.json:14-28,38-39` under the scratch root.

**HeldOutGuard-2:** A single completeness predicate substitutes divisibility for exact equality. Unlike the v1 one-sided relational guard defect, it still rejects both eight and ten counted operands. With the witness loop containing the entire nine-leg panel twice and all statuses zero, observed tally results were:

```text
pristine exit 2: REGRESSION: SETUP (case-tally mismatch: cases=9 counted=18)
modified exit 0: REGRESSION: PASS (cases=9 passed=18; ledger legs exact: killed-delta<=0 flips<=0)
```

The copy itself retains exactly the original nine loop operands; the witness changes both tally loops only for the counter-owned guard experiment, as allowed by the schema. Evidence: `receipts/2.json:14-28,38-39`.

**HeldOutGuard-3:** Arithmetic FAIL/SETUP predicates and a numeric `[[ ]]` completeness predicate preserve all outcomes. This is not the v1 cosmetic arm or simplified-pass-count guard copy. Evidence: `receipts/3.json:14-20,30-31`.

**HeldOutGuard-4:** The three verdict blocks run in reverse order. Explicit exclusions make completeness applicable only without FAIL/SETUP, and make SETUP applicable only without FAIL, preserving precedence and all exit codes. This is not an operand permutation or unqualified SETUP-before-FAIL fault. Evidence: `receipts/4.json:14-20,30-31`.

### Hashes and restoration

Pinned runner, all four before hashes, and all four after hashes:

```text
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9
```

Frozen tool before and after:

```text
9639c458002ce2f954addbe047427010ae011353e073b293396bec800fa699ef
```

| id | modified copy SHA-256 | held-out JSON SHA-256 |
|---|---|---|
| HeldOutGuard-1 | `28176f17d8f5d72e6051f2582293108caaa19f17e32f2f949f04298ba153adb6` | `8a9c213d85849175f833a63b9a0b41b6ecaa3cd9cf3e73c4d1e7875e09c8077d` |
| HeldOutGuard-2 | `32d139f976f8c6eba6f66ea41bec8144fe2a251d142259210a32664f703b4358` | `b59702f1e1c7e96a6b205ea60f1c201e0357e10a07c43a1433a8e2055f5b1670` |
| HeldOutGuard-3 | `26a74300d8357e607e1e14df90b6b8ae3614b1c7d705ab97841b8abdab341c8a` | `79e5405b3a1b4a57fade6e2144f915464d484b7a63f2d920b86a5c4e2c2b9012` |
| HeldOutGuard-4 | `8fb8a090b1c9dc8fd0fe4393512edfdd6d360b11d86f5f8174ba3c8e9064bb54` | `e38529bc332df1ecfd5e8da57c062bfa03b0104e73fdc165249b50e0b0ae8d67` |

Every receipt records `restored_exact: true` and a restored exit-0 PASS (`receipts/1.json:30-36`, `2.json:30-36`, `3.json:22-28`, `4.json:22-28`). The clone's original runner remained at the pinned hash. `copies/1.sh` through `copies/4.sh` are restored probe targets; the tested modified bytes are retained separately as `mutants/HeldOutGuard-1.sh` through `mutants/HeldOutGuard-4.sh`. The integration deliverables are the four JSON files in `heldout/`, pasted verbatim below. All subprocesses were awaited; no detector timeout occurred or background service was started.

## Smallest safe correction

Do not alter the frozen tool or contract before the measurement. For a later revision, add these two witnesses to `check_runtime`: one mixed FAIL/setup-majority vector and one whole-panel duplication guard stress. Retain oracle comparisons of both exit and first line. No production correction was applied by this seat.

## Sealed files

HELDOUT-FILE HeldOutGuard-1
```json
{
  "id": "HeldOutGuard-1",
  "author": "HeldOutGuard",
  "set": "kill",
  "edits": [
    {
      "old": "  if [[ $nfail -gt 0 ]]; then\n",
      "new": "  if [[ $nfail -gt 0 && $nsetup -le $((npass + nfail)) ]]; then\n"
    }
  ],
  "rationale": "The FAIL condition is incorrectly gated on a majority of non-setup legs, so five setup statuses suppress an existing failure instead of preserving FAIL precedence.",
  "witness": {
    "vector": [1, 2, 2, 2, 2, 2, 0, 0, 0]
  }
}
```

HELDOUT-FILE HeldOutGuard-2
```json
{
  "id": "HeldOutGuard-2",
  "author": "HeldOutGuard",
  "set": "kill",
  "edits": [
    {
      "old": "  if (( npass + nfail + nsetup != nlegs )); then\n",
      "new": "  if (( (npass + nfail + nsetup) % nlegs != 0 )); then\n"
    }
  ],
  "rationale": "The completeness guard checks divisibility instead of equality, so an entire duplicated nine-leg panel reports PASS with eighteen counted statuses.",
  "witness": {
    "vector": [0, 0, 0, 0, 0, 0, 0, 0, 0],
    "loop": ["st_js", "st_kagi", "st_tsu", "st_mado", "st_checklist", "st_claims", "st_roundgate", "st_sourcescheck", "st_citecheck", "st_js", "st_kagi", "st_tsu", "st_mado", "st_checklist", "st_claims", "st_roundgate", "st_sourcescheck", "st_citecheck"]
  }
}
```

HELDOUT-FILE HeldOutGuard-3
```json
{
  "id": "HeldOutGuard-3",
  "author": "HeldOutGuard",
  "set": "accept",
  "edits": [
    {
      "old": "  if [[ $nfail -gt 0 ]]; then\n",
      "new": "  if (( nfail > 0 )); then\n"
    },
    {
      "old": "  if [[ $nsetup -gt 0 ]]; then\n",
      "new": "  if (( 0 < nsetup )); then\n"
    },
    {
      "old": "  if (( npass + nfail + nsetup != nlegs )); then\n",
      "new": "  if [[ $((npass + nfail + nsetup)) -ne $nlegs ]]; then\n"
    }
  ],
  "rationale": "Arithmetic conditions replace the FAIL and SETUP numeric tests while a numeric [[ ]] comparison replaces the completeness expression without changing any verdict or exit."
}
```

HELDOUT-FILE HeldOutGuard-4
```json
{
  "id": "HeldOutGuard-4",
  "author": "HeldOutGuard",
  "set": "accept",
  "edits": [
    {
      "old": "  if [[ $nfail -gt 0 ]]; then\n    printf 'REGRESSION: FAIL (cases=%s passed=%s failed=%s setup=%s)\\n' \\\n      \"$nlegs\" \"$npass\" \"$nfail\" \"$nsetup\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    exit 1\n  fi\n  if [[ $nsetup -gt 0 ]]; then\n    printf 'REGRESSION: SETUP (cases=%s passed=%s cannot-verify=%s)\\n' \\\n      \"$nlegs\" \"$npass\" \"$nsetup\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    exit 2\n  fi\n  # r30: tally completeness (round-29 routed leg-sum defect). A PASS needs every one of the\n  # nlegs statuses counted; counts that do not sum to nlegs refuse as SETUP (S087: the totals\n  # of a mutation report are sums of its per-state counts).\n  if (( npass + nfail + nsetup != nlegs )); then\n    printf 'REGRESSION: SETUP (case-tally mismatch: cases=%s counted=%s)\\n' \\\n      \"$nlegs\" \"$((npass + nfail + nsetup))\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    exit 2\n  fi\n",
      "new": "  # Completeness is only decisive when no leg has failed or needs setup.\n  if (( nfail == 0 && nsetup == 0 && npass + nfail + nsetup != nlegs )); then\n    printf 'REGRESSION: SETUP (case-tally mismatch: cases=%s counted=%s)\\n' \\\n      \"$nlegs\" \"$((npass + nfail + nsetup))\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    exit 2\n  fi\n  if [[ $nfail -eq 0 && $nsetup -gt 0 ]]; then\n    printf 'REGRESSION: SETUP (cases=%s passed=%s cannot-verify=%s)\\n' \\\n      \"$nlegs\" \"$npass\" \"$nsetup\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    exit 2\n  fi\n  if [[ $nfail -gt 0 ]]; then\n    printf 'REGRESSION: FAIL (cases=%s passed=%s failed=%s setup=%s)\\n' \\\n      \"$nlegs\" \"$npass\" \"$nfail\" \"$nsetup\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    exit 1\n  fi\n"
    }
  ],
  "rationale": "Completeness, SETUP and FAIL are tested in reverse order with explicit exclusions for higher-priority outcomes, preserving every first line and exit code."
}
```

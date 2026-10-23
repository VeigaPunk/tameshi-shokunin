# HeldOutPrintf — sealed held-out copies for C1 counter v2

Verdict: **SURVIVED — both valid must-kill copies defeat the frozen tool.** The frozen `tools/tally-audit.py` (sha256 `9639c458…99ef`) exits 0 with `TALLY_AUDIT: PASS` on HeldOutPrintf-1 and HeldOutPrintf-2, i.e. it accepts two runner copies that misreport their printed tally counts. Both must-accept copies were correctly accepted. These are direct detector results on the frozen tool, not a full C1 counter measurement (the counter's `main` was never run).

Seat: HeldOutPrintf.
Scratch: `/fast/scratch/hyaku/tameshi-r32-seats/HeldOutPrintf/`.
Axes: printed REGRESSION-line field correctness; frozen-tool detection of those fields; held-out validity under the frozen counter schema; byte-exact equivalence of the accept copies.

## 1. Results

Expected detector outcome: a must-kill copy must exit 1 with a stdout line beginning `TALLY_AUDIT: FAIL`; a must-accept copy must exit 0 with `TALLY_AUDIT: PASS`.

| ID | Set | Validity | Tool exit | Exact TALLY_AUDIT line | Defeats tool |
| --- | --- | --- | --- | --- | --- |
| HeldOutPrintf-1 | kill | valid | 0 | `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)` | **Yes: survived** |
| HeldOutPrintf-2 | kill | valid | 0 | `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)` | **Yes: survived** |
| HeldOutPrintf-3 | accept | valid | 0 | `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)` | No: correctly accepted |
| HeldOutPrintf-4 | accept | valid | 0 | `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)` | No: correctly accepted |

All four files are under `/fast/scratch/hyaku/tameshi-r32-seats/HeldOutPrintf/heldout/`; their materialized runner copies are `copies/HeldOutPrintf-1.sh` … `copies/HeldOutPrintf-4.sh` under the same seat directory.

## 2. Environment and method

Clone at the measurement revision `a4f718138bdad20de741faeca57891645e5a64d9`:

```sh
mkdir -p /fast/scratch/hyaku/tameshi-r32-seats/HeldOutPrintf && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r32-seats/HeldOutPrintf/c && git -C /fast/scratch/hyaku/tameshi-r32-seats/HeldOutPrintf/c checkout -q --detach a4f718138bdad20de741faeca57891645e5a64d9
```

Pinned runner extracted with the frozen base revision:

```sh
git -C /fast/scratch/hyaku/tameshi-r32-seats/HeldOutPrintf/c show e24688b2ff6cca1c9ad20e112f02c629b8597ff8:tools/mutate-and-run.sh > /fast/scratch/hyaku/tameshi-r32-seats/HeldOutPrintf/pinned.sh
```

Observed SHA-256 (from `final2.py`, fingerprints block):

```text
clone tool       9639c458002ce2f954addbe047427010ae011353e073b293396bec800fa699ef
lane  tool       9639c458002ce2f954addbe047427010ae011353e073b293396bec800fa699ef
clone counter v2 1ab9e9cf8e408f6230110ac42495da2b9c3f51236fe3a32754bd23524f7f7c94
lane  counter v2 1ab9e9cf8e408f6230110ac42495da2b9c3f51236fe3a32754bd23524f7f7c94
pinned runner    a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9
```

The clone's tool and counter bytes are identical to the lane's, and the pinned runner matches `PINNED_RUNNER_SHA` (`c1-measure-v2.py:64`). Validity was checked by importing the frozen counter and calling `v2.validate(ho, pristine, ppath, tmp, [])` — the counter's `main` was never invoked. The validity rules exercised are `.ufo/evidence/round-32/v2/c1-measure-v2.py:206-252`; the kill-witness comparison is at `:229-230` and the accept sweep/stress/harness comparisons at `:240-251`.

Batch commands (all inside the seat directory, all waited for):

```sh
timeout 900 python3 /fast/scratch/hyaku/tameshi-r32-seats/HeldOutPrintf/gen.py
timeout 280 python3 /fast/scratch/hyaku/tameshi-r32-seats/HeldOutPrintf/final2.py
timeout 280 python3 /fast/scratch/hyaku/tameshi-r32-seats/HeldOutPrintf/final3.py
```

Each held-out copy was then audited directly with the frozen tool:

```sh
timeout 300 python3 /fast/scratch/hyaku/tameshi-r32-seats/HeldOutPrintf/c/tools/tally-audit.py --runner /fast/scratch/hyaku/tameshi-r32-seats/HeldOutPrintf/copies/HeldOutPrintf-1.sh
timeout 300 python3 /fast/scratch/hyaku/tameshi-r32-seats/HeldOutPrintf/c/tools/tally-audit.py --runner /fast/scratch/hyaku/tameshi-r32-seats/HeldOutPrintf/copies/HeldOutPrintf-2.sh
timeout 300 python3 /fast/scratch/hyaku/tameshi-r32-seats/HeldOutPrintf/c/tools/tally-audit.py --runner /fast/scratch/hyaku/tameshi-r32-seats/HeldOutPrintf/copies/HeldOutPrintf-3.sh
timeout 300 python3 /fast/scratch/hyaku/tameshi-r32-seats/HeldOutPrintf/c/tools/tally-audit.py --runner /fast/scratch/hyaku/tameshi-r32-seats/HeldOutPrintf/copies/HeldOutPrintf-4.sh
```

All four exited 0 with empty stderr and printed:

```text
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=349 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=27/27
TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)
```

Every copy also passes the runner's own gate, `bash <copy> --selftest`, with `MUTATE_SELFTEST: 106/106 pass | VERDICT: PASS` (exit 0) — same as the pristine runner. Both defective copies are therefore invisible to the runner's internal selftest as well as to the external audit; the printed tally is the only place the defect is observable.

## 3. The two surviving must-kill copies

Both defects are in the **printed** REGRESSION lines of the pinned tally block (`tools/mutate-and-run.sh:1441-1451`), in the branch that the assignment named: a field that prints the wrong counter in one branch only. Neither touches the loop operands, the leg assignments, the completeness guard or the selftest harness, so all three of the tool's checks pass.

### HeldOutPrintf-1 — the FAIL branch's `failed=` field under-reports

`tools/mutate-and-run.sh:1441-1443` prints `failed=%s` from `$nfail`. The copy subtracts one from the reported failure count whenever three to eight legs failed and at least one leg passed:

```sh
"$nlegs" "$npass" "$((nfail - (nfail > 2 && npass > 0 ? 1 : 0)))" "$nsetup"
```

Witness through the counter's own `tally_outputs` instrument (`final3.py`), vector `[0, 1, 1, 1, 0, 0, 0, 0, 0]`:

```text
pinned exit=1 line='REGRESSION: FAIL (cases=9 passed=6 failed=3 setup=0)'
copy   exit=1 line='REGRESSION: FAIL (cases=9 passed=6 failed=2 setup=0)'
```

The exit code stays 1 and the `cases=`/`passed=`/`setup=` fields stay correct; only the reported failure count is wrong. The whole stdout differs only in that field:

```text
pinned  (1, b'REGRESSION: FAIL (cases=9 passed=6 failed=3 setup=0)\nREGRESSION_WORKDIR: c1v2 (kept)\n')
copy    (1, b'REGRESSION: FAIL (cases=9 passed=6 failed=2 setup=0)\nREGRESSION_WORKDIR: c1v2 (kept)\n')
```

### HeldOutPrintf-2 — the SETUP branch's `cannot-verify=` field under-reports

`tools/mutate-and-run.sh:1447-1449` prints `cannot-verify=%s` from `$nsetup`. The copy subtracts one when exactly three legs could not be verified:

```sh
"$nlegs" "$npass" "$((nsetup == 3 ? nsetup - 1 : nsetup))"
```

Witness through the same instrument, vector `[2, 2, 2, 0, 0, 0, 0, 0, 0]`:

```text
pinned exit=2 line='REGRESSION: SETUP (cases=9 passed=6 cannot-verify=3)'
copy   exit=2 line='REGRESSION: SETUP (cases=9 passed=6 cannot-verify=2)'
```

The exit code stays 2 and the verdict class stays SETUP; the reported unverified-leg count is wrong.

### Why the tool misses both

The tool's runtime check compares the copy's printed first line against an oracle over a fixed vector set (`tools/tally-audit.py:218-245`). The set reaches only a narrow slice of the count space. Reconstructing it from the source (`probe.py`, `tool_vectors()`) and reporting the reachable counter values:

```text
frozen tool runtime vectors: 331
  reachable nfail values   : [0, 1, 2, 9]
  reachable nsetup values  : [0, 1, 2, 9]
  reachable npass values   : [0, 7, 8, 9]
  -> 3..8 simultaneous failures sampled? False
  -> all 36 leg pairs sampled?           True
```

The tool's own vectors are: all-zero; one status `1..255` at leg 0 (`tally-audit.py:222-223`); one status in `{1,2,3,4,126,127,255}` at each leg (`:224-228`); two legs at `(0, n-1)` and `(n//2, n//2+1)` with pairs from `{(1,1),(2,2),(1,2),(2,1),(3,4)}` (`:229-233`); and the two uniform vectors `[1]*n` and `[2]*n` (`:234-235`). The reachable `nfail`/`nsetup` values are therefore `{0,1,2,9}` — **3..8 is never produced**. HeldOutPrintf-1 needs `nfail ∈ 3..8`; HeldOutPrintf-2 needs `nsetup == 3`. Neither regime is sampled, so the oracle never fires and the tool reports PASS. The tool's static check (`:200-216`) and harness check (`:338-352`) are untouched by these edits and both pass, which is why the verdict is a clean `PASS` on all three checks.

This is a coverage gap in the vector set, not a gap in the oracle: the oracle itself (`:183-198`) would flag both copies correctly if the vectors reached the regime.

## 4. The two must-accept copies

Both are byte-identical-output rewrites of the printed lines, and neither changes the operand multiset, the leg names, the guard or the harness.

- **HeldOutPrintf-3** changes only the printf format specifiers of the four printed REGRESSION lines from `%s` to `%d`. Every argument is an integer, so the bytes are unchanged. This is a different shape from the v1 accept families (pristine, T07 equivalent guard, reversed operands, decoy comments, cosmetic arm edit, renamed harness variable, random operand permutation, nonce comments): it rewrites the *format* of the printed contract lines.
- **HeldOutPrintf-4** changes only the spelling of the five `REGRESSION_WORKDIR` printfs (one respelled as `printf '%s\n' "REGRESSION_WORKDIR: $root (kept)"`, four with `${root}` instead of `"$root"`). The printed bytes are unchanged.

Byte-identity check of the whole stdout+stderr and the exit code against the pinned block over seven vectors (all-zero, single 1, single 2, single 3, two 1s, two 2s, three 1s), from `final3.py`:

```text
HeldOutPrintf-3 full-output byte identity vs pinned over 7 vectors: IDENTICAL (all stdout+stderr bytes and exit codes)
HeldOutPrintf-4 full-output byte identity vs pinned over 7 vectors: IDENTICAL (all stdout+stderr bytes and exit codes)
```

Both passed the counter's mandatory accept validation (leg names and operand multisets equal to the pinned ones, tally equal on the sweep, equal under the duplicate/drop stress, and equal harness verdicts on the reference block and the counter's 18 fault blocks with the empty held-out block-witness list).

## 5. Scope boundary found while probing: the REGRESSION_WORKDIR line is unobservable to the schema

A separate probe (not submitted as a held-out file) changed only the FAIL branch's workdir line to report a wrong scratch root:

```sh
printf 'REGRESSION_WORKDIR: %s (kept)\n' "$root/wrong-scratch-dir"
```

Observed with the frozen tool: `exit=0 TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)`. The printed bytes do change:

```text
pinned         exit=1 stdout='REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: /tmp/scratch-root (kept)\n'
workdir-probe  exit=1 stdout='REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: /tmp/scratch-root/wrong-scratch-dir (kept)\n'
```

The tool never compares the workdir line, and the counter's kill schema cannot express this defect either: `v2.validate` rejected it with `Invalid: vector witness shows no difference`, because the vector witness compares only the exit code and the **first** stdout line (`c1-measure-v2.py:229-230` compares `tally_outputs`, which returns `(exit, first line)` at `:129-138`). So a misreported `REGRESSION_WORKDIR` path is neither detectable by the frozen tool nor expressible as a valid held-out must-kill copy under the frozen schema. I did not submit it; the counter excludes invalid files, and this one is invalid by the schema's own rule.

## 6. Smallest safe correction

For a future, unfrozen revision of the audit tool, extend the runtime vector set in `check_runtime` (`tools/tally-audit.py:218-245`) to reach the `nfail`/`nsetup` regimes the current set skips — in particular the 3..8 band, which is the entire gap both surviving copies exploit. Adding the 3..8 uniform-failure and uniform-setup vectors is the minimal change:

```python
    for k in range(3, n):
        vectors.append([1] * k + [0] * (n - k))
        vectors.append([2] * k + [0] * (n - k))
```

I applied exactly this to a **scratch copy** of the tool (the lane tool was never modified; the patched file is `tally-audit-patched.py` under the seat directory, sha256 `466080bbd3845648`) and re-ran it (`probe2.py`):

```text
patched tool vs pinned and the four held-out copies:
  pinned                     exit=0 TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)
  HeldOutPrintf-1.sh         exit=1 TALLY_AUDIT: FAIL (static=pass runtime=fail harness=pass)
  HeldOutPrintf-2.sh         exit=1 TALLY_AUDIT: FAIL (static=pass runtime=fail harness=pass)
  HeldOutPrintf-3.sh         exit=0 TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)
  HeldOutPrintf-4.sh         exit=0 TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)
```

The patched tool kills both surviving copies, keeps passing pristine, and keeps accepting both equivalent copies. This is evidence for a future revision only: the frozen tool's SHA-256 is pinned by the counter (`c1-measure-v2.py:70`, `TOOL_SHA256`), so the current measurement cannot use a patched tool. Keep the frozen tool, contract, counter and pinned runner unchanged for this measurement and retain all four submitted files; the surviving copies are a coverage finding, not permission to relax the predicate.

If the maintainers instead want the workdir line covered, that requires a separate change: the tool would have to compare the full stdout of the tally block (not only its first line), and the counter's kill schema would need a witness form that can express a difference outside the first line. Both are larger than the vector-set fix and neither is in scope for this frozen measurement.

## 7. Bounds and handoff

Only this report and files under `/fast/scratch/hyaku/tameshi-r32-seats/HeldOutPrintf/` were written. No production tool, contract, counter or runner was edited; the patched tool exists only as a scratch file and the lane's `tools/tally-audit.py` still hashes to `9639c458…99ef`. Git writes occurred only in the private clone; no `jj` command was run anywhere; the fleet repo, sibling lanes and the lane index were not touched. The counter's `main` was never executed — only `v2.validate` was imported and called. No regression replay, production gate, subagent, package install or tool update was run. All launched processes were waited for; one background batch was killed by the harness at 300 s and was re-run in the foreground with the selftest evidence collected separately.

## 8. Held-out file contents

HELDOUT-FILE HeldOutPrintf-1
```json
{
  "id": "HeldOutPrintf-1",
  "author": "HeldOutPrintf",
  "set": "kill",
  "edits": [
    {
      "old": "  if [[ $nfail -gt 0 ]]; then\n    printf 'REGRESSION: FAIL (cases=%s passed=%s failed=%s setup=%s)\\n' \\\n      \"$nlegs\" \"$npass\" \"$nfail\" \"$nsetup\"\n",
      "new": "  if [[ $nfail -gt 0 ]]; then\n    printf 'REGRESSION: FAIL (cases=%s passed=%s failed=%s setup=%s)\\n' \\\n      \"$nlegs\" \"$npass\" \"$((nfail - (nfail > 2 && npass > 0 ? 1 : 0)))\" \"$nsetup\"\n"
    }
  ],
  "rationale": "The REGRESSION: FAIL line's failed= field prints one less than the real number of failed legs whenever three to eight legs failed, so the printed tally misreports the failure count; a real defect in a printed REGRESSION field.",
  "witness": {
    "vector": [
      0,
      1,
      1,
      1,
      0,
      0,
      0,
      0,
      0
    ]
  }
}
```

HELDOUT-FILE HeldOutPrintf-2
```json
{
  "id": "HeldOutPrintf-2",
  "author": "HeldOutPrintf",
  "set": "kill",
  "edits": [
    {
      "old": "  if [[ $nsetup -gt 0 ]]; then\n    printf 'REGRESSION: SETUP (cases=%s passed=%s cannot-verify=%s)\\n' \\\n      \"$nlegs\" \"$npass\" \"$nsetup\"\n",
      "new": "  if [[ $nsetup -gt 0 ]]; then\n    printf 'REGRESSION: SETUP (cases=%s passed=%s cannot-verify=%s)\\n' \\\n      \"$nlegs\" \"$npass\" \"$((nsetup == 3 ? nsetup - 1 : nsetup))\"\n"
    }
  ],
  "rationale": "The REGRESSION: SETUP line's cannot-verify= field prints one less than the real number of unverified legs when exactly three legs could not be verified, so the printed tally misreports the cannot-verify count; a real defect in a printed REGRESSION field.",
  "witness": {
    "vector": [
      2,
      2,
      2,
      0,
      0,
      0,
      0,
      0,
      0
    ]
  }
}
```

HELDOUT-FILE HeldOutPrintf-3
```json
{
  "id": "HeldOutPrintf-3",
  "author": "HeldOutPrintf",
  "set": "accept",
  "edits": [
    {
      "old": "    printf 'REGRESSION: FAIL (cases=%s passed=%s failed=%s setup=%s)\\n' \\\n      \"$nlegs\" \"$npass\" \"$nfail\" \"$nsetup\"\n",
      "new": "    printf 'REGRESSION: FAIL (cases=%d passed=%d failed=%d setup=%d)\\n' \\\n      \"$nlegs\" \"$npass\" \"$nfail\" \"$nsetup\"\n"
    },
    {
      "old": "    printf 'REGRESSION: SETUP (cases=%s passed=%s cannot-verify=%s)\\n' \\\n      \"$nlegs\" \"$npass\" \"$nsetup\"\n",
      "new": "    printf 'REGRESSION: SETUP (cases=%d passed=%d cannot-verify=%d)\\n' \\\n      \"$nlegs\" \"$npass\" \"$nsetup\"\n"
    },
    {
      "old": "    printf 'REGRESSION: SETUP (case-tally mismatch: cases=%s counted=%s)\\n' \\\n      \"$nlegs\" \"$((npass + nfail + nsetup))\"\n",
      "new": "    printf 'REGRESSION: SETUP (case-tally mismatch: cases=%d counted=%d)\\n' \\\n      \"$nlegs\" \"$((npass + nfail + nsetup))\"\n"
    },
    {
      "old": "  printf 'REGRESSION: PASS (cases=%s passed=%s; ledger legs exact: killed-delta<=0 flips<=0)\\n' \\\n    \"$nlegs\" \"$npass\"\n",
      "new": "  printf 'REGRESSION: PASS (cases=%d passed=%d; ledger legs exact: killed-delta<=0 flips<=0)\\n' \\\n    \"$nlegs\" \"$npass\"\n"
    }
  ],
  "rationale": "Only the printf format specifiers of the four printed REGRESSION lines change from %s to %d; every argument is an integer, so all printed bytes, exit codes and harness verdicts are unchanged."
}
```

HELDOUT-FILE HeldOutPrintf-4
```json
{
  "id": "HeldOutPrintf-4",
  "author": "HeldOutPrintf",
  "set": "accept",
  "edits": [
    {
      "old": "      \"$nlegs\" \"$npass\" \"$nfail\" \"$nsetup\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    exit 1\n",
      "new": "      \"$nlegs\" \"$npass\" \"$nfail\" \"$nsetup\"\n    printf '%s\\n' \"REGRESSION_WORKDIR: $root (kept)\"\n    exit 1\n"
    },
    {
      "old": "      \"$nlegs\" \"$npass\" \"$nsetup\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    exit 2\n",
      "new": "      \"$nlegs\" \"$npass\" \"$nsetup\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"${root}\"\n    exit 2\n"
    },
    {
      "old": "      \"$nlegs\" \"$((npass + nfail + nsetup))\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    exit 2\n",
      "new": "      \"$nlegs\" \"$((npass + nfail + nsetup))\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"${root}\"\n    exit 2\n"
    },
    {
      "old": "    printf 'REGRESSION_WORKDIR: %s (removed on PASS; --keep retains)\\n' \"$root\"\n",
      "new": "    printf 'REGRESSION_WORKDIR: %s (removed on PASS; --keep retains)\\n' \"${root}\"\n"
    },
    {
      "old": "    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n  fi\n",
      "new": "    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"${root}\"\n  fi\n"
    }
  ],
  "rationale": "Only the spelling of the five REGRESSION_WORKDIR printfs changes (one respelled as printf '%s\\n' with an interpolated argument, four with ${root} instead of \"$root\"); the printed bytes are identical, so no tally or harness behaviour changes."
}
```

## 9. Copy digests

| Copy | SHA-256 |
| --- | --- |
| HeldOutPrintf-1.sh | `8b092abf1f3fd17191e17fc9bf19b70a2b5550439f1029830da513cc63f3e74e` |
| HeldOutPrintf-2.sh | `e0142d719278f1f36bdc99abb06ec2e6c1e6c5a7dd8bffdbb655bef4cb2b87ac` |
| HeldOutPrintf-3.sh | `f3f57d4d2ca7a4fcc22ecf636599305b342829649f2c7efd92d575f28f4b5041` |
| HeldOutPrintf-4.sh | `abc9b1dabe71d8f2189b6c7939a2985c213e86c37fc38d3c3a438b678229a22f` |

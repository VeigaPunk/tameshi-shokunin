# MutateTallyExtra — frozen tally probe

## Verdict

**Three killed; seven survived; none inconclusive.** Four survivors are real tally-behavior coverage gaps (mixed FAIL/SETUP precedence, two failures, two setup results, and status 3). Two survivors are equivalent with the intact nine-operand loop but expose an untested completeness guard under a separate undercount stress. One survivor is an equivalent guard rewrite. No v4 score or round-admission judgment is made.

Axis: **operability**. Probe dimensions: detector coverage, isolation, and exact-byte restoration. All ten pristine and all ten restored selftests exited 0 with `MUTATE_SELFTEST: 101/101 pass` and `VERDICT: PASS`. Every edited runner was restored exactly.

## Evidence: scope and commands

`C = /fast/scratch/hyaku/tameshi-r30a2-seats/TameshiR30A2.MutateTallyExtra-7/clone`; `R = C/tools/mutate-and-run.sh`. Each mutant was applied only to `C/mutation-probes/M01/tools/mutate-and-run.sh` through `M10/tools/mutate-and-run.sh`, after copying `C/tools/` into that probe directory. References below use line numbers in the frozen, restored `R`.

Observed setup command (exit 0; no stdout/stderr):
```sh
mkdir -p /fast/scratch/hyaku/tameshi-r30a2-seats/TameshiR30A2.MutateTallyExtra-7
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r30a2-seats/TameshiR30A2.MutateTallyExtra-7/clone
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r30a2-seats/TameshiR30A2.MutateTallyExtra-7/clone checkout -q --detach f09d3425258403a51422c9959e25340807982947
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r30a2-seats/TameshiR30A2.MutateTallyExtra-7/clone apply /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/witness/fix.diff
```
The actual clone, checkout, and apply invocations had outer `timeout 180`, `timeout 60`, and `timeout 60` respectively.

Pristine full-runner SHA-256: `9a931bc2d0c31c32dd3a4ccf6594b56c3474628cca513b675901a8666fbec7d4`.
Pristine extracted tally SHA-256: `e163133c0f54bb0cbd1c3f123e18b5efc17ced6df4558de034575089a8a2215d` (matches the assignment).

For each copy, the **same command** ran on pristine, mutated, and restored bytes. `TREE` was the absolute `C/mutation-probes/Mxx` directory. A maximum of four detector jobs ran concurrently. The sandbox gives each job a private `/tmp`; no host `/tmp` fixtures or failing scratch directories remain.
```sh
timeout 310 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE bwrap --unshare-all --die-with-parent --new-session --clearenv --ro-bind /usr /usr --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib /lib64 --symlink usr/bin /sbin --ro-bind /etc /etc --proc /proc --dev /dev --tmpfs /tmp --setenv PATH /usr/bin --setenv HOME /w --setenv LANG C.UTF-8 --setenv TMPDIR /tmp \
  --bind "$TREE" /w --chdir /w \
  timeout 300 bash tools/mutate-and-run.sh --selftest
```
The Python subprocess working directory was `C`. The runner command inside the sandbox is exactly the requested bounded detector. An additional initial pristine run at `C` also exited 0 with `MUTATE_SELFTEST: 101/101 pass`; no detector run timed out.

### Hand-made changes and detector outcomes

| Mutant | Exact change; source location | Pristine exit / tally | Mutated exit / `MUTATE_SELFTEST` | Restored exit / tally | Verdict and survivor classification |
|---|---|---|---|---|---|
| M01 | Delete only the completeness-guard `if` block (six lines). `R:1454-1459` | 0 / 101/101 pass | 0 / `MUTATE_SELFTEST: 101/101 pass` | 0 / 101/101 pass | Survived; equivalent for the intact nine-operand loop, but the guard itself is unexercised. The separate missing-operand stress proves the lost protection. |
| M02 | Change guard `!= nlegs` to `> nlegs`. `R:1454` | 0 / 101/101 pass | 0 / `MUTATE_SELFTEST: 101/101 pass` | 0 / 101/101 pass | Survived; equivalent for the intact nine-operand loop, but undercounts are no longer refused. This is a guard-test gap, not a new ordinary status-vector failure. |
| M03 | Change `nlegs=9` to `nlegs=8` and remove the final `"$st_citecheck"` operand. `R:1430-1431` | 0 / 101/101 pass | 1 / `MUTATE_SELFTEST: 96/101 pass` | 0 / 101/101 pass | Killed; existing leg-count agreement and the exact extraction anchor both reject it. |
| M04 | Move the entire SETUP check before the FAIL check, preserving both bodies. `R:1439-1450` | 0 / 101/101 pass | 0 / `MUTATE_SELFTEST: 101/101 pass` | 0 / 101/101 pass | Survived; real detector gap: mixed failure/setup precedence changes. |
| M05 | Insert `[[ $st -eq 1 ]] && st=0` immediately inside the loop. `R:1431-1432` | 0 / 101/101 pass | 1 / `MUTATE_SELFTEST: 100/101 pass` | 0 / 101/101 pass | Killed; all nine singleton failure vectors are misclassified. |
| M06 | Change failure condition from `[[ $nfail -gt 0 ]]` to `[[ $nfail -eq 1 ]]`. `R:1439` | 0 / 101/101 pass | 0 / `MUTATE_SELFTEST: 101/101 pass` | 0 / 101/101 pass | Survived; real detector gap: two failing legs produce PASS. |
| M07 | Change setup condition from `[[ $nsetup -gt 0 ]]` to `[[ $nsetup -eq 1 ]]`. `R:1445` | 0 / 101/101 pass | 0 / `MUTATE_SELFTEST: 101/101 pass` | 0 / 101/101 pass | Survived; real detector gap: two setup legs produce PASS. |
| M08 | Insert `3) npass=$((npass + 1)) ;;` before the wildcard case arm. `R:1434-1435` | 0 / 101/101 pass | 0 / `MUTATE_SELFTEST: 101/101 pass` | 0 / 101/101 pass | Survived; real tally-surface detector gap: status 3 bypasses the existing wildcard SETUP behavior. This does not assert that a normal regression leg returns 3. |
| M09 | Change the guard predicate to `(( npass != nlegs ))`. `R:1454` | 0 / 101/101 pass | 0 / `MUTATE_SELFTEST: 101/101 pass` | 0 / 101/101 pass | Survived; equivalent rewrite. Both positive failure/setup counts have already exited, so the removed terms are zero whenever the guard is reached. |
| M10 | Change only the FAIL branch exit from `exit 1` to `exit 0`. `R:1443` | 0 / 101/101 pass | 1 / `MUTATE_SELFTEST: 100/101 pass` | 0 / 101/101 pass | Killed; the singleton failure vectors check exit status as well as the first line. |

Expected detector: the frozen selftest extracts the real tally and checks all-zero plus nine singleton status-1 and nine singleton status-2 vectors (`R:1992-2018`). A mutant differing on those vectors must fail; M03 additionally violates the existing nine-leg agreement (`R:1945-1954`). M04/M06/M07/M08 deliberately differ outside those 19 vectors. M01/M02 cannot be distinguished by any status vector while every loop iteration increments exactly one of the three counters, so the separate stress below is necessary to observe guard adequacy.

Actual failing detector lines:
```text
M03:
FAIL leg-count agreement: calls=9 specs=9 nlegs=8 (want 9)
FAIL tally harness: block extracted, leg status names=28 (want 9)
FAIL tally harness: all nine legs pass -> PASS passed=9, exit 0
FAIL tally harness: one leg status 1 at each of 9 positions -> REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0) (0/9)
FAIL tally harness: one leg status 2 at each of 9 positions -> REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1) (0/9)
MUTATE_SELFTEST: 96/101 pass
VERDICT: FAIL (scratch kept: /tmp/tameshi-r4-2-selftest.96hJfB)
M05:
FAIL tally harness: one leg status 1 at each of 9 positions -> REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0) (0/9)
MUTATE_SELFTEST: 100/101 pass
VERDICT: FAIL (scratch kept: /tmp/tameshi-r4-2-selftest.IJRpID)
M10:
FAIL tally harness: one leg status 1 at each of 9 positions -> REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0) (0/9)
MUTATE_SELFTEST: 100/101 pass
VERDICT: FAIL (scratch kept: /tmp/tameshi-r4-2-selftest.M4omr9)
```
Every other mutant printed `MUTATE_SELFTEST: 101/101 pass` and `VERDICT: PASS` with exit 0.

### Survivor witnesses and equivalence boundary

Status positions were independently taken from `run_regression` assignments before the tally: `st_js st_kagi st_tsu st_mado st_checklist st_claims st_roundgate st_sourcescheck st_citecheck`. A zero fills every unlisted position. The following bounded supplemental probe ran on pristine, mutated, and restored blocks; every restored observation matched pristine in exit code, complete stdout, and stderr. Every supplemental stderr was empty.

| Mutant | Witness | Pristine / restored exit and first line | Mutated exit and first line |
|---|---|---|---|
| M01 | `0 0 0 0 0 0 0 0 0; remove only the final tally operand in the in-memory harness` | 2; `REGRESSION: SETUP (case-tally mismatch: cases=9 counted=8)` | 0; `REGRESSION: PASS (cases=9 passed=8; ledger legs exact: killed-delta<=0 flips<=0)` |
| M02 | `0 0 0 0 0 0 0 0 0; remove only the final tally operand in the in-memory harness` | 2; `REGRESSION: SETUP (case-tally mismatch: cases=9 counted=8)` | 0; `REGRESSION: PASS (cases=9 passed=8; ledger legs exact: killed-delta<=0 flips<=0)` |
| M03 | `0 0 0 0 0 0 0 0 0` | 0; `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)` | 0; `REGRESSION: PASS (cases=8 passed=8; ledger legs exact: killed-delta<=0 flips<=0)` |
| M04 | `1 2 0 0 0 0 0 0 0` | 1; `REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)` | 2; `REGRESSION: SETUP (cases=9 passed=7 cannot-verify=1)` |
| M05 | `1 0 0 0 0 0 0 0 0` | 1; `REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)` | 0; `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)` |
| M06 | `1 1 0 0 0 0 0 0 0` | 1; `REGRESSION: FAIL (cases=9 passed=7 failed=2 setup=0)` | 0; `REGRESSION: PASS (cases=9 passed=7; ledger legs exact: killed-delta<=0 flips<=0)` |
| M07 | `2 2 0 0 0 0 0 0 0` | 2; `REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)` | 0; `REGRESSION: PASS (cases=9 passed=7; ledger legs exact: killed-delta<=0 flips<=0)` |
| M08 | `3 0 0 0 0 0 0 0 0` | 2; `REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)` | 0; `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)` |
| M09 | `0 0 0 0 0 0 0 0 0; remove only the final tally operand in the in-memory harness` | 2; `REGRESSION: SETUP (case-tally mismatch: cases=9 counted=8)` | 2; `REGRESSION: SETUP (case-tally mismatch: cases=9 counted=8)` |
| M10 | `1 0 0 0 0 0 0 0 0` | 1; `REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)` | 0; `REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)` |

Each supplemental stdout also contained exactly `REGRESSION_WORKDIR: extra-tally (kept)` as its second line. The extra-tally path is only a label: `auto=0 KEEP=1` prevents directory removal, and no directory was created for that label.

For M01/M02, deleting the final operand is a **second, explicitly declared stress**, not part of the mutant used for the selftest verdict. Their survival is therefore not presented as an ordinary nine-status regression failure. The stress demonstrates the precise completeness-guard detector omission: the original and restored guard refuse counted=8, whereas the removed/weakened guard prints PASS. M09 still refuses the same stress and is a true equivalent at this control-flow point (`R:1439-1459`).

The two-leg vectors and status 3 are outside the fixed 19. Four survivor witnesses therefore establish missing detector coverage, not a failure to meet the frozen finite-vector predicate.

The supplemental subprocess command used the same sandbox prefix above, followed by `--bind TREE /w --chdir /w timeout 20 bash -s`. Its stdin was assembled by the following exact probe logic (run in Python Eval, no helper file written):
```python
src = raw.decode()
start = re.search(r'^  local nlegs=\d+ npass=0 nfail=0 nsetup=0 st\n', src, re.M).start()
end = src.index('\n}\n', start) + 1
tb = src[start:end]
if spec['drop_last']:
    site = ' "$st_citecheck"; do\n'
    if tb.count(site) != 1:
        raise ValueError('drop stress site not unique')
    tb = tb.replace(site, '; do\n', 1)
decl = ' '.join(n+'='+str(s) for n,s in zip(status_names, spec['statuses']))
stdin = 'set -u -o pipefail\nfixed() {\n  local '+decl+'\n  local root=extra-tally auto=0 KEEP=1\n'+tb+'}\nfixed\n'
command = bwrap_prefix + ['--bind', str(tree), '/w', '--chdir', '/w', 'timeout', '20', 'bash', '-s']
p = subprocess.run(command, input=stdin, cwd=root, capture_output=True, text=True, timeout=40)
```

### Separation from public counter families

Inspected only the public `c1-measure-v4.py`: fixed arm mutants at lines 102-107, held-out drop/arm/threshold generator at 143-207, inserted constant arithmetic terms at 213-252, and plain drops at 387-405. These hand-made changes instead edit guard control flow, count-plus-topology together, verdict precedence, input normalization, equality thresholds that reject multi-leg outcomes, an extra status arm, or exit status. None is an exact output shape of those public mutant generators. M09 is intentionally an equivalent rewrite rather than a defect.

The sealed set was not opened, listed, searched, inferred, or recovered. No claim is made about matching an unknown sealed edit. The public counter sanity check requires sealed mutants to differ on at least one of its 19 vectors (`c1-measure-v4.py:409-417`); the surviving mixed/two-leg/status-3 mutants are identical on those 19 and are outside that discrimination surface. No counter or sweep was run.

### Before, mutated, and restored hashes

`P = 9a931bc2d0c31c32dd3a4ccf6594b56c3474628cca513b675901a8666fbec7d4`. Each `before` and `restored` entry below is the SHA-256 of the complete runner file, not just the tally. Restoration used inverse surgical edits, including restoring the moved block to its exact original position. Direct byte comparison to the preserved pristine bytes was true for all ten copies.

| Mutant | Before SHA-256 | Mutated SHA-256 | Restored SHA-256 | Exact bytes; restored detector |
|---|---|---|---|---|
| M01 | P | `32b98e7ec13ae33d8f0ac86f44bb4359c264de57906a5d4a6de99698b9cdbefb` | P | true; exit 0, `MUTATE_SELFTEST: 101/101 pass` |
| M02 | P | `a2d1f256b019609ca5f5eac604958d27f410efc6b3410d329a3a5fa574d61bda` | P | true; exit 0, `MUTATE_SELFTEST: 101/101 pass` |
| M03 | P | `cc748144ec5daf1f0e3ffdd8f68e6b6bb44a6d442bc442b269074490075d499e` | P | true; exit 0, `MUTATE_SELFTEST: 101/101 pass` |
| M04 | P | `e056c65dae1ec74b251eb8a73e0206502a1de9bd9bad3c1beec04ec7e7eeeae1` | P | true; exit 0, `MUTATE_SELFTEST: 101/101 pass` |
| M05 | P | `e0b0bbd9b71be967d4128d3aceb7516c59ca12755a04f61c8cafac247a6634e1` | P | true; exit 0, `MUTATE_SELFTEST: 101/101 pass` |
| M06 | P | `ecc72e4ff4ad647927e65d1ba265ad94a8796661cde760d736db223d92b575d7` | P | true; exit 0, `MUTATE_SELFTEST: 101/101 pass` |
| M07 | P | `712b7556070e1c4b1f8593d1c17f2d33676bea53bf3dc571fc2c7aeea1a3a14b` | P | true; exit 0, `MUTATE_SELFTEST: 101/101 pass` |
| M08 | P | `87f2f845f131439e2815a2307a6c11a43dc8c5929c36f8b324f8426d19bd5bcb` | P | true; exit 0, `MUTATE_SELFTEST: 101/101 pass` |
| M09 | P | `62ba9d53ab8c185f0f6648bce3849909264af235b5b21a5171e5040b0cfe0b5e` | P | true; exit 0, `MUTATE_SELFTEST: 101/101 pass` |
| M10 | P | `aec53af92c5bb3c1968c3b126146204be4fa6a653a529a8246141208b35a5d4f` | P | true; exit 0, `MUTATE_SELFTEST: 101/101 pass` |

The main scratch-clone `C/tools/mutate-and-run.sh` remained at P throughout. All subprocesses returned; no background services or persistent process trees were started. Bubblewrap namespaces ended with their commands. No production source, sibling repository, fleet state, or lane Git index was edited. No Git write command ran outside the assigned scratch clone. No subagent or model runtime was invoked. Tools installed or updated: none (existing `bubblewrap 0.13.1` was used).

## Smallest safe correction

No correction was applied: this seat is a mutation probe only. Keep the frozen contract unchanged. To close the demonstrated detector gaps in a later explicitly authorized change, extend the existing behavioral selftest with one mixed `1,2` vector (expect FAIL/1), one two-failure vector (FAIL/1), one two-setup vector (SETUP/2), and one status-3 vector (SETUP/2), checking both exact first line and exit. To exercise the new completeness guard, add an explicitly incomplete-count harness case that executes the actual guard and requires SETUP/2 rather than accepting only a failed outer selftest. Retain M09 as an equivalent-rewrite check; do not reject it merely for different text.

## Exact mutation diffs

These diffs record the transient bytes actually tested. Probe files now contain the restored frozen fix.

### M01

```diff
--- M01/pristine/tools/mutate-and-run.sh
+++ M01/mutated/tools/mutate-and-run.sh
@@ -1453,8 +1453,2 @@
   # of a mutation report are sums of its per-state counts).
-  if (( npass + nfail + nsetup != nlegs )); then
-    printf 'REGRESSION: SETUP (case-tally mismatch: cases=%s counted=%s)\n' \
-      "$nlegs" "$((npass + nfail + nsetup))"
-    printf 'REGRESSION_WORKDIR: %s (kept)\n' "$root"
-    exit 2
-  fi
   printf 'REGRESSION: PASS (cases=%s passed=%s; ledger legs exact: killed-delta<=0 flips<=0)\n' \
```

### M02

```diff
--- M02/pristine/tools/mutate-and-run.sh
+++ M02/mutated/tools/mutate-and-run.sh
@@ -1453,3 +1453,3 @@
   # of a mutation report are sums of its per-state counts).
-  if (( npass + nfail + nsetup != nlegs )); then
+  if (( npass + nfail + nsetup > nlegs )); then
     printf 'REGRESSION: SETUP (case-tally mismatch: cases=%s counted=%s)\n' \
```

### M03

```diff
--- M03/pristine/tools/mutate-and-run.sh
+++ M03/mutated/tools/mutate-and-run.sh
@@ -1429,4 +1429,4 @@
 
-  local nlegs=9 npass=0 nfail=0 nsetup=0 st
-  for st in "$st_js" "$st_kagi" "$st_tsu" "$st_mado" "$st_checklist" "$st_claims" "$st_roundgate" "$st_sourcescheck" "$st_citecheck"; do
+  local nlegs=8 npass=0 nfail=0 nsetup=0 st
+  for st in "$st_js" "$st_kagi" "$st_tsu" "$st_mado" "$st_checklist" "$st_claims" "$st_roundgate" "$st_sourcescheck"; do
     case $st in
```

### M04

```diff
--- M04/pristine/tools/mutate-and-run.sh
+++ M04/mutated/tools/mutate-and-run.sh
@@ -1438,2 +1438,8 @@
 
+  if [[ $nsetup -gt 0 ]]; then
+    printf 'REGRESSION: SETUP (cases=%s passed=%s cannot-verify=%s)\n' \
+      "$nlegs" "$npass" "$nsetup"
+    printf 'REGRESSION_WORKDIR: %s (kept)\n' "$root"
+    exit 2
+  fi
   if [[ $nfail -gt 0 ]]; then
@@ -1443,8 +1449,2 @@
     exit 1
-  fi
-  if [[ $nsetup -gt 0 ]]; then
-    printf 'REGRESSION: SETUP (cases=%s passed=%s cannot-verify=%s)\n' \
-      "$nlegs" "$npass" "$nsetup"
-    printf 'REGRESSION_WORKDIR: %s (kept)\n' "$root"
-    exit 2
   fi
```

### M05

```diff
--- M05/pristine/tools/mutate-and-run.sh
+++ M05/mutated/tools/mutate-and-run.sh
@@ -1431,2 +1431,3 @@
   for st in "$st_js" "$st_kagi" "$st_tsu" "$st_mado" "$st_checklist" "$st_claims" "$st_roundgate" "$st_sourcescheck" "$st_citecheck"; do
+    [[ $st -eq 1 ]] && st=0
     case $st in
```

### M06

```diff
--- M06/pristine/tools/mutate-and-run.sh
+++ M06/mutated/tools/mutate-and-run.sh
@@ -1438,3 +1438,3 @@
 
-  if [[ $nfail -gt 0 ]]; then
+  if [[ $nfail -eq 1 ]]; then
     printf 'REGRESSION: FAIL (cases=%s passed=%s failed=%s setup=%s)\n' \
```

### M07

```diff
--- M07/pristine/tools/mutate-and-run.sh
+++ M07/mutated/tools/mutate-and-run.sh
@@ -1444,3 +1444,3 @@
   fi
-  if [[ $nsetup -gt 0 ]]; then
+  if [[ $nsetup -eq 1 ]]; then
     printf 'REGRESSION: SETUP (cases=%s passed=%s cannot-verify=%s)\n' \
```

### M08

```diff
--- M08/pristine/tools/mutate-and-run.sh
+++ M08/mutated/tools/mutate-and-run.sh
@@ -1434,2 +1434,3 @@
       1) nfail=$((nfail + 1)) ;;
+      3) npass=$((npass + 1)) ;;
       *) nsetup=$((nsetup + 1)) ;;
```

### M09

```diff
--- M09/pristine/tools/mutate-and-run.sh
+++ M09/mutated/tools/mutate-and-run.sh
@@ -1453,3 +1453,3 @@
   # of a mutation report are sums of its per-state counts).
-  if (( npass + nfail + nsetup != nlegs )); then
+  if (( npass != nlegs )); then
     printf 'REGRESSION: SETUP (case-tally mismatch: cases=%s counted=%s)\n' \
```

### M10

```diff
--- M10/pristine/tools/mutate-and-run.sh
+++ M10/mutated/tools/mutate-and-run.sh
@@ -1442,3 +1442,3 @@
     printf 'REGRESSION_WORKDIR: %s (kept)\n' "$root"
-    exit 1
+    exit 0
   fi
```

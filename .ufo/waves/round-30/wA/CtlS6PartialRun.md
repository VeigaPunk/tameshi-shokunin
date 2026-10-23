CONTROL CtlS6PartialRun-11: v3_meets=true built=yes

## Verdict

The public v3 counter accepts this reduced-work control. Its selftest executes the extracted tally block under only the all-zero vector; it replaces the other 18 behavioral vectors with static checks of the nonzero counter arms and positive-count guards. A separate one-byte failure-exit mutant survived this detector. This is a coverage finding, not a change to the contract. No v4 result is claimed; L1 owns that measurement.

Axes considered: operability, coverage, and calibration. Byte fidelity is held fixed.

## Evidence

- Commit: `a934f99e93a35f2bac533ec4a90b02fe5c167290`.
- Clone: `/fast/scratch/hyaku/tameshi-r30a2-seats/CtlS6PartialRun-11/clone`.
- Patch: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/wA/CtlS6PartialRun-11.diff`.
- Runner SHA-256: `2daa1695f5fceef44cb0c6f0a6ffacba341515006cec5948cf1aa165f15e4c9e`.
- Tally block SHA-256: `e163133c0f54bb0cbd1c3f123e18b5efc17ced6df4558de034575089a8a2215d`, exactly the frozen fix's required value.

All runner line references below are relative to the clone. `tools/mutate-and-run.sh:1987-2006` extracts the tally and runs its single all-zero vector. `tools/mutate-and-run.sh:2007-2032` performs the static checks. The frozen tally remains at `tools/mutate-and-run.sh:1430-1468`. Only the frozen fix's selftest hunk was changed after applying the fix; its runtime completeness guard was retained unchanged.

### Construction and export

Executed from `/fast/scratch/hyaku`:

```sh
mkdir -p /fast/scratch/hyaku/tameshi-r30a2-seats/CtlS6PartialRun-11 && timeout -k 5 90 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r30a2-seats/CtlS6PartialRun-11/clone && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r30a2-seats/CtlS6PartialRun-11/clone checkout -q --detach f09d3425258403a51422c9959e25340807982947 && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r30a2-seats/CtlS6PartialRun-11/clone apply /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/witness/fix.diff
```

Observed: exit 0, no output. The scoped selftest edit and the mutation/restoration described below used the edit tool.

After restoration, executed from the clone:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git add -- tools/mutate-and-run.sh && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -c user.name=CtlS6PartialRun-11 -c user.email=ctls6partialrun-11@shokunin.local commit -q -m 'Control: one zero-vector tally run with static nonzero checks' -- tools/mutate-and-run.sh && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git rev-parse HEAD && sha256sum tools/mutate-and-run.sh && python3 -c "import hashlib,sys;t=open(sys.argv[1]).read();s=t.find('  local nlegs=9 npass=0 nfail=0 nsetup=0 st\n');e=t.find('\n}\n',s);print(hashlib.sha256(t[s:e+1].encode()).hexdigest())" tools/mutate-and-run.sh
```

Observed, exit 0:

```text
a934f99e93a35f2bac533ec4a90b02fe5c167290
2daa1695f5fceef44cb0c6f0a6ffacba341515006cec5948cf1aa165f15e4c9e  tools/mutate-and-run.sh
e163133c0f54bb0cbd1c3f123e18b5efc17ced6df4558de034575089a8a2215d
```

The exact patch output from this command was written to the patch path above:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git diff f09d3425258403a51422c9959e25340807982947 HEAD -- tools/mutate-and-run.sh
```

### Public v3 measurement

Executed from the clone. The sandbox makes the host read-only except this clone, maps the runner's hard-coded `/tmp` into the clone, and contains descendant processes in its own PID namespace:

```sh
timeout -k 5 1500 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE bwrap --ro-bind / / --bind /fast/scratch/hyaku/tameshi-r30a2-seats/CtlS6PartialRun-11/clone /fast/scratch/hyaku/tameshi-r30a2-seats/CtlS6PartialRun-11/clone --bind /fast/scratch/hyaku/tameshi-r30a2-seats/CtlS6PartialRun-11/clone/.r30tmp /tmp --proc /proc --dev /dev --unshare-pid --die-with-parent --chdir /fast/scratch/hyaku/tameshi-r30a2-seats/CtlS6PartialRun-11/clone env TMPDIR=/tmp python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/c1-measure-v3.py --repo /fast/scratch/hyaku/tameshi-r30a2-seats/CtlS6PartialRun-11/clone --rev a934f99e93a35f2bac533ec4a90b02fe5c167290 --jobs 4
```

Observed summary and captured process exit:

```text
C1_R30: rev=a934f99e93a35f2bac533ec4a90b02fe5c167290 pristine_selftest=1 harness=19/19 refused_drops=9/9 killed=13/13 equiv_pass=4/4 heldout_killed=12/12 heldout_equiv=4/4 insert_killed=8/8 insert_equiv=4/4
PREDICATE: C1_R30_PASS=true
V3_EXIT=0
```

The counter's external harness still runs its own 19 vectors. That does not change the control selftest's single-vector execution.

### Assigned mutation probe

Mutant: in the tally's failure branch, `tools/mutate-and-run.sh:1443`, replace `exit 1` with `exit 0`. This changes one byte. Expected semantic effect [INFERENCE]: a nonzero failure count still prints FAIL but returns success. A detector exercising a status-1 vector and checking its exit should reject it.

The same bounded detector command was run on pristine control bytes, mutant bytes, and restored control bytes, from the clone:

```sh
timeout -k 5 300 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE bwrap --ro-bind / / --bind /fast/scratch/hyaku/tameshi-r30a2-seats/CtlS6PartialRun-11/clone /fast/scratch/hyaku/tameshi-r30a2-seats/CtlS6PartialRun-11/clone --bind /fast/scratch/hyaku/tameshi-r30a2-seats/CtlS6PartialRun-11/clone/.r30tmp /tmp --proc /proc --dev /dev --unshare-pid --die-with-parent --chdir /fast/scratch/hyaku/tameshi-r30a2-seats/CtlS6PartialRun-11/clone bash tools/mutate-and-run.sh --selftest
```

Before the first run, `mkdir -p .r30tmp` created the private temporary directory. Actual outputs for each phase:

| Phase | Exit | Selftest summary | Verdict |
| --- | --- | --- | --- |
| Pristine control | 0 | `MUTATE_SELFTEST: 100/100 pass` | `VERDICT: PASS` |
| Failure-exit mutant | 0 | `MUTATE_SELFTEST: 100/100 pass` | `VERDICT: PASS` |
| Exact restoration | 0 | `MUTATE_SELFTEST: 100/100 pass` | `VERDICT: PASS` |

Each run also printed these exact detector lines:

```text
PASS tally harness: block extracted, leg status names=9 (want 9)
PASS tally harness: all nine legs pass -> PASS passed=9, exit 0
PASS tally static check: nonzero arms increment their counters and guards test positive
```

Verdict: **SURVIVED**. The baseline was green, so the result is not inconclusive.

Restoration evidence, obtained with `sha256sum tools/mutate-and-run.sh` and the tally-hash command above:

| Bytes | Runner SHA-256 | Tally block SHA-256 |
| --- | --- | --- |
| Before mutation | `2daa1695f5fceef44cb0c6f0a6ffacba341515006cec5948cf1aa165f15e4c9e` | `e163133c0f54bb0cbd1c3f123e18b5efc17ced6df4558de034575089a8a2215d` |
| Mutated | `e77cc4849d0606d8dead3c48f9cf4150984d3cd815d780618a2428066d0cbf60` | `fc4e1b75e49b5e3c93a261a8800708be86960b87b939a429df9d7dcc424bc271` |
| Restored and committed | `2daa1695f5fceef44cb0c6f0a6ffacba341515006cec5948cf1aa165f15e4c9e` | `e163133c0f54bb0cbd1c3f123e18b5efc17ced6df4558de034575089a8a2215d` |

The mutation was restored before committing or measuring v3. All bounded sandboxes returned; no persistent services were started. No sealed directory was opened, listed, searched, or read. Production code and lane indexes were not modified. No tools were installed or updated.

## Smallest safe correction

For the observed survivor, reinstate one status-1 behavioral vector asserting exit 1 and the exact FAIL line. The frozen witness's full 19-vector detector retains the intended per-position failure and setup coverage. These are recommendations only; the submitted control intentionally retains reduced work and does not change the contract.

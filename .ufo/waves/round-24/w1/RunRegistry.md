# RunRegistry — round24 W1 registry battery at c8c5b88

Axes (godspeed): A1 execution fidelity (exact prescribed argv/rev) · A2 evidence completeness (decisive lines per non-held row) · A3 calibration honesty (layout counterfactual before any defect claim).

## Verdict

Battery executed exactly as prescribed. Prescribed invocation: **exit 1, held=45/47, superseded=7**. Of the 47 counted rows, 2 active rows were not held (`mutate-and-run-regression`, `round21-measure-selftest`). Both failures were attacked and **overturned as revision defects**: they are artifacts of grading from a privately-named `/tmp` clone whose parent directory lacks the fleet-sibling layout. A layout-faithful counterfactual run of the identical battery holds **47/47, exit 0**. **No defect found at rev `c8c5b88c8e961a929cdc351b95a7074c76958909`; no row fails calibration under the intended fleet layout.**

## Run 1 — prescribed invocation

- argv: `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/registry-check.py --root /tmp/TameshiR24-2.RunRegistry-r24 --rev c8c5b88c8e961a929cdc351b95a7074c76958909 --json`
- cwd: `/tmp/TameshiR24-2.RunRegistry-r24` (private clone, `git clone --no-hardlinks` of the lane, `checkout -q --detach c8c5b88c8e961a929cdc351b95a7074c76958909`, `rev-parse HEAD` → `c8c5b88c8e961a929cdc351b95a7074c76958909`)
- exit: **1** (JSON `"exit": 1`; shell `EXIT_CODE=1`)
- decisive: `REGISTRY_CHECK: held=45/47 superseded=7`; JSON `total=47`, `rev_resolved=c8c5b88c8e961a929cdc351b95a7074c76958909`, `registry_sha256=a8f255f1c88fa32d75059c52a75229322796bfba7316798ba092ee18b10c8a0f` (clone's own `tools/registry.json`; no `--registry` passed)
- mirror used: `/tmp/tameshi-registry-check-barl72w9/fleet/TameshiR24-2.RunRegistry-r24` (mkdtemp, removed by the checker); wall time 110.4 s

### Rows not held (run 1) — 7

Counted (active), the only two that drive exit 1:

1. `mutate-and-run-regression` (registry.json:462) — expect=0, got=2, `stdout_missing: ["REGRESSION: PASS"]`. Full tail (artifact://1689 raw line 318): 6 of 8 ledger legs SETUP `repo_identity_mismatch: /tmp/tameshi-registry-check-barl72w9/fleet/{kumitate,tsukuroi,mado}-shokunin is not its own repository; toplevel=unresolved` (js-kimi-census, bash-tsukuroi-census, bash-mado-verify, js-claims-check, js-round-gate, js-sources-check); the 2 kagi legs passed (`REGRESSION_CASE bash-surface-census: PASS`, `REGRESSION_CASE bash-checklist-run: PASS`) because `/tmp/kagi-shokunin` existed and was symlinked into the mirror. Final `REGRESSION: SETUP (cases=8 passed=2 cannot-verify=6)` → exit 2 per tools/mutate-and-run.sh:1370-1374; guard at tools/mutate-and-run.sh:1119-1123.
2. `round21-measure-selftest` (registry.json:875) — expect=0, got=1, needle `ROUND21_MEASURE_SELFTEST: 13/13 pass` missing. Direct reproduction stderr: `subprocess.CalledProcessError: Command '['git', '-C', '/tmp/tameshi-shokunin', 'show', '08175c62d661fddf052ed10abc91313dec8eb77d:tools/mutate-and-run.sh']' returned non-zero exit status 128` (tools/round21-measure.py:74 via :151 via :162; `ROOT = Path(__file__).resolve().parents[1]`, surface pinned at .ufo/evidence/round-21/c2-contract.json:25). `/tmp/tameshi-shokunin` does not exist (`/tmp/*-shokunin` glob → only `/tmp/kagi-shokunin`).

Superseded rows that ran red (still executed, excluded from N/M by design — registry-check.py:30-34):

3. `evidence-disposition-round17` → superseded_by `evidence-disposition-round18` — expect=0 got=2, `expected_input_digest_mismatch` on `tools/bash-witness-study.py` (observed 60575e62… expects frozen 49e9e5e2…).
4. `evidence-disposition-round17-before` → `evidence-disposition-round18-before` — expect=1 got=2, same digest mismatch.
5. `evidence-disposition-round14-superseded` → `evidence-disposition-round18` — expect=0 got=2, same.
6. `command-binding-selftest` → `command-binding-selftest-r24` — expect=0 got=0, needle `COMMAND_BINDING_SELFTEST: 38/38 pass` absent (the r24 selftest loads a second fixture file and its output line changed); its pinned successor `command-binding-selftest-r24` held.

(7th superseded row `trace-inputs-round17-selftest` held but is likewise excluded from N/M.)

## Root cause (run-1 failures 1 and 2)

tools/registry-check.py `clone_lane_at_rev` (:756-782): `fleet_root = dirname(realpath(--root))`; it symlinks every `*-shokunin` sibling of that directory (excluding the lane itself) into the mirror and clones the lane under `basename(root_real)`. With `--root /tmp/TameshiR24-2.RunRegistry-r24` the mirror fleet/ therefore contains only `kagi-shokunin` (the sole `*-shokunin` entry in `/tmp`) plus the lane clone named `TameshiR24-2.RunRegistry-r24` — `fleet/tameshi-shokunin` and `fleet/{kumitate,tsukuroi,mado}-shokunin` cannot exist, whatever the revision contains. Under the intended invocation (`--root /home/vgpnk/Projects/shokunin/tameshi-shokunin`) the parent supplies all sibling lanes and the `tameshi-shokunin` basename.

## Run 2 — layout-faithful counterfactual

Identical argv except `--root /tmp/TameshiR24-2.RunRegistry-r24/.probe/fleet/tameshi-shokunin` — a detached clone of my clone at the same rev, built inside my own clone tree, with sibling symlinks `kumitate/tsukuroi/mado/kagi-shokunin → /home/vgpnk/Projects/shokunin/*-shokunin` (read-only git access only: rev-parse/cat-file/show/ls-tree/clean checks; sweeps mutate materialized copies in `/tmp` scratch, never the source lanes).

- cwd: `/tmp/TameshiR24-2.RunRegistry-r24/.probe/fleet/tameshi-shokunin`
- exit: **0**; decisive (`/tmp/TameshiR24-2.RunRegistry-r24/.probe/probe-stderr.txt`):
  - `:21 ROW mutate-and-run-regression expect=0 got=0 held`
  - `:43 ROW round21-measure-selftest expect=0 got=0 held`
  - `:55 REGISTRY_CHECK: held=47/47 superseded=7`
  - zero occurrences of `repo_identity_mismatch` / `toplevel=unresolved` / `CalledProcessError`
- wall time 188.8 s; probe clones removed afterwards (log retained)

## Falsification summary

- Attacked: the two counted non-held rows named by the battery. Counterexample (run 2) overturns both as revision defects; concrete mechanism above. None of the 47 counted rows fails at c8c5b88 under the fleet-faithful layout.
- Also checked: the 4 red superseded rows are frozen-input drift independent of layout (old-round digest pins on `tools/bash-witness-study.py`; changed selftest output line) and each has a pinned/updated successor that held — consistent with the wave's supersession design, not defects.

## Smallest safe correction

No production change warranted. To measure the revision at full strength, grade with `--root` at a fleet-layout path (e.g. the live lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`) so the mirror obtains the sibling symlinks and the `tameshi-shokunin` basename; optionally registry-check could warn when `fleet_root` lacks expected `*-shokunin` siblings — not implemented here (no production edits authorized for this seat).

## Compliance notes

- Writes: `/tmp/TameshiR24-2.RunRegistry-r24/**` (clone, probe, logs) and this report only. Fleet repo untouched except read-only inspection; no git/jj write commands run in the fleet checkout; no installs performed (python3/git sufficed).
- Scope: producer authentication, promotion, R17-CMD-BIND closure, and numeric score uplift not claimed.

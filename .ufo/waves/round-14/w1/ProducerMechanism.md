# Round 14 w1 — ProducerMechanism: exact failure mechanism vs path-layout crash

Seat: `TameshiR14.ProducerMechanism` (scout, leaf member).
Role: Read-only research seat.
Assignment: Inspect exact `producer_before` crash versus `producer_before_oracle` failure and `producer_after_oracle` pass. Identify stable literal evidence showing mechanism and what exit-only cannot prove. Read outputs without executing tools.
Destination: `.ufo/waves/round-14/w1/ProducerMechanism.md`
Tool installs/updates: none.
Mid-flight checks: none (no test, gate, selftest, or runner executed).

---

## 1. Axes in scope

- **Calibration (primary):** Distinguish accidental relocation/infrastructure crash from true semantic regression. Prevent false credit for exit-only matching (`exit == 1`). Ensure that before-repair "red" evidence exercises and fails the exact targeted defect rather than an unhandled environment exception.
- **Depth:** Ground the single-delta fix (`declaration.get("declared", {}).get("kind")` → `declaration.get("kind")`) with digest-anchored files, exact line numbers, and literal stdout/stderr evidence demonstrating cause and effect.
- **Coverage, Operability, Freshness, Adjacency:** Unchanged / unaffected.

---

## 2. Comparison of the three observations

All observations are read directly from committed round-13 evidence files without tool execution:
- Historical receipt: `.ufo/evidence/round-13/verification.json`
- Historical repair receipt: `.ufo/evidence/round-13/producer-oracle-repair.json`
- Historical expectation: `.ufo/evidence/round-13/expected.json`
- Historical verdict: `.ufo/evidence/round-13/verification-verdict.json`

| Dimension | `producer_before` (retained raw) | `producer_before_oracle` (effective replacement) | `producer_after_oracle` (effective replacement) |
|---|---|---|---|
| **Receipt file** | `verification.json` (lines 81–98) | `producer-oracle-repair.json` (lines 7–24) | `producer-oracle-repair.json` (lines 25–42) |
| **Command / argv** | `["python3", ".ufo/evidence/round-13/producer-before.py", "selftest"]` | `["python3", ".ufo/evidence/round-13/producer-oracle.py", "--source", ".ufo/evidence/round-13/producer-before.py", "--runner", "tools/mutate-and-run.sh"]` | `["python3", ".ufo/evidence/round-13/producer-oracle.py", "--source", "tools/bash-witness-study.py", "--runner", "tools/mutate-and-run.sh"]` |
| **Started at (UTC)** | `2026-10-20T04:59:26.753309+00:00` | `2026-10-20T05:00:00.756121+00:00` | `2026-10-20T05:00:00.820293+00:00` |
| **Exit code** | `1` (`expected_exit: 1`, `exit_matches: true`) | `1` (`expected_exit: 1`, `exit_matches: true`) | `0` (`expected_exit: 0`, `exit_matches: true`) |
| **Stderr status** | Unhandled `FileNotFoundError` traceback | `""` (clean) | `""` (clean) |
| **Stdout terminal check** | Truncated after check 34 (`mutant digest mismatch refuses ok`) | Check 39: `summary preserves top-level exposed declaration kind FAIL` | Check 39: `summary preserves top-level exposed declaration kind ok` |
| **Stdout summary** | None (crashed before reaching summary) | `WITNESS_SELFTEST: 40/41 pass`<br>`VERDICT: FAIL` | `WITNESS_SELFTEST: 41/41 pass`<br>`VERDICT: PASS` |
| **Target assertion executed?** | **NO** (never reached) | **YES** (evaluated and failed) | **YES** (evaluated and passed) |
| **Mechanism proven?** | **NO** (path-layout relocation crash) | **YES** (true semantic defect) | **YES** (true semantic repair) |

---

## 3. Detailed mechanism analysis

### A. The `producer_before` relocation crash

In `producer-before.py`:
- Line 93: `REPO = Path(__file__).resolve().parent.parent`
- Line 95: `RUNNER = REPO / "tools" / "mutate-and-run.sh"`

When `bash-witness-study.py` was located at `<lane_root>/tools/bash-witness-study.py`, `__file__.resolve().parent.parent` evaluated to `<lane_root>`, so `RUNNER` was `<lane_root>/tools/mutate-and-run.sh`.

However, when snapshot into `.ufo/evidence/round-13/producer-before.py`:
- `__file__.resolve()` = `<lane_root>/.ufo/evidence/round-13/producer-before.py`
- `.parent` = `<lane_root>/.ufo/evidence/round-13`
- `.parent.parent` (`REPO`) = `<lane_root>/.ufo/evidence`
- `RUNNER` = `<lane_root>/.ufo/evidence/tools/mutate-and-run.sh` (non-existent path!)

During `cmd_selftest` at line 1478 (check 35 full-manifest check fixture setup):
```python
1478: "runner": {"sha256": sha256_file(RUNNER)},
```
At line 218 in `sha256_file`:
```python
218: with open(path, "rb") as fh:
```
This raised:
```text
FileNotFoundError: [Errno 2] No such file or directory: '/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/tools/mutate-and-run.sh'
```
Because this exception was uncaught, Python terminated immediately with exit code 1.
The execution halted between check 34 and check 35. Checks 35 through 41 were **never executed**.
Specifically, check 39 (`summary preserves top-level exposed declaration kind` at lines 1542–1544) was never reached.

### B. The `producer_before_oracle` semantic failure

The harness `producer-oracle.py` (lines 13–20) isolates the runner in a temporary directory:
```python
with tempfile.TemporaryDirectory(prefix='tameshi-r13-producer-oracle-') as d:
    tools = pathlib.Path(d) / 'tools'
    tools.mkdir()
    shutil.copyfile(a.source, tools / 'bash-witness-study.py')
    shutil.copyfile(a.runner, tools / 'mutate-and-run.sh')
    result = subprocess.run([sys.executable, str(tools / 'bash-witness-study.py'), 'selftest'])
    sys.exit(result.returncode)
```
In this layout, `tools/bash-witness-study.py` resolves its `.parent.parent` to the temp directory root `d`, where `tools/mutate-and-run.sh` exists.
Checks 1 through 38 all pass.

At check 39 (lines 1537–1544 of `producer-before.py`):
```python
1537: qsummary = build_summary(
1538:     qev, {"kind": "declared-witness mapping (not a blind preregistration)",
1539:           "declared": {"sha256": qdigest}, "inputs": {}}, qdigest,
1540:     {"target_sha256": "a" * 64},
1541:     {"exit": 0, "cli_log": "sweep/cli.log"}, qctl, qrows, "complete")
1542: check("summary preserves top-level exposed declaration kind",
1543:       qsummary["declaration"]["kind"] ==
1544:       "declared-witness mapping (not a blind preregistration)")
```
In `producer-before.py` line 787:
```python
787: "kind": declaration.get("declared", {}).get("kind"),
```
Because the input declaration has `"kind"` at the top level and `"declared"` contains only `{"sha256": qdigest}`, `declaration.get("declared", {}).get("kind")` evaluates to `None`.
Consequently:
```python
qsummary["declaration"]["kind"] == "declared-witness mapping (not a blind preregistration)"
```
evaluates to `None == "declared-witness mapping..."`, which is `False`!

The test framework logs:
```text
  check summary preserves top-level exposed declaration kind FAIL
```
and increments `failed` by 1.
Checks 40 and 41 pass.
Final lines:
```text
WITNESS_SELFTEST: 40/41 pass
VERDICT: FAIL
```
The script returns `EXIT_FAIL` (exit code 1).
This proves the exact semantic bug: `build_summary` failed to preserve the top-level declaration kind.

### C. The `producer_after_oracle` semantic pass

In `tools/bash-witness-study.py` line 787, the getter is corrected:
```python
787: "kind": declaration.get("kind"),
```
Under the same `producer-oracle.py` harness:
- `declaration.get("kind")` retrieves `"declared-witness mapping (not a blind preregistration)"`.
- At check 39, `qsummary["declaration"]["kind"] == "declared-witness mapping..."` evaluates to `True`.
- Check 39 logs:
  ```text
    check summary preserves top-level exposed declaration kind ok
  ```
- All 41 checks pass (`failed == 0`).
- Final lines:
  ```text
  WITNESS_SELFTEST: 41/41 pass
  VERDICT: PASS
  ```
- The script returns `EXIT_OK` (exit code 0).

---

## 4. Stable literal evidence

### A. SHA-256 Digest anchors
- `producer-before.py`: `592c5c3de86a684fbb694d3aa8dd4c1e2b62263e7a50d72a9169092ad3fab9a0`
- `producer-oracle.py`: `d5ae0bd4d4f75a461e7105b63eb737d249c3d09ffc15a3bfeb7aecea21ccd38b`
- `tools/bash-witness-study.py` (live/delivered): `49e9e5e20b73f115626fb4f81aac9b238e0f01811230c4fd0ff726c1f350ad80`
- Historical producer (round 12 frozen): `249d9dcd2dfb410f7e6847989da2cb3ab6ef7dd693b87ec2b9b4d6b193d43f1a`
- `tools/mutate-and-run.sh`: `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`

### B. Code delta between `producer-before.py` and `tools/bash-witness-study.py`
The exact single delta at line 787:
```diff
--- .ufo/evidence/round-13/producer-before.py
+++ tools/bash-witness-study.py
@@ -787,1 +787,1 @@
-            "kind": declaration.get("declared", {}).get("kind"),
+            "kind": declaration.get("kind"),
```

### C. Exact literal stdout/stderr strings
- `producer_before` stderr:
  `FileNotFoundError: [Errno 2] No such file or directory: '/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/tools/mutate-and-run.sh'`
- `producer_before_oracle` stdout:
  `  check summary preserves top-level exposed declaration kind FAIL\n  check count recomputes rows and matches summary    ok\n  check count refuses summary/raw mismatch           ok\nWITNESS_SELFTEST: 40/41 pass\nVERDICT: FAIL\n`
- `producer_after_oracle` stdout:
  `  check summary preserves top-level exposed declaration kind ok\n  check count recomputes rows and matches summary    ok\n  check count refuses summary/raw mismatch           ok\nWITNESS_SELFTEST: 41/41 pass\nVERDICT: PASS\n`

---

## 5. What exit-only cannot prove

1. **Accidental exit 1 vs. semantic failure:**
   Both `producer_before` and `producer_before_oracle` produce exit code 1.
   Under an exit-only check (`rc == 1` or `{"exit": 1}`), a path resolution crash (`FileNotFoundError`), a syntax error, a missing dependency, or a segmentation fault is completely indistinguishable from an intentional assertion failure that proves the defect.
2. **Predicate violation in raw receipt:**
   In `expected.json`:
   ```json
   "producer_before": {
     "exit": 1,
     "contains": "summary preserves top-level exposed declaration kind"
   }
   ```
   In `verification.json`, `producer_before` satisfied `"exit": 1`, but **failed the `contains` expectation** because the process died at check 34 and never printed the assertion text. An exit-only checker would have marked this as a pass, falsely claiming verification.
3. **What honest verification requires:**
   - **Clean execution environment:** `stderr == ""` and zero unhandled exceptions.
   - **Discriminating failure assertion:** stdout contains the exact failure tag (`... FAIL`).
   - **Denominator integrity:** all other assertions in the suite pass (e.g. `40/41 pass`), proving that the failure is isolated strictly to the targeted defect.
   - **Symmetric repair pass:** the identical runner with the single delta passes completely (`41/41 pass`, `... ok`, exit 0).

---

## 6. Concrete changes and risks for Round 14

### Concrete Changes
1. **Contract cardinality clarification:**
   `expected.json` has **12** `expected_checks` keys (not 13):
   - 11 effective checks: `pin_selftest`, `metadata_selftest`, `metadata_old_null`, `metadata_corrected`, `producer_before_oracle`, `producer_after_oracle`, `producer_after`, `witness_check`, `witness_count`, `pin_live`, `source_census`.
   - 1 superseded check: `producer_before`.
   (The number "13" in earlier prompt text conflated the 13 `expected.json.inputs` or the 13 checks in `verification.json`).
2. **Explicit supersession record:**
   `dispositions.json` must record `producer_before` with state `superseded`, citing `reason: "path-layout FileNotFoundError before target assertion"` and `superseded_by: ["producer_before_oracle", "producer_after_oracle"]`.
   The gate must require both replacement checks to be effective and to pass their original frozen expectations.
3. **Structured predicate enforcement:**
   `evidence-disposition.py` must parse receipts and evaluate predicates (`exit`, `contains`, `id`, `reason`) from stdout, without executing any receipt argv.

### Risks
1. **Stale expectation evaluation on raw row:**
   If `evidence-disposition.py` attempts to apply the frozen `contains` predicate to raw `producer_before`, it will fail because the string is absent from `verification.json`. The gate specification must explicitly bypass the original `contains` predicate for superseded rows whose superseding replacements pass.
2. **Raw evidence deletion or rewriting:**
   The raw `producer_before` run in `verification.json` must be retained verbatim. It must not be deleted or rewritten; supersession is an audit overlay, not a historical redaction.

---

## 7. Checks L1 should run (deferred to L1)

1. Verify `evidence-disposition.py` isolated selftest:
   ```sh
   python3 tools/evidence-disposition.py --selftest
   ```
   Must exit 0 with clean fixture output.
2. Verify dispositions against lane evidence:
   ```sh
   python3 tools/evidence-disposition.py --root /home/vgpnk/Projects/shokunin/tameshi-shokunin --dispositions .ufo/evidence/round-14/dispositions.json --json
   ```
   Must exit 0, reporting all 11 effective expectations satisfied and `producer_before` superseded by `producer_before_oracle` and `producer_after_oracle`.
3. Verify digest integrity of input receipts:
   Confirm SHA-256 digests of `expected.json`, `verification.json`, `producer-oracle-repair.json`, `producer-before.py`, and `producer-oracle.py` match pinned values.
4. Verify no receipt argv was executed during disposition checking.

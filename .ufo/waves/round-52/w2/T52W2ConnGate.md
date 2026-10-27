# UFO-FSD Connector Report — Round 52 Wave 2 (Seat T52W2ConnGate)

## 1. Goal & Named Axes

- **Seat**: `T52W2ConnGate`
- **Milestone**: Recurrence -> Gate
- **Target**: Synthesize `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-52/w1/T52W1ScoutRecurrence.md` into one `QUALITY.md` criterion draft for `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/QUALITY.md` addressing the recurring defect class: *"a tool's behaviour changed while its registered gate row or SKILL statement did not"* (R47.1, R51.1).
- **Axes Named**:
  - **Operability** (Harmed at round 51 by R51.1; target of Claim C1): Ensures registered entry gates remain executable and satisfiable across revisions.
  - **Calibration** (Lowest non-retired numeric axis at 8; target of Claim C2): Ensures recorded statements, leg counts, and gate expectations accurately reflect code reality without `cannot_see` blind spots.
  - **Depth** (10): Preserves comprehensive test/leg panels.
  - **Freshness** (9): Preserves monitor population standards.

---

## 2. Evidence & Citations

Every finding below names `file:line` and the exact shell command that demonstrates it.

### Finding 1: Recurrence Class & Gate Inadequacy
- **File & Line**: `tameshi-shokunin/.ufo/waves/round-52/w1/T52W1ScoutRecurrence.md:8,15-20`
- **Command**:
  ```bash
  sed -n '8p;15,20p' /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-52/w1/T52W1ScoutRecurrence.md
  ```
- **Evidence**:
  Row 8 documents that tool behavior vs registered gate drift occurred in round 47 (fixed in round 48 via `routed-defects.json:606-627`) and recurred in round 51 (R51.1). Lines 15–20 establish that R51.1 occurred because implementation growth changed `tools/mte-interop.py`'s observable leg count while its registered expectation remained `9/9`. The analysis explicitly notes that a prose reminder is insufficient; only an operational registry replay at candidate revision enforces agreement.

### Finding 2: Precedent Drift Defect R47.1
- **File & Line**: `tameshi-shokunin/corpus/lessons/round-47-verifier-spotcheck.md:103` and `tameshi-shokunin/corpus/routed-defects.json:606-628`
- **Commands**:
  ```bash
  sed -n '103p' /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-47-verifier-spotcheck.md
  sed -n '606,628p' /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/routed-defects.json
  ```
- **Evidence**:
  Round-47 verifier spot-check defect 1 routed: `C1 standing row: append a superseding row for six-leg regression ledger stating the stable observation ... hermetic env-differential probe printed 9/9 and 2/9 under one profile and needs the same treatment`. In `routed-defects.json`, R47.1 records the fix committed in `c7586b9a` by restating rows from repeated runs with declared stable classes.

### Finding 3: Recurred Operability Harm R51.1
- **File & Line**: `tameshi-shokunin/corpus/lessons/round-51-verifier-spotcheck.md:84-88,126`
- **Command**:
  ```bash
  sed -n '84,88p;126p' /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-51-verifier-spotcheck.md
  ```
- **Evidence**:
  The round-51 closure spot-check confirms: `tools/registry.json` remained unchanged base to tip while `tools/mte-interop.py` added `bash-drift-pins` to `LEG_TABLE` (`:75-78`), outputting `10/10` and making active registered row `mte-interop-check` (expecting `9/9`) unsatisfiable at REV. Furthermore, `SKILL.md:2136` still read "nine ledger legs". Routed defect 1 mandated updating the row to the ten-leg panel and demonstrating `registry-check` green with a committed receipt.

### Finding 4: Base Failure Receipt (Able to Fail)
- **File & Line**: `tameshi-shokunin/.ufo/evidence/round-52/control/C1_CTL_0.stdout:1-4,36`
- **Command**:
  ```bash
  sed -n '1,4p;36p' /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-52/control/C1_CTL_0.stdout
  ```
- **Evidence**:
  Replay of `tools/registry-check.py` against base revision `ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4` demonstrates failure:
  `C1_REGISTRY_CHECK exit=1 summary=48/49 not_held=['mte-interop-check']`
  `C1_MTE_ROW BAD legs=10 want='MTE_INTEROP: PASS legs_conforming=10/10' status=active needles=['MTE_INTEROP: PASS legs_conforming=9/9']`
  `C1_R52: rev=ef19d8e1... held=48/49 not_held=2 ... C1_R52_PASS=false`.

### Finding 5: Positive Control Receipt (Able to Pass)
- **File & Line**: `tameshi-shokunin/.ufo/evidence/round-52/control/C1_CTL_POSITIVE.stdout:1-4,36`
- **Command**:
  ```bash
  sed -n '1,4p;36p' /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-52/control/C1_CTL_POSITIVE.stdout
  ```
- **Evidence**:
  Under control revision `63b12e8c75dbcc1f3a795c14704ec6bb2c29056d`, the synchronized tool and registry pass cleanly:
  `C1_REGISTRY_CHECK exit=0 summary=49/49 not_held=[]`
  `C1_MTE_ROW ok legs=10 want='MTE_INTEROP: PASS legs_conforming=10/10' status=active needles=['MTE_INTEROP: PASS legs_conforming=10/10']`
  `C1_R52: rev=63b12e8c... held=49/49 not_held=0 ... total=0 C1_R52_PASS=true`.

### Finding 6: Sibling Fleet Closure & Routing Connections
- **File & Line**: `tameshi-shokunin/.ufo/waves/round-52/w1/T52W1ConnSibling.md:12-49`
- **Command**:
  ```bash
  sed -n '12,49p' /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-52/w1/T52W1ConnSibling.md
  ```
- **Evidence**:
  The sibling scan reveals four cross-lane instances of this exact defect class:
  1. `kotodama-shokunin` (`SKILL.md:661`): `tools/check-gate-battery.py` added `register-law-gate.py` in `11df1fd5` moving coverage from `9/9` to `10/10`, while `SKILL.md:661` pinned `9/9`.
  2. `kengaku-shokunin` (`SKILL.md:609`): `plans/gate_flip_check.py` added 8 test fixtures in commit `02287ee` (moving selftest from `19/19` to `27/27` in response to round-43 verifier spot-check R1 routing at `round-43-verifier-spotcheck.md:160`), while `SKILL.md:609` remained pinned at `19/19`.
  3. `kake-shokunin` (`SKILL.md:1274`): `scripts/id_resolver.py` moved from 49 checks to 72, while `SKILL.md:1274` documented 49/59.
  4. `chousa-shokunin` (`SKILL.md:130,136`): `tools/assimilate-rows.py` moved from 27/27 (5 legs) to 40/40 (8 legs), resolved cleanly by appending a superseding row at line 136 (`assimilate-rows (v4, round 53)`).

---

## 3. Second-Order Analysis & Non-Obvious Move

### Contradiction
- **Rigid Needles vs Operability**: Rigidly pinning literal counts (`N/N`) catches regressions but breaks candidate operability whenever a tool is enhanced or expanded without simultaneously updating registry rows (R47.1, R51.1).
- **Loose Needles vs Calibration**: Loosening needles to generic success tokens (`REGRESSION: PASS`, e.g. `mutate-and-run-regression` in `tools/registry.json:982`) prevents spurious gate failures, but introduces a calibration blind spot (`cannot_see`) where dropped legs or muted assertions pass unnoticed.
- **Notes Fail**: A prose instruction ("remember to update registry rows") routinely fails under delivery pressure across all lanes.

### The Non-Obvious Move: Mechanical Co-Commit Gate
Synthesize an automated admission gate (Criterion 103) that couples:
1. Operational replay of every active registry row at the candidate commit using `python3 tools/registry-check.py --rev REV`.
2. Static AST extraction and diffing of tool leg tables (e.g., `LEG_TABLE` in `tools/mte-interop.py`) against `SKILL.md` leg-count statements.
3. Requiring intentional supersession rows (the `chousa-shokunin` pattern) when historical registry entries must be preserved.

### Second-Order Effects Across Surfaces:
- **Runtime Surface**: Replay under `--rev` executes inside an isolated clone with fleet-mirror symlinks, guaranteeing that gate evaluation is hermetic and immune to working tree artifacts.
- **Contract Surface**: Guarantees that the lane's external commitments (`tools/registry.json` and `SKILL.md`) change in lockstep with internal tool semantics.
- **Substrate Surface**: Machine-readable JSON registries remain authoritative, preventing doc/code divergence.
- **Verification Surface**: Fast, deterministic, pre-commit or pre-deciding gate checks with unambiguous pass/fail exits.

---

## 4. Deliverable: QUALITY.md Criterion Draft

The following draft matches the format and numbering of `corpus/QUALITY.md` (following Criterion 102):

```markdown
## Criteria appended — round 52 (2026-10-27)

### Criterion 103 — a tool change co-commits its registered gate row and SKILL statement

A tool's implementation and its registered gate contract are one commit surface. Whenever a tool's observable behavior, output format, or internal panel (such as leg count or fixture tally) changes, the candidate commit must co-commit the matching expected outcome in `tools/registry.json` (or mark the previous row superseded by a new active row) and synchronize every leg/count assertion in `SKILL.md`. A tool improvement must never leave a standing gate unsatisfiable or a documented leg count stale.

Check that can fail: at candidate revision `REV`, run `python3 tools/registry-check.py --rev REV` across all active rows in `tools/registry.json`, and parse `SKILL.md` leg/count statements against the tools' internal tables (including `len(LEG_TABLE)` in `tools/mte-interop.py`). The check passes with exit 0, `held=N/N`, `not_held=[]`, and zero mismatched phrases in `SKILL.md`. It fails with exit 1 if any active row differs from its registered expectation or if any documented leg/count statement diverges from the tool's implementation.

Lesson: `corpus/lessons/round-52.md` `## Mistakes` row 1; `corpus/lessons/round-51-verifier-spotcheck.md:84-88,126` (defect R51.1: `mte-interop.py` grew to 10 legs while `tools/registry.json` pinned `9/9` and `SKILL.md:2136` pinned "nine ledger legs"); `corpus/lessons/round-47-verifier-spotcheck.md:103` (defect R47.1: `six-leg regression ledger` and `env-differential probe` drift, fixed in `corpus/routed-defects.json:606-628`). Cross-lane instances: `kotodama-shokunin` `SKILL.md:661` (`check-gate-battery.py` 9/9→10/10), `kengaku-shokunin` `SKILL.md:609` (`gate_flip_check.py` 19/19→27/27, routed from `round-43-verifier-spotcheck.md:160`), `kake-shokunin` `SKILL.md:1274` (`id_resolver.py` 49→72), and `chousa-shokunin` `SKILL.md:130,136` (superseded row pattern).

Falsifier that must fail: at base revision `ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4`, `tools/registry-check.py --rev` exits 1 with `REGISTRY_CHECK: held=48/49` and `not_held=['mte-interop-check']`, where the tool prints `legs_conforming=10/10` against an active expectation of `9/9` (receipt `.ufo/evidence/round-52/control/C1_CTL_0.stdout:1-4`); under positive control revision `63b12e8c75dbcc1f3a795c14704ec6bb2c29056d`, the check exits 0 with `held=49/49` and `not_held=[]` (receipt `.ufo/evidence/round-52/control/C1_CTL_POSITIVE.stdout:1-4`).
```

---

## 5. Risks & Verification

- **Risks**:
  - *Fleet Dependencies*: If a tool invoked by `registry-check.py` resolves sibling repositories (e.g. through `ROOT.parent`), running outside a fleet mirror layout could fail rows spuriously.
  - *Mitigation*: `registry-check.py --rev` already automatically constructs a temporary fleet mirror (`mkdtemp` populated with sibling symlinks) before executing rows in the isolated clone.
- **Verification**:
  - Base failure verified: `C1_CTL_0.stdout` (`held=48/49`, `not_held=['mte-interop-check']`).
  - Positive resolution verified: `C1_CTL_POSITIVE.stdout` (`held=49/49`, `not_held=[]`).

---

## Summary
- Analyzed recurrence of tool behavior vs gate/SKILL drift (R47.1 in round 47; R51.1 in round 51).
- Identified sibling occurrences across `kotodama` (battery), `kengaku` (flip-check), and `kake` (resolver).
- Formulated Criterion 103 for `corpus/QUALITY.md` enforcing co-commitment of gates and docs.
- Defined check via `python3 tools/registry-check.py --rev REV` and tool AST leg-table diffing.
- Cited failure receipt at base `ef19d8e1` (`C1_CTL_0.stdout`: `held=48/49`, `not_held=['mte-interop-check']`).
- Cited passing receipt at control `63b12e8c` (`C1_CTL_POSITIVE.stdout`: `held=49/49`, `not_held=[]`).
- Connected lesson pointers to `corpus/lessons/round-52.md` and closures of rounds 47 and 51.
- Synthesized move resolves the tension between rigid calibration and candidate operability.

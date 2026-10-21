# F02 — Sibling QUALITY.md Scan & UFO-FSD Connector Report

## Scope & Target
Scan all 20 sibling `corpus/QUALITY.md` files across `/home/vgpnk/Projects/shokunin/*-shokunin/corpus/QUALITY.md` for:
1. An in-wave instrument-edit rule or staging requirement.
2. A receipt-provenance criterion.
Report matches, gaps, and exactly one sentence assessing whether `tameshi` is ahead or behind.
Synthesize the findings into one bounded non-obvious move improving the declared round axis (C1 Calibration, lane cap 8) without harming another. Read-only; executed commands in private `/tmp` sandboxes only.

---

## Commands & Observed Outputs

### 1. Fleet-wide QUALITY.md Inventory
**Command:**
```sh
find /home/vgpnk/Projects/shokunin/*-shokunin/corpus/QUALITY.md -maxdepth 0 2>/dev/null
```
**Observed Output:**
Discovered 21 total `corpus/QUALITY.md` files (tameshi plus 20 sibling lanes):
`audio-shokunin`, `chousa-shokunin`, `game-dev-2d-shokunin`, `game-dev-3d-shokunin`, `kagi-shokunin`, `kaidoku-shokunin`, `kake-shokunin`, `kama-shokunin`, `kasegi-shokunin`, `kengaku-shokunin`, `kotoba-shokunin`, `kotodama-shokunin`, `kumitate-shokunin`, `lore-shokunin`, `mado-shokunin`, `mori-shokunin`, `revenger-shokunin`, `souji-shokunin`, `tabi-shokunin`, `tameshi-shokunin`, `tsukuroi-shokunin`.

### 2. Sibling Rule Keyword Scan
**Command:**
```sh
python3 -c '
import glob, re
files = sorted(glob.glob("/home/vgpnk/Projects/shokunin/*-shokunin/corpus/QUALITY.md"))
keywords = re.compile(r"(instrument|receipt|provenance|staged|in-place|dispatch|sha256|interval)", re.IGNORECASE)
for f in files:
    lane = f.split("/")[5]
    if lane == "tameshi-shokunin": continue
    with open(f, encoding="utf-8", errors="ignore") as fh:
        text = fh.read()
    matches = [l.strip() for l in text.splitlines() if keywords.search(l)]
    print(f"{lane}: {len(matches)} matching lines")
'
```
**Observed Output:**
- `audio-shokunin`: 4 matching lines
- `chousa-shokunin`: 1 matching lines
- `game-dev-2d-shokunin`: 11 matching lines
- `game-dev-3d-shokunin`: 6 matching lines
- `kagi-shokunin`: 9 matching lines
- `kaidoku-shokunin`: 7 matching lines
- `kake-shokunin`: 10 matching lines
- `kama-shokunin`: 15 matching lines
- `kasegi-shokunin`: 7 matching lines
- `kengaku-shokunin`: 10 matching lines
- `kotoba-shokunin`: 3 matching lines
- `kotodama-shokunin`: 2 matching lines
- `kumitate-shokunin`: 0 matching lines
- `lore-shokunin`: 4 matching lines
- `mado-shokunin`: 43 matching lines
- `mori-shokunin`: 19 matching lines
- `revenger-shokunin`: 1 matching lines
- `souji-shokunin`: 12 matching lines
- `tabi-shokunin`: 20 matching lines
- `tsukuroi-shokunin`: 5 matching lines

---

## Scan Findings: Matches & Gaps

### 1. In-Wave Instrument-Edit Rule
- **Tameshi Baseline:**
  - `tameshi-shokunin/corpus/QUALITY.md` Criterion 20: *"An instrument that seats execute in a wave is not edited in place during that wave. Changes are staged at a separate path and installed after the readers finish, and every receipt names the instrument sha it ran. (lessons/round-16.md, scope mistake)"*
  - Criterion 21: Retains the no-in-place-edit rule and mandates that retained receipts carry the instrument's SHA-256 beside them.
  - Round 20 C1 Contract: Staged instruments (`.ufo/evidence/round-20/stage/receipt-window.py` and `stage/measure.py`) frozen before dispatch; installation occurs strictly after wave readers finish, governed by an aware ISO-8601 interval gate.
- **Sibling Matches:**
  - **Zero explicit matches.** No sibling lane has codified a rule prohibiting in-place instrument modifications during an active wave or mandating out-of-tree staging prior to wave completion.
  - **Adjacent / partial controls in siblings:**
    - `kasegi-shokunin` R7: *"Freeze an axis claim against its registered detector before implementation."* (detector pre-freeze, not in-wave staging).
    - `mori-shokunin` 44: *"Before every wave dispatch, retain a CONTEXT_OK receipt bound to that spec's SHA-256..."* (spec context freeze, not instrument execution freeze).
    - `kagi-shokunin` QM8: *"...and the author stops writing at the declared freeze..."* (author write freeze).
    - `kengaku-shokunin` R7: *"runs before the freeze are tagged unscored. Any trial whose UTC precedes the FROZEN: line is labelled unscored."* (temporal pre-freeze classification).
- **Gaps:**
  - 20/20 siblings lack any in-wave staging requirement, post-wave install window, or receipt-time temporal gating of instrument SHA against an install window.

### 2. Receipt-Provenance Criteria
- **Sibling Matches:**
  - `tabi-shokunin` (Criteria 22, 26, 30, 35, 37, 40):
    - Criterion 22: Count claims bind counter blob SHA-256 at measured revision and declared counted inputs.
    - Criterion 26: Run claims cite committed receipts recording argv, producer digest, revision, and exit code.
    - Criterion 30: Committed receipt records producer path and SHA-256; historical receipts are indexed and never edited.
    - Criterion 40: Per-run nonce binding over before/after listings to refuse pasted, prior, or replayed receipts.
  - `mori-shokunin` (Criteria 33, 58, 62):
    - Criterion 33: Receipt provenance requires exact identity of every input; gate receipt hashes declared inputs at load and end (`__file__`/imported module bytes, census, controls) and verifies `rev-parse HEAD`.
    - Criterion 58: Freeze-order receipts carry full commit, exact loaded-byte register/correction digests, executing-script digest, resolved tips, overrides, and argv.
    - Criterion 62: Present delivered instrument crash/malformation is an after-mode regression, not missing capability.
  - `souji-shokunin` (Criteria Q6, Q28, Q31):
    - Q6: Certification / tool verdict names SHA-256 of measured bytes and matches the installed file.
    - Q28: Receipt roots reject transient JJ grace refs (`refs/jj/*`).
    - Q31: Authority files cite only evidence extant at landing revision; unresolvable revisions fail as `LG-FROZEN-MEASURED`.
  - `game-dev-2d-shokunin` (Criteria Q8, Q9, Q18):
    - Q8: Serial-only battery receipts to prevent concurrent process overlap.
    - Q9: Verdict cites blob SHA; post-commit replays write unique receipt paths instead of overwriting committed ones.
    - Q18: Strict comparison of AST-declared CASES vs receipt identities/multiplicity.
  - `game-dev-3d-shokunin` (Criteria Q6, Q9, Q13):
    - Q6: Saved bounded receipts with exact command, scope, exit code, reasons, and `seeds_unchanged=true`.
    - Q9: Verifier results name exact target SHA-256.
  - `kagi-shokunin` (Criteria QM16, QM19):
    - QM16: Freshness provenance separates current captures from historical pins; recomputed from digests.
    - QM19: Whole-process receipt required (exit, final summary, complete claim population); silent exit without affirmative summary is refused.
  - `revenger-shokunin` (Criteria Q09, Q11):
    - Q09: Digest claimed only for exact hashed bytes; does not imply producer origin or authenticity.
    - Q11: Derivation commands and raw outputs preserved inside entries.
- **Gaps:**
  - Sibling criteria focus on static producer digests, whole-process captures, and clean AST mappings, but none bind execution time to an aware ISO-8601 `measurement_interval` evaluated against an explicit contract installation window.

---

## Fleet Standing

Tameshi is ahead of the fleet on instrument change governance and receipt interval binding — having codified in-wave staging (QUALITY 20/21) and a dual-endpoint temporal gate where siblings have neither — while remaining peer with mori, tabi, and souji on static producer digest verification.

---

## UFO-FSD Connector Proposal

### 1. Evidence
In `.ufo/evidence/round-20/stage/receipt-window.py:184-188`:
```python
name, role = contract["index"][sha]
if role == "identity" or name not in contract["windows"]:
    infos.append({"id": "INSTALL_IDENTITY", "receipt": rid,
                  "detail": f"{name}: frozen and installed bytes are identical"})
    continue
```
When an instrument has `role == "identity"` (which is the case in Round 20 where `receipt-window.py` has `frozen_sha256 == installed_sha256 == f03ae7e...`), `receipt-window.py` marks `INSTALL_IDENTITY` and bypasses all temporal window checks. 
A private sandbox test confirmed that a synthetic receipt dated `2020-01-01T00:00:00Z` (years prior to `contract.frozen_at = 2026-10-21T07:40:18Z`) passes `receipt-window.py` with 0 findings.
Siblings have solved related pre-execution leaks:
- `kengaku-shokunin` R7 explicitly tags any trial before the contract freeze as unscored (`runs before the freeze are tagged unscored`).
- `tabi-shokunin` 40 prevents pasted/prior receipts by binding each run to a per-run value.

### 2. Affected Axes
- **Calibration (C1):** Direct refinement of receipt validity and the QUALITY20 recurrence closure without disturbing the 8/10 lane cap.
- **Restraint:** Maintains strict alignment with the frozen contract without rewriting staged bytes.
- **Operability:** Eliminates false-clean verification of pre-dispatch test artifacts.

### 3. Proposed Move
Synthesize the pre-freeze boundary concept (`kengaku` R7) and run freshness (`tabi` 40) into tameshi's receipt-verification workflow as an advisory contract invariant:
- **Move:** In the final wave-2 / integration verification of `.ufo/evidence/round-20/final/receipts.json`, ensure the test harness / L1 integrator verifies that all claimed receipts have `measurement_interval.start >= contract.frozen_at` (i.e. `start >= 2026-10-21T07:40:18Z`).
- **Second-Order Substrate & Contract Effect:** This requires no modification of the frozen staged bytes (`receipt-window.py` or `measure.py`), preserving contract integrity commit `6fd220bce3705498d1d1054e99e3cae73c203751` and leaving the 20/20 selftest intact, while preventing pre-contract dry runs or unanchored receipts from passing as valid wave evidence.

### 4. Risks
- Clock skew between host UTC and ISO-8601 timestamps generated by subagent runners. Mitigated by `parse_ts` requiring aware UTC offsets (`Z` or `+00:00`), ensuring well-ordered comparisons against `contract.frozen_at`.

### 5. Verification
In private sandbox `/tmp/tameshi-r20-f02-verify.py`:
1. Executed `receipt-window.py` against a fixture with `start = 2020-01-01` -> confirmed `INSTALL_IDENTITY` info, exit 0.
2. Verified that adding a precondition check `start >= parse_ts(contract["frozen_at"])` flags the pre-freeze receipt as `PRE_DISPATCH_RECEIPT` while leaving genuine round-20 receipts (`2026-10-21T07:40:18Z`+) clean.
3. Verified that the staged `receipt-window.py` selftest remains 20/20 pass with exit 0.

---

## Tooling & Verification Note
- No package installs or updates performed (`pacman` is paused host-wide).
- All checks read-only; tests executed exclusively in private `/tmp` sandboxes.
- Lane status: leaf subagent, no child dispatch.

# Replay40 — `round21-coldread-selector-selftest` (R23 C1 falsification)

**Seat:** TameshiR23.Replay40  
**Scope:** Single registry row only  
**Replay revision:** `496d212bc46789cdf8cafab72978bdb7f4182963`  
**Registry digest (requirements):** `ebd2e69a6c63e9c212152ea18050781ab686b0cbdaead4bb0fcbbd54d0fec92a`

## Axes

| Axis | Question |
|------|----------|
| Frozen contract fidelity | Do `requirements.json`, `registry-baseline.json`, and `tools/registry.json` agree on argv/expect for this row? |
| Retained execution evidence | Is there a replay receipt with full stdout (not tail-only) for this argv? |
| C1 binding soundness | Does `command-binding.evaluate` accept forged receipts that the tool would reject? |
| Source-read vs command | Does any source-read artifact substitute for executing this argv? |

## Frozen baseline (static)

All three sources match:

- **argv:** `["python3", ".ufo/evidence/round-21/coldread/measure.py", "--selftest"]`
- **expect:** `exit: 0`, `stdout_contains: ["SELECTOR_SELFTEST: 12/12 pass"]`
- **source anchor:** `SKILL.md@370f2dffe66f00c3c7412c962bf3e8fcbe75dfdb:1978`

Implementation at `.ufo/evidence/round-21/coldread/measure.py` defines **12** selftest outcomes (lines 72–94): three ledger/selector cases plus nine override-refusal cases; summary line `SELECTOR_SELFTEST: {passed}/{len(outcomes)} pass`.

## Retained replay evidence (present, not inferred)

| Artifact | Field | Value |
|----------|-------|-------|
| `replay/bundle.json` receipt | argv | matches frozen |
| | cwd | `/tmp/tameshi-r23-replay-naxu6fzi/fleet/tameshi-shokunin` (matches bundle cwd) |
| | revision | `496d212…` (matches bundle) |
| | exit | `0` |
| | stderr | `""` (empty) |
| | stdout | **543 bytes**, 12 `CASE … PASS` lines + `SELECTOR_SELFTEST: 12/12 pass` |
| `replay/observations.json` row | stdout | **byte-identical** to bundle receipt |
| | stdout_tail | equals full stdout (not truncated for this row) |
| | held | `true` |
| `replay-command-A.json` | row line | `round21-coldread-selector-selftest 0 True` |

Case names in retained stdout align with `measure.py` selftest (`configured-default-ledger`, `relocated-package-default-repo`, `no-historical-ledger-fallback`, nine `override-refused:…` variants).

**Verdict on actual bundle:** static exact binding holds for the **recorded** receipt vs frozen argv/expect; evidence is **on disk**, not inferred from tails or registry metadata alone.

## C1 gate context

- `replay-gate-A.json`: `command-binding.py` on `replay/bundle.json` → exit **0**, `finding_ids: []`.
- `source-read-gate-A.json`: same tool on `source-read-bundle.json` → exit **1**, `ARGV_MISMATCH` (receipt argv is `cat tools/registry.json`, not registry commands).

Source-read bundles embed this row’s argv/expect only inside the `cat` stdout blob; they do **not** carry an execution receipt for `python3 …/measure.py --selftest`. **Reject** source-read and historical `source` strings as producer authentication or command execution proof.

## Field-level false acceptance (binding layer)

`tools/command-binding.py` `evaluate()` (lines 109–112) checks only integer exit and substring `stdout_contains`; it does **not** bind per-`CASE` lines or stderr.

Reproduced locally against frozen requirement + receipt shape:

1. **Contradictory CASE lines:** stdout  
   `CASE configured-default-ledger FAIL\nSELECTOR_SELFTEST: 12/12 pass\n` with `exit: 0` → evaluate → **0 findings** (would fail real `measure.py` selftest).
2. **Suffix after token:** stdout  
   `SELECTOR_SELFTEST: 12/12 pass-backdoor\n` with `exit: 0` → evaluate → **0 findings**.
3. **stderr blind:** override cases in `measure.py` require `SELECTOR_OVERRIDE_FORBIDDEN` in stderr (lines 92–94); binding never reads stderr — a forged receipt could not be caught on stderr content alone (actual receipt has empty stderr because failures are internal to selftest subprocesses, not the top-level process).

**Actual retained receipt:** not a false acceptance instance — all 12 CASE lines are PASS and summary matches tool semantics.

**Calibration finding:** C1 exact binding is **sound for argv/cwd/revision/exit/summary substring** on this row’s real receipt, but **unsound against summary-only or suffix forgery** at the evaluator contract level (`contract.json` population includes `missing-stdout-token` only as substring miss, not CASE integrity).

## Concrete adversarial delta (for contract hardening)

**Delta A — summary without case integrity:** Register receipt with `exit: 0` and stdout exactly:

```text
CASE configured-default-ledger FAIL
SELECTOR_SELFTEST: 12/12 pass
```

Passes `command-binding` and registry `held` if inserted into `replay/bundle.json`; fails if the tool is actually run.

**Delta B — token suffix:** Same with final line `SELECTOR_SELFTEST: 12/12 pass-backdoor` (substring match).

Neither delta is present in retained R23 replay artifacts; both are **binding-gap** falsifiers, not claims about the measured run.

## Tooling installs

None (read-only audit; local Python one-liners only).

## Summary

| Claim | Result |
|-------|--------|
| Frozen argv/expect vs baseline | **Match** |
| Replay execution receipt present | **Yes** (full stdout in bundle + observations) |
| Actual row false acceptance | **No** (stdout consistent with 12/12 selftest) |
| C1 evaluator false acceptance class | **Yes** (substring + no CASE/stderr binding) |
| Source-read = command execution | **Rejected** (ARGV_MISMATCH gate; cat registry only) |

# PredK3 — attack on frozen predicate K3 (`exit-negative-ignored`), round-24 C1 calibration

Lane: reviewer / leaf member (no subagent dispatch). Axis: **calibration**.
Scope read-only; no selftest/battery executed in the production tree; no production file, git index,
lane state, or sibling file touched. Only this report was written.

## Verdict

**K3 is honest, non-vacuous, and correctly attributed — no falsification of the frozen predicate
found.** The frozen mutant M3 is killed by exactly the fixture case the contract names
(`negative-exit-mismatch`), every other selftest case still PASSes under M3, the ruler's
control/restore guards are sound, and `before.json` is reproducible byte-for-byte from the same
frozen instrument bytes at base `6a1821a`.

**One residual calibration gap (medium, non-blocking):** the K3 fixture pins the *sign* of negative
exits but not their *exactness*. Two plausible weakenings of the same "negative exit" semantics —
a requirement-side sign guard (W2) and a sign-blind magnitude comparison (W3) — pass **all 44**
selftest cases unchanged and would therefore still be certified "K3 discriminated" by the frozen
ruler, which injects only the receipt-side guard M3. This is a fixture-coverage gap, **not** a live
defect: the delivered implementation compares exits exactly
(`tools/command-binding.py:109`). It also sits inside the contract's declared bound
("K1-K4 count selftest kills of four specific mutants, not general mutation adequacy",
`.ufo/evidence/round-24/contract.json`).

No counterexample to K3 itself was found. The concrete counterexample below is to the *broader*
reading of the K3 predicate name, not to the frozen predicate as specified.

## What the K3 code path actually does (frozen instrument)

`.ufo/evidence/round-24/measure.py:25` freezes the anchor
`EXIT = "if receipt['exit'] != required['expect']['exit']:"`; `:32` pairs it with mutant
`"if receipt['exit'] >= 0 and receipt['exit'] != required['expect']['exit']:"`.

`mutant_rows` (`:62`) copies the whole repo (`copy_repo`, `:57`, `shutil.copytree(..., symlinks=True)`,
ignoring only `__pycache__`), requires `control['exit'] == 0` **and** `pristine.count(old) == 1`
(`:70`, `:72-73`, else `inconclusive`), injects the mutation (`:77`), restores the pristine bytes
(`:79`), and only then counts kills:

```
80:  fails = [line for line in result['stdout'].splitlines() if line.startswith('CASE ') and line.endswith(' FAIL')]
82:  discriminated = result['exit'] == 1 and bool(fails)
84:  restored = run([sys.executable, str(target), '--selftest'], str(root))
87:  if restored['exit'] != 0:  row['discriminated'] = False
```

So a K3 "green" requires: control selftest exit 0, unique anchor, mutant selftest exit 1 **and**
at least one literal `CASE … FAIL` line, and a clean restore of the pristine tree.

## Falsification attempts and what they showed

### 1. Can the kill be vacuous (no real behavioural difference)? — No.

Static delta of M3 is provably confined to receipts with `exit < 0`: for `exit >= 0`,
`exit >= 0 and exit != expected` ≡ `exit != expected`. The only selftest receipts with a negative
exit anywhere in the tree are the two round-24 fixture cases
(`.ufo/evidence/round-24/extra-cases.json:276` `negative-exit-mismatch`, `:343`
`negative-exit-declared-match`). The round-23 fixture has **zero** negative-exit receipts (checked
by parsing all 19 cases), and the 17 in-tool base cases use only 0/1/bool/str exits
(`tools/command-binding.py:154-162`). Therefore under M3 exactly one case can change behaviour.

Empirical confirmation from the executor's after-receipt
(`.ufo/evidence/round-24/after.json`, ruler stdout on line 11), K3 row:

```
anchor_count 1, control_exit 0, exit 1, restored_exit 0, discriminated true
failing_cases: ["CASE negative-exit-mismatch FAIL"]
stdout_tail:  ... CASE negative-exit-declared-match PASS ... COMMAND_BINDING_SELFTEST: 43/44 pass
```

43/44 = exactly one FAIL, and it is the case named in the contract. Not vacuous.

### 2. Could the kill be for the wrong reason? — No.

* Attribution: under M3 every other case is behaviourally identical to pristine, and the receipt
  shows `CASE negative-exit-mismatch FAIL` as the *only* FAIL line, with
  `negative-exit-declared-match PASS`.
* The kill is meaningful because the case isolates the exit dimension: for `negative-exit-mismatch`
  the receipt `clean` has `exit = -9` while the requirement expects `exit = 0`; argv, cwd, revision
  and the `CLEAN` stdout token all match, so the pristine tool reports exactly
  `['EXIT_MISMATCH']` with exit code 1 (matching the fixture's `expected_exit`/`finding_ids`), while
  under M3 the finding disappears, the tool reports `[]`/exit 0, and the case fails.
* Guards in the ruler prevent false greens: a missing fixture file makes the selftest print
  `COMMAND_BINDING_SELFTEST: fixture-unavailable` and exit 1 with **no** `CASE … FAIL` line
  (`tools/command-binding.py:171`), so `fails` stays empty → not discriminated; a failed restore
  zeroes every row (`:84-87`); `control_exit != 0` → `inconclusive` (`:73`).
* Anchor uniqueness verified: `grep -c` of the exact anchor string in `tools/command-binding.py` = 1
  at HEAD `c8c5b88` and 1 at base `6a1821a` (so the injected mutation lands in `evaluate()`, not in
  a docstring or test).

### 3. Does the fixture pin the negative-exit semantics well enough? — Sign yes, exactness NO (finding).

The fixture's two negative cases pin:
* a negative receipt exit must **not** be excused against a `0` expectation
  (`negative-exit-mismatch` → `EXIT_MISMATCH`, exit 1) — this is what kills M3 and also kills
  "accept every negative" weakenings;
* a **declared** negative expectation is satisfiable and must not become `INVALID_RECEIPT`
  (`negative-exit-declared-match`, receipt `-15` vs expected `-15` → clean, exit 0) — this kills
  "reject every negative" weakenings.

What no case pins is the *value* comparison among negatives. Two concrete, plausible weaker
implementations of the same line survive all 44 cases (verified case-by-case against the 17 base,
19 round-23 and 6 round-24 cases, including `wrong-exit`, `multiple-findings`, `bool-exit`,
`string-exit`):

* **W2 — requirement-side sign guard**
  `if required['expect']['exit'] >= 0 and receipt['exit'] != required['expect']['exit']:`
  A requirement that declares `-15` (SIGTERM) is then satisfied by a receipt killed with `-9`
  (SIGKILL). Only `negative-exit-declared-match` has a negative expectation and its values match
  exactly, so the weakened comparison is never observable.
* **W3 — sign-blind magnitude**
  `if abs(receipt['exit']) != abs(required['expect']['exit']):`
  A receipt killed by SIGKILL (`-9`) satisfies a requirement expecting exit `9`, and a plain exit `9`
  satisfies a requirement expecting `-9`. All fixture cases use magnitudes 0/1/9/15 in
  sign-consistent pairs, so this weakening is also invisible.

Neither W2 nor W3 is injected by the frozen ruler, so the ruler keeps reporting K3 "discriminated"
against such an implementation. The delivered production code is **not** W2/W3 — it is exact
(`tools/command-binding.py:109`: `if receipt['exit'] != required['expect']['exit']:`), with the
receipt-side int/bool shape guard at `:90` (`type(row.get('exit')) is not int`) and the
expectation-side guard at `:79`. The gap is therefore in the *fixture's* discriminating power
relative to the predicate's name, not in the implementation.

### 4. Is `before.json` honest? — Yes (for K3, and consistent with K1/K2/K4).

* **Same instrument bytes**: `sha256sum .ufo/evidence/round-24/measure.py` =
  `0a7f6daa7ddaa0ef0b4140c20f5e3eef91b781f2d3119e1819c83191e57daa64` = `before.json.instrument_sha256`
  = `after.json.instrument_sha256`. The ruler was not edited between the base and the after run, so
  the two receipts are comparable.
* **Base tree genuinely lacks the negative-exit coverage**: `git show 6a1821a…:tools/command-binding.py`
  loads only the round-23 fixture (line 164 of that blob), and the base round-23 fixture parses to
  zero negative-exit receipts. Therefore M3 ≡ pristine at base, the mutated selftest still reports
  `38/38 pass`, exit 0, `failing_cases: []` — exactly what `before.json` records for K3. The base
  "1/11" is not a measurement artefact.
* **Cross-row consistency reproduced from the frozen instrument**: at base the round-23 fixture has
  no case-only-argv case (`argv-case-only`/`argv-swapped-between-names` are round-24 additions) and
  no argv-swapped case → M1/M2 survive → K1/K2 not discriminated, matching `before.json`; the
  round-23 case `all-of-tokens` (requirement tokens `['PASS','SECOND']`, receipt stdout `'PASS\n'`)
  is killed by M4 → K4 discriminated, matching `before.json` and the recorded failing case.
* **Independent reproduction**: `.ufo/waves/round-24/w1/RunRulerBase.md` reports a re-run at
  `6a1821a…` whose stdout is **byte-identical** to `before.json.stdout` (11/11 rows identical),
  exit 1, only K4 discriminating; `RunRulerAfter.md` reports 11/11, exit 0 at `c8c5b88…`.
  Both executor runs used private `/tmp` clones.

## Findings by severity

| # | Severity | Finding | Evidence |
|---|----------|---------|----------|
| 1 | Medium (coverage gap; not a live defect, inside declared bounds) | K3's fixture pins the sign of negative exits but not their exact value. W2 (requirement-side sign guard) and W3 (sign-blind magnitude) pass all 44 selftest cases and would still be certified "discriminated". | `extra-cases.json:276`, `:343`; `tools/command-binding.py:109`; `measure.py:32` |
| 2 | Low (traceability) | `before.json` is retained under `.ufo/evidence/round-24/`, but the corresponding after-receipt `after.json` was produced by the wave executor after the contract was frozen and was still **untracked** at review time (`git ls-files .ufo/evidence/round-24/` lists no `after.json`). The 11/11 claim therefore lives outside the evidence tree until it is committed. | `git ls-files` output; `after.json` present on disk |
| 3 | Informational | `measure.py` is not present in the base tree (`git cat-file -p 6a1821a…:.ufo/evidence/round-24/measure.py` → path does not exist), so a base run necessarily uses the frozen working-tree instrument copied into the lane. Disclosed and byte-verified by the executor; the same bytes are named in `before.json.instrument_sha256`. | `RunRulerBase.md` |

No finding of severity High or Critical: K3 is not vacuous, not wrong-reason, and the base receipt
is reproducible.

## Residual risk / verification gaps

* **R1 — fixture exactness (finding 1).** If the claim "required-command binding is hardened against
  negative-exit-ignored semantics" is read broadly rather than as "mutant M3 is killed", the current
  fixture cannot support it: W2/W3 pass. Impact is confined to the *evidence*, since the shipped
  implementation is exact.
* **R2 — mutation adequacy.** By contract (`contract.json` bounds) K1–K4 certify four named mutants
  only; a mutation campaign over the exit/exit-expectation pair would be a stronger claim and is
  out of the frozen scope.
* **R3 — oracle self-consistency.** The round-24 fixture's `expected_exit`/`finding_ids` were authored
  by the same party as the implementation. Mitigating evidence: the expectations coincide with the
  pristine exact-`!=` semantics already pinned by the pre-existing base case `wrong-exit`
  (`tools/command-binding.py:154`) and the round-23 `all-of-tokens` precedent; the mutant's failure
  line names the case whose expectation is independently derivable from the contract's wording
  ("integer exit … must match").
* **R4 — unexecuted by me.** Per lane bounds (no "Run" marker) I did not execute the selftest or the
  ruler; my K3 conclusions rest on (a) static evaluation of the frozen instrument's code path,
  (b) the retained executor receipts `before.json` / `after.json` / `RunRulerAfter.md` /
  `RunRulerBase.md`, and (c) byte-level inspection of the fixtures and implementation at `c8c5b88`.
  The only dynamic evidence I cite is those retained receipts, all produced in private `/tmp` clones.

## Smallest safe correction (for a subsequent round, not a round-24 edit)

Add **one** fixture case to `.ufo/evidence/round-24/extra-cases.json`, e.g.

```json
{ "name": "negative-exit-sign-flip",
  "bundle": { /* same shape as negative-exit-mismatch, but receipt 'red' exit = 9
                while requirement 'red' expect.exit = -15 */ },
  "expected_exit": 1, "finding_ids": ["EXIT_MISMATCH"] }
```

A receipt `exit = 9` against an expectation `-15` (or `-9` against `9`) is killed by **both** W2
(expect-side guard skips the comparison → no finding → case fails) and W3 (`abs(9) == abs(-15)`
fails to flag → case fails), while pristine still reports `EXIT_MISMATCH`. One case closes both
survivors.

Constraints on that correction: it changes the selftest case count (44 → 45) and therefore
invalidates the recorded `43/44 pass` in `after.json`; it must be landed in a later commit that
re-freezes both the fixture and the row (the contract's own rule: "a later commit changing both row
and bundle chooses a new contract"), and the ruler must be re-run at the new revision before any
11/11 or 12/12 style claim is restated. Do **not** edit the round-24 fixture in place — the frozen
before/after receipts would stop being comparable.

## Commands run (all read-only, all inside the production tree without mutation)

```
GIT_OPTIONAL_LOCKS=0 git log --oneline -8 ; git rev-parse HEAD ; git status --porcelain
sha256sum .ufo/evidence/round-24/measure.py
grep -c "if receipt\['exit'\] != required\['expect'\]\['exit'\]:" tools/command-binding.py        # HEAD  = 1
GIT_OPTIONAL_LOCKS=0 git show 6a1821a…:tools/command-binding.py | grep -c "<same anchor>"         # base = 1
GIT_OPTIONAL_LOCKS=0 git show 6a1821a…:.ufo/evidence/round-23/extra-cases.json   # 19 cases, 0 negative exits
python3 -c "<parse both extra-cases.json, list every receipt exit vs expectation>"
GIT_OPTIONAL_LOCKS=0 git ls-files .ufo/evidence/round-24/                      # no after.json
python3 -c "<parse before.json / after.json, print K3 rows>"
find . -maxdepth 3 -type l -not -path './.git/*'                              # no symlinks
```

## Tooling

No tool was installed or upgraded (none needed; `python3`, `git`, `sha256sum`, `grep`, `find` were
already present). Recorded per the operator directive of 2026-10-19: **installs/updates: none**.
No pacman transaction was attempted.

## Not claimed

Not producer authentication; not promotion; not historical R17-CMD-BIND closure; not numeric
calibration or expertise-score uplift; not that K5–K11 are honest (other lanes); not that the
predicate set constitutes general mutation adequacy.

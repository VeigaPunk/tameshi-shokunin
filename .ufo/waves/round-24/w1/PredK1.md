# PredK1 — frozen predicate K1 `argv-name-insensitive` (round24 C1 calibration)

**Lane:** reviewer, leaf member (no subagents dispatched).
**Target:** `.ufo/evidence/round-24/measure.py` K1 path; implementation at `c8c5b88c8e961a929cdc351b95a7074c76958909`.
**Question:** can K1 pass vacuously, pass for the wrong reason, or fail to discriminate a plausible weaker implementation? Is `before.json` honest?
**Method:** read-only inspection + static derivation over the frozen ruler, the mutant definition, the production gate and every fixture. My item carries no "Run" token, so the frozen ruler / registry battery / selftests were **not** executed (see Verification gaps). No tool installs were needed (no tooling record required).

---

## Verdict

**K1 is sound and the base result is honest. No defect found; no counterexample found.**

Three independent questions, answered:

1. **Vacuous pass?** No. Every vacuity channel I could construct fails closed (mutant survives ⇒ `discriminated:false`, not `true`): missing/empty/malformed fixture ⇒ control selftest exit ≠ 0 ⇒ row `reason:'inconclusive'`; stale bytecode ⇒ impossible (script, not import, and `__pycache__` is excluded from the copy); anchor drift ⇒ `anchor_count != 1` ⇒ inconclusive.
2. **Pass for the wrong reason?** No, and the reason is structural, not lucky: the K1 mutant changes **only** the argv comparison, so a selftest case can fail under the mutant only if it asserts `ARGV_MISMATCH`. The killing case is exactly the intended fixture and it is the **only** case that fails under the mutant (proved below by exhaustive fixture scan).
3. **Fail to discriminate a plausible weaker implementation?** No for the mutant K1 names. The mutation is the canonical name-insensitivity weakening (`argv ∈ pool of all requirement argvs` instead of `argv == own requirement's argv`), the fixture models it faithfully (two distinct requirements, receipts' argv transposed), and the mutant's own weakening is exactly the property the fixture encodes.

---

## Evidence

### 1. The frozen ruler's K1 path (`.ufo/evidence/round-24/measure.py`)

* `measure.py:24` — `ARGV = "if receipt['argv'] != required['argv']:"`
* `measure.py:28-29` — `('K1', 'argv-name-insensitive', ARGV, "if receipt['argv'] not in [row['argv'] for row in requirements.values()]:")`
  ⇒ the mutant replaces the per-name equality with membership in the pool of **all** requirement argvs: a receipt may carry *another* requirement's argv and still pass. That is precisely "name-insensitive".
* `measure.py:72-84` — the row is only `discriminated` when: control selftest exit 0 **and** `anchor_count == 1` **and** mutated selftest exit == 1 **and** at least one `CASE … FAIL` line (`measure.py:80`), and the restored selftest must exit 0 (`measure.py:85-89`).

Anchor uniqueness at the delivered revision (verified):

```
$ grep -Fc "if receipt['argv'] != required['argv']:" tools/command-binding.py
1
```
(same for the K2/K3/K4 anchors → `anchor_count == 1`, no inconclusive path.)

### 2. The implementation the mutant actually hits is production code, not a test shim

* `tools/command-binding.py:103` — `if receipt['argv'] != required['argv']:` — inside `evaluate()`, the gate used by the CLI (`--bundle/--expected/--json`).
* Active registry rows that exercise it: `tools/registry.json` → `command-binding-selftest-r24`, `command-binding-frozen-clean-pinned`, `command-binding-source-read-red-pinned` (all `status: active`).
* `tools/registry-replay.py:105-111` — the projection writes a `command-binding-v1` bundle whose receipt `argv` comes from `row.get('argv')` while the requirement `argv` comes from `row['requirement']['argv']` — **two independent fields** of the observations file. `command-binding.py` per-name argv equality is therefore the only place the two are bound, so K1's mutant sits exactly on the production binding property (a receipt recorded under the wrong name / with another row's command).

### 3. The fixture that kills the mutant is well-formed and argv-specific

`.ufo/evidence/round-24/extra-cases.json:7` (`argv-swapped-between-names`, `expected_exit:1`, `finding_ids:["ARGV_MISMATCH"]`, `why` at `:71`):

* requirements: `clean → ["gate","--check"]`, `red → ["gate","--bad"]`
* receipts: `clean → ["gate","--bad"]`, `red → ["gate","--check"]` (argv transposed between names)
* structurally valid against `evaluate()`'s shape gates: schema/key-set exact, `revision` 40×`1`, `cwd` canonical, `argv` non-empty string lists, `expect` keys ⊆ {exit, stdout_contains}, `exit` int, stdout/stderr str ⇒ it is **not** an INVALID_* case, so the only difference between pristine and mutant is the presence of `ARGV_MISMATCH`.

Derivation on pristine: receipt `clean` argv `["gate","--bad"] ≠ ["gate","--check"]` → `ARGV_MISMATCH`; cwd/revision/exit/stdout all match → findings exactly `["ARGV_MISMATCH"]`, exit 1 ⇒ **fixture PASSES pristine**.
Derivation on the mutant: `["gate","--bad"]` and `["gate","--check"]` are both in the pool ⇒ no `ARGV_MISMATCH` ⇒ findings `[]`, exit 0 ≠ expected 1 ⇒ **fixture FAILS** ⇒ stdout line `CASE argv-swapped-between-names FAIL` (matches `measure.py:80`'s `startswith('CASE ')` / `endswith(' FAIL')`), selftest prints `43/44 pass` and returns 1 (`command-binding.py:193-194`) ⇒ `discriminated = True`.

### 4. Attribution: exactly one case fails under the K1 mutant (no wrong-reason kill)

I scanned **every** fixture in both fixture files for receipts whose argv equals *another* requirement's argv in the same bundle (the only way the mutant can change an outcome):

```
$ python3 -c "... scan round-23 + round-24 extra-cases ..."
extra-cases.json unknown-added               receipt extra argv matches requirement ['one']
extra-cases.json argv-swapped-between-names  receipt clean argv matches requirement ['red']
extra-cases.json argv-swapped-between-names  receipt red   argv matches requirement ['clean']
```

* `unknown-added` (round-23) expects `["MEMBERSHIP_MISMATCH"]`; the receipt named `extra` is not in the requirement set, so it is never compared, and the compared receipt `one` matches its own argv ⇒ the mutant changes nothing ⇒ it still PASSES under the mutant.
* ⇒ under the K1 mutant **only** `argv-swapped-between-names` fails. The kill is attributable to the argv assertion, not to an unrelated failure mode.

### 5. Why the base was honest, and reproducible from the frozen counter

* `before.json` records `instrument_sha256 = 0a7f6daa7ddaa0ef0b4140c20f5e3eef91b781f2d3119e1819c83191e57daa64`; the current file hashes to the same value ⇒ **the ruler was not edited after the base measurement** (frozen-counter integrity holds).
  ```
  $ sha256sum .ufo/evidence/round-24/measure.py
  0a7f6daa7ddaa0ef0b4140c20f5e3eef91b781f2d3119e1819c83191e57daa64
  ```
* Base `6a1821a8897eea6e7d9669292160ec9593669409` has **no** `round-24` tree at all (`git ls-tree 6a1821a .ufo/evidence/round-24/` → empty) and its selftest loads **one** fixture file:
  ```
  $ git show 6a1821a:tools/command-binding.py | grep -n "extra-cases"
  164:    fixtures = Path(__file__).resolve().parents[1] / '.ufo/evidence/round-23/extra-cases.json'
  ```
  ⇒ the swapped fixture could not exist at base ⇒ the name-insensitive mutant necessarily survived at base.
* Base case arithmetic closes exactly: 1 base case + 16 `changed(...)` inline + 19 round-23 fixture cases + 2 (`tampered`, `duplicate-json-key`) = **38**, matching the recorded `COMMAND_BINDING_SELFTEST: 38/38 pass` in the K1 row's `stdout_tail` (mutant exit 0, `failing_cases: []`, `discriminated:false`). The base's single discriminating predicate is K4, via the round-23 `all-of-tokens` case (`stdout_contains:["PASS","SECOND"]`, receipt stdout `"PASS\n"`): pristine raises `STDOUT_MISMATCH` (`any` semantics), the K4 mutant (`all` semantics) does not ⇒ killed. Both the 1/11 count and the note in `before.json` are **honest**.
* The delivered change is *necessary*, not decorative: `tools/command-binding.py:166` now loops over `(round-23/extra-cases.json, round-24/extra-cases.json)`; without that second file the swapped fixture is never loaded and the mutant survives (→ K1 honestly *false*). Adding the fixture alone would not have moved K1.

### 6. Vacuity channels all fail closed (explicit enumeration)

| hypothetical tampering | observable | K1 outcome |
|---|---|---|
| fixture file deleted | `command-binding.py:170-172` prints `COMMAND_BINDING_SELFTEST: fixture-unavailable`, exit 1 | control_exit ≠ 0 ⇒ `reason:'inconclusive'` ⇒ **false**, not vacuous true |
| fixture `{"cases":[]}` | control 38/38 → mutant also 38/38, exit 0 | `discriminated:false` ⇒ honest failure |
| fixture malformed (bad JSON / missing `cases`) | `decode()`/`KeyError` caught ⇒ `fixture-unavailable`, exit 1 | inconclusive ⇒ false |
| anchor rewritten by a future edit | `anchor_count != 1` (`measure.py:73`) | inconclusive ⇒ false |
| mutant written but not applied (write failure) | mutant run == control, exit 0, no FAIL line | `discriminated:false` |
| stale `.pyc` masking the mutant | impossible: the tool is executed as a script (never imported → no bytecode cache for `__main__`), `sys.dont_write_bytecode = True` (`command-binding.py:21`), and `copy_repo` excludes `__pycache__` (`measure.py:64`) | n/a |
| restored file broken | `restored_exit != 0` ⇒ `discriminated=False` (`measure.py:85-89`) | false |

### 7. Plausible weaker argv implementations — do they escape?

Not a K1 obligation (contract bound: "K1-K4 count selftest kills of four specific mutants, not general mutation adequacy"), but I checked whether the delivered fixture set already closes the argv family. Static scan of all 10 argv fixtures against 10 candidate weakenings:

| weaker argv comparison | killed by |
|---|---|
| name-insensitive / membership in pool (K1) | `argv-swapped-between-names` (round-24) |
| casefold (K2) | `argv-case-only` (round-24) |
| whitespace-strip | `argv-padded-token` (round-24) |
| set/dedup comparison | `argv-repeated-flag` (round-24) |
| first-token-only | `argv-swapped-between-names` (both argvs start `gate`) |
| order-insensitive (sorted) | `argv-order` (round-23) |
| prefix/subset | `argv-extra`, `argv-missing` (round-23) |
| path normalisation (`./gate.py`) | `argv-normalized` (round-23) |
| shell-joined string | `argv-joined-collision`, `argv-shell-string` (round-23) |
| "second token only" | `argv-second-only` (round-23) |

No plausible argv weakening in this family survives the delivered 44-case selftest.

---

## Residual risks (not defects)

1. **The predicate boolean does not require the *specific* fixture.** `measure.py:82` accepts any `CASE … FAIL` line. Structural consequence (proved above): any failing case under the K1 mutant must assert `ARGV_MISMATCH`, so the kill is always an argv assertion — but it is *not* pinned to `argv-swapped-between-names`. Today the attribution holds (only that one case fails, §4). If a future fixture introduced a second cross-name argv match, `failing_cases` would list both and the boolean would not distinguish them. Severity: low; the row's `failing_cases` field makes it auditable.
2. **K1 certifies one mutant only.** `K1 = true` must not be read as "argv binding is hard"; it certifies mutant #1 of four. The broader argv coverage in §7 comes from the fixture set, not from the K1 boolean — deleting any of the other nine argv fixtures would leave K1 green while silently weakening argv binding.
3. **Fixture is data outside `tools/`.** `command-binding.py:166` loads evidence files by path relative to `__file__`; the selftest therefore has a runtime dependency on `.ufo/evidence/round-{23,24}/extra-cases.json` existing in the tree under test. This fails closed (exit 1) but means a deployment without `.ufo/` cannot run the selftest at all.
4. **`stdout_tail` truncation.** The row stores only the last 400 chars of stdout; the failing case line is printed *early* (supplemental cases run before `tampered`/`duplicate-json-key`), so `stdout_tail` will usually not show it. `failing_cases` does. Do not audit K1 from `stdout_tail` alone.

## Verification gaps

* ~~No after-measurement receipt was available to me.~~ **Closed while the report was being written.** The `RunRulerAfter` lane published `.ufo/evidence/round-24/after.json` (revision `c8c5b88c8e961a929cdc351b95a7074c76958909`, exit 0, `discriminated 11/11`). Its K1 row is exactly the observable this review predicted from static derivation:

  ```json
  {"id": "K1", "name": "argv-name-insensitive", "anchor_count": 1, "control_exit": 0,
   "exit": 1, "restored_exit": 0, "discriminated": true,
   "failing_cases": ["CASE argv-swapped-between-names FAIL"],
   "stdout_tail": "... CASE argv-swapped-between-names FAIL\nCASE argv-case-only PASS\nCASE argv-padded-token PASS\nCASE argv-repeated-flag PASS\nCASE negative-exit-mismatch PASS\nCASE negative-exit-declared-match PASS\n... COMMAND_BINDING_SELFTEST: 43/44 pass\n"}
  ```

  ⇒ `control_exit:0`, `anchor_count:1`, `exit:1`, `restored_exit:0`, `discriminated:true`, and `failing_cases` contains **only** `argv-swapped-between-names` — matching §3 and §4 exactly (43/44 = one failed case; the failed case is the intended one). The attribution story in §4 is confirmed by observation, not only by derivation. (I read this receipt; the lane wrote it.)
* I did not execute the ruler or the selftest (my item carries no "Run" token; lane bounds forbid running the registry battery/selftests in the lane repo).
* The base reconstruction (§5) is arithmetic over `git show 6a1821a:…` plus the recorded `stdout_tail`; I did not re-run the ruler at the base revision.

## Smallest safe correction

**None required for K1.** No production file, fixture, or ruler change is needed; the delivered `argv-swapped-between-names` fixture + the second fixture-file load in `command-binding.py:166` are sufficient and minimal, and the base receipt is reproducible.

Optional, strictly cosmetic hardening of the *ruler* (not of production code, and **not** required for the 11/11 target): require the K1 row's `failing_cases` to contain the expected fixture name before setting `discriminated` — i.e. replace the generic `bool(fails)` at `measure.py:82` with a per-predicate expected-case list. This closes residual risk 1 and 2 at the cost of touching the frozen counter, which would itself invalidate `before.json`'s `instrument_sha256`. Recommend **not** doing it inside this frozen round; if desired, land it in a later round with a fresh contract and a fresh base receipt.

## Tooling

No packages installed or upgraded (read-only inspection only; `git` used with `GIT_OPTIONAL_LOCKS=0`, `git show/log/ls-tree/diff` only — no write commands, no mutation of the lane repo).

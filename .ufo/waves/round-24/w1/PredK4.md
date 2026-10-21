# PredK4 — falsification of frozen predicate K4 (stdout-any-token)

Seat: TameshiR24-2.PredK4 (critic, read-only). Revision inspected: c8c5b88c8e961a929cdc351b95a7074c76958909; base 6a1821a8897eea6e7d9669292160ec9593669409.

## Verdict

**K4 is honest and non-vacuous as frozen, and the base result in before.json is honest. K4 is weak as calibration.** It discriminates only the one literal `any()` mutant. A plausible weaker implementation, where a loop overwrites its result so only the last token counts, survives the whole public selftest at c8c5b88. Three other weaker stdout predicates also survive.

This is a scope tradeoff, not a ruler defect: contract bound 1 says "K1-K4 count selftest kills of four specific mutants, not general mutation adequacy". It becomes a defect only if a document reads K4 as "stdout requires all tokens" being hardened. `corpus/knowledge/replay-projection-hardening.md:15` comes close to that (see the impacted axes below).

## What I checked

- **The ruler path** (`.ufo/evidence/round-24/measure.py`).
  - K4 is discriminated only when all of the following hold: the pristine selftest exits 0, the anchor `STDOUT` occurs exactly once, the mutant selftest exits 1 with at least one `CASE ... FAIL` line, and the restored selftest exits 0 (measure.py:70-88).
  - The mutant is `if required['expect'].get('stdout_contains') and all(token not in receipt['stdout'] for token in ...)` (measure.py:34-36). It adds a finding only when none of the tokens is present, which is the correct encoding of "any token suffices".
- **Vacuity.**
  - If the fixtures are missing, the selftest prints `fixture-unavailable` with exit 1 and no `CASE` lines (`tools/command-binding.py:170-172`), so K4 is not discriminated.
  - If the anchor drifts, the row is inconclusive. A syntax-broken mutant also produces no `CASE` lines.
  - The mutant cannot raise for any input: a falsy list short-circuits before `all()`.
  - No vacuous pass was found.
- **Wrong reason.**
  - The ruler credits any failing case, not specifically a stdout case. That is a ruler-wide weakness, but it is not exercised here.
  - The before.json K4 row lists exactly `['CASE all-of-tokens FAIL']` with exit 1, control_exit 0, restored_exit 0 and anchor_count 1.
  - The killing fixture (`.ufo/evidence/round-23/extra-cases.json`, case `all-of-tokens`) requires `['PASS','SECOND']` against stdout `PASS\n` and expects exit 1 with `['STDOUT_MISMATCH']`. That is the correct reason.
- **The anchor is unchanged from base to c8c5b88.** The line `if any(token not in receipt['stdout'] for token in required['expect'].get('stdout_contains', [])):` occurs exactly once at both revisions (`git show 6a1821a8:tools/command-binding.py | grep -c` gives 1; the c8c5b88 working file gives 1).
  - `git diff 6a1821a8 c8c5b88 -- tools/command-binding.py` only adds the round-24 fixture load (lines 164-169).
  - The round-23 fixture is byte-unchanged between the two revisions (`git diff --quiet` succeeds).
  - So K4 measures no round-24 change. `corpus/lessons/round-24.md:10-12` states this ("kept as a control, not a repair"), which is correct provenance.
- **Honesty of before.json.**
  - `instrument_sha256` 0a7f6daa…a57 matches both `sha256sum .ufo/evidence/round-24/measure.py` and `git show c8c5b88:.ufo/evidence/round-24/measure.py | sha256sum`. The ruler was frozen in e338f1b.
  - The base selftest count of 38 is consistent with the base code: 17 inline cases plus 19 round-23 fixture cases plus 2 (tampered and duplicate-json-key).
  - The mutant tail shows 37/38 pass, with the single FAIL being `all-of-tokens`. That is the expected outcome from static reading of the base code.
  - Its note ("K4 already discriminated at base") agrees with `contract.json` before = 1/11.
  - Limitation: I could not independently re-verify that the /tmp clone was checked out at 6a1821a. Only the recorded `revision` field attests to it.

## Counterexample (a plausible weaker implementation that is not discriminated)

To find this, I took the fixture bundles from round-23 and round-24 plus the two stdout-relevant inline selftest bundles (the base bundle and `stderr-cannot-supply-token`). Exit-2 shape cases never reach the stdout check, so I excluded them. For each remaining case I compared the pristine stdout finding with each candidate's. This was in-memory Python over JSON reads only; no repo tool, selftest, gate or battery was run, and nothing was written.

| Weaker stdout predicate | Killed by |
|---|---|
| K4 frozen `any()` mutant | `all-of-tokens` |
| first token only (`tokens[:1]`) | `all-of-tokens` |
| stdout+stderr union | `stderr-cannot-supply-token` |
| **last-wins loop overwrite** (`for t in tokens: ok = t in stdout`) | **none: survives** |
| **casefolded token match** | **none: survives** |
| **whitespace-stripped stdout** | **none: survives** |
| **stdout checked only for the first sorted requirement name** | **none: survives** |

Concrete counterexample for the last-wins case:

- Requirement `one` with `stdout_contains: ["SECOND","PASS"]` and a receipt stdout of `PASS\n`.
- The specification ("all required stdout tokens", `SKILL.md:2015`; the module docstring "required stdout tokens must match") demands exit 1 with `STDOUT_MISMATCH`.
- The last-wins implementation returns exit 0 with an empty finding list.
- No selftest case distinguishes the two, for these reasons:
  - The only multi-token case puts the missing token last.
  - Every stdout-mismatch case targets the first sorted requirement name (`one` or `clean`).
  - No fixture differs only in token case.

## Impacted axes

- **Calibration.** The C1 claim "harden required-command binding" inherits K4's single-mutant reach.
- **False-provenance risk (minor wording).** `corpus/knowledge/replay-projection-hardening.md:15` lists "stdout tokens checked with any() instead of all()" as a hardened weak link that "Fails when only one of two required tokens is present". That is true only when the present token comes first. The lesson's reject line ("reading four mutant kills as general mutation adequacy") already bounds the claim, so this is not a contract violation.
- **No regression and no duplicate authority.** K4's frozen meaning is unchanged.

## Smallest safe correction

No change to the frozen K4 ruler is needed; re-freezing it would choose a new contract. If the next round wants stdout binding to be real calibration, it should add data-only supplemental fixtures to a round-25 `extra-cases.json` file:

1. **`all-of-tokens-first-missing`**: tokens `["SECOND","PASS"]`, stdout `PASS\n`, expecting exit 1 with `STDOUT_MISMATCH`. This kills the last-wins mutant.
2. **`stdout-case-differs`**: token `CLEAN`, stdout `clean\n`, expecting exit 1 with `STDOUT_MISMATCH`. This kills the casefold mutant.
3. **A stdout mismatch on the second sorted requirement only**: for example `red` with stdout `ok\n`, expecting exit 1 with `STDOUT_MISMATCH`. This kills the first-name-only mutant.
4. **A multi-token clean control**: tokens `["PASS","SECOND"]`, stdout `SECOND PASS\n`, expecting exit 0 with no findings. This guards against over-strict or order-sensitive fixes.

Optionally, add a matching new predicate rather than mutating K4. Separately, the knowledge-row wording could say "the any() mutant is killed; all-of-tokens fidelity is otherwise unmeasured".

## Tooling

No tools were installed or updated.

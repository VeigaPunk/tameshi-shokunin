# MutateReattribute — round 16 wave 2

**Verdict: falls — `--selftest` detected none of the six assigned attribution regressions: 0 killed, 6 survived, 0 inconclusive; all pristine and restored runs passed.** This is a detector-coverage finding, not a judgment of the round or permission to change the contract.

## Scope and axes

- **Depth:** challenge six specific behavior-bearing points in attribution parsing and old-rule fidelity enforcement.
- **Calibration:** distinguish a killed mutant from a baseline failure, retain actual stdout/stderr/exits, and establish exact-byte restoration by before/after SHA-256.
- Source revision: `c699c8c36d6e4eca4b796b81a8247904aa145ec8` in `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. Only committed bytes were copied; no live lane implementation was executed or edited.
- Target: `.ufo/evidence/round-16/attribution/reattribute.py` (git blob `2c099225311a3a8b646077112d9961c1eee9fad6`).
- Receipt: `.ufo/evidence/round-15/verification-3.json` (git blob `87987fb8bf2841aeedaf2fdfda492c019ad70793`).
- Scratch: `/tmp/tameshi-r16w2-MutateReattribute-IYmyv6`. Each mutant had its own `<scratch>/<mutant>/.ufo/evidence/round-16/attribution/reattribute.py` and matching `.ufo/evidence/round-15/verification-3.json`. This preserves the root/receipt resolution at `.ufo/evidence/round-16/attribution/reattribute.py:45–47`.
- Runtime observed: `python3 --version` → `Python 3.14.8`, exit 0. No tools installed or upgraded.

## Detector and execution method

The expected detector for every mutant was the existing CLI `python3 <absolute isolated target> --selftest`, unchanged across pristine, mutated and restored bytes. Each subprocess had a 20-second timeout. Six independent subprocesses ran concurrently within each phase, with each phase completed before mutation/restoration. No background jobs, subagent dispatch, additional behavioral detectors, or other assistant runtimes were used.

A kill required a passing pristine detector followed by a mutant rejection; a failing pristine run would be inconclusive. There were no timeouts, syntax errors, baseline failures, restored failures, or detector stderr. All 18 invocations exited 0 and printed the same selftest results (only the isolated-root prefix varies across mutants).

Commands actually executed for input acquisition (all exit 0):

```text
mktemp -d /tmp/tameshi-r16w2-MutateReattribute-XXXXXX
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin ls-tree -r c699c8c36d6e4eca4b796b81a8247904aa145ec8 -- .ufo/evidence/round-16/attribution/reattribute.py .ufo/evidence/round-15/verification-3.json
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c699c8c36d6e4eca4b796b81a8247904aa145ec8:.ufo/evidence/round-16/attribution/reattribute.py
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c699c8c36d6e4eca4b796b81a8247904aa145ec8:.ufo/evidence/round-15/verification-3.json
python3 --version
```

The two `git show` stdout byte strings were written into the isolated layouts using the file-write tool. Mutations were applied with the surgical-edit tool; restoration rewrote each target from the original committed byte string. Before and after every detector invocation, `sha256sum <absolute target> <absolute receipt>` ran successfully (36 checksum commands; neither input changed during any detector invocation).

## Exact mutants and outcomes

All line references in this table refer to `.ufo/evidence/round-16/attribution/reattribute.py` **at the source revision**, not shifted mutant line numbers. Mutants were independent, never cumulative.

| Isolated root suffix | Source lines | Mutation | Pristine / mutated / restored exits | Outcome |
|---|---|---|---|---|
| `M01-first-match` | 111–117, especially 116 | `found = match` → `return match`: first exit-eligible full-line verdict wins. | 0 / 0 / 0 | **survived** |
| `M02-no-exit-crosscheck` | 115 | `if match and (exit_code is None or int(match.group(3)) == exit_code):` → `if match:`. | 0 / 0 / 0 | **survived** |
| `M03-no-json-branch` | 121–127 | Delete only the JSON-result branch in `new_rule`; text parsing remains. | 0 / 0 / 0 | **survived** |
| `M04-stdout-first` | 130–132, especially 131 | In the both-stream branch, `return None` → `return on_out.group(2)`: stdout wins. | 0 / 0 / 0 | **survived** |
| `M05-no-ambiguity` | 130–131 | Delete the both-stream rejection; the existing `on_err or on_out` now makes stderr win. | 0 / 0 / 0 | **survived** |
| `M06-no-old-fidelity` | 246–249 | Delete the warning/nonzero-return block for `fidelity_failures` in `run_correction`; collection and JSON diagnostic remain. | 0 / 0 / 0 | **survived** |

The stdout-first mutant is deliberately behavior-bearing: merely swapping `on_err or on_out` while retaining the ambiguity rejection would be equivalent. M04 instead replaces the ambiguous result with the stdout id. M05 independently removes ambiguity rejection and therefore selects stderr. Both are one-point changes to the dual-stream decision, with distinct precedence.

Executed CLI commands below were each run three times, once per byte state (the exit triplet for each is recorded above):

```text
python3 /tmp/tameshi-r16w2-MutateReattribute-IYmyv6/M01-first-match/.ufo/evidence/round-16/attribution/reattribute.py --selftest
python3 /tmp/tameshi-r16w2-MutateReattribute-IYmyv6/M02-no-exit-crosscheck/.ufo/evidence/round-16/attribution/reattribute.py --selftest
python3 /tmp/tameshi-r16w2-MutateReattribute-IYmyv6/M03-no-json-branch/.ufo/evidence/round-16/attribution/reattribute.py --selftest
python3 /tmp/tameshi-r16w2-MutateReattribute-IYmyv6/M04-stdout-first/.ufo/evidence/round-16/attribution/reattribute.py --selftest
python3 /tmp/tameshi-r16w2-MutateReattribute-IYmyv6/M05-no-ambiguity/.ufo/evidence/round-16/attribution/reattribute.py --selftest
python3 /tmp/tameshi-r16w2-MutateReattribute-IYmyv6/M06-no-old-fidelity/.ufo/evidence/round-16/attribution/reattribute.py --selftest
```

## Actual detector output

Full stdout from the M01 pristine invocation:

```text
/tmp/tameshi-r16w2-MutateReattribute-IYmyv6/M01-first-match/.ufo/evidence/round-15/verification-3.json sha256=3c419055723319f50611eb7d2fa3de46e4d4c37fb405267609eee80aecc7d8ce
usage-proof-new: oracle=usage_error old='context_consistent' FAIL new='usage_error' PASS
gate-usage: oracle=usage_error old='context_consistent' FAIL new='usage_error' PASS
usage-proof-old: oracle=receipt_missing old='receipt_missing' PASS new='receipt_missing' PASS
forged-first-line: oracle=usage_error old='context_consistent' FAIL new='usage_error' PASS
SELFTEST: PASS (new rule 4/4; old rule fails 3/4; same fixtures and oracles)
```

For **each** mutant, pristine, mutated and restored stdout were byte-identical; stderr was the empty string in all three states. Across all 18 invocations, replacing only the six isolated-root prefixes with one common prefix produced exactly one stdout variant. Thus every mutated and restored invocation printed the four row results and the same final `SELFTEST: PASS (new rule 4/4; old rule fails 3/4; same fixtures and oracles)` line shown above.

## Coverage explanation and limits

Static anchors explain why these independent defects escaped; these explanations are **[INFERENCE] from the inspected source and retained fixtures**, not claims that extra witness inputs were executed:

1. **First versus last:** the forged fixture prepends `CONTEXT: OK (id=context_consistent exit=0)` to a usage-error stream whose process exit is 64 (`.ufo/evidence/round-16/attribution/reattribute.py:269–276`). M01 retains the exit cross-check, so the planted first line is ineligible. This fixture does not independently establish last-match selection among two exit-eligible verdicts.
2. **Exit cross-check:** M02 retains last-match selection. The real usage verdict follows the planted exit-0 line, so last-match behavior masks the absent cross-check (`.ufo/evidence/round-16/attribution/reattribute.py:111–117,274–276`).
3. **JSON branch:** the three retained cases are text-result cases. In `usage-proof-old` and `usage-proof-new`, `--json` is the value immediately after `--receipt`, not an enabled flag; `.ufo/evidence/round-16/attribution/reattribute.py:65–73` reconstructs that distinction. Receipt anchors: `.ufo/evidence/round-15/verification-3.json:183` (`usage-proof-old`), `:213` (`usage-proof-new`), `:359` (`gate-usage`). There is no successful JSON-result oracle in `.ufo/evidence/round-16/attribution/reattribute.py:260–276`.
4. **Stream precedence and ambiguity:** the selected retained fixtures use stdout alone (`usage-proof-old`) or stderr alone (`usage-proof-new`, `gate-usage`). The forged case only prepends stderr. No case provides eligible verdicts on both streams, so neither M04 nor M05 reaches its differing outcome (`.ufo/evidence/round-16/attribution/reattribute.py:128–133,260–276`).
5. **Old-rule fidelity:** `--selftest` dispatches only to `run_selftest`, not `run_correction` (`.ufo/evidence/round-16/attribution/reattribute.py:297–304`). Its `old_fails >= 1` contrast assertion (`:288`) is not the receipt-wide old-rule fidelity rejection removed by M06 (`:246–249`). The diagnostic list is still produced by the correction path, but nonzero enforcement was removed; that default correction path was not run in this assignment.

These results establish weakness of this named `--selftest` detector against the six named mutations. They do not establish that the pristine production rules themselves return incorrect ids, nor that other unrun checks would miss these defects. No fixes or contract changes were made.

## Hashes and restoration evidence

SHA-256 aliases (full values):

```text
H0 target pristine/restored: b81086b0978976efd4f8199c59bb66df018ea35d24d642a6590bf25942b714e9
F0 receipt, all copies and states: 3c419055723319f50611eb7d2fa3de46e4d4c37fb405267609eee80aecc7d8ce
```

| Mutant | Target before mutation | Target while mutated | Target after restoration | Receipt before/after every invocation |
|---|---|---|---|---|
| `M01-first-match` | H0 | `c255b837cdaf2523eb46b9d90d7a5df182372b5270fbb33cdb862e876c00606d` | H0 | F0 / F0 |
| `M02-no-exit-crosscheck` | H0 | `47bb8cc21405a2fdb4f9021b284d7bf069e9982b55a3f683f99d2d4afc6a5089` | H0 | F0 / F0 |
| `M03-no-json-branch` | H0 | `ee44284c1c95c20cc11fedb19e83e186e8c3fd8c3b0b6bbe81e16b0f7c1d5287` | H0 | F0 / F0 |
| `M04-stdout-first` | H0 | `028130cb88278cce11dfdfa6761ac248cb4f898f20770735d8d818d43e420cf7` | H0 | F0 / F0 |
| `M05-no-ambiguity` | H0 | `38e5e59214ee121f0d114b2747fe8f302b825f3d6d59e5d462a3b3cb30035158` | H0 | F0 / F0 |
| `M06-no-old-fidelity` | H0 | `5ddd4e8378fa7abd4bef9823f6b4b4ef653527edb1556d559b8d0196892d2d53` | H0 | F0 / F0 |

All six restored targets matched H0 before **and** after their restored detector invocation. All 36 before/after receipt samples matched F0. Restoration occurred in a `finally` block before the restored detector batch, so detector failure would not have skipped restoration.

Full raw command records (argv, cwd, timeout bound, exit, stdout, stderr and both input hashes) were retained under scratch:

- `/tmp/tameshi-r16w2-MutateReattribute-IYmyv6/pristine-results.json`
- `/tmp/tameshi-r16w2-MutateReattribute-IYmyv6/mutated-results.json`
- `/tmp/tameshi-r16w2-MutateReattribute-IYmyv6/restored-results.json`
- `/tmp/tameshi-r16w2-MutateReattribute-IYmyv6/all-results.json`

The decisive outputs, exact mutation descriptions, commands and hashes are embedded above; the finding does not depend on retaining `/tmp`. The report is the only lane write. No commits, git adds, sibling edits, production fixes or unrelated checks were performed.

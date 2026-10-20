# FalsifySelftestWiring — round 15 w2 critic

Seat: `TameshiR15.FalsifySelftestWiring`. This is a static review only. I ran no selftest, check, build or other verification. Tool installs and updates: none.

## Source read

`tools/context-capture.py` (read snapshot `#472A`, 2116 lines):
- docstring and exit map: 1–106
- constants and USAGE: 121–277
- utilities and validators: 296–750
- recompute functions: 756–1106
- verdict, expected pin, `apply_expected` and `run_check`: 1108–1344
- fixture builder: 1349–1569
- `SelftestHarness`: 1572–1725
- all cases: 1728–2002
- `run_selftest`, `parse_argv` and `main`: 2005–2116

I also read Routed defect 5 in `corpus/lessons/round-14-verifier-spotcheck.md` (lines 154–162). `AGENTS.md` has no match for "gate standard" or "selftest". Before writing, I grepped the existing w2 reports, and none reports this hole.

## Bounded agreement (static trace)

- **Every case runs the real CLI in a subprocess.**
  - `check_case` runs `[sys.executable, "-I", SELF, "--check", "--receipt", R, "--expected", E, "--json"]` (1637–1640).
  - `usage_case` runs `[sys.executable, "-I", SELF] + argv` (1686).
  - Both use `env=SELFTEST_ENV`, `stdin=DEVNULL`, a cwd under the mkdtemp root, and `timeout=60`.
  - No case calls a helper function in-process. Only fixture construction and `sha256_bytes` run in the parent.
- **Each case pins a literal id/exit pair.**
  - There are 31 `check_case` pairs, 5 `usage_case` pairs (exit 64 plus `id=usage_error` on stderr) and 2 hermetic records.
  - A check case passes only if the process returncode, the JSON `exit` and the JSON `id` all equal the literal values, `findings` is a list, and stderr has no `Traceback` (1653–1659).
  - A clean case also needs `findings == []` and a receipt sha equal to the fixture bytes (1660–1664).
- **Each fixture reaches its intended rule.** I traced every mutated fixture through `check_receipt`, and the first finding is the intended id:
  - `payload-digest-lie` → `comparison_tool_digest_mismatch` at 933
  - `mapping-constant-swap` → the raw-false `elif` at 1102, with honest flags
  - `control-ineffective` → the `elif` at 1011
  - The structure cases that all share the id `receipt_structure_invalid` each fail at their intended check: `require_bool` at 635 and 692, `require_int` (bool rejected) at 510, the exclusions check at 574 and `require_object` at 571. No case passes because of an unintended extra key.
  - `duplicate-key` gives `receipt_json_invalid` and not `receipt_structure_invalid`, so the duplicate-key hook is being tested.
- **Routed defect 5 on self-invocation is addressed for the explicit-mode verdict path**, subject to the hole below.

## Counterexample: the CLI's own pin verdict for non-zero results is never asserted

`apply_expected` (1265–1286) enforces the expected pin in two ways:
- **Recomputed exit is 0:** it rewrites the result to `expected_verdict_mismatch` with exit 1.
- **Recomputed exit is non-zero:** it only appends an `expected_verdict_mismatch` finding (1283–1285) and sets `verdict_matches_expected=false`. The top-level `id` and `exit` stay as recomputed.

The harness never reads `verdict_matches_expected` or `expected_verdict_mismatch`. It only checks the top-level `id` and `exit` (1653–1659). For non-zero cases, that top-level id/exit comparison is the harness's own check against the pin it wrote, not the CLI's enforcement. Only `missing-injected-env` uses `expected_ids` (1743).

Which branches the selftest reaches:
- **Exit-0 branch:** only `expected-verdict-mismatch` (1928–1936) reaches it.
- **Non-zero branch:** only `snapshot-tampered` (1906–1913) reaches it. That case's pin `context_consistent/0` disagrees with the result `snapshot_tampered/2`, yet the case counts as OK and its appended finding is never checked.
- **No case** pins a non-zero receipt with a wrong id at the same exit.

Mutants that survive the whole selftest. I traced each against all 38 records; none was executed:
- **M-A:** at 1269–1270, compare exit only: `matches = result["exit"] == expected["exit"]`.
  - `clean` still matches (0/0).
  - `expected-verdict-mismatch` still differs (pin 1 vs result 0), so it still rewrites to `expected_verdict_mismatch/1`.
  - Every other non-zero case keeps its recomputed top-level id and exit.
  - Effect: the pin `{receipt_sha256: <mapping-check-lie bytes>, id: comparison_mismatch, exit: 1}` gives `id=mapping_mismatch`, `exit=1`, `verdict_matches_expected=true` and no `expected_verdict_mismatch`. A wrong-id pin then counts as reproduced.
- **M-B:** delete the `else: collect_finding(...)` branch (1283–1285).
  - Every case still passes. `snapshot-tampered` still returns `snapshot_tampered/2`.
  - Effect: a non-zero pin with the wrong id leaves no finding at all.

Under both mutants and under the current source, the process exit for a non-zero pin with the wrong id equals the exit for a matched pin (1/1 or 2/2). So the selftest cannot see whether the id half of a non-zero pin is enforced.

Impacted axes:
- C1 "literal expected exit/finding pairs" enforced by the public CLI, rather than credited by the harness's own comparison.
- The exit/finding pair claim for `expected_verdict_mismatch`.

## Smallest safe correction (fixable defect, not a judge-level tradeoff)

Both changes go in the selftest only; the gate semantics stay as they are.

1. **Assert the CLI's pin verdict.** In `check_case`, when the default pin was written (`expected_override is None and write_expected`), also require:
   - `payload.get("verdict_matches_expected") is True`
   - no finding with id `expected_verdict_mismatch`
2. **Add one literal case.** Take the `mapping_check_lie` receipt and pin it with its correct digest as `{id: "comparison_mismatch", exit: 1}`. Expect:
   - `id=mapping_mismatch`, `exit=1`, returncode 1
   - `findings` containing `expected_verdict_mismatch`
   - `verdict_matches_expected is False`

   This needs a small `check_case` parameter for the expected `verdict_matches_expected` value, plus `expected_ids`.

With these two changes, both M-A and M-B fail at least one record.

Tradeoff for the judge (not part of this hole): under the current exit map, a non-zero pin with the wrong id still exits 1 or 2, the same as a matched pin. Exit-only consumers therefore cannot detect it. Lines 91–93 document only the matched-pin case. Whether the gate should change that is a semantics decision that needs no selftest change.

## Out of bounds / not claimed

- Frozen mode (`--check` with no receipt) has no selftest case, because covering it hermetically would need the real archived bytes. Its correctness rests on L1's direct frozen run. I do not count this as the hole.
- I make no claim about runtime pass or fail; L1 runs all checks.

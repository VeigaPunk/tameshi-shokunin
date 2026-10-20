# FalsifyControl — round 15 wave 2 critic

Target: `tools/context-capture.py` (snapshot tag `#472A`). The question was whether a receipt whose stored `positive_control.effective` contradicts an injected run that exited 0 gets caught, without the tool claiming it re-executed git.

## Source read (static only; I executed no verification)

- `tools/context-capture.py:1-106` (docstring), `146-175`, `252-277` (USAGE), `439-512`, `604-620` (`validate_positive_control`), `878-1015` (`recompute_comparison`, `recompute_positive_control`), `1108-1181` (`verify_recorded_verdict`, `check_receipt`), `1222-1345` (result/expected/run_check), `1500-1545` (fixture control block), `1579-1730` (`SelftestHarness`), `1784-1804`, `1928-1945` (selftest control and verdict cases). I also grepped the file for `subprocess.` and for exit/stderr mutations.
- Historical `.ufo/evidence/round-14/capture-context.py:395-411, 570-571` (`positive_control_block`, `decide`), via grep.
- The retained positive-control block of `.ufo/evidence/round-14/context-receipt.json`, read once with a read-only `python3 -c json.load` print. It records injected exit 128, stderr naming the poison path, all three flags True, and status `ok`/0/`[]`.
- Routed defect 5 in `corpus/lessons/round-14-verifier-spotcheck.md:154-162`.

## Where the source agrees

1. **The recompute matches the historical formula.** Line 984-989 matches historical 403-409 exactly:
   - `baseline_ok = exit==0 and stdout.strip()!=""`
   - `reflects = POISON in stdout or POISON in stderr or injected.exit != baseline.exit`
   - `effective = baseline_ok and injected.exit != 0 and reflects`

   With the injected exit set to 0, the recomputed `effective` is False whatever stdout/stderr contain. A stored `effective: True` therefore produces a `positive_control_ineffective` problem (line 999-1002). If the stored verdict also says ok/0/[], `receipt_verdict_mismatch` is added after it (line 1120-1126). Findings keep their order, so the primary id stays `positive_control_ineffective` with exit 1 (line 1340).
2. **No claim of re-executed git.** Outside the selftest harness the file has no `subprocess` calls; the only one is line 1603, which runs `sys.executable -I SELF`. The docstring (line 11, 100-103) says the tool "does not execute the probe or git" and that a pass "is not proof that the historical commands were re-executed". The stored `positive_control.argv` (`/usr/bin/git … rev-parse --git-dir`) is only validated as data, never run.
3. **Types are strict.** `require_bool` rejects a non-bool `effective` (line 612). `require_int` uses `type() is int`, so `exit: true` or `false` cannot pass for an integer exit (line 443).

## The one hole: the selftest never tests effective's own condition

The two control cases never separate the `injected.exit != 0` part of `effective` from the `reflects` part:

- **`control-ineffective` (1784-1794):** injected exit 0, stderr "", and both flags stored False. The recomputed `reflects` is False, so `effective` is False with or without the exit test. It is caught by the `elif effective is False` branch.
- **`control-flag-lie` (1796-1804):** injected exit 0, stdout and stderr both "", with the stored `injected_reflects_poison: True` left from the base fixture. That stored `reflects` flag is already wrong, so the case passes on line 995 before `effective` matters. It sets no `expected_ids`.

**Mutant that survives.** Delete `injected["exit"] != 0 and` from line 989, leaving `effective = baseline_ok and reflects`:
- the clean case, frozen replay and `control-ineffective` still get the same answers;
- `control-flag-lie` still produces `positive_control_ineffective`/1 through the `reflects` problem.

All pinned id/exit pairs are unchanged, so `--selftest` cannot detect a gate that accepts an injected exit 0 as an effective control. That is exactly the target's contradiction.

**Counterexample receipt.** Start from `build_fixture_receipt()` and set:
- `positive_control.injected.exit = 0`;
- `positive_control.injected.stderr = "warning: '/nonexistent/tameshi-round14-poison'\n"`;
- leave `injected_reflects_poison: True` and `effective: True`, plus the top-level `status "ok"`, `exit 0`, `reasons []`.

| Version | What it does | Result |
|---|---|---|
| Delivered source | `reflects` is True, which matches the stored flag; recomputed `effective` False vs stored True | `positive_control_ineffective`, plus `receipt_verdict_mismatch`; primary `positive_control_ineffective`, exit 1 |
| Mutant | `effective` True; no findings | `context_consistent`/0 |

The mutant's `context_consistent`/0 would differ from a `positive_control_ineffective`/1 pin.

This is a fixable defect in the selftest, not a source-logic defect and not a tradeoff. It falls under routed defect 5's requirement that the selftest test exits and stable finding IDs. It does not widen the bounded retained-replay C1 scope.

## Impacted axes

- The selftest's red-proof discrimination for the positive-control re-derivation.
- Source correctness, exit map, frozen replay and the no-re-execution claim are unaffected.

## Smallest safe correction

Add one selftest case next to `control-flag-lie`:

```python
def control_effective_lie(document):
    document["positive_control"]["injected"]["exit"] = 0
    document["positive_control"]["injected"]["stderr"] = (
        "warning: '" + POISON_PATH + "'\n")
    # injected_reflects_poison stays True (truthful); effective stays True (lie);
    # stored status/exit/reasons stay ok/0/[]
harness.check_case(
    "control-effective-lie", mutate(control_effective_lie),
    "positive_control_ineffective", 1,
    expected_ids=["positive_control_ineffective", "receipt_verdict_mismatch"])
```

Optionally, give `control-flag-lie` the expected ids as well. Do not change any production logic.

## Process

- Tool installs/updates: none.
- No pacman, uv or npx use.
- I wrote only this report and did not message TameshiR15: the source is correct, and only the selftest misses this case, so it is not implementation-critical.

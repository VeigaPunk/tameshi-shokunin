# FrozenEvidence — selftest intent and boundary

## Axes

- **Gate conformance:** does the selftest exercise the maintained tool's verdict through its CLI, with literal expected exit/finding results?
- **Hermeticity:** can it pass or fail using only synthetic fixtures under a temporary root?
- **Historical no-harm:** does it leave the round-14 source and receipts untouched and avoid restating the round-14 experiment as new evidence?

## Reconstructed contract

The selftest is a regression test for the **new active command**, not a rerun or frozen-state measurement of the round-14 context experiment. It should demonstrate that the public command classifies a synthetic clean fixture, a synthetic verdict mismatch, and an input/usage failure correctly. Its expected results are literals; its inputs and any digests are generated inside its temporary fixture. It must not read the live lane's round-13 pins, probe, runner, or round-14 receipt, execute the round-14 harness, or write outside the temporary root.

The normal capture operation is separate: it may observe the live inputs and produce only the new round-15 receipt. Keep `.ufo/evidence/round-14/capture-context.py` and every round-14 receipt/guardrail byte historical and unchanged.

## Evidence chain

1. **The original source describes a measurement, not a selftest.** The historical file `.ufo/evidence/round-14/capture-context.py` says it runs the pin probe twice under baseline and injected environments, compares the results, statically maps six runner legs to round-13 pins, never runs the runner, and writes `.ufo/evidence/round-14/context-receipt.json` (source lines 2–31). Its input paths are fixed (lines 54–60); `evaluate()` reads those lane files and runs the probe/Git positive control (lines 465–550). `decide()` returns clean or mismatch based on comparison, source pins, environment, control, and mapping (lines 553–580), and `main()` writes the receipt and returns 0/1/2; unsupported arguments return 64 (lines 605–643). That is persisted-expectation verdict behavior, even though the file called itself a context probe.
2. **Round 14 explicitly had no selftest.** `ReceiptHarness.md` says “No selftest is defined; do not look for one” (lines 135–145), documents the live experiment and fixed round-14 write (lines 18–82), and records that it was not executed by that seat (lines 1–7). The helper controls in `.ufo/evidence/round-14/guardrails.json` are Python `-c` checks and a `runpy` call into helper functions; they are not the harness's public CLI self-invocation (guardrails lines 21–47). The retained context receipt records an actual round-14 `GIT_DIR` injection and `status=ok`, `exit=0` (context receipt lines 14–28, 421–423), but that is measurement evidence, not selftest evidence.
3. **The routed correction distinguishes the two.** `corpus/lessons/round-14-verifier-spotcheck.md:160` says the digest/mapping comparisons against committed expected values make the “probe” a gate, and requires a standalone isolated self-invocation checking exits and stable expected finding IDs. It also says the harness's source-defined exit 64 was missing from its registry. The same note at line 162 says a static count printer is not a verdict gate merely because it prints counts, and not every finding ID needs its own fixture. `SKILL.md:1570–1576` bounds the round-14 observation: a prospective context result applies only to that experiment and does not establish general hermeticity or safe reuse; `SKILL.md:1592–1595` still describes the old harness as a round-14 opt-in probe.
4. **No existing stable mismatch IDs or selftest can be reused.** The historical source's `InvalidContext.kind` values identify input errors, but `decide()` emits free-text reasons rather than stable finding IDs; `main()` has no `--selftest` branch. The current `tools/` inventory has no `context-capture.py`; the active path is a new command, not a reason to edit the archived script. The LSP device is unavailable (`read xd://lsp` returned “No such tool”), so this is based on direct source/document reads, not semantic-reference results.

## Exact minimum correction for the maintained command

1. Add `--selftest` to the new `tools/context-capture.py` and dispatch it before any live capture, receipt creation, or external probe/Git invocation. Make the selftest stand alone from current lane evidence.
2. Build one compact synthetic lane under a temporary directory. Invoke the exact maintained script as a child process (`sys.executable` plus its resolved `__file__` path), using a fixture-root entry path/option and a temporary output location. Use synthetic probe/Git shims or equivalent controlled fixture inputs so no host measurement occurs. Assert the child exit and stable result identifier(s), not only a summary string. Clean the temporary directory on every path.
3. Minimum literal cases:
   - synthetic valid capture: **exit 0**, no finding IDs;
   - one deliberately failing synthetic verdict predicate: **exit 1**, one fixed mismatch ID (for example, `context_mismatch`); the ID must be defined by the maintained command because round-14 `decide()` has only free-text reasons;
   - one malformed synthetic input: **exit 2**, assert the exact stable input ID (the source already has `InvalidContext.kind`, e.g. `invalid_manifest`, available as a basis);
   - one unsupported argument: **exit 64**, classified as **usage**, with no receipt. The round-14 source defines 64 as usage/no receipt, so do not relabel this harness's 64 as could-not-evaluate. Registry rows must name the context command's 64 class explicitly.

The proposed `context_mismatch` is a new stable identifier recommendation, not an observed identifier in the historical implementation. A fixture may cover one representative mismatch; the round-14 note explicitly does not require one fixture per emitted ID. A clean/mismatch/tamper selftest is not a source digest census, mutation sweep, rerun of `GIT_DIR` injection, or claim of fresh mutation effectiveness.

## Scope and confidence

**Do:** add and register the standalone selftest only in the new active command; preserve its default capture/write behavior as round-15-only; record literal expected exit/result pairs.

**Do not:** alter/re-hash/rewrite round-14 files, import round-14 mutable inputs into selftest fixtures, rerun old capture or sibling gates, add broad environment/reuse claims, or turn selftest into a frozen-input measurement.

Confidence: **high** on the historical measurement/selftest distinction and the needed gate/self-invocation correction (direct source plus routed closure evidence); **moderate** on the proposed minimal fixture mechanics because the new active command is absent and its CLI/output interface was not reviewed. No selftest, gate, build, lint, or verification command was run; no tools were installed.
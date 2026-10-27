# T51W2CritC3Truth — C3 row falsification

Axis: **operability**, with cross-claim impact on **calibration** (cold-read truth). Candidate `6d8c11e378aa90b12650808e1b79270742935f15`; base `9962033fd7a75aa2f2847e979dd687a5d28505a1`. Frozen contract and counter: `.ufo/evidence/round-51/contract.json` C3 lines 45–57; `.ufo/evidence/round-51/c3/measure.py` predicate lines 5–27, implementation 117–184. Candidate rows: `git show 6d8c11e…:SKILL.md`, round-51 table at lines 2140–2171.

## F1 — Round21 facade is a truthful row which fails C3

The `round21 measure facade` row (SKILL.md:2157) truthfully registers `python3 tools/round21-measure.py --selftest`, expects `ROUND21_MEASURE_SELFTEST: 13/13 pass`, and describes its external pins. From the counter's fresh clone at CAND the command exits **1**, with no stdout: `git show 175de6ba…:scripts/kimi-census.mjs` fails because the clone lacks sibling `kumitate-shokunin`. Independent row-level reproduction is retained in `.ufo/waves/round-51/w2/@P@ExecTool07/15-row16-round21-selftest-clone-context.stdout`; the frozen counter's full run is `.ufo/waves/round-51/w2/@P@ExecTool02/c3-counter-full-run.txt` (line 16: `MISSING ... selftest-exit=1 last=`). This is a genuine inability to meet the frozen requirement, not a row formatting error. Do not alias `--help`, shim sibling repositories, or fabricate a pass.

**Verdict:** A canonical table with one truthful failing tool does **not** satisfy the frozen predicate. C3_R51_PASS is honestly **false** at CAND: the counter requires every tool covered and total=0; this single uncovered tool makes missing/total nonzero (contract C3 predicate and counter lines 5–25). Leave the row truthful and report the frozen claim red unless the frozen scope is lawfully amended outside this review.

## F2 — Other row-level falsifications are counter blind spots, not a reason to counterfeit a green

The independent executor evidence shows that a passing row need not be fully truthful. For example, `tools/registry-check.py` row (SKILL.md:2154) is counter-credited, but its quoted purported last line appends `at 84aa673`; actual output is `SELFTEST: PASS (51 cases)`. The counter compares only the first token (measure.py:178–180). Evidence: `.ufo/waves/round-51/w2/T51W2ExecTool13.md` §§1, 4, M1 (especially lines 123–143), with candidate source/output receipts in `T51W2ExecTool13/`. This is a marker/provenance mismatch and impacts calibration; it does not repair F1.

`tools/receipt-measure.py` row (SKILL.md:2152) says exit 2 is “only on usage”; its pinned stage measure also returns 2 for no resolvable revision when `--repo` is given without `--rev`. Evidence: `.ufo/waves/round-51/w2/@P@ExecTool11.md` §3.1 and `@P@ExecTool11/03-exit-code-survey.txt`. It is a false exit-map gloss that the counter's token-presence check misses, impacting operability description, not the frozen result.

## F3 — Scope and limits of this review

The supplied aggregate counter and peer reports establish the CAND table's decisive outcome: 29 tools have runnable rows while `round21-measure.py` is missing; see `.ufo/waves/round-51/w2/@P@ExecTool02/c3-counter-full-run.txt`. I inspected the frozen predicate and candidate table and checked concrete falsifiers against executor receipts; I do not claim an independent execution/audit of every cell in all 30 rows. The smallest safe correction is no row lie: retain the truthful failing row and declare C3_R51_PASS=false under the unchanged freeze. If a future claim wants a green, first make the self-test genuinely pass in a fresh clone without changing its meaning, or establish a separately authorized contract amendment; neither is part of this seat.

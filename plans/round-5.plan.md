# WWKD plan — tameshi round 5 (ufo-round-plan-v1)

Axis set: depth (mutation-craft), calibration (suite honesty), operability.
Axis move: **depth** — the third worked mutation case, in a third shape: kotoba
`verifiers/verify_corpus_independent.py` (Python; sha256 `430fe289…`).
Claim (falsifiable): 10 single-edit mutants (same N as both prior cases, for
comparability) swept through `tools/mutate-and-run.sh --target
kotoba-shokunin/verifiers/verify_corpus_independent.py --suite 'python3
"$MUTANT" --self-test'` on fresh /tmp copies measure (a) the kill-rate in a
third language and (b) the matrix's §4 width mechanism (I) by taking its
missing cell — this suite rebuilds fixture roots per section
(`tempfile.mkdtemp` :599; `_fixture_index` :604, `_fixture_pointers` :638,
`_fixture_clean` :703) like the bash case AND asserts exact equality (`st.eq`,
54 literal sites / 52 executed) plus 2 CLI end-to-end runs (:726-739) like the
JS case. Resolution test, pre-registered: if per-mutant width stays
near-singleton (bash-like), fixture-per-case isolation is the dominant factor;
if one edit breaks many assertions (JS-like), assert exactness is — one of the
two must move, and the (I) becomes measured either way. Also pre-registered:
every value/count/behavior mutant handed to the suite dies; any survivor sits
in reported-but-unasserted surfaces (row D — e.g. the `--json` remainder beyond
the two keys read at :732 / :738, the printed text lines) or unreached arms
(row E).
Why this gate (measured, read-only, 2026-10-14; scratch /tmp/w4-prept5-* only):
(i) fleet survey of self-test-bearing gates — `grep -rln --include='*.sh'
--include='*.py' --include='*.mjs' --include='*.js' -E 'self[_-]test|SELFTEST'
*/` → non-JS, non-bash candidates are kotoba ×5 + fault harness, kengaku
`grader.py`,
revenger ×6, `.ufo/waves/round-15/closure-check.py` (kumitate = JS, kagi and
tsukuroi = bash, kake = mjs, game batteries have no self-test suite above
them); (ii) prior gate-mutation campaigns exclude the pick — closure-check 7/7
(`mutation-gate.md`), kengaku 4/4 + 11/11 + 18/18 (its SCORECARD rows), kotoba
siblings 13 faults (kotoba LOG.md:501) and a 46-row harness on
`verify_skill_checklist.py` (LOG.md:745-746), while no campaign is recorded on
this artifact (its LOG/SCORECARD mentions are agreement, cold-run, freshness
and pin records — e.g. LOG.md:376, SCORECARD.md:29);
(iii) specimen — 776 lines, pin = the one kotoba's own SCORECARD.md:29 already
records, `--self-test` → `self-test: 52 assertions, 0 failures`, exit 0
(measured this lane; ~0.1 s, /tmp-only writes, pin held after, kotoba porcelain
0 lines @ `02302c5`); 54 literal `st.eq` sites vs 52 executed (the two env-gate
try/except pairs execute one branch each) — the executed count, not the static
count, is the denominator. Fallback if the pinned bytes drift before the round:
kotoba `verify_harness_claims.py` (same lane and assert style, 10 executed
assertions).
Anti-claim: a survivor outside the matrix's classes (the differential property,
the env gate, the aggregate `report_total`) is the finding — the matrix gains a
row, never an average; if the tool cannot express the case (spec v1), that is
the operability finding.
Also: `--regression` (r4-2) gains case 3 as an embedded spec + recorded
expectation row, so the tool's own gate covers JS + bash + Python.
Deferred (stated, not absorbed): the fleet-wide suite-completeness census as
tameshi's service round — round 6+; the census's classification vocabulary
should first be tested on three shapes, and its seed table is the survey above.
SHONEN evidence: e2e = the third worked case (kill table + case note); the case
doubles as the first non-author test of the r4 matrix on a shape it did not see
(rows D/E checked before the sweep, not after).
Measure: kill table (mutant → KILLED/SURVIVED/INCONCLUSIVE + failing assertion
numbers); control `52/52` green before any mutant run; pin `430fe289…`
before=after (`MUTATE_RESTORE: OK`); kotoba tree porcelain-empty before/after;
per-mutant width; matrix row verdicts; note
`corpus/knowledge/mutation-case-kotoba-independent.md`; the round record folds
into SCORECARD/LOG at lane review.
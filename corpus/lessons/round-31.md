# Round 31 — lesson (tameshi)

Base `36c1d3933f680125aeefc447f07db0f03004901a` (round-30 spot-check head). L1 TameshiR31, attempt 1
(no `lane-dead-no-report tameshi round=31` line in `.ufo/watchdog.log`; nothing inherited; the lane was
clean at start, `jj-lane.sh state`: `tracked=0 untracked=0`).

One claim, **C1 — calibration, measured**: the standing rows of `SCORECARD.md`'s `| Capability |` and
`| Axis | Score (0–10) |` tables against what each row's own command prints. Frozen in
`.ufo/evidence/round-31/contract.json` with the counter `.ufo/evidence/round-31/c1-measure.py` at
`c111dab5` before any seat ran. Sourced on S055 (re-opened), S095 and S096 (new), through the entry
`corpus/knowledge/executable-self-assessment.md`.

Round order: freeze `c111dab5` (counter, contract, binding v4, base receipt) → wave-1 dispatch record
`ce1d7a64` → wave-1 control receipts and binding v5 `87eb64eb` → content revision `2da841bd` (SCORECARD
rows, SOURCES, QUALITY 66-71, README row, knowledge entry, one SKILL.md line) → wave-2 dispatch record
`3351738a` → ledger append `83c001a5` (the measurement revision) → this record.

## Gate

Sources opened this round (every new or touched row; quotes located in the fetched bytes by the seat
named, and re-opened in wave 2 by a second seat with equal digests):

- **S055** (existing row re-opened; seats SrcDoctest, ReopenS055): https://docs.python.org/3/library/doctest.html,
  fetched 2026-10-23, 216574 bytes, sha256 `369dcc17009a2f36000284ca86eedb7cef4bc10f773e554754bbdad07791cc46`.
  Quote (module introduction, first common-use bullet, HTML lines 249-250, 18 words): "To check that a
  module’s docstrings are up-to-date by verifying that all interactive examples still work as documented."
- **S095** (new; seats SrcGoExamples, ReopenS095): https://go.dev/blog/examples, accessed 2026-10-23 UTC,
  40059 bytes, sha256 `1a40ae77c967d7e203b8d7706784bd6633542ff3583d197d854755233c958178`. Quote
  (§Output comments, HTML lines 514-517, 11 words): "The test passes if the test’s output matches its output comment."
- **S096** (new; seats SrcRustdoc, ReopenS096): https://doc.rust-lang.org/rustdoc/write-documentation/documentation-tests.html,
  accessed 2026-10-23 UTC, 51137 bytes, sha256 `95572c7300af0f27eab4c7ed47125a509a9c5854fc80dc2d7fd162d894de3cb7`.
  Quote (§Documentation tests, HTML lines 181-182, 22 words): "rustdoc supports executing your documentation
  examples as tests. This makes sure that examples within your documentation are up to date and working."

Row changes, old → new (`corpus/SOURCES.md`, rows 92 → 94):

| ID | status | recheck | used-by |
|---|---|---|---|
| S055 | mined → mined | on-release → on-release | `corpus/lessons/round-16.md` → `corpus/lessons/round-16.md, corpus/knowledge/executable-self-assessment.md` |
| S095 | (none) → mined | (none) → 180d | (none) → `corpus/knowledge/executable-self-assessment.md` |
| S096 | (none) → mined | (none) → on-release | (none) → `corpus/knowledge/executable-self-assessment.md` |

S055's `opened` (2026-10-20) and anchor (Python 3.15.0) cells were left as written; the live page is
3.15.1 (ReopenS055). The entry renders the S055 and S095 apostrophes as ASCII `'` where the pages use
U+2019 (ReviewEntry L1); the words are verbatim.

Rejects (each a real reject with its reason):

- **SrcDoctest's draft row "S095" for the doctest page: rejected** — same URL as S055; a second row
  without `supersedes S055` would be census E04 (ReopenS055). S055 was re-opened instead.
- **SrcRustdoc's id "S095": rejected** — it collides with the Go row; ids allocated Go S095, rustdoc S096.
  SrcRustdoc also flagged that `mined` needs the citing entry to exist: the rows landed in the same
  commit as the entry (`2da841bd`).
- **Binding v4: rejected before data.** CtlBindV4Old killed the seven round-30 shapes and the five
  controls (0/32 each), but CtlBindV4New kept 63/63 forged entries with five lexical shapes (literal
  heredoc, `python3 -c tools/trace-inputs.py …`, `false && <call>`, an uncalled function body, a quoted
  `';'` argument), and ReviewBindV4 listed further false accepts (FA-1..FA-8). v5 was written and
  re-scored before any wave-2 seat: 63/63 real round-30 entries kept, the 9 new shapes and the 7 old
  shapes and 5 controls all at 0 (`.ufo/evidence/round-31/ctl/README-bind-v5.txt`,
  `contract-addendum-1.json`). ReviewContractTrail notes the addendum is the L1's own supersession,
  not part of the original freeze; it touches only the no-harm instrument, never the C1 counter.
- **A pre-data "stale count" reading of seven calibration errors: rejected as the size of the gain.**
  CriticC1 (pre-data) and CriticC1After: the round-1 axis table is an explicitly dated baseline, and a
  round-17 prose line had already superseded four capability counts; of the seven base mismatches,
  three were stale *current* statements (runner 95/95, regression 7 legs, evidence-disposition 56/56 in
  that line) and the rest were dated literals with no current restatement. The counter's 7 → 0 stands as
  measured; the gain is reported with that decomposition.

## Controls before data (wave 1, 32 seats, none dead)

Every control ran the frozen counter, unchanged (sha256 `657fcc12…7584`), on its own sandbox commit.
Summary generated by command over the reports: `.ufo/evidence/round-31/ctl/c1-controls-summary.txt`.

| Control | Result | Reading |
|---|---|---|
| CtlDoNothing | `mismatches=7`, PASS false | the target is out of a do-nothing round's reach |
| CtlJunkRows | 12 mismatches, false | wrong values in the parsed phrase forms fail |
| CtlLabelShortcut (old values keyed on ids) | 7 mismatches, false | a label shortcut fails |
| CtlLabelShortcut (values read from the committed base receipt) | 0, **true** | route control: correct values copied from a fresh receipt; the contract (`controls_before_data`) declared this route before data, since the counter measures agreement itself |
| CtlReceiptCopy | V1 1 mismatch (no committed receipt said 92 rows), V2 0, **true** | same route; stale receipts fail |
| CtlRowsDeleted A/B/C | 12 unparsed, false | deletion fails closed |
| CtlHiddenRows (comment, fence, indent) | 7, false | hidden rows are not read |
| CtlRewriteInPlace A/B/C | false (append_only=0; B also last-row order) | history rewrite fails |
| CtlWrongHeader A/B/D | false | |
| CtlWrongHeader C (`| Axis | Score |`) | 0, **true** | the code accepts any second header cell starting `Score`; the contract text says `Score (0–10)`. Recorded, not amended; the round-31 rows use the exact header (Mistake 5) |

MutCounter: 2 of 8 counter mutants killed by its three fixtures; four survivors (append-only ignored,
UNPARSED as match, header prefix, hidden-table stripping off) are each killed by a separate control
above; two (observing at base, exit forced to zero) stay fixture gaps. DeterminismProbe: two counter runs
byte-identical in their STATEMENT lines; 4/4 regression runs PASS. CtlLabelShortcut's restored run saw
one `--regression` FAIL (`bash-tsukuroi-census B7 measured=KILLED recorded=SURVIVED`); RegressionFlake
traced it to a SIGPIPE race in the pinned tsukuroi suite (`set -o pipefail` with `printf … | grep -q`,
`tsukuroi-census.sh@165307fe:139,771-777`), load-sensitive, not a B7 effect. ReviewCounter: the counter
matches its docstring; fail-safe gaps only (a locale-undecodable output raises instead of UNOBSERVABLE).
SentinelCounter: the counter symlinks the real sibling repos into `--work`; the regression replay's git
use is read-only, but the links are writable in principle (MEDIUM).

## After measurement

Measurement revision `83c001a5d95f33a78a9e2d51f5ec1c9a6ddf2217` (SCORECARD rows from `2da841bd` plus the
ledger append). First full counter run there (`.ufo/evidence/round-31/after/c1-at-83c001a5.stdout`, exit 0):

```
C1_R31: statements=12 mismatches=0 unparsed=0 unobservable=0 append_only=1 rev=83c001a5d95f33a78a9e2d51f5ec1c9a6ddf2217 C1_R31_PASS=true
```

Before at `36c1d393`: `mismatches=7`, PASS false. At the content revision `2da841bd` (seats RerunC1Content,
ReviewScorecardRows, MutateC1RowsA/B): 11/12, the calibration row claimed 8 while the drifted monitor read
6, as planned. Row sensitivity at `2da841bd`: a one-value mutation of each of the 12 last rows makes that
statement MISMATCH (11 informative; the calibration row was already red there).

No-harm: strict monitor at `83c001a5`: `C1_MONITOR: covered=64/64 restraint=8 box3_mismatch=0
depth_score=9` (`after/c1monitor-at-83c001a5.stdout`); at the content revision 55/64, restraint 6 (nine
drifted sections: eight by input drift on SOURCES/QUALITY/README, one by the SKILL.md line edit;
MonitorAtRev). Wave 2 gave each drifted section three fresh readers (groups A/B/C); 24 entries assembled,
24 kept by binding v5, appended 456 → 480, prefix equal as data (`coldread/append-receipt-w2.json`).
Census exit 0 (eight W04, unchanged set; RerunCensus). Command D `recorded_cases=9 depth_score=9`. Tools
unchanged since base.

## Mistakes

1. **class:** reviewer authority taken from a seat's label, not from who dispatched it. **evidence:**
   `SCORECARD.md:1473` ("named non-author seat") vs `corpus/lessons/round-30-verifier-spotcheck.md:40-43`.
   **captured-by:** the round-30 closure, conformance step. **fix:** erratum appended to SCORECARD (round-31
   block) and QUALITY 66. Shown able to fail: the round-30 row itself, at `SCORECARD.md:1473`.
2. **class:** a line-range cite wider than its paragraph. **evidence:** `corpus/lessons/round-30.md:59`
   cites `regression-tally-completeness.md:60-62`; the paragraph is line 60 (61 blank, 62 `## Limits`).
   **captured-by:** CloseSpotSources. **fix:** erratum here — read that cite as `:60`; QUALITY 70. Shown
   able to fail: `:60-62` includes the `## Limits` heading.
3. **class:** process deaths attributed to the seat's own timeout without checking who killed them.
   **evidence:** `.ufo/waves/round-30/wC/ColdA09.md:139-146` vs `TameshiR30A3.ColdA01.jsonl:173-176`
   (kill of PIDs 321391 and 321402 at 07:32:43Z). **captured-by:** the round-30 closure (`:181-186`).
   **fix:** the section-26 note below and the SKILL.md recipe sentence (per-seat `--workdir`, cwd check;
   QUALITY 67). Section-26 note for ColdA09 (round 30): ColdA01's cleanup at 07:32:43Z killed two `bash`
   selftest processes in ColdA09's replay workdir `/tmp/tameshi-r4-2-regression.1e5R9E`; the attribution
   of those two deaths to ColdA09's own 300 s / 560 s timeouts is withdrawn. Section 26 still has no
   complete `--regression` receipt from ColdA09; the full nine-leg replay is ColdB09's (`wC/ColdB09.md:34`).
4. **class:** standing self-assessment literals not refreshed when the tools changed; a prose
   "supersedes" line drifted the same way. **evidence:** `.ufo/evidence/round-31/before/c1-at-base.stdout`
   (`mismatches=7`); `SCORECARD.md:632-636` (round 17: 95/95, 7 legs, 56/56, all stale at base); first
   divergences dated by ScribeMistakes31 (`c699c8c` seventh leg, `2a22ade` pin 19 and new
   evidence-disposition cases). **captured-by:** none until this round's counter. **fix:** C1's appended
   rows and QUALITY 71. Shown able to fail: the base receipt, exit 1.
5. **class:** the contract's description of the frozen table type is narrower than the counter's code.
   **evidence:** `contract.json` surface "`| Axis | Score (0-10) |` tables" vs `c1-measure.py`
   `header[1].startswith('Score')`; CtlWrongHeader shape C passed with `| Axis | Score |`.
   **captured-by:** the control wave (addendum §9: one predicate, same sentence in plan and code).
   **fix:** next contract quotes the exact code condition for every table or row selector, and a control
   per selector clause runs before freeze. Shown able to fail: CtlWrongHeader C, `C1_R31_PASS=true`.
6. **class:** a binding frozen with lexical blind spots. **evidence:** CtlBindV4New (five shapes, 63/63).
   **captured-by:** QUALITY 69 (controls before data). **fix:** v5 before data; residual false accepts
   found by ReviewBindV5 (double heredoc on one line, `f () {` with a space, a later error result after a
   clean one) are routed. Shown able to fail: `ctl/bind-v5-new-shapes.stdout` kills all nine v4 survivors
   and controls.
7. **class:** wave text not regenerated after an instrument changed. **evidence:** `spec-w2.json`
   `context` says readers are bound by "binding v4 (…/bind-select-v4.py)", while every cold-read item's
   recipe names v5, the instrument actually frozen and applied (ReviewQuality31 finding 3). The contract's
   drift plan also omitted the SKILL.md line edit (RerunC1Content). **captured-by:** none before dispatch.
   **fix:** the wave generator takes the binding path from one variable used in both context and recipe.
   Shown able to fail: `git show 3351738a:.ufo/waves/round-31/spec-w2.json | grep -c bind-select-v4` is
   nonzero.

Holds: wave-2 seat CtlBindV5Fresh (mutation-tester) died on a provider safety filter
(`Codex error event: This content was flagged for possible cybersecurity risk … (code=cyber_policy)`).
Its item ends there; it was not retried or rerouted, and none of its output is evidence.

## Routed defects of round-30-verifier-spotcheck.md

1. JudgeC1 "non-author" → erratum in the SCORECARD round-31 block; QUALITY 66. Resolved.
2. Cold-read recipe `--workdir` + cwd check → `SKILL.md:1886` sentence (round 31) and QUALITY 67; ColdA09
   note above. Partial: ReviewSkillRecipe asks for "processes it started" in the SKILL sentence (routed).
3. Dead-seat check → `.ufo/evidence/round-31/dead-seat-check.py` (fails on the round-30 pair: 1 FLAG,
   exit 1); run before wave 2 (`dead-seat-check-w2.txt`, wave 1 had no dead seat). Partial: its 0.60
   default cannot separate cold-read items (ReviewDeadSeatCheck F2); three mutants survive its selftest
   (MutDeadSeatCheck M04, M05, M12).
4. Binding v4 / per-leg tally / 8 guard survivors → binding v5 (resolved for the tested shapes). The
   per-leg tally check and the 8 MutateHead survivors stay deferred: `tools/mutate-and-run.sh` is an input
   of 270 of 456 ledger entries (ReviewRoutedR30: 26 latest-entry sections would drift). This re-defers
   round 30's route ("opens round 31's content revision"); stated, not hidden.
5. Lesson cite `:60-62` → Mistake 2 above; stale `Next unused id: S092.` → SOURCES note (round 31).
   Resolved.
6. Owner of `/tmp/tameshi-r4-2-regression.j0FKnk` → TameshiR30A3.ColdA08 (RevengerStrayTmp; agreed by
   ReviewStrayOwner): created by its `registry-check.py` replay (tool call `88ac577c`, 07:20:56Z), workdir
   kept after its own `timeout 330`. Resolved.

## Routed to round 32

- Runner: per-leg presence in the `--regression` tally and the 8 MutateHead selftest survivors.
- Binding v5 false accepts (ReviewBindV5 FA-1..FA-3) and false rejects (line continuations, control
  structures, `--out "$O"`).
- Dead-seat check: a cold-read-aware threshold or anchor rule, the three surviving mutants, wiring into
  the wave generator.
- C1 counter fixtures for the two MutCounter survivors; header selector quoted exactly (Mistake 5).
- `tools/mte-interop.py --selftest` prints `SETUP (No module named 'jsonschema')` on this host: the
  capability is not runnable here (stated in the re-stated row).
- QUALITY errata: criterion 69 cites Mistake 2 at `round-30.md:69-73`, its body is `:148-153`; criterion 71
  routes this round's own C1, not a round-30 item (ReviewQuality31).
- Adjacency (not absorbed): the tsukuroi suite's SIGPIPE race under `pipefail`
  (`.ufo/waves/round-31/w2/RegressionFlake.md`) belongs to tsukuroi-shokunin; the lane's recorded
  `SURVIVED` for B7 is right and stays.

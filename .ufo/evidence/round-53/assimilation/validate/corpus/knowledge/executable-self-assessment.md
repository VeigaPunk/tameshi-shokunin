source: S055 — Python documentation, "doctest — Test interactive Python examples", module introduction (re-opened round 31, seat SrcDoctest); S095 — Go Blog, "Testable Examples in Go", §Introduction and §Output comments; S096 — The rustdoc book, "Documentation tests", §Documentation tests (all opened 2026-10-23; URLs below)
verified-at: 2026-10-23 — the cited source sections were opened with curl by round-31 seats (SrcDoctest, SrcGoExamples, SrcRustdoc, ScribeEntry); the round-31 rule below is a local inference from those examples and the frozen contract, not a claim the sources make
recheck: `python3 .ufo/evidence/round-31/c1-measure.py --rev REV --work EMPTY_SCRATCH_DIR` (an empty work directory; it compares the last matching SCORECARD rows with their commands' output at REV and checks the base-file prefix); re-open the cited source sections

# Executable self-assessment rows: claims with checks

A standing capability row says what a tool can do and quotes what its command printed. A standing
axis row states a score. Each is a claim about the repository at some revision, not a timeless fact.
Give the claim a check: run the row's own command at the same revision and compare the values the
row states with the values the command prints.

When the tool changes and the row does not, the row goes stale. Stale means "needs a fresh check";
it does not by itself prove the row wrong, and a dated row that names its measured revision may
still be true of that revision. A re-check either confirms the values or shows they need a new
statement.

## What the sources say, and what this entry infers

The sources describe executable examples in three language ecosystems:

- **S055, Python `doctest`, module introduction:** "To check that a module's docstrings are
  up-to-date by verifying that all interactive examples still work as documented." Location: first
  common-use bullet, <https://docs.python.org/3/library/doctest.html>.
- **S095, Go Blog, §Output comments:** "The test passes if the test's output matches its output
  comment." Location: <https://go.dev/blog/examples>; §Introduction also says examples are
  "verified by running them as tests."
- **S096, rustdoc book, §Documentation tests:** "rustdoc supports executing your documentation
  examples as tests. This makes sure that examples within your documentation are up to date and
  working." Location: <https://doc.rust-lang.org/rustdoc/write-documentation/documentation-tests.html>.

Those are the sources' claims about documentation examples. **Inference in this entry:** a
SCORECARD row that quotes a command's output is a documentation example of the lane's own tools,
so the same remedy applies: execute the quoted command and compare. The language sources do not
establish the SCORECARD rule; the local rule comes from round 31's frozen contract and counter.

Adjacent prior art (read-only, sibling lane): kumitate-shokunin re-derives its own SCORECARD terms
with `scripts/proxy-check.mjs` (`corpus/knowledge/executable-scorecard.md` at kumitate
`9b33e03e`; seat ConnectorOverlap). It recomputes kumitate's own frozen terms from its own tree;
tameshi's check runs each row's quoted command instead. Cite, do not copy.

## Round 31's concrete check

C1 is a calibration claim over the standing `SCORECARD.md` rows. The frozen set is the ten rows of
the `| Capability |` tables and the two rows of the `| Axis | Score (0–10) |` tables
(`.ufo/evidence/round-31/contract.json`; `.ufo/evidence/round-31/c1-measure.py` docstring). For each
statement the counter takes the last data row in file order of its table type whose first cell is
the statement id, and compares its parsed values with the values the statement's frozen command
prints at the requested revision. Fenced code and HTML comments do not count. An unparsable row or
an unobservable command output is a mismatch, never a match.

```sh
python3 .ufo/evidence/round-31/c1-measure.py --rev REV --work EMPTY_SCRATCH_DIR
```

The base receipt (`.ufo/evidence/round-31/before/c1-at-base.stdout`) records seven mismatches of
twelve at `36c1d393`: the census row count (44 stated, 92 printed), the runner selftest (80/80 vs
106/106), the regression ledger (6 legs vs 9), the pin-disposition selftest (18/18 vs 19/19), the
evidence-disposition selftest (34/34 vs 66/66), and the depth and calibration scores of the round-1
baseline table (6 and 0 vs 9 and 8). Five matched. A round-17 prose line already marked four
capability counts as dated literals and gave successor counts; three of those successor counts were
stale again at base (runner 95/95, regression 7, evidence-disposition 56/56), so the prose
supersession was itself a standing statement that drifted.

## Preserve the old statement

Correct a stale row by appending a new statement; never edit or delete the old row. The frozen C1
predicate requires the base `SCORECARD.md` to stay a byte prefix and reads the last matching row,
so the old record stays readable and the later row carries the current claim. The new row names its
measured revision, so it is itself a dated claim that the next re-check can confirm or replace.
This append-only rule is an inference from the local predicate, not a claim of S055, S095 or S096.

## Limits

- A matching tally shows only that the selected row values equal the command's parsed output at that
  revision. It is not proof that the capability works in every way its prose describes.
- The check covers the frozen rows and phrase forms only. Other standing numbers in the file (the
  saturation sentence, line cites, receipt descriptions; seat ScoutStatements found four stale ones
  at the freeze) and the three later `| capabilities addition |` tables are outside it.
- Results depend on the environment: the counter runs each command in a fresh clone with the real
  sibling repos symlinked into its work directory (the regression replay reads them; seat
  SentinelCounter found the replay's git use read-only but the symlinks writable in principle), and a
  tool that needs a missing Python module prints SETUP on this host whatever the row says.
- An honest restatement copied from current committed receipts meets the check as well as a fresh
  run does (control CtlReceiptCopy): the check measures agreement, not how the values were obtained.

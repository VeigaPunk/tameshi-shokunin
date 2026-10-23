# ScribeEntry — Round 31 executable self-assessment

**Verdict:** The full knowledge-entry draft and its README row are ready for L1 to integrate. No production file was edited, and no C1 after-measurement is claimed.

## Evidence

- The frozen contract names **C1 on the calibration axis**, its surface (10 capability rows and the depth/calibration axis rows), its last-row and byte-prefix predicate, the frozen counter, and the required target: `.ufo/evidence/round-31/contract.json:9-27`. The counter docstring defines the same predicate and says the command exits 0 only when it passes: `.ufo/evidence/round-31/c1-measure.py:4-20`.
- The frozen command table associates each statement with its command and output pattern: `.ufo/evidence/round-31/c1-measure.py:34-65`. The parser selects the last row for each table type and ignores fenced code and HTML comments: `:78-123`. The observed output is compared with the parsed claim: `:206-224`.
- The baseline receipt's final line is exactly `C1_R31: statements=12 mismatches=7 unparsed=0 unobservable=0 append_only=1 rev=36c1d3933f680125aeefc447f07db0f03004901a C1_R31_PASS=false` (`.ufo/evidence/round-31/before/c1-at-base.stdout:13`). This is a base-revision result, not a result for a later revision.
- Read-only command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c111dab58b0a8d55e991bbd2efe3aad56717b95a:SCORECARD.md`. The requested sections show the current-axis table (`SCORECARD.md:58-76`) and capability table (`:236-251`). The evidence paths in these rows include commands and asserted outputs.
- Existing entry shape and metadata were read from `corpus/knowledge/regression-tally-completeness.md:1-8` and `corpus/knowledge/survivor-fixture-minimization.md:1-10`. QUALITY requires falsifiable, sourced claims and separates observation from inference (`corpus/QUALITY.md:1-8`); it requires a `source:`, `verified-at:`, and `recheck:` header and a SOURCES row for external sources opened this round (`:27-30`), plus a same-round README coverage row (`:15-22`). The latest round-entry README table format is at `corpus/README.md:449-454`.
- Source pages were fetched with these exact commands; `curl` wrote the response bodies to the named scratch files, and the relevant sections were read there:
  - `timeout 60 curl --fail --location --silent --show-error --max-filesize 1000000 https://docs.python.org/3/library/doctest.html -o /fast/scratch/hyaku/tameshi-r31-seats/ScribeEntry/S095-doctest.html` — Python documentation title and `doctest` module section read at `S095-doctest.html:241-252`.
  - `timeout 60 curl --fail --location --silent --show-error --max-filesize 1000000 https://go.dev/blog/examples -o /fast/scratch/hyaku/tameshi-r31-seats/ScribeEntry/S096-examples.html` — Go Blog title, introduction and “Examples are tests” read at `S096-examples.html:453-475`.
  - `timeout 60 curl --fail --location --silent --show-error --max-filesize 1000000 https://doc.rust-lang.org/rustdoc/write-documentation/documentation-tests.html -o /fast/scratch/hyaku/tameshi-r31-seats/ScribeEntry/S097-rustdoc-tests.html` — Rustdoc “Documentation tests” section read at `S097-rustdoc-tests.html:180-220`.
- `corpus/SOURCES.md` ended with `Next unused id: S095` (`:364`) when read; the search for S095–S097 found that footer line only. The requested source pages were opened, but their S095–S097 registry rows were not present in that read and were not edited here.

## Draft correction for L1

### `corpus/knowledge/executable-self-assessment.md` — full draft

```markdown
source: S095 — Python documentation, “doctest — Test interactive Python examples,” `#module-doctest`; S096 — Go Blog, “Testable Examples in Go,” `#introduction`; S097 — The Rustdoc Book, “Documentation tests,” `#documentation-tests` (opened 2026-10-23; URLs below)
verified-at: 2026-10-23 — the cited source sections were opened with curl; the round-31 rule below is a local inference from those examples and the frozen contract, not a new lane measurement
recheck: `python3 .ufo/evidence/round-31/c1-measure.py --rev REV --work EMPTY_SCRATCH_DIR` (use an empty work directory; this frozen check compares the latest matching rows with command output at REV and checks the base-file prefix; reopen the cited source sections)

# Executable self-assessment rows: claims with checks

A standing capability row says what a tool can do. A standing axis row states a value. Each is a claim about the repository, not a timeless fact. Give the claim a check that runs its associated command against the same revision and compares the command's stated values with the row.

If the command's tool changes while the row stays unchanged, treat the row as stale until the command is re-run at a named revision. Stale means “needs a fresh check”; it does not by itself prove that the row is wrong. A recheck can show that the values still match or that they need correction.

## What the sources say, and what this entry infers

The sources describe executable examples in three language ecosystems:

- **S095, Python `doctest`, module documentation:** “executes those sessions to verify that they work exactly as shown.” Location: `#module-doctest`, <https://docs.python.org/3/library/doctest.html>.
- **S096, Go Blog, introduction:** “verified by running them as tests.” Location: `#introduction`, <https://go.dev/blog/examples>.
- **S097, Rustdoc Book, Documentation tests:** “rustdoc supports executing your documentation examples as tests.” Location: `#documentation-tests`, <https://doc.rust-lang.org/rustdoc/write-documentation/documentation-tests.html>.

Those are the sources' claims about executable examples. **Inference in this entry:** executable examples can reveal a mismatch between documentation and observed behavior; by analogy, a standing self-assessment can be checked by running its command and comparing what it says with what the command reports. The language sources do not establish the SCORECARD rule. The local rule comes from round 31's frozen contract and counter.

## Round 31's concrete check

C1 is a calibration claim over the standing `SCORECARD.md` rows. The frozen set is the ten rows under `| Capability |` and the two rows under `| Axis | Score (0–10) |` (`.ufo/evidence/round-31/contract.json:9-15`; `.ufo/evidence/round-31/c1-measure.py:10-15`). For each statement, the counter takes the last data row in file order for its frozen table type and identifier, then compares its parsed values with the values reported by that statement's frozen command at the requested revision. Fenced code and HTML comments do not count. An unparsable row or unobservable command output is a mismatch, not a match (`c1-measure.py:10-15, 91-123, 206-224`).

The C1 command is:

```sh
python3 .ufo/evidence/round-31/c1-measure.py --rev REV --work EMPTY_SCRATCH_DIR
```

`EMPTY_SCRATCH_DIR` must be absent or empty (`c1-measure.py:169-180`). In this counter, each command is stored in the frozen statement list and is run at REV; the checker compares the output to the corresponding row. This rule is bounded to that frozen command-to-statement mapping (`c1-measure.py:34-65, 136-166`).

The baseline receipt records seven mismatches among the twelve statements and `C1_R31_PASS=false` (`.ufo/evidence/round-31/before/c1-at-base.stdout:13`). It is evidence about the base revision only; it is not a later-revision result.

## Preserve the old statement

Correct a stale row by appending a new restatement; do not edit or delete its old row in place. For a SCORECARD self-assessment, append the re-stated table rows after the base bytes. The frozen C1 predicate requires the base `SCORECARD.md` to remain a byte prefix and evaluates the last matching row (`contract.json:14, 25-26`). Thus the old record stays available while the later row supplies the current claim. This append-only rule is an inference from the local predicate, not a claim made by S095–S097.

## Limits

- A matching tally establishes only that the selected row values equal the selected command's parsed output at that revision, with the required prefix preserved. It is not proof that the capability works in every way its prose describes, or that behavior outside the command's checks is correct.
- The result depends on the command and its inputs. The C1 counter creates revision-specific clones, also creates sibling-tree links under its work directory, and runs the six-leg regression statement in a mirror (`c1-measure.py:136-142, 186-204`). If a row command follows one of those live sibling paths, its result is conditional on the sibling state at run time as well as the lane revision. Record that boundary; do not generalize the observed output to another environment or time.
- The frozen statement set is finite. It checks those rows and commands, not every possible future claim or every behavior behind a capability description (`contract.json:12-18`; `c1-measure.py:34-65`).
```

### `corpus/README.md` — proposed appended section and row

```markdown
## Round 31 — executable self-assessment (calibration)

| Entry / ground | Admission and exact scope | Evidence |
|---|---|---|
| `knowledge/executable-self-assessment.md` / C1 calibration | Source-headed method note: capability and axis rows are claims checked against their frozen command output at the same revision; a new statement is appended rather than edited in place. The executable-example sources motivate this local inference; matching values are not full behavioral proof. | S095, S096, S097; `.ufo/evidence/round-31/contract.json`; `.ufo/evidence/round-31/c1-measure.py` |
```

## Gates, touched surfaces, and boundaries

- **Gates:** No C1 counter, test, selftest, regression, sweep, or build was run. Only the frozen files, the cited base receipt, the frozen SCORECARD revision, existing entry/README shapes, QUALITY, and the three external source sections were read. No C1 after-result is available in this report.
- **Touched surfaces:** The only lane file written is this report. The three fetched HTML documents are in the assigned scratch directory. `corpus/knowledge/executable-self-assessment.md`, `corpus/README.md`, `corpus/SOURCES.md`, `SCORECARD.md`, and the frozen counter were not edited.
- **Out of scope:** No product changes, source-registry rows, commit, push, or deployment. The draft quotes S095–S097 as requested; because those rows were absent at the observed SOURCES.md footer, L1/source integration must add the corresponding registry rows in this round to satisfy QUALITY 10.
- **Setup note:** The assigned scratch directory did not exist on the first attempt to run the read-only `git show`. `mkdir -p ScribeEntry` was run from `/fast/scratch/hyaku/tameshi-r31-seats` to create only the assigned directory; the initial `git show` call did not start. The read-only command above then ran with the assigned scratch directory as its working directory. No other seat directory was opened.
- **Install record:** No tools were installed or updated.

## Artifact paths

- Report: `.ufo/waves/round-31/w1/ScribeEntry.md`
- Scratch source captures: `/fast/scratch/hyaku/tameshi-r31-seats/ScribeEntry/S095-doctest.html`, `S096-examples.html`, `S097-rustdoc-tests.html`
- Frozen inputs and baseline receipt: `.ufo/evidence/round-31/contract.json`, `.ufo/evidence/round-31/c1-measure.py`, `.ufo/evidence/round-31/before/c1-at-base.stdout`

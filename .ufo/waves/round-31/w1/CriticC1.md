# C1 adversarial review

**Overall objection: the frozen counter measures agreement with selected table literals, but those literals are not established as the lane's current self-assessment. Its before value therefore does not establish seven current calibration errors.** This is an advisory critique, not an admission judgment.

Axes: **calibration** is the assigned axis; **freshness** overlaps with re-verification; **operability** concerns machine-readable presentation. Depth, coverage and adjacency are not improvement claims in this review.

All lane-relative citations below refer to freeze `c111dab58b0a8d55e991bbd2efe3aad56717b95a`. I inspected an isolated clone under `/fast/scratch/hyaku/tameshi-r31-seats/CriticC1/clone`. The base and freeze have the same SCORECARD blob; see command evidence below.

## 1. Axis fit

**Verdict: calibration is a legitimate fit in principle, but C1 has not established that its selected values are current assessment claims.** Updating a genuinely false current SCORECARD statement fits calibration directly. Refreshing dated evidence also resembles freshness; merely making old literals machine-readable is not automatically new calibration knowledge or additional quality credit.

Evidence:

- Fleet `/home/vgpnk/Projects/shokunin/AXES.md:14-15` distinguishes re-verification of skill claims from self-assessment quality and explicitly gives “SHONEN.md/SCORECARD entries match observed repo state” as the calibration signal. Lines 20-23 map freshness to quality and calibration to discernment.
- `.ufo/evidence/round-31/contract.json:12-14` calls the selected rows “standing self-assessment,” but the operational predicate is last matching table row plus command-output agreement.
- `.ufo/evidence/round-31/c1-measure.py:111-133` does not inspect the section's date, measured commit, supersession prose, or whether a row is being asserted as current.

Smallest safe correction: make any new table explicitly the authoritative **current** snapshot, identify what it supersedes, and bind its evidence to the actual measured revision. Do not infer a calibration improvement solely from putting historical values into the counter's selected syntax; do not double-credit the same refresh as freshness and calibration.

## 2. Current assessment or historical receipts?

**Verdict: the capability repertoire is standing, but its quoted demonstrations are dated receipts; the selected axis table is explicitly a historical baseline. Re-stating their numbers does not, by itself, demonstrate repair of the effective current assessment.** The present-tense “What it can now do” header is the strongest defense of the proposal, but it does not turn every evidence count or first-working record into a fresh measurement.

Evidence:

- `SCORECARD.md:58-76`: the heading says “fleet round-1 baseline,” the rows name measured commit `284ab0f0b8b989ee73d9c00c0c0df0a59757af8d`, and the commands say to use the **measured commit**. Line 88 explicitly preserves this as the “pre-round” record.
- `SCORECARD.md:238-249`: the capability table separates “What it can now do,” “Evidence pointer,” and “First-working round.” Rows 241-242 cite retained fleet-round-1 demonstrations; rows 243-249 carry round-specific evidence or measured revisions.
- `SCORECARD.md:632-636` is decisive: “Capability counts in the table above are dated literals,” gives four successor counts, and says “The rows stay as written; this line supersedes their counts.” The frozen counter ignores that supersession because it is prose.
- `SCORECARD.md:1475-1478`, already present at base, records the later monitor and command-D observations. The file does not end its current assessment at the old baseline table.
- Retained evidence agrees with the old capability literals: `.ufo/evidence/kaika-round-1/capability-demo/h1a-selftest-host.stdout:81-82` says `MUTATE_SELFTEST: 80/80 pass` and `VERDICT: PASS`; `h1b-regression.stdout:35` says `REGRESSION: PASS (cases=6 passed=6; ledger legs exact: killed-delta<=0 flips<=0)`.
- Historical command D actually prints `recorded_cases=6 depth_score=6` at the old table's own measured revision. Historical command C prints `boxes=4 checked=4 asserted=0 untouched=0 asserted_mark_upper_bound=0`. Exact commands are below.

Strong counterexample: the old depth literal is correct at its explicitly named revision, while the frozen base receipt calls it a mismatch against a later revision. A new table can improve lookup convenience without correcting that historical statement. Four of the five capability mismatches also concern counts expressly superseded in round 17.

Smallest safe correction: preserve the historical receipts and first-working identities, append one unambiguous current snapshot with honest revision/evidence cells, and describe the delta as that presentation change unless an actual current false assessment is identified. Do not count earlier supersessions or already-held counting rules again as newly learned calibration.

## 3. Selection by base value

**Verdict: no evidence of inclusion or exclusion conditional on base value. There is disclosed pre-freeze knowledge of the outcomes and a narrow syntax-defined universe.** Those are different issues; the evidence does not justify alleging outcome-based cherry-picking.

Evidence:

- `.ufo/evidence/round-31/contract.json:38` discloses format reconnaissance and the base counter run before freeze, says all rows of the two table types were included, and states that five of twelve match.
- `c1-measure.py:38-65` includes the ten original capability identities and both axes. The retained receipt `before/c1-at-base.stdout:1-13` contains five `MATCH` and seven `MISMATCH` results; the five matches were not dropped.
- The scope is not every repertoire entry: `SCORECARD.md:1055-1057,1148-1150,1232-1234` contains three later “capabilities addition” tables, which the exact-header selector excludes. That exclusion is structural, not evidence of outcome-based selection. Later assessment prose and differently headed verdict tables are excluded too.

Smallest safe correction: keep the disclosure and describe the population precisely as these frozen header-selected literals, not a census of all effective current assessment statements. Do not expand or replace the frozen population after seeing controls.

## 4. Cheap control meeting the target

**Verdict: copying the observed tuples from the committed base receipt into appended matching tables is the obvious cheap route. It is already disclosed and is not, by itself, a violation of the frozen outcome property. The stronger objection is that the selector also accepts explicitly non-current examples and ignores false historical provenance.**

Evidence:

- `.ufo/evidence/round-31/contract.json:36` expressly anticipates receipt copying without running the commands and distinguishes that route from skipping the claimed outcome property.
- `c1-measure.py:126-133,201-223` checks extracted tuples and the prefix condition, not the meaning of the evidence cells or surrounding prose.
- I ran a bounded **parser-only** counterexample using the unchanged frozen parser. It copies observed tuples from the committed base receipt into an in-memory appended appendix headed `Archived formatter example, NOT current self-assessment`, while retaining the old evidence and measured-commit cells. All twelve selected rows came from that appendix and matched the receipt tuples; the prefix remained intact. No statement command or full counter was run by this probe.

Exact command, from the isolated clone:

```sh
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE PYTHONDONTWRITEBYTECODE=1 python3 authority-probe.py
```

Observed summary:

```text
STATIC_AUTHORITY_PROBE: frozen_statements=12 receipt_backed_tuple_matches=12 parser_mismatches=0 prefix_preserved=True
No commands from STATEMENTS were run; no full counter PASS is claimed.
```

Probe source: `/fast/scratch/hyaku/tameshi-r31-seats/CriticC1/clone/authority-probe.py:6-49`; the disclaimer is at line 33 and selection/comparison at lines 38-45. Its selected axis rows retained the `284ab0f0b8b989ee73d9c00c0c0df0a59757af8d` measured-commit cell while taking the later receipt's values.

[INFERENCE] If the frozen commands continue printing the recorded tuples at a committed appendix-only revision, the full tuple-and-prefix predicate would pass despite the non-current heading. This review does **not** report an observed full-counter pass for that variant. The actual historical command-D output below already shows why retaining the old measured-commit cell with the later tuple would be false provenance if presented as a real measurement.

Late peer evidence, read from the published lane report rather than another seat's scratch: `.ufo/waves/round-31/w1/CtlReceiptCopy.md:77-105` records a full frozen-counter run of receipt-copy **V1**, `aebfdc874ebcf716e10d14ef29013550017e8ae3`. The peer's exact V1 command was:

```sh
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/CtlReceiptCopy/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r31-seats/CtlReceiptCopy/w-receipts3
```

Its reported output was eleven matches, `STATEMENT sources-registry: claimed=0,89 observed=0,92 (exit=0) MISMATCH`, and:

```text
C1_R31: statements=12 mismatches=1 unparsed=0 unobservable=0 append_only=1 rev=aebfdc874ebcf716e10d14ef29013550017e8ae3 C1_R31_PASS=false
```

V1's reported exit was 1. It is an observed failing control, not a full pass. The peer initially overlooked the frozen round-31 `before/c1-at-base.stdout:1`, which already states `observed=0,92`; after I supplied that qualification, the peer withdrew its missing-receipt claim (`CtlReceiptCopy.md:25-28`) and measured V2 below. I did not rerun or edit either control.

**Subsequent observed V2: the receipt-only route does meet the frozen target.** The peer's corrected control is `47ee5b6276da0c4429aee546e063d1b34699cc33`, with the census value copied from that committed before receipt. `CtlReceiptCopy.md:107-126` records twelve matches and exit 0. Its exact command was:

```sh
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r31-seats/CtlReceiptCopy/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r31-seats/CtlReceiptCopy/w-receipts4
```

Observed peer summary:

```text
C1_R31: statements=12 mismatches=0 unparsed=0 unobservable=0 append_only=1 rev=47ee5b6276da0c4429aee546e063d1b34699cc33 C1_R31_PASS=true
```

The peer constructed the appended tables without executing the twelve commands; the frozen counter itself necessarily ran its observations. This is now a reported full-counter pass for the receipt-copy route, distinct from my still-parser-only archived-formatter/provenance variant. It corroborates the frozen contract's stated outcome-only meaning; it does not establish command execution by the row author or resolve whether the old literals were current self-assessment.

Smallest safe correction: retain the frozen counter and its honest result; review the appended content for explicit current authority and truthful measured revisions. Do not invent a new “author must rerun everything” requirement to defeat the permitted receipt-copy route. Copying accurate numbers is a route choice; asserting they were measured at an incompatible old revision is calibration harm, not an acceptable trade for freshness or a green tuple count.

## 5. Too thin for a round?

**Verdict: one small claim is not inherently too thin, but this before-to-after is too weak to establish the advertised calibration gain without answering the historical-authority objection.** The strongest objection is not “only twelve rows.” It is that the claimed seven errors are constructed by treating historical, sometimes expressly superseded, evidence as current assertions, while later current observations already exist in the same base document.

Evidence:

- Fleet `AXES.md:25-38` permits one independently verifiable axis improvement; it supplies no minimum row count or implementation size.
- `SCORECARD.md:632-636` already holds the dated-evidence/supersession distinction, and `:1475-1478` already records the later observations. Reprinting those in a preferred header does not establish that the lane previously misunderstood its state.
- The authority/provenance counterexample above improves the measured tuples without establishing better self-assessment; if copied metadata is asserted as real measurement, it can make self-assessment worse instead.

Smallest pre-data answer: state exactly which effective **current** assertion is wrong and how the appended authoritative snapshot corrects it, without claiming that the old dated receipt was false. Give the snapshot truthful evidence/revision cells and keep historical rows intact. If no such current misassessment can be identified, report the frozen syntactic target result separately and do not present it as evidence of substantive calibration learning. No change to the frozen counter, predicate, population or target is proposed. Whether the bounded presentation improvement supports this round's claim is left to the canonical judge; this seat does not admit or re-score it.

## Command evidence and scope

All commands run by this seat used cwd `/fast/scratch/hyaku/tameshi-r31-seats/CriticC1/clone` except initial clone creation, whose cwd was its parent seat directory. Git overrides were unset. No production file was edited; this report is the only file write outside the seat directory. No orchestration or judgment runtime, gate, sweep, regression or full C1 counter was invoked by this seat. The peer's separately attributed command above was not run here. No tool was installed or upgraded. No process started by this seat remains running.

Frozen identity command:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git rev-parse HEAD 36c1d3933f680125aeefc447f07db0f03004901a:SCORECARD.md c111dab58b0a8d55e991bbd2efe3aad56717b95a:SCORECARD.md
sha256sum .ufo/evidence/round-31/c1-measure.py .ufo/evidence/round-31/contract.json
```

Observed output:

```text
c111dab58b0a8d55e991bbd2efe3aad56717b95a
8c3241309d42365359f69cfde2f6805b10d3b1d1
8c3241309d42365359f69cfde2f6805b10d3b1d1
657fcc1291d781577c20f4f0c4dc55feb84aadb38bce846bfdb296c7ef1e7584  .ufo/evidence/round-31/c1-measure.py
8e7cebb326f60952311f253da173c127dea206f0c4759850215c40373cf91c79  .ufo/evidence/round-31/contract.json
```

Historical command D, including a pipe-failure guard:

```sh
set -o pipefail && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git show 284ab0f0b8b989ee73d9c00c0c0df0a59757af8d:tools/mutate-and-run.sh | python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))'
```

Observed output:

```text
recorded_cases=6 depth_score=6
```

Historical command C:

```sh
set -o pipefail && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git show 284ab0f0b8b989ee73d9c00c0c0df0a59757af8d:SHONEN.md | python3 -c 'import re,sys; m=re.findall(r"^- \[([x~ ])\] ",sys.stdin.read(),re.M); print("boxes="+str(len(m))+" checked="+str(m.count("x"))+" asserted="+str(m.count("~"))+" untouched="+str(m.count(" "))+" asserted_mark_upper_bound="+str(min(8,2*m.count("~"))))'
```

Observed output:

```text
boxes=4 checked=4 asserted=0 untouched=0 asserted_mark_upper_bound=0
```

One initial historical lookup mistyped that hash by omitting `c0`, producing `fatal: invalid object name` and a misleading zero from the unguarded pipeline. A read-only `cat-file -t` of that same mistyped name also failed. Those are operator transcription errors, not evidence that the cited object is missing; the corrected commands above succeeded. The zero was not used as evidence.

The baseline C1 failure was read from the frozen committed receipt, not rerun. Its retained summary is:

```text
C1_R31: statements=12 mismatches=7 unparsed=0 unobservable=0 append_only=1 rev=36c1d3933f680125aeefc447f07db0f03004901a C1_R31_PASS=false
```

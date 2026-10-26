# T47RevProvince — per-entry PROVINCE.md + QUALITY.md gate (round 47, w1)

Seat: `T47RevProvince`. Item: gate the three C3 package entries
(`flaky-aware-verdict-evidence.md`, `r8-flakiness-not-static.md`,
`r8-flaky-cost-baseline.md`) on PROVINCE.md and corpus/QUALITY.md, and reject at
least one of the other entries of the same theme.

Read-only seat. No lane write except this file. No tool installed (checked:
`pdftotext` already present, `/usr/bin/pdftotext`); nothing upgraded, so the
2026-10-19 install directive has no entry to record here. Scratch:
`/tmp/tameshi-r47-T47RevProvince/`.

Revision context: freeze `9acfbe21435e1976636a276448dee1d5e7155915`, base
`0b5b7cd2b2c15d23086e811a0f0348d84261277b`. I ran no counter as a verdict; the
only execution that matters here is the *predicate* of
`.ufo/evidence/round-47/coverage/measure.py::entry_ok`, imported as a library
into scratch and applied to the package copies (no verdict, no `--rev` run).

## 0. Verdicts

| Entry | Verdict | Deciding PROVINCE line | Deciding QUALITY criterion |
|---|---|---|---|
| `flaky-aware-verdict-evidence.md` | **ADMIT, conditionally** (F3) | `PROVINCE.md:3-5` (domain), `:40-42` (F3 frontier → Core only via admitted source-headed entry) | 10 (provenance trio + mined row + tier rule), 2 (measured anchor), 3 (observation/inference separate) |
| `r8-flakiness-not-static.md` | **ADMIT, conditionally** (F7 method half + F3) | `PROVINCE.md:3-5`, `:40-42` | 2, 3, 10 |
| `r8-flaky-cost-baseline.md` | **ADMIT narrowly** (F7 cost side only; transfer refused at its own boundary) | `PROVINCE.md:3-5`, `:40-42`; not `:14-18` because no policy is adopted | 1 (falsifiable/opinion), 2, 3, 10 |
| `r14-quarantine-threshold-is-a-policy.md` | **REFUSE** (primary reject) | `PROVINCE.md:14-16` (Refuses product domains; two-lane clause) | 10 (tier-C never sole support), 9 (evidence copied into the repo), 34 (citation into a file the lane does not own), 2 |
| `r13-flaky-false-red-rate.md` | **REFUSE** (duplicate) | `PROVINCE.md:40-42` (F3/F7 already held) | 15 (retained expectation must be effective or named-superseded), 7 |
| `r12-flaky-mitigation-and-quarantine.md` | **REFUSE** (duplicate) | same | 15 |
| `r8-gtest-order-and-seed.md` | **REFUSE** (already landed, stale copy) | `PROVINCE.md:40-42` | 15 |
| `r8-predictive-test-selection-cost.md` | **REFUSE** (out of province, unopened row) | `PROVINCE.md:14-18` | 10, 2 |

None of the three admits is unconditional: §3–§5 below list defects that make a
byte-copy or a relabelled copy an honest *refusal*, not an admission.

## 1. The province question, decided

> Is test-flakiness prediction and the cost of CI flakiness fixture craft, or
> generic software-testing material the lane Refuses?

**Decided: neither wholesale.** The line runs through *what the claim does to a
lane verdict*, not through the source's topic.

- `PROVINCE.md:3-5` defines the domain as "verification-fixture craft — the
  reusable method of honest checks: hermetic suites, mutation testing,
  fail-closed arms, verdict-line discipline, no-permissiveness audits,
  before/after proof". A claim is in province when it constrains **how the lane
  earns or reads its own verdict**; it is out when it prescribes **a product or
  team process** no lane instrument can falsify.
- Applied:
  - **In province.** (a) A rerun budget and the choice between repeats of one
    order and several orders (F3's "determinism precondition, flaky-aware
    verdicts", `corpus/README.md:80`, `:125-140`) — it says what a green/red
    observation is worth. (b) The published measurement-protocol objection
    (static properties of test code are insufficient to decide flakiness;
    benchmark shortcuts inflate F1) — it is a claim about *instrument validity*,
    the craft itself. (c) The cost of a red versus a rerun, **only** as the
    bounded price F7 (`corpus/README.md:84`) trades against, with transfer
    refused in the entry.
  - **Refused.** (a) A quarantine threshold as the lane's policy: the number is
    two tier-C practitioner pages' band, and a policy is a process decision, not
    a method (`PROVINCE.md:14-18`). (b) Change-level test selection at vendor
    scale: a CI-infrastructure product result; F7's next move is "pin-level
    cadence only → per-leg reuse decisions classified"
    (`corpus/README.md:84`), i.e. which of the lane's own legs to re-sweep, not
    which tests to run per change. (c) Framework usage guidance is *not*
    automatically refused — round 45 admitted GoogleTest `advanced.md` (S256)
    because it states the run-identity discipline the lane's instrument needed;
    that is craft. Re-adopting the same entry is a duplicate (`§6`), not a
    province question.
- The two-lane clause (`PROVINCE.md:15-16`) bites on the *general-pattern* form:
  an entry may carry a source's measurement as a lane input with a named
  boundary, but may not turn one project's number into the lane's rule. This is
  exactly the difference between `r8-flaky-cost-baseline.md` (reports 2.5 % /
  $5.67, refuses transfer in its "What is still unknown" block) and
  `r14-quarantine-threshold-is-a-policy.md` (asserts "A test is quarantined when
  its flip rate ... exceeds 0.3" as the lane's rule).

## 2. Quote verification against the committed snapshots

Method (reproducible): fold each quoted span the way the counter folds
(`unicodedata.NFKC` + whitespace collapse, `measure.py:58-78`), then substring
against the folded text of the committed snapshots
(`.ufo/evidence/round-47/coverage/sources/arxiv-2302.09330-abs.html`,
`arxiv-2607.09345-abs.html`, `s2-icst24-cost-of-flaky.json`,
`lam-2020-reruns.txt`) and the held PIT FAQ snapshot
(`.ufo/evidence/round-42/sources/pit-faq.html`). Script:
`/tmp/tameshi-r47-T47RevProvince/` session output; token counts are the
counter's `fold`+split, i.e. the quantity QUALITY 87 makes mandatory.

| Entry | Quote (first words) | Tokens | Located in | Status |
|---|---|---|---|---|
| flaky-aware | "one can use ≤ 5 reruns ... check correctly ≥ 82% of the time" | 23 | — | **ABSENT from the frozen text snapshot** (see F3) |
| flaky-aware | "run tests in a test suite instead of in isolation, ... more times each" | 28 | — | **ABSENT from the frozen text snapshot**; also >25 tokens |
| flaky-aware | "without such requirements on the underlying programming language..." | 14 | arxiv-2302 (`S261`) | ok |
| flaky-aware | "the tests' outcomes and durations..." | 14 | arxiv-2302 (`S261`) | ok |
| flaky-aware | "does not require additional reruns..." | 14 | arxiv-2302 (`S261`) | ok |
| flaky-aware | "Both these measurements can be affected by external factors..." | 33 | pit-faq (`S156`) | located, **>25 tokens**, and cited as `S160` (wrong document, F5) |
| flaky-aware | "one control per sweep → N ≥ 3 byte-identical controls..." | 14 | `corpus/README.md:80` | lane quote, ok |
| flakiness-not-static | "How Far Are We from Detecting Flaky Tests?..." | 14 | arxiv-2607 (`S263`) | ok, but already in the package copy |
| flakiness-not-static | "15 pages, 7 figures, under review" | 6 | arxiv-2607 (`S263`) | ok |
| flakiness-not-static | "argue that the field is studying the wrong problem: ..." | 31 | arxiv-2607 (`S263`) | located, **>25 tokens** |
| flakiness-not-static | "found that widely used benchmarks contain shortcuts..." | 12 | arxiv-2607 (`S263`) | ok |
| flakiness-not-static | "evaluation protocols overstate generalizability" | 4 | arxiv-2607 (`S263`) | ok |
| cost-baseline | "Cost of Flaky Tests in Continuous Integration..." | 11 | s2 json (`S264`) | ok |
| cost-baseline | "the time spent ... at least 2.5% of the productive developer time" | 20 | s2 json (`S264`) | ok |
| cost-baseline | "Contrary to most other studies ... costs 0.02 cents," | 24 | s2 json (`S264`) | ok |
| cost-baseline | "not rerunning ... manual investigation costing $5.67" | 15 | s2 json (`S264`) | ok |

Every quoted sentence that exists in a committed snapshot was found there
byte-for-byte after the counter's fold, **except the two S158 guideline
sentences** (F3). One further sentence is not a source quote at all
("re-sweep versus a human investigating a red build", 8 tokens) — it is the
entry's own coinage in double quotes and is located nowhere (F9).

## 3. `flaky-aware-verdict-evidence.md` — ADMIT (F3), with mandatory repairs

**Decides it:** `PROVINCE.md:3-5` + `:40-42` (F3 is a lane frontier row; its
next move is a repeated-control capability, `corpus/README.md:80`, `:125-140`)
and QUALITY 10 (provenance trio + mined `SOURCES.md` row + tier rule), QUALITY
2 (every claim carries a measured anchor), QUALITY 3 (observation, inference,
unknown separate). The entry is the only admitted candidate whose topic *is* the
verdict discipline itself: it prices a rerun budget, names a source of flakiness
evidence the lane's records can supply, and states that a verdict class
(timeout) can be run-dependent. Its prediction numbers (F1 95.5 %, the three
features) are carried as the source's measurement, not adopted as lane claims.

**Why admitted rather than refused:** the entry's operands are `(line, exit,
rerun)` verdict rules, not a product process. Its explicit refusal — "None of
this upgrades a single green control into a determinism claim"
(`corpus/QUALITY.md:34-37`, criterion 11, correctly cited) — keeps it inside the
craft.

**Admission conditions (all mechanical; any one unmet = honest miss):**

- **F1 — ids by document, never by arithmetic.** The package header's `S155`,
  `S158`, `S160` are *package* ids. In the lane (`corpus/SOURCES.md`): `S155` is
  PIT *basic concepts* (`:125`), `S156` is PIT *FAQ* (`:126`), `S158` is
  `DetectionStatus.java` (`:128`), `S160` is the Stryker *equivalent mutants*
  page (`:130`). Per `.ufo/evidence/round-46/assimilation/adoption-map.json`
  and the contract, the re-grounded entry must cite **S261** (arXiv 2302.09330),
  **S262** (Lam camera-ready), and **S156** for the pitest FAQ quote — the third
  is the trap: the quote is located only in `S156`'s snapshot, and a citation to
  `S160` would point at a different document with a different digest.
- **F2 — all cited ids must be on line 1.** `measure.py:124-126` reads
  `CITE_RE.findall(lines[0])`. The package copy has three `source:` lines
  (lines 2–4) with `verified-at:` on line 5 and a leading blank line 1 → the
  counter returns `no provenance trio` before any quote is examined (verified by
  importing `entry_ok`; same for all three copies). Collapse the sources to line
  1, `verified-at: 2026-10-25` on line 2, `recheck:` on line 3.
- **F3 — the two S158 guideline sentences are not verifiable from the frozen
  snapshot.** `lam-2020-reruns.txt` is a two-column PDF extraction interleaved
  line-by-line: `:113` reads
  `one can use ≤ 5 reruns (50% less than Google's default ten           conducted
  surveys of developers after the tests were fixed and`, with the sentence
  continuing only at the next line's left column. Folded, the sentence is not
  contiguous, so the 23-token and 28-token quotes are **absent** from the
  committed text. The PDF itself does carry them: `pdftotext -f 2 -l 2
  lam-2020-reruns.pdf -` places `... ≤ 5 reruns ... ≥ 82% of the time` on page 2
  (verified: page 2 hit count 1, pages 1 and 3 = 0), which also confirms the
  entry's `p. 2` locator. Since the snapshot set is frozen at the freeze commit,
  the entry must either anchor the claim to the PDF page (§Guidelines, p. 2) and
  say the text snapshot's extraction is interleaved, or drop the two claims.
  Presenting them as located evidence in the txt is a QUALITY 2 miss.
- **F4 — the `recheck:` command as written returns 0.** It greps the PDF bytes:
  `grep -c '5 reruns' lam-2020-reruns.pdf` → `0` on the committed PDF (compressed
  streams); the same grep on the text snapshot → `3`. A recheck that cannot
  return its expected value is a broken control; fix to a command that reads the
  text layer (`pdftotext` the committed PDF, or grep the committed txt for
  `≤ 5 reruns`).
- **F5 — two lane-state claims are false as written.**
  1. "(the lane's own convention, per its held S001)" scoring a timeout as a
     **kill** is inverted. The lane's recorded rule: "**Inconclusive** — timeout,
     crash before summary, or missing count is not a kill and is excluded"
     (`corpus/knowledge/mutation-score-semantics.md:16`), and
     "Rejected for Tameshi's recorded score: ... a timeout ... is Inconclusive,
     not a kill" (`:71`); "The lane's own rule ... makes a timeout or a crash
     before the summary Inconclusive, not a kill"
     (`corpus/knowledge/pit-outcome-vocabulary.md:49-52`). `S001` is Stryker's
     docs — Stryker counts a timeout as *detected*, which the lane's entry
     explicitly **rejects** for its own score (`:71`). This is inference about
     the lane presented as observation, with the anchor saying the opposite.
  2. "(the lane's own ledger keeps outcomes and exit codes per case)" is not
     true of the ledger. `corpus/knowledge/fleet-kill-rate-ledger.md` is one row
     per gate with the columns *suite size · kill-rate (composition) · survivor
     classes · hardened · last-sweep pin* (`:7-11`, `:30-40`); no per-case
     outcome or exit-code column exists in it. Per-case outcomes live in counter
     receipts, so the claim needs a receipt anchor or removal.
- **F6 — one sentence drifts from its source.** "S158 gives a defensible
  number: five reruns classify ≥ 82% of failures correctly" vs the source
  (p. 2): "one can use **≤ 5** reruns ... and still **check correctly ≥ 82% of
  the time**". Ceiling → exact five; correctness of the check → share of
  failures. Restate the source sentence and its measured token count (QUALITY 87).
- **F7 — no counter-locatable fresh quote.** Even with F1/F2 repaired, the
  predicate returns `no located quote` for this copy: its only single-line 6–25
  token quote is `"Is it random?"` (3 tokens), and every substantive quote wraps
  across lines (`QUOTE_RE` forbids `\n`). The entry must carry at least one
  single-line 6–25-token quote that is located in a cited row's snapshot **and**
  absent from the package copy. Verified candidates (all fresh): `S261`
  "Non-deterministically behaving test cases cause developers to lose trust in
  their regression test suites and to eventually ignore failures." (19 t; split
  it is fine — place it on one line); `S261` "The best model was able to achieve
  an F1-score of 95.5% using only 3 features:" (15 t). Do **not** take the fresh
  quote from `S262`: its frozen text extraction is interleaved, so plausible
  "sentences" in it are artifacts ("Several of involve multiple threads,
  asynchronous wait for tests that these studies have focused on OD tests.",
  17 t) — quoting one would ship an extraction bug as evidence. `S156` cannot
  supply a fresh quote either: its substantive run-dependence sentence is the
  33-token quote already in the package copy, and any 6–25-token substring of it
  necessarily occurs in the package copy, which fails the freshness rule.

## 4. `r8-flakiness-not-static.md` — ADMIT (F7 method half + F3), with repairs

**Decides it:** `PROVINCE.md:3-5` + `:40-42`; QUALITY 2, 3, 10. The paper's
objection — "Flakiness is not a static property of test code, which often lacks
the information needed to decide whether a test is flaky", plus "widely used
benchmarks contain shortcuts that inflate reported F1 scores" and "evaluation
protocols overstate generalizability" (all located in `S263`, exact quotations)
— is a statement about *instrument validity*, which is the lane's own subject:
a static property read as a behavioural verdict. That is in province and it is
the counter-evidence an F7 prediction row must be read against. The entry keeps
its transfer hypothetical ("the lane's gates are not flaky-test detectors, and
the paper does not study environment-differential instruments"), which is the
correct boundary.

**Repairs:**

- **F8 — the author list is false against the committed snapshot.** The package
  header says "(Baltes, McKim, Zaidman, Wagner)". The committed
  `arxiv-2607.09345-abs.html` carries
  `citation_author`: **Ömer Oktay Gültekin, Alexander Berndt, Jonathan Bell,
  Thomas Bach, Sebastian Baltes**; `McKim`, `Zaidman` and `Wagner` occur zero
  times in the snapshot (`grep -o` on the tag set; the page's author block reads
  the same five). The package row (`/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md:60`)
  repeats the wrong list, so this is precisely the metadata a re-grounding must
  not copy. Fix to the snapshot's five authors, and note the package row's
  divergence in the round report.
- **F9 — two dangling citations and one unanchored history claim.**
  - `(S208)` — `S208` is not a lane row (`grep -c '| S208 ' corpus/SOURCES.md` →
    0). In the package registry it is a *path* to
    `lanes/tameshi/round8/evidence/env-diff-w4-12-receipt.json`
    (`SOURCES.append.md:62`), and this repo has no `lanes/` directory
    (`ls -d lanes` → no such file). An unresolvable measured anchor.
  - `S152` — the package registry has no `S152` row at all (`grep -c 'S152'
    SOURCES.append.md` → 0); in the lane, `S152` is "Understanding snapshot
    testing in practice" (Cruz, UFMG 2024, `corpus/SOURCES.md:122`), used by two
    snapshot entries. It does not carry "a gate pinned at a revision was read as
    a verdict". Re-point by document or drop the sentence.
  - "Round 7 could only source F7's cost side" — a lane-history claim with no
    receipt; anchor it or mark it unknown.
- **F10 — freshness.** With the header repaired the predicate returns `no quote
  fresh against the package copy`: both located single-line quotes (title, 14 t;
  "15 pages, 7 figures, under review", 6 t) are already in the package copy.
  Verified fresh candidates in `S263`: "Flaky tests pass and fail on the same
  code version, weakening the signal of test results and disrupting continuous
  integration (CI) pipelines." (22 t) and "Code-based flakiness detectors report
  strong benchmark results, yet their use in practice remains limited." (14 t).
- **F11 — the 31-token quote exceeds the bar.** "argue that the field is
  studying the wrong problem: ..." measures 31 whitespace tokens under the
  counter's fold; the admission quote must be 6..25 (QUALITY 87; the C1 bar the
  counter applies). Quote the inner sentence instead ("Flakiness is not a static
  property of test code, ...", which is itself 24 tokens — measure it before
  writing the label).

## 5. `r8-flaky-cost-baseline.md` — ADMIT narrowly (F7 cost side), with repairs

**Decides it:** `PROVINCE.md:3-5` + `:40-42` (F7 is open, `corpus/README.md:84`)
and QUALITY 1, 2, 3, 10. The cost of CI flakiness is **project economics, not
fixture craft**; it enters the lane only as the bounded cost side of F7's own
decision (which legs to re-sweep, and what a false red costs against a rerun),
and this copy keeps that boundary in its own words: "One commercial project.
Whether the 2.5 % and the $5.67 transfer to a thirty-developer fleet of small
shell gates is not established by this source." It also refuses the policy
inference that `r14` makes ("it is a cost *of the problem*, not of a
mitigation"). That refusal is what keeps it on the in-province side of
`PROVINCE.md:14-18`.

The lane has already stated the exact standard this entry now meets:
`corpus/knowledge/r9-false-red-rate.md:39` — "The package copy of this entry
priced a rerun, priced a manual investigation and attributed a detection-floor
percentage to `S156`. None of those figures is restated: the lane holds no row
carrying those prices, and this snapshot states no such numbers." Round 46
declined the prices because no row carried them; `S264` (S2 record of the ICST
paper) is the row that carries them. That precedent is also why the
coverage-map/used-by bookkeeping must be exact: r9:39 records that the package
text had already mis-pointed a figure at `S156` — the same staged-vs-lane id
collision that F1 and F5 make concrete in this round.

**Repairs:**

- **F12 — venue conflict against the committed record.** The header says "IEEE
  ICST 2024". The committed `s2-icst24-cost-of-flaky.json` `venue` field reads
  **"International Conference on Information Control Systems & Technologies"**
  (`year` 2024, `paperId` `15c73cff…`), while the DOI
  `10.1109/ICST60714.2024.00037` and the DBLP key `conf/icst/LeinenEPSSJ24` say
  ICST. The entry must state the record's field verbatim and name the conflict,
  or add a publisher-side snapshot; it must not assert "IEEE ICST 2024" from the
  DOI alone.
- **F13 — the row URL must use the `%2C` form or the row will never be counted.**
  `URL_RE` (`measure.py:54`) stops at `,`, so a literal-comma fields query (the
  package header's form) is truncated to `...?fields=title`, whose `doc_key` is
  **not** in `DOCS`. Demonstrated: the `%2C` form lowercases to exactly the
  `DOCS` entry; the literal-comma form does not. The `SOURCES.md` row must carry
  `?fields=title%2Cabstract%2Cyear%2Cvenue%2Cauthors%2CexternalIds`.
- **F14 — two unverifiable provenance claims.** "the record carries the
  publisher's abstract verbatim" cannot be checked inside the lane (no publisher
  page snapshot exists), and "the open full text at mediaTUM timed out twice this
  round" has no receipt. Both are access-path observations; either commit the
  publisher page as a snapshot or mark them as unverified in this round.
- **F15 — minor metadata drift.** The record spells the last author `Elmar
  Jurgens`; the entry writes `Jürgens`. The `openAccessPdf.status` is `GREEN`
  with `license: other-oa` (matches "green open-access pointer").
- **F16 — freshness + self-quoted coinage.** With the header repaired the
  predicate returns `no quote fresh against the package copy` (the title quote
  is the only located 6–25-token one). Fresh candidates: "They spend a lot of
  effort trying to detect, repair, and mitigate the negative effects of flaky
  tests." (18 t); "However, it is yet unclear where and to what extent the costs
  of flaky tests manifest in industrial Continuous Integration (CI) development
  processes." (23 t). The 8-token `"re-sweep versus a human investigating a red
  build"` is the entry's own coinage in quotation marks and is located nowhere —
  de-quote it, or a reader (and the counter) will treat it as a source quote.

## 6. Rejections

### 6.1 PRIMARY — `r14-quarantine-threshold-is-a-policy.md` (REFUSE)

Cited from `/home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge/corpus/knowledge/r14-quarantine-threshold-is-a-policy.md`
(sha256 `9549c148da03cae0…`).

**PROVINCE line:** `PROVINCE.md:14-18` — "**Refuses:** product domains — every
lane's gate remains its own; tameshi owns only the reusable craft (a pattern is
admitted from evidence in TWO independent lanes before it is claimed general)."
The entry's operative content is a *process policy for the lane*: "A test is
quarantined when its flip rate over the lane's own repeated control exceeds
0.3", plus a "review period is a week" and a "may not cover more than a tenth of
the suite" ceiling. Quarantine is a workflow decision (take a test off the
critical path, file a bug); the lane runs no CI, has no build cop and files no
bugs, so no lane instrument can falsify the threshold. `PROVINCE.md:20` says
"Out of province → report, never absorb" — this is absorption.

**QUALITY criteria that decide it:**
- **10** — "a tier-C row is never sole support": the two numbers the policy
  asserts (0.3, 10 %) come from `S243` (qam-hub, tier C) and `S244` (FlakyGuard,
  tier C) — `SOURCES.append.md:97-98` — and the entry admits it: "The 0.3 and
  the 10 % come from two practitioners' pages (tier C), not from a published
  finding".
- **9** — "evidence a claim rests on is copied into the repo before the commit
  that cites it": `S242` is a receipt at
  `lanes/tameshi/round14/evidence/f2-quarantine-threshold.txt`; that path does
  not exist in this repo (`ls -d lanes` → no such file). It exists only in the
  read-only package tree
  (`/home/vgpnk/Projects/shokuknow/lanes/tameshi/round14/evidence/f2-quarantine-threshold.txt`).
- **34** — "A citation into a file that moves, or that the lane does not own, is
  anchored by function or symbol name and the cited rev": the citation is a bare
  path into a tree the lane may not write.
- **2** — the header's `S241` anchor is the month archive
  `https://testing.googleblog.com/2017/04/`, not the post; the registry row names
  the per-post feed record.
- **Two-lane clause**, `PROVINCE.md:15-16`: the policy is claimed for the lane
  from one lane's (missing) sweep plus two vendor blogs; there is no second
  independent lane.

**Flip condition (all four, else refuse):** (1) a receipt committed *inside* the
lane that measures a flip-rate threshold on the lane's own repeated-control
instrument, with the command and the counts; (2) the same threshold shape
independently measured in a second lane (PROVINCE two-lane clause); (3) a
`SOURCES.md` row opened in the round that writes it, `mined`, with a snapshot
under the round's evidence dir; (4) the entry restated as a *reported* practice
("two teams use 2–5 %") rather than "the lane's threshold".

### 6.2 `r13-flaky-false-red-rate.md` — REFUSE (duplicate)

Its claimed content is the same feed document (`S235` =
`6277555988217606236`) already held as lane `S260` (`corpus/SOURCES.md:471`,
round 46), and almost every claim it carries is already held:
- "about 84 % of the transitions we observe from pass to fail involve a flaky
  test" — `corpus/knowledge/r9-false-red-rate.md:16`;
- "causing it to report a failure only if it fails 3 times in a row", the
  quarantine sentence and the "could easily mask a real race condition" sentence
  — `r9-false-red-rate.md:20,22`;
- "the ability to re-run only failing tests ..." —
  `corpus/knowledge/repeated-control-precondition.md:21`;
- "15 tests will likely fail" — `r9-false-red-rate.md:18` (inside the post's
  1.5 %-of-results arithmetic).

It has exactly one sentence of new content — the "requiring expensive
investigation by a build cop or developer" clause — and that clause belongs as an
appended correction to `r9` (QUALITY 35), not as a second entry on the same
document. The lane's own dedupe rule names this exact case: staged `S225`, `S229`
and `S235` "carry the same feed document and are not adopted separately"
(`.ufo/evidence/round-46/assimilation/adoption-map.json`, `note`).

**QUALITY 15** (a retained expectation must be effective or superseded by named,
checked replacement evidence) and **7** (a knowledge file lands with its
coverage-map row; a second map row for a held document has no ground to map).
**Flip:** the build-cop clause promoted to a *correction block inside*
`r9-false-red-rate.md` with its measured token count — not a new entry, and not a
new row (the document is already `S260`).

### 6.3 `r12-flaky-mitigation-and-quarantine.md` — REFUSE (duplicate)

Same feed (`S229`), same sentences, same held provenance (`S260`): the 16 %
share at `r9-false-red-rate.md:14`, the mitigation quotes at
`repeated-control-precondition.md:21` and `r9-false-red-rate.md:18`, the
quarantine and masking sentences at `r9:22`, and its "direction of travel is
detection without a re-run" inference at `r9:24`. **QUALITY 15** + the same
round-46 dedupe note.

Its one delta is the inference that 1.5 % is a share of *results* and 16 % a
share of *tests*, i.e. different denominators. `r9-false-red-rate.md:37`
explicitly declines that step: "The snapshot states the 84% transition rate and
the 1.5% result rate in different paragraphs and states no relationship between
them; none is derived here." So the delta is an unmeasured inference laid over
quotes the lane already holds — an errata-sized claim, not an entry.
**Flip:** the denominator distinction stated as a *measured* difference from the
snapshot (a located sentence that fixes the two names), appended as a correction
inside `r9-false-red-rate.md`.

### 6.4 `r8-gtest-order-and-seed.md` — REFUSE (already landed)

The entry exists in the lane as `corpus/knowledge/r8-gtest-order-and-seed.md`
(sha256 `5a648d7214260916…`, source `S256`, round 45), grounded in the committed
round-45 snapshot. The package copy is the pre-adoption draft (sha256
`172254096cd489ef…`) whose package ids `S202`/`S203` dedupe to lane `S256`/`S257`
(`adoption-map.json`). Landing it again would either duplicate the file name
(QUALITY 15) or, worse, replace a re-grounded entry with an ungergrounded copy.
**Flip:** a claim against `S256`'s snapshot that the held entry does not carry.

### 6.5 `r8-predictive-test-selection-cost.md` — REFUSE (out of province, unopened row)

Content: Facebook's change-level test selection, "reduces the total
infrastructure cost of testing code changes by a factor of two, while
guaranteeing that over 95 % of individual test failures ... are still reported".
That is a CI-infrastructure product result at vendor scale. F7's next move is
per-leg reuse of *the lane's own gates* (`corpus/README.md:84`), not per-change
test selection, and no lane instrument can falsify a factor of two on Facebook's
infrastructure. **PROVINCE.md:14-18** (product domain) and **QUALITY 10** (its
document `S205` / arXiv 1810.05286 is not a lane row: `grep -c '1810.05286'
corpus/SOURCES.md` → 0) and **QUALITY 2** (the quote's magnitude cannot be
checked against any committed snapshot). **Flip:** open `S205` as a mined row
with a round snapshot *and* name the lane move that consumes change-level
selection; absent that, it stays a report line, not an entry.

## 7. Defect register

| id | severity | entry | defect | evidence |
|---|---|---|---|---|
| F8 | **high** | flakiness-not-static | author list false vs committed snapshot (Gültekin, Berndt, Bell, Bach, Baltes) | `arxiv-2607.09345-abs.html` `citation_author` tags; package `SOURCES.append.md:60` repeats it |
| F5.1 | **high** | flaky-aware | "the lane scores a timeout as a kill (per its held S001)" inverts the lane's rule | `mutation-score-semantics.md:16,71`; `pit-outcome-vocabulary.md:49-52` |
| F3 | **high** | flaky-aware | two S158 quotes are not contiguous in the frozen text snapshot (two-column interleave) | `lam-2020-reruns.txt:113`; `pdftotext` page 2 = 1 hit |
| F7/F10/F16 | **high** (C3-blocking) | all three | no counter-locatable *fresh* single-line 6–25-token quote in any copy | `entry_ok` returns `no located quote` (flaky-aware) and `no quote fresh ...` (other two) |
| F2 | **high** (C3-blocking) | all three | leading blank line + multi-line `source:` block; `verified-at` not on line 2 | `entry_ok` → `no provenance trio` on all three copies |
| F1 | **high** | flaky-aware | ids `S155`/`S158`/`S160` name lane documents of different identities | `corpus/SOURCES.md:125,126,128,130` |
| F12 | medium | cost-baseline | "IEEE ICST 2024" vs the record's `venue` field | `s2-icst24-cost-of-flaky.json` |
| F13 | medium (C3-blocking) | cost-baseline row | literal-comma fields query truncates at `URL_RE`; row never counted | `measure.py:54`, `DOCS` tuple |
| F4 | medium | flaky-aware | `recheck` greps the PDF → 0 hits, expects 1 | `grep -c '5 reruns' lam-2020-reruns.pdf` = 0; txt = 3 |
| F6 | medium | flaky-aware | "five reruns classify ≥ 82 % of failures" drifts | source p. 2: "≤ 5 reruns ... check correctly ≥ 82 % of the time" |
| F5.2 | medium | flaky-aware | ledger "keeps outcomes and exit codes per case" — no such column | `fleet-kill-rate-ledger.md:7-11,30-40` |
| F9 | medium | flakiness-not-static | `S208` and `S152` dangling/wrong; round-7 claim unanchored | `grep -c '\| S208 '` = 0; `SOURCES.append.md:62`; `corpus/SOURCES.md:122` |
| F11 | medium | flakiness-not-static | 31-token quote exceeds the 6..25 bar | measured |
| F14 | low | cost-baseline | "abstract verbatim" and mediaTUM timeout unverifiable | no snapshot / no receipt |
| F15 | low | cost-baseline | `Jürgens` vs record's `Jurgens` | `authors` array |
| F9' | low | cost-baseline | self-quoted coinage located nowhere | measured 8 t, absent from `S264` |

## 8. C3 mechanical preconditions (counter-exact, for the seat that lands them)

From `.ufo/evidence/round-47/coverage/measure.py` (read, not run as a verdict):

1. Entry line 1 starts `source:` and carries every adopted id (`CITE_RE` on
   `lines[0]` only); line 2 is `verified-at: >= 2026-10-25`; line 3 starts
   `recheck:`; no leading blank line.
2. Each cited id is a `SOURCES.md` row with exactly 13 pipe cells, status cell
   exactly `mined`, first URL equal to one of the three frozen documents
   (`doc_key`, case-insensitive, no scheme/`www.`/trailing slash), anchor cell
   carrying a `.ufo/evidence/round-47/coverage/sources/…` path whose first 8+
   hex sha256 prefix recomputes over the snapshot bytes.
3. The entry path `corpus/knowledge/<basename>` appears in that row's used-by
   cell (comma/semicolon separated, exact string).
4. At least one double-quoted span on **one line**, 6..25 whitespace tokens
   after the counter's fold, located in the cited row's snapshot text, and at
   least one such located span absent from the package copy of the same
   basename.
5. The entry path is backticked in `corpus/README.md` at REV; the coverage-map
   row lands in the same round (QUALITY 7).
6. QUALITY 87: every token count the entry prints is produced by a command over
   the quote's own bytes, folded the counter's way.

Note the row's URL trap (F13): the Semantic Scholar row must use the `%2C` form.

## 9. Residual risk and verification gaps

- The S2 record's `venue` conflict (F12) cannot be resolved inside the lane: the
  only committed artifact is the Semantic Scholar record, and it disagrees with
  the DOI/DBLP key. The gate can require the conflict be stated; it cannot decide
  which is right without a publisher-side snapshot.
- The arxiv 2607 author mismatch (F8) may be a package-row error or an arXiv
  metadata error. I verified only against the committed snapshot, which is the
  lane's evidence standard (QUALITY 2). I did not fetch the live page.
- I did not verify the S158 claims' content against the ACM version (no access;
  the entry says the same). The PDF check was page-locator only.
- The counter's `DOCS`/`rows` construction was read and its predicate executed
  in scratch against real snapshot bytes; I ran no `--rev` measurement, so no
  numeric C3 state is claimed here.
- `flaky-aware-verdict-evidence.md`'s "the lane's own ledger keeps outcomes and
  exit codes per case" could be true of a *counter receipt* rather than the
  ledger; if the seat re-anchors it to a receipt, F5.2 downgrades to a citation
  fix. I found no such receipt in the ledger itself.
- `lsp` was not available: the device list reports no `lsp` mount (mounted:
  `ast_edit`, `debug`, the `tripo_*` / `unity_cli_status` MCP tools), and the
  files under review are Markdown entries plus a Python monitor script with no
  language server attached. All quote-location and cross-reference checks here
  are therefore text-level (counter `fold` + substring, `grep -c`) and are
  recorded as such — the one semantic check that mattered (does the lane's rule
  score a timeout as a kill?) was resolved by reading the two held entries, not
  by grep alone.

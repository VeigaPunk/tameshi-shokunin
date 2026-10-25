# Review: staged PIT outcome-vocabulary entry (round 42 w1)

Reviewed entry: `/home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge/corpus/knowledge/pit-outcome-vocabulary.md` (staged `S159`/`S160`).
Bar: `corpus/QUALITY.md` criteria 1–36 (read in full) and `PROVINCE.md` (Core/Frontier F1, lines 40–42, 105).
Access date for every quote below: 2026-10-25.

## Verdict: ADMIT-WITH-EDITS

Every source claim checks out against the live pages and against the lane's held S001 row; three prose fixes (E1–E3) and two adoption obligations (E4–E5) are required before landing.

## Findings

### V1 — Lane claim “holds S001 Stryker semantics” verified
Entry line 26: “score = detected ÷ valid, with compile and runtime errors excluded”.
- `corpus/SOURCES.md:12` (row S001): “score = detected / valid x 100 with detected = killed + timeout; compile and runtime errors excluded”.
- `corpus/knowledge/mutation-score-semantics.md:23` (Stryker `detected/valid`, compile/runtime errors invalid and excluded) and `:16` (Timeout counted as detected).
✅ holds.

### V2 — Lane claim “treats a timeout as a detection” verified, but worded as if it were the lane's own verdict rule (EDIT E1)
- `corpus/SOURCES.md:12`: “detected = killed + timeout”. ✅ the held Stryker semantics counts timeout as detected.
- But the lane's **own** verdict rule is the opposite: `mutation-score-semantics.md:10` (“only Killed and Survived enter its rate … Inconclusive excluded”) and `:71` (Rejected rule: “count Timeout as a kill” — Tameshi's recorded score; “merely observing a timeout is insufficient”). Entry line 35-36 (“The lane's own convention has a known hole. The lane's recorded convention treats a timeout as a detection (its held S001 semantics)”) therefore conflates the recorded external Stryker semantics with the lane's own scoring convention. The load-instability finding is real (V4) but attaches to Stryker-style scoring, not to the lane's own k/(k+s) rule. Fix: reword to “the Stryker semantics the lane records (S001) treat a timeout as a detection”, and note the lane's own rule already excludes inconclusives, so the inference applies to Stryker-style reports, not to the lane's own score.

### V3 — Seven-way PIT vocabulary verified on the live page
`curl -fsSL 'https://pitest.org/quickstart/basic_concepts/'` (saved `/tmp/tameshi-r42-L1Tameshi42.ReviewPitEntry/basic_concepts.html`, sha256 `c51d8423f5a75e00c7039463f8a5992ef8f1f92b994d69f67d212ff7bfd92b3a`, 12155 B) contains all seven terms: Killed, Survived, No coverage, Non viable, Timed Out, Memory error, Run error. Both quoted sentences are verbatim:
- “Survived … means the mutation was not detected by the covering test.” (basic_concepts.html, `<strong>Survived</strong>` paragraph)
- “No coverage … is the same as Survived … except there were no tests that exercised the line of code where the mutation was created.” (same file, next paragraph)

### V4 — FAQ determinism quote verified; “names the timeout class as the mechanism” is half of it (EDIT E2)
`curl -fsSL 'https://pitest.org/faq/'` (saved `/tmp/tameshi-r42-L1Tameshi42.ReviewPitEntry/faq.html`, sha256 `ccf6ac493d6935e2f0a90b716254c57024973d5e2bf1bf3c1e8e60b9772629c1`, 20845 B):
- Verbatim: “works hard to be fully deterministic, but two factors might cause the results to differ slightly between two runs with the same input.” (faq.html, “Is it random?” section)
- Timeout mechanism, verbatim: “Both these measurements can be affected by external factors (other processes on the machine etc), so a mutant may be detected as timed out on one run, but killed or surviving on another.” (faq.html, §Timeouts)
- The FAQ names **two** factors (Timeouts **and** Static initializers, `h3#static-initializers` directly after); entry line 20 (“names the timeout class as the mechanism”) silently drops the second. The finding survives; the sentence should say timeouts (and static initializers) are the two factors, with the timeout class being the one whose classification depends on machine load.

### V5 — 404 claim verified
`curl -sSL -o /dev/null -w '%{http_code}\n' 'https://pitest.org/quickstart/mutationcoverage/'` → `404`. Entry lines 51–53 accurate.

### V6 — Recheck commands are live
- Entry line 5 recheck: `curl -fsSL 'https://pitest.org/quickstart/basic_concepts/' | grep -c 'No coverage'` → today `2` (non-zero, as the entry expects).
- Staged row S160 recheck string: `grep -c 'timed out on one run' faq.html` → `1` (matches the row's “expect 1”).

### V7 — Staged SOURCES rows exist and qualify (criterion 10)
`SOURCES.append.md:13-14` (S159, S160): tier A, kind docs, status mined, opened 2026-10-23, recheck 365d, used-by includes `corpus/knowledge/pit-outcome-vocabulary.md`. Not tier-C; the entry's `source:`/`verified-at:`/`recheck:` header (lines 2–5) satisfies criterion 10.
No id collision: the lane registry holds S001–S154 (`SOURCES.md:437-440`, 109 rows); S159/S160 are outside it. At adoption the staged ids renumber to S155/S156 (per round-42 collision register), so the entry's `source:` lines must be updated to the adopted ids in the same commit.

### E3 — Lane-internal claims lack measured anchors (criterion 2)
The S001-semantics claims (lines 24–41) cite only “S001” without path:line into the lane. Append anchors: `corpus/SOURCES.md:12`, `corpus/knowledge/mutation-score-semantics.md:16,23,71`, `SKILL.md:191-213` (via mutation-score-semantics.md:10).

### E4 — Fetched bodies must be carried into the repo (criterion 9)
The package carries no evidence copy of either page. Round-41 precedent pins sources to committed snapshots (`SOURCES.md:437`). At adoption, commit `basic_concepts.html` / `faq.html` under `.ufo/evidence/round-42/sources/` with the sha256s in V3/V4 (or an opened.tsv-style record), in the round that writes the entry.

### E5 — Coverage-map row (criterion 7)
The adopt round must add the `corpus/README.md` coverage-map row for `knowledge/pit-outcome-vocabulary.md`, or name the missing row as debt in `LOG.md` with an owner (the merge package contains no README amendment).

## Cut list
Nothing to cut. The “Boundary of this entry” section (lines 46–53) is honest: it declines a mapping claim, records the 404, and stays within PIT-vs-Stryker vocabulary comparison. The inference “answerable in the negative for at least one pair” is supported by V3+V4 juxtaposed with S001.

## Remaining risk / verification gaps
- I did not run the lane's counters or the merge adopt checklist; adoption mechanics (id renumber S159→S155/S160→S156, append of `SOURCES.append.md`, README row) are outside a read-only review and remain the operator's gate.
- The lane's own score rule is cited via `mutation-score-semantics.md:10,71` (which anchor `SKILL.md:191-213`); I did not open `SKILL.md` directly — trusted with that anchor.
- `MERGE-REPORT.md:132` reassigns S159's used-by to also cover `r13-f7-cadence-and-floor.md`; I did not verify that second file's citation.
- No tools installed (none needed); only `curl`/`grep`/`perl` reads into `/tmp/tameshi-r42-L1Tameshi42.ReviewPitEntry/`.

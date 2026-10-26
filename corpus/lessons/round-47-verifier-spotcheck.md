# Round 47 verifier spot-check

author: hyaku closure (non-author integrator, @m_opus)
date: 2026-10-26
lane HEAD measured: `03facb22a3f083b93fb55d061be58ac867eabf24` (base `0b5b7cd2b2c15d23086e811a0f0348d84261277b`; freeze `9acfbe21435e1976636a276448dee1d5e7155915`; content revision `8b0e15d25ea598c0bf908d183fb410a085bf3a18`; report-cited tip `663e068287a19ebfeabfefec10620957b3dad0f4`)
driver lines (`.ufo/watchdog.log` lines 1437 and 1463 at closure): `2026-10-25T20:28:53-03:00 launch tameshi round=47 pgid=2933816 driver=hyaku-inline attempt=1`; `2026-10-26T01:03:32-03:00 complete tameshi round=47; hyaku-inline attempt=1`

## Step-1 conformance

| Check | Command | Observed |
|---|---|---|
| Report committed by lane identity | `git log --format='%an %H %ci' -- .ufo/reports/round-47/tameshi.md` (fleet repo) | `tameshi-shokunin 445b71ab773d904a12550e72728ad40144960084 2026-10-26 00:14:16 -0300` (after its last cited commit `663e0682`, 00:13:32) |
| SHONEN heading, one line per box | read report lines 45-50 | one `## SHONEN`, four `[~]` lines with prior pointers; none `[x]` |
| Cited commits exist and are ancestors of `master` | `git cat-file -t <h>`; `git merge-base --is-ancestor <h> master` for 9acfbe21, a944eb55, 8b0e15d2, edd4ca44, 663e0682 (and base 0b5b7cd2) | all `commit`, all ancestors |
| Lane pushed, clean | `scripts/hyaku/jj-lane.sh state …/tameshi-shokunin`; `git status --porcelain` | `branch=master local=remote=03facb22… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty |
| Receipts-only tail (criterion 86) | `git diff --name-only 8b0e15d2 663e0682` minus `after/`, `census-end*`, `.ufo/waves/round-47/` | `SCORECARD.md` only (the append-only deciding-results and errata block; records, no counted surface) |
| Prompt carries template contract | every non-placeholder line of `templates/round-prompt.md` (fleet and canonical copies, 140 lines) searched in `.ufo/prompts/tameshi-round-47.md` (545 lines) | 0 missing; §1-§5 plus hyaku addendum §6 |
| Real report, not a marker | report + 7 lane commits base..HEAD with evidence trees | real work; status `ok` |

Conformance defects (status-neutral):
1. **Undispatched wave / below floor.** One wave of 40 seats ran; wave 2 (32 seats) was built and never dispatched (report line 52). The round is below the 64-100 L2 floor and no falsification wave attacked the entries, additions or restated rows.
2. **Seat report rewritten after landing.** `03facb22` (orchestrator, after the report) rewrites `.ufo/waves/round-47/w1/T47ConnCross.md` (+228/-214). It is not cited by any claim; `6b5ea3b1` (orchestrator in-flight snapshot) is likewise uncited. Neither changes a counted surface.
3. **Selftest tallies not committed as L1 receipts.** The counter selftests the report cites (C1 35/35, C2 14/14, C3 24/24) appear only in lane-dispatched seat reports (`w1/T47MutC1Counter.md:11`, `w1/T47RevC2Predicate.md:193`, `w1/T47MutC3Counter.md:6`); `addition-lint.py --selftest` 7/7 (SCORECARD capability row) has no committed output anywhere (`grep -rn ADDITION_LINT_SELFTEST .ufo/evidence/round-47 .ufo/waves/round-47` → only the source line). Round 46 committed `selftest/c*-selftest.stdout`; round 47 did not.
4. **Criterion 93 falsifier has no receipt.** `quality/c91-92-falsifiers.stdout` (7 lines) carries `CRITERION-91-FALSIFIER-OK` and `CRITERION-92-FALSIFIER-OK` only; block 93 of `falsifiers.sh` exists but its output is uncommitted. The report says the receipt was taken before 91 was added to the script, yet it contains the 91 line.
5. **Lesson dependence sets disagree with the rows.** `corpus/lessons/round-47.md:117-118` gives `six-leg regression ledger` {fleet-root, node} and `hermetic env-differential probe` {env, node}; the standing rows state {env, fleet-root, node} and {bwrap, node}, and the deciding run observed {fleet-root, node} and {bwrap, node}. The instability is disclosed in SCORECARD; the lesson line is a stale observation (corrections-sweep rule).

## Per-claim re-check

Method: the three counters are lane-owned gates. Per PROTOCOL §Gate standard (Closure consequence) I did not execute them or the lane's selftests; I verified their committed deciding receipts, the revision measured, the sha256 pins, and re-measured with plain commands (git, grep, sha256sum, jq, curl) what can be re-measured without them.

### C1 calibration (lowest non-retired axis, monitor 6): MISS, evidence-verified + inputs re-measured

Committed deciding line (`.ufo/evidence/round-47/after/c1.stdout`, rev `8b0e15d2…`, `after/c1.exit` = `1`): `C1_R47: self_pin=1 stmts_pin=1 statements=22 mismatches=1 unparsed=0 unobservable=0 dep_mismatch=1 unpinned=0 append_only=1 total=2 … C1_R47_PASS=false`. Before (`before/c1-at-freeze.stdout`): `unparsed=22 total=22 C1_R47_PASS=false`. The failing statement (`after/c1.stdout:5`): `six-leg regression ledger: claimed=REGRESSION: FAIL (cases=9 passed=7|1 … observed=REGRESSION: PASS (cases=9 passed=9|0 … MISMATCH declared_deps=env,fleet-root,node observed_deps=fleet-root,node DEPS-MISMATCH`.

My re-derivation at `03facb22`:
- `git show B:SCORECARD.md` is a byte prefix of `git show A:SCORECARD.md` → `True`; `git diff --numstat B A -- SCORECARD.md` → `63 0`.
- Round-47 standing table: 22 rows carry `tool sha256` and 22 carry a `deps` clause (Python regex count over the section).
- `git show A:<tool> | sha256sum | cut -c1-12` for the 19 distinct pinned files (16 `tools/*`, `kaika-round-1/sources-census-v2.sh`, `round-15/verify.py`, `round-21/coldread/measure.py`, `round-45/freshness/measure.py`) equals every row prefix (b9b754713c9c … ba64041f49ff); `git diff --name-only B A -- tools .ufo/evidence/{round-15,round-21,round-45,kaika-round-1}` → 0 paths.
- `calibration/statements.json` sha256 `924102df…` = contract pin; the seven frozen counter files hash to `after/frozen.stdout` `COUNTER_SHA256` lines; `git diff --stat 9acfbe21 8b0e15d2` over the frozen counters → only `deciding-run.sh` and the two v2 hardening counters (the C2 deliverable) changed.
- Controls (`control/controls-at-freeze.stdout`): CTL_I `total=22`, CTL_J `dep_mismatch=5`, CTL_K `total=0 PASS`.
- The errata block (`SCORECARD.md`, last section, appended in `663e0682`) names the wrong row, states the round-46 value was the stable one, and says the target was not narrowed.

Ruling: the claim **does not verify** (total 2 ≠ 0). 21 of 22 rows now match with an observed dependence set, which is real progress, but the declared target is all 22. The mis-stated row is marked in the same file by the lane's own errata, so the axis is not harmed: **calibration unchanged** (monitor 6 → 6, `after/no-harm.stdout`).

### C2 operability: met, evidence-verified

Committed deciding line (`after/c2.stdout`, rev `8b0e15d2…`, exit `0`): `killed=183 applicable=183 neutral_killed=0 pristine=2 equivalence=1 target=150 … C2_R47_PASS=true`. Before (`before/pool-base.stdout`, `--targets base`): `killed=122` (freshness 58, coverage 64).

My checks: `grep -c '^MUT .* killed | FAIL' after/c2.stdout` → `183`, `grep -c '^MUT '` → `183`, `grep -c '^NEUTRAL .* survived'` → `14` of 14; `GROUP` lines: freshness 101/101, coverage 82/82, both `neutral_killed=0 pristine=1`; `jq '.groups|map_values(length)' hardening/pool.json` → freshness 111, coverage 86 (= 183 real + 14 neutral); pool sha256 `b4f0d075…` = contract pin; `after/addition-lint.stdout` `findings=0` twice; `after/frozen.stdout` `HARDENED_REBUILD=1 ADDITION_LINT_OK=1`. Controls CTL_E (`neutral_killed=14`), CTL_F (`pristine=0`), CTL_G (`killed=122`), CTL_H (`killed=0`) all false. Limits I confirm as limits, not harm: the frozen counter alone admits a differential oracle (160/183, disclosed; the lint closes it for the nine additions); no fresh-mutant generalization was measured; I did not re-run any mutant (lane gate). **operability improved**.

### C3 coverage (F3, sourced, assimilation): met, re-measured

Committed deciding line (`after/c3.stdout`, exit `0`): `rows=3 entries=3 indexed=3 covered=3 row_ids=S261,S263,S264 … C3_R47_PASS=true`; before `rows=0 entries=0`.

My re-derivation:
- `grep -cE '^ {0,3}\| S[0-9]{3,} \|' corpus/SOURCES.md` → `124`; at base → `120`; diff 12+/0-. Rows at lines 136-139, all `mined`, opened 2026-10-25.
- `git show B:corpus/SOURCES.md | grep -ciE '2302\.09330|2607\.09345|ICST60714\.2024\.00037|LamETAL20'` → `0` (unheld at base); base `corpus/README.md:577` F3 line holds clustering and the false-red figure only.
- `sha256sum coverage/sources/*`: 2965343c…, 16ecdefc…, 6ab5b3f5… equal the three row anchors; Lam PDF `0b880458…` and text `bf52c908…` equal S262's anchor.
- Each entry opens `source: S26x — <url>`, `verified-at: 2026-10-25`, `recheck:`; indexed at `corpus/README.md:585-587`; each differs from its package copy (`diff` lines only in lane: 75, 42, 37).
- Live re-open (below) located all four Gate quotes.

Ruling: **coverage improved** (three entries on ground the base map did not hold).

### No-harm

`after/no-harm.stdout`: seven monitors `ok` (command D 9, coldread 6, r45 freshness fresh=71, r45 coverage 2/2, S160 count 1, registry 124 ≥ 120, r46 coverage 3/3); `after/coldread-sections.stdout` `60 (base 60)`; `git diff --stat B A -- PROVINCE.md SKILL.md SHONEN.md` → empty; `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit `0`, `ok`, eleven W01/W04 warnings (all pre-existing rows S047-S160), no error code.

## Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| calibration | unchanged | C1 honest miss: total 22 → 2 (target 0); the wrong row is marked by the lane's errata; monitor 6 → 6 |
| operability | improved | C2 killed 122 → 183 of 183, neutral 0; evidence-verified |
| coverage | improved | C3 rows 120 → 124, three indexed entries on unheld ground; re-measured |
| depth | unchanged | command D 9 → 9 |
| freshness | unchanged | fresh 71, score 9 → 9 |
| adjacency | unchanged | no sibling ground touched; misroot sweep reported, nothing absorbed |

No axis harmed. Re-measured: C3 fully; C1 inputs (sha pins, row and deps counts, append-only, frozen paths). Evidence-verified only: the C1 and C2 counter verdicts and all selftest tallies. Round verdict: **rejected-honest-stop** (C1 does not verify; nothing harmed).

## Discernment spot-check

| Item | Decision | Re-opened source | agree/disagree | Reason |
|---|---|---|---|---|
| S261 arXiv 2302.09330 | admit | live `curl -fsSL https://arxiv.org/abs/2302.09330` → 43,549 bytes, sha256 `2965343ceaac627c…` = snapshot | agree | the 24-token Gate quote ("Detecting flaky tests is therefore a crucial task … systematic response") occurs 3× live; ground unheld at base |
| S263 arXiv 2607.09345 | admit | live abs page → 44,459 bytes, sha256 `16ecdefca1f247d3…` = snapshot; `citation_author` meta | agree | the 10-token quote occurs 3× live; authors live are Gültekin, Berndt, Bell, Bach, Baltes, confirming the lane's correction of the package attribution |
| S262 Lam et al. camera-ready PDF | admit (uncounted fourth row) | live PDF sha256 `0b88045817f146db…` = anchor; `pdftotext` (non-layout) | agree | "one can use ≤ 5 reruns (50% less than Google’s default ten" located once, curly apostrophe intact, and "check correctly ≥ 82% of the time" present; supports the quarantine-S110 adoption |
| S264 Semantic Scholar record of DOI 10.1109/ICST60714.2024.00037 | admit narrowly, tier B | live API: HTTP 429 on three attempts; fallback `api.crossref.org/works/10.1109/ICST60714.2024.00037` + committed snapshot | agree | quote located once in the committed snapshot; Crossref gives "2024 IEEE Conference on Software Testing, Verification and Validation (ICST)" while the S2 `venue` reads "International Conference on Information Control Systems & Technologies", so the lane's carrier-defect disclosure and tier B are right. Live S2 bytes not re-opened |
| `r13-flaky-false-red-rate.md` | reject (duplicate) | package copy `shokuknow/merge/tameshi/knowledge/corpus/knowledge/r13-flaky-false-red-rate.md:7,13`; lane `SOURCES.md` S026 and S260 rows; `corpus/knowledge/r9-false-red-rate.md` | agree | the 84% pass-to-fail figure is already held by two lane rows and an admitted entry |
| `r8-predictive-test-selection-cost.md` | reject | package copy head (cites staged S205, arXiv 1810.05286); `grep -c 1810.05286 corpus/SOURCES.md` → 0; live arXiv quote present (1); `PROVINCE.md:14-18` | agree, reason partly | the decisive reason is QUALITY 10/2: the entry cites a row the lane never opened. The `PROVINCE.md:14-18` cite is weak (those lines refuse product domains and sibling gates, not test selection); the flip condition (an opened row tied to an own-leg F7 re-sweep decision) is the right one |
| New row S264 (`corpus/SOURCES.md:139`) and its ≤25-word quote | row fields | snapshot `s2-icst24-cost-of-flaky.json` | agree | anchor prefix `6ab5b3f5` = snapshot sha256; the 23-token Gate quote is in the `abstract` field; the row's 0.02 cents / $5.67 figures are in the same abstract |

Result: the spot-check agrees with the gate on four admits and two rejects. One reject rests on a weaker cited line than it needs; the decision stands.

## Trend verdicts

- **expansion: improved**: three admitted entries on ground the base coverage map did not hold (prediction from recorded history, flakiness not static, cost of a failed pipeline). Each cites a newly opened, snapshot-pinned `mined` row, and every Gate quote was located live or in the pinned snapshot.
- **quality: unprovable-but-better**: the pool kill count rose 122 → 183 with a lint against embedded oracles, and QUALITY 91 shipped a red-before/green-after receipt. No non-author re-ran a kill, no fresh-mutant generalization exists, and one standing row was superseded by a flaky value. The row is marked by errata, so it is not harmed, but it is a step back from the round-46 row.
- **discernment: improved**: the outside spot-check agrees with the gate on admits and rejects. Round-46 routed defects 2, 3 and 4 became QUALITY 93, 92 and 91, each citing its lesson row and carrying a falsifier. Receipts exist for 91 and 92, not for 93 (defect 4 above).

## Routed defects for the lane next round

1. **C1 standing row**: append a superseding row for `six-leg regression ledger` stating the stable observation (or a declared-unstable form the counter can score), and make the C1 counter's observation repeatable (N ≥ 3 per profile, or a declared nondeterministic class) before re-claiming calibration. `hermetic env-differential probe` printed 9/9 and 2/9 under one profile and needs the same treatment.
2. **Commit selftest receipts** for the three round-47 counters, `addition-lint.py` and the criterion-93 falsifier block (conformance defects 3 and 4).
3. **Lesson correction**: append a named correction for `corpus/lessons/round-47.md:117-118` dependence sets (conformance defect 5).
4. **Reject citation**: when refusing `r8-predictive-test-selection-cost.md` again, cite the unopened-row reason (QUALITY 10) rather than `PROVINCE.md:14-18`.
5. **Carried items** (from SCORECARD Planned round 48, still open): round-45 per-snapshot fetch receipt and S026/S093/S108 anchor refresh; dead `brace_depth_at` helpers; the C1 counter's 8 and the C3 counter's 10 mutation survivors (`w1/T47MutC1Counter.md`, `w1/T47MutC3Counter.md`); a located-name (author) check.
6. **Round shape**: run the falsification wave in the round that lands the entries; a 40-seat round below the floor leaves the additions and restated rows unattacked.
7. SHONEN: all four boxes remain `[~]`, and none is fully checkable by a non-author this round. Promotion stays operator-owned.

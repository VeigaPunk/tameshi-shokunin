seat: T46ConnCross1
item: pattern-find across round-46 claims (C1, C2, C3) and sources applying r6-flaky-failures-cluster independence argument; probe counts, effective sample sizes, inflation analysis, comparison table, and one bounded connector proposal.

## Method and Bounds
- Read-only inspection of lane repository at base `683eedde3a50441c34d85a22f5fd5346f8b1ec6d`, freeze `745a583181648cfc7f9c1b476cd1be7dc68f7433`, and content revision `6f2168e028ce7ff6e82ac92093ac05dd1f147c32`.
- Read-only package `/home/vgpnk/Projects/shokuknow` untouched.
- Scratch workspace `/tmp/tameshi-r46-T46ConnCross1/` used for all temporary analysis scripts.
- Only the single designated deliverable `.ufo/waves/round-46/w2/T46ConnCross1.md` is written. No mutating git commands, no pacman transactions.

---

## 1. The Independence Argument (`r6-flaky-failures-cluster.md`)

The C3 knowledge entry `corpus/knowledge/r6-flaky-failures-cluster.md` (citing S258, arXiv:2504.16777v1 [cs.SE], Parry, Kapfhammer, Hilton, McMinn, 2025) establishes a fundamental principle of verification evidence:
- **Root-cause clustering**: *"flaky tests often exist in clusters, with co-occurring failures that share the same root causes, which we call systemic flakiness"* (line 16).
- **Upper bound vs real bound**: *"Inference: N controls drawn from one cluster are one probe of one cause repeated N times, so the count of controls is an upper bound on independent evidence, and the count of distinct causes touched is the real bound"* (line 28).
- **Survivor list overstatement**: *"Inference: two survivors from one cluster supply one anchor, not two, so a per-survivor verdict table that does not record cluster membership overstates the number of independent anchors it holds"* (line 32); *"Survivor lists are not independent observations. Inference: if a survivor set contains several members of one flaky cluster, it is one finding counted N times; the classification should carry cluster membership beside each per-survivor verdict"* (line 36).

When this exact epistemological lens is turned inward onto the lane's own round-46 claims and counters, it reveals that every declared claim target relies on nominal entity counts that conflate clustered probes with independent observations.

---

## 2. Independent Probe Counts by Claim

### Claim C1: Calibration
- **Claim surface**: Standing self-assessment re-stated against the repo; 22 frozen statements in `.ufo/evidence/round-46/calibration/statements.json` matched against the latest standing rows in `SCORECARD.md`.
- **Target**: `total = 0` (mismatches + unparsed + unobservable = 0 across all 22 statements).
- **Nominal $n$**: 22 statements (19 capability rows + 3 axis rows: depth, calibration, freshness).
- **Analysis of independence**:
  1. *Command-level probe independence*:
     - Running command: `python3 -c "import json; data=json.load(open('.ufo/evidence/round-46/calibration/statements.json')); cmds=[s['cmd_text'] for s in data['statements']]; print('total=%d unique_cmds=%d' % (len(cmds), len(set(cmds))))"`
     - Output: `total=22 unique_cmds=21`
     - Statements 15 and 16 execute identical command strings:
       - Statement 15 (`tally-audit-v3 runner audit`): `python3 tools/tally-audit-v3.py --selftest`
       - Statement 16 (`bounded ANSI-C code_view`): `python3 tools/tally-audit-v3.py --selftest`
     - In `statements.json:229-260`, both entries specify identical `argv` (`["python3", "tools/tally-audit-v3.py", "--selftest"]`), identical regex `obs` (`^(TALLY_AUDIT_V3_SELFTEST: \d+/\d+ pass)`), identical `sha_file` (`tools/tally-audit-v3.py`), and identical `timeout` (1800s).
     - In `SCORECARD.md:1290-1293` (at revision `6f2168e0`), both standing rows carry identical evidence pointers: `` `python3 tools/tally-audit-v3.py --selftest` → `TALLY_AUDIT_V3_SELFTEST: 35/35 pass`, exit 0, tool sha256 `da8c1ef4b30c` ``.
     - A single run of `python3 tools/tally-audit-v3.py --selftest` satisfies or fails both rows simultaneously. They share a single execution root cause.
  2. *Executable script-level probe independence*:
     - Distinct scripts/binaries tested: 20.
     - Statement 2 (`mutation sweep runner`, `bash tools/mutate-and-run.sh --selftest`) and Statement 3 (`six-leg regression ledger`, `bash tools/mutate-and-run.sh --regression`) invoke the same script target `tools/mutate-and-run.sh`.
     - Statements 15 and 16 invoke `tools/tally-audit-v3.py`.
  3. *Tool evolutionary family clustering*:
     - Statements 14 and 15/16 invoke `tools/tally-audit-v2.py` and `tools/tally-audit-v3.py` (successive iterations of the tally audit runner).
     - Statements 17 and 18 invoke `tools/write-path-census-v2.py` and `tools/write-path-census-v3.py` (successive iterations of the write-path census).
     - Grouping by distinct tool families yields 18 tool families.
- **Effective independent $n$**: 21 independent command executions (or 20 distinct script targets).

### Claim C2: Operability
- **Claim surface**: Hardening the round-45 claim counters; 25 declared survivors in `.ufo/evidence/round-46/hardening/mutants.json` (15 on `freshness/measure.py`, 10 on `coverage/measure.py`), plus 6 neutral mutants.
- **Target**: `killed >= 23` of 25 (with `neutral_killed = 0`, `pristine = 1`, `equivalence = 1`).
- **Nominal $n$**: 25 declared mutants.
- **Analysis of independence**:
  1. *Rule-line clustering*:
     - 25 mutants touch only **19 distinct source code lines** across both target files:
       - **Freshness counter (`.ufo/evidence/round-45/freshness/measure.py`, 437 lines)**:
         - Line 97 (in `population()`): **3 mutants** share this exact line (`if r['status'] == 'mined' and int(rid[1:]) <= MAX_ID and r['url']}`):
           - `F04`: drops `and r['url']`
           - `F14`: mutates `r['status'] == 'mined'` to `r['status'] != 'queued'`
           - `F15`: mutates `<= MAX_ID` to `< MAX_ID`
         - Line 256 (in `measure()`): **2 mutants** share this exact line (`passed = self_pin == 1 and fresh >= TARGET`):
           - `F11`: drops `self_pin == 1 and`
           - `F12`: mutates `fresh >= TARGET` to `fresh >= 0`
         - Lines with 1 mutant each (10 lines): L142 (`F01`), L151 (`F02`), L157 (`F03`), L189 (`F07`), L204 (`F06`), L206 (`F08`), L209 (`F09`), L211 (`F13`), L241 (`F05`), L254 (`F10`).
         - Total distinct lines in freshness: 12 lines for 15 mutants.
       - **Coverage counter (`.ufo/evidence/round-45/coverage/measure.py`, 224 lines)**:
         - Line 135 (in `measure()`): **4 mutants** share this exact line (`passed = self_pin == 1 and len(entries) >= 2 and len(rows) >= 2 and len(indexed) == len(entries)`):
           - `C07`: mutates `len(rows) >= 2` to `len(rows) >= 1`
           - `C08`: mutates `len(entries) >= 2` to `len(entries) >= 1`
           - `C09`: mutates `len(indexed) == len(entries)` to `len(indexed) >= 1`
           - `C10`: mutates `self_pin == 1 and len(entries)` to `self_pin >= 0 and len(entries)`
         - Lines with 1 mutant each (6 lines): L35 (`C01`), L36 (`C02`), L83 (`C03`), L98 (`C04`), L103 (`C05`), L129 (`C06`).
         - Total distinct lines in coverage: 7 lines for 10 mutants.
     - Total distinct rule lines across all 25 declared mutants: $12 + 7 = \mathbf{19}$ distinct lines.
     - Fully 9 of the 25 mutants (36%) cluster onto just 3 lines of code (L97, L256, L135).
  2. *Function-level scope clustering*:
     - 25 mutants live in only **9 distinct functions / logical scopes**:
       - Freshness (5 functions): `population()` (3 mutants: F04, F14, F15), `grade()` (3 mutants: F01, F02, F03), `review_sets()` (4 mutants: F06, F08, F09, F13), `measure()` (4 mutants: F05, F10, F11, F12), `wave_seats()` (1 mutant: F07).
       - Coverage (4 scopes): `measure()` (5 mutants: C06–C10), `entry_ok()` (2 mutants: C04, C05), top-level configuration (2 mutants: C01, C02), `gt_rows()` (1 mutant: C03).
  3. *Assertion coupling*:
     - On Coverage line 135, four mutants weaken separate conjuncts of one predicate. While each mutant can be individually isolated by crafting an artificial fixture with a single conjunct violated, any test run that alters the common evaluation state of `measure()` couples their verdicts.
     - On Freshness line 97, the single test `T15_population_bounds` in `freshness-counter.py:368` evaluates `pop == ['S001']` over a 4-row input, which directly addresses the filtering rules of F04, F14, and F15 simultaneously.
  4. *Target calculation under independence*:
     - Nominal target: kill $\ge 23$ of 25 declared mutants ($92.0\%$).
     - How many distinct rule lines are killed when 23 of 25 mutants are killed?
       - If the 2 surviving mutants sit on single-mutant lines, the 23 killed mutants cover $16 - 2 + 3 = 17$ distinct lines ($17/19 = 89.5\%$).
       - If the 2 surviving mutants are co-located (e.g. F11 and F12 on L256, or two of C07–C10 on L135), the 23 killed mutants cover 18 distinct lines ($18/19 = 94.7\%$).
       - If 25 of 25 are killed (as observed at `6f2168e0` via `mutate.py`), exactly 19 distinct lines are killed ($100\%$).
     - Thus, the nominal target of 23 kills corresponds to killing at least 17 to 18 distinct rule lines out of 19.
- **Effective independent $n$**: 19 distinct rule lines (or 9 distinct functions).

### Claim C3: Coverage
- **Claim surface**: 3 new registry rows in `corpus/SOURCES.md` (S258, S259, S260) and 3 re-grounded knowledge entries (`r5-undetected-flaky-failures.md`, `r6-flaky-failures-cluster.md`, `r9-false-red-rate.md`).
- **Target**: `rows >= 3`, `entries >= 3`, `indexed == entries`, `covered == rows`.
- **Nominal $n$**: 3 documents / rows / entries.
- **Analysis of independence**:
  1. *External bibliographic work independence*:
     - Document 1 (S258): `https://arxiv.org/abs/2504.16777` — arXiv:2504.16777v1 [cs.SE], Parry, Kapfhammer, Hilton, McMinn (2025). Genuinely novel external paper.
     - Document 2 (S259): `https://portal.fis.tum.de/en/publications/an-empirical-study-of-detected-and-undetected-flaky-test-failures/` — TUM portal record of IEEE TSE 2026 paper, Leinen et al. Genuinely novel external paper.
     - Document 3 (S260): `https://testing.googleblog.com/feeds/posts/default/6277555988217606236?alt=json` — Google Testing Blog per-post JSON feed of John Micco's post "Flaky Tests at Google and How We Mitigate Them", published 2016-05-27.
     - **Duplicate carrier of held S026**:
       - Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 6f2168e028ce7ff6e82ac92093ac05dd1f147c32:corpus/SOURCES.md | grep -E '^\| S(026|260) \|'`
       - Row S026 (held since round 12): `| S026 | Flaky Tests at Google and How We Mitigate Them (John Micco, Google Testing Blog, 2016) — https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html | docs | A | Google's flakiness rates and mitigations | Post body, published 2016-05-27 ... | mined | 2026-10-19 | 730d | corpus/knowledge/repeated-control-precondition.md |`
       - Row S260 (adopted round 46): `| S260 | Flaky Tests at Google and How We Mitigate Them (Micco; Google Testing Blog, published 2016-05-27; the publisher's per-post JSON record of the post) — https://testing.googleblog.com/feeds/posts/default/6277555988217606236?alt=json | docs | A | ... | entry.content body of the per-post record, post id tag:blogger.com,1999:blog-15045980.post-6277555988217606236, published 2016-05-27T17:31:00-07:00 ... |`
       - As documented by w1 seat `ConnPackageCross.md:21-22, 50`, staged rows S216, S225, S229, S235 all cite this identical 2016-05-27 blog post via its per-post feed, and S212 cites the general feed.
       - S260 introduces a new *access carrier* (the Blogger JSON API endpoint), but **not a new source document**. The empirical findings (1.5% flaky runs, 84% pass-to-fail transitions, 3-in-a-row rerun mark) are identical to the text held in S026 since round 12.
       - The count of genuinely novel external bibliographic works added in round 46 is **2**, not 3.
  2. *Thematic clustering*:
     - All three documents belong to the identical thematic cluster: F3 determinism precondition / flaky-aware verdicts, studying flaky test reruns in CI systems (Google's rerun mitigation vs TUM's undetected failure blindness vs arXiv's systemic failure clustering).
- **Effective independent $n$**: 2 novel external bibliographic works (and 1 thematic cluster).

---

## 3. Inflation Analysis and Stricter Counts

### Which Claim's Target is Most Inflated?

Evaluating inflation depends on whether one measures **novelty of external evidence** or **structural concentration of test fixtures**:

1. **Claim C3 is most inflated in external evidence novelty**:
   - Nominal $n = 3$, independent novel documents $n = 2$.
   - **Inflation factor = $3 / 2 = 1.50\times$ (50% inflation)**.
   - Fully **33.3% of Claim C3's target surface** (1 of 3 rows) is an alternate API carrier format of an existing held document (S026). Counting S260 as an independent discovery inflates the true external coverage advance by 1.5×.

2. **Claim C2 is most inflated in structural concentration**:
   - Nominal $n = 25$ mutants across only 19 distinct lines ($25 / 19 = 1.32\times$) and only 9 functions ($25 / 9 = 2.78\times$).
   - Line 135 in `coverage/measure.py` alone hosts 4 declared mutants (16% of the entire manifest) on a single boolean conjunct.
   - Killing 23 mutants does not require 23 independent fixes or tests; it requires testing at most 17 to 19 distinct code sites.

3. **Claim C1 is the least inflated**:
   - Nominal $n = 22$, independent commands $n = 21$ ($22 / 21 = 1.048\times$, 4.8% inflation).
   - Only a single command execution (`tools/tally-audit-v3.py --selftest`) is evaluated twice to back statements 15 and 16.

### Stricter Target Counts

- **Stricter C1 Target**: Require `total = 0` over **21 distinct command probes** (or 20 distinct script files), explicitly de-duplicating statements that execute identical `cmd_text` strings.
- **Stricter C2 Target**: Require killing **at least 17 of 19 distinct mutant lines** ($89.5\%$), with a cap of at most 1 kill credited per code line, ensuring that kills cannot be harvested from multiple syntactic variants of a single boolean line (e.g. L135 or L97), and requiring all 9 functional scopes to be touched.
- **Stricter C3 Target**: Require **3 distinct external bibliographic works** (defined by canonical publication identity rather than URL/API carrier variation), which would reject S260 as a carrier alias of held S026 and require 3 genuinely novel external sources.

---

## 4. Cross-Claim Independence Summary Table

| Claim | Nominal $n$ | Independent $n$ | Inflation Factor | Concrete Repository Evidence |
|---|---|---|---|---|
| **C1** (Calibration) | 22 statements | 21 distinct commands (20 distinct scripts) | $1.048\times$ (by command)<br>$1.100\times$ (by script) | Stmt 15 (`tally-audit-v3 runner audit`) and Stmt 16 (`bounded ANSI-C code_view`) both run `python3 tools/tally-audit-v3.py --selftest` with identical regex and sha (`statements.json:229-260`, `SCORECARD.md:1290-1293`). Stmts 2 & 3 both target `tools/mutate-and-run.sh` (`--selftest` vs `--regression`). |
| **C2** (Operability) | 25 declared mutants (target $\ge 23$) | 19 distinct rule lines (9 distinct functions) | $1.316\times$ (by line)<br>$2.778\times$ (by function) | 9 mutants cluster onto 3 lines: coverage L135 hosts 4 mutants (C07–C10 in `measure()`); freshness L97 hosts 3 mutants (F04, F14, F15 in `population()`); freshness L256 hosts 2 mutants (F11, F12 in `measure()`). 25 mutants live in 9 functions (`mutants.json`, `freshness-counter.py:97,256`, `coverage-counter.py:135`). |
| **C3** (Coverage) | 3 documents / rows / entries | 2 novel external works (1 thematic cluster) | $1.500\times$ (by novel work) | S260 (`google-flaky-feed-6277555988217606236.json`) is an alternate Blogger JSON API carrier for held row S026 (`https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html`, Micco 2016). Only S258 (arXiv 2504.16777) and S259 (TUM TSE 2026) are novel external works (`SOURCES.md:37,135`, `ConnPackageCross.md:21-22,50`). |

---

## 5. Connector Synthesis: One Bounded Proposal

### Evidence
1. `corpus/knowledge/r6-flaky-failures-cluster.md:28, 36`: Controls or survivors drawn from one cluster are one observation repeated $N$ times; reporting unclustered lists overstates independent evidence.
2. `statements.json:229-260`: C1 measures 22 statements, but Statements 15 and 16 run the exact same command on the same file with identical regex.
3. `mutants.json` and `.ufo/evidence/round-46/hardening/coverage-counter.py:135`: C2 counts 25 mutants, but 4 mutants cluster onto line 135 and 3 cluster onto line 97.
4. `SOURCES.md:37, 135`: C3 counts 3 new sources, but S260 shares canonical publication identity with held S026.
5. Sibling precedent (`souji-shokunin/SCORECARD.md:14` and `tabi-shokunin/SCORECARD.md:1245`): Lanes maintain explicit assertion boundaries and report distinct mismatch and resolution classes.

### Affected Axes
- **Calibration (Primary, C1)**: Directly improves calibration by reporting effective sample size alongside nominal counts, closing the gap between nominal claims and empirical observations without invalidating frozen contracts.
- **Operability (C2)**: Protects mutation hardening against artificial clustering where multiple mutants on a single line inflate kill counts.
- **Coverage (C3)**: Distinguishes true literature expansion from carrier-format migrations.
- **Depth & Freshness**: No harm; all existing monitors and scores remain unaffected.

### Proposed Move
**Cluster-Partitioned Claim Accounting (Partition-Aware Verification Manifests)**:
In future round manifests and counters, introduce an explicit cluster partition field for verification entities:
1. In `statements.json`, attach an optional `probe_id` (defaulting to the normalized command string). The calibration counter reports both `statements=N` and `probes=M`, verifying that $M$ distinct commands were executed.
2. In `mutants.json`, attach a `site: "<file>:<line>"` and `scope: "<function>"` annotation to each mutant. The mutation driver reports both `killed=K/declared=N` and `sites_killed=S/sites_declared=L`, preventing multiple kills on a single boolean conjunct (such as line 135) from satisfying the kill threshold without site diversity.
3. In `SOURCES.md`, attach a `canonical_doc_id` field to each row (e.g. S260 references `canonical: S026`). The coverage counter reports both `rows_adopted` and `novel_works_adopted`.

### Risks
1. *Risk*: Adding cluster requirements mid-round would alter frozen contracts (`contract.json:32, 46, 60` forbid post-score changes).
   - *Mitigation*: This proposal is strictly prospective for subsequent round design. For round 46, the counter outputs remain unedited, and effective sample sizes are reported in wave reviews.
2. *Risk*: Grouping mutants by line might disincentivize testing subtle boundary deltas on complex compound expressions.
   - *Mitigation*: The metric is dual-reported (`killed=25/25, sites_killed=19/19`), maintaining fine-grained mutant tracking while ensuring broad site coverage.

### Verification
1. Manifest parser check on round-46 artifacts:
   `python3 -c "import json; m=json.load(open('.ufo/evidence/round-46/calibration/statements.json')); print('stmts=%d cmds=%d' % (len(m['statements']), len(set(s['cmd_text'] for s in m['statements']))))"`
   Output: `stmts=22 cmds=21` (exit 0).
2. Mutant cluster check on round-46 artifacts:
   `python3 -c "import json; m=json.load(open('.ufo/evidence/round-46/hardening/mutants.json')); print('groups=%d declared=%d' % (len(m['groups']), sum(len([x for x in g['mutants'] if x['kind']=='mutant']) for g in m['groups'].values())))"`
   Output: `groups=2 declared=25` (exit 0).
3. Both checks execute cleanly in `<0.1s`, verifying that cluster partitioning is directly computable from existing manifest formats without additional dependencies.

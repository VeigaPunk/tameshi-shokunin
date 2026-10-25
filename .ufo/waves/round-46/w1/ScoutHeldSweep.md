item: C3 unheld-ground sweep for the three flaky-failure sources
seat: ScoutHeldSweep

## Findings

Classification is by claim; a different carrier URL does not make an already-held claim new.

| Document / claim | Finding | Held overlap and README coverage row | Expansion credit (CORPUS.md rule 4) |
|---|---|---|---|
| arXiv:2504.16777 — co-occurring flaky failures / 75% clustered, mean size 13.5 | **Unheld**: no matching lane registry row or knowledge entry. The only knowledge hit for `cluster|co-occur` is `runner-tally-audit-v2.md:71`, about mutation-status co-occurrence, not flaky-test clustering. | Adjacent: `repeated-control-precondition.md` §2 says retries do not repair and observed evidence is finite; `r43-survivor-resolution-rule.md` and `oracle-anchored-survivors.md` classify survivors individually, without cluster membership. The proposed knowledge note belongs in a Round-46 README index row and relates to Frontier **F3** (README:80); its package ground also names **F8** (README:85; Round 27 supersedes the displayed `open` status to `partly held`, README:424-437). | **Honest if** the admitted entry states the unheld clustering/co-occurrence claim and its bounded inference, rather than counting rows. The cluster claim is absent from lane knowledge. |
| TUM portal record, TSE 2026 — undetected flaky failures (9.8–16.3%), fresh-environment reruns, up to 3× environment variation | **Unheld** for those claims: no portal/TSE row, and no lane knowledge hit for 9.8, 16.3, or fresh-environment protocol. | Adjacent: `repeated-control-precondition.md` §2 says retries do not repair; `hermetic-env-differential.md` (F5) measures the lane's own environment differential and explicitly distinguishes raw output variation from flaky pass/fail evidence. `r8-gtest-order-and-seed.md` and `r8-gtest-primer-independence.md` (S256/S257) cover framework order/fixture independence; the TUM paper's reordering-trigger claim is adjacent, not the 9.8–16.3% measurement. README Frontier **F3** (80) and **F5** (82). | **Honest if** the entry contributes the paper's blind-spot measurement and fresh-environment protocol; the F5 overlap is only adjacent. The re-grounded row must put the TUM portal URL first: staged S190 starts with a DOI, which the frozen counter's first-URL matcher rejects. |
| Google Testing Blog per-post feed 6277555988217606236?alt=json — false-red rate / mitigation | **Held at claim level; feed carrier itself is not a lane row.** S026 is mined for the same post's rendered HTML URL and is used by `repeated-control-precondition.md`, which quotes the 1.5% rate (`:1130`) and 84% pass-to-fail figure (`:1132`), and discusses the fail-3-in-a-row mitigation (`:1136`). The feed URL has no lane row. | The held entry is the direct overlap; it is not merely a neighbouring statistic. The exact masking sentence and alarm analogy are absent from lane knowledge (grep hits: 0). Proposed README row relates to the package's F7 ground, but lane Frontier **F7** (README:84) means incremental re-sweep granularity; the held 84%/1.5% claim is already represented under **F3** via S026. A Round-46 README index row is still required. | **Not honest as new expansion if it only restates 84%/1.5%.** It can earn credit for genuinely new admitted knowledge, e.g. a distinct masking/alarm claim or a justified carrier/extraction claim, not for adding a second carrier row alone. The fresh quote candidate “It is human nature to ignore alarms when there is a history of false signals coming from a system” is present in the feed snapshot and absent from the r9 package copy. |

### Required overlap checks

`repeated-control-precondition.md` is the principal held F3 overlap: S004/S026, finite-sample limits, retries do not repair, and the S026 rates above. It does **not** state the clustering result or TUM blind-spot percentage. The two round-45 GoogleTest entries cover undefined order/shuffle/seed and per-test fixture independence; they are neighbouring framework rules, not flaky-cluster or rerun-blindness measurements. S013 and S025 mentioned by those entries are `queued` rows, not mined.

### Frozen-counter / carrier observations

- `python3 .ufo/evidence/round-46/coverage/measure.py --selftest` → `C3_R46_SELFTEST: cases=24 failed=0`; `VERDICT: PASS`; exit 0.
- At freeze `745a583181648cfc7f9c1b476cd1be7dc68f7433`, the counter printed `self_pin=1 rows=0 entries=0 indexed=0 covered=0 ... C3_R46_PASS=false` (unmoved). This is not a deciding run.
- Offline inspection using the frozen counter's `norm_text`/`fold` functions confirmed one snapshot-located, 6–25-token quote absent from each same-basename package copy: arXiv “We performed agglomerative clustering of flaky tests based on their failure co-occurrence” (12 tokens); TUM “All apparently deterministic failures were systematically validated through reruns in fresh environments” (12); Google alarm sentence above (19). These are feasibility observations, not counter verdicts.
- The first-URL predicate rejects staged S190 (DOI first) for the TUM document and staged S216 (URL token ends in `**`) for the Google feed. Landed source cells must place the exact required portal/feed URL first and unadorned. Snapshot sha256 prefixes: arXiv `28d2954d`, TUM `5eb59adf`, feed `434d8658`. Rows also need `mined`, snapshot path+digest in anchor, and exact `corpus/knowledge/<entry>.md` in used-by; README must backtick the entry path (round-45 pattern at README:562-563).
- Freshness comparison is basename-keyed: the counter loads `package/<basename(entry)>`; if absent, `package_text is None` makes any located quote fresh. Preserve the package basenames (`r6-flaky-failures-cluster.md`, `r5-undetected-flaky-failures.md`, `r9-false-red-rate.md`) so the comparison actually runs.
- Package r6's “S140, round 5” cross-reference for the 9.8–16.3% fact does not resolve to a lane registry row; lane round-40 records S140 as refused/payload-absent, while the TSE paper is staged S190 and adopted as S259. Do not carry that reference into a re-grounded entry.

## Requested sweeps (commands and output)

1. `grep -rniE 'flak(y|iness)' .../corpus/knowledge .../SKILL.md .../PROVINCE.md | cut -c1-200` — hits only in corpus knowledge: `repeated-control-precondition.md` (S004/S026, rates/retries), `hermetic-env-differential.md:84` (raw output variation, not flaky pass/fail), and the two `r8-gtest-*.md` entries (F3/order/independence). No SKILL.md or PROVINCE.md hits. Full command output was the 14 lines from these files.
2. `grep -rniE 'cluster|co-occur|false.red|false-red|undetected|same-job|rerun' .../corpus/knowledge | cut -c1-200` — no flaky-clustering hit. `repeated-control-precondition.md` has retry/finite-sample hits; `hermetic-env-differential.md` has the raw-output boundary; `r8-gtest-*.md` have order-related hits; `runner-tally-audit-v2.md:71` is mutation-status co-occurrence. Other `undetected`/`rerun` hits concern mutation semantics or recorded sweeps.
3. `grep -nE 'F3|F8|F7' corpus/README.md | cut -c1-200` — Frontier rows: F3 at 80 (`determinism precondition, flaky-aware verdicts`, open); F7 at 84 (`incremental re-sweep granularity`, open); F8 at 85 (`oracle anchoring as a survivor class`, displayed open but superseded to partly held at 424-437). README also has F3/F7/F8 round-history references and a Round-45 F3 section.
4. `grep -nE '2504.16777|googleblog|fis.tum|TSE.2026|flaky' corpus/SOURCES.md | cut -c1-220` — rows S025 (queued), S026 (mined Google rendered page; used by repeated-control-precondition.md), S027 (queued), S040 (queued), plus an unopened arXiv lead at line 269. No 2504.16777, portal.fis.tum, TSE.2026, or feed URL row.

### Literal requested command outputs

```text
$ grep -rniE 'flak(y|iness)' /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge /home/vgpnk/Projects/shokunin/tameshi-shokunin/SKILL.md /home/vgpnk/Projects/shokunin/tameshi-shokunin/PROVINCE.md | cut -c1-200
/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/repeated-control-precondition.md:1:source: S004 — https://mutants.rs/using-results.html — §§“Tests fail in an clean tree?”, �
/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/repeated-control-precondition.md:3:recheck: 730d — S026's registry cadence; S004's registry cadence is `on-release`, so re-open it at 
/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/repeated-control-precondition.md:4:ground: F3 — determinism precondition, flaky-aware verdicts (tameshi-art.md §4)
/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/repeated-control-precondition.md:18:- definition (`:1130`): “We define a "flaky" test result as a test that exhibits both a passing an
/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/repeated-control-precondition.md:19:- rate (`:1130`): “a continual rate of about 1.5% of all test runs reporting a "flaky" result”; 
/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/repeated-control-precondition.md:20:- transitions (`:1132`): “about 84% of the transitions we observe from pass to fail involve a flak
/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/repeated-control-precondition.md:21:- retry family, and S026's own verdict on it (`:1136`): “the ability to re-run only failing tests,
/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/repeated-control-precondition.md:27:- **Retries do not repair.** S026's own verdict on its re-run / fail-3-in-a-row family is that it re
/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/repeated-control-precondition.md:29:- **The evidence is finite, so the claim is finite.** `controls_match` states that the N runs actual
/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/repeated-control-precondition.md:71:- **Not a repair or a cure** — it measures agreement among runs; it does not remove nondeterminism
/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/hermetic-env-differential.md:84:**raw output variation**, not evidence of flaky pass/fail outcomes. It is
/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/r8-gtest-order-and-seed.md:28:- Held lane rows already touch order dependence: S013 (Jest `--randomize` with `--seed` reproduces order-d
/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/r8-gtest-primer-independence.md:4:ground: F3 — determinism precondition, flaky-aware verdicts (corpus/README.md F3 frontier row; QUALI
/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/r8-gtest-primer-independence.md:25:- The relation to held rows S013 (Jest `--randomize`/`--seed`) and S025 (order dependency as a flaky-

$ grep -rniE 'cluster|co-occur|false.red|false-red|undetected|same-job|rerun' /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge | cut -c1-200
/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/fleet-suite-census.md:477:  `presweep-independent-1743Z.txt`, formal D2/D9 `formal-rerun-175044Z.txt`,
/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/fleet-kill-rate-ledger.md:436:runner (`.ufo/waves/round-18/w2/RerunC1.md`). Tameshi's own read-only case; it
/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/mutation-score-semantics.md:15:| **Survived** — green + full count (`SKILL.md:205-206`) | **Survived** or **NoCoverage** are both unde
/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/mutation-score-semantics.md:23:For the same valid mutant set, let `k` = killed, `s` = survived (including any NoCoverage mutants for the
/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/mutation-score-semantics.md:44:Recorded sweep commands for the six tallies (quoted from each case note; not rerun for this entry):
/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/witness-scoped-kill-verdict.md:90:`rerun-20261020T035435Z/` agreed on all ten classifications without
/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/repeated-control-precondition.md:102:The other passing checks were not rerun merely to prettify the evidence.
/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/incremental-pin-disposition.md:1:source: S003 — https://stryker-mutator.io/docs/stryker-js/incremental/ — §Incremental mode, §Limi
/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/incremental-pin-disposition.md:43:mode." It reruns "all mutants in scope, regardless of the incremental file."
/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/incremental-pin-disposition.md:94:  dependencies, `.snap` files and non-mutated/non-test files as undetected;
/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/incremental-pin-disposition.md:190:the six legs' tables; this entry adds no leg, reruns none, and revises no rate.
/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/incremental-pin-disposition.md:200:| environment variables | S003: "changes to environment variables" undetected | the pinned blob is on
/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/incremental-pin-disposition.md:201:| (dev) dependencies | S003: "updated (dev) dependencies" undetected | the pinned blob's interpreter
/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/incremental-pin-disposition.md:202:| snapshot files | S003: "changes to `.snap` files" undetected | any golden/snapshot fixture a selfte
/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/incremental-pin-disposition.md:384:`verification.json`. No oracle, target suite or mutation sweep was rerun.
/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/mutation-case-kumitate-round-gate.md:2:verified-at: 2026-10-20; re-run in wave 2 (RerunSweep
/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/mutation-case-kumitate-round-gate.md:124:got identical verdicts and mutant sha256s (RerunSweep). The final runner
/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/mutation-case-kumitate-round-gate.md:144:  single-edit, non-hostile edits, and RerunSweep reproduced every mutant
/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/guard-kill-closure.md:145:  `01d586d` open=0/11 (`c2-probes-v2-e08271a.txt`; w2 RerunC2After, RerunC2Before).
/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/required-command-binding.md:53:undetected corruption of the old pinned contract. Self-consistent forged
/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/mte-report-interop.md:78:- `totalUndetected = survived + noCoverage`;
/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/mte-report-interop.md:79:- `totalValid = totalUndetected + totalDetected`;
/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/regression-tally-completeness.md:27:S087's library code counts the eight named mutant status buckets, passes them to `toMetrics`, and de

$ grep -nE 'F3|F8|F7' /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/README.md | cut -c1-200
80:| F3 | determinism precondition, flaky-aware verdicts | S004, S011, S025, S026, S027, S040 | open | one control per sweep (`.ufo/evidence/kaika-round-1/capability-demo/README.md` H2) → N ≥ 3 by
84:| F7 | incremental re-sweep granularity | S003, S004, S005, S008, S041 | open | pin-level cadence only → per-leg reuse decisions classified |
85:| F8 | oracle anchoring as a survivor class | S012 | open | 0 test-oracle lines → one survivor classified against an independently anchored expectation |
127:| `knowledge/repeated-control-precondition.md` / F3 | A standalone exact-tuple repeated-control gate; a clean result is finite sample agreement, not proof of determinism or a flaky-test cure | S00
130:F3's original next move is the repeated-control capability, not the stronger
138:causality. F3's named finite-sample capability is the claimed advancement,
148:## Round 13 — F7 content disposition and outside-review correction
152:| `knowledge/incremental-pin-disposition.md` / F7 | Structured six-leg pinned/HEAD/worktree content observation and the explicit boundary `result_reuse=not_established`; no target gate runs and no
155:F7 advances from pin-cadence prose to a bounded machine-readable
175:The full F7 per-leg **reuse-decision** frontier remains open; only the
188:This round does not complete whole-F7 verdict reuse, F1 interop, any successor
206:whole-F7 result reuse, F1 interop or a successor mutation sweep. Legacy
234:frontier item moves to Core: the cold-read is calibration evidence, and F8
255:No frontier row moves: F7 stays open (the v2 disposition and the credit rule
271:moves to Core: F3's determinism control is measured for case 8 only
338:or proof of universal hermeticity. F3 universal determinism stays open.
413:No F-row changes. F3 stays open (one control per sweep). F1 stays held and
418:## Round 27 — frontier F8, oracle-anchored survivor classification
422:| `knowledge/oracle-anchored-survivors.md` / F8 | source-headed entry citing S012 (re-opened and mined this round) and S090, S091 (new); the four round-26 cite-check hole survivors re-judged again
424:F8 moves from open to **partly held**: its next move (one survivor
427:pristine-differential until anchored. Line 85's F8 row reads "open"; this
431:## Round 29 — F8 wording correction, F6 pre-registration
433:F8 correction (round-27 spot-check routed item 4): the round-27 section
434:above says the round-27 next move "is measured" against "an independently
437:F8 stays partly held on that bound.
558:## Round 45 — GoogleTest test-order and fixture-lifecycle ground (F3); held-row live re-verification

$ grep -nE '2504.16777|googleblog|fis.tum|TSE.2026|flaky' /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md | cut -c1-220
36:| S025 | An Empirical Analysis of Flaky Tests (Luo, Hariri, Eloussi, Marinov; FSE 2014) — https://mir.cs.illinois.edu/marinov/publications/LuoETAL14FlakyTestsAnalysis.pdf | paper | A | flaky test root causes and fix
37:| S026 | Flaky Tests at Google and How We Mitigate Them (John Micco, Google Testing Blog, 2016) — https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html | docs | A | Google's flakiness rates an
38:| S027 | A Systematic Evaluation of Environmental Flakiness in JavaScript Tests (Hashemi, Tahir, Shi, Rasheed, Blagojevic; arXiv 2602.19098) — https://arxiv.org/abs/2602.19098 | paper | A | environmental flakiness r
49:| S040 | A Survey of Flaky Tests (Parry, Hilton, Kapfhammer, McMinn; TOSEM 2021) — https://o-parry.github.io/papers/2021a.pdf (DOI 10.1145/3476105) | paper | B | F3 — flaky-test definitions and the determinism ass
269:- *230,439 Test Failures Later: flaky failure classifiers* — https://arxiv.org/abs/2401.15788.
```

No tools installed. No lane files changed except this report; scratch directory: `/tmp/tameshi-r46-ScoutHeldSweep/`.
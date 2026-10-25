seat: RevProvince
item: per-entry PROVINCE.md + QUALITY.md gate for the three round-46 package entries (r6-flaky-failures-cluster, r5-undetected-flaky-failures, r9-false-red-rate), quote-vs-snapshot verification, inference-as-observation flags, F8 ground-tag ruling, and the craft-vs-generic-SE decision.

## Bounds compliance

- Read-only on the lane except this report; read-only on /home/vgpnk/Projects/shokuknow (no writes, no fetch, no campaign tool there).
- Scratch: /tmp/tameshi-r46-RevProvince/ (extracted snapshot texts arxiv.txt / tum.txt / feed.txt, quote spans quotes.json, blog-extracted.txt).
- No counters run (my item is the gate, not a measurement); no pacman, no tool installed or updated (nothing needed beyond repo python3).

## Verdicts

| entry | staged -> adopted id | verdict | deciding PROVINCE line | deciding QUALITY criteria |
|---|---|---|---|---|
| r6-flaky-failures-cluster.md | S195 -> S258 | ADMIT with 2 conditions | PROVINCE.md:3-5 (domain: verification-fixture craft) + :40-42 (Frontier F1-F10; ground moves to Core through an admitted, source-headed knowledge/ entry) | 2 (anchor: both quotes located in committed snapshot), 3 (body labels Inference), 10 (source/verified-at/recheck header; row opened this round per adoption-map.json) |
| r5-undetected-flaky-failures.md | S190 -> S259 | ADMIT with 2 conditions | PROVINCE.md:3-5 + :40-42 (F3 README:80, F5 README:82) | 2 (all 5 quotes located), 3, 10, 11 (repeated-control discipline — the entry's fresh-environment rerun requirement strengthens it) |
| r9-false-red-rate.md | S212/S216 -> S260 | ADMIT, conditional on re-grounding | PROVINCE.md:3-5 + :40-42 (F7 README:84 — the false-red rate a re-sweep cadence is priced against) | 2 (all 3 quotes located in the committed feed snapshot), 3, 10, 34 (current header cites a foreign store — see flag 3) |

Rejects: **none** — no entry met the refuse bar (all 10 quoted sentences located in the committed snapshots; every entry scopes its numbers honestly in a boundary section). Per the item, a reject is recorded only on failure; instead each admission carries flip conditions (below).

## Quote verification (mandated check: `grep -cF` after `--extract` normalization)

Snapshots (sha256sum):
- `28d2954d22ea45af7bd0454f1a8b01bb5db40e8e5cc235eed176a1621aa26a14  coverage/sources/arxiv-2504.16777-abs.html`
- `5eb59adf099304a07059530b0857f7b517eaa72c832049f46952915a77e71a6f  coverage/sources/tum-portal-flaky-failures.html`
- `434d86586ecf3ea03f57d4342c6e8575576eef6a9fd452a5c0a9e67bd8889929  coverage/sources/google-flaky-feed-6277555988217606236.json`

Normalization: `python3 .ufo/evidence/round-45/freshness/measure.py --extract <snapshot>` (NFKC fold, curly quotes->straight, dashes->hyphen, tag strip, whitespace collapse). Quote strings folded identically, `**` stripped (entry formatting, not source text). Counts (`grep -cF -f q.tmp <extracted>`; each snapshot folds to one line, so 1 = present):

| quote | snapshot | count |
|---|---|---|
| r6 "finding that 75% of flaky tests across all projects belong to a cluster, with a mean cluster size of 13.5 flaky tests" | arxiv | 1 |
| r6 "challenging the deep-seated assumption that flaky test failures are isolated occurrences" | arxiv | 1 |
| r5 "We analyzed 8.8 billion test executions … over two-month periods." | tum | 1 |
| r5 "All apparently deterministic failures were systematically validated through reruns in fresh environments …" | tum | 1 |
| r5 "We found that, across all projects, undetected flaky failures account for 9.8 %-16.3 % of failed pipeline runs." | tum | 1 |
| r5 "These flaky failure rates spike temporarily, triggered primarily by code changes and test reordering." | tum | 1 |
| r5 "Additionally, test environments significantly influence flakiness, with up to 3× variation in flake rates between them." | tum | 1 |
| r9 "about 84% of the transitions we observe from pass to fail involve a flaky test" | feed | 1 |
| r9 "If 1.5% of test results are flaky, 15 tests will likely fail" | feed | 1 |
| r9 "It is quite common to ignore legitimate failures in flaky tests due to the high number of false-positives" | feed | 1 |

**Mandatory re-grounding fix (r5):** with the entry's `**` bold markers kept inside the quotation marks, the same `grep -cF` counts are **0** for the three marked r5 quotes. The coverage counter's located-quote check (`coverage/measure.py:142-143`, `quote in rows[c]['text']` after fold, no asterisk removal) will reject them. Flip condition: strip `**` from inside quoted spans (or move emphasis outside the quotes) in the re-grounded entries, else the entries fail `no located quote`.

## Inference presented as observation — flags

1. **r6, the S140 sentence (QUALITY 2, concrete defect).** "(S140, round 5: the same-job rerun misses 9.8 %–16.3 % of flaky failures in the first place)" — (a) no S140 row exists in the round-46 staged append (`grep -n 'S140' merge/tameshi/SOURCES.append.md` → no match) nor in lane `corpus/SOURCES.md`; (b) S140 is a retired shokuknow round-4 id (`/home/vgpnk/Projects/shokuknow/lanes/tameshi/ID-REMAP.md:84` `| round4 | S140 | S184 |`); (c) the lane's own record refused an S140 row payload-absent (`corpus/lessons/round-40.md:69` "absent — the quoted span and the row's recheck output are in no cited source. Refuse"); (d) the figures verifiably belong to S190 (`SOURCES.append.md:44`), whose snapshot carries them (count 1 above) — and S190's denominator is **failed pipeline runs**, not "of flaky failures", so the paraphrase also shifts the denominator. Flip condition: repoint to S190/S259 with the pipeline-run denominator, or drop the sentence.
2. **r5, "round 1's `S107`" (QUALITY 2, minor misanchor).** Lane S107 is the TensorFlow Federated golden-testing row (`corpus/SOURCES.md:119`, anchor "F4 explicit update flag"); the "one green control" round-1 surface is the kaika-round-1 capability demo (README:80 F3 row). Flip condition: anchor to the F3 row's round-1 surface or drop the parenthetical.
3. **r9 header vs committed carrier (QUALITY 34 + 2).** Line 1 cites the rendered HTML and `lanes/tameshi/round9/evidence/google-flaky-blog-text.txt` — a path in the read-only shokuknow store the lane does not own (the file exists there; `ls` verified). QUALITY 34 (QUALITY.md:251): a citation into a file the lane does not own needs a rev/function anchor; a bare path expires. The staged rows themselves route the quotes through the feed (`SOURCES.append.md:66` S212, `:70` S216). Flip condition: re-grounded entry's line 1 must cite the adopted S260 row (committed feed snapshot); it does not, as packaged. Factual note, non-blocking: S216's rationale ("the rendered page … the checker cannot reach a single one of them") did not reproduce with the round-45 extractor on the round-9 HTML copy — `--extract` on `/home/vgpnk/Projects/shokuknow/lanes/tameshi/round9/evidence/google-flaky-blog.html` (26626 bytes) finds the 84% sentence count 1 (raw count 2; `text/template` present) — but the feed is still the committed, re-checkable carrier and all three sentences locate in it exactly once.
4. **r9, the round-8 cost sentence (QUALITY 2).** "Round 8 priced a rerun at 0.02 cents against a $5.67 manual investigation" has no anchor anywhere in the lane repo (`grep -rn '5\.67'` over the lane → only the package copy itself and unrelated round-32/34 receipts); the figures trace to the shokuknow round-8 dossier (`lanes/tameshi/round8/.deepresearch/20261024_034822_tameshi-r8/final_turn_001.md:41`, backed by staged S207, ICST 2024). Not fabricated — but unanchored for a lane reader. Flip condition: anchor it to an adopted row (e.g. the ICST cost paper, if adopted) or drop/mark it as package history.
5. **r6 header `ground: F8 (oracle anchoring as a survivor class)` (QUALITY 3, form).** The same move is labeled "Inference:" in the body but presented unlabelled as the entry's ground in the header. See F8 ruling below.

## Is the 'F8' ground tag in the r6 entry warranted?

**Not as the primary ground.** F8's row (README:85) is "oracle anchoring as a survivor class — 0 test-oracle lines → one survivor classified against an independently anchored expectation". S195 measures co-occurrence clustering of flaky *CI test failures*; it contains nothing about test oracles, mutant survivors, or anchored expectations. The r6 entry's F8 connection ("survivor sets are not independent observations … record cluster membership") is analogy — the entry itself labels it "Inference:" — and the staged row repeats the stretch ("so a set of flaky or surviving cases is not a set of independent observations", `SOURCES.append.md:49`, where "surviving cases" is the row author's extension, not the paper's measurement). The measured content lands squarely on F3 (README:80, determinism precondition / flaky-aware verdicts — same-job rerun blindness is F3's stated surface), with the 3× environment figure touching F5 (README:82). Recommendation: `ground: F3`, demote the cluster-membership concern to a labeled secondary note (F8 optional, marked as the entry's own inference). Scope note: this is craft-level only — the C3 counter (`coverage/measure.py:124-150`) parses `source:`/`verified-at:`/`recheck:`/quotes/used-by/indexing and never reads `ground:`, so the tag cannot move the C3 verdict.

## Is flaky-failure measurement generic SE material or verification-fixture craft for this lane?

**Craft — in province for all three entries**, because each one's contribution lands on a lane instrument, not on software engineering at large:
- r6/S195 → how a repeated-control or survivor verdict may be *counted* (cluster membership; a green rerun licenses nothing beyond its sample — the discipline QUALITY 11 already states for repeated controls).
- r5/S190 → the *rerun budget / determinism precondition* (validation "through reruns in fresh environments" is exactly the F5 environment-differential protocol applied to verdicts).
- r9/S212+S216 → the *false-red prior* that an F7 re-sweep cadence is priced against (README:84).

The generic-SE residue (Google's triage organization, the authors' CI-mining method, flaky-test remediation as product advice) stays **report, never absorb** per PROVINCE.md:14-16 (product domains; a pattern is claimed general only from two independent lanes) and :20 ("Out of province → report, never absorb"). Adjacency check: none of the three touches engine-specific nondeterminism (PROVINCE.md:44-47, refused to the game lanes) — these are CI/test-level sources.

## Unrun checks

- No counter executed (`measure.py`, `mutate.py`) — my item is the per-entry gate; the C1/C2/C3 deciding runs belong to other seats/the L1.
- The S216 "checker cannot reach the rendered page" claim was tested only against the round-45 freshness extractor on the shokuknow round-9 HTML copy (result above), not against whatever extractor produced the staging-time lint record.
- I did not verify the arXiv/TUM snapshots byte-for-byte against the live web (no fetch); the gate is against the committed snapshots, which is what C3's counter grades.

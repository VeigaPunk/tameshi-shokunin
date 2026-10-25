seat: T46ScoutCorrections
item: corrections sweep of every file the round touched (683eedde..6f2168e0) for superseded wording left standing in sibling files

## Method and bounds

- All reads are of the content revision, not the lane tip. The lane HEAD is `eada0b36` (wave-2 spec commit), one commit past `6f2168e0`, so I extracted the revision with `git archive 6f2168e028ce7ff6e82ac92093ac05dd1f147c32 | tar -x -C /tmp/tameshi-r46-T46ScoutCorrections/t` and grepped there. Line numbers below are those of `6f2168e0`.
- `git diff --name-only 683eedde 6f2168e0 | grep -v '^.ufo/'` prints 10 files: `LOG.md`, `PROVINCE.md`, `SCORECARD.md`, `corpus/QUALITY.md`, `corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/r5-undetected-flaky-failures.md`, `corpus/knowledge/r6-flaky-failures-cluster.md`, `corpus/knowledge/r9-false-red-rate.md`, `corpus/lessons/round-46.md`.
- `git diff --stat` over six of them shows insertions only (192 insertions, 0 deletions), so the base text stands byte-for-byte below each append.
- Not changed by the round, so unedited but still swept: `SKILL.md`, `SHONEN.md`, `README.md`, `AGENTS.md`, `MINT.md`.
- Counters run only as `--selftest`, in `/tmp/tameshi-r46-T46ScoutCorrections/t` (no verdict run):
  - `calibration/measure.py --selftest` → `C1_R46_SELFTEST: cases=18 failed=0`, `VERDICT: PASS`
  - `hardening/mutate.py --selftest` → `C2_R46_SELFTEST: cases=8 failed=0`, `VERDICT: PASS`
  - `coverage/measure.py --selftest` → `C3_R46_SELFTEST: cases=24 failed=0`, `VERDICT: PASS`
  These match LOG.md:2313 (C1 18/18, C2 8/8, C3 24/24) and SCORECARD's round-46 capability rows.
- Unrun: the census (`sources-census.sh`), the three deciding commands, the no-harm script.

## Findings (stale or inconsistent, with correction)

| # | Sev | file:line | Old text | Why stale / still correct | Exact correction to append |
|---|---|---|---|---|---|
| 1 | HIGH | `corpus/SOURCES.md:470` (last line of the file) | `- Next unused id: S258 (the staged-id guard's safe floor after this append; staged ids S161–S255 stay reserved by document for the package).` | The file has no round-46 paragraph (`git diff --stat`: SOURCES.md +3 lines, the three rows only). Rows S258/S259/S260 now exist (`grep -nE '^ {0,3}\| S(258\|259\|260) \|' corpus/SOURCES.md` → lines 133-135), so the last footer line names an id that is taken. The round-45 line is a dated literal and stays; every earlier round appended its own paragraph plus footer (rounds 41-45 at lines 448-470), and the same stale-footer defect was routed in rounds 27 and 30 (`corpus/lessons/round-27-verifier-spotcheck.md:194`, `round-30-verifier-spotcheck.md:215`). | Append after line 470: `Round 46: three rows added, S258 (arXiv 2504.16777), S259 (TUM portal record, TSE 2026) and S260 (testing.googleblog.com per-post feed record), tier A, opened 2026-10-25, adopted by document from the shokuknow merge/tameshi package (staged S195, S190, S216), each pinned to a snapshot under .ufo/evidence/round-46/coverage/sources/. - Census: round start 117 rows exit 0 (.ufo/evidence/round-46/census-start.stdout); round end 120 rows (deciding receipt after/census.stdout). - Next unused id: S265 (the round-46 guard map reserves S261-S264 for staged S155-S158; staged ids S161-S255 stay reserved by document).` The S265 floor is `[INFERENCE]` from `corpus/lessons/round-46.md:70-74`, not from a guard run. |
| 2 | HIGH | `SCORECARD.md:2163` (`**Planned (round 46):**`) | `kill the C1/C2 counter selftest survivors (…) and add a per-snapshot fetch receipt to the freshness ledger (calibration/operability); re-pin the anchor-refresh candidates in .ufo/waves/round-45/w2/ConnDriftAnchors.md (freshness).` | Only the first of three items is answered by the round-46 block (C2 `killed=25 survived=0`, line 2209). `grep -n -i -E 'fetch receipt\|per-snapshot\|ConnDriftAnchors\|anchor-refresh' SCORECARD.md LOG.md PROVINCE.md corpus/lessons/round-46.md corpus/QUALITY.md corpus/README.md` shows the round-46 text never mentions the per-snapshot fetch receipt or the anchor re-pin, and `Planned (round 47)` (line 2228) does not carry them. The Planned line is a dated literal (append-only); the fix is a carry, not an edit. The planned line also names the source audits as the survivor set while the declared set is 25 (15 freshness + 10 coverage) against 12 + 8 + 8 = 28 in LOG.md:2307; the round-45 audits are not reconciled to the manifest (`mutants.json` `declared_from`). | Append to the round-46 block after line 2228: `Round-46 disposition of "Planned (round 46)": item 1 (kill the counter selftest survivors) answered by C2; item 2 (per-snapshot fetch receipt on the freshness ledger) and item 3 (re-pin the anchor-refresh candidates in .ufo/waves/round-45/w2/ConnDriftAnchors.md) were not claimed, frozen or measured this round and carry to round 47; the 28 audited survivors reduce to the 25 declared ones (manifest declared_from; three audited survivors are not declared).` The last clause is unverified against the audits: say it only after someone reconciles 28 vs 25. |
| 3 | LOW | `corpus/lessons/round-46.md:125` | `End: .ufo/evidence/round-46/census-end.stdout (recorded at the content revision).` | No such file exists at `6f2168e0` (`git ls-tree` shows only `census-start.*` under `.ufo/evidence/round-46/`), and no script writes the name: `.ufo/evidence/round-46/deciding-run.sh:31` writes `$OUT/census.stdout` (`after/census.stdout`). The reference will not resolve after the receipts-only commit either. | Append to the lesson: `Erratum: the census end receipt is .ufo/evidence/round-46/after/census.stdout (written by deciding-run.sh line 31); there is no census-end.stdout.` |
| 4 | LOW | `corpus/README.md:80` (frontier table row F3) | `S004, S011, S025, S026, S027, S040 \| open \| …` | Status `open` is consistent with every other F3 mention (below). The candidate-source column was not extended by round 45 (S256, S257) or round 46 (S258-S260), and already omitted S156. The README round-45 and round-46 sections (lines 565, 577) carry the additions, so this is an index lag, not a contradiction. | Append under the table or in the round-46 section: `F3 candidate sources now also S156, S256, S257, S258, S259, S260 (status unchanged: open).` |
| 5 | INFO | `SCORECARD.md:2199` (axes row, calibration, last-change `46 (restated 8 → 6; no raise claimed)`) and `SCORECARD.md:2173` | the restated row says the round-31 table "stated 8" and "8 was a stale standing value" | Correct as written for the standing table. The history it omits: round 41 had already printed `calibration 6 → 6` and called the carried 8 "superseded as an upper bound" (`SCORECARD.md:1923-1926`, `LOG.md:2100`, `LOG.md:2152`), and rounds 42-45 carry 6 (2008, 2044, 2063, 2108, 2143, 2161). Round 46 is the first time a standing table row itself was restated, not the first time the 6 was seen. No wrong number stands. | Optional one-line append to the round-46 restatement: `The monitor has printed 6 since round 41 (SCORECARD.md:1923); round 46 is the first restatement of the standing row itself.` |
| 6 | INFO | `SCORECARD.md:2204-2228` (round-46 "Capabilities demonstrated this round") | three new rows (standing-statement counter, declared-mutant driver, no-harm / seat-name gates) | They are not among the 22 frozen statements and `Planned (round 47)` adds only the five unpinned-tool pins, not these three rows, so the next restatement's frozen list would still be 22 and miss them. Not stale yet; flag for round 47. | none now; if the next claim extends the list, state `22 → 25` explicitly. |

## Sweep results by requested class (no stale mention, or dated literal that stays)

### `calibration 8` / `calibration | 8`

`git grep -n -i -E 'calibration[ |]*8|calibration8' 6f2168e0` over `SCORECARD.md SKILL.md PROVINCE.md SHONEN.md corpus/README.md AGENTS.md README.md MINT.md LOG.md`:

- `SKILL.md`, `PROVINCE.md`, `SHONEN.md`, `corpus/README.md`, `AGENTS.md`, `README.md`, `MINT.md`: **zero hits**. `SKILL.md:426` (`calibration | 9/10 pre-run verdict expectations`) is a different quantity (expectation calibration of the E1 run), not the axis score. `SHONEN.md:6-12` mentions only report paths.
- `LOG.md:1091, 1175, 1295, 1397, 2073`: dated round entries (rounds 15-40) that state 8 at their time; append-only, still correct as dated literals. `LOG.md:2307` is the round-46 entry that quotes the stale 8 on purpose.
- `SCORECARD.md:652, 776, 861, 865, 968, 1029, 1129, 1477, 1532, 1535-1537, 1545, 1557, 1598, 1703, 1796, 1823, 1835, 1855, 1864, 1872, 1891`: dated round blocks, kept as written. The table row at `SCORECARD.md:1537` (`| calibration | 8 |`) is the only one in standing-table form and is superseded explicitly by `SCORECARD.md:2172` (the round-46 section says it supersedes the round-31 axis and capability tables "for every value it states") and by `SCORECARD.md:2199` (`| calibration | 6 |`). `SCORECARD.md:1703` (`calibration 8 → 6`) is the round-35 drop, and `1731` records the later refresh `6 → 8`; both dated.
- `SCORECARD.md:861` and `LOG.md:1091`-style "saturation line 8" sentences are the declared line, not the axis value; the line is unchanged at 8 (contract: "calibration 6 is below the saturation line 8").
- Verdict: no stale `calibration 8` stands outside a dated block that the round-46 restatement supersedes by name.

### `F3` rows saying `open` vs the new entries

- `corpus/README.md:80` (`open`), `corpus/README.md:565` (round 45, "F3 stays `open`"), `corpus/README.md:577` (round 46, "F3 stays `open`"), `PROVINCE.md:126` ("F3 stays `open` in the frontier table"), `corpus/README.md:413, 338` (older "stays open"). All say `open`; none says `held`. Consistent. The only gap is the candidate-source column (finding 4).
- `SCORECARD.md:2208` calls C3 "frontier F3; sourced, assimilation" without claiming a status change. `LOG.md:2310` and `corpus/lessons/round-46.md:8` ground F3 and make no status claim.

### Registry-count sentences

- Actual count at `6f2168e0`: `grep -cE '^ {0,3}\| S[0-9]{3,} \|' corpus/SOURCES.md` → `120`.
- `SCORECARD.md:2176` (round-46 standing row, `rows=120`), `LOG.md` ("rows 117 → 120"): correct.
- `SCORECARD.md:2146, 2164` (`115` at round 44, `117` at round 45), `SCORECARD.md:2028, 2090, 2134` (`sources_rows=113/114/115` in dated receipts), `LOG.md:2202, 2248, 2267`, `corpus/SOURCES.md:461, 466`, `corpus/lessons/round-43*.md`, `round-44*.md`, `round-45.md:168`, `round-46.md:124` (`117 rows` at round start): each correct at its own date; leave.
- `SKILL.md`, `PROVINCE.md`, `SHONEN.md`, `README.md`, `AGENTS.md`, `MINT.md`, `corpus/README.md`: no registry-count sentence found (`git grep -n -E '\b(11[0-9]|120|121) (rows|ids)|rows=1[12][0-9]|(115|116|117|118|119)[ -]row'` over them → no hits). Only the footer in finding 1 is stale.

### `Planned (round 46)` in `SCORECARD.md`

See finding 2. It sits at `SCORECARD.md:2163`, last line of the round-45 block. Answered by the round-46 block: item 1 only.

### Stale "capability" counts

- The restated table `SCORECARD.md:2176-2196` has 19 capability rows (counted: 20 table lines in the slice including the header), equal to the contract's "19 capability rows" plus 3 axis rows = 22 statements. No sentence anywhere states a different total.
- `LOG.md:1397` ("no new capability-table entry since round15") and `SCORECARD.md:1796` ("no capability added in rounds 35–36") are dated.
- Finding 6 is the only forward-looking count risk.

### `PROVINCE.md` Core appends

- A round-46 append exists (`PROVINCE.md:119-135`, header `## Core — round 46 append (2026-10-25)`, "Appended; lines above are unchanged"; diff is +17 lines, no deletions). It names S258/S259/S260 and the three entries, says F3 stays `open`, names the counter and hardening paths, and says the recorded mutation legs stay nine and no sibling gate is added.
- All three entry basenames it cites exist and are named identically in `corpus/README.md:573-575`.
- Nothing in the append contradicts an older Core paragraph. The round-26 correction ("line 101 reads nine") is untouched and still correct.
- `SHONEN.md` box 4 ("PROVINCE.md still accurate") is an unchanged `[~]` lane assertion; I found no cross-domain bleed in the append (it states that flaky-test engineering "stays adjacent (report, never absorb)"), and no mark change is needed.

## Spot checks that held

- `corpus/README.md:573-575` figures against the committed snapshots under `.ufo/evidence/round-46/coverage/sources/`: `810 flaky tests` (arxiv abstract), `8.8 billion test executions from four industry-scale projects` and `up to 3× variation` (TUM record), `legitimate failure` wording and `published 2016-05-27` (Google feed JSON) are all present. `README.md:573` writes "75% of 810 flaky tests"; the abstract says 75% of flaky tests across all projects belong to a cluster and that the dataset contains 810, so the phrase is a compression, not a false figure (INFO).
- `LOG.md:2313` selftest counts match the selftests I ran (above).

## Unreproduced / not attacked

- I did not run the census, the deciding commands or the wave-1 counters against the revision, so no census exit, `C1_R46_PASS`, `C2_R46_PASS` or `C3_R46_PASS` is reported by this seat.
- I did not reconcile 28 audited survivors against 25 declared (finding 2 states the gap; the manifest group lists 18 freshness + 13 coverage entries including the 6 neutrals and 25 declared mutants).

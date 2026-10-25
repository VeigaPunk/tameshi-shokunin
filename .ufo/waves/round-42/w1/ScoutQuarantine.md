# ScoutQuarantine — round 42 wave 1 findings

Access date: 2026-10-25. Lane: tameshi-shokunin (read-only seat; no lane edits made).

## 1. Re-derivation of the tameshi slice matches the quarantine slice file (17 lines, identical)

Command:

```
awk -F'|' -v l=tameshi '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
```

Output (17 rows): S105, S109, S110, S118, S119, S124, S126, S129, S131, S132, S137, S140, S141, S143 (all class `payload-absent`), then S113, S123, S134 (class `the cited source could not be fetched, so no quote was checked`).

This is byte-identical, row-for-row and in the same order, to `tameshi-shokunin/.ufo/waves/round-42/assimilation/quarantine-slice` (17 lines; snapshot `[quarantine-slice#3CDE]`). No slice id is missing from the re-derivation; the file and the re-derivation agree exactly.

## 2. All 17 slice ids have a verdict in the round-40 Quarantine table — none missing

Source: `tameshi-shokunin/corpus/lessons/round-40.md`, `### Quarantine — 17 data rows, one verdict each` at line 49; table at lines 53–71. Every one of the 17 slice ids appears exactly once with a verdict:

| id | verdict (round-40.md table) |
|---|---|
| S105 | present — register verdict is a whitespace-fold false positive; adopt-eligible, not appended (line 55) |
| S109 | absent — linter's ABSENT mechanically correct; Refuse (line 56) |
| S110 | present, verbatim; adopt-eligible, not appended (line 57) |
| S113 | present — DOI resolves, quote verbatim in author camera-ready PDF §3.2; prose class stale; adopt-eligible, not appended (line 58) |
| S118 | misbound — quoted span is a parenthetical provenance note, not page content; not fabrication; not appended (line 59) |
| S119 | present, verbatim (locator off by one); adopt-eligible, not appended (line 60) |
| S123 | present — URL answers 202; figures verbatim in the arXiv carrier pinned as S193; prose class stale; adopt-eligible, not appended (line 61) |
| S124 | present — quoted line in cited source; adopt-eligible, not appended (line 62) |
| S126 | present — quoted span in cited source; adopt-eligible, not appended (line 63) |
| S129 | present — flagged token is a code token from provenance note; two real gate quotes verify; adopt-eligible, not appended (line 64) |
| S131 | refuse as pinned — pinned locator times out from this host; unreachable, not fabricated; covered by S105; not appended (line 65) |
| S132 | present — raw README row D29 carries title; **Adopted** (line 66) |
| S134 | present — DOI opens through campaign's own `aaron` channel; quote locatable; prose class stale; adopt-eligible, not appended (line 67) |
| S137 | absent — flip from round 39 unmet at `31687496`; Refuse (line 68) |
| S140 | absent — quoted span and recheck output in no cited source; Refuse (line 69) |
| S141 | absent — commit `31687496` carries no 86-site census; Refuse (line 70) |
| S143 | absent — source live but quote in none of it; Refuse (line 71) |

Summary line 73: one adopted, seven refused, nine present-but-not-appended; no row called a fabrication. No slice id is without a verdict.

## 3. No slice id is cited by the theme candidates (staged:S159, staged:S160, staged:S163–S166)

Theme candidates = the six staged knowledge pages and their SOURCES rows in `/home/vgpnk/Projects/shokuknow/merge/tameshi/`:
`knowledge/corpus/knowledge/pit-outcome-vocabulary.md` (S159), `flaky-aware-verdict-evidence.md` (S160), `mutation-score-semantics-cjk.md` (S163/S164/S165), `llm-mutant-equivalence-cost.md` (S165), `survivor-classification.md` (S166), `pbt-generator-as-fixture.md` (S166); plus `SOURCES.append.md` rows at lines 13 (S159), 14 (S160), 17–20 (S163–S166).

- `grep -rnE 'S(105|109|110|113|118|119|123|124|126|129|131|132|134|137|140|141|143)\b'` over the six theme-candidate knowledge pages: **0 matches in every one of them**.
- The theme candidates' `SOURCES.append.md` rows cite no slice id (their source/used-by cells name URLs, sections, and knowledge file paths only — e.g. line 13's used-by is `corpus/knowledge/pit-outcome-vocabulary.md, corpus/knowledge/r13-f7-cadence-and-floor.md`).
- The only slice-id occurrences anywhere in the assimilation package are in non-candidate artifacts:
  - old adopted/parked knowledge pages: r3-cjk-test-suite-effectiveness.md:24 (`S118`), :50 (`S113`); r6-flaky-failures-cluster.md:29 (`S140`); r7-snapshot-practice-published-study.md:37,53 (`S126`); r11-carrier-audit-corpus-wide.md:23,47 (`S141`); r11-write-site-quote-paraphrase.md:14,49,61 (`S141`); r12-write-site-census-reproduces.md:15 (`S141`); r13-recheck-carrier-fix.md:18,35 (`S119`); r14-landing-kit.md:24 (`S119`); japanese-flaky-verdict-and-environment.md:12,19,22 (`S123`); amendments/corpus/knowledge/r6-snapshot-practice-corpus.md:14 (`S126`);
  - MERGE-REPORT.md:120 (`S153` row cites `S105` as the lane-held duplicate row — collision row, not a theme candidate);
  - SOURCES.append.md:78 (S224 row cites `S141` as the carrier that re-checks it), :91 (S237 row) — neither is a theme candidate.

Conclusion: none of the 17 slice ids is cited by any theme candidate (staged:S159/S160/S163–S166).

## What I could not check

- I did not run the round-42 counters (out of scope for this scout question).
- The verdict *correctness* of the round-40 table is not re-audited here; I only verified presence of one verdict per slice id.
- No tools installed; no repo edits made.

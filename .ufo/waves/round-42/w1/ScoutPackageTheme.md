# ScoutPackageTheme — round 42 wave 1: assimilation-package inventory (mutant outcome vocabulary)

Scout: L1Tameshi42.ScoutPackageTheme — 2026-10-25. Read-only; no lane edits,
no tool installs (tooling directive: nothing was installed).

## 1. Inventory command (exact)

```
cd /home/vgpnk/Projects/shokuknow/merge/tameshi
grep -ril "killed\|run error\|runtime\|denominator\|outcome" \
  knowledge/corpus/knowledge/ amendments/corpus/knowledge/ | sort
```

Result: **31 knowledge entries + 1 amendment** match. Amendment match:
`amendments/corpus/knowledge/golden-comparison-verdict.md` (only match in amendments/).
All 31 knowledge files plus the one amendment are listed in §2.

Keyword-per-file counts were produced with
`grep -oE "killed|run error|runtime|denominator|outcome|kills?|killed_on_witness|k_witness|survivor|survived" <file> | sort | uniq -c`.
Relevance tag: `central` = body/title actually concerns outcome classes / kill
semantics / score denominators; `incidental` = matched only via "runtime"/"outcome"
in an unrelated sense (host trash runtime, run cost, agent-eval outcome wording).

## 2. Inventory (source ids, lane-held-by-URL, frontier status)

Lane registry: `corpus/SOURCES.md` holds 109 rows S001–S154; `Next unused id: S155`
(SOURCES.md:440). URL-hold check: for each entry's `source:` URLs, grep the URL in
`/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md`; a lane row id in
the right column means the lane already holds that URL under that row.

| Entry (knowledge/corpus/knowledge/) | sources | URL held by lane row | ground (README frontier) | relevance |
|---|---|---|---|---|
| pit-outcome-vocabulary.md | S159 (PIT basic_concepts), S160 (PIT faq) | NONE, NONE | F1 (partly held) | central |
| mutation-score-semantics-cjk.md | S164, S163, S165 | NONE ×3 | F1 (partly held) | central |
| survivor-classification.md | S166 (zenn j-six-mutation-testing), S156 (arXiv 2406.09843) | NONE, NONE | F8 (open) | central |
| cjk-mutation-metric-and-tool-comparison.md | S168 (jos.org.cn 7113) | NONE | F1 (+F9) | central |
| r3-cjk-test-suite-effectiveness.md | S181 (jos.org.cn 6953) | NONE | F1 (+F8) | central |
| r9-mte-schema-vocabulary.md | S211 (stryker report-schema master) | **S002** (same URL) | F1 | central |
| llm-mutant-equivalence-cost.md | S156 (arXiv 2406.09843), S165 | NONE, NONE | F9 (open) | central |
| flaky-aware-verdict-evidence.md | S155, S158, S160 | NONE ×3 | F3 (open) | central |
| r7-ieice-mutant-abstraction-authority.md | S197 (web.archive IEICE TR) | NONE | F6 (+F2,F8) | central |
| r10-witness-scope-counted.md | S218 (own-work repo URL) | NONE (own-work, no row) | F2 + F7 | central |
| mte-report-interop-measured.md | S174 (own-work repo URL) | NONE (own-work, no row) | F1 | central (F1 interop) |
| r9-false-red-rate.md | S212 (google testing blog page) | **S026** (same URL) | F7 | incidental (denominator ×1) |
| r11-f1-blocker-third-round.md | S222 (own-work) | NONE | F1 + F3 | incidental |
| r12-f1-blocker-mechanism.md | S227 (own-work) | NONE | F1 + F3 | incidental |
| r12-flaky-mitigation-and-quarantine.md | S229 (feed URL) | NONE (S026 is the rendered page, not the feed) | F7 + F3 | incidental |
| r13-trash-refusal-root-cause.md | S230 (own-work) | NONE | F1 | incidental ("host trash runtime" ×14) |
| r14-landing-kit.md | S247 (own-work) | NONE | F5 | incidental |
| r15-landing-kit-dry-run.md | S250 (lanes/…f3-kit-dryrun.txt own-work) | NONE | F1 | incidental |
| r16-process-level-agent-evaluation-in-japanese.md | S254 (alphaxiv ja) | NONE | F3 | incidental (outcome wording) |
| r16-step-level-verification-in-english.md | S255 (arXiv 2603.14465) | NONE | F3 | incidental (outcome wording) |
| r16-trajectory-evaluation-in-the-chinese-tradition.md | S253 (yeasy.gitbook.io) | NONE | F3 | incidental |
| r3-fleet-regression-leg-ledger.md | S179 (own-work) | NONE | F1 | incidental (kill-rate ledger) |
| r4-f1-control-red-mechanism.md | S187 (own-work) | NONE | F1 | incidental |
| r5-f1-control-instability.md | S191 (own-work) | NONE | F1 + F3 | incidental |
| r6-f1-control-teardown-mechanism.md | S194 (own-work) | NONE | F1 + F3 | incidental |
| r7-snapshot-practice-published-study.md | S198 (web.archive JSS) | NONE (lane has DOI lead only) | F4 | incidental |
| r8-predictive-test-selection-cost.md | S205 (arXiv 1810.05286) | NONE | F7 | incidental |
| r8-width-sweep-and-race.md | S208 (own-work) | NONE | F5 + F3 | incidental |
| r9-f1-blocker-is-the-host-shim.md | S213 (own-work) | NONE | F1 + F3 | incidental |
| pbt-generator-as-fixture.md | S157 (doi joss.01891), S166 | NONE, NONE | F10 | incidental (killed/survived in PBT context) |
| pbt-generator-craft-author.md | S170 (tufts quviq) | NONE | F10 | incidental |
| amendments/corpus/knowledge/golden-comparison-verdict.md | S153 (POSIX diff), S154 (google/golden) | **S105**, **S106** (same URLs) | F4 (+F5) | incidental (golden outcomes, not mutant) |

Notes:
- **Collision hazard (already known):** package `S153`/`S154` ids collide with lane
  S153/S154 (lane S153 = CPython ast, lane S154 = pathlib; SOURCES.md:437). The
  package's S153/S154 **URLs are already held by the lane under S105/S106** — so if
  this amendment is adopted, it should cite the lane's S105/S106, not renumber onto
  the collision.
- Two cited URLs exist as lane **leads (unopened)**, not rows: arXiv 2406.09843
  (leads list, SOURCES.md:254) and doi:10.21105/joss.01891 (SOURCES.md:253).
- `github.com/VeigaPunk/tameshi-shokunin` own-work citations (S174, S218, S222,
  S227, S230, S247, S250, S179, S187, S191, S194, S208, S213 …) are not registry
  rows; the lane's own-work rows (S031, S050, S051, S082–S085 …) cite tool paths,
  not the bare repo URL.

## 3. Frontier status used above (README.md `## Frontier`, + status-correction block)

- F1 "external mutation-score semantics + report interop": **partly held**
  (README.md:111–114 — score semantics + six-case recomputation admitted; report
  interop not held, NoCoverage candidates stay U; round 12/13/15 blocks keep F1
  partly held).
- F2: partly held (README.md:115–118). F3–F10: open (README.md:76–87), with the
  round-12 F3/round-13 F7 updates (README.md:123–178).

## 4. Ranked best-fit entries for theme "mutant outcome vocabulary — which outcomes count as a kill"

1. **pit-outcome-vocabulary.md** — exact theme: enumerates PIT's outcome classes
   (§Killed, §Survived, §No coverage, §Non viable, §Timed out, §Memory error,
   §Run error; S159) plus FAQ timeout/static-initializer instability (S160);
   headline "A mutation score's denominator is a choice of outcome class, and one
   of those classes is not stable across runs". Sources S159/S160 not held by URL.
   Ground F1 (partly held). Contract-staged: S155/S156.
2. **mutation-score-semantics-cjk.md** — score denominators: "The mutation score
   excludes equivalent mutants from the denominator — and the Chinese-language
   literature says so explicitly" (S164 进化变异测试 slides; S163 Huawei Cloud
   用例通过率 report rows; S165 deck). Sources not held. Ground F1 (partly held).
3. **survivor-classification.md** — kill semantics from the survivor side:
   "A surviving mutant is a candidate hole; it becomes a hole only after it is
   classified" (S166 Zenn 生存ミュータント practical numbers; S156 arXiv
   2406.09843 equivalence). Sources not held. Ground F8 (open).

Runner-ups verified but not selected: `r9-mte-schema-vocabulary.md` (status-enum
vocabulary, URL already held as S002 — lowest new-ground value), `llm-mutant-equivalence-cost.md`
(F9 open, but equivalence-cost is adjacent, not outcome classes), `cjk-mutation-metric-and-tool-comparison.md`
(per-tool denominator numbers, F1 already partly held).

## 5. Not checked

- Lane self-assessment counters (C1/C2) not run (scout read-only seat; the one
  deciding run belongs to the L1).
- Package `MERGE-REPORT.json/.md` contents were not used as evidence; this report
  is built from the entry files themselves and the lane corpus.
- No fetches were made: source quotes and URLs are read from the package files
  (their own `source:` headers) as-is.

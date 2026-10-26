# T50ConnSiblingShrink — sibling-overlap scan for C2 (F6 fixture shrinker)

Seat: T50ConnSiblingShrink. Scope: read-only scan of fleet lanes
`/home/vgpnk/Projects/shokunin/*-shokunin/` for test-case reduction / delta
debugging / shrinking / minimization ground, and for SOURCES rows of Zeller &
Hildebrandt TSE 2002 (10.1109/32.988498), MacIver & Donaldson 2020, and the
Fuzzing Book reducer. Verdict on whether F6 is tameshi ground by PROVINCE.md.

## Method (commands that show each finding)

- `grep` (pattern `Zeller|Hildebrandt|MacIver|Donaldson|fuzzingbook|Fuzzing [Bb]ook|Shrink|ddmin|delta|reduc|minimiz|isolat`)
  over all 21 `*-shokunin/corpus/SOURCES.md` (two passes; loose and strict).
- `glob` over `*-shokunin/tools|scripts|census` and
  `*-shokunin/corpus/knowledge/*{minim,shrink,delta,reduc,ddmin}*`.
- `read` of every lane's `PROVINCE.md` (pattern
  `shrink|ddmin|delta[- ]debug|minimiz|reduc|reducer`).

## Findings

### 1. No sibling lane holds test-case reduction / delta-debugging / shrinking / minimization ground

Sibling SOURCES.md rows that match the vocabulary are all a different object
(report, never absorb):

| Lane | File:line | Match | Why it is NOT test-case reduction |
|---|---|---|---|
| kama | `corpus/SOURCES.md:118-122,142-146` (S106–S110, S130–S134) | "Context reduction", "fit reduces it", "context-reduction sentinel" | llama.cpp KV-context / memory sizing at runtime; the minimized object is server memory, not a test case |
| souji | `corpus/SOURCES.md:53` (S030), `:55` (S032) | "How to Reduce Git Repository Size Safely", `git-filter-branch` | repository-hygiene rows, both REJECTED; no test-input reduction |
| mori | `corpus/SOURCES.md:55-62` (S050–S055), `corpus/knowledge/evidence-minimization-r18.md`, `PROVINCE.md:126-128`, `tools/mori-content-review.py:18` | "minimization", DECISIONS `minimized` | log/privacy data minimization (retention/redaction); not test-case reduction |
| tsukuroi | `corpus/SOURCES.md:166-167` (S160–S161), `:97` (S091) | "reducing allocated-but-unused chunks", `paccache` cleanup | btrfs balance / package-cache maintenance |
| kake | `scripts/probe-delta.mjs:1-2`, `corpus/knowledge/probe-delta-alerting.md` | "violated[]-delta + probe-coverage detector" | delta between consecutive website-probe sweeps (change detection), not delta debugging; no minimality claim |
| tabi | `corpus/SOURCES.md:131,138` (S116, S125) | "delta reset", "traverseHistory steps by delta" | rate-limit header fields / BiDi traversal vocabulary |
| kotodama | `corpus/SOURCES.md:318,395` (S288, S366) | "reduction of Geryon…", "post-1910 reduction of the kingship" | historical prose, unrelated |
| kasegi | `corpus/knowledge/cisa-bod-20-01-vdp-minimums.md` | "minimums" | VDP disclosure-minimum policy, unrelated |
| kaidoku | (cited via tabi `corpus/adjacency-screen-browser.tsv:69`) | "vacuuming shrinks the window" | crash-core retention scheduling phrase, unrelated |

Tool-name glob across all lanes found no `shrink|reduce|minim|ddmin|delta`
tools/scripts in any sibling lane beyond kake's `probe-delta.mjs` above.

### 2. SOURCES rows for the three named sources exist ONLY in tameshi

- `tameshi-shokunin/corpus/SOURCES.md:33` — **S022** MacIver & Donaldson
  ECOOP 2020, *Test-Case Reduction via Test-Case Generation* (DOI
  10.4230/LIPIcs.ECOOP.2020.13); queued.
- `tameshi-shokunin/corpus/SOURCES.md:34` — **S023** Shrink Ray README
  (DRMacIver/shrinkray); queued.
- `tameshi-shokunin/corpus/SOURCES.md:35` — **S024** *Reducing
  Failure-Inducing Inputs* (The Fuzzing Book, Zeller et al. — the Fuzzing
  Book reducer); mined, used-by `corpus/knowledge/survivor-fixture-minimization.md`.
- `tameshi-shokunin/corpus/SOURCES.md:151` — the lane's "Reduction and
  generation of fixtures" learning chain (S024 → S022 → S023 → …).
- `tameshi-shokunin/corpus/SOURCES.md:184-186` — search-log record that
  Zeller & Hildebrandt TSE 2002 (F6) stayed a lead (author PDFs timed out,
  DOI resolver metadata only).
- **Staged S167** = Zeller & Hildebrandt, *Simplifying and Isolating
  Failure-Inducing Input* (IEEE TSE 28(2):183-200, DOI 10.1109/32.988498):
  `merge/tameshi/SOURCES.append.md:21` (status mined, opened 2026-10-23 from
  a university course mirror), used by the assimilation-theme entry
  `merge/tameshi/knowledge/corpus/knowledge/delta-debugging-minimization-contract.md:2,5,7`
  (ground F6; 1-minimality witness + cost in runs). No sibling lane's
  SOURCES.md has any row for any of the three sources.

### 3. F6 is tameshi ground by PROVINCE.md

- `tameshi-shokunin/PROVINCE.md:40-42` — "Frontier — F1–F10 in
  `corpus/README.md` `## Frontier`"; ground moves to Core only through an
  admitted, source-headed `knowledge/` entry whose `source:` cites a `mined`
  `SOURCES.md` row.
- `tameshi-shokunin/corpus/README.md:83` — F6 row: "fixture minimization for
  survivors | S022, S023, S024 | open | B5 probe fixture size: unmeasured →
  reduced size + kill check".
- `tameshi-shokunin/PROVINCE.md:20` — "Out of province → report, never
  absorb". The lane owns the method and its own corpus/gates; C2's
  `tools/shrink-case.py` is a tameshi-frontier deliverable under this
  registry, with no sibling claiming the same ground.
- Prior in-lane history: `corpus/knowledge/survivor-fixture-minimization.md`
  (round 29 F6 attempt: B5 probe stayed open; ddmin made 171 oracle tests and
  kept nothing; F6 stayed open).

## Contested scope

No contested scope: no sibling asserts reduction/minimization ground. The
adjacent-but-distinct domains above (mori data minimization, souji git size
reduction, kama runtime context reduction, kake probe-delta alerting,
tsukuroi minimal-failing-command evidence standard, kasegi VDP minimums) are
reported, never absorbed. Within tameshi, the round-50 C2 claim (shrink-case
shrinker + F6 held) is a new capability on the lane's own registered frontier;
the staged S167 row is the F6 source-headed admission input.

## Summary

- No fleet lane other than tameshi holds test-case reduction/delta-debugging/
  shrinking/minimization ground; all near-miss vocabulary matches are other
  domains (llama context sizing, git repo hygiene, log-data minimization,
  probe change-detection, policy minimums).
- The three named sources have SOURCES rows only in tameshi: S022 (MacIver &
  Donaldson ECOOP 2020), S023 (Shrink Ray), S024 (Fuzzing Book reducer);
  Zeller & Hildebrandt TSE 2002 is staged as S167 in `merge/tameshi/SOURCES.append.md:21`.
- F6 is tameshi ground per PROVINCE.md:40-42 + corpus/README.md:83; the C2
  shrinker is an in-lane frontier deliverable; no sibling overlap or
  contested scope found.
- Confirmed by grep over all 21 lane SOURCES.md (two passes), glob of
  tools/scripts/census/knowledge names, and PROVINCE.md reads; commands
  listed per finding above.

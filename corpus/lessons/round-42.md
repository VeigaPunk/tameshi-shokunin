# Round 42 lesson

author: tameshi L1 (hyaku run 6, attempt 1)
date: 2026-10-25

## Gate

Theme (assimilation, addendum §10): **mutant outcome vocabulary — which outcomes count as
a kill**, from `/home/vgpnk/Projects/shokuknow/merge/tameshi/` (read only; no campaign tool
run). One entry admitted, one refused, one left unadopted with positive gate verdicts. Every
source below was opened by this lane on 2026-10-25 and pinned to a committed snapshot under
`.ufo/evidence/round-42/sources/`; the snapshot digests reproduced across four independent
wave-1 fetches (`.ufo/waves/round-42/w1/ScoutPitConcepts.md`, `ScribeRows.md`,
`ReviewPitEntry.md`, `CriticOracleSource.md`) and the L1's own fetch
(`.ufo/evidence/round-42/sources/sha256.txt`).

### Admit — `corpus/knowledge/pit-outcome-vocabulary.md` (S155, S156, S158; S001 held)

- S155 — https://pitest.org/quickstart/basic_concepts/ — title "Basic concepts", 12155 B,
  sha256 `c51d8423f5a75e00c7039463f8a5992ef8f1f92b994d69f67d212ff7bfd92b3a`. Located quotes:
  §Running the tests, line 175, "Killed means a test caught the mutation successfully."
  (8 words); line 192, "A run error means something went wrong when trying to test the
  mutation." (13 words); line 179, the No coverage sentence (23 words).
- S156 — https://pitest.org/faq/ — title "FAQ", 20845 B, sha256
  `ccf6ac493d6935e2f0a90b716254c57024973d5e2bf1bf3c1e8e60b9772629c1`. §Is it random?, line
  293, "Pitest works hard to be fully deterministic, but two factors might cause the
  results to differ slightly between two runs with the same input." (24 words).
- S158 — PIT `DetectionStatus.java` at upstream commit `f7fe5adf` (resolved with
  `git ls-remote https://github.com/hcoles/pitest refs/heads/master`; the pinned raw file is
  byte-identical to master at fetch time), 2988 B, sha256
  `3bf295ad53126560ec284c42b384fc3288f7b2e674da987f38d7380ec5d419c6`. Line 63: `RUN_ERROR(true),`
  — the boolean is the `detected` field (line 78) returned by `isDetected()` (line 108).
  New row, not from the package: a wave-1 critic found it while attacking the round's oracle
  citation (`.ufo/waves/round-42/w1/CriticOracleSource.md`).
- S001 (held) re-opened: 27068 B, sha256
  `ac2733869c64ac637a6beb6f2b315d46ca1afaa585eb5322c1a76be18698fc11`; line 26, "It is not
  represented in your mutation score." (8 words), under Runtime error.
- Edits made to the staged text before admission, from `.ufo/waves/round-42/w1/ReviewPitEntry.md`.
  E1: the staged entry said the lane's own convention treats a timeout as a detection. That
  describes Stryker. The lane's rule makes a timeout Inconclusive (`SKILL.md:208-212`), and
  the entry now says so. E2: the FAQ names two factors, timeouts and static initializers, not
  one. E3: the entry now carries lane anchors. The staged headline claim "a mutation score's
  denominator is a choice of outcome class" was cut, because S155 defines no score at all
  (`.ufo/waves/round-42/w1/ScoutPitConcepts.md`). The new headline rests on S158 and S001.
- PROVINCE: mutation-outcome semantics for the lane's own kill verdicts is Core F1 ground.
  QUALITY: every quote is at most 25 words and located, both snapshots are committed
  (criterion 79), and the coverage row is in `corpus/README.md`.

### Reject — `survivor-classification.md` (`staged:S166`, `staged:S156`)

Refused. (1) One direct quote has drifted: the staged text reads 「…テストの穴とは当たりません」
and the page opened 2026-10-25 reads 「…とは限りません」. The meaning is the same, but a quote
the source does not carry is not a located quote. (2) Its recheck predicate is false on the
live bytes: `grep -c '168 killed'` returns 2, and the entry expects 1. (3) Its thesis duplicates
the held F8 entry `corpus/knowledge/oracle-anchored-survivors.md` (`corpus/README.md:85`;
`.ufo/waves/round-42/w1/ReviewSurvivorGate.md`). Flip condition: re-quote from a committed
snapshot, fix the recheck, and state what the entry adds beyond the held F8 entry.
`staged:S156` (arXiv 2406.09843) is a package id and is not the lane's S156.

### Not adopted this round — `mutation-score-semantics-cjk.md` (`staged:S163`–`staged:S165`)

Both gates said admit (`.ufo/waves/round-42/w1/ScoutCjkEntry.md`, `ReviewCjkGate.md`). It is
not adopted because a round takes one theme and the entry's ground is the score
denominator, not which outcomes count as a kill. It is a sibling theme, not a refusal.
Flip: a later assimilation round re-opens the three sources and snapshots them.

### Ids, collisions, census

- Registry before: 109 rows (S001–S154). Staged: 103 ids. `comm -12` → 2 collisions, `S153`
  and `S154` (`.ufo/waves/round-42/assimilation/collisions`).
- Guard proof: a scratch registry with an indented row `  | S159 |` collides under the
  0–3-space extractor (`S153 S154 S159`) and not under the column-zero one (`S153 S154`);
  receipts in `.ufo/waves/round-42/assimilation/guard/`.
- Renumber map, by document: `staged:S159` (pitest.org/quickstart/basic_concepts/) → S155;
  `staged:S160` (pitest.org/faq/) → S156. S157 and S158 are new rows, not from the package.
- Scratch mirror validate before any commit: `sources-census.sh validate --file <mirror>`
  exit 0, zero E codes (`.ufo/waves/round-42/assimilation/validate.stdout`); the append block
  is `.ufo/waves/round-42/assimilation/append-block.diff`.
- Round start `sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit 0,
  109 rows, 9 × W04 + 1 × W01 (`.ufo/evidence/round-42/census-sources/start.stdout`).
- Quarantine slice: 17 data rows (14 `payload-absent`, 3 could-not-be-fetched), the same set
  the round-40 lesson holds a verdict for; none is cited by this round's theme
  (`.ufo/waves/round-42/assimilation/quarantine-slice`, `.ufo/waves/round-42/w1/ScoutQuarantine.md`).
- Recheck cells normalized: the staged `365d — curl … | grep -c …` cells become `180d`
  (the cadence of the lane's other docs rows). The stripped commands are kept here:
  `curl -fsSL 'https://pitest.org/quickstart/basic_concepts/' | grep -c 'No coverage'` (2 on
  2026-10-25) and `curl -fsSL 'https://pitest.org/faq/' | grep -c 'timed out on one run'` (1).
- Used-by changes: S001 `mutation-score-semantics.md, mutation-case-kumitate-sources-check.md`
  → the same plus `pit-outcome-vocabulary.md` and `r42-attribute-and-outflag-destinations.md`.
  S153 `r41-variable-destination-writes.md` → the same plus
  `r42-attribute-and-outflag-destinations.md`. All in `corpus/knowledge/`.

### considerthese

`considerthese/2026-10-24.md` proposal 5 (SHONEN promotion readiness), the one proposal of
that file not mined before. Mined as this table (`.ufo/waves/round-42/w1/ScoutConsiderthese.md`),
for the operator only:

| SHONEN box | standing command a non-author can run | gap |
|---|---|---|
| 1 SKILL.md tables, patterns, checklists, sources | none | no script asserts SKILL.md content; `reports/round-1-calibration.md` is a manual audit |
| 2 end-to-end task logged in LOG.md | none | no runnable check |
| 3 executable without oral context | `python3 .ufo/evidence/round-21/coldread/measure.py --rev REV` | exit 0 at the base, selftest 12/12; this is the only box with a standing check |
| 4 no cross-domain bleed | none | no tool reads `PROVINCE.md` |

One box out of four is mechanically checkable today. No box moves this round.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| stale-receipt | `.ufo/waves/round-41/residual/receipt.json` says `present: false` for `ResidualReceipts.md`, which is in the tree; the receipt was written before that report landed | none at round 41; the round-41 closure routed it (`corpus/lessons/round-41-verifier-spotcheck.md`, defect 2) | C1 class m10 plus an appended superseding receipt (`.ufo/waves/round-42/supersede/round-41-residual-receipt.json`); shown able to fail: `.ufo/evidence/round-42/before/c1-at-base.stdout` (m10=1) and selftest cases `T2_*` (`.ufo/evidence/round-42/before/c1-selftest.stdout`); QUALITY criterion 81 |
| newline-spanning-extractor | the round-41 C1 counter's backtick pattern spanned newlines, so a mispaired span hid the paths after it | the round-41 closure (defect 1) | line-scoped pattern in the round-42 counter; shown able to fail: selftest `T1_old_extractor_misses` / `T1_new_extractor_sees`; wave-1 mutant M1 (revert) killed (`.ufo/waves/round-42/w1/MutC1M8.md`) |
| half-true-citation | the frozen contract and counter docstring cite "PIT Run error and Stryker RuntimeError, which neither tool counts as a kill"; PIT's source scores `RUN_ERROR` as detected (S158) | a wave-1 critic, not any criterion (`.ufo/waves/round-42/w1/CriticOracleSource.md`) | contract post-freeze amendment P1, QUALITY criterion 82 (cite the tool whose rule you follow); shown able to fail: the crash probe in criterion 82 prints `runtime_error` |
| delegated-build-without-interface-test | the wave-1 executor's v4 rewrote v3 in compressed form and reached `fixtures_pass=3/10` with duplicate site records (`.ufo/waves/round-42/w1/ExecV4Tool.md`) | the frozen C2 counter, run by the seat itself | the L1 rebuilt v4 on v3's walk (contract amendment P4); the counter caught it before any landing |

The unchanged mistake from round 41 that this round does not repeat: no append-only file was
edited in place. `git diff --numstat` on `LOG.md`, `SCORECARD.md`, `corpus/QUALITY.md` and
`corpus/README.md` shows insertions only. `corpus/SOURCES.md` shows two in-place used-by
cell changes, logged above as the registry contract requires.

## C1 instrument — limits found by the wave, disclosed not repaired

The counter is pinned (sha256 `9782a5a0…`); none of these was used to reach the target.

- m10 is content-blind. A superseding receipt clears a stale claim for any path that
  resolves, including an empty file, an unrelated stub or a directory
  (`.ufo/waves/round-42/w1/CriticSupersedeGaming.md`). This round's superseded path is a
  24386-byte seat report, read by the wave.
- m10 reads only boolean `present` beside a string `report` or `path`, under
  `.ufo/waves/`, in parseable JSON. Other key names, string booleans, list-valued reports,
  receipts elsewhere and malformed JSON are not read (`.ufo/waves/round-42/w1/ExecC1Falsify.md`
  f1–f6). One real out-of-class disagreement existed: the round-20 snapshot's
  `report_exists: false` for an existing seat report (`.ufo/waves/round-42/w1/ScoutReceiptSweep.md`
  D2). It is superseded by `.ufo/waves/round-42/supersede/round-20-outcomes.json` and is not
  counted toward C1.
- m7 checks round-42 records only, though the contract statement names round-41 records too
  (contract amendment P2). Hand check: the round-41 records cite S001, S153 and S154, all
  `mined` in `corpus/SOURCES.md`.
- m7 misses `S 155` (space); m11 misses uppercase hex; m6 misses a registry row indented
  four spaces (`ExecC1Falsify.md` f9–f11). The `(?<![0-9a-f:])` lookbehind makes the
  `blob:`/`tree:` skips redundant, and any hex after a colon is skipped (`MutC1M11.md`, M3
  survived).
- Two m10 mutants survive the selftest: treating any `supersedes` as covering, and comparing
  `present` to `True` always (`MutC1M10.md`). Two m8 mutants survive too: dropping the
  fleet-path skip, and dropping `$` from the skip set (`MutC1M8.md`, which names the
  fixture that would kill each). A fixture with a superseding receipt whose target is not a
  receipt, and one with a `present: true` claim for a missing path, would kill the two m10
  survivors.

## C2 instrument — limits found by the wave, disclosed not repaired

- The battery cannot tell a resolver from a tool that special-cases its names and line
  numbers. A v3 copy with literal tables passes all ten fixtures and all three live sites
  (`.ufo/waves/round-42/w1/CriticFixtureOverfit.md`). The kill oracle only sees that a case
  differs, so a literal-table tool also kills its mutants. The separation from a cheat is
  shown outside the predicate, by a renamed-identifier battery run in wave 2 and by reading
  the v4 source.
- Untested shapes (`.ufo/waves/round-42/w1/MutC2Fixtures.md`): attribute and output flag
  in one file, flag scope, multi-site ordering, robustness inputs. F07 and F08 are
  near-duplicates.
- The oracle is stricter than both vendors. Timeouts become `runtime_error` (both tools
  count a timeout as detected), and one crash anywhere in the battery makes the whole
  mutant a run error.
- Booleans in the tool's JSON are coerced with `bool()`, so a string `"false"` reads true
  (`ReviewC2Counter.md`). v4 emits real booleans.

## Holds

- v4 is bounded: one module, depth eight, one distinct assignment per attribute, one
  top-level return per folded method, four output-flag spellings, `parse_args` only. Its
  docstring now says aliases, closures and attribute reassignment are not reliably resolved,
  which corrects v3's blanket "NOT resolved" (round-41 routed defect 5).
- `explicit_out` separates operator-named destinations from hidden updates; it does not
  make the write harmless.
- The round-41 routed v3 false positives (defect 4) are resolved by v4, not by editing v3:
  v3's bytes stay pinned at `095924a7…`.
- Round-41 routed defect 7 (cosmetic list split in `corpus/SOURCES.md`) is left as is:
  re-flowing a closed note is an in-place edit for no parse gain.

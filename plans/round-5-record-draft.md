# Round-5 record draft — for the parent scribe to finalize (TAMESHI-SCR-T5)

Drafted 2026-10-14, poll window 14:02–14:32 (assignment: 30-min cap) by the
round-5 scribe-prep lane (SCR-T5). This file carries: **A** the SCORECARD
move-log row, **B** the LOG.md round-5 entry text, **C** the SCR-T5 evidence
ledger, **D** landing status + parent checklist. Write-scope: this file only;
scratch `/tmp/w5-scr-t5-*`.

**Round-5 shape** (from `plans/round-5.plan.md`, 12 lines, mtime 13:59). Axis
move: **depth** (third data point, cross-author) — the mutation method on a
THIRD gate from a DIFFERENT author and style: `tsukuroi-shokunin/tools/
tsukuroi-census.sh` (bash, 26-case suite), kill-rate measured against 10 fresh
mutants; cross-author surfaces either confirm or amend the arm-class matrix.
Also: **VER-T1's two precision errata land** (chmod enumeration `:608/:654`;
JS wording scope). Anti-claim: a divergent kill profile amends the matrix —
recorded, not smoothed. Measure: third kill-rate table; matrix errata block;
tsukuroi original sha256 unchanged (read-only on a sibling's tool).

## 0. Landing status at draft time (observation; tameshi tree, HEAD `b58b26f`)

LANDED in-tree (all mtimes 2026-10-14):

- **T5-1 third-case note** — `corpus/knowledge/mutation-case-tsukuroi-census.md`
  (396 `wc -l` / 397 display lines, final line unterminated / 30787 B, sha256
  `b431bc6ce2b53e4e…`, mtime 14:12:39, stable ≥6 min). Headline: **6/10
  killed (60 %)**; composition 6 kill-aimed + 4 hole-aimed; **incident I1**
  headlined (substrate moved mid-run by a concurrent lane → the assigned
  before/after sha claim is unsatisfiable; all measured cells on a frozen
  `084951be` copy); its own errata E1–E4, §6 cross-revision replay on
  `aae45531`, U1–U7, full reproduce block §8.
- **T5-2 errata (both VER-T1 precision landings), append-only** — landed
  14:06:39:
  - `corpus/knowledge/arm-class-matrix.md` — `## Errata (round 5)` block with
    **E3** (chmod enumeration corrected to 15 live sites: `:521-588`, `:608`,
    `:654`, `:704-717`, `:768`; B5's verdict unchanged; cites AUD-T1 F2). Now
    524 `wc -l` / 38531 B, sha256 `631873232e46f914…` (was 497/36706/
    `4df037f7…`); block starts at `:498`, E3 text at `:506`; old blob a
    byte-prefix of the new file (§C.3).
  - `corpus/knowledge/mutation-case-kimi-census.md` — `## Errata (round 5)`
    block with **E2** (JS "unreached" wording scope: fixture-unreached vs
    assert-caused; D2 stays reported-but-unasserted; row E's JS-side scope
    bounded to D4/D5). Now 237 `wc -l` / 15679 B, sha256
    `034524eff8f19cb8…`; block starts `:207`, E2 at `:215`; byte-prefix held.
  - ⚠ Both block headings landed glued to the previous unterminated final line
    (no leading newline) — rendering repair note in §D.
- **T5-4 fleet-wide suite-vs-arm census** — new `corpus/knowledge/
  fleet-suite-census.md` (385 `wc -l` / 28842 B, sha256 `adeb3070cf7ed705…`,
  last write 14:07:54). Static read + one `--selftest` pulse per gate; scratch
  `/tmp/w5-tameshi-census/`. Headline: 348 executed cases across six green
  suites (62/42/60/102/39/43); 5/6 completeness meta-checks; 1/6 mutation
  controls; 1/6 integration groups; 0/6 kill-rate harnesses.
- **SKILL.md round-5 append** — `## Third case — cross-author confirmation
  (round 5, measured)` (+127 L → 791 L / 55138 B, sha256
  `928e073fa57e3988…`, mtime 14:13:50; old blob 45644 B is a byte-prefix).
  Distils the third case: incident I1, the 6/10 table, the row-A–G
  confirm/amend cells, calibration, and "what a fourth case would need to
  show". First append in this repo that inserts the missing newline properly.
- **`plans/round-6.plan.md`** (33 L, mtime 14:08:59) — next round's plan
  (adjacency: first service engagement on `cite-check.mjs`; its own commit
  item, not round-5 content).

NOT LANDED at draft close: **T5-3's** matrix fold (matrix unchanged since
14:06:39); any round-5 **audit verdict** (AUD-T5 had only control/pin evidence
under `/tmp/w5-aud-t5-*` at 14:02–14:03 and no verdict log by 14:18);
`corpus/README.md` rows; LOG/SCORECARD (this draft's job).

CROSS-LANE (tsukuroi repo, not written by this lane): S5-1's hardening
(976 → 1032 L, sha `084951be…` → `aae45531…`, selftest 26 → 35 cases) — the
cause of incident I1 and the target of the note's §6 replay; S5-2's
`timer-drift-plane.md`; the tsukuroi scribe's own record draft. The tsukuroi
lane's separate 23-defect sweep (quoted 13 killed / 10 survived) is *quoted* in
the note, not in this lane's evidence.

## A. SCORECARD.md — move-log row (append after the round-4 row)

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 5 | depth | two measured kill tables, both 80 %, both tameshi-cut on sibling gates (JS `kimi-census.mjs` r2; bash kagi `surface-census.sh` r3); matrix U4 "no third gate/language" (`arm-class-matrix.md:267-268`); round-4 carry "§13 projection awaits its measured sweep" | third measured kill-rate, **cross-author**: `tsukuroi-census.sh` (26-case hermetic suite, 976 L @ `084951be…`) vs 10 pre-registered single-edit mutants → **6/10 killed (60 %)** — first measurement inside the 50–80 % band; composition 6 kill-aimed + 4 hole-aimed, 10/10 pre-registrations held on verdicts and failing counts (first perfect sweep of the three); kills B1–B6 incl. the widest bash kill measured (B6 rollup-flip 21/26); survivors B7 cap-raised-past-fixture (26/26; probe: sampled set differs), B8 usage-exit 2→1 (CLI parser never exercised; probe: `--bogus` rc 2→1), B9 roll-line field swap (verdict fields unasserted; probe: wrong plane attribution), B10 PCI-unreadable branch (probe: BLOCKED→HEALTHY flip) — rows A/D re-confirmed cross-author, row C gains "cap reachability is per-cap", row E promoted toward pattern (2 bash instances, still no JS), row G 9/9 across three gates, row B narrowed to case-coverage-bound; **incident I1 recorded not smoothed**: the substrate moved mid-run (S5-1's concurrent hardening, +56/−0, 26→35 cases) so the plan's "original sha256 unchanged" check is **unsatisfiable** — every measured cell sits on a frozen pre-hardening copy, the provable negative is "this lane's writes never touched the substrate", and the §6 replay on the hardened revision shows the hardening closed B10 only (B7/B8/B9 still survive 35/35); plus the round's supporting surfaces: the two VER-T1 precision errata landed append-only (matrix **E3** chmod enumeration corrected to `:521-588 · :608 · :654 · :704-717 · :768`, B5 verdict unchanged; kimi note **E2** JS "unreached" wording scoped, D2 stays reported-but-unasserted) and the six-gate suite-vs-arm census (`fleet-suite-census.md`: 348 cases 6/6 green; 5/6 meta-checks; 1/6 mutation controls; 0/6 kill-rate harnesses — tameshi's standing service offer) | independent tool re-sweep by SCR-T5 over the pinned bytes (`084951be…`, extracted read-only from tsukuroi git): `CONTROL: GREEN`, B1–B6 `KILLED` (FAIL lines 2/3/1/1/1/21 of 26), B7–B10 `SURVIVED`, `MUTATE_RESTORE: OK`, `MUTATE: DONE (… killed=6 survived=4 inconclusive=0 kill-rate=60%)`, exit 0, 19.5 s; mutant sha256 set identical to T5-1's `results.json` (10/10); note tallies re-read (`mutation-case-tsukuroi-census.md` @ `b431bc6c…`: table rows 11, §5 E1–E4, §7 U1–U7, §6 replay 4 cells); errata anchors re-read + byte-prefix proven (§C.3, §C.6); census headline `fleet-suite-census.md:46-71`; SKILL append prefix-checked (§C.8). Re-run 2026-10-14 (TAMESHI-SCR-T5) |

## B. LOG.md — round-5 entry (append as a new bullet after the round-4 entry)

- 2026-10-14 — round 5: planned as a ufo-round-plan (`plans/round-5.plan.md`,
  ufo-round-plan-v1 — axis move **depth** (third data point, cross-author) +
  VER-T1's two precision errata landing; anti-claim pre-registered: a
  divergent kill profile amends the matrix, recorded not smoothed). Same
  dispatch shape as rounds 1–4 — lane write-scopes leave this LOG to the
  scribe; no `.ufo/waves/tameshi-r5-*` directory exists (checked 2026-10-14),
  so the lane deliverables in this repo ARE the wave record (observation).
  Content lanes:
  TAMESHI-T5-1 → `corpus/knowledge/mutation-case-tsukuroi-census.md` (396
  `wc -l`, final line unterminated; 30787 B; sha256 `b431bc6c…`): the third
  measured kill-rate, first cross-author — tsukuroi `tools/tsukuroi-census.sh`
  @ `084951be…` (44947 B, 976 newlines), 26-case hermetic suite vs 10
  pre-registered single-edit mutants (fresh copies, `count==1` asserted) →
  **6/10 killed (60 %)**, the corpus's first non-80 % headline and first
  50–80-band point; control green `PASS (26 cases, 26 passed, 0 failed)`
  rc 0, 11 runs in 19.6 s, no
  inconclusive run, count held every run; kills B1 inverted nvidia guard
  (2/26), B2 Qkk rc-tolerance {0,1}→{0,2} (3/26), B3 deleted empty-ring
  fail-closed arm (1/26), B4 weakened kernel class pin (1/26), B5 drift
  counter +2 (1/26), B6 rollup `worse()` flip (21/26 — widest bash kill
  measured); survivors B7 `SAMPLE_N` 8→9 (fixture samples 4; probe: 9-package
  input samples 9), B8 usage exit 2→1 (no case runs the parser; probe
  `--bogus` rc=1), B9 roll printf args swapped (probe: wrong plane
  attribution under a DEGRADED verdict), B10 PCI-unreadable arm → silent
  absent (probe: BLOCKED→HEALTHY); pre-registration held 10/10 on verdicts
  and 10/10 on failing counts (first of the three with no calibration miss);
  **incident I1 (headline)**: the substrate moved mid-run — concurrent lane
  S5-1 hardened the tool at 14:06:23 (+56/−0, 9 new cases, 26→35) — so the
  assigned before/after sha claim is unsatisfiable; all cells on the frozen
  copy, writes confined to `/tmp/w5-tameshi-1-work/`; §6 replays the four
  survivors on `aae45531`: hardening closed B10 only, B7/B8/B9 still survive
  35/35; note errata E1 (perfect pre-registration, method-not-luck) E2
  (incident; recommends a mtime/inode note in tool receipts) E3 (rate bands
  are composition-bound: record kill-aimed vs hole-aimed beside every rate)
  E4 (convergence with S5-1's hardening classes, 8/9 overlap — corroboration,
  not double-counting); U1–U7. Independent SCR-T5 re-sweep through
  `tools/mutate-and-run.sh` (r4-2, `597e1419…`) reproduced every verdict and
  mutant sha, `MUTATE_RESTORE: OK`.
  TAMESHI-T5-2 → both VER-T1 precision errata landed append-only (14:06:39):
  `corpus/knowledge/arm-class-matrix.md` gains `## Errata (round 5)` **E3** —
  §6's chmod enumeration ("`:521-588`, `:704-717`, `:768`") corrected to 15
  live sites (**`:521-588`, `:608`, `:654`, `:704-717`, `:768`**; the two
  omissions are `verbs()` probe env-file `chmod 600`s); B5's fixture-absent
  conclusion and every verdict cell stand; cites AUD-T1's independent F2.
  `corpus/knowledge/mutation-case-kimi-census.md` gains **E2** — JS
  "unreached" wording scope: the ≥6-findings truncation region is
  *fixture*-unreached while D2's survival is *assert-caused* (prefix DRIFT
  assert `:498`); D2 stays row A/D, and row E's JS-side scope is bounded to
  the probed arm-deletion mutants (D4/D5) — B5 remains the only
  unreached-arm instance among the 20. Both blocks byte-append; ⚠ both block
  headings landed glued to the previous unterminated line (see parent
  checklist).
  TAMESHI-T5-4 → `corpus/knowledge/fleet-suite-census.md` (385 L, sha
  `adeb3070…`): the round-4 §13 projection extended to all six kumitate gates
  — 348 executed cases across six green suites (62/42/60/102/39/43), 5/6
  completeness meta-checks (cite-check none), 1/6 mutation controls
  (cite-check's integration-gated copy), exactly 1/6 integration groups,
  0/6 kill-rate harnesses; the note closes with tameshi's standing service
  offer (queue head: cite-check).
  SKILL round-5 append → `SKILL.md` (665 → 791 L, +127; sha
  `928e073f…`): `## Third case — cross-author confirmation (round 5,
  measured)` — the third-case distillation (incident, 6/10 table, matrix
  cells A–G, calibration, fourth-case criteria); byte-prefix held.
  TAMESHI-T5-3 → third-case fold onto the matrix (polling at this draft's
  close; NOT folded here).
  Audits: no round-5 audit verdict landed at this draft's close (AUD-T5
  target = the tsukuroi-side mutation note; control/pin evidence only at
  14:02–14:03); the in-tree evidence at draft time is the two errata blocks'
  own live re-measurements, the census's pin pulses, and the note's §6
  replay. If an audit batch lands, fold its named verifiers here.
  Scribe verification (this draft, TAMESHI-SCR-T5, all re-run 2026-10-14;
  scratch `/tmp/w5-scr-t5-*`): independent 10-defect re-sweep through the
  shipped tool against the pristine extracted from tsukuroi git HEAD →
  `CONTROL: GREEN`, `MUTATE: DONE (… killed=6 survived=4 inconclusive=0
  kill-rate=60%)` exit 0, `MUTATE_RESTORE: OK` (10/10 mutant shas identical);
  both errata appends and the SKILL append proven byte-prefix against the
  committed blobs; both fleet pins held; tool selftest 37/37; tsukuroi gate
  selftest observed 26/26 at the swept revision and 35/35 post-hardening
  (cross-lane, observation).
  SCORECARD round-5 move: depth improved (third kill-rate, first cross-author
  survivor taxonomy confirmations + two new species, first non-80 % headline
  with composition binding; counting commands in the move-log row).
  Carried to round 6 (recommendations, not absorbed): the T5-3 matrix fold (if
  not landed by close); the census queue (cite-check first — round-6 plan
  already anchors there, with PREP-T6's 1/4 probe recorded); matrix U1–U6
  stand (coordinated edits; D2 boundary; host-gated bash verbs; band
  interiors — now with one 50–80-band point; drift/cross-host; class
  membership (I)); the note's U1–U7 (incl. tool-receipt improvement
  recommendation, re-run B7/B8/B9 against `aae45531` successors); R4-3 SKILL
  calibration append superseded by the round-5 SKILL section (decide fold vs
  drop); the two glued errata headings (repair = insert newline,
  append-only-safe).

## C. SCR-T5 evidence ledger (commands re-run by this lane 2026-10-14; scratch `/tmp/w5-scr-t5-*`)

1. Baseline pins at 14:02 on HEAD `b58b26f` (working tree clean except
   `plans/round-5.plan.md`): SKILL.md 665 L / 45644 B / `dd2f4dee9df7a422…`;
   `tools/mutate-and-run.sh` 1001 L / 42291 B / `597e141989065e03…`;
   `arm-class-matrix.md` 497 `wc -l` / 36706 B / `4df037f7f84f541a…`;
   `verification-patterns-fleet.md` 306 L / 39663 B / `bbf04a5e959b68b4…`;
   SCORECARD.md 17 L; LOG.md 303 L.
2. Independent re-sweep (the round's headline, re-measured by this lane):
   pristine extracted read-only from tsukuroi git
   (`git show HEAD:tools/tsukuroi-census.sh` → sha `084951be…`, 44947 B);
   spec generated from T5-1's defect list (10 defects, escape-safe);
   `bash tools/mutate-and-run.sh --target /tmp/w5-scr-t5-work/pristine.sh
   --defects /tmp/w5-scr-t5-work/spec.txt --suite 'bash "$MUTANT" --selftest'
   --workdir /tmp/w5-scr-t5-work/sweep --label tsukuroi-census-r5-recheck` →
   exit 0, 19.5 s: `CONTROL: GREEN (exit=0 …)`; B1 2, B2 3, B3 1, B4 1,
   B5 1, B6 21 FAIL lines (all `KILLED`); B7–B10 `SURVIVED` (26/26 green);
   `MUTATE_RESTORE: OK (target-sha256 before=after=084951be…)`;
   `MUTATE: DONE (… killed=6 survived=4 inconclusive=0 kill-rate=60%)`.
   Mutant sha256 list identical to T5-1's `evidence/results.json` — 10/10
   (e.g. B1 `f1a89634…`, B6 `96cf6558…`, B10 `c4162bac…`). Evidence:
   `/tmp/w5-scr-t5-work/sweep/{results.tsv,evidence/*.out}` +
   `/tmp/w5-scr-t5-evidence/recheck-sweep.out`.
3. Errata appends (append-only proof + anchors):
   `git show HEAD:corpus/knowledge/arm-class-matrix.md` (36706 B, sha256
   `4df037f7f84f541a…`) is a byte-prefix of the new file (38531 B, sha256
   `631873232e46f914…`) — `cmp` OK; same for
   `mutation-case-kimi-census.md` (13648 B, old blob sha `3b8c4984338adfef…`
   prefix of 15679 B / `034524eff8f19cb8…`). E3 at `:506`,
   E2 at `:215`; `grep -c '^## Errata (round 5)'` → 0 in both (headings glued
   at `:498` / `:207`; repair note in §D).
4. Selftests: `bash tools/mutate-and-run.sh --selftest` →
   `MUTATE_SELFTEST: 37/37 pass` / `VERDICT: PASS`, rc 0. Sibling pulses
   (read-only): the frozen swept revision (this lane's `pristine.sh` copy of
   `084951be…`) `--selftest` → `TSUKUROI_CENSUS_SELFTEST: PASS (26 cases,
   26 passed, 0 failed)` rc 0 (re-run at 14:29); the live hardened revision →
   `PASS (35 cases, 35 passed, 0 failed)` (observed). No
   `.ufo/waves/tameshi-r5-*` directory exists (`find … -iname '*tameshi*'` →
   none) — the lane deliverables in this repo ARE the wave record.
   tsukuroi tree left untouched by this lane.
5. Census headline re-reads (`fleet-suite-census.md`, landed 14:07:54):
   headline block `:46-71` (348 cases 6/6 green; 5/6 meta-checks; 1/6
   mutation controls; 1/6 integration groups; 0/6 kill-rate harnesses; two
   prior tables); scope/pins `:16-43`; provenance `:9-14`.
6. Errata substance re-measured on the pins (this lane): `grep -n chmod`
   on `kagi-shokunin/corpus/surface-census.sh` (@ `275d8294…`, held) → 15
   sites exactly as E3 states, `:608`/`:654` present, `:707` the only
   exec-row chmod; `sed -n '378p;498p'` on `kumitate-shokunin/scripts/
   kimi-census.mjs` (@ `83016d45…`, held) → the `slice(0, 6)` cap and the
   prefix-based DRIFT assert — both E2 anchors verbatim; kagi + kumitate
   trees porcelain-empty.
7. Third-case note re-reads (`mutation-case-tsukuroi-census.md` @
   `b431bc6c…`, stable 14:12:39→14:18): §1 kill table 11 rows (control +
   B1–B10) with failing counts 2/3/1/1/1/21 and 0×4; §5 E1–E4; §6 replay
   cells (B7/B8/B9 survive 35/35, B10 killed by D19); §7 U1–U7. These match
   this lane's re-sweep on every §1 cell; the §6 replay cells and the S5-1
   23-defect table are *quoted* (not re-run by SCR-T5) — U.
8. SKILL append prefix check: `git show HEAD:SKILL.md` (45644 B) is a
   byte-prefix of the new SKILL.md (791 L / 55138 B / `928e073f…`); the new
   section (`## Third case — cross-author confirmation (round 5, measured)`)
   reads the note's numbers correctly (spot-checked: 6/10, incident, recipe
   row table).

## D. Parent checklist (round close)

- **Fold T5-3's matrix amendment** when it lands (matrix sha moves off
  `631873232e46f914…`; re-check its own bookkeeping — the round-5 errata block
  is append-only, so a fold must land as a new block, not an edit).
- **Repair the glued errata headings** (both files): insert a `\n` between the
  previous unterminated final line and `## Errata (round 5)` — byte-prefix
  property is preserved by an insertion after the old bytes, so append-only
  discipline holds; precedent: round-2 SCORECARD repair (SC-1). If left as
  is, record the rendering defect instead.
- **Record the incident honestly** wherever the round's measures are quoted:
  the plan's "tsukuroi original sha256 unchanged" is unsatisfiable (I1);
  name both revisions (swept `084951be…` vs hardened `aae45531…`) and the
  frozen-copy basis of every measured cell.
- **Coverage-map rows** (`corpus/README.md`): still missing a row for
  `arm-class-matrix.md` (round-4 carry); add rows for
  `fleet-suite-census.md`, `mutation-case-tsukuroi-census.md`, the round-5
  errata blocks, and update the SKILL row to the new revision
  (`928e073f…`, 791 L — historical citations of `dd2f4dee…`/665 L refer to
  the executor's executed revision; keep those).
- **Commit items** (lane identity + round shape; precedents `2587e0a`,
  `53e74a8`, `b58b26f`): `plans/round-5.plan.md`,
  `corpus/knowledge/arm-class-matrix.md` (E3),
  `corpus/knowledge/mutation-case-kimi-census.md` (E2),
  `corpus/knowledge/fleet-suite-census.md`,
  `corpus/knowledge/mutation-case-tsukuroi-census.md`, `SKILL.md` (+127),
  T5-3's fold if landed, this draft's finalized record; `plans/round-6.plan.md`
  is the next round's plan (its own item).
- **Stale citations**: matrix round-4 sha `4df037f7…` superseded by
  `631873232e46f914…`; SKILL `dd2f4dee…` superseded at the live revision by
  `928e073f…`; round-4 record's "§13 projection awaits its measured sweep"
  is now partially answered — the round-5 sweep tested the *tsukuroi* gate,
  not kumitate `round-gate.mjs`; keep that distinction.
- R4-3 (SKILL calibration append) is superseded by the round-5 SKILL section;
  decide fold vs drop, record either way.
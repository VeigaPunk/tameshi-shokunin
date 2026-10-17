# Round-4 record draft — for the parent scribe to finalize (TAMESHI-SCR-T)

Drafted 2026-10-14 ~13:44 by the round-4 scribe-prep lane (SCR-T), after a poll
window 13:14–13:44 (assignment: 30-min cap). This file carries: **A** the
SCORECARD move-log rows, **B** the LOG.md round-4 entry text, **C** the SCR-T
evidence ledger, **D** landing status + parent checklist. Write-scope: this
file only; scratch `/tmp/w4-scrt-*`.

**Landing status at draft time** (observation: `git status --porcelain` +
mtimes; round 4 is uncommitted, HEAD still `53e74a8` = round-3 close):

- LANDED in-tree: `corpus/knowledge/arm-class-matrix.md` (R4-1, 13:10:22 →
  §13 = R4-4, present at the 13:40 re-check (recorded mtime 13:25:53; ordering
  caveat §C.9); now 498 lines / 497 `wc -l` / 36706 B,
  sha256 `4df037f7…`); `tools/mutate-and-run.sh` r4-2 (R4-2, 13:10:58); the
  append-only `## Errata (round 4)` block V-R4-1…3 in
  `corpus/knowledge/verification-patterns-fleet.md` (ERR-T, 13:31:10);
  `plans/round-4.plan.md` (13:04).
- NOT landed in-tree at 13:44: **R4-3** (SKILL.md calibration append — draft
  at `/tmp/tameshi-r4-3-draft.md`, poller log ended 13:10:52). Its paragraph
  is marked ⧗ and stays provisional; fold the real numbers in if/when the
  write lands.
- Transient-state note: R4-4's §13 appeared inside the matrix file during the
  poll window (recorded mtime 13:25:53; present at the 13:40 re-check);
  `git status --porcelain` does not surface untracked-file content changes, so
  it was caught only by an mtime+size re-check — §13 is folded in throughout
  this draft (§C.9 for the ordering caveat).
- No `.ufo/waves/tameshi-r4-*` directory exists (checked 2026-10-14): the lane
  deliverables in this repo ARE the wave record (rounds 1–3 precedent).
- Every number below is one of: **[O-SCRT]** re-run by this lane (commands in
  §C), or **[O-lane]** quoted from a landed artifact with its anchor.

## A. SCORECARD.md — move-log rows (append after the round-3 rows)

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 4 | calibration | two measured kill tables existed (r2 JS note 206 lines, r3 bash note 258 lines) but the comparison between them was per-note prose: which arm classes a hermetic green generically protects vs misses had never been stated for the pair, and PROVINCE's ≥2-lane bar had admitted nothing at matrix level (round-3 carried list: "a third gate … is the next depth move"); the plan pre-registered the cross-case re-cut with disagreement-as-finding as its anti-claim (`plans/round-4.plan.md:2-8`) | the arm-class matrix (`corpus/knowledge/arm-class-matrix.md`, 498 lines / 497 `wc -l`, final line unterminated, sha256 `4df037f7…`): all 20 mutants (10 JS D1–D10 + 10 bash B1–B10) re-cut BY ARM CLASS — 7 classes (A verdict paths · B fail-closed arms · C counts · D reported-but-unasserted surfaces · E unreached arms · F coordinated edits · G behavior predicates, added so all 20 mutants land in a row), ledger **16 killed / 4 survived / 0 inconclusive** (both suites 8/10); survivors fall in exactly two classes — reported-but-unasserted surfaces (D2, D10, B10) + unreached arm (B5); admission table = **5 classes admitted** on the 2-lane bar (reported-but-unasserted surfaces; verdict-stem protected / remainder unasserted; fail-closed exit-map narrow; asserted counts; behavior predicates), **1 proposed** (unreached-arm survivor — single instance, JS counter-instances D4/D5 bound it), **1 unknown** (coordinated edits); disagreements recorded as the finding, never averaged (pin style exact-line vs substring; fail-closed arm species environment-failure vs malformed-input; kill width 16/43 vs ≤3/16); class membership is (I) on (O) verdicts (U6); 2 append-only errata (E1 pre-write model miss, E2 deliberate dual-row listing) + U1–U6; §12 live spot-check block (anchors re-read on the pinned bytes + both suite pulses); §13 = R4-4's round-gate projection (third gate, explicitly projection NOT measurement: 14 finding kinds 14/14 statically covered by the suite's one meta-check; 7 fail-closed tokens 6/7 hand-asserted, 1 token + 2 call-site species uncovered; full-line anchored verdict parse, tighter than either measured case; PU1–PU5 bound it, nothing admitted) | `wc -l corpus/knowledge/arm-class-matrix.md` → 497 (498 lines, final unterminated; `sha256sum` → `4df037f7…`, 36706 B; §13 appended 13:25:53) [O-SCRT]; ledger `grep -cE '^\| [DB][0-9]+ \|'` → 20, killed `grep -c` → 16, survived → 4; matrix rows `^| [A-G] |` → 7; admission rows → 7; `^- U[0-9]` → 6; `^E[0-9]` → 2 [O-SCRT]; anchors re-read on pinned bytes: `sed -n '498,499p;511,512p;526p'` on kumitate `kimi-census.mjs` = DRIFT prefix-assert / exact CLEAN-line equality / `j.totals.frozen.K5 === 3`; `sed -n '747,760p'` on kagi `surface-census.sh` = `run_case` exit+token grammar; `sed -n '862p;866p'` = the two summary arg lists; `grep -n -- '-x '` → single hit `:214` (inside B5's arm) [O-SCRT]; §13 anchors re-checked: round-gate `sha256sum` → `f890e277…`, 1511 lines, `grep -n 'failClosed('` → 10 sites incl. `:683`, `FINDING_KINDS` `:171-176` → 14 kinds, meta-check `:1487` [O-SCRT]; pins held `sha256sum` → kimi-census `83016d45…4f426`, surface-census `275d8294…53009f`; live pulses `bash kagi-shokunin/corpus/surface-census.sh --selftest` → `SELFTEST: PASS (16 cases)` exit 0 (skip-cases 15/16 substrate-absent, kagi tree porcelain-clean after), `node kumitate-shokunin/scripts/kimi-census.mjs --selftest` → `KIMI_CENSUS_SELFTEST: 43/43 pass` / `VERDICT: PASS` exit 0 [O-SCRT]. Re-run 2026-10-14 (TAMESHI-SCR-T) |
| 4 | operability | the tool (r3-2, 611 lines) ran any spec but could not check itself: selftest 24/24 measured the engine against a synthetic fixture only; the two worked cases were re-runnable only by hand-cut specs; an edit to the tool had no recorded-result regression gate | the tool ships its own regression gate (`--regression`, r4-2; 611 → 1001 lines): re-runs BOTH worked cases over fresh copies of the pinned fleet artifacts — embedded specs = the notes' §7 edits (all 20 @old strings re-verified count==1 against the live bytes), recorded tables (10 defects each, killed 8 / survived 2), revision pins enforced (js `83016d45…` / bash `275d8294…`; a live mismatch is a SETUP refusal — the table is revision-tied), stated band (|killed−8| ≤1, ≤1 verdict flip, defects exactly 10, inconclusive 0, control green, `MUTATE_RESTORE: OK` required), exit map 0 PASS / 1 FAIL / 2 SETUP, `--keep`, `--target/--defects/--suite/--label` refused (usage, exit 64); selftest **24 → 37/37** (adds: in-band fixture PASS, doctored-table FAIL naming each flipped row, pin-mismatch + missing-target SETUP, fixture byte-identity after the regression fixture runs, arg refusal); measured live: `REGRESSION: PASS (cases=2 passed=2; band killed-delta<=1 flips<=1)`, both `REGRESSION_TABLE … match=10/10 … kill-rate=80%` flips=0, `MUTATE_RESTORE: OK` ×2 (sha before=after), fleet trees porcelain-clean after, 19 s, exit 0 | `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 37/37 pass` / `VERDICT: PASS`, exit 0 [O-SCRT]; `sha256sum tools/mutate-and-run.sh` → `597e1419…331b` (1001 lines; uncommitted at draft time — the revision SCR-T verified) [O-SCRT]; regression run + retained evidence `/tmp/w4-scrt-regression/` (per-case `sweep.log` carries `MUTATE_RESTORE: OK` ×2 with sha before=after, `results.tsv` per case) → `REGRESSION: PASS …` exit 0 [O-SCRT]; kagi/kumitate `git status --porcelain` empty after the run; pins re-read held after [O-SCRT]. Re-run 2026-10-14 (TAMESHI-SCR-T) |

**R4-4 landed as §13 of the matrix note** (not a separate file; recorded
mtime 13:25:53, present at this lane's 13:40 re-check — §C.9 ordering
caveat): a static projection
onto kumitate `round-gate.mjs` @ `f890e277…`, 1511 lines — 14 finding kinds
14/14 statically covered by the suite's one meta-check (`:1487-1493`), 7
declared fail-closed tokens over 10 call sites / 6 tokens hand-asserted (1
token + 2 call-site species uncovered), full-line anchored verdict parse
(`:862-868`, tighter than either measured case), §13.6 uncovered set, §13.9
PU1–PU5, §13.10 spot-checks — explicitly **projection, NOT measurement**;
nothing admitted, PROVINCE's 2-lane bar untouched. It is already spliced into
the calibration row above; keep the projection/measurement distinction
verbatim wherever the parent moves it.

## B. LOG.md — round-4 entry (append as a new bullet after the round-3 entry)

- 2026-10-14 — round 4: planned as a ufo-round-plan (`plans/round-4.plan.md`,
  ufo-round-plan-v1 — axis move **calibration** (suite-vs-arm completeness
  across the two worked cases) + the tool's `--regression` mode; claim:
  a cross-case re-cut of the two kill tables BY ARM CLASS yields the
  protected/not-protected matrix; anti-claim pre-registered: a per-class
  disagreement IS the finding, never averaged). Same dispatch shape as rounds
  1–3 — lane write-scopes left this LOG to the scribe; no
  `.ufo/waves/tameshi-r4-*` directory exists (checked 2026-10-14), so the lane
  deliverables in this repo ARE the wave record (observation). Content lanes:
  TAMESHI-R4-1 → `corpus/knowledge/arm-class-matrix.md` (498 lines, 497
  `wc -l`, final line unterminated; sha256 `4df037f7…`; §13 appended by R4-4
  at 13:25:53): the two kill tables
  re-cut by arm class — 7 classes (A verdict paths · B fail-closed arms · C
  counts · D reported-but-unasserted · E unreached arms · F coordinated edits ·
  G behavior predicates), all 20 mutants placed; ledger 16 killed / 4 survived
  / 0 inconclusive (both suites 8/10); survivors fall in exactly two classes —
  reported-but-unasserted surfaces (JS D2/D10, bash B10) + unreached arm (bash
  B5); admission table on PROVINCE's 2-lane bar: 5 admitted (reported-but-
  unasserted surfaces; verdict-stem protected/remainder unasserted; fail-closed
  exit-map narrow; asserted counts; behavior predicates), 1 proposed
  (unreached-arm survivor — single instance, JS counter-instances D4/D5 bound
  it), 1 unknown (coordinated edits); the anti-claim's findings recorded not
  averaged — pin style (JS pins one whole CLEAN line by equality; bash pins no
  line weight above a substring), fail-closed arm species (environment failure
  vs malformed-input refusal), kill width (16/43 vs ≤3/16; per-case fresh
  fixtures + exit/token asserts vs shared fixtures + exact-line asserts);
  errata E1 (pre-write model expected the disagreements only in unreached arms
  + coordinated edits; measured set is wider) and E2 (D2/B10 dual-listed by
  design, totals stay 20/16/4); U1–U6 (coordinated edits unmeasured; D2
  boundary bounded not closed; bash verbs-path mutants host-gated; no third
  gate/language; drift + cross-host stability unmeasured; class membership is
  (I)); §12 three spot-check groups (JS assert tiers, bash assert grammar,
  live pulses) re-read on the pinned bytes.
  TAMESHI-R4-2 → `tools/mutate-and-run.sh` r4-2 (611 → 1001 lines, sha256
  `597e1419…`; uncommitted at draft time): the tool's own kill-rate regression
  gate — `--regression` re-runs BOTH worked cases over fresh copies of the
  pinned fleet artifacts (embedded specs = the notes' §7 edits; recorded tables
  10 defects each at 8/10; revision pins enforced, mismatch = SETUP refusal),
  stated band (|killed−8| ≤1, ≤1 flip, defects exactly 10, inconclusive 0,
  control green, restore OK), exit map 0/1/2, `--keep`, target/defects/suite
  args refused; selftest **24 → 37/37**; measured live 2026-10-14 by the scribe:
  `REGRESSION: PASS (cases=2 passed=2 …)`, js+bash `match=10/10 … kill-rate=80%`
  flips=0, `MUTATE_RESTORE: OK` ×2, fleet trees clean, 19 s.
  TAMESHI-ERR-T → `corpus/knowledge/verification-patterns-fleet.md`,
  append-only `## Errata (round 4)` (34588 → 39663 B; the old blob is a
  byte-prefix of the new file, verified this draft): V-R4-1 the g2d extension's
  substrate moved (`9fb50aa9` → `1275746c`, 10 commits; corpus/live verifier
  files 51 → 56, report rounds 11 → 15, LOG 778 → 863 lines) — state pins
  refreshed, every cited line re-resolved, the extension's prediction not
  falsified; flags `corpus/README.md:12` (stale revision text) without editing;
  V-R4-2 the P5 citation `SHONEN.md:14` → `:36` (the round-2/3 rewrites moved
  the header-pins line; PROTOCOL.md:419-428/:430-431 held); V-R4-3 AXES.md
  ranges corrected (table `:9-16`, adjacency `:16`) and spec.json seat label
  corrected (`:15` = audio-scout; author `:21`).
  ⧗ TAMESHI-R4-3 → `SKILL.md` calibration append: NOT LANDED in-tree at this
  draft's poll close (13:44); /tmp draft (`/tmp/tameshi-r4-3-draft.md:1-45`):
  an arm-class table aligned to the R4-1 note, a mutation-pass trigger list
  (case-set/assert edits; reported-but-unasserted surfaces; fixture-reach
  unproven; tool edits), pre-registered falsifiers (a)–(d), confidence
  statement. Parent: fold in with the landed line count + sha256.
  TAMESHI-R4-4 → §13 of `corpus/knowledge/arm-class-matrix.md` (appended
  13:25:53; §§0–12 unchanged): a static projection of the matrix vocabulary
  onto kumitate `round-gate.mjs` @ `f890e277…` (1511 lines) — 14 finding
  kinds, 14/14 statically covered by the suite's one meta-check; 7 declared
  fail-closed tokens over 10 call sites, 6/7 hand-asserted with 1 token + 2
  call-site species uncovered; 4 verdict families incl. a full-line anchored
  parse (tighter than either measured case); §13.6 uncovered set, §13.9
  PU1–PU5, §13.10 three read-only spot-checks; nothing admitted, PROVINCE's
  2-lane bar untouched. **Projection, NOT measurement** — kept verbatim.
  Audits: no separate non-author audit lane landed in-tree at this draft's
  poll close; the in-tree evidence is the matrix's §12 spot-check block (plus
  §13.10 for the projection), the tool's `--regression` self-gate, and the
  scribe's independent re-run of it (below). If a round-4b audit batch lands, fold its named verifiers here.
  Scribe verification (this entry, TAMESHI-SCR-T draft, all re-run 2026-10-14;
  scratch `/tmp/w4-scrt-*`): `bash tools/mutate-and-run.sh --selftest` → 37/37
  PASS exit 0; `--regression --workdir /tmp/w4-scrt-regression` → PASS exit 0,
  both cases `match=10/10` `kill-rate=80%` flips=0, restore OK ×2 (sha
  before=after), kagi + kumitate trees porcelain-clean; fleet pulses green
  (`surface-census.sh --selftest` → `SELFTEST: PASS (16 cases)`, skip 15/16
  substrate-absent; `kimi-census.mjs --selftest` → `KIMI_CENSUS_SELFTEST:
  43/43 pass` / `VERDICT: PASS`); matrix tallies re-counted (20/16/4; 7 rows;
  5+1+1 admissions; U1–U6; E1–E2; §13 PU1–PU5); anchors re-read
  (`kimi-census.mjs` :498-499/:511-512/:526; `surface-census.sh`
  :747-760/:862/:866/`-x ` :214; round-gate §13's `f890e277…`/1511 lines,
  `failClosed(` 10 sites, FINDING_KINDS `:171-176`, meta-check `:1487`);
  ERR-T's append-only block proven by byte-prefix (34588 B old = prefix of
  39663 B new) and V-R4-2 re-checked (`sed -n '14p;36p' SHONEN.md`; g2d HEAD
  `1275746c`).
  SCORECARD round-4 moves: calibration improved (the two-case comparison
  becomes the 7-class matrix with an admission table, the disagreements named
  and the unknowns bounded; counting commands in the move-log row);
  operability improved (the tool gains its own regression gate over both
  recorded cases — selftest 37/37, live PASS 2/2; counting commands in the
  move-log row).
  Carried to round 5 (recommendations, not absorbed): matrix U1–U6 (coordinated
  edits; D2 boundary; bash verbs-path host gate; no third gate/language — the
  50 % band and both interiors still unmeasured; drift/cross-host stability;
  class membership is (I)); R4-4's §13 projection awaits
  its measured sweep (a third-gate measurement would also test rows D/E on a
  shape the matrix has not seen); sibling-owned items stay recorded-not-
  absorbed (kumitate integration groups + `INTERNAL_ERROR` arm — now with the
  static projection; kagi live verdicts 5/6 + F-2's two-lines-per-path fix);
  `corpus/README.md:12` stale g2d revision text (ERR-T flagged; decide fix vs
  leave at round close).

## C. SCR-T evidence ledger (all commands re-run by this lane 2026-10-14; scratch `/tmp/w4-scrt-*`)

1. Tool selftest: `bash tools/mutate-and-run.sh --selftest` →
   `MUTATE_SELFTEST: 37/37 pass` / `VERDICT: PASS`, exit 0.
2. Tool regression: `bash tools/mutate-and-run.sh --regression --workdir
   /tmp/w4-scrt-regression` → exit 0, 19 s:
   `REGRESSION: PASS (cases=2 passed=2; band killed-delta<=1 flips<=1)`;
   `REGRESSION_TABLE js-kimi-census: match=10/10 recorded-killed=8
   measured-killed=8 survived=2 inconclusive=0 flips=0`; same for
   bash-surface-census; `REGRESSION_SWEEP … kill-rate=80%` ×2;
   `grep 'MUTATE_RESTORE' /tmp/w4-scrt-regression/*/sweep.log` → 2× `OK`
   (kimi-census `83016d45…` before=after=pristine; surface-census
   `275d8294…` before=after=pristine).
3. Fleet trees untouched: `git -C kagi-shokunin status --porcelain` empty
   before/after; same for kumitate after; pins re-read held.
4. Fleet pulses: `bash kagi-shokunin/corpus/surface-census.sh --selftest` →
   `SELFTEST: PASS (16 cases)` exit 0, cases 15/16 `skip-case …
   substrate-absent`; `node kumitate-shokunin/scripts/kimi-census.mjs
   --selftest` → `KIMI_CENSUS_SELFTEST: 43/43 pass` / `VERDICT: PASS` exit 0.
5. Matrix tallies (arm-class-matrix.md @ 498 lines / 497 `wc -l`, final
   unterminated; sha256 `4df037f7…`, 36706 B; **re-checked after R4-4's §13
   append at 13:25:53** — the append adds no D/B ledger rows): 20 ledger rows,
   16 killed / 4 survived; 7 matrix rows (A–G); 7 admission rows; U1–U6;
   E1–E2; §13's PU1–PU5 and row projections 13.1–13.8.
6. Anchor re-reads on the pinned bytes: `sed -n '498,499p;511,512p;526p'
   kumitate-shokunin/scripts/kimi-census.mjs` → DRIFT prefix assert / exact
   CLEAN equality / `j.totals.frozen.K5 === 3`; `sed -n '747,760p'
   kagi-shokunin/corpus/surface-census.sh` → `run_case` = exit + one substring
   token; `sed -n '862p;866p'` → the CLEAN/DRIFT summary arg lists;
   `grep -n -- '-x '` → `:214` only (inside B5's arm).
7. ERR-T block: old blob (`git show HEAD:corpus/knowledge/
   verification-patterns-fleet.md`, 34588 B) is a byte-prefix of the new file
   (39663 B) → append-only held; `grep -n '^## Errata (round 4)\|^\*\*V-R4-'`
   → block at `:235`, V-R4-1 `:253`, V-R4-2 `:282`, V-R4-3 `:292`;
   V-R4-2 re-check `sed -n '14p;36p' SHONEN.md` → `:14` inside the end-to-end
   box, `:36` = header pins; V-R4-1 re-check `git -C game-dev-2d-shokunin
   rev-parse HEAD` → `1275746cedfa314246755a81b4ab60e57075df98`
   (2026-10-14 12:51:17, "r73 report-last + simplifier-fold …").
8. R4-4's §13 anchors (landed; re-checked by SCR-T on the pinned bytes):
   `sha256sum kumitate-shokunin/scripts/round-gate.mjs` → `f890e277…`, 1511
   lines; `grep -n 'failClosed('` → emission sites `:527 :531 :536 :644 :647
   :652 :683` (+ def `:596`, `:656`); `grep -n 'INTERNAL_ERROR'` → doc `:117`,
   emission `:683`; `sed -n '171,176p'` → 14 FINDING_KINDS; meta-check
   `:1487`; `grep -n '^## 13\|^### 13\|^\*\*13\.'` → §13 at `:298`, 13.1–13.10
   present.
9. Landing catch (ordering caveat): at ~13:30 this lane's checks still read
   the pre-§13 bytes (sha `39d3361b…`, 295 `wc -l`); by the 13:40 re-check the
   note read 498 lines / `4df037f7…` with a recorded mtime of 13:25:53.
   `git status --porcelain` does not surface untracked-file content edits, so
   the landing was invisible there; the recorded mtime reads earlier than this
   lane's last old-byte check, so treat file mtimes as unreliable for ordering
   this landing — the §13 content itself was verified present at 13:41 and the
   tallies above were re-run on those bytes.

## D. Parent checklist (round close)

- Fold ⧗ R4-3 when it lands: SKILL.md sha256 + line count change (currently
  `dd2f4dee…3753`, 665 lines — still the r3 revision). R4-4 already landed as
  §13 of `arm-class-matrix.md` (the row cites `4df037f7…` / 498 lines); keep
  "projection ≠ measurement".
- `corpus/README.md`: add a coverage-map row for `arm-class-matrix.md` (and a
  row for the ERR-T errata block if the precedent holds; round-2 addenda rows
  exist). Also `corpus/README.md:12` carries the stale g2d revision text
  ERR-T flagged (V-R4-1) — decide fix vs leave, record either way.
- `SHONEN.md`: probation completed at round 3; round 4 adds no new box —
  roster-row decision is fleet-level (MINT.md). Historical citations of
  `SKILL.md dd2f4dee…` / 665 lines in SHONEN/README refer to the revision the
  executor ran — do not rewrite if R4-3 lands.
- Commit at close (lane identity + round shape; precedents `2587e0a`
  round-2, `53e74a8` round-3): include `plans/round-4.plan.md`,
  `corpus/knowledge/arm-class-matrix.md`, `tools/mutate-and-run.sh` r4-2,
  `corpus/knowledge/verification-patterns-fleet.md` (ERR-T block), this
  draft's finalized record, plus R4-3's SKILL append if landed (R4-4's §13 is
  inside the matrix note already listed); `plans/round-5.plan.md`
  is the next round's plan (L1; 60 `wc -l`, sha `452b9cc0…`, mtime 13:26:18
  as of this draft's close) — its own commit item,
  not part of the round-4 record.
- The tool revision SCR-T verified is sha256 `597e1419…331b` (1001 lines);
  if the tool is edited again before commit, re-run §C.1–C.2 and update the
  row's evidence.

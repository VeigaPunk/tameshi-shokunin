# T54W1ScribeScorecard — SCORECARD.md additions for round 54 (draft for L1 TameshiR54a2)

Seat: scribe, axis calibration, milestone "SCORECARD rows draft".
Everything below is measured at the content commit C0
`59c38109bf119d0e9d4f878644a82babc937bc1e` (or at the revision the cell names) by
this seat's own read-only runs; no lane file was edited. The `After` cells are
placeholders the L1 fills from the deciding receipts, never from this draft.

Scratch used: `/fast/scratch/hyaku/tameshi-r54/T54W1ScribeScorecard/`
(`HYAKU_SCRATCH=/fast/scratch/hyaku`), no writes outside
`.ufo/waves/round-54/w1/`.

---

## 1. Round header (draft prose)

## Round 54 — cold-read floor repair (calibration) + one scratch-root exit class (operability) (2026-10-28)

L1 TameshiR54a2, hyaku run 11, attempt 2. Base
`d33053f7552db4bd290c99a36979760f544c41ad`, the round-53 closure tip. Two claims
on distinct axes, pre-registered with both counters, the controls harness, 14
no-harm monitors and the deciding script in `.ufo/evidence/round-54/contract.json`,
frozen at `441c26bec5e4c1cc31bc2a840f311cb8d1965259`
(`.ufo/evidence/round-54/freeze.json`) before any seat ran; `amendments: []`
(attempt 1 left nothing behind, per `corpus/lessons/round-54.md`).
Shape: one v2 wave (band 64–128) plus at most one residual call;
`.ufo/waves/round-54/spec-w1.json` lists 76 items (27 scribe, 13 executor,
12 mutation-tester, 5 reviewer, 4 scout, 4 critic, 4 sentinel, 3 revenger,
2 connector, 2 simplifier). All content edits landed first in one commit, C0
`59c38109bf119d0e9d4f878644a82babc937bc1e`, which descends from the freeze
(`git merge-base --is-ancestor 441c26b 59c38109` exit 0); under the round's
method (`corpus/lessons/round-54.md` § The method) the readers read the final
bytes and the deciding run re-derives every number from the committed tree.
Calibration (8) is the lowest non-retired axis and carries C1; C2 works
operability, which carries no numeric score.

## 2. Standing axis table — re-stated at C0 (`59c38109`)

The round-50 table (`SCORECARD.md:2416`, "Standing axis table — re-stated at
round 50") is the standing table; this restatement supersedes its values as the
standing values and nothing above is rewritten. Each row quotes the command that
yields the number and what that command printed at C0. A value the same command
does not print at C0 is marked **not reproduced** rather than carried silently.

| Axis | Score (0–10) | Evidence / counting rule | At C0 (`59c38109`) | Last-change round |
|---|---|---|---|---|
| depth | 10 | command D over the leg ledger, capped at 10: `git show REV:tools/mutate-and-run.sh \| python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js\|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))'` | `recorded_cases=10 depth_score=10` | 51 (tenth recorded case) |
| calibration | 8 | `python3 .ufo/evidence/round-21/coldread/measure.py --repo LANE --rev REV` → `calibration_restraint_score` (2 points per asserted SHONEN box; 8 = all four, the ceiling) and `coldread.sections_covered`; any lost/blocked section vetoes the score to 6 | `score=6 covered=41` — **not reproduced**. The 6 is the coldread veto, not a graded drop: all four boxes are asserted (`shonen.marks=['~','~','~','~']`, `box3_ledger_link=true`) and `coldread.reasons` shows `credited: 41` plus `input-drift:` classes — `corpus/SOURCES.md`, `tools/registry.json`, the four tools this round edited (`tools/bash-witness-study.py`, `tools/env-diff.py`, `tools/evidence-disposition.py`, `tools/pin-disposition.py`), plus `.ufo/evidence/round-15/verify.py` and `corpus/knowledge/service-limits.md` (receipt `.ufo/waves/round-54/w1/T54W1ScribeScorecard-receipts/calibration-at-rev.txt`). The latest revision this seat verified printing 8 is `e3729de8` (`score=8 covered=64`); `88afa941` prints 6/58 and `d33053f7` prints 6/57 | 49 measured, 50 restated; round 53 claimed 8 in prose only (see §6) |
| freshness | 9 | `python3 .ufo/evidence/round-45/freshness/measure.py --lane LANE --rev REV \| tail -1` → `score = (10*fresh)//population` | `self_pin=1 population=74 entries=73 verified=73 drifted=0 unreachable=0 invalid=0 unreviewed=0 disputed=2 fresh=71 score=9 target=50 ... C1_R45_PASS=true` (710//74 = 9) | 48 (restated) |

Note on the freshness cell: the round-50 table wrote the rule as
`floor(10 * fresh / 73)`; the population has since moved to 74 (S274, round 52)
and the counter computes `score = (10 * fresh) // len(pop)`
(`.ufo/evidence/round-45/freshness/measure.py:255`), so the rule cell should read
`(10*fresh)//population`, not `/73`.

## 3. Claim rows (targets condensed from the contract; `After` placeholders)

The exact predicates are in `.ufo/evidence/round-54/contract.json`; the cells
below condense them without narrowing them. The `Before` numbers are the
pre-registered CTL_0 lines (`.ufo/evidence/round-54/control/controls-a.stdout`,
untracked at this seat's read — gate 0 of the deciding run requires it committed
at REV).

| Claim | Axis | Before (CTL_0, freeze bytes) | Target | Counting command | After (deciding receipt) |
|---|---|---|---|---|---|
| C1 — the cold-read floor reads 64/64 credited at the deciding revision; the seven base-lost headings each carry a fresh entry bound under `rekey-r54-<c0>` that credits, every entry's reader report pins the section's bytes at `<c0>`, and no re-key entry pins `LOG.md` or `SCORECARD.md` | calibration (8; surface: the cold-read floor) | `CTL_0_c1 C1_R54: rev=d33053f7552d c0=none credited=57 lost=7 rekeyed=0/7 readers=0/7 monitor=6/57 unstable=0 total=4 C1_R54_PASS=false` (`.ufo/evidence/round-54/control/controls-a.stdout`). At C0 the same counter reads `credited=41 lost=23` — the round's own edits drifted 23 headings (`.ufo/evidence/round-54/c1/lost-headings-at-c0.json`, 23 entries; the frozen seven are `c1/lost-headings-at-base.json`) | `C1_R54_PASS=true`: frozen round-48 precheck prints `cand_credited=64 lost=0 ok`, the unchanged round-21 selector reads `covered=64 score=8`, all seven base-lost headings re-keyed and reader-bound at `<c0>`, no `LOG.md`/`SCORECARD.md` input | `python3 .ufo/evidence/round-54/c1/measure.py --lane LANE --rev REV --work EMPTY_DIR --explain` | `<fill from .ufo/evidence/round-54/after/c1.stdout>` |
| C2 — one scratch-root exit class across the seven `strict_scratch_root()` tools: 7/7 self-tests exit 2 (could-not-evaluate, naming the TMPDIR value, no traceback) on a set-but-unusable TMPDIR, 7/7 exit 0 on `TMPDIR=""` and on a usable root with no mkdir under `/tmp`, the seven registry rows carry the `scratch_root` cell, and the note cites S277–S279 opened 2026-10-28 | operability (no numeric score; surface: the scratch-root exit class) | `CTL_0_c2 C2_R54: rev=d33053f7552d tools=7 unusable_exit2=3 naming=7 empty_ok=7 usable_ok=7 tmp_mkdirs=0 docs=0 note=0 sources=0 total=13 C2_R54_PASS=false` (same receipt) | `C2_R54_PASS=true` at every arm (contract target; any arm short of 7/7 makes it false) | `python3 .ufo/evidence/round-54/c2/measure.py --lane LANE --rev REV --work EMPTY_DIR --explain` | `<fill from .ufo/evidence/round-54/after/c2.stdout>`. This seat's C0 run reads `C2_R54: rev=59c38109bf11 tools=7 unusable_exit2=7 naming=7 empty_ok=7 usable_ok=6 tmp_mkdirs=0 docs=7 note=1 sources=3 total=1 C2_R54_PASS=false` — every arm is full except `usable_ok=6`, whose single failure is `usable registry-check rc=1` (the strace timing case; §5). `sources=3` is S277, S278 and S279 all cited, mined and gate-cited; `docs=7` is the seven registry rows |

Controls: phase A is 5/5 as pre-registered
(`.ufo/evidence/round-54/control/controls-a.stdout`: CTL_0_c1 false, CTL_0_c2
false, CTL_R53 false, CTL_FAB false, CTL_LOGINPUT false; exit 0 in
`controls-a.exit`). Phase B (`CTL_POS_c1`, `CTL_POS_c2`, `CTL_EXIT0`) is **not
yet receipted at C0**: `controls.sh` defines it
(`.ufo/evidence/round-54/control/controls.sh:141-167`) but no
`controls-b.stdout` / `controls-b.exit` exists, and `deciding-run.sh` gate 0
requires all four receipts committed at REV in a commit descending from FREEZE
(`deciding-run.sh:22-26`).

What the counters cannot see (contract `cannot_see`, carried verbatim in
substance): C1 — whether a reader's judgment of a section is fair, and whether a
re-keyed entry's inputs are the ones the reader actually needed; C2 — whether a
tool's self-test exercises the branch that allocates scratch on its real path,
and whether a registry cell describes the tool as it now behaves beyond the three
named arms. The wave's adversarial re-reads and the L1's disclosed adjudications
stand in for the first; the second stays unmeasured.

## 4. Capabilities

Capabilities: none claimed this round. C1 moves the calibration surface (the
cold-read floor) and C2 moves operability, which carries no numeric score; depth
and freshness are unchanged.

## 5. Planned (round 55)

Carried from round 53 (its `Planned (round 54)` line plus the closure's routed
defects that are still open at C0):

- **R53.2 / R53.3 / R53.4 / R53.5 — evidence-layer records.** Round-53's deciding
  receipts were never committed (R53.2); its phase-B `CONTROLS_B:` tally receipt
  did not exist (R53.3); its C2 receipt named a scratch-clone revision (R53.4);
  its freeze receipt was two amendments stale (R53.5). Round 54 anchors the
  round-53 counter output at the committed revision `88afa941` in
  `.ufo/evidence/round-54/control/r53-counter-at-88afa941.stdout`, but that file
  is **untracked at C0**, so the record is not yet closed; the same discipline
  (receipts at committed revisions, committed before the close) applies to
  round-54's own `after/` and to its phase-B receipt (see below).
- **R53.7 — the "inputs pinned at C7" claim.** The closure's words: "11 of 11 747
  rekey input keys pin at the reader's read_rev or fix-pass-2 (`5b703c6f`, file
  changed again at `ceb372c`) rather than C7 `8f474419`"
  (`corpus/lessons/round-53-verifier-spotcheck.md`). Restate the claim or re-pin.
  Round 54's C1 target re-binds inputs under `rekey-r54-<c0>` but does not
  address the round-53 record.
- **R53.8 — the S275 locator.** At C0 `corpus/SOURCES.md:150` still reads `p. 4`
  in the anchor cell; the closure found the quote on physical page 3 (printed
  footer 1787) with the `pdftotext` line anchor exact. (The lane working tree
  carries an uncommitted edit to that row at this seat's read; C0 does not.)
- **R53.1 — the round-53 counter's pathspec and the `total=6` record.** The frozen
  round-53 bytes still discover re-key directories non-recursively
  (`rekeyed=0/30`); the round-54 anchor receipt prints the counter's real line
  `total=37`, so the record should quote 37 and the frozen bytes stay immutable.
- **Round-53 reader nits:** the remaining locator imprecision in what-stays-open;
  the recipe's restore-discipline anchors (377-378) re-verified at their heading;
  the `service-limits.md` §5 U1 heading anchor re-read.
- **The 84 remaining staged `merge/tameshi` entries** (85 at round 53; this round
  refused `delta-debugging-minimization-contract.md` on capacity): next-ranked
  `delta-debugging-minimization-contract.md` — its subject, a stated minimality
  witness, matches the round-50 shrinker's `cannot_see` line — then
  `r8-predictive-test-selection-cost.md`.
- **considerthese proposals 2–5** (proposal 1, the contract-debt table, was mined
  into this round's planned line; at most one per round).
- **Closed by C0, not carried:** round-53's C2 follow-on «TMPDIR empty-string
  semantics documented in the registry rows» is done — the seven rows' new
  `scratch_root` cells state the three arms (TMPDIR unusable → exit 2
  could-not-evaluate; empty → unset; usable → no `/tmp`), so the C2 counter's
  `docs=7` arm is full at C0.

What C0 leaves open (each measured at `59c38109`):

- **The re-read set and its binder.** 23 headings are credit-lost at C0
  (`.ufo/evidence/round-54/c1/lost-headings-at-c0.json`; the frozen seven are
  `c1/lost-headings-at-base.json`); the C1 counter at C0 prints
  `rekeyed=0/7 ... readers=0/7`, so no `rekey-r54-<c0>` directory and no reader
  report exist yet. Neither `c1/lost-headings-at-c0.json` nor `integrate/binder.py`
  is in the C0 tree (both untracked at this seat's read). At base the drift set
  already includes `LOG.md` and `SCORECARD.md`
  (`…receipts/calibration-at-rev.txt`) — the round-53 failure mode the C1
  counter's `unstable` arm forbids for this round's entries.
- **Control receipts.** At this seat's read the tree has only
  `control/controls-a.stdout` and `control/controls-a.exit`, both untracked;
  `controls-b.*` are absent. Gate 0 of
  `deciding-run.sh` refuses (exit 3, nothing run) until all four are committed at
  REV in a commit descending from the freeze.
- **Before/after receipts.** `.ufo/evidence/round-54/before/` is empty and
  `after/` absent at C0, while the contract's C1 and C2 `before` cells cite
  `.ufo/evidence/round-54/before/c1.stdout` and `before/c2.stdout`; those files
  must be produced by the deciding run or the pointers corrected to the control
  receipts (the numbers themselves are in `controls-a.stdout`).
- **C2's usable arm is load-sensitive (new, measured).** `registry-check`'s
  self-test runs two timeout-kill cases against a `elapsed < 3.5` budget
  (`tools/registry-check.py`, `run_escape_case`), and the C2 counter runs every
  self-test under `strace -f` (`.ufo/evidence/round-54/c2/measure.py`, usable arm).
  Under that wrapper the two cases took `elapsed=6.015s` and `elapsed=6.559s`
  (FAIL), reproduced in a second strace run (`FAIL (2 of 51 cases: …)`), while
  unstraced on the same clone they took `1.692s` and `1.677s` (PASS). So
  the seat's non-deciding run at base read `usable_ok=6 ... total=14` against the
  control receipt's `usable_ok=7 ... total=13`, and the same run at C0 reads
  `usable_ok=6 ... total=1 C2_R54_PASS=false` — the whole C0 verdict turns on this
  one arm. The deciding run can lose C2 to machine load unless
  the arm exempts timing cases or the budget is raised; this is a counter /
  reproducibility decision for round 55, not a claim change.

## 6. Record corrections this restatement makes (no earlier prose is edited)

- **The round-53 close's "calibration 8 (restored, was harmed at base)".** The
  same paragraph's frozen counter printed `credited=58 lost=6`
  (`.ufo/evidence/round-54/control/r53-counter-at-88afa941.stdout`), and the
  round-21 monitor prints 8 only when the coldread veto is clear: this seat's runs
  of the same command print 6 at 57/64 (`d33053f7`), 6 at 58/64 (`88afa941`) and
  6 at 41/64 (`59c38109`), and 8 only at `e3729de8`'s 64/64. The defensible reading is
  "the floor moved 45 → 58; the score stayed 6 until 64/64". The restated table
  above therefore shows 8 as the standing ceiling with `score=6 covered=41` at
  C0, not as a reproduced C0 value.
- **The round-53 close's `total=6`.** The frozen counter's own line at
  `88afa941` is `... total=37 C1_R53_PASS=false`; the anchor receipt is
  `.ufo/evidence/round-54/control/r53-counter-at-88afa941.stdout`.

## 7. Provenance — every number and the exact command that yields it

All commands were run by this seat read-only against the lane's git objects; the
work directories were fresh and empty under the seat scratch. `LANE` below is
`/home/vgpnk/Projects/shokunin/tameshi-shokunin`. The raw counter outputs are
committed beside this file under
`.ufo/waves/round-54/w1/T54W1ScribeScorecard-receipts/`
(`c1-at-base.explain.txt`, `c1-at-c0.explain.txt`, `c2-at-base.explain.txt`,
`c2-at-c0.txt`, `calibration-at-rev.txt` — a field extraction from the four
round-21 JSON runs, `freshness-at-c0.txt`, `depth-at-c0.txt`,
`regcheck-strace.out.txt`, `regcheck-strace2.out.txt`, `tmp-mkdirs-strace.txt`);
the seat scratch tree is removed after the receipts were copied.

| Number | Command (exact) | Output observed |
|---|---|---|
| depth 10 at C0 | `git show 59c38109bf119d0e9d4f878644a82babc937bc1e:tools/mutate-and-run.sh \| python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js\|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))'` | `recorded_cases=10 depth_score=10` (also 10 at `d33053f7`) |
| calibration at C0 | `python3 .ufo/evidence/round-21/coldread/measure.py --repo LANE --rev 59c38109bf119d0e9d4f878644a82babc937bc1e` | `score 6 covered 41`; `shonen={'asserted': 4, 'box3_ledger_link': True, 'marks': ['~','~','~','~']}`; `reasons` = `credited: 41` + `input-drift:` classes |
| calibration at base | same command, `--rev d33053f7552db4bd290c99a36979760f544c41ad` | `score=6 covered=57` |
| calibration 8 reproduced | same command, `--rev e3729de862f73ae080d98fcf522a7081ce16e40a` | `calibration_restraint_score: 8`, `covered=64` |
| calibration at round-53 close | same command, `--rev 88afa9415454` | `calibration_restraint_score: 6`, `covered=58` |
| freshness 9 at C0 | `python3 .ufo/evidence/round-45/freshness/measure.py --lane LANE --rev 59c38109bf119d0e9d4f878644a82babc937bc1e` | `... population=74 ... fresh=71 score=9 target=50 ... C1_R45_PASS=true` |
| C1 before | `python3 .ufo/evidence/round-54/c1/measure.py --lane LANE --rev d33053f7552db4bd290c99a36979760f544c41ad --work EMPTY_DIR --explain` (CTL_0 of the frozen controls harness) | `cand=d33053f7552d cand_credited=57 lost=7 RED`; `C1_R54: rev=d33053f7552d c0=none credited=57 lost=7 rekeyed=0/7 readers=0/7 monitor=6/57 unstable=0 total=4 C1_R54_PASS=false` |
| C1 at C0 | same command, `--rev 59c38109bf119d0e9d4f878644a82babc937bc1e` | `cand=59c38109bf11 cand_credited=41 lost=23 RED`; `C1_R54: rev=59c38109bf11 c0=none credited=41 lost=23 rekeyed=0/7 readers=0/7 monitor=6/41 unstable=0 total=4 C1_R54_PASS=false` |
| C2 before | `python3 .ufo/evidence/round-54/c2/measure.py --lane LANE --rev d33053f7552db4bd290c99a36979760f544c41ad --work EMPTY_DIR --explain` (CTL_0) | control receipt: `tools=7 unusable_exit2=3 naming=7 empty_ok=7 usable_ok=7 tmp_mkdirs=0 docs=0 note=0 sources=0 total=13 C2_R54_PASS=false`; the seat's independent run that day: `usable_ok=6 ... tmp_mkdirs=0 docs=0 note=0 sources=0 total=14` (see §5) |
| C2 at C0 | same command, `--rev 59c38109bf119d0e9d4f878644a82babc937bc1e` | `EXPLAIN unusable registry-check rc=2 line='registry-check: could-not-evaluate: ...'` … `EXPLAIN usable registry-check rc=1 tmp_mkdirs=0`; `C2_R54: rev=59c38109bf11 tools=7 unusable_exit2=7 naming=7 empty_ok=7 usable_ok=6 tmp_mkdirs=0 docs=7 note=1 sources=3 total=1 C2_R54_PASS=false` |
| usable-arm mechanism | `cd CLONE-at-rev && TMPDIR=USABLE python3 tools/registry-check.py --selftest` vs `strace -f -e trace=mkdir,mkdirat -o LOG python3 tools/registry-check.py --selftest` (base clone `d33053f7`) | plain: `SELFTEST: PASS (51 cases)`, `timeout-kills-setsid-pipe PASS (elapsed=1.692s)`; straced: `SELFTEST: FAIL (2 of 51 cases: timeout-kills-setsid-pipe, timeout-kills-setpgid-pipe)`, `FAIL (exit=1 elapsed=6.015s ...)`, `FAIL (exit=1 elapsed=6.559s ...)`; a second strace run printed the same `FAIL (2 of 51 cases: …)` line; `mkdir` under `/tmp`: 0 |
| freeze ancestry | `git rev-parse 441c26b 59c38109 && git merge-base --is-ancestor 441c26b 59c38109` | `441c26bec5e4c1cc31bc2a840f311cb8d1965259`, `59c38109bf119d0e9d4f878644a82babc937bc1e`, exit 0 |
| re-read set sizes | `python3 -c "import json;print(len(json.load(open('.ufo/evidence/round-54/c1/lost-headings-at-c0.json'))))"` and the base twin | 23 (C0), 7 (base) |
| wave size | `python3 -c "import json;d=json.load(open('.ufo/waves/round-54/spec-w1.json'));print(len(d['items']))"` | 76 |
| census at C0 | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` | exit 0 (W04 duplicate-url warnings only); row count `git show 59c38109:corpus/SOURCES.md \| grep -cE '^ {0,3}\| S[0-9]{3,} \|'` = 139, last id `S279` |

Limits of this draft: these are non-deciding seat runs at C0, not the deciding
receipts; the `After` column and the "measured close" paragraph stay empty until
`.ufo/evidence/round-54/after/` exists. The C2 usable-arm reading differed between
the control receipt and this seat's run by one arm (§5); the L1 should resolve it
before the deciding run rather than average it.

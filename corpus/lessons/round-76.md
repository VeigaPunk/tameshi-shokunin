# tameshi round 76 — lesson

Round 76 (attempt 1), base `451ed5cb6d5f8c2bf4b3e10836e4634cfcb03ee0`
(`= origin/master`, clean tree — the round-75 non-author closure verdict
commit, `corpus/lessons/round-75-verifier-spotcheck.md`, verdict
`rejected-honest-stop`). Claims, counters, kill rules, the frozen kill matrix
and controls are frozen **before any claim data** in
`plans/round-76.plan.md` (declaration commit
`5b7bbe1afa209b477bc71872d2424f6993e5c69d`, together with the design-phase
candidates, batteries and measured matrices; one appended design-phase
correction at `be4e7c86` — a byte-level evidence repair, no predicate change,
disclosed below). Round shape: one v1 wave, 12 seats (4 executor · 1 scribe ·
1 scout · 2 reviewer · 1 critic · 1 mutation-tester · 1 connector · 1
sentinel; attack seats 4 = 33.3 %), policy
`scripts/hyaku/ufo-wave-policy.json`, band 8–16; `w1-results.json` carries 12
records, 12 seat reports, no dead seats. `labrat` is a frozen-topology seat
the validator rejects, so no labrat item exists; the planner seat stays with
the L1 per the orchestrator ruling.

Saturation state at round start (`SCORECARD.md`): scored axes depth 10,
calibration 8, freshness 9 — all at or above the saturation line 8. No
capability entered the table at round 75 (the settlement errata declined
acquisition credit), so one capability-less completed round sits inside the
stagnation window (N = 2) and the nudge does **not** fire. C2 works the
lowest scored numeric axis (calibration 8).

## Gate — the source (S006 re-opened)

**S006 — re-open, not a new row.** `shmutant README (BWBama85/shmutant)` is
already held (opened 2026-10-19, tier A `code`, status `mined`, recheck `90d`,
anchor cell `shmutant's own bash mutation verdict semantics`) at page
`currentOid 7eefc73010ad6342b80e3ed43915503e02c90618`
(`corpus/SOURCES.md:17`; re-opened with fresh quotes at round 75). This
round's two arms rest on the same document's §The three verdicts and §How a
row is run — the witness-scoped verdict (a kill is red ON THE NAMED WITNESS;
red elsewhere banks accidental; an unapplied row tests nothing) and the
refuse-what-you-cannot-apply discipline — so a second row on the same URL
would be a within-scope duplicate (CORPUS.md rule 2; the S289/S293
precedent). The curation delta is a **re-open**: S006's `used-by` cell gains
`corpus/lessons/round-76.md` and this Gate carries fresh located quotes. The
row's status, `recheck` and anchor stay as written (append-only).

- Source: shmutant README, BWBama85/shmutant. The row's canonical URL is
  <https://github.com/BWBama85/shmutant>; the document opened this round is
  the README at
  <https://raw.githubusercontent.com/BWBama85/shmutant/master/README.md>.
  Fetched 2026-11-04 (HTTP/2 `200`; HTTP date `Wed, 04 Nov 2026 03:55:07
  GMT`; 13,970 B; sha256
  `960577288ed5c5eb80f42669fcb30bf254b9a917ae2bde3a117888056ef354e2` —
  byte-identical to the round-75 receipt, so the page is unchanged; extract
  `.ufo/waves/round-76/w1/T76W1SC1/s006-extract.md`, headers
  `s006-headers.txt`; seat T76W1SC1). Header hygiene:
  `grep -ic set-cookie` → `0`; the only `authorization` occurrence is the
  `vary: Authorization,Accept-Encoding` cache directive, not a credential.
- Quote 1 (extract line 24, 6 whitespace tokens): "**witness**: the assertion
  that must fail." — a row is scored against the assertion that **must**
  fail; arm19 and ARM11 name their witness and the receipt carries the
  witness's own FAIL line (`got=printed-none-reached-comparison`).
- Quote 2 (extract line 29, 16 tokens): "| `killed` | The suite went red
  **on its witness**. The test detects the defect. |" — the verdict is
  **witness-scoped**: red is not a kill; red *on the named arm* is the kill
  (the frozen kill matrix pins which mutant dies on which arm, and the
  critic's forgery C shows a crash-killed mutant that never shows its
  witness fails exactly this test).
- Quote 3 (extract line 31, 25 tokens): "| `accidental` | The suite went
  red, but not on its witness. Caught by accident, not by the assertion that
  claims to cover it. |" — an accidental red banks as accidental, never as a
  kill; the battery is adjudicated per named arm, not by exit colour alone.
- Supporting locator (the C1 fixtures rest on it): the `unapplied` row
  (extract line 38, 17 tokens): "| `unapplied` | The old literal matched
  nothing. The row injected no defect and tests **nothing**. |" — a row that
  cannot apply its binding is a refusal, never a pass; the same discipline
  is what `record-printed-absent`, `printed-not-in-span` and the selfstate
  setup refusals implement.
- **Admit:** S006's witness-scoped re-open (the four located quotes above;
  the row's status, recheck and anchor stand as written).
- **Reject (standing, re-sampled):** a new `shmutant` row at the current
  bytes — same URL, same document, within-scope duplicate (CORPUS.md rule 2;
  the S289/S293 and S073/S103 precedent; exactly one row holds the shmutant
  URL, verified by the scout). Flip condition: S006 is retired or the README
  is superseded by a new document.
- S006 `used-by` old → new:
  `corpus/knowledge/witness-scoped-kill-verdict.md, corpus/knowledge/mutation-score-semantics.md, corpus/lessons/round-12.md, corpus/lessons/round-75.md`
  → the same plus `corpus/lessons/round-76.md`.

### Gate — census

Start: exit 0, 164 rows (`.ufo/evidence/round-76/census-start.txt`; the
standing warning set: 18 × `W04` duplicate-url across scopes + 1 × `W01
S101`; final line `tameshi	ok	…`). End: exit 0, 164 rows
(`.ufo/evidence/round-76/census-end.txt`; no SOURCES row is added — S006
re-opened in place, its `used-by` cell extended; warnings only, the standing
set). Next unused id: S305 (confirmed by the scout: row ids top out at
S304).

## Claims

### R76-C1 — operability: the two round-75 survivors become measured arms

**Before** (measured at base; all four lines verbatim in
`.ufo/waves/round-76/l1/base-survivors.txt`, receipts
`mut-base-bypass.out` / `mut-base-docrev.out`): pristine
`WAVE_RECONCILE_SELFTEST: 18/18 pass` (tool sha256 `bf10c0e4…`) and
`SELFSTATE_SELFTEST: 10/10 pass` (tool sha256 `3b096763…`); the bypass
mutant on base bytes reads `18/18 pass`; the doc-rev-ignored mutant on base
bytes reads `10/10 pass`.

**After** (measured on the landed bytes at `4af6695f`, receipts
`.ufo/evidence/round-76/`): `WAVE_RECONCILE_SELFTEST: 19/19 pass` exit 0
(`c1-landed-selftest-wr.txt`); `SELFSTATE_SELFTEST: 11/11 pass` exit 0
(`c1-landed-selftest-ss.txt`); the lane runner over the landed spec prints
`CONTROL: GREEN`, `MUTATE_RESTORE: OK` (target sha256 identical
before/after/pristine = `ca05ec15…`, the landed bytes) and
`MUTATE: DONE (target=wave-reconcile-arms-r76 defects=7 killed=7 survived=0
inconclusive=0 kill-rate=100%)` (`c1-landed-battery.txt`). The frozen
matrix holds row-for-row: `m2` → arm13 + arm16 (r75 collateral, unchanged);
`span-rule-removed` → arm14 + arm17 + arm18 (unchanged);
`seat-reports-any-depth` → arm15; `mc-record-bound` → arm16; `roles-bypass`
→ arm17; `attack-bypass` → arm18; `adv-seatreports-require-printed-bypass`
→ **arm19 only**, FAIL line `got=printed-none-reached-comparison
want=setup:record-printed-absent` (receipt line 75). The five instrument
mutants each die on their named arm against the landed bytes
(`ss-mut-*-landed.txt`): `echo-doc-token` → ARM2 (+ disclosed ARM3 + ARM9);
`expect-ignored` → ARM2; `capability-absent-deflected` → ARM4;
`zero-rows-success` → ARM6; `doc-rev-ignored` → **ARM11 only** — the
round-75 survivor is dead. Arms 1–15 are byte-identical base→landed
(`cmp c1-arms1-15-base.txt c1-arms1-15-landed.txt`, empty).

**Independent re-derivations (wave seats).** E1 rebuilt candidate and spec
from base bytes — both byte-identical to the L1's committed design-phase
files, battery reproduced, arms 1–15 identical. E2 built an independent
ARM11 candidate (different bytes, same behavior, `11/11`), proved
hermeticity (`unshare -rn` pass, `strace` socket/connect count 0, TMPDIR
containment, throwaway fixture identity). M1 replicated the battery in its
own scratch (matrix identical) and caught the design-phase evidence defect
mined below. R1 verified every kill-rule clause executable against
committed bytes (clause (i)/(vi) initially un-checkable from the broken
committed bytes — repaired at `be4e7c86` — and green after), plus the
constructive analysis that a wrapper-less arm19 still kills (via drift) but
fails the frozen matrix, which is why the wrapper is load-bearing. C1
(`T76W1C1.md`) verdicts: **R76-C1 verifies-as-frozen** — all seven clauses
satisfiable by construction pre-data; three cheap forgeries caught (arms-only
→ rule (i); vacuous arm19 → rule (iii) `killed=6`; crash-form arm19 → the
frozen matrix, rule (iv)); the closure must read the matrix row (the
witness's FAIL line), not exit-code counts — S006's named-witness principle.

### R76-C2 — calibration: the routed dated-literal cells re-derive from their instruments

**Before** (measured at base, receipt
`.ufo/waves/round-76/l1/c2-before-r76.txt`; re-derived byte-identically by
E3 and R2): with the extended 20-row manifest and `--doc-rev 451ed5cb`,
`SELFSTATE: rows=20 match=16 stale=4 unexpected=2` exit 1 —
`r76-pin-disposition-selftest` `doc_figure=18/18 measured_figure=19/19
stale UNEXPECTED`; `r76-evidence-disposition-selftest` `34/34` vs `66/66`
stale UNEXPECTED; `r76-r17-evidence-disposition` `56/56` vs `66/66` →
stale, expect=stale, ok.

**After** (receipt `.ufo/evidence/round-76/c2-after-r76.txt`, measured at
`4af6695f`): `SELFSTATE: rows=20 match=18 stale=2 unexpected=0` exit 0 —
both repaired cells quote the instruments' own current output lines
(`SELFTEST: PASS (19/19)`, `SELFTEST: PASS (66/66)`; the repairs are
row-scoped with `count(old)==1` anchors `→ 18/18 PASS0` and `→ PASS34/34
exit0`, everything else byte-identical — the token-uniqueness and
wrong-scope corruption analysis is R2 §A3); the two standing stale-ok rows
are `r74-frozen-addr-six` and `r76-r17-evidence-disposition`; every live
row `match`. The 17-row base population re-runs green at the landing rev
(`rows=17 match=16 stale=1 unexpected=0` exit 0,
`c2-base17-at-landing.txt`). The tuple freeze is load-bearing and complete:
the critic's manifest-data forgery (expect-flip) prints
`rows=20 match=16 stale=4 unexpected=0` exit 0 **at base with zero
repairs** — caught only by the plan's tuple table; the landed manifest's
`rows[17:]` canonical sha256 `14789e6a…` equals the critic's own
transcription of the plan table and the L1 manifest (all three identical).
The loose `\d+/\d+` regex itself does not false-green: R2 measured the r75
common-token class (`PASS`, `[0-9]`, `.*`) refusing with
`figure-not-unique` before any verdict — the r75 uniqueness guard has real
teeth on these two instruments.

## What was measured — controls and the rides-along work

- **Controls (pre-data, in the plan's own commit).** Do-nothing: at base
  both survivors pass everything and C2 reads `unexpected=2` — both
  after-states unreachable without the work (re-confirmed independently by
  C1 and R1 from base bytes). The always-fail control: each new arm passes
  unmutated and fails only under its mutant. The no-op guard: every spec
  edit `count(old)==1`, `@new ≠ @old`, fail-closed (the runner refuses a
  weakened defect with exit 2 — C1 tried it).
- **Routed payments landed this round** (round work, not claims): the
  receipt-exists scratch-leak fix (red-before `leftover_count=2`,
  `receipt-exists-leak-r76.txt`, independently reproduced by E4; green-after
  `leftover_count=0` with the selftest at `4/4 pass`,
  `receipt-exists-leak-green-after-r76.txt`; the fix removes both mkdtemp'd
  dirs in a `finally` via `shutil.rmtree` — the S299 form; TMPDIR honoured,
  no `/tmp` literal); the round-73 plan erratum (appended to
  `plans/round-73.plan.md`, naming the contradicted kill-rule sentence at
  its lines 80–82; the r72 plan-erratum `3e0ef1c8` is the precedent); the
  round-74 S294 `used-by` old→new record (appended to
  `corpus/lessons/round-74.md`, append-only); QUALITY criteria 126/127
  (kill rules satisfiable by construction before data; counter tuples
  frozen in the plan), each citing the r75 spotcheck and the r75 lesson
  mistakes that produced them; the registry home (SKILL.md gate-registry
  rows for the four instruments with full Gate-standard fields, plus 11 new
  `tools/registry.json` rows for the six standing instruments — count-recheck,
  pointer-recheck, anchor-drift-sweep, arm-liveness, figure-attribution,
  receipt-exists — each expect measured hermetically by E4 and re-verified
  by the L1, with `verdict_map`/`write_scope`/`owner`/`pinned_value` on
  every touched row; 17 further selftest-carrying tools with no registry
  row are named in `T76W1E4/registry-gaps.txt` and stay routed); the four
  re-pins (wave-reconcile selftest 19/19, mutants label `wave-reconcile-arms-r76`
  + `defects=7 killed=7`, selfstate selftest 11/11, selfstate sweep
  `rows=20 match=18 stale=2 unexpected=0`); the out-of-population
  `wave-record reconciliation` cell supersession (`18/18` →
  `WAVE_RECONCILE_SELFTEST: 19/19 pass`, receipted by the landed battery —
  r75 Correction-2-item-2 precedent, outside both claims' counters).
- **Named gaps (disclosed, not rows).** The round-17 line's `95/95` (now
  `MUTATE_SELFTEST: 107/107 pass`) and `cases=7` (now `cases=10`) are
  printed by bash instruments; the selfstate runner spawns `python3 -I`
  scripts only (`selfstate-freshness.py:296` — C1 verified the mechanism),
  so they cannot enter the population without widening the runner. Receipts:
  `T76W1E3/mutate-selftest.out`, `T76W1E3/mutate-regression.out`
  (`REGRESSION: PASS (cases=10 passed=10 …)`). The SCORECARD round-76
  disclosure paragraph (immediately after the round-17 line) names both and
  states the round-17 values stand as dated history.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| `receipt-revision-binding` (the wave's catch) | the first wave seat (M1) found the COMMITTED design-phase evidence at `5b7bbe1a` unparseable: `cand-ss-11.py` and the five `mut-*.py` carried a SyntaxError from a broken string-templating builder inside `design.py`, whose re-run (for the arm19 fix) had silently overwritten the good `design2.py` build in scratch before the wave-dir copy batch committed the broken bytes — while the committed `mut-*.out` receipts were from the earlier good builds. | the receipt-revision-gate standing rule (SKILL.md: a receipt is evidence only for the revision it names) + the mutation seat reading the committed bytes instead of trusting the scratch. | repaired pre-data at `be4e7c86`: candidate + mutants rebuilt from base via `design2.py`, receipts re-measured on the rebuilt bytes, plan correction 1 appended, the sha256 list committed; R1's clause (i)/(vi) then re-verified green on the repaired bytes. Design discipline going forward: a design script that regenerates shared scratch paths re-runs the whole chain, and the wave-dir copy happens once, from the final bytes, with the copy's sha256s recorded in the same commit. |
| `scratch-leak` | `tools/receipt-exists.py --selftest` leaves its scratch dirs behind: red-before receipt `.ufo/evidence/round-76/receipt-exists-leak-r76.txt` measures a `TMPDIR` dir count 0 → 2 during one selftest (`leftover_count=2`, dirs `receipt-exists-selftest-*` + `-extra`); independently reproduced by E4 (2 leftovers, different mkdtemp suffix). | the S279 caller-deletion duty (the instrument predates its enforcement sweep); no gate read TMPDIR leftovers before this round. | the fix candidate removes both dirs in a `finally` via `shutil.rmtree(..., ignore_errors=True)`; green-after `leftover_count=0`, selftest `4/4 pass`, no `/tmp` literal (`receipt-exists-leak-green-after-r76.txt`). |
| `attribution` | the design-phase battery receipt certified the L1's scratch candidate bytes, not the tool bytes that would land; the landing step re-ran the battery against the LANDED tool and spec (`c1-landed-battery.txt`, target sha256 `ca05ec15…` = the landed bytes). | the landing step itself + R1's rule (v) reading; the same class as the round-75 lesson's `attribution` row. | every after-state receipt now names the landed bytes' sha256; the candidate receipt stays cited only as the pre-data design measurement. |

## Findings routed to round 77

- **New survivor (M1):** a recursion-removal mutant of the wave-reconcile
  seat_reports listing walk survives `19/19` (arm15's fixture is flat) and
  is non-equivalent on a production-shaped nested listing (127 reports →
  0). The next arm needs a nested-listing fixture; the receipt is in
  `T76W1M1.md`.
- **Bash-instrument gaps** (`95/95` → `107/107`, `cases=7` → `cases=10`)
  stay routed until the selfstate runner widens beyond `python3 -I`
  scripts; nothing mechanically measures those two cells going forward —
  the queue pattern, disclosed (C1's residual-gap note).
- **Registry gaps:** 17 of the 44 `--selftest`-carrying tools still carry
  no `tools/registry.json` row (`T76W1E4/registry-gaps.txt`); the SKILL.md
  table carries none of their rows either.
- **Closure wording notes (C1, pinned pre-data):** verify the adv defect by
  its frozen matrix row (the arm19 FAIL line), not exit-code counts; verify
  C2 against the full summary line (`match=18 stale=2`), not
  `unexpected=0` alone.
- **Stagnation-window state:** round 76 enters no capability row (the round
  declines acquisition credit for the arm work — the arms are deepening of
  held instruments, not a new repertoire entry). Two capability-less
  completed rounds (75, 76) now sit at the window boundary: if round 77
  lands no capability row, the nudge fires and the round must be a
  frontier/capability move.

## considerthese baseline (2026-10-28 proposal 4, the round's one mined proposal)

`considerthese/2026-10-28.md` proposals 1–3 and 5 are landed instruments
(`receipt-exists.py`, `arm-liveness.py`, `rekey-cost.py`,
`pointer-recheck.py` — adoption receipts in the file's own status section;
CN1 cross-checked each). Proposal 4 — an assimilation-backlog burn-down —
is still unimplemented; this round lands its **baseline only**, as a
provenance-qualified count, per the connector's measurement (exit 0):

```
BACKLOG_BASELINE entries=81 target_files_present=12 path_cited=3 package_id_cited=13 path_or_id_cited=13 no_path_or_id_citation=68
```

Denominators are explicit, not inflated: 81 new-file knowledge entries in
`/home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge/` (the package's
MERGE-REPORT says 86 proposed entries; the filesystem holds 81 new-file
entries + 4 amendment files, and the report itself folds a duplicate
canonical target — neither 86 nor the file count is the denominator). The
13 path-or-ID hits are **citation candidates, not adoptions** (adoption
requires target/source-document identity, and staged S-ids were re-keyed on
adoption — e.g. staged S161 → held S275). The counting source is
`.ufo/waves/round-76/w1/T76W1CN1/backlog-count.py`; the proposal text is
`considerthese/2026-10-28.md` (proposal 4), read this round. No
burn-down rate is asserted yet — that needs a second measured point.

## Assimilation

`Assimilation: none` — the connector's overlap scan of
`/home/vgpnk/Projects/shokuknow/merge/tameshi/` found comparator material
only (`r10-witness-scope-counted.md` is the strongest witness-scope
comparator; `survivor-classification.md`, `r9-mte-schema-vocabulary.md` and
the registry-carrier entries were each deferred with reasons in
`T76W1CN1.md` §2), no theme slot fits this round's claims, and the
per-entry gates were not opened — so nothing was adopted and nothing was
appended beyond the S006 `used-by` cell above.

## Routed-queue reconciliation (round-75 spotcheck §6 item 3)

- **Already corrected by the round-75 report (recorded here, not re-paid):**
  the round-73 report's 22-of-23 landed-changes table (`e309f59f` missing)
  and its `19 × W04` census sentence (the receipt reads 18) — both corrected
  in `.ufo/reports/round-75/tameshi.md`, the correcting-round form.
- **Paid this round:** the round-73 plan erratum (append-only, naming the
  contradicted sentence) and the round-74 S294 `used-by` old→new record.
  The r75 spotcheck's item 3 queue is now empty; items 1–2 are paid as
  QUALITY criteria 126/127; item 5 (registry home) is paid this round
  (SKILL.md rows + 11 registry.json rows; the remaining 17 tools stay
  routed); item 6 is paid as C2; item 7 is paid as ARM11 (the
  `--doc-rev`-ignored survivor dies on ARM11 only); item 8 (load order) is
  honored this round — the lane read `skill://shokunin`, the canonical
  protocol files, the fleet MISSION/AXES, then the lane files, in order.

## Settlement: the rekey took four batches, and why (append-only)

The plan's landing order said "one rekey batch"; the monitor's actual
convergence took **four** (`r76-batch-1` 13 sections, `r76-batch-2` 4,
`r76-batch-3` 11, `r76-batch-4` 3; ledger 899 → 916 → 927 → 930), and two of
the detours are mined mistakes, recorded above and in the SCORECARD round
block:

1. **The stale need_rekey artifact.** `union-plan.py` reads
   `rekey-plan.json` from its own directory — the committed round-63 copy,
   last written 2026-11-01 — so a batch planned from it rekeys a
   round-63-era section set, not the measured loses. Batches must plan from
   the monitor's own measured uncredited set (batch-3 onward did; the fresh
   plans are `rekey-plan-r76b3.json` / `-r76b4.json`, committed).
2. **Flat trace numbering.** The rebind writes `traces/section-NN.json`
   numbered by plan index, so batch-2 overwrote batch-1's first four trace
   receipts and my recovery `mv` made it worse before the per-batch fix:
   the script now takes `--batch-tag` and writes `traces-<tag>/`, and every
   entry labels its own batch (`rekey_round: 76`, `rekey_batch: bN`).
   Consequence of the detour: b4 exists solely to re-credit three sections
   whose b2 trace receipts b3 destroyed.
3. **A `cp` overwrote an edited plan.** The batch-2 union plan's new-section
   row was filled in-memory and written to the lane, then a scratch→lane
   `cp` restored the unfilled version; the rebind recorded an entry with no
   inputs (`inputs-unrecorded`). Mined: never copy scratch artifacts over
   landed edits; the landing step re-verifies the bytes it is about to run.

Final state: monitor `credited=65/65` at the landing tip `b2b0f82a`
(`.ufo/evidence/round-76/coldread-green-r76.txt`); the red-before receipt
`credited=48/65` at the records commit
(`.ufo/evidence/round-76/coldread-red-r76.out`). The standing sweeps all
read clean at the tip (`WAVE_RECONCILE: rows=6 met=6 unexpected=0`;
`SELFSTATE: rows=20 match=18 stale=2 unexpected=0`; `COUNT_RECHECK: rows=7
met=7 unexpected=0`; `POINTER_RECHECK: rows=12 met=12 unexpected=0`;
`ANCHOR_DRIFT: rows=16 met=16 unexpected=0`; `ARM_LIVENESS: rows=9 live=9
dead=0`; `ADDRANGE` totals line; `SELFSTATE_SELFTEST: 11/11 pass`).

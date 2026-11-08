# tameshi round 100 — frozen declarations (plan)

Lane `tameshi-shokunin`, round 100, attempt 1, L1 `TameshiR100` (holds the canonical §3 planner
seat). Base `34d8d7cef87ec78ed84bf5247e2609814cce74c8` (`.ufo/waves/round-100/base-rev.txt`).
Instruments `3a11af7e` (tool + rows), `4b6ebcc4` (controls runner, quote-presence control, full
registry check at base), `f8f912df` (selftest renderer-at-rev repair found by the pre-freeze
control) — instruments revision I = `f8f912dfd569a33fade039af605f55cec15b921a`
(`.ufo/waves/round-100/instruments-rev.txt`). Every pre-freeze receipt below is in
`.ufo/evidence/round-100/pre-freeze/` and carries its command, measured revision and tool sha256
(runner `.ufo/evidence/round-100/pre-freeze-run.sh`; tools execute from `git show I:<tool>` bytes).

Inputs read first: the round-99 non-author spot-check (`corpus/lessons/round-99-verifier-spotcheck.md`,
admitted; routed items 1-5), SCORECARD §Round 99 Planned, `considerthese/2026-11-08.md`
(ideas 1-7; idea 1 applied in round 99), Amendment 59 (pre-file falsification ledger). Fresh-start
rule: not in force for this round (rounds 95-99 admitted).

Scores at base: depth 10, calibration 8 (lowest non-retired; the score rule caps it at 8 until
independent SHONEN promotion review), freshness 9.

## Claims (frozen before data)

Records revision R = the lane commit that carries the wave's reports and any amendments; R is
written to `.ufo/waves/round-100/records-rev.txt` before the records run. Each claim is
verifiable with the other's tool deleted (C1 reads only `tools/registry.json` rows tagged
`r100-c1` and four pre-existing tools; C2 reads only `tools/gate-line-recheck.py`, the R93S1
renderer and committed lessons/snapshots).

### C1 — operability: the no-harm monitor governs the round-98/99 audits

Routed by the round-99 spot-check item 3 ("Neither round-98/99 audit has a `tools/registry.json`
row … register them before any claim rests on them as gates") and SCORECARD §Round 99 Planned.

**Wording.** At R, `python3 -I tools/registry-check.py --rev R --tag r100-c1` prints
`REGISTRY_CHECK: held=12/12 superseded=0` and exits 0. The twelve rows are active and tagged
`r100-c1`: for each of `tools/tally-reconcile.py`, `tools/control-assertion-audit-v2.py`,
`tools/control-assertion-audit.py` and `tools/registry-cell-immutability.py`, one `--selftest`
row (exit 0), one red gate row (exit 1) and one green gate row (exit 0), each red/green row pinned
to committed historical revisions and carrying its exact summary line as `stdout_contains`. At
base `34d8d7ce` the same command exits 2 (`--tag ['r100-c1'] selects no registry row`). In a
scratch checkout of R, replacing any one of the four tools by an always-green stub (prints that
tool's selftest and green summary lines, exits 0) makes that tool's red row differ
(`held=11/12`, exit 1) — four stubs, four flips. No harm: the full registry check at R prints
`REGISTRY_CHECK: held=87/91 superseded=7` and its differing rows are exactly the four that differ
at base (`sources-census`, `verify-round15`, `mte-interop-check`, `receipt-bytes-tree`;
`.ufo/evidence/round-100/base/registry-check-full-at-base.out`: `held=75/79 superseded=7`).

- Counter: `python3 -I tools/registry-check.py --rev R --tag r100-c1` (cwd lane, TMPDIR scratch).
- No-harm counter: `python3 -I tools/registry-check.py --rev R` (full registry).
- Before (pre-freeze, committed): `c1-before-tag-miss.out` rc 2; `c1-rows-base-vs-instr.out`
  `tools_with_rows=0/4` at base, `4/4` (3 rows each) at I.
- At I (pre-freeze): `c1-at-instruments.out` `held=12/12` rc 0; `c1-forgery-stub-*.out` four
  files, each `held=11/12` rc 1 with exactly that tool's red row `differs`.
- Declared limits: the rows prove the four tools still print their recorded verdicts on pinned
  historical inputs; they do not prove the tools are correct on new inputs, and a stub that
  reproduces both the red and the green lines per argv would pass (the red/green pair defeats
  only argv-blind stubs). The rows' `source` cites SCORECARD.md at base line 5933 (the Planned
  note), not a tool line.
- Kill: tag check not `held=12/12` rc 0 at R; any stub that fails to flip its red row; the
  full-registry differing set at R differs from base's four (harm, or an unexplained change).

### C2 — calibration: Gate line pointers reconciled with the rendered snapshot they cite

Mines `considerthese/2026-11-08.md` idea 2 ("Gate line-pointer checker … confirm that each cited
`line N` holds the start of its quote"); the class is the round-95 spot-check D1
(`corpus/lessons/round-95-verifier-spotcheck.md:172-183`). It counts mismatches between the
lane's self-assessment (each Gate's "line N: <quote>") and observed repo state (the committed
snapshot rendered by the lane's canonical renderer). Sourced: S327 (opened this round).

**Wording.** At R, `python3 -I tools/gate-line-recheck.py --repo . --rev R --record
corpus/lessons/round-95.md --record corpus/lessons/round-96.md --record corpus/lessons/round-97.md
--record corpus/lessons/round-98.md --record corpus/lessons/round-99.md` prints
`GATE_LINE_RECHECK records=5 pointers=21 hit=12 miss=6 absent=0 unbound=3` (plus
`renderer_sha256=2d431606…a1bf`) and exits 1; its six `GATE_LINE miss` lines are exactly
`corpus/lessons/round-95.md:17`…`:22` with cited 84, 4399, 4393, 4493, 2615, 2355 (the six
pointers the round-95 closure's D1 found off); the same command with only round-95 prints
`pointers=6 hit=0 miss=6 absent=0 unbound=0` exit 1; only round-97 and only round-99 each print
`pointers=2 hit=2 miss=0 absent=0 unbound=0` exit 0; `--selftest --repo . --rev R` prints
`GATE_LINE_SELFTEST: 24/24 pass` exit 0. The do-nothing control (the lane's prior check class,
quote present anywhere in the rendered snapshot) over the same pointers prints
`QUOTE_PRESENCE pointers=21 present=18 absent=0 unbound=3 flagged_d1=0` — it sees none of the six.

- Grammar, binding and verdict rules: the tool docstring (declared, not inferred). Records and
  snapshots are read as blobs at --rev; only the `strip_tags`, `norm_text`, `_bare`, `locate`
  definitions of `.ufo/waves/round-93/w1/R93S1-tagstrip.py` at --rev are compiled.
- Before: `c2-before-token.out` (`git grep -c GATE_LINE_RECHECK <base>` rc 1).
- At I (pre-freeze): `c2-population.out`, `c2-red-r95-only.out`, `c2-green-r97-only.out`,
  `c2-green-r99-only.out`, `c2-selftest.out`, `c2-control-quote-presence.out` — the values above.
- Forgery control: a scratch clone child of I with one round-96 pointer moved `4403`→`4399`
  (fixture identity) flips that pointer to `miss` (`c2-forgery-r96-pointer.out`: `hit=5 miss=1`
  vs unforged `hit=6 miss=0`, `c2-forgery-r96-unforged.out`).
- Renderer-choice control: under the round-95 Gate's own literal convention (no script/style
  removal) all six are still misses (`c2-r95-stated-renderer.out`: `hit_under_stated=0`) — the
  miss is not an artefact of renderer choice.
- Declared limits: a `line N` hit means some occurrence of the quote starts on N (a quote that
  occurs twice can hit on an occurrence the Gate did not mean); the observed start is the line of
  the quote's first word (`a single header row` starts on 4395 where the round-95 closure wrote
  4396); pointers with no quote, no resolvable snapshot or a JSON snapshot are `unbound` (counted,
  exit 1, never hit); quote extraction is the declared three-step rule; only lesson `## Gate`
  sections are read (plans, SOURCES anchors and reports are not); one renderer.
- Kill: summary or miss set differs at R; any wave artifact shows a pointer graded `hit` whose
  quote does not start on the cited line under the canonical renderer (false green); the
  quote-presence control flags any of the six (then C2 does not beat the do-nothing control).

## Pre-registered controls (executed and committed before this freeze)

| control | receipt | observed |
|---|---|---|
| C1 before | `pre-freeze/c1-before-tag-miss.out` | rc 2, no row selected |
| C1 rows base vs I | `pre-freeze/c1-rows-base-vs-instr.out` | 0/4 → 4/4 tools with rows |
| C1 at I | `pre-freeze/c1-at-instruments.out` | `held=12/12`, rc 0 |
| C1 forgery ×4 | `pre-freeze/c1-forgery-stub-{tally-reconcile,control-assertion-audit-v2,control-assertion-audit,registry-cell-immutability}.out` | each `held=11/12`, rc 1, own red row differs |
| C1 no-harm base | `base/registry-check-full-at-base.out` | `held=75/79 superseded=7`, 4 differ |
| C2 before | `pre-freeze/c2-before-token.out` | rc 1 |
| C2 population at I | `pre-freeze/c2-population.out` | `pointers=21 hit=12 miss=6 absent=0 unbound=3`, rc 1 |
| C2 red/green | `pre-freeze/c2-red-r95-only.out`, `c2-green-r97-only.out`, `c2-green-r99-only.out` | miss=6 rc 1; hit=2 rc 0; hit=2 rc 0 |
| C2 selftest | `pre-freeze/c2-selftest.out` | `24/24 pass` |
| C2 do-nothing | `pre-freeze/c2-control-quote-presence.out` | `flagged_d1=0` |
| C2 forgery | `pre-freeze/c2-forgery-r96-pointer.out` vs `c2-forgery-r96-unforged.out` | `miss=1` vs `miss=0` |
| C2 renderer choice | `pre-freeze/c2-r95-stated-renderer.out` | `hit_under_stated=0` |

## Do-nothing controls

- C1: no work = no `r100-c1` rows → the tag counter exits 2 at base; the monitor cannot see a
  broken audit (forgery stubs at base have no row to flip).
- C2: no work = the lane's existing quote-presence check → `flagged_d1=0` over the 21 pointers.

## Amendments

Rows are added only from wave artifacts, before the records run, each citing its artifact. A
post-data amendment (after the records run) goes into the marked sub-table `### Post-records`
below (round-99 spot-check routed item 1).

| id | artifact | change | effect on wording |
|---|---|---|---|
| A1 | `.ufo/waves/round-100/w1/R100E3.md` F4/F5; `w1/R100SN1-F7-backtick-in-quote.out` | The C2 declared semantics delegated to the tool docstring are narrowed: `absent` means `locate()` finds no word-sequence match for the extracted quote (a lone punctuation token left by a tag boundary reduces to an empty word and can make a verbatim quote `absent`, out-of-set round-77:70 and round-88:46); a markdown table is one block (one sid, one explicit-snapshot fallback for every row; a quote written before its pointer is not extracted — out-of-set round 89); a backticked snapshot name inside a quote can become the explicit binding. Tool bytes unchanged. | C2's frozen counter, predicate and numbers unchanged; the claim covers only the five in-set records (no table-shared block, `absent=0`); the docstring's "the quote is not located anywhere" is read as "`locate()` finds no match", nothing wider. |
| A2 | `w1/R100R2-receipt-renderer-default-arg.out`, `w1/R100R2-receipt-renderer-decorator-on-def.out`; `w1/R100SN1-F1-renderer-exec.out` | The plan sentence "only the `strip_tags`, `norm_text`, `_bare`, `locate` definitions … are compiled" and the docstring's "nothing else in it runs" are narrowed: compiling those four definitions also evaluates their decorator and default-argument expressions (a default-argument marker file was created; a decorator naming an uncompiled helper raised `NameError`), and their bodies run when called. Nothing outside the four definitions runs. Tool bytes unchanged. | C2's numbers unchanged; the trust boundary is restated as "code in the four renderer definitions of the lane's own blob at `--rev`, including their decorators and defaults". |
| A3 | `w1/R100C1b.md` F3 (`R100C1b-F3-decoy-c2-unseen.out`) | A frozen-pin printer that never renders reproduces C2's summary and exit on the frozen arms; it differs on the unseen round-93 lesson (`pointers=2 hit=2` rc 0 vs the tool's `pointers=0` rc 1). C2's instrument is narrowed to its bytes: the claim is that `tools/gate-line-recheck.py` with blob sha256 `dae90e50d8d5d447c7a85d77df8e973114355d8ce96e5b78f522b82e88ad3bb9` at R prints the frozen lines; every records receipt carries that sha. The claim does not assert that the summary predicate alone discriminates a program that replays it; per-pointer agreement is evidenced separately by the independent re-implementation (`w1/R100E2.md` F2, 21/21 verdicts and spans) and out-of-set runs (`w1/R100E3.md`). | Counter, predicate and numbers unchanged; the wording "prints …" is read as "the pinned tool blob prints …". |
| A4 | `w1/R100R1b.md` F4 (`R100R1b-receipt-argv-aware-stub.out`) | An argv-aware stub that replays the three recorded verdicts holds all three of its tool's rows. C1's title and surface word "governs"/"governing" is narrowed to "registers": the twelve rows register the four audits with the no-harm monitor and prove they still print their recorded verdicts on pinned historical inputs (the plan's own declared limit); they do not prove the tools compute those verdicts. | Counter, predicate and numbers unchanged; C1 reads "the no-harm monitor registers the round-98/99 audits". |

### Post-records

| id | artifact | change | effect on wording |
|---|---|---|---|

## Routed items (round-99 spot-check)

1. Post-data amendment → marked sub-table: adopted above (`### Post-records`).
2. Reconciler silence is not agreement: carried; C2 reports `unbound` separately and exits 1 on it.
3. Register the round-98/99 audits: C1.
4. Two citation grammars / two binding walkers (A8): carried, not claimed this round.
5. SHONEN promotion: operator-owned; unchanged.

## Frontier step (§2b)

S327 (Jergas & Baethge 2015, quotation accuracy meta-analysis; admit, grounds C2) and S328
(Mogull 2017, recalculated quotation error rate; reject with flip) opened 2026-11-08,
snapshots `.ufo/evidence/round-100/sources/s327.json`, `s328.json`. Mistake mined into
`corpus/lessons/round-100.md` `## Mistakes`. considerthese: `2026-11-08.md` idea 2 → C2.
Assimilation: none planned.

## Attempt 2 (L1 `TameshiR100a2`)

Attempt 1 (`TameshiR100`) froze both claims (`56f247da`), dispatched w1 (`6ab72d6f`) and died with
the orchestrator session (watchdog `lane-dead-no-report tameshi round=100`, 21:09:24). Its w1 seats
were finalized with `output: null` (`.ufo/waves/round-100/w1-results.json`). Adopted unchanged:
the frozen plan and claims, the pre-freeze receipts, the inherited `corpus/SOURCES.md` S327/S328
rows, `.ufo/evidence/round-100/records-run.sh`, `.ufo/evidence/round-100/mistakes/`, and every
seat file in `w1/` (E2, E3, M1, RV1 reports; R2, SN1, S1 receipts without a report). Re-run as the
residual `w1r` (4 seats, `make-w1r-dispatch.py`): R100C1→R100C1b, R100CN1→R100CN1b,
R100R1→R100R1b, R100E1→R100E1b, against the same FREEZE. Not re-run: R100SC1 (scout; S327/S328
re-opened by the L1 instead, lesson §Gate) and R100S1 (scribe; the L1 drafted the knowledge entry).
Discarded: nothing.

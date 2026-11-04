# tameshi round 76 — plan (frozen before any claim data)

Lane: tameshi-shokunin. Base: `451ed5cb6d5f8c2bf4b3e10836e4634cfcb03ee0`
(branch `master` = `origin/master`, clean tree — the round-75 non-author
closure verdict commit, `corpus/lessons/round-75-verifier-spotcheck.md`).
Round shape: **one v1 wave, 12 seats** (policy
`scripts/hyaku/ufo-wave-policy.json`, band 8–16; attack seats by the policy's
named set = 2 reviewer + 1 critic + 1 mutation-tester = 4 = 33.3 %; `labrat`
is a frozen-topology seat the validator rejects, so no labrat item exists —
the planner seat stays with the L1 per the orchestrator ruling).

Saturation state at round start (SCORECARD.md): scored axes depth 10,
calibration 8, freshness 9 — all at or above the saturation line 8. A
capability entered the table at round 74 (`round-range additivity sweep`);
round 75 entered none (the settlement errata declined acquisition credit), so
one capability-less completed round sits inside the stagnation window (N = 2)
and the nudge does **not** fire. C2 works the lowest scored numeric axis
(calibration 8).

Two claims, distinct axes, causally separable: C1 lands only inside
`tools/wave-reconcile.py`, `tools/selfstate-freshness.py`, their mutant specs
and their battery receipts; C2 lands only inside
`tools/selfstate-freshness.json` and the SCORECARD cells it measures. C2's
declared population excludes the `wave-record reconciliation` row C1's landing
moves; C2 is verifiable at base (its before-state) and its after-state needs
only the two cell supersessions, never C1's files. Neither claim needs the
other's counters or commits.

Design-phase disclosure (pre-data, this plan's own commit): the L1 built both
candidates and ran both batteries in scratch before this plan was frozen; the
candidate bytes, the seven-defect spec, the five instrument mutants, the full
battery transcripts and the measured kill matrices are committed under
`.ufo/waves/round-76/l1/` and `.ufo/evidence/round-76/` in the same commit as
this plan. The predicates below are frozen against those measurements; the
wave seats re-derive them independently and attack them.

## R76-C1 — operability (verdict-only; sourced on the re-opened S006): the two round-75 survivors become measured arms

**Named survivors (round-75 carry).**
`adv-seatreports-require-printed-bypass` — dropping `require_printed=True` in
the `seat_reports` branch only survives the round-75 18-arm suite
(`corpus/lessons/round-75.md` Findings; measured again at base this round:
receipt `.ufo/waves/round-76/l1/mut-base-bypass.out`, `18/18 pass` on base
bytes). `--doc-rev-ignored` — the selfstate instrument mutant survived the
round-75 battery 10/10 (`corpus/lessons/round-75.md` Settlement errata;
re-measured at base: `.ufo/waves/round-76/l1/mut-base-docrev.out`, `10/10
pass`).

**Before (measured at base `451ed5cb`, receipts in the design-phase commit).**
`git show 451ed5cb:tools/wave-reconcile.py | sha256sum` →
`bf10c0e490e78e3f98fdb580442916e685968a94ff8c3fc977dead4b74a7f791`;
`python3 -I -X utf8 tools/wave-reconcile.py --selftest` →
`WAVE_RECONCILE_SELFTEST: 18/18 pass` exit 0; the bypass mutant on base bytes
reads `18/18 pass`.
`git show 451ed5cb:tools/selfstate-freshness.py | sha256sum` →
`3b09676340fc63007d3a1e5de3e54471feddb22024a2f40bd4b3b469f560eba6`;
`python3 -I -X utf8 tools/selfstate-freshness.py --selftest` →
`SELFSTATE_SELFTEST: 10/10 pass` exit 0; the doc-rev-ignored mutant on base
bytes reads `10/10 pass`.

**After.**
`tools/wave-reconcile.py` gains `arm19-seatreports-printed-required`: a
seat_reports row whose record carries no `printed` value must refuse with
`record-printed-absent`; the wrapper also catches the TypeError the bypass
mutant raises (printed=None reaches the detail formatting) so the suite stays
runnable under mutation. `SELFTEST_ARMS` 18 → 19.
`tools/wave-reconcile-mutants.spec` gains the seventh defect
`adv-seatreports-require-printed-bypass` (the exact single edit, first six
blocks byte-identical to base).
`tools/selfstate-freshness.py` gains `ARM11_doc_rev_cli_binding`: the real CLI
runs as a subprocess against a two-state git fixture (rev1 doc `4/4` vs
worktree doc `9/9`, toy instrument committed at rev1); reading `--doc-rev`
must measure `rows=1 match=1 stale=0 unexpected=0` exit 0; a tool that ignores
`--doc-rev` reads the worktree and fails the arm. `SELFTEST_ARMS` 10 → 11.

Counting commands (pasteable; after-state at the landing rev):

```sh
python3 -I -X utf8 tools/wave-reconcile.py --selftest | tail -1
python3 -I -X utf8 tools/selfstate-freshness.py --selftest | tail -1
bash tools/mutate-and-run.sh --target tools/wave-reconcile.py \
  --defects tools/wave-reconcile-mutants.spec \
  --suite 'python3 -I -X utf8 "$MUTANT" --selftest' \
  --workdir "$HYAKU_SCRATCH/tameshi-r76/l1/battery" --label wave-reconcile-arms-r76
```

Expected after-state: `WAVE_RECONCILE_SELFTEST: 19/19 pass` exit 0;
`SELFSTATE_SELFTEST: 11/11 pass` exit 0; the battery prints `CONTROL: GREEN`,
`MUTATE: DONE (target=wave-reconcile-arms-r76 defects=7 killed=7 survived=0
inconclusive=0 kill-rate=100%)` and `MUTATE_RESTORE: OK` byte-identical. The
five instrument mutants (rebuilt single edits on the landed bytes) each die on
their named arm: `echo-doc-token` → ARM2 (collateral ARM3 + ARM9, disclosed);
`expect-ignored` → ARM2; `capability-absent-deflected` → ARM4;
`zero-rows-success` → ARM6; `doc-rev-ignored` → ARM11 only.

**Kill matrix (frozen; measured on the design-phase candidate
`.ufo/waves/round-76/l1/bat-wr.out`, pristine 19/19):**

| mutant | dies on |
|---|---|
| `m2-delimited-tautology` | arm13 + arm16 (r75 collateral, unchanged) |
| `span-rule-removed` | arm14 + arm17 + arm18 (r75 collateral, unchanged) |
| `seat-reports-any-depth` | arm15 |
| `mc-record-bound` | arm16 |
| `roles-bypass` | arm17 |
| `attack-bypass` | arm18 |
| `adv-seatreports-require-printed-bypass` | **arm19 only** (got=`printed-none-reached-comparison`) |

**Kill rule (frozen, satisfiable by construction).** C1 fails if (i) either
pristine selftest is not green at the stated count (19/19, 11/11); (ii) the
battery control is not GREEN or the restore is not byte-identical; (iii) the
battery is not `defects=7 killed=7 survived=0`; (iv) the new defect dies on
any arm other than arm19, or any pre-existing mutant loses its matrix kill
above; (v) any base arm 1–15 changes its outcome between base bytes and
landed bytes (the arms 1–15 selftest lines must be byte-identical); (vi) any
of the five instrument mutants survives, or dies on an arm other than its
named arm plus the disclosed echo collateral; or (vii) the landed bytes change
any counter other than the two selftests and the two mutant specs (the
standing six-row wave sweep and the 17-row selfstate sweep stay out of scope
this round — C2 owns the selfstate sweep change).

**Controls (pre-data).** Do-nothing: at base both survivors pass everything
(receipts above), so both after-states are unreachable without the arms. The
always-fail control: each new arm passes on the unmutated candidate and fails
only under its mutant. The no-op guard: every spec edit is `count(old)==1`
asserted by the runner (fail-closed), and the `@new` differs from `@old`.

## R76-C2 — calibration (lowest scored numeric axis, 8): the routed dated-literal cells re-derive from their instruments

**The population (frozen tuples; the landed `tools/selfstate-freshness.json`
must equal the 17 committed rows plus EXACTLY these three appended rows —
same `schema` key, instruments pinned at base `451ed5cb`):**

| id | mode | capability / span | figure regex | instrument (path @ `451ed5cb`, argv) | expect |
|---|---|---|---|---|---|
| `r76-pin-disposition-selftest` | capability | `six-leg content-disposition probe` | `\d+/\d+` | `tools/pin-disposition.py`, `--selftest` | match |
| `r76-evidence-disposition-selftest` | capability | `effective expectation reconciliation` | `\d+/\d+` | `tools/evidence-disposition.py`, `--selftest` | match |
| `r76-r17-evidence-disposition` | span | span `56/56` (the round-17 supersession line) | `\d+/\d+` | `tools/evidence-disposition.py`, `--selftest` | stale |

Rationale: round-75 spotcheck §6 item 6 routed the two dated-literal
capability cells and the stale round-17 supersession values to this round.
`56/56` is the round-17 line's evidence-disposition supersession; the span row
makes the instrument MEASURE its drift on every sweep (the
`r74-frozen-addr-six` pattern), never assume it.

**Named gaps (disclosed, not rows):** the round-17 line's `95/95`
(mutation-sweep selftest; instrument `bash tools/mutate-and-run.sh
--selftest`, current token `107/107` at r75) and its `cases=7` (current
`cases=10`, measured this round) are printed by bash instruments, and the
selfstate runner spawns `python3 -I` scripts only — they cannot enter this
population without widening the runner, which is not this round's claim.
They are named in the round-76 disclosure line and stay routed.

**Before (measured at base, receipt
`.ufo/waves/round-76/l1/c2-before-r76.txt`):** with the extended manifest and
`--doc-rev 451ed5cb`:
`SELFSTATE: rows=20 match=16 stale=4 unexpected=2` exit 1 —
`r76-pin-disposition-selftest` reads `doc_figure=18/18 measured_figure=19/19
stale UNEXPECTED`; `r76-evidence-disposition-selftest` reads
`doc_figure=34/34 measured_figure=66/66 stale UNEXPECTED`;
`r76-r17-evidence-disposition` reads `56/56` vs `66/66` → stale, expect=stale,
ok. (Token uniqueness pre-checked: pin-disposition stdout carries exactly one
`\d+/\d+` match `19/19`; evidence-disposition exactly one, `66/66`.)

**After.** Two capability cells are superseded (row-scoped, historical bytes
disclosed in the round-76 SCORECARD block): `six-leg content-disposition
probe` quotes `SELFTEST: PASS (19/19)` and `effective expectation
reconciliation` quotes `SELFTEST: PASS (66/66)` — the instruments' own output
format. A round-76 supersession line is appended directly after the round-17
disclosure naming the current tokens with receipts (`107/107` and `cases=10`
as the two named bash gaps, `19/19`, `66/66`) and stating that the round-17
values stand as dated history. After-state at the landing rev:

```sh
python3 -I -X utf8 tools/selfstate-freshness.py --repo . \
  --manifest tools/selfstate-freshness.json --doc-rev <landing-rev> | tail -1
```

Expected: `SELFSTATE: rows=20 match=18 stale=2 unexpected=0` exit 0, with the
frozen `r74-frozen-addr-six` row and `r76-r17-evidence-disposition` the two
stale-ok rows and every live row `match`.

**Kill rule (frozen).** C2 fails if (i) the landed manifest's three new rows
differ from the table above (a laxer regex, a foreign instrument, a dropped
row — the manifest is not the counter); (ii) the population is not exactly 20
rows; (iii) `unexpected≠0` at the landing rev; (iv) either repaired cell does
not quote the instrument's current token in the instrument's own output
format; (v) the round-76 disclosure line is absent or names neither bash gap;
(vi) a setup refusal (capability-absent, figure-not-unique,
instrument-figure-absent, span-absent) occurs at the landing rev — a refusal
is a failure to measure, never a pass; or (vii) any of the 17 pre-existing
rows changes its base verdict (the r75 line `rows=17 match=16 stale=1
unexpected=0` must still re-run green at the landing rev).

**Controls (pre-data).** Do-nothing: `unexpected=2` at base — the target is
unreachable without the repairs. Echo-stub lineage: the receipt carries the
per-row `measured_figure=` tokens (the instrument's own stdout, not a doc
copy) and the two standing stale rows must read `stale` every sweep.
Row-deletion: a manifest row whose capability/span no longer resolves is a
setup refusal (exit 2). Tuple freeze: this table IS the counter; the reviewer
seat diffs the landed manifest's three rows against it byte-wise.

## Frontier step (part of the round, not a claim)

- **Sourced claim: C1 rests on S006 (shmutant README), RE-OPENED this round**
  (fresh fetch, fresh located quotes, `used-by` gains
  `corpus/lessons/round-76.md`; status/recheck/anchor unchanged — append-only;
  the scout seat fetches and quotes; the lesson Gate records URL, access
  date, quotes). **Reject (standing):** a new shmutant row at the current
  bytes — same URL, same document, within-scope duplicate (CORPUS.md rule 2;
  S289/S293 precedent); flip: S006 retired or the README superseded.
- **Census before:** `.ufo/evidence/round-76/census-start.txt` (exit 0, 164
  rows); must read exit 0 at round end; no new row is planned (164 → 164);
  next unused id stays S305.
- **Mistake to mine (`corpus/lessons/round-76.md` `## Mistakes`):** the
  receipt-exists selftest scratch leak (measured red-before this round:
  `TMPDIR` dir count 0 → 2 during one `--selftest`,
  `.ufo/evidence/round-76/receipt-exists-leak-r76.txt`; class
  `scratch-leak`, captured-by the S279 caller-deletion duty — the instrument
  predates the rule's enforcement sweep); fix ships with red-before →
  green-after receipts (cleanup in `finally` via `shutil.rmtree`, S299).
- **considerthese:** the connector seat scans `considerthere`-adjacent
  material (tameshi `considerthese/`, latest file 2026-10-28); at most ONE
  still-unimplemented proposal may be mined, as a lesson baseline citing
  `considerthese/<file>` + date. Assimilation from `merge/tameshi/` is
  decided by the connector's overlap findings; if no theme slot fits the
  claims, the report's Sources & frontier section says `Assimilation: none`.

## Routed payments (round work, not claims)

1. **receipt-exists scratch leak** (r75 wave finding): red-before measured
   (0 → 2 dirs under `TMPDIR` during one selftest); candidate fix cleans up in
   `finally`; green-after re-measured 0 → 0; selftest stays `4/4 pass`.
2. **Round-73 routed item 3** (r75 spotcheck §6 item 3): append the erratum to
   `plans/round-73.plan.md` for the contradicted kill-rule sentence.
3. **Round-74 S294 used-by old→new** (r75 spotcheck §6 item 4): append the
   record to `corpus/lessons/round-74.md` (append-only).
4. **Queue reconciliation** (r75 spotcheck §6 item 3): the round-76 lesson
   records which routed items the round-75 report already corrected and which
   this round pays, so the queue stops double-listing.
5. **QUALITY criteria 126/127** from r75 spotcheck §6 items 1–2 (kill rules
   satisfiable by construction before data; counter tuples frozen in the
   plan), each citing `corpus/lessons/round-75-verifier-spotcheck.md` and the
   r75 lesson mistakes.
6. **Registry home** (r74 closure defect 4, r75 spotcheck §6 item 5): SKILL.md
   gate-registry rows for `tools/wave-reconcile.py`, `tools/additivity-range.py`,
   `tools/selfstate-freshness.py` (full Gate-standard fields); executor seat
   drafts verified `tools/registry.json` rows for the standing instruments
   that still carry none (printed-count, line-pointer, anchor-drift,
   arm-liveness, figure-attribution, receipt-exists minimum set), and the
   touched rows gain verdict-map / pinned-value / write-scope / owner fields.
7. **Out-of-population record repair, disclosed:** after C1 lands, the
   `wave-record reconciliation` capability cell (18/18) is superseded to the
   new `19/19` token with the battery receipt — outside C2's frozen population
   (r75 precedent, Correction 2 item 2).
8. **Registry re-pins:** the four `tools/registry.json` rows whose expects
   quote the changed counters (wave-reconcile selftest 18/18 → 19/19,
   wave-reconcile mutants defects=6 → 7, selfstate selftest 10/10 → 11/11,
   selfstate sweep rows=17 → rows=20) are re-pinned at the landing rev with
   measured outputs.

## Cold-read / landing plan

Monitored edits this round (forecast receipt
`.ufo/evidence/round-76/rekey-cost-full-r76.txt`): `SCORECARD.md`, `LOG.md`,
`corpus/SOURCES.md`, `corpus/QUALITY.md`, `SKILL.md`, `tools/registry.json` →
`REKEY_COST sections=64 planned=6 at_risk=16 predicted_lost=16`. One rekey
batch after every content edit; the monitor must read `credited=64/64` at the
landing tip. The receipt-exists fix touches `tools/receipt-exists.py` (not a
monitored input; no forecast impact).

## Write scope and landing order

Lane repo `/home/vgpnk/Projects/shokunin/tameshi-shokunin` only (plus the
fleet report and an L0 line if needed). Order: (1) declaration commit — this
plan, the LOG declaration, the design-phase receipts and candidates, census
and rekey receipts; (2) the wave; (3) C1 tools + specs + batteries on the
landed bytes; (4) the receipt-exists fix + registry rows; (5) C2 cell
supersessions + the round-76 disclosure line; (6) records (SCORECARD block,
LOG measured, lesson Gate/Gate-census/Mistakes/routed-reconciliation, SOURCES
note, QUALITY criteria 126/127, r73/r74 appends); (7) the rekey batch;
(8) the report (cites the pushed lane tip) and the fleet commit.

### Design-phase correction 1 (appended before any wave data, 2026-11-04): committed evidence repaired

The first wave seat (T76W1M1) caught that the committed `.ufo/waves/round-76/l1/cand-ss-11.py`
and the five committed `mut-*.py` instrument mutants did not parse (a broken
string-templating builder inside `design.py` had silently overwritten the good
`design2.py` build during a re-run, and the wave-dir copy then committed the
broken bytes while the committed `mut-*.out` receipts came from the earlier
good builds). This is the receipt-revision-binding violation the lane's
standing rule names; it is mined in `corpus/lessons/round-76.md`.

Repair (pre-data; no predicate, counter, kill rule or matrix changed): the
candidate and the five mutants were rebuilt from base via `design2.py`, the
five mutants re-run on the rebuilt bytes, and the wave-dir copies replaced.
Post-repair receipts, measured on the rebuilt bytes: `SELFSTATE_SELFTEST:
11/11 pass` exit 0; `echo-doc-token` → 8/11 (ARM2 + ARM3 + ARM9 FAIL);
`expect-ignored` → 10/11 (ARM2); `capability-absent-deflected` → 10/11
(ARM4); `zero-rows-success` → 10/11 (ARM6); `doc-rev-ignored` → 10/11
(ARM11 only). The battery-certified pair (`cand-wr-19.py` + `bat-wr.out`,
19/19 pristine, 7/7 killed) was unaffected. The repair commit carries the
sha256 list of the corrected bytes.

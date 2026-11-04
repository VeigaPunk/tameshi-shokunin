# tameshi round 75 — plan (frozen before any claim data)

Lane: tameshi-shokunin. Base: `21ef81e99966198cf8cdb2c6d8e56aa3c482da56`
(branch `master` = `origin/master`, clean tree — the admitted round-74
non-author closure, `corpus/lessons/round-74-verifier-spotcheck.md` §7).
Round shape: **one v1 wave, 12 seats** (policy
`scripts/hyaku/ufo-wave-policy.json`, band 8–16; attack seats by the policy's
named set = 2 reviewer + 1 critic + 1 mutation-tester = 4 = 33.3 %; `labrat` is
a frozen-topology seat the validator rejects, so no labrat item exists — the
planner seat stays with the L1 per the orchestrator ruling).

Saturation state at round start (SCORECARD.md): scored axes depth 10,
calibration 8, freshness 9 — all at or above the saturation line 8. A
capability entered the table at round 74 (`round-range additivity sweep`), so
the stagnation window (N = 2) is **not** exceeded and the nudge does not fire.
C2 works the lowest scored numeric axis (calibration 8).

Two claims, distinct axes, causally separable: C1 lands only inside
`tools/wave-reconcile.py`, its mutant spec and its battery receipts; C2 lands
only inside `tools/selfstate-freshness.py` + `tools/selfstate-freshness.json`
and the SCORECARD capability cells it measures. C2's declared population
excludes the wave-reconciliation rows C1 changes. Neither claim needs the
other's files, counters or commits.

## R75-C1 — operability (verdict-only): the two round-74 survivors become measured arms

**Before (measured at base, receipt `.ufo/evidence/round-75/base-measure-c1.txt`).**
`git show 21ef81e9:tools/wave-reconcile.py | sha256sum` →
`97bb9272afb6c243cf7fb2dfde7bd34b90b4bcd769974d112ca574fccafd21fa`.
`python3 -I -X utf8 <pristine> --selftest` → `WAVE_RECONCILE_SELFTEST: 15/15
pass`, exit 0. Three single-edit mutants built from those bytes each read
`15/15 pass` (all three survive the whole suite):

| mutant | the edit | what it widens |
|---|---|---|
| `M-C` record-bound printed | `_record_claim` binds `printed` to the decoded RECORD text instead of `rec['span']` | a number delimited anywhere in the record passes for a number in the span |
| `roles-bypass` | `_record_claim(row, readers)` deleted from the `roles` branch only | roles rows skip the record-span binding |
| `attack-bypass` | the same deletion in the `attack_share` branch only | attack_share rows skip the record-span binding |

The round-74 carry names `M-C` (`corpus/lessons/round-74.md`, appended
correction; `.ufo/waves/round-74/w1/T74W1M1.md` §4–§5) and the selective
`_record_claim` bypass (`.ufo/waves/round-74/w1/T74W1R1.md` §2). The cause is a
fixture population, not a rule change: no arm's record carries a delimited
occurrence of `printed` OUTSIDE its span, and no arm exercises a roles or
attack_share row with a span absent from its record.

**After.** Three frozen arms are added; each named mutant dies on its named arm
and on no other:

| arm | the rule it guards | fixture input that moves it |
|---|---|---|
| `arm16-printed-span-not-record` | `printed` must be delimited INSIDE the bound span, not merely somewhere in the record | span `11 reports`, `printed: 1`, record `- The wave: 11 reports; 1 seat filed late.` (a delimited `1` outside the span) → setup refusal `printed-not-in-span` |
| `arm17-record-claim-live-on-roles` | the `roles` branch binds the record span before measuring | roles row whose record span `13 seats` is absent from the record → setup refusal `span-not-in-record` |
| `arm18-record-claim-live-on-attack-share` | the `attack_share` branch binds the record span before measuring | attack_share row whose record span `13 seats` is absent → setup refusal `span-not-in-record` |

Counting commands (pasteable; the first re-derives the after-state alone, the
second re-derives the load-bearing property):

```sh
python3 -I -X utf8 tools/wave-reconcile.py --selftest | tail -1
bash tools/mutate-and-run.sh --target tools/wave-reconcile.py \
  --defects tools/wave-reconcile-mutants.spec \
  --suite 'python3 -I -X utf8 "$MUTANT" --selftest' \
  --workdir "$HYAKU_SCRATCH/tameshi-r75/l1/battery" --label wave-reconcile-arms-r75
```

Expected after-state: `WAVE_RECONCILE_SELFTEST: 18/18 pass` exit 0; the battery
prints `CONTROL: GREEN`, each of the three new defects `KILLED` with its FAIL
line on its **named** arm only (`arm16`, `arm17`, `arm18`), the suite at
`17/18` under each mutation, `MUTATE_RESTORE: OK` byte-identical and
`MUTATE: DONE (… defects=6 killed=6 survived=0 inconclusive=0 kill-rate=100%)`
for the six-defect spec (the three round-74 defects plus the three new ones).

**Kill rule (frozen).** C1 fails if (i) any of the three named mutants still
passes every arm; (ii) any mutant is killed by an arm other than the one it is
named against; (iii) any pre-existing arm 1–15 changes its `ok`/`got` outcome;
(iv) the arm count is not exactly 18; (v) a new arm fails on the unmutated
copy (an always-fail arm is not a kill); or (vi) the battery control is not
GREEN or the restore is not byte-identical.

**Controls (pre-data).** The do-nothing control is the base measurement above:
installing no arm leaves `15/15` and all three mutants alive. The always-fail
control: each new arm must pass on the unmutated copy (checked by the suite
itself) and fail only under its mutant.

## R75-C2 — calibration (lowest scored numeric axis, 8): the live capability rows re-derive from their instruments

**Before (measured at base, receipt `.ufo/evidence/round-75/base-measure-c2.txt`).**
Round-74 closure defect 3 (`corpus/lessons/round-74-verifier-spotcheck.md` §6
item 3) found two live capability rows quoting figures the tip tools no longer
print. The control scan (`.ufo/evidence/round-75/selfstate-control-scan.py`,
the L1's pre-freeze prototype) reads the SCORECARD `## Capabilities` table at
`21ef81e9` and compares 16 declared figure spans against the lane instruments
that print them: `SELFSTATE_CONTROL: rows=16 match=9 stale=7` exit 1. The seven
stale figures are the commit-bind selftest (`4/4` vs `7/7`), the quoted-line
selftest (`4/4` vs `5/5`), the arm-liveness selftest (`4/4` vs `5/5`), the
arm-liveness standing sweep (`rows=3 live=3 dead=0` vs `rows=9 live=9 dead=0`),
the anchor-drift sweep (`rows=4` vs `rows=16`), the line-pointer sweep
(`rows=8` vs `rows=12`) and the additivity sweep (`rows=6` vs `rows=11`).

**After.** `tools/selfstate-freshness.py` + `tools/selfstate-freshness.json`:
a declared population of 17 rows — 16 live capability figures
(`mode: capability`, located by exact first-cell name in the `## Capabilities`
section at `--doc-rev`) and 1 frozen historical statement (`mode: span`, the
round-74 block's `ADDRANGE: rows=6 met=6 unexpected=0` line, `expect: stale`).
Each row carries the figure regex and the instrument (path, pinned rev, argv);
the instrument is extracted from git objects at its rev and run
`python -I -X utf8` with `TMPDIR` honoured, and its stdout is searched with the
same regex. A row measures `match` when the doc's figure equals the
instrument's; `expect: match|stale` makes a divergence `unexpected`. Absent
capability row or absent figure is a **setup refusal (exit 2)**, never a pass.

Counting command (pasteable):

```sh
python3 -I -X utf8 tools/selfstate-freshness.py --repo . \
  --manifest tools/selfstate-freshness.json --doc-rev <rev> | tail -1
```

Expected after-state at the landing tip:
`SELFSTATE: rows=17 match=16 stale=1 unexpected=0` exit 0, with every live row
reading `match` and the frozen row reading
`SELFSTATE_ROW r74-frozen-addr-six expect=stale measured=stale ok`. Before
state with the same instrument at `21ef81e9`:
`SELFSTATE: rows=17 match=9 stale=8 unexpected=7` exit 1.

The seven live repairs this forces (SCORECARD capability cells, superseded in
place with the historical receipts left untouched): commit-bind `4/4` → `7/7`;
quoted-line `4/4` → `5/5`; arm-liveness `4/4` → `5/5` and `rows=3` → `rows=9`;
anchor-drift `rows=4` → `rows=16`; line-pointer `rows=8` → `rows=12`;
additivity `rows=6` → `rows=11`.

**Kill rule (frozen).** C2 fails if (i) `unexpected≠0` at the landing tip;
(ii) any declared live capability row is absent from the table or its figure
regex matches nothing (setup refusal is a failure to measure, not a pass);
(iii) the frozen red row does not measure `stale`; (iv) the row population is
not exactly 17; or (v) a row's `measured` value is not the instrument's own
stdout token (an echo/copy of the doc is not a measurement — the instrument
prints `measured=` per row and the receipt carries the raw instrument stdout).

**Controls (pre-data).** (1) Do-nothing: the same scan at `21ef81e9` reads
`stale=7`, so the target `unexpected=0` is unreachable by doing nothing.
(2) Echo-stub: a counter that copies the doc's own figure as the measurement
reads `stale=0`; the count alone is not self-authenticating, so the receipt
carries the per-row `measured=` tokens and the frozen red row must read
`stale` on every sweep. (3) Row-deletion: the instrument refuses a manifest row
whose capability no longer resolves (setup exit 2), so deleting a row cannot
lower the count.

## Frontier step (part of the round, not a claim)

- **Source, re-opened: S006** (`shmutant README`, tier A code, held since
  2026-10-19 at `currentOid 7eefc730…`). Re-opened this round for the
  witness-scoped verdict ground the new arms rest on; the row's status,
  `recheck` and anchor stay as written (append-only). `used-by` old → new:
  `corpus/knowledge/witness-scoped-kill-verdict.md,
  corpus/knowledge/mutation-score-semantics.md, corpus/lessons/round-12.md` →
  the same plus `corpus/lessons/round-75.md`. Fetch receipt and snapshot:
  `.ufo/evidence/round-75/sources/s006-shmutant-readme.md` (+ headers).
- **Reject, standing:** a new shmutant row at the current bytes — same URL,
  same document, within-scope duplicate (CORPUS.md rule 2; the S289/S293
  precedent). Flip condition: the row is retired or the page is superseded.
- **Census before:** `.ufo/evidence/round-75/census-start.txt` (exit 0, 164
  rows); must read exit 0 at round end.
- **Mistake to mine** (`corpus/lessons/round-75.md` `## Mistakes`): the stale
  live capability figures (class `number-drift`/`stale-premise`, evidence the
  round-74 closure defect 3 + this round's control scan, captured-by `none`);
  and the control prototype's first run deriving its repo root from
  `__file__`, which measured nothing (class `reference-drift`, captured-by the
  instrument's own `--repo` requirement).

## Cold-read / landing plan

Monitored edits this round (forecast receipt
`.ufo/evidence/round-75/rekey-cost-r75.txt`): `SCORECARD.md`, `LOG.md`,
`corpus/SOURCES.md`, `corpus/QUALITY.md` →
`REKEY_COST sections=64 planned=4 at_risk=13 predicted_lost=13`. One rekey
batch (`r75-batch-1`) after every content edit; the monitor must read
`credited=64/64` at the landing tip. No `SKILL.md` edit is planned this round
(the registry-table carry stays open, named in the report).

## Write scope and landing order

Lane repo `/home/vgpnk/Projects/shokunin/tameshi-shokunin` only (plus the
fleet report and an L0 line). Order: (1) declaration commit — this plan, the
LOG declaration, the pre-data receipts; (2) the wave; (3) C1 tool + spec +
battery receipt; (4) C2 instrument + manifest + selftest + receipts; (5) the
seven SCORECARD cell supersessions, the round-75 SCORECARD block, the lesson
(Gate + Mistakes), the S006 `used-by` append and Round-75 SOURCES note, the
QUALITY criterion; (6) the rekey batch; (7) the report (cites the pushed lane
tip) and the fleet commit.

### Correction 1 (appended before any claim data, 2026-11-04)

Kill rule (ii) as first written — "any mutant is killed by an arm other than
the one it is named against" — cannot hold for the pre-existing round-74
mutants once the new arms land: arm16 exercises `delimited()` (m2's rule) and
arms 17/18 exercise the record-span guard (the span-rule mutant's rule), so
both pre-existing mutants fail those new arms as collateral. Measured
pre-freeze on the L1's own 18-arm candidate (identical target: `18/18 pass`,
six defects killed), receipt `.ufo/evidence/round-75/l1-c1-battery.txt`:
`m2` fails arm13 AND arm16; the span-rule mutant fails arm14, arm17 and arm18;
the three round-75 mutants each fail only their own named arm. Corrected rule
(ii): each of the three R75 mutants dies on its own named arm and on no other
arm; a pre-existing mutant must keep its named-arm kill, and collateral
failures on the new arms are expected, not disqualifying. The after-state
target (`18/18 pass`; six defects killed on their named arms) is unchanged.

### Correction 2 (appended before the C2 after-state is measured, 2026-11-04)

The wave's critic (T75W1C1) measured a control that reaches C2's target without
the claimed work and a wording/sizing defect; both are adopted here as a
control freeze, not a target change. The predicate (`SELFSTATE: rows=17
match=16 stale=1 unexpected=0`) and the seven repair cells are unchanged.

1. **The population is the frozen tuple table, not any manifest.** The 16 live
   rows are exactly the (capability, figure regex, instrument path, argv)
   tuples listed in SPECS of the committed pre-freeze prototype
   `.ufo/evidence/round-75/selfstate-control-scan.py`, each instrument pinned at
   `21ef81e9`; the 17th row is the frozen span row `r74-frozen-addr-six`
   (`expect: stale`) exactly as declared. The landed
   `tools/selfstate-freshness.json` must equal that table (id, mode, capability,
   figure, instrument path/rev/argv, expect). A manifest that differs — a
   laxer regex, a foreign instrument, a dropped row — is not this claim's
   counter, whatever its summary prints.
   *Control 4 measured* (`.ufo/evidence/round-75/controls-c75b.txt`): with each
   live regex replaced by a token common to doc and instrument but not the
   figure (the verdict prefix, or `dead=0`), the same instrument prints
   `SELFSTATE: rows=17 match=16 stale=1 unexpected=0` exit 0 at base with zero
   repairs. The tuple freeze is what fails that manifest; the count alone is
   not self-authenticating.
2. **Population wording.** "The live capability rows re-derive" reads, from
   here on, as **the 16 declared live figures on 10 capability rows** (the
   prototype's population). The `## Capabilities` table holds 24 rows; rows
   outside the population are named in the report. The `mutation sweep runner`
   (`80/80` → `107/107`) and `wave-record reconciliation` (`12/12` → `18/18`)
   cells are superseded with C1's landing as out-of-population record repairs;
   `six-leg content-disposition probe` (`18/18` → `19/19`) and
   `effective expectation reconciliation` (`34/34` → `66/66`) stay as written
   under the round-17 dated-literal disclosure (`SCORECARD.md:655-659`) and are
   routed to round 76 as a named defect (the disclosure's own superseding
   figures are themselves stale: `95/95` and `56/56`).
3. **C1 kill rule (ii) matrix disclosed.** The measured six-defect matrix is
   `m2` → 16/18 (arm13 + arm16), span-rule → 15/18 (arm14 + arm17 + arm18),
   seat-reports → 17/18 (arm15), and each of the three R75 mutants → 17/18 on
   its named arm only. The earlier sentence "the suite at `17/18` under each
   mutation" is superseded by this matrix; the after-state target (`18/18`;
   `killed=6`) is unchanged. Correction 1's rule (ii) scope stands.
4. **Rule (iii) baseline and mutant pins in the receipts.** The pristine →
   candidate arms 1–15 line diff is `c1-arms1-15-diff.txt` (no output: PASS);
   the three base mutants' exact `@old`/`@new` edits and sha256 are appended to
   `base-measure-c1.txt`, and the landed spec's first three `@defect` blocks are
   byte-identical to `21ef81e9:tools/wave-reconcile-mutants.spec` (three
   appended blocks only), checked in the C1 battery receipt.
5. **Sourced-claim quote location.** The S006 re-open carries the 14-word
   located quote "A harness that only checks for \"red\" banks three very
   different outcomes as passes." (`§The three verdicts`, extract line 24) in
   the lesson Gate and the SOURCES note, plus the raw URL and the snapshot
   sha256 (`960577288ed5c5eb80f42669fcb30bf254b9a917ae2bde3a117888056ef354e2`).

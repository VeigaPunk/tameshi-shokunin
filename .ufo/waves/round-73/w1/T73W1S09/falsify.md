# T73W1S09 — falsification review of R73-C1 and R73-C2

Seat: critic/falsifier, round-73 w1. Every tracked file read-only; all writes under
`/fast/scratch/hyaku/tameshi-r73/T73W1S09/` (deleted before yield). No subagents.
No git/jj mutation; fixture work used `git -C <lane> archive` / `git -C <lane> show`
(read-only) into scratch trees.

Tips the counters were measured at when the headline block below was captured:
lane `7c5ffe04` (`round-73: pointer-recheck note in the file's own UTF-8 style`), fleet
`b3697f75`. The lane advanced several times during the review (first observed `17cd1939`;
tips measured `2e89e539`, `3e0ef1c8`, `caa5c4c5`, `7c5ffe04`); the four frozen lines were
re-measured at each and never changed. The round-72 artifacts the manifest pins were
unchanged across all of them, and C1's rows are rev-pinned so no tip move can affect them.

What I did **not** run: the plan's three pre-freeze controls (i)–(iii) — those are the L1's
rehearsal receipts at `.ufo/evidence/round-73/reh/reh-c1-controls.txt`; I ran my own cheaper
control instead (Q1b). No check below is claimed that does not carry its command and output.

## Frozen counters at the reviewed tip

```
$ cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
$ python3 -I -X utf8 tools/wave-reconcile.py --selftest
...
WAVE_RECONCILE_SELFTEST: 12/12 pass
exit=0

$ python3 -I -X utf8 tools/wave-reconcile.py --repo . \
    --extra-root fleet=/home/vgpnk/Projects/shokunin --manifest tools/wave-reconcile.json
WAVE_ROW r72-report-seats kind=seats expect=meet measured=meet ok | printed=12 seats=12 records=12
WAVE_ROW r72-report-seatreports kind=seat_reports expect=drift measured=drift ok | printed=11 files=12
WAVE_ROW r72-plan-seats kind=seats expect=meet measured=meet ok | printed=12 seats=12 records=12
WAVE_ROW r72-spec-roles kind=roles expect=meet measured=meet ok | declared={"connector": 1, ... "revenger": 1, ...} measured={same}
WAVE_ROW r72-plan-roles kind=roles expect=drift measured=drift ok | declared={... "labrat": 1 ...} measured={... "revenger": 1 ...}
WAVE_ROW r72-attack-share kind=attack_share expect=meet measured=meet ok | attack=3/12=25.0% floor=25.0%
WAVE_RECONCILE: rows=6 met=6 unexpected=0
exit=0

$ python3 -I tools/rekey-cost.py --arms
REKEY_ARM sources        expected=13 measured=13 ok
REKEY_ARM province       expected=6 measured=6 ok
REKEY_ARM quality        expected=6 measured=6 ok
REKEY_ARM scorecard      expected=0 measured=0 ok
REKEY_ARM pointer        expected=0 measured=0 ok
REKEY_ARM union          expected=17 measured=17 ok
REKEY_ARM ignored-skill  expected=0 measured=0 ok
REKEY_ARMS: arms=7 meet=7 unexpected=0
exit=0

$ python3 -I tools/rekey-cost.py --selftest
REKEY_COST_SELFTEST: 8/8 pass
exit=0
```

Both claims' frozen predicates are literally met at the tip. The rest of this document
tests whether those lines mean what the claims say they mean.

---

## 1. Does C1's counter require the work? Can a tool-less tree reach the line?

**1a. No tool → no line.** Two independent scratch trees, both without
`tools/wave-reconcile.py`:

```
$ S=/fast/scratch/hyaku/tameshi-r73/T73W1S09
$ git -C <lane> archive a3dd35742eee608d1205843dacebc461b4242b9e | tar -x -C $S/q1/notool
$ cd $S/q1/notool && python3 -I -X utf8 tools/wave-reconcile.py --selftest
python3: can't open file '.../q1/notool/tools/wave-reconcile.py': [Errno 2] No such file or directory
EXIT=2
$ python3 -I -X utf8 tools/wave-reconcile.py --repo . \
    --extra-root fleet=/home/vgpnk/Projects/shokunin --manifest tools/wave-reconcile.json
python3: can't open file '.../q1/notool/tools/wave-reconcile.py': [Errno 2] No such file or directory
EXIT=2
```

The same at the reviewed tip with the instrument deleted from an `archive HEAD` copy
(`$S/q1/tip-notool`): identical two lines, `EXIT=2`. The base tree cannot print the sweep
line at all — the plan's "before" measurement is confirmed.

**1b. …but the frozen *strings* are reachable with zero reconciliation.** A stub whose whole
implementation is two prints (`$S/q1/stub/tools/wave-reconcile.py`) passes both frozen
commands verbatim:

```
$ cd $S/q1/stub && python3 -I -X utf8 tools/wave-reconcile.py --selftest
WAVE_RECONCILE_SELFTEST: 12/12 pass
EXIT=0
$ python3 -I -X utf8 tools/wave-reconcile.py --repo . \
    --extra-root fleet=/home/vgpnk/Projects/shokunin --manifest tools/wave-reconcile.json
WAVE_RECONCILE: rows=6 met=6 unexpected=0
EXIT=0
```

So the frozen counter pair is *necessary but not sufficient*. It does not distinguish the
committed reconciler from a printer; the discriminating part is the row engine (which the
stub never touches). This is a calibration limit of the counter block, not of the tool.

**1c. The red arm is load-bearing.** Flipping `r72-report-seatreports` from `expect=drift` to
`expect=meet` on a scratch manifest and re-running the committed tool:

```
WAVE_ROW r72-report-seatreports kind=seat_reports expect=meet measured=drift MISMATCH | printed=11 files=12
WAVE_MISMATCH r72-report-seatreports expect=meet measured=drift
WAVE_RECONCILE: rows=6 met=5 unexpected=1
exit=1
```

The drift is measured, not asserted; the manifest's `expect` column is doing real work.

**1d. Missing root is an uncaught exception, not the declared setup exit.** Omit
`--extra-root` and the tool violates its own "exit 2 setup" contract:

```
$ python3 -I -X utf8 tools/wave-reconcile.py --repo . --manifest tools/wave-reconcile.json
  File ".../tools/wave-reconcile.py", line 152, in _record_span
    reader = readers[rec.get('root', 'lane')]
KeyError: 'fleet'
EXIT=1
```

`_artifact()` guards this case (`unknown-root` → SetupError → exit 2); `_record_span()` and
the `roles` declaration reader index the dict raw. A runner who forgets the fleet root sees
a traceback and exit 1 — the *drift* exit class — with no `WAVE_RECONCILE` line.

**1e. Three of six rows carry `record` blocks the engine never reads.** Poisoning
`record.span` / `record.printed` on `r72-spec-roles`, `r72-plan-roles`, `r72-attack-share`
with `"NOT-A-BYTE-SUBSTRING-OF-THIS-RECORD"` / `999`:

```
WAVE_ROW r72-spec-roles ... measured=meet ok
WAVE_ROW r72-plan-roles ... measured=drift ok
WAVE_ROW r72-attack-share ... measured=meet ok
WAVE_RECONCILE: rows=6 met=6 unexpected=0
exit=0
```

`measure()` calls `_record_span()` only for `seats` and `seat_reports`. The docstring's
"the record span must be a byte substring of the record" is true for 2 of 6 rows; the other
three `record` blocks are dead config. The plan-roles red arm is still genuinely bound — by
its *declaration* span, which is enforced:

```
$ (declaration span poisoned) python3 -I -X utf8 tools/wave-reconcile.py ...
WAVE_RECONCILE error=setup:span-not-in-record:r72-plan-roles:plans/round-72.plan.md
exit=2
```

**Answer (1):** no tool-less tree can reach the line (exit 2). But the counter *strings* are
reachable by a printer stub, so the pair is not by itself evidence of the re-derivation; the
manifest rows are, and they were verified working (1c) with one enforced-span red arm (1e).

---

## 2. Are C1's two red arms genuinely red, or a stale-rev artifact?

Re-pinned both red rows to the round-73 tips (record, declaration and artifact revs all set
to the tip SHAs) and re-ran the same engine:

```
lane_tip=7c5ffe04637d27316cf84eda3cc1e836358e658a
fleet_tip=b3697f75df1efdba599f9d00aa68c4f4f3d25131
--- base manifest (a3dd3574 / 3664a6d3 rows) -> exit=0
WAVE_ROW r72-report-seatreports ... expect=drift measured=drift ok | printed=11 files=12
WAVE_ROW r72-plan-roles        ... expect=drift measured=drift ok | declared={... "labrat": 1 ...} measured={... "revenger": 1 ...}
WAVE_RECONCILE: rows=6 met=6 unexpected=0
--- re-pinned at round-73 tips -> exit=0
WAVE_ROW r72-report-seatreports ... expect=drift measured=drift ok | printed=11 files=12
WAVE_ROW r72-plan-roles        ... expect=drift measured=drift ok | declared={... "labrat": 1 ...} measured={... "revenger": 1 ...}
WAVE_RECONCILE: rows=6 met=6 unexpected=0
```

Why this is not a stale-rev artifact:

* The fleet report blob is `7f8c8017af897291245d06f6045af59fdbe695a1` at `3664a6d3` **and**
  at the current fleet tip; `git log -1 -- .ufo/reports/round-72/tameshi.md` is still
  `3664a6d3 round-72: tameshi report`. Nothing was corrected after the pinned rev.
* The report contradicts itself *within one document* at the tip: line 56
  `12 seats, 11 reports; three seats found real` and line 81
  `All 12 seats settled and returned a report (w1/*.md)`. The "11" is a live arithmetic
  error, not a historical one. (I searched the file for "erratum"/"correction": no erratum
  for this line exists in the fleet report.)
* The wave artifacts are unchanged: 12 top-level `*.md`, 12 records, at `a3dd3574` and at
  the tip; `results.seats=12`.
* The plan's `1 labrat` line still exists at the tip at char 7123, because the round-73
  plan erratum (`3e0ef1c8`) is append-only: it names the drift and leaves the frozen line
  standing, so the roles arm still reads `drift` at the tip. Had the erratum rewritten the
  file, the row would have become setup exit 2 (`span-not-in-record`), i.e. the meter would
  have gone dark, not green — the append-only discipline is what keeps the arm measurable.

**Answer (2):** genuinely red at the tip; not a stale-rev artifact. The roles arm now meters a
*known and errata'd* defect (by design), the seat_reports arm meters a *live* uncorrected one.

---

## 3. C2 `--arms`: behaviour change or re-spelling of receipts?

Provenance of every arm value, parsed from the committed tool and every committed receipt:

```
== ARM_TABLE parsed from tools/rekey-cost.py
sources        edits=corpus/SOURCES.md                 expected=13
province       edits=PROVINCE.md                       expected=6
quality        edits=corpus/QUALITY.md                 expected=6
scorecard      edits=SCORECARD.md                      expected=0
pointer        edits=tools/pointer-recheck.json        expected=0
union          edits=corpus/SOURCES.md,PROVINCE.md     expected=17
ignored-skill  edits=SKILL.md                          expected=0

== per-arm provenance
sources        expected=13  recorded_in=cost-arm-sources.txt,cost-live-arm-sources.txt        EXISTING
province       expected=6   recorded_in=cost-arm-province.txt,cost-live-arm-province.txt      EXISTING
quality        expected=6   recorded_in=cost-arm-quality.txt,cost-live-arm-quality.txt        EXISTING
scorecard      expected=0   recorded_in=cost-arm-scorecard.txt,cost-live-arm-scorecard.txt    EXISTING
pointer        expected=0   recorded_in=cost-arm-pointer.txt,cost-live-arm-pointer.txt        EXISTING
union          expected=17  recorded_in=cost-prediction-at-edit.json,cost-round-plan-r72.txt     EXISTING
ignored-skill  expected=0   recorded_in=NONE                                                  NEW

== byte identity: cost-arm-* vs cost-live-arm-*   (all six)  True
```

* Six of seven values already existed. Only `ignored-skill 0` is new; its value is
  indistinguishable from the pointer/scorecard arms' `0` — its whole content is the *path*
  `SKILL.md`.
* `cost-live-arm-*.txt` and `cost-arm-*.txt` are byte-identical for all six names: the
  "live" receipts carried no information the older ones did not.
* The `union 17` value lived in `cost-prediction-at-edit.json` (`"at_risk": 17`) and
  `cost-round-plan-r72.txt` (`at_risk=17`), **not** in any `cost-live-arm-*.txt` — the
  plan's sentence "those six values existed only as static receipts
  (`cost-live-arm-*.txt`)" is imprecise for one of the six.
* One recorded live arm is *not* in the battery: `cost-live-arm-empty.txt` (no planned path,
  exit 2). It stays in the selftest's fixture (`arm6-empty-set-setup`), as the plan says, so
  the battery's `arms=7` = five receipt values + union + the new ignored arm.
* `--arms` changes no forecast semantics: the committed diff touches only the docstring,
  `ARM_TABLE`, `run_arms()` and `argparse`; `forecast()`, `latest_entries()`, `IGNORED` and
  the selftest are untouched (`git diff a3dd3574..HEAD -- tools/rekey-cost.py`, 74 insertions,
  2 deletions, all in the battery block/docstring/argparse).

**Answer (3):** a re-spelling of five receipt values plus one union value recorded elsewhere,
*plus* exactly one new arm. The capability delta is re-runnability (executed vs replayed),
which is what the claim says; no new forecast behaviour is claimed or delivered.

---

## 4. Is M3 the right mutant for the ignored class?

Four mutants of the same `IGNORED` literal, built in scratch by string replacement of

```
IGNORED = frozenset((SKILL, '.ufo/evidence/round-17/coldread/ledger.json',
                     LEDGER))
```

and scored with the committed battery (`--repo <lane>`) and the frozen selftest:

| mutant | replacement | battery | selftest |
|---|---|---|---|
| pristine | — | `arms=7 meet=7 unexpected=0` exit 0 | 8/8 exit 0 |
| **M3** all members dropped | `IGNORED = frozenset()` | `meet=6 unexpected=1` (ignored-skill 0→**9**) exit 1 | 7/8 (arm5) exit 1 |
| **M3a** SKILL only dropped (cheaper) | `frozenset(('.ufo/…/round-17/…ledger.json', LEDGER))` | `meet=6 unexpected=1` (ignored-skill 0→**9**) exit 1 | 7/8 exit 1 |
| **M3b** ledger members dropped | `frozenset((SKILL,))` | **`meet=7 unexpected=0` exit 0 — survives** | **8/8 exit 0 — survives** |
| **M3c** a real pin swallowed (stronger) | `frozenset((SKILL, '…round-17…', LEDGER, 'corpus/knowledge/fleet-kill-rate-ledger.md'))` | **`meet=7 unexpected=0` exit 0 — survives** | **8/8 exit 0 — survives** |

Mutant bytes: pristine `85ca2b69…bd88f4`, M3 `7e0fdf62…81db844` — **identical to the sha256
pair pinned in `.ufo/evidence/round-73/reh/README.txt`**, so this reproduction is the same M3.

M3 over the six recorded arms (`--edit` per arm, pristine vs M3):

```
sources   at_risk=13 vs 13  SAME      scorecard at_risk=0 vs 0   SAME
province  at_risk=6  vs 6   SAME      pointer   at_risk=0 vs 0   SAME
quality   at_risk=6  vs 6   SAME      union     at_risk=17 vs 17 SAME
empty     exit2      vs exit2 SAME
KILLING_ARMS=0/7   (0/6 over either six-arm grouping: the receipt set or the battery set)
```

The directional argument, measured two ways:

* Removing an `IGNORED` member can only *add* pins → at_risk can only rise. M3 is a
  **conservative-direction** mutant: it over-reports (`SKILL.md` 0 → 9). A battery that
  kills M3 proves the filter is *not over-permissive to the point of hiding SKILL.md*; it
  does not prove the filter is *sound*.
* The dangerous direction is over-filtering (a real pin swallowed → false green). M3c does
  exactly that: `--edit corpus/knowledge/fleet-kill-rate-ledger.md` reads **20** under the
  pristine bytes and **0** under M3c, while all seven arms and all eight selftest arms stay
  green. That is a silent under-report of 20 sections the credit rule would owe.
* M3b shows the two ledger members are exercised by neither the battery nor the selftest:
  only 1 of the 3 IGNORED members has any arm covering it.
* M3a is a strictly smaller edit set (one member vs three) and is killed identically — the
  kill hinges on the `SKILL` member alone, not on the filter as a class.

**Answer (4):** M3 is a *sufficient* killer but not the minimal one (M3a is cheaper and also
killed), and it tests only the conservative direction. A stronger mutant (M3c) survives both
the battery and the selftest while turning a 20-pin forecast into a false `0`.

---

## 5. Are the claims causally separable?

**Bytes.** No cross-reference exists in either direction:

```
tools/wave-reconcile.py    mentions rekey-cost: False ; mentions rekey: False
tools/wave-reconcile.json  mentions rekey-cost: False ; mentions rekey: False
tools/rekey-cost.py        mentions wave-reconcile: False ; mentions WAVE_RECONCILE: False
```

The commits are file-disjoint: `fddbb667` = `tools/wave-reconcile.{py,json}` (+624);
`7982619f` = `tools/rekey-cost.py` (+74/−2). C1's rows read only git objects at revs frozen
before the round (`a3dd3574`, `3664a6d3`) — C1 is immune to the round's live edits. C2 reads
only `SKILL.md`, the round-21 ledger and the frozen `measure.py`.

**Values.** C2's frozen numbers are a function of ledger *content*, and the ledger is the
surface C1's corpus edits force the round to rekey. One legitimate rekey entry (the same
shape the round's own rebind writes) in a scratch fixture:

```
-- fixture ledger unmodified (copy of the committed ledger)
REKEY_ARMS: arms=7 meet=7 unexpected=0 | exit=0
-- after appending one entry for "## Standing rules" whose inputs no longer pin PROVINCE.md
   REKEY_ARM province       expected=6 measured=5 UNEXPECTED
   REKEY_ARM quality        expected=6 measured=5 UNEXPECTED
   ARM_UNEXPECTED province expected=6 measured=5
   ARM_UNEXPECTED quality  expected=6 measured=5
   summary: REKEY_ARMS: arms=7 meet=5 unexpected=2 | exit=1
```

(The same section pins both `PROVINCE.md` and `corpus/QUALITY.md`, hence two arms move.) So
C2 is *not* causally independent of the corpus work at the value level — only at the byte
level. The round's own rekey path happens to preserve the pins (both batches did: ledger
820 → 833 → 846, and `--arms` was green at every observed tip), because the rebind rewrites
each entry's full input set. The dependency is real but currently benign; it is exactly the
"recorded amendment" the tool's docstring declares.

**Answer (5):** separable in bytes (verified), and currently separable in values — but only
because the round's rekey preserved pins; the battery's expected values are downstream of
ledger writes that C1's edits trigger, and one narrowed rekey entry flips two arms.

---

## 6. Does either claim harm an axis? Which edited surface is not rekeyed?

Round-edited tracked files (`git diff --name-only a3dd3574..HEAD`, `.ufo/` excluded) and the
committed forecast for each:

| edited surface | forecast | rekeyed? |
|---|---|---|
| `corpus/SOURCES.md` | `at_risk=13` | yes — rekey batch 1+2; `live-green` `lost=0 ok`, rev mode `credited=64/64` |
| `corpus/QUALITY.md` | `at_risk=6` | yes — same two batches; union of the two = **13** (`--edit … --edit …` → `at_risk=13`) |
| `tools/pointer-recheck.json` | `at_risk=0` | not needed (unpinned) |
| `tools/rekey-cost.py` | `at_risk=0` | not needed |
| `tools/wave-reconcile.py`, `.json` | `at_risk=0` | not needed |
| `plans/round-72.plan.md`, `plans/round-73.plan.md` | `at_risk=0` | not needed |
| `LOG.md`, `corpus/lessons/round-73.md` | `at_risk=0` | not needed |

RED-at-edit receipt matches the forecast (`lost=13 RED`), and both rekey batches restored
`lost=0 ok` / `credited=64/64` (`live-green-r73.out`, `live-green-b2-r73.out`,
`live-revmode*`). **No edited pinned surface is left unrekeyed.**

Axis costs found, none of them a regression:

* **Calibration (C1).** The counter pair is printer-passable (Q1b); one red arm is
  span-enforced while three `record` blocks are inert (Q1e); a missing `--extra-root` exits
  1 with a traceback instead of setup exit 2 (Q1d). None of these touch the six measured
  rows.
* **Coverage (C2).** The ignored *class* is covered at 1 of 3 members; over-filtering is
  invisible (Q4: M3b, M3c survive battery + selftest).
* **Freshness (C2).** The arm table is ledger-coupled: any pin move turns the battery red
  and requires a recorded amendment of `tools/rekey-cost.py` (measured in Q5). It fails
  loudly, so it is a maintenance cost, not a silent one.
* **Adjacency (C1).** 3 of 6 rows read the *fleet* repo
  (`r72-report-seats`, `r72-report-seatreports`, `r72-attack-share`; `record.root=fleet`).
  The lane's standing counter cannot run from the lane alone, and the frozen command
  hard-codes `/home/vgpnk/Projects/shokunin`.
* **False generalization in the plan's no-harm paragraph.** "`tools/*` forecast 0 (no
  section pins them)" is false: `tools/trace-inputs.py` → `at_risk=35`,
  `tools/mutate-and-run.sh` → `at_risk=35`. The conclusion holds for *this round's* tool
  edits only because those specific files are unpinned. Likewise "evidence paths are free"
  is only true for *new* paths: `.ufo/evidence/round-18/final/checks.json` → `at_risk=13`.

**Answer (6):** no axis harm measured; every pinned edited surface was rekeyed and the guard
reads green at both floors. The costs are calibration/coverage limits plus the false
generalizations above, which should be scoped to the enumerated edit set.

---

## Smallest safe corrections (no frozen output changes)

1. **C1 — guard the root lookup.** In `_record_span()` (and the `roles` declaration reader),
   replace `readers[rec.get('root', 'lane')]` with the `_artifact()` pattern
   (`if root not in readers: raise SetupError('unknown-root:…')`). Exit 2 instead of a
   traceback; no selftest or sweep line moves (no arm exercises an absent root).
2. **C1 — delete the three inert `record` blocks** (`r72-spec-roles`, `r72-plan-roles`,
   `r72-attack-share`) or wire `_record_span()` into them. Measured: poisoning them changes
   nothing, so deletion keeps `rows=6 met=6 unexpected=0`.
3. **C1 — add a negative counter run** to the frozen counter block (the `expect`-flip in
   Q1c must print `WAVE_RECONCILE: rows=6 met=5 unexpected=1`, exit 1). Zero tool bytes
   changed; it is the one cheap line that separates the reconciler from a printer.
4. **C2 — add one fail-closed arm** to kill the unsafe direction: an arm asserting that a
   *pinned* path is not swallowed (e.g. `--edit corpus/knowledge/fleet-kill-rate-ledger.md`
   expected 20, or a meta-assertion `IGNORED == <frozen three>`) . Kills M3c/M3b at zero
   cost; alternatively, state in the docstring that M3 is a conservative-direction mutant.

## Verdicts

C1 upheld
C2 upheld

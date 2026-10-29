# T57W2ConnectorWaves — cross-wave pattern finder (round 57, wave 2)

Seat: `T57W2ConnectorWaves` (leaf connector; no subagent dispatch). Lane repo
`/home/vgpnk/Projects/shokunin/tameshi-shokunin`; lane base `5e3569969b532310d2b8a3d130901757a3df356b`;
content commit C0 `ca75c2674645ab6bdadeecb8584007c74342bfa9` (landed); wave-1 evidence commit
`06e9849` (landed). **No lane file was edited. No frozen path was touched. No tool was installed.**

Inputs: all 47 wave-1 reports under `.ufo/waves/round-57/w1/*.md` (read in full), the wave-1
`.json` siblings, the wave-1 receipts, the lane's C0 tree, the installed counters
`.ufo/evidence/round-57/c1/measure.py` and `.ufo/evidence/round-57/c2/measure.py`, and the
L1's own dry-run scripts `.ufo/waves/round-57/dry-c1.sh` and `dry-c2.sh`.

Scratch: `export HYAKU_SCRATCH=/fast/scratch/hyaku; S=$HYAKU_SCRATCH/tameshi-r57/T57W2ConnectorWaves`.
Clones: `git clone --shared <lane> $S/clone…`, `git -C "$S/clone…" checkout --detach <rev>`;
every git call names `-C`. Fixture commits were made only inside those clones with
`-c user.name=fixture -c user.email=fixture@example.invalid`. The lane and the fleet repo were
never mutated.

---

## 0. Method and the sweep that backs every claim below

Three sweeps were run, in this order, and each result is reproducible from the commands quoted.

**Sweep A — seat co-occurrence on candidate findings.** For each candidate finding a grep pattern
was run over all 47 wave-1 `.md` reports and the number of distinct seats hitting it was counted.
This is what turns "two seats said it" from an impression into a measurement.

```
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w1
for pat in 'R4\\d' 'exit 1' 'RECEIPT_REV_CONTENT_DRIFT' 'gate-kind\|kind .gate.\|gate row' \
           '64/64\|64 of 64' 'total=14\|total=13' 'R56\.2' 'R54\.8' 'R52\.3' \
           'open_unplanned' 'planned_ids'; do
  n=$(grep -l -- "$pat" *.md 2>/dev/null | wc -l); echo "$n seats  <- $pat"
  grep -l -- "$pat" *.md 2>/dev/null | sed 's/^/      /' | paste -sd' ' -
done
```

Output (seat counts):

| pattern | seats |
|---|---|
| `open_unplanned` | 15 |
| `R4\d` (inherited planned-id regex) | 15 |
| `planned_ids` | 14 |
| `gate-kind\|kind .gate.\|gate row` | 17 |
| `RECEIPT_REV_CONTENT_DRIFT` | 13 |
| `exit 1` | 11 |
| `64/64\|64 of 64` | 11 |
| `R56\.2` | 10 |
| `total=14\|total=13` | 4 |
| `R52\.3` | 4 |
| `R54\.8` | 3 |

**Sweep B — the two L1 dry runs, executed.** These are the only measurements of the *current*
tree and are the ground truth for every "is it still open" question below.

```
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
bash .ufo/waves/round-57/dry-c1.sh   # exit 0, 26 EXPLAIN lines  -> C1_R57_PASS=false total=21
bash .ufo/waves/round-57/dry-c2.sh   # exit 0, 16 EXPLAIN lines  -> C2_R57_PASS=true  total=0
```

C1 verdict line, verbatim:

```
C1_R57_TERMS: fixed=34 open=15 declined=2 fixed_this_round=7 missing=0 extra=0 duplicate=0
old49=0 spotcheck_changed=0 defects_pin=0 bad_status=0 evidence_bad=4 key_miss=8 fixed_bad=8
open_unplanned=0 declined_bad=0 fixed_short=0 declined_over=0 this_round_short=0 panel_pin=1
panel_over=0 base_status_bad=0
C1_R57: self=63a88c257490 rev=… rows=51/51 agree=31/51 old49=ok fixed=34 declined=2
thisround=7 panel=pin spot=ok total=21 C1_R57_PASS=false
```

C2 verdict line, verbatim:

```
C2_R57: self=7d49e3c493b3 rev=… gate_rows=3 exits=0,2,3 held=3/3 mutants=3/3 skill_row=1
codes_known=4/4 standing_cell=ok total=0 C2_R57_PASS=true
```

**Sweep C — the two rule sets scored over the same inputs.** The installed round-57 counter and
the inherited round-50 counter were both run over the *same* 51-item defect set and the *same*
ledger, so the difference is attributable to the rules, not to the data.

```
# round-50 rules, round-57 defect set, ledger at C0+fixture commit
python3 - <<'PY'
import importlib.util, json, subprocess
L='/fast/scratch/hyaku/tameshi-r57/T57W2ConnectorWaves/clone50b'
spec=importlib.util.spec_from_file_location('m50',L+'/.ufo/evidence/round-50/c1/measure.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
defs=json.load(open('/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-57/c1/defects.json'))
rev=subprocess.run(['git','-C',L,'rev-parse','HEAD'],capture_output=True,text=True).stdout.strip()
ex=[]; out=m.measure(L,rev,defs['defects'],True,fixed_floor=0,declined_cap=999,this_round_floor=0,
                      base='5e3569969b532310d2b8a3d130901757a3df356b',explain=lambda *a: ex.append(a))
print(out[1]); print(out[3])
PY
```

Result: `{'extra': 49, 'evidence_bad': 4, 'key_miss': 8, 'fixed_bad': 1, 'open_unplanned': 10}`,
`total=100`. The installed counter gives `key_miss=8, fixed_bad=8, open_unplanned=0, total=21`.

**The comparison is the sharpest result of this seat.** The **same 8 `key_miss` rows** fail under
both rule sets (R51.1, R51.6, R52.1, R52.2, R52.6, R54.5, R54.6, R56.1) — so `key_miss` is a
*data* defect in the key sets, not a rule defect. The **`fixed_bad` count differs 1 vs 8** — so the
seven extra `fixed_bad` rows are produced *only* by the round-57 Amendment-1 tie rule, not by the
inherited rules. That isolates the amendment as the cause. §2.3 below.

---

## 1. Findings two or more seats made independently (corroborated)

These are the cross-wave patterns. For each: what the seats found, the corroboration count, and
whether the finding is still live at the deciding revision.

### 1.1 The inherited round-50 counter cannot credit any R5x `open` row — 15 seats

**Seats (15):** `T57W1CritC1` §5, `T57W1CritClaimShape` C1-B4a, `T57W1ExecC1Counter`,
`T57W1ScribeItemsR51x5to8`, `R52x1to3`, `R52x4to6`, `R53x1to3`, `R53x4to6`, `R53x7to9`, `R54x1to4`,
`R54x8to10`, `R55x1to4`, `R56x1to4`, `R56x5to7`, `T57W1SentLedger` (item 5).

All fifteen report the same defect: `.ufo/evidence/round-50/c1/measure.py:111` has
`planned_ids` matching only `\bR4\d\.\d+\b`, so no `R5x` id is ever "planned" and every `open`
row for rounds 50–56 fails `open_unplanned`. `T57W1CritC1` measures it directly:
`re.findall` on `R51.1 R53.2 R56.7` with the R4 regex returns `[]`.

**Command:**
```
grep -n "R4\\\\d" /fast/scratch/.../clone/.ufo/evidence/round-50/c1/measure.py
# 111:    for rid in re.findall(r'\bR4\d\.\d+\b', para):
```

**Status at the deciding revision: FIXED.** The installed counter uses
`PLANNED_ID = re.compile(r'\bR5[0-6]\.\d+\b')` (`measure.py:81`) and selects the paragraph by
*round number*, not file position (`measure.py:139-146`, `int(m.group(1)) >= best`). The dry run
confirms `open_unplanned=0` with 15 open rows. This is the one wave-1 finding the L1 closed
completely.

### 1.2 The C1 `fixed` arm accepts a commit that never introduced its excerpt — 3 seats

**Seats:** `T57W1CritC1` §4 (R52.5 with commit `51d1f0eb`; "commit does not add this line",
`grep -c '^+.*fallback to /tmp'` → 0), `T57W1CritDoNothing` F1 (probe `C1_CTL_FAB_TEXT` reaches
`total=0 C1_R57_PASS=true` by quoting 51 excerpts into a new file), `T57W1ExecExtract` (keys are
"tokens a fixing excerpt in the tree would carry", keys are free).

Mechanism, named by `T57W1CritDoNothing`: `then = show(routed_at, path)`; a path that did not exist
at `routed_at` gives `then = None`, which counts as fresh. `T57W1CritC1` adds the second half: a
commit need not *introduce* the excerpt, only the excerpt be absent at `routed_at`.

**Status: FIXED by the installed counter**, which adds (a) the excerpt must be absent at the
commit's first parent and present at the commit, and (b) the commit must be tied to the item —
either the commit message names the item id, or the item's own text names the evidence path
(`measure.py:242-259`). This is the round-57 `Amendment 1`.

### 1.3 The gate's exit map is incomplete — exit 1 exists — 11 seats

**Seats (11):** `T57W1CritC2` (needle strength and "the mutant arm forces a row"),
`T57W1CritClaimShape` §2 (probe table: no arguments → exit 1), `T57W1CritDoNothing` F5,
`T57W1LabratRegistryCheck` F2 ("the gate's usage errors call `raise SystemExit('usage: …')` which
exits **1**… in registry-check exit 1 is the `differs` class, while the documented
could-not-evaluate class is 2"), `T57W1RevGateSurface` §2 (full exit-path table; "the map is
incomplete: exit 1 also exists"), `T57W1RevInherited`, `T57W1ScoutSourceA` (grep's own §2.3
"2 if an error occurred"), `T57W1ScribeItemsR53x1to3`, `T57W1ScribeKnowledge` finding 1,
`T57W1ScribeQuality`, `T57W1ScribeSourcesRow`.

**Command (executed, in a scratch clone):**
```
python3 tools/receipt-revision-gate.py --lane . --certified 5e35699… --receipt x:verdict
# → rc=1, usage text on stderr, no named code
```

**Status: FIXED at C0.** `SKILL.md:1547` now carries the row
`| receipt-revision gate | gate | … | 0 PASS; 2 certified revision unresolvable
(RECEIPT_REV_UNRESOLVABLE); 3 refused with a named code; 1 usage | …`. The dry C2 run reads
`skill_row=1`. `T57W1ScoutSourceA`'s GNU-grep row (`S283`, landed) is the external grounding the
contract's `sourced_claim` asked for.

### 1.4 The SKILL `## Standing rules` cell names the wrong code — 13 seats

**Seats (13):** `T57W1ConnectorCross` (class 1, R56.2), `T57W1CritC2`, `T57W1CritClaimShape` §2,
`T57W1CritDoNothing`, `T57W1ExecC2Counter`, `T57W1ExecRegistryRows`, `T57W1ExecStandingRules`,
`T57W1MutGate`, `T57W1RevGateSurface`, `T57W1ScribeItemsR55x5to7`, `R56x1to4`,
`T57W1ScribeKnowledge` finding 4, `T57W1SimplScope` D2.

All report: `SKILL.md:53` said `RECEIPT_REV_MISMATCH` for a verdict receipt on a declared
`--paths` surface, but the gate emits `RECEIPT_REV_CONTENT_DRIFT` on that branch
(`tools/receipt-revision-gate.py:151`) and `RECEIPT_REV_MISMATCH` only at line 146, the
`paths is None` branch. `T57W1ExecStandingRules` built the full 8-row truth table; `T57W1RevGateSurface`
independently built an 11-code reachability table over 44 invocations and reached the same
branch assignment.

**Command:**
```
sed -n '145,152p' tools/receipt-revision-gate.py
sed -n '53p'   SKILL.md     # before: RECEIPT_REV_MISMATCH
```

**Status: FIXED at C0.** `SKILL.md:53` now reads `RECEIPT_REV_CONTENT_DRIFT` with the
"with no `--paths` the code is `RECEIPT_REV_MISMATCH`" condition in the rule cell. The dry C2 run
prints `cell gate emitted=['RECEIPT_REV_CONTENT_DRIFT'] exit=3 verdict=REFUSED; table cell
carries=['RECEIPT_REV_CONTENT_DRIFT']` → `standing_cell=ok`.

### 1.5 The registry has zero `gate`-kind rows for the gate — 17 seats

**Seats (17):** the largest cross-seat agreement in wave 1. `T57W1CritC2`, `T57W1CritClaimShape`
§2 (`gate-rows-naming-gate 0`), `T57W1CritDoNothing` (`C2_CTL_0 … gate_rows=0`), `T57W1ExecC2Counter`
(base run `gate_rows=0`), `T57W1ExecControls`, `T57W1ExecNoHarm`, `T57W1ExecRegistryRows`,
`T57W1ExecStandingRules`, `T57W1LabratFloor`, `T57W1LabratRegistryCheck`, `T57W1RevExtractRecall`,
`T57W1ScoutSourceA`, `T57W1ScribeItemsR51x1to4`, `R56x5to7`, `T57W1SimplScope`, plus
`T57W1ConnectorCross` and `T57W1ConnectorSiblings` on the same class.

**Command:**
```
python3 -c "import json;r=json.load(open('tools/registry.json'))['rows'];\
print([ (x['name'],x['kind']) for x in r if 'receipt-revision' in json.dumps(x)])"
# base: [('receipt-revision-gate-selftest','selftest')]
```

**Status: FIXED at C0.** Three rows landed (`receipt-gate-accept` exit 0,
`receipt-gate-content-drift` exit 3, `receipt-gate-unresolvable-certified` exit 2) plus the SKILL
registry row. The dry C2 run: `gate_rows=3 exits=0,2,3 held=3/3 mutants=3/3`.

### 1.6 Cold-read drift is concentrated in four pinned files — 4 seats, and they agree numerically

**Seats:** `T57W1ScoutDrift` (11 single-path clones, measured), `T57W1LabratFloor` (6 probes,
measured), `T57W1ScribeQuality` (2-line QUALITY append measured through
`coldread-precheck.sh`), `T57W1ScribeItemsR56x1to4` (3 monitor probes measured).

The two seats that measured the same paths independently **agree exactly**:

| path | `ScoutDrift` | `LabratFloor` | `ScribeQuality` | `R56x1to4` |
|---|---|---|---|---|
| `tools/registry.json` | 11 lost, score 8→6 | 11 lost (53/64, score 6) | — | — |
| `corpus/QUALITY.md` | 6 lost | — | **6 lost** (58/64, RED) | — |
| `corpus/README.md` | 6 lost | — | — | **6 headings lost** (58/64, score 6) |
| `SKILL.md` | 1 lost (`## Standing rules`) | — | — | **1 lost** (63/64, score 6) |
| `corpus/routed-defects.json` | 0 lost | **0 lost** | — | — |

This is the strongest *positive* corroboration in wave 1: four seats, two independent
instrumentation styles (single-path clone probes vs. `coldread-precheck.sh`), identical numbers.
`T57W1LabratFloor` additionally shows the ledger edit itself is free (0 internal pins) — which
is what lets the 51-row append land without a no-harm cost.

### 1.7 The cold-read floor reads 64/64 score 8 at base — 11 seats

**Seats (11):** `T57W1ExecFreezeBind`, `T57W1ExecNoHarm` (coldread-floor monitor), `T57W1LabratFloor`
(base control), `T57W1RevExtractRecall`, `T57W1ScoutDrift` (base re-derived), `R52x1to3`,
`R53x1to3`, `R55x1to4`, `R56x1to4`, `T57W1ScribeQuality`, `T57W1ScribeRecords`.

**Command (executed in a scratch clone):**
```
python3 .ufo/evidence/round-21/coldread/measure.py --repo <clone> --rev 5e35699…
# → sections_covered: 64, calibration_restraint_score: 8, box3_full_page: true
```

This is the NO-HARM arm the round contract names. Unchanged at the deciding revision; the L1
re-reads and re-binds the headings C0 uncredited in wave 3.

### 1.8 Three defects are `open` at base and the closure's own lesson rows say otherwise — 2 seats

`T57W1SentLedger` §"Base needs repair" measures the base ledger itself under its own counter:
`total=9 C1_R50_PASS=false` (`evidence_bad=3` R41.6/R42.3/R49.3; `open_unplanned=6` R45.1,
R45.4, R46.2, R47.5, R48.4, R49.5). `T57W1RevInherited` F1 measures the same base facts from the
other direction (49 rows, 31 fixed / 7 open / 11 declined, no `R5x` id present) and finds the
contract's `before/` receipts absent.

Both are confirmed by the dry runs: the base ledger is *not* a pass under the round-50 rules it
was written for (Sweep C: `extra=49, open_unplanned=10, evidence_bad=4`), and the round-57
counter's own `old49` arm reports `old49=ok` — the 49 original rows *are* preserved byte-for-byte,
but they are not self-consistent under the inherited rules. **The inherited counter was never a
pass at base; the round-57 counter's `old49` arm fixed the preservation half and left the
consistency half unaddressed.**

---

## 2. Single-seat findings that contradict another seat — adjudicated with a command

These are the contradictions. Each is stated with who is right and the command that decides it.

### 2.1 The id-rule note (round 51) — `T57W1ExecExtract` vs `T57W1RevExtractRecall` vs the lane's own lesson

**The disagreement.** `T57W1ExecExtract` (the extractor seat) states a "DECISION the L1 must know:
id rule deviation in round 51", arguing that because item 1 is labelled `**R51.1` and items 2–8 are
unlabelled, the position-among-unlabelled reading would give item 2 the id `R51.1` again, so the
extractor uses the position among *all* items. `T57W1RevExtractRecall` F1 independently reaches the
*same* conclusion ("The extractor's rule (position among all items) is the only collision-free
reading and matches the file's order. I agree with it"). So the two seats agree on the *rule*.

But `T57W1RevExtractRecall` F2 then finds something the extractor seat's own note denies, and
this is where the contradiction bites:

> **Who is right about the extractor being right — and about the ids being usable as ledger keys.**

`T57W1ExecExtract` claims its choice "also agrees with the lane's own citations inside the items
('R51.2/R51.3' in item 2, 'R51.4', 'R51.5' in item 4)". `T57W1RevExtractRecall` F2 says the
opposite: "'R51.2' names two lane defects in the same file."

**The command that decides it:**
```
cd <clone>
sed -n '126,133p' corpus/lessons/round-51-verifier-spotcheck.md   # the closure's 8 items
sed -n '94,98p'  corpus/lessons/round-51.md                        # the LANE's own 5 labels
```

Output, both files:

```
closure  R51.1=registry gate  R51.2=Stale SKILL  R51.3=Cold-read re-key  R51.4=C3 counter
         R51.5=Cross-domain routing owed to kagi  R51.6=## Gate  R51.7=Ledger cell  R51.8=Freeze-stamped
lane     R51.1=operability harm  R51.2=SKILL.md:2136 + runner /tmp  R51.3=Runner line pointers
         R51.4=C3 round21-measure  R51.5=The C3 counter's mutation attack
```

**Verdict: `T57W1RevExtractRecall` is right and `T57W1ExecExtract`'s "also agrees with the lane's
own citations" clause is wrong.** The lane's own `R51.2` is *SKILL.md:2136 + the runner's /tmp
scope*; the closure's `R51.2` is a *bundle* that also contains the runner line pointers (which
the lane calls `R51.3`). The lane's own `R51.5` is *"The C3 counter's mutation attack"*; the
closure's `R51.5` is *"Cross-domain routing owed to kagi"* — and the closure's item 4 at line 129
literally says `Also run the C3 counter's missing mutation attack (R51.5)`, i.e. the closure
*itself* uses `R51.5` to mean the mutation attack while the extractor assigns `R51.5` to a
different defect. Confirmed:
```
sed -n '129p' corpus/lessons/round-51-verifier-spotcheck.md | grep -o "mutation attack (R51\.5)"
# → mutation attack (R51.5)
```

The rule the extractor chose is the only collision-free one (both seats agree on that, and the
installed extractor implements it at `extract-defects.py:89-92`, `n = it['label'] if it['label']
is not None else pos`). **The defect is in the lane's labels, not the extractor's rule**, and
`T57W1RevExtractRecall`'s recommendation — key rows by *file + line span + closure item*, not by
bare id text — is the correct repair. The installed counter has *not* adopted it: its
`PLANNED_ID` regex and the ledger's `id` field are both bare ids, so the collision is live in
the tree. **The L1 must key the ledger rows by closure item, or `R51.2`/`R51.5` name two
different defects to any reader.**

### 2.2 R54.8 status vs the round-55 lesson's own FIXED row — `T57W1ScribeItemsR54x8to10` vs the round-55 lesson

**The disagreement.** `T57W1ScribeItemsR54x8to10` records **R54.8 = open**, with a staged patch,
arguing: (a) is closed by `9cf0146` (the seat file carries a SUPERSEDED block) but (b) is still
true at base — `corpus/lessons/round-54.md` has no record of the `config.yml` write; the record
lives only in `corpus/lessons/round-55.md` and SCORECARD `ER-R54-8`.

The round-55 lesson's own row says the opposite:
`corpus/lessons/round-55.md:62` → `| R54.8 | FIXED, with a withdrawal — the seat file is marked
superseded and the incident is recorded here; … |`.

**The command that decides it:**
```
cd <clone>
grep -c -i "config" corpus/lessons/round-54.md   # → 0
grep -c -i "config" corpus/lessons/round-55.md   # → 1
sed -n '122p' corpus/lessons/round-54-verifier-spotcheck.md
```

The routed item R54.8 says: *"The report says the incident is 'recorded here **and in the
lesson**', but `corpus/lessons/round-54.md` contains no mention of `config.yml` or a host write.
Append a correction to both."* The named lesson is **`round-54.md`**. `round-55.md` is a
different file; recording the incident there does not close a defect that names
`round-54.md`.

**Verdict: `T57W1ScribeItemsR54x8to10` is right; the round-55 lesson's FIXED row is the
overclaim.** Gap (b) is still open at base. Note this is *not* merely a lesson-row quibble: it
is the same shape as the R55.4 case (§2.4) and the R51.7 case — a lesson row asserting `FIXED`
where the tree still carries the defect. The dry C1 run corroborates the seat: `R54.8` fails
`evidence-bad … soft-excluded-path .ufo/waves/round-54/w1/T54W1ExecStraceNoise.md`, i.e. the
row's evidence is a wave file, which the counter refuses as evidence. The seat's own note
(`.ufo/waves/round-57/w1/T57W1ScribeItemsR54x8to10/stage/corpus/lessons/round-54.md`) is the
right repair and is not staged in the lane.

### 2.3 R52.3 — `T57W1ScribeItemsR52x1to3` vs the round-53 contract's own note

**The disagreement.** `T57W1ScribeItemsR52x1to3` records **R52.3 = open**, fixable-costly, and
says explicitly: *"The round-53 contract's note claims R52.3 'worked under this round', but no
tree change backs that."* The round-53 contract at `.ufo/evidence/round-53/contract.json:44`
says the opposite: *"R52.1 …, R52.2 …, R52.3 (over-count re-derivation), R52.5 (this claim) and
R52.6 … are worked under this round."*

`T57W1RevExtractRecall` F3 independently finds the same defect from the other end: round-52
lesson line 46 says *"See routed defect R52.4"* but the over-count review is R52.3 (L85) — the
cross-reference points at the wrong item.

**The command that decides it:**
```
cd <clone>
git log --oneline c1d49d76..5e35699 -- corpus/lessons/round-52.md   # → (empty)
sed -n '27p' corpus/lessons/round-52.md
# → - 8 over-count (01, 02, 06, 09-13). Example: Corr12, where the reviewer found 0 of 14 …
grep -o "R52.3 (over-count re-derivation)" .ufo/evidence/round-53/contract.json
```

**Verdict: `T57W1ScribeItemsR52x1to3` and `T57W1RevExtractRecall` are right; the round-53
contract's note is the overclaim.** No commit after the routing commit
`c1d49d76` touches `corpus/lessons/round-52.md`, so the "0 of 14" statement the item names is
still standing at base. The contract note is a claim ahead of receipt — the exact class-1 shape
the round exists to catch, and the reason the item was routed. Both independent findings
(the status and the mis-pointed cross-reference) survive to the deciding revision: `R52.3` is
`open` in the working-tree ledger and the dry run reports no fault on it, which is correct —
an open row that resolves and is planned is *not* a counter failure.

### 2.4 R55.4 — `T57W1ScribeItemsR55x1to4` vs the round-56 lesson's own row

**The disagreement.** `T57W1ScribeItemsR55x1to4` records **R55.4 = open** ("Carried, not fixed"),
and reports the contradiction itself: *"Lesson conflict. `corpus/lessons/round-56.md:105` says
R55.4 is FIXED. The ledger row says open."* The round-56 wave-1 disposition file
`.ufo/waves/round-56/w1/T56W1RevRound55Dispositions.md:12` agrees with the scribe:
**"F2 (overclaim): R55.4 'FIXED by construction' … Correct disposition is `carried`."**

**The command that decides it:**
```
sed -n '105p' corpus/lessons/round-56.md
# → | R55.4 | FIXED by construction: the control set is the frozen .ufo/evidence/round-56/controls.sh, …
sed -n '12p;22p;94p' .ufo/waves/round-56/w1/T56W1RevRound55Dispositions.md
```

**Verdict: the scribe and the round-56 disposition are right; the round-56 lesson row is the
overclaim.** Two independent round-56 artifacts (the wave-1 disposition file and the wave-3
record) say `carried`, and the lesson row still says `FIXED by construction`. The scribe's staged
one-line correction to `corpus/lessons/round-56.md:105` is the right repair and is **not
staged in the lane** — C0 did not touch `corpus/lessons/round-56.md` (verified:
`git show ca75c26 --name-only` lists no `round-5[0-6].md`). So the overclaim is still live at the
deciding revision. This is the second instance of the §2.2 pattern: a lesson row asserting
`FIXED` over an unfixed defect.

### 2.5 The `mutants.json` bank vs `T57W1MutGate`'s eight-mutant sweep — and one mutant that survives the selftest

**The disagreement.** `T57W1MutGate` sweeps **eight** mutants and finds that three are killed by
*no* registry row and only by `--selftest` (`wrong-refusal-code`, `drop-ambiguity-check`,
`swap-ancestor-test`), because *"the three rows never reach the strict-mismatch branch
(`paths is None`), the ambiguity branch, or the control-ancestor branch."* It recommends a
**different three** (`accept-on-drift`, `exit0-instead-of-2`, `exit0-instead-of-3`).
`T57W1CritC2` independently proposes the bank the contract names (accept-on-drift, wrong refusal
code, exit 0 on unresolvable) and the installed `mutants.json` uses CritC2's three.

But `T57W1MutGate` finding 1 is the sharper claim and **no other seat makes it**: the mutant
`always-print-pass-line` (the verdict token `verdict` → `'PASS'`) **survives the entire 19-case
selftest**, because "only case 1 inspects `verdict=PASS`, and it is a PASS case, so no case
asserts `verdict=REFUSED` on a refused run."

**The command that decides it** (executed in a scratch clone at base):
```
python3 - <<'PY'
import subprocess,os
c='<scratch clone>'
p=os.path.join(c,'tools/receipt-revision-gate.py'); s=open(p).read()
old="or 'none', verdict))"; new="or 'none', 'PASS'))"
print("count of old string:", s.count(old))     # → 1
open(p,'w').write(s.replace(old,new))
r=subprocess.run(['python3',p,'--selftest'],capture_output=True,text=True,cwd=c,
                 env={**os.environ,'TMPDIR':'<scratch>'})
print("selftest rc:",r.returncode)              # → 0
print(r.stdout.strip().splitlines()[-1])         # → GATE_SELFTEST: 19/19 pass
PY
```

**Verdict: `T57W1MutGate` is right and is the only seat to say so.** A mutant that turns a
`REFUSED` verdict line into `PASS` passes the gate's own 19-case selftest with exit 0. The
installed bank does not include that mutant, so the blind spot is unmeasured. This is a real
gap in the C2 evidence base, not a bookkeeping detail — the bank is a sample of three mutants
from a 359-line tool (the contract's own `cannot_see` says so), and `T57W1MutGate` shows the
sample can be improved without changing the contract.

Note the contract-vs-installed check on the bank itself: the installed M2 replaces
`codes.append('RECEIPT_REV_CONTENT_DRIFT')` → `codes.append('RECEIPT_REV_MISMATCH')`, which is
CritC2's M2. `T57W1MutGate`'s own `wrong-refusal-code` mutant is a *different* edit
(`RECEIPT_REV_MISMATCH` → `RECEIPT_REV_ABSENT`, at the strict branch, line 146) — and by
MutGate's own measurement that mutant is killed by **no row**, because the rows never reach that
branch. **Both seats are right about their own mutants and the disagreement is a naming
collision**: two different edits are both called "wrong refusal code". The installed M2 (the
drift branch) *is* killed by a row — the dry run shows
`mutant M2 wrong-refusal-code: killed by receipt-gate-content-drift(got=3)` — while MutGate's
M2 (the strict branch) would not be. **If the L1 adds MutGate's strict-branch mutant, it must
also add a row that exercises the strict branch, or the mutant arm goes from 3/3 to 2/3.**

### 2.6 `T57W1CritC1`'s R52.5 "cheap fixed row" vs `T57W1ScribeItemsR52x4to6`'s R52.5 = fixed

**The disagreement.** `T57W1CritC1` §4 lists R52.5 among five items that "get a passing `fixed`
row in one step each", and asserts the cited commit `51d1f0eb` **does not add** the line
(`git show 51d1f0eb -- tools/registry-check.py | grep -c '^+.*fallback to /tmp'` → 0).
`T57W1ConnectorCross` flag 1 says the opposite: R52.5 is **"stale at base"** — the base row
should record *"fixed at base (round 53)"*, and the residual is only the `tempfile.gettempdir()`
fallback at :772. `T57W1ScribeItemsR52x4to6` records **R52.5 = fixed** by `218bc6b5`.

**The command that decides it:**
```
cd <clone>
git log --oneline -S"fixtures only under the scratch root (TMPDIR)" -- tools/registry-check.py
# → 218bc6b round-53: fix pass — … tools/ /tmp hardcodes honour TMPDIR
# → 5b703c6 round-53: fix pass 2 — … strict TMPDIR scratch-root helper in 7 tools
git show 218bc6b5 -- tools/registry-check.py | grep -n "^[+-].*tmp"
# → -        work = tempfile.mkdtemp(prefix="tameshi-registry-check-", dir="/tmp")
# → +        raise RuntimeError(f"cannot create clone scratch under the scratch root: {exc}") from exc
git merge-base --is-ancestor c1d49d76 218bc6b5 && echo "descends from routed_at"
git show c1d49d76:tools/registry-check.py | grep -c "fixtures only under the scratch root (TMPDIR)"  # → 0
git show 218bc6b5:tools/registry-check.py | grep -c "fixtures only under the scratch root (TMPDIR)"    # → 1
```

**Verdict: `T57W1ConnectorCross` and `T57W1ScribeItemsR52x4to6` are right; `T57W1CritC1`'s
R52.5 row is a mis-attribution.** The fixing commit is `218bc6b` (or `5b703c6`), it descends
from the routed commit `c1d49d76`, and it removes the literal `dir="/tmp"` — the excerpt is
absent at routing time and present at the fix. `T57W1CritC1` picked the wrong commit
(`51d1f0eb`, a round-55 C1 commit) and therefore correctly reported *that commit* adds nothing.
Its general point — that a wrong commit can pass the `fixed` arm — stands and is exactly what
the installed Amendment 1 now prevents. **But R52.5 is genuinely fixed at base**, and a ledger
row citing `51d1f0eb` would be wrong. The working-tree ledger row cites `218bc6b` — correct.
`T57W1CritC1` also independently found the same `218bc6b`-vs-`51d1f0eb` split (§4 table), so
the two seats are consistent in the mechanism and differ only in which commit they name.

### 2.7 `T57W1CritC1`'s "the inherited counter's `extra` rule makes the 49 original rows unkeepable" vs the installed `old49` arm

**The disagreement.** `T57W1CritC1` §3 claims the inherited counter *"counts rows outside the
frozen set as `extra` and fails the total, so the '49 original rows' can never be kept"* (S2c:
`extra=49`, total 49) — and says *"No code checks byte-identity of the 49 rows"*, so the
contract's *"the 49 original rows byte-identical to base"* clause is unenforced.
`T57W1ExecC1Counter` (the counter seat) implements an `old49` arm instead: every row of the
ledger at BASE must be present exactly once at REV and equal as canonical JSON.

**The command that decides it:**
```
# installed counter, real run (dry-c1.sh):
#   C1_R57_TERMS: … old49=0 extra=0 …   → old49 arm holds, extra arm holds
# round-50 rules, same 51-item set, same ledger (Sweep C):
#   {'extra': 49, …}  → the inherited rule indeed cannot hold the 49 rows
```

**Verdict: `T57W1CritC1` is right about the inherited counter and the installed counter answers
it.** The inherited rule *does* make the 49-row requirement unsatisfiable; the installed
`old49` arm is the direct repair and it works (`old49=0`). One caveat `T57W1CritC1` raises that
the installed counter does **not** answer: *"the ledger header fields (`round`, `note`, `schema`)
are not compared"* (from `T57W1ExecC1Counter`'s own risks section) — the `old49` arm compares
canonical JSON of the *rows*, not the header. Minor, but it means "byte-identical to base" is
still slightly stronger than what is enforced.

### 2.8 `T57W1CritC1`'s "the floors are not the defence" vs `T57W1CritClaimShape`'s "keep fixed ≥ 20"

**The disagreement.** `T57W1CritC1` §1 recommends floors of `fixed ≥ 20, declined ≤ 14, open ≤ 17`
and says *"the recommended floors, not lowered after scoring: fixed ≥ 20 (kept, but each fixed row
must introduce its excerpt)"*. `T57W1CritClaimShape` C1-B2 argues the opposite: *"Remove
`fixed >= 20`, `declined <= 14` and `>= 6 this-round fixes` from the target (they reward claimed
fixes: a ledger that honestly marks 30 items open fails)"*, and proposes the **blind-panel** arm
instead.

**The command that decides it — the L1's own installed constants:**
```
sed -n '66,74p' .ufo/evidence/round-57/c1/measure.py
# 66 # Amendment 1 (L1, before any scoring; contract amendments[0]): the round-50 floors (fixed >= 20,
# 67 # declined <= 14) are replaced by the blind-panel arm below - a floor on a status rewards claiming,
# 68 # not agreeing (wave-1 critic T57W1CritClaimShape B2, T57W1CritC1). They stay as arms with
# 69 # non-binding values so the verdict line is stable.
# 70 FIXED_FLOOR = 0
# 71 THIS_ROUND_FLOOR = 6
# 72 DECLINED_CAP = 999
# 73 PANEL_PATH = '.ufo/evidence/round-57/c1/panel.json'
```

**Verdict: `T57W1CritClaimShape` is right and the L1 adopted its position** — the floors are
non-binding (`FIXED_FLOOR=0`, `DECLINED_CAP=999`) and the blind panel replaced them. The
counter's own comment cites both critics, but the *design* is ClaimShape's, and the wording of
its own recommendation is what the comment paraphrases.

**But the panel arm is not yet satisfiable, and this is a live blocker neither seat could have
seen.** The installed counter requires `.ufo/evidence/round-57/c1/panel.json` to exist and to
match `PANEL_SHA256`, which is still the literal placeholder
`PIN_PENDING_SET_BY_L1_AFTER_THE_BLIND_PANEL`. The dry run prints
`EXPLAIN panel-pin .ufo/evidence/round-57/c1/panel.json` and `panel=pin`, contributing **1 to
`total=21`**. The file does not exist:
```
ls -la .ufo/evidence/round-57/c1/panel.json
# → No such file or directory
```

**Consequence for the L1, stated plainly:** until the panel file is written and pinned, C1
cannot pass — and the panel is not a formality. It is the *only* arm left that constrains the
status mix (with the floors set to 0/999), and it is the arm that two independent critics argued
for. The wave-2 seats should treat writing `panel.json` as the critical path, not a formality
after the ledger is final.

### 2.9 `T57W1SentLedger`'s "the inherited rules accept forged ledgers" vs the installed Amendment 1

**The disagreement.** `T57W1SentLedger` shows the inherited rules accept **three classes of
forged `fixed` row** (off-topic prose line, off-topic code line, comment line) and a **fourth**
(SHONEN restatement, one commit, four rows), and that a full ledger of 20 fixed + 29 open scores
`total=0 C1_R50_PASS=true` from the real round-50 CLI. It measures candidate extra checks and
finds **X1 (word-overlap ≥ 3) false-rejects a genuine fix (R49.1)** and **X1 ∧ X9 false-rejects
four**. Its recommendation is hedged: *"That is a real harm, so the choice is the L1's, not free."*

The installed counter takes a different route: it does **not** implement word-overlap. It
implements (a) whole-token key match and (b) the commit tie — and the tie rule is what makes
7 of the 8 `fixed_bad` rows fail (§3.2).

**The command that decides it** — the sweep that isolates the amendment's cost:
```
# same 51-item set, same ledger:
#   round-50 rules : fixed_bad=1   (only R55.1)
#   round-57 rules : fixed_bad=8   (R51.3 R53.6 R53.7 R54.7 R54.9 R54.10 R55.1 R55.3)
```

**Verdict: `T57W1SentLedger` is right that the inherited rules are forgeable, and the installed
counter closes the forgery it named — but the closure is not free, and `T57W1SentLedger` had
already priced that.** The 7 extra `fixed_bad` rows are the price. The measured sub-conditions
are decisive and are the actionable content of this finding:

| row | commit message names the id | evidence path named by the item's own text | the path the item text names is *touched* by the commit |
|---|---|---|---|
| R51.3 | no | yes (`.ufo/evidence/round-52/coldread/refresh.py`) | **no** |
| R53.6 | no | no | — |
| R53.7 | no | no | — |
| R54.7 | no | no | — |
| R54.9 | no | no | — |
| R54.10 | no | yes (`.ufo/evidence/round-54/control/controls-a.stdout`) | **no** |
| R55.1 | no | yes (`.ufo/evidence/round-56/before/c2.stdout`) | **no** |
| R55.3 | no | no | — |

**The rule's conjunction is too strong.** The installed code requires
`item['path'] in files` (the commit touches the path) **and**
(`names_id` **or** the path is named by the item text) — measured at `measure.py:249-251`:
```
for item in keyed:
    if item['path'] not in files: continue
    if not (names_id or item['path'] in item_text or os.path.basename(item['path']) in item_text): continue
```
For R51.3, R54.10 and R55.1 the item text names a path that the commit does **not** touch, while
the path the commit *does* touch is not named by the item text. So the two branches never
co-occur on one evidence item and the row fails. **Three of the eight failures are an artefact of
the conjunction, not of a forgery.** The other five (R53.6, R53.7, R54.7, R54.9, R55.3) fail
because the item text names no path at all and the commit message names no id — a real gap in
those rows' evidence, and the seat should re-derive their evidence paths.

### 2.10 `T57W1CritClaimShape`'s "C2 is not content-separable from C1" vs the L1's installed `cell` arm

**The disagreement.** `T57W1CritClaimShape` §4 argues C1 and C2 are content-coupled through
three rows (R56.2, R56.5, R56.6) and proposes a specific repair: *"rows R56.2, R56.5 and R56.6
are `fixed` only if a post-routing commit at or below REV adds a new keyed excerpt to their
path, and are otherwise `open`."* `T57W1CritC2` §"Proposed exact rewrites" goes further and
demands that the counter **exclude the pre-existing `receipt-revision-gate-selftest` row** from
kill credit, because *"A counter that credits it toward arm (c) passes arm (c) with no new row
at all."*

**The command that decides it:**
```
# installed counter's row-admission rule (measure.py:230 area / registry row filter):
grep -n "kind.*gate\|'--selftest' not in\|argv\[1\] == GATE" .ufo/evidence/round-57/c2/measure.py
# dry-c2.sh output:
#   EXPLAIN rows gate_rows=3 exits=0,2,3 missing_exits=none refusal_rows_without_known_code=none
#   EXPLAIN executed receipt-gate-accept expect=0 got=0 held
#   EXPLAIN executed receipt-gate-content-drift expect=3 got=3 held
#   EXPLAIN executed receipt-gate-unresolvable-certified expect=2 got=2 held
```

**Verdict: `T57W1CritC2` is right and its rewrite was adopted** — the C2 counter admits only
rows with `kind == "gate"`, `argv[1] == "tools/receipt-revision-gate.py"`, and no `--selftest`,
so the pre-existing selftest row cannot be credited. The dry run shows `gate_rows=3` and
`held=3/3`, i.e. the three *new* rows, and `mutants=3/3`.

**But `T57W1CritClaimShape`'s separability worry is not resolved by the counter, only by the
ledger's statuses.** The C2 counter does not read C1, so C1 remains verifiable without C2 *as a
mechanism*. Whether it *is* verifiable without C2 depends on the three rows' statuses, and the
working-tree ledger now records **R56.2 = fixed** (evidence `SKILL.md:53`), **R56.6 = fixed**
(registry rows) and **R56.5 = open**. So two of the three coupling rows are closed by C0's
content — **by a claim, not by a receipt that the C1 counter can see.** `T57W1CritDoNothing`'s
F1 is the direct warning: a commit that only quotes an excerpt into a new file reaches
`total=0 C1_R57_PASS=true`. R56.2's row cites `SKILL.md:53` — a real C0 edit to the real cell —
and its `status_at_base` is `open` while its `status` is `fixed`, so the base-status coherence
arm (`base_status_bad=0`, measured) is satisfied. **The row is honest; the concern was about the
mechanism, and the mechanism is now sound for these rows specifically.**

---

## 3. The pattern this wave surfaces

### 3.1 The cross-wave pattern in one line

**Every wave-1 finding that two or more seats made independently is now closed at C0, and every
finding that only one seat made is either still open or was closed by that seat's own staged
patch — which the L1 did not install.** Concretely:

| | corroborated (2+ seats) | single-seat |
|---|---|---|
| closed at C0 | 1.1 planned-id regex · 1.2 excerpt-introduced-by · 1.3 exit 1 · 1.4 cell code · 1.5 gate rows · 1.6/1.7 no-harm | — |
| **still open at the deciding revision** | 1.8 base-ledger inconsistency | 2.1 id namespace · 2.2 R54.8(b) · 2.4 R55.4 · 2.5 selftest verdict-line blind spot · 2.9 3 of 8 `fixed_bad` are a rule artefact · 2.8 panel.json missing |

**The lesson's `## Mistakes` row should be: *the wave-1 seats' own staged repairs were not
installed*.** Seven of the nine open items above have a patch staged under
`.ufo/waves/round-57/w1/<seat>/stage/` — R54.8's lesson patch, R55.4's one-line lesson
correction, R51.6's `## Gate` block, R53.8's lesson correction, R55.2's, R56.7's, R56.3's
recheck line and README index, R56.4's referent record — and C0 installed *different* content
for several of them (the R56.3 errata landed as `ER-R57-K1` in
`corpus/knowledge/receipt-revision-binding.md` rather than the one-line recheck edit the seat
staged; the R56.4 referent landed as `.ufo/evidence/round-57/coldread-referent-r56.md`; R53.8,
R55.2 and R56.7 landed as a `corpus/lessons/round-57.md` errata block). The ledger rows then
cite the C0 artifacts, which is self-consistent, but **the surfaces the routed items named are
still wrong**:
```
sed -n '23p' corpus/lessons/round-53.md
# → quote (22 words, camera-ready p. 4, pdftotext lines 289–294)     ← R53.8's named surface, unchanged
sed -n '318,319p' corpus/lessons/round-56.md
# → No `SKILL.md`, `corpus/QUALITY.md`, … byte changed after C0/PIN    ← R56.7's named surface, unchanged
sed -n '3p' corpus/knowledge/receipt-revision-binding.md
# → recheck: … must print `GATE_SELFTEST: 14/14 pass`               ← R56.3's named surface, unchanged
sed -n '44p' .ufo/waves/round-55/w1/T55W1ScribeSkill-receipts/c2-integrated.out
# → C2_R55: … total=1 C2_R55_PASS=false                             ← R55.2's named surface, unchanged
git show ca75c26 --name-only --format="" | grep -c "round-5[0-6].md"    # → 0
```
The C0 corrections live *beside* the defects, in a new lesson, and the ledger rows point at the
beside. That satisfies the counter (all those rows agree) and does **not** satisfy the routed
items. **A ledger row that points at a new record rather than at the surface the item named is
the wave-57 mistake class, and it is exactly the class `T57W1CritC1` and `T57W1CritDoNothing`
warned about in a different guise.**

### 3.2 The second-order effect the wave-1 seats could not see: the key sets

The 8 `key_miss` rows fail **identically under both rule sets** (Sweep C: round-50 gives
`key_miss=8`, the same 8 ids). So this is not an amendment artefact — it is a **key-set**
defect, and it is the one finding that two seats made *with different keys and the same
conclusion*.

The counter reads keys from the **defect set** (`defects.json` → `d['keys']`), and the
installed `keys.json` is byte-identical to the extractor's staged copy:
```
diff <(cat .ufo/evidence/round-57/c1/keys.json) \
     <(cat .ufo/waves/round-57/w1/T57W1ExecExtract/stage/.ufo/evidence/round-57/c1/keys.json)
# → identical
```
The 15 scribe seats each produced **their own** per-id keys in their `rows.json` — and the
L1's ledger builder **drops them**:
```
grep -n "keys" .ufo/waves/round-57/build-ledger.py
# 15:        r.pop('verdict_basis', None); r.pop('keys', None)
```
Measured against the installed whole-token rule:

| key source | rows failing `key_miss` |
|---|---|
| the extractor's `keys.json` (installed) | **9** |
| the scribes' own per-row `keys` (dropped by `build-ledger.py`) | **2** (R51.2, R56.4) |

`T57W1ExecExtract` itself flags the risk in its own report: *"Keys are checked case-insensitively
as substrings… entries like `rekey`-style short words are the weakest discriminators"* and
*"Guesses about future fix text … are `[INFERENCE]`; a reviewer should widen those if a fixing
excerpt misses them."* `T57W1ScribeItemsR50x1to4` says the same from the other side: *"The rows'
keys and the staged extractor's default keys both pass for these four ids."*

**Verdict: the two seat families are jointly right and the L1 merged the wrong half.** The
scribes' key sets are the ones that match the excerpts the scribes actually chose; the
extractor's key sets were guesses made before any fix existed. Merging the scribes' keys into
`defects.json` (and re-pinning `DEFECTS_SHA256`) would clear 7 of the 8 `key_miss` rows. The
two exceptions, R51.2 and R56.4, need the seat's own evidence re-derived.

This is the single most actionable finding in this report: **7 of C1's 21 remaining points are a
one-line-per-row merge, not a repair of any defect.**

### 3.3 The third-order effect: `evidence_bad` and the soft-path rule

4 rows fail `evidence-bad` (R53.9 ×2, R54.8, R55.4 ×2, R55.6 ×4 — 8 evidence items over 4 rows).
Every one of them fails the **same** rule: the evidence path is under `.ufo/waves/`, which the
counter treats as soft (uncredited) unless the path ends with one of the item's keys:
```
measure.py:177:  if path.startswith(SOFT) and not any(path.endswith(k) for k in keys):
#                return 'soft-excluded-path'
```
All of these are seats that cited a **wave-1 seat's own report file** as the evidence for the
defect. `T57W1ScribeItemsR53x7to9` (R53.9) cites `.ufo/waves/round-53/w2/T53W2RevW1Specialists.md`;
`T57W1ScribeItemsR54x8to10` (R54.8) cites `.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md`;
`T57W1ScribeItemsR55x1to4` (R55.4) cites two round-56 wave files; `T57W1ScribeItemsR55x5to7`
(R55.6) cites four round-55 wave files. `T57W1SimplScope` D3 had already noted that the counter
reads only `id, status, evidence, commit, reason` — so `seat` and `note` carry the provenance
that these rows would lose. **A wave file is not a lane record; citing one as the evidence for
a lane defect is the same mistake as §3.1, in a different column.** The four rows need evidence
in a lane record (a lesson, a knowledge entry, a `corpus/` file), not in a seat report.

### 3.4 What the two counters say together

| | C1 | C2 |
|---|---|---|
| verdict | `total=21 C1_R57_PASS=false` | `total=0 C2_R57_PASS=true` |
| arms failing | `key_miss=8`, `fixed_bad=8`, `evidence_bad=4`, `panel_pin=1` | none |
| rows agreeing | 31/51 | 3/3 gate rows held; 3/3 mutants killed; `skill_row=1`; `codes_known=4/4`; `standing_cell=ok` |
| dominant cause | **data** (key sets + wave-path evidence + 3 rule-artefact rows), not mechanism | — |

C2 is closed and its own blind spot is measurable (§2.5). C1 is not closed, and its 21 points
decompose as **8 key-set** (§3.2) + **8 rule-artefact-or-evidence** (§2.9, §3.3) + **4
evidence** (§3.3) + **1 missing panel file** (§2.8). **Only 8 of the 21 need a repair of a
defect; 7 need a keys merge; 1 needs a file written; 5 need their evidence path moved off a
wave file; and 3 of the 8 `fixed_bad` need the tie rule's conjunction relaxed.**

---

## 4. Contradiction adjudication summary

| # | topic | seats in conflict | who is right | command |
|---|---|---|---|---|
| 2.1 | round-51 id namespace | `ExecExtract` (agrees with lane citations) vs `RevExtractRecall` F2 | **RevExtractRecall** | `sed -n '94,98p' corpus/lessons/round-51.md` vs `sed -n '126,133p' …spot-check.md` |
| 2.2 | R54.8 status | `ScribeItemsR54x8to10` (open) vs `corpus/lessons/round-55.md:62` (FIXED) | **scribe** | `grep -c -i config corpus/lessons/round-54.md` → 0 |
| 2.3 | R52.3 status | `ScribeItemsR52x1to3` + `RevExtractRecall` F3 (open) vs round-53 contract:44 (worked) | **both seats** | `git log c1d49d76..5e35699 -- corpus/lessons/round-52.md` → empty |
| 2.4 | R55.4 status | `ScribeItemsR55x1to4` (open) vs `corpus/lessons/round-56.md:105` (FIXED) | **scribe** | `sed -n '12p' .ufo/waves/round-56/w1/T56W1RevRound55Dispositions.md` |
| 2.5 | mutant bank | `MutGate` (8 mutants, 3 row-killed) vs `CritC2`/installed (3 mutants) | **both**, naming collision; `MutGate`'s selftest-survivor is unique and real | selftest on the `verdict`→`'PASS'` mutant → `19/19 pass`, rc 0 |
| 2.6 | R52.5 fixing commit | `CritC1` (`51d1f0eb`) vs `ConnectorCross` + `ScribeItemsR52x4to6` (`218bc6b`) | **the two seats** | `git show 218bc6b -- tools/registry-check.py \| grep '^[+-].*tmp'` |
| 2.7 | 49-row byte-identity | `CritC1` (unenforceable) vs `ExecC1Counter` (`old49` arm) | **CritC1** about the inherited rule; the installed arm answers it | dry-c1 `old49=0` vs round-50 `extra=49` |
| 2.8 | floors vs blind panel | `CritC1` (keep fixed ≥ 20) vs `CritClaimShape` B2 (drop floors) | **CritClaimShape**; L1 adopted it | `sed -n '66,74p' .ufo/evidence/round-57/c1/measure.py` |
| 2.9 | forgery closure cost | `SentLedger` (X1 costs a genuine fix) vs installed tie rule (7 extra `fixed_bad`) | **both**; 3 of 8 are a rule artefact | round-50 `fixed_bad=1` vs round-57 `fixed_bad=8` |
| 2.10 | C1/C2 separability | `CritClaimShape` §4 (coupled) vs `CritC2` (exclude the selftest row) | **CritC2**; separability now depends on row statuses | `grep -n "kind.*gate\|'--selftest' not in" .ufo/evidence/round-57/c2/measure.py` |

---

## 5. Findings no other wave-1 seat made (single-seat, and still live)

| finding | seat | still live? | how to check |
|---|---|---|---|
| The round-51 `id` namespace collides with the lane's own `R51.x` labels; ledger rows must be keyed by closure item, not bare id | `RevExtractRecall` F2 | **yes** | `sed -n '94,98p' corpus/lessons/round-51.md` |
| The gate's verdict line can be turned to `PASS` and the 19-case selftest still passes | `MutGate` finding 1 | **yes** | mutant `or 'none', verdict))` → `or 'none', 'PASS'))`; selftest rc 0, `19/19 pass` |
| The C1 tie rule's conjunction (`path touched` **and** `path named by item text`) artefacts 3 of 8 `fixed_bad` rows | this seat (§2.9) | **yes** | `measure.py:249-251`; R51.3/R54.10/R55.1 named path is not touched by the fix commit |
| 7 of 8 `key_miss` rows fail because the L1 merged the extractor's guessed keys and dropped the scribes' per-row keys | this seat (§3.2) + `ExecExtract`'s own risk note | **yes** | `grep -n "keys" .ufo/waves/round-57/build-ledger.py` → `r.pop('keys', None)` |
| `panel.json` does not exist; `PANEL_SHA256` is a placeholder; the panel arm contributes 1 to C1's total and is the only remaining constraint on the status mix | this seat (§2.8) | **yes** | `ls .ufo/evidence/round-57/c1/panel.json` → No such file; dry-c1 `panel-pin` |
| `corpus/routed-defects.json` is uncommitted in the lane, and the C1 counter reads it at REV — a ledger edit that never lands cannot be scored | this seat | **yes** | `git status --short corpus/routed-defects.json` → ` M` |
| The inherited round-50 counter was never a pass at base (`total=9`), so "the 49 rows are byte-identical" does not imply "the 49 rows are consistent" | `SentLedger` | **yes** | `python3 .ufo/evidence/round-50/c1/measure.py --lane … --rev BASE --explain` → `total=9` |

---

## 6. Suggested moves for wave 2 (in dependency order, each falsifiable)

These are **not** applied. This seat edits nothing; each is a proposal with its own falsifier.

1. **Merge the scribes' per-row keys into `defects.json` and re-pin `DEFECTS_SHA256`.** Expected:
   `key_miss` 8 → 1 (R51.2, R56.4 remain). Falsifier: `bash dry-c1.sh` still prints
   `key_miss=8`.
2. **Write `.ufo/evidence/round-57/c1/panel.json`** with one verdict per id
   (`fixed|open|declined AT BASE`) and set `PANEL_SHA256` to its sha256. Expected:
   `panel_pin=1` → 0. Falsifier: dry-c1 still prints `panel-pin`.
3. **Move the 8 wave-file evidence paths onto lane records** (R53.9, R54.8, R55.4, R55.6).
   Expected: `evidence_bad=4` → 0. Falsifier: dry-c1 still prints `evidence-bad`.
4. **Relax the tie rule's conjunction** so that a path named by the item text suffices even when
   the commit touches a *different* path the row also cites, or let the commit message name the
   item id. Expected: `fixed_bad` 8 → 5. Falsifier: dry-c1 still prints `fixed_bad=8`.
5. **Re-derive the 5 remaining `fixed_bad` rows' evidence** (R53.6, R53.7, R54.7, R54.9, R55.3)
   so a path the fix commit touched is also named by the item text. Expected: `fixed_bad` → 0.
6. **Re-key the ledger rows by closure item** (§2.1) — add the closure's line span to each row's
   `note` or evidence, so `R51.2`/`R51.5` are unambiguous. Falsifier: a reader following
   `R51.5` still lands on two different defects.
7. **Install the staged patches the wave-1 seats wrote but C0 did not** — R54.8's
   `corpus/lessons/round-54.md` block, R55.4's one-line `round-56.md:105` correction, R53.8's
   `round-53.md` word counts, R56.7's `round-56.md` errata — so the routed items' named surfaces
   carry the correction, not only a neighbouring record. Falsifier: `grep -c -i config
   corpus/lessons/round-54.md` still 0.
8. **Add the `always-print-pass-line` mutant** to `mutants.json` **and** a registry row that
   reaches the strict-mismatch branch, so the two are added together (§2.5). Falsifier: the
   mutant survives `registry-check` unchanged.
9. **Commit `corpus/routed-defects.json`** — it is uncommitted; nothing in the deciding run can
   score a ledger that is not at REV.

---

## 7. Limits and honesty

- **No lane file was edited.** The only writes by this seat are this report, its `.json`, and
  `T57W2ConnectorWaves-receipts/`. `git status --short` in the lane shows the same
  `M corpus/routed-defects.json` and untracked entries that were there when this seat started.
- **The `fixed_bad` sub-condition table in §2.9 is a measurement of the installed code's
  predicate, re-implemented in a separate script** (§3.2's comparison harness), not a re-run of
  the counter with instrumentation. The *row list* and the *count* are the counter's own output
  (dry-c1 `EXPLAIN` lines); the *attribution* of each failure to a specific sub-condition is
  this seat's re-implementation of `measure.py:242-259`. If the attribution is wrong, §2.9's
  "3 of 8 are a rule artefact" claim is wrong; the counts are not.
- **`status_at_base` coherence was measured** (0 incoherent rows of 51: `base_status_bad=0` in the
  dry run, and an independent check: `(status_at_base == 'fixed') == is_ancestor(commit, BASE)`
  holds for every row with a commit). This is a positive result the L1 should record — the
  blind-panel arm's precondition is met in the ledger.
- **Not run:** the round-21 cold-read monitor at the deciding revision (the wave-1 seats'
  64/64 base measurement is quoted, not re-measured); `registry-check.py --rev REV` over the
  full registry (only the three `new-r57` rows, via the C2 counter's `held=3/3`); the
  `deciding-run.sh`; the `no-harm.sh` re-base; `sources-census.sh validate` (the wave-1 seat's
  exit-0 result is quoted).
- **The `key_miss` attribution in §3.2 (9 rows with extractor keys vs 2 with scribe keys)** is
  this seat's own re-implementation of `has_key` under both the installed whole-token rule and
  the round-50 substring rule. The `key_miss=8` count and the id list are the counter's own
  output and agree with the round-50 rules' output exactly.
- **Not verified:** that the panel verdicts would agree with the ledger's `status_at_base` —
  the panel file does not exist, so the ≤5-disagreement allowance cannot be exercised. The
  coherence check above shows the ledger side is internally consistent; the panel side is
  unwritten.
- **Judgement, not measurement:** the §6 ordering, the claim that the C0 "beside the defect"
  pattern (§3.1) is the round's dominant mistake class, and the ranking of the moves. Each §6
  item carries its own falsifier so a wave-2 seat can reject it by running one command.
- **Read coverage:** all 47 wave-1 `.md` reports were read in full (3,458 lines by `wc -l`).
  Two reports (`T57W1SentLedger`, `T57W1SimplScope`) and the elided middles of three more
  (`T57W1CritC2`, `T57W1ExecControls`, `T57W1RevGateSurface`) were re-read at their elided
  ranges before being cited.
- **Tools installed or upgraded: none.** No `pacman`, no `uv`, no `npm`. Only the host's
  `git` 2.56.0, `python3` 3.14.8, `grep`, `sed`, `awk`, `jq`, `sha256sum`, `diff`, `comm`.

---

## 8. Receipts

`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w2/T57W2ConnectorWaves-receipts/`

| file | contents |
|---|---|
| `01-seat-occurrence-sweep.txt` | the grep-loop output of Sweep A (every pattern, every seat) |
| `02-dry-c1.stdout` | the full `dry-c1.sh` output (26 EXPLAIN lines + the verdict line) |
| `03-dry-c2.stdout` | the full `dry-c2.sh` output (16 EXPLAIN lines + the verdict line) |
| `04-rule-comparison.txt` | round-50 rules vs round-57 rules over the same 51-item set and the same ledger, with the note list |
| `05-fixed-not-new-subconditions.txt` | the per-row measurement of `msg_names_id` / `path_in_item_text` / `touched` for the 8 `fixed_bad` rows |
| `06-key-miss-attribution.txt` | the `key_miss` id list under both rule sets, and the extractor-keys vs scribe-keys comparison |
| `07-id-namespace.txt` | the round-51 closure items vs the lane's own `R51.x` labels, side by side |
| `08-mutant-selftest-survivor.txt` | the `verdict`→`'PASS'` mutant: occurrence count, selftest rc, last stdout line |
| `09-item-surface-status.txt` | the routed items' named surfaces at HEAD (round-53.md:23, round-56.md:318-319, receipt-revision-binding.md:3, c2-integrated.out:44, round-54.md config count) |
| `10-base-ledger-under-round50.txt` | the base ledger scored by the round-50 counter: `total=9` |
| `11-status-at-base-coherence.txt` | the per-row `(status_at_base == 'fixed') == is_ancestor(commit, BASE)` check |
| `12-commands.txt` | every command quoted in this report, in order, with its exit status |

Scratch tree `$HYAKU_SCRATCH/tameshi-r57/T57W2ConnectorWaves` (clones `clone`, `clone50`,
`clone50b`, `mg`) was removed on exit.

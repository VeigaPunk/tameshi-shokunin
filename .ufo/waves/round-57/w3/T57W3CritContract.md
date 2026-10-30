# T57W3CritContract: contract audit against the round-57 counters

Item: audit `.ufo/evidence/round-57/contract.json` (final text, amendments 1 and 2, panel block) against the C1 and C2 counters, the `before` receipts, `frozen_paths`, and the deciding-run / controls / no-harm / bind inputs. Never edited; all candidate changes are staged under `.ufo/waves/round-57/w3/T57W3CritContract/stage/`.

Lane state: the lane HEAD is `2c51affd` (an "honest stop" commit recording that neither C1 nor C2 was scored and that wave 3 produced no reports). C0b is `adf87899c70d616140a81185a8f9acbbdfb30392`, an ancestor of HEAD. Every counter run below used C0b, or a scratch clone of C0b with the instruments committed. Nothing was installed. No lane file was edited.

Scratch: `/fast/scratch/hyaku/tameshi-r57/T57W3CritContract/` (clones `clone`, `fix57`, `c2chk`, `c2stage*`; copies `c1_measure.py`, `c2_measure.py`). Receipts: `.ufo/waves/round-57/w3/T57W3CritContract/T57W3CritContract-receipts/`. Combined staged diff: `stage/T57W3CritContract.diff` (265 lines).

Verdict: **the contract is not ready to freeze.** Two counter-side blockers (the C1 selftest fails the freeze precondition; the C2 counter passes a target clause that the committed tree fails) and several contract sentences that are false at C0b/HEAD. Counts below are from the commands shown.

---

## A. Blocking defects

### B1. C1 selftest fails the freeze precondition (counter defect, not staged)
Contract `claims.C1.freeze_precondition` requires `C1_R57_SELFTEST: n/n pass`, exit 0. Measured:

```
$ python3 .ufo/evidence/round-57/c1/measure.py --selftest --work <scratch>      (lane HEAD counter)
SELFTEST panel agrees: panel=0/5, pass                                FAIL
SELFTEST panel exactly allowed disagreements passes                   FAIL
SELFTEST panel one over allowed: panel_over=1                         FAIL
SELFTEST panel over counts the excess only                            FAIL
SELFTEST panel without a verdict for an id disagrees                  FAIL
SELFTEST panel without a verdict for a fixed-at-base id disagrees     FAIL
SELFTEST cli good exits 0, verdict is last line                       FAIL
C1_R57_SELFTEST: 89/96 pass
```
Receipt: `T57W3CritContract-receipts/c1-selftest-at-lane-head.txt`. The contract's "measured: 11/45" is an older run (`T57W2CritFreeze-receipts/c1-selftest.txt`).

Cause: amendment 2 added the A9 provenance arm (`panel_provenance`, called at line 457), and every panel fixture writes `{'verdicts': panel}` with no `detail` and no `files` (line 630). So `panel_prov=3` on every good fixture (`last run: {'panel_prov': 3} notes=[('panel-provenance', 'R50.1', None), ...]`). No selftest case exercises the A9 arm with a positive fixture. Fixing this needs counter fixture work (fixture panel with a `detail` naming a seat, a `files` sha, and a `w2-results.json` listing it); that is not staged here.

### B2. C2 counter passes a target clause the committed tree fails (counter defect, staged)
Contract C2 target: every gate row expecting exit 2 or 3 has an element of `expect.stdout_contains` **equal** to a CODES member, and the exit-2 element is exactly `RECEIPT_REV_UNRESOLVABLE`. Amendment 1(i) says the counter must be changed to match before freeze. The counter still uses substring matching (`CODE_RE.findall`, measure.py:245-247 at HEAD).

Command (the committed C0b registry, element equality against the gate's CODES):
```
$ git show adf87899…:tools/registry.json | python3 …   (receipt: element-equality-at-c0b.txt)
receipt-gate-accept exit 0 element-equal-to-CODES= []
receipt-gate-content-drift exit 3 element-equal-to-CODES= []
receipt-gate-unresolvable-certified exit 2 element-equal-to-CODES= []
```
Counter at C0b plus the committed instruments (scratch commit `1eca4e5ff3b3`, no staged change):
```
C2_R57: self=a5138acb2248 rev=1eca4e5ff3b3 gate_rows=3 exits=0,2,3 held=3/3 mutants=3/3 skill_row=1 codes_known=4/4 standing_cell=ok total=0 C2_R57_PASS=true
```
So the counter reports PASS on a tree whose target element clause is false.

Staged fix (`stage/.ufo/evidence/round-57/c2/measure.py`, plus `stage/tools/registry.json`):
- `row_named_codes(row, codes)` returns only elements equal to a CODES member;
- an exit-2 row must name `RECEIPT_REV_UNRESOLVABLE` exactly;
- the registry gains the bare code as a second element on `receipt-gate-content-drift` and `receipt-gate-unresolvable-certified`.

Results:
```
# staged counter, C0b registry (receipt c2-counter-staged-on-c0b-registry.txt)
C2_R57: … total=2 C2_R57_PASS=false
# staged counter + staged registry (receipt c2-counter-staged-candidate.txt)
C2_R57: self=69a0248acbfc rev=8f26e4a7b041 … total=0 C2_R57_PASS=true     (run after the CODES scope fix)
```
The first attempt raised `NameError: name 'CODES' is not defined`; fixed by passing `codes` in. An earlier "total=0" for this candidate was produced by running the original counter, not the patched one, and is withdrawn.

Note: the registry edit changes a frozen input (`tools/registry.json`) and the bind/precheck inputs, so it has a re-bind cost.

### B3. C2 staged counter selftest 19/20 (open)
```
CASE good fixture: every arm 0 FAIL  C2_R57: … skill_row=0 … standing_cell=ok total=1 C2_R57_PASS=false
C2_R57_SELFTEST: 19/20 pass      (receipt c2-selftest-staged.txt)
```
The good fixture's registry rows lack the bare-code elements and its SKILL verdict-map row lacks exit 1 and `RECEIPT_REV_UNRESOLVABLE`, so the stricter arms fire. Not fixed in this pass; the fixture rows and `FX_ROW` need the same edits as the registry and SKILL changes.

---

## B. Contract sentences false or unmapped at C0b/HEAD (staged in `stage/.ufo/evidence/round-57/contract.json`)

### C1. `claims.C1.before` quotes an unresolvable revision
The contract quotes `rev=aa691617c08b`. `git rev-parse --verify aa691617c08b^{commit}` does not resolve. The receipt `T57W2CritFreeze-receipts/before-c1.txt` says `rev=5014a93a6e26`. The receipt's `self=63a88c257490` is not the counter now at HEAD (`sha256` sha12 `6f3b7627a41d`), so the before-run must be re-produced by the frozen counter. Staged: rev corrected, and the self mismatch noted.

Before paths that do not exist (the contract asks for them): `.ufo/evidence/round-57/before/` is empty (`ls -A … | wc -l` = 0), so `before/c1.stdout`, `before/c2.stdout` and `before/c2-at-base.stdout` are absent. The C2 `before` admits the same gap.

### C2. TERMS in the contract versus the counter
`terms_line` says 18 terms; the counter's `TERMS` has 19 (`panel_prov` is missing from the contract). No `predicate_terms` clause maps `panel_prov`. Command: a python diff of `TERMS` against the contract text gives `IN COUNTER NOT IN CONTRACT: ['panel_prov']`. Staged: `terms_line` says 19; term (9) maps `panel_prov`.

### C3. Predicate and target clause (4): item tie is wider in the counter
The contract says the commit must "name the item id or the path in the item text". Counter (measure.py:324-328) also accepts the basename of the path in the item text, and a commit that begins with the blind panel's `detail` commit for the id (amendment 2(b)). Staged predicate and target (both identical, `predicate==target` checked) state all three forms.

### C4. Predicate and target clause (9): panel provenance is not stated
Clause (9) covers only the budget and the pin. The counter's `panel_prov` term (A9, `panel_provenance`) is not in the predicate. Staged.

### C5. `claims.C1.cannot_see` (c) cites the wrong lines
The contract cites `judge(), measure.py lines 272-275` for the open arm. Those lines are the `npath` canonicalisation (`sed -n 270,276p` shows `if isinstance(row.get('evidence'), list):` … `row = dict(row, evidence=…)`). The open arm is at lines 347-349 (`elif status == 'open':` and `note('open-unplanned', …)`), confirmed by `grep -n`. Staged.

### C6. `panel.status`, `frozen_notes`, `enumeration.panel_verdicts` say panel.json is absent
Command: `git ls-tree -r --name-only HEAD -- .ufo/evidence/round-57/c1/panel.json` lists the file; it has 51 verdicts and 25 `files` entries; `git cat-file -e HEAD:…` succeeds. The "NOT RUN … absent" and "does not exist yet" sentences are false. Staged.

### C7. `freeze_precondition`: docstring claim
"the docstring arms list matches the TERMS above" is false: `c1-terms-in-docstring.txt` reports `absent=9` (missing, spotcheck_changed, defects_pin, bad_status, evidence_bad, key_miss, open_unplanned, declined_bad, this_round_short). Staged sentence states that. The docstring fix itself is a counter edit (not staged).

### C8. `C2.enumeration.standing_tokens` names a floor the counter does not compute
Contract: "the non-vacuity floor is at least 4 table data rows and at least 4 distinct tokens". The counter's codes arm (`short['codes'] = unknown + (1 if not tokens)`) computes neither. Staged: the sentence states what the counter does.

---

## C. Panel (`c1/panel.json`) against the six re-seated ids

Contract `panel.seats`: "for those six ids the re-seat verdict is the panel verdict". Command (lane HEAD, receipt `panel-vs-reseat-at-lane-head.txt`):
```
R51.5   reseat=open    panel=open    MATCH   panel_detail=T57W2PanelR515R516
R51.6   reseat=open    panel=fixed   DIFFERS panel_detail=T57W2PanelR515R516
R52.5   reseat=fixed   panel=fixed   MATCH   panel_detail=T57W2PanelR525R526   (detail commit 5b703c6 ≠ re-seat 218bc6b5)
R52.6   reseat=open    panel=open    MATCH   panel_detail=T57W2PanelR525R526
R54.2   reseat=fixed   panel=open    DIFFERS panel_detail=T57W2PanelR542R543
R54.3   reseat=fixed   panel=open    DIFFERS panel_detail=T57W2PanelR542R543
```
Also: `panel.files` has no `T57W3Reseat*` entry; the w3 seat files are not committed (`git ls-tree … w3/ | grep -c Reseat` = 0); `w3-results.json` is not committed (A9 requires it).

Staged `c1/panel.json`: verdicts, `detail` (seat and commit) and `files` replaced for the six ids from the re-seat files; `files` references 25 seats; the staged file's re-seat check gives `differs=0` (`panel-vs-reseat-staged.txt`). Staging does not commit the w3 seat files or `w3-results.json` (the latter is orchestrator-written).

**Adjudication question for the L1:** the contract says "panel.json is not edited after its commit", and panel.json is already committed at HEAD. The correction is needed before `PANEL_SHA256` is pinned; the L1 must decide whether that is a pre-pin correction or needs a recorded amendment.

---

## D. `frozen_paths` against the instruments the run reads

`deciding-run.sh`'s freeze-integrity maps only `.ufo/evidence/round-57/…` and `tools/…` keys. Its `key()` returns `None` for anything else (verified: `key('.ufo/waves/round-57/w2-results.json') = None`), and an unmappable entry is a refusal. So the provenance inputs cannot be listed as written.

Read by the run, not in `frozen_paths` (found by regex over `deciding-run.sh`, `controls.sh`, `no-harm.sh`):
- `.ufo/waves/round-57/w2/*.json`, `w3/T57W3Reseat*.json`, `w2-results.json`, `w3-results.json` (read by C1 A9; not mappable);
- `tools/mutate-and-run.sh`, `tools/pbt-staged-id.py`, `tools/staged-id-guard.py`, `tools/shrink-case.py` (read by no-harm via `git show`; mappable). **Staged** as additions.
- `.ufo/evidence/round-21/coldread/measure.py`, `.ufo/evidence/round-21/coldread/ledger.json`, `.ufo/evidence/round-45/{freshness,coverage}/measure.py`, `.ufo/evidence/round-46/coverage/measure.py`, `.ufo/evidence/round-47/coverage/measure.py`, `.ufo/evidence/round-48/quality/coldread-precheck.sh`, `.ufo/evidence/round-18/measure.py`, `.ufo/waves/round-55/w1/T55W1ExecReKeyDryBind-receipts/binder-r55.py` (read by no-harm, the precheck and bind). These are not mappable under the current freeze. `ledger.json` is written by the bind, so it cannot be frozen at all. The contract's `frozen_notes` now says so. Closing this needs an amendment to `deciding-run.sh` (itself frozen).

All 19 entries in the original `frozen_paths` exist at C0b or HEAD (`ls`/`git cat-file` checked for the round-57 instruments; the lane tree has them).

---

## E. C2 contract sentences checked against the counter (verified)

- Gate rows at BASE: 22 `gate`-kind rows, none running the gate except the selftest row (not a gate row). Verified against `5e3569…:tools/registry.json`.
- SKILL at BASE: no row in `### Gate/probe registry` names `receipt-revision-gate.py`; the standing-rules row reads `RECEIPT_REV_MISMATCH` (SKILL.md:53). Verified.
- At C0b: 3 admitted gate rows (exits 0, 3, 2); SKILL registry row present (line 1547) with `0 PASS; 2 … (RECEIPT_REV_UNRESOLVABLE); 3 …; 1 usage`; standing cell `RECEIPT_REV_CONTENT_DRIFT`; CODES = 11 (AST-parsed).
- Counter's skill-row arm checks digits `0,2,3` only (`'023'`, measure.py:199) and no code; contract target requires exit 1 and the code. **Staged** (`'0123'` plus `RECEIPT_REV_UNRESOLVABLE` in the cell).
- Mutants: `mutants.json` present at HEAD with pin `d51f558c…` matching the counter; each `old` occurs once in the gate at C0b (`M1 1, M2 1, M3 1`); counter killed 3/3 (`mutant M1 … killed by receipt-gate-content-drift(got=0)` etc.).

---

## F. C1 counter facts checked

- Items: `defects.json` has 51 rows, 51 unique ids; 7 spot-check files (`python3 …` output in the contract matches).
- BASE ledger: 49 rows (31 fixed / 7 open / 11 declined), verified by `git show 5e35699…:corpus/routed-defects.json`.
- Counter's `PLANNED_ID`, `MAX_SPAN=30`, excerpt 15-400 chars, `THIS_ROUND_FLOOR=6`, `PANEL_ALLOWED=5`: match the contract text.
- Contract `predicate` and `target` are identical (checked).
- `PANEL_SHA256` is still `PIN_PENDING_SET_BY_L1_AFTER_THE_BLIND_PANEL`; the counter's `panel=pin` path is as stated.

---

## G. Deciding-run / cold-read gate (observed)

- Round-21 monitor at C0b: `score=6 credited=46 / 64 box3=False` (the contract's no-harm floor needs 64/64, score 8). Expected: this is the bind's input.
- `coldread-precheck.sh` at C0b: `COLDREAD_PRECHECK floor=5e3569969b53 floor_credited=64 cand=adf87899c70d cand_credited=46 lost=18 RED`, exit 1. The deciding run refuses at gate 0 until the bind (`rekey-r57-…`) is committed and measured. Consistent with the contract's no-harm arm.

---

## H. Not checked (stated)

- Panel verdicts themselves at BASE (25 seats, 51 verdicts): not re-audited; only the six re-seat ids were compared.
- `cannot_see` (c) "31 open rows passed in the wave-1 do-nothing run": not checked here.
- `corpus/lessons/round-57.md` exists (2922 bytes) but its `## Mistakes` row and the S283+ citation were not checked.
- The controls (`controls.sh`) and the no-harm monitors were not run end to end; only the deciding-run's gate-0 precheck and the counters were run.

---

## Staged files

- `stage/.ufo/evidence/round-57/contract.json`: C1 before rev, C1 term list and (9)/(4) predicate and target, freeze_precondition, cannot_see (c) lines, panel status and frozen_notes, `panel_verdicts`, C2 standing-tokens floor, four tools added to `frozen_paths`. JSON loads; predicate equals target.
- `stage/.ufo/evidence/round-57/c1/panel.json`: six re-seat ids corrected (verdicts, detail), `files` re-keyed to 25 seats including the three w3 re-seat seats. Round-trip identical format.
- `stage/.ufo/evidence/round-57/c2/measure.py`: element equality, exit-2 exactness, skill-row exit 1 and code. Compiles; selftest 19/20 (B3).
- `stage/tools/registry.json`: bare-code second element on two gate rows.
- `stage/T57W3CritContract.diff`: all four as `diff -u`.

Not staged (needs authoring by the L1 or a counter edit): the C1 selftest fixture work (B1), the C1 docstring TERMS list (C7), the C2 selftest fixture rows (B3), the w3 re-seat seat files and `w3-results.json`, the before-run receipts (C1, and C2 at BASE), and the `frozen_paths` closure for the bind/no-harm inputs (D; needs a `deciding-run.sh` amendment).

## Commands run (summary)

`git show <rev>:<path>`, `git ls-tree`, `git cat-file -e`, `git rev-parse --verify`, `git clone --shared` + `checkout --detach` (scratch), `python3 measure.py --selftest` (C1, at HEAD and staged), `python3 measure.py --lane … --rev … --explain` (C2 at C0b with instruments, staged on C0b registry, staged candidate), `coldread-precheck.sh` at C0b, `round-21/coldread/measure.py --rev adf8788…`, python snippets for TERMS/docstring, element equality, panel vs re-seat, freeze `key()` mapping, and the provenance arm on fixtures. Each output is quoted above and saved under `T57W3CritContract-receipts/`. The C1 `before` line is not re-run: it is cited from the existing receipt and was not reproduced here.

No tool was installed or upgraded.

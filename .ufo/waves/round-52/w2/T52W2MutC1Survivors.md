# T52W2MutC1Survivors — frozen C1 survivor follow-up

Scope: C1 counter at CAND0 `bcba8924894216268afc4171f06eb8c28e912b46`; read-only lane; scratch clone at `/fast/scratch/hyaku/tameshi-r52/T52W2MutC1Survivors/clone`. No fixture commits were needed: the assigned checks are pure imported predicates. No `registry-check` or other runtime was invoked.

## Probes and classification

| Item | Concrete probe / evidence | Classification |
|---|---|---|
| M05/M06/M19 base-active drop | Wave-1 shows the forged tree: change a BASE-active row to `superseded`. In source `measure.py:116-117`, the active set and dropped set use only REV registry bytes; `len(dropped)` is directly part of the total at line 142. A registry edit in a lane revision therefore reaches the M05/M06/M19 blind point. | **Real forgery reachable by lane edit.** M05 or M06 can suppress the dropped set; M19 can omit its contribution. No fixture commit made; this conclusion is the concrete tree in W1 and clause-level source inspection. Command: `python3 -c '...read measure.py lines 116-117,142...'` (equivalent source displayed by `python3 -c`/`git show`). |
| M14 C3 digest gate | `measure.py:121-130` gets C3 source from REV and executes it only if its digest equals the frozen digest. A REV edit replacing the C3 file with the W1 one-line PASS-printing stub makes the digest differ, thus pristine sets output to empty and `parse_c3` returns `(None,30)` (lines 80-82); M14's `if True` instead executes attacker code. | **Real forgery reachable by lane edit.** The forged tree and expected behavior are detailed in W1; no runtime invoked here. Command: `git -C <clone> show bcba8924894216268afc4171f06eb8c28e912b46:.ufo/evidence/round-52/c1/measure.py` (source lines 121-130). |
| M20 PASS label / M21 exit | A nonzero total is directly rendered and returned in source lines 142-146. At CAND0 the C2 probe is irrelevant; W1 gives the concrete BASE total=4 example, where M20 would print true with nonzero total and M21 would return 0. Such a one-point counter edit is in the frozen C1 script, not a lane-content edit. | **Requires editing frozen evidence.** `deciding-run.sh` includes `.ufo/evidence/round-52/c1/measure.py` in `FROZEN`, and `git diff --quiet "$FREEZE" "$REV" -- $FROZEN` rejects any difference (lines 32-35). Command: `python3 -c 'print(...)'` reading `.ufo/evidence/round-52/deciding-run.sh`; excerpt verified directly. |
| Pristine parse_c3 ignores PASS token / consistency | Imported CAND0 module probe: `parse_c3("C3_R51: tools=10 rows=10 covered=29 missing=1 total=0 C3_R51_PASS=false")` returned `(29, 0)`. A REV change to the C3 tool can emit this accepted line while frozen C3 digest remains intact, since the C3 counter measures the REV tree. | **Real forgery reachable by lane edit.** Command: `python3 -c 'import importlib.util; ... print(m.parse_c3("C3_R51: tools=10 rows=10 covered=29 missing=1 total=0 C3_R51_PASS=false"))'` (actual output `(29, 0)`). |
| Pristine mte needle list accepts stale 9/9 beside correct K/K | Imported probe with active gate row, required `2/2` needle and additional `9/9` needle returned `(True, ...)`. A REV registry edit can retain both; this check is independent of actual tool output. | **Real forgery reachable by lane edit.** Command: imported `mte_row_ok` probe; actual output starts `(True, "legs=2 want=...`.
| Pristine absent LEG_TABLE allows None/None needle | Imported probe with `mte_src='x=1'` and needle `MTE_INTEROP: PASS legs_conforming=None/None` returned `True`; `leg_count('x=1')` returned `None`. Lane edit can delete LEG_TABLE and adjust registry needle. | **Real forgery reachable by lane edit.** Command: imported `leg_count`/`mte_row_ok` probe; actual output `(... True ...) leg_count None`.

## Commands / evidence

- Required contract read first; witness: `.ufo/evidence/round-52/contract.json` C1 predicate and cannot-see statement.
- Imported probe command executed: `python3 -c 'import importlib.util,json; ... parse_c3(...); ... mte_row_ok(...); leg_count(...)'`; outputs above are literal.
- Clone identity verified before any possible fixture mutation: `git -C /fast/scratch/hyaku/tameshi-r52/T52W2MutC1Survivors/clone rev-parse --show-toplevel` → that clone path. Candidate resolved to CAND0. No git mutation/commit occurred.
- Counter lane SHA-256 observed: `3edfdb8737c667430f5555076899851ecaa25e4b2e5ccfe4c0603ae3e0bb3ec6`. Lane untouched. No tools installed/updated.
- All findings are clause-level; the full counter was intentionally not run, as requested. The assignment's “PRISTINE frozen counter would wrongly pass” cases are not asserted as end-to-end run receipts where the frozen counter invokes an external detector; they are proven at the exact imported functions/branch points.

## Summary
- M05/M06/M19 and M14 are reachable by lane content changes; their blind points are main() clauses, not detector coverage.
- PASS-token inconsistency, stale dual needles, and absent-table `None/None` are reachable lane-edit holes, proven by imported CAND0 predicates.
- M20/M21 require changing frozen C1 evidence; deciding-run FROZEN diff detects that change.
- No full registry-check, test suite, or other runtime was invoked; lane counter bytes remained unchanged.

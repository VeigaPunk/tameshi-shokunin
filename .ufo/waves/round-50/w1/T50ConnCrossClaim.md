# T50ConnCrossClaim — cross-claim pattern finder (C1 × C2)

Seat: `T50ConnCrossClaim` (connector). Round 50, lane `tameshi-shokunin`, base `e3729de862f73ae080d98fcf522a7081ce16e40a`, freeze `cdbf24c07f9be3a991997c25b1f1d4bb375014ae`. Read-only on the lane; probes were run on a scratch clone at `/fast/scratch/hyaku/tameshi-r50/T50ConnCrossClaim/lane` (deleted before yield); a probe is never a verdict.

## Evidence base

- `contract.json` (round-50) read in full; both frozen counters read in full (`.ufo/evidence/round-50/c1/measure.py`, `c2/measure.py`).
- Probes (observed output):
  - `c1/measure.py --selftest` → `C1_R50_SELFTEST: cases=25 failed=0`, exit 0.
  - `c2/measure.py --selftest --lane <clone> --work <scratch>` → `C2_R50_SELFTEST: cases=9 failed=0`, exit 0.
  - `c1/measure.py --lane <clone> --rev HEAD --explain` at `HEAD=4afb060c…` → `defects=49 rows=0 fixed=0 open=0 declined=0 … missing=49 … total=74 C1_R50_PASS=false`, exit 1 (the contract's before-state; no ledger exists yet).
- Git facts:
  - `git diff 7d3d977f e3729de8 -- tools/` → empty: the frozen generator (`GEN_REV` `7d3d977f`; `c2/measure.py:50-51`) is byte-identical to the base copy.
  - `git diff e3729de8 HEAD -- tools/ corpus/` → empty: round-50 has touched neither `tools/` nor `corpus/` so far; `tools/shrink-case.py` is absent.
  - Round-50 commits so far are only `.ufo/evidence/round-50/*` plus the SCORECARD pre-registration (`4afb060`).

## (a) Causal separability

### Claim-local surfaces

- C1 (`c1/measure.py:153-269`) consumes: the frozen 49-item `defects.json` (byte-pinned, sha256 `6a953e6e…`), the ten spot-check blobs (byte-pinned per item), `corpus/routed-defects.json`, `SCORECARD.md` (newest `**Planned (round` paragraph, `planned_ids` at `c1/measure.py:95-111`), and git history (`is_ancestor`, `touched` via `diff-tree`). None of these exist only after C2 lands.
- C2 (`c2/measure.py:187-322`) consumes: `tools/shrink-case.py` at REV, `tools/staged-id-guard.py` (byte-pinned, `guard_pin`), `tools/pbt-staged-id.py` at `GEN_REV` (frozen, pinned) and at REV (copied next to the shrinker, which may import it; `c2/measure.py:227-230`), the two panels (public round-49, hidden round-50), and the records: `corpus/README.md` (a line with `F6` and `held (round 50)`), `corpus/SOURCES.md` (a row with `mined` in cell 7 and `2026-10-26` in cell 8), and a `corpus/knowledge/` file new since base naming F6 and citing such a row (`c2/measure.py:325-354`). None read the ledger.

### Intersection list: files both claims could touch or cite

1. `tools/pbt-staged-id.py` — the only file one claim **writes** while the other **executes/imports**. C1: routed item R49.1 (`keys`: `pbt-staged-id.py`, `os.path.isfile`, `T49W2RevGenCode`, `unreadable guard`), `routed_at` = base; the no-harm tools-scope monitor allows exactly `A:tools/shrink-case.py` and `M:tools/pbt-staged-id.py` (`no-harm.sh:29-31`), so R49.1's fix is the edit to this file. C2: the frozen copy is the kill oracle and the case finder; the REV copy is handed to the shrinker to import.
2. `tools/staged-id-guard.py` — C2 pins it (freeze digest `03a796c5…`; `guard_pin` counts a mismatch as a fail and falls back to BASE; `deciding-run.sh:36` diffs it between freeze and REV, so any C1 fix commit touching it breaks the deciding run). C1 may cite it read-only (no item key matches today).
3. `corpus/README.md` — C2's record check reads it (F6 `held (round 50)`); C1 evidence may cite it (allowed path). Currently the frontier table row F6 is `open` at `corpus/README.md:83` (`S022, S023, S024`; no `held (round 50)` line exists yet).
4. `corpus/SOURCES.md` — C2's record check parses its rows (`c2/measure.py:331-338`); C1 evidence may cite it — R41.7's keys literally name `SOURCES.md:436`.
5. `corpus/knowledge/*.md` — C2 requires a new F6 entry since base; C1 evidence may cite knowledge files (S-key items).
6. `.ufo/evidence/round-50/c2/measure.py` — C2's own instrument; it is **not** in C1's `HARD` set (`c1/measure.py:59-60` lists only `c1/`, `control/`, `contract.json`, `freeze.json`), so a C1 row could legally cite the C2 counter as evidence (e.g., R49.2's "successor counter" wording). Asymmetry: C1's own instruments are excluded, C2's is not.
7. `tools/shrink-case.py` — C2's deliverable, not excluded for C1 evidence; no key requires it, but any row citing it would make C1 depend on C2 having landed first.
8. `SCORECARD.md` — C1 reads it for `open` status (newest `**Planned (round` paragraph; currently `SCORECARD.md:2410` = `**Planned (round 50):**`); C2 never reads it.

### Directional verdicts

- **C1 verifies without C2 landed: yes.** None of C1's inputs are produced by C2; the HEAD probe (`missing=49`, `total=74`) is a pure C1-before state. C1's pass conditions (fixed ≥ 20, declined ≤ 12, ≥ 5 fixes by commits after base) are independent of the shrinker and the F6 records.
- **C2 verifies without C1 landed: yes, with one caveat.** C2's inputs exist at base except the shrinker and the records. The caveat is the shared generator: if R49.1 has not landed, REV generator == frozen generator (verified identical) — the safest state. If R49.1 has landed, C2's shrinker imports the REV copy while the judge verifies with the frozen copy; C2 then passes only if the fix keeps the generator's executed semantics stable on the panel domain.
- The routing ask for R49.1 (round-49 spot-check lines 120-127: error-path exit codes, `os.path.isfile` guard check, selftest-add that fails before the fix) targets a domain C2 never walks — guards are always regular files created in the counter's work dirs — so today the dependency is benign, but it is **unchecked** (see (c)).

## (b) Shared blind spots

- **C1 — semantic support** (contract `cannot_see`, line 35): `fixed` is entirely structural — a keyed excerpt that is new since routing, whose `commit` is not an ancestor of `routed_at` and touches the path, on lines free of `ACK_WORDS`. Any new keyed line passes even if no behavior changed; `CTL_FAB` reaches `fixed=38` with every other term green, and only the after-base floor stops it (contract line 42).
- **C1 — underclaim**: `open`/`declined` rows are never checked against the tree; an item actually fixed can be marked `declined` with a ≥ 40-char reason and pass.
- **C2 — search quality** (contract line 59): `runs` is the instrumented guard-invocation count, not the strategy; a shrinker that meets 1-minimality only on the 20 cases still passes (19/20 bar, hidden panel is a sample).
- **C2 — oracle authority**: the kill oracle is the frozen generator's own `check()` (`c2/measure.py:296-299` uses `gen.check`); it is self-referential (the same generator class C1's R49.1 fix edits), and nothing compares the REV copy (which the shrinker imports) to the frozen copy. A divergence would not be diagnosed — it would only surface as an unexplained `ok_short`.
- **Shared**: one snapshot, exactly one deciding invocation, history-trusting (`is_ancestor`/`touched`/`diff`), self-authored artifact per claim (ledger statuses; shrinker tool) validated only within its own mechanical rules.

## (c) One pattern worth a QUALITY criterion

**Pattern — dual-use artifact drift.** A single repository file (`tools/pbt-staged-id.py`) is simultaneously (i) C1's fix target and evidence surface for R49.1 and (ii) C2's behavioral dependency (frozen oracle + REV copy imported by the shrinker). C1 cannot see behavior (only text newness); C2 never checks that the two generator copies agree. So C1's fix is a silent variable in C2's verdict, and C2 is the only place a behavioral regression in that file would manifest — as a non-diagnostic shrinker failure.

**Criterion — cross-claim behavioral equivalence of shared executed files.** At the deciding revision, a file modified by a fix cited in C1's ledger that is also executed or pinned by another round gate must satisfy the sibling claim's contract, verified behaviorally, not by prose. Concretely: in `c2/measure.py`, per panel mutant, also run `find_case` with the REV generator copy and require the same counterexample index as the frozen copy (one extra generator run per mutant, ~+5% runtime). Alternative/cheaper: extend `no-harm.sh`'s `r49-generator-capability` monitor (`no-harm.sh:32-35`) with mutant-mode agreement (REV copy finds the same 12 public mutants as the frozen copy). This makes the R49.1 edit an explicit, machine-checked input to C2 instead of an unobserved one.

## Also noted

- `deciding-run.sh:36` protects the guard and every round-50 instrument in its `FROZEN` list; `tools/pbt-staged-id.py` is deliberately outside it (it is C1's allowed edit), which is why the (c) check belongs in the C2 counter or no-harm rather than in deciding-run.
- C1 rows may cite C2's record files (`corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/*`) read-only; the append-only record discipline keeps such excerpts stable across C2's additions.

## Summary

- Current1 and C2 are causally separable: C1's inputs exist before C2; C2's exist before C1 except the shrinker and F6 records (probes: C1 selftest 25/25, C2 selftest 9/9, C1 @ HEAD missing=49 total=74).
- The only real edge is `tools/pbt-staged-id.py`: C1 writes it (R49.1), C2 imports/executes it (frozen oracle + REV copy).
- Both gaps named in the contract hold: C1 semantic support (CTL_FAB=38; floor is the only backstop) and C2 search quality (cost = guard calls; 19/20 sample).
- New shared blind spot: C2 never compares the REV generator copy to the frozen one, so C1's R49.1 fix is an unchecked variable in C2's verdict.
- Proposed QUALITY criterion: cross-claim behavioral equivalence of shared executed files — REV copy must find the same panel counterexamples as the frozen copy (in C2's measure or no-harm).
- Today the dependency is benign (the fix targets error paths C2 never walks), but it is unverified; the criterion makes it explicit.
- Receipts: `T50ConnCrossClaim.c1-selftest.stdout`, `T50ConnCrossClaim.c1-explain.stdout`, `T50ConnCrossClaim.c2-selftest.stdout` in this wave dir.

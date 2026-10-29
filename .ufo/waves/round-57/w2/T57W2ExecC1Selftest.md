# T57W2ExecC1Selftest — C1 counter selftest for amendment 1

Staged: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w2/T57W2ExecC1Selftest/stage/.ufo/evidence/round-57/c1/measure.py` (sha256 de1b47a042cb183b7f871781de769621c5624cc7b06564d9464bcd9eb8cd37ad). Install at `.ufo/evidence/round-57/c1/measure.py`.
Receipts: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w2/T57W2ExecC1Selftest-receipts/` (selftest.txt, mutants.txt, real-tree-smoke.txt).

## Result
`python3 measure.py --selftest --work DIR` -> `C1_R57_SELFTEST: 95/95 pass`, exit 0 (baseline before my work: every case that used the ledger failed, 30+ FAIL, because rows lacked `status_at_base` and fixture commits did not name ids).

## Code changes (besides the selftest rewrite)
1. `measure()` result carries `panel_allowed`; `verdict()` prints `panel=<n>/<res.panel_allowed>` (was the global PANEL_ALLOWED, so a non-default `panel_allowed` was mis-shown). Shape unchanged (panel before spot), exit codes unchanged.
2. Module docstring rewritten: "Amendment 1 ... exactly as coded" A1..A6 + updated arms/row rules/verdict line.
3. Selftest prints the non-zero counts and EXPLAIN notes of the last run under any FAIL line (debug aid).
`DEFECTS_SHA256` and `BASE` untouched (a case asserts their values).

## Fixtures per amended arm (each: refusal asserted on the tally, the explain note and the verdict line; plus a passing control)
- (1) status_at_base: absent, outside enum, fixed-at-base now open, fixed-at-base now declined -> base_status_bad; fixed at base with commit not ancestor of BASE -> fixed_bad (+note fixed-base-incoherent); commit ancestor of BASE with sab open -> fixed_bad; controls: sab fixed + base=fix passes; sab declined + fix after base passes.
- (2) whole-token keys: hyphen/underscore/letter neighbours before and after refuse (key_miss); parentheses+case and comma pass; path suffix `docs/wave-slots` and `wave-slots` pass, `docs/xwave-slots`, `docs/wave-slots-notes` refuse; underscore key neighbour (BACKTICK / TICK_RE in BACKTICK_RE) refuse, `compile` / `BACKTICK_RE` pass.
- (3) fixed rows: wave-1 forgery (`unrelated tidy` commit quotes the excerpt into a new file) refused; same quote under message `tidy R50.1` passes; message naming R50.12 / xR50.1 / v1.R50.1 refused; tie by item text path, basename, extended_text pass, different path refused; excerpt already at the first parent refused (commit names the id, so only `introduced` refuses) vs excerpt added by that commit passes; excerpt at routed_at, dropped, re-added by the commit refused; ack control (same commit, ack-free line passes, `carried forward` line refused).
- (4) newest Planned by round number: round 10 vs round 9 in both file orders (also catches lexical compare); R50.3 open then open_unplanned, R50.2 open passes.
- (5) panel arm via `panel_pin`: file absent -> panel_pin=1; agree -> 0/5 pass; pin mismatch -> panel_pin=1, panel=pin, panel_over=0; exactly allowed (1/1) passes; one over (1/0) and excess-only (2/1) -> panel_over=1; missing verdict disagrees; sab vs verdict disagreement. CLI: explicit pin passes; default pin (PANEL_SHA256) is a miss (exit 1, panel=pin) whatever it holds, so the selftest does not depend on it. Shape case for the verdict line (regex, panel before spot).
- (6) floors: explicit floors in all fixtures; case proves FIXED_FLOOR=0, DECLINED_CAP>=999 non-binding (explicit floors give fixed_short=1, declined_over=1 on the same ledger; defaults give 0/0).

## Liveness sweep (mutants of the staged file; `mutants.txt`)
32 mutants, each run through the selftest: 30 killed (`n/95` < full, exit 1). Survivors: `tie-path-off` (dropping `item['path'] in item_text`) is an EQUIVALENT mutant: if the path is in the text, the basename always is, so the basename clause alone decides — the path clause is redundant dead weight in measure.py (not changed: not in scope, harmless). `routed-off` survived the first sweep, which exposed a missing fixture (excerpt present at routed_at, removed, re-added by the commit); fixture added, rerun: 94/95, killed. `tie-id-prefix` was a syntax-error mutant (not a result); the id-boundary arm is killed by `tie-id-lookbehind` and `tie-id-lookahead`.

## Real-tree smoke (not a gate)
Staged counter on the lane working tree (dry-c1 recipe, staged measure.py): runs clean, exit path ok; `C1_R57_PASS=false total=31` (evidence_bad=4 key_miss=8 fixed_bad=8 open_unplanned=10 panel_pin=1) — ledger/panel are the L1's, not part of this item. `panel=pin` is the by-design miss of the pending pin.

## Risks
- The wave-1 forgery arm rests on commit-message / item-text tie only; semantic support stays unseen (docstring says so).
- Tools: none installed.

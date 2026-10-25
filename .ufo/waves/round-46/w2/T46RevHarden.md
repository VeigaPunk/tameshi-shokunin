seat: T46RevHarden
item: review the two hardened counters (.ufo/evidence/round-46/hardening/{freshness,coverage}-counter.py) against the round-45 originals — diff non-additivity, mutants.json byte identity, 3x selftest stability, addition audit (pin/__file__/crash-pass/fixture assumptions), try-mutants tables, and masked equivalence over the round-45 data revision ea25e022.

## Scope and provenance
- Lane: /home/vgpnk/Projects/shokunin/tameshi-shokunin. Read-only except this report. Scratch: /tmp/tameshi-r46-T46RevHarden/ (diff outputs, selftest logs, re-assembled copies). No git mutations; only `git show`/`git log`/`git status` reads.
- Content revision check: `git cat-file -t 6f2168e028ce7ff6e82ac92093ac05dd1f147c32` -> commit; `git show 6f2168e0:.ufo/evidence/round-46/hardening/{freshness-counter.py,coverage-counter.py,mutants.json} | cmp - <worktree>` -> all three byte-identical to the working tree. `git status --short` on both dirs: clean. HEAD eada0b36 adds only wave-2 spec/dispatch/registry files.
- No tools installed; python3 + git only. Pacman untouched.

## 1. Diff non-additivity — VERIFIED
`diff -u round-45/freshness/measure.py round-46/hardening/freshness-counter.py` (402 diff lines) and `diff -u round-45/coverage/measure.py round-46/hardening/coverage-counter.py` (211 lines). Removed lines per file, excluding the `---` header: exactly 2 each —
- `SELF_PATH = '.ufo/evidence/round-45/{freshness,coverage}/measure.py'` -> `'.ufo/evidence/round-46/hardening/{freshness,coverage}-counter.py'`
- the tally print `len(cases)[+4]` -> `len(cases)[+4] + extra_cases` with the `extra_cases = 0` head and one `_c, _f = extra_*()` call pair per addition.

Everything else is `+` only. Matches assemble.py's documented transform exactly.

Reassembly check: `assemble.py --group freshness --add w1/Hard{Grade,Population,Reviews,Measure}.addition.py` and `--group coverage --add w1/HardCover{1,2}.addition.py` into /tmp — `cmp` vs committed counters: **byte-identical** both (`FRESH-IDENTICAL`, `COVER-IDENTICAL`). The committed files contain exactly the six w1 additions, in the named order, nothing else.

## 2. mutants.json rule lines byte-identical — VERIFIED
Script over all 31 entries: every non-null `old` occurs exactly once in its round-45 source AND exactly once in the hardened copy (freshness 15 mutants + FN2/FN3, coverage 10 + CN2/CN3; `byte_in_orig=True`, `orig_count=1 hard_count=1` for all). FN1/CN1 are `old=null` appends (a trailing comment — inert). No mutant anchor was shadowed by added text (assemble.py inserts before `def main()`; all anchors retained count==1), so none goes silently inapplicable.

## 3. Selftest x3 — VERIFIED
`python3 <hardened> --selftest` three times each (python-timed runs):

freshness: rc=0 all runs; walls 0.35s/0.35s/0.31s; `C1_R45_SELFTEST: cases=34 failed=0` + `VERDICT: PASS`; PASS-lines 33+header; outputs diff-identical across runs even before tmp-path normalization (no tmp paths appear in stdout); stderr empty.
coverage: rc=0 all runs; walls 0.93s/1.21s/1.00s; `C2_R45_SELFTEST: cases=20 failed=0` + `VERDICT: PASS`; outputs identical across runs; stderr empty.

Baselines: originals print cases=19 (freshness) and cases=10 (coverage); additions add 15 (3+3+5+4) and 10 (5+5) — tallies match exactly.

## 4. try-mutants on hardened files — full tables
`python3 .ufo/evidence/round-46/hardening/try-mutants.py --group freshness --file .ufo/evidence/round-46/hardening/freshness-counter.py` (wall 6.7s):
```
PRISTINE pass VERDICT: PASS
MUTANT F01 mutant killed
MUTANT F02 mutant killed
MUTANT F03 mutant killed
MUTANT F04 mutant killed
MUTANT F05 mutant killed
MUTANT F06 mutant killed
MUTANT F07 mutant killed
MUTANT F08 mutant killed
MUTANT F09 mutant killed
MUTANT F10 mutant killed
MUTANT F11 mutant killed
MUTANT F12 mutant killed
MUTANT F13 mutant killed
MUTANT F14 mutant killed
MUTANT F15 mutant killed
MUTANT FN1 neutral survived
MUTANT FN2 neutral survived
MUTANT FN3 neutral survived
```
`python3 .ufo/evidence/round-46/hardening/try-mutants.py --group coverage --file .ufo/evidence/round-46/hardening/coverage-counter.py` (wall 15.3s):
```
PRISTINE pass VERDICT: PASS
MUTANT C01 mutant killed
MUTANT C02 mutant killed
MUTANT C03 mutant killed
MUTANT C04 mutant killed
MUTANT C05 mutant killed
MUTANT C06 mutant killed
MUTANT C07 mutant killed
MUTANT C08 mutant killed
MUTANT C09 mutant killed
MUTANT C10 mutant killed
MUTANT CN1 neutral survived
MUTANT CN2 neutral survived
MUTANT CN3 neutral survived
```
Result: killed=25/25 declared, neutral_killed=0/6, pristine=1 — exceeds the 23-of-25 bar.

Baseline on the originals (`--file .ufo/evidence/round-45/.../measure.py`): all 25 mutants `survived`, all 6 neutrals `survived`, pristine pass — reproduces the contract's before_state (killed=0) and confirms each manifest entry is a genuine declared survivor of the *round-45 selftest*, not already-dead.

## 5. Equivalence over ea25e0224fc81060414b27301c27bd1344669165 — VERIFIED
`python3 <counter> --lane <lane> --rev ea25e022...`, then masked every token starting `self_pin=` or containing `_PASS=` (same rule as mutate.mask):

freshness: orig `self_pin=1 population=73 entries=73 verified=73 drifted=0 unreachable=0 invalid=0 unreviewed=0 disputed=2 fresh=71 score=9 target=50 rev=ea25e022 C1_R45_PASS=true` (rc 0) vs hardened identical except `self_pin=0` / `PASS=false` (rc 1 — hardened path absent at that rev, expected). Masked outputs: **identical** (plus 2 shared DISPUTED lines).
coverage: orig `self_pin=1 rows=2 entries=2 indexed=2 row_ids=S256,S257 rev=ea25e022 C2_R45_PASS=true` vs hardened same with `self_pin=0`/false; ENTRY lines identical. Masked outputs: **identical**. At the deciding rev the hardened copies are committed at their SELF_PATHs, so the driver's own equivalence() sees self_pin=1 on both sides; the non-vacuousness guard is satisfied (orig prints `_PASS=true`).

## 6. Per-mutant kill attribution — VERIFIED (strongest check)
Ran each of the 31 mutated hardened copies' --selftest (mutate.apply + run_selftest logic, 300s timeout): every declared mutant FAILs **exactly one case and it is the case named after it** (F01->F01_snapshot_absent_reason, F02->F02_quote_upper_bound_25, ... C10->C10_self_pin_zero_fails), rc=1, no Traceback anywhere. All 6 neutrals print VERDICT: PASS rc=0. So every kill is the discriminating assertion the seat intended — no crash-kills, no collateral-kills, no case killed for the wrong reason.

## 7. Addition audit (Hard{Grade,Population,Reviews,Measure}, HardCover{1,2})
- Source pinning: none. `__file__` is read only to (a) invoke the counter CLI in a scratch repo and (b) write its bytes into the fixture's SELF_PATH slot so the *subprocess* computes self_pin — HardMeasure.addition.py:58, HardCover1.addition.py:33, HardCover2.addition.py:40-41. sha256 calls hash fixture snapshots/pages, never source bytes; C10's `self_bytes` override writes foreign bytes to *create* the self_pin=0 input, not to assert a digest. The CTL_E cheat class (pinning own byte length) is absent.
- Crash-pass: none. Every measure-level case asserts fields of the printed `C1_R45:`/`C2_R45:` summary plus exit code (_xHardMeasure_case checks rc; Cover1/2 assert `want in last stdout line`); a crash produces no summary -> FAIL, not PASS. Kill-matrix run shows all mutated copies exit 1 with named FAIL lines, no tracebacks.
- Fixture assumptions: all fixtures are hermetic scratch repos (git init, `rev-parse --show-toplevel` asserted == scratch dir before first commit, throwaway identity only there). No case depends on lane state — no S160-row or live-ledger assumption; F15 derives its boundary from the counter's own MAX_ID=160 constant, F11 builds TARGET=50 rows from the constant itself. Pristine selftest passes 34/34 and 20/20, so no case fails on the pristine counter.
- Honest kills verified semantically, e.g. F01 mutant `raw=b''` falls through the sha256 check (fixture uses raw_sha256=sha256(b''), verdict drifted) -> returns `('drifted','ok')` vs wanted `('invalid','snapshot absent')`; F06/F09 attack different gates (author equality vs reviewer-in-report-text); C02 mutant regex `round-4[45]` admits the round-44 fixture anchors -> rows=2 vs wanted 0. Mutant `new` strings all parse (no syntax-error freebies).
- env hygiene: `_xHardMeasure_env`, `_xHardCover{1,2}` build scrubbed GIT_* envs with GIT_CONFIG_GLOBAL=/dev/null.

## Findings
- **INFO** — `coverage-counter.py:253` (`_xHardCover1_last_line`) runs the counter subprocess without `env=env`, inheriting ambient GIT_* vars; sibling `_xHardCover2_build` at :353-354 passes `env=env`. This mirrors the *original* round-45 selftest's own convention (measure.py:174 does the same), is unreachable inside the deciding path (mutate.py scrubs ENV before every run_selftest), and cannot flip a verdict on this host — noted only for the record.
- No BLOCKING/HIGH/LOW defect found in scope. No unreproduced defect attempted.

## Residual risks / verification gaps
- The C2 driver `mutate.py` itself is out of my scope; MutDriver (w1) reports its 8-case selftest is toy-shaped with 8 declared driver-rule probes surviving (e.g. MIN_KILLED 23->22, neutral_killed gate, equivalence `_PASS=true` guard, self_pin digest drop). Those are coverage gaps of the driver's own selftest, not defects observed in the shipped code path; the deciding run's arithmetic (`killed>=23`, `neutral_killed==0`, pristine, equivalence) was exercised here only via try-mutants + my own equivalence check, both consistent.
- I did not run the deciding command (`mutate.py --lane --rev 6f2168e0 --targets hardened`); per bounds that run is the L1's. My working-tree try-mutants runs are bit-exact proxies (files `cmp`-identical to the 6f2168e0 blobs).
- Wall times: three-runs + try-mutants (6.7s/15.3s) leave ample margin under the driver's TIMEOUT=300/mutant (8 workers); no flakiness observed in 3+31+37 executions.

## Verdict
Operability artifacts pass every attack I could construct: diffs are exactly the two sanctioned needles; all 31 rule lines byte-identical and uniquely applicable; selftests stable across runs; additions pin no source bytes, never pass on crashes, and are hermetic; 25/25 declared mutants killed by their own named discriminating case; 0/6 neutrals killed; masked equivalence at the round-45 data revision holds. Recommendation: C2's hardened-counter surface is sound for the deciding run.

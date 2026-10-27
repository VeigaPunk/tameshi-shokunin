# T51W2CritC2Counter — falsifier review

Axes: **calibration** (strength of findings vs evidence), **depth** (counterexample quality), **operability** (reproducible evidence and bounded correction).

## F1 — M01–M15 are plausible single-edit weakenings, but “violates exactly its named clause” is only partly established

The mutation recipe is concrete: `w1/receipts/probe.py:64-115` makes one exact replacement per mutant and asserts one occurrence (`:119-127`); `mutant-diffs.txt:1-45` records the diffs. The flip generator `probe.py:401-429` constructs a deliberate tree for M01–M15 and runs pristine plus mutant (`:432-449`). Example M01: the forge changes the new leg's table count from 2 to 3; the receipt says pristine reports `UNWIRED (table-counts)`, `wired_legs=9`, whereas M01 reports PASS (`receipts/run-flip-wired-mutant.txt:13-16`). This is a genuine violation of the all-wired condition, not merely an unexplained green result.

However, the blanket wording “each T_X satisfies every clause except X” is too strong for some forges. In particular M14's `dict(ledger='m14')` construction needs scrutiny: the report says it drops `js-cite-check` and duplicates another, and the observed marker is `pin_ok=0` (not an explicit `base_present=0`) at `T51MutC2Counter.md:132-134`; absent full pristine receipt evidence for all ten flags, it is not demonstrated that *only* base-presence fails. Likewise the shared fake runner for these forges can establish the counter's predicate behavior but cannot establish authentic regression provenance, explicitly admitted by the report itself (`:47-55`). Treat the findings as counter-forge demonstrations, not evidence that the real candidate's C2 receipts are trustworthy. The report's own evidence index points to exact per-forge receipts; a reviewer should inspect those, not generalize from the matrix.

D1/D2/D3 non-detection is established operationally for each tested mutant by the matrix and detector protocol (`T51MutC2Counter.md:10-25, 66-86`; `receipts/probe.py:378-390`). But D2/D3 use only negative 9-leg controls; thus their all-green result on weakened predicates is expected and says nothing about their behavior on positive evidence trees. D1 tests parser/selftest paths, not positive clause consumers (`T51MutC2Counter.md:147-160`).

## F2 — Independent blind spot: the regression-output recognizer accepts a forged PASS line

A direct code-level counterexample is M08's weakest acceptance rule: production `regression()` takes the *last* line beginning `REGRESSION: ` from captured stdout and returns green whenever return code is zero and that line starts with `REGRESSION: PASS (cases=10 passed=10` (`.ufo/evidence/round-51/c2/measure.py:162-188`). It does not verify that ten `REGRESSION_CASE` records exist, that their names are unique/expected, or that the summary's counts agree with them. The registered regression requirement is only the final prefix and successful exit (contract C2 at `contract.json:35-43`; actual code above). Therefore a runner can print the required line without executing cases and still satisfy `f['regression']=1`; an even sharper probe is ten duplicate/missing case lines plus the accepted summary. Existing M08 forge tests only the `cases=9` spelling (`probe.py:417`), not the absent/forged per-case output case.

Reproducible source inspection commands:

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 6d8c11e378aa90b12650808e1b79270742935f15:.ufo/evidence/round-51/c2/measure.py | nl -ba | sed -n '162,188p'
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 6d8c11e378aa90b12650808e1b79270742935f15:.ufo/waves/round-51/w1/receipts/probe.py | nl -ba | sed -n '401,449p'
```

Small correction: parse and validate exactly ten unique expected `REGRESSION_CASE` names and their PASS status, plus consistency with the terminal summary (or consume a structured receipt); bind the actual executed suite separately. This remains a forged-tree counter limitation, not a claim that the candidate runner did this.

## F3 — M16 equivalence is conditional; the stated proof omits a cardinality premise

The reasoning at `T51MutC2Counter.md:138-145` correctly identifies `recorded == len(legs)` and that a name-keyed `wired` set/list cannot exceed ledger legs only if its construction ensures the subset relation, then `len(wired)==10` implies at least ten records. But the report states “wired ⊆ legs” and does not establish that the parsed `legs`/`wired` collections are unique sets rather than duplicate-preserving lists. With duplicate ledger records, `len(wired)==10` can coexist with `recorded>10` if the parser counts duplicates and wiring emits one item per occurrence; or, if it deduplicates, duplicate rows may break the claimed cardinality relation. The nearest route is one duplicated already-wired base leg and both counters reject it; that single route does not prove all routes, especially malformed/duplicate row representations. The report's phrase “no distinguishing tree” is an empirical bound, not a proof of equivalence absent inspection of `wiring()` cardinality behavior and a uniqueness invariant.

Evidence to inspect: `measure.py:49-118` (ledger parser and wiring result shape), `measure.py:272-275` (depth/passed), and `T51MutC2Counter.md:140-145`; the reported experiment is only `receipts/run-flip-m16try-{pristine,mutant}.txt`. Safe calibration: call M16 “redundant on the tested inputs; likely logically implied if `wired` is a duplicate-preserving subset of parsed ledger rows.” To claim equivalence, explicitly establish `len(wired) <= recorded` for every accepted syntax and test the multiplicity boundary.

## F4 — M17 is correctly killed, but it is a harness/exit-contract kill

The edit changes only `measure()`'s return code (`probe.py:113-115`). On CTL_0 the mutant returns rc=0 while printing `C2_R51_PASS=false` (`receipts/run-M17_exit_always_zero-ctl0.txt:22-23`); the pre-registered D2 contract requires rc=1 plus final `PASS=false` (`T51MutC2Counter.md:14-20`), so this is a real kill of exit-code wiring. D1's e2e selftest also explicitly asserts rc=1 (`measure.py:283 onward`); D3 is likewise an expected failure. Do not characterize it as a predicate-clause kill: the printed predicate remains false, and the experiment measures detector/harness integrity, as the report notes (`T51MutC2Counter.md:24-25, 183-184`).

## F5 — Overclaims to avoid

1. “Each forged tree satisfies every clause except X” is not established merely by a marker or mutant PASS; preserve full flag-by-flag receipts as the proof, especially M14.
2. “Equivalent” for M16 outruns the single nearest-route probe unless parser uniqueness/cardinality is proven.
3. “No regression fixture ... per clause” is supportable for this counter's D1/D2/D3 as run, but “a one-edit weakening of any of the ten clauses ... ships undetected” (`T51MutC2Counter.md:157-160`) is too universal: tested mutants are selected single replacements; other code-level implementations of a weakening, malformed inputs, and interaction mutations are outside that matrix.
4. The synthetic all-clause pass demonstrates consistency forgery, not an independently sourced/valid candidate result; the suite is unbound and counter does not establish provenance (also evidenced by `T51W2CritC2Registration.md:13-27`).

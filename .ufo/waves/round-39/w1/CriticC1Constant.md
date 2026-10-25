# CriticC1Constant — Milestone "Constant 9" (axis: depth)

## Finding: CONFIRMED — the stripped probe kills a constant-9 guard

A guard that reports `recorded_cases=9` regardless of input **fails** the C1
predicate. Executed end-to-end through the real counter, not by inspection.

## Counterexample

Guard regex `^ *command ` (matches exactly the 9 `command -v` dependency-check
lines in `tools/mutate-and-run.sh`, none of which is a ledger line) reproduces
`recorded_cases=9 depth_score=9` on the live runner **and** still prints 9/9 on
the ledger-stripped copy — a faithful stand-in for a hard-coded constant 9.

## Evidence

Scratch lane `/tmp/tameshi-r39-CriticC1Constant/scratch-lane` (lane checkout
untouched): `tools/mutate-and-run.sh` = bytes of base rev
`50aadd1bbd94e43cd3fcfb81459414394db2dc35`; contract `no_harm_guard.depth_command_d_regex`
set to `^ *command `; committed as rev `133019a14780c311fae1e21f04e2cfc2a39a4b13`.

Command:

    python3 .ufo/evidence/round-39/guard/measure.py \
      --lane /tmp/tameshi-r39-CriticC1Constant/scratch-lane \
      --rev 133019a14780c311fae1e21f04e2cfc2a39a4b13

Output (exit 1):

    C1_R39: guard_absent=0 live_guard=9/9 live_d=9/9 strip_guard=9/9 strip_d=0/0
    live_agree=1 stripped_agree=0 r38_regex_hits=0 mismatches=1
    rev=133019a14780c311fae1e21f04e2cfc2a39a4b13 C1_R39_PASS=false

Mechanism: `measure.py:37` `strip_ledger` drops only lines matching
`COMMAND_D` (`^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+`), so `strip_d=0/0` while the
constant guard still counts 9 → `stripped_agree=0` (`measure.py:98-101`) →
`ok` false (`measure.py:102`).

Base-rev control (run in the live lane, no mutation):

    python3 .ufo/evidence/round-39/guard/measure.py --lane LANE --rev 50aadd1...
    → guard_absent=1 live_d=9/9 strip_d=0/0 … C1_R39_PASS=false  (exit 1)

## Impacted axes

- **C1 calibration**: the `stripped_agree` conjunct is load-bearing — a guard
  tuned to the live ledger (9 matches) passes `live_agree` but is caught on the
  stripped copy. The predicate is not vulnerable to constant-9 saturation.
- **Depth (C2)**: unaffected; no interaction observed.

## Smallest safe correction

None needed — predicate already rejects this attack. If a proposal hard-codes
9 (or any regex matching only non-ledger lines, e.g. `^ *command `), the
canonical judge MUST reject it: `stripped_agree=0`.

Note: `strip_ledger` removes every `COMMAND_D` line unconditionally, so a guard
regex that matches only *ledger* lines scores 0/0 on stripped and fails
`live_agree` instead — the constant-9 class is the only near-miss, and it dies
on the stripped side as demonstrated.

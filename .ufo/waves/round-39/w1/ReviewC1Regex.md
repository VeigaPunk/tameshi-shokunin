# ReviewC1Regex — round-39 C1: non-D regexes reach live_agree=1 + stripped_agree=1 (PASS)

## Finding (HIGH — predicate vacuity confirmed)

**Yes — multiple regexes other than command D still produce `live_agree=1`,
`stripped_agree=1`, `mismatches=0`, and `C1_R39_PASS=true` on the current
runner.** The predicate (contract.json:13) is implemented as pure count-tuple
equality: `live_agree`/`stripped_agree` compare `(len(findall), min(10,n))`
(measure.py:31-33, 97-102). Match identity, line anchoring, and semantic scope
are never checked. Because `strip_ledger` (measure.py:36-38) only deletes lines
matching `COMMAND_D.match`, any regex whose 9 hits all sit inside those 9
ledger rows agrees on both runners.

## Confirmed counterexamples (runner = `git show HEAD:tools/mutate-and-run.sh`, HEAD=233077f)

End-to-end runs of the **unmodified** `guard/measure.py` (`main()` executed with
`git_show` monkeypatched to serve HEAD bytes + a contract whose
`no_harm_guard.depth_command_d_regex` was swapped; no lane file touched):

| regex | live | strip | result |
|---|---|---|---|
| ` %\)` (4 chars — matches the ` %)` score column, not the row structure) | 9/9 | 0/0 | **C1_R39_PASS=true** |
| `\d+ %\)` (percent column) | 9/9 | 0/0 | **C1_R39_PASS=true** |
| `^#   \S+-\S+\s+\S+\s+\d+/\d+` (any tool prefix — accepts `python-foo`, `ruby-x` rows command D rejects) | 9/9 | 0/0 | **C1_R39_PASS=true** |
| `^#   \S+\s+\S+\s+\d+/\d+` (no hyphenated name required) | 9/9 | 0/0 | **C1_R39_PASS=true** |

Actual emitted output for the first three (identical to a deciding run's form):

```
C1_R39: guard_absent=0 live_guard=9/9 live_d=9/9 strip_guard=0/0 strip_d=0/0 live_agree=1 stripped_agree=1 r38_regex_hits=0 mismatches=0 rev=SIM C1_R39_PASS=true
```

`r38_regex_hits` stays 0 because it is counted from the runner by the separate
`R38_VACUOUS` pattern (measure.py:18,72) — it cannot veto the guard choice.

## Boundary check (predicate is underdetermined, not vacuous for all patterns)

- ` %` → live=154, strip=145 → fails (hits outside ledger rows).
- `/\d+` → live=31/10, strip=22/10 → fails (matches path/ratio fragments everywhere).
- `^\s*leg` → live=0 → fails (already covered by CriticC1Vacuous; consistent).
- So agreement requires total-hits-inside-D-lines == 9. ` %\)` meets this only
  by accident of the runner's current bytes — a single ` %)` added to a
  non-ledger comment line silently breaks it.

## Defect mechanism

`counts()` (measure.py:31-33) reduces a regex to `(n, min(10,n))`. The contract
summary claims the guard "agrees with canonical SCORECARD command D", but the
verified property is *numerosity on one runner pair*, not *is command D* or
even *matches the same lines*. Concretely, ` %\)`'s 9 hits are inside the
ledger rows but the regex knows nothing about `#`, `js|bash`, the path field,
or line starts. Likewise `^#   \S+-...` is strictly weaker than D (admits any
tool-name prefix) yet indistinguishable to the predicate.

## Impact

- `C1_R39_PASS=true` does not certify that the round-39 depth guard is, or even
  line-anchors like, command D. At frozen HEAD the contract does pin the real
  D pattern (contract.json:35), so the current after_target is legitimately
  met — the vacuity means PASS is *necessary-but-not-sufficient evidence* for
  the claim's prose. The letter of the predicate is satisfied by design
  ("recorded_cases and depth_score equal"); the prose overclaims "agrees with
  command D".
- No `min(10,n)` saturation exploit is live today (live_d=9 < 10; a saturating
  regex would need ≥10 hits yet equal `n`, which saturation cannot mask at n=9).

## Residual risk

Low for the deciding run (regex is frozen to real D in contract.json at HEAD).
The finding documents that the predicate formalizes agreement as count equality
only — a lane whose contract named ` %\)` would still pass. Not a blocker for
C1_R39_PASS at this REV.

## Verification gaps / method

- End-to-end PASS lines were produced by executing `measure.main()` with
  `git_show` swapped for HEAD bytes — identical code path, simulated REV. A
  real `git show REV:` run with a swapped contract was not performed because
  the contract is frozen and lane edits are out of bounds; the simulation is
  byte-identical (runner = `git show HEAD:tools/mutate-and-run.sh`).
- No lane checkout mutation; scratch at /tmp/tameshi-r39-ReviewC1Regex/.
- No tool installs performed.

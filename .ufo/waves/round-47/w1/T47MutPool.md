# T47MutPool — mutation audit of the C2 pool counter (`pool.py` --selftest and measure())

Seat: T47MutPool (leaf, no subagents). Lane: tameshi. Freeze audited: `9acfbe21435e1976636a276448dee1d5e7155915`.
Target under audit: `.ufo/evidence/round-47/hardening/pool.py` (sha256 `7ea9ab1e2bcf0b15df7dc4e8f7ac5b91a5446c899623a5aeefba815fa40e1904`) against its frozen pool `.ufo/evidence/round-47/hardening/pool.json` (sha256 `b4f0d0758bfc3e8a8057b4e80a3b038ea228c0879fdfaf4a4f669b8c63af4483`).

## Method

All work in a scratch clone (`git clone --no-hardlinks` of the lane → `/var/tmp/tameshi-r47-T47MutPool/lane`, checked out at the freeze; `git rev-parse --show-toplevel` verified). For each rule below, ONE minimal byte-level mutation was applied to the clone's `pool.py`, `--selftest` was run, the mutated bytes were committed in the clone with a throwaway identity (`T47MutPool <t47mutpool@scratch.invalid>`), and — where the selftest was blind — a real `--targets base` full-pool run was executed against the probe commit (`--rev <sha>`), one sweep at a time per the orchestrator's /tmp-and-load directive. The lane checkout was never written (this report file excepted); no git state command ever ran in the lane. 18 probes + 1 pristine baseline + 2 CTL_E repro runs (74 s). Tooling authorization: nothing installed (python3 + git only).

Pristine baseline reproduced in the clone (`--targets base --rev 9acfbe…`): `killed=122 applicable=183 neutral_killed=0 pristine=2 C2_R47_PASS=false`, GROUP lines `coverage killed=64 … crashed=8` / `freshness killed=58 … crashed=4` — byte-consistent with the frozen receipt `.ufo/evidence/round-47/before/pool-base.stdout`. Pristine `--selftest`: `cases=14 failed=0`, exit 0.

## Results (18 mutants)

Verdicts: **killed** = a bounded detector fails (named case / verdict change / control flip); **SURVIVED** = no detector in the assigned bound sees it (coverage finding).

| # | Rule probed | Mutation (one site) | --selftest (14 cases) | Real run (--targets base, full pool) | Verdict |
|---|---|---|---|---|---|
| P01 | exclusion regex | `^(selftest\|main\|…)` → drop `selftest\|` | **FAIL P01, FAIL P09** (`selftest:cmp:0` enumerated; `selftest` mutable) | — | killed by selftest |
| P02 | cmp map `Is` entry | `ast.Is: ast.IsNot` → `ast.Is: ast.Is` | blind (VERDICT: PASS) | killed 122→**119** (−3 = exactly the 3 baseline-killed `Is` sites; `survived` +3) | killed by run |
| P03 | cmp map `In` entry | `ast.In: ast.NotIn` → `ast.In: ast.In` | blind | killed →**116** (−6 = the 6 baseline-killed `In` sites) | killed by run |
| P04 | `int` inverse | `+ 1` → `- 1` | **FAIL P06_int_bump** | — | killed by selftest |
| P05 | `bool` inverse | `Or() if …And() else And()` → reversed | **FAIL P04_bool_swap** | — | killed by selftest |
| P06 | `const` inverse | `= not node.value` → `= node.value` | blind | killed →**109** (−13 = exactly the 13 baseline const kills; coverage crashed 8→5) | killed by run |
| P07 | `not` deletion | `replace_node(tree, node, node.operand)` → `pass` | **FAIL P05_not_deleted** | — | killed by selftest |
| P08 | commute inverse map | `COMMUTE` `ast.Lt: ast.Gt` → `ast.Lt: ast.Lt` | blind | `NEUTRAL freshness/grade:commute:3 killed`, `neutral_killed=1` (Lt commute is genuinely behaviour-changing) | killed by run |
| P09 | ordinal addressing | delete `counts['cmp'] += 1` (all cmp ordinals collapse to 0) | blind (P03/P08 use ordinal 0; P08's `cmp:99` still None) | killed →**89** (−33), `inapplicable=15+28` (pinned `:cmp:1+` ids never yielded) | killed by run |
| P10 | commute purity filter | `pure(left) and pure(comparators[0])` → `(… or …)` | blind | **byte-identical to baseline** (killed=122, neutral_killed=0) | **SURVIVED** |
| P11 | neutral accounting gate | drop `and neutral_bad == 0` from `passed` | blind | base identical (false via killed<150); **CTL_E repro below flips false→true** | killed by run (CTL_E) |
| P12 | named-FAIL kill rule | `if p.returncode != 0 and named:` → `if named:` | blind (P11's toy exits 1) | `--try` toy (prints `FAIL r`, exits 0): pristine `MUT git:cmp:0 crashed` → mutant `MUT git:cmp:0 killed` | killed by --try probe |
| P13 | crashed vs timeout | `TIMEOUT = 90` → `TIMEOUT = 0` | **FAIL P10/P11/P12 + P14/P15 reclassified `timeout`** (5 cases) | — | killed by selftest |
| P14 | pristine requirement | `pr = int(state == 'pass')` → `pr = 1` | blind | byte-identical to baseline (pristine passes at base) | **SURVIVED** |
| P15 | pool pin | `POOL_SHA256` last hex char 3→4 | blind | `pool_pin=0` → false | killed by run |
| P16 | TARGET_KILLED comparison | `TARGET_KILLED = 150` → `100` | blind | **`C2_R47_PASS=true` on the do-nothing baseline** (killed=122 ≥ 100), exit 0 — flips frozen control CTL_G to pass | killed by run at base; see hazard note |
| P17 | self-pin strength | `self_pin = int(blob is not None and sha(blob)==sha(me))` → `int(blob is not None)` | blind | run against `--rev 9acfbe` (blob = pristine ≠ running mutant bytes): honest 0, mutant prints **`self_pin=1`** | killed by run |
| P18 | equivalence guard | `return a == b and '_PASS=' in a[1]` → `return a == b` | blind | base: n/a — equivalence is computed only under `--targets v2`. Unit: `stdout_equal((1,'boom'),(1,'boom'))` pristine **False** → mutant **True** | **SURVIVED at base** |

### CTL_E repro for P11 (the decisive scenario)

Fixture built exactly like the frozen control harness (v2 counters at the round-47 paths, selftest pins the AST of the rule code with a named `FAIL PIN_ast_of_rule_code` line), committed in scratch clones; identical fixture, only `pool.py` differs:

```
CTL_E [pristine pool.py]    rc=1  C2_R47: self_pin=1 pool_pin=1 targets=v2 killed=183 applicable=183
                                  neutral_killed=14 pristine=2 equivalence=1 target=150 … C2_R47_PASS=false
CTL_E [P11-mutant pool.py]  rc=0  C2_R47: … killed=183 … neutral_killed=14 pristine=2 equivalence=1
                                  target=150 … C2_R47_PASS=true
```

Matches the frozen receipt `control/controls-at-freeze.stdout` line `CTL_E_selftest_pins_rule_ast rc=1 … C2_R47_PASS=false` under the pristine counter and inverts it under the mutant: with the neutral gate dropped, the printed `neutral_killed=14` no longer gates anything. The neutral requirement is enforced in exactly one place.

## Required question: does an AST-different, behaviour-equal rewrite of a RULE function turn pool addresses `inapplicable`?

**No — a behaviour-equal local rewrite does not.** Renaming the local `rid`→`rowid` throughout `parse_rows` in the round-46 freshness counter and scoring via `--try --group freshness --ids parse_rows:cmp:0,parse_rows:not:0,parse_rows:int:0`:

```
PRISTINE pass
MUT parse_rows:not:0 killed
MUT parse_rows:cmp:0 killed
MUT parse_rows:int:0 killed
```

Addresses are structural (function qualname + kind + ordinal in `ast.walk` order); a rename changes neither node kinds nor walk order, so every address still resolves and the same mutants are killed. What DOES turn addresses `inapplicable` is changing the qualname: `parse_rows`→`parse_rows_renamed` gives `PRISTINE crashed` and `inapplicable` for all its ids. The residual risk is ordinal shift, not inapplicability: a rewrite that adds or removes a same-kind site before a pinned ordinal silently re-points the address to a different node (the P09 probe demonstrates the mechanism from the other side: 43 pinned ids became never-yielded, 33 kills lost).

## Findings

1. **`pool.py`'s own `--selftest` never exercises `measure()`.** All 14 cases cover enumeration, the five application kinds, address miss, exclusion, and the kill-rule toys; none covers the gates (self-pin, pool-pin, pristine, equivalence, neutral accounting, TARGET_KILLED). Every gate defect above was invisible to `--selftest` by construction.
2. **Survivors (coverage findings; no contract change proposed).**
   - P10 (purity `or`): invisible at base and at v2 (v2 rule code == round-46 rule code; no comparison in it has exactly-one-pure operands, so ordinals don't shift). It would corrupt only a future `--build-pool` (impure commutes labelled `neutral`). Killing case as code: `sites_of` with `or` yields e.g. `'x' in row('k')` as a commute site; the frozen pool simply contains none.
   - P14 (pristine `pr=1`): no detector in the frozen set isolates the pristine gate — CTL_F (always-fail) also trips the neutral gate (`neutral_killed=14`), so dropping/forcing `pr` alone changes no verdict anywhere. The gate is defence-in-depth that is currently redundant given the killed+neutral gates, because any pristine selftest failure propagates to every mutant (they run the same selftest).
   - P18 at base: `stdout_equal`'s `_PASS=` guard is only reachable under `--targets v2`; at base the equivalence branch is skipped entirely, so the two-identical-failures hazard has no base detector.
3. **Unpinned-constant hazard (P16).** `TARGET_KILLED = 150` is a bare constant with no cross-check; lowering it below the true kill count prints `C2_R47_PASS=true` on the do-nothing baseline (CTL_G must be false). At a v2 deciding run the flip would be invisible to the pass mechanics — the only trace is the `target=100` field in the verdict line, i.e. detection relies on receipt review against the contract's 150.
4. **Kill rule (P12).** The exit-nonzero half of "killed iff exits nonzero AND prints `FAIL `" lives in one conjunct; dropping it makes an exit-0 `FAIL`-printing selftest count as a kill (demonstrated through the sanctioned `--try` entry point, no re-plumbing).
5. **Timeout rule (P13 + [INFERENCE]).** The timeout path is reachable and correctly non-kill (toy cases reclassify to `timeout` under `TIMEOUT = 0`); the 90 s boundary itself is untested. A handler returning `'killed'` on `TimeoutExpired` would be invisible at the default 90 s because no real selftest approaches it — reasoned, not run (a run would need a ≥90 s toy).
6. **What held up well.** The five operator inverses (P04, P05, P07 selftest-killed; P02, P03, P06, P08 run-killed with deltas matching the per-site baseline attribution exactly), the exclusion regex, ordinal addressing, the pool pin, the self-pin, and the neutral gate (via CTL_E) all have live detectors. The counter is not stale: 15 of 18 single-site defects are caught by the bounded battery (selftest + one base run + CTL_E), and the two v2-only surfaces (equivalence, TARGET_KILLED-at-v2) are exactly where the survivors live.

## Restoration evidence

- Clone `git status --porcelain` empty; HEAD = `9acfbe21435e1976636a276448dee1d5e7155915`; `pool.py` sha256 `7ea9ab1e2bcf0b15df7dc4e8f7ac5b91a5446c899623a5aeefba815fa40e1904` after every probe (printed per step in the harness log; `restored … (pristine=True)` and `final tree sha=… pristine=True`).
- Probe commits were made only in the scratch clone and the branch was reset to the freeze afterwards (commits orphaned); the lane checkout, its jj state and its Git index were never touched. Scratch dir `/var/tmp/tameshi-r47-T47MutPool/` deleted after this report.
- No tools installed or upgraded (pacman untouched).

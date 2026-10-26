# T47RevC2Predicate — C2 claim = predicate = label

Seat: reviewer (leaf). Rev reviewed: `9acfbe21435e1976636a276448dee1d5e7155915` (freeze), base
`0b5b7cd2b2c15d23086e811a0f0348d84261277b`, data rev `ea25e0224fc81060414b27301c27bd1344669165`.
Contract `.ufo/evidence/round-47/contract.json` read, never edited.
Scratch `/tmp/tameshi-r47-T47RevC2Predicate/`. Read-only on the lane except this report (one
self-inflicted `__pycache__`, removed — §9).

Verdict in one line: **the C2 statement, the counter's docstring predicate and the printed label are
the same statement; the baseline 122/183 is real and reproduces exactly; the 150 target is sized for
one round (20 of the 28 needed kills demonstrated in ~110 lines, ceiling 156 without any PATH stub
and 171 with the brief's stub method); no pool mutant is plainly equivalent; the one real defect is
that `equivalence=1` is vacuous at `ea25e` and cannot mean what its name suggests (F1).**

## 1. Side by side

Contract `claims.C2.statement` (verbatim, abridged to the predicate clauses):

> At REV the v2 counters `.ufo/evidence/round-47/hardening/{freshness,coverage}-counter.py` pass
> their own `--selftest` (exit 0, `VERDICT: PASS`, no `FAIL` line), kill at least 150 of the 183 real
> pool mutants (a mutant is killed only when the selftest exits nonzero AND prints a line starting
> `FAIL`; a crash, a timeout and an inapplicable address are not kills), kill none of the 14 neutral
> mutants, and print byte-identical stdout (with a verdict line) to the round-46 hardened counters
> over the round-45 data revision `ea25e0224fc81060414b27301c27bd1344669165`.

`claims.C2.target`:

> `C2_R47_PASS=true: self_pin=1 pool_pin=1 killed>=150 neutral_killed=0 pristine=2 equivalence=1`

`claims.C2.kill_rule`:

> killed < 150, any neutral killed, a failing pristine selftest or equivalence=0 = honest miss; no
> pool mutant is removed, relabelled neutral or relaxed after any seat has scored

`pool.py` docstring (`:3-29`):

> Frozen predicate (the same sentence in the contract, here and in the receipt label):
> `C2_R47_PASS=true` iff `self_pin=1`, `pool_pin=1`, for BOTH targets (freshness, coverage) the
> pristine selftest of the target passes (exit 0, `VERDICT: PASS`, no `FAIL` line), the neutral
> mutants all survive (`neutral_killed=0`), the v2 target prints byte-identical stdout to the
> round-46 hardened counter over the round-45 data revision (`equivalence=1`), and the pool's killed
> total over both targets is `>= TARGET_KILLED`.

Printed label (`pool.py:290-293`), measured at the freeze (`--targets base`, my probe):

```
C2_R47: self_pin=1 pool_pin=1 targets=base killed=122 applicable=183 neutral_killed=0 pristine=2 equivalence=na target=150 rev=9acfbe21435e1976636a276448dee1d5e7155915 C2_R47_PASS=false
```

Same statement? **Yes.** Every field of the target string is printed (`self_pin`, `pool_pin`,
`killed`, `neutral_killed`, `pristine`, `equivalence`, plus `target`, `targets`, `applicable`,
`rev`). `pristine=2` is the two targets; `equivalence=na` only in the control mode. Deltas found:

| # | Where | Delta | Direction |
|---|---|---|---|
| D1 | docstring "byte-identical stdout" vs `stdout_equal` | code compares the `(exit, stdout)` tuple | code **stricter** than docstring text |
| D2 | docstring "the neutral mutants **all survive** (`neutral_killed=0`)" | a neutral that `crashed`/`timeout`/`inapplicable` also leaves `neutral_killed=0` | docstring **looser** than the code; contract's "kill none" matches the code |
| D3 | contract "with a verdict line" | a **failing** verdict line (`..._PASS=false`) satisfies `'_PASS=' in stdout` | see **F1** — this is the one that matters |
| D4 | contract `surface` names the **round-46** counters; the statement names the **round-47 v2** counters | `surface`=what is measured at freeze (before), `statement`=deciding surface; `before_state` resolves it | wording only |
| D5 | target is a **total** ≥150 over both groups | no per-group floor; 90+60 would pass | by design; per-group `GROUP` lines expose it |
| D6 | "rule code" regex `^(selftest\|main\|extra_\w+\|_x\w+)$` | `check()` — whose own docstring says "Seat helper (**never a measurement**)" — is counted as rule code; 9 of the 183 mutants live there | pool composition, not a mis-statement |

Universal words: "at least 150 of the **183**" and "none of the **14**" are enumerated and
reproducible (`--build-pool` at `base_rev` reproduces `pool.json` byte-equivalently: same
`base_sha256`, `coverage` 86 sites / `freshness` 111 sites, identical `id` lists **and order**,
identical `kind`/`neutral`/`desc`). "a crash, a timeout and an inapplicable address are not kills" is
implemented exactly (`judge`/`run_selftest`: `killed` only on `returncode != 0` **and** a stdout line
starting `FAIL `). No over-reach found in the counting vocabulary.

## 2. Baseline: 122 of 183 is what `--targets base` prints

`before/pool-base.stdout` (freeze, `--targets base`, exit 1):

```
GROUP coverage: pool=82 killed=64 survived=10 crashed=8 timeout=0 inapplicable=0 neutral=4 neutral_killed=0 pristine=1
GROUP freshness: pool=101 killed=58 survived=39 crashed=4 timeout=0 inapplicable=0 neutral=10 neutral_killed=0 pristine=1
C2_R47: ... targets=base killed=122 applicable=183 neutral_killed=0 pristine=2 equivalence=na target=150 ... C2_R47_PASS=false
```

122 = 64 + 58 ✔; 183 real = 82 + 101 ✔; 14 neutral = 4 + 10 ✔; `applicable=183` (0 inapplicable) ✔.
`pool.json` sha256 = `b4f0d0758bfc…af4483` = the contract's `pool_sha256` ✔ (recomputed).

**Reproduced independently** as a probe (`--targets base --rev 9acfbe…`, `TMPDIR` on my scratch dir):
identical `GROUP` and `C2_R47` lines, exit 1, 46.8 s wall. The surface is genuinely unmoved at base:
`killed=122 < 150`, `C2_R47_PASS=false` ✔.

## 3. Is `killed >= 150 of 183` sized for one round?

Baseline decomposition (receipt, counts cross-checked against `pool.json`):

| group | real | killed | survived | crashed | neutral |
|---|---|---|---|---|---|
| coverage | 82 | 64 | 10 (`entry_ok` 5, `measure` 5) | 8 (`Tree.read` 1, `entry_ok` 3, `gt_rows` 3, `measure` 1) | 4 |
| freshness | 101 | 58 | 39 (`check` 9, `extract` 2, `grade` 3, `live` 13, `measure` 5, `parse_rows` 4, `words` 3) | 4 (`parse_rows` 2, `review_sets` 2) | 10 |
| **total** | **183** | **122** | **49** | **12** | **14** |

Survivors + crashes = 61 as the item states; **needed = 28 more kills**.

**No pool mutant is plainly equivalent.** I read every survivor's mutated expression against its
operand domain; each differs on at least one input. Eight are *boundary-only* (they differ at exactly
one argument value, not semantically): `grade:cmp:11` (n==25), `grade:cmp:9`,`grade:int:0` (shared==2),
`words:cmp:0`,`words:int:0` (4-letter token), `measure:cmp:4` (fresh==50), `entry_ok:cmp:0`,
`entry_ok:int:0` (len(lines)==3), `entry_ok:int:3` (6 tokens), `entry_ok:int:4` (26 tokens). All the
boundary ones except `measure:cmp:4` were killed in the PoC below; `measure:cmp:4` was killed by the
floor fixture. The remaining survivors differ on ordinary inputs. **Consequence: the contract's
"no mutant removed after a seat scored" rule is untriggered — nothing needs removing, and 150 is not
being propped up by padding.**

**Structural dead weight: the 12 crashes are unreachable by the sanctioned assembly path** (F2, §5),
so the true ceiling is **171 of 183**, not 183.

**Reachability, measured (not asserted)** — three scratch addition files, ~110 lines total:

| block | sites | status |
|---|---|---|
| `words` 3, `grade` 3, `parse_rows` 4 (freshness) | 10 | **killed** — direct call of the pure rule with a crafted table / 6- and 25-token quotes / shared==2 |
| `entry_ok` 5 (coverage) | 5 | **killed** — 3-line entry (full `(False,'no located quote')` tuple), 6-token quote, 26-token quote, curly-quote (`q.group(3)` raises → caught → `FAIL`) |
| `measure` 5 (freshness) | 5 | **killed** — reuse `_xHardMeasure_fixture/case`: a *passing* fixture at the floor (fresh==50, `pin_self=True`), an empty-population fixture, and a stray-`INVALID`-line assertion |
| `measure` 5 (coverage) | 5 | reachable — `_xHardCover1_last_line` / `_xHardCover2_build` exist and are `_x`-excluded from the pool (never mutated) |
| `check` 9 (freshness) | 9 | reachable — one temp lane repo (`_xHardMeasure_build` builds it) + fragments; sketched, not demonstrated by me |
| `live` 13, `extract` 2 | 15 | reachable only with a PATH stub (`curl` / `pdftotext`); this is exactly what `hard-brief.md` §2 prescribes |

Measured sweep on the assembled PoCs (`--try` without `--ids`, 279 s wall, both files):
`poc-fresh.py` killed **68/101** (58→68, neutrals 10 survive, crashed set unchanged 4);
`poc-cov.py` killed **69/82** (64→69, neutrals 4 survive, crashed set unchanged 8). Targeted re-run of
`poc-fresh2.py` (adds the measure fixture) killed **all 5** `measure` survivors → **20 proven kills,
zero regressions** (no baseline kill flipped to `crashed`).

Arithmetic: 122 + 20 = 142 with the proofs in hand; **8 more needed**, with 29 remaining sites
(9 `check`, 5 coverage-`measure`, 15 stub-only). Without any stub the ceiling is 122+34 = **156
(slack 6)**; with the brief's stub method the ceiling is **171 (slack 21)**.

**Judgment (recommendation): sized for one round — yes, not generously.** 28 kills against a
reachable ceiling of 156 (no stubs) / 171 (stubs) means the round can miss 6–21 of the 49 survivors.
It is *not* reachable by "adding a handful of hash-free assertions": the two stub blocks and the
coverage-`measure` block must actually land, and the 12 crashes must be written off, not chased.

## 4. Assembler invariance — verified

- `assemble.py --group {freshness,coverage} --add <dummy extra_>` → output selftest `VERDICT: PASS`
  (35 / 21 cases).
- `pool.py --enumerate` on the assembled files vs `pool.json`: **freshness 111 ids, coverage 86 ids,
  identical id list, identical order, identical `kind`/`neutral`/`desc`, 0 line shifts**; the dummy
  `extra_*` is excluded by `EXCLUDE` and adds no site. Pool addresses therefore survive assembly
  untouched.
- `diff` assembled vs the round-46 source: exactly **one removed line** (`SELF_PATH = '…round-46…'`),
  **3 added call lines** immediately before the tally print, **one inserted block** before
  `def main():`. The rule code is byte-identical, so per-function `ast.walk` ordinals cannot move.

## 5. Findings by severity

### F1 — MEDIUM: `equivalence=1` is vacuous and its docstring intent is not implemented
`stdout_equal(a, b)` returns `a == b and '_PASS=' in a[1]`. At the frozen data revision `ea25e…`,
`SELF_PATH` **does not exist for any of the four counters** (`git cat-file -e ea25e:<path>` →
ABSENT for `.ufo/evidence/round-46/hardening/{freshness,coverage}-counter.py` and for both round-47
paths). Both runs therefore necessarily print `self_pin=0` and a `..._PASS=false` verdict line, which
contains `_PASS=` — so the guard accepts **two identical failures**, exactly what the function's own
docstring says "prove nothing". Measured (base vs assembled-with-dummy, both at `ea25e…`):
`exit=1` both, stdout `BYTE_IDENTICAL` for both pairs, e.g.
`C1_R45: self_pin=0 population=73 … fresh=71 score=9 target=50 rev=ea25e… C1_R45_PASS=false`.
So `equivalence=1` is guaranteed for **any** v2 that leaves the `measure()` print path intact; it
detects only crashes/format changes, and it never demonstrates behavioural equivalence in the
*passing* regime that the field name implies. The label is honest about *what it measured*; the
contract's phrase "byte-identical stdout (with a verdict line)" is satisfied literally, but a reader
will over-read it. Advisory (no edit by me, no pool/contract change): compare at a revision where both
`SELF_PATH`s resolve, or require `_PASS=true` in the compared stdout, or rename the field.

### F2 — MEDIUM: the 12 crashed mutants are structurally unreachable under the assembler
All 12 crashes occur **in the parent selftest process, in round-46 fixture construction**, and
`assemble.py` inserts the added calls *after* the round-46 calls (`src.replace(tally_old, calls +
tally_old)`):
- freshness: `selftest` → `population`/`parse_rows` (traceback `c.py:309 → :86`, `:308 → :82`) and
  `review_sets` (`c.py:319 → :187`);
- coverage: `selftest → build` (`c.py:174 → :163`) for `Tree.read`, `entry_ok`, `gt_rows`, `measure`.
Because the process dies before any added case runs, the brief's "wrap the call and print `FAIL`"
cannot convert them. Effect: ceiling 171/183; 150 still leaves 21. The definition of v2 ("round-46
counters + new selftest additions") does not say whether hand-patching those fixture bodies is
permitted; today no seat needs to, but that ambiguity should be settled before one tries.

### F3 — LOW: the neutral gate is one-sided
`neutral_killed` counts only `killed`. A neutral mutant that `crashed`, `timeout`ed or became
`inapplicable` still yields `neutral_killed=0` and passes. The contract's "kill none" matches the
code; the docstring's "all survive" does not. Hedges the claim against a selftest that aborts on
AST-different-but-equal code for non-semantic reasons.

### F4 — LOW/INFO: `check()` is pool "rule code" although no measurement path calls it
`EXCLUDE` keeps `check` in the pool (9 of 183 sites), while the counter's own docstring calls it
"Seat helper (never a measurement)". They are killable by direct call (same pattern as the proven
`words`/`grade`/`parse_rows` kills), so this is composition, not a defect — but 5 % of the pool
denominator sits in a function the counter never measures.

### F5 — INFO: `pool.py` selftest passes, labels skip P13
`--selftest` → `C2_R47_SELFTEST: cases=14 failed=0`, `VERDICT: PASS` (P01–P12, P14, P15; no P13).
Cosmetic only.

### F6 — INFO: label carries four fields beyond the target string
`targets`, `applicable`, `target`, `rev` are extra and honest; `applicable=183` independently confirms
that no address went inapplicable.

## 6. Operability of the deciding run (residual risk)

- **`TMPDIR` is not pinned**; `run_selftest` creates one temp dir per mutant (197/sweep). Three C1
  seats recorded `/tmp` at 100 % today. A full mutant whose fixtures need scratch then reports
  `crashed` (not killed) and silently lowers the count — with only 6–21 kills of slack that can flip
  the verdict. Recommendation: run the deciding sweep with `TMPDIR` on a roomy filesystem (my
  reproduction did, and reproduced 122/183 exactly). There is no per-mutant repeat, so a one-off
  crash is invisible.
- `/tmp` scratch aside, the sweep is cheap and stable: 46.8 s (`--targets base`, 197 mutants, 12
  workers) and 279 s for two serial `--try` sweeps. `TIMEOUT=90` per mutant was never approached.

## 7. Verification gaps (what I did **not** prove)

- `live` 13 and `extract` 2 kills via PATH stubs: method read from `hard-brief.md` §2, not executed.
- `check` 9 and coverage-`measure` 5 kills: poked at the rule (see §3) and the fixtures exist, but no
  kill byte was produced by me.
- Neutral-mutant behaviour under a *fixed* v2 counter: only the baseline (all 14 survive) and my PoC
  (all 14 survive, both groups) were observed.
- The deciding `--targets v2` path: at the freeze the v2 counters do not exist
  (`before/pool-v2-at-freeze.stdout`: `target absent .ufo/evidence/round-47/hardening/coverage-counter.py`),
  which is correct pre-data; I never ran a v2 verdict.

## 8. Commands run (exit codes)

```
# pool derivation + baseline
python3 <lane>/.ufo/evidence/round-47/hardening/pool.py --lane <lane> --rev 0b5b7cd2… --build-pool   # 0, identical to pool.json
python3 <lane>/.ufo/evidence/round-47/hardening/pool.py --lane <lane> --rev 9acfbe21… --targets base # 1, killed=122 == receipt
python3 <lane>/.ufo/evidence/round-47/hardening/pool.py --selftest                                  # 0, VERDICT: PASS (14 cases)
# assembler invariance
python3 <lane>/.ufo/evidence/round-47/hardening/assemble.py --group freshness --add <dummy> --out …  # 0
python3 …/pool.py --enumerate <assembled>                                                            # 0, ids == pool.json (111/86)
diff -u <round-46>/freshness-counter.py <assembled>                                                  # 1 (1 removed line, 3+1 added)
# kill reachability (scratch only)
python3 <poc-fresh>.py --selftest                                                                    # 0, cases=45 failed=0, VERDICT: PASS
python3 <poc-cov>.py  --selftest                                                                     # 0, cases=24 failed=0, VERDICT: PASS
python3 …/pool.py --try <poc-fresh> --group freshness --ids words:bool:0,…,grade:int:0               # 0, 10/10 killed
python3 …/pool.py --try <poc-cov>   --group coverage  --ids entry_ok:cmp:0,…,entry_ok:int:7           # 0, 5/5 killed
python3 …/pool.py --try <poc-fresh2> --group freshness --ids measure:cmp:4,…,measure:int:5            # 0, 5/5 killed
python3 …/pool.py --try <poc-fresh> --group freshness   (no --ids)                                   # 0, killed 68, neutrals 10 survive
python3 …/pool.py --try <poc-cov>   --group coverage    (no --ids)                                   # 0, killed 69, neutrals 4 survive
git -C <lane> cat-file -e ea25e…:<each of the four counter paths>                                    # 1 (ABSENT) ×4
```

## 9. Hygiene, tooling, disclosures

- Nothing installed or upgraded; no pacman transaction attempted. No git/jj mutating command; the
  lane's Git index untouched (`git status --porcelain` shows only other seats' untracked wave files).
- **Disclosure:** loading `pool.py` once through `importlib` for analysis wrote
  `.ufo/evidence/round-47/hardening/__pycache__/pool.cpython-314.pyc` (module-level
  `sys.dont_write_bytecode` runs too late for the loader's write). I removed the directory; the
  hardening dir is back to `assemble.py`, `pool.json`, `pool.py`. Later analyses used
  `exec(compile(…))`, which writes nothing.
- All scratch under `/tmp/tameshi-r47-T47RevC2Predicate/` (PoC addition files, assembled counters,
  `--try` transcripts, equivalence runs, base probe).

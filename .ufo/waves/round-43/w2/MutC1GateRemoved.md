# MutC1GateRemoved — is the C1 reachability gate load-bearing?

Scope: one mutation of the C1 counter's kill gate at the assigned freeze, run entirely in
`/tmp/tameshi-r43-w2-MutC1GateRemoved-scratch/` against a `git clone --shared` of the lane.
No lane file was written except this report. The lane's own bytes were never touched; the
counter under test was extracted with `git show 3aee2c0:…`, not read from the working tree.

## Verdict

**KILLED — the gate is load-bearing, not decorative.** Replacing

```python
if mf and reachable_fails:        # .ufo/evidence/round-43/mutants/measure.py:571 @ 3aee2c0
```

with a plain `if mf:` moves `method_fold_several_returns` out of `dead_code_only` and into
`killed`, and the predicate flips:

| leg (bytes) | `mutants_killed` | `dead_code_only` | `C1_R43_PASS` | exit |
|---|---|---|---|---|
| pristine frozen counter (`0d0f81bd…`) | 5 | 1 | true | 0 |
| gate removed (`3f3ecd3f…`) | **6** | **0** | **false** | 1 |
| restored to pristine bytes (`0d0f81bd…`) | 5 | 1 | true | 0 |

The mutant's `killed` ledger gains exactly one name,
`method_fold_several_returns`, and `dead_code_names` empties. `mutants_killed=6
dead_code_only=0` is the **same line wave-1 seat MutC1F11 printed on the pre-A5 counter**, the
defect amendment A5 was written to repair (contract A5 `why`, `.ufo/evidence/round-43/contract.json`).
The gate is therefore the single line standing between the frozen rule K and the defect K was
frozen to exclude.

## 1. Setup and the mutation

```
$ git clone --shared --no-checkout /home/.../tameshi-shokunin /tmp/…-scratch/lane
$ git -C /tmp/…-scratch/lane checkout --detach 3aee2c078f8976499b587086af3577fc94dc8cf1
$ git -C /tmp/…-scratch/lane show 3aee2c0:.ufo/evidence/round-43/mutants/measure.py > counter_pristine.py
$ sha256sum counter_pristine.py
0d0f81bdbe09bb53997ade30911fc178a38de072f84aacf23c6c9c0a710e57f1   # == contract claims.C1.counter_sha256
$ cp counter_pristine.py counter_mutant.py   # then ONE edit
$ diff -u counter_pristine.py counter_mutant.py
@@ -568,7 +568,7 @@
                 runtime_error.append(name)
                 continue
             reachable_fails = [case for case in mdetail if not mdetail[case]]
-            if mf and reachable_fails:
+            if mf:
                 killed.append(name)
                 continue
```

One hunk, one conditional. The `reachable_fails` computation is left in place (now unused by the
branch) so the diff is exactly the gate's condition. Mutant bytes:
`3f3ecd3fc925c60fcf82e1933440b48b5ca3fe67e2372550eae62e4364ca6b69`
(preserved as `mutant_saved.py`; restored copy verified back to `0d0f81bd…`).

Both legs ran the assigned pair:

```
python3 <counter> --lane /tmp/…-scratch/lane --rev 3aee2c078f8976499b587086af3577fc94dc8cf1 \
                  --freeze 3aee2c078f8976499b587086af3577fc94dc8cf1
```

## 2. Assigned measurement — actual outputs

Pristine (baseline; `self_pin=1`, so these are provably the frozen bytes):

```
C1_R43: self_pin=1 tool_absent=0 tool_sha_ok=1 selftest_exit=0 fixtures_pass=12/12 run_errors=0
live_ok=3/3 live_unflagged_v4=0 live_tool_errors=0 mutants_declared=6 mutants_killed=5
dead_code_only=1 equivalent=0 not_killed=0 runtime_error=0 apply_error=0 unresolved=0
killed_names=attr_bind_several_assignments,attr_never_resolve_self,method_fold_disabled,
outflag_dests_never_recorded,outflag_no_parse_args_check
dead_code_names=method_fold_several_returns dead_code_cases=F12_method_two_returns
dead_code_arg_ok=1 kill_fixture_reachable=1 rev=3aee2c0… freeze=3aee2c0… C1_R43_PASS=true
exit=0
```

Gate removed:

```
C1_R43: self_pin=0 tool_absent=0 tool_sha_ok=1 selftest_exit=0 fixtures_pass=12/12 run_errors=0
live_ok=3/3 live_unflagged_v4=0 live_tool_errors=0 mutants_declared=6 mutants_killed=6
dead_code_only=0 equivalent=0 not_killed=0 runtime_error=0 apply_error=0 unresolved=0
killed_names=attr_bind_several_assignments,attr_never_resolve_self,method_fold_disabled,
method_fold_several_returns,outflag_dests_never_recorded,outflag_no_parse_args_check
dead_code_names= dead_code_cases= dead_code_arg_ok=0 kill_fixture_reachable=1
rev=3aee2c0… freeze=3aee2c0… C1_R43_PASS=false
exit=1
```

Restored (bytes back to `0d0f81bd…`, re-run): identical to the pristine line, `C1_R43_PASS=true`,
`exit=0`.

Every measurement field other than the mutant ledger and `self_pin` is unchanged
(`fixtures_pass=12/12`, `run_errors=0`, `live_ok=3/3`, `unresolved=0`). The battery itself was
not perturbed — only the classification branch was.

## 3. Attribution — the predicate flip is the gate, not `self_pin`

The mutant necessarily prints `self_pin=0` (its bytes differ from the pin), so a `PASS=false`
could in principle be blamed on the pin alone. Neutralising the byte self-pin in **both** copies
(`running = pin` in place of `running = sha(handle.read())`, diagnostic copies only) holds that
variable equal:

| leg | `self_pin` | `mutants_killed` | `dead_code_only` | `dead_code_arg_ok` | `C1_R43_PASS` | exit |
|---|---|---|---|---|---|---|
| pristine + pin neutralised | 1 | 5 | 1 | 1 | true | 0 |
| gate removed + pin neutralised | 1 | **6** | **0** | **0** | **false** | 1 |

With `self_pin` fixed at 1 on both sides, the predicate still flips. The four conjuncts that go
false are all gate-caused
(`measure.py:630` `len(killed)==5`, `len(dead_code_only)==1`, `len(dead_names)` membership for
`method_fold_several_returns`, `:634` `dead_arg_ok==1`); the pin is not among them.

## 4. Surgical isolation — the `--control` path is untouched

`--control` skips both new fixtures (amendment A2), so it never sees F12 and must be blind to
this mutation. It is:

```
control, pristine : fixtures_pass=10/10 mutants_declared=6 mutants_killed=4 C1_R43_CONTROL_PASS=false  exit=1
control, mutated  : fixtures_pass=10/10 mutants_declared=6 mutants_killed=4 C1_R43_CONTROL_PASS=false  exit=1
$ diff -q control_pristine.out control_mutant.out   # IDENTICAL
```

This rules out the mutation having any effect outside the measurement branch, and separately
reproduces the contract's declared do-nothing control (`mutants_killed=4`).

## 5. Freeze drift during the probe (disclosure)

While this seat ran, a new freeze **A11** (`b510ad1822cc081a47fa14e8a1d8bcc4260128fe`) landed in
the lane. The assigned revision pair above remains `3aee2c0`, and the `0d0f81bd…` pin I report is
the A10 pin, not the current one; the lane working tree now carries the A11 counter
(`b56a34d71e83937330da35024ec60a623d0b10a51652c68be07cddbe2b6d7726`), which is what A11 pins.
That is drift after this seat's extraction, not a stale read.

The gate survived A11 **byte for byte** — `git show b510ad1:….ufo/evidence/round-43/mutants/measure.py`
still has `if mf and reachable_fails:` at **line 577**, with only `sorted()` added on the
`reachable_fails` line above it. So the probe was repeated on the A11-pinned counter (same
permitted `--rev 3aee2c0`, `--freeze b510ad1`; `mutants.json` at 3aee hashes to A11's
`mutants_sha256` `b3abab06…`):

| A11 leg | `self_pin` | `mutants_killed` | `dead_code_only` | `dead_code_arg_ok` | `C1_R43_PASS` | exit |
|---|---|---|---|---|---|---|
| pristine (`b56a34d7…`) | 1 | 5 | 1 | 1 | true | 0 |
| gate removed | 0 | **6** | **0** | **0** | **false** | 1 |
| pristine + pin neutralised | 1 | 5 | 1 | 1 | true | 0 |
| gate removed + pin neutralised | 1 | **6** | **0** | **0** | **false** | 1 |

A11's new `kill_cases` field makes the defect visible as data rather than inference: in the
gate-removed run the offending entry is

```
method_fold_several_returns:
```

— an **empty** case list. The mutant enters `killed` on zero reachable failing cases; its only
failure is F12, whose `mdetail[F12]` is `True` (contains a statement after an unconditional
`return`, `measure.py:228`-block). Under the pristine gate it never reaches `killed`, and
`dead_code_cases=F12_method_two_returns` records where its divergence actually lives. The gate is
the only thing that turns that empty list into a refusal.

## 6. What this does and does not establish

Established: the `reachable_fails` conjunct at `measure.py:571` (A10) / `:577` (A11) is the sole
carrier of rule K's reachability sentence in the measurement path. Delete it and the frozen
predicate goes false for the right reason.

Not established, and recorded as coverage notes rather than findings:

1. **The rule is implemented twice.** The `--probe-mutant` path carries its own copy
   (`:513-519` at A10, `:516-521` at A11: `elif fails and reachable: killed`). A mutation of that
   copy alone cannot move `C1_R43_PASS`, because the predicate never reads probe output — so the
   probe path is a second sighting that this mutation does not reach. It survived; that is a
   coverage gap, not a contract problem.
2. **The gate's discriminating power depends on `unreachable_statements()`**
   (`:381-398` at A10, `:384-401` at A11), which flags a statement after an unconditional
   `Return`/`Raise` in the same `body` only. F12's second `return` is caught. A dedicated seat
   could next mutate that function (e.g. return `[]`) and check whether the gate degrades to
   dead weight; that is a different mutant and was not run here.

## 7. Restoration and bound compliance

- Mutant bytes preserved at `mutant_saved.py` (`3f3ecd3f…`); the working copy `counter_mutant.py`
  was restored to the frozen bytes and verified `0d0f81bdbe09bb53997ade30911fc178a38de072f84aacf23c6c9c0a710e57f1`,
  then re-run with the pristine output above.
- All writes are under `/tmp/tameshi-r43-w2-MutC1GateRemoved-scratch/` (deleted on return) and
  this report file. The lane checkout was only read (`git show`, `git ls-tree`, `sha256sum`);
  no `git add/commit/checkout/reset/…` and no mutating `jj` command was run in the lane — the
  only checkout was inside the scratch clone.
- No counter was run at `c5335c70bff750218b3a6db0a92daae76509a0de`. The counters measured were
  copies; the deciding run belongs to the L1.
- Tool installs: none (no pacman, uv, cargo or npm transaction was needed; `git` and `python3`
  were already present).

# Round 42 wave 2 — MutantAuthor (non-author mutation tester, C2 mutant_protocol)

Seat: `L1Tameshi42.MutantAuthor`. Attacked thing: `tools/write-path-census-v4.py` (sha256 `784de4c0feef3364c4444632788af7ebb57d53032b79f60cc4330c094d122fe5`, identical in lane, clone and pristine copy) against the frozen battery in `.ufo/evidence/round-42/census/measure.py` (sha256 `3c3727ec…0ff2` = contract pin). Access date 2026-10-25.

Scratch clone (KEPT): `/tmp/tameshi-r42w2-MutantAuthor-clone`, `git clone --shared` of the lane at `a21845f`; mutants.json committed there as `ae4bf4af20a65fb55e3553cb899243571e5e41ff` ("scratch: round-42 C2 mutants.json (MutantAuthor)"). No lane checkout, Git index or jj state was touched. My only lane write is this file.

## Selection rule (fixed before any run)

The rule was fixed before I scored anything. For each class, I declared one mutant that disables the step at its use site and one that weakens the first guard the v4 docstring names for that step:

- Attribute step: the guard is "exactly one distinct assigned expression" (docstring lines 17-20).
- Method step: the guard is "exactly one top-level `return`" (lines 21-23).
- Output-flag step: the guard is "`<ns>` bound to a `parse_args(...)` call" (lines 26-27).

I did not tune any mutant after seeing results. Each `find` has `str.count == 1` in the v4 bytes, each mutant parses (`ast.parse`), and each changes the bytes.

| name | class | targets (v4 path:line) | edit |
|---|---|---|---|
| attr_bind_several_assignments | attr | `ClassInfo.__init__` :131-132 | `len(vals) == 1` → `>= 1` (binds the first of several distinct assignments) |
| attr_never_resolve_self | attr | `_resolve` :207 | `if False and …` (self attributes never resolved) |
| method_fold_disabled | method | `_resolve` :196 | `value, method_env = None, None` (self-method fold off) |
| method_fold_several_returns | method | `ClassInfo.method_return` :139 | `len(returns) != 1` → `< 1` (folds the first of several top-level returns) |
| outflag_dests_never_recorded | outflag | `Module.__init__` :99 | `self.out_dests[dest] = flag` → `pass` |
| outflag_no_parse_args_check | outflag | `_out_flag` :284 | `if flag and _parse_args_ns(…):` → `if flag:` (any `<x>.<dest>` counts) |

## Findings

### F1 — scratch-clone count (falsifier run, not the measurement)

Command:

`cd /tmp/tameshi-r42w2-MutantAuthor-clone && python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-42/census/measure.py --lane /tmp/tameshi-r42w2-MutantAuthor-clone --rev HEAD --freeze 322b5cd32b4319a05340d249ae752d12a9e6b19f` (exit 1)

```
MUTANT attr_bind_several_assignments class=attr outcome=killed detail=F03_attr_ambiguous scratch=1 want 0
MUTANT attr_never_resolve_self class=attr outcome=killed detail=F01_attr_scratch scratch=0 want 1
MUTANT method_fold_disabled class=method outcome=killed detail=F01_attr_scratch scratch=0 want 1
MUTANT method_fold_several_returns class=method outcome=survived detail=
MUTANT outflag_dests_never_recorded class=outflag outcome=killed detail=F04_outflag explicit_out=0 want 1
MUTANT outflag_no_parse_args_check class=outflag outcome=survived detail=
C2_R42: self_pin=1 tool_absent=0 tool_sha256=784de4c0feef3364c4444632788af7ebb57d53032b79f60cc4330c094d122fe5 v3_sha_ok=1 v2_sha_ok=1 selftest_exit=0 fixtures_pass=10/10 run_errors=0 live_1682_ok=1 live_1685_ok=1 live_123_ok=1 live_unflagged_v3=3 live_unflagged_v4=0 live_tool_errors_v4=0 mutants_declared=6 mutants_killed=4 mutant_classes_killed=attr,method,outflag rev=ae4bf4af20a65fb55e3553cb899243571e5e41ff freeze=322b5cd32b4319a05340d249ae752d12a9e6b19f C2_R42_PASS=false
```

Every non-mutant term of the predicate holds. The mutant term fails because 4 of 6 mutants are killed, while the counter requires `killed == declared` (measure.py:455).

### F2 — detector baseline is clean (pristine v4 under the same oracle)

Command: `python3 …/census/measure.py --lane /tmp/tameshi-r42w2-MutantAuthor-clone --rev HEAD --freeze 322b5cd3… --probe-mutant /tmp/tameshi-r42w2-MutantAuthor-pristine.py`

Output: `PROBE outcome=survived detail=`

The unmutated bytes pass the whole battery, so every kill in F1 comes from the mutation, not from an existing failure. The pristine copy has the same sha256 as the lane v4 (`784de4c0…`).

### F3 — survivor `outflag_no_parse_args_check` is a killable coverage gap in BOTH oracle and selftest

- The mutant passes the tool's own `--selftest` (`WRITE_CENSUS_V4_SELFTEST: cases=15 failed=0`).
- The selftest case `output_attr_not_parse_args` (v4:610-618) registers no `add_argument`, so `out_dests` is empty. That means the case never reaches the `_parse_args_ns` check it is named for.
- Battery fixture F05 uses `--input`, which is also not an output option. No fixture registers `--out` and then reads `.out` off something that is not a parse_args namespace.

Witness file: `/tmp/tameshi-r42w2-MutantAuthor-wit/W1_outflag_non_ns_attr.py`. It registers `--out`, then writes `open(os.path.join(cfg.out, 'expected.json'), 'w')`, where `cfg.out = 'golden'`. Command: `python3 -I <tool> --file W1… --json`.

- Pristine: `scratch False, explicit_out False, unflagged True`. This is correct: the write is a hidden golden write.
- Mutant: `explicit_out True, unflagged False, resolved …'argparse --out'`. The mutant hides the write.

The fix belongs to the battery owner: one fixture of this shape kills the mutant. A surviving mutant does not license a contract change.

### F4 — survivor `method_fold_several_returns` is distinguishable only on unreachable code

- The mutant passes the selftest (`failed=0`).
- The selftest case `method_two_returns` (v4:510-526) has exactly one top-level return; the other return is nested under `if`. So the `!= 1` guard (v4:139) is not exercised by any selftest or battery input.

Witness file: `/tmp/tameshi-r42w2-MutantAuthor-wit/W2_method_dead_second_return.py`, with `return self.base` followed by an unreachable `return 'golden'`:

- Pristine: `scratch False, unflagged True`, because the method is not folded.
- Mutant: `scratch True, unflagged False`, because it folds the first return, which is mkdtemp.

The mutant is killable, but only by a fixture with dead code. On that input the mutant's answer is arguably the more correct one, because the first return is the only reachable one. I kept it under the no-tuning instruction. The reviewer seat should rule on whether it counts as an equivalent mutant; the contract's mutant_protocol has no clause excluding equivalent mutants.

### F5 — related defect in UNMUTATED v4 (method step): nested returns are invisible to the uniqueness guard

Witness file: `/tmp/tameshi-r42w2-MutantAuthor-wit/W3_method_nested_return_pristine.py`. The method is `where(real)`, containing `if real: return 'golden'` followed by top-level `return self.base` (mkdtemp). The call site writes `os.path.join(self.where(True), 'expected.json')`.

Pristine v4 output: `scratch True, explicit_out False, unflagged False, resolved …tempfile.mkdtemp()…`.

v4 folds to the top-level mkdtemp return and ignores the reachable `'golden'` return, so a golden write goes unflagged. The cause is that `method_return` counts only `method.body` top-level `Return`s (v4:138), whereas the docstring (v4:21-23) promises "exactly one top-level return". The code matches that docstring wording, but the result is a false negative, which contradicts the claim that the mkdtemp text proves the destination is scratch. This is outside the C2 predicate; it is a correctness finding against the "resolves" statement.

### F6 — supplementary probes (not in mutants.json; the second-named guard per class)

`--probe-mutant` runs with the same counter, clone and freeze as F1:

- `alt_method_env_dropped`: v4:198, `_resolve(value, method_env, …)` → `_resolve(value, {}, …)`. Result: `PROBE outcome=killed detail=F01_attr_scratch scratch=0 want 1`.
- `alt_outflag_any_caller`: v4:305-306, `return None` → `continue`, so only some callers need the flag instead of every caller. Result: `PROBE outcome=killed detail=F06_outflag_mixed_callers explicit_out=1 want 0`.

The battery does guard the every-caller rule and the method-env rule. The gaps are confined to F3 and F4.

### F7 — selftest signal per mutant

Command: `python3 -I /tmp/tameshi-r42w2-MutantAuthor-mut-<name>.py --selftest`

- attr_bind_several_assignments: failed=2
- attr_never_resolve_self: failed=2
- method_fold_disabled: failed=2
- method_fold_several_returns: failed=0
- outflag_dests_never_recorded: failed=8
- outflag_no_parse_args_check: failed=0

The two battery survivors also survive the tool's own selftest. The oracle (`oracle()`, measure.py:311-317) runs only the battery anyway; `selftest_exit` is checked for the pristine tool only.

## Restoration evidence

The lane v4 and the clone v4 both have sha256 `784de4c0feef3364c4444632788af7ebb57d53032b79f60cc4330c094d122fe5`, before and after. The counter applies mutants only inside its own `tempfile.mkdtemp` work directory, and my mutant files are separate `/tmp/tameshi-r42w2-MutantAuthor-mut-*.py` copies. No tracked byte was mutated in place, and the clone working tree is clean (`git status --short` is empty).

The clone is KEPT as instructed. The witness directory `/tmp/tameshi-r42w2-MutantAuthor-wit/` and the mutant copies are also kept as evidence.

Tooling: no installs or updates.

## mutants.json to land unchanged

Path: `.ufo/evidence/round-42/census/mutants.json`, 1241 bytes, sha256 `b3abab06a48d41535aa35bc520d0884489cb684a7a52b5369c2aadc3db430358`. The bytes are reproducible with `git -C /tmp/tameshi-r42w2-MutantAuthor-clone show ae4bf4a:.ufo/evidence/round-42/census/mutants.json`.

```json
{
  "mutants": [
    {
      "name": "attr_bind_several_assignments",
      "class": "attr",
      "find": "if len(vals) == 1 and not isinstance",
      "replace": "if len(vals) >= 1 and not isinstance"
    },
    {
      "name": "attr_never_resolve_self",
      "class": "attr",
      "find": "if ctx.cls is not None and _is_self_attr(node) and node.attr in ctx.cls.attrs:",
      "replace": "if False and ctx.cls is not None and _is_self_attr(node) and node.attr in ctx.cls.attrs:"
    },
    {
      "name": "method_fold_disabled",
      "class": "method",
      "find": "value, method_env = ctx.cls.method_return(node.func.attr)",
      "replace": "value, method_env = None, None"
    },
    {
      "name": "method_fold_several_returns",
      "class": "method",
      "find": "if len(returns) != 1:",
      "replace": "if len(returns) < 1:"
    },
    {
      "name": "outflag_dests_never_recorded",
      "class": "outflag",
      "find": "                self.out_dests[dest] = flag",
      "replace": "                pass"
    },
    {
      "name": "outflag_no_parse_args_check",
      "class": "outflag",
      "find": "if flag and _parse_args_ns(node.value, env, ctx, depth + 1, seen):",
      "replace": "if flag:"
    }
  ]
}
```

Verdict: BROKEN: the C2 claim "every declared mutant of the new resolution code is killed" fails. Two of six mutants survive (outflag_no_parse_args_check, which is killable via witness W1, and method_fold_several_returns, which differs only on dead code), so the scratch run gives C2_R42_PASS=false at 4/6 killed. Separately, unmutated v4 misreads nested-return methods as scratch (witness W3).

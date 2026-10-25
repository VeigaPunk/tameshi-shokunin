# MutC1F12 — is F12 counted as a kill?

Scope: one mutation of the round-43 C1 counter's F12 declaration, run entirely in
`/tmp/tameshi-r43-MutC1F12-GVxBti/`, plus the two bounded diagnostics needed to explain the
result. No lane file was written by this seat except this report. The lane counter held
`ad7ecf8c…` when this seat copied and ran it; another seat's A5 commit (`901d947f…`, HEAD
`5cd2154f`) replaced it afterwards — §10 records that, and nothing below was re-derived from it.
Read-only apart from `/tmp`.

Counter under test: `ad7ecf8c1c1ea1e84982eec5da6bb453ab5533eb6c4f0c09af5559f6ba6bc875`, the C1 pin
at the `17f6ef0c…` freeze this item named. Mid-wave the lane advanced to `5cd2154f` and amendment
A5 repaired this counter to `901d947f…`; §10 records the post-flight check of the repaired bytes.
Every `file:line` citation in §§1-9 refers to the `ad7ecf8c…` counter.

## Verdict

**F12 is counted as a kill — the item's premise is refuted.** At the freeze revision the frozen
counter already prints `method_fold_several_returns` inside `killed_names`
(`mutants_killed=6 dead_code_only=0`). Flipping F12's declared `want` from `expected=False` to
`expected=True` does **not** move the mutant `dead_code_only → killed`: it stays `killed`, the
kill reason merely shifts from the `expected` bit to the `unflagged` bit, and the mutation's only
other observable effect is to break the green control (`fixtures_pass` 12/12 → 11/12).

The deeper result, which is the part that matters for C1: **no declaration of F12 can admit both
the pristine tool and this mutant.** Their F12 fingerprints differ on `expected`, `unflagged` and
`resolved` (§4), so under the counter's own oracle F12 is a *kill* fixture, not a
survive-then-classify D discriminator. The D branch at `mutants/measure.py:553-562` is unreachable
for this mutant, `dead_code_only=1` is therefore unsatisfiable as frozen, and the declared
`mutants_killed=5 dead_code_only=1` split (`contract.json:23`) is off by exactly one missing gate
at `mutants/measure.py:546`. Both routes to it are measured: `skip_dead_code=True` (§6) and the
generic reachability gate committed as A5 (§10).

## 1. Setup

```
$ cp .ufo/evidence/round-43/mutants/measure.py /tmp/tameshi-r43-MutC1F12-GVxBti/measure.py
$ cp .ufo/evidence/round-43/mutants/measure.py /tmp/tameshi-r43-MutC1F12-GVxBti/measure-pristine.py
ad7ecf8c1c1ea1e84982eec5da6bb453ab5533eb6c4f0c09af5559f6ba6bc875  measure-pristine.py
ad7ecf8c1c1ea1e84982eec5da6bb453ab5533eb6c4f0c09af5559f6ba6bc875  measure.py
$ sha256sum .ufo/evidence/round-43/mutants/measure.py   # lane file, untouched
ad7ecf8c1c1ea1e84982eec5da6bb453ab5533eb6c4f0c09af5559f6ba6bc875
```

`ad7ecf8c…` is the contract pin (`contract.json:25`) and the freeze blob
(`17f6ef0c:…/measure.py`), so the byte-identical copy is the frozen counter and scores
`self_pin=1`. The declared mutant was regenerated from the unchanged round-42 declaration with
the counter's own `apply_once` (find `if len(returns) != 1:` → `if len(returns) < 1:`,
`apply_count=1`), sha256 `b455639c2f7c7ddb53546d52a916a0863601e417c1693e698f4e54349d8979d5`.

## 2. Baseline — the unmodified counter at the freeze revision

```
$ python3 measure-pristine.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    --rev 17f6ef0c72ec27e1aea305b5c95806b43bb2caef \
    --freeze 17f6ef0c72ec27e1aea305b5c95806b43bb2caef
C1_R43: self_pin=1 tool_absent=0 tool_sha_ok=0 selftest_exit=0 fixtures_pass=12/12 run_errors=0 live_ok=3/3 live_unflagged_v4=0 live_tool_errors=0 mutants_declared=6 mutants_killed=6 dead_code_only=0 equivalent=0 not_killed=0 runtime_error=0 apply_error=0 unresolved=0 killed_names=attr_bind_several_assignments,attr_never_resolve_self,method_fold_disabled,method_fold_several_returns,outflag_dests_never_recorded,outflag_no_parse_args_check dead_code_names= dead_code_cases= dead_code_arg_ok=0 kill_fixture_reachable=1 rev=17f6ef0c72ec27e1aea305b5c95806b43bb2caef freeze=17f6ef0c72ec27e1aea305b5c95806b43bb2caef C1_R43_PASS=false
EXIT=1
```

The mutant is already killed, and the F12-only probe says by which fixture:

```
$ python3 measure-pristine.py ... --probe-mutant ./mutant_method_fold_several_returns.py
C1_R43_PROBE: verdict=killed failures=1 errors=0 first=['F12_method_two_returns expected=1 want 0']
EXIT=0
```

One failure, no run errors, and it is F12. Independently corroborated by the sibling seat
`.ufo/waves/round-43/w1/MutC1F11.md` §4(a), which saw the same `mutants_killed=6 dead_code_only=0`
and the same probe line on its own `/tmp` copy.

## 3. The assigned mutation — F12 `expected=False` → `expected=True`

Total diff against the frozen bytes, one hunk: only the `expected` bit on one line changes.

```diff
@@ -239,7 +239,7 @@
     def run(self):
         with open(self.destination(), 'w') as handle:
             handle.write('x')
-''', {'expected': False, 'scratch': False, 'explicit_out': False, 'unflagged': False},
+''', {'expected': True, 'scratch': False, 'explicit_out': False, 'unflagged': False},
         'self.destination()', 11),
 }
```

`measure.py` sha256 after the edit: `938e2d2ff6800a2e7f56c54e808206201b612e0f04085f28d5a49fbcff3d0058`.

```
$ python3 measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    --rev 17f6ef0c72ec27e1aea305b5c95806b43bb2caef \
    --freeze 17f6ef0c72ec27e1aea305b5c95806b43bb2caef
C1_R43: self_pin=0 tool_absent=0 tool_sha_ok=0 selftest_exit=0 fixtures_pass=11/12 run_errors=0 live_ok=3/3 live_unflagged_v4=0 live_tool_errors=0 mutants_declared=6 mutants_killed=6 dead_code_only=0 equivalent=0 not_killed=0 runtime_error=0 apply_error=0 unresolved=0 killed_names=attr_bind_several_assignments,attr_never_resolve_self,method_fold_disabled,method_fold_several_returns,outflag_dests_never_recorded,outflag_no_parse_args_check dead_code_names= dead_code_cases= dead_code_arg_ok=0 kill_fixture_reachable=1 rev=17f6ef0c72ec27e1aea305b5c95806b43bb2caef freeze=17f6ef0c72ec27e1aea305b5c95806b43bb2caef C1_R43_PASS=false
EXIT=1
```

Delta against baseline: `mutants_killed` 6 → 6, `dead_code_only` 0 → 0, `killed_names`
identical, `unresolved` 0 → 0. The one moving field is `fixtures_pass` 12/12 → 11/12 — the
pristine-tool green control rejecting the wrong declaration — and `self_pin` 1 → 0, the
self-pin refusing to certify edited counter bytes.

```
$ python3 measure.py ... --probe-mutant ./mutant_method_fold_several_returns.py
C1_R43_PROBE: verdict=killed failures=1 errors=0 first=['F12_method_two_returns unflagged=1 want 0']
```

So the mutant still FAILs the battery under the flipped declaration; the mutant was not
"surviving until the declaration was broken".

## 4. Why the flip cannot produce the requested transition

`check_site` (`mutants/measure.py:314-331`) compares all four `BITS` plus the needle. On F12
(`mutants/measure.py:230-243`, `lineno=11`, needle `self.destination()`):

| tool | expected | scratch | explicit_out | unflagged | resolved |
|---|---|---|---|---|---|
| pristine `write-path-census-v4.py` | False | False | False | False | `self.destination()` |
| `method_fold_several_returns` | **True** | False | False | **True** | `os.path.join('tmp', 'expected.json')tmp'tmp'expected.json'expected.json'` |

Measured admittance probes (counter's own `check_site`, same staged fixture):

```
pristine  declared want                    -> None                       (passes)
pristine  want w/ expected,unflagged negated -> expected=0 want 1        (fails)
pristine  own bits, declared needle        -> None                       (passes)
mutant    declared want                    -> expected=1 want 0          (fails)
mutant    want w/ expected,unflagged negated -> resolved lacks 'self.destination()'  (fails)
mutant    own bits, declared needle        -> resolved lacks 'self.destination()'    (fails)
```

The two bit-vectors are disjoint and the mutant's `resolved` string does not contain the
declared needle, so **every** declaration fails at least one of the two tools. A fixture that the
pristine tool passes is therefore a kill fixture for this mutant by construction, and the D
branch (`mutants/measure.py:553-562`) is never entered for it — `dead_code_cases` stays empty, so
the D outcome cannot exist. That is why the item's requested direction (`dead_code_only →
killed`) is unobservable: the state machine is already at `killed`.

## 5. `dead_code_arg_ok` — computed from the differential, not hardcoded

```
mutants/measure.py:553            differ = differential(tool_path, path, work)
mutants/measure.py:554            dead = [case for case, kind in differ if kind == 'dead_code']
mutants/measure.py:555            live_diff = [case for case, kind in differ if kind != 'dead_code']
mutants/measure.py:560-562         else: dead_code_only.append(name); dead_code_cases[name] = dead
mutants/measure.py:567            dead_arg_ok = 1 if dead_code_cases.get(DEAD_CODE_NAMES[0]) == [DEAD_CODE_FIXTURE] else 0
```

It is the observed `differential()` result for `method_fold_several_returns`, gated to exist only
when `differ` is non-empty and every differing case is labelled `dead_code` by
`unreachable_statements()`; it is compared against the hardcoded fixture-name constant
`DEAD_CODE_FIXTURE` (`:246`), not to a hardcoded `1`. It varies with the evidence: `0` in the
frozen run (differential never reached, `dead_code_cases` empty) and `1` in §6 where the D path
runs with `dead_code_cases=F12_method_two_returns`. So: **computed, with a hardcoded expected
case name on both sides of the comparison.**

## 6. Diagnostic (outside the item, labelled) — the one argument that produces the declared split

The counter has a `skip_dead_code` switch, `battery(..., skip_dead_code=False)` at
`mutants/measure.py:333`, applied at `:341` (`if skip_dead_code and name == DEAD_CODE_FIXTURE:
continue`), and **never passed**. `grep -n skip_dead_code` returns only those two lines. Passing
it for the mutant battery — the single change at `:546`,
`battery(path, work)` → `battery(path, work, skip_dead_code=True)` — on a third pristine copy
(`measure-skipdc.py`) gives:

```
C1_R43: self_pin=0 tool_absent=0 tool_sha_ok=0 selftest_exit=0 fixtures_pass=12/12 run_errors=0 live_ok=3/3 live_unflagged_v4=0 live_tool_errors=0 mutants_declared=6 mutants_killed=5 dead_code_only=1 equivalent=0 not_killed=0 runtime_error=0 apply_error=0 unresolved=0 killed_names=attr_bind_several_assignments,attr_never_resolve_self,method_fold_disabled,outflag_dests_never_recorded,outflag_no_parse_args_check dead_code_names=method_fold_several_returns dead_code_cases=F12_method_two_returns dead_code_arg_ok=1 kill_fixture_reachable=1 rev=17f6ef0c72ec27e1aea305b5c95806b43bb2caef freeze=17f6ef0c72ec27e1aea305b5c95806b43bb2caef C1_R43_PASS=false
EXIT=1
```

Every declared C1 field appears (`mutants_killed=5 dead_code_only=1 dead_code_arg_ok=1`,
`dead_code_cases=F12_method_two_returns`), and `outflag_no_parse_args_check` keeps its F11 kill —
i.e. the contract's K-then-D semantics is one call-argument away from the frozen code. This is
characterisation for L1, not a proposed contract change and not part of the assigned mutation.
`tool_sha_ok=0` survives the patch (§7), so the predicate still cannot pass.

## 7. Independent blocker observed while running the item — `tool_sha_ok` reads the wrong pin

`mutants/measure.py:486` compares `sha(show(REV, 'tools/write-path-census-v4.py'))` against
`contract['tool_sha256']`. That top-level key is the **guard's** pin, not the census tool's:

```
contract.json:68  "tool_sha256": "8140945a…"   (= tools/staged-id-guard.py at the freeze blob)
contract.json:70  "tools/write-path-census-v4.py": "784de4c0…"
contract.json:71  "tools/staged-id-guard.py":      "8140945a…"
git show 17f6ef0c:tools/write-path-census-v4.py | sha256sum -> 784de4c0feef3364c4444632788af7ebb57d53032b79f60cc4330c094d122fe5
```

A4, applied by another seat *during* this run, moved that top-level key to
`efa5f129…` (the octet-repaired guard, see `git diff 17f6ef0c -- .ufo/evidence/round-43/contract.json`),
which is still the guard, so `tool_sha_ok` is 0 at every revision either way — a wrong-referent
error, not a stale pin. My runs passed `--freeze 17f6ef0c…` and therefore read the freeze blob
(`8140945a…`); the A4 edit landed after and does not affect any line above. C1's own pin is
`contract['frozen_tools']['tools/write-path-census-v4.py']`, which matches the staged tool
exactly. Reported here because it blocks `C1_R43_PASS` independently of F12; the fix belongs to
L1, not to this seat. A5 (HEAD, `5cd2154f`) did fix it — `tool_sha_ok=1` in §10.

## 8. Restoration

F12's declaration was restored byte-for-byte, not merely re-declared:

```
$ python3 - <<'PY' ... (edit applied with the same tool) PY
$ sha256sum measure.py measure-pristine.py
ad7ecf8c1c1ea1e84982eec5da6bb453ab5533eb6c4f0c09af5559f6ba6bc875  measure.py
ad7ecf8c1c1ea1e84982eec5da6bb453ab5533eb6c4f0c09af5559f6ba6bc875  measure-pristine.py
$ diff -q measure.py measure-pristine.py && echo RESTORED_BYTES_IDENTICAL_TO_PIN
RESTORED_BYTES_IDENTICAL_TO_PIN
```

Restored bytes re-run through the same detector reproduce the baseline line exactly
(`self_pin=1 … mutants_killed=6 dead_code_only=0 … killed_names=…,method_fold_several_returns,…`,
`EXIT=1`), so pristine → mutated → restored is behaviourally stable and the mutated result in §3
is attributable to the single flipped bit.

The unmodified line, `mutants/measure.py:242` (no trailing whitespace, verified with `cat -A`):

```
''', {'expected': False, 'scratch': False, 'explicit_out': False, 'unflagged': False},
```

Lane counter re-hashed immediately after the restoration run:
`ad7ecf8c1c1ea1e84982eec5da6bb453ab5533eb6c4f0c09af5559f6ba6bc875` — unchanged at that moment,
and `git status --porcelain .ufo/evidence/round-43/mutants/measure.py` was empty. A5
(`901d947f…`, HEAD `5cd2154f`) replaced those bytes afterwards; §10.

## 9. Bounds and tooling

- Writes: only `/tmp/tameshi-r43-MutC1F12-GVxBti/` (deleted after the runs) and this report.
  The lane checkout, its Git index/jj state, the fleet repo and `/home/vgpnk/Projects/shokuknow`
  were not written; no mutating git or jj command ran (only read-only `git show`, `rev-parse`,
  `status`, `diff`, `log`).
- No tool installed or upgraded; `python3 3.14.8` as shipped. `pacman` untouched.
- Scratch hashes for the record: pristine/restored `ad7ecf8c…`, mutated `938e2d2f…`,
  skip-dead-code diagnostic `ad7ecf8c…` + one hunk.

## 10. Post-flight — the counter was repaired mid-wave (A5), and F12 stops being a kill

While this seat ran, HEAD advanced `17f6ef0c… → 5cd2154f` ("freeze A4/A5 — guard map-shape repair
(wave-1 finding) and C1 reachability gate + tool-pin source"). The C1 counter is now
`901d947fb912a6cbbcc2de8c876a72a55daa3ab6ca49e8e9c634aac041ccc7e0` (the C1 pin at HEAD), and it
changes exactly the two mechanisms this probe exposed:

- `battery()` now returns a seventh value `detail` (fixture → unreachable-statement flag), and the
  kill branch becomes `reachable_fails = [case for case in mdetail if not mdetail[case]]; if mf
  and reachable_fails: killed.append(name)` (`mutants/measure.py:559-562` at HEAD) — the K
  sentence at `mutants/measure.py:11-15` made executable.
- `tool_sha_ok` now reads `contract['frozen_tools'][TOOL_REL]` with the top-level pin as fallback
  (`mutants/measure.py:493-495` at HEAD).

Verification with the repaired bytes copied to `/tmp/tameshi-r43-MutC1F12-GVxBti/measure-a5.py`
(`901d947f…`), at the freeze revision this item named:

```
$ python3 measure-a5.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    --rev 17f6ef0c72ec27e1aea305b5c95806b43bb2caef \
    --freeze 17f6ef0c72ec27e1aea305b5c95806b43bb2caef
C1_R43: self_pin=0 tool_absent=0 tool_sha_ok=1 selftest_exit=0 fixtures_pass=12/12 run_errors=0 live_ok=3/3 live_unflagged_v4=0 live_tool_errors=0 mutants_declared=6 mutants_killed=5 dead_code_only=1 equivalent=0 not_killed=0 runtime_error=0 apply_error=0 unresolved=0 killed_names=attr_bind_several_assignments,attr_never_resolve_self,method_fold_disabled,outflag_dests_never_recorded,outflag_no_parse_args_check dead_code_names=method_fold_several_returns dead_code_cases=F12_method_two_returns dead_code_arg_ok=1 kill_fixture_reachable=1 rev=17f6ef0c72ec27e1aea305b5c95806b43bb2caef freeze=17f6ef0c72ec27e1aea305b5c95806b43bb2caef C1_R43_PASS=false
EXIT=1
```

On the repaired counter **F12 is not counted as a kill**: the mutant leaves `killed_names`, gains
`dead_code_only` with `dead_code_cases=F12_method_two_returns`, and `dead_code_arg_ok=1`. Every
declared C1 field except `self_pin` (0 by construction — repaired bytes scored against the older
freeze's pin) now matches `contract.json:23`. `[INFERENCE]` At the new freeze the pin matches by
construction (`git show HEAD:.ufo/evidence/round-43/mutants/measure.py | sha256sum` = `901d947f…`
= the HEAD contract's C1 `counter_sha256`), so `self_pin=1` there and the predicate would be
satisfied on the same inputs. I did not run a measurement at HEAD: my bounds name `487b8f0d…` and
`17f6ef0c…` only, and the deciding run is L1's.

Residual, control mode only: the repaired `--probe-mutant` path still derives its verdict from
`fails` alone and ignores `detail` (`mutants/measure.py:508-514` at HEAD), so the same mutant still
probes as killed:

```
$ python3 measure-a5.py --probe-mutant ./mutant_method_fold_several_returns.py --rev 17f6… --freeze 17f6…
C1_R43_PROBE: verdict=killed failures=1 errors=0 first=['F12_method_two_returns expected=1 want 0']
EXIT=0
```

After A5 a falsifier seat using `--probe-mutant` therefore gets a verdict that contradicts the
measurement path for a dead-code-only mutant. A one-line gate on `detail` there would align them;
it changes no C1 field.


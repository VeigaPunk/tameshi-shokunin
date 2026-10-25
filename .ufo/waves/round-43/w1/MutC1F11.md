# MutC1F11 — is the F11 kill F11's?

Scope: one ablation of the round-43 C1 counter at the freeze revision, run entirely in
`/tmp/tameshi-r43-MutC1F11-ablate/`. No lane file was written; the lane counter's bytes are
unchanged (verified before and after, `ad7ecf8c…`). Read-only apart from `/tmp`.

## Verdict

**F11's kill is F11's — proven, and single-source.** Removing the `F11_outflag_namespace` entry
from `FIXTURES` and changing nothing else in the battery drops exactly one mutant out of
`killed_names`: `outflag_no_parse_args_check`. `mutants_killed` 6 → 5, and the lost mutant
becomes `equivalent` over the remaining eleven fixtures, i.e. it diverges from the pristine tool
on **no** other fixture. Two per-mutant probes confirm the same attribution directly.

Secondary (out of item, but it is the same two fields): the frozen counter at the freeze revision
does **not** emit the contract target `mutants_killed=5 dead_code_only=1`
(`.ufo/evidence/round-43/contract.json:23`). It emits `mutants_killed=6 dead_code_only=0`, so
`C1_R43_PASS=false` for two reasons that are independent of F11 (see §4).

## 1. Ablation setup

```
$ cp .ufo/evidence/round-43/mutants/measure.py /tmp/tameshi-r43-MutC1F11-ablate/measure.py
$ cp .ufo/evidence/round-43/mutants/measure.py /tmp/tameshi-r43-MutC1F11-ablate/measure-unmodified.py
$ sha256sum /tmp/tameshi-r43-MutC1F11-ablate/measure-unmodified.py
ad7ecf8c1c1ea1e84982eec5da6bb453ab5533eb6c4f0c09af5559f6ba6bc875   # == contract pin and lane file
```

The byte-identical copy scores `self_pin=1`, so it is provably the frozen counter, not a
lookalike. The ablated copy is `94595cc837292d7bd409475e623ffaca8d5b6681aa50dfd5836406187b895a75`
and its total diff against the frozen bytes is **two hunks**:

```diff
@@ -202,28 +202,6 @@
-    # F11 — kill fixture for outflag_no_parse_args_check. Reachable code: the
-    ... (4 comment lines) ...
-    'F11_outflag_namespace': ('''import argparse
-    ... (F11 body, {'expected': True, 'scratch': False, 'explicit_out': False, 'unflagged': True}, None, 8) ...
@@ -566,7 +544,7 @@
-            FIXTURES['F11_outflag_namespace'][0]) else 1
+            FIXTURES.get('F11_outflag_namespace', ('',))[0]) else 1
```

Hunk 1 is the ablation the item asks for. Hunk 2 is forced, and it is a finding in its own right
(§3): the counter hard-codes F11's key inside the `C1_R43_PASS` predicate at
`mutants/measure.py:568-569`, so with the entry removed the counter dies before it prints
`mutants_killed`. The shim only makes an absent key non-fatal; it changes no classification,
no fixture, and no oracle.

## 2. The two measurement runs, verbatim

Run B first (the ablation), then Run A (unmodified), both from `/tmp/tameshi-r43-MutC1F11-ablate/`,
same `--lane`, `--rev`, `--freeze` (`17f6ef0c72ec27e1aea305b5c95806b43bb2caef`):

```
$ python3 measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    --rev 17f6ef0c72ec27e1aea305b5c95806b43bb2caef \
    --freeze 17f6ef0c72ec27e1aea305b5c95806b43bb2caef
C1_R43: self_pin=0 tool_absent=0 tool_sha_ok=0 selftest_exit=0 fixtures_pass=11/11 run_errors=0 live_ok=3/3 live_unflagged_v4=0 live_tool_errors=0 mutants_declared=6 mutants_killed=5 dead_code_only=0 equivalent=1 not_killed=0 runtime_error=0 apply_error=0 unresolved=0 killed_names=attr_bind_several_assignments,attr_never_resolve_self,method_fold_disabled,method_fold_several_returns,outflag_dests_never_recorded dead_code_names= dead_code_cases= dead_code_arg_ok=0 kill_fixture_reachable=1 rev=17f6ef0c72ec27e1aea305b5c95806b43bb2caef freeze=17f6ef0c72ec27e1aea305b5c95806b43bb2caef C1_R43_PASS=false
EXIT=1
```

```
$ python3 measure-unmodified.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    --rev 17f6ef0c72ec27e1aea305b5c95806b43bb2caef \
    --freeze 17f6ef0c72ec27e1aea305b5c95806b43bb2caef
C1_R43: self_pin=1 tool_absent=0 tool_sha_ok=0 selftest_exit=0 fixtures_pass=12/12 run_errors=0 live_ok=3/3 live_unflagged_v4=0 live_tool_errors=0 mutants_declared=6 mutants_killed=6 dead_code_only=0 equivalent=0 not_killed=0 runtime_error=0 apply_error=0 unresolved=0 killed_names=attr_bind_several_assignments,attr_never_resolve_self,method_fold_disabled,method_fold_several_returns,outflag_dests_never_recorded,outflag_no_parse_args_check dead_code_names= dead_code_cases= dead_code_arg_ok=0 kill_fixture_reachable=1 rev=17f6ef0c72ec27e1aea305b5c95806b43bb2caef freeze=17f6ef0c72ec27e1aea305b5c95806b43bb2caef C1_R43_PASS=false
EXIT=1
```

The lane's own counter, run in place over the same args, prints the unmodified line byte for byte
(including `self_pin=1`), `EXIT=1` — so the `/tmp` copy is behaviourally the lane file.

### The delta

| field | unmodified | F11 removed | delta |
|---|---|---|---|
| `mutants_killed` | 6 | 5 | **−1** |
| `killed_names` | 6 names | 5 names | set difference = `{outflag_no_parse_args_check}` |
| `equivalent` | 0 | 1 | +1 (the evicted mutant) |
| `fixtures_pass` | 12/12 | 11/11 | −1 fixture |
| `unresolved` | 0 | 0 | 0 |
| exit code | 1 | 1 | 0 |

Every other mutant's verdict is unchanged. Because the battery runs each fixture as an isolated
subprocess on its own file (`battery()`, `mutants/measure.py:333-369`), removing one fixture
cannot perturb another fixture's outcome; the set difference is therefore exactly F11's
contribution to `mutants_killed`.

## 3. Direct per-mutant probes (independent of the aggregate)

Both mutants were materialised by applying the round-42 declaration once to
`17f6ef0c…:tools/write-path-census-v4.py` (`applies=1`, base `784de4c0…`):

```
$ python3 measure-unmodified.py ... --probe-mutant mutant-outflag.py
C1_R43_PROBE: verdict=killed failures=1 errors=0 first=['F11_outflag_namespace explicit_out=1 want 0']
EXIT=0

$ python3 measure.py ... --probe-mutant mutant-outflag.py          # F11 removed
C1_R43_PROBE: verdict=survived failures=0 errors=0 first=[]
EXIT=1
```

So the mutant's single FAIL under the twelve-fixture oracle is the F11 fixture, and with F11 gone
it produces zero failures anywhere. The failing bit, `explicit_out=1 want 0`, is precisely the
`_parse_args_ns` guard the mutant deletes (`if flag and _parse_args_ns(...)`), and F11 is the
fixture that routes an operator-named destination through a `SimpleNamespace` rather than
`parse_args` — reachable code with no statement after an unconditional return
(`unreachable_statements(F11) == []`, `kill_fixture_reachable=1` in both runs).

### 3a. Structural finding — the ablation as specified cannot run

Strict removal of the `FIXTURES` entry alone (no shim) aborts before any verdict line:

```
Traceback (most recent call last):
  File "/tmp/tameshi-r43-MutC1F11-ablate/measure.py", line 595, in <module>
    sys.exit(main())
  File "/tmp/tameshi-r43-MutC1F11-ablate/measure.py", line 547, in main
    FIXTURES['F11_outflag_namespace'][0]) else 1
KeyError: 'F11_outflag_namespace'
EXIT=1
```

`mutants/measure.py:568-569` re-reads F11's source by literal key after the mutant loop, so the
counter carries a second, hard dependency on F11 that is not part of the battery. Any falsifier
that ablates F11 (or that wants to score the counter with a reduced fixture set) needs the same
one-line tolerance; the counter should use `.get(...)` and report the field as not-applicable.

## 4. Consequential finding — the frozen counter disagrees with the contract target

The unmodified run at the freeze revision prints `mutants_killed=6 dead_code_only=0
dead_code_arg_ok=0` and `C1_R43_PASS=false`, against the declared target
`mutants_killed=5 dead_code_only=1` (`contract.json:23`). Two independent causes, neither
involving F11:

**(a) The kill rule has no reachability gate.** The docstring declares K as "a mutant is `killed`
when the battery produces at least one FAIL … The killing fixture must contain no
runtime-unreachable statement" (`mutants/measure.py:11-15`), but the implementation records a
kill on any FAIL (`mutants/measure.py:550-551`) without consulting
`unreachable_statements()`. F12 — the fixture whose body carries a statement after an
unconditional `return` — therefore *kills* `method_fold_several_returns` instead of serving as
the D discriminator, and the `dead_code_only` branch never runs for it:

```
$ python3 check_reachability.py measure-unmodified.py        # counter's own function
fixtures=12
F12_method_two_returns UNREACHABLE ['module.body[1].body[0][1]']
F11_reachable=1 F12_reachable=0

$ python3 measure-unmodified.py ... --probe-mutant mutant-methodfold.py
C1_R43_PROBE: verdict=killed failures=1 errors=0 first=['F12_method_two_returns expected=1 want 0']

$ python3 measure-noF12.py ...          # F12 removed, F11 kept
... mutants_killed=5 dead_code_only=0 equivalent=1 ... killed_names=attr_bind_several_assignments,attr_never_resolve_self,method_fold_disabled,outflag_dests_never_recorded,outflag_no_parse_args_check ... C1_R43_PASS=false
EXIT=1
```

With F12 removed, `method_fold_several_returns` leaves `killed` and becomes `equivalent`, every
other kill is unchanged, and the surviving five include `outflag_no_parse_args_check` — i.e. F11
carries its own kill independently, exactly as the contract's amendment states
(`contract.json:87`). The 6/0 split is F12's, not F11's.

**(b) `tool_sha_ok=0` at every revision.** The counter compares
`sha(tools/write-path-census-v4.py@REV)` against `contract['tool_sha256']`
(`mutants/measure.py:486`), but that top-level pin is the **guard's** hash:

```
contract.json:68   "tool_sha256": "8140945a816873562eee8bcc6862d5e098f95b8083b4760b087812568f97b762"
contract.json:70   "tools/write-path-census-v4.py": "784de4c0feef3364c4444632788af7ebb57d53032b79f60cc4330c094d122fe5"
contract.json:71   "tools/staged-id-guard.py":      "8140945a816873562eee8bcc6862d5e098f95b8083b4760b087812568f97b762"

$ git -C LANE show 17f6ef0c72ec27e1aea305b5c95806b43bb2caef:tools/write-path-census-v4.py | sha256sum
784de4c0feef3364c4444632788af7ebb57d53032b79f60cc4330c094d122fe5
$ git -C LANE show 487b8f0da89fa0e2b8bea6930068accbf36e70a9:tools/write-path-census-v4.py | sha256sum
784de4c0feef3364c4444632788af7ebb57d53032b79f60cc4330c094d122fe5
```

The census tool is identical at base and freeze, so `tool_sha_ok` is 0 on both permitted
revisions and the predicate is unsatisfiable until `contract.json:68` names the census tool.

## 5. What this does and does not settle

- Settles: `outflag_no_parse_args_check` owes its kill to F11 and to nothing else. The ablation
  delta is a one-name set difference and two probes agree.
- Does not settle: whether the round-43 C1 predicate can pass. It cannot at the freeze revision,
  for the two reasons in §4 — both outside this seat's item and outside F11's attribution.
- Bounds respected: the only writes are under `/tmp/tameshi-r43-MutC1F11-ablate/`; the lane
  checkout, its jj/Git state, the fleet repo and `/home/vgpnk/Projects/shokuknow` were not
  written. No tools installed or upgraded.

## 6. Scratch cleanup

`/tmp/tameshi-r43-MutC1F11-ablate/` (measure.py `94595cc8…`, measure-unmodified.py `ad7ecf8c…`,
measure-noF12.py, gen_mutant.py, check_reachability.py, the two mutant files) deleted after the
runs. Lane counter re-hashed after the runs: `ad7ecf8c…`, unchanged.

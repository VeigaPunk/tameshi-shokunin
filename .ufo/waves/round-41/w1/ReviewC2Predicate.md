# ReviewC2Predicate — round 41, C2 census-v3 counter

Seat: `L1Tameshi41.ReviewC2Predicate` (reviewer, read-only).
Freeze `d4ee4e63a0a4402bd8628fbc80f06bbd8f37d937`, base `a3d6c690bcbf8914551d4f4e8e1612784c1c2046`.
Contract read first, never edited. No lane checkout, jj state, Git index or sibling lane was modified.

What I ran (all permitted): base-rev counter run, `--control`, the tool's `--selftest`, the tool's
`--file` classifier, and scratch lanes under `/tmp/tameshi-r41-reviewc2-*`. **I did not run either
counter at the measurement revision.**

Artifact identities I reviewed, and the drift I had to chase:

| artifact | at the freeze `d4ee4e6` | at the measurement commit `b37ce97` |
|---|---|---|
| `census/measure.py` | `5d57c709…` | `83268eff…` (+`ARG_MARK`/`ARG_MUTANT`, third mutant) |
| `census/fixtures.json` | `a4123ce3…` | `20b6254d…` (fixtures re-rooted) |
| `tools/write-path-census-v3.py` | `095924a7…` | `095924a7…` (unchanged) |
| `contract.json` pins (`claims.C2`) | `5d57c709…`/`a4123ce3…`/`095924a7…` | `83268eff…`/`20b6254d…`/`095924a7…` |

HEAD advanced from `d4ee4e6` to the measurement candidate `b37ce974b6efb8c465626d7346149549a3300a4b`
while I was reviewing. Every line number below is quoted against the blobs **committed at
`b37ce97`**, i.e. against what the deciding run will execute — I verified
`git show b37ce97:<path> | sha256sum` equals the working-tree shas above for all three artifacts.

The drift is **declared** in `contract.json` `amendments[1]` (A2, found by `MutFixtureVar`) and is a
tightening, not a loosening: it added the `symlink_arg` mutant and re-rooted the two fixtures. The
only post-`b37ce97` working-tree edit is `amendments[4]` (A5, C1 counter only); `claims.C2` is
byte-identical at HEAD and in the working tree, so nothing in this review moves with it.

---

## S1 — CRITICAL — the counter executes the artifact in-process, then takes the artifact's verdict

`.ufo/evidence/round-41/census/measure.py:177` (`mod = load_mod(...)` → `:74 spec.loader.exec_module`)
runs the measured tool **before** the selftest (`:179`) and the mutants (`:203`), in the counter's own
interpreter. Every verdict the pass predicate consumes afterwards is then supplied by that same
module: fixture fields `:238` (from `:81 mod.summarize(mod.classify_source(...))`), live records
`:210`, and the mutant results, which are `subprocess.run` calls the artifact can rewrite at import
(`:203`, judged at `:208`).

Consequence: `C2_R41_PASS=true` is reachable with **zero destination resolution**. Demonstrated:

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-41/census/measure.py \
        --lane /tmp/tameshi-r41-reviewc2-stub/lane --rev HEAD
# C2_R41: tool_absent=0 tool_sha_ok=1 v2_sha_ok=1 selftest_exit=0 var_unflagged=1 var_expected=1
#   symlink_unflagged=1 symlink_expected=1 literal_unflagged=1 scratch_var_unflagged=0
#   v2_var_expected=0 v2_symlink_sites=0 live_var_lineno=811 live_var_resolved_v3=1
#   live_var_scratch_v3=1 live_var_expected_v2=0 live_symlink_lineno=820
#   live_symlink_resolved_v3=1 live_symlink_scratch_v3=1 live_symlink_sites_v2=0
#   mutant_resolve_killed=1 mutant_symlink_killed=1 mutant_symlink_arg_killed=1 C2_R41_PASS=true
```

`/tmp/tameshi-r41-reviewc2-stub/lane/tools/write-path-census-v3.py` never parses an argument, never
opens a fixture, and never reads `tools/repeat-control.py`. It returns constant records, patches
`subprocess.run` to report `0` for the selftest and `1` for anything whose path contains `mutant`,
and carries the three marker lines in a function that is never called. The marker lines exist only so
the counter can produce the three mutated copies it then asks this same patched module to run.

Note `hashlib` is digesting before `load_mod` (`:141`), so `sha_ok` alone is not forgeable this way —
the rest of the predicate is.

## S2 — HIGH — the "contract pin" is self-referential; nothing pins the counter or the fixtures

`:142-149` reads `claims.C2.tool_sha256` from `contract.json` **at the measured revision** and compares
it to the tool blob at that same revision. There is no counter-side constant for v3, in contrast with
`V2_SHA` at `:30`/`:152`, which *is* a literal. So any commit that writes the tool and its sha into the
same `contract.json` reports `tool_sha_ok=1`; the clause "the committed v3 tool matches its contract
pin" cannot fail for a tool written for the occasion. The S1 stub demonstrates exactly this — its sha
was accepted because I wrote it into the stub lane's contract in the same commit.

Two adjacent gaps in the same direction:

- `claims.C2.fixtures_sha256` is declared but **never read** by the counter (`grep -n sha256` yields
  only `:141`, `:152` and the tool read at `:142`). Fixtures can be rewritten without the pin moving.
- `claims.C2.counter_sha256` is not self-checked either, so a counter edited after the freeze still
  "measures". The amendment ledger is the only control here, and it is prose, not a check: the
  amendment at A2 legitimately re-pinned counter and fixtures, and an unlogged re-pin would look
  identical to the counter.

## S3 — HIGH — the live half is self-attested; no counter-side expected value exists

`:210` takes `live_records = mod.classify_source(live_text)` from the artifact, and `:224-232` derive
`live_var_resolved`, `live_var_scratch`, `live_sym_resolved`, `live_sym_scratch` only from
`rec['expected']`, `rec['scratch']`, `rec['kind']` and `rec['lineno']`. `rec['resolved']` is **never
inspected** by the counter (its only uses are those four booleans). So the clause "both live
variable-destination sites resolve to an expected-value path" is checked as "the artifact says so".

Demonstrated: `/tmp/tameshi-r41-reviewc2-sham/lane` — a tool whose live branch is literally

```python
if 'snap-tamper-duplicate-key' in text:
    return [{'lineno': 811, 'kind': 'open', 'expected': True, 'scratch': True, ...},
            {'lineno': 820, 'kind': 'os.symlink', 'expected': True, 'scratch': True, ...}]
```

and whose fixture branch is one substring test — scored `live_var_resolved_v3=1`
`live_symlink_resolved_v3=1` and `C2_R41_PASS=true` (command shape as in S1, `--lane
/tmp/tameshi-r41-reviewc2-sham/lane`). The live evidence for `repeat-control.py:811/820` is therefore
reported, not verified.

## S4 — MEDIUM — "mutant killed" means "exit code != 0": a crash or usage error counts

`:208` is `killed[name] = int(run.returncode != 0)`. Any traceback, `SystemExit`, or argparse usage
error (`exit 2`) is indistinguishable from a recognizer removal. Demonstrated at
`/tmp/tameshi-r41-reviewc2-mut2/resolve_mut.py`: mutating `bound = env.get(node.id)` to `bound = None`
in a tool whose `_resolve` output is otherwise unused kills the run with
`AttributeError: 'NoneType' object has no attribute 'id'` — and the counter records
`mutant_resolve_killed=1`.

Scoped honestly: against the real `write-path-census-v3.py` the three mutants do die **on the right
fixture class**, not by crash (I ran each mutated copy against the current fixtures):

```
resolve    -> FAIL planted var_unflagged: want unflagged=1 got 0 / want expected_sites=1 got 0
symlink    -> FAIL planted symlink_unflagged: want unflagged=1 got 0 / want expected_sites=1 got 0
symlink_arg-> FAIL planted symlink_unflagged: want expected_sites=1 got 0
```

The artifact is not relying on the crash path today; the gate still admits it.

## S5 — MEDIUM — `os.replace`/`os.rename` record the **source** argument as a destination

`tools/write-path-census-v3.py:133` returns `[node.args[1], node.args[0]]` for
`os.replace`/`os.rename`, and `:161-165` joins every entry into one `resolved` string. A site that
merely *reads* an expected file is therefore classified as writing to one:

```
python3 tools/write-path-census-v3.py --file /tmp/tameshi-r41-reviewc2-lit.py
# /tmp/.../lit.py:4 os.replace expected=1 scratch=0 unflagged=1 \
#   os.path.join(root, "actual.json")tests/fixturesroot "tests/fixtures"actual.json"
# expected_sites=1 ... unflagged=1 variable_expected=1
```

(that file is `os.replace(join(root,"expected.json"), join(root,"actual.json"))` — destination is
`actual.json`.) This was live in the frozen fixture set: the freeze `d4ee4e6`
(`fixtures_sha256 a4123ce3…`) scored `literal_unflagged=1` while its write destination was `tests/actual.json`
(`os.replace(join("tests","expected.json"), join("tests","actual.json"))`). A2 re-rooted the fixture
so the destination is now the expected file, which repairs the fixture but not the tool: no fixture
or mutant distinguishes argument 0 from argument 1 for the `os.replace` class, so "resolves a write
destination" remains unproven there, and a read-only expected path anywhere in the live file would
count.

## S6 — MEDIUM-LOW — for `Call` nodes the "resolved" text is source text, so `expected` is lexical

`:88` seeds the result of `_resolve` with `parts = [trace]` (the node's own source segment) and
returns the concatenation. A non-folding call therefore contributes its spelling, not its value:
`pick("expected.json", "actual.json")` or `os.environ.get("X", "snapshot")` classifies as expected no
matter what the call returns. The live output shows this directly — the `resolved` string printed for
`repeat-control.py:811` is
`os.path.join(tamper_duplicate_key, "expected.json")os.path.join(scratch, "snap-t…")`, a
concatenation of source segments, not a path. This is what `live_var_resolved_v3=1` actually rests on.

## S7 — LOW — `scratch` and `expected` are matched against identifier spellings

`:166-168` tests `SCRATCH_MARKERS` (`'scratch'`, `'/tmp'`, …) against `trace` as well as `resolved`.
`live_var_scratch_v3=1` is satisfied by the variable name `scratch` appearing in the binding's source
(`tamper_duplicate_key = os.path.join(scratch, …)`, `repeat-control.py:806`), not by any check that the
runtime path is a temp dir. (Here it happens to be one — `tempfile.mkdtemp` at `repeat-control.py:597`
— so the value is right for the wrong reason.)

## S8 — LOW — live windows are hardcoded line numbers, last match wins

`:224-227` accepts `kind == 'open'` in `805..815` and `kind == 'os.symlink'` in `815..825`, taking the
last matching record, with no check that the record's site is `repeat-control.py:811`/`:820` or that
its destination is the expected file. Any `open(...,'wb')` later inserted in that window whose source
text contains `expected`/`golden`/`snapshot` satisfies the clause, and an artifact can emit any lineno
inside the window (S3).

## S9 — LOW — `--control` is not the do-nothing control the contract describes

`control()` (`:103-112`) only re-runs the v2 regex misses and passes iff
`var_expected == TARGET['var_expected']` (`:107`) — i.e. iff v2 **does** resolve one expected
destination, the opposite of the measured value, so it can never pass. It never scores the base
revision. Verified: `--control` → `C2_R41_CONTROL: v2_var_expected=0 v2_symlink_sites=0
C2_R41_CONTROL_PASS=false` (exit 1). The base-revision half of the contract's `do_nothing_control`
therefore rests on a separate run, which does hold:
`--rev a3d6c690…` → `tool_absent=1 … C2_R41_PASS=false` (exit 1). `--control` also reads fixtures from
the working tree (`:123`), not from `--rev`, so it can be evaluated against uncommitted fixtures.

## S10 — LOW — `v2_symlink_sites == 0` is vacuous

The main predicate requires `v2_misses = v2_var_expected == 0 and v2_symlink_sites == 0` (`:239`), but
`V2_WRITE_RE` has no `os.symlink` alternative (`:39-45`, identical to the real v2 `WRITE_RE`,
`tools/write-path-census-v2.py:16-22`). Any symlink-only fixture scores `0` sites by construction:

```
v2_fixture_misses({'var_unflagged':'', 'symlink_unflagged':'os.symlink(...)\n'}) -> (0, 0)
```

That half of the "v2 misses the new classes" control cannot fail. (I confirmed the counter's embedded
`V2_WRITE_RE`/`V2_EXPECTED_RE` are the same patterns as v2's own, so the control measures the right
regex set; it is the fixture shape that makes it unfalsifiable.)

## S11 — LOW — module-level bindings leak into function bodies

`tools/write-path-census-v3.py:211` passes `dict(env)` into every nested statement body, including
`FunctionDef`/`AsyncFunctionDef` bodies, so a module-level binding is visible inside a function that
does not assign it. Python scoping is not modelled; the direction of error is a false-positive
resolution. This is not covered by the declared scope limit.

---

## Where the predicate is genuinely sound (so the L1 does not over-correct)

- The fixtures/mutants trio does bind the artifact to *some* real work: name→binding resolution,
  `os.symlink` recognition, and `args[1]` (not `args[0]`) destination selection are each load-bearing
  for at least one fixture, and all three mutants die on the correct fixture class (S4 evidence).
- A2's re-rooting removed the real defect it names: the old `tests/golden` root let the directory
  token satisfy `EXPECTED_RE` even when the destination argument was flipped; the new
  `tests/fixtures` root makes `symlink_arg` kill for the right reason.
- The base revision cannot pass (`tool_absent=1`), so a do-nothing path is closed.
- v2's pin (`V2_SHA`, `:30`/`:152`) is a real, counter-side literal and is unchanged at both revs.

## Residual risk and verification gaps

- I did not run the counter at the measurement revision (kill rule). The pass/fail numbers quoted for
  the lane are from the base revision, `--control`, `--selftest`, and my scratch lanes only. The live
  line numbers `811`/`820` were read at the measurement candidate `b37ce97`; `tools/repeat-control.py`
  is unmodified at that commit (it is not in `git status`), so they hold for the deciding run unless a
  further commit lands.
- The two false-pass demonstrations (S1, S3) are scratch-lane constructions: they prove the predicate
  is forgeable, **not** that the lane's committed tool is forged. `tools/write-path-census-v3.py` at
  `095924a7…` resolves the two live sites for real (its `--file` output matches `repeat-control.py`
  for 811/820), and its three mutants die semantically.
- No tool was installed or upgraded for this seat.
- I did not evaluate C1, the scorecard table, the lesson or the entry; another seat owns each.

Severity order is the order a fix should take: S1 (in-process execution) and S3 (live self-attestation)
are the two that a dishonest or merely careless tool could walk through; S2 is what makes any such
walk-through look pinned.

Report: .ufo/waves/round-41/w1/ReviewC2Predicate.md

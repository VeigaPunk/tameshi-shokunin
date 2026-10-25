# ExecV3Selftest — v3 write-path census: pristine + recognizer/mutant legs, freeze and amended fixtures (scratch copies only)

Seat: `L1Tameshi41.ExecV3Selftest` (leaf executor). Round 41, attempt 2, freeze `d4ee4e63a0a4402bd8628fbc80f06bbd8f37d937`, base `a3d6c690bcbf8914551d4f4e8e1612784c1c2046`.

Scope: reproduce the `selftest_exit`, `mutant_resolve_killed`, `mutant_symlink_killed` legs of C2 in **/tmp copies**. The lane checkout was not modified; no counter was run against the tip.

## Axes named
- **A1 kill-power of the variable-resolution recognizer** (`_resolve` env binding at line 70).
- **A2 kill-power of the symlink recognizer** (`_write_call` at line 135).
- **A3 fidelity**: scratch tree layout and fixture bytes identical to the lane, so default and explicit fixture resolution agree.

## Setup (all under /tmp/tameshi-r41-execv3-*)
Mirrored the lane layout inside each scratch root so `FIXTURE_REL` default resolution (script dir → parent → `.ufo/evidence/round-41/census/fixtures.json`) behaves exactly as in the lane:

```
/tmp/tameshi-r41-execv3-{pristine,mutbound,mutsymlink}/tools/write-path-census-v3.py
/tmp/tameshi-r41-execv3-{pristine,mutbound,mutsymlink}/.ufo/evidence/round-41/census/fixtures.json
```

Pinned bytes (verified against `contract.json` before copying):
- tool sha256 `095924a7a165be96e69ff9dad67d3e513d23ba6737c35a0537f898482eef0279` — matches `tool_sha256`
- fixtures sha256 `a4123ce373447563a93ad86c21cc3344f5448f1c6157ba696a7239569a58dc31` — matches `fixtures_sha256`
- all three copies hash identically before mutation.

## A3 — pristine run

```
cd /tmp/tameshi-r41-execv3-pristine
python3 tools/write-path-census-v3.py --selftest
```

- **exit 0**
- stdout (single line, verbatim):

```
WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=0
```

No `FAIL` lines. This is exactly the `EXPECT` table in `tools/write-path-census-v3.py:268-273` and supplies `selftest_exit=0` for C2.

## A1 — mutant: `tools/write-path-census-v3.py:70`

Diff vs pristine (`/tmp/tameshi-r41-execv3-mutbound/tools/write-path-census-v3.py`), one line only:

```diff
@@ -67,7 +67,7 @@
     if isinstance(node, ast.Name):
-        bound = env.get(node.id)
+        bound = None
         if bound is None:
             return '', trace
```

Invocation: `python3 tools/write-path-census-v3.py --selftest` (and again with `--selftest --fixtures <explicit path>`, output byte-identical).

- **exit 1**
- stdout (verbatim):

```
WRITE_CENSUS_V3_SELFTEST: var_unflagged=0 symlink_unflagged=1 literal_unflagged=1 scratch_var=0
FAIL planted var_unflagged: want unflagged=1 got 0
FAIL planted var_unflagged: want expected_sites=1 got 0
FAIL planted scratch_var: want expected_sites=1 got 0
```

Kill mechanism: `env.get` is the only reader of the assignment environment (`_bind` at `:159-166` populates `env`, `_resolve` consumes it), so every variable destination collapses to `''`; the `var_unflagged` fixture loses both its `unflagged` and `expected_sites` credit, and `scratch_var` loses its `expected_sites` credit. → `mutant_resolve_killed=1`.

## A2 — mutant: `tools/write-path-census-v3.py:135`

Diff vs pristine (`/tmp/tameshi-r41-execv3-mutsymlink/tools/write-path-census-v3.py`), one line only:

```diff
@@ -132,7 +132,7 @@
-    if dotted == 'os.symlink':
+    if dotted == 'os.symlink_DISABLED':
         if len(node.args) >= 2:
             return 'os.symlink', [node.args[1]]
```

Invocation: `python3 tools/write-path-census-v3.py --selftest` (and again with explicit `--fixtures`, byte-identical).

- **exit 1**
- stdout (verbatim):

```
WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=0 literal_unflagged=1 scratch_var=0
FAIL planted symlink_unflagged: want unflagged=1 got 0
FAIL planted symlink_unflagged: want expected_sites=1 got 0
```

Kill mechanism: the `_write_call` symlink branch is unreachable, so the symlink site is never classified; only the `symlink_unflagged` fixture fails, confirming the two mutants are independent. → `mutant_symlink_killed=1`.

## Cross-check against the counter's own mutation contract

`.ufo/evidence/round-41/census/measure.py:32-35` declares exactly these two edits:

```
RESOLVE_MARK   = '        bound = env.get(node.id)'
RESOLVE_MUTANT = '        bound = None'
SYMLINK_MARK   = "    if dotted == 'os.symlink':"
SYMLINK_MUTANT = "    if dotted == 'os.symlink_DISABLED':"
```

and scores `killed[name] = int(run.returncode != 0)` at `measure.py:200-205` with `--selftest --fixtures <path>`. Both mutants satisfy `returncode != 0` under that exact invocation, so the counter's `mutant_resolve_killed` and `mutant_symlink_killed` legs should read 1 at the measurement revision.

## Results table

| variant | edit | exit | FAIL lines |
|---|---|---|---|
| pristine `/tmp/tameshi-r41-execv3-pristine` | — | 0 | none |
| mutbound `/tmp/tameshi-r41-execv3-mutbound` | `:70` `bound = env.get(node.id)` → `bound = None` | 1 | 3 (`var_unflagged` ×2, `scratch_var` ×1) |
| mutsymlink `/tmp/tameshi-r41-execv3-mutsymlink` | `:135` `'os.symlink'` → `'os.symlink_DISABLED'` | 1 | 2 (`symlink_unflagged` ×2) |

## Lane containment

- `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin status --porcelain -- tools/write-path-census-v3.py .ufo/evidence/round-41/census/fixtures.json` → empty (both tracked and clean at `HEAD=d4ee4e63a0a4402bd8628fbc80f06bbd8f37d937`, the freeze revision, while this seat ran).
- Re-hashed after the mutant runs: lane tool still `095924a7…eef0279`, lane fixtures still `a4123ce3…9a58dc31`.
- **Superseded while this seat was still running**: the lane committed `b37ce97` at 03:39:24 -0300, moving HEAD off the freeze revision and amending the C2 fixtures pin. The freeze-content results above remain valid *for those bytes*; the re-test against the current pin is in the Addendum. Tool sha is unchanged in both.
- Whole-tree `git status --porcelain` shows only the three pre-existing untracked paths from other seats (`.ufo/evidence/round-41/sources/`, `.ufo/waves/round-41/`, `corpus/knowledge/r41-variable-destination-writes.md`); this seat added only this report file.
- No counter invocation was made; neither `calibration/measure.py` nor `census/measure.py` was executed.

## Tooling

No installs or upgrades were performed (no pacman transaction; the host-wide pause was respected). Runner: host `python3`.

## Risks / limits

- The mutation is a single-token removal, not a behavioural fuzz: it proves the selftest detects loss of each recognizer, not that the resolvers handle every shape. That bound is the contract's `declared_scope_limit` (one-hop-ish, depth four) and is not widened here.
- Scratch copies live under `/tmp` and are not evidence for C2 by themselves; the counter's own temp-file mutants remain authoritative. Byte-identical fixtures and mirrored layout keep them representative.
- Durability: every exit code and every stdout line in this report is recorded verbatim above, so no claim here depends on the `/tmp/tameshi-r41-execv3-*` trees surviving. At 03:45 the external sweep that removed `.ufo/waves/round-35/scratch/` had not touched them (`ls -d /tmp/tameshi-r41-execv3-*` still listed the three freeze-content roots and their captured `.out` files; the amended-content `nf-*` and `of-*` roots were created later and are likewise disposable). Every variant is reproducible from the pinned inputs by the commands quoted above. This report contains no `round-35` or `.ufo/.../scratch/` reference.
- `mutbound` also fails `scratch_var: expected_sites`, i.e. that fixture is not purely an `unflagged` probe — worth keeping in mind when reading the counter's `scratch_var_unflagged=0` expectation, which is unaffected (the mutant run shows `scratch_var` unflagged stays 0, only `expected_sites` drops).

## Addendum — post-freeze contract amendment A2 (observed 03:41–03:48)

Written after the freeze-content runs, because the lane amended the contract underneath this seat. No step here was taken by this seat; the changes came from the lane's own commit and the L1's working tree.

Changed in the lane:
- HEAD moved `d4ee4e6` → `b37ce97` (`round-41: C1 records reconciliation + C2 write-path-census-v3 …`, 2026-10-25 03:39:24 -0300). It rewrote `claims.C2.fixtures_sha256`, `claims.C2.counter_sha256`, `claims.C2.target` and added amendment **A2**, `found_by: wave-1 seat MutFixtureVar`.
- fixtures `a4123ce3…9a58dc31` (freeze) → `20b6254d…a26329` (current; equals HEAD, that path is clean). The diff is exactly two bodies: `symlink_unflagged` root `tests/golden` → `tests/fixtures`, and `literal_unflagged` rewritten from a literal `os.path.join("tests", "expected.json")` destination to a `root = "tests/fixtures"` variable destination.
- counter `.ufo/evidence/round-41/census/measure.py` `5d57c70…ef696` → `83268eff…3ce94c`, adding `ARG_MARK`/`ARG_MUTANT` (`measure.py:36-37`), `killed.get('symlink_arg')` (`:285`, emitted as `mutant_symlink_arg_killed`) and the `ok` requirement at `:257`.
- tool `tools/write-path-census-v3.py` **did not change**: still `095924a7a165be96e69ff9dad67d3e513d23ba6737c35a0537f898482eef0279`, so every `:70` / `:135` line citation above still lands.
- Later, amendment **A5** (C1 counter only) appeared in the contract working tree; the C2 pins above are unaffected by it.

Re-test against the current pinned content, four fresh scratch roots `/tmp/tameshi-r41-execv3-nf-*`, each `python3 tools/write-path-census-v3.py --selftest --fixtures /tmp/tameshi-r41-execv3-nf-<v>/.ufo/evidence/round-41/census/fixtures.json`:

| variant | edit | exit |
|---|---|---|
| `nf-pristine` | — | **0** |
| `nf-mutbound` | `:70` `bound = env.get(node.id)` → `bound = None` | **1** |
| `nf-mutsymlink` | `:135` `'os.symlink'` → `'os.symlink_DISABLED'` | **1** |
| `nf-mutarg` | `:137` `[node.args[1]]` → `[node.args[0]]` (the new A2 mutant) | **1** |

- `nf-pristine` stdout: `WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=0` — identical to the freeze-content run.
- `nf-mutbound` stdout: byte-identical FAIL set to the freeze-content run (the same three lines; quoted in full in the A1 section above).
- `nf-mutsymlink` and `nf-mutarg` stdout: byte-identical to each other — `WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=0 literal_unflagged=1 scratch_var=0`, then `FAIL planted symlink_unflagged: want unflagged=1 got 0` and `FAIL planted symlink_unflagged: want expected_sites=1 got 0`. `nf-mutarg` loses both credits because `_record` computes `unflagged = expected and not scratch and not flagged` and only credits `expected_sites` when `expected` holds (`tools/write-path-census-v3.py:169-178`), so a destination that resolves to `actual.json` scores zero on both.

Expected counter legs at the measurement revision: `selftest_exit=0`, `mutant_resolve_killed=1`, `mutant_symlink_killed=1`, `mutant_symlink_arg_killed=1`.

### A2's justification reproduced independently
On the **freeze** fixtures the same `:137` argument mutant **survives**: `/tmp/tameshi-r41-execv3-of-mutarg` (freeze fixtures `a4123ce3…`, arg mutant only) → **exit 0**, stdout `WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=0`. Mechanism is the one A2 names: `EXPECTED_RE` matches the bare directory token `golden`, so even with the destination argument pointing at `actual.json` the resolved text still contains `tests/golden` and the site keeps its expected credit. With the root at `tests/fixtures` no token matches and the mutant dies. A2 is load-bearing, not cosmetic.

### Residual scope note (not a blocker, and not a request to change the contract)
- After A2 no planted fixture carries a literal destination: `literal_unflagged` is now `root = "tests/fixtures"` plus `os.path.join(root, …)`. The literal-on-one-line parity class the fixture is named for is no longer asserted directly. It is only partly subsumed — literal destinations and variable destinations both funnel through the same `_resolve` Constant/join branches, so a regression there still kills `var_unflagged` — but nothing now pins the literal shape itself.
- `tests/fixtures` (like `tests/golden` before it) does not exist in the repo. It is a synthetic token inside planted snippet text, not a repo-relative citation, so C1's m8 class is not involved.

# ReviewV4Source — round 42 wave 2 (FALSIFY), seat L1Tameshi42.ReviewV4Source

Attacked: `tools/write-path-census-v4.py` at integration tip `a21845f523b75adbd3e3f7a62af91294db224ad9`
(sha256 `784de4c0feef3364c4444632788af7ebb57d53032b79f60cc4330c094d122fe5`, identical in the lane and in the scratch clone),
compared with `tools/write-path-census-v3.py`. Access date 2026-10-25.

Method: a scratch clone was made with `git clone --shared` into `/tmp/tameshi-r42w2-ReviewV4Source-probes/lane`, checked out at `a21845f`.
Both tools' `classify_source` were imported in-process from that clone; 16 attack probes were run (`probes.py`), plus a lane-wide
differential (`diff_lane.py`, all 172 tracked `*.py`), cost probes, and v4 `--selftest`. No counter was run. No lane writes other than this file.
LSP: no language server was reachable from this harness, so caller and definition checks used text grep over a 695-line single module,
together with AST execution of the probes. The grep results are not semantic proof; the probe outputs are the evidence.
Tools installed: none.

## Findings by severity

### HIGH — v4 hides true positives that v3 reported (it sets `explicit_out` or `scratch` when it should not)

**H1. Function parameters do not shadow outer bindings, so `explicit_out` is borrowed from a module global.**
- `tools/write-path-census-v4.py:428-430`: a function body is walked with `dict(env)`, the module env at `def` time, and its parameters are never removed from it.
- `:296-298`: `_out_flag` consults `env` before `_param_args`.
- Effect: in `def emit(ns): open(ns.out + "/expected.json", "w")` after a module-level `ns = ap.parse_args()`, the parameter is resolved to the global parser namespace.
- Probe P01: the caller passes an object with `out = "tests/golden"`.
  - v3: `unflagged: true`.
  - v4: `"explicit_out": true, "unflagged": false, "resolved": "ap.parse_args()/out/expected.json argparse --out"`.
- The same root cause feeds `scratch` through `_resolve` (`:176-181`). That leak is inherited from v3, but only v4 turns it into a silencing `explicit_out`.

**H2. A name that is not in `env` is assumed to be the enclosing module function's parameter.**
- `:424-426`: a nested `def` keeps the outer `ctx.func`.
- `:237-239`, `:299`: `_param_args` matches by name only.
- `_bind` (`:342-353`) never binds `for` targets, comprehension variables, or nested-function parameters.
- Probe P02: `def emit(dest_dir): def inner(dest_dir): open(join(dest_dir,"expected.json"),"w"); inner("tests/golden")`, with `emit(ns.out)` from `--out`.
- Probe P03: `for dest_dir in ["tests/golden"]: open(join(dest_dir,"expected.json"),"w")` inside `emit(dest_dir)`.
- Both: v3 `unflagged: true`; v4 `"explicit_out": true, "unflagged": false`.

**H3. Starred arguments misalign the parameter-to-argument mapping.**
- `:247-250`: v4 rejects only when the selected argument itself is `ast.Starred`. A starred argument earlier in the call shifts positions.
- Probe: `def emit(blob, dest_dir, extra)` is called as `emit(*pair, ns.out)` with `pair = ("{}", "tests/golden")`.
- The real `dest_dir` is `"tests/golden"`. v4 output `[(3, True, False)]`, i.e. `explicit_out=True`, `unflagged=False`.

**H4. The attribute-ambiguity rule misses non-plain assignments, so a rebound attribute reads as scratch.**
- `:119-130` collects only `Assign`, `AnnAssign` and `AugAssign` whose target is directly `self.<attr>`.
- Tuple or starred targets, `for self.x in`, `with ... as self.x`, walrus, and `setattr(self, ...)` are all skipped.
- This contradicts the docstring rule at `:17-20` ("two or more distinct expressions ... leave it unresolved, so it is never read as scratch").
- Probe P09: `__init__` sets `self.root = tempfile.mkdtemp()`; `rebase()` does `self.root, self.n = "golden", 0`.
  - v3: `unflagged: true`.
  - v4: `"scratch": true, "unflagged": false`, with resolved text containing `tempfile.mkdtemp()`.

**H5. v4 drops expected-value sites that v3 counted.** This is a regression in classification, not in write forms.
- `:195-199`: the method-return fold returns only the folded return value. It discards the call's arguments and source text, which v3's Call branch (v3 `:87-93`) kept in `resolved`.
- `:207-209`: the attribute fold replaces `self.<attr>` with the assigned expression. The attribute name, which v3 `:94-96` kept, is lost.
- Probe P07: `open(self.path_for("expected.json"), "w")` with `def path_for(self, name): return name`.
  - v3: `expected: true, unflagged: true`.
  - v4: `"expected": false, "unflagged": false, "resolved": ""`.
- Probe P08: `self.golden_path = Path(sys.argv[1])`, then `self.golden_path.write_text("x")`.
  - v3: `expected: true, unflagged: true`.
  - v4: `"expected": false`, resolved `Path(sys.argv[1])argv...`.
- Not live at `a21845f`: the lane differential shows zero `expected` bit changes. The defect is latent.

### MEDIUM

**M1. Two destinations under the same flag never count as `explicit_out`, so `unflagged` stays true.**
- `:367`: `explicit_out = bool(flags) and len(flags) == len(dests)` compares a *set* of flags with the number of destination arguments.
- For `os.replace` or `os.rename` with both arguments under `--out`, the set has 1 element and `dests` has 2.
- Probe P06: atomic replace `os.replace(Path(ns.out)/"expected.json.part", Path(ns.out)/"expected.json")`.
  - v4: `"explicit_out": false, "unflagged": true`.

**M2. An output option with a repository default still counts as explicit.**
- `Module.__init__` (`:92-99`) ignores `default=`, `required=` and `set_defaults`.
- Probe P04: `ap.add_argument("--out", default="tests/golden")`, then `(Path(ns.out)/"expected.json").write_text(...)`.
  - v4: `"explicit_out": true, "unflagged": false`.
- With no flag passed, this silently rewrites goldens: exactly the hidden update the census is supposed to catch. It is consistent with the contract's wording but not with what "explicit" means.

**M3. Attribute binding is per-class, so a subclass rebinding is invisible.**
- `ClassInfo(stmt)` at `:423` sees only the class being walked.
- Probe P10: base class `H` sets `self.root = tempfile.mkdtemp()`; `class Live(H)` sets `self.root = "tests/golden"`.
  - v4: `"scratch": true, "unflagged": false`; v3: `unflagged: true`.
- Inheritance is not listed in the docstring's out-of-scope list (`:35-43`).

### LOW

- **L1.** `os.path.join` with an absolute later component. `:291-292` checks only `args[0]`. Probe P05: `os.path.join(ns.out, "/repo/tests/golden/expected.json")` gives `explicit_out: true`, although Python discards `ns.out` when a later component is absolute.
- **L2.** Conservative gaps where `unflagged` stays true (false positives, the safe direction):
  - P12, `out = Path(out)` rebinding a parameter: the `env` self-loop exhausts the depth limit (`:296-298`).
  - P13, `self.out = Path(args.out)`: `_out_flag` has no self-attribute branch.
  - P14, `Path(ns.out).joinpath(...)`: not in `PATH_WRAPPERS` (`:69-70`).
  - P15, `tmp = tempfile.mkdtemp(); self.root = tmp`: the attribute is resolved with `{}` at `:208`.
  - The output-flag trace also gives up after about 3 function hops. With chain=3, k=10, `explicit_out=True`; with chain=4, `False`, in 0.00 s. The "depth of eight" in `:35-36` is not a hop count, and that limit is undocumented.
- **L3.** Writes inside `match`/`case` are never visited, in either v3 or v4 (v4 `:427-432` and v3 `:208-213` walk only `body`, `orelse`, `finalbody` and `handlers`; `_calls_in_stmt` skips nested statements). Probe P11: v3 `[]`, v4 `[]`. This is a shared gap, not a v4 regression.
- **L4.** v4 dropped v3's text-mode totals line (v3 `:338`) and the `--fixtures` option (v3 `:312`).
  - `python3 -I lane/tools/write-path-census-v4.py --selftest --fixtures x` → `error: unrecognized arguments: --fixtures x`.
  - Per-site text lines are byte-identical to v3 on the `t.py` probe. Round-42 `measure.py` parses only per-site lines (`V3_LINE`, `:213`), so nothing in this round breaks.
- **L5.** `MAX_DEPTH` went from 4 to 8 (`:71`), which inflates `resolved` text on self-referencing assignments (`p = os.path.join(p,…)`). At width 5, `resolved_len` is 1807 in v3 and 181657 in v4, but takes only 0.004 s. Cost stays bounded.

## What survived the attack

- **No special-casing of fixture names or line numbers.** Grepping v4 for `1682|1685|\b123\b|case_dir|context-capture|registry-replay|publish|F0\d|F10|lineno\s*==|'root'|"root"|\bname\s*==` hits only docstring prose at `:8` and `:12`. The selftest (`:462-642`) uses its own sources and none of the counter fixtures.
- **`explicit_out` and `unflagged` are never both true.** `:385` reads `unflagged = expected and not scratch and not flagged and not explicit_out`. Across all probes and the lane, no record had both bits set.
- **No v3 write form was dropped.** `diff` of the `_write_call` sections printed `WRITE_CALL_IDENTICAL`; `_calls_in_stmt` and `_bind` differ only in signature lines. In the lane differential (`python3 -I diff_lane.py`, 172 files), `sites_v3=500` and `sites_v4=500`, with zero `SITE_DROPPED_BY_V4`, `SITE_ADDED_BY_V4`, `DUP_KEY_V4` or `DUP_RECORD_V4`.
- **No duplicate records.** The collect pass (`:456`) writes into a throwaway `[]`, and `:413-416` uses `continue`, so it never calls `_record`.
- **Bit changes on the lane.** `unflagged` went 1→0 on 4 sites: `context-capture.py:1682` and `:1685` (scratch via `mkdtemp`), `registry-replay.py:123`, and `.ufo/evidence/round-23/replay.py:74`. The last two are `explicit_out`; round-23 has `--out` with `required=True` (`replay.py:28`), so it is correct. `scratch` went 0→1 on 12 non-expected sites. `expected` changed on none.
- **Recursion guards terminate.**
  - Mutual recursion f→g→f is stopped by `seen` (`:235`, `:274`, `:304`) and gives `explicit_out False`, `unflagged True` (conservative).
  - Fan-out up to k=10 runs in ≤0.01 s, because depth runs out after about 3 hops and `:305-306` short-circuits.
  - `_resolve` has no `seen`, but `MAX_DEPTH` bounds it (L5).
- **Selftest and round-41 fixtures pass.** `python3 -I lane/tools/write-path-census-v4.py --selftest` → `WRITE_CENSUS_V4_SELFTEST: cases=15 failed=0`, exit 0. The round-41 v3 fixtures (`var_unflagged`, `symlink_unflagged`, `literal_unflagged`, `scratch_var`) give the same summaries under v3 and v4.

## Residual risk and verification gaps

- **These defects are invisible to the deciding run.** H1–H5 and M1–M3 do not occur in the lane's live tools at `a21845f`, and none of counter fixtures F01–F10 exercises them. The C2 predicate can pass while v4 misclassifies these shapes.
- **Mutation testing will not catch them either.** A mutation seat that kills only F01–F10-visible behaviour leaves them all untested.
- **Suggested counter fixtures:** P01/P02/P03 (shadowing), P07/P08 (v3 expected regression), P09 (tuple rebind), P06 (same-flag replace).
- **Not checked:** behaviour on `AsyncFunctionDef` call collection beyond the code read, and class-level (non-`self`) attribute writes.
- Scratch dir `/tmp/tameshi-r42w2-ReviewV4Source-probes` was deleted before return.

Verdict: BROKEN: v4 silences unflagged expected-value writes that v3 reported (parameter/loop/nested-def shadowing, starred-argument misalignment, and tuple-rebound attributes give false `explicit_out` or `scratch`), and its method and attribute folds drop expected-value detection v3 had (P07, P08). Write forms and site counts are intact, and there is no fixture special-casing.

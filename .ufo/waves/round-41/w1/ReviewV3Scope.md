# ReviewV3Scope — do the docstring's stated non-resolution classes hold?

Seat: `L1Tameshi41.ReviewV3Scope` (read-only). The lane checkout, fleet repo, sibling lanes, jj state
and Git index were not modified; the only writes outside `/tmp` are this report. No tool installs.
Neither counter was run; no deciding run was made.

Contract read first: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-41/contract.json`.
`sha256 tools/write-path-census-v3.py` = `095924a7a165be96e69ff9dad67d3e513d23ba6737c35a0537f898482eef0279`
= C2 `tool_sha256`, so every probe below ran against the pinned bytes. Frozen fixtures blob at the
freeze rev `d4ee4e63…` = `a4123ce373447563a93ad86c21cc3344f5448f1c6157ba696a7239569a58dc31` = C2
`fixtures_sha256` (see the evidence hazard at the end: the *worktree* copy no longer matches).

Scratch: `/tmp/tameshi-r41-reviewv3scope-NH4YwK/` (alive at 03:47). My seat cites neither
`.ufo/waves/round-35/scratch/` nor `scratch-evidence/`, so the round-35 scratch change needs no
citation rewrite here; for the record I verified it read-only in `mado-shokunin`: commit `4efaf63`
(`2026-10-25T03:43:55-03:00`, "checkpoint the 235 seat evidence files and drop the 3.2 GB mutant
trees") **adds** (235 × `A`, no `R`) a snapshot under `scratch-evidence/`; that tree now holds 261
tracked files in 59 seat dirs, while `scratch/` is untracked (`??`, 7 dirs / 3 files) and volatile.
So `scratch-evidence/` is a point-in-time copy, not a move, and a file replaced after 03:43 is not
represented there. My `/tmp` directory is a disposable path; every decisive record — each
`resolved` string, its `expected`/`scratch`/`unflagged` flags, and each runtime destination — is
inlined in the tables below, so this report does not dangle if the directory is swept. Verification
checksums for the six snippet files (taken from the files as written; nothing was rebuilt) were:

```
aee10edb2191ee4cf7ab2772244f7ed502f0a3e1ad06d520a11d9814051d4da0  1_alias_rebinding.py
8633d5201161406cc6cb64aadb4675a595aa30d32772334212447ffb9384172a  2_closure_reassigned.py
b422b42bec697d2330f43ab697505d4c0d1743095e825e90bcdf95a2bfc8e485  3_attribute_reassign.py
cfd232322c29833c9aa42fa08c3e9be90bffa4014d963ffb739042e1c2c0bee4  4_conditional_assign.py
7d3ffb7fc90a3c07a5bdbc8dd5fe2e251e5ab98b594008cc74e13c925b3a046c  5_nonfolding_helper.py
78150fdd0b0b329f83096569f22d6f6c6c15c4953aec4c720aa073267cf5e27d  6_src_dst_conflation.py
```

The exact bodies are in this seat's transcript (`history://L1Tameshi41.ReviewV3Scope`); a rebuilt
copy matching these hashes reproduces the run. `frozen-fixtures.json` in the same directory is
`a4123ce3…` (= the contract pin), regenerable with
`git -C tameshi-shokunin show d4ee4e63:.ufo/evidence/round-41/census/fixtures.json`.

## Method

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/write-path-census-v3.py \
        --file /tmp/tameshi-r41-reviewv3scope-NH4YwK/<snippet>.py
# and, for untruncated `resolved` strings, an import harness:
python3 /tmp/tameshi-r41-reviewv3scope-NH4YwK/dump.py <snippet>.py ...
```

Runtime destinations were established by executing the same binding shapes with `print` instead of a
write (`/tmp/tameshi-r41-reviewv3scope-NH4YwK/semantics_check.py`), so no file outside `/tmp` was
touched:

```
closure A dest = tests/expected.json
closure B dest = /tmp/census-scratch.json
for-body dest = /tmp/census/scratch.json
if-body dest (scratch=True) = /tmp/census/scratch.json
attribute snapshot = /tmp/census/run.bin | golden_blob = /tmp/census/run.bin
out_path("expected.json") = /tmp/census/expected.json
golden_dump("tests") = tests/actual.json
```

The tool's own selftest against the *pinned* fixtures passes:
`WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=0`,
exit `0` (`--fixtures /tmp/tameshi-r41-reviewv3scope-NH4YwK/frozen-fixtures.json`). So the defects
below are scope defects in a tool whose own fixtures pass, not a broken build.

## The five snippets

Docstring claims are at `tools/write-path-census-v3.py:15-21`:
"Aliases, closures over reassigned names, attribute reassignment, conditional assignment, dictionary
and list elements, and any path computed by a function call that does not fold to a literal are
**NOT resolved**."

| Snippet (file:line) | Class as declared | Tool record `expected/scratch/unflagged` — `resolved` | Real destination | Verdict |
|---|---|---|---|---|
| `1_alias_rebinding.py:11` | aliases | no record (`sites=1` for 3 writes) | `tests/golden/actual.json` | site dropped, not "unresolved" |
| `1_alias_rebinding.py:16` | aliases | no record | `tests/golden/actual.json` | site dropped |
| `1_alias_rebinding.py:22` | aliases | `1/0/1` — `os.path.join(root, "actual.json")… os.path.join(root, "expected.json")…` | `expected.json → actual.json` | **resolved** — docstring too broad |
| `2_closure_reassigned.py:10` | closure over reassigned name | `0/1/0` — resolves `/tmp/census-scratch.json` | `tests/expected.json` | **stale resolve: real expected write missed** |
| `2_closure_reassigned.py:21` | closure over reassigned name | `1/0/1` — resolves `expected.json` | `/tmp/census-scratch.json` | **unsupported expected claim** |
| `2_closure_reassigned.py:30` | closure over reassigned name | `0/0/0` — `resolved='out.json'` | `/tmp/late-bind.json` | unresolved, but silently (no flag) |
| `3_attribute_reassign.py:10` | attribute reassignment | `0/0/0` — `resolved='dest'` | `tests/golden/expected.json` | fabricated token `'dest'`, expected write missed |
| `3_attribute_reassign.py:15` | attribute reassignment | `0/0/0` — `resolved='dest'` | `/tmp/census/scratch.json` | fabricated token |
| `3_attribute_reassign.py:25` | attribute reassignment | `1/0/1` — `resolved='snapshot'` | `/tmp/census/run.bin` | **unsupported expected claim** |
| `3_attribute_reassign.py:26` | attribute reassignment | `1/0/1` — `resolved='golden_blob'` | `/tmp/census/run.bin` | **unsupported expected claim** |
| `4_conditional_assign.py:10` | conditional assignment | `1/0/1` — resolves pre-branch `expected.json` | `/tmp/census/scratch.json` when `scratch` | **unsupported expected claim** |
| `4_conditional_assign.py:19` | conditional assignment | `0/1/0` — resolves pre-branch `/tmp/census/run.bin` | `expected.json` or `actual.json` | stale resolve, both branches missed |
| `4_conditional_assign.py:26` | (loop body; not named in docstring) | `1/0/1` — resolves pre-loop `expected.json` | `/tmp/census/scratch.json` **unconditionally** | **deterministically wrong claim** |
| `5_nonfolding_helper.py:25` | non-folding call | `1/1/0` — call text spliced | `/tmp/census/expected.json` | suppressed only by the identifier `scratch` |
| `5_nonfolding_helper.py:30` | non-folding call | `1/0/1` — `… golden_path(root)root` | `root/expected.json` | verdict right, evidence is the callee *name* |
| `5_nonfolding_helper.py:36` | non-folding call | `1/0/1` — `… out_path("expected.json")expected.json` | `/tmp/census/expected.json` | **unsupported expected claim** |
| `5_nonfolding_helper.py:42` | non-folding call | `1/0/1` — `… golden_dump(root)root` | `root/actual.json` | **unsupported expected claim (wrong)** |

`6_src_dst_conflation.py` is an extra probe, outside the five named classes — see finding 5.

## Findings by severity

### 1. HIGH — an attribute *name* is classified as a destination (`3_attribute_reassign.py:25,26`)

`_resolve`'s Attribute branch returns the bare attribute name when the base is unbound
(`tools/write-path-census-v3.py:94-96`: `(base + '/' + node.attr) if base else node.attr`), and `_bind`
never records attribute targets at all (`:142-155` handles only `Name` targets). With
`self.snapshot = os.path.join("/tmp", "census", "run.bin")`, both
`self.snapshot.write_text("x")` and `self.golden_blob.write_bytes(b"x")` are reported
`expected=1 scratch=0 unflagged=1` because `snapshot` / `golden` are `EXPECTED_RE` alternatives
(`:32`), while the `/tmp` marker sitting in the initializer is invisible to `scratch`
(`:163-168`). Real destinations: `/tmp/census/run.bin` (verified above). The docstring calls
attribute reassignment "NOT resolved"; the tool resolves *something* — the attribute's identifier —
and then classifies it, which is worse than leaving it blank. The same mechanism prints
`resolved='dest'` for `self.dest` (`:10`, `:15`), a string that is not a path in the program and
that silently swallows a real `tests/golden/expected.json` write.

### 2. HIGH — a call expression splices the callee name and its argument literals (`5_nonfolding_helper.py:36,42`)

`_resolve`'s Call branch starts from `_src(node)` and then appends each argument's resolution
(`tools/write-path-census-v3.py:87-93`). The call's own source text therefore becomes part of the
"destination": `out_path("expected.json")` resolves to
`… out_path("expected.json")expected.json…` (real destination `/tmp/census/expected.json`), and
`golden_dump(root)` — a function returning `root/actual.json` — resolves to `… golden_dump(root)root`
and is claimed expected purely because the callee is named `golden_…`. This is the exact case the
docstring says is "NOT resolved" (`:19-20`), and it is the only mechanism that makes `:30` pass
(`golden_path(root)` — the resolved text contains no `expected.json` token at all). `:25` is
suppressed from `unflagged` only because the helper is *named* `scratch_path`
(`SCRATCH_MARKERS` contains `'scratch'`, `:33-41`); rename the helper and the same `/tmp` write
becomes an unflagged expected destination.

### 3. HIGH — closures are resolved against the def-time env, both directions (`2_closure_reassigned.py:10,21`)

`_walk_stmts` descends into a `FunctionDef` body with `dict(env)` (`tools/write-path-census-v3.py:208-211`)
and never merges or invalidates; nothing tracks that the closure's `dest` cell is rebound before the
call. `2_closure_reassigned.py:21` therefore reports `expected=1 unflagged=1` for a call that writes
`/tmp/census-scratch.json`; `:10` reports `/tmp/…` for a call that writes `tests/expected.json`. So a
closure over a reassigned name is not "not resolved" — it is resolved to a value the program never
uses at that call, in both a false-positive and a false-negative direction.

### 4. HIGH — bindings made inside a block are dropped, including unconditional ones (`4_conditional_assign.py:26`, `:10`)

Blocks are walked with a copy and never merged back (`tools/write-path-census-v3.py:208-213`), so
*any* binding inside `if` / `for` / `while` / `with` / `try` is invisible after the block.
`4_conditional_assign.py:26` is the decisive case: `for _ in range(1): dest = …/scratch.json` executes
unconditionally before the write (verified: `for-body dest = /tmp/census/scratch.json`), yet the tool
claims `expected=1 unflagged=1` from the pre-loop binding. This is not a "conditional assignment"
caveat — it is a deterministic wrong claim. `:10` shows the `if` form: with `scratch` true the write
goes to `/tmp` and the tool still claims expected; `:19` shows the mirror miss.

### 5. MEDIUM — `os.replace`/`os.rename` source and destination are collapsed into one classification (`6_src_dst_conflation.py:8`, frozen `fixtures.json` `literal_unflagged`)

`_write_call` returns `[node.args[1], node.args[0]]` (`tools/write-path-census-v3.py:131-133`) and
`_record` joins all destinations into one `resolved` string before matching (`:162-165`), so an
expected token on *either* endpoint sets `expected` for the site. `6_src_dst_conflation.py:8` moves
`tests/expected.json` → `build/out.bin` and is reported `expected=1 unflagged=1`; `:13`, the exact
mirror, is reported identically. The docstring does say "both arguments" (`:13`), so recording both is
declared — but the record cannot say *which* endpoint matched, and the counter's field names
(`expected_sites`, `variable_expected`) read as destinations. The pinned `literal_unflagged` fixture
is this very shape: freeze blob record `expected=1 unflagged=1`,
`resolved='os.path.join("tests", "actual.json")… os.path.join("tests", "expected.json")…'` — the
destination is `tests/actual.json`, and `C2`'s target `literal_unflagged=1` is satisfied by the read
side. Structurally, the two live C2 checks are immune (`open` has a single destination; `os.symlink`
records only `args[1]`), so this does not by itself threaten `live_var_*` / `live_symlink_*`.

### 6. LOW — aliases: silently dropped sites, and one alias form the docstring wrongly says is unresolved (`1_alias_rebinding.py:11,16,22`)

`_write_call` matches on `_dotted(func)`/`attr` (`tools/write-path-census-v3.py:112-138`), so
`os_alias.replace(...)` and `from os import rename; rename(...)` produce **no record at all** —
`sites=1` for three write calls. That is consistent with "aliases … NOT resolved" only if "not
resolved" means "not seen"; the consequence is that a genuine expected-value write is neither an
expected destination nor an unresolved site, so the `sites` counter silently undercounts. Conversely
`dest_alias = dest` (`:22`) *is* resolved (`expected=1 unflagged=1`), contradicting the blanket
claim. So the claim is both too broad (destination aliasing works) and mis-labelled (callee aliasing
loses the site).

### 7. LOW — keyword-argument write forms yield zero sites

`open(path=dest, mode="w")`, `os.replace(src=…, dst=…)` and `os.symlink(target=…, dst=…)` all produce
`sites=0` because the branches require positional args (`tools/write-path-census-v3.py:126`, `:132`,
`:136`). The docstring's write-form sentence (`:12-13`) states these APIs without qualifying
positional form, and the failure is silent (zero, not "unresolved"). Consistent with a bounded
recognizer, but not with a reader's reading of that sentence.

## Docstring consistency verdict

The scope paragraph is a limitation claim, and five of the six listed classes are contradicted by
observation:

| Declared class | Observed |
|---|---|
| aliases | callee aliases lose the whole site; destination aliases **are** resolved |
| closures over reassigned names | **resolved** from the def-time env — false positive at `2:21`, false negative at `2:10` |
| attribute reassignment | **resolved to the attribute name** — `3:25,26` unsupported expected claims, `3:10,15` fabricated path token |
| conditional assignment | **resolved to the pre-branch binding** — `4:10` unsupported expected claim; `4:19` stale miss |
| function call that does not fold to a literal | **spliced into the destination text** — `5:36,42` unsupported claims, `5:30` name-only evidence |
| dictionary / list elements | consistent: `m = {"out": …}; os.replace(m["out"], …)` → `resolved='x'` (the other argument only) |

The accurate statement would be: bindings inside blocks and closures are not merged and the
pre-branch/def-time binding is used instead; attribute access falls back to the attribute name; and
any call expression contributes its own source text plus resolved argument literals. The tool never
marks a site unresolved — a miss and an absence look identical (`2:30`, `3:10`).

## Evidence hazard (outside my five-snippet scope, affects what "selftest passes" proves)

The worktree `fixtures.json` is **not** the pinned bytes:

```
sha256sum .ufo/evidence/round-41/census/fixtures.json
20b6254d39a75fb9b09b783131a7cdcaf360c36642e39424343166515aa26329   # contract pin: a4123ce3…
git show d4ee4e63….ufo/evidence/round-41/census/fixtures.json | sha256sum
a4123ce373447563a93ad86c21cc3344f5448f1c6157ba696a7239569a58dc31   # = pin
```

`git status --porcelain` shows it as ` M` (also recorded by `ScoutLiveCensus.md:111`). The diff
changes `symlink_unflagged`'s `root` from `"tests/golden"` to `"tests/fixtures"` and rewrites
`literal_unflagged` to put `expected.json` on the destination argument (freeze blob: on the source).
Both variants still make the selftest exit `0`, so nothing in the round would catch it. Impact: the
counter reads fixtures from the measured revision (`census/measure.py:153`, `git_show(...)`), so a
default-mode run at `d4ee4e63` or `a3d6c690` uses the pinned bytes and is unaffected; but any
worktree-mode run (`--selftest`, `--control`, `--rev work`) scores the drifted bytes, and the
`literal_unflagged` semantics it demonstrates are now the *opposite* of the pinned fixture's. I did
not touch the file and make no attribution.

## Residual risk / verification gaps

- Not run: either counter (kill rule), and the snippets' write calls themselves — runtime
  destinations were established with print-equivalent control flow, not by executing the writes.
- Two live C2 sites inspected statically only (`tools/repeat-control.py:811`, `:820`); `var_rec` /
  `sym_rec` are selected by hard-coded line windows `805-815` / `815-825`
  (`census/measure.py:223-227`), so any line shift in `repeat-control.py` silently yields
  `live_var_lineno=0`. Inside those windows the selection is by `rec['expected']`, so a
  `2_`/`3_`/`5_`-style false positive landing in the window would satisfy `live_var_resolved_v3`
  without resolving the intended variable.
- Findings are demonstration-level (planted snippets), not a measurement of the live corpus; no claim
  is made about how many real sites the recognizer misclassifies.
- `EXPECTED_RE` substring semantics (`snapshot`, `golden`) and `SCRATCH_MARKERS` including
  `'scratch'`/`'tempfile'` mean identifier names drive both classifications; findings 1, 2 and the
  `5:25` suppression all trace to that, not to path resolution.

Tool installs/updates: none.

Finding: `tools/write-path-census-v3.py:94-96` (attribute name as destination), `:87-93` (call text
spliced into destination), `:208-213` (block/closure bindings never merged) produce unsupported
expected-destination claims at `3_attribute_reassign.py:25,26`, `5_nonfolding_helper.py:36,42`,
`2_closure_reassigned.py:21`, `4_conditional_assign.py:10,26`; the docstring's `:15-21` non-resolution
claims do not hold for five of the six listed classes.

Report: .ufo/waves/round-41/w1/ReviewV3Scope.md

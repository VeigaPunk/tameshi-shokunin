source: S153 — ast — Abstract syntax trees (Python 3.15.1 documentation) — https://docs.python.org/3/library/ast.html — snapshot .ufo/evidence/round-41/sources/ast.html sha256 183a4f8c3d593be4c45dc64406df2622ebc7080cf5ca3c0f0102649e57545317 — opened 2026-10-25
source: S154 — pathlib — Object-oriented filesystem paths (Python 3.15.1 documentation) — https://docs.python.org/3/library/pathlib.html — snapshot .ufo/evidence/round-41/sources/pathlib.html sha256 0044cae699c55963a41c93f1f6c2a59fbc3a9e1240a4099a7b14c88534e4f093 — opened 2026-10-25
verified-at: 2026-10-25
recheck: 180d — re-open both committed snapshots and re-locate the two quotes below in the tag-stripped text
ground: F4 (golden / snapshot fixture discipline)

# A literal-line census cannot see a destination held in a variable

## What the sources state

- S153 (CPython's own `ast` reference): "The ast module helps Python applications to
  process trees of the Python abstract syntax grammar." (15 words). The page documents
  the node types the resolver uses — `Name`, `Assign`, `Call`, `Attribute` — and
  `ast.get_source_segment`, which returns the source segment for a node and `None` when
  location information is missing. `iter_child_nodes` yields direct children only;
  `ast.walk` is the recursive walker. The parse keeps a call site and the assignment that
  feeds its argument in one tree, which is the property a line-oriented matcher lacks.
- S154 (`Path.write_text`): "Open the file pointed to in text mode, write data to it,
  and close the file:" (16 words). The signature is `Path.write_text(data, encoding=None,
  errors=None, newline=None)` — it has no destination parameter, so for `Path` the file
  written is the path the method is called on. `Path.write_bytes(data, …)` takes the same
  shape. This is why the receiver, not an argument, is the destination for that write
  form.

Neither source says anything about static analysis of a fixture census. They supply the
two mechanisms the tool uses: a tree that keeps assignment and call together, and the
receiver-as-destination rule for the path-method write form.

## The measured finding

At the round-41 freeze revision, `tools/write-path-census-v2.py` (round 40) reads one
line at a time and requires the expected-value token to be a literal on that line.
`tools/write-path-census-v3.py` resolves it instead. On `tools/repeat-control.py`:

| site | form | what v3's trace resolves | v2 |
|---|---|---|---|
| `:811` | `with open(duplicate_path, "wb")` | the `expected.json` literal under `duplicate_path`, three hops from `scratch = tempfile.mkdtemp(…, dir="/tmp")` at `:597` | write site yes, expected-value destination no — the destination is the bare name `duplicate_path` |
| `:820` | `os.symlink(…, os.path.join(tamper_manifest_symlink, "expected.json"))` | the expected-value destination, rooted at the same `scratch` | no write site at all (`os.symlink` is outside its pattern), and the literal sits on the next line |

The record field is a concatenation of the source segments the resolver consulted, not a
normalized filesystem path: reading it as `…/snap-tamper-duplicate-key/expected.json`
overstates it. `expected=1 scratch=1 unflagged=0` is the honest reading of both rows.

Both live sites are scratch fixtures, so both are correctly exempt from the "unflagged
write path" count. The capability the round adds is **visibility of the destination**,
not a new open write path.

### Known false-positive class (disclosed, not fixed here)

A census over the whole `tools/` directory reports three `unflagged` sites. Two are false
positives: `tools/context-capture.py:1682` and `:1685`. Both are scratch in fact —
`expected_path = os.path.join(directory, "expected.json")` is rooted at
`directory = self.case_dir(name)`, and `self.root = tempfile.mkdtemp(…, dir="/tmp")`.
`_bind` records plain `Name` targets only, so `self.root` never enters the environment,
and a non-folding call still contributes its own source text; the destination therefore
resolves to a non-empty string with no scratch marker, and the tool scores it `unflagged`.
The third, `tools/registry-replay.py:123`, is a real non-scratch write of
`expected.json` into an explicit `--out` directory; the census counts it because an
explicit output flag is not in the update-flag pattern. That is a classification gap, not
a hidden update.

The rule for reading the tool's `unflagged` column is therefore: **verify the base
expression**. The fix (dotted-attribute binding plus a completeness flag, so a destination
whose base does not fold can never score `unflagged`) is routed to the next round; this
round's claim names two live sites and claims no directory-wide count.

`os.replace` / `os.rename` are recorded with both arguments as destinations, so a *read*
of an expected file can be listed beside its write. `tools/repeat-control.py` has no such
site; the seven in `tools/` all resolve `expected=False`, so no measured count changes.

## The method, bounded

Parse with `ast`; walk statements in source order; bind `Name -> value` for plain and
annotated assignment and `with … as`; resolve a destination through `os.path.join`, `+`,
`/`, `JoinedStr` and attribute chains to a depth of four; then classify the resolved text
as expected-value (`expected.json`, `expected.txt`, `.expected`, `golden`, `snapshot`) or
scratch (`/tmp`, `tempfile`, `TemporaryDirectory`, `NamedTemporaryFile`, `mkdtemp`,
`scratch`). The update flag (`--update_goldens`, `--update-goldens`, `--update`,
`update_goldens`) is read from the whole file, not from the call site. A scratch marker
seen anywhere in the resolution trace exempts the site, so a variable rooted in the
scratch directory is exempted rather than mistaken for a repo-level write — while a
variable rooted at a fixture directory that is not scratch stays counted.

## Prior art (adjacent; reported, not absorbed)

Two sibling tools already resolve write destinations through assignments:
`kotodama-shokunin/tools/harness/round_runner_conformance.py` (a five-pass constant
fixpoint to depth 8) and `kotodama-shokunin/tools/harness/receipt_guard_adoption.py`
(a `Resolver` class to depth 6). Both landed 2026-10-19, six days before this lane's v2.
v3 is a **subset** of that machinery — depth 4, no fixpoint, no `__file__`, `with_name` or
`joinpath` — plus three things those do not do: `os.symlink` destinations, the
expected-value / scratch / update-flag classification, and scratch tracing through the
assignment chain. No novelty is claimed for destination resolution as a technique.
`PROVINCE.md` forbids absorbing a sibling's gate code, and one sibling lane does not
satisfy the two-independent-lane admission rule, so this is adjacency: observed, cited and
not absorbed. A reader who wants the stronger resolver should read the sibling's tool.

## What is not claimed

- No universality. Callee aliases and destination-name aliases are not tracked
  consistently, a closure's definition-time environment is used and never invalidated,
  an attribute's own name can stand in for its value, block rebindings are dropped, and a
  non-folding helper is resolved by its name. The scope seat exercises those cases and
  the docstring says the resolver is bounded.
- No dataflow guarantee, no taint tracking, no interprocedural analysis.
- No new gate coverage and no claim about any sibling lane's gates.
- v2 is not deprecated or edited by this entry; its pin stays where round 40 put it.

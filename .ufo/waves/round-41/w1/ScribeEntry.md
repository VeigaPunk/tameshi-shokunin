# ScribeEntry — r41-variable-destination-writes draft (round 41, wave 1)

Seat: read-only scribe. Wrote only this file. Lane checkout, jj state and Git index untouched.

## Behavior

Verified the two registry rows, both snapshot hashes, both verbatim quotes, the two live
sites and v3's declared scope, then produced a 55-line draft of
`corpus/knowledge/r41-variable-destination-writes.md` (limit 60). The draft is reproduced
verbatim below; it is NOT written into the lane checkout.

## Evidence (commands and observed results)

| check | command | observed |
|---|---|---|
| snapshot pins | `sha256sum .ufo/evidence/round-41/sources/*.html` | `183a4f8c3d593be4c45dc64406df2622ebc7080cf5ca3c0f0102649e57545317  ast.html`; `0044cae699c55963a41c93f1f6c2a59fbc3a9e1240a4099a7b14c88534e4f093  pathlib.html` — both match the contract |
| S153 quote | tag-strip + whitespace-normalize `ast.html`, find `The ast module helps Python applications` | FOUND verbatim; 15 words |
| S154 quote | tag-strip + whitespace-normalize `pathlib.html`, find `Open the file pointed to in text mode` | FOUND verbatim; 16 words (source sentence continues with `:`) |
| live sites | `read tools/repeat-control.py:806-823:raw` | `:811 with open(duplicate_path, "wb") as handle:`; `:820 os.symlink(` with dest `os.path.join(tamper_manifest_symlink, "expected.json")` at `:822` |
| live measurement | `python3 tools/write-path-census-v3.py --file tools/repeat-control.py` | `tools/repeat-control.py:811 open expected=1 scratch=1 unflagged=0 …`; `tools/repeat-control.py:820 os.symlink expected=1 scratch=1 unflagged=0 …`; summary `expected_sites=2 parse_errors=0 scratch_expected=2 sites=6 symlink_expected=1 unflagged=0 variable_expected=1` |
| exact records | import v3, `classify_source` on `tools/repeat-control.py`, filter lineno 811/820 | both `expected=true scratch=true flagged=false unflagged=false`; trace base is `tempfile.mkdtemp(prefix="tameshi-r12-repeat-control-selftest.", dir="/tmp")` |
| v3 scope | `tools/write-path-census-v3.py:15-20` | "through assignment, `os.path.join`, `+`, `/` and f-strings, to a depth of four"; `MAX_DEPTH = 4` at `:43`; `ast.JoinedStr` `:75`; `ast.Add, ast.Div` `:83`; `_bind` handles `Assign`, `AnnAssign`, `With` (`:142-153`) |
| v2 limits | `tools/write-path-census-v2.py:16-40` | `WRITE_RE` needs a mode literal on the same line; `EXPECTED_RE` needs a quoted expected token on the same line; no `os.symlink` pattern |
| registry | `grep -n 'S153\|S154' corpus/SOURCES.md`; `grep -c '^| S[0-9]' corpus/SOURCES.md` | rows at `:123` (S153, ast) and `:124` (S154, pathlib), both `mined`, `opened 2026-10-25`, `recheck 180d`, used-by names this doc; 109 rows total |
| statuses | awk over the registry status column | 81 mined / 22 queued / 6 rejected |

`tools/repeat-control.py` is unmodified in the working tree (`git status --porcelain` shows
only ` M corpus/SOURCES.md` and untracked round-41 paths), so the run above measures the
freeze content of that file.

## Gates

- C1 and C2 counters were NOT run, in any mode, including `--rev work`; the one deciding run
  is the L1's. Only the v3 tool's own `--file` mode was invoked, which is not a counter.
- No build, lint or test run (not this seat's assignment).

## Findings

1. Line limit. The draft already present at
   `corpus/knowledge/r41-variable-destination-writes.md` (untracked, mtime
   `2026-10-25 03:38:33 -0300`) is **62 lines**, over the 60-line limit. My draft is 55.
2. Quote word counts in that file are wrong: it says "(16 words)" for the S153 quote and
   "(17 words)" for the S154 quote; measured counts are 15 and 16. My draft drops the counts.
3. That file's sentence "the round's scope seat exercises five of them" is not observable in
   any seat output I read; my draft drops it.
4. Wording conflict, reported verbatim. The assignment says
   "the bounded scope (depth 4; assignment/os.path.join/+/f-string only; no aliases or
   closures)"; `tools/write-path-census-v3.py:15-20` and the contract's
   `declared_scope_limit` also include `/` (`ast.Div`, `tools/write-path-census-v3.py:83`).
   My draft lists `/` to match the tool.
5. Seat conflict, reported verbatim. The task says "Draft
   /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/r41-variable-destination-writes.md"
   while the seat says "your only write is your own report file. Never edit the lane
   checkout". Resolved by putting the full draft here and leaving the lane file untouched.
6. Registry dependency is satisfied as of this read: S153/S154 exist at
   `corpus/SOURCES.md:123-124` and are `mined`, so the draft's header does not cite an
   unmined id. The registry grew 107 → 109 rows; the SCORECARD standing row (m6) is not this
   seat's file and was not touched.
7. No tool installs or upgrades were needed or performed.

## Touched surfaces

- Wrote `/.ufo/waves/round-41/w1/ScribeEntry.md` (this file) only.
- Scratch: `/tmp/tameshi-r41-scribeentry/draft.md` (55-line copy of the draft).
- Did not edit `corpus/knowledge/r41-variable-destination-writes.md`, `corpus/SOURCES.md`,
  any counter, any tool, the jj state or the Git index.

## Out of scope

Committing, pushing, updating the SCORECARD standing count, editing the on-disk knowledge
file, and running either deciding counter.

## Artifact paths

- Report: `.ufo/waves/round-41/w1/ScribeEntry.md`
- Draft scratch: `/tmp/tameshi-r41-scribeentry/draft.md` — convenience copy only. The
  fenced draft above is the durable evidence locus; the two were diffed identical (55
  lines) at write time, and if `/tmp` disappears nothing is lost.
- Contract: `.ufo/evidence/round-41/contract.json`

## Draft (verbatim, 55 lines)

```markdown
source: S153 — ast — Abstract Syntax Trees (Python 3.14 documentation) — https://docs.python.org/3/library/ast.html — snapshot .ufo/evidence/round-41/sources/ast.html sha256 183a4f8c3d593be4c45dc64406df2622ebc7080cf5ca3c0f0102649e57545317 — opened 2026-10-25
source: S154 — pathlib — Object-oriented filesystem paths, Path.write_text (Python 3.14 documentation) — https://docs.python.org/3/library/pathlib.html — snapshot .ufo/evidence/round-41/sources/pathlib.html sha256 0044cae699c55963a41c93f1f6c2a59fbc3a9e1240a4099a7b14c88534e4f093 — opened 2026-10-25
verified-at: 2026-10-25
recheck: 180d — re-open both committed snapshots and re-locate the two quotes below
ground: F4 (golden / snapshot fixture discipline)

# A literal-line census cannot see a destination held in a variable

## What the sources state

- S153 (`ast`): "The ast module helps Python applications to process trees of the
  Python abstract syntax grammar." A parsed module exposes `Name`, `Assign`, `Call`
  and attribute nodes, so a call site and the assignment feeding its argument sit in
  one tree, and `ast.get_source_segment` recovers a node's own bytes.
- S154 (`Path.write_text`): "Open the file pointed to in text mode, write data to it,
  and close the file". The receiver is the destination: a path method writes to the
  object it is called on, not to an argument. The same holds for `write_bytes`, which
  is why the receiver, not the argument list, is the destination to resolve.

Neither source describes a fixture census. They supply the two mechanisms the tool
relies on: a tree that keeps assignment and call together, and the
receiver-as-destination rule for the path-method write form.

## The measured finding

At the round-41 freeze revision, `tools/write-path-census-v2.py` reads one line at a
time and needs the expected-value token to be a string literal on that line.
`tools/write-path-census-v3.py` resolves it instead. On `tools/repeat-control.py`:

| site | form | v3 | v2 |
|---|---|---|---|
| `:811` | `with open(duplicate_path, "wb")` | expected, scratch; `expected.json` under a directory traced to `scratch` and `tempfile.mkdtemp(..., dir="/tmp")`; unflagged false | write site, no expected-value destination |
| `:820` | `os.symlink(..., os.path.join(tamper_manifest_symlink, "expected.json"))` | expected, scratch through the same traced base; unflagged false | not a write site (`os.symlink` is outside its pattern) |

Both live destinations are expected-value paths, and both are scratch-exempt, so the
unflagged-write-path count stays zero. What round 41 adds is visibility of the
destination, not a new open write path. A non-scratch unflagged site found later is a
finding against this lane's tools, not part of this entry.

## The method, bounded

Parse with `ast`; walk statements in source order; bind `Name -> value` for plain and
annotated assignment and `with ... as`; resolve a destination through `os.path.join`,
`+`, `/` and f-strings, to a depth of four. Aliases and closures over reassigned names
are not resolved, and neither are attribute reassignment, conditional assignment, or
any path computed by a call that does not fold to a literal. A scratch marker anywhere in
the resolution trace exempts the site.

## What is not claimed

- No universality: a bounded recognizer, not a static analyzer.
- No dataflow, taint or interprocedural guarantee.
- No gate coverage: no claim about any gate, any sibling lane, or every write in the
  tree.
- v2 is not deprecated or edited; its pin stays where round 40 put it.
```

# ExecParaphrase — scratch paraphrase of the `write_bytes` fixture (axis: depth)

Seat: executor (leaf). Lane checkout never edited; all work in `/tmp/tameshi-r40-ExecParaphrase/`.
No default-mode counter run was performed (only `--selftest` and scratch copies).

## Setup (exact)

```
mkdir -p /tmp/tameshi-r40-ExecParaphrase
cp tools/write-path-census-v2.py /tmp/tameshi-r40-ExecParaphrase/write-path-census-v2.py
cp .ufo/evidence/round-40/census/fixtures.json /tmp/tameshi-r40-ExecParaphrase/fixtures.json
```

```
$ sha256sum /tmp/tameshi-r40-ExecParaphrase/write-path-census-v2.py
4022853295882c5a11e192274e9215ea5a008e54eb0a2f77a8a2365f522d878b  /tmp/tameshi-r40-ExecParaphrase/write-path-census-v2.py
```

Scratch copy sha equals the frozen C1 pin (`contract.json` `claims.C1.tool_sha256`).

## Paraphrase fixture

`path.write_bytes(b"x")` — destination inside a variable, **no** quoted `expected.json`
literal on the write line. Two bindings were tested, plus same-line controls
(`/tmp/tameshi-r40-ExecParaphrase/cases.py`):

```
$ python3 /tmp/tameshi-r40-ExecParaphrase/cases.py
A  var_only                write_sites=1 unflagged=0
B  var_bound_prev_line     write_sites=1 unflagged=0
B2 var_bound_expected_ext  write_sites=1 unflagged=0
C  literal_control         write_sites=1 unflagged=1
D  comment_quote           write_sites=1 unflagged=1
E  bound_same_line         write_sites=1 unflagged=1
```

Bodies (B is the paraphrase the task asks for):

| case | body |
|---|---|
| A | `path.write_bytes(b"x")` |
| B | `path = out / 'expected.json'` ⏎ `path.write_bytes(b"x")` |
| B2 | `path = out / 'case.expected'` ⏎ `path.write_bytes(b"x")` |
| C | `(out / 'expected.json').write_bytes(b'x')` |
| D | `p.write_bytes(b'x')  # mirrors 'expected.json'` |
| E | `p = out / 'expected.json'; p.write_bytes(b'x')` |

## Answer: does `classify_text` count it?

**No.** `write_sites=1`, `unflagged=0`. The write *form* is recognised, but it is not
credited as an expected-artifact write.

Mechanism, `tools/write-path-census-v2.py:32-42`:

- `WRITE_RE` matches `.write_bytes\s*\(` on the line → `write_sites += 1` (`:36-41`).
- `EXPECTED_RE` is applied to **that same line only** (`:40`) and requires a *quoted*
  string containing `.expected` / `expected.txt` / `expected.json` / `golden` / `snapshot`
  (`:23-25`). In A/B/B2 the name lives in an earlier assignment, so `EXPECTED_RE` misses
  and `unflagged` stays 0.

The recognition is literal-and-line-scoped, confirmed by the boundary:

- `B` (two-line binding) → 0, but `E` (same binding joined with `;` on one line) → 1.
  Only line layout changed, not semantics.
- `D` shows the dual error: a quoted `expected.json` inside a **comment** on a write line
  is credited → `unflagged=1` false positive. `EXPECTED_RE` proves the literal appears
  somewhere on the line, not that it is the destination.

## Consequence for the tool's own detector

Adding the paraphrase as an *extra* fixture key is silently ignored (the selftest's
`expect` dict is the fixed five names, `tools/write-path-census-v2.py:54-60`):

```
$ python3 write-path-census-v2.py --selftest --fixtures fixtures-plus.json
WRITE_CENSUS_V2_SELFTEST: bytes_unflagged=1 replace_unflagged=1 bytes_flagged=0 replace_flagged=0 scratch_replace=0
rc=0
```

Substituting the paraphrase for the planted `bytes_unflagged` body is caught:

```
$ python3 write-path-census-v2.py --selftest --fixtures fixtures-swapped.json
WRITE_CENSUS_V2_SELFTEST: bytes_unflagged=0 replace_unflagged=1 bytes_flagged=0 replace_flagged=0 scratch_replace=0
FAIL planted bytes_unflagged: want unflagged=1 got 0
rc=1
```

## v1 comparison (embedded classifier from `census/measure.py:v1_classify`)

```
A  var_only              v1_writes=1 v1_unflagged=0
B  var_bound_prev_line   v1_writes=1 v1_unflagged=0
C  literal_control       v1_writes=1 v1_unflagged=0
```

v1 misses both the paraphrase **and** the literal `expected.json` control (its
`V1_EXPECTED_RE` has no `expected.json` alternative, `census/measure.py:38-40`), so this
paraphrase does **not** widen the v1/v2 discrimination gap. It is a v2 boundary, not a
regression of the pinned claim.

## Live-corpus check for a latent false negative

Same recognizer run read-only over the lane (`/tmp/.../cases.py`-style scan):

- `tools/` `*.write_bytes` expected-artifact hits: **1** — `tools/registry-replay.py:123`
  `(out / 'expected.json').write_bytes(encode({'schema': 'command-binding-expected-v1',`
  (literal on the write line, exactly the contract's live case).
- Repo-wide (`*.py`, excluding `.git`, `.ufo`, `node_modules`): **77** `.write_bytes`
  sites; **5** have expected-ish names in the 3 preceding lines, and all five write a
  *different* filename (`bundle.json`, `observations.json`, `live-dependent.json`), none
  bound to `expected.json`. E.g. `tools/registry-replay.py:125`
  `(out / 'live-dependent.json').write_bytes(...)`.

So no live site is currently miscounted; the literal dependency is a latent blind spot,
not an active census error.

## Effect on the frozen predicate

None. `C1` requires the planted `bytes_unflagged` literal to score 1 (`fixtures.json:2`),
which it still does; the paraphrase is a new, unclaimed form. C1's capability wording —
"a string literal expected.json on a .write_bytes call" (`contract.json:22`) — is exactly
as narrow as observed; the paraphrase sits outside it. No counter was run in default mode.

## Risks

- Refactoring any census-tracked write to `p = out / 'expected.json'` + `p.write_bytes(...)`
  drops the C1 count from 1 to 0 while the selftest stays green, because the planted
  fixture is a single-line literal. The selftest cannot detect this class by construction.
- `EXPECTED_RE` has no destination anchoring: comment text or an unrelated quoted
  `expected.json` on a write line is credited (case D).

## Lane untouched

```
$ sha256sum tools/write-path-census-v2.py tools/write-path-census.py
4022853295882c5a11e192274e9215ea5a008e54eb0a2f77a8a2365f522d878b  tools/write-path-census-v2.py
bc8c660c56f871f85dad8912be28446293fd63f62b4fd1c16eb153f7a27edc62  tools/write-path-census.py
```

Both match the frozen pins. `git status --porcelain -- tools .ufo/evidence/round-40`
shows only the pre-existing `?? .ufo/evidence/round-40/after/`.

No installs, updates, or package transactions were performed.

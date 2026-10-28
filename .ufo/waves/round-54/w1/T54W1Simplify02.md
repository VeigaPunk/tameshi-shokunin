# T54W1Simplify02 — the `scratch_root` cell: one sentence × seven rows

**Item.** The `scratch_root` cell is one ~45-word sentence repeated on seven rows of
`tools/registry.json`. Is that the right home, or does one registry-level note plus a
one-word cell govern the same behaviour with less duplication? What reads those rows?
Give the deletion, with its cost. No edits.

**Verdict.** The sentence's right home is the knowledge note, where it already is; the row's
right home is a *pointer that still carries the three arm tags*. A registry-level note plus a
one-word cell does **not** govern the same behaviour: it turns the only reader red, and the note
it adds would be a third home that nothing reads. I would delete the duplicated clauses from the
seven cells (266 B → 174 B each, −644 B) and leave the note as sole authority. Details, and the
one wording defect this exercise surfaced (`tools/env-diff.py:186`), below.

Premise correction first, because the size drives the decision: the cell is **266 bytes / 37 words**,
not ~45 words, and the seven copies are **1862 B of a 28902-byte file** (6.4 %).

```
rows with the cell: 7   landed cell: 266 bytes, 37 words
landed total in registry: 1862 bytes; registry file: 28902 bytes
```

---

## 1. What reads the cell

Exactly one thing, and it is round-scoped:

| Reader | Reads `scratch_root`? | Evidence |
|---|---|---|
| `tools/registry-check.py` (the only file in the lane that opens `tools/registry.json`) | **no** — the key does not occur in it | `grep -rln "registry\.json" tools/*.py` → `tools/registry-check.py` alone (the lane has no `scripts/`; the census script lives at the fleet root); `grep -c '"scratch_root"' tools/registry-check.py` → `0` |
| `.ufo/evidence/round-54/c2/measure.py:148` (C2's `docs` arm) | yes, three substrings | below |
| `corpus/knowledge/scratch-root-contract.md` | prose only ("the registry rows say so", `:29-30`) | `:51` names "7/7 rows carrying the `scratch_root` cell" |

So after round 54 closes and its evidence counter is no longer the live reader, **the cell has no
reader at all** while remaining a third live copy of a rule that SKILL.md (`:32-39`) and the note
(`:11-15`) already state. That is weight with no consumer — the case for shrinking it.

`registry-check` validates a *closed* set of row fields and ignores everything else:
`name` (`:199`), `kind` (`:209`), `argv` (`:214`), `expect.exit` / `expect.stdout_contains`
(`:224`), `timeout_s` (`:238`), `source` against `SOURCE_RE` (`:257`), `status` (`:263`),
`tags`, and the booleans `external`/`discriminating` (`:274`). `scratch_root` is not in that list,
and an unknown key is not an error (`registry_errors`, `tools/registry-check.py:181-283`).

Two receipts make that concrete — garbage in the cell still passes, a prose `source` does not:

```
$ python3 tools/registry-check.py --root LANE --registry variants/C_one_word.json --only env-diff-selftest
ROW env-diff-selftest expect=0 got=0 held
REGISTRY_CHECK: held=1/1 superseded=0
rc=0

$ python3 tools/registry-check.py --root LANE --registry variants/E_typo_drops_empty_token.json --only env-diff-selftest
ROW env-diff-selftest expect=0 got=0 held
REGISTRY_CHECK: held=1/1 superseded=0
rc=0

$ python3 tools/registry-check.py --root LANE --registry variants/G_bad_source.json --only env-diff-selftest
REGISTRY_CHECK: could-not-evaluate (registry invalid: rows[0].source must be <file>@<7-40 hex rev>:<line>, got 'see the scratch-root note')
rc=2

$ python3 tools/registry-check.py --root LANE --registry variants/H_unknown_row_and_top_key.json --only env-diff-selftest
ROW env-diff-selftest expect=0 got=0 held
REGISTRY_CHECK: held=1/1 superseded=0
rc=0
```

`E_typo` is the landed sentence with the word `empty` replaced by `blank`; `C_one_word` replaces every
cell with `"contract"`; `H` adds a free-text row key and a top-level `registry_note` no reader reads.
Receipts: `T54W1Simplify02-receipts/registry-check-silent.out`, `registry-check-contrast.out`.

**Consequence for the item's question.** A registry-level note is *silently legal* (H proves it) and
*invisible* to every reader — so it is not a home for the rule, it is a second dead copy of a note
that already exists at `corpus/knowledge/scratch-root-contract.md`.

## 2. What the docs arm actually measures

`TOOLS` is imported from the frozen counter, and the loop is copied verbatim from
`c2/measure.py:147-150`; `docs-arm-probe.py` re-implements nothing:

```python
    for _name, _path, _arg, row_name in TOOLS:
        cell = (by_name.get(row_name) or {}).get('scratch_root')
        if isinstance(cell, str) and all(k in cell for k in ('TMPDIR', 'empty', 'could-not-evaluate')):
            docs += 1
```

The counter's own declared requirement is the same three tokens — `c2/measure.py:19-21`:
"every cell names TMPDIR, the empty-string arm and the could-not-evaluate exit class" — and
`contract.json:24` asks only that "the seven registry rows carry the `scratch_root` cell". No
frozen text requires the sentence, its parentheticals, or its provenance suffix.

Seven variants, run through that block (`receipts/docs-arm-probe.out`, `arm-absence.out`,
`final-candidate.out`):

| Variant | cell | docs | C2 `total` |
|---|---|---|---|
| A as landed | 266 B / 37 w | **7/7** | +0 |
| P_final (recommended) | 174 B / 21 w | **7/7** | **+0** |
| P1 arms-one-line | 162 B / 20 w | 7/7 | +0 |
| P2 pointer-only | 83 B / 4 w | 7/7 | +0 |
| C one-word | `contract` | **0/7** | **+7** |
| C + top-level note | `contract` + `notes.scratch_root` = full sentence | **0/7** | **+7** |
| E typo (`empty`→`blank`) | 266 B | 0/7 | +7 |
| F tokens only, no anchor | `TMPDIR empty could-not-evaluate` | **7/7** | +0 |
| cell absent / `null` | — | 0/7 | +7 |

Two facts fall out:

1. **The arm cannot tell the essay from three words.** F scores 7/7 while naming no file, no
   behaviour and no anchor. So the 266-byte wording is not load-bearing for C2 — only the three
   tokens are. Nothing measures the prose that makes the duplication expensive.
2. **The one-word cell is the one shape that fails.** `C` and `C+note` both score 0/7, i.e.
   `C2_R54_PASS=false` (`total += len(TOOLS) - docs` = 7). It is not a cheaper spelling of the
   rule; it is a red claim.

## 3. The deletion I would make

Replace all seven cells with one line — arms kept as tags (so the row still declares the behaviour),
clauses already stated in the note and in SKILL dropped, the note left as sole authority:

```
TMPDIR set-unusable => exit 2 could-not-evaluate (value named); empty => unset; usable => scratch under TMPDIR, nothing under /tmp — corpus/knowledge/scratch-root-contract.md
```

```
P_final (recommended)  174 B / 21 w  docs=7/7  total+=0  registry-B total=1218
saving: 644 bytes of 28902 (2.2%)
```

What the 92 deleted bytes per row remove:

- `(the value is named, no traceback)` → `(value named)`: the "no traceback" half is the note's
  `:15` ("the value is named, the class is printed, nothing falls back to `/tmp`") and SKILL
  `:37` ("never a traceback, never exit 1", C0 blob). `no traceback` is the only phrase lost at
  registry granularity, and no artifact requires it in the registry: `grep -n "never a traceback"`
  finds it in `corpus/knowledge/scratch-root-contract.md:15`, `SKILL.md:37` and four tool
  docstrings (`tools/bash-witness-study.py:206`, `tools/evidence-disposition.py:192`,
  `tools/pin-disposition.py:162`, `tools/env-diff.py:33`) — all still say it after the deletion.
- `the platform default applies` → `unset`: the note's table row `:13` carries the
  resolver (`tempfile.gettempdir()`), SKILL `:33-35` the S-id citations (S278:163-165, S279).
- `a usable TMPDIR holds every mkdtemp` → `scratch under TMPDIR`: see §4 — the wide claim is true
  in effect and false by construction, and the narrow phrase stops asserting it.
- `(round 54, `: the round tag is provenance; the row already carries a validated `source` anchor
  for its command (`<file>@<rev>:<line>`, `tools/registry-check.py:257`), and the note is the
  round's artifact, named in the cell and cited by SKILL `:32-39`.

**Cost.** (i) A reader who sees only `tools/registry.json` now needs one hop to the note, whose path
the cell still carries — no fact becomes unreachable. (ii) The byte saving is small (2.2 % of the
file); the gain that matters is the *home count*: the rule goes from three restatements
(SKILL `:32-39`, note `:11-15`, seven cells) to two, with the cells reduced to a pointer + tags.
(iii) The frozen counter is untouched: verdict measured byte-neutral (7/7 → 7/7, `total` +0), so the
instrument is not fitted to the change. (iv) The drift surface shrinks but does not close — seven
sites still hold three tokens each, and `registry-check` still validates none of them (§1). Closing
it needs a *validated* cell shape (below), which is a `registry-check` + counter change and not this
round's move.

**P2, the pointer-only cell (83 B, −1281 B), is cheaper and I would not take it now.** It falsifies
the note's own last line of that paragraph — `corpus/knowledge/scratch-root-contract.md:29-30`:
"a lane declaration that follows the resolver the lane actually calls, and the
registry rows say so" — because pointer-only rows would no longer say so. So P2 costs a second file
edit (the note) to save 637 B more than P_final. Wrong trade for one round.

**Frontier (out of scope here, recorded for a later round):** make the cell a validated shape, e.g.
`"scratch_root": {"contract": "corpus/knowledge/scratch-root-contract.md", "arms": ["unset","empty","unusable"]}`,
teach `registry_errors` (`tools/registry-check.py:181-283`) to check it — turning the free-text cell
into a field the gate can fail — and change C2's arm to assert the contract path and the arm set
rather than three substrings, which F passes today. That is the durable fix; it cannot be done
in-round because it edits the frozen instrument while the instrument is scoring the round.

## 4. Wording defect the exercise surfaced (supporting, not the item)

While checking whether the cell's claims still resolve at C0 I checked every scratch-allocation
site at the content commit — `receipts/alloc-sites-at-c0.out`, run over `git show C0:tools/<tool>.py`:

```
c0/bash-witness-study.py    1259  strict=True
c0/bash-witness-study.py    1264  strict=False     # dir=private_root, itself under the strict root
c0/context-capture.py         27  strict=False     # docstring mention, not a site
c0/context-capture.py       1638  strict=True
c0/env-diff.py                80  strict=True
c0/env-diff.py               186  strict=False     # bare: no dir=
c0/evidence-disposition.py  2370  strict=True
c0/pin-disposition.py        725  strict=True
c0/registry-check.py         780  strict=True
c0/registry-check.py         930  strict=True
c0/repeat-control.py         611  strict=True
```

Ten real allocation sites; nine route through `strict_scratch_root()` (bash-witness `:1264` via a
child of it). One does not — `tools/env-diff.py:186`,
`with tempfile.TemporaryDirectory(prefix="tameshi-r21-envdiff-pin.") as tmp:` — and on a
set-but-unusable `TMPDIR` it falls back to `/tmp` silently, the exact behaviour the contract forbids:

```
=== C0 blob tools/env-diff.py, TMPDIR=/nonexistent
TMPDIR = /nonexistent/tameshi-bare
strict_scratch_root() raises ScratchRootUnusable: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/nonexistent/tameshi-bare' (could-not-evaluate)
bare TemporaryDirectory (the :186 form) -> /tmp/tameshi-r21-envdiff-pin.adjiay95
```

It is shielded today by ordering only: `selftest()` (`:162`) calls `execute()` at `:180`, whose
`:80` raises before `:186` is reached (`receipts/bare-site-at-c0.out`; `grep -n "execute(" tools/env-diff.py`).
The cell's wide clause — "a usable TMPDIR holds every mkdtemp and nothing is created under /tmp" —
is therefore true for the usable arm (both sites land under `TMPDIR` because `gettempdir()` honours
it) but it is true *by accident of `gettempdir()` and call order*, not by construction. A prose
sentence repeated seven times cannot notice that; the note's narrower frame can ("Every lane tool
that allocates scratch through a `strict_scratch_root()` helper", `:3-4`). This is a maintainability
finding for the tool, not a live failure, and I made no edit to it.

## 5. Scope, opening list, cleanup

- Opened: `tools/registry.json` (C0 blob, all seven cells), `tools/registry-check.py` (`:1-120`,
  `:175-340`, validation field set, `--only`/`--registry` behaviour), `.ufo/evidence/round-54/c2/measure.py`
  (`:1-155`), `.ufo/evidence/round-54/contract.json` (`:22,:24`), `corpus/knowledge/scratch-root-contract.md`
  (whole), all seven tools' `strict_scratch_root()` and allocation sites at C0,
  `tools/env-diff.py:30-100,178-200`, `tools/bash-witness-study.py:1250-1275`.
- SKILL.md citations here are to the **C0 blob** (`git show 59c3810:SKILL.md`), where the bullet is
  `:32-39`. The working tree's `SKILL.md` was rewritten by a sibling seat while this seat ran
  (`git status --porcelain` → ` M SKILL.md`; the same bullet now reads `:32-39` with different
  wrapping), so working-tree line numbers can differ by a line — I report the committed ones and
  made no edit there.
- No lane file edited; nothing committed. `git -C LANE rev-parse HEAD` → `59c38109bf119d0e9d4f878644a82babc937bc1e`;
  `git -C LANE status --porcelain` shows only pre-existing sibling modifications (`SKILL.md`,
  `corpus/QUALITY.md`, `corpus/SOURCES.md`, `corpus/knowledge/change-aware-resweep-cadence.md`,
  `corpus/lessons/round-54.md`, `tools/env-diff.py`) and the untracked `.ufo/evidence/round-54/`,
  `.ufo/waves/round-54/` — none written by me except this report and its receipts directory.
- Writes: `.ufo/waves/round-54/w1/T54W1Simplify02.md` and
  `.ufo/waves/round-54/w1/T54W1Simplify02-receipts/` only (fixture registries derived from the C0
  blob, probe outputs, `docs-arm-probe.py`).
- Census conformance at seat time: `scripts/sources-census.sh validate --root FLEET tameshi` →
  `tameshi ok /…/corpus/SOURCES.md`, `rc=0`.
- Scratch: `$HYAKU_SCRATCH/tameshi-r54/T54W1Simplify02/`, removed on exit (`ls -d` → No such file);
  no `/tmp` artifacts of mine remain (the one `/tmp/tameshi-r21-envdiff-pin.*` in
  `bare-site-at-c0.out` was created *inside* the probe to demonstrate the fallback, and Python's
  `TemporaryDirectory` removed it on exit). Four entries from other owners remain in `/tmp` —
  `closure-r53-tameshi.json`, `tameshi-r14-evidence-disposition-selftest.j7oylhrj` (11:39, a tool
  this seat never invoked, likely a live sibling's C2 run) and two empty
  `tameshi-r4-2-regression.*` dirs; none is mine and I did not delete them.
- No tools installed or upgraded.

## Receipts index

`T54W1Simplify02-receipts/` — `registry.at-c0.json` (C0 blob), `docs-arm-probe.py` + `.out`,
`final-candidate.out`, `arm-absence.out`, `byte-accounting.out`, `registry-check-silent.out`,
`registry-check-contrast.out`, `alloc-sites-at-c0.out`, `alloc-sites.out` (working tree, superseded
by the C0 one), `bare-site-at-c0.out`, `bare-site.out` (working tree, same result), and the fixture
registries `P_final.json`, `C_one_word.json`, `C_one_word_plus_top_level_note.json`,
`E_typo_drops_empty_token.json`, `F_tokens_only_no_anchor.json`, `G_bad_source.json`,
`H_unknown_row_and_top_key.json`.

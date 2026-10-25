# ReviewSourceRows — round 41, wave 1

Reviewer seat, axes `discernment`. Read-only: the only write is this report. No counter was
run (`calibration/measure.py`, `census/measure.py` untouched); the deciding run stays the L1's.

## Rows under review

`corpus/SOURCES.md:123-124` (working tree, appended at 2026-10-25T03:39:41-03:00):

- S153 `ast — Abstract Syntax Trees (Python 3.14 documentation) — https://docs.python.org/3/library/ast.html`
- S154 `pathlib — Object-oriented filesystem paths, Path.write_text (Python 3.14 documentation) — https://docs.python.org/3/library/pathlib.html`

The <=25-word quotes the rows must be judged against live in the entry draft
`corpus/knowledge/r41-variable-destination-writes.md:11-12` (S153) and `:16-17` (S154); neither
row carries a quote column, so the criterion is read as "row + its entry quote".

## Method and exact evidence

```
mkdir -p /tmp/tameshi-r41-reviewsourcerows-live && cd /tmp/tameshi-r41-reviewsourcerows-live
for u in ast pathlib; do
  curl -sS -L --max-time 60 -o $u.html \
    -w "$u http=%{http_code} bytes=%{size_download}\n" \
    https://docs.python.org/3/library/$u.html
done
sha256sum ast.html pathlib.html
cmp -s ast.html  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-41/sources/ast.html && echo ast-identical
cmp -s pathlib.html /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-41/sources/pathlib.html && echo pathlib-identical
```

Observed:

| | ast | pathlib |
|---|---|---|
| HTTP | `200` (HTTP/2) | `200` (HTTP/2) |
| `content-length` / downloaded bytes | `362029` / `362029` | `271189` / `271189` |
| sha256 (live) | `183a4f8c3d593be4c45dc64406df2622ebc7080cf5ca3c0f0102649e57545317` | `0044cae699c55963a41c93f1f6c2a59fbc3a9e1240a4099a7b14c88534e4f093` |
| sha256 (snapshot, working tree) | identical, `cmp` silent | identical, `cmp` silent |
| matches the round-41 known-fact pin | yes | yes |

Quote location and word count, tag-stripped body only (`<section …>` onward, tags removed,
`html.unescape`, whitespace collapsed):

```
python3 - <<'PY'
import re, html
for p, q in (
  ('.ufo/evidence/round-41/sources/ast.html',
   'The ast module helps Python applications to process trees of the Python abstract syntax grammar.'),
  ('.ufo/evidence/round-41/sources/pathlib.html',
   'Open the file pointed to in text mode, write data to it, and close the file')):
    raw = open(p, encoding='utf-8').read()
    body = raw[raw.find('<section'):]
    norm = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', body)))
    print(p, 'present=', q in norm, 'words=', len(q.split()))
PY
```

Result: `ast present= True words= 15`; `pathlib present= True words= 16`. Both `<= 25`.

- ast quote body location: `.ufo/evidence/round-41/sources/ast.html:243-244`
  (`<p>The <code …>ast</code> module helps Python applications …`). The same words also sit in
  `<meta>` tags at `:11`, `:15`, `:16` — decoys, not the prose.
- pathlib quote body location: `.ufo/evidence/round-41/sources/pathlib.html:1563-1564`, under
  `id="pathlib.Path.write_text"` at `:1560`. The sentence continues with `file:`; the quoted
  string is an exact substring.

## Verdict per row

### S153 — DISAGREE

1. **Version label is false.** The row calls the page "Python 3.14 documentation"; the fetched
   bytes title it `<title>ast — Abstract syntax trees — Python 3.15.1 documentation</title>`
   (`.ufo/evidence/round-41/sources/ast.html`, same for `pathlib.html`). The lane's own precedent
   S084 (`corpus/SOURCES.md:93`) labels the served version (`Python 3.15.1`).
2. **teaches claims far more than the quote supports.** Row teaches: "a parsed tree exposes
   Name, Assign, Call and attribute nodes; ast.get_source_segment recovers a node's source;
   iter_child_nodes and NodeVisitor walk the tree". The quoted sentence says only that the
   module helps applications *process trees of the abstract syntax grammar*. It names no node
   class and no function. Every claim is true **of the page** (`ast.Name` :840, `ast.Call` :1068,
   `ast.Attribute` :1119, `ast.Assign` :1330, `ast.get_source_segment` :2809 with doc text at
   :2811, `ast.iter_child_nodes` :2855, `ast.NodeVisitor` :2870) but none of it is supported by
   the quote, so the pair as written overreaches.
   *Fix (preferred):* keep the rich teaches and move its support into the anchor, e.g.
   `§Node classes (ast.Name, ast.Assign, ast.Call, ast.Attribute) · §ast.get_source_segment · §ast.iter_child_nodes · §ast.NodeVisitor · §ast.walk`; then the quote is illustrative only.
   *Fix (minimal):* narrow teaches to the quote: "the ast module processes trees of Python's
   abstract syntax grammar, so a parsed module can be handled as a tree".
3. **One teaches assertion is factually imprecise.** `iter_child_nodes` does not walk the tree:
   "Yield all direct child nodes of node" (`ast.html:2856-2857`). The recursive walk is
   `ast.walk` (`ast.html:2859-2861`). `NodeVisitor` does walk (`:2871`). Rewrite as
   "iter_child_nodes yields direct children; ast.walk and NodeVisitor traverse the tree".
4. **Anchor omits the section that backs "node types".** Anchor is `§Abstract Syntax Trees and
   §ast.get_source_segment`; `#ast-abstract-syntax-trees` resolves (it is the module H1 span id,
   `ast.html:240`), but node types live under `§Node classes` (`#node-classes`).
5. **Snapshot is not committed** — see F2.

### S154 — DISAGREE (two cells), AGREE on the core teaches sentence

1. **Version label is false** — same as S153.
2. **teaches core is supported.** "write_text opens the file pointed to in text mode, writes the
   data and closes the file" tracks the quote nearly word for word. The trailing "so the receiver
   expression is the destination path" is an inference, not a quote statement: it follows from
   the method binding `Path.write_text(data, …)` (`pathlib.html:1560-1563`), whose subject is
   `self`. Because the anchor already names `§Path.write_text`, the inference is anchored; it
   should be read as method-binding semantics, not as something the 16-word sentence says.
3. **Scope names `write_bytes` with no anchor for it.** Scope: "Path.write_text and write_bytes …";
   anchor: `§Path.write_text` only. `write_bytes` is documented separately at
   `pathlib.html:1583-1585` ("Open the file pointed to in bytes mode, write data to it, and close
   the file"). Add `§Path.write_bytes` to the anchor (or drop `write_bytes` from scope).
4. **Snapshot is not committed** — see F2.

## Findings, severity ordered

**F1 (high) — both rows mislabel the served docs version as 3.14.** Page title is
`Python 3.15.1 documentation`; `python3 --version` on this host is `3.14.8`, which is a different
fact from the version of the fetched page. Fix `corpus/SOURCES.md:123`, `:124`, and the same
label in `corpus/knowledge/r41-variable-destination-writes.md:1-2`.

**F2 (high) — the snapshot the rows pin is not committed, and the registry note says it is.**
Evidence: `git status --porcelain` → `?? .ufo/evidence/round-41/sources/`;
`git ls-tree -r --name-only HEAD | grep round-41` → only the four frozen tool/contract files;
`git log --oneline --all -- .ufo/evidence/round-41/sources` → 0 commits; the directory is not
ignored (`git check-ignore` exit 1). Yet `corpus/SOURCES.md:437` states "Each is pinned to a
committed snapshot under `.ufo/evidence/round-41/sources/`". At `d4ee4e6` that sentence is false
and the anchor path does not resolve. Digest equality itself is exact (live == working-tree
snapshot), so the pin becomes true the moment the two HTML files land. Required: commit
`.ufo/evidence/round-41/sources/{ast,pathlib}.html` plus `corpus/knowledge/r41-variable-destination-writes.md`
in the measurement commit — the entry file the rows name in `used-by` is likewise currently
untracked (`?? corpus/knowledge/r41-variable-destination-writes.md`), so the `used-by` cell and any
round-41 lesson that backticks either path would otherwise trip C1 `m8`
(`.ufo/evidence/round-41/calibration/measure.py:181-191` collects backticked tokens under the
`.ufo/evidence/round-41/` and `corpus/` prefixes; m8 at `:237-242`).

**F3 (high, S153) — teaches not derivable from the quote** (detail above). S154's teaches is
acceptable once the receiver inference is attributed to the method signature.

**F4 (medium, S153) — `iter_child_nodes` mis-described as a tree walk** (`ast.html:2856-2857` vs
`ast.html:2859-2861`).

**F5 (medium, S154) — `write_bytes` in scope has no anchor**; add `§Path.write_bytes`
(`pathlib.html:1583-1585`).

**F6 (low) — word counts in the entry draft are off by one.** `r41-variable-destination-writes.md:12`
says `(16 words)` for a 15-word quote; `:17` says `(17 words)` for a 16-word quote. The `<=25`
requirement is unaffected, but the stated counts are wrong and the row/lesson must not repeat them.

**F7 (low) — S153 anchor omits `§Node classes`** for its "node types" scope.

**F8 (info, agree) — id collision is recorded honestly and the note's arithmetic is right.**
`corpus/SOURCES.md:438`: registry 109 ids S001–S154 (verified: 109 rows, min S001, max S154);
staged 103 ids S153–S255 (verified: `assimilation/staged-ids` has 103 unique ids, 255-153+1 = 103);
`assimilation/collisions` holds exactly `S153` and `S154`, matching
`/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md:7-8` (POSIX `diff` spec and
google/golden — different sources). Keeping the ids is a merge decision deferred with a stated
hazard; residual risk is that a wholesale append of the staged block duplicates both ids. This
seat would not change it, but the next assimilation must renumber the staged S153/S154, not the
mined rows.

**Format checks (agree).** Both rows are 13 `awk -F'|'` fields (11 columns), 12 pipe characters,
no pipe inside any cell; `opened` ISO `2026-10-25`; `recheck` `180d`; `status` `mined`; `tier` A;
`kind` docs. Registry live count 109; `Next unused id: S155` (`corpus/SOURCES.md:440`) is
internally consistent.

## Residual risk and verification gaps

- Byte identity is against a CDN cache HIT (`last-modified: Sun, 25 Oct 2026 06:21:21 GMT`).
  It proves what the CDN served now, not that the origin cannot change between cache fill and
  my fetch. The committed-snapshot pin is the correct defence; it must actually be committed (F2).
- Both URLs are the `/3/` alias. Measuring the versioned `https://docs.python.org/3.15/library/{ast,pathlib}.html`
  returns **byte-identical** files (same two sha256 values), so adopting `/3.15/` is free and
  aligns with the lane's S100 lesson (`corpus/SOURCES.md:108`: "the /3/ alias drifts"). Not
  required for this round, recommended.
- No counter was run; no claim here about m6/m7/m8/m9 outcomes.
- Out of seat, observed only: the working-tree contract now carries an append-only `amendments`
  array (A1 C1 `registry()` index 9→8 and counter re-pin; A2 fixture re-root and second mutant;
  A3 lesson wording), each with `rule_changed: false`, `before_data: true`, and
  `kill_rule_note` stating no default-mode run preceded them. HEAD still pins the pre-amendment
  counters (`f00917…`/`5d57c7…`), which hash to the HEAD counter files; the worktree re-pins to
  `5ccb42…`/`83268e…`, matching the worktree files. No action from this seat; the amendment
  record is auditable as written.

## Tooling

No installs or upgrades (curl, python3, coreutils sufficed). No pacman transaction attempted
(host-wide guard respected). Scratch only under `/tmp/tameshi-r41-reviewsourcerows-live/`.

Report: .ufo/waves/round-41/w1/ReviewSourceRows.md

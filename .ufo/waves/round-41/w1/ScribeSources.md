# ScribeSources — round 41 (attempt 2), wave 1 — registry rows S153/S154

Axes: conformance (registry shape and census), calibration (C1 counter/scorecard agreement),
depth (the C2 write-path census consumer of both rows). Read-only seat: this report is the only
file written in the lane checkout; the draft was exercised in
`/tmp/tameshi-r41-scribesources-scratch` (copy of `d4ee4e6`).

## 1. Draft to apply (not applied by this seat)

Insertion point: `corpus/SOURCES.md:122`, immediately after the `| S152 | …` row and before the
blank line plus `## Paths` at `corpus/SOURCES.md:124` (freeze revision `d4ee4e6`). Every cell is
pipe-free; each line is 11 columns / 13 awk fields / 12 `|` delimiters.

```md
| S153 | ast — Abstract syntax trees (CPython 3.15.1 library reference) — https://docs.python.org/3/library/ast.html | docs | A | what the standard-library `ast` reference states about parsing source into a node tree and recovering a node's own source bytes, for write-destination resolution | §ast — Abstract Syntax Trees intro, HTML line 243, and §ast.get_source_segment, HTML line 2811 @ snapshot .ufo/evidence/round-41/sources/ast.html fetched 2026-10-25 (362,029 bytes; SHA-256 183a4f8c3d593be4c45dc64406df2622ebc7080cf5ca3c0f0102649e57545317) | ast.parse returns an AST node — compile with only-AST flags — while Name, Call and Assign are node classes and get_source_segment recovers the source text a node generated, so a call and the assignment that feeds its argument are recoverable from one tree | mined | 2026-10-25 | 180d | corpus/knowledge/r41-variable-destination-writes.md |
| S154 | pathlib — Object-oriented filesystem paths, Path.write_text and Path.write_bytes (CPython 3.15.1 library reference) — https://docs.python.org/3/library/pathlib.html | docs | A | the receiver-is-destination rule of the path-method write forms the write-path census must resolve | §Reading and writing files, Path.write_text, HTML lines 1561-1572, and Path.write_bytes, HTML lines 1583-1594 @ snapshot .ufo/evidence/round-41/sources/pathlib.html fetched 2026-10-25 (271,189 bytes; SHA-256 0044cae699c55963a41c93f1f6c2a59fbc3a9e1240a4099a7b14c88534e4f093) | write_text opens the file its receiver points to, writes the data and closes it — write_bytes the same in bytes mode — and an existing file of the same name is overwritten, so the receiver expression is the destination, not the argument list | mined | 2026-10-25 | 180d | corpus/knowledge/r41-variable-destination-writes.md |
```

Two-line registry-note append, at the end of `## Id allocation` (`corpus/SOURCES.md:433` at
freeze; the section is append-only):

```md
Round 41: new rows S153 (CPython `ast` library reference: a parsed tree keeps a call and the assignment feeding it) and S154 (the CPython library reference's `Path.write_text` and `Path.write_bytes` receiver-is-destination rule), both tier A / docs / mined, opened 2026-10-25, recheck 180d, used-by `corpus/knowledge/r41-variable-destination-writes.md`, anchors byte- and sha256-pinned to the round-41 snapshots. Rows 107 → 109; no existing row's status, recheck or used-by changed, and the staged package's S153/S154 ids collide with these with no renumber map applied this round.
- Next unused id: S155.
```

Shape checks on the exact draft (scratch, `corpus/SOURCES.md:123-124`): `awk -F'|' … {print NF}`
→ 13; per-line pipe count → 12; no duplicate ids; no enum violations; no missing `used-by`
path; no new W-code. Census: `bash scripts/sources-census.sh validate --file corpus/SOURCES.md`
in the scratch tree → exit 0, identical warning set to the live lane (9 × W04, 1 × W01), zero
E codes, 109 rows.

## 2. Grounding (verified against the snapshots, not against the knowledge entry)

| item | evidence |
|---|---|
| `ast.html` title | `ast — Abstract syntax trees &#8212; Python 3.15.1 documentation` (`grep -o '<title>[^<]*'`) |
| `ast.html` digest/size | `sha256sum` = 183a4f8c3d593be4c45dc64406df2622ebc7080cf5ca3c0f0102649e57545317, 362,029 bytes |
| ast quote 1 | `.ufo/evidence/round-41/sources/ast.html:243` — "The ast module helps Python applications to process trees of the Python abstract syntax grammar." (15 words) |
| ast quote 2 | `ast.html:2811` — "Get source code segment of the source that generated node." |
| ast node/helper anchors | `ast.html:840` Name, `:1068` Call, `:1330` Assign, `:2678` parse, `:2809` get_source_segment, `:2855` iter_child_nodes, `:2870` NodeVisitor |
| `pathlib.html` title | `pathlib — Object-oriented filesystem paths &#8212; Python 3.15.1 documentation` |
| `pathlib.html` digest/size | `sha256sum` = 0044cae699c55963a41c93f1f6c2a59fbc3a9e1240a4099a7b14c88534e4f093, 271,189 bytes |
| pathlib quote 1 | `pathlib.html:1563` — "Open the file pointed to in text mode, write data to it, and close the file" (16 words) |
| pathlib overwrite | `pathlib.html:1572` (write_text) and `:1594` (write_bytes) — "An existing file of the same name is overwritten." |
| pathlib bytes form | `pathlib.html:1585` — "Open the file pointed to in bytes mode, write data to it, and close the file" |

Both digests and byte sizes equal the contract's known facts. Both `source:` labels in
`corpus/knowledge/r41-variable-destination-writes.md:1-2` say "Python 3.14 documentation"; the
snapshot titles say 3.15.1 — the labels, not the snapshots, are wrong (see F3).

## 3. Executed checks

| command | result |
|---|---|
| `python3 .ufo/evidence/round-41/calibration/measure.py --lane … --rev a3d6c690bcbf8914551d4f4e8e1612784c1c2046` | `m6=1 m9=1 total=2 records=0 sources_rows=107` — reproduces the contract's `before` |
| `sha256sum .ufo/evidence/round-41/calibration/measure.py` (successive observations during this seat's run) | `5ccb42d8a60d6d1e5e509a1ddb954a602d7e46476ee0355084810b48b8f08553`, then `9aaa99ac5a5abd16a42123fba4bf5c90151b3d043aa2d92ee99116e5789d92cd` — the file was edited twice while this seat ran |
| `git -C … show d4ee4e6:.ufo/evidence/round-41/calibration/measure.py \| sha256sum` | `f00917ddd7b519f0eb631f8a11dcc9bbcdcdfa0de9cbbb62639431f5794cb0c2` (bytes frozen in the contract at `d4ee4e6`) |
| `claims.C1.counter_sha256` in the worktree `contract.json` vs `sha256sum` of the file at handoff | contract `8bc9b4221c59c7b380892b7f97885e9b8ada1f5d82b0703effa166f0519ce11c` (amendment A4) ≠ file `9aaa99ac…` — **un-reconciled at handoff** |
| `git diff .ufo/evidence/round-41/calibration/measure.py` | one hunk: `- status = cells[9]…` → `+ status = cells[8]…` at `measure.py:137` |
| scratch `…/calibration/measure.py --lane /tmp/tameshi-r41-scribesources-scratch --rev work` (pinned bytes, drafted rows, lesson citing S153/S154) | `m6=0 m7=2 m8=0 m9=1 total=3` — m7: "S153 cited but status=2026-10-25", same for S154 |
| scratch, worktree copy of the counter (`/tmp/tameshi-r41-scribesources-fixed.py`) | `m6=0 m7=0 m8=0 m9=1 total=1` (m9 only because the synthetic lesson carries no round-40 correction) |
| scratch minus the three cited artifacts, pinned counter | `m6=0 m7=2 m8=3 m9=1 total=6` — m8 on both snapshot paths and on `corpus/knowledge/r41-variable-destination-writes.md` |
| `bash scripts/sources-census.sh validate tameshi --root /home/vgpnk/Projects/shokunin` | exit 0, live lane 109 rows, 9 × W04 + 1 × W01, zero E codes |
| `bash scripts/sources-census.sh validate --file corpus/SOURCES.md` (scratch) | exit 0, same warning set, 109 rows |

## 4. Findings (severity, path:line)

- **F1 (critical, amended but pin un-reconciled) — the C1 counter's status column is off by
  one in the frozen bytes.** `measure.py:137` read `cells[9]`, which for an 11-column row is
  `opened`, not `status` (`status` is `cells[8]`; verified: all 107 base rows carry a date in
  `cells[9]`). At the base revision m7 is vacuously 0 because `records=0`; the live round-41
  lesson cites S153/S154 (`corpus/lessons/round-41.md:13`), so a deciding run over the original
  frozen bytes yields `m7=2` and `C1_R41_PASS=false` — exactly the scratch receipt above. The
  defect has since been found independently by seat ExecC1Base and amended as **A1** in the
  worktree `contract.json`; `measure.py:137` now reads `cells[8]`, and a re-run at the base
  revision with the current bytes still reproduces `before` (`m6=1 m9=1 total=2`, observed at
  handoff). **Live hazard:** the contract's C1 pin is now `8bc9b422…` (amendment A4) while the
  file on disk is `9aaa99ac…`, i.e. the pin lags a further edit; verify with
  `sha256sum .ufo/evidence/round-41/calibration/measure.py` against
  `python3 -c "import json;print(json.load(open('.ufo/evidence/round-41/contract.json'))['claims']['C1']['counter_sha256'])"`
  before the deciding run and record an amendment for any delta.
- **F2 (critical) — the three artifacts the round-41 records cite are untracked at the freeze
  revision.** `git cat-file -e d4ee4e6:<path>` → ABSENT for
  `.ufo/evidence/round-41/sources/ast.html`,
  `.ufo/evidence/round-41/sources/pathlib.html`, and
  `corpus/knowledge/r41-variable-destination-writes.md`; `git status --porcelain` shows them as
  `??`. The live lesson backticks the knowledge path at
  `corpus/lessons/round-41.md:13` and both snapshot paths at `:16` and `:20`, so a deciding run
  at a revision without them is `m8=3` (receipt above). They must be committed with the round.
- **F3 (major) — the live rows mislabel the pinned bytes and drop the digest.**
  `corpus/SOURCES.md:123` reads "…(Python 3.14 documentation)" and `:124` the same, while both
  snapshots' `<title>` say 3.15.1; the `anchor` cells carry no byte size and no SHA-256, unlike
  S102/S103. The knowledge entry repeats the 3.14 label at
  `corpus/knowledge/r41-variable-destination-writes.md:1-2`. All three are uncommitted
  (`M corpus/SOURCES.md`, `?? corpus/knowledge/…`), so they are still correctable in place; the
  draft in §1 is the corrected shape. The live rows do satisfy shape (NF=13 at `:123`/`:124`)
  and their `teaches` names only facts present in the snapshot (Name/Assign/Call,
  `get_source_segment`, `iter_child_nodes`, `NodeVisitor` all located).
- **F4 (minor) — the live note is four lines, not two.** `corpus/SOURCES.md` tail carries the
  "Round 41: two rows added…" paragraph plus id-collision, census and `- Next unused id: S155.`
  lines. Its "committed snapshot" wording is false until F2 lands. The two-line version is in §1.
- **F5 (dependency, resolved at handoff) — m6 target after these rows is 109.** The last
  `| sources-registry |` line, `SCORECARD.md:1851`, must have `109 rows` as its first
  `(\d+) rows` match. It read `103 rows at round 35` when this seat started; at handoff it reads
  "109 rows at round 41 (restated from 103 …)", so `m6` clears. Scratch receipt: with `109 rows`
  the counter gives `m6=0`. The edit was another seat's, not this one's.

## 5. Out-of-scope / untouched

No edit to `corpus/SOURCES.md`, the contract, the counters, the scorecard, the knowledge entry,
any sibling lane, the jj state or the Git index. The two registry rows and the four-line note
already present in the live worktree were written by another seat; this report does not adopt
or renumber them, it supplies the corrected draft and the evidence for the decision. During
this seat's run other seats also modified `.ufo/evidence/round-41/contract.json` (its
`amendments` array now carries A1–A4), both round-41 counters and `census/fixtures.json`,
`SCORECARD.md`, `LOG.md`, and `corpus/{QUALITY,README}.md`; those edits are theirs. At handoff
the live rows still carry the 3.14 label and no digest (F3), and the note still claims committed
snapshots the freeze revision does not hold (F2, F4).

## 6. Tooling

No install or upgrade. No `pacman` transaction (host-wide pause observed). Scratch artifacts:
`/tmp/tameshi-r41-scribesources-scratch` (draft + census), `/tmp/tameshi-r41-scribesources-uncommitted`
(m8 demonstration), `/tmp/tameshi-r41-scribesources-fixed.py` (worktree counter copy).

Report: `.ufo/waves/round-41/w1/ScribeSources.md`

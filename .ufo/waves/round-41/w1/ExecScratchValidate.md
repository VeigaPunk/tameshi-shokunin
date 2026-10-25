# ExecScratchValidate — S153/S154 draft rows validated in a scratch registry

Seat: `L1Tameshi41.ExecScratchValidate` (executor, read-only on the lane). Milestone:
scratch-mirror validation of the two round-41 draft registry rows.

Not run, by contract: C1 `calibration/measure.py`, C2 `census/measure.py` (no `--rev`, no
`--control`, no `--selftest`). The lane checkout, its `.jj` state and its Git index were not
written; the only file this seat wrote outside `/tmp` is this report.

## Answer

| Question | Answer |
|---|---|
| exit code, spec-shaped scratch (base corpus + the two rows) | **1** — five `E11` only |
| **E03 duplicate id** | **absent, 0 lines** |
| **E04 duplicate url within scope** | **absent, 0 lines** |
| warnings | `W01 S101` (1) + `W04` (9) — all pre-existing in the base registry, none on S153/S154 |
| exit code when the row's `used-by` file exists | **0**, `ok` |
| exit code on a snapshot of the live lane | **0**, `ok` (109 rows, no E03/E04) |
| decisive risk | the live registry already holds S153/S154; appending the draft again gives **`E03 S153`/`E03 S154`** |

## 1. Validator identity

The only `sources-census.sh` implementing `validate --file` is the fleet one; the lane-local
`.ufo/evidence/kaika-round-1/sources-census.sh` has no mode parser at all (it is a fixed
census pipeline over `corpus/SOURCES.md`).

```
$ sha256sum /home/vgpnk/Projects/shokunin/scripts/sources-census.sh
3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30  scripts/sources-census.sh
$ wc -l scripts/sources-census.sh
806 scripts/sources-census.sh
```

Code read for the two codes under question:

- `scripts/sources-census.sh:641` — `else if (id in seen) printf "%s\tE03\t%s duplicate id\n"`
- `scripts/sources-census.sh:649` — `E04` fires only when the **same url + same scope** repeats,
  the later row is non-`rejected`, an earlier row in that scope was non-`rejected`, and `teaches`
  lacks `supersedes S<nnn>`.
- `scripts/sources-census.sh:501` — `--file` resolves `used-by` against
  `realpath(dirname(SOURCES.md)/..)`, i.e. the mirror root, which is why a corpus-only mirror
  reports the pre-existing `tools/…` misses.

## 2. Scratch artifacts

All under `/tmp`; `corpus/` extracted from the frozen base
`a3d6c690bcbf8914551d4f4e8e1612784c1c2046` via `git archive` (never from the moving worktree —
a sibling was writing `corpus/SOURCES.md` concurrently).

| dir | shape | rows | `corpus/SOURCES.md` sha256 |
|---|---|---|---|
| `/tmp/tameshi-r41-execscratchvalidate-mirror` | base `corpus/` + S153/S154 appended after S152 (`:123-124`) | 109 | `a3045edf58c1126f467299c905d6b316d47d0ac1ed3ec5d551cfd666e1ac126e` |
| `/tmp/tameshi-r41-execscratchvalidate-mirrorplus` | same + base `tools/` + a labelled placeholder `corpus/knowledge/r41-variable-destination-writes.md` | 109 | `a3045edf58c1126f467299c905d6b316d47d0ac1ed3ec5d551cfd666e1ac126e` |
| `/tmp/tameshi-r41-execscratchvalidate-mirrorlive` | live-worktree `corpus/` snapshot + base `tools/` | 109 | `9b73ec116913d73e85ec65197c39bc95d25ce6edb349cf40bbe96450cbecb705` |
| `/tmp/tameshi-r41-execscratchvalidate-collision` | live snapshot + the two draft rows added on top | 111 | `f21823a3ccc625cc57c7840aa28f7bc39abbd8d51f53446e493687c1febf0d9f` |

The appended pair in the first two mirrors, as landed (`:123-124`), sha256 of the two lines:

```
$ sed -n '123,124p' /tmp/tameshi-r41-execscratchvalidate-mirror/corpus/SOURCES.md | sha256sum
750f47460cbd5a441d43e46df19c6f2bb36d3ef6686195760479f5ff54101c1d  -
```

```
| S153 | ast — Abstract syntax trees (Python 3.15.1 documentation) — https://docs.python.org/3/library/ast.html | docs | A | the `ast` module as the authoritative parse surface for a Python source tree — node types for assignments, calls and attribute access — not a dataflow or scope analyser | §Abstract syntax trees, module introduction paragraph and ast.parse signature @ Python 3.15.1 documentation fetched 2026-10-25; snapshot .ufo/evidence/round-41/sources/ast.html sha256 183a4f8c3d593be4c45dc64406df2622ebc7080cf5ca3c0f0102649e57545317 | `ast.parse` returns a tree of node types rather than text, so a consumer reads assignment and call nodes instead of matching source lines; the grammar may change with each Python release, so the version is part of the claim | mined | 2026-10-25 | 180d | corpus/knowledge/r41-variable-destination-writes.md |
| S154 | pathlib — Object-oriented filesystem paths, Path.write_text and Path.write_bytes (Python 3.15.1 documentation) — https://docs.python.org/3/library/pathlib.html | docs | A | `Path.write_text` and `Path.write_bytes`: the file the method is called on is the destination | §Path.write_text and §Path.write_bytes @ Python 3.15.1 documentation fetched 2026-10-25; snapshot .ufo/evidence/round-41/sources/pathlib.html sha256 0044cae699c55963a41c93f1f6c2a59fbc3a9e1240a4099a7b14c88534e4f093 | write_text opens the file pointed to in text mode, writes the data and closes the file, so the receiver expression is the destination path and a census reading only the call's arguments misses the write | mined | 2026-10-25 | 180d | corpus/knowledge/r41-variable-destination-writes.md |
```

Grounded on the committed snapshots (fetched live too; both live fetches were byte-identical
to the committed bytes — `183a4f8c…5317` at 362029 bytes, `0044cae6…f093` at 271189 bytes).
Page `<title>` of both: `Python 3.15.1 documentation`.

## 3. Run 1 — the asked-for command, exit and findings

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh \
    validate --file /tmp/tameshi-r41-execscratchvalidate-mirror/corpus/SOURCES.md
file	W04	S047 duplicate url pitest.org/quickstart/incremental_analysis across scopes
file	W04	S048 duplicate url pitest.org/quickstart/incremental_analysis across scopes
file	W04	S075 duplicate url man7.org/linux/man-pages/man1/strace.1.html across scopes
file	W04	S076 duplicate url docs.jj-vcs.dev/latest/git-compatibility across scopes
file	W04	S077 duplicate url man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html across scopes
file	W04	S078 duplicate url man7.org/linux/man-pages/man2/open.2.html across scopes
file	W04	S081 duplicate url bazel.build/reference/test-encyclopedia across scopes
file	W04	S092 duplicate url bazel.build/remote/caching across scopes
file	W01	S101 tierC mined used-by=corpus/knowledge/witness-equivalence-rule.md
file	W04	S104 duplicate url cgit.git.savannah.gnu.org/cgit/bash.git/plain/doc/bashref.texi?id=b8c60bc9ca365f8261fa97900b6fa939f6ebc303 across scopes
file	E11	S097 missing used-by tools/tally-audit.py
file	E11	S102 missing used-by tools/tally-audit-v3.py
file	E11	S104 missing used-by tools/tally-audit-v3.py
file	E11	S153 missing used-by corpus/knowledge/r41-variable-destination-writes.md
file	E11	S154 missing used-by corpus/knowledge/r41-variable-destination-writes.md
EXIT=1
```

- **No `E01`–`E10` and no `E12`** on any line. That is the machine proof that both new rows are
  NF=13, `id` matches `S[0-9]{3,}`, `kind=docs` and `tier=A` and `status=mined` are in enum,
  `opened=2026-10-25` is not in the future (checked at 2026-10-25), `recheck=180d` is an admitted
  cadence, and `tier A` is not paired with `kind=community`.
- **E03 = 0.** **E04 = 0** — `docs.python.org/3/library/ast.html` and `…/pathlib.html` occur
  nowhere else in the 107-row base registry (`grep -n 'docs.python.org' corpus/SOURCES.md` returns
  only subprocess, doctest, json, cmdline, os.path, doctest-3.15), so no url+scope collision is
  even reachable.
- `W01 S101` and the nine `W04` lines are **identical** in the untouched base registry (they are
  inherited warnings, not introduced by S153/S154).
- The four `E11` on `tools/…` are an artifact of the spec's "copy `corpus/`" shape: `--file`
  resolves `used-by` from the mirror root, which has no `tools/`.

## 4. Run 2 — same rows with the `used-by` target present

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh \
    validate --file /tmp/tameshi-r41-execscratchvalidate-mirrorplus/corpus/SOURCES.md
… (the same W01 + nine W04 lines) …
file	ok	/tmp/tameshi-r41-execscratchvalidate-mirrorplus/corpus/SOURCES.md
EXIT=0
```

So: **the two rows themselves raise no E-code.** The only E11 they can produce is the
`used-by` file not existing yet. Once
`corpus/knowledge/r41-variable-destination-writes.md` exists at the lane root, `validate`
returns `ok` and exits 0. (In the live lane that file now exists — 5264 bytes, `03:42`.)

## 5. Run 3 — snapshot of the live lane (no edits)

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh \
    validate --file /tmp/tameshi-r41-execscratchvalidate-mirrorlive/corpus/SOURCES.md
… W01 S101 + nine W04 …
file	ok	/tmp/tameshi-r41-execscratchvalidate-mirrorlive/corpus/SOURCES.md
EXIT=0
```

Live `corpus/SOURCES.md` currently holds 109 rows, with S153 at `:123` and S154 at `:124` and
`corpus/knowledge/r41-variable-destination-writes.md` present. The live state validates clean
(`ok`, exit 0) — **no E03, no E04, no E11**.

## 6. Run 4 — the collision this seat exists to catch

Adding the two draft rows on top of a registry that already carries S153/S154:

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh \
    validate --file /tmp/tameshi-r41-execscratchvalidate-collision/corpus/SOURCES.md
file	E03	S153 duplicate id
file	E03	S154 duplicate id
EXIT=1
```

**Do not append the draft pair to the live registry** — ids S153/S154 are already occupied at
`corpus/SOURCES.md:123-124`. The draft is only safe against a registry whose highest id is
S152 (the base revision), which is the shape in runs 1–2. If a second S153/S154 pair lands, the
lane fails `E03` twice.

## 7. Finding F1 — the live rows' version label contradicts the page they cite

The live rows' `source` cell reads `(Python 3.14 documentation)`; the page served at that URL
stamps `3.15.1`:

```
$ grep -o '<title>[^<]*</title>' .ufo/evidence/round-41/sources/ast.html
<title>ast — Abstract syntax trees &#8212; Python 3.15.1 documentation</title>
$ grep -o '<title>[^<]*</title>' .ufo/evidence/round-41/sources/pathlib.html
<title>pathlib — Object-oriented filesystem paths &#8212; Python 3.15.1 documentation</title>
$ grep -o 'Python 3\.1[0-9]\.[0-9]*' .ufo/evidence/round-41/sources/ast.html | sort | uniq -c
      2 Python 3.15.1
```

The 11 (`ast`) / 15 (`pathlib`) occurrences of `3.14` inside the snapshots are Sphinx changelog
annotations, not the document version:

```
$ grep -o '.\{40\}3\.14.\{40\}' ast.html | head -2
… <span class="versionmodified changed">Changed in version 3.14: </span>The …
… since version 3.8, removed in version 3.14: </span>Previous versions of Python pro …
```

Consequence: `(Python 3.14 documentation)` in `corpus/SOURCES.md:123` and `:124` is a false
version claim, and no E-code covers it (`anchor` only needs a section + access date). It also
sits badly with the anchor cells, which pin the snapshot by hash but name no version. The rows
validated in the scratch said `Python 3.15.1 documentation` for exactly this reason. If the lane
keeps the `3.14` label, the round-41 lesson's `## Gate` quote must not repeat it.

## 8. Notes and residual risk

- `E03`/`E04` are the two codes the task asked for; both are **0** on the spec-shaped scratch and
  on the live snapshot, and `E03` is **2** only when the pair is applied twice.
- Base registry's trailing `- Next unused id: S105.` (`corpus/SOURCES.md:433` at
  `a3d6c69`) is stale against its own highest id S152; my scratch left it untouched (it is prose,
  not a row, and no E-code reads it). The live lane already carries `S155` at `:440`.
- The mirror row count is 109 = base 107 + S153 + S154; `E02` stayed silent, so neither id
  collides with the base.
- Tooling: **no install and no upgrade** was performed (`pacman` untouched, per the paused
  transaction guard); `curl`, `gawk`, `sha256sum`, `bash` were already present.
- Scratch is `/tmp`-local: `/tmp/tameshi-r41-execscratchvalidate-{mirror,mirrorplus,mirrorlive,collision}`.
  Nothing under the round-35 scratch tree is involved — that tree was relocated to
  `.ufo/waves/round-35/scratch-evidence/` (per `L1Mado35.RevQuoteS210`), not deleted, and neither
  path is cited here — so the relocation reported by `L1Mado35.RevEntryR15` does not touch this
  evidence.

Report: .ufo/waves/round-41/w1/ExecScratchValidate.md

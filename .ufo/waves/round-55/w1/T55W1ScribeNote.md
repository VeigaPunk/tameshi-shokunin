# T55W1ScribeNote — round-55 C2 note: "one line, every mode"

Seat: `T55W1ScribeNote` (scribe, leaf). L1 `TameshiR55`, hyaku run 11, one v2 wave.
Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. Base `0a2010acd1e92e4e332774050825e21bcfc7e079`;
frozen counter set `631cd6455e58dce969310b4c0466c3383d9f5108`.
Judged axis: operability. Milestone: C2 note — one line section.

## Behavior

I drafted the new `## One line, every mode (round 55)` section of
`corpus/knowledge/scratch-root-contract.md` and wrote it as a drop-in at
`.ufo/waves/round-55/w1/T55W1Er10.md`, with:

- (a) the counter's frozen grammar **as the counter carries it** — the `GRAMMAR` regex verbatim
  (`.ufo/evidence/round-55/c2/measure.py`), plus one rendered operator line. The round's claim
  statement writes the optional group as `(\.py)?`; the counter writes `(?:\.py)?` — identical
  language, and the draft quotes the counter.
- (b) the **nine** allocating modes named exactly as the counter's mode ids: `env-diff --selftest`,
  `env-diff --contract`, `repeat-control --selftest`, `registry-check --selftest`,
  `registry-check --rev`, `bash-witness-study selftest`, `pin-disposition --selftest`,
  `evidence-disposition --selftest`, `context-capture --selftest` — with the note that `--rev` is
  marked expensive by the counter (unusable arm only; its usable path is the tool's own self-test).
- (c) the five lazy modes (`repeat-control --snapshot`, `bash-witness-study count`,
  `pin-disposition --read`, `evidence-disposition --json`, `context-capture --check`) and why they
  keep their exit — measured, not assumed: they allocate no scratch at all (below).
- (d) the honest boundary: the class is an operator-visible line grammar, **not** a shared Python
  type. The draft states the tree's real split, which is not the item's phrasing: six of the seven
  tools declare their own local `ScratchRootUnusable(RuntimeError)`; `registry-check` declares no
  class and raises the builtin `RuntimeError` with the same text. `registry-check` is named as the
  proof that a conforming tool may have no exception class at all.
- Citations: S277-S279 stay on the `TMPDIR` arms (S277 the definition, S278 the resolver, S279 the
  documented order). **S280** (GNU Coding Standards §4.4 Formatting Error Messages: `program:
  message`, message not capitalized) was registered by the sources scribe while this seat ran; the
  draft cites it for the one-line shape, grounded in the verbatim extraction
  `.ufo/evidence/round-55/assimilation/S280-gnu-errors.txt`. The mode inventories are the counter's
  own table, stated as a lane measurement rather than a sourced claim.

Patch: `.ufo/waves/round-55/w1/T55W1ScribeNote-receipts/one-line-section.patch` — 79 insertions on
`631cd64`, applied to a fresh clone of the lane (`git clone --shared`) and committed there as
`030fd5687d658891d6aee5d3e15bda5e31ebad23`; `git rev-parse --show-toplevel` was asserted equal to
the clone before committing, `git apply --check` passes, and the patched file's last 79 lines are
byte-identical to `receipts/draft-section.md` (`receipts/patch-apply.txt`).

The mode set moved under me mid-seat: the counter held eight allocating modes when I started
(`sha ab3ae75…`) and nine when I finished (`sha 36ca47d3…`, `registry-check --rev` added by an
amendment that also raised the note target to `len(allocating)`). The draft tracks the live table —
`note_arm=9/9` — and the receipt `counter-evolution.txt` records both readings so the change is
auditable rather than inferred.

## State of the landed text (not mine, observed)

The working tree carries a `## One line, every mode (round 55)` section (`corpus/knowledge/
scratch-root-contract.md` line 71 to the end, 102 lines, mtime **14:12:16**) plus a paragraph before
it closing the round-54 residue. It is a sibling/L1 edit; I did not touch it. As of 14:12 it names
all nine allocating modes and **passes the note arm** (`note-arm-landed.txt`: 9/9 allocating ids,
5/5 lazy ids), so the arm is satisfiable today; the corrections below are accuracy — one false
sentence, an unmatchable template, a weak rationale and a missing citation — not arm-passing
failures.

## Findings (each with the command and its output)

**F1 — the landed boundary sentence is false for four tools, and one tool has no class.**
Landed text: "the tools keep their own exception classes (`ScratchRootUnusable` in the two round-55
edits, a local class in `env-diff`)". Tree (`receipts/exception-classes.txt`):

```
$ grep -n "^class ScratchRootUnusable" tools/*.py
tools/bash-witness-study.py:205
tools/context-capture.py:300
tools/env-diff.py:32
tools/evidence-disposition.py:191
tools/pin-disposition.py:161
tools/repeat-control.py:148
$ grep -c "class ScratchRootUnusable" tools/registry-check.py
0
$ grep -rn "import.*ScratchRootUnusable" tools/*.py | wc -l
0
$ ls tools | grep -c scratch
0
```

Six local classes, all named `ScratchRootUnusable`; `env-diff` is one of the six, not a different
kind of thing; `registry-check` has none (inline `raise RuntimeError(...)` at
`tools/registry-check.py:766`); no cross-tool import and no shared module. The item's own phrasing
("the seven tools keep their own exception classes") is likewise inaccurate for `registry-check`.
The draft states the accurate split.

**F2 — the landed section prints a template, not the counter's grammar.**
Landed: `    <tool>: could-not-evaluate: ... '<value>' (could-not-evaluate)`. The counter carries the
regex (receipt `grammar-check.txt`):

```
^[A-Za-z][A-Za-z0-9_.-]*(?:\.py)?: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '.+' \(could-not-evaluate\)$
```

`<tool>` / `<value>` are not matchable and hide that the leading token is not uniform. The nine
allocating modes emit seven distinct tokens (receipt `nine-allocating-modes.txt`): `ENVDIFF_SETUP`
(both `env-diff` modes), `repeat-control`, `registry-check` (both modes), `WITNESS_STUDY`,
`pin-disposition.py`, `evidence-disposition.py`, `context-capture.py`; all nine lines match the regex
9/9, and the draft's rendered template matches 7/7 for those tokens.

**F3 — the landed lazy rationale is weaker than the measured fact.**
Landed: "because scratch is allocated on the real path, not at parse time". Measured
(`receipts/lazy-arm.txt`): with a fresh **usable** `TMPDIR` all five exit 0 and leave the directory
empty (`before=0 after=0`); with an unusable `TMPDIR` all five still exit 0 (5/5). So none of the
five allocates scratch at all — they work on the real tree and never consult the scratch root. The
draft says that, and keeps the counter's warning that a lazy exit 0 is never a pass on the contract.

**F4 — the landed section carries no source citation, and S280 now exists for it.**
Lines 71-102 hold no `S27x`/`S280` token. At my first census `corpus/SOURCES.md` had 139 rows ending
at S279; the sources scribe then appended **S280** (GNU Coding Standards §4.4 — "`program:
message`", message not capitalized; extraction
`.ufo/evidence/round-55/assimilation/S280-gnu-errors.txt`), and that row's `mined` column names
`corpus/knowledge/scratch-root-contract.md` as its consumer. The note is therefore the document that
is supposed to cite S280 and does not. The draft cites it for the one-line shape and keeps S277-S279
on the `TMPDIR` arms.

**F5 — OBSERVATION for the L1, not something I can rule on: `repeat-control` still prints a setup token on stdout.**
Deliverable 1 says the refused arm leaves "no `RuntimeError` token, no traceback, stdout carries no
setup error". Measured (`receipts/nine-allocating-modes.txt`, `repeat-control-selftest`): rc=2,
stderr = the frozen grammar (MATCH), stdout = 28 bytes `REPEAT_CONTROL: setup_error`. That token is
pre-existing and documented (`git show 0a2010ac:tools/repeat-control.py` lines 43-46 name
`setup_error` as "this tool's own failure class"; the emit is at base line 216), it is that tool's
finding-id vocabulary rather than the cross-tool class, and the frozen counter passes it (it rejects
only `RuntimeError`/`Traceback` on either stream). I did not change it: removing it is a tool
behaviour change, not a note edit. The draft states the edge so a stdout parser cannot mistake
`setup_error` for the class line; whether the letter of deliverable 1 requires its removal is the
L1's call.

**F6 — the freeze manifest lagged its own files during the amendment cycle, then converged.**
Observed at 13:50 (`receipts/freeze-check.txt`): `freeze.json` was written 13:49:59 and
`contract.json` + `c2/measure.py` were edited 13:50:08, so three digests drifted and the manifest
listed amendments `[1,2,3]` while the contract already declared more. Re-read at 14:14
(`receipts/counter-evolution.txt`): **match=7/7**, seven files, `amendments [1..7]` on both sides —
the manifest again certifies the bytes it holds, including `c2/measure.py` at `36ca47d3…`. Recorded
because the window existed and a reader of the 13:50 state would have seen a false certificate;
nothing is fixed by me (frozen files).

**F7 — the frozen contract names "the frozen grammar" without carrying its bytes.**
`grep -c "cannot create clone scratch under the scratch root" .ufo/evidence/round-55/contract.json`
→ `0`; the C2 target says "one stderr line matching the frozen grammar" and gives no literal, so the
only in-repo copy is the counter's `GRAMMAR` regex and, after this round, the note's rendering.
Reported, not fixed. Consequence for my item: the draft quotes the regex verbatim, so the readable
copy cannot drift from the counter's bytes without a diff.

**F8 — the counter's own docstring still says eight allocating modes.**
`c2/measure.py` line 17 "grammar  8 allocating modes (the seven self-tests + `env-diff --contract`)",
line 24 "… and the eight allocating modes issue no mkdir", line 28 "names all eight allocating
modes" — while the live table has nine and the note target is `len(allocating)`. The code is right
(`len(allocating)`, `cheap` lists); the prose is stale. Report-only: it is frozen, and a reader who
trusts the docstring instead of the table would expect an 8-mode note arm. The draft never quotes the
docstring; it names the nine modes the table produces.

## Gates

- Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` exits
  **0** at round start (139 rows, S001-S279) and at round end (140 rows, S001-S280 — the sources
  scribe registered S280 during the wave) — `receipts/census.txt`.
- Lane mutation by this seat: none. Production-file mtimes are all earlier than my first write
  (13:40-13:52, L1/sources-scribe), and my writes sit only under the untracked
  `.ufo/waves/round-55/` (`T55W1ScribeNote.md`, `T55W1Er10.md`,
  `T55W1ScribeNote-receipts/`). `git status --porcelain` grew from 14 entries at my first
  observation to 43 at my last, every addition being another seat's work — `receipts/lane-status.txt`.
  HEAD is `631cd64` (the freeze commit); I ran no mutating git/jj command on the lane. The one commit
  I made was inside a scratch clone (later reclaimed), so the durable form is the patch.

## Measurement in a scratch clone (not the lane)

- **Note arm, reproducible from the surviving patch** (`receipts/patch-apply.txt`): a fresh clone of
  the lane at `631cd64`, `git apply receipts/one-line-section.patch` (79 insertions), patched note's
  last 79 lines byte-identical to `receipts/draft-section.md`, then the frozen counter's own
  `modes()` + whitespace normalization over that note → **note_arm=9/9, lazy=5/5**
  (`receipts/note-arm-draft.txt`); the landed text scores the same
  (`receipts/note-arm-landed.txt`).
- **Grammar arm on captured lines** (`receipts/grammar-check.txt`, `receipts/nine-allocating-modes.txt`):
  all nine allocating modes were run from the lane's working tree with `TMPDIR=<nonexistent>`; each
  exits 2 with exactly one stderr line, all nine match the frozen `GRAMMAR` (9/9), and stdout is
  empty except `repeat-control`'s 28-byte status token (F5).
- **Lazy arm** (`receipts/lazy-arm.txt`): 5/5 exit 0 under the unusable `TMPDIR`; 5/5 exit 0 with a
  fresh usable `TMPDIR`, which stays empty (`before=0 after=0`).
- **Not run: the full frozen C2 counter.** It was launched against a scratch clone and produced no
  receipt because my seat scratch directory was removed while it ran
  (`receipts/scratch-reclaim.txt`: the parent still held sibling seat dirs, mine alone was gone). No
  C2 verdict is claimed here; the deciding run at the integrated revision is the L1's. Also not
  claimed: the empty/usable and registry `docs` arms — other seats' surfaces; the working tree
  nevertheless shows 56 registry rows with 7 `scratch_root` cells, all 7 carrying the marker
  (`receipts/helpers-and-cells.txt`).

## Out of scope (not done by this seat)

Tool edits (`tools/repeat-control.py`, `tools/context-capture.py`, the `registry-check --rev` fix),
the seven registry `scratch_root` cells, `SKILL.md` (including the drift section), `SCORECARD.md`,
`corpus/lessons/**`, `LOG.md`, `corpus/SOURCES.md`. No mutating git/jj command touched the lane.

## Tooling

Nothing installed or upgraded; no pacman/uv/npx/official-binary step was needed. Tools used: `git`
(clone/apply/status), `python3` (`importlib` loading of the frozen counter), `strace` (only inside the
frozen counter's own arms), `grep`/`find` through the harness.

## Artifacts

- `.ufo/waves/round-55/w1/T55W1ScribeNote.md` — this report.
- `.ufo/waves/round-55/w1/T55W1Er10.md` — the drop-in draft section (deliverable).
- `.ufo/waves/round-55/w1/T55W1ScribeNote-receipts/one-line-section.patch` — patch on `631cd64`.
- `.../draft-section.md` — the section body alone (79 lines).
- `.../note-arm-draft.txt`, `.../note-arm-landed.txt` — the counter's own note arm, both 9/9 + 5/5.
- `.../patch-apply.txt` — clone + `git apply` + body-identical check + note arm, reproducible now.
- `.../scratch-reclaim.txt` — the observed loss of the seat scratch dir.
- `.../counter-evolution.txt` — counter sha, mode table, note target, amendments, freeze digests
  (7/7), and the 8→9 mode change.
- `.../grammar-check.txt` — regex, nine captured lines 9/9 MATCH, template renders 7/7.
- `.../nine-allocating-modes.txt` — per-mode rc, stdout bytes, stderr line 1, grammar verdict.
- `.../lazy-arm.txt` — five lazy modes, unusable and usable arms, empty TMPDIR after.
- `.../exception-classes.txt` — the class split (F1).
- `.../helpers-and-cells.txt` — seven `strict_scratch_root()` definitions, 56 registry rows,
  7 `scratch_root` cells each carrying the marker.
- `.../freeze-check.txt`, `.../lane-status.txt` — freeze audit (F6) and lane state.
- `.../census.txt` — census exit 0 at start (139 rows) and end (140 rows).
- Raw per-mode captures: `*-selftest.{out,err}`, `env-diff-*.{out,err}`, `registry-check-rev.{out,err}`,
  `lazy-*.{out,err}`, `lzu-*.{out,err}`. There is no `c2-full.out`: no counter verdict is claimed.

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
  (`.ufo/evidence/round-55/c2/measure.py`), plus one real rendered operator line. The round's claim
  statement writes the same optional group as `(\.py)?`; the counter writes `(?:\.py)?` — identical
  language, and the draft quotes the counter.
- (b) the eight allocating modes named exactly as the counter's mode ids: `env-diff --selftest`,
  `env-diff --contract`, `repeat-control --selftest`, `registry-check --selftest`,
  `bash-witness-study selftest`, `pin-disposition --selftest`, `evidence-disposition --selftest`,
  `context-capture --selftest`.
- (c) the five lazy modes (`repeat-control --snapshot`, `bash-witness-study count`,
  `pin-disposition --read`, `evidence-disposition --json`, `context-capture --check`) and why they
  keep their exit — measured, not assumed: they allocate no scratch at all (below).
- (d) the honest boundary: the class is an operator-visible line grammar, **not** a shared Python
  type. The draft states the tree's real split, which is not the item's phrasing: six of the seven
  tools declare their own local `ScratchRootUnusable(RuntimeError)`; `registry-check` declares no
  class and raises the builtin `RuntimeError` with the same text. That is stated rather than
  papered over, and `registry-check` is named as the proof that a conforming tool may have no
  exception class at all.
- Citations: S277-S279 stay attached to the `TMPDIR` arms (S277 the definition, S278 the resolver,
  S279 the documented order). The sources scribe registered **S280** (GNU Coding Standards §4.4
  Formatting Error Messages: `program: message`, message not capitalized) for the one-line shape
  while this seat was running; the draft cites it, grounded in the verbatim extraction
  `.ufo/evidence/round-55/assimilation/S280-gnu-errors.txt`. The mode inventories are the counter's
  own table and are stated as a lane measurement, not a sourced claim — no row is borrowed for them.

Patch: `.ufo/waves/round-55/w1/T55W1ScribeNote-receipts/one-line-section.patch` — 76 insertions on
`631cd64`, applied to a fresh clone of the lane (`git clone --shared`) and committed there as
`fbd75fafe3ae2801e341077560b71143e2ea2a1d`; `git rev-parse --show-toplevel` was asserted equal to
the clone before committing, `git apply --check` passes, and the patched file's last 76 lines are
byte-identical to `receipts/draft-section.md` (`receipts/patch-apply.txt`). Prose is wrapped to the
note's ~78-column width; only the regex and the rendered line exceed it, because a grammar is one
token.

## State of the landed text (not mine, observed)

The working tree already carried an uncommitted `## One line, every mode (round 55)` section
(`corpus/knowledge/scratch-root-contract.md` lines 74-98, mtime 13:41:14, same second as `SKILL.md`)
plus a new paragraph before it. It is a sibling/L1 edit; I did not touch it. It **passes the note
arm** (receipt `note-arm-landed.txt`: 8/8 allocating ids, 5/5 lazy ids), so the arm is satisfiable
today; the corrections below are accuracy — a false sentence, an unmatchable template and a missing
citation — not arm-passing failures.

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
kind of thing; `registry-check` has none (inline `raise RuntimeError(...)` at `tools/registry-check.py:766`);
no cross-tool import and no shared module. The item's own phrasing ("the seven tools keep their own
exception classes") is likewise inaccurate for `registry-check`. The draft states the accurate split.

**F2 — the landed section prints a template, not the counter's grammar.**
Landed: `    <tool>: could-not-evaluate: ... '<value>' (could-not-evaluate)`. The counter carries the
regex (receipt `grammar-check.txt`):

```
^[A-Za-z][A-Za-z0-9_.-]*(?:\.py)?: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '.+' \(could-not-evaluate\)$
```

`<tool>` / `<value>` are not matchable and hide that the leading token is not uniform. The eight
allocating modes actually print seven distinct tokens (receipt `eight-allocating-modes.txt`):
`ENVDIFF_SETUP` (both `env-diff` modes), `repeat-control`, `registry-check`, `WITNESS_STUDY`,
`pin-disposition.py`, `evidence-disposition.py`, `context-capture.py`; all eight lines match the
regex 8/8, and the draft's rendered template matches 7/7 for those seven tokens.

**F3 — the landed lazy rationale is weaker than the measured fact.**
Landed: "because scratch is allocated on the real path, not at parse time". Measured
(`receipts/lazy-arm.txt`): with a fresh **usable** `TMPDIR` all five exit 0 and leave the directory
empty (`before=0 after=0`); with an unusable `TMPDIR` all five still exit 0 (5/5). So none of the
five allocates scratch at all — they work on the real tree and never consult the scratch root. The
draft says that, and keeps the counter's warning that a lazy exit 0 is never a pass on the contract.

**F4 — the landed section carries no source citation, and a row now exists for it.**
Lines 74-98 hold no `S27x`/`S280` token. At my first census `corpus/SOURCES.md` had 139 rows ending
at S279, so nothing existed to cite; while this seat ran, the sources scribe appended **S280** (GNU
Coding Standards §4.4 Formatting Error Messages — "`program: message`", message not capitalized;
extraction `.ufo/evidence/round-55/assimilation/S280-gnu-errors.txt`), and that row's own `mined`
column names `corpus/knowledge/scratch-root-contract.md` as its consumer. So the note is now the
document that is supposed to cite S280 and does not. The draft cites it for the one-line shape (and
keeps S277-S279 on the `TMPDIR` arms), which also removes the need for any `S-pending` marker.

**F5 — OBSERVATION for the L1, not something I can rule on: `repeat-control` prints a setup token on stdout.**
Deliverable 1 says the refused arm must leave "no `RuntimeError` token, no traceback, stdout carries
no setup error". Measured (`receipts/eight-allocating-modes.txt`, `repeat-control-selftest`):
rc=2, stderr = the frozen grammar (MATCH), stdout = 28 bytes `REPEAT_CONTROL: setup_error`. That
token is pre-existing and documented (`git show 0a2010ac:tools/repeat-control.py` lines 43-46 name
`setup_error` as "this tool's own failure class"; the emit is at base line 216), it is the tool's
finding-id vocabulary rather than the cross-tool class, and the frozen counter passes it (it rejects
only `RuntimeError`/`Traceback` on either stream). I did not change it: removing it is a tool
behaviour change, not a note edit. The draft states the edge so a stdout parser cannot mistake
`setup_error` for the class line; whether the letter of deliverable 1 requires its removal is the
L1's call.

**F6 — frozen-set integrity, report-only (I did not edit frozen files).**
`freeze.json` lists six digests and declarations "amendments" 1-3 (the c2 counter's clone-branch
fix, whitespace-normalized matching, and the `bash-witness-study selftest` mode-id label). Timestamps
and digests (`receipts/freeze-check.txt`, `receipts/lane-status.txt`):

```
freeze.json      written 13:49:59
contract.json    edited  13:50:08   digests 0b99dd8cd1e8 vs frozen ed6871e17697   DRIFT
c2/measure.py    edited  13:50:08   digests d6ca1d851bb0 vs frozen ab3ae7514691   DRIFT
the other four files                                                             ok
```

So at the moment of the audit the manifest no longer matches two of the six files it certifies. If
the amendment flow is mid-flight this is transient (re-hash the two entries); if not, the manifest
certifies bytes the counter no longer has. Reported, not fixed. The counter's `GRAMMAR`, `MARKER`,
`NOTE` and mode ids are unchanged across that edit (re-read after 13:50:08: note arm still 8/8 for
both the draft and the landed text).

**F7 — the frozen contract names "the frozen grammar" without carrying its bytes; the note is the only
human-readable copy.**
`grep -c "cannot create clone scratch under the scratch root" .ufo/evidence/round-55/contract.json`
→ `0`; the contract's C2 target says "one stderr line matching the frozen grammar" and gives no
literal. The only in-repo copy of the bytes is `c2/measure.py`'s `GRAMMAR` (verified:
`^[A-Za-z][A-Za-z0-9_.-]*(?:\.py)?: … \(could-not-evaluate\)$`), which is a regex, and the note after
this round is the readable rendering. Reported, not fixed (frozen files). Consequence for my item:
the draft quotes the regex, so the note does not silently disagree with the counter's bytes.

## Gates

- Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` exits
  **0** at round start (139 rows, S001-S279) and at round end (140 rows, S001-S280 — the sources
  scribe registered S280 during the wave) — `receipts/census.txt`.
- Lane mutation by this seat: none. `git status --porcelain` showed 14 entries at my first observation
  and 18 at my last; every addition is another seat's work (`LOG.md`, `corpus/SOURCES.md`,
  `corpus/lessons/round-55.md`, `.ufo/evidence/round-55/assimilation/`), and my writes sit only under
  the untracked `.ufo/waves/round-55/` (`T55W1ScribeNote.md`, `T55W1Er10.md`, `T55W1ScribeNote-receipts/`).
  Production-file mtimes are all earlier than my first write (13:41 and 13:52 from the L1/sources
  scribe, never mine) — `receipts/lane-status.txt`. HEAD is `631cd64` (the freeze commit).

## Measurement in a scratch clone (not the lane)

- **Note arm, reproducible from the surviving patch** (`receipts/patch-apply.txt`): a fresh clone of
  the lane at `631cd64`, `git apply receipts/one-line-section.patch` (76 insertions), patched note's
  last 76 lines byte-identical to `receipts/draft-section.md`, then the frozen counter's own
  `modes()` + whitespace normalization over that note → **note_arm=8/8, lazy=5/5**
  (`receipts/note-arm-draft.txt`; the landed working-tree text scores the same — `note-arm-landed.txt`).
- **Grammar arm on captured lines** (`receipts/grammar-check.txt`): the eight allocating modes were
  run from the lane's working tree with `TMPDIR=<nonexistent>`; all eight exit 2 with exactly one
  stderr line, and all eight lines match the frozen `GRAMMAR` 8/8
  (`receipts/eight-allocating-modes.txt`). The draft's rendered template also matches 7/7 for the
  seven distinct tokens, so the quoted shape is the shape the tools emit.
- **Lazy arm** (`receipts/lazy-arm.txt`): 5/5 exit 0 under the unusable `TMPDIR`; 5/5 exit 0 with a
  fresh usable `TMPDIR`, which stays empty (`before=0 after=0`).
- **Not run: the full frozen C2 counter.** It was launched against a scratch clone and produced no
  receipt because my seat scratch directory was removed while it ran
  (`receipts/scratch-reclaim.txt`: the parent still holds sibling seat dirs, mine alone is gone). No
  C2 verdict is claimed here; the deciding run at the integrated revision is the L1's. Also not
  claimed: the `empty`/`usable` arms and the registry `docs` arm — other seats' surfaces; the working
  tree nevertheless shows 56 registry rows with 7 `scratch_root` cells, all 7 carrying the marker
  (`receipts/helpers-and-cells.txt`).

## Out of scope (not done by this seat)

Tool edits (`tools/repeat-control.py`, `tools/context-capture.py`), the seven registry
`scratch_root` cells, `SKILL.md` (including the drift section), `SCORECARD.md`, `corpus/lessons/**`,
`LOG.md`, `corpus/SOURCES.md`. No mutating git/jj command touched the lane; the one commit I made was
inside a scratch clone and that clone was later reclaimed (`receipts/scratch-reclaim.txt`) — the
durable form of the change is `receipts/one-line-section.patch`, re-applied and re-checked after the
loss.

## Tooling

Nothing installed or upgraded; no pacman/uv/npx/official-binary step was needed. Tools used:
`git` (clone/status), `python3` (counters, `importlib` loading of the frozen module), `strace` (only
inside the frozen counter's own arms), `grep`/`find` via the harness.

## Artifacts

- `.ufo/waves/round-55/w1/T55W1ScribeNote.md` — this report.
- `.ufo/waves/round-55/w1/T55W1Er10.md` — the drop-in draft section (deliverable).
- `.ufo/waves/round-55/w1/T55W1ScribeNote-receipts/one-line-section.patch` — patch on `631cd64`.
- `.ufo/waves/round-55/w1/T55W1ScribeNote-receipts/draft-section.md` — the section body alone.
- `.../note-arm-draft.txt`, `.../note-arm-landed.txt` — the counter's own note arm, 8/8 and 5/5.
- `.../patch-apply.txt` — clone + `git apply` + body-identical check + note arm, reproducible now.
- `.../scratch-reclaim.txt` — the observed loss of the seat scratch dir (why no full-counter receipt).
- `.../grammar-check.txt` — regex, eight captured lines 8/8 MATCH, template renders 7/7.
- `.../eight-allocating-modes.txt` — per-mode rc, stdout bytes, stderr line 1.
- `.../lazy-arm.txt` — five lazy modes, unusable and usable arms, empty TMPDIR after.
- `.../exception-classes.txt` — the class split (F1).
- `.../helpers-and-cells.txt` — seven `strict_scratch_root()` definitions, 56 registry rows,
  7 `scratch_root` cells each carrying the marker.
- `.../freeze-check.txt`, `.../lane-status.txt` — F6 evidence, lane state.
- `.../census.txt` — census exit 0 at start (139 rows, S001-S279) and end (140 rows, S001-S280).
- Raw per-mode captures: `*-selftest.{out,err}`, `env-diff-*.{out,err}`, `lazy-*.{out,err}`,
  `lzu-*.{out,err}`. There is no `c2-full.out`: the full-counter run produced nothing (reclaimed
  scratch), and no counter verdict is claimed.

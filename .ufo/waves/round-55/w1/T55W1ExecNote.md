# T55W1ExecNote — round-55 C2 note: "One line, every mode" applied and measured

Seat: `T55W1ExecNote` (executor, leaf). L1 `TameshiR55`, hyaku run 11, one v2 wave.
Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. Freeze rev `631cd6455e58dce969310b4c0466c3383d9f5108`.
Judged axis: operability. Milestone: C2 note applied.

## What I did

1. Scratch clone (`git clone --shared` of the lane, `checkout --detach 631cd64`), asserted
   `git rev-parse --show-toplevel` = the clone before the single commit.
2. Applied `T55W1ScribeNote`'s draft (`T55W1ScribeNote-receipts/draft-section.md`,
   sha256 `b9822bec…`) as the new `## One line, every mode (round 55)` section — **byte-identical
   append** (last 76 lines of the file hashed `b9822bec…` = the draft) — then made four corrections
   the tree required (C1–C4 below) and one tense fix in the pre-existing `## Falsifier` paragraph.
3. Ran the frozen C2 counter at the clone: **note arm 0/9 → 9/9, grammar still 6/9**.
4. Audited every citation in the resulting note against the clone.

Nothing in the lane's production files was touched; the single commit is in my scratch clone.
Scratch: `$HYAKU_SCRATCH/tameshi-r55/T55W1ExecNote` (`/fast/scratch/hyaku/...`).

## Measured result (frozen counter, `--explain`)

```
C2_R55: rev=82c978eb919e grammar=6/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=0/7 note=9/9 skill=0/1 total=11 C2_R55_PASS=false
```

Verbatim from `receipts/c2-final4.stdout` (the last line of the `--explain` run; the exit code is
1, as the non-note arms are still red on purpose).

- `receipts/c2-final4.stdout` — the shipped commit (`82c978eb`), counter sha256 `0458f632…`.
- `receipts/note-ids-base.txt` — the same counter's own `modes()` table applied to
  `git show 631cd64:corpus/knowledge/scratch-root-contract.md`: every allocating id `MISSING`,
  `note arm at base = 0/9`.
- `receipts/note-ids-final.txt` — per-id listing on the shipped commit: 9/9 allocating,
  5/5 lazy, `marker present: True`, note sha256 `cd16b914…`.

The delta is exactly the note term (9 points). `grammar=6/9` is expected on a note-only commit:
the three modes that still fail the line grammar there (`repeat-control --selftest`,
`context-capture --selftest`, `registry-check --rev`) are the tool edits other seats own.
`docs=0/7` and `skill=0/1` are likewise other seats' deliverables.

### The counter moved under this seat (report, not repaired)

| When | `c2/measure.py` sha256 | allocating modes | my run |
|---|---|---|---|
| seat start | `ab3ae751…` | 8 | `note=8/8 total=10` (`c2-after-note.stdout`, `c2-final.stdout`) |
| after amendments 4–8 | `0458f632…` | 9 (`registry-check --rev`, amendment 6) | `note=9/9 total=11` (`c2-final2/3/4`) |

The item's target was written as "note 0/8 → 8/8"; with the ninth mode the live denominator is
**9**. My first applied draft scored 8/8 on the 8-mode table, so I re-wrote the mode inventory to
nine and re-measured: `receipts/counter-sha-at-remesure.txt`, `receipts/counter-sha-at-final.txt`.
The shipped section states nine because that is what the counter measures today.

## The diff

`receipts/note.patch` — one hunk, `@@ -57,10 +57,97 @@`, **94 insertions / 7 deletions**,
against `631cd64`. Two parts:

**Hunk B (tense fix, 7 lines → 8).** The `## Falsifier` paragraph still read, in the present
tense, "One residue is named, not fixed: `tools/context-capture.py` exits 2 … prefixes the line
with `SELFTEST: FAIL`" — false the moment this round's tool edit lands, and false in the lane's
current HEAD. Rewritten to past tense with one sentence pointing at the section that states the
line. (The lane's own integration instead *kept* the false sentence and appended a
"Round 55 closed that residue" paragraph after it — see F1.)

**Hunk A (the section, 76 draft lines → 86).** Content, in order: the counter's `GRAMMAR` regex
verbatim plus one rendered operator line; the per-tool leading token with the "key on the tail,
never the prefix" rule; the nine allocating modes and what each does under an unusable `TMPDIR`;
`registry-check --rev`'s grammar-arm-only measurement; the five lazy modes and why a lazy exit 0
is not a pass; the boundary paragraph (line grammar, not a shared type); two named edges; the
sources (S277–S280).

### C1–C4 — corrections to the scribe draft, each measured

- **C1** `registry-check --rev` added to the inventory (the draft predated the ninth mode).
  `receipts/counter-sha-at-remesure.txt` shows the counter's table demanding it.
- **C2** The draft's "six of the seven tools declare their own local `ScratchRootUnusable`, and
  `registry-check` declares none" became false when `tools/registry-check.py` was repaired in
  this round's C0 commit. At HEAD all seven declare it:
  `git show HEAD:tools/<t>.py | grep -c 'class ScratchRootUnusable'` → 1 for each of
  `env-diff`, `repeat-control`, `registry-check`, `bash-witness-study`, `pin-disposition`,
  `evidence-disposition`, `context-capture`; cross-tool imports: 0. Rewritten to seven local
  near-copies with no import, which is a *stronger* instance of the same claim.
- **C3** The draft's "the eight modes print `ENVDIFF_SETUP`, `repeat-control`, `registry-check`, …"
  enumerated seven labels for eight modes without saying which tool owns which. Rewritten
  per tool: `env-diff` → `ENVDIFF_SETUP`, `bash-witness-study` → `WITNESS_STUDY`, the other five
  → their own names. Verified against HEAD: `registry-check --rev` prints
  `registry-check: could-not-evaluate: …` on stderr, rc 2, stdout empty.
- **C4** The draft's closing "the grammar is matched on stderr, so a caller that parses stdout
  sees nothing" is false; `repeat-control` writes `REPEAT_CONTROL: setup_error` (28 bytes) to
  stdout. The shipped text names that token as the tool's own finding id instead of denying it.

## Citation audit (the item's check)

```
$ grep -n 'tools/' corpus/knowledge/scratch-root-contract.md      # receipts/cite-grep.txt
60:One residue was named, not fixed, in round 54: `tools/context-capture.py` exited
129:`ScratchRootUnusable(RuntimeError)` — in `tools/env-diff.py`,
130:`tools/repeat-control.py`, `tools/registry-check.py`,
131:`tools/bash-witness-study.py`, `tools/pin-disposition.py`,
132:`tools/evidence-disposition.py` and `tools/context-capture.py` — seven
```

Every cited path resolves in the clone (`receipts/cite-resolve.txt`): `tools/env-diff.py`,
`tools/repeat-control.py`, `tools/registry-check.py`, `tools/bash-witness-study.py`,
`tools/pin-disposition.py`, `tools/evidence-disposition.py`, `tools/context-capture.py` — 7/7 `OK`,
0 `MISS`. The other path citations in the note (`.` and
`.ufo/evidence/round-55/c2/measure.py`) resolve too (`receipts/cite-resolve-other.txt`).

The source tokens resolve as well: `S277`, `S278`, `S279`, `S280` each match exactly one row in
`corpus/SOURCES.md` (`grep -c '^| S27N |'` = 1 each). S280's own `mined` column names
`corpus/knowledge/scratch-root-contract.md`, so the note is the document obliged to cite it — the
landed section cites none (F5).

**No line numbers are cited for lane files, deliberately:** the section lands in the same commit as
three tool edits, so any `tools/x.py:NNN` written at `631cd64` would be off by the time a reader
opens it. Path + symbol is the stable anchor.

## Findings against the text landed in the lane (report-only)

HEAD at the time of writing is `4f7a704` (`c31cdd9` when I first compared; the note text is
identical across the two — `git diff c31cdd9 4f7a704 -- corpus/knowledge/scratch-root-contract.md`
is empty); the section landed in `9cf0146`. Each finding has the command and its output; these are
accuracy defects in that text, not arm failures (the landed section also names all nine modes).

**F1 — the residue sentence is left present-tense and false.** Landed lines 60–64 still read
"One residue is named, not fixed: `tools/context-capture.py` exits 2 … prefixes the line with
`SELFTEST: FAIL`", followed by "Round 55 closed that residue". Measured at HEAD:
`TMPDIR=/no-such-r55 python3 tools/context-capture.py --selftest` → rc 2, stdout 0 bytes,
stderr = the grammar line. My Hunk B replaces the sentence instead of contradicting it.

**F2 — the class sentence is false at HEAD.** Landed: "(`ScratchRootUnusable` in the two round-55
edits, a local class in `env-diff`)". Measured: seven tools declare `class
ScratchRootUnusable(RuntimeError)` (one each), zero imports, and three tools were edited this
round (`repeat-control`, `context-capture`, `registry-check`), not two.

**F3 — "a caller that parses stdout sees nothing" is false.** Measured at HEAD:
`TMPDIR=/no-such-r55 python3 tools/repeat-control.py --selftest` → rc 2, stdout 28 bytes
`REPEAT_CONTROL: setup_error`, stderr = the grammar line. **Status at 14:47: a sibling has already
corrected this sentence in the lane worktree** (uncommitted, `git diff` at that moment: "The grammar
is matched on stderr, so a caller that reads only stdout sees no class line — but it can still see
each tool's own verdict token there (`REPEAT_CONTROL: setup_error` is the one that remains)"), which
is the same fact my shipped text states. F1, F2, F4 and F5 were still present in that worktree.

**F4 — the lazy rationale is weaker than the measurement.** Landed: "because scratch is allocated
on the real path, not at parse time". Measured (`T55W1ScribeNote-receipts/lazy-arm.txt`): the five
modes never allocate at all — with a fresh usable `TMPDIR` the directory is still empty
(`before=0 after=0`). The shipped text says that.

**F5 — the landed section prints an unmatchable template and cites no source.** It shows
`<tool>: could-not-evaluate: … '<value>' …` rather than the counter's regex, and carries no
`S27x`/`S280` token although S280 exists and names this file as its consumer. The shipped section
prints the regex, one rendered line, and the four source tokens.

## Observations (not defects of my item)

**G1 — the frozen counter is a moving target inside one wave.** Three shas in one seat:
`ab3ae751` (8 modes) → `0458f632` (9 modes, amendments 4–8). Anyone who measured "8/8" earlier in
the wave now has a stale denominator. The freeze commit `631cd64` carries `9d076812`, and its own
`freeze.json` correctly names that blob — so the *commit* is self-consistent; it is the working
tree that has moved three times. Consequence for the L1: re-check the note arm against the final
counter bytes before the deciding run — the cheap check is:

```
python3 - <<'PY'
import importlib.util
s = importlib.util.spec_from_file_location("m", ".ufo/evidence/round-55/c2/measure.py")
m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
t = m.modes(__import__("pathlib").Path("/tmp/w"), __import__("pathlib").Path("."))
txt = " ".join(open(m.NOTE).read().split())
alloc = [x[0] for x in t if x[3]]
print(sum(i in txt for i in alloc), "/", len(alloc), [i for i in alloc if i not in txt])
PY
```

**G2 — corroboration of amendment 4's diagnosis (the straddle is real).** My first base run of the
counter at `631cd64` printed `usable=12/13` (`registry-check --selftest` rc=1); two later identical
runs printed `usable=13/13`. I reproduced the failing leg directly and named the cases:
`cd <clone at 631cd64>; TMPDIR=<fresh> strace -f -e trace=mkdir,mkdirat -o log python3
tools/registry-check.py --selftest` → rc **1**, plain (no strace) → rc **0**, with
`SELFTEST: FAIL (2 of 51 cases: timeout-kills-setsid-pipe, timeout-kills-setpgid-pipe)`
(`receipts/probe3-strace.out`; strace dilation ~7× — 242 s vs 33 s). Those two cases assert on
killing a process *group*/*session*, which is exactly what ptrace perturbs. Amendment 4 already
took the exit code from the plain run and left strace the `/tmp` census, so the current counter is
not exposed; this seat's probe is independent evidence that the repair was necessary, not cosmetic.
(The first base receipt itself was lost when the host swept my scratch directory at 13:54; the
reproduction above is the retained evidence.)

**G3 — the section is a statement about the integrated tree.** On a note-only clone the prose's
"nine modes carry the line" and "seven local classes" are not yet true (that clone has 4 classes
and `registry-check --rev` still prints its old stdout form). It is true at `9cf0146`/HEAD, which I
verified by running the three repaired tools. Do not land the note without C0.

## Risks

- The counter may take another amendment before the deciding run; the note names nine modes and
  would need a re-sync if a tenth appears (G1's one-liner detects it in seconds).
- The section's `cheap` sentence is coupled to the counter flag: if amendment 8's bookkeeping or
  the `cheap=False` handling changes again, re-read the "grammar arm only" clause.
- `docs=0/7` and `skill=0/1` are outside this seat; the note arm alone cannot make C2 pass.

## Lane hygiene

- Lane production files: untouched by this seat. At hand-off, lane HEAD is `4f7a704` with four
  production files dirty from other seats (`corpus/knowledge/scratch-root-contract.md`,
  `tools/context-capture.py`, `tools/registry-check.py`, `tools/registry.json`); my writes are
  confined to `.ufo/waves/round-55/w1/T55W1ExecNote.md` and
  `.ufo/waves/round-55/w1/T55W1ExecNote-receipts/` (24 untracked files).
- No mutating git command anywhere except `add`/`commit --amend` inside my own clone, after
  asserting `rev-parse --show-toplevel`.
- Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` →
  exit **0**, 140 rows (S001–S280; S280 registered during this wave).
- Tooling: nothing installed or upgraded. `git`, `python3`, `strace` (the last only inside the
  counter's own arms and my probe).

## Artifacts

- `.ufo/waves/round-55/w1/T55W1ExecNote.md` — this report.
- `.ufo/waves/round-55/w1/T55W1ExecNote-receipts/note.patch` — the diff on `631cd64`
  (94 insertions, 7 deletions).
- `.../note-commit.txt`, `.../note-sha.txt` — clone commit `82c978eb` and the shipped note's sha256.
- `.../c2-final4.stdout`, `.../c2-final4.stderr` — the counter on the shipped commit.
- `.../c2-final2.stdout`, `.../c2-final3.stdout` — earlier 9-mode runs (same verdict).
- `.../c2-after-note.stdout`, `.../c2-final.stdout` — the 8-mode-counter runs (note 8/8, total 10).
- `.../note-ids-base.txt`, `.../note-ids-final.txt` — per-id note arm, 0/9 at base, 9/9 shipped.
- `.../counter-sha-at-remesure.txt`, `.../counter-sha-at-final.txt` — the counter bytes each run used.
- `.../cite-grep.txt`, `.../cite-resolve.txt`, `.../cite-resolve-other.txt` — citation audit.
- `.../probe3-strace.out`, `.../probe2-strace.log` — G2 reproduction: the named failing selftest
  cases and the strace'd run's log at the counter's own cwd.
- `.../section-from-file.md`, `.../section-from-report.md` — proof the appendix below is
  byte-identical to the shipped section (`diff` empty).

## Appendix — the section as shipped

```markdown
## One line, every mode (round 55)

Round 55 closed the round-54 residue (`context-capture` no longer prefixes
`SELFTEST: FAIL`; it and `repeat-control` print the line below) and widened
the measurement from the self-test to every documented allocating mode. The
class is one stderr line, matched by the counter's own pattern
(`.ufo/evidence/round-55/c2/measure.py`, `GRAMMAR`):

    ^[A-Za-z][A-Za-z0-9_.-]*(?:\.py)?: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '.+' \(could-not-evaluate\)$

so what an operator sees is

    repeat-control: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/no/such/dir' (could-not-evaluate)

The leading token is each tool's own setup label, not a fixed string: at round
55 `env-diff`'s two modes print `ENVDIFF_SETUP`, `bash-witness-study` prints
`WITNESS_STUDY`, and the other five print their own names (`repeat-control`,
`registry-check`, `pin-disposition.py`, `evidence-disposition.py`,
`context-capture.py`) — `env-diff` and `registry-check` each cover two modes.
A caller keys on the tail from
`: could-not-evaluate: cannot create clone scratch under the scratch root:`
onward, never on the prefix. The pattern admits a letter followed by letters,
digits, `_`, `.` or `-`; the value is the `%r` rendering of the rejected
pathname, so a path holding a quote is echoed with its quotes, and the line
is a diagnostic — not an invocation to re-enter in a shell. The shape itself
is the standard's: a noninteractive program's message is one program-prefixed
line, `program: message`, and the message does not begin with a capital letter
when it follows the program name (S280) — which is why the class is one line
and why `could-not-evaluate` is lower-case.

### The nine allocating modes

`env-diff --selftest`, `env-diff --contract`, `repeat-control --selftest`,
`registry-check --selftest`, `registry-check --rev`,
`bash-witness-study selftest`, `pin-disposition --selftest`,
`evidence-disposition --selftest`, `context-capture --selftest`. Each exits 2
under a set-but-unusable `TMPDIR`, prints that one line on stderr, and prints
no `RuntimeError` or `Traceback` token on either stream. `registry-check --rev`
is measured on the grammar arm only: it builds a full fleet clone, so its
usable path stays with the tool's own self-test (the counter's `cheap` flag).
The arm's meaning is S277's ("a pathname of a directory made available for
programs that need a place to create temporary files"); the empty value stays
the round-54 arm (S278 `_candidate_tempdir_list`:163-165 and S279's documented
order).

### The five lazy modes

`repeat-control --snapshot`, `bash-witness-study count`,
`pin-disposition --read`, `evidence-disposition --json`,
`context-capture --check` keep their expected exit under the same unusable
`TMPDIR`. None of them allocates scratch: they work on the real tree, and
the scratch root is consulted on first use — never at import or argument
parse — by the modes that clone. A lazy mode's exit 0 is therefore not
evidence that the scratch root was usable: it is never a pass on this
contract, and the counter measures it only as "unchanged exit".

### The boundary: a line grammar, not a shared type

The contract is the operator-visible line, not a shared Python type. No
module implements it once: each of the seven tools declares its own local
`ScratchRootUnusable(RuntimeError)` — in `tools/env-diff.py`,
`tools/repeat-control.py`, `tools/registry-check.py`,
`tools/bash-witness-study.py`, `tools/pin-disposition.py`,
`tools/evidence-disposition.py` and `tools/context-capture.py` — seven
near-copies of the helper under the same class name, with no import between
them. A tool could satisfy the contract with no exception class at all: the
type only exists so a tool can catch its own refusal at the entry point. Seven
standalone scripts should not depend on one module (or
on one another) for a one-line rule; what must stay equal is the bytes on
stderr and the exit code, not the type name.

Two edges are stated, not hidden. The counter reads stderr, so a caller
that parses stdout finds no class line — and `repeat-control` still prints
its own `REPEAT_CONTROL: setup_error` there, a documented finding id that
maps to exit 2 and belongs to that tool's vocabulary, not to the cross-tool
class. And the inventory's only authority is the registry plus the tools'
usage text: a documented mode in neither place would allocate scratch
unmeasured.

Sources: S277-S279 remain the authority for the `TMPDIR` arms above (S277 the
definition, S278 the resolver's skip-empty rule, S279 the documented order),
and S280 is the authority for the one-line shape. The nine-mode and
five-mode inventories are the round-55 counter's own table
(`.ufo/evidence/round-55/c2/measure.py`) — a lane measurement, not a sourced
claim.
```

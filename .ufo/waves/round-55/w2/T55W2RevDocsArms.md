# T55W2RevDocsArms — the C2 documentation arms at C0

Seat: T55W2RevDocsArms (wave 2, attack). Judged on: operability. Milestone: attack the docs arms.

**Revision note.** Assigned revision is content commit C0 `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`
(base `0a2010ac`, freeze `e2979f2`). While this review ran, the lane moved to `c31cdd9`
(commit `133b2ce` = freeze amendment 8, then `c31cdd9` = contract C2 before-value F4). The three
surfaces I was asked to attack are **byte-identical** between C0 and `c31cdd9`:

```
$ git diff --quiet 9cf0146 c31cdd9 -- tools/registry.json && echo SAME
SAME
$ git diff --quiet 9cf0146 c31cdd9 -- corpus/knowledge/scratch-root-contract.md && echo SAME
SAME
$ git diff --quiet 9cf0146 c31cdd9 -- SKILL.md && echo SAME
SAME
```

So every finding below is measured on committed bytes and is live at HEAD except F1, which amendment
8 closed after C0 and which I report because it is the state at the revision I was assigned and
because its docstring residue is still open (F4).

Two later movements are worth naming so nothing here is misread as a working-tree claim. First, while
this review ran the **working tree** gained uncommitted edits to `tools/registry.json`, the note and
two tools from other seats; the registry diff shows the seven cells being rewritten from the false
`<tool>.py:` token to the token each tool actually prints (`repeat-control:`, `WITNESS_STUDY:`,
`registry-check:`, `ENVDIFF_SETUP:`) plus "and no verdict token", and the note's closing paragraph
being rewritten to say a stdout reader sees the tool's own verdict token. That is F2 and residual
gap 1 being repaired in flight — F2 is therefore reported against C0/`c31cdd9` bytes. Second,
`git status` at the time of writing shows those files `M`; I did not write any of them (my only writes
are this file and `T55W2RevDocsArms-receipts/`).

All work was read-only: a `git clone --shared` of the lane checked out at C0 in
`$HYAKU_SCRATCH/tameshi-r55/T55W2RevDocsArms/clone` (removed on exit); no lane production file,
frozen file or wave spec was created, modified or deleted.

---

## Verdicts, claim by claim

| # | Claim (source) | Verdict | Evidence |
|---|---|---|---|
| 1a | Each registry cell describes **its** tool's allocating modes — `selftest` for five, `selftest, --rev` for `registry-check`, `selftest, --contract` for `env-diff` (`tools/registry.json:44,87,135,333,424,620,895`) | **HOLD** | Every `strict_scratch_root()` call site is inside `selftest`/`cmd_selftest`/`SelftestHarness.__init__` except `registry-check.clone_lane_at_rev` (reached only from the `--rev` branch, `tools/registry-check.py:1934`) and `env-diff.execute` (reached from both `--contract` and `--selftest`). Receipt `inventory.txt` |
| 1b | Each cell carries the frozen grammar | **HOLD as a marker probe, WRONG as quoted bytes** for 4 of 7 tools | `cells.txt`: the cell quotes `repeat-control.py:`, `bash-witness-study.py:`, `registry-check.py:`, `env-diff.py:`; the tools print `repeat-control:`, `WITNESS_STUDY:`, `registry-check:`, `ENVDIFF_SETUP:` |
| 1c | "with no `RuntimeError`/`Traceback` token" | **HOLD** | 7/7 selftests: one stderr line, rc 2, no traceback token — `grammar.txt` |
| 1d | "TMPDIR empty => unset, the platform default applies" | **HOLD** | code `t = os.environ.get("TMPDIR"); if t:` (`tools/repeat-control.py:161-167`, `tools/env-diff.py:41-48`); counter empty arm 13/13 rc expected (`c2-head.out`) |
| 1e | "a usable TMPDIR holds every mkdtemp and nothing is created under /tmp" | **HOLD** | counter usable arm 13/13, `tmp_mkdirs=0` (`c2-head.out`); independent strace of the five lazy modes: 0 `mkdir` under TMPDIR (`lazy.txt`) |
| 2a | The note names **all nine** allocating modes | **HOLD** | `arms.txt`: 9/9 labels present; and the nine are exactly every mode that reaches `strict_scratch_root` in the seven tools |
| 2b | The note's grammar quote is byte-identical to the counter's `GRAMMAR` regex | **HOLD** (modulo the `<tool>`/`<value>` placeholders) | `arms.txt`: the literal `could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '<value>' (could-not-evaluate)` is present verbatim in the normalized note; `GRAMMAR` at `c2/measure.py:47-50` differs only in the leading token class and `'.+'` |
| 2c | The five lazy modes "keep their expected exit ... because scratch is allocated on the real path, not at parse time" | **HOLD on the exit, WRONG on the mechanism** | 5/5 rc 0 on both arms and **0 mkdir under TMPDIR** (`lazy.txt`) — these modes never allocate scratch at all, so "allocated on the real path" is false as written |
| 2d | "The counter measures nine allocating modes on the unusable arm, thirteen modes on the empty and usable arms" | **HOLD** | `len(allocating)=9`, `len(cheap)=13` (`c2/measure.py:118-160,255`); run shows `empty=13/13 usable=13/13` |
| 2e | "`registry-check --rev` ... its usable path is covered by the tool's own self-test, which exercises the same helper" | **HOLD** | the selftest runs a child with `--rev` (`tools/registry-check.py:1101`, inside `selftest()` at `:933`), which calls `clone_lane_at_rev` |
| 2f | "`ScratchRootUnusable` in the **two** round-55 edits, a local class in `env-diff`" | **WRONG** | three tools gained the class at C0 (`repeat-control`, `context-capture`, `registry-check` all lack it at base), and `env-diff`'s local class is itself named `ScratchRootUnusable` (`tools/env-diff.py:32`) — `classes.txt` |
| 3a | SKILL: "Measured on every documented allocating mode — the seven self-tests plus `env-diff --contract` and `registry-check --rev`" (`SKILL.md:37-38`) | **HOLD** | nine modes measured; no tenth mode reaches `strict_scratch_root` (mode inventory in `inventory.txt`) |
| 3b | SKILL: "as one stderr line, `<tool>: could-not-evaluate: ...`" (`SKILL.md:39-41`) | **HOLD on the line, OVERREACH on `<tool>`** | one stderr line and rc 2 for 9/9; but for `env-diff` the token is `ENVDIFF_SETUP` and for `bash-witness-study` it is `WITNESS_STUDY`, neither a tool name |
| 3c | SKILL: "the five non-allocating modes stay lazy" (`SKILL.md:41`) | **HOLD** | `lazy.txt` |
| 3d | SKILL: "the seven registry `scratch_root` cells" (`SKILL.md:42-43`) | **HOLD** | `arms.txt`: exactly 7 cells |

---

## Findings

### F1 — HIGH (at C0; closed by amendment 8 after C0): the C0 C2 counter cannot pass at any green state — two wrong denominators

At C0 the total is computed with **14 rows** in the empty/usable terms while those arms run only the
**13** cheap modes, and with a hard-coded **8** in the note term while the note arm counts **9**:

```
$ git show 9cf0146b:.ufo/evidence/round-55/c2/measure.py | sed -n '271,273p'
    total = (len(allocating) - grammar_ok) + (len(lazy) - lazy_ok) \
        + (len(table) - empty_ok) + (len(table) - usable_ok) \
        + tmp_total + (7 - docs) + (8 - note) + (1 - skill)
```

With every arm green (grammar 9/9, lazy 5/5, empty 13/13, usable 13/13, tmp_mkdirs 0, docs 7/7,
note 9/9, skill 1/1) the total is `(14-13)+(14-13)+(8-9) = 1`, and `PASS` requires `total == 0`:

```
$ CLONE=.../clone python3 arms.py arms
docs  = 7/7 (MARKER in each scratch_root cell)
note  = 9/9 mode labels present; missing=[]
skill = 1/1 (MARKER present: True)
--- counter total at C0 bytes with every arm green ---
len(table)=14 cheap=13 note=9
total = (9-9)+(5-5)+(14-13)+(14-13)+0+(7-7)+(8-9)+(1-1) = 1
PASS requires total == 0 and no bad arm -> PASS=False
```

Measured, C0 counter bytes against the C0 revision — every arm green, verdict still false:

```
$ python3 clone/.ufo/evidence/round-55/c2/measure.py --lane <lane> --rev 9cf0146b... --work <empty>
exit status: 1
C2_R55: rev=9cf0146b94dd grammar=9/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=1 C2_R55_PASS=false
```

(`c2-both-revisions.txt`, `c0-counter.out`). The lane's own Amendment 8 admits the same figure:
"*at the all-green state the verdict read total=1 with an empty bad map*"
(`.ufo/evidence/round-55/freeze.json`, amendment 8, commit `133b2ce`). **Status:** `133b2ce` rewrote
lines 272–273 to `(len(cheap) - ...)` / `(len(allocating) - note)`;
the counter run on those bytes at C0 reads
`C2_R55: ... grammar=9/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=0 C2_R55_PASS=true`
(`c2-head.out`). I report F1 because the assigned revision carries it: at C0 the C2 predicate was
unsatisfiable, so any C0-time reading of "the docs arms pass" would have been a failed counter, not
a failed document.

### F2 — MEDIUM (live at HEAD): 4 of 7 registry `scratch_root` cells quote a leading token their tool does not print

The cells are written as exact quotations, e.g. `tools/registry.json:44`:

```
One stderr line, exit 2, could-not-evaluate: "repeat-control.py: could-not-evaluate: cannot create
clone scratch under the scratch root: TMPDIR is not a usable directory: '<value>' (could-not-evaluate)",
```

The tool prints `repeat-control: could-not-evaluate: ...` (no `.py`; `tools/repeat-control.py:231-233`).
Measured on the unusable arm (`cells.txt`):

| cell (line) | claimed token | actual first token |
|---|---|---|
| `repeat-control-selftest` (44) | `repeat-control.py` | `repeat-control` |
| `bash-witness-selftest` (87) | `bash-witness-study.py` | `WITNESS_STUDY` |
| `registry-check-selftest` (620) | `registry-check.py` | `registry-check` |
| `env-diff-selftest` (895) | `env-diff.py` | `ENVDIFF_SETUP` |
| `pin-disposition-selftest` (135) | `pin-disposition.py` | `pin-disposition.py` ✓ |
| `evidence-disposition-selftest` (333) | `evidence-disposition.py` | `evidence-disposition.py` ✓ |
| `context-capture-selftest` (424) | `context-capture.py` | `context-capture.py` ✓ |

The counter cannot see this: the `docs` arm tests only `MARKER in row["scratch_root"]`, and `MARKER`
stops at "…under the scratch root" (`c2/measure.py:46,248`). (At the time of writing, other seats'
uncommitted edits in the working tree rewrite all seven cells to the actual tokens; the finding stands
for C0 and `c31cdd9`.) A caller that anchors a parser on the
quoted prefix (`grep '^repeat-control\.py: could-not-evaluate'`) matches nothing. The claim is an
overreach the measurement surface is blind to, which is exactly the class this round is re-keying.

### F3 — MEDIUM (live at HEAD): the note and SKILL present `<tool>` as the line's first token, but two modes print something else

`corpus/knowledge/scratch-root-contract.md:75` and `SKILL.md:39-40` both write the template as
`<tool>: could-not-evaluate: ...`. Two of the nine allocating modes do not print a tool name:
`env-diff` prints `ENVDIFF_SETUP:` (`tools/env-diff.py:234,264`) and `bash-witness-study` prints
`WITNESS_STUDY:`. The counter's `GRAMMAR` tolerates this (`^[A-Za-z][A-Za-z0-9_.-]*(?:\.py)?:` —
`_` is in the class), so grammar 9/9 is honest; the documents overstate what the slot contains. Note
that this is the *only* reason the table above (F2) passes: the regex is looser than the documents.

### F4 — MEDIUM (live at HEAD): the frozen counter's own docstring still declares eight allocating modes and `N/8`

`.ufo/evidence/round-55/c2/measure.py:17,24,28,32` (bytes unchanged by amendment 8):

```
17:  grammar  8 allocating modes (the seven self-tests + `env-diff --contract`):
24:  usable   13 modes with a fresh TMPDIR exit their expected code, and the eight
28:           names all eight allocating modes;
32: `C2_R55: rev=... grammar=N/8 ... note=N/8 ...`
```

The table it describes holds nine (`:118-160`), the verdict line prints `grammar=%d/%d` and
`note=%d/9` (`:280`), the note says nine, `SKILL.md` says nine, and amendment 6 says
"*Denominators: grammar 8->9, note 8->9*". So the instrument's header contradicts its own body and
every document that reads it. This is the residue amendment 8 did not touch (it changed only lines
272–273).

### F5 — LOW (live at HEAD): the note's reason for the lazy arm is false as written

`corpus/knowledge/scratch-root-contract.md:93-94`: the five lazy modes "keep their expected exit
under an unusable `TMPDIR`, because scratch is allocated on the real path, not at parse time." They
do not allocate scratch at all: with a usable `TMPDIR` they issue **zero** `mkdir`/`mkdirat` under it
and leave it empty (`lazy.txt`), and the counter's own docstring repeats the same figure of speech
("scratch is allocated lazily, never at parse time", `:22`). A reader can only conclude that these
modes do allocate scratch, later. The honest statement is that they never reach
`strict_scratch_root`; the counter's separate sentence ("A lazy mode's exit 0 is not evidence that the
scratch root was usable", `:94-95`) already carries the right caveat, so this is wording, not a
measurement error.

### F6 — LOW (live at HEAD): "the two round-55 edits" is the wrong count

`corpus/knowledge/scratch-root-contract.md:86`: "(`ScratchRootUnusable` in the two round-55 edits, a
local class in `env-diff`)". At base, three of the seven tools have no such class; at C0 all seven do:

```
$ python3 arms.py classes
=== 0a2010ac ===
tools/repeat-control.py            (no ScratchRootUnusable class)
tools/registry-check.py            (no ScratchRootUnusable class)
tools/context-capture.py           (no ScratchRootUnusable class)
=== 9cf0146b ===  (all seven define class ScratchRootUnusable(RuntimeError))
```

Three round-55 edits, not two, and `env-diff`'s "local class" is named `ScratchRootUnusable` too
(`tools/env-diff.py:32`), so the parenthetical distinguishes nothing.

### F7 — LOW (live at HEAD): registry.json was re-emitted whole for seven cell edits

`git diff --numstat 0a2010ac 9cf0146 -- tools/registry.json` → `1275 1026 tools/registry.json`.
The parsed content differs in **exactly the seven `scratch_root` keys** — same 56 rows, same order,
same schema (`diff.txt`) — but the file was re-indented from 2 spaces to 1 (`"  \"schema\"…"` →
`" \"schema\"…"`) and, in later rows, compact one-line arrays were expanded (`:833` region, rows such
as `receipt-window-selftest`). No frozen file or evidence pin in round 55 names `tools/registry.json`
bytes (freeze.json lists only the round-55 evidence files), so nothing breaks; the cost is that a
review of "seven registry cells" has to read a 1026-line rewrite, and the commit message's shape
("seven registry cells") does not describe the diff's shape. It is not a collateral *semantic*
change: no other row's value moved.

---

## Residual risk and verification gaps

1. **The `docs` arm cannot fail on wrong bytes.** It tests `MARKER` only; F2 is invisible to it. Same
   for `skill` (`MARKER in norm(SKILL.md)`). The `note` arm tests only that each of the nine mode
   labels is a substring — it never checks the grammar quote at all, although its docstring says the
   note must "state the grammar" (`c2/measure.py:28`). So the note's template is verified by me, not
   by the counter.
2. **`registry-check --rev` has no usable-arm measurement** by design (documented, and covered by the
   tool's own selftest). I confirmed the selftest drives `--rev` and therefore `clone_lane_at_rev`,
   but the counter does not.
3. **The nine-mode inventory is complete against `strict_scratch_root` call sites, not against
   prose.** I enumerated the documented modes of all seven tools (`repeat-control` `--runs/--snapshot/
   --selftest`; `bash-witness-study` `declare/run/rerun/count/check/selftest`; `pin-disposition`
   default/`--read`/`--selftest`; `evidence-disposition` default/`--json`/`--selftest`;
   `context-capture` `--check/--selftest`; `registry-check` `--root/--rev/--registry/--only/--tag/
   --json/--selftest`; `env-diff` `--contract/--selftest`). Only the nine allocate. A mode outside
   both the registry and the usage text remains unmeasured, as the note itself says.
4. **`ENVDIFF_SETUP` matching the grammar is incidental.** The regex admits `_`; if a future tool
   printed `ENVDIFF SETUP` (a space) it would fail — correctly — but the documents give no rule for
   what the token may be.
5. **`repeat-control --selftest` also writes one stdout line** (`REPEAT_CONTROL: setup_error`) on the
   unusable arm (`grammar.txt` stdout count; `cells.txt`). The "one line" claims are stderr-scoped and
   hold, and `setup_error` is not a verdict token, so no claim is false — recorded because the
   round-54 residue was precisely a stdout verdict token (`SELFTEST: FAIL`).
6. I did not re-run the C1 counter; out of scope for this seat.

---

## Commands and artifacts

Reproduce: `.ufo/waves/round-55/w2/T55W2RevDocsArms-receipts/run.sh` (clones the lane at C0 into
`$HYAKU_SCRATCH/tameshi-r55/T55W2RevDocsArms/clone` and writes `cells.txt`, `diff.txt`,
`grammar.txt`, `lazy.txt`, `arms.txt`, `classes.txt`).

Individual commands (all against the C0 clone unless stated):

```
git clone --shared --no-checkout <lane> clone && git -C clone checkout -B probe 9cf0146b94ddba12d454ebf7288ce6e5c5d535bb
CLONE=clone python3 arms.py {cells,diff,grammar,lazy,arms,classes}
git -C clone diff --numstat 0a2010ac 9cf0146b -- tools/registry.json
python3 .ufo/evidence/round-55/c2/measure.py --lane <lane> --rev 9cf0146b... --work <empty> --explain   # lane bytes (amendment 8)
python3 clone/.ufo/evidence/round-55/c2/measure.py --lane <lane> --rev 9cf0146b... --work <empty>      # C0 bytes
git show 9cf0146b:.ufo/evidence/round-55/c2/measure.py | sed -n '17,32p;261,283p'
```

Artifacts opened (all at C0 unless marked):

- `tools/registry.json` (7 `scratch_root` cells at lines 44, 87, 135, 333, 424, 620, 895)
- `corpus/knowledge/scratch-root-contract.md` (heading `## One line, every mode (round 55)` at :71)
- `SKILL.md` `## Standing rules` scratch bullet (:32-43)
- `.ufo/evidence/round-55/c2/measure.py` (`MARKER` :46, `GRAMMAR` :47-50, `modes()` :118-160, docs arm :245-248, note/skill arms :257-260, total :271-273, verdict :279-282)
- `.ufo/evidence/round-55/freeze.json` (amendments 6 and 8), `.ufo/evidence/round-55/contract.json` (C2 before value, via `c31cdd9`)
- `tools/{repeat-control,context-capture,registry-check,env-diff,bash-witness-study,pin-disposition,evidence-disposition}.py`
- receipts: `T55W2RevDocsArms-receipts/{cells,diff,grammar,lazy,arms,classes,inventory}.txt`,
  `counter-denominator.txt`, `c2-head.out`, `c0-counter.out`, `c2-both-revisions.txt`

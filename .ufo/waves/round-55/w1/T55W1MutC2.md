# T55W1MutC2 — mutation test of the frozen C2 counter (round 55, wave 1)

Item: mutate `.ufo/evidence/round-55/c2/measure.py` in scratch copies with at least six
single-edit mutants, score each at the base revision and at a fixed tree, and report
KILLED / SURVIVED with the verdict lines, naming for each mutant the arm it is meant to
kill and whether it did.

Scored artefacts (machine-readable list: `T55W1MutC2.json`, beside this file):

| what | value |
|---|---|
| counter under test | `.ufo/evidence/round-55/c2/measure.py`, sha256 `0458f632087f665fbafc07efc6920d32febf7551d9fc5964d0c87fa0e139476b` = the bytes at rev `133b2ce6d4d86d783db38607343c3654350194b8` (round-55 freeze amendment 8) |
| base tree | `0a2010acd1e92e4e332774050825e21bcfc7e079` |
| fixed tree | `133b2ce` — the lane's own all-green pole (C0 `9cf0146` + freeze amendments), **not** a hand-built clone |
| violated tree A (`break2`) | scratch clone of the fixed pole + six deliberate arm violations, `4ce8ec98ee96` |
| violated tree B (`break3`) | scratch clone of the fixed pole + one deliberate `mkdir` under `/tmp`, `bfa16792aad2` |

The lane re-froze the counter twice while this item ran (`e2979f2` amendments 1-7;
`133b2ce` amendment 8, which added the ninth allocating mode `registry-check --rev` and
changed three denominators). A first pass on the pre-amendment bytes `d6ca1d85` was
abandoned mid-item and is **not** scored; its files sit as tracked siblings in
`T55W1MutC2-receipts/` and are explained by
`T55W1MutC2-receipts/superseded-d6ca1d8/README.txt`. Everything below is the re-based
pass on the bytes the deciding run will read.

## Method

1. Each mutant is exactly **one edited line** in a copy of the counter (one `@@` hunk,
   one `+`/`-` pair — `T55W1MutC2-receipts/mutants-133b2ce/mN.diff`), and the edit is the
   smallest change that makes the arm credit something it must reject.
2. The detector is the counter itself, run with the frozen CLI
   (`--lane <tree> --rev <rev> --work <empty dir> --explain`). Nothing else was used to
   score.
3. Every tree is its own baseline: pristine bytes are run first, and a mutant is
   **KILLED** only when its verdict line differs from the pristine arm of the same tree.
   A pristine failure is a baseline, not a kill.
4. Trees: base (two arms failing, grammar among them), the fixed pole (all arms green),
   and two purpose-built violated trees that each break one arm's input in a plausible
   way. The violated trees exist because leniency mutants are invisible on a conforming
   tree — see "Why three trees" below.

Baselines (verbatim):

```
base    C2_R55: rev=0a2010acd1e9 grammar=6/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=0/7 note=0/9 skill=0/1 total=20 C2_R55_PASS=false
fixed   C2_R55: rev=133b2ce6d4d8 grammar=9/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=0  C2_R55_PASS=true
break2  C2_R55: rev=4ce8ec98ee96 grammar=4/9 lazy=4/5 empty=12/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=7  C2_R55_PASS=false
break3  C2_R55: rev=bfa16792aad2 grammar=9/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=1 docs=7/7 note=9/9 skill=1/1 total=1  C2_R55_PASS=false
```

The six `break2` violations (`break-tree-violations.diff`), one per tool so each is
independently attributable:

| tool / mode | violation | arm it makes fail |
|---|---|---|
| `repeat-control --selftest` | the frozen line moved to **stdout** (stderr empty) | grammar / stream |
| `context-capture --selftest` | stderr marker line with the `(could-not-evaluate)` suffix dropped | grammar / shape |
| `pin-disposition --selftest` | conforming line **plus** a second line `pin-disposition: setup: RuntimeError: ...` | grammar / raw-type residue |
| `env-diff --selftest`, `--contract` | the class exits **1** instead of 2 | grammar / exit class |
| `bash-witness-study count` | inspects `TMPDIR` at parse time, exits 1 when unusable | lazy |
| `context-capture --check` | treats `TMPDIR=""` as a path, exits 1 | empty |

`break3` (`leak-tree-violation.diff`) adds one `os.makedirs("/tmp/t55w1mutc2-leak")` to
`repeat-control --selftest`'s usable path: `mkdir("/tmp/t55w1mutc2-leak", 0777) = 0`, one
census hit.

## Results

`base` / `fixed` / `break` are the mutant's `total` and PASS; **verdict** is against that
tree's own pristine arm.

| # | single edit (measure.py line) | arm it is meant to kill | base | fixed | violated tree | verdict |
|---|---|---|---|---|---|---|
| m1 | `:200` `rc == 2` → `rc in (1, 2)` | grammar / exit class | 20 ✗ = base | 0 ✓ = fixed | break2 5 ✗ vs 7 | **KILLED** (break2) |
| m2 | `:201` drop `and "RuntimeError" not in err + out` | grammar / raw-type residue | 20 = base | 0 = fixed | break2 6 vs 7 | **KILLED** (break2) |
| m3 | `:200` `err.splitlines()` → `(out + err).splitlines()` | grammar / stderr-only | 20 = base | 0 = fixed | break2 6 vs 7 | **KILLED** (break2) |
| m4 | `:248` `docs = sum(...)` → `docs = 7` | docs (seven cells) | 13 ≠ 20 | 0 = fixed | — | **KILLED** (base) |
| m5 | `:209` lazy `ok = rc == exp` → `ok = True` | lazy (five modes) | 20 = base | 0 = fixed | break2 6 vs 7 | **KILLED** (break2) |
| m6 | `:233` empty `ok = rc == exp` → always credit empty | empty (`TMPDIR=""`) | 20 = base | 0 = fixed | break2 6 vs 7 | **KILLED** (break2) |
| m7 | `:260` `skill = ...` → `skill = 1` | skill (SKILL.md) | 19 ≠ 20 | 0 = fixed | — | **KILLED** (base) |
| m8 | `:258` `m[0] in note_txt` → `m[0].split()[0] in note_txt` | note (all nine modes) | 19 ≠ 20 (note 1/9) | 0 = fixed | — | **KILLED** (base) |
| m9 | `:200` `GRAMMAR.match(l)` → `MARKER in l` | grammar / line shape | 20 = base | 0 = fixed | break2 6 vs 7 | **KILLED** (break2) |
| m10 | `:270` `tmp_total = sum(...)` → `tmp_total = 0` | usable / `/tmp` census | 20 = base | 0 = fixed | break3 **0** vs 1 | **KILLED by total, not by PASS** (break3) |

Mutation score: **10/10 killed across the tree set**; 3/10 killed by the base tree alone;
**0/10 killed by the fixed tree**. Surviving mutants: none.

Verbatim verdict lines for the deciding cells (`T55W1MutC2-receipts/verdict-lines.txt`
has all 31):

```
m1-break2   C2_R55: rev=4ce8ec98ee96 grammar=6/9 lazy=4/5 empty=12/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=5  C2_R55_PASS=false
m2-break2   C2_R55: rev=4ce8ec98ee96 grammar=5/9 lazy=4/5 empty=12/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=6  C2_R55_PASS=false
m3-break2   C2_R55: rev=4ce8ec98ee96 grammar=5/9 lazy=4/5 empty=12/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=6  C2_R55_PASS=false
m5-break2   C2_R55: rev=4ce8ec98ee96 grammar=4/9 lazy=5/5 empty=12/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=6  C2_R55_PASS=false
m6-break2   C2_R55: rev=4ce8ec98ee96 grammar=4/9 lazy=4/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=6  C2_R55_PASS=false
m9-break2   C2_R55: rev=4ce8ec98ee96 grammar=5/9 lazy=4/5 empty=12/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=6  C2_R55_PASS=false
m4-base2    C2_R55: rev=0a2010acd1e9 grammar=6/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=0/9 skill=0/1 total=13 C2_R55_PASS=false
m7-base2    C2_R55: rev=0a2010acd1e9 grammar=6/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=0/7 note=0/9 skill=1/1 total=19 C2_R55_PASS=false
m8-base2    C2_R55: rev=0a2010acd1e9 grammar=6/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=0/7 note=1/9 skill=0/1 total=19 C2_R55_PASS=false
P-break3    C2_R55: rev=bfa16792aad2 grammar=9/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=1 docs=7/7 note=9/9 skill=1/1 total=1  C2_R55_PASS=false
m10-break3  C2_R55: rev=bfa16792aad2 grammar=9/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=0  C2_R55_PASS=false
```

### Which arms each mutant was meant to kill, and whether it did

- **grammar, exit class (m1)** — meant to be caught by a tree whose allocating mode exits
  1 with a conforming line. *Base and fixed never produce that* (all 9 allocating modes
  exit 2 on both), so the mutant survives both. It did kill on `break2`: grammar 6/9 vs
  pristine 4/9, because `env-diff --selftest` and `--contract` then credited.
- **grammar, raw-type residue (m2)** — meant to be caught by a conforming line on stderr
  plus a line carrying the raw exception type. Base cannot do it: both failing modes print
  on **stdout**, so dropping the token leg changes nothing (grammar stays 6/9). Killed on
  `break2` by `pin-disposition`, which emits the conforming line *and*
  `setup: RuntimeError: ...` (grammar 5/9 vs 4/9).
- **grammar, stderr-only (m3)** — meant to be caught by the frozen line arriving on
  stdout. Survives base for the reason above (base's stdout lines also carry
  `RuntimeError`, so the token leg still rejects them). Killed on `break2` by
  `repeat-control` (grammar 6/9 vs 4/9).
- **grammar, line shape (m9)** — meant to be caught by a marker line that is not the
  frozen line. Survives base and fixed. Killed on `break2` by `context-capture`'s
  suffix-less line (grammar 5/9 vs 4/9).
- **docs (m4), skill (m7), note (m8)** — all three are visible on the base tree because
  the base documents carry no marker at all: docs 7/7 vs 0/7, skill 1/1 vs 0/1, note 1/9
  vs 0/9. All three killed at base; all three survive the fixed tree, as a leniency
  mutant must.
- **lazy (m5)** — meant to be caught by a non-allocating mode that reads `TMPDIR` at parse
  time. Base and fixed have all five lazy modes at rc 0, so the mutant is invisible there;
  killed on `break2` (lazy 5/5 vs 4/5).
- **empty (m6)** — meant to be caught by a mode that fails on `TMPDIR=""`. Invisible on
  base and fixed (13/13 both); killed on `break2` (empty 13/13 vs 12/13).
- **`/tmp` census (m10)** — meant to be caught by an allocating mode that mkdirs under
  `/tmp` on a usable root. Invisible on base and fixed (`tmp_mkdirs=0`); on `break3` the
  pristine arm reads `tmp_mkdirs=1 total=1` and the mutant reads `tmp_mkdirs=0 total=0`.
  Note the classification: the mutant is killed **by the total, not by the verdict
  boolean** — `return 0 if total == 0 and not bad else 1` keeps `C2_R55_PASS=false`
  because `bad` still holds `tmp_mkdirs:repeat-control --selftest`. A scorer that reads
  only the PASS token would call this mutant SURVIVED here. That redundancy is a feature
  for the gate and a weakness for mutation scoring; it is reported, not repaired.

## Why three trees (the finding that matters for the round)

The fixed tree kills **nothing**: on a conforming tree every leniency mutant produces the
same `total=0 C2_R55_PASS=true`. The counter's discriminating power therefore lives
entirely in its failing directions, and the base tree only reaches three of the ten arms
(docs, note, skill). The remaining seven mutants are killed only by a tree that violates
one arm's input on purpose.

Bound against the round's own controls (`controls.sh:127-141`, read-only):

- `CTL_BREAK_c2` rewrites the class line to `repeat-control: setup: RuntimeError: ...`.
  That single edit would trip the **shape** leg and the **raw-type** leg at once; it
  separates neither, and it exercises neither the exit-class leg (m1) nor the stderr-only
  leg (m3).
- It also cannot run at all on this round's tree: the anchor it rewrites,
  `emit_err(f"repeat-control: could-not-evaluate: {exc}")`, occurs **0 times** at the base
  rev, at `133b2ce`, and in the worktree — the landed tool emits
  `emit_err(f"repeat-control: could-not-evaluate: {message}")` (`tools/repeat-control.py:233`).
  The `assert src.count(old) == 1` aborts, the clone stays clean, `gitcommit` exits 1, and
  `|| exit 2` stops phase b before `CTL_BREAK_c2` is scored, so no
  `CONTROLS_B: n/n as pre-registered` line can be produced at this rev and
  `deciding-run.sh:56-57` will refuse with `DECIDING_REFUSED controls-a/b-verdict-missing`.
  See F5 and `receipts/ctl-break-anchor-demo.txt`.
- No pre-registered control violates the **lazy** arm (m5), the **empty** arm (m6), or the
  **`/tmp` census** (m10). Those three arms are live predicates — `break2`/`break3` prove
  each one fires when its input is violated — but nothing in the round's control set
  demonstrates that.

So the mutation result is not "the counter is wrong"; it is: every arm is sensitive when
its input is violated, and **five of the ten arms are exercised by no control the round
pre-registered**. If the L1 wants the deciding run to carry evidence for those arms, the
`break2`-style tree is the cheapest vehicle (one tree, six violations, four arms
distinguished in one run).

## Findings outside the mutation table

**F1 — the fixed pole still prints a setup error on stdout, and the counter cannot see
it.** At `133b2ce`, `TMPDIR=<nonexistent> python3 tools/repeat-control.py --selftest`
gives `rc=2`, stderr = the frozen line, and **stdout = `REPEAT_CONTROL: setup_error`**;
the counter scores that mode `ok` and prints `grammar=9/9 … total=0 C2_R55_PASS=true`
(`receipts/fixed-pole-repeat-control-streams.txt`). The round's integration item 1 says
"stdout carries no setup error", so the landed tool and the round's own wording disagree
about whether a tool's verdict token may share stdout with the class line. The counter
cannot arbitrate: its stdout leg is two literals (`RuntimeError`, `Traceback`), not "no
setup-error token". Whichever way the L1 rules, the record should say so.

**F2 — the frozen before-receipt's `total` does not follow from its own bytes.**
`.ufo/evidence/round-55/before/c2.stdout` as committed at `133b2ce` prints
`total=21` with `grammar=6/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=0/7
note=0/9 skill=0/1`. The counter's arithmetic on that vector is 3+7+9+1 = **20**, and an
independent re-run of the frozen bytes at the same base rev prints `total=20`. The two
files differ in **one line only** — all 42 `EXPLAIN` lines are byte-identical
(`receipts/before-receipt-vs-rerun.diff`). `PASS=false` either way, so no claim changes
hands, but the pre-registered "before" number is off by one and the same round has an
amendment 8 whose subject is exactly the total's arithmetic. Reported, not fixed.

**F3 — the usable arm can flake under host load.** In a ten-way concurrent batch on the
pre-amendment bytes (the usable-arm comparison is unchanged by amendment 8),
`registry-check --selftest` returned `rc=1` on the usable arm in 3 of 9 fixed-tree cells,
producing `usable=12/13 total=1 C2_R55_PASS=false`; re-running those three cells serially
gave `total=0 C2_R55_PASS=true`, and the mode standalone passed 5/5 with a good `TMPDIR`
(`receipts/registry-check-flake-probe.txt`, `receipts/m7-fixed.meta` vs
`m7-fixed2.meta`). Consequence for the round: a deciding run executed while other agents
are running counters can report a false FAIL, and any mutation score taken under
concurrency can report a false KILL. My scored cells were run through a bounded queue
(≤8 concurrent) and every cell was reproduced by re-run where the arm was in doubt.

**F4 — base conflates three grammar legs.** Both base failures are stdout-resident and
token-carrying, so the grammar arm fails them for stream, shape and token simultaneously;
m2, m3 and m9 all survive base unchanged (their verdict lines are byte-identical to
`P-base2`). Base therefore cannot distinguish the counter's legs, and it should not be
used as the sole mutation input.

**F5 — the pre-registered `CTL_BREAK_c2` cannot apply to this round's tree.** Its anchor
`emit_err(f"repeat-control: could-not-evaluate: {exc}")` has zero occurrences at the base
rev, at `133b2ce` and in the worktree; the landed tool emits
`emit_err(f"repeat-control: could-not-evaluate: {message}")`
(`tools/repeat-control.py:233`). Reproduced in a scratch clone at `133b2ce`: the
`assert src.count(old) == 1` aborts, nothing changes, `gitcommit` exits 1 (no
`--allow-empty`), and `|| exit 2` (controls.sh:136) ends phase b before the control is
scored. Consequence: `controls-b.stdout` cannot carry
`CONTROLS_B: n/n as pre-registered`, and `deciding-run.sh:56-57` refuses the deciding run
for a missing control verdict. Frozen file — reported, not repaired
(`receipts/ctl-break-anchor-demo.txt`).

**F6 — `docs` counts cells, it does not identify them.** `docs` sums rows that carry a
`scratch_root` cell and mention one of the seven tool paths, guarded only by
`len(cells) != 7` (`measure.py:245-249`). Seven cells belonging to the wrong modes (or to
the ninth allocating mode) still read 7/7 when the marker text is present. Recorded as the
arm's known limit; no tree was built for it and it is not counted in the score.

## Restoration / blast radius

- No lane production file was edited by this seat: no `tools/**`, `SKILL.md`,
  `SCORECARD.md`, `LOG.md`, `corpus/**`, and no frozen byte. Every run read the lane only
  through `git clone --shared` + checkout of a commit.
- Writes: this file, `T55W1MutC2.json`, and `T55W1MutC2-receipts/**`. Nothing else.
  Note for the integrator: an `git add -A` sweep captured this seat's in-progress
  receipts into commit `133b2ce`, so the first pass's files are **tracked** siblings in
  that directory (`P-base.*`, `counter-bytes.txt`, `fixed-tree-line-*.txt`, `mutants/`).
  They are superseded, deliberately left unmodified, and explained by
  `receipts/superseded-d6ca1d8/README.txt`; the scored set is
  `mutants-133b2ce/`, `verdicts/`, `verdict-lines.txt`, `counter-under-test.sha256`.
- Mutating git commands ran only inside scratch clones, each asserted with
  `git -C <dir> rev-parse --show-toplevel` before any commit: `lane-base`, `lane-fixed`,
  `lane-fixed2`, `lane-break`, `lane-break2`, `lane-break3`, `ctlbreak-demo` — all under
  `/fast/scratch/hyaku/tameshi-r55/T55W1MutC2`, all removed after the receipts were
  copied. The lane's own worktree was never committed to, checked out, or otherwise
  touched.
- Tooling: nothing installed or upgraded (no `pacman`, no `uv tool`, no `npx`); the runs
  used the host's `python3`, `git` and `strace`.
- Census, run once during this item and untouched since:
  `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` printed
  `tameshi ok /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md` and exited
  0 (its only other lines were two pre-existing `W04` duplicate-URL warnings for S268 and
  S274).

## Precondition for the deciding run (not a defect of this seat's item)

The deciding script copies the counters **from `$REV`** and refuses when the frozen list
differs from `$FREEZE` (`FROZEN_UNCHANGED=0`, `deciding-run.sh:60-67`). The scored bytes
here are the ones at `133b2ce`; the lane worktree was still moving while this item ran
(contract amendments 8 and rising, `tools/**` edited by the integrator). If the counter
changes again, the freeze manifest must be re-derived at the new pole and this mutation
table re-scored on the new bytes — the predicates are stable but three denominators and
the allocating-mode count have already changed once inside this round.

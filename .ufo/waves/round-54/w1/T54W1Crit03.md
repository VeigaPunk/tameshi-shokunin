# T54W1Crit03 — C2 registry `scratch_root` cell vs behaviour

- Seat: `T54W1Crit03` (critic, leaf). Round 54 / hyaku run 11 / L1 `TameshiR54a2`.
- Axes: discernment? calibration.
- Milestone: falsify the claims.
- Attack: C2 docs arm — does each `scratch_root` cell describe what its tool now does?
- Cand: `59c38109bf119d0e9d4f878644a82babc937bc1e` (C0). Scratch: `/fast/scratch/hyaku/tameshi-r54/T54W1Crit03/` (removed at end).
- Write scope: only this file + `T54W1Crit03-receipts/`. No lane production edits. No tooling install.
- Verdict up front: **live cells match the three measured arms**; **the docs arm does not check that** — a keyword-only predicate accepts cells that assert the opposite. Contract `cannot_see` covers behaviour *beyond* the three arms, **not** a lie *about* the three arms.

## Axes named

| Axis | How this attack loads it |
|---|---|
| discernment | Does C2's docs check actually discern cell-vs-behaviour fidelity, or only keyword presence? |
| calibration | Is "rows carry the scratch_root cell" calibrated to description quality, or saturated by substring hits? |

## Counterexample (docs arm)

`c2/measure.py` docs loop (receipt `04-docs-predicate-source.txt`):

```
cell = (by_name.get(row_name) or {}).get('scratch_root')
if isinstance(cell, str) and all(k in cell for k in ('TMPDIR', 'empty', 'could-not-evaluate')):
    docs += 1
```

Forged cell (inverted behaviour; contains all three substrings via "TMPDIR", "empty stderr", "could-not-evaluate"):

```
TMPDIR set but unusable => exit 0 with empty stderr; never prints could-not-evaluate; falls back to /tmp
```

Command + output (`07-forged-docs-pass-demo.txt`):

```
forged_cell= TMPDIR set but unusable => exit 0 with empty stderr; never prints could-not-evaluate; falls back to /tmp
docs_count= 7 of 7
would_docs_arm_pass= True
NOTE: behavioural arms are separate; this shows docs arm alone accepts inverted description
cannot_see= whether a tool's self-test exercises the branch that allocates scratch on its real path, and whether a registry cell describes the tool as it now behaves beyond the three named arms
covers_lie_about_three_arms= False # text says beyond the three named arms, not about them
covers_lie_beyond_three_arms= True
```

Two more forgeries also `docs_pass=True` (`04-docs-keyword-attack.txt`): `wrong-exit-1`, `opposite-arms`. Control lacking `empty`/`could-not-evaluate` fails (`missing-keyword-control`), proving the gate is substring presence only.

### Does `cannot_see` cover it?

**No for this counterexample.** Contract C2 `cannot_see` (freeze `441c26be` / `contract.json`):

> whether a tool's self-test exercises the branch that allocates scratch on its real path, and whether a registry cell describes the tool as it now behaves **beyond the three named arms**

The forgery lies *about* the three named arms themselves. That gap is outside `cannot_see` as written, and outside the docs predicate as implemented. Behavioural arms would still catch a tool that actually inverted; the docs arm would not catch a cell that inverted.

## Live cells vs behaviour (not inverted)

### Seven identical cells at C0

Command + output (`04-docs-keyword-attack.txt`):

```
=== live cells at C0 ===
registry-check-selftest: sha16=08b1cc092867b917 len=266
env-diff-selftest: sha16=08b1cc092867b917 len=266
bash-witness-selftest: sha16=08b1cc092867b917 len=266
evidence-disposition-selftest: sha16=08b1cc092867b917 len=266
pin-disposition-selftest: sha16=08b1cc092867b917 len=266
context-capture-selftest: sha16=08b1cc092867b917 len=266
repeat-control-selftest: sha16=08b1cc092867b917 len=266
TEXT= 'TMPDIR set but unusable => exit 2, could-not-evaluate (the value is named, no traceback); TMPDIR empty => unset, the platform default applies; a usable TMPDIR holds every mkdtemp and nothing is created under /tmp (round 54, corpus/knowledge/scratch-root-contract.md)'
identical_across_seven= True
live_docs_count= 7
```

### Three arms by hand — `tools/env-diff.py --selftest`

Clone: `/fast/scratch/hyaku/tameshi-r54/T54W1Crit03/clone-hBto5b` @ C0 (`00-setup.txt`). Receipt: `02-env-diff-three-arms.txt` + `02-env-diff-strace.log`.

```
=== ARM1 unusable ===
rc=2
ENVDIFF_SETUP: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/fast/scratch/hyaku/tameshi-r54/T54W1Crit03/unusable-tmpdir-r54-never-created' (could-not-evaluate)
has_could_not_evaluate=1
names_value=1
has_traceback=0
=== ARM2 empty TMPDIR ===
rc=0
ENVDIFF_SELFTEST: 9/9 pass
=== ARM3 usable + strace mkdir ===
rc=0
ENVDIFF_SELFTEST: 9/9 pass
tmp_mkdirs=0
```

Word-by-word vs cell segments (`06-word-by-word.txt`):

| Cell segment | Observed |
|---|---|
| `TMPDIR set but unusable => exit 2, could-not-evaluate (the value is named, no traceback)` | rc=2; line names unusable path; contains `could-not-evaluate`; no traceback |
| `TMPDIR empty => unset, the platform default applies` | `TMPDIR=""` → rc=0 (platform default path succeeds) |
| `a usable TMPDIR holds every mkdtemp and nothing is created under /tmp` | rc=0; strace `tmp_mkdirs=0`; mkdtemps under usable root |

**Live env-diff cell describes the three arms correctly.**

### Sweep — all seven tools, three arms

Command + output (`03-seven-tools-three-arms.txt`):

```
name|arg|unusable_rc|unusable_cne|unusable_names|unusable_tb|empty_rc|usable_rc
registry-check|--selftest|2|1|1|0|0|0
env-diff|--selftest|2|1|1|0|0|0
bash-witness-study|selftest|2|1|1|0|0|0
evidence-disposition|--selftest|2|1|1|0|0|0
pin-disposition|--selftest|2|1|1|0|0|0
context-capture|--selftest|2|1|1|0|0|0
repeat-control|--selftest|2|1|1|0|0|0
```

Unusable lines (all name the TMPDIR value + `could-not-evaluate`, no traceback) — receipts `03-unusable-*.out`:

```
registry-check: could-not-evaluate: ... TMPDIR is not a usable directory: '.../unusable-tmpdir-r54-never-created' (could-not-evaluate)
ENVDIFF_SETUP: could-not-evaluate: ...
WITNESS_STUDY: could-not-evaluate: ...
evidence-disposition.py: could-not-evaluate: ...
pin-disposition.py: could-not-evaluate: ...
SELFTEST: FAIL (setup error: RuntimeError: ... (could-not-evaluate))
repeat-control: setup: RuntimeError: ... (could-not-evaluate)
REPEAT_CONTROL: setup_error
```

So for the three named arms, each identical cell is **behaviourally accurate** at C0. Wording differences (ScratchRootUnusable catch vs bare `RuntimeError` / `SELFTEST: FAIL` / `setup_error`) stay inside the cell's claim atoms.

### Impl split (same three-arm outcomes)

`01-strict-scratch-impl.txt`: 4 tools raise `ScratchRootUnusable` (C0); 3 raise bare `RuntimeError` (`registry-check`, `context-capture`, `repeat-control`). Docstring on the 4 mentions empty⇒unset; the 3 omit that sentence — behaviour still uses `if t:` so empty is unset. Cell text is still true for all seven on the measured arms.

## Impacted axes

- **discernment**: docs arm cannot discern a faithful cell from an inverted one; only behavioural arms carry the description claim.
- **calibration**: "carry the scratch_root cell" is calibrated to three substrings, not to "describes what the tool now does." Live C0 cells happen to be right; the counter would still PASS docs if they were rewritten to lie.

This does **not** by itself force `C2_R54_PASS=false` at C0 (behavioural 7/7 holds; live docs keywords hold). It falsifies the stronger reading that the docs arm *validates* cell↔behaviour fidelity.

## Smallest safe correction

1. Tighten the docs predicate so a cell must carry claim atoms the behavioural arms already measure, e.g. require all of `exit 2`, `could-not-evaluate`, and an empty-arm token that cannot be satisfied by `empty stderr` (e.g. `empty =>` or `TMPDIR empty`), **or** pin the known-good cell digest `sha256→08b1cc092867b917…` / full 266-byte string; and
2. Either widen `cannot_see` to admit "docs arm is keyword-only / does not read cell semantics," or drop the implication that carrying the cell means describing the tool.

Do not treat the keyword gap as already covered by today's `cannot_see` (it is scoped *beyond* the three arms).

## Receipts index

Under `.ufo/waves/round-54/w1/T54W1Crit03-receipts/`:

- `00-setup.txt` — shared clone @ C0
- `01-strict-scratch-impl.txt` — seven `strict_scratch_root` bodies
- `02-env-diff-three-arms.txt`, `02-env-diff-strace.log` — hand three-arm run
- `03-seven-tools-three-arms.txt`, `03-unusable-*.out` — 7×3 sweep
- `04-docs-keyword-attack.txt`, `04-docs-predicate-source.txt` — keyword gate + forgeries
- `05-runtimeerror-handlers.txt`, `08-cne-catch-sites.txt`, `09-context-capture-setup-catch.txt`, `10-repeat-control-setup-catch.txt` — catch paths
- `06-word-by-word.txt`, `07-forged-docs-pass-demo.txt` — cell vs arms + docs forgery demo

## Tooling

None installed or upgraded (pacman paused; nothing needed).

# T55W2Read02 — cold read of `## Standing rules` at C0 (grammar vs code)

Seat: reader, wave 2, round 55. Candidate revision `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb` (C0).
Scope of the read: the section's scratch bullet against the three round-55 tools' code, the
seven scratch-root tools, the frozen C2 counter, and `corpus/knowledge/scratch-root-contract.md`.

**Verdict.** The section's substantive claim holds at C0: the nine documented allocating modes
each emit exactly one stderr line, exit 2, no `RuntimeError`/`Traceback`, on a set-but-unusable
`TMPDIR`; the five non-allocating modes stay lazy (rc 0, empty stderr); the nine named modes are
exactly the modes that allocate; the quoted grammar matches the frozen counter's `GRAMMAR` for
every ordinary value. Three defects are recorded below (quote-style totality, registry-cell
prefix drift, and an unreachable PASS in the cited counter at C0). None of them falsifies
"one line, exit 2, nine modes"; all three are receipt/edge defects a parser can hit.

## Section identity

Cut from the blob at C0, never the working tree:

```
$ git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show \
    9cf0146b94ddba12d454ebf7288ce6e5c5d535bb:SKILL.md | sed -n '17,44p'
## Standing rules
...
  cells).
```

SHA computed with the frozen round-18 sectionizer (its `sectionize`, not an invented scheme):

```
$ python3 -c 'import importlib.util,subprocess; ... m.sectionize(raw) ...'
17 44 acfb671afd767c32476f57b040399972f6c870cd7dde3d821c344cae1a9ad767
```

Working tree lines 17–44 are identical to C0 at the time of this read
(`diff` of the two `sed` outputs → `WORKTREE_SAME_17_44`), but the numbers above come from the
C0 blob only.

## 1. Grammar vs the frozen counter, byte for byte

Counter bytes at C0 = `36ca47d3...` (verified: `git show C0:.ufo/evidence/round-55/c2/measure.py |
sha256sum`), identical to the freeze pointer `e2979f2`'s bytes.

Counter grammar (`c2/measure.py:47-50` at C0):

```
^[A-Za-z][A-Za-z0-9_.-]*(?:\.py)?: could-not-evaluate: cannot create clone
scratch under the scratch root: TMPDIR is not a usable directory: '.+'
\(could-not-evaluate\)$
```

The section's line, with `<tool>` and `<value>` substituted, is accepted by that regex:

```
template-vs-GRAMMAR: True
```

and every line measured below is accepted too (8/8 from the first run + `registry-check --rev`):
`bash-witness-selftest.err True`, `context-capture-selftest.err True`, `env-diff-contract.err True`,
`env-diff-selftest.err True`, `evidence-disposition-selftest.err True`, `pin-disposition-selftest.err True`,
`registry-check-selftest.err True`, `repeat-control-selftest.err True` (the ninth,
`registry-check-rev.err`, was written by the second command and matches by inspection of the same
literal text: `registry-check: could-not-evaluate: cannot create clone scratch under the scratch
root: TMPDIR is not a usable directory: '<value>' (could-not-evaluate)`).

## 2. The nine allocating modes, measured directly

Fixture: `git clone --shared` of the lane at C0 in `$HYAKU_SCRATCH/tameshi-r55/T55W2Read02/clone`,
asserted `git rev-parse --show-toplevel` = that clone; every run with
`TMPDIR=<scratch>/no-such-tmpdir` (a nonexistent path), cwd = the clone, `timeout 900`.

```
$ bash run-modes.sh <clone> <out> <no-such-tmpdir>
env-diff-selftest            rc=2  ENVDIFF_SETUP: could-not-evaluate: cannot create clone scratch ... '<no-such-tmpdir>' (could-not-evaluate)
env-diff-contract            rc=2  ENVDIFF_SETUP: could-not-evaluate: cannot create clone scratch ... '<no-such-tmpdir>' (could-not-evaluate)
repeat-control-selftest      rc=2  repeat-control: could-not-evaluate: cannot create clone scratch ... '<no-such-tmpdir>' (could-not-evaluate)
registry-check-selftest      rc=2  registry-check: could-not-evaluate: cannot create clone scratch ... '<no-such-tmpdir>' (could-not-evaluate)
bash-witness-selftest        rc=2  WITNESS_STUDY: could-not-evaluate: cannot create clone scratch ... '<no-such-tmpdir>' (could-not-evaluate)
pin-disposition-selftest     rc=2  pin-disposition.py: could-not-evaluate: cannot create clone scratch ... '<no-such-tmpdir>' (could-not-evaluate)
evidence-disposition-selftest rc=2 evidence-disposition.py: could-not-evaluate: cannot create clone scratch ... '<no-such-tmpdir>' (could-not-evaluate)
context-capture-selftest     rc=2  context-capture.py: could-not-evaluate: cannot create clone scratch ... '<no-such-tmpdir>' (could-not-evaluate)
registry-check-rev           rc=2  registry-check: could-not-evaluate: cannot create clone scratch ... '<no-such-tmpdir>' (could-not-evaluate)
```

Counts: 9/9 exit 2, 9/9 one stderr line, 9/9 GRAMMAR-matching, 0 `RuntimeError`, 0 `Traceback`
on either stream (line/token census over every `.out`/`.err` under the run directory).

The C0 counter itself, run from its C0 bytes against a C0 clone (373.9 s), reproduces the same
nine on its grammar arm: `EXPLAIN grammar ... rc=2 ok` ×9.

## 3. The five lazy modes

```
repeat-control-snapshot      rc=0  stderr empty
bash-witness-count           rc=0  stderr empty
pin-disposition-read         rc=0  stderr empty
evidence-disposition-json    rc=0  stderr empty
context-capture-check        rc=0  stderr empty
```

A lazy mode's rc 0 is not a scratch-root pass (the note says so); what it shows here is that the
unusable `TMPDIR` is never touched on these five paths, i.e. allocation is lazy, matching the
section's "the five non-allocating modes stay lazy".

## 4. The mode set is exactly the allocating set (code census)

Every `strict_scratch_root()` call site in the seven tools, and the documented mode that reaches it:

| tool | call site | documented mode(s) that reach it |
|---|---|---|
| repeat-control.py | 629 | `--selftest` |
| context-capture.py | 1643 | `--selftest` |
| registry-check.py | 784 (`clone_lane_at_rev`), 935 | `--rev`, `--selftest` |
| bash-witness-study.py | 1260 | `selftest` |
| pin-disposition.py | 725 | `--selftest` |
| evidence-disposition.py | 2370 | `--selftest` |
| env-diff.py | 80 (`execute`, reached by `probe`) | `--selftest`, `--contract` |

So the section's "the seven self-tests plus `env-diff --contract` and `registry-check --rev`" is
the complete allocating set over the documented modes: 7 self-tests + 2 = 9. No other documented
mode allocates (`repeat-control --runs/--snapshot`, `bash-witness-study declare/run/rerun/count/check`,
`registry-check` default, `pin-disposition` default, `evidence-disposition` default,
`context-capture --check` have no `mkdtemp`/`TemporaryDirectory` on their path;
`bash-witness-study.py` mkdtemps only in `cmd_selftest`).

## Findings

### F1 — the quoted line is not total: `%r` switches to double quotes for a value containing `'`

Quote (line 24 at C0): ``root: TMPDIR is not a usable directory: '<value>' (could-not-evaluate)` ``

Every tool formats the value with `%r` (`repeat-control.py:164`, `context-capture.py:312`,
`registry-check.py:769`, `env-diff.py:46`, `pin-disposition.py:175`, `evidence-disposition.py:205`,
`bash-witness-study.py:219`). `repr()` of a string that contains `'` and no `"` uses double quotes.
Measured with `TMPDIR=<scratch>/it's-not-a-dir`:

```
$ TMPDIR="$S/it's-not-a-dir" python3 tools/repeat-control.py --selftest      -> rc=2
repeat-control: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: "/fast/scratch/hyaku/tameshi-r55/T55W2Read02/it's-not-a-dir" (could-not-evaluate)
$ TMPDIR="$S/it's-not-a-dir" python3 tools/context-capture.py --selftest    -> rc=2
context-capture.py: could-not-evaluate: ... usable directory: "/fast/.../it's-not-a-dir" (could-not-evaluate)
$ TMPDIR="$S/it's-not-a-dir" python3 tools/registry-check.py --rev HEAD     -> rc=2
registry-check: could-not-evaluate: ... usable directory: "/fast/.../it's-not-a-dir" (could-not-evaluate)
GRAMMAR_match = False, False, False
```

The class is right (one stderr line, exit 2, no traceback, value named); the byte-shape is not
(the frozen regex requires `'.+'`). The section's template says single quotes unconditionally, so
a caller keyed on the frozen grammar misses exactly this class of value. The C2 counter cannot see
it: its unusable arm uses one fixed path with no quote. Receipt:
`T55W2Read02-receipts/apostrophe-tmpdir.txt`.

### F2 — four of the seven cited registry cells quote a prefix the tool never emits

Quote (line 26 at C0): ``corpus/knowledge/scratch-root-contract.md; the seven registry `scratch_root` ``

Cell text vs measured first line:

| cell | cell quotes | tool emits | match |
|---|---|---|---|
| repeat-control | `repeat-control.py: could-not-evaluate: ...` | `repeat-control: ...` | no |
| registry-check | `registry-check.py: could-not-evaluate: ...` | `registry-check: ...` | no |
| env-diff | `env-diff.py: could-not-evaluate: ...` | `ENVDIFF_SETUP: ...` | no |
| bash-witness-study | `bash-witness-study.py: could-not-evaluate: ...` | `WITNESS_STUDY: ...` | no |
| pin-disposition | `pin-disposition.py: ...` | `pin-disposition.py: ...` | yes |
| evidence-disposition | `evidence-disposition.py: ...` | `evidence-disposition.py: ...` | yes |
| context-capture | `context-capture.py: ...` | `context-capture.py: ...` | yes |

All seven still match the frozen regex, because its prefix class is `[A-Za-z][A-Za-z0-9_.-]*` (it
accepts `ENVDIFF_SETUP` and `WITNESS_STUDY`), and the counter's `docs` arm matches only `MARKER`
(the suffix, `c2/measure.py:40-41`), not the prefix — so the counter's 7/7 docs arm is blind to
this. Consequence for the section: its `<tool>` placeholder silently covers two allocating modes
whose prefix does not name the tool, and the receipt it cites is not the bytes in the tools. A
caller attributing the line by prefix mis-attributes `env-diff` and `bash-witness-study` lines.
Receipt: `T55W2Read02-receipts/nine-allocating-and-five-lazy.txt`; cell text from
`tools/registry.json` (`scratch_root` cells at lines 44, 87, 135, 333, 424, 620, 895 at C0).

### F3 — the cited C2 counter cannot report PASS at C0

Quote (lines 21–22 at C0): "Measured on every documented allocating mode — the seven self-tests
plus `env-diff --contract` and `registry-check --rev` — as one stderr line,"

The nine-mode content is true (section 2 above). The receipt is not: at C0 the counter's total is

```
total = (len(allocating)-grammar_ok) + (len(lazy)-lazy_ok)
      + (len(table)-empty_ok) + (len(table)-usable_ok)
      + tmp_total + (7-docs) + (8-note) + (1-skill)
```

with `len(table)=14`, `cheap=13`, `note=9` (the note names all nine modes),
`C2_R55_PASS=true` only when `total == 0 and not bad` (c2/measure.py:276-282 at C0). In the
all-green state the two `len(table)` terms contribute 2 and `(8-note)` contributes -1, so
`total = 1` and the verdict is `C2_R55_PASS=false`, exit 1 — at every possible state. Computed from
the C0 bytes' own mode table:

```
allocating 9 lazy 5 cheap 13 table 14
C0 all-green total = 1
```

Measured, not just computed — the C0 counter bytes (`36ca47d3...`) from the C0 clone, run over an
empty work dir against the lane at C0 with `--explain`:

```
$ python3 .ufo/evidence/round-55/c2/measure.py --lane <lane> --rev 9cf0146b94dd... \
      --work <empty> --explain
EXPLAIN grammar  repeat-control --selftest        rc=2  ok
... (9 grammar, 5 lazy, 13 empty, 13 usable, docs 7/7, note 9/9, skill 1/1: every arm ok)
C2_R55: rev=9cf0146b94dd grammar=9/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 \
        docs=7/7 note=9/9 skill=1/1 total=1 C2_R55_PASS=false
C2_C0_RC=1
```

Every arm is green and the verdict is still false with exit 1. Post-C0 commit `133b2ce`
("freeze amendment 8") changes exactly these three terms and records the same symptom ("at the
all-green state the verdict read total=1 with an empty bad map"). That commit is not the C0
receipt the section cites (`36ca47d3`), so at C0 the cited receipt cannot affirm the claim it is
cited for, even though direct measurement of the nine modes confirms it.

## What I did not claim

- My own per-mode runs covered the unusable arm and the five lazy modes; the empty/usable arms and
  the `strace` /tmp census are the C0 counter's own arms and are reported only as its run
  (13/13, 13/13, `tmp_mkdirs=0`), not as independent measurement here. I did not run `no-harm.sh`.
- I did not treat a lazy mode's rc 0 as evidence of a usable scratch root (the note forbids it).
- I did not read the working tree as authority for the section; its bytes were cross-checked only
  as a hygiene fact after the C0 cut.
- I did not edit any lane file: all writes went to the clone under scratch and to
  `.ufo/waves/round-55/w2/T55W2Read02*`.

## Artifacts opened

- `SKILL.md` at `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb` (`## Standing rules`, lines 17–44) — section under read.
- `tools/repeat-control.py` — `ScratchRootUnusable` 148, `strict_scratch_root` 156, `could_not_evaluate` 227-235, `selftest` 624-629, `main` 922-945, exit map 122-128.
- `tools/context-capture.py` — `ScratchRootUnusable` 300, `strict_scratch_root` 304-312, `SelftestHarness` 1642-1643, `run_selftest` 2211-2225, `main` 2299-2335.
- `tools/registry-check.py` — `ScratchRootUnusable` 757, `strict_scratch_root` 761-770, `clone_lane_at_rev` 774-790, `--selftest` handler 1845-1856, `--rev` handler 1930-1951.
- `tools/env-diff.py` — `strict_scratch_root` 36-46, `execute` 79-81, `probe` 129-133, `surface_result` 149-159, `selftest` 162-190, CLI handlers 225-275.
- `tools/pin-disposition.py` — `ScratchRootUnusable`/`strict_scratch_root` 162-175, selftest mkdtemp 725, handler 1400.
- `tools/evidence-disposition.py` — `ScratchRootUnusable`/`strict_scratch_root` 192-205, selftest mkdtemp 2370, handler 3232.
- `tools/bash-witness-study.py` — `ScratchRootUnusable` 206, `strict_scratch_root` 209-219, selftest mkdtemps 1259-1265, handler 1789, subcommands 1771-1785.
- `corpus/knowledge/scratch-root-contract.md` — whole file (three arms, "One line, every mode (round 55)", five lazy modes).
- `tools/registry.json` — the seven `scratch_root` cells and their `argv` rows.
- `.ufo/evidence/round-55/c2/measure.py` at C0 (`36ca47d3...`) — `MARKER` 40-41, `GRAMMAR` 47-50, `SEVEN` 52-53, `modes()` 78-130, arms and verdict 200-282.
- `.ufo/evidence/round-55/c2/measure.py` at HEAD `133b2ce` (`0458f63...`) — read only to attribute the post-C0 amendment; not used as evidence.
- `.ufo/evidence/round-18/measure.py` — `sectionize` 209-253 (section sha).
- `.ufo/evidence/round-55/freeze.json` — at `133b2ce` (amendment 8, file shas) and the pre-amendment file list.
- `git show --stat 133b2ce` — to establish that the post-C0 commit touched only the three `.ufo` files.

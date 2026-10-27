# Read11 cold read: SKILL.md `### Gate/probe registry`

- Lane repo: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
- Content commit (C*): `a41195dfc13a73958e4c5228ec196b28d03ded03`
- SKILL.md at C*: `sha256 c329d3c150200ff32c47cb218800fb87c014345a7f342e1b11c70f5cacfc83ee`, 2178 lines
- Section: lines 1506-1522, `sha256 c1aabe900e6fbc46288d2ff241348a5fba8481388979ed62d7720dff0b244c65`, 2198 bytes, no trailing newline
- Verdict: **2 findings** (both stale scratch locations in the write-scope column). Every other cell and the two prose claims re-verified at C*.

## Setup and section resolution

Read via git objects only; the lane working tree was never read as content.

```
$ git -C .../tameshi-shokunin show a41195dfc13a73958e4c5228ec196b28d03ded03:SKILL.md > SKILL.md
$ wc -l SKILL.md            -> 2178 SKILL.md
$ sha256sum SKILL.md        -> c329d3c150200ff32c47cb218800fb87c014345a7f342e1b11c70f5cacfc83ee
$ grep -n '^### Gate/probe registry' SKILL.md   -> 1506:### Gate/probe registry
```

Split by the frozen monitor rule (heading `^#{1,3}(\s|$)` outside ``` fences; heading line through the line before the next heading; trailing whitespace-only lines stripped; joined with `\n`, no trailing newline). The next heading after the section is `## Pin disposition and provenance correction — round 13` at line 1524, so the section body ends at line 1522 (line 1523 is the single blank separator). Two independent computations were run:

1. line list (`str.splitlines()` and `str.split("\n")`, both gave the identical result), sliced, re-joined, hashed;
2. raw byte slice `raw[start:end-1]` from byte offsets of line 1505 and line 1522 - `sha256` matched the string build and the decoded slice compared equal to the joined section text.

Both gave `c1aabe900e6fbc46288d2ff241348a5fba8481388979ed62d7720dff0b244c65`. So the confirmed range is 1506-1522 and the hash is not an artefact of one split convention.

Cross-check on the section identity itself: the tool sha256 printed by the section's own entry command in the same revision reports `repeat-control.py r12 ... tool-sha256=6dd44263c2b3f9ebe847cd0263a9bed0b096036ebea88288a196b4410416477e`.

All command runs used a full `git archive` extraction of C* into scratch (`207M`), with `TMPDIR` pointed at scratch; nothing in the lane was executed from a writable copy and no lane path was modified.

## Checks run

Execution tree: `git -C <lane> archive a41195dfc13a73958e4c5228ec196b28d03ded03 | tar -x -C <scratch>/repo`.

### Entry and self-test commands (both rows)

```
$ cd <scratch>/repo && python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate
SNAPSHOT_INPUTS 9 verified
SNAPSHOT_EXPECTED id=controls_match exit=0
SNAPSHOT_OBSERVED id=controls_match exit=0
REPEAT_CONTROL: controls_match
exit=0

$ python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate/mismatch
SNAPSHOT_EXPECTED id=controls_mismatch exit=1
SNAPSHOT_OBSERVED id=controls_mismatch exit=1
exit=1

$ python3 tools/repeat-control.py --selftest
SELFTEST_CASE snapshot-committed-stable PASS (expected=controls_match/0 observed=controls_match/0)
SELFTEST_CASE snapshot-committed-mismatch PASS (expected=controls_mismatch/1 observed=controls_mismatch/1)
SELFTEST: PASS (29 cases)
exit=0
```

```
$ python3 tools/bash-witness-study.py count
declared	0def0d3b...	.../declared.tsv
control	exit=0	denominator=16	exercised=14	skipped=2	skip=verbs-sandboxed,verbs-break-injection
row	B1	KILLED	...	class=killed-on-witness
row	B5	SURVIVED	exit=0	declared=NONE	failed=-	...	class=survived
row	B10	SURVIVED	exit=0	declared=NONE	failed=-	...	class=survived
counts	killed_on_witness=8	accidental=0	survived=2	inconclusive=0	total=10	witness_classified=10
declared_none	B5,B10
unresolved	none
exit=0

$ python3 tools/bash-witness-study.py selftest
WITNESS_SELFTEST: 51/51 pass
VERDICT: PASS
exit=0
```

### The stale-pin sentence (dated, so a hold, but re-measured)

```
$ git show C*:tools/mutate-and-run.sh | sha256sum
977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda  -

$ python3 tools/bash-witness-study.py check
WITNESS_CHECK: DRIFT tools/mutate-and-run.sh sha256=977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda committed=75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5
WITNESS_CHECK: FAIL (1 problems; 96 files covered)
exit=1

$ python3 tools/bash-witness-study.py run    -> WITNESS_STUDY: CANNOT-EVALUATE (runner-drift ...) exit=2
$ python3 tools/bash-witness-study.py rerun  -> WITNESS_STUDY: CANNOT-EVALUATE (runner-drift ...) exit=2
```

`count` exited 0 with the same stale pin in place, so "count never reads the runner" is observed, not inferred. `count`'s exit-1 arm is `return EXIT_FAIL if tally["unresolved"] else EXIT_OK` (`tools/bash-witness-study.py:1125`).

### Pinned-value and pointer existence (via `git ls-tree` at C*)

- `.ufo/evidence/round-12/ControlGate/expected.json` - present
- `.ufo/evidence/round-12/ControlGate/mismatch/expected.json` - present
- `.ufo/evidence/round-12/BashWitness/declaration.json`, `declared.tsv`, `manifest.json` - all present
- `.ufo/waves/round-27/w1/Read25.md` - present (read in full; it is the round-27 cold read of this same section)
- seat `ReRead08` - traces present at `.ufo/evidence/round-27/coldread/traces/ReRead08-1.json` .. `-18.json`

`manifest.json` self-pinning: the manifest object has exactly the keys `created_at` and `files` (95 entries); `"manifest.json"` is not a member of its own `files` map, so "`manifest.json` itself is not pinned" holds. (The one `manifest.json` string inside the file is the nested `rerun-20261020T035435Z/manifest.json` entry.)

### Calibration-correction claims

```
$ git show C*:SHONEN.md | sed -n '1,14p'
- [~] Instructions executable by an agent without oral context
  [lane assertion, input-keyed monitor only; no independent promotion verifier](.ufo/evidence/round-21/coldread/ledger.json)

$ git show 9df9212:SHONEN.md | sed -n '1,12p'     # round-12 landing commit
- [~] Instructions executable by an agent without oral context
  [lane assertion, scope-bounded: fleet round-1 cold-read of blob 4eb4cf3:SKILL.md - Appendix A + B sweep recipe only, ...; no independent promotion verifier](reports/round-1-kaika-coldread.md)
```

```
$ git show C*:corpus/lessons/round-1-verifier-spotcheck.md | grep -n 'score'
17:... ADMITTED after post-review fixes `01b358c`: ... with the score re-pinned at 6 - the box-3 increment is not credited (cold-read covered Appendix A+B only, probes reconstructed); ...
```

The referent of "the historical promotion paragraph above" resolves to `## Promotion-evidence calibration — fleet round-1`, whose line 1479 reads "Box 3 was `[ ]` at this write". Box 3 at round 12 (`9df9212`) is `[~]` with an explicit "scope-bounded" qualifier, so "carried a scope-bounded `[~]` at round 12, not `[ ]`" holds and the lesson does exclude the increment from the score.

## Findings

### F1 - repeated-controls write scope names `/tmp`, the tool writes under `$TMPDIR`

Quote (byte-exact, appears in the section):

```
isolated `/tmp/tameshi-r12-*` selftest
```

Why it fails at C*: `tools/repeat-control.py:597` at C* is

```
scratch = tempfile.mkdtemp(prefix="tameshi-r12-repeat-control-selftest.", dir=tempfile.gettempdir())
```

`tempfile.gettempdir()` is `$TMPDIR` whenever that directory is writable, and `/tmp` only as the fallback. Measured in this seat's own environment:

```
$ TMPDIR=<scratch>/tmp python3 -c 'import tempfile,os
d=tempfile.mkdtemp(prefix="tameshi-r12-repeat-control-selftest.",dir=tempfile.gettempdir());print(d)'
/fast/scratch/hyaku/tameshi-r53/w1/T53W1Read11/tmp/tameshi-r12-repeat-control-selftest.ayq90wto

$ env -u TMPDIR python3 -c 'import tempfile;print(tempfile.gettempdir())'
/tmp
```

(The base is tested for writability, not merely read: with `TMPDIR` pointed at a `chmod 555` directory, `gettempdir()` falls back to `/tmp` and the self-test still passes 29/29.)

The patch that made this true is `218bc6b` ("round-53: fix pass - ... tools/ /tmp hardcodes honour TMPDIR; recipe+registry scratch docs name HYAKU_SCRATCH"), an ancestor of C*:

```
$ git show 218bc6b -- tools/repeat-control.py
-    scratch = tempfile.mkdtemp(prefix="tameshi-r12-repeat-control-selftest.", dir="/tmp")
+    scratch = tempfile.mkdtemp(prefix="tameshi-r12-repeat-control-selftest.", dir=tempfile.gettempdir())
```

The same commit updated the sibling `tools/env-diff.py` registry cells to the TMPDIR form ("an isolated scratch sandbox under `$TMPDIR` (`tameshi-r21-envdiff.*`)", SKILL.md:1982; "sandboxes under `$TMPDIR` (`tameshi-r21-envdiff.*`) and TMPDIR-respecting selftest trees", SKILL.md:2152) but left this cell on the literal `/tmp`. Since the host scratch directive of 2026-10-25 tells seats to run with `TMPDIR` set outside `/tmp`, the declared write scope is not where the self-test writes. The cell is still correct as a description of the *prefix* (`tameshi-r12-repeat-control-selftest.` matches `tameshi-r12-*`) and of "isolated" and of "snapshot read-only" (the snapshot modes execute nothing and were verified above); only the base directory is stale.

Also noted, outside the section and therefore not a finding: the tool's own docstring still says `/tmp/tameshi-r12-repeat-control-selftest.*` (`tools/repeat-control.py:67`), i.e. the tool-internal text drifted in the same commit. Read06 owns the `/tmp/tameshi-r12-controls-UNIQUE` recipe line in the preceding section.

### F2 - bash witness-study write scope names `/tmp`, the tool writes under `$TMPDIR`

Quote (byte-exact, appears in the section):

```
isolated `/tmp/bash-witness-selftest-private.*` (selftest only)
```

Why it fails at C*: `tools/bash-witness-study.py:1240-1241` at C* is

```
private_root = Path(tempfile.mkdtemp(
    prefix="bash-witness-selftest-private.", dir=tempfile.gettempdir()))
```

and the same `218bc6b` patch changed it:

```
$ git show 218bc6b -- tools/bash-witness-study.py
-        prefix="bash-witness-selftest-private.", dir="/tmp"))
+        prefix="bash-witness-selftest-private.", dir=tempfile.gettempdir()))
```

So the private root is `$TMPDIR/bash-witness-selftest-private.*` whenever `TMPDIR` is writable. As with F1 the prefix, the "selftest only" qualifier and the rest of the cell hold - the self-test passes 51/51 and removes its private root ("check private root is removed ok") - but the declared base directory is not the one the tool uses.

The history matters for calibration: the round-27 cold read of this section (`.ufo/waves/round-27/w1/Read25.md`, W1) reported that this cell's *prefix* was wrong (`/tmp/tameshi-r12-*` in the bash row) and asked for `/tmp/bash-witness-selftest-private.* (selftest only)`. That fix landed, and the round-53 TMPDIR patch then made the base stale in turn. The row is now wrong in one dimension instead of another.

## What holds

Table row 1 (repeated pristine controls), all cells except the write-scope base:

- `--runs 3 --out DIR -- COMMAND ARG...` and `--snapshot DIR` both exist and both ran; `--out` must not already exist is the tool's own contract (`DIR` refused with exit 64 on reuse), consistent with "fresh caller-selected DIR".
- Verdict map `0 clean; 1 failed; 2 and 64 could-not-evaluate`: `EXIT_BY_ID` (`tools/repeat-control.py:122-130`) is `controls_match 0`, `controls_mismatch 1`, `baseline_nonzero`/`command_unavailable`/`snapshot_tampered`/`setup_error` 2, `invalid_usage` 64. The labels "clean"/"failed" are a compression of `controls_match`/`controls_mismatch` rather than the tool's finding IDs (round-27 Read25 M1 raised the same point); it is a labelling gap, not a false exit map, so I did not file it.
- `--selftest` exits 0 with `SELFTEST: PASS (29 cases)`; the expectations are literal IDs/exits embedded in the tool (`expected=controls_mismatch/1 observed=controls_mismatch/1` style), so "literal expected IDs/exits in tool selftest" holds.
- Both pinned snapshot paths exist and both were re-verified byte-for-byte by the tool (`SNAPSHOT_INPUTS 9 verified` each).
- "snapshot read-only" holds: `--snapshot` executes nothing and recomputes the finding from stored bytes; both exit codes came out as recorded.

Table row 2 (bash declared-witness study), all cells except the write-scope base:

- Entry command `count` exits 0 on a complete classified sample (`witness_classified=10`, `unresolved none`, `inconclusive=0`), matching "0 complete classified sample".
- `1 unresolved/failed integrity` matches `EXIT_FAIL if tally["unresolved"]` (line 1125) plus the tamper/mismatch refusals in `check`/`run`.
- `2 could-not-evaluate` matches `EXIT_CANNOT` (line 949, 1073) and the observed `run`/`rerun` refusals.
- `64 usage only (argparse)`: `EXIT_USAGE = 64` (line 119) with the parser overriding argparse's default 2; the parenthetical "(argparse)" names the mechanism, and the tool documents the override ("Usage errors exit 64 (the probe contract), not argparse's default 2"). I did not exercise a usage error directly; this is read from the constants and the parser.
- `selftest` exits 0 with `WITNESS_SELFTEST: 51/51 pass`.
- The three pinned paths exist; `manifest.json` is not self-pinned (checked structurally, 95 entries).
- "own evidence directory": the sweep writes `--workdir` inside the evidence tree, and `check` covers 96 files including `summary.json`, `declared.tsv`, the target `pristine.sh` and the spec `bash-surface-census.spec`.

Paragraph claims:

- "Registry scope is these round-12 instruments": both tools are round-12 (`repeat-control.py` banner "r12", `bash-witness-study.py` docstring "round 12, seat BashWitness").
- "Witness declarations are integrity-frozen (declaration, mapping, target, spec, summary; `manifest.json` itself is not pinned, seat ReRead08)": the covered set is exactly those five kinds, `check` exits 1 only on the runner drift line (no TAMPER line among 96 files), and `manifest.json` is absent from its own `files` map. Seat ReRead08 traces exist at C*.
- "not blind: ... had seen the source, the spec, the recorded aggregate outcomes and the per-defect KILLED/SURVIVED entries (`declaration.json`; seat ReRead08)": `declaration.json`'s `disclosure` names the kill-rate header, the corpus coverage row, the SOURCES row and the TABLE_BASH per-defect KILLED/SURVIVED entries, and states no per-defect witness classification pre-existed.
- The stale-pin sentence is **dated to round 27** and still true at C* on every clause: `check` exits 1 with `DRIFT ... committed=75ed934d...`, `run`/`rerun` exit 2 refusing, `count` exits 0 without reading the runner, and the `Read25.md` receipt exists. The declaration's committed runner sha256 is still `75ed934d...` while the runner at C* is `977de470...`. Treated as a hold because it is explicitly dated, not as a live claim.
- "The bash study deepens one recorded case, never a seventh independently measured gate": scope claim; consistent with `count`'s single leg (10 defects, one target, one suite).
- Calibration correction: holds (SHONEN box 3 was a scope-bounded `[~]` at round 12 in `9df9212`, and `corpus/lessons/round-1-verifier-spotcheck.md` does not credit the box-3 increment).
- "Appending this registry does not extend the earlier Appendix A/B cold-read to new material or establish full-page instruction sufficiency": a disclaimer; nothing in the section contradicts it.

## Smallest safe correction (for L1; nothing edited)

1. Repeat row write scope: `isolated \`$TMPDIR\` (\`tameshi-r12-repeat-control-selftest.*\`) selftest`, matching the env-diff rows' form.
2. Bash row write scope: `isolated \`$TMPDIR\` (\`bash-witness-selftest-private.*\`) (selftest only)`.
3. Optional, tool-internal and outside SKILL.md: `tools/repeat-control.py:67` docstring still says `/tmp/...`; it should name `$TMPDIR`/`gettempdir()` like the code.

## Verification gaps

- No usage-error run for either tool (exit 64 taken from the constants and parser wiring).
- The `Kind` and `Owner` cells are registry metadata and were not checked against anything.
- No mutation sweep was attempted: `run`/`rerun` refuse at C* by design, so sweep behaviour at this revision is unobserved (the same gap round-27 Read25 recorded).
- The pre-218bc6b `/tmp` code was read only through the `git show` diff, not executed.

## Scratch / tooling

- Scratch: `/fast/scratch/hyaku/tameshi-r53/w1/T53W1Read11/` (removed before yield). No git mutation; `git archive`, `git show`, `git ls-tree`, `git grep`, `git rev-parse`, `git merge-base --is-ancestor` only.
- Tooling installed: none. No pacman, no network fetches; only the host `python3` and `git`.

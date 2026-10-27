# T53W2Read08 — wave-2 re-read of SKILL.md `### Gate/probe registry` at C**

- Lane repo: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
- C** = `5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e` (fix pass 2, 21 re-fixed sections + strict TMPDIR helper in 7 tools)
- SKILL.md at C**: `sha256 4b4a05251208beb61b0ad70ff8f26fef42dd9d3187317c4286b06c42b06b3d6d`, 2190 lines, 197139 bytes
- Section: lines 1516-1532, 17 lines, 2230 bytes, `sha256 99285e24a71a8d2a0ea3fd6bcafe7e080acb23bfd653e7cbb3b71dfdc5144c77`, no trailing newline
- Next heading: line 1534 `## Pin disposition and provenance correction — round 13`
- Verdict: **wave-1 fixes verified in the C** bytes (both cells), 1 new finding

All SKILL.md/tool bytes were read through git objects (`git show C**:path`) and an `git archive` extraction of C** into this seat's scratch. The lane working tree was never read as content and nothing in the lane was written.

## Section resolution (frozen monitor rule)

Heading = first line matching `^#{1,3}(\s|$)` outside ``` fences equal to `### Gate/probe registry`; section = heading line through the line before the next outside-fence heading; trailing whitespace-only lines stripped; joined with `\n`; no trailing newline; sha256 over UTF-8 bytes with `surrogateescape`.

Two independent computations, both agreeing on `99285e24a71a8d2a0ea3fd6bcafe7e080acb23bfd653e7cbb3b71dfdc5144c77` / 2230 bytes / 17 lines:

1. text split on `"\n"`, slice `[start:end)`, `"\n".join`, encode with `surrogateescape`;
2. byte-level split of the raw blob on `b"\n"`, slice, `b"\n".join`.

A first attempt at the byte-slice variant used character offsets as byte offsets and came out 2 bytes short; the section contains one U+2026 (`75ed934d…`), which is 3 bytes and 1 character, so character-based offsets are not byte offsets. The corrected byte-level method (2) is what is reported above; the naive run was discarded, not reconciled.

## Fix verification (done first)

The two cells the wave-1 reader (`.ufo/waves/round-53/w1/T53W1Read11.{json,md}`) filed on were changed by the fix pass, and only those two cells changed in this section:

```
$ git diff a41195d 5b703c6 -- SKILL.md        # hunk containing both rows
-| repeated pristine controls | ... | fresh caller-selected DIR; isolated `/tmp/tameshi-r12-*` selftest; snapshot read-only | tameshi |
-| bash declared-witness study | ... | own evidence directory plus isolated `/tmp/bash-witness-selftest-private.*` (selftest only); sibling object store read-only | tameshi |
+| repeated pristine controls | ... | fresh caller-selected DIR; isolated `$TMPDIR` selftest tree (`tameshi-r12-*`); snapshot read-only | tameshi |
+| bash declared-witness study | ... | own evidence directory plus isolated `$TMPDIR` selftest tree (`bash-witness-selftest-private.*`, selftest only); sibling object store read-only | tameshi |
```

No `/tmp` string remains anywhere in the section (`grep -c '/tmp'` over the section bytes: 0).

### The cells are true of the C** code

`tools/repeat-control.py` at C**:

```
148: def strict_scratch_root():        # TMPDIR when set and usable; else platform default
153:     t = _os.environ.get("TMPDIR")
154-158: if set but not isdir/W_OK -> raise RuntimeError("... (could-not-evaluate)")
611: scratch = tempfile.mkdtemp(prefix="tameshi-r12-repeat-control-selftest.", dir=strict_scratch_root())
```

`tools/bash-witness-study.py` at C**:

```
205: def strict_scratch_root()         # same contract
1255:     prefix="bash-witness-selftest-private.", dir=strict_scratch_root()))
```

Observed, not inferred — with `TMPDIR` bound to a scratch directory, the selftest trees materialise under it with exactly the documented prefixes, and are removed:

```
repeat-control observed under $TMPDIR: ['/fast/.../T53W2Read08/poll-tmp/tameshi-r12-repeat-control-selftest.39vp49b_'] exit 0
repeat-control leftovers: []      /tmp leftovers with prefix: []
bash-witness   observed under $TMPDIR: ['/fast/.../T53W2Read08/poll-tmp/bash-witness-selftest-private.ugu4qtoz'] exit 0
bash-witness   leftovers: []      /tmp leftovers with prefix: []
```

Both fixed cells therefore hold, including the prefix patterns (`tameshi-r12-*`, `bash-witness-selftest-private.*`), the "selftest only" qualifier (the private root is created only in `cmd_selftest`, line 1255) and "isolated" (both trees removed on PASS).

## Checks run (at C**)

Execution tree: `git -C <lane> archive C** | tar -x -C /fast/scratch/hyaku/tameshi-r53/w2/T53W2Read08`, run with `TMPDIR` inside that scratch.

### Entry and self-test commands

```
$ TMPDIR=<scratch>/tmpdir python3 tools/repeat-control.py --selftest
SELFTEST_CASE snapshot-committed-mismatch PASS (expected=controls_mismatch/1 observed=controls_mismatch/1)
SELFTEST: PASS (29 cases)                                   exit=0

$ TMPDIR=<scratch>/tmpdir python3 tools/bash-witness-study.py selftest
  check private root is removed                      ok
WITNESS_SELFTEST: 51/51 pass
VERDICT: PASS                                               exit=0

$ python3 tools/repeat-control.py --runs 3 --out <scratch>/out1 -- true
REPEAT_COMPARE identical=yes runs=3
REPEAT_OUT <scratch>/out1
REPEAT_CONTROL: controls_match                              exit=0
```

### Snapshot mode — "snapshot read-only"

```
$ python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate            exit=0 (SNAPSHOT_INPUTS 9 verified, controls_match)
$ python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate/mismatch   exit=1 (controls_mismatch)
$ sha256 over all ControlGate files before/after                          -> SNAPSHOT_EVIDENCE_UNCHANGED
$ ls -A "$TMPDIR" after the two runs                                      -> 0 entries
```

### The stale-pin sentence and `check`/`run`/`rerun`/`count`

```
$ python3 tools/bash-witness-study.py check
WITNESS_CHECK: DRIFT tools/mutate-and-run.sh sha256=977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda committed=75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5
WITNESS_CHECK: FAIL (1 problems; 96 files covered)          exit=1

$ python3 tools/bash-witness-study.py run    -> CANNOT-EVALUATE (runner-drift ...)  exit=2
$ python3 tools/bash-witness-study.py rerun  -> CANNOT-EVALUATE (runner-drift ...)  exit=2
   (sha256 of every file under .ufo/evidence/round-12/BashWitness before == after -> EVIDENCE_UNCHANGED)

$ python3 tools/bash-witness-study.py count
counts	killed_on_witness=8	accidental=0	survived=2	inconclusive=0	total=10	witness_classified=10
declared_none	B5,B10
unresolved	none                                          exit=0
```

`count` exits 0 while the pin is stale, so "count never reads the runner" is observed at C**, not read off the source.

### Pinned-value and pointer existence (git objects at C**)

```
.ufo/evidence/round-12/ControlGate/expected.json            PRESENT
.ufo/evidence/round-12/ControlGate/mismatch/expected.json   PRESENT
.ufo/evidence/round-12/BashWitness/declaration.json         PRESENT
.ufo/evidence/round-12/BashWitness/declared.tsv             PRESENT
.ufo/evidence/round-12/BashWitness/manifest.json            PRESENT
.ufo/waves/round-27/w1/Read25.md                            PRESENT
.ufo/evidence/round-27/coldread/traces/ReRead08-*.json      37 files, present
```

`manifest.json` structure: keys `['created_at','files']`, 95 entries, `"manifest.json"` not a member of its own `files` map (the only `manifest.json` string is the nested `rerun-20261020T035435Z/manifest.json` entry) — so "`manifest.json` itself is not pinned" holds structurally as well as through `check` (no TAMPER line among 96 files).

### Calibration-correction paragraph

```
$ git show 9df9212:SHONEN.md | sed -n '1,12p'    (9df9212 = "round-12: repeated controls and bounded bash witness attribution", 2026-10-20 01:01)
- [~] Instructions executable by an agent without oral context
  [lane assertion, scope-bounded: fleet round-1 cold-read of blob 4eb4cf3:SKILL.md - Appendix A + B sweep recipe only, ...; no independent promotion verifier]
$ git log -1 c7986cd   -> round-1 closeout, 2026-10-19 19:15; merge-base --is-ancestor c7986cd 9df9212 -> c7986cd BEFORE 9df9212
$ git show C**:corpus/lessons/round-1-verifier-spotcheck.md
17: ... with the score re-pinned at 6 - the box-3 increment is not credited (cold-read covered Appendix A+B only, probes reconstructed); ...
```

The referent "the historical promotion paragraph above" resolves to `## Promotion-evidence calibration — fleet round-1` (lines 1481-1495), which still reads "Box 3 was `[ ]` at this write (`[~]` since `c7986cd`; Errata — round 16)". At the round-12 revision box 3 was `[~]` with an explicit "scope-bounded" qualifier, so the correction holds.

### Tools are the round-12 instruments the paragraph names

`tools/repeat-control.py:2` "repeated pristine-control gate (tameshi-shokunin, round 12)"; `tools/bash-witness-study.py:3` "bash-surface-census mutation leg (tameshi-shokunin, round 12, seat BashWitness)".

## Finding

### F1 — the row-2 verdict map no longer covers its own self-test under the strict `$TMPDIR` precondition

Quote (byte-exact, present once in the section):

```
0 complete classified sample; 1 unresolved/failed integrity; 2 could-not-evaluate; 64 usage only (argparse)
```

Why it does not hold at C**:

```
$ TMPDIR=<scratch>/no-such-dir python3 tools/bash-witness-study.py selftest
Traceback (most recent call last):
  ...
  File ".../tools/bash-witness-study.py", line 1255, in cmd_selftest
    prefix="bash-witness-selftest-private.", dir=strict_scratch_root()))
  File ".../tools/bash-witness-study.py", line 213, in strict_scratch_root
    raise RuntimeError(
RuntimeError: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '.../no-such-dir' (could-not-evaluate)
exit=1
```

- `main()` (`tools/bash-witness-study.py:1776-1790`) catches only `Fail` (exit 1) and `Cannot` (exit 2); the helper's `RuntimeError` (`:205-216`, reached from `cmd_selftest` `:1255`) escapes as a traceback with **exit 1**, which this cell classes as "1 unresolved/failed integrity". The helper's own message says `(could-not-evaluate)`, and nothing was graded — no case ran.
- The sibling row of the same table handles the identical precondition through the verdict map: `python3 tools/repeat-control.py --selftest` (and `--runs`) with the same unusable TMPDIR prints `repeat-control: setup: RuntimeError: ... (could-not-evaluate)` then `REPEAT_CONTROL: setup_error` and exits 2 (`EXIT_BY_ID` `setup_error: 2`, `tools/repeat-control.py:121-131`). So row 1's "2 and 64 could-not-evaluate" holds for the new precondition while row 2's "2 could-not-evaluate" does not.
- Consequence for a reader of the registry: at C** exit 1 from the self-test covers two different things — a genuine selftest integrity failure and a scratch-root refusal that was never evaluated — and the CR47 distinction the fix pass was enforcing (set-but-unusable `TMPDIR` is could-not-evaluate, never a silent fallback, `contract.json` claim C2) is lost at the exit code.
- The failure is confined to the self-test column; `count` and `check` do not touch the scratch root (`count` and `check` exit 0/1 respectively with the same unusable TMPDIR), so the entry-command cell and the rest of the map are unaffected.

Nothing was edited; the correction belongs to the L1 (e.g. route the helper's refusal through `Cannot` in `cmd_selftest`, or state in this row that a scratch-root refusal is exit 2).

## What holds

- Both wave-1 fixes are present in the C** bytes and are true of the C** code, as shown above:
  - "fresh caller-selected DIR; isolated `$TMPDIR` selftest tree (`tameshi-r12-*`); snapshot read-only"
  - "own evidence directory plus isolated `$TMPDIR` selftest tree (`bash-witness-selftest-private.*`, selftest only); sibling object store read-only"
- "0 clean; 1 failed; 2 and 64 could-not-evaluate" (row 1): `EXIT_BY_ID` is `controls_match 0`, `controls_mismatch 1`, `baseline_nonzero`/`command_unavailable`/`snapshot_tampered`/`setup_error` 2, `invalid_usage` 64; all four observed arms (0, 1 via `--snapshot mismatch`, 2 via the unusable-TMPDIR setup path, 64 read from the constant). The labels "clean"/"failed" compress `controls_match`/`controls_mismatch` (round-27 Read25 raised the same point); a labelling gap, not a false map, so not filed.
- Entry commands both run as written at C**: `--runs 3 --out DIR -- COMMAND ARG...` (exit 0, `identical=yes runs=3`), `--snapshot DIR` (0 and 1), `count` (exit 0, complete classified sample), `selftest` (0, 29 cases / 51-of-51).
- "literal expected IDs/exits in tool selftest": the PASS lines carry `expected=controls_mismatch/1 observed=controls_mismatch/1` style literals.
- "fresh caller-selected DIR": `--out` refuses an existing directory (exit 64, exercised as a selftest case `existing-out`); a fresh DIR is written and left with the `REPEAT_OUT` observation.
- "snapshot read-only": both snapshot runs recompute from stored bytes, execute nothing, write nothing to the evidence tree or `$TMPDIR`.
- "own evidence directory": the sweep writes `summary.json`/`manifest.json`/`sweep/` inside `.ufo/evidence/round-12/BashWitness/`; `write_manifest(root)` (`:835-855`) covers every regular file under that root except the manifest itself and `*.tmp`.
- "sibling object store read-only": "sibling object store" resolves to the kagi git object store (`KAGI_DEFAULT = REPO.parent / "kagi-shokunin"`, `:97`); the tool only reads it (`git -C kagi show --end-of-options REV:pristine.sh`, `:362`), and no git write subcommand exists in the tool.
- "Witness declarations are integrity-frozen" and "`manifest.json` itself is not pinned, seat ReRead08": `check` reports no TAMPER line over 96 files, the covered set is declaration/mapping/target/spec/summary plus run artifacts, and the manifest is not in its own map. Seat `ReRead08` traces exist at `.ufo/evidence/round-27/coldread/traces/ReRead08-*.json` (37 files) and their content is the input dump of these files.
- "not blind": `declaration.json`'s `disclosure` names the recorded kill-rate header, the corpus coverage row, the SOURCES S033 row and the TABLE_BASH per-defect KILLED/SURVIVED entries, and states that no per-defect witness classification of the leg existed before.
- "The declaration's runner pin `75ed934d…` is stale at round 27" — dated, and still true at C**: `check` exits 1 `DRIFT` with `committed=75ed934d…` vs current `977de470…`; `run`/`rerun` refuse with exit 2 and leave the evidence tree byte-identical; `count` exits 0 without reading the runner; the cited receipt `.ufo/waves/round-27/w1/Read25.md` exists and does record that drift (its line 18 quotes the same DRIFT line).
- "Registry scope is these round-12 instruments; no new conformance assertion is made about the historical runner": both tools self-identify round 12; the disclaimer is a scope statement with nothing contradicting it in the section.
- "The bash study deepens one recorded case, never a seventh independently measured gate": consistent with the single leg (10 defects, one target `pristine.sh`, one suite).
- "`SHONEN.md` box 3 carried a scope-bounded `[~]` at round 12, not `[ ]`" and "`corpus/lessons/round-1-verifier-spotcheck.md` excludes it from the score": both verified against `9df9212:SHONEN.md` and the lesson at C**.
- "Appending this registry does not extend the earlier Appendix A/B cold-read to new material or establish full-page instruction sufficiency": disclaimer; nothing in the section contradicts it.

## Out-of-scope observations (not findings)

- `tools/repeat-control.py:67` (docstring) still says the self-test writes under `/tmp/tameshi-r12-repeat-control-selftest.*` at C**, while the code writes under `$TMPDIR` when set. That is tool-internal text, outside this section; the section itself no longer carries the stale `/tmp` claim.
- A later registry (`### Round-26 gate/probe registry …`) carries a second bash-witness row for `check` whose map says "64 could-not-evaluate (usage)" where this section says "64 usage only (argparse)". Different section, not filed here.

## Verification gaps

- No usage-error run for either tool was made (exit 64 taken from the constant and the embedded selftest case).
- The `Kind` and `Owner` cells are registry metadata and were not checked against anything.
- `run`/`rerun` cannot execute at C** (by design, stale pin), so sweep behaviour at this revision is unobserved.
- The scratch-root tree location was observed by polling `$TMPDIR` during the two selftest runs (5 ms interval); a tree created and removed inside one interval would have been missed, though the documented prefixes and the no-`/tmp`-fallback results make that unlikely.

## Scratch and tooling

- Scratch: `/fast/scratch/hyaku/tameshi-r53/w2/T53W2Read08/` (removed before yield; the extraction, poll dirs, out dirs and hash snapshots lived there).
- Git use: `show`, `diff`, `log`, `cat-file -e`, `ls-tree`, `merge-base --is-ancestor`, `archive` — all read-only; no `commit`/`checkout`/`jj`, no fixture commit, no mutation anywhere.
- Tooling installed: none. No pacman (paused), no network fetches; only host `python3` and `git`.

# T55W1RevNote — attack on `## One line, every mode` (round 55, hyaku run 11)

Scope: the drafted section `corpus/knowledge/scratch-root-contract.md:71-98` plus the
note's existing text, checked against the tools, the frozen regex and the frozen
counter. No production file was edited; evidence lives in
`.ufo/waves/round-55/w1/T55W1RevNote-receipts/`.

## Reviewed state (read this before the findings)

The lane was **dirty** and changed under me mid-review. Two states matter:

- **State A (the draft as written)** — lane HEAD `631cd64`; note, `tools/registry.json`,
  `SKILL.md` mtime `13:41`; `c2/measure.py` mtime `13:50`; `tools/registry-check.py`
  as committed at base. Everything in the Findings was measured on State A unless a
  finding says otherwise.
- **State B (now)** — at `14:01:35` a concurrent uncommitted edit added
  `ScratchRootUnusable` to `tools/registry-check.py` and a catch for the `--rev`
  allocation path. That changes the outcome of F1's *code* half; the note, registry
  cells, SKILL.md and the counter still say eight (their mtimes are unchanged).

Because the draft is uncommitted, the frozen counter cannot run over it yet; every
measurement is a direct invocation of the worktree files with the exact command
recorded.

## What I ran (the sweep)

| # | command (cwd = lane) | receipt |
|---|---|---|
| 1 | `TMPDIR=<nonexistent> python3 tools/<tool>.py <mode>` × the 8 counter modes + `env-diff --contract` (contract materialised in scratch) | `01-eight-allocating-modes.txt` |
| 2 | `TMPDIR=<nonexistent> python3 tools/registry-check.py --rev 0a2010ac… --root .` (State A, and again after State B) | `02-…`, `12-…` |
| 3 | `TMPDIR=<nonexistent> python3 tools/pin-disposition.py --read` | `03-pin-disposition-read-does-not-exist.txt` |
| 4 | `TMPDIR=<nonexistent>` × the 5 counter lazy modes; `grep -n 'strict_scratch_root(' tools/*.py` | `04-lazy-modes-no-allocation.txt` |
| 5 | every emitted line matched against the frozen `GRAMMAR` imported from `.ufo/evidence/round-55/c2/measure.py` | `05-grammar-vs-react-draft.txt` |
| 6 | counter `note`/`docs` arm emulation, registry-cell dump | `06-counter-note-and-docs-arms.txt` |
| 7 | S277/S278/S279 re-read from the round-54 snapshots | `07-S277-S279-source-text.txt` |
| 8 | round-54 `before/` and `after/` C2 receipts | `08-round54-before-after.txt` |
| 9 | base-vs-worktree class census, helper census, shared-module sweep | `09-type-census.txt` |
| 10 | note lines 71-98 verbatim | `10-note-lines.txt` |
| 11 | `git log -S"strict_scratch_root"`, helper size at `5b703c6`, pre-round-53 tree | `11-helper-origin.txt` |
| 12 | mtimes + post-State-B re-measurement of `registry-check` | `12-concurrent-changes-and-freeze-integrity.txt` |
| 13 | freeze integrity exactly as `deciding-run.sh:20-40` computes it; frozen-path diff vs `FREEZE`; `before/c2.stdout` head-vs-tree | `13-freeze-and-record-integrity.txt` |

## Verdict table (the item's five checks + what else the text asserts)

| # | Claim (note lines) | Verdict |
|---|---|---|
| 1a | the note's eight mode names equal the counter's eight (77-80 vs `measure.py:78-98`) | **holds** (8/8 token-equal; the counter's `note` arm scores 8/8) |
| 1b | those eight are *the* allocating modes / "the round-55 counter measures every documented allocating mode" (77-80, 65-67) | **wrong** — a ninth documented allocating mode exists: `registry-check --rev` (`tools/registry-check.py:60-65`, `:780`). In State A it also failed the grammar; in State B it conforms but is still unmeasured. The note/registry/SKILL still say eight |
| 2a | the five lazy modes do not allocate scratch | **holds** as a fact (each tool's helper has one call site, all in the selftest) |
| 2b | the stated *reason*, "scratch is allocated on the real path, not at parse time" (91-92) | **wrong** — those five paths never call `strict_scratch_root()` at all |
| 2c | the mode named `pin-disposition --read` (88) | **wrong** — no such mode; the flag is rejected (`unknown argument: --read`) |
| 3 | the grammar quoted matches the frozen regex byte for byte (73-75) | **literal core holds; overreaches as the grammar** — token charset, non-empty value and the `^…$` anchoring (no prefix) are unstated; `<tool>` mislabels a token that is not the tool name |
| 4 | S277-S279 say what the note says (14, 17-24, 26-30) | **holds** — all three re-verified against the snapshots |
| 5 | nothing claims a shared Python type (81-85) | **holds** — no shared module or cross-import; 7 local helpers. The parenthetical is imprecise/stale (F7) |
| 6 | "the tools and their registry rows now name" the rule (5-7) | **overreaches** — 4 of 7 registry cells quote a line no tool prints; the registry-check cell omits `--rev` (F5) |
| 7 | "The counter measures 13 modes in three arms plus the seven registry cells and this note" (94-96) | **wrong** — four execution blocks over three TMPDIR values, plus a SKILL.md arm the sentence omits (F8) |
| 8 | "a caller that parses stdout sees nothing" (97-98) | **wrong** — `repeat-control` writes `REPEAT_CONTROL: setup_error` to stdout (F4) |
| 9 | "Before round 53 the helpers were seven near-copies of the same fifteen lines" (3-4) | **wrong** — the helper first appears *in* round 53 (`5b703c6`), 12 lines; before it the tools used `dir="/tmp"` (F9) |

## Findings

### F1 (high) — the allocating-mode set is nine, not eight; the ninth is unmeasured

Note 77-80: "Eight allocating modes carry it — …"; note 65-67: "the round-55 counter
measures every documented allocating mode, not the self-test only."

`registry-check` allocates scratch on two paths: `tools/registry-check.py:780`
(`tempfile.mkdtemp(…, dir=strict_scratch_root())` inside `clone_lane_at_rev`) reached
by the **documented** `--rev` mode (`tools/registry-check.py:60-65`, in the `--help`
docstring), and `:931` (the selftest, the only one the counter measures).

**State A** (measured before the concurrent edit, receipt 02):

```
rc=2
stdout: REGISTRY_CHECK: could-not-evaluate (cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/fast/scratch/…/no-such-tmpdir' (could-not-evaluate))
stderr: <empty>
```

`NOMATCH` against the frozen `GRAMMAR` (receipt 05): parenthesised, on stdout, and
the regex is anchored `^…$`.

**State B** (after the `14:01:35` edit, receipt 12): rc 2, stdout empty, stderr

```
registry-check: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/fast/scratch/…/no-such-tmpdir' (could-not-evaluate)
```

which matches the grammar. So the code half of the defect is gone, but every
statement of the taxonomy is still wrong:

- the note, unchanged since `13:41`, says eight;
- `tools/registry.json` (mtime `13:41`) still says `Allocating modes: selftest.` for
  `registry-check` (F5);
- `SKILL.md:37-42` (mtime `13:41`), which item 4 re-keys, says "Measured on every
  documented allocating mode — the seven self-tests plus `env-diff --contract`";
- the counter still has an eight-mode denominator and **never runs
  `registry-check --rev`** in any arm, so a regression back to a parenthesised
  stdout line would not be caught.

The note's blind-spot sentence (96-97: "a documented mode outside the registry and
the usage text could still allocate scratch unmeasured") does **not** cover this
case: `--rev` is inside the usage text, outside the registry.

Measured non-allocating siblings for completeness: `bash-witness-study`
`run`/`rerun`/`declare`/`check` allocate nothing (its only `tempfile.mkdtemp` calls
are in the selftest, `:1259-1264`).

### F2 (high) — `pin-disposition --read` is not a mode

Note 88 lists `pin-disposition --read` among the five lazy modes. The tool accepts
only `--manifest PATH --root FLEET` and `--selftest` (`tools/pin-disposition.py:148-149`
usage; `parse_argv` rejects anything else). Measured (receipt 03):

```
$ TMPDIR=<unusable> python3 tools/pin-disposition.py --read   → rc=2
{ "schema": "pin-disposition-v1", … "status": "invalid_input",
  "error": {"kind":"invalid_usage","message":"unknown argument: --read"} … }
```

The mode as named exits **2**, which is exactly the "expected exit" the note says
it keeps (0). The mode the counter actually runs is `--manifest
.ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin`
(`measure.py:105-108`), which exits 0 — the counter's *label* is wrong, and the note
copied it. (The base receipt's deleted EXPLAIN lines — F10 — recorded the same
fabricated label.)

### F3 (medium) — the lazy modes do not allocate; the stated mechanism is wrong

Note 87-92: "… keep their expected exit under an unusable `TMPDIR`, because scratch
is allocated on the real path, not at parse time."

`strict_scratch_root()` has exactly one call site per tool and every one is inside
the selftest (receipt 04): `repeat-control.py:629`, `bash-witness-study.py:1260`,
`pin-disposition.py:725`, `evidence-disposition.py:2370`,
`context-capture.py:1643` (`SelftestHarness.__init__`). The five modes named (with
F2's correction) exit 0 because they never enter an allocating path, not because
allocation is deferred. The measured exits are right (0/0/0/0/0); the mechanism the
sentence asserts is not.

### F4 (medium) — "a caller that parses stdout sees nothing" is false

Note 97-98. Measured (receipt 01) for `repeat-control --selftest` under an unusable
`TMPDIR`: stderr is the grammar line, and **stdout is `REPEAT_CONTROL: setup_error`**
(`tools/repeat-control.py:228-235`: `could_not_evaluate` calls `emit(...)` after the
stderr line). That is also the round's item-1 requirement ("stdout carries no setup
error") still unmet for that tool. `context-capture` is clean (stdout empty), and its
new comment (`tools/context-capture.py:2216-2218`) claims exactly that property for
itself; the sibling edit did not carry it. A stdout-parsing caller sees a setup
token; for State-A `registry-check --rev` it saw the class line itself.

### F5 (medium) — the registry cells quote lines the tools do not print, and one omits a mode

Note 5-7 vouches that "the seven tools and their registry rows now name" the rule.
The counter's `docs` arm only looks for the `MARKER` substring (`measure.py:240`), so
it scores 7/7 over these literals (receipt 06):

| cell | quoted prefix | actually printed (receipt 01/12) | allocating list in cell | truth |
|---|---|---|---|---|
| `repeat-control.py` | `repeat-control.py:` | `repeat-control:` | `selftest.` | ✔ list |
| `bash-witness-study.py` | `bash-witness-study.py:` | `WITNESS_STUDY:` | `selftest.` | ✔ list |
| `registry-check.py` | `registry-check.py:` | `registry-check:` | `selftest.` | ✘ `--rev` missing (F1) |
| `env-diff.py` | `env-diff.py:` | `ENVDIFF_SETUP:` | `selftest, --contract.` | ✔ list |
| `pin-disposition.py` | `pin-disposition.py:` | `pin-disposition.py:` | `selftest.` | ✔ |
| `evidence-disposition.py` | `evidence-disposition.py:` | `evidence-disposition.py:` | `selftest.` | ✔ |
| `context-capture.py` | `context-capture.py:` | `context-capture.py:` | `selftest.` | ✔ |

Four of seven cells put a fabricated tool-name prefix in an exact-looking quoted
line. The same fabricated prefixes and the same eight-mode universal appear in
`SKILL.md:37-42`, which round 55 re-keys (item 4) — the re-key must not land the
false universal.

### F6 (medium-low) — the quotation is the literal core, not the grammar

Note 73-75 ("The class is one stderr line, byte-shaped:") quotes

```
<tool>: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '<value>' (could-not-evaluate)
```

Against the frozen regex (`measure.py:47-50`, identical at `FREEZE` and in the
worktree — the amendment diff does not touch it):

```
^[A-Za-z][A-Za-z0-9_.-]*(?:\.py)?: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '.+' \(could-not-evaluate\)$
```

the mid-line literal matches byte for byte, and substituting real tokens matches
(8/8 `MATCH`, receipt 05). What the note does **not** state:

- the leading token's grammar `[A-Za-z][A-Za-z0-9_.-]*(?:\.py)?` — and `<tool>` is
  the wrong label: the emitted tokens are `ENVDIFF_SETUP`, `WITNESS_STUDY`,
  `registry-check`, `repeat-control`, `pin-disposition.py`, … (not the executable
  names);
- the value is `'.+'` — one or more characters, not an optional placeholder;
- the anchors `^…$`: **no prefix or suffix is allowed**, which is exactly the
  property this round is fixing (the round-54 residue was a `SELFTEST: FAIL `
  prefix). "one stderr line, byte-shaped" hedges, but the only prose constraint the
  section adds is "no `RuntimeError` or `Traceback` token", which is weaker than the
  regex: a prefix such as `SETUP: ` would pass the token test and fail the grammar.

### F7 (low) — the exception-type parenthetical is stale and mislabels `env-diff`; the anti-shared-type claim holds

Note 81-85: "the tools keep their own exception classes (`ScratchRootUnusable` in
the two round-55 edits, a local class in `env-diff`)".

- At the note's mtime (`13:41`) the two round-55 edits were `repeat-control` and
  `context-capture` (base had 0 classes in each). At State B there are **three**:
  `tools/registry-check.py:757` gained `ScratchRootUnusable` at `14:01:35`. So "the
  two round-55 edits" is stale by one tool (receipt 12).
- `env-diff`'s local class is itself named `ScratchRootUnusable` (`env-diff.py:32`),
  so the parenthetical's contrast implies a different class that does not exist.
- All seven tools now define their own `ScratchRootUnusable(RuntimeError)`
  (receipt 12), so "the tools keep their own exception classes" is true for 7/7 —
  and each is a distinct local class, which is the point.
- No shared type is claimed and none exists: seven independent
  `strict_scratch_root()` helpers (12-13 lines), no `tools/scratch*.py`, no
  cross-tool import (receipt 09). **That part of the claim holds.**

### F8 (low) — the counter-structure sentence is off

Note 94-96: "The counter measures 13 modes in three arms plus the seven registry
cells and this note". `measure.py` runs four blocks: grammar (8 modes, unusable),
lazy (5 modes, unusable), empty (13 modes), usable (13 modes) — `:190-234`; then the
docs (7 cells), note and **skill** arms — `:236-258`. "Three arms" only works if arms
= TMPDIR values; the SKILL.md arm (`skill=N/1`) is omitted, and "13 modes" is not
true of each block (8+5 split the unusable arm). Also "the five non-allocating modes"
reads as exhaustive; the seven tools have other documented non-allocating modes
(e.g. `bash-witness-study declare|run|rerun|check`, `registry-check` live mode) —
five is the counter's sample.

### F9 (low) — the helper-origin sentence is wrong

Note 3-4: "Before round 53 the helpers were seven near-copies of the same fifteen
lines". `git log -S strict_scratch_root` puts the first appearance in `5b703c6`
("round-53: fix pass 2 … strict TMPDIR scratch-root helper in 7 tools"), where each
helper is **12** lines. In the tree before round 53 the same call sites pass literal
`dir="/tmp"` or omit `dir` (e.g. `6db1d220:tools/env-diff.py:61`, `dir="/tmp"`). So
the helpers did not exist before round 53, and their size was 12, not fifteen
(receipt 11).

### F10 (high, round integrity — reported, not fixed) — frozen paths and the base receipt moved mid-wave

Receipt 13. At `13:49:59` `freeze.json` was written with no amendments; between
`13:49` and `14:01` the following changed and are still **uncommitted**:

| path | mtime | change |
|---|---|---|
| `.ufo/evidence/round-55/contract.json` | `14:00:09` | `amendments: []` → 5 entries |
| `.ufo/evidence/round-55/c1/measure.py` | `14:00:09` | +25 lines (amendment 5) |
| `.ufo/evidence/round-55/c2/measure.py` | `13:50:08` | +32/−12 (amendments 1-4) |
| `.ufo/evidence/round-55/freeze.json` | `13:49:59` | amendments 1-3 only, and stale hashes |
| `.ufo/evidence/round-55/before/c2.stdout` | `13:59:44` | **43 lines → 1 line**: the 42 per-mode `EXPLAIN` lines deleted |

Consequences to check before the deciding run (I did not fix any of them):

1. **`freeze.json` no longer matches its own files.** Its recorded hashes vs the
   worktree: `contract.json` freeze `ed6871e1` ≠ file `5de4f37b`; `c1/measure.py`
   freeze `77abe1e9` ≠ file `711507e7`; `c2/measure.py` freeze `ab3ae751` ≠ file
   `d6ca1d85`. `deciding-run.sh:20-40` reads the *committed* blobs at `FREEZE`, which
   are self-consistent at `631cd64` (`FREEZE_INTEGRITY: OK`), so the gate passes
   today — but if these files are committed and `FREEZE=631cd64` is still passed,
   `deciding-run.sh:64` computes `FROZEN_UNCHANGED=0` (four frozen paths differ) and
   the run is refused. The round needs a re-freeze commit (with `freeze.json`
   re-hashed against the final bytes of `contract.json`, `c1` and `c2`) before the
   content commit, or the amendments must be reverted out of the frozen paths.
2. **`freeze.json`'s amendment ledger under-reports:** 3 entries vs 5 in
   `contract.json` (amendment 5 — the `c1` stale-scan widening — is absent).
3. **The base receipt is no longer the per-mode evidence the contract cites.** The
   contract's `before` cites `.ufo/evidence/round-55/before/c2.stdout`; the committed
   blob had 42 `EXPLAIN` lines ending in `C2_R55: … grammar=6/8 …`, the worktree has
   the verdict line only. The surviving line still supports "6/8", but not the
   contract's per-mode claims (which tool failed, and that a mode labelled
   `pin-disposition --read` was measured). A one-line edit worth noting: the deleted
   lines are the only record that the `--read` label was used at base.

None of this is a statement the **note** makes; it is reported because the round's
frozen-record discipline is mine to check and the deciding run depends on it.

## Claims that hold (with evidence)

- **Eight names == counter's eight** (77-80 vs `measure.py:78-98`): token-equal; the
  counter's `note` arm scores 8/8, `MARKER` present, grammar literal present
  (receipt 06).
- **The eight measured modes behave as claimed** (State A): rc 2, one stderr line
  matching the frozen regex, no `RuntimeError`/`Traceback` on either stream
  (receipts 01, 05). `env-diff --contract` included, with a counter-shaped contract
  materialised in scratch.
- **Five lazy modes exit 0 under an unusable `TMPDIR`** (receipt 04) — and, per F3,
  because they never allocate.
- **Nothing claims a shared Python type** (F7): true, and none exists.
- **S277** (note 26-30): the snapshot carries "TMPDIR This variable shall represent a
  pathname of a directory made available for programs that need a place to create
  temporary files." exactly, and its TMPDIR paragraph states no empty-string rule
  (the only three "empty" hits in the page belong to LANGUAGE/locale text), so "the
  standard fixes the variable's meaning, not its empty-string handling" holds
  (receipt 07).
- **S278** (note 17-19): `_candidate_tempdir_list` lines 163-165 read exactly
  `for envname in 'TMPDIR', 'TEMP', 'TMP':` / `dirname = _os.getenv(envname)` /
  `if dirname: dirlist.append(dirname)`; the `if dirname:` skip is what makes empty
  "unset" (receipt 07).
- **S279** (note 20-22): "The list is: The directory named by the TMPDIR environment
  variable. …" then TEMP, TMP, platform locations — "starts at TMPDIR and falls
  through" holds (receipt 07).
- **Why-the-class-is-uniform history** (34-43): the round-54 `before` receipt shows
  exactly four tools at rc 1 with a raw `RuntimeError:` line (env-diff,
  bash-witness-study, evidence-disposition, pin-disposition) and three at rc 2
  (registry-check, context-capture, repeat-control); `after` shows
  `unusable_exit2=7 naming=7`, and the four now define `ScratchRootUnusable` at base
  (receipts 08, 09). "Round 54 gives each of the four a subclass" holds.
- **What-measures-it numbers** (47-53): round-54 `after` = `unusable_exit2=7
  naming=7 empty_ok=7 usable_ok=7 tmp_mkdirs=0 docs=7`, so the 7/7 statements hold
  (receipt 08).
- **Three-arms table** (11-15): unset → `tempfile.gettempdir()` and unusable → raise
  before `mkdtemp` hold in every helper. One nuance: the empty row's "the platform
  default applies" is true only when `TEMP`/`TMP` are unset too — `gettempdir()`
  continues the candidate list, as the same row's "the next candidate wins" says.
  (Cosmetic; the counter's `env_with` sets only `TMPDIR`.)

## Residual risk and verification gaps

- My evidence is the **worktree**, not a content revision; the concurrent State-B
  edit moved a finding's code half inside this review. Re-run receipts 01-05 and 12
  against the final content commit.
- The frozen counter cannot run until the round commits a content revision; the
  counter's own amendments are uncommitted (F10).
- `registry-check --rev`'s clone path was not exercised with a usable `TMPDIR` (that
  clones the lane); the allocation site is proven by the refusal path and line 780.
- I did not audit the other six `bash-witness-study` modes or `registry-check` live
  mode for indirect allocation beyond `strict_scratch_root()`; `tempfile` uses were
  grep-censused and none exist outside the selftest.
- S277-S279 were verified against the round-54 snapshots, not re-fetched; the rows
  claim the same text and the snapshots are byte-identical to what the rows quote.
- The counter's `note` arm checks only that the eight mode names appear
  (`measure.py:249-251`), not the grammar or the taxonomy: this draft scores
  `note=8/8` with F1/F2/F6 in it.

## Proposed minimal patch (diff, unapplied — L1 integrates)

```diff
@@ note 3-5
-Before round 53 the helpers were seven near-copies of the
-same fifteen lines and only some of their callers mapped the failure to the
-documented class; round 54 makes the mapping uniform and this note is the rule
+Round 53 introduced the helper as seven near-copies of the same twelve lines and
+mapped only some callers to the documented class; round 54 made the exit class
+uniform, round 55 made the line one, and this note is the rule
@@ note 73-85
-The class is one stderr line, byte-shaped:
+The class is one stderr line, matching the frozen counter grammar
+(`^[A-Za-z][A-Za-z0-9_.-]*(?:\.py)?: … '.+' \(could-not-evaluate\)$` — anchored,
+so nothing may precede or follow it; the leading token is the tool's emitted
+prefix, e.g. `ENVDIFF_SETUP`/`WITNESS_STUDY`, not the executable name):
@@ note 77-80
-Eight allocating modes carry it — … eight names …
+The counter measures eight allocating modes and all eight carry it — … eight
+names … — but they are not the whole set: `registry-check --rev`
+(tools/registry-check.py:60-65, :780) allocates too and is unmeasured, so the
+registry cell must list it and the counter should add it to the grammar arm.
@@ note 81-85
-(`ScratchRootUnusable` in the two round-55 edits, a local class in `env-diff`),
+(each tool defines its own `ScratchRootUnusable` — env-diff, repeat-control,
+registry-check, bash-witness-study, pin-disposition, evidence-disposition,
+context-capture),
@@ note 87-92
-The five non-allocating modes are measured lazy: `repeat-control --snapshot`,
-`bash-witness-study count`, `pin-disposition --read`,
-`evidence-disposition --json`, `context-capture --check` keep their expected
-exit under an unusable `TMPDIR`, because scratch is allocated on the real path,
-not at parse time.
+The counter's five non-allocating modes are measured lazy:
+`repeat-control --snapshot`, `bash-witness-study count`,
+`pin-disposition --manifest … --root …`, `evidence-disposition --json`,
+`context-capture --check`. They never call `strict_scratch_root()` at all — each
+tool's only call site is its selftest — so they keep their exit under an unusable
+`TMPDIR`; that is not evidence the root was usable.
@@ note 94-98
-The counter measures 13 modes in three arms plus the seven registry cells and
-this note, and its blind spot is narrower but real: a documented mode outside
-the registry and the usage text could still allocate scratch unmeasured (the
-round-55 wave inventories that difference), and the grammar is matched on
-stderr, so a caller that parses stdout sees nothing.
+The counter runs 13 modes under three `TMPDIR` values (8 grammar + 5 lazy on the
+unusable value, all 13 on empty and usable) and reads the seven registry cells,
+this note and SKILL.md. Its blind spot is narrower but real: a mode documented in
+a tool's usage text but absent from the registry can allocate scratch unmeasured
+(`registry-check --rev` does), the grammar is matched on stderr only, and
+`repeat-control` still writes `REPEAT_CONTROL: setup_error` to stdout.
@@ tools/registry.json — registry-check cell
-… "registry-check.py: could-not-evaluate: …" … Allocating modes: selftest.
+… "registry-check: could-not-evaluate: …" … Allocating modes: selftest, --rev.
@@ tools/registry.json — four cells
-quoted line prefix `<tool>.py:` → the tool's emitted token
-(`repeat-control:`, `WITNESS_STUDY:`, `ENVDIFF_SETUP:`)
```

## Reproduction

```sh
export HYAKU_SCRATCH=/fast/scratch/hyaku; S=$HYAKU_SCRATCH/tameshi-r55/<seat>
U=$S/no-such-tmpdir                     # deliberately never created
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
TMPDIR=$U python3 tools/repeat-control.py --selftest          # rc 2, stderr grammar, stdout REPEAT_CONTROL: setup_error
TMPDIR=$U python3 tools/context-capture.py --selftest         # rc 2, stderr grammar, stdout empty
TMPDIR=$U python3 tools/registry-check.py --rev 0a2010ac… --root .   # State A: class on STDOUT; State B: stderr grammar
TMPDIR=$U python3 tools/pin-disposition.py --read             # rc 2, unknown argument: --read
python3 - <<'EOF'   # freeze integrity, as deciding-run.sh does it
import json,hashlib,subprocess
f=json.load(open('.ufo/evidence/round-55/freeze.json'))
for p,h in f['files'].items():
    print(p, hashlib.sha256(open(p,'rb').read()).hexdigest()==h)
EOF
```

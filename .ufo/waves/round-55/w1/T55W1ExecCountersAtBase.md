# T55W1ExecCountersAtBase — independent base receipts (round 55, wave 1)

Item: independently reproduce both before receipts at
`0a2010acd1e92e4e332774050825e21bcfc7e079` in fresh work dirs, `cmp` each stdout
against the committed receipt, and name every differing byte region. A mismatch is
a finding.

Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin` (read-only for this seat;
HEAD `631cd6455e58dce969310b4c0466c3383d9f5108`). No production, frozen, or
counter file was edited by this seat; no git mutation was run in the lane.

## Verdict

| claim | committed receipt | my reproduction | comparison |
|---|---|---|---|
| C1 | `premise=10/10 stale=4 classes_corrected=0/10 total=10 C1_R55_PASS=false` | same verdict line; `total=10 C1_R55_PASS=false` | **byte-identical**, 0 differing bytes |
| C2 | `grammar=6/8 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=0/7 note=0/8 skill=0/1 total=18 C2_R55_PASS=false` | same verdict line; `total=18 C2_R55_PASS=false` | **verdict line byte-identical**; 3 differing regions of 10 bytes each in the EXPLAIN stream (all amendment 3's mode label) |

Both expectations in the seat brief hold. `census validate` exits 0; its 17-line
stdout is 15 `duplicate url` notices, 1 tier note and the final `ok` line — no
error rows. At my read `corpus/SOURCES.md` carries 140 `S###` rows, highest id
`S280` (the brief said 139 rows, `S001`–`S279`: row `S280`, GNU Coding Standards
§4.4, was added by a wave-1 seat while this seat ran). Findings below are about
the evidence pipeline, not about the two claims' truth at base.

## Commands (exact)

```
S=/fast/scratch/hyaku/tameshi-r55/T55W1ExecCountersAtBase   # run A (c1, c2 run 1)
S2=/fast/scratch/hyaku/tameshi-r55/T55W1ExecCountersAtBase-b # run B (c2 run 2, reruns)
L=/home/vgpnk/Projects/shokunin/tameshi-shokunin
REV=0a2010acd1e92e4e332774050825e21bcfc7e079

python3 $L/.ufo/evidence/round-55/c1/measure.py --lane $L --rev $REV --work <fresh empty dir> --explain
python3 $L/.ufo/evidence/round-55/c2/measure.py --lane $L --rev $REV --work <fresh empty dir> --explain
```

`--explain` is used because the committed receipts at HEAD are 43-line EXPLAIN
streams (not bare verdict lines); leaving it off would make any `cmp` meaningless.
Each work dir was created empty and used once. Exit codes: c1 = 1, c2 = 1 (both
counters exit 1 on a failed claim); both wrote nothing to stderr.

## C1 — reproduced byte-identically

- Run A, 13:49, counter sha256 `77abe1e9daf40bec2c9d7a7c12724e766e2f98d222c287fde6097df819b60783`
  (= the hash `freeze.json` pinned at that moment, and = the bytes at HEAD).
- `cmp` against `git show HEAD:.ufo/evidence/round-55/before/c1.stdout`: identical.
  sha256 both `be43a5fcc6eb3171511c861045bbd86cc21dac54295c16b63b7387bd1594f9b4`.
- The verdict line is exactly `C1_R55: rev=0a2010acd1e9 classes=10 premise=10/10
  stale=4 classes_corrected=0/10 total=10 C1_R55_PASS=false`.
- Ten derived values printed by the counter (each derived from the tree, not
  copied from the brief): R54.1 `CTL_MISMATCH + 2/3`, R54.2 `freeze
  pointer=077d431e`, R54.3 `total=13`, R54.4 `c2 digest=8528ee85`, R54.5
  `w1=28 w2=25 sections=12`, R54.6 `sweep commit=ff2a821`, R54.7 `rename
  commit=7fa9a5e`, R54.8 `config.yml + fabricated + seat marked`, R54.9
  `reviewers=5 attack=21/76 seats=76 staged=81`, R54.10 `controls-a
  rekeyed=0/7`. All ten premises hold; all ten corrections are `miss`, as the
  committed receipt records.
- Stale hits at base: 4 of the ten rows carry them — 8 hit lines in total
  (R54.1 ×3, R54.2 ×3, R54.3 ×1, R54.9 ×1); the verdict's `stale=4` is the row
  count (`grep -c 'stale:' c1-mine.stdout` = 8).

Counter drift observed after run A (not a property of the base tree): at 14:02 the
live `.ufo/evidence/round-55/c1/measure.py` was `711507e7b5bdd060...` (amendment 5:
whitespace-normalized span scan + `LOG.md` in `RECORD`). Re-running the identical
command under it raises R54.1 `stale=3` → `stale=6` (+3 span hits) and changes the
stream. That rerun is retained as `c1-rerun-amendment5.*` and is **not** the
certification of the base receipt; run A is.

## C2 — verdict reproduced; three 10-byte regions differ

Committed receipt (`git show HEAD:...before/c2.stdout`): 43 lines, 2634 bytes,
`C2_R55: rev=0a2010acd1e9 grammar=6/8 lazy=5/5 empty=13/13 usable=13/13
tmp_mkdirs=0 docs=0/7 note=0/8 skill=0/1 total=18 C2_R55_PASS=false`.

My run 2 (13:55–14:01, counter sha256 `d6ca1d851bb00373...` incl. amendment 4):
43 lines, 2634 bytes, **verdict line byte-identical**. `cmp -l` reports exactly
30 differing bytes, in three contiguous regions, one per arm that names the
bash-witness mode:

| byte region (1-based) | line | cols | committed | mine |
|---|---|---|---|---|
| 158–167 | 3 (`grammar`) | 36–45 | `bash-witness-study --selftest` | `bash-witness-study selftest` |
| 937–946 | 16 (`empty`) | 35–44 | `bash-witness-study --selftest` | `bash-witness-study selftest` |
| 1704–1713 | 29 (`usable`) | 35–44 | `bash-witness-study --selftest` | `bash-witness-study selftest` |

That is amendment 3 ("the label is the mode as invoked") and nothing else: the
committed receipt was generated by the pre-amendment counter
(`9d076812d9c0...` at HEAD), while my run used the amended one. No timing text
and no clone path appears in either stream (the brief's caveat does not apply
here); both streams are the same length and every other line is identical.

### C2 run 1 — the same command under the freeze-pinned counter reads `total=19`

Run 1 (13:49–13:53) used counter `ab3ae751469164f0...`, the hash `freeze.json`
pinned at freeze time (it lacks amendment 4). Result: `grammar=6/8 lazy=5/5
empty=13/13 usable=12/13 tmp_mkdirs=0 docs=0/7 note=0/8 skill=0/1 total=19
C2_R55_PASS=false`, with `bad = {"usable:registry-check --selftest": "rc=1
expected=0"}`. Every other arm was identical to run 2 (see
`c2-run1-vs-run2.diff`: exactly two lines differ — that arm and the verdict).

Cause, measured: in the usable arm of that counter version the exit code is taken
from the `strace -f` run. Running the same mode untraced with a usable TMPDIR in
the same base clone gives `SELFTEST: PASS (51 cases)`, rc=0, 28.3 s
(`diag-registry-check-usable.txt`). Under the tracer the same selftest returns 1
because its own timing cases (`bounded-pipe-drain`, communicate/wait 0.5 s;
pidfd/subreaper cases) sit behind `strace -f`. This is the observation amendment 4
records; my run reproduced it independently.

### Independent premise checks (grammar arm)

Base clone at `0a2010ac`, `TMPDIR=<nonexistent>`:
`repeat-control --selftest` rc=2 prints `repeat-control: setup: RuntimeError: ...`
(stderr, contains `RuntimeError`); `context-capture --selftest` rc=2 prints
`SELFTEST: FAIL (setup error: RuntimeError: ...)` **on stdout**; the other five
self-tests and `env-diff --contract` print one stderr line matching the frozen
grammar, rc=2 (`premise-grammar-7.txt`, plus the env-diff pair below). That is
exactly `grammar=6/8` at base and exactly the two modes the round must fix.

`env-diff --contract`: unusable TMPDIR → rc=2, grammar match, no `RuntimeError`;
usable TMPDIR → rc=0, `ENVDIFF: classified=1/1`.

## Findings

**F1 — the committed C2 receipt is not reproducible byte-for-byte by the frozen
counter.** The live/frozen counter (frozen at `631cd645`) labels the mode
`bash-witness-study selftest`; the committed receipt at the freeze commit labels
it `bash-witness-study --selftest`. Regions named above. Numeric effect: none (the
verdict line is identical). If a later seat diffs a fresh run against this
receipt, it must expect those three regions or the receipt must be refreshed in a
commit. Command + output: `c2-committed-vs-mine.diff`, `cmp -l` region table.

**F2 — the C2 baseline is counter-version dependent and the pinned version cannot
reach `PASS`.** With the counter bytes `freeze.json` pinned at freeze time
(`ab3ae751`, no amendment 4), base reads `usable=12/13 total=19`, and that arm is
independent of what this round lands: it scores `registry-check.py`'s self-test —
a tool the round does not edit — under `strace -f`, and that self-test returns 1
under the tracer on this host. So at that counter version `C2_R55_PASS=true` is
unreachable; amendment 4 (exit code from a plain run, tracer only for the `/tmp`
mkdir census) is load-bearing, not cosmetic. The current unpinned counter
`d6ca1d85` restores `total=18`. Evidence: run-1 vs run-2 diff; plain
`SELFTEST: PASS (51 cases)` beside the traced rc=1.

**F3 — the freeze manifest no longer describes the live frozen set.** At 14:03,
`freeze.json` pins vs live bytes:
`c1/measure.py` pin `77abe1e9` ≠ now `711507e7`;
`c2/measure.py` pin `ab3ae751` ≠ now `d6ca1d85`;
`contract.json` pin `ed6871e1` ≠ now `5de4f37b`.
`contract.json` lists 5 amendments; `freeze.json` lists 3 (missing 4 and 5).
`controls.sh`, `deciding-run.sh`, `no-harm.sh` still match. `freeze.json` itself
was rewritten again between 14:03 and 14:04 (sha256 `d1bb8c2aeb1c54a7...`, still
3 amendments and the same three stale pins), i.e. the manifest is being edited
while the wave runs. At HEAD itself the manifest is consistent (all six pins
match HEAD bytes), so gate 0 of `deciding-run.sh` passes for `FREEZE=631cd645`.

**F4 — `before/c2.stdout` was rewritten three times during the wave.** Observed:
139 B with `usable=12/13 total=19` at 13:47; 0 B at 13:50 (truncated in place);
139 B with `usable=13/13 total=18` at 13:59 (byte-identical to my run-2 verdict
line, sha256 `77721c4a33979a5b...`). A `cmp` taken mid-write reads a torn or empty
receipt. This seat's receipts are therefore compared against `git show
HEAD:...`, never against the mutable working-tree copy. Related: this seat's
scratch dir `/fast/scratch/hyaku/tameshi-r55/T55W1ExecCountersAtBase` was deleted
by an outside process at ~13:54 (only a directory created afterwards survived),
which cost run 1's artifacts; run 1's stream is retained as a harness-delivered
transcript (`c2-mine-run1.stdout.txt`, 2636 bytes; provenance in
`c2-mine-run1.provenance.txt`) and its failing arm is also visible in the
receipt JSON read before the wipe.

## Risks for integration (no fix attempted; frozen files are out of my scope)

1. **`FROZEN_UNCHANGED` will be 0 for any content revision that carries the
   current amended frozen bytes.** Simulated faithfully in a scratch fixture
   (`frozen-unchanged-simulation.txt`): fixture = `631cd64` + the four current
   live frozen files committed, then the exact `deciding-run.sh` line
   `git diff --quiet "$FREEZE" "$REV" -- $FROZEN` returns 1 →
   `FROZEN_UNCHANGED=0` → `rc=1` → `DECIDING_RUN_EXIT` nonzero. Gate 0
   (`FREEZE_INTEGRITY`) still prints `OK files=6 amendments=0` at `631cd64`.
   The L1 must either re-anchor the freeze pointer to a commit that contains the
   amended set *and* carry a `freeze.json` whose pins match it, or leave the
   frozen bytes untouched — and the latter is impossible to pass C2 with (F2).
   This needs an explicit L1 decision before the deciding run.
2. **`freeze.json` must be brought in line with `contract.json`** (amendments 4
   and 5 and the current pins); otherwise a reader who verifies the manifest
   against the worktree sees three MISMATCH rows.
3. **Any seat `cmp`ing against working-tree copies** of `before/*.stdout` can
   record a torn read (F4).
4. The working tree must be clean for `deciding-run.sh` (its
   `clean-tree-before.txt` gate). At my last read it carried other seats'
   uncommitted edits to 17 tracked files plus untracked wave files — expected
   mid-wave, but it must be resolved before the deciding run. This seat's own
   writes are confined to
   `.ufo/waves/round-55/w1/T55W1ExecCountersAtBase.{md,json}` and its receipts dir.

## Not done (deliberately)

No frozen file, counter, receipt-at-HEAD, or lane production file was modified;
no git/jj mutation was run in the lane (clones and one fixture commit live under
`/fast/scratch/hyaku/tameshi-r55/`, each asserted with
`git rev-parse --show-toplevel`). No tool was installed or upgraded this seat.
Census was run twice (13:51 and the final run saved as `census.out`):
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`
→ exit 0 both times, no error rows.

## Receipts

All under `.ufo/waves/round-55/w1/T55W1ExecCountersAtBase-receipts/`:

| file | content |
|---|---|
| `c1-mine.stdout`, `c1.stderr`, `c1-committed.stdout`, `c1-cmp.txt` | certified C1 run A, the committed receipt, and the byte comparison |
| `c1-derivations-rerun-amendment5.json`, `c1-rerun-amendment5.*` | later rerun under the drifted counter (labelled, not certified) |
| `c2-mine-run2.stdout`, `c2-mine-run2.stderr`, `c2-mine-run2.rc`, `c2-mine-run2.verdict` | certified C2 run (counter `d6ca1d85`) |
| `c2-committed.stdout`, `c2-committed-vs-mine.diff` | committed receipt and the three-region diff |
| `c2-mine-run1.stdout.txt`, `c2-mine-run1.provenance.txt`, `c2-run1-vs-run2.diff` | run under the freeze-pinned counter (`ab3ae751`), `total=19` |
| `c2-worktree-at-1359.stdout` | working-tree copy at 13:59, byte-identical to run 2 verdict |
| `diag-registry-check-usable.txt` | untraced `SELFTEST: PASS (51 cases)` |
| `premise-grammar-7.txt` | independent grammar arm for the seven self-tests |
| `frozen-unchanged-simulation.txt` | faithful fixture for the `FROZEN_UNCHANGED` line; gate-0 result |
| `timeline.txt`, `environment.txt`, `census.out` | chronology, versions, census |

Machine-readable summary: `T55W1ExecCountersAtBase.json`.

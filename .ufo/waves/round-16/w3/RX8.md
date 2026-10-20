# RX8 — cold-read re-read, page lines 1801-1808

Page: `git show 05a224754db3c6fce18f5ec1816a6873bffe3d0e:SKILL.md` — sha256
`e289acec4e90c994d303b2dd6c844d907dc1bf48330ecd2fd253ac7379f794b3` (verified; 1807 lines;
range 1801-1808 runs to EOF). Lane HEAD `05a2247` at start and at end; it was
clean except two untracked `.ufo/waves/round-16/*-residual.json` files not mine
(the shared working tree later gained uncommitted edits from other integration
work — not mine, and every tool run below used committed bytes only).

Read range only: line 1801 `### Round-16 gate/probe registry` plus the table
(lines 1802-1807). Preamble not in range.

All lane tools were executed from committed bytes extracted with
`git archive 05a2247 | tar -x -C /tmp/tameshi-r16w2-TameshiR16.RX8-lLquKM/wt`.
`--regression` resolves `FLEET_ROOT = dirname^3($SELF)`, so sibling repos were
made reachable with read-only symlinks at the scratch root (the extracted tree
has no `.git`). Lane/sibling repos were only read (`git show`, `git rev-parse`).

## Registry commands, exact as written, and observed exits

### `tools/mutate-and-run.sh` — gate — `--selftest` · `--regression`

| Invocation | Table | Observed | Key output |
|---|---|---|---|
| `bash tools/mutate-and-run.sh --selftest` | 0 pass | **0** | `MUTATE_SELFTEST: 83/83 pass` / `VERDICT: PASS` |
| `bash tools/mutate-and-run.sh --regression` | 0 PASS | **0** | `REGRESSION: PASS (cases=7 passed=7; ledger legs exact: killed-delta<=0 flips<=0)`; all seven legs exact: 80/80/60/40/47/70/50 % |
| `--regression` with one recorded table entry flipped (`TABLE_JS D2:KILLED`, scratch copy) | 1 FAIL | **1** | `REGRESSION_DEFECT js-kimi-census D2: measured=SURVIVED recorded=KILLED`; `REGRESSION: FAIL (cases=7 passed=6 failed=1 setup=0)` |
| `--regression` in a tree with no fleet siblings | 2 SETUP | **2** | `REGRESSION: SETUP (cases=7 passed=0 cannot-verify=7)`; each leg `revision not found` |
| `--bogus`, no args, `--target x`, `--regression --target x` | 64 usage | **64** each | usage text on stderr |

Leg pins verified against the pinned blobs: every `REGRESSION_PIN` sha256 equals
the constant in the script (kimi `83016d…`, surface `275d82…`, tsukuroi `084951…`,
mado `d7edaa…`, checklist `7e5ec9…`, claims `e9a21b…`, round-gate `f890e2…`); mode
`100755` mirrored where recorded.

### `.ufo/evidence/round-16/measure.py` — probe — `--rev REV` · `--selftest`

| Invocation | Table | Observed | Key output |
|---|---|---|---|
| `--rev 05a224754db3c6fce18f5ec1816a6873bffe3d0e` (default `--repo`) | 0 measured | **0** | JSON: `recorded_cases 7`, `depth_score 7`, seven `ledger_legs`, `shonen.marks ['~','~','~','~']`, `box3_ledger_link true`, `coldread.sections_total 54`, `ledger_present false`, `sources.rows 55`, `calibration_restraint_score 6` |
| `--rev nonexistent-rev` | 2 rev missing | **2** | `{"error": "rev-missing", …}` |
| `--rev HEAD --repo /tmp/definitely-not-a-repo` | 2 | **2** | repo-not-found |
| `--rev 40f8e1f…` (root commit) | 2 blob missing | **2** | `{"error":"blob-missing","missing":["tools/mutate-and-run.sh","corpus/SOURCES.md"]}` |
| no args; `--bogus` | 64 usage | **64** each | custom `UsageParser.error` → 64 |
| `--selftest` | 0 measured | **0** | `MEASURE_SELFTEST: 38/38 pass`; selftest itself asserts `exit64-no-rev`, `exit64-unknown-arg`, `exit2-bad-rev`, `exit2-blob-missing`, `exit2-no-repo` |

### `.ufo/evidence/round-16/coldread/assemble.py` — gate — `--selftest`

| Invocation | Table | Observed | Key output |
|---|---|---|---|
| `--selftest` | 0 covered | **0** | `SELFTEST: all checks passed` (including equal-rank override rejected exit 2, wrong-sha replace rejected exit 2) |
| no args | 1 uncovered | **1** | `coverage: 0/51 sections covered`; `ledger written … (0 entries)` — see finding A |
| one wrong-sha fake seat report | 1 report rejected | **1** | `REJECTED … skill_sha256 0000… matches no supplied skill file` |
| `--skill SKILL.md --skill SKILL.snapshot.md .ufo/waves/round-16/w{1,2}/*.md` | 0 if all covered | **1** | `coverage: 51/68 sections covered`; 21 REJECTED, 82 SKIPPED — correctly exit 1 because buckets are uncovered |
| `--bogus`; `--override` malformed JSON; `--override` valid JSON with invalid verdict | 2 usage / invalid override | **2** each | `ERROR: override file … stricter-mode entry needs a valid 'verdict'` |

### `.ufo/evidence/round-16/attribution/reattribute.py` — probe — `--selftest`

| Invocation | Table | Observed | Key output |
|---|---|---|---|
| `--selftest` | 0 passes oracle | **0** | `SELFTEST: PASS (new rule 8/8; old rule fails 5/8; old-rule fidelity 14/14)` |
| `--selftest` with a forced failing case (scratch copy) | 1 fails | **1** | `SELFTEST: FAIL (new rule failed 1 of 9; …)` |
| no args (correction mode) | 0 | **0** | `correction.json already exists with identical bytes; left unchanged`; 14 command rows, old rule reproduced every `observed_id` |
| `--bogus` | *(unlisted)* | **2** | argparse usage — see finding C |

**Every exit the table states for a listed command was reproduced exactly, on all
four rows.** The items below are adjacent defects found while executing.

## Findings

### A. `assemble.py` default report globs are one directory short (concrete defect; not a table-exit mismatch)

`DEFAULT_GLOBS` (`.ufo/evidence/round-16/coldread/assemble.py:60-63`) join
`HERE/../../waves/round-16/{w1,w2}/*.md`. From `HERE = .ufo/evidence/round-16/coldread`
that resolves to **`.ufo/evidence/waves/round-16/{w1,w2}`**, which does not exist
in the commit or in the live lane. The reports live at
`.ufo/waves/round-16/{w1,w2}` (68 and 67 files). Measured:

```text
GLOB …/coldread/../../waves/round-16/w1/*.md -> 0
GLOB …/coldread/../../waves/round-16/w2/*.md -> 0
os.path.isdir('.ufo/evidence/waves') -> False
actual w1 count 68
```

Consequence observed: a bare `python3 .ufo/evidence/round-16/coldread/assemble.py`
finds zero reports, prints `ledger written: …/ledger.json (0 entries)`,
`coverage: 0/51 sections covered`, and exits 1. Since `--out` defaults to
`ledger.json` next to the script (the Box3 target) and the write is an
unconditional `os.replace`, a bare run also replaces any existing ledger with the
empty one [overwrite path read at `assemble.py:1077-1083`; not exercised against
a non-empty ledger]. The registry's listed command (`--selftest`) is unaffected,
but the gate's actual round-16 assembly cannot work by default. Fix is one `..`:
`HERE/../../../waves/...`. With explicit report paths and both skill pins
(`--skill SKILL.snapshot.md --skill SKILL.md`) the tool behaves as tabled.

### B. `measure.py` row omits the failing-selftest exit 1 (minor, documentation)

The row's exits column (`0 measured · 2 rev/blob missing · 64 usage`) covers only
the `--rev` mode, yet `--selftest` is a listed command and its failure path
returns 1 (`selftest()` returns `0 if passed == len(checks) else 1`). Induced on a
patched copy: one broken expectation → `MEASURE_SELFTEST: 37/38 pass`, **exit 1**.
Compare row 1, which spells out `selftest 0 pass / 1 fail`; row 2 should say so.

### C. `reattribute.py` row omits the usage exit 2 (minor, documentation)

The row lists `0 corrected rule passes the oracle · 1 it fails`;
`python3 …/reattribute.py --bogus` exits **2** (argparse). Rows 1 and 3 both list
their usage exit (64 / 2), so the omission is inconsistent with the table's own
convention. The listed `--selftest` behavior (0/1) is exact.

### Agreement

- Row 1's five exit classes (selftest 0/1; regression 0/1/2/64) are all directly
  observed, including the FAIL and SETUP arms.
- Row 3's three arms are all observed: 0 (selftest), 1 (uncovered **and**
  rejected), 2 (argparse **and** invalid override).
- Row 4's 0/1 arms are observed; its correction mode reproduces
  `.ufo/evidence/round-16/attribution/correction.json` byte-identically.
- Row 2's 0/2/64 arms are observed; its 0 result is self-consistent with the
  committed page (54 sections, no ledger yet, seven depth legs).

## Residual risk / verification gaps

- The multi-skill real assembly run was done against the committed wave data
  (51/68 covered, exit 1). I did not read any other seat's report contents; only
  the tool's counts and its REJECTED/SKIPPED lines were used.
- The empty-ledger overwrite hazard is code-read, not exercised against an
  existing non-empty ledger.
- Tool installs: none.

## Verdict

The Round-16 registry's four rows are exit-accurate as written; one real defect
(assemble's dead default report globs) sits in the gate's unlisted default path,
plus two unlisted exit codes (measure selftest-fail 1, reattribute usage 2).

```json
{"seat":"TameshiR16.RX8","skill_sha256":"e289acec4e90c994d303b2dd6c844d907dc1bf48330ecd2fd253ac7379f794b3","sections":[{"start":1801,"heading":"### Round-16 gate/probe registry","class":"instruction","verdict":"gap-minor","blocking_gaps":[],"wrong_expectations":[],"minor_gaps":["assemble.py DEFAULT_GLOBS resolve to .ufo/evidence/waves/round-16/{w1,w2} (absent) instead of .ufo/waves/round-16/{w1,w2}; a bare run finds 0 of 135 reports, writes ledger.json with 0 entries, exits 1 (needs HERE/../../../waves)","measure.py --selftest exits 1 when a self-check fails (observed 37/38 pass -> exit 1); the row lists only 0/2/64","reattribute.py --bogus exits 2 (argparse usage); the row lists only 0/1"],"commands_executed":["git show 05a2247:SKILL.md | sha256sum -> e289acec… (match)","bash tools/mutate-and-run.sh --selftest -> 0 (MUTATE_SELFTEST: 83/83 pass, VERDICT: PASS)","bash tools/mutate-and-run.sh --regression -> 0 (REGRESSION: PASS cases=7 passed=7; legs 80/80/60/40/47/70/50%)","bash tools/mutate-and-run.sh --regression with TABLE_JS D2 flipped -> 1 (REGRESSION_DEFECT js-kimi-census D2 measured=SURVIVED recorded=KILLED; REGRESSION: FAIL cases=7 passed=6 failed=1)","bash tools/mutate-and-run.sh --regression with no fleet siblings -> 2 (REGRESSION: SETUP cases=7 passed=0 cannot-verify=7)","bash tools/mutate-and-run.sh --bogus | (none) | --target x | --regression --target x -> 64","python3 .ufo/evidence/round-16/measure.py --rev 05a2247 -> 0 (measured JSON)","python3 .ufo/evidence/round-16/measure.py --rev nonexistent-rev -> 2; --repo missing -> 2; --rev 40f8e1f -> 2 blob-missing","python3 .ufo/evidence/round-16/measure.py (no args) -> 64; --bogus -> 64","python3 .ufo/evidence/round-16/measure.py --selftest -> 0 (38/38)","python3 measure.py --selftest on a patched copy -> 1 (37/38)","python3 .ufo/evidence/round-16/coldread/assemble.py --selftest -> 0 (SELFTEST: all checks passed)","python3 .ufo/evidence/round-16/coldread/assemble.py (no args) -> 1 (0/51 covered; ledger.json 0 entries; default globs match 0 files)","python3 assemble.py --bogus -> 2; --override malformed JSON -> 2; --override invalid verdict -> 2","python3 assemble.py --skill SKILL.md --skill SKILL.snapshot.md .ufo/waves/round-16/w1/*.md .ufo/waves/round-16/w2/*.md -> 1 (coverage 51/68; 21 REJECTED; 82 SKIPPED)","python3 assemble.py --skill SKILL.md fake-seat.md -> 1 (REJECTED skill_sha256 0000…)","python3 .ufo/evidence/round-16/attribution/reattribute.py --selftest -> 0 (SELFTEST: PASS new 8/8; old fails 5/8; fidelity 14/14)","python3 .ufo/evidence/round-16/attribution/reattribute.py (no args) -> 0 (correction.json identical; 14 rows)","python3 .ufo/evidence/round-16/attribution/reattribute.py --bogus -> 2","python3 reattribute.py --selftest on a forced-fail copy -> 1 (SELFTEST: FAIL new rule failed 1 of 9)"],"opened":["SKILL.md@05a2247 lines 1801-1807","tools/mutate-and-run.sh",".ufo/evidence/round-16/measure.py",".ufo/evidence/round-16/coldread/assemble.py",".ufo/evidence/round-16/attribution/reattribute.py",".ufo/evidence/round-16/attribution/correction.json",".ufo/evidence/round-15/verification-3.json",".ufo/evidence/round-16/measure-repair/*.json (paths only)","git rev-list/merge-base metadata in tameshi-shokunin","path listings .ufo/waves/round-16/w1 and w2 (counts only; no report contents read)"],"scratch":"/tmp/tameshi-r16w2-TameshiR16.RX8-lLquKM"}]}
```

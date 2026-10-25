# RevSC43 — round-43 SCORECARD block cell-by-cell vs the three counters at the freeze

Seat: L1Tameshi43.RevSC43 (leaf member). Scope: the `## Round 43` block in
`SCORECARD.md` — for each claim row, whether the `Before` cell matches a committed
receipt, whether the `After` target string matches the counter's own printed
fields, and whether the `Counting command` runs as written. Falsification wave 2.

## Method (all runs in scratch clone `/tmp/tameshi-r43-w2-RevSC43-a`, `git clone --shared`,
counters byte-identical to the lane at the measured revs; no lane writes, no tools installed)

Permitted revs only: base `487b8f0da89fa0e2b8bea6930068accbf36e70a9` and freeze
`3aee2c078f8976499b587086af3577fc94dc8cf1` (the freeze of record named in the task; the lane
HEAD moved to `6b83a11c…` mid-audit — A11–A14 commits — and the block is being live-edited,
see §Findings 8–9). Never ran at `c5335c70…`.

Reproduced receipts (all in the scratch, exact commands):

| counter | rev | freeze | result |
|---|---|---|---|
| C1 `mutants/measure.py` | 3aee2c07 | 3aee2c07 | `C1_R43_PASS=true`, exit 0 |
| C1 | 3aee2c07 | 17f6ef0c (as written) | `self_pin=0 … C1_R43_PASS=false`, exit 1 |
| C1 | 487b8f0 | 3aee2c07 | `C1_R43_PASS=true mutants_killed=5`, exit 0 |
| C1 | 487b8f0 | 17f6ef0c | `self_pin=0 … C1_R43_PASS=false`, exit 1 |
| C2 `calibration/measure.py` | 3aee2c07 | 3aee2c07 | `m7=5 m8=3 total=8 C2_R43_PASS=false`, exit 1 |
| C2 | 487b8f0 | 3aee2c07 | `m12=2 m13=1 total=3 C2_R43_PASS=false`, exit 1 |
| C2 | 487b8f0 | 17f6ef0c | `self_pin=0` + same classes, exit 1 |
| C3 `guard/measure.py` | 3aee2c07 | 3aee2c07 | `C3_R43_PASS=true`, exit 0 |
| C3 | 3aee2c07 | 17f6ef0c | `self_pin=0 tool_sha_ok=0 … C3_R43_PASS=false`, exit 1 |
| C3 | 487b8f0 | 3aee2c07 | `tool_absent=1 C3_R43_PASS=false`, exit 1 |
| round-42 C2 counter `round-42/census/measure.py` | 487b8f0 | 322b5cd3 | `mutants_killed=4 C2_R42_PASS=false`, rc 1 — matches `before/c1-round42-at-base.stdout` |
| command D at 3aee2c07 | — | — | `recorded_cases=9 depth_score=9` |
| coldread monitor at 3aee2c07 | — | — | `calibration_restraint_score: 6` |
| `grep -cE '^ {0,3}\| S[0-9]{3} \|'` at 3aee2c07 | — | — | 114 (column-zero form also 114) |

Contracts/bytes: at `17f6ef0c` the contract pins C1 `ad7ecf8c…`, C2 `092c76cd…`, C3
`6278edcd…`; at `3aee2c07` C1 `0d0f81bd…`, C2 `97609511bb…`, C3 `ae66342d…`; counter bytes
at `3aee2c07` == HEAD `e20cf89` (sha-identical). Tool `tools/staged-id-guard.py` at
`17f6ef0c` = `8140945a8168…`; at `3aee2c07` = `2e8f2e891ea2…` (= contract `tool_sha256`).
`.ufo/evidence/round-43/after/` contains zero tracked files at `3aee2c07`.

## Findings, by severity

### 1. [HIGH] The `Counting command` cells pin a superseded freeze — all three rows fail
the predicate exactly as written at the freeze of record

All three counting-command cells (SCORECARD.md lines 2059–2061) append
`--freeze 17f6ef0c72ec27e1aea305b5c95806b43bb2caef` — the A2/A3-level freeze, which is
**not** the freeze of record `3aee2c07` (nor the freeze recorded in the contract at the records
commit, `114ffacd`). The counters read the contract and their own bytes at `--freeze`; at
`17f6ef0c` the contract pins pre-A4/A5 counter bytes, so the frozen counters (bytes
`0d0f81bd…`/`97609511bb…`/`ae66342d…`) fail self-pin.

Empirical (exact commands from the cells, only `--lane .` concretised):
- C1: `python3 .ufo/evidence/round-43/mutants/measure.py --lane . --rev
  3aee2c078f8976499b587086af3577fc94dc8cf1 --freeze 17f6ef0c72ec27e1aea305b5c95806b43bb2caef`
  → `self_pin=0 … C1_R43_PASS=false`, exit 1. The target `C1_R43_PASS=true exit 0` is not met.
- C2: same shape → `self_pin=0 … C2_R43_PASS=false`, exit 1.
- C3: same shape → `self_pin=0 tool_sha_ok=0 … C3_R43_PASS=false`, exit 1.
  (`tool_sha_ok=0` additionally because the 17f6-level contract pins the pre-A4 tool
  `8140945a…` while the rev tool is `2e8f2e89…`.)

With the correct pin (`--freeze 3aee2c07`), C1 and C3 reach their targets; C2 does not
(§Finding 3). So the cells are wrong in two ways: they name the wrong freeze, and they don't
reflect that the C2 target is not reached at the freeze.

### 2. [HIGH] The block's freeze narration is stale/wrong: "frozen at 17f6ef0c …
amendments A1–A3 are pre-data"

Line 2053–2054 says the contract is frozen at `17f6ef0c` and "amendments A1–A3 are pre-data".
The contract at the records commit `c5335c7` (the commit that carries the scorecard block)
already lists **A1–A9** and states the freeze of record is `114ffacd`; A4–A7 are "during wave 1"
and A8's own `why` exists to correct the stale narration. The current freeze of record is
`3aee2c07` (A10) and, in the live working tree, `6b83a11c` (A14). The sentence "before any
seat ran" is also false for A4–A14. The block's freeze identity and amendment count are
contradicted by the contract object it cites.

(At the time of writing the working-tree block has been updated to `6b83a11c` but still carries
the same "A1–A3 are pre-data" line — see Finding 8.)

### 3. [HIGH] C2 `After` target is contradicted by the frozen counter's own fields at the freeze

Line 2060: target `m6=0 m7=0 m8=0 m10=0 m11=0 m12=0 m13=0 total=0 C2_R43_PASS=true`, exit 0.
Running the frozen counter at the freeze prints:

```
C2_R43: self_pin=1 classes=7 m6=0 m7=5 m8=3 m10=0 m11=0 m12=0 m13=0 total=8
records=4 sources_rows=114 standing=114 C2_R43_PASS=false first=m7:corpus/lessons/round-43.md_unknown_S160
```

exit 1. Enumerated (patched counter run): m7 = `corpus/lessons/round-43.md` unknown S160,
S166, S256, S259 + `LOG.md#round-43` unknown S256; m8 =
`corpus/lessons/round-43.md:.ufo/waves/...`, `corpus/lessons/round-43.md:tools/*.py`,
`SCORECARD.md#round-43:.ufo/evidence/round-43/after/`. The lesson and LOG cites are in
`corpus/lessons/round-43.md:75,83-84,116,118,121,140,158` and `LOG.md:2243` (S256).

Because `c5335c7..3aee2c0` changes only the C2 counter/contract/guard (checked via
`git diff --name-status`), the records tree at the freeze is byte-identical to the records
commit — so the C2 target is also not reached at the records tree. No `after/` receipt exists
for it. The one document the scorecard itself cites in its Evidence cell
(`.ufo/evidence/round-43/after/`, empty at the freeze) is itself one of the m8 failures.

The counter-version note: at the base rev the same counter prints `m12=2 m13=1 total=3`
(Finding 5), so the claimed 0 is not reached at either permitted rev.

### 4. [MEDIUM-HIGH] C2 `Before` cell contradicts the committed final-counter base receipt

Line 2060 Before: `m12=1 m13=1 total=2 classes=7 C2_R43_PASS=false`, exit 1, at base. That
matches the committed receipt `.ufo/evidence/round-43/before/c2-at-base.stdout` (freeze
`f0f26367`). But the A10 amendment re-ran the base with the final counter and **committed the
new line beside it**: `.ufo/evidence/round-43/before/c2-at-base-A10.stdout` prints
`m12=2 m13=1 total=3` (first=`m12:**Planned_(round_43):**`). My rerun with the frozen counter
at base reproduces exactly `m12=2 … total=3`. The Before cell quotes the superseded receipt and
omits the final counter's value. (The contract's own `before_state` text has the same
staleness.)

### 5. [MEDIUM] Capability row pins the pre-amendment tool bytes

Line 2074: `tool tools/staged-id-guard.py @ 8140945a816873562eee8bcc6862d5e098f95b8083b4760b087812568f97b762`. That is the SHA of the tool at `17f6ef0c` (pre-A4/A7/A10). The frozen tool is `2e8f2e891ea20417c141e16871819182d5040c6f33916a435e9454a94d4d6ff2` (contract `tool_sha256`, and what the C3 counter validates). The row advertises bytes the counter refuses.

### 6. [MEDIUM] "Measured commit" and "Verdict" cells and Evidence dirs are dangling — no after subsection, empty `after/`

All three rows: `Measured commit = see the after subsection`; `Verdict = see the after
subsection`; Evidence includes `.ufo/evidence/round-43/after/`. The round-43 block contains no
"after the deciding run" subsection (the file ends at the sources-registry row), and
`.ufo/evidence/round-43/after/` is empty at the freeze and at HEAD (git ls-tree count 0; the
working-tree dir is empty). No deciding receipt exists for any of the three claims. (Round 42
has the precedent subsection with real receipts; round 43 does not.)

### 7. [LOW-MEDIUM] C1 `Before` cell is not reproducible by the row's own counting command

Line 2059 Before: `mutants_declared=6 mutants_killed=4` with both survivors named, exit 1, at
base, labelled "(round-42 counter)". That matches the committed receipt
`.ufo/evidence/round-43/before/c1-round42-at-base.stdout` and I reproduce it with the
**round-42** counter at base (rc 1). But the row's own Counting command at base
(`--rev 487b8f0 --freeze 3aee2c07`, with the correct freeze) prints
`mutants_killed=5 dead_code_only=1 C1_R43_PASS=true`, exit 0 — i.e. the row's Before cell
can't be produced by the row's Counting command, and the claimed before/after delta for C1
exists only across counter versions, not across revs (the tool is byte-identical at base and
freeze). The label "(round-42 counter)" is honest, but the row then presents a Before that its
own command contradicts.

### 8. [LOW] Prerun receipts committed as wave-1 evidence are stale for the freeze of record

`.ufo/evidence/round-43/prerun/c1-at-freeze.stdout` / `c3-at-freeze.stdout` are run at rev
`114ffacd` (pre-A8–A10) and print `live_collisions=6`, `selftest_cases=23` — the frozen
counter at the freeze prints `live_collisions=7`, `selftest_cases=24`, `held_refused=1`,
`live_held=3` (added by A7/A9). The C3 row's evidence pointer (`before/c3-at-base.stdout`,
`control/c3-constant-empty.stdout`) also excludes the A10 control re-run (`c3-constant-empty-A10.stdout`
differs: `expected_collisions=7` vs 6) and the A10 base C2 line. The committed evidence set is
a mixture of at least four counter generations.

### 9. [LOW] The block is being live-revised during this audit — the cited freeze pin is already moving

The lane HEAD advanced to `6b83a11c` (A14) while this seat ran; the working-tree block now
pins `6b83a11c` in the counting commands and `03a796c5…` in the capability row (matching the
A14 tool), but the frozen version of the block (at `3aee2c07` and at the records commit) pins
`17f6ef0c`/`8140945a…`. The internal consistency of the A14 freeze is verifiable by byte
comparison (contract pins at `6b83a11c` equal the counter bytes at that rev; tool SHA equals
the A14 tool) but the A14 revision is outside my permitted run revs, so its receipts are
unverified by me. The "A1–A3 are pre-data" sentence (Finding 2) is still present in the live
block.

## What is supported (no finding)

- C1 After target field names all exist in the counter output (`mutants_killed`, `dead_code_only`,
  `equivalent`, `unresolved`, `C1_R43_PASS`), and at the correct freeze the values match and
  exit is 0. Same for C3 (`C3_R43_PASS=true`, exit 0) and for C2's field names (all tokens
  print; values at the freeze do not match).
- C3 Before cell matches `before/c3-at-base.stdout` and reproduces exactly.
- The numeric-axes sentence (lines 2064–2067) holds at the freeze of record: command D = 9/9,
  coldread monitor = 6 at `3aee2c07`; however its cited receipt (ExecCommandD) ran at
  `17f6ef0c`, not at the freeze of record.
- The sources-registry row's count command `grep -cE '^ {0,3}\| S[0-9]{3} \|'` → 114 at the
  freeze, matching the row and the counter's `sources_rows=114` (m6=0).

## Residual risk / verification gaps

- I did not run any counter at `c5335c7` (prohibited) or at `6b83a11c` (outside permitted
  revs); the C2 failure at the records tree is established by the `c5335c7..3aee2c0` diff
  showing records byte-identical.
- `sources-census.sh validate` was not run (fleet-root tool; row claim taken on the counter's
  m6/m13 output and the grep count).
- Peers are concurrently editing w1 reports, the contract, and the lesson; any of findings
  1–2, 5, 8 may be partially mitigated by in-flight A11–A14 re-runs, but the committed
  scorecard block at the freeze of record contains all of them.

— L1Tameshi43.RevSC43

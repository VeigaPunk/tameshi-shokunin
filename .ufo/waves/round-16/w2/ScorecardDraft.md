# ScorecardDraft — tameshi round 16, wave 2 (falsify: depth + calibration)

**Verdict:** partial. C1 depth 6→7 **holds** (measured at committed `c699c8c`). C2 calibration 6→8 **falls as a claim** at `c699c8c`: measured 6→6, and 8 is blocked by (a) no committed `coldread/ledger.json` and (b) a `measure.py` box-3 detection defect that would keep C2 at 6 even with a complete ledger. Both reproduced below.

All numbers come from committed blobs (`git show REV:path`) or committed evidence. Nothing in the lane working tree was measured.

## Draft: `## Round 16` section (for SCORECARD.md)

```
## Round 16 — js-round-gate mutation case and cold-read ledger (wave 2 draft)

C1 depth moves 6→7. C2 calibration stays 6→6 at the measured commit; the
candidate 8 is pending the ledger and a counter repair (not claimed).
No stagnation waiver, retirement or promotion credit.

| Claim | Axis / type | Falsifiable before → after | Score delta | Measured evidence |
|---|---|---|---|---|
| C1 seventh recorded mutation case (kumitate round-gate.mjs) | depth; capability | recorded legs 6→7; 10 pre-registered predictions held 10/10; kill-rate 5/10 (50 %) | 6→7, delta+1 | `tools/mutate-and-run.sh` leg line 91; `.ufo/evidence/round-16/round-gate/sweep/results.tsv`; `.ufo/evidence/round-16/round-gate/runner-regression.txt` (`REGRESSION: PASS (cases=7 passed=7`) |
| C2 cold-read full-page ledger (box 3) | calibration; capability | box3 credited 0/54 → full-page 54/54 with complete ledger | PENDING: 6→6 measured; candidate 8 NOT claimed | `coldread total 54 covered 0`; `box3_ledger_link False` at `c699c8c`; see defects D1–D2 |

Counting command, both revisions:
`python3 .ufo/evidence/round-16/measure.py --rev REV`, exit 0 each.
Before `7650fe4db89f3a706aed63d048ac47e02289cc72` (round-15 measured end);
Pre-registration `e69b488f65b17bcfd41949abf7d538a77678dc26` (predictions committed before the sweep).
After `c699c8c36d6e4eca4b796b81a8247904aa145ec8` (wave-1 content commit).
Measured commit for the C2 ledger: `<PENDING: ledger commit>`.
Integrating commit that carries this section: `<PENDING: L1 integration commit>`.

Measured values (exit 0 each):

| Rev | recorded_cases / depth | calibration_restraint | coldread covered / total | box3_ledger_link | sources rows (A/B/C; mined/queued/rejected; malformed) |
|---|---|---|---|---|---|
| 7650fe4 | 6 / 6 | 6 | 0 / 51 | False | 49 (42/5/2; 22/24/3; 0) |
| e69b488 | 6 / 6 | 6 | 0 / 51 | False | 49 (42/5/2; 22/24/3; 0) |
| c699c8c | 7 / 7 | 6 | 0 / 54 | False | 55 (47/6/2; 28/24/3; 0) |

Round-15 table values for 7650fe4 are unchanged; this draft does not restate them as new.

| Axis | Round16 lane verdict | Bound |
|---|---|---|
| depth | improved, 6→7 | seventh distinct target (kumitate `scripts/round-gate.mjs`, pin `364f1d5`, blob sha `f890e277…3d9`) |
| calibration | unchanged, 6 | ledger absent at measured commit; box-3 counter defect (D1) |
| coverage | no-harm monitor | sources +6 rows (S052–S057), malformed 0; no admitted-knowledge claim |
| operability | no-harm monitor | runner changed (+108/−24); committed selftest and regression at runner sha `89722dd…` |
| freshness | unchanged | round-gate pin at `364f1d5`, kumitate HEAD `1770305`; no successor sweep |
| adjacency | unchanged | sibling repos read-only; kumitate status clean |

Next claim: C2 8 only after (a) `coldread/ledger.json` committed covering all 54 post-repair sections, and (b) the box-3 link check reads continuation lines. Neither prerequisite is present at `c699c8c`.
```

## Evidence

### Commands and exits

| Command | Exit | Key output |
|---|---|---|
| `git show c699c8c…:SKILL.md \| sha256sum` | 0 | `3d8a1edb1803441cfef4ce46447af51a6b857644d8f5347b2aad7c612bbcb7a4` (matches page sha) |
| `python3 <scratch>/measure.py --rev <REV> --repo <lane>` for REV ∈ {c699c8c, e69b488, 0baf52e, 9f2c86f, 7650fe4, a9cf4da} | 0 each | outputs `out-<rev>.json` in `/tmp/tameshi-r16w2-ScorecardDraft-Dyx3i2/` |
| `python3 measure.py --selftest` | 0 | `MEASURE_SELFTEST: 33/33 pass (scratch /tmp/tameshi-r16-CRMeasure-ntr2191t)` |
| scratch `measure.py` sha256 vs `git show c699c8c:.ufo/evidence/round-16/measure.py` | — | both `dc3483609d14a8efb768e25fb5d8a72ac6cf37dca512536269e42afe14abfd5e` (identical) |
| `git cat-file -e c699c8c:.ufo/evidence/round-16/coldread/ledger.json` | 128 | `path … does not exist`; coldread dir holds only `SKILL.snapshot.md`, `assemble.py` |
| `git show e69b488:SKILL.md \| sha256` | 0 | `97cf436b…`, equals `SKILL.snapshot.md` (51 sections) |
| `git show c699c8c:SKILL.md` section count (measure `sectionize`) | — | 54 sections |
| kumitate `git rev-parse --short HEAD` | 0 | `1770305` |
| kumitate `git show 364f1d5…:scripts/round-gate.mjs \| sha256` | 0 | `f890e277…` = pin in `predictions.json` and `runner-regression.txt` |
| `git --no-optional-locks -C kumitate status --porcelain` | 0 | empty |
| `git log -1 --format=%cI e69b488` | 0 | `2026-10-20T10:39:59-03:00` (= 13:39:59Z) |
| sweep `MUTATE_DATE` (`sweep/sweep.log`) | — | `2026-10-20T13:40:15Z` (after pre-registration) |

No tools were installed or updated.

### Key output lines

- c699c8c: `recorded_cases 7 depth 7 legs [..., 'js-round-gate']`; `shonen ['~','~','~','~'] box3_link False box3_points False`; `coldread total 54 covered 0 full False ledger_present False`; `restraint 6`; `sources {'rows': 55, 'malformed': 0, 'tiers': {'A': 47, 'B': 6, 'C': 2}, 'status': {'mined': 28, 'queued': 24, 'rejected': 3}}`.
- e69b488 and 7650fe4: `recorded_cases 6`, `restraint 6`, `coldread total 51 covered 0`, sources `rows 49`.
- Sweep (`.ufo/evidence/round-16/round-gate/sweep/results.tsv`): KILLED A1, A3, B1, E3, C1060; SURVIVED C1059, A2, B2, CKIND, E1. Matches the ten `predict` labels in `defects.tsv` → 10/10; killed 5/10.
- Regression (`.ufo/evidence/round-16/round-gate/runner-regression.txt`, committed record, not re-run here): `REGRESSION_TOOL … sha256=89722ddb…5594`, `REGRESSION_CASE js-round-gate: PASS`, `REGRESSION: PASS (cases=7 passed=7; ledger legs exact …)`.
- Selftest record (`runner-selftest.txt`): 81 `PASS` lines, 0 `FAIL`; runner sha `89722ddb…` (`runner-sha256.txt`) equals `git show c699c8c:tools/mutate-and-run.sh \| sha256sum`.

### Simulation for defect D1 (scratch only, not a seat verdict)

In `/tmp/tameshi-r16w2-ScorecardDraft-Dyx3i2/sim-*`: committed `SKILL.md`, `SHONEN.md`, runner, `SOURCES.md` from `c699c8c`, plus a synthetic complete ledger (one `executed-ok`/`instruction`/`commands=1` entry per section, sha from `measure.sectionize`). This tests only the counter, not the cold-read's content.

| Variant | covered | box3_points | restraint |
|---|---|---|---|
| SHONEN.md as committed (box line `:9`, link on continuation `:10`) | 54/54 full | False | **6** |
| same file with continuation joined onto box line | 54/54 full | True | **8** |

### Defects

- **D1 (blocking for C2 = 8).** `measure.py:62` `BOX_RE = ^- \[([x~ ])\] (.*)$` captures only the box line. `measure.py:262` `box3_link = … BOX3_LINK in boxes[2][1]`. `SHONEN.md:9` is the box, `SHONEN.md:10` carries `.ufo/evidence/round-16/coldread/ledger.json`. So `box3_ledger_link` is always False on the committed layout. The self-test fixture `SHONEN_BOX3` (`measure.py:310`) is a single line, so 33/33 passes while the real file fails.
- **D2 (blocking for C2 = 8).** `coldread/ledger.json` absent at `c699c8c` (`ls-tree` shows only `SKILL.snapshot.md` and `assemble.py`). The counter reports `covered 0 / 54`.
- **D3 (not blocking, note).** The cold-read was against `SKILL.snapshot.md` (sha `97cf436b…`, 51 sections, equal to `e69b488:SKILL.md`). `c699c8c:SKILL.md` is `3d8a1edb…` with 54 sections. Any ledger must cover the post-repair section shas, not the snapshot shas.
- **D4 (observation, uncommitted sibling work).** The lane working tree has an uncommitted `.ufo/evidence/round-16/measure.py` edit (+36/−2) whose docstring says it fixes the continuation-line block; `measure-repair/` holds `old-tool-at-c699c8c.json` and `repaired-tool-at-c699c8c.json`. That agrees with D1. I did not measure it: the contract requires committed bytes. The owner must verify the repair at a committed revision.
- **D5 (minor, record wording).** The case-7 note `corpus/knowledge/mutation-case-kumitate-round-gate.md` cites tool sha `75ed934d…adc5` as "unchanged at the sweep". That is correct for the sweep time (`sweep.log` `MUTATE_TOOL … 75ed934d`). The committed runner is now `89722ddb…` (leg 7 added at `c699c8c`). Readers should use the regression record for the current sha.

### Per-axis checks

- depth: `ledger_legs` gains `js-round-gate` only; the other six legs are unchanged, and the target is a distinct file. No re-measured or duplicate case.
- calibration: four `[~]` marks unchanged between `e69b488` and `c699c8c`; no `[x]` added.
- coverage: `corpus/SOURCES.md` 49→55 rows, malformed 0; census only, no admission claim.
- operability: runner diff `tools/mutate-and-run.sh` 108 insertions / 24 deletions between `e69b488` and `c699c8c`. Committed selftest and regression records match the current sha. I did not re-run them.
- freshness: round-gate pin `364f1d5` is a recorded pin, not HEAD (`1770305`). No successor sweep is claimed.
- adjacency: kumitate status clean; `c699c8c` evidence cites read-only status.

### Capability row candidates (not admitted; `AXES.md` requires a demonstrated run)

1. **pre-registered mutation predictions** — `predictions.json` committed in `e69b488` (`2026-10-20T10:39:59-03:00`) before the sweep (`MUTATE_DATE 13:40:15Z`); 10/10 held. Candidate row, pending the integrator's acceptance.
2. **cold-read full-page counter** — NOT ready. It runs and its selftest passes (33/33), but on the committed repo it reports `covered 0/54`, and D1 keeps box 3 at 0 even with a complete ledger. Do not add a row until D1 and D2 are fixed and the real-repo count is non-zero.
3. The seventh regression leg is depth, not a capability; it does not enter the capabilities table.

### Lane working tree (not measured)

`git --no-optional-locks status --porcelain` in the lane shows modified `.ufo/evidence/round-16/measure.py`, `.ufo/waves/round-16/w1/Overlap1.md`, `corpus/lessons/round-16.md`, and untracked round-16 directories. All my numbers come from committed blobs (`git show`), so none of this affects the figures above.

### Out of scope / not done

- No re-execution of the 7-leg regression or the sweep (committed records only; RerunRegression seat owns that).
- No edits to lane files, no commits, no git add, no messages sent.
- No `REA` MCP, no omp CLI, no agent.db access.
- Tool installs: none.

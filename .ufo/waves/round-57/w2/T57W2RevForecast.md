# T57W2RevForecast — cold-read forecast vs measured drift (round 57, wave 2, seat T57W2RevForecast)

Item: compare the heading list of `tools/cold-read-forecast.py` with the MEASURED drift of the
round-21 cold-read monitor at C0, report precision/recall, name every heading the forecast missed
or invented and why, and stage the fix.

Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, base `5e3569969b532310d2b8a3d130901757a3df356b`,
C0 `ca75c2674645ab6bdadeecb8584007c74342bfa9`. Nothing in the lane was edited. The staged fix is at
`.ufo/waves/round-57/w2/T57W2RevForecast/stage/tools/cold-read-forecast.py` (the L1 installs it);
the `diff -u` against the shipped tool is `.../T57W2RevForecast-receipts/cold-read-forecast.patch`.
The wave-3 reader list is `.../w2/T57W2RevForecast.json`.

## Headline

**The shipped forecast tool is exactly calibrated on this round's actual change set: 18 forecast
headings vs 18 measured, precision 1.00, recall 1.00, symmetric difference empty.** No heading is
missed and none is invented. That is the answer to the calibration question the round asked.

**But the tool's calibration is a coincidence of this round's shape, not a property of the tool.**
Three defects in the shipped `--diff-to` mode are demonstrated below with fixture commits: it
**misses** a heading added at the target rev, it **invents** headings removed at the target rev, and
it **crashes** (exit 1, Python traceback) when SKILL.md is deleted at the target rev. None of the
three fires on C0 — C0 edits two existing SKILL.md sections and adds and removes no heading — so
the round's number is right. The defects will fire on the next round that reshapes SKILL.md, which
is exactly what wave 3's re-key does.

Measured ground truth: **base 64/64 covered, score 8; C0 46/64 covered, score 6**; the 18
uncovered headings at C0 are the reader list wave 3 must re-key.

## The measurement (the ground truth)

Both monitor runs are in `.../T57W2RevForecast-receipts/` (`monitor-base.explain.json`,
`monitor-c0.explain.json`), full `--explain` JSON.

```console
$ export HYAKU_SCRATCH=/fast/scratch/hyaku
$ S=$HYAKU_SCRATCH/tameshi-r57/T57W2RevForecast; mkdir -p "$S"
$ git clone --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin "$S/clone"
$ git -C "$S/clone" checkout --detach 5e3569969b532310d2b8a3d130901757a3df356b
$ TMPDIR="$S" python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/coldread/measure.py \
      --repo "$S/clone" --rev 5e3569969b532310d2b8a3d130901757a3df356b --explain > "$S/measured-base.txt"
$ git -C "$S/clone" checkout --detach ca75c2674645ab6bdadeecb8584007c74342bfa9
$ TMPDIR="$S" python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/coldread/measure.py \
      --repo "$S/clone" --rev ca75c2674645ab6bdadeecb8584007c74342bfa9 --explain > "$S/measured-c0.txt"
```

| rev | sections_covered | sections_total | score | uncovered_headings |
|---|---|---|---|---|
| base `5e35699` | 64 | 64 | 8 | 0 |
| C0 `ca75c26` | **46** | 64 | **6** | **18** |

Base is fully covered, so every one of the 18 uncovered headings at C0 is a genuine loss of
credit, and the wave-3 reader list is exactly those 18 (none was already uncovered at base).

**Independent validation of the tool's credit rule** (receipt
`independent-credit-rule-check.txt`): the forecast tool's *own* re-implementation of the credit
rule, evaluated at a rev, equals the frozen monitor at that rev — **at base 0 uncovered = 0, and
at C0 18 uncovered = 18 with all 18 reason sets identical (18/18)**. The tool is not guessing the
monitor's behaviour; it reproduces it exactly. That is what makes the staged fix below sound:
measuring the target rev with the tool's rule is measuring what the monitor would read.

## The forecast (three invocations, all at the base rev)

```console
$ T=/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/cold-read-forecast.py
$ python3 "$T" --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
      --rev 5e3569969b532310d2b8a3d130901757a3df356b \
      --diff-to ca75c2674645ab6bdadeecb8584007c74342bfa9 --json
$ python3 "$T" --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
      --rev 5e3569969b532310d2b8a3d130901757a3df356b \
      --paths .ufo/evidence/round-57/coldread-referent-r56.md SKILL.md corpus/QUALITY.md corpus/README.md \
               corpus/SOURCES.md corpus/knowledge/gate-row-exit-map.md corpus/knowledge/receipt-revision-binding.md \
               corpus/lessons/round-57.md tools/cold-read-forecast.py tools/fixtures/receipt-gate/accept.receipt \
               tools/fixtures/receipt-gate/drift.paths tools/fixtures/receipt-gate/drift.receipt tools/registry.json \
      --json
$ python3 "$T" --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
      --rev 5e3569969b532310d2b8a3d130901757a3df356b --paths <same 13 paths> \
      --skill-section '## Standing rules' --skill-section '### Gate/probe registry' --json
```

The 13 paths are exactly `git diff --name-only base C0` (receipt `commands` in the receipts
README). Outputs: `forecast-original-diffto.json`, `forecast-original-paths.json`,
`forecast-original-paths-skill-sections.json`.

| invocation | forecast headings | measured | precision | recall | missed | invented |
|---|---|---|---|---|---|---|
| `--diff-to C0` (retrospective) | 18 | 18 | **1.00** | **1.00** | none | none |
| `--paths <13 files>` (as assigned) | 17 | 18 | 1.00 | 0.944 | `### Gate/probe registry` | none |
| `--paths <13> --skill-section '## Standing rules' --skill-section '### Gate/probe registry'` | 18 | 18 | **1.00** | **1.00** | none | none |

**Every heading the forecast missed and every one it invented, with the why:**

- **Missed (one, only in the bare `--paths` invocation): `### Gate/probe registry`** (SKILL.md
  L1541). Reason: `--paths` mode prices a SKILL.md edit ONLY through an explicit
  `--skill-section`/`--skill-lines`. Without one, the tool reports SKILL.md as `UNPRICED` and
  exits 2 with `FORECAST_UNPRICED: SKILL.md is read directly by the monitor and pinned by no
  entry; its cost cannot be forecast (pass --skill-section/--skill-lines)`. The heading IS lost at
  C0 — its SKILL.md text changed (the `receipt-revision gate` registry row was appended), so its
  own sha256 no longer matches any ledger entry (`no-ledger-entry` in the monitor's words). The
  tool's own exit code and note say the number is incomplete; the number it prints (17) is a
  floor, not the cost. **This is the tool behaving as documented, not a bug** — but it is the
  difference between 17 and 18 for a caller who does not read the note, and the fix below makes
  the retrospective mode exact so the note is not needed.
- **Invented: none**, in any of the three invocations.
- The 17 headings the bare `--paths` invocation does report are all correct (no false positives),
  and their reasons (`input-drift:<path>`) are a strict subset of the monitor's per-section reason
  strings — the tool names only the entries that *credited at base* and now fail, while the
  monitor lists every failing entry including ones already stale at base (the noise wave-1's scout
  flagged: `tools/env-diff.py`, `tools/registry-check.py`, `corpus/knowledge/service-limits.md`).

**Per-path attribution** (`--diff-to C0`, `by_path`): `corpus/SOURCES.md` 12, `tools/registry.json`
10, `corpus/QUALITY.md` 5, `corpus/README.md` 5 — the same four content paths wave-1's per-path
probes found, plus the two SKILL.md section edits (`## Standing rules` L17 and
`### Gate/probe registry` L1541) that the drift itself prices as `section-sha-void`.

**Anchor shift: none.** C0 edits SKILL.md by 4 lines added / 4 removed (`git diff --numstat`), so
the file keeps 2214 lines and every `###`/`##` heading keeps its base line number (verified: base
and C0 both have 63 heading lines, 0 shifts). The tool's "line-count change shifts later `:NNN`
anchors" caveat does not bite at C0, so the 18 headings' line numbers are valid in both revs and
wave 3 can cite them as-is.

## The three defects (the sweep, with the commands and their outputs)

The sweep is `.../T57W2RevForecast-receipts/fixture-sweep.sh`; its raw output is
`.../fixture-sweep.stdout`. Each fixture is a clone of the lane at base with ONE fixture commit
(`git -C "$D" -c user.name=fixture -c user.email=fixture@example.invalid commit`), and the monitor
(the ground truth), the SHIPPED tool and the STAGED tool are each run against it.

| # | fixture (one commit on base) | monitor (ground truth) | SHIPPED `--diff-to` | STAGED `--diff-to` |
|---|---|---|---|---|
| fx1 | a new `###` heading appended to SKILL.md | 64/65 covered, uncovered `### Brand new section added by round 57` | **readers 0 — MISSES the heading** | readers 1, reason `no-ledger-entry` |
| fx3 | the trailing `###` section deleted from SKILL.md | 63/63 covered, **0 uncovered** | **readers 1 — INVENTS `### Round-26 gate/probe registry`** | readers 0 |
| fx4 | a mid-file `###` section deleted from SKILL.md | 62/62 covered, **0 uncovered** | **readers 2 — INVENTS `### Round-13 gate/probe registry` and `## Effective expectation reconciliation — round 14`** | readers 0 |
| fx2 | SKILL.md deleted | (the target rev cannot be measured) | **exit 1, Python traceback** (`KeyError: 'SKILL.md'`) | exit 2, `COLDREAD_FORECAST_COULD_NOT_EVALUATE` |

**Root cause (one sentence).** The shipped `--diff-to` mode never evaluates the monitor at the
target rev. It simulates: it takes `git diff --name-only`, treats every changed path as a drifted
pin, and voids every SKILL.md section whose sha256 is not in the target's sha set
(`tools/cold-read-forecast.py:583-588`). A heading **added** at the target has no base entry to
void and no base pin to drift, so it is invisible; a heading **removed** at the target has a base
sha that is (correctly) absent from the target's set, so it is mis-voided as if it had been
edited; and `tree_modes(repo, other)[SKILL][1]` at line 587 raises `KeyError` when SKILL.md is
absent at the target.

The shipped mode therefore cannot answer the question it is named for ("what does the monitor
read at REV2?") — it answers a proxy question that happens to agree with the monitor when the
change set only *edits* existing text and adds/removes no headings. C0 is such a change.

## The staged fix

`diff -u tools/cold-read-forecast.py <staged>` is in
`.../T57W2RevForecast-receipts/cold-read-forecast.patch` (225 lines). It makes `--diff-to` MEASURE
the target rev with the tool's own (already monitor-faithful) credit rule instead of simulating:

- new `section_uncovered` / `uncovered_sections` / `entry_causes` / `diff_forecast`;
- `run()`'s `--diff-to` branch builds a second `Model` at the target rev and calls
  `diff_forecast`, so the lost set is exactly "uncovered at target, minus already-uncovered at
  base" — the monitor's own definition;
- a section edited at the target → `section-sha-void`; a section **added** at the target →
  `no-ledger-entry` (both cost one reader); a section **removed** at the target → not lost (it is
  gone from the page);
- `target_rev` / `target_covered` / `target_sections_total` are reported so the output states
  what was measured;
- `render()` prints the target's section count as the denominator;
- the ledger path stays `UNPRICED` (if the ledger itself changes, the credit SET changed and
  cannot be diffed this way);
- four new selftest cases (added heading, removed heading, deleted SKILL.md, target-measured
  counts) and four fixture commits in `build_fixture`.

The `--paths` (planning-time) mode is **unchanged** — it is the mode that answers "if I edit these
paths, what happens", which is what the round wanted at planning time, and the wave-1 planning
forecast it produced was correct.

### Verification of the staged fix

```console
$ python3 .../stage/tools/cold-read-forecast.py --selftest
FORECAST_SELFTEST: 20/20 pass          # shipped tool: 16/16 (its own 16 cases still pass)
$ python3 .../stage/tools/cold-read-forecast.py --lane LANE --rev base --diff-to C0 --json
FORECAST: paths=13 headings=18 readers=18 of 64     # == the monitor's 18
```

- **Against the C0 measurement:** patched `--diff-to C0` → 18 headings, missed ∅, invented ∅,
  precision 1.00, recall 1.00, `target_covered 46 / 64` — the monitor's numbers exactly. The
  patched tool's reason strings for all 18 headings are a strict subset of the monitor's measured
  per-section reason strings (checked programmatically: `fr_norm <= mr` for every heading).
- **Against the four fixtures:** the table above — every defect gone.
- **Mutants (4 single-edit mutations of the staged tool, each killed by the new selftest):**
  added-heading-not-lost → 19/20; removed-heading-counted-as-lost → 19/20;
  measure-base-instead-of-target → 17/20; SKILL-deleted-silent-fallback → 19/20. The unmutated
  staged tool: 20/20.
- **The shipped tool fails the new cases** (proving the fix is real, not cosmetic): OLD on the
  `added` fixture → exit 2 (it cannot express the answer); OLD on the `removed` fixture → 1 lost
  heading; OLD on the `noskill` fixture → exit 1 with a traceback.
- **No regression in the mode the round used** (receipt `regression-paths-and-w1rows.stdout`):
  - `--paths` mode (the planning mode) is **byte-identical** between the shipped and the staged
    tool on all four content paths: SOURCES 13 headings, registry.json 11, QUALITY 6, README 6 —
    the same headings in the same order in both.
  - **Wave-1's two retrospective calibration rows re-run with the staged tool give the same
    numbers as wave 1 reported and as the shipped tool gives**:
    `0a2010a → 21eb3c6` → readers 18, base covered 64, 0 already-uncovered (wave-1: "forecast 18 |
    monitor 18 uncovered — yes, 18/18 heading texts, symmetric difference empty");
    `21eb3c6 → c013745` → readers 0, base covered 46, 18 already-uncovered (wave-1: "base 46 −
    0 new = 46"). The patch therefore does not change any number wave 1 published.
  - Selftest: shipped 16/16, staged 20/20 (receipt `selftest.stdout`).

**Not changed, and why.** The bare `--paths` invocation's 17-vs-18 gap is *documented behaviour*:
the tool prints `FORECAST_UNPRICED` and exits 2 precisely because it cannot know which SKILL.md
section a planned edit will land in. Making `--paths` guess would be worse than saying so. The
staged fix removes the need to guess by making the retrospective mode exact.

## Wave-3 reader list

`.../w2/T57W2RevForecast.json` — `{lost: [18 headings], reasons: {heading: reason}}`. The 18
headings are the measured uncovered set at C0 (not the forecast's), so wave 3 re-keys exactly what
the monitor does not credit. `reasons` carries the **C0-attributable** cause per heading (the
subset of the monitor's reason string attributable to C0's own edits), not the monitor's raw
string — the raw strings carry pre-existing stale-entry noise (e.g. `input-drift:tools/env-diff.py`
for a path C0 never touched) that wave 1's scout warned the re-key must not copy.

Two headings are `section-sha-void` (SKILL.md text changed at C0: `## Standing rules` L17,
`### Gate/probe registry` L1541); the other 16 are `input-drift` on the four content paths
`corpus/SOURCES.md`, `corpus/README.md`, `corpus/QUALITY.md`, `tools/registry.json`.

## Residual risk and verification gaps

- **The calibration number is verified only for C0's change shape** (text edits to existing
  sections + four drifted content paths). The four fixtures cover added/removed/deleted SKILL.md
  headings, but not: a changed ledger (the tool refuses, exit 2 `UNPRICED`), a changed trace
  receipt, a changed `SHONEN.md` box (the score, not the credit set), or a changed monitor script
  (the tool refuses, exit 2). Those paths are priced as UNPRICED, loudly, and are not verified
  here.
- **The patched `--diff-to` mode is verified against the monitor at C0, at four fixtures, and on
  wave-1's two published calibration rows** (both reproduced identically by the shipped and the
  staged tool — see the regression receipt). The round-55 / round-56 rows quoted in
  `T57W1ExecForecast.md` are the only retrospective rows wave 1 published; the third row it quotes
  (the "one appended line to QUALITY/SOURCES/README" row) names a clone commit `4182777` that
  **is not present in the lane repo** (`git rev-parse --verify 4182777` fails), so that row
  cannot be re-run and is unverified here.
- **The monitor's `external_inputs` labels are not verified by the monitor** (see
  `.ufo/evidence/round-57/coldread-referent-r56.md`): 13 of 18 round-56 bound entries carry a
  stale `corpus/SOURCES.md` label. The monitor ignores those labels; the forecast ignores them
  too. They do not affect this measurement, but they do mean the *ledger's* recorded labels are
  not self-consistent — the wave-3 re-key should re-record them.
- **Live-lane reads**: the monitor accepts a live-lane read when the file is a blob at REV with
  the recorded sha256. The forecast's `live_bound` mirrors that. Both the C0 measurement and the
  fixtures ran against the same live lane, so a drift in the live lane's working tree between
  the two runs would change the two numbers together; the measurement was taken with the lane
  clean except `corpus/routed-defects.json` (uncommitted, and pinned by no entry — the scout
  measured that path as costing 0 headings).
- **`tools/cold-read-forecast.py` itself is a NEW path at C0** (absent at base), so it is `NEW`
  and costs 0 headings; the same for the three `tools/fixtures/receipt-gate/*` files, the two
  `corpus/knowledge/*` files and `corpus/lessons/round-57.md`. The round-21 ledger pins none of
  them, so a future round that pins them will start pricing them.

## Honesty

- Commands and their outputs: every number above comes from a receipt in
  `.../T57W2RevForecast-receipts/` (the sweep script and its complete stdout, `fixture-sweep.stdout`, from a run with no deadline; plus `independent-credit-rule-check.txt`, `regression-paths-and-w1rows.stdout`, `selftest.stdout`).
- The monitor ran in the sweep for fixtures fx1, fx3 and fx4 (the sweep prints each measurement), plus the base and C0 runs. fx2 has no measurable target (SKILL.md absent). Every monitor run exited 0. Exploratory monitor runs made while developing the fixtures are not receipts and are superseded by the sweep.
- The wave-1 planning forecast (`--paths` with the 10 planned paths and the two planned SKILL.md sections; `forecast-w1plan.json`) gives 18 headings, the same 18 the monitor measured at C0.
- The sweep script asserts `git -C "$D" rev-parse --show-toplevel` equals the fixture dir before
  every commit, and commits only with `-c user.name=fixture -c user.email=fixture@example.invalid`
  and `-C "$D"`. No mutating git command ran in the lane or the fleet repo; the lane's only
  additions are my seat's stage and receipts directories.
- Scratch under `/fast/scratch/hyaku/tameshi-r57/T57W2RevForecast`.
- **No tools installed or upgraded** (none needed; python3 + git from the host).

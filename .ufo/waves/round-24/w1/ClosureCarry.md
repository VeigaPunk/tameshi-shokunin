# ClosureCarry — round23 routed items mapped to round24

**Verdict.** Round24 has a concrete mechanism for 9 of the 11 items routed by the
round23 closure (`MANIFEST.json` `rounds[421].notes`, line 11562): 5 carry a frozen
predicate, 1 is implemented but sits outside the predicate denominator, and 3 are
partial. One item (`loose stdout tokens`) has **no round24 record at all**; one
(`dead-falsifier coverage gap`) is handled only as a criterion. No routed repair is
falsely claimed fixed. The ruler target is now executed: `after.json` (untracked at
inspection) records **11/11, exit 0** at `c8c5b88` with the frozen ruler digest,
corroborated by `RunRulerAfter.md`; `noharm-c8c5b88.json` records the round21
monitor at **62/62, restraint 8, depth 8, overrides false, missing []**, and
registry **47/47 held, superseded 7**. The remaining record defect is that both
receipts and the wave's seat reports are **untracked**: they are not in the
delivered revision's tree, so any closure that cites `c8c5b88` must land them or
cite them explicitly as post-revision evidence. The only intermediate on record is
the disclosed harm (`monitor-intermediate-A.json`: 47/62, restraint 6 at
`bd38c02`), now superseded by the 62/62 final.

Axes: A1 routed-item coverage, A2 traceability (path:line per disposition),
A3 calibration honesty (tested vs trusted; no overclaim). This item is read-only; it
makes no move on any axis and changes no production file.

## Mapping (11 routed items)

Routed list verbatim: `MANIFEST.json:11562`; the any-vs-all ruler defect is at
`MANIFEST.json:11553` ("survives the ten-case ruler (single-token fixtures) but is
killed by selftest all-of-tokens").

| # | Routed item | Round24 disposition | Evidence | Status |
|---|---|---|---|---|
| 1 | argv swap-name / name-insensitive | K1 + fixture `argv-swapped-between-names` | `.ufo/evidence/round-24/extra-cases.json:7`; `measure.py:27-31` (mutant), `:107-137` (substitute/pin not used by K1; selftest path in `mutant_rows:62`); `before.json` K1 anchor 1, exit 0, no FAIL line at base | **Predicated** (after 11/11) |
| 2 | negative-exit mutants | K3 + `negative-exit-mismatch` and `negative-exit-declared-match` | `extra-cases.json:276,343`; `measure.py:32-33`; `before.json` K3 anchor 1, exit 0, no FAIL line at base | **Predicated** |
| 3 | `bundle_sha256` pins in frozen registry rows | K5/K6; three round23 rows superseded, two active pinned successors | `tools/registry.json:928-990`; literals `3d6c99b7…` and `db620668…` equal `sha256sum` of the two round23 bundles; `before.json` K5/K6 `control true / substituted true` (defect reproduced at base) | **Predicated** |
| 4 | runner `held` / `cleanup` / `external` in replay projection | `project()` refuses `cleanup_error`, refuses `held is not True`, lists `external`/`non_hermetic_argv`; K7/K8/K10 | `tools/registry-replay.py:86-101`; `measure.py:172-184`; actual replay `.ufo/evidence/round-24/replay/live-dependent.json` = `pin-disposition-read`, `verify-round15` | **Predicated** |
| 5 | hash clone runner copy | `run_replay()` hashes and imports the clone copy | `registry-replay.py:162-166`; `observations.json` `runner_sha256_clone_copy cba16646…` = `git show d2eaecd:tools/registry-check.py \| sha256sum` | **Implemented, not predicated** (knowledge entry: "recorded per run, not a ruler predicate") |
| 6 | fleet-root realpath | `plan()` realpath-normalises repo, fleet root and siblings; K11 | `registry-replay.py:63-69`; `measure.py:186-201`; `observations.json.plan` has canonical fleet root and siblings | **Predicated** |
| 7 | bounded streams | `--max-stream-bytes` + `STREAM_LIMIT`; K9 | `registry-replay.py:92-97,175`; `measure.py:175` | **Partial** — see F2: the bound gates publication, not retention |
| 8 | loose stdout tokens | No round24 artifact names them; old rows and tokens unchanged | Examples still active: `repeat-control-selftest` → `SELFTEST: PASS`; `witness-metadata-check` → `metadata_consistent`; new pinned rows' first token is the loose `"finding_ids": []` (`registry.json:971-990`) | **No round24 record** (round23 adjudication's no-retrofill is the only stated reason) |
| 9 | multi-token stdout fixture in the ruler | K4 kills the any-vs-all mutant by running the selftest, which loads round23 `all-of-tokens` | `round-23/extra-cases.json:1356`; `measure.py:34-35`; ruler's own `obs()` has one token (`measure.py:148`, K9 at `:175`); round24 fixtures: 0 multi-token cases (scanned) | **Property closed by delegation / literal ruler fixture absent** |
| 10 | re-run guard sweep | K1-K4 re-mutate argv/exit/stdout; cwd/revision/membership/duplicate are re-covered by the round23 ten-case ruler re-run at `c8c5b88` (10/10), and their guard code is byte-identical | `git diff -U0 6a1821a..c8c5b88 -- tools/command-binding.py` changes only selftest lines 164-169; `RunR23Ruler.md` = 10/10 exit 0, tool sha `9230c68…`; `after.json` K1-K4 `exit 1` with one FAIL each | **Partial** — ruler re-run receipted; guard-weakening mutants for the other four not repeated (transfer by byte-identical `evaluate()`) |
| 11 | dead-falsifier coverage gap | QUALITY48 criterion + lesson Mistakes row + this wave's re-dispatch | `corpus/QUALITY.md:489-500`; `corpus/lessons/round-24.md:53`; `spec1.json` items PredK1-11, Mut*, Code*, Rev*; seat reports landing under `.ufo/waves/round-24/w1/`, no accounting file yet | **Criterion-only** (gap named; re-dispatch in flight, no completion accounting yet) |

Extras beyond routing, harmless: K2 case-fold and fixtures `argv-padded-token`,
`argv-repeated-flag` (`extra-cases.json:74,141,208`) harden stripping and
de-duplication, which routing did not name. They add no new claim.

All five "Predicated" rows are discriminated in `after.json` at `c8c5b88`
(11/11, exit 0, frozen-ruler digest) and in `RunRulerAfter.md`; that run was
produced by the wave's RunRulerAfter seat, not by this item. The superseded
`command-binding-selftest` row now holds false (it expects 38/38; the tool prints
44/44) while `noharm-c8c5b88.json` reports 47/47 active rows held, superseded 7 —
the designed append-only supersession, and the reason K5/K6's control set excludes
superseded rows.

## Fresh falsification (concrete)

**F1 — the ruler still cannot fail on a token-dropping projection.**
All ruler-owned fixtures use exactly one `stdout_contains` token
(`measure.py:148`, K9 at `:175`); round24's fixture file has zero multi-token cases
(programmatic scan; only round23 `all-of-tokens` has two). K7-K10 assert finding IDs,
bundle existence and `live_dependent`; they never compare the published bundle's
requirements to the input. Counterexample: change
`registry-replay.py:101` to `requirements.append({**requirement, 'expect': {**requirement['expect'], 'stdout_contains': requirement['expect'].get('stdout_contains', [])[:1]}})`
— the published bundle binds a weaker expectation while K7-K11 stay green and K4
still kills the gate mutant. Not a present false result: the retained round24 bundle
does carry 7 multi-token requirements (observed). It is a sufficiency gap in the
routed remedy, not in today's output.

**F2 — "bounded streams" bounds publication, not retention.**
`run_replay` builds rows from `run_row(..., retain_streams=True)` and writes
`observations.json` at `registry-replay.py:183` **before** `project()` checks
`--max-stream-bytes` at `:184`. Counterexample: `--run --max-stream-bytes 16` with a
row emitting 64 KiB still writes the full 64 KiB (and any secret in it) to
`observations.json`; only the bundle is refused. The routed defect was "retained
without size bounds or redaction"; the knowledge table's row ("unbounded retained
streams" → "refuses with STREAM_LIMIT") conflates the two.

**F3 — loose-token disposition is missing from round24.**
No round24 artifact (contract bounds `contract.json:60-65`, knowledge Bounds, SKILL
round24 section, SCORECARD) carries the no-retrofill decision; only
`fresh-adjudication.json` does. This matters because a frozen row can still pass on a
source read — the exact point Replay26 made about `MEASURE_SELFTEST:`. The decision
is correct; the record is absent.

**F4 — QUALITY48 and the eighth repair disagree.**
QUALITY48 (`corpus/QUALITY.md:489-500`) says a routed gap "does not count as
repaired until a frozen predicate for it fails at the base revision and holds after
the change." The hash-clone-runner-copy repair is implemented
(`registry-replay.py:162-166`) and verified equal to the rev blob, but it has no
predicate and the knowledge entry says so explicitly. Under the new criterion it is
therefore not repaired; under the round's narrative it is. Also, the 1/11 → 11/11
delta is 10 new kills (K4 pre-existing control) and K5/K6 exercise one mechanism
(digest pin) on two rows — 9 new discriminating mechanisms, not 11. State that, or
QUALITY48 needs a recorded carve-out.

**F5 — the after and no-harm receipts exist but are untracked.**
`after.json` (11/11, exit 0, revision `c8c5b88`, `instrument_sha256 0a7f6daa…` =
the frozen ruler) and `noharm-c8c5b88.json` (monitor 62/62, restraint 8, depth 8,
overrides false, missing []; registry 47/47 held, superseded 7) are in the working
tree, produced by the wave's executors and corroborated by `RunRulerAfter.md`.
Neither is tracked: `git status --porcelain` shows both as `??`, so the tree at
`c8c5b88` still contains no measured after and no final monitor. A closure that
cites `c8c5b88` for 11/11 or no-harm would be citing post-revision, uncommitted
evidence. `corpus/lessons/round-24.md:53` ("recorded below once executed") and
`SCORECARD.md:1145` still forward-reference results that are not in the committed
text. This is a record defect, not a measurement defect: the observations are now
executed.

**F6 — the round24 replay pair is not pinned by any registry row.**
`grep "round-24/replay" tools/registry.json` → none. The routed "regenerated bundle
plus regenerated expected would still hold" pattern was fixed for the two round23
bundles only; the new 43-row bundle (`4f4240…`) has a digest in its expected file
but no repeatable row. No false green (there is no row), just no coverage. Adding a
row now would change the frozen replay baseline, so this is a next-round item.

## Commands observed (read-only; nothing executed beyond inspection)

- `python3 -c` JSON parse of `MANIFEST.json`: `rounds[421]` = round 23; notes
  `:11562`, rechecks `:11553`.
- `sha256sum .ufo/evidence/round-24/measure.py` = `0a7f6daa…` = `before.json`
  `instrument_sha256`; ruler is the committed frozen file.
- `sha256sum` round23 replay bundle = `3d6c99b7…`; source-read bundle = `db620668…`
  (both match `registry.json:971-990` literals); round24 bundle = `4f4240…` (matches
  `replay/expected.json` and `replay-gate.json` stdout).
- `git show d2eaecd:tools/registry-check.py | sha256sum` = `cba16646…` =
  `observations.json.runner_sha256_clone_copy`; `registry-replay.py` = `9fcd2dbb…`
  and `command-binding.py` = `9230c68…`, matching `replay-command.json`,
  `replay-gate.json` and the live tree (c8c5b88 did not change tools or registry).
- `git diff -U0 6a1821a..c8c5b88 -- tools/command-binding.py`: only lines 164-169
  (fixture loader); `evaluate()` unchanged.
- Fixture scan: round24 multi-token cases = `[]`; round23 = `["all-of-tokens"]`.
- Registry dump: 3 superseded + 4 active new rows; 0 active tokens ≤6 chars; loose
  examples above.
- `observations.json`: 43 rows, 2 external (`pin-disposition-read`,
  `verify-round15`), 0 rows missing `held`, max stdout 8 110 B.
- `after.json`: `discriminated 11 / total 11`, `exit 0`, `revision c8c5b88…`,
  `instrument_sha256 0a7f6daa…`; K1-K3 `restored_exit 0`, K5/K6
  `control true / substituted false`, K7-K11 `discriminated true`. Same result in
  `.ufo/waves/round-24/w1/RunRulerAfter.md`.
- `noharm-c8c5b88.json`: monitor `sections_covered 62 / 62`, `missing []`,
  `calibration_restraint_score 8`, `depth_score 8`, `overrides_used false`,
  `trace_gate strict`; registry `held 47`, `superseded 7`, `exit 0`. Both files are
  untracked (`git status --porcelain` → `??`).
- `RunR23Ruler.md`: round23 ten-case ruler at `c8c5b88` = 10/10, exit 0, control
  exit 0 with empty findings, `tool_sha256 9230c68…`.
- No tool installed or updated. No ruler, selftest, gate or battery executed
  (this item has no "Run"). Only this report was written.

## Smallest safe correction (for the L1)

1. Commit `after.json`, `noharm-c8c5b88.json` and the wave seat reports (or a
   manifest pinning their digests) before the closure cites 11/11 or no-harm, and
   replace the two forward references (`lessons/round-24.md:53`,
   `SCORECARD.md:1145`) with the committed paths. The measured values themselves
   need no correction: 11/11 and 62/62 hold at `c8c5b88`.
2. Record the three partials in the round24 report/lesson bounds (not in the frozen
   ruler, whose sha `0a7f6daa…` is the before receipt): multi-token discrimination
   is delegated to round23 `all-of-tokens`; `--max-stream-bytes` gates publication,
   not retention; cwd/revision/membership/duplicate transfer by byte-identical
   `evaluate()`, receipted by the round23 ten-case ruler re-run (10/10).
3. Add one bounds bullet naming the frozen loose-token rows and no-retrofill.
4. Add one sentence to QUALITY48's scope or the contract bounds: the runner-digest
   repair is recorded per run and sits outside the predicate denominator — or it is
   not counted repaired.
5. Route to round25: a two-token `obs()` fixture plus a bundle-fidelity assertion in
   the ruler; truncation/redaction at retention time; an optional pinned row for the
   round24 replay pair.

## Bounds

Read-only mapping; no execution of the ruler, selftests, registry battery or replay
by this item. "Predicated" means the mechanism and fixture exist and the base row
shows the defect; the after kill is read from the retained `after.json` and
`RunRulerAfter.md`, not produced here. K4 is a pre-existing control; K5/K6 share one
mechanism. No producer authentication, promotion, historical R17-CMD-BIND closure or
numeric score uplift is claimed.

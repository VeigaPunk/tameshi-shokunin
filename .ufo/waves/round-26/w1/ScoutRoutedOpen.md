# ScoutRoutedOpen — routed item 4, second part (state of three carried-open groups)

Seat: `TameshiR26.ScoutRoutedOpen` (leaf scout, no subagents). Judged on: calibration.
Head examined: `a08e85c5d7f899e8a5992e20517edb1a380d79eb` (base `d4140796`). Read-only throughout:
`GIT_OPTIONAL_LOCKS=0 git` only, no `jj` command anywhere, no clone, no gate, selftest or sweep.
Line numbers are bytes at `a08e85c`; the working tree matched that revision for every file cited below
(`git diff --stat a08e85c -- <cited files>` empty at read time).

## Verdict

**All three groups are open at `a08e85c`: 14/14 re-attack FINDING rows, 3/3 round-24 spot-check items 2–4,
and the SiblingOverlap provenance gap.** Nothing in `c9ff09f..a08e85c` repairs any of them. Among `tools/`,
that range touches only `mte-interop.py`, `mutate-and-run.sh` and `registry.json` (+20 lines, two appended
`mte-interop` rows, 54 → 56), and none of the three groups' subject files appears in it. This agrees with the
lane's own routing text at `corpus/lessons/round-25-verifier-spotcheck.md:200-203`, which lists the same three
groups as "still open", and with round-26's C2 bound (`contract.json`: "items 4 and 5 of the same routing are
dispositioned in the lesson and report, not counted").

"Open" here means: the row's status is unchanged, and the substrate the finding attacks is byte-unchanged from
the revision the finding audited. I did not re-execute any of the 14 counterexamples this session, so "open"
is a byte/state fact, not a fresh demonstration (see Unknowns).

## (a) The 14 re-attack FINDING rows — one line each

State locus: `.ufo/evidence/round-25/dead-falsifier-disposition.json`, `"status": "reattacked-finding"` at the
line given. Seat line = status − 2; report line = status + 1; one 7-line object per row. The status values were
derived from each report's verdict token by `.ufo/evidence/round-25/build-disposition.py:37`, and the round-25
non-author spot-check re-checked 34/34 tokens (`corpus/lessons/round-25-verifier-spotcheck.md:47`); I did not
re-derive all 14 tokens this session.

1. `TameshiR25.ReOutputComplete` — **OPEN** — `dead-falsifier-disposition.json:31`; report `w1/ReOutputComplete.md:3`; subject `tools/registry-replay.py:176-184` (full stdout/stderr written to `observations.json` at `:183` before `--max-stream-bytes` is applied in `project()` at `:184`).
2. `TameshiR25.ReReplay02` — **OPEN** — `dead-falsifier-disposition.json:52`; report `w1/ReReplay02.md:3`; subject `tools/registry.json:24` row `repeat-control-snapshot-mismatch`, expect at `:32-34` is `{"exit": 1}` alone.
3. `TameshiR25.ReReplay06` — **OPEN** (calibration class) — `dead-falsifier-disposition.json:80`; report `w1/ReReplay06.md:7`; subject `tools/registry.json:106`, expect `:116-119` adds `"unavailable": 0`, which the cited source `registry-baseline.json:123` does not state.
4. `TameshiR25.ReReplay10` — **OPEN** — `dead-falsifier-disposition.json:108`; report `w1/ReReplay10.md:61`; subject `tools/registry.json:252` row `evidence-disposition-round18`, stdout-only expect (`evaluate()` `tools/command-binding.py:111`).
5. `TameshiR25.ReReplay13` — **OPEN** — `dead-falsifier-disposition.json:129`; report `w1/ReReplay13.md:9`; subject `tools/registry.json:350`, expect `:358-361` is an unanchored `context_consistent` substring.
6. `TameshiR25.ReReplay14` — **OPEN** — `dead-falsifier-disposition.json:136`; report `w1/ReReplay14.md:3`; subject `tools/registry.json:372`, expect `:383-386` is an unanchored `missing_injected_environment` substring.
7. `TameshiR25.ReReplay15` — **OPEN** — `dead-falsifier-disposition.json:143`; report `w1/ReReplay15.md:5`; subject `tools/registry.json:397`, expect `:408-410` is `{"exit": 1}` with no `stdout_contains` for a 14-way shared exit code.
8. `TameshiR25.ReReplay18` — **OPEN** — `dead-falsifier-disposition.json:164`; report `w1/ReReplay18.md:5`; subject `.ufo/evidence/round-23/replay.py:66-71` (receipt projection keeps `held`/`cleanup_error` out) and `tools/registry.json:462`.
9. `TameshiR25.ReReplay19` — **OPEN** — `dead-falsifier-disposition.json:171`; report `w1/ReReplay19.md:5`; subject `tools/registry.json:483`, expect `:493-496` accepts a revision label with no evidence the measured commit matches.
10. `TameshiR25.ReReplay20` — **OPEN** — `dead-falsifier-disposition.json:178`; report `w1/ReReplay20.md:5`; subject `tools/registry.json:508`, expect `:515-518` pins only `MEASURE_SELFTEST:` (case count free).
11. `TameshiR25.ReReplay25` — **OPEN** — `dead-falsifier-disposition.json:192`; report `w1/ReReplay25.md:8`; subject `tools/registry.json:614`, expect `:621-624` pins only `SELFTEST: PASS` (case count free).
12. `TameshiR25.ReReplay27` — **OPEN** — `dead-falsifier-disposition.json:199`; report `w1/ReReplay27.md:5`; subject `tools/registry.json:692` (`source: "SKILL.md@98bea7d:1806"`), and `git ls-tree -r --name-only 98bea7d -- .ufo/evidence/round-17/coldread/assemble.py` prints nothing.
13. `TameshiR25.ReSchemaPriority` — **OPEN** (LOW) — `dead-falsifier-disposition.json:220`; report `w1/ReSchemaPriority.md:3`; subject `tools/command-binding.py:83` (`DUPLICATE_REQUIREMENT` depends on requirement order; exit 2 in both orders), with the report's adjacent A1 at `w1/ReSchemaPriority.md:68`.
14. `TameshiR25.ReWaveAccounting` — **OPEN** — `dead-falsifier-disposition.json:241`; report `w1/ReWaveAccounting.md:3`; subject `tools/registry.json:896-898` (`wave-accounting-frozen-entry` still pins the round-22 bundle) and the death basis in `.ufo/waves/round-23/original-outcomes2.json`.

All 12 registry-row subjects report `status=active` and no `superseded_by` at `a08e85c`; the two rows round-26
appended (`:1001`, `:1011`) are `mte-interop` rows and supersede none of them.

## (b) Round-24 spot-check routing items 2–4 — one line each

Source: `corpus/lessons/round-24-verifier-spotcheck.md` (header `:61`, items 1–5 at `:63-67`; item 1 is round-26's
neighbour, not this item's target).

1. **Item 2, `:64` — OPEN.** No registry row references `.ufo/evidence/round-24/` or a round-24 ruler/replay bundle (`registry.json` 56 rows, `grep -c 'round-24'` = 0); MutPins outcomes survive only in `.ufo/waves/round-24/w1/MutPins.md:75-80` (four "survives direct --only", two "internally inconclusive"), and `git grep -i mutpins a08e85c -- .ufo/evidence/round-26 .ufo/waves/round-26` returns nothing.
2. **Item 3, `:65` — OPEN.** `tools/registry-replay.py` is byte-identical `d2eaecd..a08e85c` (`git diff --quiet` exit 0), still carries the promise block at `:7-20`, and has no consumer-entrypoint marking; its only registry row remains `registry-replay-selftest` at `registry.json:991-993`.
3. **Item 4, `:66` — OPEN.** No file the item names changed: `registry-replay.py` identical (above), round-24 replay evidence untouched (`git diff --stat c9ff09f a08e85c -- .ufo/evidence/round-24/` empty, so `replay/live-dependent.json` and the bare `revision` string at `.ufo/evidence/round-23/replay.py:66` stand), and the one stale locator the lane already re-found is still live at `registry.json:692` (see (a) row 12).

## (c) SiblingOverlap provenance sentence — one line

**OPEN** — locus `.ufo/waves/round-25/w1/SiblingOverlap.md:15` ("keys the file by basename only and carries no
lane, revision or pin"), mechanism drawn at `:178-182`; at `a08e85c` the `leg_report` body is byte-identical to
`c9ff09f` (`diff` of the extracted function → `IDENTICAL leg_report body`), its return at
`tools/mte-interop.py:160-162` emits only `schemaVersion`/`thresholds`/`framework`/`files` with a basename key
at `:139`, and none of the 8 committed `*.mte.json` files contains `"config"` (`git grep -l '"config"' a08e85c
-- '*.mte.json'` → 0). The ninth leg's interop changes are emitter-level selftest cases and a status map, not
provenance.

## Commands and observed output (all read-only, `GIT_OPTIONAL_LOCKS=0`)

- `git diff --stat c9ff09f a08e85c -- tools/` → `mte-interop.py | 189 +…`, `mutate-and-run.sh | 116 +…`, `registry.json | 20 +++`; 3 files, 258 insertions, 67 deletions.
- `git show a08e85c:tools/registry.json | jq '.rows|length'` → 56; same at `c9ff09f` → 54; `git diff c9ff09f a08e85c -- tools/registry.json | grep '^+'` → the two `mte-interop` rows at `:1001`,`:1011`, both `source: "...round-25-verifier-spotcheck.md:189-192 (routed item 1)"`.
- `jq -r '.rows | to_entries[] | select(.value.status=="reattacked-finding") …'` over the disposition file → 14 rows, seats as listed.
- `git show a08e85c:tools/registry.json | jq` over the 12 attacked names → all `active`, `superseded_by` unset.
- `git diff --stat c9ff09f a08e85c -- .ufo/evidence/round-23/ .ufo/evidence/round-24/` → empty.
- `git log --oneline a08e85c -- .ufo/evidence/round-25/dead-falsifier-disposition.json .ufo/waves/round-25/w1/ReReplay02.md` → `77302fa` only.
- `git ls-tree -r --name-only a08e85c | grep -c '\.mte\.json$'` → 8; `git grep -l '"config"' a08e85c -- '*.mte.json' | wc -l` → 0.
- `git ls-tree -r --name-only 98bea7d -- .ufo/evidence/round-17/coldread/assemble.py` → no output, exit 0.

## Smallest safe correction

None to production bytes. The integrator's only safe move is to keep the existing routing text and not credit
closure: refresh `corpus/lessons/round-25-verifier-spotcheck.md:200-203` only if the three groups are re-worded,
and do not read round-26's two new registry rows as item 2 of round-24 — they are sourced to
`round-25-verifier-spotcheck.md:189-192` (the `mte-interop` registration defect), a different item on a
different routing. If a future wave closes any row, the smallest honest edit is that row's `status` plus a
successor registry row, never a rewrite of a historical report.

## Unknowns and bounds

- **Not re-executed.** No mutant, selftest, gate or sweep was run; the 14 findings' counterexamples were not
  re-demonstrated. I verified only that their substrates are byte-unchanged, so a finding whose counterexample
  was already invalid at `c9ff09f` would still read as "open" here. Re-attack reports disagree on severity
  (row 13 marks itself LOW), and I did not re-adjudicate severity.
- **Round-26 wave artifacts** (`.ufo/waves/round-26/`) do not exist at `a08e85c` (`git ls-tree` empty); a later
  commit could close any of these, so this verdict is scoped to that revision.
- Tooling: no installs or upgrades; `git`, `jq`, `diff`, `grep` as already present. Scratch:
  `/tmp/scout-routed-open/` only (pinned-file copies and one `registry.json`); nothing written outside this file.

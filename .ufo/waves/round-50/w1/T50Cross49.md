# T50Cross49 — C1 independent cross-coding, round-49 spot-check (wave 1)

Seat: T50Cross49 (independent cross-coder). Scope: items R49.1..R49.6 of
`.ufo/evidence/round-50/c1/defects.json`. Coded at base `e3729de862f73ae080d98fcf522a7081ce16e40a`.

Method: read the frozen defect set and the round-49 verifier spot-check's routed list, then
resolved each item against the lane tree at the base (scratch clone, `git -C $S/lane show
e3729de:<path>`). Read full text of each item in
`corpus/lessons/round-49-verifier-spotcheck.md` (Routed defects items 1-6). No T50Disp*.* file
was read; the C1 counter was not run (rules read from its docstring only). No tool installs
(none needed).

Key structural fact: for every R49 item, `routed_at` == the round-50 base `e3729de` (the
spot-check commit itself). A `fixed` row requires the keyed excerpt to be ABSENT at `routed_at`
and the fix commit to be a descendant of `routed_at` (measure.py `fixed_bad` check). Therefore no
R49 item can be `fixed` at the base by construction; the only honest dispositions are `open` and
`declined`. All six are coded `open`: each ask is unmet in the base tree and there is no
≥40-character decline reason on record.

## Findings (file:line; commands)

### R49.1 — generator error paths (unreadable guard / F2 / F3) — **open**
- `tools/pbt-staged-id.py:982-984` (`git show e3729de:tools/pbt-staged-id.py | sed -n '980,986p'`):
  `main()` still checks only `if not os.path.isfile(guard):` then `return
  _setup_error('guard is not a regular file: %s' % guard)`. An unreadable regular file passes
  `isfile`; there is no `os.access(guard, os.R_OK)` pre-check.
- `tools/pbt-staged-id.py:771-778`: `run_guard` catches only `subprocess.TimeoutExpired`
  (line 773) and `(ValueError, UnicodeDecodeError)` (line 777) — no `OSError` around
  `subprocess.run`. The F1 path (python3 -I exits 2 with empty stdout → `json.loads(b'')` →
  `answer=None` → violation, exit 1) is intact.
- F2 (uncaught mid-run `dump.write`/`write_text` OSError, lines 803-806 region) and F3
  (`os.makedirs(case_dir …)` before the try/finally, lines 790-791 vs 815-817) are unchanged.
- No selftest case covering an unreadable guard exists (`--selftest` runs the oracle/classifier
  without the guard, line 842 comment). `T49W2RevGenCode.md` (the source of F1-F3) exists at
  base. Ask unmet.
- Doubt checked: the docstring documents the *observed* 1-for-refused-analysis — but it still
  promises exit 2 for an unreadable guard, and the fix asked for (exit 2 + selftest case) is not
  in the tree.

### R49.2 — counter blind spots (successor counters) — **open**
- No successor counters exist at base: `git -C $S/lane ls-tree --name-only e3729de
  .ufo/evidence/` lists round-12..round-49 only (no `round-50/`).
- The round-49 C1 counter still implements the uncapped, evidence-free `absent` class:
  `.ufo/evidence/round-49/c1/measure.py:23-24` (a path pointer that does not resolve passes with
  a `absent` row), `:274-276` (`res['absent'] += 1` with no cap and no evidence requirement).
- The round-49 C2 counter still only checks generator presence/pristine run/panel confirms
  (`.ufo/evidence/round-49/c2/measure.py` head), i.e. it cannot tell a property-based generator
  from a differential one — exactly the blind spot the item asks a successor counter to close.
  Ask unmet (the ask explicitly says "not prose").
- Doubt checked: the round-49 lesson (corpus/lessons/round-49.md:79, 125) describes the successor
  plan in prose — prose is not the counter.

### R49.3 — outside-section stale sentences (SKILL.md 1503/1509/1555) — **open**
- `SKILL.md:1503` still claims the selftest namespace "`/tmp/tameshi-r12-*`" in the round-12
  repeat-control registry row (overlaps `/tmp/tameshi-r12-controls-UNIQUE`; round-49.md:125).
- `SKILL.md:1509` still reads "deepens one recorded case, never a seventh independently measured
  gate." and `SKILL.md:1555` "No registry row changes rank, SHONEN authority, or the six recorded
  cases." — the two true-but-stale sentences the round-49 closure routed (round-49.md:79).
- All three lines are byte-unchanged at base; no correction or re-pin exists. Ask unmet.
- Doubt checked: line 1508 already acknowledges the runner pin is stale at round 27 — that is a
  different, older edit; the three routed lines themselves are untouched.

### R49.4 — standing axis table — **open**
- The newest standing axis table at base is the round-48 one:
  `SCORECARD.md:2355` reads "| calibration | 6 | …" (round-48 content revision, "48
  (restated)"). No restated table with round-49 values (calibration 8, depth 9, freshness 9)
  exists; the round-49 section states "calibration 8 (was 6)" only in prose. Ask (append a
  restated standing table) unmet.
- Doubt checked: the round-31 table (line 1537) also states "calibration | 8" but is a dated
  historical literal, not a round-49 restatement; the ask targets the standing table that is
  newest (round-48), which still says 6.

### R49.5 — carried round-48 items — **open**
- Round-48 spot-check routed defect 4 carried: dead `brace_depth_at` helpers, round-47 counter
  survivors, S205/F7 candidates, six-leg regression ledger decision, located-name check,
  append-only rule.
- At base the two dead helpers are still present: `tools/tally-audit-v2.py:135-136` and
  `tools/tally-audit-v3.py:234-235` (`def brace_depth_at(text, offset):`) — standing sha-pinned
  rows unchanged. `SCORECARD.md:2410` (**Planned (round 50)**) still lists "carried items from
  round 48's list". Compound item: one unmet ask ⇒ open.
- Doubt checked: even if a sub-item (six-leg decision, located-name check) had landed, the
  brace_depth_at ask alone is unmet, so the item cannot be fixed.

### R49.6 — SHONEN — **open**
- `SHONEN.md:5-12`: all four boxes remain `[~]`, each with "[lane assertion, no independent
  promotion verifier]". Promotion asks unmet; no box is checkable by a non-author at base. Ask
  unmet.
- Doubt checked: the defect text says "promotion stays operator-owned" — that is a statement of
  who may promote, not a lane decision to decline the item; the round-49 closure routed it as a
  defect for the lane next round. Nothing in the tree shows a decline (no ≥40-char reason), so
  `open`.

## Cross-cutting notes for the L1
- The base `SCORECARD.md:2410` **Planned (round 50)** paragraph names the work but contains no
  `R49.x` id strings; the counter's `open_unplanned` check matches ids (`\bR4\d\.\d+\b`) in the
  newest Planned paragraph at REV — the ids for the open rows must be added there when the ledger
  is finalized.
- All six codes carry evidence that is not a spot-check, not the ledger, not c1/control, with key
  occurrences: R49.1 `os.path.isfile`, R49.2 `absent`, R49.3 `/tmp/tameshi-r12-*`, R49.4
  `calibration | 6`, R49.5 `brace_depth_at`, R49.6 `[~]`.

## Summary
- R49.1..R49.6 all coded `open` at base e3729de; no `fixed` is possible (routed_at == base) and
  no `declined` reason exists.
- R49.1: guard still exits 1 for unreadable guard (isfile-only check, no OSError catch); no
  selftest case; F2/F3 unchanged (tools/pbt-staged-id.py:982-984, 771-778, 790-817).
- R49.2: no successor counters; round-49 C1 `absent` still uncapped and evidence-free,
  C2 still presence-only (no round-50 evidence dir at base).
- R49.3: SKILL.md 1503/1509/1555 byte-unchanged with the routed stale statements.
- R49.4: newest standing axis table (SCORECARD.md:2355) still calibration 6; no round-49
  restated table.
- R49.5: dead brace_depth_at helpers still in tally-audit-v2.py:135 / v3.py:234; remainder still
  carried in Planned (round 50).
- R49.6: SHONEN.md four `[~]` boxes unchanged; no independent promotion verifier.
- Caveat: Planned (round 50) paragraph lacks the R49.x ids; add them for `open` rows before the
  deciding run.

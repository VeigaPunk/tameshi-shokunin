# R98S1 — LOG entry draft (`## Round 98 (2026-11-08)`)

> Draft by seat R98S1 (scribe), in the shape of the round-96/97 `LOG.md` entries. Receipt
> lines quoted below were read from blobs committed at
> `764aca97e513d650949999362cd4b0f5f0e566a5`. `<TO FILL AT RECORDS>` marks the
> records-revision values.

## Round 98 (2026-11-08) — measurement-derived control codes (C1) and guard refusal receipts (C2)

- **Shape.** Base `034240a5`; instruments `d32043ec`; freeze `764aca97` (plan, claims, 12
  pre-freeze controls, S012/S009 snapshots); records `<TO FILL AT RECORDS>`. One v1 wave
  `w1`, 13 seats.
- **R98-C1 (calibration).** The round-97 spot-check's D-2: `controls97.py:156` registered
  `add("c2-nowork-absent", 0, …)`, so the state passed whatever the wrapped `git grep`
  returned — the committed receipt carries outer `rc=0` while the body records the grep's
  `rc=1`. `tools/control-assertion-audit.py` reads a driver blob at `--rev` through `git
  cat-file` (never the worktree) and classifies every static `add(...)` site's recorded code
  as `measured` (derived from `sh`, `git`, `run`, `subprocess.run` — directly, through the
  name's last assignment before the call, or as the first element of `code, out = run(...)`),
  `literal`, or `unresolved`; a site inside a loop counts once; the expectation is data and is
  not classified. Pre-freeze at `d32043ec`: the round-97 driver prints `CONTROL_ASSERT
  sites=15 measured=14 literal=1 unmeasured=1` exit 1 (line 156 named), the repaired driver
  prints `sites=15 measured=15 literal=0 unmeasured=0` exit 0, the selftest is `12/12`, and
  the repaired driver's full run at base `07e50d6d` prints `CONTROLS98 states=18 matched=18
  mismatched=0` with `c2-nowork-absent`'s outer `rc=1`. At `<RECORDS_REV>`:
  `<TO FILL AT RECORDS>`.
- **R98-C2 (operability).** The round-97 spot-check's D-6: two of the six `GUARD_SETUP`
  refusal classes the round-97 matrix declared had no committed receipt or selftest case.
  `.ufo/evidence/round-98/refusals/guard-refusals.py` reads the frozen tool as a blob at
  `--rev` (pinned `--tool-sha`), builds one manifest fixture per class in a scratch clone, and
  runs the public CLI once per class, requiring exit 2 and the exact class token on a line of
  the tool's own stdout; the committed manifest must print `GUARD_INERTIA rows=10 killed=8
  limits=2 survived=0 unmet=0` exit 0. Pre-freeze at `d32043ec`: `GUARD_REFUSALS classes=6
  refused=6 wrong=0 positive=ok` exit 0; the red arm (`--red state-unbuildable`) prints
  `classes=6 refused=5 wrong=1 positive=ok red=state-unbuildable` exit 1 — the battery's own
  able-to-fail demonstration; selftest `9/9`. The frozen tool emits 13 `GUARD_SETUP` tokens in
  all; the battery covers the six the matrix declared, and the record says so. The battery
  reads the tool blob whose digest the caller pins (`--tool-sha`), so the frozen tool's
  identity is the caller's obligation — a stub with the same interface scores the same
  (R98R2 F1); a non-64-hex and a mismatched pin print `GUARD_REFUSALS_SETUP tool-sha-invalid`
  / `tool-sha-mismatch`, exit 2 (wave receipts). The red arm's evidence is the named
  `GUARD_REFUSALS_RED <class> missed-as-declared` line; the summary line and exit 1 are the
  same for a missed and a refused red class (R98R2 F2). The battery prints no per-class
  success line and discards the tool's ten `GUARD_ROW` lines, so the six per-class runs are
  carried by a wave harness receipt, not by the battery's stdout (R98R2 F3). At
  `<RECORDS_REV>`: `<TO FILL AT RECORDS>`.
- **Motivating evidence and routed defects.** The round-97 spot-check's D-1…D-7 are this
  round's work items. D-1 (the in-place `anchor` additions on S006/S159) is logged old → new
  in `corpus/lessons/round-98.md` §Registry changes and measured by
  `tools/registry-cell-immutability.py` (red pair: two `anchor` findings, `changed=2`, exit 1;
  green pair: `changed=0`, exit 0; selftest `10/10`). D-3's three stale pre-A15 fragments are
  marked superseded by appended notes with both digests; D-4's two round-97 capability rows
  and this round's rows entered the SCORECARD table; D-5's report erratum and the
  `CONTROLS97` summary receipt landed; D-7 is graded in the report. Mistakes in
  `corpus/lessons/round-98.md`: M1 the mined round-97 anchor edit; M2 the round-98 battery's
  `main()` without `sys.exit(main())`, whose red verdict printed while the process exited 0
  and whose committed repair prints the same line with `rc=1`.
- **Frontier.** S012 re-opened (fetch 2026-11-08, HTTP 200, 42588 B, sha256 `fb6f384d…`,
  renderer line 112, 16-word quote) and cited by
  `corpus/knowledge/control-assertion-anchoring.md`; S009 probed — the L1's default-UA fetch
  returned 403 and the scout's declared-UA fetch returned the page (200, 42254 B, sha256
  `be3f85db…`, abstract at renderer line 413), so the challenge is UA-keyed, the row stays
  `queued` this round and its flip condition is recorded as met for the next round. No new row
  is written. Census exit 0 before (183 rows, A 165 · B 14 · C 4, mined 149 · queued 23 ·
  rejected 11) and after: `<TO FILL AT RECORDS>`. QUALITY 177; README round-98 row.

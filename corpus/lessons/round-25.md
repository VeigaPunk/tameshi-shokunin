# Round 25 — routed-item dispositions and mutation report interop

author: TameshiR25 (L1, attempt 2; fresh identity, attempt 1 not resumed)
Date: 2026-10-22. Base `1f7315732e0cfe0ba9dfe0fff2ef36d1c8481bb5`.

## Claims

- **C1 calibration (repair-first, routed by `round-24-verifier-spotcheck.md:63`).**
  The three round-23 closure-routed items that round 24 left unrecorded
  (MANIFEST `rounds[421].notes`: "multi-token stdout fixture in the ruler,
  re-run guard sweep, and dead-falsifier coverage gap") each get a SCORECARD
  row and an executed check. Counter
  `python3 .ufo/evidence/round-25/c1-measure.py --repo CLONE_AT_REV`:
  before 0/3 (exit 1), target 3/3 (exit 0). This is a record repair: the
  gate `tools/command-binding.py` is unchanged since base, so under QUALITY48
  the R1/R2 kills are controls, not gate repairs. The 0/3 baseline reflects
  absent files only.
- **C2 coverage, capability (frontier F1 report interop).**
  `tools/mte-interop.py` emits the eight recorded ledger legs as
  mutation-testing-elements reports, validates them with the official schema
  3.9.0 and scores them with the official metrics library 3.9.0. Counter
  `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root /home/vgpnk/Projects/shokunin`:
  before tool absent (0/8), target `MTE_INTEROP: PASS legs_conforming=8/8`.

Both were frozen in `.ufo/evidence/round-25/contract.json` (`2a97ec1`) before
the wave. Amendment 1 (`c9ff09f`) only made the C2 counter runnable from a
clone. Amendment 2 (`09dc114`, before any after measurement) only added
checks the wave showed were missing; see `contract-amendment-2.json`.

## Gate

Admit candidate: `corpus/knowledge/mte-report-interop.md`,
`tools/mte-interop.py` with its two vendored, sha512-pinned packages, the
round-25 rulers (`multitoken-cases.json`, both mutant specs, `c1-suite.py`),
`c1-pins.py` and `dead-falsifier-disposition.json`.

Reject:
- reading `C1_ROUTED: dispositioned=3/3` as closure of all round-23 routed
  breadth: the counter's population is the three fixed labels
  (`c1-measure.py:43`), not a list derived from the routing source;
- reading the guard sweep's 14/14 as guard adequacy: seat MtGuardGaps found
  17 single-edit weakenings of `evaluate()` that the gate's own selftest does
  not kill (cwd prefix match, exit via `abs()`, revision prefix compare and
  more). That is open ground, routed below;
- reading "official score equals tameshi kill rate" as an independent
  measurement: with the 1:1 status mapping it holds by construction (seat
  C2Tautology). The load-bearing C2 checks are `ledger` and `per_mutant`;
- reading the interop as a Stryker run, as Stryker mutators, or as producer
  authentication.

Flip condition: an independently retained, applicable execution or authority
record.

S086 opened 2026-10-22 UTC by the L1 (`npm pack` and `npm view
dist.integrity`, registry tarball
https://registry.npmjs.org/mutation-testing-report-schema/-/mutation-testing-report-schema-3.9.0.tgz)
and re-opened by seats C2SchemaSource, C2Integrity and DraftSources. Located
quote, `package/src/mutation-testing-report-schema.json:92`:
"`"enum": ["Killed", "Survived", "NoCoverage", "CompileError", "RuntimeError", "Timeout", "Ignored", "Pending"]`".
Second quote, same file, the Position definition: "Position of a mutation.
Both line and column start at one."

S087 opened 2026-10-22 UTC the same way
(https://registry.npmjs.org/mutation-testing-metrics/-/mutation-testing-metrics-3.9.0.tgz).
Located quote, `package/src/model/metrics.ts:70-71`: "The total percentage of
mutants that were killed, or NaN if not available. `totalDetected / totalValid * 100`".
Second quote, `:40-41`: "The total number of mutants that were detected,
meaning either killed or caused a time out."

Both new rows start as mined, tier A, recheck 180d, used by
`knowledge/mte-report-interop.md`. No existing row's status, recheck or
used-by changes. The vendored tarballs are byte-identical to the registry
artifacts (sha512 equal to `dist.integrity`), and the schema member is
byte-identical to the GitHub master file S002 tracks.

Bounded lookup: identified 2, screened 2, included 2, excluded 0.

## Mistakes

| Class | Evidence pointer | Captured-by | Fix / shown able to fail |
|---|---|---|---|
| population declaration with an unrouted denominator | MANIFEST `rounds[421].notes` routes eleven items, including "multi-token stdout fixture in the ruler, re-run guard sweep, and dead-falsifier coverage gap"; round-24 `contract.json` claims "eleven named … predicates routed by round23 critics and closure"; `lessons/round-24.md` Erratum I counts "eight round23 routed defects"; the verifier records "three closure-routed items remain unrecorded" (`round-24-verifier-spotcheck.md:34,37`) | QUALITY 12 (`corpus/QUALITY.md:39-41`, "report all declared defects, unresolved denominators"); QUALITY 48 has no membership clause (round-24 seat CorpusQuality48) | New QUALITY 50 (routed-item ledger by identity, not count). Shown able to fail on this round's ledger: `c1-pins.py` refuses a disposition file with one row dropped (P3) and a SCORECARD row that does not read `dispositioned` (P5); see `## After measurement`. Limit: the three-label population of `c1-measure.py` cannot see a routed item outside those labels. |
| fleet-state side effect from a seat | seat ReReplay14 ran `jj log` at the fleet root; its report says a working-copy reset and git import were printed; fleet `git status` afterwards shows intent-to-add entries | wave context bound "never touch the fleet repo" (seats are told, nothing enforces it) | Reported to Main during the round; no repair attempted by the lane. Next wave contexts should name `jj` explicitly next to git: any `jj` command, even `jj log` or `jj st`, snapshots a colocated working copy. Seat ReOutputComplete also ran `jj st` in the lane. |
| a frozen ruler weaker than its routed item | the guard sweep frozen at `2a97ec1` re-ran only four of round 23's ten anchors verbatim (seats QualityCriterion, C1Framing); the seven multi-token fixtures let four strictly weaker token matchers survive (seat MtWeakerGate) | QUALITY 44 (frozen population anchors are never dropped silently) | Amendment 2 adds G9–G14 (all ten round-23 anchors now verbatim) and fixtures 8–11 with mutants M7–M10; the sweeps kill 14/14 and 10/10 with explicit witnesses. |

## Wave findings routed forward (not claimed this round)

- MtGuardGaps: 17 single-edit weakenings of `command-binding.py` `evaluate()`
  survive the gate selftest (cwd prefix/basename/commonprefix, exit `abs()` or
  modulo 256, token case-fold or strip, unknown requirement keys, unchecked
  `stdout_contains`/`stderr` types, unchecked `schema`, revision prefix or
  suffix compare, case-insensitive membership, newline-joined argv). Fixture
  additions only; the gate code needs no change.
- Re-attack FINDING rows (14 of 34, `dead-falsifier-disposition.json`): loose
  substring tokens accept zero-case or echoed verdicts (Replay13, 14, 16, 20,
  25, 27), exit-only rows accept a wrong snapshot verdict (Replay02, 15), the
  replay projection drops `held`/`cleanup_error` (Replay18), numeric prefix
  collisions (Replay10), revision is copied, not observed (Replay19), a
  registry token stricter than its source (Replay06), unbounded retained
  streams (OutputComplete), row-order-dependent finding ids
  (SchemaPriority), a false recorded death mechanism and a "byte-exact" claim
  off by one newline in round-23 accounting (WaveAccounting).
- Spot-check routing items 2–4 stay open (seat SpotRouting2 gives path:line for
  each); item 5 is fleet scope.
- C2: suite timeouts (exit 124) are emitted as RuntimeError by convention;
  NoCoverage for the 35 recorded survivors is frontier F1b.

## After measurement

At `77302fa8f79144d06c1d2d2e2d2898c44b459bda`, in a fresh clone
(`.ufo/evidence/round-25/after/`):

- C1: `C1_ROUTED: dispositioned=3/3`, exit 0. `c1-pins.py`: HOLD, 0 failures,
  10 pinned files, dispositions 20 AGREE / 14 FINDING / 0 died.
- C2: `MTE_INTEROP: PASS legs_conforming=8/8`, exit 0 (146.7 s), every leg
  `per_mutant=ok failed=none`; selftest 17/17. The runner's integer
  kill-rate equals the official score rounded half up on all eight legs.
- Negative controls in a scratch clone at the same revision: one disposition
  row dropped gives `C1_PINS: FAIL` and `C1_ROUTED: dispositioned=2/3`; the
  R23-ROUTED-2 row changed to "NOT dispositioned" gives `C1_PINS: FAIL` while
  the frozen counter still says 3/3. The QUALITY 50 fix can fail; the frozen
  counter's row test cannot see row content.
- Harmed intermediate: the strict cold-read monitor read 45/62, restraint 6
  (base `1f73157`: 62/62, restraint 8). Cause: input drift of 17 SKILL.md
  sections whose traced inputs include corpus files edited this round
  (QUALITY, README, SOURCES, PROVINCE, SCORECARD). SKILL.md itself is
  unchanged. Restored by actual traced L1 source reads with the round-23
  re-anchor tool at the final content revision; the result follows.

Restoration and final no-harm, at `3b20f073c7305a582562cd323982991464c324f3`
(`.ufo/evidence/round-25/after/`): at `154bf4d` the monitor still read 45/62,
restraint 6 (`monitor-harmed-154bf4d.json`). The round-23 re-anchor tool made
seventeen actual traced L1 source reads at `154bf4d`
(`source-traces/`, `source-refresh-receipts.json`); the seventeen entries
were appended to the cold-read ledger with its 287-entry byte prefix
unchanged (`source-prefix-preservation.json`). These are author source reads,
not independent or blind cold-reads. Final: strict monitor 62/62,
restraint 8, depth 8, overrides false; registry held 47/47, superseded 7,
exit 0; census exit 0 (85 rows, seven pre-existing W04 warnings); C1 counter
3/3 and `c1-pins.py` HOLD again at this revision; `tools/mte-interop.py` is
byte-identical to the C2 measured commit `77302fa`.

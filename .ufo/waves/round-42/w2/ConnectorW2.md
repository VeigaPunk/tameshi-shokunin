# ConnectorW2 — fleet knowledge overlap scan (round 42, wave 2)

Attacked: the fleet novelty and adjacency of `corpus/knowledge/pit-outcome-vocabulary.md` and
`corpus/knowledge/r42-attribute-and-outflag-destinations.md`. Read-only; no counter run; no
scratch clone; no tool installed or upgraded. Access date 2026-10-25.

## Scan

Run from `/home/vgpnk/Projects/shokunin` across all 21 `*-shokunin/corpus/knowledge/` dirs:

```
rg -n -i 'RUN_ERROR|run[ _-]?error|runtime[ _-]?error' *-shokunin/corpus/knowledge/
rg -n -i -l 'stryker|pitest|\bPIT\b'                     *-shokunin/corpus/knowledge/
rg -n -i 'argparse|parse_args|\bdest\b'                  *-shokunin/corpus/knowledge/
rg -l 'RUN_ERROR' *-shokunin | grep -v /corpus/knowledge/
```

Outside tameshi, the only Stryker or PIT hit on mutation scoring is kama. The kotodama "PIT"
hits are archaeology ("Great Death Pit", storage pits), for example
`kotodama-shokunin/corpus/knowledge/myth-symbol/ritual-liminality.md:11`, so they are false
positives. Outside tameshi, `RUN_ERROR` appears only in kama
(`corpus/SOURCES.md`, `corpus/lessons/round-20.md`).

## Finding 1: the PIT `RUN_ERROR(true)` finding is not new to the fleet

- `kama-shokunin/corpus/knowledge/error-is-not-a-verdict.md:32-36`: "S063 PIT instead marks
  `RUN_ERROR(true)` and counts it in detected totals. Thus the inference "all mutation tools
  exclude crashes" is rejected." (≤25 words, line 33-35)
- `kama-shokunin/corpus/SOURCES.md:75` (S063): this is the same URL as tameshi S158, at the
  same commit `f7fe5adfa5fb6e727c12d2403a48f5e4e9dd2fc6`. Locator "RUN_ERROR(true) line 63;
  isDetected lines 102–109; ScorePrecursor.java lines 34–46". Status `rejected` (as support
  for a universal rule), dated 2026-10-21, in kama round 20.
- `kama-shokunin/corpus/SOURCES.md:74` (S062) is the same Stryker page as tameshi S001
  (`tameshi-shokunin/corpus/SOURCES.md:12`). The Stryker-against-PIT contrast therefore
  already exists in kama knowledge, four days before round 42.
- The line numbers agree. In tameshi's snapshot
  (`.ufo/evidence/round-42/sources/pit-DetectionStatus.java`, sha256 `3bf295ad…`, 119
  lines), `:63` is `RUN_ERROR(true),` and `:108` is `public boolean isDetected() {`.
  Kama's range 102–109 runs from the Javadoc at `:102` to `return this.detected;` at `:109`.
  The two citations do not conflict.
- Kama went deeper. `kama-shokunin/.ufo/waves/round-20/build/advice/SrcPitStatuses.md:12-13`
  traces `ScorePrecursor.java:34-46` → `Score.java:39-43,72-77`, which prints the detected
  total under "Killed". It also cites PIT's own `DetectionStatusTest.java:59-63`, which
  asserts `RUN_ERROR.isDetected()` under the comment `// really? dubious`. Tameshi traces
  only as far as the enum and says "the scoring claim rests on PIT's source"
  (`pit-outcome-vocabulary.md:72-73`). Kama's caller trace is the evidence that the flag
  reaches the printed score.

What is genuinely new to the fleet in tameshi's entry: S155 and S156 (PIT docs: the
seven-outcome vocabulary, No coverage against Survived, and run-to-run nondeterminism of
timeouts), the `TIMED_OUT(true)` and `getForErrorExitCode` reading (`:31-34`, `:53`), and
the finding that the lane's timeout rule matches neither tool (`:49-56`). Kama's entry does
not cover timeouts or the outcome vocabulary.

## Finding 2: neither tameshi entry cites kama

```
rg -n -i 'kama|error-is-not-a-verdict' tameshi-shokunin/corpus tameshi-shokunin/SCORECARD.md tameshi-shokunin/.ufo/waves/round-42/w1
```

The only kama hits are about province (endpoint health) and the fleet census. None concerns
PIT or Stryker scoring. `pit-outcome-vocabulary.md:11` says "S158 is new this round". That
is true for the lane but silent about the fleet. No round-42 record claims fleet novelty,
so nothing false is asserted:
- `corpus/lessons/round-42.md:31,115`
- `LOG.md:2197`
- `corpus/QUALITY.md:1030`

The gap is an adjacency omission, not a false claim.

## Finding 3: argparse-derived destinations have no fleet knowledge overlap; one adjacent entry

- No fleet knowledge entry derives argparse `dest`, binds `parse_args()` results, or
  resolves `self.<attr>` write roots. The argparse hits are incidental mentions:
  - `chousa-shokunin/corpus/knowledge/claim-verification-r2.md:39` (a line-range citation)
  - `kama-shokunin/corpus/knowledge/ollama-evidence-replay.md:131` (bad argv exits 2)
  - `mado-shokunin/corpus/knowledge/waybar-walker-semantics.md:437` (help text)
- One adjacent entry, to cite and not absorb:
  `kotoba-shokunin/corpus/knowledge/checklist-execution-round16.md:143` declares an
  output-flag list `-o --out --output --write --dest --log --to --target -O`. Under it, a
  written path with an undeclared flag FAILs. This is a static pasted-command checker
  driven by a declared flag list, not a dest derivation. The two lists differ:
  - Tameshi v4 traces `--out`, `--output`, `--out-dir` and `--output-dir`
    (`r42-attribute-and-outflag-destinations.md:41`).
  - Kotoba omits `--out-dir` and `--output-dir`. Tameshi omits `-o`, `--write`, `--dest`,
    `--log`, `--to`, `--target` and `-O`.
- The entry's Adjacency section (`r42-attribute-and-outflag-destinations.md:87-91`) rests on
  the wave-1 connector scan. That scan covered tool, script, verifier and census trees
  (`.ufo/waves/round-42/w1/ConnectorSibling.md:152`), not knowledge. This scan closes the
  knowledge half, and the entry's "no sibling tool" claim survives it.

## Proposed move (one, bounded; for L1 to judge, not applied)

Add one cite-not-absorb line to `pit-outcome-vocabulary.md`, either in §Boundary or a new
§Adjacency:

> kama holds the same `RUN_ERROR(true)` reading (kama S063, same commit, rejected as
> support for a universal rule; `kama-shokunin/corpus/knowledge/error-is-not-a-verdict.md:32-36`).
> Its round-20 scout traced the flag into PIT's printed "Killed" score
> (`kama-shokunin/.ufo/waves/round-20/build/advice/SrcPitStatuses.md:12-13`).

Optionally, add one line to `r42-…destinations.md` §Adjacency naming kotoba's declared
output-flag list as the nearest non-resolving neighbour.

- **Axes:** adjacency improves, because prior fleet work becomes visible and the entry stops
  implying the reading is original. Depth is unharmed. The cite also strengthens tameshi's
  scoring inference, which currently rests on the enum alone, by pointing to a caller trace
  already in the fleet. No-harm is unharmed: the edit is knowledge text only, and neither
  counter, the v4 tool, nor the pinned bytes change.
- **Risks:**
  - Kama's caller trace is wave advice, not a committed snapshot. The cite must stay a
    pointer and must not import kama's line numbers as tameshi evidence.
  - Kama's S063 status is `rejected`, but only as support for a universal rule, not as a
    reading. A careless cite could read as "kama rejected this source".
- **Verification:** re-run Finding 2's `rg` after the edit and expect exactly one PIT-related
  kama hit in `pit-outcome-vocabulary.md`. `sed -n '32,36p'
  kama-shokunin/corpus/knowledge/error-is-not-a-verdict.md` re-locates the cited sentence.

## Verdict

BROKEN: the PIT `RUN_ERROR(true)` finding is not new to the fleet. Kama S063 and
`error-is-not-a-verdict.md:32-36` have held it at the same commit since 2026-10-21, and
neither round-42 entry cites it. The entries' own lane-scoped claims and the argparse "no
sibling" adjacency SURVIVE.

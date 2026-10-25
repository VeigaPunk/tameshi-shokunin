# ReopenS158 — round 42 wave 2 (FALSIFY)

Seat: L1Tameshi42.ReopenS158 (scout, read-only). Attacked: the S158 row, the committed
snapshot `pit-DetectionStatus.java`, and every S158-attributed quote in the three round-42
records. Accessed 2026-10-25. Scratch: `/tmp/tameshi-r42w2-ReopenS158-x60W` (deleted on return).
No counter run. No tool installed.

## F1 — snapshot re-fetch: identical

```
curl -fsSL -m 60 -o $D/DetectionStatus.java https://raw.githubusercontent.com/hcoles/pitest/f7fe5adfa5fb6e727c12d2403a48f5e4e9dd2fc6/pitest/src/main/java/org/pitest/mutationtest/DetectionStatus.java   # exit 0
sha256sum: 3bf295ad53126560ec284c42b384fc3288f7b2e674da987f38d7380ec5d419c6  (re-fetch)
           3bf295ad53126560ec284c42b384fc3288f7b2e674da987f38d7380ec5d419c6  .ufo/evidence/round-42/sources/pit-DetectionStatus.java
wc -lc: 119 lines, 2988 B (both); cmp → IDENTICAL
```

- `.ufo/evidence/round-42/sources/sha256.txt:5` carries the same digest.
- Lesson claim "byte-identical to master at fetch time" (`corpus/lessons/round-42.md:28-30`)
  still holds today: `git ls-remote https://github.com/hcoles/pitest refs/heads/master` →
  `f7fe5adfa5fb6e727c12d2403a48f5e4e9dd2fc6`, and the raw `master` file hashes `3bf295ad…`.

## F2 — S158 row (`corpus/SOURCES.md:128`): holds

`sed -n '128p' corpus/SOURCES.md | awk -F'|' '{print NF}'` → 13 fields, so 11 cells between
the outer pipes. The header at `corpus/SOURCES.md:10` has 11 columns. No cell contains a pipe.

| cell | value | check |
|---|---|---|
| id | S158 | ok |
| source | hcoles/pitest at full commit + blob URL | URL resolves to the same bytes (F1) |
| kind / tier | code / A | ok |
| anchor | "enum constants RUN_ERROR and TIMED_OUT, isDetected() and getForErrorExitCode() … 2988 B sha256 3bf295ad" | all four are in the snapshot: lines 63, 37, 108, 91; size and digest prefix match |
| teaches | "PIT marks RUN_ERROR and TIMED_OUT as detected and maps a non-zero child exit that is not out of memory or a timeout to RUN_ERROR, so its score counts run errors as detections" | holds; see gap G1 |
| status / opened / recheck | mined / 2026-10-25 / 180d | ok |
| used-by | `corpus/knowledge/pit-outcome-vocabulary.md`, `corpus/knowledge/r42-attribute-and-outflag-destinations.md` | `test -f`: both exist; both cite S158 (`pit-outcome-vocabulary.md:3`, `r42-…:4`) |

## F3 — S158-attributed quotes and line citations (snapshot `grep -n`)

Each quoted string is one word, so all are within the 25-word limit. All are verbatim.

| # | record path:line | quoted / cited | snapshot line | verdict |
|---|---|---|---|---|
| 1 | `pit-outcome-vocabulary.md:31` | `RUN_ERROR(true)`, "snapshot line 63" | 63: `  RUN_ERROR(true),` | verbatim, line correct |
| 2 | `pit-outcome-vocabulary.md:32` | `detected` field, line 78; `isDetected()`, line 108 | 78: `private final boolean detected;`, 108: `public boolean isDetected() {` | correct |
| 3 | `pit-outcome-vocabulary.md:33-34` | `getForErrorExitCode` (line 91) → `RUN_ERROR` unless OOM/timeout | 91–98 | correct (G1) |
| 4 | `pit-outcome-vocabulary.md:53` | `TIMED_OUT(true)`, line 37 | 37: `  TIMED_OUT(true),` | verbatim, line correct |
| 5 | `pit-outcome-vocabulary.md:43-44` | "PIT counts it as detected (S158)" (claim, no quote) | 63, 108 | supported (G1) |
| 6 | `r42-attribute-and-outflag-destinations.md:61-62` | `RUN_ERROR(true)`, line 63 | 63 | verbatim, line correct |
| 7 | `round-42.md:31` | `RUN_ERROR(true),` (with comma), line 63 | 63 | verbatim, comma included, line correct |
| 8 | `round-42.md:32` | `detected` field (line 78), `isDetected()` (line 108) | 78, 108 | correct |
| 9 | `round-42.md:30-31` | 2988 B, sha256 `3bf295ad…c419c6` | F1 | correct |
| 10 | `round-42.md:115` | "PIT's source scores `RUN_ERROR` as detected (S158)" (claim) | 63 | supported (G1) |

Header pins: `pit-outcome-vocabulary.md:3` gives the URL, the full sha256 and the anchor,
all correct. `r42-attribute-and-outflag-destinations.md:4` names the snapshot only, with no
URL and no digest. It is less detailed than its sibling entry, but it is not wrong.

## Gaps (disclosed, not breaks)

- **G1: two steps that S158's bytes alone do not show.** I checked both upstream at the
  same commit, and both hold.
  (a) "so its score counts run errors as detections" needs the score code:
  `pitest-entry/src/main/java/org/pitest/mutationtest/statistics/ScorePrecursor.java:34-45`
  (sha256 `615d88c1…`) sums the status counts filtered by `a.getStatus().isDetected()`, and
  `MutationStatistics.java:84-85` computes the percentage from that total.
  (b) "non-zero child exit" needs the caller:
  `pitest-entry/.../build/MutationTestUnit.java:121-125` (sha256 `e03df52d…`) calls
  `getForErrorExitCode` only under `if (!exitCode.isOk())`, and `pitest/.../util/ExitCode.java:19`
  makes `OK(0)` the only zero code.
  The records ground (a) and (b) on S158 alone. Neither file is registered or snapshotted.
  A later round that wants the scoring claim pinned should add `ScorePrecursor.java`.
- **G2: an adjacent quote, not attributed to S158.** `corpus/lessons/round-42.md:115`
  puts "PIT Run error and Stryker RuntimeError, which neither tool counts as a kill" in
  quotation marks and attributes it to "the frozen contract and counter docstring". Neither
  carries that string. `.ufo/evidence/round-42/census/measure.py:20-21` reads `PIT's "Run
  error" and Stryker's RuntimeError, which neither tool counts as a kill`, and
  `.ufo/evidence/round-42/contract.json:46` reads `PIT Run error, Stryker RuntimeError), not
  killed`. The meaning is preserved, but the lesson's wording is a paraphrase inside quotation
  marks. It falls outside this seat's S158 scope and is routed to the lesson reviewer.

## Upstream files fetched (scratch only, at f7fe5adf)

DetectionStatus.java `3bf295ad…` (pinned and master), ExitCode.java `c23b3aa9…`,
MutationStatistics.java `366cfd27…`, MutationStatisticsPrecursor.java `b5057bfe…`,
Score.java `65539d56…`, ScorePrecursor.java `615d88c1…`, StatusCount.java `9a483ae2…`,
MutationTestUnit.java `e03df52d…`. Tree listing: `gh api repos/hcoles/pitest/git/trees/<commit>?recursive=1`.

SURVIVES

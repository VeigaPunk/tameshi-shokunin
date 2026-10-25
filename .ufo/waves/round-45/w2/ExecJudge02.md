seat: ExecJudge02

# Round-45 w2 C1 falsify: S005, S072, S087

Independent re-judgement of three wave-1 ledger entries authored by ExecRows02 (S005),
ExecRows13 (S072) and ExecRows15 (S087). Inputs read at
`ad5942c6e9858af19d00000b58439b321ddfa62b` (`.ufo/evidence/round-45/freshness/ledger.json`,
committed snapshots); registry rows read from the worktree `corpus/SOURCES.md`
(S005 line 16, S072 line 81, S087 line 96); counter read-only at
`.ufo/evidence/round-45/freshness/measure.py`. Read-only on the lane; no tool installed
(stock curl/python3/tar only; pacman paused, nothing needed).

## Verdicts

S005 agree — reviewer ExecJudge02 — live sha256 equals both the ledger's and the committed snapshot's, and the 15-token quote sits at HISTORY.rst:23 inside §3.8.0 (anchor :13-46) as a changelog fix bullet stating exactly the CPU-time-limit kill-vs-timeout lesson the teaches cell names, with the env-clearing false-survivor bullet at :13 and per-function hashing at :46 still present.
S072 agree — reviewer ExecJudge02 — live sha256 equals both the ledger's and the committed snapshot's, the page footer still reads `Linux man-pages 6.19 2026-02-08` exactly as the anchor states, and the 22-token quote is the O_TRUNC entry of the DESCRIPTION file-creation-flags list (normalized offset 18537) naming O_RDWR as an access mode that allows writing and asserting truncation to length 0, i.e. the write-capable-input claim.
S087 agree — reviewer ExecJudge02 — live sha256 equals both the ledger's and the committed snapshot's, and the 24-token quote is the doc comment plus declaration of `totalDetected` at `package/src/model/metrics.ts:39-43` (anchor :39-42) defining detected as killed + timed out, with `totalUndetected = survived + no coverage` (:44-48), `totalValid = totalDetected + totalUndetected` (:54-58), `mutationScore = totalDetected / totalValid * 100` (:69-73) and `totalInvalid = runtimeErrors + compileErrors` (calculateMetrics.ts:238) all still present in the same tarball.

No disputes.

## Provenance (fetched now, 2026-10-25)

```
for u in ...; do curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o /…/S###.live "$url"; done
S005 fetched 19417 bytes      S072 fetched 76506 bytes      S087 fetched 32668 bytes
sha256sum *.live
e9cace4dc9d4e2b438ad26782b50e8bd5fa17f838706a28699eee06a459e7ae3  S005.live
d665489cadb85624d98fae03a8d8d06209030f32735cff8aeba949ad8491c789  S072.live
ce17812bf718cf2415fb429b2774c7ad3e1e0ca57234e7f8cfa0d794f38ec548  S087.live

gunzip -c .ufo/evidence/round-45/freshness/sources/S###.raw.gz | sha256sum
e9cace4dc9d4e2b438ad26782b50e8bd5fa17f838706a28699eee06a459e7ae3  -
d665489cadb85624d98fae03a8d8d06209030f32735cff8aeba949ad8491c789  -
ce17812bf718cf2415fb429b2774c7ad3e1e0ca57234e7f8cfa0d794f38ec548  -
```

Ledger `raw_sha256` values are byte-identical to both columns for all three rows, so
provenance is confirmed against live bytes — not merely snapshot-internal. The quote was
additionally re-located in today's live extract output (`measure.py --extract` of each
`S###.live`, `--member package/src/model/metrics.ts` for S087): `quote_in_today_live=True`
for S005 (15 tokens), S072 (22), S087 (24).

## Context located (quote ± a few words)

S005, HISTORY.rst line 23, inside `3.8.0` (header :4-5, next section `3.7.0` at :35), i.e.
within the anchor's :13-46:
`… * Fix time measurement including test setup/teardown instead of only the main test run (#544) * Fix mutants stopped by the CPU-time limit being reported as killed instead of timed out (#565) * Fix mutate_only_covered_lines breaking when …`
Body content of the changelog, not a title/nav/footer. All three teaches clauses survive:
:23 CPU-time limit → reported as killed instead of timed out; :13 `Fix mutants being
reported as survived when a test uses patch.dict(os.environ, ..., clear=True) (#511, #552)`;
:46 `Per-function source hashing for incremental cache invalidation` under `3.7.0`.

S072, normalized offset 18537, DESCRIPTION file-creation-flags list (access-mode sentence at
offset 2363: `The argument flags must include one of the following access modes: O_RDONLY,
O_WRONLY, or O_RDWR. These request opening the file read-only, write-only, or read/write,
respectively.`):
`… ubifs (Linux 4.9) O_TRUNC If the file already exists and is a regular file and the access mode allows writing (i.e., is O_RDWR or O_WRONLY ) it will be truncated to length 0. If the file is a FIFO or terminal device file, the O_TRUNC flag is ignored. Otherwise, the effect of O_TRUNC is unspecified. creat() …`
Footer: `Linux man-pages 6.19 2026-02-08 open(2)` — matches the anchor's `6.19 (footer
2026-02-08)`; the page's only other date is the man7.org HTML-render stamp `2026-09-09`,
which is rendering chrome, not a version bump.

S087, `package/src/model/metrics.ts:39-43`:
`… ignored: number; /** * The total number of mutants that were detected, meaning either killed or caused a time out. * \`killed + timed out\` */ totalDetected: number; /** * The total number of mutants that were undetected, so either survived or were not covered by any code …`
Supports the teaches arithmetic: numerator killed+timed out; denominator `totalValid =
totalDetected + totalUndetected` with `totalUndetected = survived + no coverage`;
`mutationScore = totalDetected / totalValid * 100`; errors are not survivors
(`totalInvalid = runtimeErrors + compileErrors` at calculateMetrics.ts:238, matching the
anchor's `calculateMetrics.ts:234-255` citation, whose :234-237, :253 repeat the same
arithmetic).

## Mechanical predicate (seat helper, never a measurement)

```
python3 .ufo/evidence/round-45/freshness/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev 3310e7be803516ca5934b4e949d91bcec824b179 --check /…/S###.json
CHECK S005 verified ok   (exit 0)
CHECK S072 verified ok   (exit 0)
CHECK S087 verified ok   (exit 0)
```

Independent recomputation of the two non-snapshot predicates (same STOP/fold rules):
`copied_from_row=False` for all three; shared content words S005 3 `{killed, mutants, time}`,
S072 6 `{access, allows, file, mode, rdwr, writing}`, S087 4 `{detected, killed, timed,
totaldetected}`; token counts 15 / 22 / 24 — inside the 6-25 band.

## Notes, not disputes

- S072's quote begins mid-sentence (`a regular file …`): the dropped lead-in is
  `If the file already exists and`, so the quote itself still conditions on a regular file
  and states truncation when the mode allows writing. The row's teaches says "whenever the
  access mode allows writing" while the page also excludes FIFOs/terminals
  (`If the file is a FIFO or terminal device file, the O_TRUNC flag is ignored.`). That
  over-generalisation is pre-existing row-cell wording, not a freshness failure: the quote
  does not misstate the rule and the claim under test (an O_RDWR+O_TRUNC open of a file is
  write-capable) is stated outright.
- S087's metrics.ts doc comment says `totalInvalid` is `runtimeErrors + transpileErrors`
  while the declared field is `compileErrors` (upstream comment staleness); the teaches'
  "compile and runtime errors are invalid" is confirmed by calculateMetrics.ts:238
  (`totalInvalid = runtimeErrors + compileErrors`) in the same tarball.

## Environment / scratch

- `/tmp` hit ENOSPC mid-run (`OSError: [Errno 28] No space left on device`, `df -h /tmp`
  showed 128G/128G, 364K free — host-wide, other seats' scratch), so my scratch was moved
  to `/home/vgpnk/r45-scratch/ExecJudge02/` (396K) to free `/tmp` for siblings; `reviews.json`
  was written at the assigned path `/tmp/tameshi-r45-ExecJudge02/reviews.json` once space
  returned, with an identical copy in the home scratch. No lane file other than this report
  was touched; no git/jj command was run.
- Retained evidence in `/home/vgpnk/r45-scratch/ExecJudge02/`: `S005.live`, `S072.live`,
  `S087.live` (today's bytes), `S###.snap` (gunzipped committed snapshots), `S###.txt` /
  `S###.live.txt` (extract output), `S087.metrics.ts`, `calc.ts`, `reviews.json`.

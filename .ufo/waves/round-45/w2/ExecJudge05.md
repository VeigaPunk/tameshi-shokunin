seat: ExecJudge05

# Round-45 C1 falsify wave (wave 2) — independent re-judgment of S081, S106, S158

Inputs read at `ad5942c6e9858af19d00000b58439b321ddfa62b` (`git show ad5942c:.ufo/evidence/round-45/freshness/ledger.json` → 73 entries) and the lane's committed snapshots at the current tip. Authors: S081 → ExecRows04 (`.ufo/waves/round-45/w1/ExecRows04.md`), S106 → ExecRows21 (`ExecRows21.md`), S158 → ExecRows24 (`ExecRows24.md`). I am the author of none of them. Registry rows read at `corpus/SOURCES.md:90` (S081), `:118` (S106), `:128` (S158).

## Verdicts (one line per row)

S081 agree — reviewer ExecJudge05 — sha256 equal across live fetch, committed snapshot and entry `raw_sha256` (`d12c985a…`); the 19-token quote sits in the "Role of the test runner" normal-completion paragraph the anchor names and states the teaches clauses that normal completion with exit zero passes and stdout PASS/FAIL is irrelevant, with the optional `TEST_PREMATURE_EXIT_FILE` row still reading "used for catching calls to exit()".
S106 agree — reviewer ExecJudge05 — sha256 equal across live fetch, committed snapshot and entry `raw_sha256` (`4b2c2ad0…`); the quote is exactly lines 72-73 of the `Compare` doc comment the anchor names, line 78 still opens with `shouldUpdateGolden()`, and lines 68-70 still report a unified diff, so both teaches clauses hold.
S158 agree — reviewer ExecJudge05 — live bytes differ from the entry only in GitHub request-id / visitor-uuid head chrome (normalized text identical, quote present in today's live extract), the quote is the `isDetected()` body adjacent to the anchor's `RUN_ERROR ( true )`, `TIMED_OUT ( true )` and `getForErrorExitCode()` mapping, and the teaches' upstream summation clause checks out at the pinned commit in `ScorePrecursor.java:44-45` and `MutationStatistics.java:84-85`.

`/tmp/tameshi-r45-ExecJudge05/reviews.json` carries the same three verdicts with `"report": ".ufo/waves/round-45/w2/ExecJudge05.md"`.

## Provenance — fetch, snapshot, entry digest

Command shape per row: `curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o /tmp/tameshi-r45-ExecJudge05/S###.live '<row url>'`, then `sha256sum`, then `gunzip -c <lane>/.ufo/evidence/round-45/freshness/sources/S###.raw.gz > /tmp/tameshi-r45-ExecJudge05/S###.snap && sha256sum`.

```
S081 http=200 bytes=221292
  live     d12c985aff6170d53e4f2f60c4be187665df6d2921282e97b06a9b693510c55a
  snapshot d12c985aff6170d53e4f2f60c4be187665df6d2921282e97b06a9b693510c55a  (221292 B)
  entry    d12c985aff6170d53e4f2f60c4be187665df6d2921282e97b06a9b693510c55a   EQUAL
S106 http=200 bytes=4043
  live     4b2c2ad039c45a548216588cc38bb954c3356d3d76b675e7e09a019f02de4e9f
  snapshot 4b2c2ad039c45a548216588cc38bb954c3356d3d76b675e7e09a019f02de4e9f  (4043 B)
  entry    4b2c2ad039c45a548216588cc38bb954c3356d3d76b675e7e09a019f02de4e9f   EQUAL
S158 http=200 bytes=276940
  live     7bc1ebd56144e23b888f184c471ef841adc62b093c2479870d1bec9825029ae3
  snapshot 51deedf9340ac8d9ba9a59385d75bb56ccd9705e7f8a00f33d84577426587bfe  (276935 B)
  entry    51deedf9340ac8d9ba9a59385d75bb56ccd9705e7f8a00f33d84577426587bfe   snapshot == entry, live DIFFERS (5 B)
```

S158 drift is page chrome, not content: common prefix 27052 B, common suffix 103536 B, and the differing span is a GitHub `<meta>`/uuid pair — snapshot `4dc18d76-48c2-93ee-4373-e548792c027e">` vs live `26b3440b-3e71-04e1-7c14-55b0bfdd8a34">` (request-id / visitor id). `python3 …/measure.py --extract` of both files yields byte-identical normalized text (`cmp -s S158.text S158.live.text` → identical, 6146 B each), and the quote occurs once in today's live text, so the per-brief "different chrome ⇒ quote must appear live" condition is satisfied. S081 and S106 needed no such fallback: live == snapshot == entry.

## Located context (few words either side)

S081 — `--extract` of the snapshot, one occurrence, at the "Role of the test runner" heading:
> … or output tree. **Role of the test runner** From the point of view of the test runner, each test is a program which can be invoked with execve() . … If a test process runs to completion and terminates normally with an exit code of zero, the test has passed. Any other result is considered a test failure. *In particular, writing any of the strings PASS or FAIL to stdout has no significance to the test runner.* If a test takes too long to execute …

Body prose at the anchor, not a title/nav/footer. The same extract still carries the `Initial conditions` table line `optional TEST_PREMATURE_EXIT_FILE absolute path to a private file in a writable directory (used for catching calls to exit() )` and the early-exit paragraph "a test may create a file at the path specified by TEST_PREMATURE_EXIT_FILE upon start and remove it upon exit", so the third teaches clause (a cooperative hook, not every early termination) is still stated.

S106 — one occurrence, at `Compare`'s doc comment; `awk 'NR>=60&&NR<=95'` on the raw snapshot shows the quote is exactly lines 72-73 and the anchor's branch is line 78:
> 68: // Compare compares the actual parameter … 69: // returns an empty string if they match. If they don't match, it returns a 70: // unified diff string documenting the differences. … **72: // If the -update_golden flag is set, this function will overwrite the 73: // contents of goldenFile with the actual value.** … 77: func Compare(actual string, goldenFile string) string { **78: if shouldUpdateGolden() {** 83: if err := ioutil.WriteFile(fullPath, []byte(actual), 0660); …

Both teaches clauses are body content at the anchor: the overwrite path behind the explicit flag (lines 72-73, 78) and the mismatch-as-unified-diff sentence (lines 69-70). The extract keeps the `//` comment markers, which is why the quote reads "the // contents" — it is verbatim from `--extract`, not a transcription slip.

S158 — one occurrence, in the rendered Java body (not the page's "Skip to content / Navigation Menu / Sign in" chrome), immediately after `getForErrorExitCode`:
> … public static DetectionStatus getForErrorExitCode ( final ExitCode exitCode ) { if ( exitCode . equals ( ExitCode . OUT_OF_MEMORY )) { return DetectionStatus . MEMORY_ERROR ; } else if ( exitCode . equals ( ExitCode . TIMEOUT )) { return DetectionStatus . TIMED_OUT ; } else { return DetectionStatus . RUN_ERROR ; } } /** * Returns true if this status indicates that the mutation was distinguished … * @return True if detected, false if not. */ *public boolean isDetected () { return this . detected ; }* …

The same code block (a few hundred bytes earlier) reads `TIMED_OUT ( true )`, `NON_VIABLE ( true )`, `MEMORY_ERROR ( true )`, `RUN_ERROR ( true )`, `NO_COVERAGE ( false )`, `EQUIVALENT ( true )` and `private final boolean detected ;`, which is what the teaches sentence "marks RUN_ERROR and TIMED_OUT as detected (isDetected() true)" asserts. Caveat recorded rather than smoothed: the 11-token quote itself covers only the `isDetected()` clause — the enum flags and the exit-code mapping that carry the rest of the sentence are adjacent in the same block at the anchor, which is why I still agree. The teaches' third clause is outside this file, so I checked it at the pinned commit: `pitest-entry/src/main/java/org/pitest/mutationtest/statistics/ScorePrecursor.java:44-45` is `private static Predicate<StatusCount> isDetected() { return a -> a.getStatus().isDetected(); }` and `MutationStatistics.java:84-85` is `public int getPercentageDetected() { return getPercentage(getTotalMutations(), getTotalDetectedMutations()); }` (both HTTP 200 at `f7fe5adfa5fb6e727c12d2403a48f5e4e9dd2fc6`), so PIT does sum every detected status into its score at that commit.

## Predicate re-run (allowed modes only)

Fragments rebuilt from the ledger entries, snapshots decompressed into `/tmp/tameshi-r45-ExecJudge05/snapraw/S###.raw`:

```
$ python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-45/freshness/measure.py \
    --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 3310e7be803516ca5934b4e949d91bcec824b179 \
    --check /tmp/tameshi-r45-ExecJudge05/S081.frag.json --snapdir /tmp/tameshi-r45-ExecJudge05/snapraw
CHECK S081 verified ok          rc=0
CHECK S106 verified ok          rc=0
CHECK S158 verified ok          rc=0
```

Quote token counts (whitespace tokens): S081 19, S106 19, S158 11 — all inside 6-25. None of the three quotes appears in its row's source/scope/anchor/teaches cells, so none is row-copied (the counter's `quote copied from row` guard is not what my agree rests on; I read each cell and compared). No deciding measurement was run by this seat: only `--extract` and `--check` at `--rev 3310e7be…`, as the bounds allow.

## Risks / notes for L1

- All three agrees only count if this report is committed under `.ufo/waves/round-45/`, `reviews.json` lands at `.ufo/evidence/round-45/freshness/reviews.json`, and ExecJudge05 has non-empty output in the orchestrator-written `.ufo/waves/round-45/w2-results.json` at the deciding revision (`measure.py:200-225` `review_sets`). Reviews are also voided if the deciding revision's ledger entry names a different author for the same id.
- S158 is the one entry whose live bytes no longer match its `raw_sha256`; the snapshot is what the predicate hashes, and the snapshot still matches the entry, so nothing is lost — but a future re-open of that row will see the same chrome-only drift and should not read it as content change.
- No disputes. No tools installed (curl, python3, awk already present; pacman is host-paused and was not touched). Scratch kept at `/tmp/tameshi-r45-ExecJudge05/` (`S0{81,06,58}.live`, `*.snap`, `*.text`, `snapraw/`, `*.frag.json`, `reviews.json`, `tree.json`, `ScorePrecursor.java`, `MutationStatistics.java`). Lane untouched apart from this report file.

# B18MistakesDraft — round-18 `## Mistakes` draft (staged)

Seat: TameshiR18.B18MistakesDraft (leaf, scribe). Base: `183f87b899e6cae46be98d251cbc87fb5118f6ca`.
Output: `.ufo/waves/round-18/staged/lesson-round-18-mistakes.md` (new file, staging only).
Tools installed or updated: none. No subagents dispatched. No lane file edited; no git write.

## Behaviour

Drafted a `## Mistakes` block with five rows from the round-17 spot-check
(`corpus/lessons/round-17-verifier-spotcheck.md`, §5 G5 row and §7 items 2–3).
Each row carries class, evidence pointer, captured-by, and fix with a falsifier.

| Row | Class | Verdict on evidence |
|---|---|---|
| a | breadth overclaim: "K02 holes 1–4 closed" | Confirmed. Hole 1 (receipt argv / page-command binding) is open in `measure.py`; holes 2–4 have code at `:517`, `:82-84`, `:184`. |
| b | guard admitted without killing test | Confirmed: seven survivors, 2 + 2 + 3 across three mutation reports (`w2/MutateDispositionV2.md:54,58`; `MutateRegistryCheck.md:52,53`; `MutateTraceInputs.md:52,54,55`). |
| c | knowledge exit sentence not executed before admission | Confirmed: `input-keyed-coldread-credit.md:75` says missing ledger exits 2; code path is `no-ledger` (exit 0), `measure.py:546-552`. |
| d | wrong cross-reference (G7 "K02 hole 5" → hole 7) | Confirmed: `round-17.md:24` vs K02 `:28` (hole 5) and `:30` (hole 7). |
| e | stale count (89 vs final 94) | Confirmed as a presented-as-current count; 94 is the spot-check's committed tally, not re-executed. |

Captured-by is "none" for a, c, d, e, and "none for the kill requirement" for b.
For a, `QUALITY 24`'s sweep clause partly applied (wave 2 caught hole 2 at `round-17.md:81`),
and that was not swept to `:22`.

## Verification

Base-rev source check (script run over `git show 183f87b…:<path>`): 34 citations
`(path, line, quoted fragment)`, `BAD COUNT 0`. Every quoted fragment is a
substring of the cited base line.

Base-rev argv check: `measure.py` contains `argv` at lines 773 (fixture), 1462 and 1483
(CLI `main(argv)`). None reads receipt `argv`, so the hole-1 claim holds.

Base presence: `corpus/lessons/round-18.md` is absent at base (`git cat-file -e` exit 128).
The base for the staged file is therefore empty. Staged bytes = base + appended block trivially:
the prefix of length 0 is empty, and the whole file is the block.

Staged file: 14 lines, 5007 bytes, `sha256 360aa4f699078a74144f4761605b992c0647ac919db2a9b07295a7ac3329e6b9`,
starts `## Mistakes\n`, ends with LF, no CR, six `|` rows (header, separator, five data rows).

Lane state after writing: `git --no-optional-locks status --porcelain` shows `.ufo/waves/round-18/`
(my staged and report files), `.ufo/evidence/round-18/` and `tools/trace-inputs.py`
(other seats, not touched by me). HEAD and master remain `183f87b…`.

## Not verified here

- The probe rulers P01–P07 and the round-18 owner fixes are not built or run;
  the falsifiers in rows a–b name them as the test to run later.
- The 94-case measure tally was not re-executed.
- `measure.py` was read, not run.

## Routed to L1

- Row a's erratum at `round-17.md:22` and row d's erratum are proposals; the L1 installs them.
- The final `round-18.md` should carry this block once the L1 decides placement.

Verdict: built (staged draft, 5 rows, 34/34 base-rev citations verified; falsifiers not run).

# FSourceS058 — round-19 W2 falsifier of w1 SourceS058 (scout, advisory)

Seat `TameshiR19-2.FSourceS058`, 2026-10-21. Advisory only: it closes nothing and carries no admission authority.
Frozen build is `55e1d312c4e8ac67aefad80099bd27581ff805c9`. Master tip `e7039fd` adds only wave-2 plan/run/spec/registry files and `current-ledger-monitor-55e1d31.json`.

## Strongest material assertion (the only C1-bearing one)
`SourceS058.md:149-178` (§6, dated 2026-10-21) says the C1 ruler never checks the R18-4 receipt's tool/runner hashes:
"Then a mutant with a wrong tool or runner hash must reopen R18-4. Today the ruler has no such check."
- **On that claim: DISAGREE at 55e1d31.** It was true at `21e7932` and has since been repaired.
- **On the source re-open: AGREE.** I reproduced the digest, the quote and the row identity independently.

## Evidence (observed)
- **21e7932 ruler.** `measure.py` has 257 lines. A grep for `tool_sha256|runner_sha256|TOOL_SHA|RUNNER_SHA|INSTRUMENT|tool_|runner` finds nothing (exit 1), so §6 was accurate there.
- **55e1d31 ruler.** `measure.py` has 410 lines, sha256 `bb651eef…5053`, and equals the worktree file.
  - `:23-24` pin `TOOL_SHA18` and `RUNNER_SHA18`.
  - `witness()` `:192-193` requires `row.get('tool_sha256') == TOOL_SHA18` and `row.get('runner_sha256') == RUNNER_SHA18`.
  - Selftest `:285-286` adds `wrong-tool` and `wrong-runner` mutants, each expected to open exactly `['R18-4']`.
- **Pins match the blobs** (`git cat-file blob 4b7c682:<path> | sha256sum`): `tools/bash-witness-study.py` → `8dfaa25a…3a12` and `tools/mutate-and-run.sh` → `d22c4025…94a8b`. Both equal the pins and the receipt fields.
- **§6's "round18-final-measure.json records no tool hash" (unrecorded dependency) is also stale.**
  - The receipt bytes are unchanged from 21e7932 to 55e1d31 and still have no such field.
  - A new companion, `round18-final-measure-instrument.json`, absent at 21e7932, binds `receipt_sha256 a9536bfb…8a44` (= receipt blob) and `instrument_sha256 7ca87a7c…dd37` (= `4b7c682:.ufo/evidence/round-18/measure.py`).
  - `measurement()` `:212-216` checks it against `MEASURE_SHA18` (`:38`).
- **The lesson integrates the repair** (`55e1d31:corpus/lessons/round-19.md`): `:117-122` "independently re-derived tool/runner hashes" (NegativeControls), `:126-129` AxisBound's companion, `:202-204` Route04/ReceiptIntent. The repair is credited to other seats and SourceS058 is not cited, which is not a defect.
- **Read-only reproduction at 55e1d31.** Python read blobs via `git cat-file`, then compared with `json.loads`/`hashlib.sha256`; the ruler was NOT executed. All checks came back True:
  - argv, revision and integer exit 0; stream paths and digests (stdout `316b9713…20be`, stderr empty `e3b0c442…b855`)
  - `recorded_at` ≥ FREEZE_TIME, which is the 78b99dd committer date (02:28:10-03:00); supersedes list exact
  - stdout byte-equal to `round-18/final/bash-witness.stdout`; old checks.json row still exit 64 with empty-stdout digest
  - measure stdout `55c530bb…0ae8`: 60/60, restraint 8, no overrides; both round-18 erratum phrases present
- **Source re-open.**
  - My own curl at 2026-10-21 06:22:35 GMT: http 200, 728,559 B, etag "67c2470c-b1def", sha256 `d6c175a4…4ede`, equal to the S058 anchor.
  - `pdftotext` p14 starts "79:14". "4.2.2 Verifying Traces" is at normalized offset 3432 and the quote at 3512, once each in raw and layout output; 21 words. Each p15 supporting quote occurs once.
  - The S058 row `awk | sha256sum` is `b95853ec…60c5` at eb7838b, 7243e7f, 21e7932, 55e1d31, e7039fd and the worktree; NF=13 (11 cells). Recheck falls due 2028-10-19.
  - The frozen round-19.md never cites S058, so no used-by log is owed; the report's condition is not met.

## Concrete falsifier
- **Against the report's claim, now.** Per frozen `:192-193` and `:285-286`, a receipt whose `tool_sha256` or `runner_sha256` differs from the pin makes `witness()` false, so R18-4 goes `open` and `--check` exits 1. This comes from reading the code, not running it.
- **Against my disagreement.** An authorized mutation-tester `--snapshot` probe at ruler `bb651eef…5053` would settle it. Start from a pristine passing control and change only `tool_sha256` (or `runner_sha256`) to `'0'*64`. If R18-4 still comes back `corrected` with exit 0, I am wrong. I did not run it; this seat is read-only.

## Other stale items in the report (not new defects)
- **Line cites are from 21e7932** (report → frozen): `receipt()` `:61-76`→`:78-96`, `guard()` `:89-96`→`:139-148`, `source()` `:97-104`→`:149-164`, `arithmetic()` `:105-111`→`:165-182`, `witness()` `:112-120`→`:183-199`, `measurement()` `:121-136`→`:200-222`, PATHS `:30-34`→`:46-51`, `inputs` `:248`→`:401`, mutants `:179-194`→`:279-345`.
- **The §5 fit table is incomplete for the frozen ruler.** It omits the SHA-pinned source snapshots (R18-2/3); `recorded_at`, tally, supersedes and tool pins (R18-4); and the instrument companion (R18-5). Its S058 verdicts (reject for R18-2/3, the count, authenticity) still stand.
- **round-19.md cites carry no revision.** `:23`, `:38-40`, `:67-70` and `:85` hold at 55e1d31. But `21e7932:round-19.md` has only 79 lines, so they were read from an uncommitted draft.

## Residual unknowns
- **QUALITY 21 scope.** `55e1d31:corpus/QUALITY.md:107-109` says: "A retained receipt carries the instrument's sha256 beside it in the same file". R18-5's identity instead sits in a later, separate companion (05:53:30Z versus the receipt's 05:28:25Z). Whether criterion 21, scoped by criterion 20 to wave-executed instruments, governs an L1 replay is UNKNOWN. Neither the report nor round-19.md addresses it. I do not claim it as a defect.
- **Pins are L1 constants.** The ruler does not recompute them from REV18 blobs at run time. Producer and runner identity stay self-reported (`round-19.md:123`, "not producer authentication").
- **Worktree lesson not assessed.** The worktree `corpus/lessons/round-19.md` has uncommitted changes (sha `63f34890…`).

## Scope / no-harm
- **Read:** SourceS058.md and the measure.py, SOURCES, round-19.md, QUALITY 20-24/37-40, credit-note `:1,28` and receipt blobs at 55e1d31, 21e7932 and 7243e7f, plus the round-18 erratum note.
- **Git:** read-only `rev-parse`, `log`, `diff --stat`, `ls-tree`, `cat-file`, `show -s` and `status --porcelain`, all with `--no-optional-locks`, under `env -i PATH=/usr/bin HOME=/tmp/fs058-home`.
- **Scratch:** `/tmp/tameshi-r19-FS058/` (disposable).
- **Not done:** no ruler, selftest or receipt argv executed; no installs.
- **Tools:** curl, poppler, git, python3.
- **Wrote:** this file only. The PDF was treated as data.

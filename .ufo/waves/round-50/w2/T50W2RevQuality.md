# T50W2RevQuality — QUALITY 100 & 101 falsifiers, run as written at `80ea77e9`

Seat: T50W2RevQuality (L1 TameshiR50, wave 2). Everything read at `80ea77e99e239982ab0b93e416645ef2359725d3`;
all runs in scratch `/fast/scratch/hyaku/tameshi-r50/T50W2RevQuality/` against a `git clone -q --shared` of the lane
(toplevel asserted equal to the clone dir before first use). No tool installs (pacman paused; none needed).
Scratch deleted before this report was yielded; the receipts cited below are copies under `.ufo/waves/round-50/w2/`.

Byte-identity of the instruments (no drift between worktree, frozen revision, and receipt):

    sha256sum <lane>/<p> | cut -d' ' -f1  ==  git -C <lane> cat-file blob 80ea77e9:<p> | sha256sum | cut -d' ' -f1

holds for `seat-report-append-only.py`, `receipts/fixture-driver.sh`, `receipts/c100-falsifier.py`,
`.ufo/evidence/round-50/quality/selftest-reach.py`, all four `measure.py` counters (r49+r50, c1+c2) and both
`reach-r*.stdout`. Checker sha256 `cee1a2dddf6ed7a1dcd13cfb2993f491314fa0713b3064d575eed243d8cbce4f` equals
`receipts/00-toolchain.txt` line `checker sha256:`.

## Verified (behavior reproduces the criteria exactly)

Criterion 100 — checker windows (`python3 <checker> <scratch-lane> FROM TO`), every number identical to
`.ufo/waves/round-50/w1/T50ScribeAppendOnly.tool-runs.txt`:

| FROM | TO | SUMMARY | exit | REWRITTEN |
|---|---|---|---|---|
| 487b8f0 | 5891bdb | checked=2819 rewritten=0 | 0 | — |
| c5335c70 | 83beaf98 | checked=2856 rewritten=9 | 1 | 9× round-43 `prefix-lost`, incl. `RevC2Classes.md` |
| edd4ca44 | 03facb22 | checked=3193 rewritten=1 | 1 | `round-47/w1/T47ConnCross.md prefix-lost` |
| 6b5ea3b1 | 03facb22 | checked=3186 rewritten=3 | 1 | draft `deleted`, `build-spec.py`, `T47CritC1Control.md` `prefix-lost` |
| 9b9b2a01 | fc5ac743 | checked=3787 rewritten=2 | 1 | `round-49/build-spec-w2.py`, `T49RevengerLapse.md` `prefix-lost` |
| 65a2215 | 80ea77e9 | checked=3984 rewritten=0 | 0 | — (round-50 adding commit #1) |
| 80ea77e9 | 80ea77e9 | checked=4371 rewritten=0 | 0 | — (the named round-50 window; see INFO-2) |

Round-50 adding commits at `80ea77e9` (git log --diff-filter=A per path): `65a2215` (5 files) and `80ea77e9`
(387 files, all w1 reports + this checker + receipts). Criterion's census sentence (22 pairs / 1165 files /
20 files) matches `T50ScribeAppendOnly.census.txt` governing section verbatim.

- Fixture driver (`receipts/fixture-driver.sh`, 11 cases): rc 0, **16 PASS / 0 FAIL**; exit histogram 3×0, 4×1, 4×2;
  `01-append` prints `SUMMARY<TAB>checked=2<TAB>rewritten=0`; in-place/deleted/truncated/renamed each exit 1 naming
  the right path and reason (`A.md prefix-lost`, `B.md deleted`, `C.md prefix-lost`, `C.md deleted`); cases 08/10/11
  print `ERROR: …` on stderr. Receipt: `T50W2RevQuality.c100-fixture-driver.stdout`.
- Falsifier entry point: `CRITERION-100-FALSIFIER-OK`, exit 0, `mutants recognised as wrong: 3/3`, each mutant
  printing a `FAIL ` line (`prefix-to-length`, `drop-deleted`, `widen-scope` — edits exactly as the criterion
  describes). Only the mktemp fixture hashes differ from the committed `receipts/quality/c100-falsifiers.stdout`.
  Receipt: `T50W2RevQuality.c100-falsifier.stdout`.
- Checker internals match the criterion's mechanics: scope regex `^\.ufo/waves/round-[^/]+/`
  (seat-report-append-only.py:36), `ls-tree -r -z --full-tree` (:67), blob-only reads via `cat-file --batch`
  (:86-146), prefix test `new.startswith(old)` (:187), `deleted` branch (:174), exit 0/1/2 (:199,:216,:223).

Criterion 101 — `python3 selftest-reach.py <counters>` (receipt: `T50W2RevQuality.c101-reach.txt`):

- Round-49 counters: `REACH … selftest=1 calls_measure=0 FAIL` twice, `SELFTEST_REACH: files=2 failed=2`, exit 1 —
  matches committed `reach-r49.stdout`/`reach-r49.exit`.
- Round-50 counters: `calls_measure=2 ok` (C1) and `calls_measure=1 ok` (C2), exit 0 — matches `reach-r50.*`.
- Output line format and exit rules match `selftest-reach.py:37` and `corpus/QUALITY.md:1536-1538`.
- Probe presence: `T50MutC1Counter.md` and `T50MutC2Counter.md` exist at `80ea77e9`; counts match the criterion
  (`QUALITY.md:1533`): C1 29 mutants, 11 killed / 18 survived in phase 1 (`T50MutC1Counter/results.json` len=29);
  C2 28 mutants, 14 killed / 14 survived (`T50MutC2Counter.md` verdict header).
- Path resolution: all 23 paths cited by the two criteria resolve at `80ea77e9` (`git cat-file -e`), and all ten
  named commits resolve (`git rev-parse --verify`): 487b8f0, 5891bdb, c5335c70, 83beaf98, edd4ca44, 03facb22,
  6b5ea3b1, 9b9b2a01, fc5ac743, 506e99c7.
- Lesson quotes check out: `corpus/lessons/round-43-verifier-spotcheck.md:12` (dirty `RevC2Classes.md`,
  "unrelated dirty worktree change" at :64) and `round-47-verifier-spotcheck.md:22` defect 2 (`03facb22` rewrites
  `T47ConnCross.md`); `corpus/lessons/round-50.md` Mistakes row 1 carries the r49 numbers (14 of 28, 9 of 15).

## Findings by severity

**LOW-1 — criterion names a reason token the checker never emits.** `corpus/QUALITY.md:1476` says a non-blob side
is reported as `type-change`; the checker emits `source-not-a-blob` (seat-report-append-only.py:170) or
`target-not-a-blob` (:178). `grep -rn type-change` over the lane's receipts and checker finds nothing. A reader
auditing receipts for the criterion's token finds zero rows. Fix belongs to the criterion author as a dated
erratum (rename the token in text); receipts already use the real tokens. Command:
`git -C <lane> grep -n 'type-change\|not-a-blob' 80ea77e9 -- corpus/QUALITY.md .ufo/waves/round-50/w1/T50ExecAppendOnly`.

**LOW-2 — "the three setup cases exit 2" undercounts.** `corpus/QUALITY.md:1517-1518`; the driver has FOUR exit-2
cases: fixture-driver.sh:114 (`08-bad-rev`), :118 (`09-missing-arg`), :123 (`10-non-repo`), :128 (`11-missing-lane`).
My run's exit histogram is 3×0 / 4×1 / 4×2 across the 11 cases. The tool is stricter than the text; no behavior
defect. Command: `grep -c $'\t2' <receipts>/fixture/*.exit` (or see driver stdout receipt).

**LOW-3 — bad-arguments refusal does not print `ERROR: …`.** `corpus/QUALITY.md:1491-1492` says every setup refusal
is "exit 2 with an `ERROR: …` line on stderr"; the argc≠4 path writes a bare usage line
(seat-report-append-only.py:198-199), visible in my case `09-missing-arg.stderr`. The other three refusal kinds do
print `ERROR: …` (:216). Command: `cat <receipts>/fixture/09-missing-arg.stderr`.

**INFO-1 — `checked=0` really does exit 0.** `SUMMARY checked=0 rewritten=0`, exit 0, from the root commit as FROM
(even with 4371 wave files at TO). `QUALITY.md:1492`'s "refusal-shaped result, not a pass" is reader guidance only;
nothing in the tool enforces it. The adding-commit rule mitigates; a closure harness could additionally assert
`checked>0`. Command: `python3 <checker> <lane> 40f8e1f3 40f8e1f3`.

**INFO-2 — the named round-50 window is tautological today and a third adding commit now exists.** FROM=TO=`80ea77e9`
compares identical trees (pass is real but carries no discrimination until TO advances). At the current lane tip,
`4efa5cf` (wave-2 spec/dispatch) is a distinct round-50 adding commit:
`git -C <lane> log --oneline 80ea77e9..4efa5cf -- .ufo/waves/round-50/` → `4efa5cf`. The closure battery must run
A ∈ {65a2215, 80ea77e9, 4efa5cf} → landing tip. Out of my mandate (TO fixed at `80ea77e9`), so not run here.

**INFO-3 — the probe-presence half of criterion 101 is not machine-checked.** `selftest-reach.py` implements only
the reach half (:24-41); "plus the presence of a mutation-probe report" is a manual step. Presence holds (both
probe reports at `80ea77e9`). "The round's lesson names the survivors" is satisfied via the round-49 survivors in
`corpus/lessons/round-50.md` Mistakes row 1; round-50's own per-mutant survivor lists live in the probe reports.
Command: `git -C <lane> show 80ea77e9:.ufo/evidence/round-50/quality/selftest-reach.py | grep -n 'probe\|mut'` → empty.

**INFO-4 — "can still miss most mutants" is exact for C1, loose for C2.** C1: 18/29 survived (62%) — "most" holds;
C2: 14/28 survived (exactly half). The stated numbers (`QUALITY.md:1533`) are correct under the killed-reading;
wording nit only.

## Residual risk / verification gaps

- Nothing after `80ea77e9` was compared (mandate fixed TO); `4efa5cf` and any landing/wrap-up commits are the L1's
  closure runs, which must use each distinct adding commit as FROM.
- The non-blob (`type-change`) branch is unexercised by any fixture, mutant, or receipt — no gitlink case in the
  driver; behavior known only from code (LOW-1 is about the name, not the discrimination).
- Census counts are pinned to its tip `4afb060` (round-50 w1 uncommitted then); the criterion cites the receipt, so
  this is provenance, not drift.
- LOW-1..3 fixes are errata on `corpus/QUALITY.md`; I am read-only on it (append-only lane rule, not my file).

## Receipts (copies in `.ufo/waves/round-50/w2/`)

- `T50W2RevQuality.c100-windows.txt` — all nine window runs (SUMMARY + REWRITTEN lines)
- `T50W2RevQuality.c100-fixture-driver.stdout` — driver: 16 PASS / 0 FAIL
- `T50W2RevQuality.c100-falsifier.stdout` — `CRITERION-100-FALSIFIER-OK`, 3/3 mutants caught
- `T50W2RevQuality.c101-reach.txt` — reach runs, r49 rc=1 / r50 rc=0

Tool installs this seat: none.

## Summary

- Every falsifier behaves exactly as its criterion receipt claims: 5 named windows byte-identical to
  `T50ScribeAppendOnly.tool-runs.txt`; round-50 window (80ea77e9→80ea77e9) and 65a2215→80ea77e9 clean (4371/3984
  checked, 0 rewritten); driver 16 PASS/0 FAIL; falsifier OK exit 0; reach r49 FAIL×2 exit 1, r50 ok×2 exit 0.
- All 23 cited paths and 10 commits resolve at 80ea77e9; instruments byte-identical to frozen blobs and receipt sha.
- 3 LOW text-vs-tool defects in QUALITY.md itself: `type-change` token never emitted (checker says
  source/target-not-a-blob); "three setup cases" vs four; bad-arguments refusal prints usage, not `ERROR:`.
- 4 INFO: checked=0 exits 0; the named r50 window is tautological until TO advances and 4efa5cf adds a third
  adding commit for closure; probe-presence not machine-checked; "miss most mutants" loose for C2.
- No tool behavior defect found; all fixes are criterion-text errata owned by the criterion author.

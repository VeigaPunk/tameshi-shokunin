# tameshi round 78 — lesson (hyaku run 15)

Lane: tameshi-shokunin. Round: 78 (attempt 1), 2026-11-04. Base:
`5bcb13ea7cc08bb0b594fcd0c2bb770cb8fe64a0` (= `origin/master`, the round-77
non-author closure verdict commit). Frozen plan: `plans/round-78.plan.md`
(declaration `c1c220d475a04aa0e9c28be4f632c03e20d30116`). Two claims on
distinct axes: R78-C1 operability, a **capability acquisition** (a non-Python
instrument can carry a live freshness row) and R78-C2 coverage (the two
survivors the round-77 wave named become fixture coverage). Round 78 is the
capability round the stagnation nudge directs: rounds 75, 76 and 77 entered no
capability row, so the window (N = 2) was full at round start.

## What was measured — R78-C1

- Base (`5bcb13ea`), base manifest: `SELFSTATE: rows=20 match=18 stale=2
  unexpected=0`, exit 0 (`.ufo/evidence/round-78/c1-base-sweep.txt`).
- Do-nothing control (the BASE runner bytes plus the NEW manifest row): the
  hardcoded `['python3', '-I', '-X', 'utf8', dest]` prefix cannot execute a
  bash script, so the row's stdout carries no figure:
  `SELFSTATE error=setup figure-absent:mutation-runner-selftest`, exit 2, no
  summary (`.ufo/evidence/round-78/c1-control-bash-row-on-base-runner.txt`).
- Landed: `INTERPRETERS = {'python': ('python3','-I','-X','utf8'), 'bash':
  ('bash',)}`, an undeclared interpreter defaulting to python, an unknown name
  refused before any row effect, and the row `mutation-runner-selftest`
  (`mutation sweep runner`, figure `MUTATE_SELFTEST: \d+/\d+ pass`, instrument
  `tools/mutate-and-run.sh` at the base revision, argv `--selftest`,
  interpreter `bash`).
- After: `SELFSTATE_ROW mutation-runner-selftest capability=mutation sweep
  runner expect=match measured=match ok doc_figure=MUTATE_SELFTEST: 107/107
  pass measured_figure=MUTATE_SELFTEST: 107/107 pass instrument_exit=0`;
  `SELFSTATE: rows=21 match=19 stale=2 unexpected=0`, exit 0
  (`.ufo/evidence/round-78/c1-landed-sweep.txt`).
- `SELFSTATE_SELFTEST: 13/13 pass` exit 0
  (`.ufo/evidence/round-78/c1-landed-selftest.txt`), with arm 12 (unknown
  interpreter refused) and arm 13 (a `bash` row executed from extracted bytes
  by the real CLI against a git fixture, then a second invocation on the same
  fixture asserting that a python-defaulted row on the same path/rev/argv is
  refused `figure-absent:toy-python` — the row cache is keyed by the
  interpreter too; the declared design bytes had omitted it and the round's
  reviewer reproduced the bypass, receipt `.ufo/evidence/round-78/c1-cache-kill.txt`
  and the exact mutant `c1-cache-kill-mutant.py`: `12/13` with arm13 FAIL).
  The instrument's docstring had said "Nine arms" while the suite ran eleven;
  the count line now states the true list — see `## Mistakes` 2.
- Sourced on **S306** (GNU Bash manual, *Invoking Bash*, opened this round).

## What was measured — R78-C2

- Base: `WAVE_RECONCILE_SELFTEST: 20/20 pass` exit 0
  (`.ufo/evidence/round-78/c2-base-selftest.txt`).
- Do-nothing control (the round-78 10-defect spec on BASE bytes): `MUTATE: DONE
  (target=wave-reconcile-base-control-r78 defects=10 killed=8 survived=2
  inconclusive=0 kill-rate=80%)`, the two survivors exactly
  `git-listing-uses-head` and `arm20-cleanup-removed`, `CONTROL: GREEN`,
  restore byte-identical `sha256 67d3a4cc2e75…`
  (`.ufo/evidence/round-78/c2-base-control-battery.txt`).
- Landed: arm20 scans the scratch parent for `wave-reconcile-git-*` entries
  before and after its fixture and returns `leak:<n>` when a fixture survives
  its cleanup; arm21 builds a TWO-commit fixture (rev1: `report.md` "1 seat
  report" + `wave/one.md`; rev2 = HEAD adds `wave/two.md`) and measures at
  rev1, so a HEAD-resolving listing drifts. `SELFTEST_ARMS` 20 → 21.
- After: `WAVE_RECONCILE_SELFTEST: 21/21 pass` exit 0
  (`.ufo/evidence/round-78/c2-landed-selftest.txt`); battery `CONTROL: GREEN`,
  `MUTATE_RESTORE: OK` byte-identical (`sha256 f534225f0cbd…`), `MUTATE: DONE
  (target=wave-reconcile-arms-r78 defects=10 killed=10 survived=0
  inconclusive=0 kill-rate=100%)`
  (`.ufo/evidence/round-78/c2-landed-battery.txt`, per-defect streams under
  `.ufo/evidence/round-78/battery/`).
- Kill matrix: `m2` → arm13+arm16; `span-rule-removed` → arm14+arm17+arm18;
  `seat-reports-any-depth` → arm15+arm20; `mc-record-bound` → arm16;
  `roles-bypass` → arm17; `attack-bypass` → arm18; `adv-seatreports-…` →
  arm19; `git-listing-recursion-removed` → arm20+**arm21** (new intrinsic
  collateral, disclosed: a non-recursive listing of the two-commit fixture also
  counts zero top-level reports); `git-listing-uses-head` → arm21 only;
  `arm20-cleanup-removed` → arm20 only.
- Sourced on **S091** (gitrevisions, re-opened this round for the revision-name
  ground: `HEAD` is one spelling of a revision parameter, so a listing given a
  rev must resolve that rev).

## Gate

New row this round (opened 2026-11-04):

- **S306 — GNU Bash Reference Manual, *Invoking Bash*
  (https://www.gnu.org/software/bash/manual/html_node/Invoking-Bash.html)**,
  fetched 2026-11-04 (HTTP date `Wed, 04 Nov 2026 05:50:32 GMT`, HTTP/1.1 200,
  12,377 B, sha256
  `ea86a64cd2d2cbc338fa911c73bcf81aac23da1910d54ba8ab76c20f5d0497c4`,
  snapshot `.ufo/evidence/round-78/sources/s306-bash-invoking.html`, headers
  `s306.headers`). Located quote: "Bash reads and executes commands from this file, then exits."
  (10 words, page line 249); the file-argument context is the paragraph at
  page lines 242-249. Tier A, status `mined`, recheck 180d, `used-by
  corpus/lessons/round-78.md`.

Re-opened row (same round, old → new logged):

- **S091 — gitrevisions (Git documentation)**, re-opened 2026-11-04 (05:50:32
  GMT): `https://git-scm.com/docs/gitrevisions`, HTTP/2 200, 74,654 B, sha256
  `1ab7124a99e6919e6882be82f77c629ac8fe623bb36af56a749fd4db1919070b`,
  snapshot `.ufo/evidence/round-78/sources/s091-gitrevisions.html`, headers
  `s091.headers`. Located quotes: "Here are various ways to spell object
  names." (8 words, page line 2157) and "names the commit on which you based
  the changes in the working tree." (13 words, page line 2225, the `HEAD`
  definition; the `HEAD` label is page line 2223). Scope, anchor, `opened` date
  and status stand as written; `used-by` old → new:
  `corpus/knowledge/oracle-anchored-survivors.md` → the same plus
  `corpus/lessons/round-78.md`.

Rejected (recorded, no id): a kernel.org mirror of the same `gitrevisions`
manual (https://mirrors.edge.kernel.org/pub/software/scm/git/docs/gitrevisions.html,
fetched 2026-11-04, 53,827 B) — refused as a second row because the canonical
URL answers with the same document and the same quote: same document, so one
row (the round-75/76 within-scope-duplicate precedent). Flip: the canonical
URL stops serving the document.

Assimilation: `Assimilation: none` — the staged package
(`/home/vgpnk/Projects/shokuknow/merge/tameshi/`) was searched for both
grounds; the verdict and its searches are in the round report's Sources &
frontier section (connector seat `T78W1CN1`).

## Mistakes

1. **class registry-row-without-its-round-entry · evidence pointer
   `corpus/SOURCES.md` at `c1c220d4`: S305 exists (round 77) and the per-round
   log jumps from round 76 to nothing for round 77 · captured-by: none (the
   census validates rows and not the round log, so a registry-clean file hides
   the gap) · fix: append-only round-77 correction entry written this round
   (SOURCES.md), and criterion 129 — a round that appends a registry row
   writes that round's log entry in the same commit; a census-clean registry
   whose newest row has no round entry is a conformance defect.**
2. **class docstring-count-drift · evidence pointer
   `tools/selfstate-freshness.py` at `5bcb13ea`: the module docstring said
   "Nine arms" while `SELFTEST_ARMS = 11` and the suite ran 11 · captured-by:
   none (nothing asserts the docstring against the constant) · fix: the
   docstring now enumerates the 13 arms the widened suite runs, and the
   selftest's own `ok == total == SELFTEST_ARMS` binding keeps the count
   honest; the remaining gap (docstring text still unasserted) is named in the
   round report, not waved off.**

3. **class plan-cites-an-absent-receipt · evidence pointer
   `plans/round-78.plan.md` cites `.ufo/evidence/round-78/c2-base-control-battery.txt`
   while `git cat-file -e c1c220d4:.ufo/evidence/round-78/c2-base-control-battery.txt`
   exits 128 at the declaration commit (round-78 critic `T78W1C1`, confirmed by
   the L1) · captured-by: none at the freeze (the control WAS run before the
   freeze; only its stdout landed later) · fix: the receipt is committed with
   the round's records commit and the executor seat `T78W1E3` re-ran the same
   control on base bytes in a clone (killed=8, survived=2, survivors exactly
   the two round-78 defects); the rule for round 79 is that a frozen plan cites
   only receipts its own commit carries, or says in the plan which receipt
   lands later and why.**

## Wave findings (adopted)

Twelve seats under `scripts/hyaku/ufo-wave-policy.json` band 8–16 (3 executor,
1 scribe, 1 scout, 2 reviewer, 1 critic, 1 mutation-tester, 1 connector,
1 sentinel, 1 simplifier; attack 4 = 33.3 %). Every finding below is adopted
into the record, not argued away (`.ufo/waves/round-78/w1/`):

- **The declared C1 design had a cache-key hole** (`T78W1R1`, `T78W1C1`, and
  independently `T78W1E2` and the connector): the row cache was keyed
  `(rev, path, argv)`, so a `bash` row's stdout could satisfy a python-defaulted
  row on the same path/rev/argv — the python row was certified without being
  executed. The L1 fixed it (interpreter in the key; a non-string interpreter is
  a setup refusal). The fix first landed as a 14th arm; the reviewer voted FAIL
  because the frozen kill rule (iii) names `13/13` and the suite printed
  `14/14`. The L1 folded the assertion into arm13
  (`ARM13_bash_interpreter_row_and_cache`) instead of adding an arm, so the
  frozen count holds literally. The reviewer re-measured the final bytes and
  voted PASS; its pre-fold FAIL is retained in its report. Receipts:
  `.ufo/evidence/round-78/c1-cache-kill.txt` (mutant → `12/13`, arm13 FAIL,
  `cache rc=0`), `c1-cache-kill-mutant.py`, `c1-landed-selftest.txt` (`13/13`).
- **The plan cited a receipt its declaration commit did not carry**
  (`T78W1C1`): `git cat-file -e c1c220d4:.ufo/evidence/round-78/c2-base-control-battery.txt`
  exits 128. The control was run before the freeze (killed=8 survived=2) but its
  stdout was committed only in the records commit; `T78W1E3` re-ran the same
  control on base bytes in a clone and reproduced `survived=2` with exactly the
  two round-78 defects. See `## Mistakes` 3.
- **No-harm monitor coverage corrected** (`T78W1C1`): the documented arms diff
  covers arms 1–19 only; arm20's outcome (`meet` at base and landed) is asserted
  separately and arm21 is new. The monitor sentence is restated, not widened
  after data.
- **The "no other counter" sentence is too strong** (`T78W1C1`): C1's row reads
  `MUTATE_SELFTEST` from `tools/mutate-and-run.sh` and C2's battery uses the same
  runner as its harness. Neither reads the other claim's files; both depend on
  the mutation runner. Recorded as the corrected separability sentence.
- **The nudge sentence contradicted itself** (`T78W1C1`): the plan said "the
  lowest-axis obligation is not waived" while the nudge was ACTIVE. Corrected:
  the nudge waives the lowest-axis obligation this round; C2 works coverage
  anyway because two axes were wanted.
- **Both after-states are guard sets** (`T78W1C1`, the round-77 admission
  class): C1's natural scalar is "registered counter-defects surviving the
  interpreter/cache surface: 1 → 0" (the cache mutant survives the declared
  design 13/13, dies 12/13 after the fold); C2's is "surviving registered
  defects: 2 → 0". The rest are guards frozen in the plan.
- **Independent rebuilds agree** (`T78W1E1`, `T78W1E2`, `T78W1E3`): E1's own
  two-commit arm21 reads `meet` pristine / `drift` under its own head-mutant
  (21/21 vs 20/21); E2's own widening reproduces `rows=21` with the bash row
  match and the base-runner control refusal; E3 re-ran both counters on a clone
  of the declaration commit, and both counters move when their work is reverted
  to base (C1: exit 2 `figure-absent`; C2: `survived=2`).
- **Named survivors for round 79** (`T78W1M1`, `T78W1SC1`): the leak detector is
  a nested closure and `return set()` survives 21/21 (the round's own new guard
  is unguarded — a positive-control arm is the fix); dropping `-I` from the
  python tuple survives (no arm distinguishes interpreter isolation); arm21's
  `HEAD != rev` self-guard removal survives (equivalent-ish, but it would let a
  fixture bug silently disarm the arm). The scout's table lists 9 selfstate and
  11 wave-reconcile unprotected rules with a measured single-edit mutant each
  (`.ufo/waves/round-78/w1/T78W1SC1.md` §1) and a bounded 3-item data-walk.
- **Registry quotes corrected** (`T78W1S1`): the applied S306 teaches cell used
  a 14-word sentence that crosses a raw-HTML line break (not a byte substring);
  the row now carries the single exact line-249 quote (10 words) and the S091
  gateway quotes are 8 and 13 words. The `HEAD` label is page line 2223.
- **Assimilation: none** (`T78W1CN1`): searches A/B/B_precise/B_lifecycle over
  `/home/vgpnk/Projects/shokuknow/merge/tameshi/` establish no entry on the
  frozen-interpreter freshness capability or the leak/pinned-rev fixture ground;
  the nearest in-province entries are named in its report. Its id check reads
  registry=166, staged=103, **8 collisions** — a future adoption needs
  renumbering by document; nothing was appended.
- **The leak post-condition was not concurrency-safe** (`T78W1S2` P1): scanning
  `tempfile.gettempdir()` for `wave-reconcile-git-*` entries makes two
  `--selftest` runs that share an ambient `TMPDIR` see each other's live fixture
  and report a spurious `leak:1`. Measured: four concurrent runs on the pre-fix
  bytes (commit `6f532752`) fail 4/4 with `leak:2`/`leak:3`; the landed
  per-fixture check (`if os.path.exists(fix)` after the `finally`) passes 4/4
  and leaves zero leftovers, with the battery matrix byte-for-byte unchanged
  (`.ufo/evidence/round-78/c2-concurrency-prepost.txt`).
- **The manifest note and the docstring still carried stale counts**
  (`T78W1S2` P4): the note said "17 declared rows" while the file carried 20 at
  base and 21 now (criterion 122), and the docstring still said "Nine arms / no
  git, no lane subprocess" while arms 11 and 13 drive the real CLI against a git
  fixture. Both are corrected in the landed bytes; the note no longer carries a
  count.
- **One new clause stays unverified**: deleting `isinstance(interp, str)` from
  the manifest check leaves the suite `13/13` green (`T78W1S2`). It is kept — it
  converts a `TypeError`/exit-1 path into a typed exit-2 refusal — and named
  here as an unguarded clause for round 79, because covering it would need a
  fifteenth arm and the frozen kill rule names `13/13`.
- **Declined refactors**: the simplifier's builder de-duplication (P2/P3, one
  `_cli_fixture` and one git-fixture builder) is not required by any frozen
  predicate; the duplication is disclosed and carried to round 79 rather than
  landed after the wave without its own re-measurement.
- **Containment** (`T78W1SN1`): the tool → instrument boundary (path/argv/rev/
  cwd) is confirmed; ordinary-exception cleanup leaves 0 leftovers per arm;
  with TMPDIR unset the instruments write to the platform default (the
  scratch-root contract's declared behaviour), and universal containment under
  SIGKILL is unprovable from `finally` blocks — named, not claimed.


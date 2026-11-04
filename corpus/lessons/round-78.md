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
  by the real CLI against a git fixture). The instrument's docstring had said
  "Nine arms" while the suite ran eleven; the count line now states the true
  list — see `## Mistakes` 2.
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
  `s306.headers`). Located quotes: "the first argument is treated as the name
  of a file containing shell commands" (14 words, page line 245) and "Bash
  reads and executes commands from this file, then exits." (11 words, page
  line 249). Tier A, status `mined`, recheck 180d, `used-by
  corpus/lessons/round-78.md`.

Re-opened row (same round, old → new logged):

- **S091 — gitrevisions (Git documentation)**, re-opened 2026-11-04 (05:50:32
  GMT): `https://git-scm.com/docs/gitrevisions`, HTTP/2 200, 74,654 B, sha256
  `1ab7124a99e6919e6882be82f77c629ac8fe623bb36af56a749fd4db1919070b`,
  snapshot `.ufo/evidence/round-78/sources/s091-gitrevisions.html`, headers
  `s091.headers`. Located quotes: "A revision parameter <rev> typically, but
  not necessarily, names a commit object." (13 words, page line 2155) and
  "names the commit on which you based the changes in the working tree." (12
  words, page line 2225, the `HEAD` definition). Scope, anchor, `opened` date
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

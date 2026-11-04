# tameshi round 77 — lesson (hyaku run 15)

Lane: tameshi-shokunin. Round: 77 (attempt 1), 2026-11-04. Base:
`ac6baf7a46df613b171b4c1ab834c888cd6321b9` (= `origin/master`, the round-76
non-author closure verdict commit). Frozen plan:
`plans/round-77.plan.md` (declaration `d39be4b0`). Two claims on distinct
axes: R77-C1 operability (the round-76 recursion survivor becomes arm20 of
`tools/wave-reconcile.py`) and R77-C2 calibration (the cold-read credit the
record claims is the monitor's reading at the revision the record names).

## What was measured — R77-C1

- Base `tools/wave-reconcile.py` sha256
  `ca05ec154454d57902313dcddd3c1e6980628bb352f57344afdcd820db5767e3`,
  selftest `WAVE_RECONCILE_SELFTEST: 19/19 pass`; the
  `git-listing-recursion-removed` mutant (drop `-r` in `GitReader.listing`)
  also reads `19/19 pass` on base bytes — the do-nothing control
  (`.ufo/evidence/round-77/base-survivor-r77.txt`).
- Landed: `SELFTEST_ARMS` 19 → 20, arm20 builds a real git fixture and
  measures the production reader; sha256
  `67d3a4cc2e75ef7211a8588e43dcaf3874aaec66c3eea1d59a2b43b5a35e4e84`;
  `WAVE_RECONCILE_SELFTEST: 20/20 pass` exit 0
  (`.ufo/evidence/round-77/c1-landed-selftest-wr.txt`, whose header carries the
  measured rev and tool sha — round-76 closure §6.2 paid).
- Battery on the landed bytes: `CONTROL: GREEN`, eight defects all `KILLED`,
  `MUTATE_RESTORE: OK` byte-identical,
  `MUTATE: DONE (target=wave-reconcile-arms-r77 defects=8 killed=8
  survived=0 inconclusive=0 kill-rate=100%)`
  (`.ufo/evidence/round-77/c1-landed-battery.txt`). Landed kill matrix:
  `m2` → arm13+arm16; `span-rule-removed` → arm14+arm17+arm18;
  `seat-reports-any-depth` → arm15+arm20; `mc-record-bound` → arm16;
  `roles-bypass` → arm17; `attack-bypass` → arm18; `adv-seatreports-…` →
  arm19; `git-listing-recursion-removed` → arm20 only — exactly the frozen
  matrix.
- Sourced on **S305** (new row, opened this round): git's own `git-ls-tree`
  page — `-r` "Recurse into sub-trees." (page line 1664) and "directory name
  (without -r) will behave differently" (page lines 1631-1632).

## What was measured — R77-C2

- Before at base: `COLDREAD_PORTABLE rev=ac6baf7a46df credited=63/65
  elapsed=2.7s probe_sampled=20 probe_mismatches=0`; the `--out` JSON measures
  `sections_covered=63 sections_total=65 box3_full_page=false` with the two
  uncredited headings `## Standing rules` and `## Mutation-sweep recipe —
  numbered steps; bounded cold-read evidence`, both `input-drift` on
  `LOG.md`, `SCORECARD.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`,
  `tools/registry.json`, `PROVINCE.md`
  (`.ufo/evidence/round-77/coldread-base-r77.json`).
- The record it corrects: the round-76 block says `credited=65/65` "at the
  landing tip (`b2b0f82a`)"; `b2b0f82a` is the last rekey batch, the tip is
  two record commits later, and the tip reading is `63/65`.
- After: one settlement batch at the content tip `1d91c384` covering exactly
  the monitor's 14 uncredited sections (`REBIND OK sections=14
  entries_added=14`, ledger 930 → 944), measured at the settlement commit
  `29a1a7d0`: `COLDREAD_PORTABLE rev=29a1a7d0a198 credited=65/65` with
  `sections_covered=65 sections_total=65 box3_full_page=true`
  (`.ufo/evidence/round-77/coldread-after-r77.json`). The records commit that
  follows this paragraph appends `SCORECARD.md`/`LOG.md` — two pinned inputs —
  so a second, small settlement batch re-settles the sections it stales, and
  that second batch is the round's last lane commit.

## Gate

New row this round (opened 2026-11-04):

- **S305 — Git `git-ls-tree` (https://git-scm.com/docs/git-ls-tree)**,
  fetched 2026-11-04 (HTTP date `Wed, 04 Nov 2026 05:16:07 GMT`, 39,083 B,
  sha256 `ff06fbc8b15b0fee505a259e4dc54096c9fba0460f4f02b449d55ecce7818267`,
  snapshot `.ufo/evidence/round-77/sources/s305-ls-tree.html`). Located
  quotes: `-r` "Recurse into sub-trees." (page line 1664, 4 words); "directory
  name (without -r) will behave differently" (page lines 1631-1632, 8 words).
  Tier A, status `mined`, recheck 365d, `used-by corpus/lessons/round-77.md`.
- **Rejected row (recorded, no new id):** the same page was already read at
  round 60 (S292's scope note says "the git-ls-tree page does not enumerate the
  octal modes") but never registered; a second row for the *mode* ground would
  be a within-scope duplicate of S291/S292, so only the recursion ground is
  registered, under S305. Flip: S305 retired or the page superseded.
- Assimilation: see the connector's verdict recorded in the round report
  (`Assimilation: none` when the package holds no entry on this round's
  claims).

## Mistakes

1. **class record-runs-ahead-of-artifacts · evidence pointer
   `SCORECARD.md`/`LOG.md` round-76 blocks ("credited=65/65 at the landing tip
   (`b2b0f82a`)") vs the monitor's `63/65` at the true tip `ac6baf7a` ·
   captured-by: none at round 76 (criterion 128 is written this round; the
   round-76 closure routed the defect without a criterion) · fix: criterion
   128 — a settlement's restored credit is measured at the settlement commit,
   records never name a pre-settlement revision as the tip, and content edits
   all precede the last settlement batch (new evidence paths never stale a
   blob-level pin).**

Why it happened: round 76 landed its four rekey batches and then appended two
record commits that touched `SCORECARD.md` and `LOG.md`, both pinned inputs of
the two newest ledger entries. The rekey's `REBIND OK` was true at its own
pin; the record's sentence then named that pin as "the tip". The monitor was
never wrong — the record named the wrong revision.

## Findings and carries

- The two bash-instrument gaps stay carried: `bash tools/mutate-and-run.sh
  --selftest` prints `MUTATE_SELFTEST: 107/107 pass` and `--regression` prints
  `REGRESSION: PASS (cases=10 …)`, but `tools/selfstate-freshness.py`
  executes instruments as `python3 -I -X utf8`, so a bash instrument cannot
  become a live row. Widening the runner needs its own before/after and a
  frozen tuple table (criterion 127); it does not fit this round's claim cap.
- 17 of the 44 `--selftest`-carrying tools still have no `tools/registry.json`
  row (re-derived this round; see the executor seat's receipt). Carried for
  the same reason.
- Round 77 landed no capability row (C1 is an arm on an existing capability,
  C2 is a settlement on an existing run-book), so a capability-less third
  round sits at the stagnation window boundary and the nudge fires for round
  78: round 78 should be a capability round.
- The cold-read monitor's two ledgers: `measure.py`'s default path resolves
  `.ufo/evidence/round-18/coldread/ledger.json` (a 1.2 MB historical copy),
  while the live ledger is `.ufo/evidence/round-21/coldread/ledger.json`
  (51.7 MB). Reading the historical default gives `11/65`; the lane's own
  `tools/coldread-precheck-portable.py` reads the live one. Any counting
  command that names `measure.py` without `--ledger-rev` measures the wrong
  population — the round's counter uses the portable precheck and says so.

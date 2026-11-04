# tameshi round 79 — lesson (hyaku run 15)

Lane: tameshi-shokunin. Round: 79 (attempt 1), 2026-11-04. Base:
`0cac8e4604e01ff2e2bc0813c745c99d928b5dd5` (= `origin/master`, the round-78
non-author closure verdict commit). Frozen plan: `plans/round-79.plan.md`
(declaration `92c007052cdd9503ef32de8f901c0a4805049e28`). Three claims on
distinct axes: R79-C1 calibration + capability acquisition (a receipt's
recorded tool bytes exist in a revision the receipt names), R79-C2 coverage
(the two survivors the round-78 wave named become fixture coverage), R79-C3
operability (the selfstate runner's `-I` is load-bearing).

## What was measured — R79-C1

- Base (`0cac8e46`), the candidate instrument over the round-78 receipt
  population: `RECEIPT_BIND: receipts=12 bound=4 corrected=0 unbound=8`, exit
  1; the eight unbound receipts are `c1-cache-kill`, `c1-landed-selftest`,
  `c1-landed-sweep`, `c2-concurrency-prepost`, `c2-landed-battery`,
  `c2-landed-selftest`, `standing-sweep-ss-r78`, `standing-sweep-wr-r78`, each
  `detail=bytes-rev-absent` (`.ufo/evidence/round-79/c1-base-sweep.txt`).
- The do-nothing control is the same population with no correction line: the
  base reading above (adding nothing cannot reach the after-state).
- Landed: `tools/receipt-bytes-bind.py` (declared population; `bound` /
  `corrected` / `unbound` states; setup exit 2 before any row effect) and eight
  append-only `# measured_bytes_rev:
  091d50e47bfea5a38d97671934ae0127ef760edc` lines, one inserted after each
  receipt's `# tool_sha256:` line. `091d50e4` is the earliest commit whose
  `tools/selfstate-freshness.py` / `tools/wave-reconcile.py` blobs equal the
  recorded shas (`7edecba8…` / `f8071c8a…`).
- After: `RECEIPT_BIND: receipts=12 bound=4 corrected=8 unbound=0` exit 0
  (`.ufo/evidence/round-79/c1-landed-sweep.txt`); `RECEIPT_BIND_SELFTEST:
  10/10 pass` exit 0 (`.ufo/evidence/round-79/c1-selftest.txt`). The
  false-correction control (one correction flipped to `6f532752…`, whose blob
  differs) reads `receipts=12 bound=4 corrected=7 unbound=1` exit 1 with
  `detail=bytes-rev-mismatch` (`.ufo/evidence/round-79/c1-false-correction.txt`).
- Sourced on **S289** (git-cat-file, re-opened this round for the
  `blob <rev>:<path>` binding ground).

## What was measured — R79-C2

- Base: `WAVE_RECONCILE_SELFTEST: 21/21 pass` exit 0
  (`.ufo/evidence/round-79/c2-base-selftest.txt`).
- Do-nothing control: the landed tool with the two new arm registrations
  removed (suite 21/21) scored by the frozen 12-defect spec → `MUTATE: DONE
  (target=wave-reconcile-control-r79 defects=12 killed=10 survived=2
  inconclusive=0 kill-rate=83%)`, survivors exactly `leak-detector-blind` and
  `head-guard-removed`, `CONTROL: GREEN`, restore byte-identical
  (`sha256 25df7bd78eae…`) (`.ufo/evidence/round-79/c2-control-battery.txt`).
- Landed: `_leftover(path)` extracted (both branches measured by arm22),
  `_build_listing_fixture(fix, mode, second_commit=True)` extracted with the
  `git-fixture-head-equals-rev` refusal measured by arm23, `SELFTEST_ARMS` 21 →
  23, spec 10 → 12 defects (the `arm20-cleanup-removed` anchor gained the arm20
  cleanup comment line to stay unique after the refactor; the edit it performs
  is unchanged).
- After: `WAVE_RECONCILE_SELFTEST: 23/23 pass` exit 0
  (`c2-landed-selftest.txt`); battery `CONTROL: GREEN`, `MUTATE_RESTORE: OK`
  byte-identical (`sha256 cdbc4c05dffb…`), `MUTATE: DONE
  (target=wave-reconcile-arms-r79 defects=12 killed=12 survived=0
  inconclusive=0 kill-rate=100%)` (`c2-landed-battery.txt`). Kill matrix: the
  eight base defects keep their arms (m2 → arm13+16; span-rule → arm14+17+18;
  seat-reports-any-depth → arm15+20; mc-record-bound → arm16; roles-bypass →
  arm17; attack-bypass → arm18; adv-seatreports → arm19;
  git-listing-recursion-removed → arm20+21; git-listing-uses-head → arm21;
  arm20-cleanup-removed → arm20), and the two new mutants die on arm22 only and
  arm23 only.
- Sourced on **S305** (git-ls-tree, re-opened this round for the `-r`
  recursion ground the arm20 fixture measures).

## What was measured — R79-C3

- Base: `SELFSTATE_SELFTEST: 13/13 pass` exit 0
  (`c3-base-selftest.txt`). The do-nothing control is the BASE tool bytes
  scored by the frozen one-defect spec: `MUTATE: DONE
  (target=selfstate-control-r79 defects=1 killed=0 survived=1 inconclusive=0
  kill-rate=0%)`, survivor `python-isolation-dropped`, `CONTROL: GREEN`,
  restore byte-identical (`sha256 7edecba8b9c6…`) (`c3-control-battery.txt`).
- Landed: arm14 runs the real CLI against a git fixture whose python
  instrument prints `TOY_ISO: 1/1 pass` iff `sys.flags.isolated`, so the frozen
  `('python3', '-I', '-X', 'utf8')` tuple measures `match` and a tuple without
  `-I` measures `stale`; `SELFTEST_ARMS` 13 → 14 and
  `tools/selfstate-freshness-mutants.spec` (new) is the standing battery.
- After: `SELFSTATE_SELFTEST: 14/14 pass` exit 0 (`c3-landed-selftest.txt`);
  battery `MUTATE: DONE (target=selfstate-arms-r79 defects=1 killed=1
  survived=0 inconclusive=0 kill-rate=100%)`, the mutant's FAIL set exactly
  `ARM14_python_isolation_tuple`, `CONTROL: GREEN`, restore byte-identical
  (`sha256 4c8c4174cd2f…`) (`c3-landed-battery.txt`).
- Sourced on **S307** (Python 3.15 `using/cmdline.html`, the `-I`
  isolated-mode ground; opened this round).

## Gate

New row this round (opened 2026-11-04):

- **S307 — Python 3.15, Command line and environment
  (https://docs.python.org/3.15/using/cmdline.html)**, fetched 2026-11-04
  (HTTP date `Wed, 04 Nov 2026 06:32:17 GMT`, 171,073 B, sha256
  `18de854cfac544da30b7133ab8eaa3218c419b20983e8ea927745cb0e851e702`,
  snapshot `.ufo/evidence/round-79/sources/cmdline315.html`, headers
  `cmdline315.headers`). Located quote: "All PYTHON* environment variables are
  ignored, too." (8 words, page lines 308-311, the `-I` entry's paragraph).
  Tier A, status `mined`, recheck on-release, `used-by
  corpus/lessons/round-79.md`.

Re-opened rows (same round, old → new logged):

- **S289 — Git, git-cat-file documentation**, re-opened 2026-11-04 (06:31:53
  GMT): `https://git-scm.com/docs/git-cat-file`, 79,488 B, sha256
  `91805d9aec858f88581552fc1fe105a40a649544f872e72e6daff210a113e910`,
  snapshot `.ufo/evidence/round-79/sources/catfile.html`. Located quote:
  "Output the contents or other properties such as size, type or delta
  information of one or more objects." (20 words, page line 2205). `used-by`
  old → new: `… corpus/lessons/round-61.md` → `… corpus/lessons/round-61.md,
  corpus/lessons/round-79.md` (no other cell changes).
- **S305 — Git, git-ls-tree documentation**, re-opened 2026-11-04 (06:31:53
  GMT): `https://git-scm.com/docs/git-ls-tree`, 39,083 B, sha256
  `ff06fbc8b15b0fee505a259e4dc54096c9fba0460f4f02b449d55ecce7818267`,
  snapshot `.ufo/evidence/round-79/sources/lstree.html`. Located quote:
  "Recurse into sub-trees." (4 words, page line 1664). `used-by` old → new:
  `corpus/lessons/round-77.md` → `corpus/lessons/round-77.md,
  corpus/lessons/round-79.md` (no other cell changes).

Refused (reject, with flip condition): a second row for
`https://docs.python.org/3/library/sys.html` as the `-I` ground — the
`sys.flags` table only maps `flags.isolated` to the `-I` option and carries no
prose for it (page lines 831-832 and 999), so the row could not teach the
isolation semantics; flip: the page gains prose defining isolated mode.

Assimilation: none. The round-78 connector's staged-package id collision
condition is unchanged (see the connector's re-derivation this round); no
staged entry was adopted, so no registry row was appended from the package.

## Mistakes

1. **A receipt's `measured_rev` was captured from a worktree whose bytes landed
   in a later commit.** Class: record-to-bytes misattribution (the round-77
   §6.1 / round-78 §6.1 relapse). Evidence pointer:
   `.ufo/evidence/round-78/c1-landed-sweep.txt` and seven siblings — each names
   `6f532752…` while its recorded tool sha first exists at `091d50e4…`
   (`corpus/lessons/round-78-verifier-spotcheck.md` §6.1). Captured-by:
   criterion 128 (a settlement's credit is measured at the settlement commit)
   covered record sentences, not receipt headers, so nothing in the lane
   re-derived the pair. Fix: `tools/receipt-bytes-bind.py` + criterion 130; the
   fix is shown able to fail — on the base population it prints `unbound=8`
   exit 1, and a false correction prints `unbound=1`
   (`detail=bytes-rev-mismatch`) exit 1.
2. **A round's own new guard had no positive-branch exercise.** Class:
   unguarded guard — the round-78 leak post-condition only ever measured its
   passing branch (a healthy cleanup never leaks), so an always-clean detector
   survived 21/21 (`T78W1M1` `w1-leak-scan-empty`). Captured-by: none; no
   criterion required a new guard's failing branch to be measured. Fix:
   arm22 (both branches) + criterion 131; shown able to fail — the
   `leak-detector-blind` mutant survives the 21-arm control and dies on arm22
   only.
3. **A spec anchor lost uniqueness after a refactor.** Class: spec drift —
   extracting the arm bodies duplicated `shutil.rmtree(fix, ignore_errors=True)`
   four times, and the `arm20-cleanup-removed` mutant refused to apply
   (`old-string-count=4 expected=1`, first battery run). Captured-by: the
   mutator's own count==1 assertion (the fix is the anchored comment line, and
   the edit it performs is unchanged). Fix: the spec's `@old` gains the arm20
   cleanup comment line; the battery re-runs 12/12.

## Wave findings

Every finding cites its committed seat report under `.ufo/waves/round-79/w1/`.
The wave changed the landed bytes in six places, all disclosed and all
re-measured after the change.

1. **Two real holes in the new C1 instrument (sentinel `T79W1SN1`).** (a) A
   receipt with one valid and one malformed `# tool:` line bound against the
   valid one; `parse_receipt` counted only regex-valid headers, so a
   recognised prefix whose value did not parse disappeared. Fixed with a
   `receipt-header-malformed` refusal folded into ARM6 (the frozen count stays
   `10/10`); falsification: with the check disabled ARM6 FAILs (`9/10`) and the
   malformed receipt binds (`bound=1 unbound=0`). (b) A `# tool: /etc/passwd`
   absolute path had no arm (only `..` traversal was exercised); folded into
   ARM10; the round-79 wave's own mutation-tester measured
   `absolute-tool-path-accepted` surviving before the fold and dying after.
2. **The selfstate fixture builders violated the lane's git-fixture rule
   (sentinel).** Arms 11/13/14 initialised, added and committed without a
   `rev-parse --show-toplevel` assertion; all three now assert the fixture root
   before any commit. Further, every fixture git call (and the two tools'
   production git reads) inherited `GIT_DIR`/`GIT_WORK_TREE`: under a hostile
   environment the suites read the wrong repository (selfstate crashed,
   wave-reconcile read `21/23`); with the isolated env both read `14/14` and
   `23/23` under `GIT_DIR=<decoy> GIT_WORK_TREE=<decoy>`.
3. **The carrying revision is not the measured revision (scout `T79W1SC1`
   F5).** `091d50e4` postdates the receipts' `at_utc` by 57 s and is not the
   unique carrier (three commits carry the bytes; one on master). The
   correction therefore says "a commit whose committed bytes carry the recorded
   sha", never "the revision that was measured"; the receipt's measured
   revision is unchanged.
4. **A landed battery receipt was measured on pre-hardening bytes (scout
   `T79W1SC1` F9).** The C3 receipt named the 36,332-byte candidate; the
   post-sentinel bytes are 37,311 bytes. The final receipts are regenerated at
   the landing rev by `.ufo/evidence/round-79/gen-receipts-r79.py`, so every
   after-state receipt names the revision that carries its measured bytes.
5. **Two stale capability figures (scout `T79W1SC1` F11/F12).** `wave-record
   reconciliation` printed `19/19` against the tool's `21/21` at base, and
   this round's `14/14` would have left `non-Python instrument freshness row`
   printing `13/13`. Both cells are repaired to the current tokens as
   calibration work (no claim credit), and the `non-Python` cell is
   re-demonstrated round 79.
6. **The sweep cannot catch a rewritten sha line (reviewer `T79W1R1`).** A
   population whose `# tool_sha256:` lines are all rewritten to match the
   named rev sweeps clean (`bound=12 unbound=0`); the binding is a
   binding-of-record check, and the compensating guard is the frozen kill rule
   that the eight corrections change no existing line (verified: eight `1 0`
   numstat rows, zero deleted content lines, every `# tool_sha256:`
   byte-identical). Stated as a limit, not a guarantee.

Named survivors for round 80 (each measured, none fixed this round): the python
tuple's `-X utf8` (`T79W1M1` `python-utf8-dropped`, a `sys.flags.utf8_mode`
fixture distinguishes it); the scout's 18 surviving single-edit mutants in the
20-rule table, shortlisted `ss-bom-strip`, `wr-record-unknown-root-check-removed`
and `ss-cache-key-drops-argv` (`T79W1SC2`).

Assimilation: none (connector `T79W1CN1`: the eight staged-package id
collisions are unchanged and the same ids denote different documents; staged
PIT documents map to the held S155/S156 rather than new rows). One connector
documentation proposal is adopted: the carrying-revision correction certifies
which committed tool blob matches a historical receipt's recorded sha — it does
not re-run the historical command or attest isolation; generic blob-bound
receipt verification already exists in souji, and this lane adds the historical
population sweep and the append-only correction contract.

7. **The critic's two static counterexamples (no seat report; terminal yield).**
   (a) The frozen design parser at `92c00705` lacks the raw-prefix malformed
   guard the sentinel's probe needs, so the receipts committed at the
   declaration (`design_tool_sha256: c20082b0…`) describe the pre-fix bytes;
   the landed receipts are regenerated at the landing rev
   (`gen-receipts-r79.py`), and the frozen predicate (`10/10`, `unbound=0`)
   holds on both. (b) R79-C3 changes fixture coverage, not production
   behaviour: the python tuple already carried `-I` at base, so the round's
   move is that the runner's execution contract is now measured, not that the
   runner changed. The operability label follows the lane's arm-addition
   precedent; the critic's reading is recorded rather than argued away.
4. **A copied run-book rekey tool carried the round-78 trace path and the
   round-61 label (recurrence of the round-78 `## Mistakes` 4 class).** Class:
   frozen-copy drift. The settlement's first batch appended 14 ledger entries
   whose `traces` pointed at `.ufo/evidence/round-78/rekey/traces/…` (a
   hardcoded `trace_rel` in the copied `coldread-rekey-rebind-r63.py`), so at
   the settlement tip the monitor read `credited=51/65` with
   `trace-input-drift:LOG.md` — the trace files it resolved were the committed
   round-78 ones, not the batch's. Evidence:
   `.ufo/evidence/round-79/coldread-after-r79.json` at `a4b2d4c7` (51/65).
   Captured-by: the tool's own summary printed `REBIND OK`, which the lane's
   run-book treats as producer evidence — nothing re-ran the monitor before the
   commit. Fix: the copy's `trace_rel` is now
   `str(Path(--traces-dir) / 'section-%02d.json')` and `rekey_round` is 79;
   batch 2 appended 14 corrected entries (ledger 976 → 990) and the monitor
   reads `credited=65/65` at `1a210b1f` (`.ufo/evidence/round-79/
   coldread-after-r79.json`). The batch-1 entries stay (append-only) and are
   harmless: a section is credited by any matching entry and only a failing
   entry vetoes.

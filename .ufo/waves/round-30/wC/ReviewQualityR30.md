# ReviewQualityR30 — review of criteria 58–65 and README Round-30 block

seat: ReviewQualityR30
reviewed: `git diff 9ed6db84..bb681566 -- corpus/QUALITY.md corpus/README.md` at
`bb681566b18211adf8ae9c28df91e17678e3f545` (read-only, `GIT_OPTIONAL_LOCKS=0`).
Routing source: `corpus/lessons/round-29-verifier-spotcheck.md` (same revision).

Verdict: criteria 58, 59, 60, 61, 64, 65 hold — every Falsifier pointer resolves at
`bb681566` and says what the criterion claims, and each routes the spot-check item it
names. Two mismatches found: a wrong class-name in criterion 60's Falsifier, and a
routing preamble that omits Mistake 3. Minor wording issues in criteria 62 and 63.
No mismatch in README's Round-30 section.

## Findings, by severity

### F1 (minor defect) — `corpus/QUALITY.md:686` (criterion 60): wrong class name in the Falsifier

The criterion text reads: "…lists 10 entries excluded on assembler shape alone
(assembler verdict normalization, report `executed-ok` vs entry `gap-minor`, and seat
self-labels such as `TameshiR29.Read08A`), every report verdict a passing class."

Observed in `.ufo/evidence/round-29/coldread/select-receipt-w1.json`
(`excluded_entries[8]`, seat Read12B): the report verdict recorded is
`verified-record`, not `executed-ok` — the pair is `report_verdict verified-record`
vs `entry_verdict gap-minor`. `excluded_verdicts` is `["gap-minor","verified-record"]`,
so a `verified-record` → `gap-minor` normalization exists. The criterion names only
the `executed-ok` → `gap-minor` case. The substance (10 exclusions, all on assembler
shape, all entry verdicts passing classes) is correct; the falsifier's list of
normalization pairs is incomplete and slightly mislabels the second pair.

Smallest safe correction: at line 686 write "(assembler verdict normalization —
`executed-ok` and `verified-record` reports normalized to `gap-minor` entries — and
seat self-labels such as `TameshiR29.Read08A`)".

### F2 (minor defect) — `corpus/QUALITY.md:649-651` (block preamble): Mistake 3 missing from the routing list

The preamble reads "`lessons/round-29.md` Mistakes 1, 4 and 5". But criterion 61
(`QUALITY.md:694-695`) cites "(Mistakes 3 and 4)" for routed items 5(a) and 5(b), and
`lessons/round-29.md` Mistake 3 (the misrooted Read10C report, sha256 `fafd4c36…` at
lesson line ~99-103) is the lesson record behind 5(a). The preamble's enumeration
should read "Mistakes 1, 3, 4 and 5". Not criterion-gating — the criteria themselves
cite the right mistake numbers — but the preamble's source list is inaccurate as
written.

### F3 (cosmetic) — `corpus/QUALITY.md:706` (criterion 62): "the only C2 head receipt"

The falsifier calls `.ufo/evidence/round-29/c2-at-E.stdout` (rev `7a45f7b9`) "the
only C2 head receipt". `7a45f7b9` is a mid-lane commit, not the head; the intended
reading is "the only committed C2 counter receipt". Substance verified and correct:
`c2-at-E.stdout` reads `quote_located=0 rev=7a45f7b9…`, was committed at `9bb699a`
(`git log -- .ufo/evidence/round-29/c2-at-E.stdout`), `git grep` finds no committed
receipt naming `6892c3ee`, `1a1e8b22` or `3c16b3a6`, and the fleet report
(`shokunin/.ufo/reports/round-29/tameshi.md` at `772f7105`, line 77) prints C2
`quote_located=1` and names those three commits as measured. The residual report
`.ufo/waves/round-29/res/RerunC2Head.md` re-ran at `7a45f7b9` only, so "no C2
receipt for the three head commits" holds.

### F4 (cosmetic) — `corpus/QUALITY.md:718-721` (criterion 63): unverifiable construction details

The falsifier asserts the sandbox commit `daa11583` was built by "one comment line
appended to each of SOURCES, QUALITY, README and the runner" and that drift was
"64 → 33". The receipt `drift-sim-union4.txt` shows only `covered=33/64 …
rev=daa11583c999b249b35055cc45eeb00b38040996`; `daa11583` is not an object in the
lane repository (`git cat-file -t` → "could not get object info"), so the
construction cannot be re-checked from committed bytes. The construction story is
corroborated by `.ufo/evidence/round-30/contract.json` ("a sandbox commit appending
one comment line to each of the four files"), and the "64" end is corroborated by
`monitor-at-base.stdout` (`covered=64/64` at `9ed6db84`), the "52" end by
`.ufo/evidence/round-29/c1-at-A.stdout` (`covered=52/64` at `9f3084bc`). Acceptable
as supporting evidence; a falsifier's pointer ideally commits its construction
recipe or sandbox rev.

## Verified items (no mismatch)

- **Criterion 58** (`QUALITY.md:653`): `contract.json` resolves as
  `.ufo/evidence/round-29/contract.json`; `controls_required_before_data` lists
  "shortcut keyed on ids or labels". `.ufo/waves/round-29/ctl/` contains no scored
  shortcut receipt (only C1v2-rescore, CriticC1/C2Design, CriticC2v2, CtlC1/C2Cheap,
  CtlC2v2Port). Refusal holds recorded in
  `.ufo/waves/round-29/res/ReviewControls.md:73-90` (CtlC1Shortcut pre-data;
  CtlC2Shortcut first recorded at E). Routes spot-check item 1 ("Unscored shortcut
  control class", spot-check line 190). Match.
- **Criterion 59** (`QUALITY.md:665`): `r29-mistake1-ordering.txt` reads the exact
  two mtimes claimed (CriticC2v2.md 22:33:57-03, task-adapter-w1.json 22:27:45-03)
  and shows both first-committed in `bc2058a4` — "no committed order" is accurate.
  The file is committed in `bb681566`, the same commit as the criterion. Routes
  items 4 + 7 (item 7 bullet 3, spot-check line 220, is the Mistake-1 falsifier
  carry-over). Match.
- **Criterion 60** (`QUALITY.md:677`): `select-receipt-w1.json` `excluded` count is
  10; reasons are assembler shape only (verdict normalization pairs and
  `seat-not-registry-member:TameshiR29.*` self-labels); all excluded entry verdicts
  are `gap-minor`/`verified-record` — passing classes. Routes items 2 + 3
  (spot-check lines 194-200). Match modulo F1.
- **Criterion 61** (`QUALITY.md:690`): `.ufo/waves/round-29/spec-w1.json` `context`
  (4320 chars) lacks the never-kill sentence; `BuildF6B.md:350` records the kill of
  PID 2758108; `lessons/round-29.md` Mistake 3 records the misrooted Read10C report
  with sha256 `fafd4c3698e3…` and Mistake 4 records the containment breach. Routes
  items 5(a) + 5(b) (spot-check lines 205-210); 5(c) correctly excluded as a work
  assignment (runtime kill of a seat's own process group, not a lane rule). Match
  modulo F2.
- **Criterion 64** (`QUALITY.md:723`): `c1-measure-v4-draft.py:315` builds
  `st-<job>` dirs (`os.path.join(tree, '..', 'st-' + name)`) — job identity readable
  from cwd. `K9-on-draft.stdout` reads `PREDICATE: C1_R30_PASS=true` (the
  directory-sniffing control passes on the draft); `K9.stdout` reads
  `PREDICATE: C1_R30_PASS=false` on the frozen counter (all drops pass → killed=0/13).
  Both receipts carry `rev=e7590f6e` — the sealed-fixture rev, not a lane commit;
  consistent with "same control, counter differs". Captured-by "control K9" matches.
- **Criterion 65** (`QUALITY.md:737`): `CtlS2SymEval-v4.stdout` reads
  `sealed_killed=6/6 sealed_equiv=6/6` and `PREDICATE: C1_R30_PASS=true`, exit 0.
  `CtlS2SymEval-11.diff` adds a Python symbolic evaluator whose comment states
  "Never run the extracted shell text: the … vectors are interpreted as model state
  transitions" — it never runs bash on the block. `contract-amendment-4.json`
  records this control meeting v4 as the reason C1 went exploratory. Match.

## README Round-30 section (`corpus/README.md:449-455`)

- `knowledge/regression-tally-completeness.md` exists at `bb681566` and says what
  the row claims (exploratory C1, operability, S087/S093/S094 sources).
- The runner at `bb681566` (`tools/mutate-and-run.sh:1453-1458`) refuses
  `npass + nfail + nsetup != nlegs` as SETUP exit 2 — "tally refuses as SETUP when
  the counted leg statuses do not add up to the case count" is accurate.
- Selftest (`mutate-and-run.sh:1989-2039`): 24 `tally_line` executions = 1
  all-pass + 18 one-status-at-each-position + 4 extra vectors + 1 guard stress
  case. "23 fixed status vectors and a guard stress case" counts exactly. The
  97 → 106 delta matches the 9 new `st` assertions.
- Row 2's pointer `.ufo/evidence/round-30/sources/S059-bazel-remote-caching.md`
  resolves; sha256 = `266915c5d73f…` = the new S092 anchor (changed from
  `0d362d11…`), and the known-issue sentence stands at lines 343/345. The filename
  carries the superseded S059 id — confusing naming, content correct; noted, not a
  mismatch.

## Residual risk and verification gaps

- Criterion 58's "`.ufo/waves/round-29/ctl/` holds no scored receipt" is verified by
  listing absence, not by a pointer; a future reader must re-list the directory.
- `rev=daa11583` (criterion 63) and `rev=e7590f6e` (criterion 64 receipts) are
  non-lane objects by design (sandbox / sealed-fixture revisions); the claims they
  back rest on the receipts plus corroborating contract text, not on re-runnable
  commits.
- Not re-measured: monitor values are taken from committed stdout files, not
  re-executed (counter execution is out of scope for this review seat).
- Tooling: no installs or updates performed; stock `git`, `python3`, `sha256sum`
  sufficed.

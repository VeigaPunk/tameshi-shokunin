source: S001 Stryker mutant states and metrics (docs, mined); S052 Stryker supported mutators (docs, mined); S056 PIT mutation operators, CONDITIONALS_BOUNDARY (docs, mined); S057 Papadakis et al. survey §5.3.1 (paper, tier B, mined); S008 Petrović, Ivanković, Fraser, Just, arXiv 2102.11378 (paper, tier A, **queued** — Q1 quote recorded in `.ufo/waves/round-18/sources/S066-B02SrcGoogleMutation.md`, not yet a mined row); kumitate `scripts/sources-check.mjs` @ 0acb7752d19058b953ebbeba253b1e35f6548de5 (blob sha256 6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f), read-only; procedure: `corpus/knowledge/mutation-case-kumitate-round-gate.md` (case 7)
verified-at: 2026-10-20; pre-registration `93d22aa21a144a0e2833b1be74718d15060f002b` (2026-10-20T16:40:21-03:00), sweep 2026-10-20T19:41:29Z (after the pre-registration commit); receipts under `.ufo/evidence/round-18/sources-check/`
recheck: `git -C kumitate-shokunin show 0acb7752d19058b953ebbeba253b1e35f6548de5:scripts/sources-check.mjs | sha256sum` → `6a293a72…258f`; `node sources-check.mjs --selftest` under the `suite.txt` string → `SOURCES_SELFTEST: 46/46 pass`, exit 0; `bash tools/mutate-and-run.sh --regression` → `REGRESSION_CASE js-sources-check: PASS` (leg not yet installed at base, see §5)

# Mutation case 8 — kumitate `scripts/sources-check.mjs` (round 18)

The eighth recorded case. Like case 7, the target is a kumitate `scripts/*`
primary surface (tameshi's `PROVINCE.md:7-11`). Kumitate's tree stayed
read-only: the target is a byte copy materialized from its git object store.
At the C01 check, `git --no-optional-locks status --porcelain` in kumitate was
empty. No owner opt-in was needed. Ownership is split: kumitate owns the gate
(`kumitate-shokunin/PROVINCE.md:15` names `corpus/SOURCES.md`, checked by
`scripts/sources-check.mjs`; registry row `SKILL.md:605`); tameshi owns the
method and this measurement only. The `PROVINCE.md:15` instrument line is the
gate's own province; `:7-11` is the tameshi-side band.

## 0. Pin and suite

- Target: rev `0acb775` (the file's last touching commit, `round-34: fix SOURCES
  Markdown row parsing`). Kumitate HEAD `1770305` holds the same blob
  `6b57424f…`. Blob sha256 `6a293a72…258f`, 897 lines, 43,497 bytes, mode 100755
  (S19 §1; C01 §1; sweep `MUTATE_TARGET … bytes=43497`).
- Suite: `node sources-check.mjs --selftest`, 46 checks, `SOURCES_SELFTEST:
  46/46 pass`, `VERDICT: PASS`, exit 0 (S19 §1; control in
  `sources-check/control.txt`). The run string is `suite.txt`:
  `env -i PATH HOME=$h/home TMPDIR=$h/tmp LC_ALL=C GIT_CONFIG_NOSYSTEM=1
  GIT_CEILING_DIRECTORIES=$h node "$MUTANT" --selftest`, with a per-defect
  private `HOME` and `TMPDIR`. This is the same environment shape as case 7's
  suite, not the same bytes. Fixtures are temporary. K02's S6 records the tool
  as git-free, and the hazard summary (X10) reports the suite exercises no
  round-gate Git fixture operations.
- Control determinism: 8 pristine runs of the `suite.txt` string all exited 0
  with empty stderr and identical stdout (6,274 bytes, SHA-256
  `e0880a5a…e5`; `control/repeat-hashes.json`, `distinct_stdout_sha256: 1`).
  Case 7's stdout varied per run through a `mkdtemp` suffix; this suite's
  stdout did not. The repeat-control tool returns `controls_match`, exit 0.
  Verdicts are still graded on exit status only.
- Hazard controls (`control/hazard-summary.md`): an exported `GIT_DIR` pointing
  at a canary repo leaves the canary unchanged, 46/46; a `TMPDIR` inside a work
  tree leaves the lane clone's `git status --porcelain --untracked-files=all`
  empty, 46/46. These cover this selftest only, not round-gate's fixture
  hazards.
- Untracked artifacts: at the time of this draft the sweep and control
  directories are untracked in the lane (`?? .ufo/evidence/round-18/sources-check/sweep/`,
  `…/control/`). The citations below assume the L1 commits them.

## 1. Pre-registration

Ten defects and their predictions were committed in `93d22aa` (2026-10-20T16:40:21-03:00)
before any mutant ran. The committed files are `sources-check.defects.spec`
(sha256 `c8d24cb4…408c91`), `predictions.json` (schema
`tameshi-r18-preregistration-v1`), `suite.txt`, and `control.txt`. The first
mutant ran at 19:41:29Z, one minute after the commit.

Each `@old` anchor is unique in the pinned bytes under the runner's rule, which
keeps the text after `@old ` verbatim, leading indentation included. A Python
count on the pinned blob gives `count=1` for all ten: K_KIND :293, S_KIND :114,
K_EXIT :492, S_VERDICT :483, K_STRICT :434, K_CLOSED :182, K_ROWS :247,
S_DUP_LINE :251, S_ENTRY_COUNT :368, S_FILE_READ :356. A count that dropped the
indentation gave 5 for S_KIND; that was a bug in the count, not in the spec.

Composition: 5 kill-aimed (predicted KILLED: K_KIND, K_EXIT, K_STRICT, K_CLOSED,
K_ROWS) and 5 hole-aimed (predicted SURVIVED: S_KIND, S_VERDICT, S_DUP_LINE,
S_ENTRY_COUNT, S_FILE_READ). Each prediction names one selftest case and gives a
reason (`predictions.json`).

Operator families. S052 names the JS single-edit classes: string literal,
equality, conditional, boolean, array declaration. Four edits here are string
literal (K_KIND, S_VERDICT, K_CLOSED, S_FILE_READ), one is a conditional on a
literal (K_STRICT), and one is an array element (S_KIND). Four are numeric
(K_EXIT `64→65`, K_ROWS `+= 1→+= 2`, S_DUP_LINE `index + 1→index + 2`,
S_ENTRY_COUNT `+= 1→+= 2`). Those four are outside S052's named list, and this
entry does not call them Stryker operators. S056 is cited for the family
taxonomy only; none of the ten is a relational-boundary edit.

Selection. S008's historical-performance selection (Q1, below) is not used.
The ten edits were chosen by hand from the suite's predicates. Q1 is cited here
for contrast: "Mutants are selected based on the historical performance of
mutation operators, further eliminating irrelevant mutants and improving mutant
quality." (S066 record; 19 words, verbatim.)

## 2. Result — 5/10 killed (50 %), 10/10 predictions held

Tool: `tools/mutate-and-run.sh`, sha256
`fb6d86d59b5c9285864c9ebfa19d5a6f8938e91c47877a6d25b451a1da03001a`
(`MUTATE_TOOL` in `sweep/sweep.txt`). The control was GREEN, exit 0, and
`MUTATE_RESTORE: OK`. The target sha was unchanged before and after
(`SWEEP_TARGET_RECHECK: PASS`). The runner reports killed, survived, and
inconclusive only (inconclusive 0), so valid = 10 and kill rate = killed / 10,
as in S001's detected / valid.

| id | class | edit (sources-check.mjs line) | predicted | measured | exit | `SOURCES_SELFTEST` |
|---|---|---|---|---|---|---|
| K_KIND | kind | `TIER_ENUM` → `KIND_ENUM` in the `add` at :293 | KILLED | KILLED | 1 | 43/46 |
| S_KIND | kind | drop `'RECHECK_OVERDUE'` from `FINDING_KINDS` (:114) | SURVIVED | SURVIVED | 0 | 46/46 |
| K_EXIT | exit | usage `return 64;` → `return 65;` (:492) | KILLED | KILLED | 1 | 44/46 |
| S_VERDICT | verdict | DRIFT line `(…)` → `[…]` (:483) | SURVIVED | SURVIVED | 0 | 46/46 |
| K_STRICT | strict | `warn` → `error` in the strict test (:434) | KILLED | KILLED | 1 | 45/46 |
| K_CLOSED | fail-closed | `SOURCES_MISSING` → `READ_FAILED` (:182) | KILLED | KILLED | 1 | 44/46 |
| K_ROWS | parity | `counts.rows += 1` → `+= 2` (:247) | KILLED | KILLED | 1 | 41/46 |
| S_DUP_LINE | line | `index + 1` → `index + 2` in ID_DUPLICATE (:251) | SURVIVED | SURVIVED | 0 | 46/46 |
| S_ENTRY_COUNT | count | `entriesWithSource += 1` → `+= 2` (:368) | SURVIVED | SURVIVED | 0 | 46/46 |
| S_FILE_READ | fail-closed | per-entry read arm `READ_FAILED` → `SOURCES_MISSING` (:356) | SURVIVED | SURVIVED | 0 | 46/46 |

- Every survivor's suite ends `SOURCES_SELFTEST: 46/46 pass`, `VERDICT: PASS`,
  exit 0. The sweep has the survivor rows as printed.
- Per-check attribution is not recorded. The sweep keeps only the tail of each
  suite run (about seven lines). The failing check names appear only for K_EXIT
  (two `FAIL` lines, both the exit-64 usage checks, which matches the predicted
  case) and for K_ROWS (the awk parity `FAIL`). For K_KIND (3 failed),
  K_STRICT (1), and K_CLOSED (2), the failure count is measured but the failing
  checks are not. The predicted cases (TIER_ENUM, the strict warning fixture,
  SOURCES_MISSING) are therefore unverified at the per-check level. The sweep's
  per-mutant evidence directory was reported at a `/tmp` path (`MUTATE_EVIDENCE`)
  and is not in the lane (QUALITY 9).
- Prediction accuracy (10/10) is a separate reading from kill rate. The 10/10
  compares only KILLED or SURVIVED against the prediction. It does not check
  which case killed a mutant.

## 3. What the case measures

- **Survivors are edits to predicates the suite asserts only by exit and kind,
  or to unexecuted code.** 44 of 46 checks assert `(exit, kind)` only (S19 §2).
  The S_FILE_READ anchor (:356) and its neighbour (:357) are zero-statement lines
  under c8 (S19 §4, `ZERO STMT LINES: … 356,357 …`). That coverage reading is S19's;
  this seat measured no new coverage.
- **Gaps the survivors expose** (as predicted in `predictions.json`; each
  measured to survive):
  - S_KIND: the kind-coverage meta-check is one-sided. `FINDING_KINDS` is read
    in three places: the declaration (:108), a string at :130 that interpolates
    the list, and the meta-check `missingKinds` (:784). Removing a declared kind
    passes the meta-check. No case asserts that observed kinds are declared. This
    is the same family as case 7's CKIND, on another artifact. K02's M6 probe
    measured the same family.
  - S_VERDICT: no case pins the DRIFT verdict line. DRIFT fixtures assert exit
    and kind.
  - S_DUP_LINE: no case asserts a finding's line. S19 §2: "No check asserts a
    finding's `line`/`:N` location."
  - S_ENTRY_COUNT: a positive `entriesWithSource` is not pinned. Only
    `entries_with_source=0 legacy=1` is asserted (S19 check 32). The sweep's S1000
    line shows the mutant reporting `entries_with_source=2` while the suite passes.
  - S_FILE_READ: the per-entry read arm is not reached. The READ_FAILED fixture
    fails earlier, at `readdirSync` (predictions.json reason; that fixture's exact
    path was not re-verified here).
- **Depth.** K02's depth test asks for at least two of its D1–D5 classes.
  This spec touches D3 (severity promotion, K_STRICT) and D5 (verdict tail,
  S_VERDICT). It touches D1 (parity, K_ROWS), but without the second,
  non-host-gated witness K02's S3 asks for (§6).

## 4. Survivors — non-equivalence PENDING

No survivor is declared equivalent. S057 §5.3.1: equivalence is undecidable in
general, so a survivor needs an off-suite witness or an explicit equivalence
argument. None is supplied here. Each survivor is PENDING wave-2 off-suite
probes. The suite's 46/46 is measured. Equivalence is not.

| survivor | spec line | witness needed | status |
|---|---|---|---|
| S_KIND | :114 | verdict and exit on a fixture that emits RECHECK_OVERDUE, mutant vs pristine. The string at :130 changes by construction, so any equivalence claim must be verdict-scoped. | PENDING |
| S_VERDICT | :483 | the DRIFT line differs by construction; the consumers of that spelling are not enumerated. The SKILL.md:629-630 checklist reads `CLEAN` for the gate and `VERDICT: PASS` for the suite, not DRIFT. | PENDING |
| S_DUP_LINE | :251 | duplicate-ID fixture; the reported line differs by construction; whether `line` is a contract field is not checked here. | PENDING |
| S_ENTRY_COUNT | :368 | `entries_with_source=N` on the verdict line and `--json`; the value differs by construction. | PENDING |
| S_FILE_READ | :356 | a real per-file read failure that reaches the arm (not the directory-read fixture); none is run here. | PENDING |

## 5. Ledger leg

`js-sources-check` is the eighth leg. It holds the pin (git source, rev
`0acb7752…`, path `scripts/sources-check.mjs`, mode 100755, sha `6a293a72…258f`),
the spec, the recorded table, and the guarded suite. The table is
`K_KIND:KILLED,S_KIND:SURVIVED,K_EXIT:KILLED,S_VERDICT:SURVIVED,K_STRICT:KILLED,K_CLOSED:KILLED,K_ROWS:KILLED,S_DUP_LINE:SURVIVED,S_ENTRY_COUNT:SURVIVED,S_FILE_READ:SURVIVED`
(`TABLE_SOURCESCHECK`, staged runner `:620`). Its suite string is byte-identical
to `suite.txt`.

Status: the leg is not installed at base. `git grep js-sources-check -- tools`
finds nothing at `183f87b` or `93d22aa`. The leg lives in the staged runner
`.ufo/waves/round-18/staged/tools/mutate-and-run.sh` (`:1015` spec embed,
`:1349-1352` regression case, `:1879` leg tuple). The L1 check receipt
`.ufo/evidence/round-18/leg8-L1-check.txt` records
`REGRESSION_CASE js-sources-check: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)`,
`REGRESSION_TABLE js-sources-check: match=10/10 … flips=0`, and
`REGRESSION: PASS (cases=8 passed=8 …)`, exit 0. The receipt does not print the
runner sha, so it does not name the runner that ran. An installed-runner receipt
is pending the L1 install.

## 6. Limits

- One revision (`0acb775`), one host (node v24.21.0, Linux). The 50 % rate is a
  property of this suite at this pin, not of kumitate's gates in general. It
  shares composition (5/5 by design) with case 7's 50 %, but the two suites
  differ. Do not compare them without the composition note.
- Ownership: kumitate owns the gate, and this entry measures its suite. No kill
  is attributed to `scripts/sources-census.sh` or to kagi's census (C01 §3; C05).
  The pre-registration carries no per-defect fleet-versus-kumitate label. C05
  proposed such tags before the spec was committed. They are not in the
  prediction column, and this entry does not add them.
- K_ROWS's kill channel is the awk census parity check, which is host-gated: it
  prints `SKIP` when awk is absent (S19 §2 #46; `LOG.md:1496-1498`). The sweep
  host had awk (`awk=4/1/1`). K_ROWS is therefore a result on an awk-present
  host only. K02's S3 asks for a second, non-host-gated witness; this spec has
  none.
- Per-check failing names are not recorded (§2). Survivors are not proved
  equivalent (§4).
- The four numeric edits are outside S052's named families (§1).
- The guard scrubs the environment and does not confine. The mutants are
  single-edit and non-hostile. `bwrap` confinement is the next step for
  untrusted mutants (case 7 §6, same tool).
- Documentation drift at the pin: S19 §7 reads the SCORECARD capability cell
  (`SCORECARD.md:1616`) as 42/42, against the 46/46 live suite. C01 §1 reports
  that kumitate's `d933e15`, after the pin, sets that cell to 46/46. The two reads
  disagree about which revision they saw. Nothing in this entry depends on the
  cell.
  C05 also finds that the `sources-check.mjs:23-36` header map
  (W02/W03/overdue) does not match fleet fixtures. That is routed to kumitate
  and is not used here.
- Registry and corpus obligations (L1, not done here): S008 is `queued` with
  `used-by —`; citing it here needs the L1 to mine it and set used-by. S001
  (used-by `mutation-score-semantics.md`) and S052, S056, S057 (used-by
  `mutation-case-kumitate-round-gate.md`) need this entry added to used-by. The
  coverage-map row and LOG entry are routed under QUALITY 7.

## Errata — round 18 wave 2 (2026-10-20, append-only)

Appended after the non-author wave-2 reads at `01d586ddbc5fcd78659557c4e93a6ee8517b87d1`;
the lines above stay as written.

- **ER8-1 install and sources.** The leg is installed in `tools/mutate-and-run.sh`
  since `58e5d53` (§0 "untracked" and §5 "not installed at base" describe the
  pre-landing state). S008 is `mined` since `58e5d53`, with this entry as its
  used-by; S001, S052, S056 and S057 list this entry in used-by since round 18.
  Replay at `01d586d`: `REGRESSION: PASS (cases=8 passed=8)`, leg 8
  `match=10/10 flips=0` (`.ufo/waves/round-18/w2/RerunC1.md`, `CR21.md`, `CR22.md`).
- **ER8-2 §4 survivors probed off-suite** (`.ufo/evidence/round-18/sources-check/survivor-probes/<ID>/`):

  | ID | Off-suite input | Pristine vs mutant | Reading |
  |---|---|---|---|
  | S_VERDICT | fixture with one KIND_ENUM row | final line `DRIFT (KIND_ENUM)` vs `DRIFT [KIND_ENUM]` | non-equivalent; breaks the header's line contract (`sources-check.mjs:39-44`) |
  | S_DUP_LINE | duplicate-id fixture | `ID_DUPLICATE` at `SOURCES.md:8` vs `:9` (text and `--json` line) | non-equivalent |
  | S_ENTRY_COUNT | one source-headed entry | `entries_with_source=1` vs `2` (text and `counts.entriesWithSource`) | non-equivalent; the count is in the header contract |
  | S_FILE_READ | readable SOURCES.md + one unreadable/unopenable knowledge entry | `FAIL-CLOSED (READ_FAILED)` vs `(SOURCES_MISSING)`, both exit 2 | non-equivalent; the kind mapping is code-only, not in the header |
  | S_KIND | RECHECK_OVERDUE fixture | corpus output byte-identical; only `--help`'s kind list differs | equivalent on corpus output; distinguishable on help output only |

  Four of five survivors are suite gaps with a distinguishing input; S_KIND is
  a declaration-only gap. Recommendations travel to kumitate (`.ufo/waves/round-18/w2/KumitateRouting.md`: six additive selftest checks, each killing one survivor on a copy).
- **ER8-3 kill attribution** (`.ufo/evidence/round-18/sources-check/attribution/`):
  every predicted killing case fails for its mutant (5/5); K_STRICT's is the only
  failing check. §6's statement that K_ROWS's kill depends on host awk is wrong:
  with awk hidden from PATH the parity check SKIPs and K_ROWS still dies on four
  row-count checks (41/45). The *predicted* case for K_ROWS is the one host-dependent check.
- **ER8-4 ruler note.** Command D counts header lines only; an extra comment line
  would raise it without a leg (`.ufo/waves/round-18/w2/RerunC1.md` M2). The
  round-17/18 measure's `ledger_guardrail` (header legs = regression calls =
  selftest tuples, 8/8/8 at `01d586d`) is the cross-check to cite with it.
- **ER8-5 further corrections** (`.ufo/waves/round-18/w2/ReviewCase8Entry.md`):
  the "S066 record" mentions (`:1`, `:80`) mean the wave-1 draft file
  `.ufo/waves/round-18/sources/S066-B02SrcGoogleMutation.md`, whose quote now
  backs registry row **S008**; registry row S066 is RFC 8259 and is not cited
  here. "44 of 46 checks assert (exit, kind) only" (`:123`) is false: at most 32
  do, 14 assert other output. Case 7's `suite.txt` is byte-identical to this
  case's, not only the same shape. The control hash ends `…5e5f`. The L1 check
  receipt `.ufo/evidence/round-18/leg8-L1-check.txt` was taken with a staged
  runner whose leg-8 suite string was still the bare `node "$MUTANT" --selftest`
  (fixed before landing); the landed runner's replay is the wave-2 evidence in
  ER8-1. `SKILL.md:605`, `:629-630`, `LOG.md:1496-1498` and `SCORECARD.md:1616`
  in §3/§6 are kumitate's files.

## Erratum R18-2 — source metadata (2026-10-21, round 19)

This correction explicitly supersedes line 1's S008 `queued` / `not yet a
mined row` description. At delivered round-18 revision
`4b7c6823a462f5ea2eafcb262275300a545f3ed7`, S008 is `mined`, with
`corpus/knowledge/mutation-case-kumitate-sources-check.md` in `used-by`.
The effective source metadata is therefore S008, paper, tier A, mined;
the historical draft wording above is not its current status. ER8-1 had
already recorded the transition; this erratum names the stale provenance
line it supersedes. Verify with that revision's `corpus/SOURCES.md` S008
row, not with an assumed status inferred from this entry alone.

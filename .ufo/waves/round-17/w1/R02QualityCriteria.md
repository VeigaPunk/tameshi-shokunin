# R02 — QUALITY criteria: R16 routed-defect mapping and drafts 23–26

Seat: reviewer. Scope: `corpus/QUALITY.md` criteria 1–22 at lane tip
`98bea7da5801f4bc58e4187690ee1687c8a5061f`; the six routed defects in
`corpus/lessons/round-16-verifier-spotcheck.md` §6; draft checkable criteria
23+. Read-only against the lane: the only write is this report. `QUALITY.md`
itself is not edited (W04QualityDraft / L1 land the text).

## 1. Method and pinned bytes

Read at `98bea7d` unless stated: `corpus/QUALITY.md:1-123` (criteria 1–22,
lines 3–122); `corpus/lessons/round-16-verifier-spotcheck.md` §2 C1/C2, §3, §6;
`.ufo/evidence/round-16/coldread/ledger.json` (entry `SKILL.md:1563-1596`);
`.ufo/evidence/round-16/measure.py:178-210`; `.ufo/waves/round-16/w2/ToolsNoHarm.md`;
`.ufo/evidence/round-13/expected.json:12`; `.ufo/evidence/round-16/round-gate/runner-sha256.txt`.

Commands run (exits in the text):

| Command | Observed |
|---|---|
| `python3 .ufo/evidence/round-16/measure.py --rev 98bea7d` | exit 0; `coldread.box3_full_page: true`, `sections_covered: 54/54`, `calibration_restraint_score: 8` |
| `git show 98bea7d:tools/mutate-and-run.sh \| sha256sum` | `0673d2e5374b…c8118aa` |
| `git show 98bea7d:.ufo/evidence/round-16/round-gate/runner-sha256.txt \| grep -c 0673d2e5` | `0`, exit 1; the committed receipt's first line is `89722ddb…` |
| `cat .ufo/evidence/round-17/op1-redbefore-98bea7d.txt` | `exit=2`, `id: expected_input_digest_mismatch`, `observed 0673d2e5… expects 75ed934d…` |
| ledger entry query | `wrong_expectations: 0`, `commands_executed_count: 4`, `class: instruction`, no `inputs` key |
| `git show 98bea7d:SKILL.md \| grep -n '^2\\. \|^3\\. Run'` | step 2 at `:1581`, step 3 at `:1584`; the moved runner is annotated only in the round-15 registry row at `:1681`, restated in errata at `:1741` |

In-flight state: `.ufo/evidence/round-17/measure.py` and
`tools/registry.json` / `tools/registry-check.py` did not exist in the working
tree at read time (`.ufo/evidence/round-17/` held `census-start.txt`,
`coldread/bucket-commands.json`, `dispositions.json`, `dispositions-before.json`,
`jj/head-vs-branch.sh`, `op1-redbefore-98bea7d.txt`). The 23/25 check criteria
below bind to the wave-1 interface contracts; their unexecuted exits are marked
`[INFERENCE]`. The dispositions v2 manifest already exists
(`.ufo/evidence/round-17/dispositions.json`, `schema: evidence-dispositions-v2`,
four `historical_inputs` rows); the v2 reader is not installed yet.

## 2. Mapping — which existing criterion should have caught each R16 routed defect

Capture test: a criterion captures a defect if its stated rule, applied with its
named check at the landing rev, names the failure. `partial` means the rule
names the class but the failure survives its letter.

| Routed defect | Observed harm (anchor) | Existing criteria considered | Captured-by | Why |
|---|---|---|---|---|
| **R16-OP1** operability | After the runner moved (`75ed934d` → `89722ddb` @c699c8c → `0673d2e5` @05a2247), `evidence-disposition.py --root .` exits 2 at the shipped tree; the registry row substitutes a frozen `git archive 28aeef4` run; no debt named (`spotcheck §2 C2, §3 operability, §6.1`; `op1-redbefore-98bea7d.txt`) | 15, 20, 21 | **none** | 15's letter was met in the registry row by a named replacement that runs on a frozen tree; 15 never requires the replacement to run on the shipped tree. 20/21 govern in-wave edit ordering and receipt sha labels, both of which the round followed. No criterion names a file in a retained manifest's `inputs` as gate machinery. |
| **R16-C2a** stale instruction | `SKILL.md:1581-1586` still states the pre-round step 2/3 outcomes; only the registry row at `:1681` and errata row at `:1741` were annotated (`spotcheck §2 C2, §6.2`) | 15, 4 | **15** (partial) | Steps 2–3 are retained expectations that the moved input falsifies; 15 requires explicit effect or supersession and its reconciliation command was not run against the recipe. The errata row records the registry row, not the recipe, so the expectation's own site is unmarked. Criterion 4 governs the append form only. |
| **R16-C2b** sha-only credit | The round-14 bucket credits at section sha `e8720037…` with `commands_executed_count: 4` and no input digests, though CR26 ran against runner `75ed934d` and the landing rev ships `0673d2e5` (`ledger.json` entry; `measure.py:178-210`; `spotcheck §2 "Why C2 still fails", §6.3`) | 13, 12, 2 | **none** | 2 accepts the section sha as a measured anchor; 12 freezes witnesses but does not tie section credit to command inputs; 13 separates partial from full-page scope, not input identity. |
| **R16-C2c** box-3 overclaim | `SHONEN.md:10` says "wrong expectations repaired and re-read"; one bucket is stale at the landing rev, yet the v1 measure returned `box3_full_page: true`, 54/54, restraint 8 (`spotcheck §6.4`; my run) | 13, 1, 2 | **none** | 13's partial-vs-full rule does not define full-page credit per bucket; 1 and 2 pass under the sha-only rule (the claim is falsifiable and cites the ledger). The hole is the rule, not the anchor's presence. |
| **R16-EV1** stale receipt | `.ufo/evidence/round-16/round-gate/runner-sha256.txt` first line `89722ddb…`; landed runner `0673d2e5…`; at `98bea7d` the file contains no occurrence of the landed sha (`grep -c` = 0) and no correction (`spotcheck §2 C1 minor defect, §6.5`) | 21, 18, 4 | **none** | 21 requires the instrument sha beside the receipt (present, stale-value); 18's "corrected by an appended record" clause is scoped to attribution receipts; criterion 4 governs the append form once a correction exists. Nothing triggers on a digest that no longer recomputes. |
| **R16-MON1** selftest-only monitor | `ToolsNoHarm.md` ran nine `--selftest` invocations, all exit 0, and no registered entry command; the live-tree disposition gate was already 2 at its `c699c8c` snapshot (`spotcheck §3, §6.6`; `ToolsNoHarm.md` results table) | 17, 12 | **none** | 17 classifies a tool by behaviour and requires a standalone selftest, but sets no monitor coverage; 12 requires declared defects be reported, and the monitor declared none. Selftest green was treated as no-harm proof. |

No existing criterion is violated by the *repairs* to OP1/C2b/EV1/MON1; the
point of the table is that the 1–22 set had no rule that would have failed the
pre-repair state. Criteria 23–26 add those rules. C2a stays with 15; 24 adds the
live-tree run that makes the recipe's step fail loudly rather than only by
inspection.

## 3. Draft criteria 23–26

Append under a new `## Criteria appended — round 17` heading after criterion 22
(`corpus/QUALITY.md:116-123`). `REV` is the measured commit in every check.
Coverage of the four named defect classes: 23 covers C2b and C2c; 24 covers
OP1 and reinforces C2a; 25 covers MON1; 26 covers EV1. None of 23–26
supersedes 1–22: 23 tightens the credit rule under 13, 24 tightens 15/20/21,
25 extends 17, and 26 extends 18's appended-record rule.

23. Cold-read credit is input-keyed, not section-sha-only. An entry with
    `commands_executed_count > 0` credits only when its report's `inputs` map
    is non-empty and every recorded sha256 equals that lane path's blob at the
    measured revision; an entry with no executed commands keeps the section-sha
    rule, and `external_inputs` are reported but never credit. The measure
    withholds the bucket as `inputs-unrecorded`, `input-missing:<path>` or
    `input-drift:<path>`; the SHONEN box-3 assertion is backed by
    `box3_full_page: true` from that same measurement and is corrected by
    append when a bucket loses credit. Check:
    `python3 .ufo/evidence/round-17/measure.py --rev "$REV" --ledger-rev "$REV":.ufo/evidence/round-16/coldread/ledger.json`
    must report `box3_full_page: false` for the round-16 ledger (no `inputs`),
    and a v2 entry recording `tools/mutate-and-run.sh` at the CR26 runner
    `75ed934d…` must be withheld at `98bea7d` as
    `input-drift:tools/mutate-and-run.sh`; `--selftest` must contain that drift
    red-before.
    (`lessons/round-16-verifier-spotcheck.md` §2 "Why C2 still fails", §6 item 3;
    `.ufo/evidence/round-16/coldread/ledger.json` entry 1563–1596.)

24. A lane file named in a retained evidence manifest's `inputs` is part of
    that gate's contract. A round that changes one runs the affected gate on
    the candidate tree and retains its registered exit; a moved `tools/`
    instrument may be re-pinned through an appended supersession that names the
    path, its rev and the historical read, but the superseded gate must still be
    run on the candidate tree, and evidence bytes never move. A `git archive`
    of an older commit is not that run; a gate whose row registers a clean exit
    is not converted to a by-design could-not-evaluate by prose, but re-pinned,
    superseded, or retired as named debt. Check:
    `python3 tools/registry-check.py --rev "$REV" --json` must end
    `REGISTRY_CHECK: held=N/N`, and
    `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-17/dispositions.json --json`
    must exit 0;
    at `98bea7d` the round-14 manifest exits 2
    `expected_input_digest_mismatch` (runner `75ed934d…` pinned, `0673d2e5…`
    observed; `.ufo/evidence/round-17/op1-redbefore-98bea7d.txt`).
    (`lessons/round-16-verifier-spotcheck.md` §2 C2, §3 operability, §6 item 1;
    `.ufo/evidence/round-13/expected.json:12`.)

25. A no-harm monitor's scope is the registered entry set, not the selftest
    set. Every `status: active` row of `tools/registry.json` runs at the
    candidate rev and its receipt records argv, expected exit and observed
    exit, including each gate's live-tree form; a green selftest suite is one
    row, never the monitor, because every selftest can pass while a registered
    command returns the wrong exit. The monitor is itself no-harm: fixture-
    creating selftests run in a `/tmp` clone with `GIT_DIR` and
    `GIT_WORK_TREE` unset, and the lane's `git rev-parse HEAD` and
    `git status --porcelain` are identical before and after the monitor's run
    (its own report excepted). Check:
    `python3 tools/registry-check.py --rev "$REV" --json` exits 0 with
    `REGISTRY_CHECK: held=N/N` over the `status: active` rows, the monitor
    receipt's `ROW` lines cover every row name in `tools/registry.json`, and
    a before/after `git -C <lane> rev-parse HEAD` plus `git status --porcelain`
    comparison is empty; at `98bea7d` the live-tree disposition gate
    observes 2 (round-14 manifest) against the expected 0
    (`.ufo/evidence/round-17/op1-redbefore-98bea7d.txt`).
    (`lessons/round-16-verifier-spotcheck.md` §3 operability, §6 item 6;
    `.ufo/waves/round-16/w2/ToolsNoHarm.md` ran nine selftests only.)

26. A retained `<sha256>  <path>` receipt is a currency claim: the path's blob
    at the rev that ships it must hash to the recorded value, or the file must
    carry a dated appended correction naming the recorded digest, the observed
    digest, the path and the revs at which the observed digest holds; a receipt
    with an explicit rev field is checked at that rev. The original line is
    never rewritten, and after a correction `grep -F <observed>` on the
    receipt must succeed. Check:
    `git show "$REV:tools/mutate-and-run.sh" | sha256sum` against the first line of
    `.ufo/evidence/round-16/round-gate/runner-sha256.txt`: at `98bea7d` the
    line is `89722ddb…`, the artifact is `0673d2e5…`, and
    `git show 98bea7d:.ufo/evidence/round-16/round-gate/runner-sha256.txt | grep -c 0673d2e5` returns 0.
    (`lessons/round-16-verifier-spotcheck.md` §2 C1 minor evidence defect,
    §6 item 5.)

## 4. Check matrix — the command that can fail each criterion

| Criterion | Failing command | Pass condition | R16 red-before |
|---|---|---|---|
| 23 | `python3 .ufo/evidence/round-17/measure.py --rev 98bea7d --ledger-rev 98bea7d:.ufo/evidence/round-16/coldread/ledger.json` | round-14 bucket withheld; `box3_full_page: false`; a drift fixture withheld as `input-drift:tools/mutate-and-run.sh` | v1 credits it: `measure.py` exit 0, `box3_full_page: true`, 54/54, restraint 8. `[INFERENCE]` for the v2 output; measured v1 output above. |
| 24 | `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json` at `98bea7d` | exit 0 clean | exit 2, `expected_input_digest_mismatch` (`op1-redbefore-98bea7d.txt`, recorded). Green after the v2 manifest is `[INFERENCE]` until the v2 reader is installed. |
| 25 | `python3 tools/registry-check.py --rev 98bea7d --registry tools/registry.json --json` | exit 0, `REGISTRY_CHECK: held=N/N` | disposition row `expect=0 got=2` → `differs`. `[INFERENCE]`: the registry and checker do not exist at read time. |
| 26 | `git show 98bea7d:tools/mutate-and-run.sh \| sha256sum` and `git show 98bea7d:.ufo/evidence/round-16/round-gate/runner-sha256.txt \| grep -c 0673d2e5` | recorded line equals the artifact, or the observed digest appears in an appended correction | line `89722ddb…` vs artifact `0673d2e5…`; `grep -c` = 0, exit 1 (measured). The working-tree append (4 added lines, `git diff 98bea7d -- …runner-sha256.txt`) satisfies the check once committed. |

The current working-tree `runner-sha256.txt` correction is evidence the repair
form is usable: original line unchanged, dated correction naming
`89722ddb…`, `0673d2e5…`, four revs, and the recompute command. It is not yet
committed (`git status --porcelain` shows ` M`), so the landing must include it.

## 5. Residual risk and verification gaps

- Criteria 23 and 25 depend on wave-1 tools that did not exist at read time
  (`.ufo/evidence/round-17/measure.py`, `tools/registry.json`,
  `tools/registry-check.py`). Their check commands and expected outputs are
  bound by the interface contracts, not executed; every unexecuted exit above
  is marked `[INFERENCE]`. Criterion 24's green side is likewise unexecuted.
- Criterion 24's supersession path is restricted to `tools/` instruments by
  contract A; a moved evidence file cannot be superseded and must keep its
  bytes immutable. The criterion deliberately says so.
- Criterion 23's v1-ledger red-before (`inputs-unrecorded`) and its drift
  red-before (a v2 entry recording `75ed934d`) are distinct failure reasons;
  both must be present, or a measure that only handles one of them passes the
  wrong fixture.
- Criterion 26 applies to bare `<sha256>  <path>` receipts. A receipt that
  records a historical run must name its rev; without that field the currency
  claim is the test. The R16 receipt has no rev field, hence stale.
- No tool installs or updates were made; no sibling or lane evidence bytes were
  touched. Falsifier execution was limited to the read-only recomputes above.
- Live-repo state observed while reading (`date -Is` 12:30:55): the lane's git
  `HEAD` was detached at `e16adb7 selftest-fixture-noexec`, with
  `f8832ef selftest-fixture` → `0559c60 selftest-fixture-exec` → `e16adb7`
  committed at 12:29:33 on top of `98bea7d`; `master` still resolved to
  `98bea7d`. The worktree files I read hash equal to their `98bea7d` blobs
  (`corpus/QUALITY.md` `1b6d2d63…`, `SKILL.md` `906fb649…`, `SHONEN.md`
  `4a11ade5…`), so this report's citations are unaffected. Traced to
  `tools/mutate-and-run.sh`'s selftest fakerepo commits (`:1533`, `:1591`,
  `:1626`; staged copy `:1548`, `:1606`, `:1641`): those `git -C "$grepo"`
  calls do not scrub `GIT_DIR`, so an exported `GIT_DIR` made them commit into
  the lane `.git`. The round-16 G5 `env -i` guard covers the node suite, not
  these fakerepo legs. The commits are not mine; if they persist at landing,
  the L1 must re-anchor HEAD to `master` (or let jj re-export) before
  committing, or `git add -A` will stage the three fixture files' deletion and
  the whole tree as new. L1 was messaged at 12:32 with these facts; criterion
  25's monitor-immutability clause is written to catch this class.

## Verdict

built — six R16 routed defects mapped (one captured by 15, five `none`), four
checkable criteria 23–26 drafted with explicit failing commands and red-before
anchors.

# RerunC1: round 18, wave 2. Re-running C1's count (depth 7 -> 8)

Seat: TameshiR18.RerunC1 (wave-2 falsification). Read rev: `01d586ddbc5fcd78659557c4e93a6ee8517b87d1`.
Clone: `W=/tmp/tameshi-r18w2-RerunC1-7jKOjM`, `C=$W/fleet/tameshi-shokunin`. I made it with the contract's
clone recipe: sibling symlinks in `$W/fleet`, a detached checkout, and `git rev-parse HEAD` = `01d586dd…` (exit 0).
Every mutating run used `bwrap --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp --bind $W $W --unshare-net
--die-with-parent --chdir <dir> env -i PATH=… HOME=$W/h-<run>/home TMPDIR=$W/h-<run>/tmp LC_ALL=C …`.
Host tools: node v24.21.0, git 2.56.0, bash 5.3.20, Python 3.14.8, bwrap 0.13.1. I installed or updated nothing.

Verdict: **holds**. Each counting step reproduces exactly. The issues below concern the entry's text and the
robustness of the ruler; none of them changes the count.

## Findings by severity

There are no critical or high findings against C1.

### M1 (minor; how accurate C1's entry is, not the count): the entry still says "not yet landed", which 58e5d53 made false

`corpus/knowledge/mutation-case-kumitate-sources-check.md` (sha256 `79f629b4…`) was touched by only one commit, 58e5d53.
At 01d586d it still describes the state before landing:

- `:1` lists S008 as "(paper, tier A, **queued** — … not yet a mined row)". `:215` says "S008 is `queued` with
  `used-by —`". But at 01d586d, `corpus/SOURCES.md:19` shows S008 as `mined`, with used-by =
  `corpus/knowledge/mutation-case-kumitate-sources-check.md`. Command: the S008 row via `git show REV:corpus/SOURCES.md`
  was `queued` at 183f87b/93d22aa/aee4f36 and `mined` at 58e5d53/e08271a/01d586d.
- `:174-183` says "Status: the leg is not installed at base … The leg lives in the staged runner
  `.ufo/waves/round-18/staged/tools/mutate-and-run.sh` … An installed-runner receipt is pending the L1 install."
  `:171` also cites "staged runner `:620`". At 01d586d the leg is installed in `tools/mutate-and-run.sh` at
  `:93` (ledger), `:611-612` (pin/rev), `:620` (table), `:1015-1072` (spec heredoc), `:1349-1353` (regression call)
  and `:1879` (selftest tuple). My regression receipt below is an installed-runner receipt that includes the runner sha.
- `:215-218` lists obligations that are still unmet at 01d586d. "S001 (used-by `mutation-score-semantics.md`) and
  S052, S056, S057 (used-by `mutation-case-kumitate-round-gate.md`) need this entry added to used-by." In fact,
  `corpus/SOURCES.md:12` (S001) still lists only `corpus/knowledge/mutation-score-semantics.md`, and `:61`, `:65`,
  `:66` (S052/S056/S057) list only `corpus/knowledge/mutation-case-kumitate-round-gate.md`. The L1 has to decide
  whether the lane's source rules require symmetric used-by before admission.

### M2 (minor; calibration of the ruler): command D counts comment lines that no selftest ties to the replayed legs

Command D (`SCORECARD.md:73`) counts header comment lines that match `^#   (js|bash)-\S+\s+\S+\s+\d+/\d+`
(`tools/mutate-and-run.sh:86-93` at 01d586d). Nothing in the runner reads those lines: a grep of the runner for the
`^#   ` pattern finds nothing. The selftest's leg-count agreement (`tools/mutate-and-run.sh:1866-1870`) compares call
sites, spec files and `nlegs`, and `:1871-1882` checks the tuple count. Neither covers the header ledger.

Probe: I copied the 01d586d runner to `$W/probe/tools/mutate-and-run.sh` and added one fake ledger line,
`#   js-phantom-leg        kumitate-shokunin/scripts/none.mjs          9/10 (90 %)`.
- Command D's regex on the copy: `recorded_cases=9`.
- `bash $W/probe/tools/mutate-and-run.sh --selftest` (bwrap, no GIT_*): exit 0, `MUTATE_SELFTEST: 96/96 pass`,
  `VERDICT: PASS`. Its stdout is byte-identical to the unmodified selftest (sha256 `a438399e…` for both).

So one comment line can raise the depth score with no replayed leg behind it. At 01d586d this has not happened:
8 header lines, 8 calls, 8 spec files, `nlegs=8` (`:1355`), and 8 legs PASS. This is a residual risk for later
rounds, not a falsification of C1. A fix would be to add the header count to the leg-count agreement, or to have
command D count `regression_case_git` call sites.

### M3 (info): the pre-registration margin is 68 s; nearby activity on disk

- predictions.json was committed at 19:40:21Z and the sweep ran at 19:41:29Z, 68 s later (see check 5).
- A pristine control run happened at 19:39:01Z, before the commit. Evidence: the mtime of
  `/tmp/tameshi-r18w1-X01CaseSpec-mPCKzd/control.stdout`; the run is recorded as `control.txt` in 93d22aa. It
  mutated nothing, so it is consistent with "before any mutant".
- A placeholder integration regression ran in `/tmp/tameshi-r4-2-regression.p545BJ`. Its runner was
  `/tmp/tameshi-r18w1-X02RunnerLeg8-9lpK4u/…`, sha `4cf65d11…`. At 19:40:41Z, 20 s after the commit, it built two
  dummy assertion mutants (`R18D1`/`R18D2`) and stopped at `MUTATE: SETUP (spec/preparation failed for 1 defect(s);
  no suite run)`.
- `/tmp/tameshi-r4-2-regression.WwUUC0` ran the dummy mutants at 19:43:32Z, after the sweep.
- Neither of those runs used the registered defects, and neither ran before 93d22aa. The earliest
  registered-defect mutant on disk is from 19:41:29Z.
- [INFERENCE] Runs that pass delete their scratch automatically, so this /tmp scan cannot rule out an earlier run
  that was cleaned up. I found no positive evidence of one.

## Checks run (commands, exits, key output)

1. **Command D, both revisions.** I ran the text of `SCORECARD.md:73` verbatim from `$C`:
   `git show "$REV:tools/mutate-and-run.sh" | python3 -c '…'`.
   - REV=`183f87b899e6cae46be98d251cbc87fb5118f6ca` → `recorded_cases=7 depth_score=7`. PIPESTATUS 0/0.
   - REV=`01d586ddbc5fcd78659557c4e93a6ee8517b87d1` → `recorded_cases=8 depth_score=8`. PIPESTATUS 0/0.
   - The ruler did not move: SCORECARD line 73 is byte-identical at both revisions (line sha256 prefix
     `1cba484cac13f547` at both). Lane `SCORECARD.md` sha256 = clone sha256 = `be578181…`.
   - Intermediate revisions: 93d22aa=7, aee4f36=7, 58e5d53=8, e08271a=8. Between 183f87b and 01d586d the only change
     to a counted line is `+#   js-sources-check      kumitate-shokunin/scripts/sources-check.mjs 5/10 (50 %)`
     (`tools/mutate-and-run.sh:93`).
2. **`bash tools/mutate-and-run.sh --regression` at 01d586d, with no GIT_* variables** (`env -i`, none set):
   `--workdir $W/regA --keep`, exit 0.
   - `REGRESSION_TOOL: …/tools/mutate-and-run.sh sha256=d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b`
     (this equals the blob at 58e5d53/e08271a/01d586d).
   - `REGRESSION_PIN js-sources-check: source=git repo=$W/fleet/kumitate-shokunin rev=0acb7752d19058b953ebbeba253b1e35f6548de5 path=scripts/sources-check.mjs mode=100755 sha256=6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f`
   - `REGRESSION_TABLE js-sources-check: match=10/10 recorded-killed=5 measured-killed=5 survived=5 inconclusive=0 flips=0`
   - `REGRESSION_CASE js-sources-check: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)`
   - Legs 1-7 also PASS, each with match=N/N and flips=0.
   - `REGRESSION: PASS (cases=8 passed=8; ledger legs exact: killed-delta<=0 flips<=0)`
   - Leg-8 sweep log: `CONTROL: GREEN (exit=0 …)` and `MUTATE_RESTORE: OK`.
   - Second variant with the contract template `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1` (`$W/regB`):
     exit 0. Its 46 lines are identical to regA once the workdir path is normalised (`diff <(sed "s#$W/regA#WD#g" regA.stdout) <(sed "s#$W/regB#WD#g" regB.stdout)`
     exit 0), ending `REGRESSION: PASS (cases=8 passed=8; …)`.
3. **`bash tools/mutate-and-run.sh --selftest` at 01d586d, with no GIT_* variables:** exit 0.
   - `PASS leg-count agreement: calls=8 specs=8 nlegs=8 (want 8)`
   - `PASS leg-count agreement: selftest leg tuples=8 (want 8)`
   - `PASS embedded leg js-sources-check: spec and recorded table agree`
   - `MUTATE_SELFTEST: 96/96 pass`, `VERDICT: PASS`. stderr was empty.
4. **The leg-8 spec matches the pre-registration byte for byte.**
   - Static check: I extracted the heredoc body (`tools/mutate-and-run.sh:1016-1071`, ending in `EOT` at `:1072`)
     from `git show 01d586d:tools/mutate-and-run.sh`. sha256 `c8d24cb4b6b1a372543764fc27c9d16f65510a29fed1045bedb2863ce2408c91`,
     56 lines, 3358 bytes.
   - `git show 93d22aa:.ufo/evidence/round-18/sources-check/sources-check.defects.spec` has the same sha256.
     `cmp` exit 0.
   - Runtime check: the spec file the runner itself wrote (`$W/regA/specs/js-sources-check.spec`,
     `$W/regB/specs/…`, `$W/regA/js-sources-check/spec.copy`) is also `c8d24cb4…`. `cmp` against the 93d22aa blob:
     exit 0.
   - Only 93d22aa ever touched the spec (`git log -- …defects.spec`). The lane working file is also `c8d24cb4…`.
     This value matches `sweep/sweep.txt:3` (SWEEP_SPEC_SHA256) and `spec_sha256` in predictions.json.
5. **predictions.json was committed before the sweep.**
   - `git log --format='%H %cI %aI' -- .ufo/evidence/round-18/sources-check/predictions.json` →
     `93d22aa21a144a0e2833b1be74718d15060f002b 2026-10-20T16:40:21-03:00 2026-10-20T16:22:36-03:00`.
     That is the only commit that touches the file. Its blob, `0a440c2b…`, is the same at 93d22aa and 01d586d.
   - `sweep/sweep.txt:8` reads `MUTATE_DATE: 2026-10-20T19:41:29Z`. The commit time 16:40:21-03:00 = 19:40:21Z,
     so the predictions were committed **68 s before** the sweep.
   - The lane's `.git/logs/refs/heads/master` (I only read it) has `183f87b… 93d22aa… … 1792525221 -0300  export from jj`,
     and `date -u -d @1792525221` = `2026-10-20T19:40:21Z`.
   - `sweep.txt:2` reads `SWEEP_CONTEXT_COMMIT: 93d22aa…`. The sweep's mirror still exists at
     `/tmp/tameshi-r18w1-X01CaseSpec-mPCKzd/sweep-mirror/fleet/tameshi-shokunin`. Its `HEAD` is `93d22aa…`, and its
     predictions.json sha256 `5749a27a…` equals the lane's.
   - The sweep's mutants, `/tmp/tameshi-r4-2-run.ZIz4V0/mutant-*.sources-check.mjs`, have mtime 16:41:29.59-03:00,
     which is 19:41:29Z.
6. **Further checks:**
   - Re-ran the sweep with the pre-registration runner: the runner at 93d22aa (sha `fb6d86d5…`, the same as
     `sweep.txt:7` MUTATE_TOOL), the pinned blob, the 93d22aa spec and `suite.txt`. In bwrap, exit 0:
     `CONTROL: GREEN`, the same 10 verdicts, `MUTATE: DONE (… defects=10 killed=5 survived=5 inconclusive=0 kill-rate=50%)`.
     This matches `sweep.txt:112`, `:130` and `:131`.
   - Mutant bytes: for each of the 10 ids, the mutant sha256 in the recorded sweep (`/tmp/tameshi-r4-2-run.ZIz4V0/results.tsv`)
     equals the one in my leg-8 replay (`$W/regA/js-sources-check/results.tsv`), and so do the verdicts (10/10).
   - These four sources agree exactly: the predictions in predictions.json, the spec's `# PREDICT` comments,
     `TABLE_SOURCESCHECK` (`tools/mutate-and-run.sh:620`), and the verdicts my regA run measured.
   - `suite.txt` at 93d22aa (sha256 `6e550d5a…`) equals the runner's leg-8 suite string plus a trailing `\n`
     (`tools/mutate-and-run.sh:1351`).
   - Pin: `git -C kumitate show 0acb7752:scripts/sources-check.mjs | sha256sum` = `6a293a72…`. The blob is mode
     100755 and 897 lines long, as the spec header says. `merge-base --is-ancestor 0acb7752 HEAD` exits 0 and the
     commit is on `refs/heads/master`, so a gc cannot prune it.

Hashes of the full stdout files: regA `0e15eca7…`, regB `d8547a81…`, selfA `a438399e…`, sweep93 `97970476…`,
probe selftest `a438399e…`. They live under `$W`, which is ephemeral; the key lines are quoted above.

## Residual risk and verification gaps

- Everything ran on one host. regA, regB and selfA ran at the same time on 32 cores (load average about 7), and so
  did the sweep93 re-run and the probe selftest. All of them passed, which is evidence against timing flakes but
  does not prove there are none.
- The evidence for the ordering (committer date, reflog, file mtimes) is all on this host, and the lane owner could
  have written any of it. The sources agree to the second, but there is no external timestamp authority.
- I did not re-check the C2 claim, the calibration monitor or the S001/S008 source content. Other seats cover those.
- I did not read other seats' reports.
- I am not a CR seat, so I wrote no trace-inputs receipts.
- Lane safety:
  - In the lane and sibling repos I ran no git writes and no jj.
  - Reads in my /tmp clone: `git show/log/rev-parse/diff`.
  - Reads of the lane's `.git/logs/*`: `cat`/`tail` only.
  - Read-only git on kumitate: `show`, `ls-tree`, `merge-base`, `for-each-ref`.
  - Every run used `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR`, or `env -i` inside a bwrap
    where only `$W` was writable.
  - This report is my only write to the lane.

Final verdict: **holds**. Command D gives 7 at 183f87b and 8 at 01d586d. `--regression` exits 0 with 8/8 legs PASS
(leg 8 match=10/10, 5/10 killed) and `--selftest` exits 0 with 96/96. The embedded leg-8 spec is byte-identical to
the 93d22aa pre-registration (`c8d24cb4…`), and predictions.json was committed at 19:40:21Z, 68 s before the 19:41:29Z
sweep. The minor findings are the stale entry text (M1) and the unbound comment ledger behind command D (M2).

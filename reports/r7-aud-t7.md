# AUD-T7 — verdict table: audit of the 4-leg `--regression` ledger (TAMESHI-T7-1, tameshi round 7)

Audit run 2026-10-14 18:2x–18:4xZ by lane AUD-T7 (round-7 wave, width 32; lane
scratch `/tmp/w7-aud-t7-*`). **Read-only: no fleet file was written or edited by
this audit**; the audited tool, both sibling gates and the tameshi tree were
handled read-only throughout (pre/post `git status` identical; §4). No
substrate-mutating command was run; no secret file read; no external site
contacted. Flip-test mutants ran on scratch copies under `/tmp/w7-aud-t7-fake-*`;
the real tool was executed as-is for the primary run only (a `--regression` run
writes under `--workdir` only). Write scope: this report file only.

**Audited revision.** `tameshi-shokunin/tools/mutate-and-run.sh` sha256
`cf41efaa8be5f52d92bf7806ddb3a99a031547bf12a6811b8ef45bce37242c75`, 1,341
lines / 61,632 B, mtime 2026-10-14 15:29:01 -03; `git status` = ` M`
(uncommitted, lane T7-1); `git diff --stat` vs HEAD `4494715` = **+337/−76**
(HEAD blob `b56c6e57…`, the r6 revision). Header `:8-14` names the change:
"— every recorded mutation case replayed at its pinned original revision,
materialized from its repo's git object store (`git show <rev>:<path>`, immune
to working-tree drift)". Frozen copy: `/tmp/w7-aud-t7-work/tool-cf41efaa.sh`
(byte-identical at freeze and at write time). **No drift**: at audit close
(18:40Z) the live sha and mtime are unchanged; verdicts below bind to
`cf41efaa` — a later edit needs re-audit.

## 0. What was audited

The r7-1 ledger engine: `regression_case` (`:733-876`) with its git-materialization
branch (`:756-780`), `regression_case_git` (`:878-889`), the four recorded
pin/revision/table pairs (`:511-522`), the four leg invocations
(`:927-946`), the summary/exit map (`:948-977`). The four legs, as landed:

| leg | target @ revision | pin (sha256) | recorded table |
|---|---|---|---|
| js-kimi-census | `kumitate-shokunin/scripts/kimi-census.mjs` @ `175de6b` | `83016d45…f2724f426` | 8/10 killed (80 %) |
| bash-surface-census | `kagi-shokunin/corpus/surface-census.sh` @ `fecee87` | `275d8294…db53009f` | 8/10 killed (80 %) |
| bash-tsukuroi-census | `tsukuroi-shokunin/tools/tsukuroi-census.sh` @ `165307fe` | `084951be…c5809c78c5` | 6/10 killed (60 %) |
| bash-mado-verify | `mado-shokunin/tools/mado-verify.sh` @ `eead56b` | `d7edaab4…32d0e13` | 4/10 killed (40 %) |

Ledger legs run at **exact** tolerance (`regression_case_git` passes `0 0`,
`:888`; band line `:918`); the r4-2 fixture mode keeps ≤1/≤1. The round-7
plan states the expectation as `flips=0`, table intact
(`plans/round-7.plan.md:32-35`) — the landed exactness matches it.

## 1. Run it yourself — primary run (O)

`bash tools/mutate-and-run.sh --regression --workdir /tmp/w7-aud-t7-regr/run1`,
2026-10-14T18:34:47Z, **exit 0, 44.9 s wall**; output
`/tmp/w7-aud-t7-evidence/run1.out`. Headline lines, verbatim:

```
REGRESSION_EXPECT: recorded kill-rates — js-kimi-census=8/10 bash-surface-census=8/10 bash-tsukuroi-census=6/10 bash-mado-verify=4/10
REGRESSION_TABLE js-kimi-census: match=10/10 recorded-killed=8 measured-killed=8 survived=2 inconclusive=0 flips=0
REGRESSION_TABLE bash-surface-census: match=10/10 recorded-killed=8 measured-killed=8 survived=2 inconclusive=0 flips=0
REGRESSION_TABLE bash-tsukuroi-census: match=10/10 recorded-killed=6 measured-killed=6 survived=4 inconclusive=0 flips=0
REGRESSION_TABLE bash-mado-verify: match=10/10 recorded-killed=4 measured-killed=4 survived=6 inconclusive=0 flips=0
REGRESSION: PASS (cases=4 passed=4; ledger legs exact: killed-delta<=0 flips<=0)
```

Per-leg `REGRESSION_CASE …: PASS (band: killed-delta<=0 flips<=0
inconclusive=0 defects=10)` ×4. Survivor census read from each case's
`results.tsv` (O):

| leg | measured survivors | = recorded |
|---|---|---|
| js-kimi-census | D2, D10 | ✓ |
| bash-surface-census | B5, B10 | ✓ |
| bash-tsukuroi-census | B7, B8, B9, B10 | ✓ |
| bash-mado-verify | D3, D5, D7, D8, D9, R1 | ✓ |

Every case's `sweep.log` carries `CONTROL: GREEN` and `MUTATE_RESTORE: OK`
(target = the materialized copy; before = after = the leg's pin sha); every
case ran as a full CLI sub-invocation of the same tool (`REGRESSION_SWEEP`
lines). Supporting: the audited revision's own `--selftest` → `MUTATE_SELFTEST:
67/67 pass` / `VERDICT: PASS`, exit 0 (`/tmp/w7-aud-t7-evidence/selftest-cf41efaa.out`);
r6's count was 55/55 — the +12 are the r7-1 ledger-engine cases.

## 2. Each leg's pin resolves from git blobs — not the working tree (O)

Independent re-derivation (my own commands; `/tmp/w7-aud-t7-evidence/pin-verification.txt`),
run 18:35:47Z on the live repos:

| leg | `rev:path` object id | `git show` / `cat-file` sha = pin | materialized copy = pin | worktree file = pin |
|---|---|---|---|---|
| js-kimi-census | `a2bf15c08ca0…` | YES / YES | YES (run1 case dir) | YES (`83016d45`; clean) |
| bash-surface-census | `dcf878b95e17…` | YES / YES | YES | YES (`275d8294`; clean) |
| bash-tsukuroi-census | `dfcf6f596fab…` | YES / YES | YES | **NO** (`bba6cdf6…`; ` M`, lane S7 mid-edit) |
| bash-mado-verify | `7ccc601f8139…` | YES / YES | YES | **NO** (`90d50cdd…`; ` M`, lane M7 mid-edit) |

- Legs 3/4 are the discriminating cells: their recorded revisions are
  **historical** (`165307fe` / `eead56b`) while the HEADs have moved on
  (`dc3436d` / `c8f6667`) and both working trees are dirty and *moved during
  this audit window* (tsukuroi `d666bba3`→`bba6cdf6`; mado `c4c1afb7`→`90d50cdd`).
  Both legs still PASSed at their recorded tables — the replay bytes cannot
  have come from the working tree.
- Cross-lane corroboration: my two materialized copies are byte-identical
  (`cmp`) to the T7-1 lane's git extracts `/tmp/w7-tameshi-1-pins/
  {tsukuroi-165307fe,mado-eead56b}.sh`.
- The run's own `REGRESSION_PIN` lines (run1.out) carry the same four
  `source=git repo=… rev=… path=… sha256=…` cells quoted in §0.

## 3. Flip-test the guard — on a scratch copy (O)

Four flips against copies of the frozen revision, run from scratch fleet roots
(`/tmp/w7-aud-t7-fake-*`; repos symlinked — except F3's decoy clone). Outputs
`/tmp/w7-aud-t7-evidence/f{1,2,3,4}-*.out`.

| # | flip | expectation | observed | exit |
|---|---|---|---|---|
| F1 | pin flip: `PIN_TSUKUROI` `…951be…` → `…951bf…` | leg 3 refuses; no PASS | `REGRESSION_CASE bash-tsukuroi-census: SETUP (pin mismatch: recorded=…951bf… materialized=…951be…)`; other three legs PASS; `REGRESSION: SETUP (cases=4 passed=3 cannot-verify=1)` | **2** |
| F2 | revision flip: `REV_TSUKUROI` → `dc3436d` (blob `aae45531`) | leg 3 refuses (bytes ≠ pin) | `SETUP (pin mismatch: recorded=…951be… materialized=aae45531…)`; `REGRESSION: SETUP (cases=4 passed=3 cannot-verify=1)` | **2** |
| F3 | worktree decoy: clone of tsukuroi, worktree file replaced by `DECOY` (`18feeb0b…`, clone ` M`), git store intact | leg 3 still PASSes (bytes from git) | all 4 PASS; `REGRESSION: PASS (cases=4 passed=4 …)` | **0** |
| F4 | table flip: `TABLE_TSUKUROI` `B7:SURVIVED`→`KILLED` | leg 3 goes red, names the row | `REGRESSION_DEFECT bash-tsukuroi-census B7: measured=SURVIVED recorded=KILLED`; `match=9/10 … flips=1`; leg `FAIL (out of band: killed-delta=1 flips=1…)`; `REGRESSION: FAIL (cases=4 passed=3 failed=1 setup=0)` | **1** |

Reading: the guard is fail-closed in both directions — **sensitive** to pin and
revision tampering (F1/F2 SETUP, never a false PASS) and to a doctored
expectation (F4 FAIL), and **immune** to working-tree drift (F3 green from git;
§2's live drift green). Exit map used exactly as documented: 0 PASS · 1 FAIL ·
2 SETUP.

## 4. No-write proof (O)

- tameshi `git status --porcelain` byte-identical pre (18:34:47Z) and post
  (18:35:32Z) the run, apart from the timestamp line; the tool sha unchanged.
- The sibling trees were never written by this audit: their porcelain entries
  (tsukuroi ` M` gate + untracked notes; mado ` M` gate/LOG + untracked notes)
  are the owning lanes' own in-flight edits, present before my first read and
  carried unchanged through the audit; kumitate/kagi stayed clean at their pins.
- All mutants, clones and decoys live under `/tmp/w7-aud-t7-{work,evidence,regr,fake-*}`;
  the only in-tree artifact of this lane is this report.

## 5. Verdict

| # | claim audited | verdict |
|---|---|---|
| 1 | the 4-leg `--regression` runs and PASSes (cases=4 passed=4, exit 0) at the recorded tables, exact band | **CONFIRMED** |
| 2 | every leg's pin resolves from its repo's git object store (`show` = `cat-file` = pin), and the replay bytes are the materialized copy | **CONFIRMED** (4/4) |
| 3 | the replay is independent of the working tree (dirty + moving trees on legs 3/4; decoyed worktree on F3) | **CONFIRMED** |
| 4 | the guard fails closed on pin/revision tampering (SETUP, exit 2) and on expectation drift (FAIL, exit 1) | **CONFIRMED** (F1–F4) |
| 5 | no fleet file written by the audited run | **CONFIRMED** |

Observations (not findings): the exact (0,0) tolerance the ledger legs use is
stricter than the r4-2 fixture band and matches the round-7 plan's `flips=0`;
the plan's leg list said "cite-check r6 if landed" — cite-check stayed the 1/4
probe, and the realized 4th case is mado (whose r6 case did land; the ledger
note T7-2 §5/U3 "not yet embedded at this write" is superseded by this landing).

## 6. Spot-checks (three, re-runnable)

- **SC1** — `bash tools/mutate-and-run.sh --regression --workdir /tmp/w7-aud-t7-regr/run1`
  → `REGRESSION: PASS (cases=4 passed=4 …)`, rc 0; four `match=10/10 flips=0`
  tables (§1).
- **SC2** — per leg: `git -C <repo> show <rev>:<path> | sha256sum` equals the
  embedded `PIN_*`, and `cmp` of the run's `target.<basename>` against the
  blob; for tsukuroi/mado the worktree file sha differs (§2).
- **SC3** — F1–F4 on the scratch copies reproduce the observed exits
  2 / 2 / 0 / 1 and the exact SETUP/FAIL lines quoted in §3.

## 7. Unknowns

- **U1** — single host, 2026-10-14 (bash, node, python, git versions of this
  host); no cross-host or toolchain reading for the ledger's exact mode.
- **U2** — the audited revision is uncommitted; if T7-1 (or the round scribe)
  edits the tool after 18:40Z, these verdicts bind to `cf41efaa` and need
  re-audit (append-only).
- **U3** — cite-check's probe (1/4) is not a ledger leg; a future opt-in with
  a full spec is unmeasured.
- **U4** — the exact (0,0) mode's sensitivity means any genuine behaviour
  change in a swept gate flips the leg to FAIL by construction; whether that is
  the intended trade for future legs is the lane's convention, not measured here.
- **U5** — F3 used a clone; hardlink/alternates object stores (not used here)
  were not exercised.

## 8. Errata (append-only)

(none yet — new entries go below this line, never edits above)
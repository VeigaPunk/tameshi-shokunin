# RX7 — residual cold-read, SKILL.md 1749-1800 (round 16, wave 3)

Seat: TameshiR16.RX7 (reviewer, residual re-read after wave 2). Lane root
`/home/vgpnk/Projects/shokunin/tameshi-shokunin`; page read at
`05a224754db3c6fce18f5ec1816a6873bffe3d0e`. Read only lines 1749-1800 plus the files
that range names (case note, `$E/survivor-probes/*`, `tools/mutate-and-run.sh`,
`tools/repeat-control.py`, `measure.py`). No tool installs or upgrades were made.

## 0. Page identity

```
$ git -C … show 05a2247:SKILL.md | sha256sum
e289acec4e90c994d303b2dd6c844d907dc1bf48330ecd2fd253ac7379f794b3  -
$ … | wc -l
1807
$ … | sed -n '1749p'
## Seventh recorded case and full-page cold-read — round 16
```
Matches the cold-read interface sha. One heading in range (1749); 1800 is a blank
line. Scratch: `/tmp/tameshi-r16w2-RX7-probes-TPMDFu`, `/tmp/tameshi-r16-rg.w5idxO`
(created by the page's own `mktemp`). The `/tmp` worktree at 05a2247 was removed
after use (`git worktree remove --force` → exit 0; `worktree list` back to the lane
root only). Sibling repos were read only; `kumitate-shokunin status --porcelain`
→ 0 entries.

## 1. Reproduce block, as written

Run verbatim from the /tmp worktree; only the block's own `W`/`E` variables.

```
$ git -C ~/Projects/shokunin/kumitate-shokunin show 364f1d5…:scripts/round-gate.mjs | sha256sum
f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9  -     (1511 lines)
$ bash tools/mutate-and-run.sh --target "$W/round-gate.mjs" --defects "$E/round-gate.defects.spec" \
    --suite "$(cat "$E/suite.txt")" --label js-round-gate --workdir "$W/work"
MUTATE_TARGET: … sha256=f890e277… bytes=80415
MUTATE_SPEC: … defects=10
CONTROL: GREEN (exit=0 duration-ms=3693 pristine-sha256=f890e277…)
MUTATE_RESTORE: OK (target-sha256 before=f890e277… after=f890e277… pristine-sha256=f890e277…)
MUTATE: DONE (target=js-round-gate defects=10 killed=5 survived=5 inconclusive=0 kill-rate=50%)
SWEEP_EXIT=0
```

Matches the block's expect line exactly (control green, 5/10, 0 inconclusive,
restore OK), and `spec.copy` sha256 = `e99b87ebc16f045f43ffb31354e2fc2879d2be3a8504d4274239249b93ef11c4`
= the spec at the commit = `predictions.json.spec_sha256`.

Pre-registration anchors: `e69b488` is an ancestor of `05a2247`; committer date
`2026-10-20T10:39:59-03:00` = 13:39:59Z, i.e. 16 s before the case note's sweep
time 13:40:15Z; `git diff e69b488 05a2247 -- …/predictions.json` → empty. Programmatic
compare of `results.tsv` against `predictions.json`: 10 predictions, 10 measured,
**0 mismatches**, 5 KILLED / 5 SURVIVED / 0 INCONCLUSIVE, id sets equal. Measured
check ids (zero-padded) also match the case-note table: A1 fails `[1][2][3][12][16][21][22][27][46][47]`
plus `[51]` (nested 50/60); A3 `[52][53]`+`[51]` (58/60); B1 `[32][45]`+`[51]` (58/60);
E3 `[54]`+`[51]` (59/60); C1060 `[8]`+`[51]` (59/60).

## 2. Rules this case adds — re-executed

### 2.1 Scrub the environment (suite that shells out to git)

* The ledger leg carries the identical string: extracting the `js-round-gate` suite
  literal from `tools/mutate-and-run.sh` and comparing with `suite.txt`
  → `byte_equal: True`, 216 bytes, contains `env -i`, private `HOME`/`TMPDIR`,
  `GIT_CONFIG_NOSYSTEM=1`, `GIT_CEILING_DIRECTORIES`. `suite.txt` sha256
  `6e550d5a2f6a78fc0654c297b80bb042e8482423d80e2e16bab7374227931f7b`.
* **GIT_DIR hazard reproduced**: pristine suite with an exported
  `GIT_DIR=<scratch>/victim/.git` → suite exit 1; victim repo went from 0 to **43
  commits** (`round-5 fixture seed` / `round-5 fixture report` at HEAD c1cbc9d).
  So an inherited `GIT_DIR` really does redirect the fixture commits, and the
  control goes red (fixture threw before printing checks: `fixture … failed`).
* **TMPDIR-inside-a-worktree hazard reproduced**: `TMPDIR=<worktree>/.rx7-tmpdir-inside`
  → exit 1 with exactly **3** `FAIL` checks `[37]`, `[51]`, `[56]`; `[51]`'s nested
  tail is `58/60`. Matches "turns the control red" (case note: 3 checks).
* **"Scrubs; it does not confine" re-anchored**: a copy of the pristine gate with a
  top-of-file `fs.writeFileSync()` wrote the marker
  `/tmp/tameshi-r16w2-RX7-escape-marker` (8 B) from inside its `sandbox-CONTROL`
  cwd; `grep -nE 'bwrap|unshare|firejail|nsjail|seccomp' tools/mutate-and-run.sh`
  → none found. Hostile mutants are unconfined, as the page says. Network reach
  was not exercised; the mechanism is the same (no namespace/sandbox flags), and
  the pristine suite made 0 socket/connect calls under strace (below).

### 2.2 Grade by exit, not stdout bytes

* Three pristine runs under the exact suite string: exits **0 0 0**, stderr empty,
  63 lines each, stdout sha256 `dde6c1bf…`, `6bfd37e6…`, `27004954…` → differ
  byte-for-byte (mkdtemp suffix/sandbox path), as stated.
* `python3 tools/repeat-control.py --runs 3 --out … -- bash -c "$(cat suite.txt)"`
  with `WORKDIR`/`MUTANT`/`DEFECT_ID` exported → finding
  `REPEAT_CONTROL: controls_mismatch`, `REPEAT_EXIT: 1`, run exits `0 0 0`. The
  page's "repeated-control byte comparison reports controls_mismatch (exit 1)"
  reproduces exactly. `mutate-and-run.sh` classifies KILLED/SURVIVED from exit
  only (header contract + measured verdicts agree).

### 2.3 Projected interval at its edge

Upper edge from the sweep: `C1059 SURVIVED (exit=0)`, `C1060 KILLED (exit=1)`
(its 1059-B r8 fixture fails `[8]` as `REPORT_THIN`). Extra lower-edge probe in
/tmp (2-defect spec, same suite): `C26` (1024→26) **SURVIVED**, `C25` (1024→25)
**KILLED**, control green, restore OK. The projected `[26, 1059]` is therefore
tight at both ends, not just the upper one.

### 2.4 Survivor probes, pristine (exit 0) vs mutant (exit 1)

`GATE=<file> FXROOT=<fresh> node probes.mjs <id>`:

| survivor | probe | pristine | mutant | mutant log shape |
|---|---|---|---|---|
| A2 | P1 (FAIL-CLOSED tail) | exit 0, ALL ASSERTIONS PASS | exit 1, FAIL (1) | same as committed A2-P1-mutant-A2.log |
| A2 | P1b (remaining tails) | exit 0 | exit 1, FAIL (2) | matches committed log |
| B2 | P6 (tracked REPORTS_DIR_MISSING) | exit 0 | exit 1, FAIL (2) | matches |
| E1 | P9 (UFO_SRC set-value) | exit 0 | exit 1, FAIL (2) | matches |
| C1059 | `c1059-probe.sh` (report 1040 B) | exit 0, `ROUND_GATE: CLEAN` | exit 1, `REPORT_THIN (bytes=1040)` + DRIFT | matches committed c1059 logs |

CKIND has no probe by design: `grep -n FINDING_KINDS` at the pinned block gives
:171 (declaration) and :1488 (enum⊇observed reader) only, and mutant-CKIND runs
60/60 — the case note's equivalence-for-gate-behaviour argument holds.

## 3. Ledger leg

`bash tools/mutate-and-run.sh --regression` from a /tmp fleet layout (committed
lane bytes + symlinked sibling repos; FLEET_ROOT resolved in /tmp):

```
REGRESSION_PIN js-round-gate: source=git repo=…/kumitate-shokunin rev=364f1d5… mode=100755 sha256=f890e277…
REGRESSION_SWEEP js-round-gate: MUTATE: DONE (… killed=5 survived=5 inconclusive=0 kill-rate=50%)
REGRESSION_TABLE js-round-gate: match=10/10 recorded-killed=5 measured-killed=5 survived=5 inconclusive=0 flips=0
REGRESSION_CASE js-round-gate: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION: PASS (cases=7 passed=7; ledger legs exact: killed-delta<=0 flips<=0)   exit 0
```

All seven legs PASS at exact tolerance; `js-round-gate` is the seventh and holds
the measured 5/10 table.

## 4. Full-page cold-read accounting

```
$ python3 .ufo/evidence/round-16/measure.py --repo <worktree> --rev 05a2247…   exit 0
recorded_cases 7   depth_score 7
ledger_guardrail {header_legs:7, regression_calls:7, selftest_tuples:7, lists_agree:true, unique_recorded_gates:7}
shonen {boxes:4, marks:['~','~','~','~'], box3_marked:true, box3_ledger_link:true, box3_points:false}
coldread {sections_total:54, sections_covered:0, box3_full_page:false, ledger_present:false}
calibration_restraint_score 6
```

`ledger.json` does not exist at 05a2247 (`git ls-tree` shows only
`SKILL.snapshot.md`, `anchor-check.*`, `assemble.py`; no ledger in any ref yet).
`assemble.py` merges seat reports into `ledger.json` and exits 1 until every
section is covered, so `box3_full_page` is **false at this rev by construction** —
it can only flip after the wave-2/3 (this residual) reports are assembled. The
page's "earns the box-3 lane assertion ([~])" is therefore prospective; the mark
and the ledger link are present, the point credit is not yet measurable.

## 5. Findings (all non-blocking, documentation only)

1. **`probes.mjs` header contradicts its documented use.** Line 3-4 say
   "Runs the PRISTINE pinned blob only. Never runs a mutant." The page's rule and
   the committed `*-mutant-*.log` files run it on mutants via `GATE`; I did so
   (pristine 0 / mutant 1). A cold reader following the page could conclude the
   rule is impossible with this harness.
2. **Case note §4 C1059 row is stale.** The row names "wave-2 seat `C1059Probe`"
   and leaves the mutant column "—", although `c1059-probe.sh`,
   `c1059-pristine.log` and `c1059-mutant.log` are committed at the same rev and
   reproduce pristine 0 / mutant 1. (The row is in the file the page names as
   "detail of record"; it may already be in-flight in the L1's working tree, but at
   05a2247 it is stale.)
3. **Box-3 counting field is not yet true at the measured rev.** `coldread.box3_full_page=false`
   with `ledger_present=false` at 05a2247; see §4. Not a contradiction of any
   stated value, but a residual reader should not read "earns" as already
   instrument-verified.

No blocking gap and no wrong expectation was found: every headline number, every
prediction, every rule's observable consequence, and the ledger leg reproduce.

## 6. Residual risk / verification gaps

* `--regression` was run from a /tmp fleet with the four sibling repos symlinked
  to their live checkouts; it reads their object stores at the pinned revs only.
  It does not prove the fleet layout's paths match the real one beyond distance
  (FLEET_ROOT = `dirname³(SELF)`), which I satisfied.
* The GIT_DIR/TMPDIR hazard tests add the hostile variables explicitly under
  `env -i`; the suite string itself strips them, which is the point.
* Network reach of a hostile mutant was not exercised (only absence of socket
  calls by the pristine suite); the write-outside proof and the absence of any
  sandbox flag cover the same claim's mechanism.
* `measure.py --rev` was run at 05a2247 only; a later landing commit's ledger is
  outside this page's read and outside this seat's authority.

**Verdict:** the section reproduces end-to-end — reproduce block, all four rules,
the seven-leg ledger and the pre-registration all hold; only three non-blocking
documentation nits (stale `probes.mjs` header, stale case-note C1059 row, box-3
field still false pre-assembly) remain.

```json
{"seat":"RX7","skill_sha256":"e289acec4e90c994d303b2dd6c844d907dc1bf48330ecd2fd253ac7379f794b3","sections":[{"start":1749,"heading":"## Seventh recorded case and full-page cold-read — round 16","class":"instruction","verdict":"gap-minor","blocking_gaps":[],"wrong_expectations":[],"minor_gaps":["probes.mjs header says \"Runs the PRISTINE pinned blob only. Never runs a mutant.\" while the page's survivor-probe rule and the committed *-mutant-*.log files run it on mutants via GATE (measured pristine exit 0 / mutant exit 1) — stale header","case note §4 leaves the C1059 mutant column \"—\" and names no probe id, although c1059-probe.sh plus c1059-pristine.log and c1059-mutant.log are committed at 05a2247 and reproduce pristine 0 / mutant 1","coldread.box3_full_page is false at 05a2247 (ledger_present=false; ledger.json is assembled from seat reports by assemble.py and absent at this rev), so the \"earns the box-3 lane assertion\" sentence is prospective, not an instrument-measured state"],"commands_executed":["git -C tameshi-shokunin show 05a2247:SKILL.md | sha256sum (e289acec…f794b3)","git -C tameshi-shokunin worktree add --detach /tmp/tameshi-r16w2-RX7-wt 05a2247","git -C kumitate-shokunin show 364f1d5:scripts/round-gate.mjs | sha256sum (f890e277…a834d3e9, 1511 lines)","bash tools/mutate-and-run.sh --target $W/round-gate.mjs --defects .ufo/evidence/round-16/round-gate/round-gate.defects.spec --suite \"$(cat .ufo/evidence/round-16/round-gate/suite.txt)\" --label js-round-gate --workdir $W/work (exit 0; CONTROL GREEN; killed=5 survived=5 inconclusive=0 kill-rate=50%; MUTATE_RESTORE: OK)","git merge-base --is-ancestor e69b488 05a2247 (true; committer 2026-10-20T10:39:59-03:00)","git diff e69b488 05a2247 -- .ufo/evidence/round-16/round-gate/predictions.json (empty)","python3 compare results.tsv vs predictions.json (10/10, 0 mismatches, 5 KILLED 5 SURVIVED 0 INCONCLUSIVE)","grep -n '^FAIL' work/evidence/{A1,A3,B1,E3,C1060}.out (check ids incl. nested [51] tallies 50/58/58/59/59)","python3: embedded js-round-gate suite literal == suite.txt (byte_equal True, 216 B, env -i + GIT_CONFIG_NOSYSTEM + GIT_CEILING_DIRECTORIES)","pristine suite x3 with exported GIT_DIR=<scratch>/victim/.git (exit 1; victim 0->43 commits)","pristine suite with TMPDIR=<worktree>/.rx7-tmpdir-inside (exit 1; exactly 3 FAIL: [37],[51],[56]; nested 58/60)","mutant copy with fs.writeFileSync to /tmp/tameshi-r16w2-RX7-escape-marker via the suite (exit 0; marker written outside sandbox); grep bwrap|unshare|firejail|nsjail|seccomp tools/mutate-and-run.sh (none)","pristine suite x3 under the suite string (exits 0 0 0; stdout sha256 dde6c1bf/6bfd37e6/27004954 differ; stderr empty)","python3 tools/repeat-control.py --runs 3 --out … -- bash -c \"$(cat suite.txt)\" (REPEAT_CONTROL: controls_mismatch; REPEAT_EXIT: 1)","bash tools/mutate-and-run.sh --target $W/pristine.round-gate.mjs --defects /tmp/…/edge.spec (C26 SURVIVED, C25 KILLED, control green, restore OK)","GATE=pristine|mutant node .ufo/evidence/round-16/round-gate/survivor-probes/probes.mjs P1 (0/1), P1b (0/1), P6 (0/1), P9 (0/1)","bash .ufo/evidence/round-16/round-gate/survivor-probes/c1059-probe.sh (pristine exit 0 CLEAN, mutant exit 1 REPORT_THIN bytes=1040)","git show 364f1d5:scripts/round-gate.mjs | grep -n FINDING_KINDS (only :171 and :1488)","bash tools/mutate-and-run.sh --regression --workdir /tmp/… (exit 0; REGRESSION: PASS cases=7 passed=7; js-round-gate PASS match=10/10 flips=0)","strace -f -e trace=openat,connect,socket node pristine --selftest (exit 0; 60/60; opens under /home/vgpnk/Projects=0; socket/connect calls=0)","python3 .ufo/evidence/round-16/measure.py --repo <worktree> --rev 05a2247 (exit 0; sections_total 54, sections_covered 0, box3_full_page false, ledger_present false; ledger guardrail lists_agree true; restraint 6)","git -C tameshi-shokunin worktree remove --force /tmp/tameshi-r16w2-RX7-wt (exit 0)"],"opened":["SKILL.md:1749-1800 at 05a2247","corpus/knowledge/mutation-case-kumitate-round-gate.md at 05a2247","tools/mutate-and-run.sh at 05a2247","tools/repeat-control.py at 05a2247",".ufo/evidence/round-16/round-gate/{suite.txt,round-gate.defects.spec,predictions.json,results.tsv,evidence/*.out}","/tmp/tameshi-r16-rg.w5idxO/work/{results.tsv,defects.tsv,spec.copy,evidence/*.out}","work/spec.copy and .ufo/evidence/round-16/round-gate/round-gate.defects.spec (both e99b87eb…11c4)","work/evidence/C1060.out and A1.out FAIL lines (check ids)","/tmp/tameshi-r16w2-RX7-measure.json (measure.py output)","/tmp/tameshi-r16w2-RX7-regression.log (seven-leg regression)","/tmp/tameshi-r16w2-RX7-probes-TPMDFu/{P1,P1b,P6,P9}-{pristine,mutant}.out, edge.out, gitdir.out, tmpdir.out, rc/finding.txt, rc/run-*.{stdout,stderr,exit}, strace.out","kumitate-shokunin/scripts/round-gate.mjs at 364f1d5 (read-only via git show; working tree status 0 entries)"],"scratch":"/tmp/tameshi-r16w2-RX7-probes-TPMDFu"}]}
```

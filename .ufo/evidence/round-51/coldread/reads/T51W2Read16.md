# T51W2Read16 — cold-read re-key reader, `### Round-16 gate/probe registry`

Seat T51W2Read16, round 51 wave 2 (falsify). Candidate (CAND) `6d8c11e378aa90b12650808e1b79270742935f15`,
base `9962033fd7a75aa2f2847e979dd687a5d28505a1`. Read-only on the lane/fleet/sibling repos; every command
ran inside scratch clones under `/fast/scratch/hyaku/tameshi-r51/T51W2Read16/` (deleted before yield).
No tools installed. Contract and the C1/C2/C3 counter docstrings read before the item; the round-49-style
trace-bound re-key that consumes this row is `.ufo/evidence/round-51/coldread/refresh.py`.

## 1. The section at CAND

Heading re-resolved at CAND (not taken from the fixture list): `### Round-16 gate/probe registry` starts at
SKILL.md:1806; the next heading is `## Live-tree re-pin and entry-command monitor — round 17` at SKILL.md:1814;
the section is SKILL.md:1806-1813, 8 lines, section sha256
`2642efc5147715676537ab35e1489742f4183b39c8a6ff0e51e25213695be843` — **byte-identical to base** (the
SKILL.md diff base→CAND appends only the round-51 registry table at :2137+). Verbatim:

```
### Round-16 gate/probe registry

| Name | Kind | Command | Exits |
|---|---|---|---|
| `tools/mutate-and-run.sh` | gate | `bash tools/mutate-and-run.sh --selftest` · `--regression` | selftest 0 pass / 1 fail; regression 0 PASS · 1 FAIL · 2 SETUP · 64 usage |
| `.ufo/evidence/round-16/measure.py` | probe | `python3 .ufo/evidence/round-16/measure.py --rev REV` · `--selftest` | 0 measured · 2 rev/blob missing · 64 usage |
| `.ufo/evidence/round-16/coldread/assemble.py` | gate | `python3 .ufo/evidence/round-16/coldread/assemble.py --selftest` | 0 every bucket covered (a rejected report is printed, not counted) · 1 a bucket uncovered · 2 usage (argparse), an invalid override or a heading mismatch (round 17) |
| `.ufo/evidence/round-16/attribution/reattribute.py` | probe | `python3 .ufo/evidence/round-16/attribution/reattribute.py --selftest` | 0 corrected rule passes the oracle · 1 it fails |
```

Why it is a re-key target: the last round-21-ledger entry for this heading (entry 445, seat ColdB08,
read_rev `bb681566`) pins input `tools/mutate-and-run.sh` = `a7d3f2dd7d47511a…` (the base runner sha256);
the CAND runner sha256 is `977de47034cbe52b…` (C2's tenth leg + TMPDIR change) → `input-drift:tools/mutate-and-run.sh`.
The section's own bytes did not change; the runner it describes did.

Pointer extraction cross-check (not the fixture list): the round-49 extractor that refresh.py reuses
(`.ufo/evidence/round-49/c1/measure.py`, `extract`/`resolve`) resolves **exactly four** pointers from this
section text, all kind `path`, all direct non-record files, no line ranges, no internal pointer:

1. `tools/mutate-and-run.sh` — exists at CAND ✓
2. `.ufo/evidence/round-16/measure.py` — exists at CAND ✓ (bytes unchanged base→CAND)
3. `.ufo/evidence/round-16/coldread/assemble.py` — exists at CAND ✓ (unchanged)
4. `.ufo/evidence/round-16/attribution/reattribute.py` — exists at CAND ✓ (unchanged)

## 2. Pointers verified against candidate bytes

Method: `git clone --shared` of the lane checked out `--detach` at CAND into
`$S/fleet/tameshi-shokunin` (`$S=/fast/scratch/hyaku/tameshi-r51/T51W2Read16`), sibling `*-shokunin`
repos symlinked beside it (fleet-mirror layout), `git rev-parse --show-toplevel` asserted equal to the
clone; every invocation with `TMPDIR=$S/tmp`; exit codes captured per probe.

### P1 `tools/mutate-and-run.sh` (SKILL.md:1810) — **holds**

- Raw: `| `tools/mutate-and-run.sh` | gate | `bash tools/mutate-and-run.sh --selftest` · `--regression` | selftest 0 pass / 1 fail; regression 0 PASS · 1 FAIL · 2 SETUP · 64 usage |`
- File: `tools/mutate-and-run.sh`; ranges: none cited.
- Claim "selftest 0 pass / 1 fail": observed **exit 0** at CAND — `MUTATE_SELFTEST: 107/107 pass`,
  terminal `VERDICT: PASS` (`$S/out-selftest.txt`). The 1-fail branch is in the CAND bytes
  (`VERDICT: FAIL` → exit 1, tools/mutate-and-run.sh:2131; mktemp branch :1556) and is exercised by the
  selftest's own negative cases. Holds.
- Claim "regression 0 PASS": **observed end-to-end at CAND** — `bash tools/mutate-and-run.sh --regression
  --workdir $S/regwork` in the fleet-mirror clone exits **0** with `REGRESSION: PASS (cases=10 passed=10;
  ledger legs exact: killed-delta<=0 flips<=0)` (`$S/out-regression.txt`). This is the check prior readers
  (ColdA08, round 30) left as a minor gap ("not run end to end … exceeds the 6-minute bound"); it is closed
  here, and it is the first end-to-end regression over the **tenth** leg. All ten per-leg lines are PASS,
  including `REGRESSION_CASE bash-drift-pins: PASS (band: killed-delta<=0 flips<=0 inconclusive=0
  defects=10)`; wall time 239.7 s.
- Claim "1 FAIL": code path :1520-1524 (`REGRESSION: FAIL` → exit 1); exercised piecewise by the selftest's
  tally vectors at all ten leg positions (:2088-2098, e.g. `1:1:REGRESSION: FAIL (cases=10 passed=9 failed=1 setup=0)`),
  which passed as part of 107/107. Not triggered end-to-end (would require a leg to genuinely mismatch its
  committed table); stated as code+selftest-verified, not run-verified.
- Claim "2 SETUP": **observed** — bare `--shared` clone without sibling symlinks
  (`$S/bare-lane`), `--regression` → exit **2**, `REGRESSION: SETUP (cases=10 passed=0 cannot-verify=10)`
  (`$S/out-setup.txt`); code :1526-1529, :1535-1538; die_setup exit 2 :253-256.
- Claim "64 usage": **observed** — `--definitely-not-a-flag` → exit **64** with the usage block
  (`$S/out-usage.txt`); usage_exit :247-251; the selftest also asserts `--regression` refuses `--target` (exit 64).
- Strongest falsifier checked: the end-to-end ten-leg regression at CAND — the tenth leg
  `bash-drift-pins` (kagi `corpus/drift-pins.sh` @ `e64e81b8`, pin `c138d34c…`, TABLE_DRIFTPINS :643,
  leg call :1504-1510) must reproduce its committed 2/10 table exactly or the run exits 1 and this row's
  "regression 0 PASS" is false. It reproduced (PASS, cases=10 passed=10). Second falsifier: the selftest
  with the new leg wired (leg-count agreement calls=specs=nlegs=10, :2028-2047) — passed.
- Runner TMPDIR change (r51: three mktemp sites now `"${TMPDIR:-/tmp}/…"` at :491, :1432 and the selftest
  root): the row names no temp path, so nothing it claims is touched; observed the new behavior directly
  (the SETUP probe's auto workdir landed under my TMPDIR, `$S/tmp/tameshi-r4-2-regression.0i9bRp`).

### P2 `.ufo/evidence/round-16/measure.py` (SKILL.md:1811) — **holds**, two undeclared exits noted

- Raw: `| `.ufo/evidence/round-16/measure.py` | probe | `python3 .ufo/evidence/round-16/measure.py --rev REV` · `--selftest` | 0 measured · 2 rev/blob missing · 64 usage |`
- File exists at CAND, bytes unchanged base→CAND.
- `--selftest` → **exit 0**, `MEASURE_SELFTEST: 38/38 pass` (`$S/o1.txt`). Holds.
- `--rev CAND` → **exit 0** (measured; JSON report, `$S/o2.txt`). Holds.
- `--rev 0000000000000000000000000000000000000000` → **exit 2**, JSON `"error": "rev-missing"` (`$S/o3.txt`) — the "2 rev/blob missing" branch. Holds.
- `--bogus` → **exit 64**, argparse usage (`$S/o4.txt`). Holds.
- Strongest falsifier checked: all three declared exit branches plus the selftest, run at CAND bytes —
  every declared code reproduced on the declared trigger.
- Note (minor, pre-existing, not a round-51 falsification): the Exits cell omits the `--selftest` failure
  exit — measure.py:626 `return 0 if passed == len(checks) else 1`.
- Note (premise, undisclosed in this section): the command cell has no `--repo`; the tool defaults
  `DEFAULT_REPO = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'` (measure.py:53), so run from a clone it
  still measures the **live lane's** object store at the given rev (observed: the rev-missing error JSON
  names the live lane path). Read-only, and the round-17 section already discloses the sibling GIT_*-scrub
  gap for this tool ("run it only through `registry-check`"), but the default-repo half is not stated here.
- Side observation: pointed at base and at CAND this historical instrument reports
  `calibration_restraint_score` 6 at both revs — its own round-16 ledger's runner pins are older than base,
  i.e. the same input-drift mechanism that now drops this section, seen from the round-16 ledger.

### P3 `.ufo/evidence/round-16/coldread/assemble.py` (SKILL.md:1812) — **holds**

- Raw: `| `.ufo/evidence/round-16/coldread/assemble.py` | gate | `python3 .ufo/evidence/round-16/coldread/assemble.py --selftest` | 0 every bucket covered (a rejected report is printed, not counted) · 1 a bucket uncovered · 2 usage (argparse), an invalid override or a heading mismatch (round 17) |`
- File exists at CAND, bytes unchanged base→CAND.
- `--selftest` → **exit 0**, `SELFTEST: all checks passed` (`$S/o5.txt`). Holds.
- `--bogus` → **exit 2** argparse usage (`$S/o8.txt`) — "2 usage (argparse)" holds.
- Exit-2 branches in the CAND bytes: invalid override :1050, AsmError from `assemble()` :1071 (docstring
  :86 names heading mismatch). Holds.
- Extra: bare no-args run (default `SKILL.snapshot.md` + default globs) → **exit 0**, `missing sections: none`
  (`$S/o9.txt`) — the round-16 wave reports still validate against the snapshot; consistent with "0 every
  bucket covered (a rejected report is printed, not counted)" (SKIPPED lines printed, exit 0).
- Strongest falsifier checked: the selftest at CAND bytes plus both exit-2 triggers and the 0-path default run.
- Note (cosmetic): the "(round 17)" tag on "a heading mismatch" is imprecise provenance — the round-16
  bytes already exit 2 on a heading mismatch (AsmError, :86/:1071; the file was last committed in round 16,
  `3490708`). The behavior claim itself is accurate.

### P4 `.ufo/evidence/round-16/attribution/reattribute.py` (SKILL.md:1813) — **holds**, one undeclared exit noted

- Raw: `| `.ufo/evidence/round-16/attribution/reattribute.py` | probe | `python3 .ufo/evidence/round-16/attribution/reattribute.py --selftest` | 0 corrected rule passes the oracle · 1 it fails |`
- File exists at CAND, bytes unchanged base→CAND.
- `--selftest` → **exit 0**, `SELFTEST: PASS (new rule 8/8; old rule fails 5/8; old-rule fidelity 14/14)`
  (`$S/o6.txt`) — "0 corrected rule passes the oracle". Holds.
- The 1 branch exists (:251, :274, :307, :333). Holds as a map.
- Strongest falsifier checked: the selftest at CAND bytes (it re-derives the oracle over 14 recorded rows
  and 8 forged cases — passed).
- Note (minor, pre-existing): the tool is argparse-based (:337) and `--bogus` → **exit 2**
  (`$S/o7.txt`), which the two-code map omits.

## 3. Adversarial summary

- **No stale or moved pointer.** All four cited paths exist at CAND at the cited paths; none of the three
  evidence files changed base→CAND; the runner changed (C2) and its row was re-verified against the new
  bytes, including the first end-to-end ten-leg regression.
- **Nothing in the section is made false by the tenth leg, the runner TMPDIR change, or the four panel-tool
  updates** (tally-audit.py, tally-audit-v2.py, tally-audit-v3.py, mte-interop.py — none is cited by this
  section; their rows live in `### Gate/probe registry` :1499-1516 and the round-51 table, other seats' scope).
  The row states no leg count, no case count and no temp path, so all three changes pass through without
  touching a claim; the exit map itself is confirmed in the CAND bytes (:1520-1548) and by probe.
- **Unsupported/incomplete premises found (all pre-existing, none round-51-introduced):** P2 omits its
  selftest-1 exit and silently defaults `--repo` to the live lane path; P4 omits argparse exit 2; P3's
  "(round 17)" tag is imprecise provenance. Severity: minor — the maps are incomplete for the listed
  commands' failure/usage branches, not wrong about what they declare.
- **Scope note:** this section's 4-cell rows are outside C3's coverage surface (C3 checks only sections
  whose heading matches `^#{2,4} Gate/probe registry`, i.e. the round-51 8-cell table at :2138+); the
  runner is covered there by the "fleet mutation runner" row. This historical row remains accurate as far
  as its own claims go, and is the row this re-key re-binds.

## 4. Row for `reads.json`

```json
{
  "seat": "T51W2Read16",
  "candidate": "6d8c11e378aa90b12650808e1b79270742935f15",
  "heading": "### Round-16 gate/probe registry",
  "start": 1806,
  "end": 1813,
  "section_sha256": "2642efc5147715676537ab35e1489742f4183b39c8a6ff0e51e25213695be843",
  "section_bytes_equal_base": true,
  "pointers": [
    {
      "raw": "| `tools/mutate-and-run.sh` | gate | `bash tools/mutate-and-run.sh --selftest` · `--regression` | selftest 0 pass / 1 fail; regression 0 PASS · 1 FAIL · 2 SETUP · 64 usage |",
      "file": "tools/mutate-and-run.sh",
      "ranges": [],
      "verdict": "holds",
      "excerpt": "observed at CAND: --selftest exit 0 'MUTATE_SELFTEST: 107/107 pass'/'VERDICT: PASS'; --regression --workdir <scratch> in fleet-mirror clone exit 0 'REGRESSION: PASS (cases=10 passed=10; ledger legs exact: killed-delta<=0 flips<=0)'; sibling-less clone exit 2 'REGRESSION: SETUP (cases=10 passed=0 cannot-verify=10)'; unknown flag exit 64; FAIL->exit 1 at tools/mutate-and-run.sh:1520-1524, SETUP->2 :1526-1538, PASS->0 :1540-1548, usage_exit 64 :247-251, die_setup 2 :253-256",
      "falsifier": "end-to-end ten-leg regression at CAND (tenth leg bash-drift-pins must reproduce TABLE_DRIFTPINS 2/10 or exit 1 falsifies 'regression 0 PASS') — ran 239.7 s, all ten legs PASS incl. 'REGRESSION_CASE bash-drift-pins: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)', final 'REGRESSION: PASS (cases=10 passed=10)', exit 0; plus selftest 107/107, usage-64 and SETUP-2 probes"
    },
    {
      "raw": "| `.ufo/evidence/round-16/measure.py` | probe | `python3 .ufo/evidence/round-16/measure.py --rev REV` · `--selftest` | 0 measured · 2 rev/blob missing · 64 usage |",
      "file": ".ufo/evidence/round-16/measure.py",
      "ranges": [],
      "verdict": "holds",
      "excerpt": "observed at CAND bytes: --selftest exit 0 'MEASURE_SELFTEST: 38/38 pass'; --rev 6d8c11e3… exit 0 (measured); --rev 0000000000000000000000000000000000000000 exit 2 '{\"error\": \"rev-missing\"}'; --bogus exit 64 argparse usage",
      "falsifier": "all three declared exit branches plus the selftest executed at CAND bytes — each reproduced its declared code; undeclared-but-real: --selftest failure exit 1 (measure.py:626) and DEFAULT_REPO live-lane default (measure.py:53)"
    },
    {
      "raw": "| `.ufo/evidence/round-16/coldread/assemble.py` | gate | `python3 .ufo/evidence/round-16/coldread/assemble.py --selftest` | 0 every bucket covered (a rejected report is printed, not counted) · 1 a bucket uncovered · 2 usage (argparse), an invalid override or a heading mismatch (round 17) |",
      "file": ".ufo/evidence/round-16/coldread/assemble.py",
      "ranges": [],
      "verdict": "holds",
      "excerpt": "observed at CAND bytes: --selftest exit 0 'SELFTEST: all checks passed'; --bogus exit 2 argparse; exit-2 branches :1050 (invalid override) and :1071 (AsmError, docstring :86 names heading mismatch); bare no-args default run exit 0 'missing sections: none'",
      "falsifier": "selftest at CAND bytes plus both exit-2 triggers and the 0-path default run — all matched the declared map; '(round 17)' tag on the heading-mismatch exit is imprecise provenance (round-16 bytes already have it)"
    },
    {
      "raw": "| `.ufo/evidence/round-16/attribution/reattribute.py` | probe | `python3 .ufo/evidence/round-16/attribution/reattribute.py --selftest` | 0 corrected rule passes the oracle · 1 it fails |",
      "file": ".ufo/evidence/round-16/attribution/reattribute.py",
      "ranges": [],
      "verdict": "holds",
      "excerpt": "observed at CAND bytes: --selftest exit 0 'SELFTEST: PASS (new rule 8/8; old rule fails 5/8; old-rule fidelity 14/14)'; 1-branch at :251/:274/:307/:333; undeclared: argparse usage exit 2 on --bogus (argparse at :337)",
      "falsifier": "selftest at CAND bytes (re-derives the oracle over 14 recorded rows + 8 forgeries) — passed; usage probe shows the map omits argparse exit 2 (pre-existing incompleteness)"
    }
  ],
  "falsifier_checked": "strongest: end-to-end `bash tools/mutate-and-run.sh --regression --workdir <scratch>` at CAND in a --shared fleet-mirror clone — the tenth leg (bash-drift-pins, kagi corpus/drift-pins.sh @ e64e81b8) reproducing its committed 2/10 table is exactly what could falsify the runner row's 'regression 0 PASS'; observed REGRESSION: PASS (cases=10 passed=10), exit 0",
  "notes": [
    "section bytes identical base->CAND; it is a re-key target only via input-drift:tools/mutate-and-run.sh (last ledger entry 445/ColdB08 pins runner sha a7d3f2dd…, CAND runner sha is 977de470…)",
    "no stale/moved pointer; the three .ufo/evidence/round-16 files are byte-unchanged base->CAND",
    "nothing falsified by the tenth leg, the runner TMPDIR change, or the four panel-tool updates (none cited by this section)",
    "pre-existing map incompleteness: P2 omits selftest-1 and the live-lane DEFAULT_REPO premise; P4 omits argparse exit 2; P3's '(round 17)' tag imprecise"
  ]
}
```

## 5. Method, provenance, cleanup

- Reads: candidate SKILL.md via `git show CAND:SKILL.md` (2171 lines); section re-resolved by heading grep
  at CAND (1806) and next heading (1814); every cited file read from the CAND clone and probed by execution.
- Counter context read before the item: `.ufo/evidence/round-51/contract.json`; C1/C2/C3 counter docstrings
  (`.ufo/evidence/round-51/c{1,2,3}/measure.py`); C2 sweep receipt `.ufo/evidence/round-51/c2/sweep/sweep.txt`
  (CONTROL GREEN, 10 DEFECT lines, 2 KILLED, MUTATE_RESTORE OK, MUTATE: DONE — matches TABLE_DRIFTPINS);
  round-21 ledger entries for this heading (7 entries, last = 445 ColdB08); prior reader reports
  `.ufo/waves/round-30/wC/ColdA08.md` / `ColdB08.md` (their open minor gap on this section: regression not
  run end to end — closed by this seat).
- All commands ran in `$S/fleet/tameshi-shokunin` (clone at CAND, toplevel asserted) or `$S/bare-lane`
  (SETUP probe); outputs retained under `$S/` during the seat; **scratch deleted before yield**.
- No writes outside `$S` and this report; no git/jj mutations anywhere but scratch clones (no fixture
  commits were needed); no tools installed.

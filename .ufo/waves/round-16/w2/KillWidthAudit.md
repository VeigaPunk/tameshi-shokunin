# KillWidthAudit — §2 re-derivation from the committed sweep evidence

- seat: KillWidthAudit (round 16, wave 2 — falsify)
- lane commit: `c699c8c36d6e4eca4b796b81a8247904aa145ec8`
- target: `.ufo/evidence/round-16/round-gate/sweep/evidence/*.out` vs
  `corpus/knowledge/mutation-case-kumitate-round-gate.md` §2 (table, the `[51]`
  nested-duplicate paragraph, and the zero-skip claim)
- scratch: `/tmp/tameshi-r16w2-KillWidthAudit-UFt3wS`
- read-only against the lane; no lane edits, no commits. No tool installs or
  upgrades were needed or made.

**Verdict: holds** — §2's table, the 5/10 + 10/10 readings, and all five `[51]` nested tallies reproduce exactly from the committed `.out` files; the only mismatch is wording-level (the zero-skip claim is exact for all 11 sweep runs but not for the nested `[51]` re-run, which emits one `SKIP` and counts it as a pass; no verdict, exit, or kill-rate reading changes).

## 1. Commands and exits

Extraction (git object store; `git show <rev>:<path>`, exit 0 for every path):

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin ls-tree -r --name-only \
  c699c8c3 -- .ufo/evidence/round-16/round-gate/            # 33 files
# individually git show'd: results.tsv, defects.tsv, sweep.log, spec.copy,
# suite.txt, evidence/{A1,A2,A3,B1,B2,C1059,C1060,CKIND,E1,E3,control}.out
```

Target/identity:

```
git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show \
  364f1d5954158ef8844bca4a5fef57b05d2f2ca5:scripts/round-gate.mjs | sha256sum
# f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9  -
# wc -l -c on the extracted copy: 1511 lines, 80415 bytes (matches §0/§2 pin)
sha256sum spec.copy
# e99b87ebc16f045f43ffb31354e2fc2879d2be3a8504d4274239249b93ef11c4
# == committed .ufo/evidence/round-16/round-gate/round-gate.defects.spec
```

Per-mutant identity: I took the runner's own spec parser/apply helper (the
`py_helper` heredoc inside `tools/mutate-and-run.sh` @ c699c8c), re-applied each
`@old`/`@new` to the pinned blob, and hashed. All ten apply `old-count=1`, rc 0,
and all ten hashes equal `results.tsv` column 5:

```
A1    1186162e…9c1ca  MATCH   A3    05f2f411…458a  MATCH
B1    fc32499f…f8e5c  MATCH   E3    81cfe486…63a8  MATCH
C1060 432b4d50…6434   MATCH   C1059 35791a36…d459  MATCH
A2    d6aa922c…74f0   MATCH   B2    a8af2f4c…299a  MATCH
CKIND 1e6d4deb…a9a0   MATCH   E1    7d56ab89…cfd   MATCH
```

Live re-execution of the same suite command as `sweep/suite.txt` (private
HOME/TMPDIR per run, `env -i`, node `v24.21.0` — same as every committed
`.out` header), on the re-applied mutants and the pristine copy:

```
control rc=0  fails=[]                     60/60 pass
A1      rc=1  fails=[1,2,3,12,16,21,22,27,46,47,51]   49/60
A3      rc=1  fails=[51,52,53]                        57/60
B1      rc=1  fails=[32,45,51]                        57/60
E3      rc=1  fails=[51,54]                           58/60
C1060   rc=1  fails=[8,51]                            58/60
C1059   rc=0  fails=[]                                60/60
A2      rc=0  fails=[]                                60/60
B2      rc=0  fails=[]                                60/60
CKIND   rc=0  fails=[]                                60/60
E1      rc=0  fails=[]                                60/60
```

These FAIL sets, outer tallies, and `[51]` tails match the committed `.out`
files. I did not byte-diff the live logs; `mkdtemp` path suffixes differ by
construction (§0), which is the only expected difference but was not proven to
be the only one.

## 2. Per-mutant table re-derivation

Evidence FAIL numbers were parsed directly from the committed `.out` files.
Each file contains exactly 60 numbered check lines, numbers 1..60 each exactly
once, zero `SKIP` lines (`SEQ-OK` for all 11).

| id | exit | FAIL numbers in `.out` | excl. `[51]` | §2 says | match |
|---|---|---|---|---|---|
| A1 | 1 | 1,2,3,12,16,21,22,27,46,47,51 | 10: [1] [2] [3] [12] [16] [21] [22] [27] [46] [47] | 10: same list | yes |
| A3 | 1 | 51,52,53 | 2: [52] [53] | 2: [52] [53] | yes |
| B1 | 1 | 32,45,51 | 2: [32] [45] | 2: [32] fcA, [45] jFc | yes |
| E3 | 1 | 51,54 | 1: [54] | 1: [54] rt3 | yes |
| C1060 | 1 | 8,51 | 1: [8] | 1: [8] r8, 1059 B report `REPORT_THIN` | yes |
| C1059 | 0 | — | 0 | 0 | yes |
| A2 | 0 | — | 0 | 0 | yes |
| B2 | 0 | — | 0 | 0 | yes |
| CKIND | 0 | — | 0 | 0 | yes |
| E1 | 0 | — | 0 | 0 | yes |

Citations (paths relative to the lane root):

- A1: `sweep/evidence/A1.out:2,3,4,13,17,22,23,28,47,48` are the ten FAILs;
  `:52` is `FAIL [51/60]`; `:62` `ROUND_GATE_SELFTEST: 49/60 pass`.
- A3: `A3.out:53` `FAIL [52/60] --tracked: 3 filed reports…` (rt1),
  `:54` `FAIL [53/60] --tracked: oldest filed report untracked…` (rt2),
  `:52` `FAIL [51/60]`, `:62` `57/60`. rt8 is check `[59/60]`
  (`A3.out:60`, PASS with the mutated tail `warnings=0 errors=0`); source
  `round-gate.mjs:1481` is the prefix-only regex
  `/^ROUND_GATE: CLEAN \(mode=tracked checked=2 /`, so it stays green while
  rt1 `:1411` and rt2 `:1426` (full-line) fail. Exactly §2's wording.
- B1: `B1.out:33` `FAIL [32/60] … emits MAIN_REPO_NOT_GIT`,
  `:46` `FAIL [45/60] … kind=MAIN_REPO_NOT_GIT`, `:52` `[51]`, `:62` `57/60`.
- E3: `E3.out:55` `FAIL [54/60] … exit=0 … checked=0` under `< 1`, `:52` `[51]`.
- C1060: `C1060.out:9` `FAIL [8/60] … kinds=[REPORT_THIN,REPORT_ROUND_MISMATCH]`
  vs `control.out:9` `PASS … kinds=[REPORT_ROUND_MISMATCH]`. The r8 fixture is
  `fxMentions(10,'round-1')` (`round-gate.mjs:794,941`); node computed 1059 B
  (39-byte header + 60 × 17 bytes), so floor 1060 makes it thin and floor 1059
  does not. §2's edge-pair statement is byte-exact.
- Survivors: zero FAIL lines; `…out:62` `ROUND_GATE_SELFTEST: 60/60 pass`.

Kill/survival and predictions (`results.tsv`): 5 KILLED / 5 SURVIVED (50 %),
and parsing each `desc` "(predict …)" against the measured verdict gives 10/10
held. Durations: 29,365 ms across ten defects + 2,913 ms control = 32,278 ms,
consistent with the "32 s" line. `sweep.log` records `CONTROL: GREEN (exit=0)`,
`inconclusive=0`, `MUTATE_RESTORE: OK` with target sha `f890e277…` before,
after, and pristine.

## 3. `[51]` nested-duplicate statement

Verified against source at kumitate `364f1d5`:

- `round-gate.mjs:1396-1400` — check `[51]` spawns a nested `--selftest`
  (`:1386` sets `KUMITATE_ROUND_GATE_NESTED: '1'`) and passes only if the child
  exits 0 and its second-to-last line matches `ROUND_GATE_SELFTEST: N/M pass`.
- `:1381-1382` — in the nested run, `[51]` is replaced by
  `{ok:true, skipped:true, detail:'SKIP(nested) —…'}`.
- Committed evidence tallies, exactly §2's parenthetical:
  `A1.out:52` 50/60, `A3.out:52` 58/60, `B1.out:52` 58/60,
  `C1060.out:52` 59/60, `E3.out:52` 59/60. Every kill fails `[51]`.
- Duplicate-witness reading: in all five kills the nested tally equals 60 minus
  the number of non-`[51]` outer failures (A1 60−10=50; A3/B1 60−2=58;
  C1060/E3 60−1=59), and the outer total is exactly one lower than the nested
  tally (49/57/57/58/58) because outer `[51]` itself fails. So `[51]` adds one
  failing check but no independent failure signal in this sweep.
- Nuance (not a mismatch): `[51]` is structurally a meta-check, not literally
  redundant with any single check; it could fail alone only if the nested
  invocation itself misbehaved. That did not occur here, and §2's sentence is
  scoped to "every kill" in this sweep.

## 4. Zero-skip claim

The claim: *"No check was skipped in any run: `env -i` leaves
`KUMITATE_ROUND_GATE_NESTED` unset, so the control is 60/60 with no skips."*

- **Outer sweep runs — holds.** All 11 committed `.out` files have exactly 60
  numbered check lines (1..60, no duplicates/gaps) and zero `SKIP` lines;
  `control.out` is 60/60 PASS and `suite.txt`'s `env -i` list does not include
  `KUMITATE_ROUND_GATE_NESTED`. Live control reproduced rc 0, 60/60.
- **Nested re-run — one `SKIP` by design.** Direct observation on the pristine
  blob in `/tmp` with `KUMITATE_ROUND_GATE_NESTED=1` (otherwise the
  `suite.txt` env) exited 0 and printed:

  ```
  SKIP  [51/60]  hermeticity: nested --selftest under a polluted env — SKIP(nested) — parent run already spawned this suite once
  ROUND_GATE_SELFTEST: 60/60 pass
  VERDICT: PASS
  ```

  The tally is `results.filter(r => r.ok).length` (`round-gate.mjs:1498`) and a
  skipped result is recorded `ok:true` (`:1382`), so a skip counts as a pass;
  the reporter prints it as `SKIP` (`:1502`). Every nested re-run therefore
  executes 59 checks and skips `[51]` itself.
- Consequence for the quoted tallies: the nested "50/60", "58/60", "59/60"
  figures are 49/57/58 genuinely passing checks + one skip-as-pass. This is a
  wording overbreadth in "any run"; it does not affect any verdict: the skipped
  check is the recursion guard `[51]`, and any other failing check still makes
  the nested run exit 1, which fails the outer `[51]` (observed on all five
  kills).

## 5. Mismatches found

1. **Minor, wording only** — "No check was skipped in any run": true for the
   11 sweep invocations, false for the 11 nested re-runs they spawn (each has
   one `SKIP [51/60]`, counted as a pass by `:1498`/`:1382`). Suggested
   tightening: "in any sweep run" (the outer 60-check runs).

No other mismatch: every §2 row's measured verdict, exit, and failed-check list
is exact; the `[51]` tallies are exact; 10/10 predictions held; the evidence
paths named in §2 exist and are internally consistent.

## 6. Cross-checks (not mismatches)

- `spec.copy` sha256 = committed `round-gate.defects.spec` sha256 =
  `e99b87eb…11c4` (as §1 states).
- Sweep tool hash in `sweep.log` is `75ed934d…adc5` (§2), while the landing
  commit's `tools/mutate-and-run.sh` is `89722ddb…5594` (§5's regression runner).
  Two revisions, not a contradiction: §2 records the sweep-time tool, §5 the
  post-leg-cutover receipt. The regression receipt reads
  `REGRESSION_CASE js-round-gate: PASS`, `match=10/10`, `killed=5`, `rc=0`.
- `runner-selftest.txt` reads `MUTATE_SELFTEST: 81/81 pass` (read, not re-run).
- §2 edit line pins were checked against the source: `:163` E1, `:167`
  C1059/C1060, `:175` CKIND (`TREE_DIRTY` line), `:527` B2, `:535` E3,
  `:575-576` A3, `:617` A2, `:647` B1, `:677` A1 — all exact.

## 7. Limits

- I did not re-run `tools/mutate-and-run.sh --regression` (7 legs); the runner
  receipts were read, not reproduced. All other claims above were re-executed
  or re-derived from committed bytes.
- Live runs are one host, node v24.21.0, Linux 7.2.11 — same as the evidence
  headers. Verdicts are exit-status based, so `mkdtemp` path differences do not
  matter (and were not byte-diffed).
- I did not read or query any other seat's report, agent store, or credentials.

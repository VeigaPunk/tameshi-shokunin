# MutateAssemble — round 16, wave 2
**Verdict: partial — `--selftest` killed all six primary single-edit defects, but two additional boundary mutants survived (executed-ok minor-gap downgrade and equal-rank stricter-mode override).**
## Axes and scope
- **Depth:** attack six named behavior-bearing decisions, at their actual implementation lines, using isolated one-line changes.
- **Calibration:** require a passing pristine detector, distinguish killed from survived mutants, and prove exact-byte restoration plus a passing restored detector. This is a scoped detector finding, not a round judgment or a claim of exhaustive correctness.
- Assigned source: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-16/coldread/assemble.py` at commit `c699c8c36d6e4eca4b796b81a8247904aa145ec8`.
- Committed source size: `39982` bytes.
- Committed/pristine SHA-256 (`H0`): `8484a1b3204c506655a5e33a17fa65d5717432e322ba51ae47ee3ede6da65378`.
- Isolated scratch: `/tmp/tameshi-r16w2-MutateAssemble-DOBKzH`.
- Interpreter: `/usr/bin/python`, `3.14.8 (main, Oct  2 2026, 10:23:31) [GCC 16.2.1 20260810]`.
- No tool installs or upgrades; no other runtime, subagent dispatch, background job, commit, or git add.
- The lane implementation was not edited. The only lane write is this report; all probe files/logs are in the scratch directory.
## Commands and detector protocol
Fetched committed bytes (exit 0):
```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c699c8c36d6e4eca4b796b81a8247904aa145ec8:.ufo/evidence/round-16/coldread/assemble.py
```
The captured Git stdout was copied byte-for-byte to `assemble-pristine.py` and eight independent `assemble-M*.py` files under scratch. Every mutant had exactly one changed source line and unchanged line count; test assertions were untouched.
Each command below was run **three times on the same pathname**: pristine, single-edit mutant, restored pristine. The actual runner was `subprocess.run(argv, cwd='/tmp/tameshi-r16w2-MutateAssemble-DOBKzH', env=run_env, capture_output=True, text=True, timeout=20)`, with inherited environment plus `TMPDIR=/tmp/tameshi-r16w2-MutateAssemble-DOBKzH` and `PYTHONDONTWRITEBYTECODE=1`. Thus synthetic temporary fixtures stayed under scratch. Independent cases ran in a joined finite thread pool (maximum six simultaneous child processes); there were no detached/background jobs.
```sh
/usr/bin/python /tmp/tameshi-r16w2-MutateAssemble-DOBKzH/assemble-M1-strictest.py --selftest
/usr/bin/python /tmp/tameshi-r16w2-MutateAssemble-DOBKzH/assemble-M2-minor-downgrade.py --selftest
/usr/bin/python /tmp/tameshi-r16w2-MutateAssemble-DOBKzH/assemble-M3-class-wins.py --selftest
/usr/bin/python /tmp/tameshi-r16w2-MutateAssemble-DOBKzH/assemble-M4-never-relax.py --selftest
/usr/bin/python /tmp/tameshi-r16w2-MutateAssemble-DOBKzH/assemble-M5-skill-sha.py --selftest
/usr/bin/python /tmp/tameshi-r16w2-MutateAssemble-DOBKzH/assemble-M6-coverage-exit.py --selftest
/usr/bin/python /tmp/tameshi-r16w2-MutateAssemble-DOBKzH/assemble-M7-minor-executed-ok.py --selftest
/usr/bin/python /tmp/tameshi-r16w2-MutateAssemble-DOBKzH/assemble-M8-override-equality.py --selftest
```
All mutated runs were followed by restoration in a `finally` block, then the identical bounded detector on restored bytes. No run timed out. There were 24 detector invocations: 8 pristine, 8 mutated, 8 restored. Every pristine/restored invocation exited 0, emitted 36 `[ok]` checks and `SELFTEST: all checks passed`. The six killed mutants emitted explicit failed behavioral assertions, rather than syntax failures or crashes.
## Outcomes
| Mutant | Source mutation line (pinned revision) | Pristine exit | Mutated exit | Restored exit | Verdict |
|---|---|---:|---:|---:|---|
| M1-strictest | `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-16/coldread/assemble.py:388` | 0 | 1 | 0 | **killed** |
| M2-minor-downgrade | `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-16/coldread/assemble.py:225` | 0 | 1 | 0 | **killed** |
| M3-class-wins | `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-16/coldread/assemble.py:390` | 0 | 1 | 0 | **killed** |
| M4-never-relax | `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-16/coldread/assemble.py:568` | 0 | 1 | 0 | **killed** |
| M5-skill-sha | `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-16/coldread/assemble.py:348` | 0 | 1 | 0 | **killed** |
| M6-coverage-exit | `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-16/coldread/assemble.py:1066` | 0 | 1 | 0 | **killed** |
| M7-minor-executed-ok | `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-16/coldread/assemble.py:224` | 0 | 0 | 0 | **survived** |
| M8-override-equality | `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-16/coldread/assemble.py:568` | 0 | 0 | 0 | **survived** |

### Exact edits, expected detectors, and actual output

#### M1-strictest: Strictest-verdict merge

- Mutation: min -> max selects the most lenient observation.
- Implementation: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-16/coldread/assemble.py:388` at `c699c8c36d6e4eca4b796b81a8247904aa145ec8`.
- Detector anchor: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-16/coldread/assemble.py:805-806`.
- Expected detector: The strictest-wins assertion should fail.

```diff
-        best = min(obslist, key=lambda o: VERDICT_RANK[effective_verdict(o)])
+        best = max(obslist, key=lambda o: VERDICT_RANK[effective_verdict(o)])
```

Actual mutated stdout key lines:

```text
  [FAIL] strictest wins (gap-blocking>executed-ok) 
  [FAIL] relaxing override rejected (exit 2) got 0
SELFTEST: FAIL (2 checks)
```

Process exits: pristine `0` → mutated `1` → restored `0`. Verdict: **killed**.

#### M2-minor-downgrade: Minor-gap downgrade

- Mutation: Return the original verdict instead of gap-minor.
- Implementation: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-16/coldread/assemble.py:225` at `c699c8c36d6e4eca4b796b81a8247904aa145ec8`.
- Detector anchor: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-16/coldread/assemble.py:818-819`.
- Expected detector: The verified-record + minor_gaps downgrade assertion should fail.

```diff
-        return "gap-minor"
+        return o["verdict"]
```

Actual mutated stdout key lines:

```text
  [FAIL] minor_gaps downgrade verified-record -> gap-minor 
SELFTEST: FAIL (1 checks)
```

Process exits: pristine `0` → mutated `1` → restored `0`. Verdict: **killed**.

#### M3-class-wins: Instruction-wins class

- Mutation: Prefer record rather than instruction when both classes occur.
- Implementation: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-16/coldread/assemble.py:390` at `c699c8c36d6e4eca4b796b81a8247904aa145ec8`.
- Detector anchor: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-16/coldread/assemble.py:809-811`.
- Expected detector: The class-disagreement assertion should fail with record.

```diff
-        cls = "instruction" if "instruction" in classes else classes[0]
+        cls = "record" if "record" in classes else classes[0]
```

Actual mutated stdout key lines:

```text
  [FAIL] class disagreement -> instruction record
SELFTEST: FAIL (1 checks)
```

Process exits: pristine `0` → mutated `1` → restored `0`. Verdict: **killed**.

#### M4-never-relax: Override never-relax

- Mutation: Reject only equal-rank overrides, thereby allowing a relaxed verdict.
- Implementation: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-16/coldread/assemble.py:568` at `c699c8c36d6e4eca4b796b81a8247904aa145ec8`.
- Detector anchor: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-16/coldread/assemble.py:874-889`.
- Expected detector: The relaxing-override rejection assertion should fail: internal assembly returns 0 rather than 2.

```diff
-            if new_rank >= old_rank:
+            if new_rank == old_rank:
```

Actual mutated stdout key lines:

```text
  [FAIL] relaxing override rejected (exit 2) got 0
SELFTEST: FAIL (1 checks)
```

Process exits: pristine `0` → mutated `1` → restored `0`. Verdict: **killed**.

#### M5-skill-sha: skill_sha256 validation

- Mutation: Use the first skill as fallback for an unknown report skill SHA.
- Implementation: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-16/coldread/assemble.py:348` at `c699c8c36d6e4eca4b796b81a8247904aa145ec8`.
- Detector anchor: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-16/coldread/assemble.py:837-839`.
- Expected detector: The bad-sha rejection assertion should fail.

```diff
-        skill = skill_by_sha.get(rsha)
+        skill = skill_by_sha.get(rsha, skills[0])
```

Actual mutated stdout key lines:

```text
  [FAIL] bad-sha report rejected 
SELFTEST: FAIL (1 checks)
```

Process exits: pristine `0` → mutated `1` → restored `0`. Verdict: **killed**.

#### M6-coverage-exit: Coverage exit

- Mutation: Return success even when the ledger has missing sections.
- Implementation: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-16/coldread/assemble.py:1066` at `c699c8c36d6e4eca4b796b81a8247904aa145ec8`.
- Detector anchor: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-16/coldread/assemble.py:848-859`.
- Expected detector: The incomplete-coverage assertion should fail: internal assembly returns 0 rather than 1.

```diff
-    return 0 if not result["_meta"]["missing"] else 1
+    return 0 if not result["_meta"]["missing"] else 0
```

Actual mutated stdout key lines:

```text
  [FAIL] incomplete coverage exits 1 got 0
SELFTEST: FAIL (1 checks)
```

Process exits: pristine `0` → mutated `1` → restored `0`. Verdict: **killed**.

#### M7-minor-executed-ok: Minor-gap executed-ok branch

- Mutation: Narrow the downgrade predicate to verified-record only.
- Implementation: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-16/coldread/assemble.py:224` at `c699c8c36d6e4eca4b796b81a8247904aa145ec8`.
- Detector anchor: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-16/coldread/assemble.py:759; /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-16/coldread/assemble.py:818-819`.
- Expected detector: Contract-sensitive detection would reject executed-ok + nonempty minor_gaps remaining executed-ok. The existing selftest only names the verified-record downgrade case.

```diff
-    if o["verdict"] in RELAXING and o.get("minor_gaps"):
+    if o["verdict"] == "verified-record" and o.get("minor_gaps"):
```

Actual mutated stdout key lines:

```text
  [ok] minor_gaps downgrade verified-record -> gap-minor 
  [ok] relaxing override rejected (exit 2) got 2
  [ok] stricter override exit 0 got 0
SELFTEST: all checks passed
```

Process exits: pristine `0` → mutated `0` → restored `0`. Verdict: **survived**.

#### M8-override-equality: Strictly-stricter override boundary

- Mutation: Change >= to > so an equal-rank override is accepted.
- Implementation: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-16/coldread/assemble.py:568` at `c699c8c36d6e4eca4b796b81a8247904aa145ec8`.
- Detector anchor: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-16/coldread/assemble.py:874-913`.
- Expected detector: Contract-sensitive detection would require exit 2 for an equal-rank stricter-mode override. The existing selftest exercises relaxed and stricter overrides, not equality.

```diff
-            if new_rank >= old_rank:
+            if new_rank > old_rank:
```

Actual mutated stdout key lines:

```text
  [ok] minor_gaps downgrade verified-record -> gap-minor 
  [ok] relaxing override rejected (exit 2) got 2
  [ok] stricter override exit 0 got 0
SELFTEST: all checks passed
```

Process exits: pristine `0` → mutated `0` → restored `0`. Verdict: **survived**.

## Surviving-mutant coverage findings
1. **Executed-ok downgrade is not distinguished by this selftest.** The contract explicitly includes both executed-ok and verified-record (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-16/coldread/assemble.py:18-23`), while the supplied minor-gap fixture is verified-record (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-16/coldread/assemble.py:759`) and its assertion names only verified-record (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-16/coldread/assemble.py:818-819`). M7 removed executed-ok from the implementation predicate at line 224 and still passed all 36 checks. [INFERENCE from the one-line predicate change] An executed-ok observation with nonempty minor_gaps would now remain executed-ok. That specific input was not additionally executed; the prescribed detector alone was used.
2. **Equal-rank rejection is not distinguished by this selftest.** The contract requires a strictly stricter verdict (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-16/coldread/assemble.py:29-30`). M8 changed the guard at line 568 from `>=` to `>` and still passed all 36 checks. The existing override fixtures exercise relaxation and tightening (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-16/coldread/assemble.py:874-913`), not equality. [INFERENCE from the one-character operator change] An equal-rank stricter-mode override would now be accepted. This is a strictness-boundary finding, **not** evidence that the direct never-relax check is absent: M4 was killed. No additional equality-input probe was run.
Neither survivor changes the contract, and neither is a claim that the pristine implementation contains that defect. They demonstrate blind spots in `--selftest` for these deliberately introduced defects. No fix or integration was performed.
## Hashes and exact restoration
Every before/restored digest below is the full committed source digest, not a normalized-text hash. Exact equality of restored bytes to captured Git stdout was also checked for every copy. Detector runs themselves left the script hashes unchanged.
| Mutant | Before SHA-256 | Mutated SHA-256 | Restored SHA-256 | Restored exact bytes |
|---|---|---|---|---|
| M1-strictest | `8484a1b3204c506655a5e33a17fa65d5717432e322ba51ae47ee3ede6da65378` | `b54a04911d9b3ee98ebdfa5f5be77c8b07b97f5ddcb57dd62b0d3a0bd2f7c165` | `8484a1b3204c506655a5e33a17fa65d5717432e322ba51ae47ee3ede6da65378` | true |
| M2-minor-downgrade | `8484a1b3204c506655a5e33a17fa65d5717432e322ba51ae47ee3ede6da65378` | `cc93d0509958568681e18c577fbab3f94c76dbbe3d9be83c48b57b19c7de089b` | `8484a1b3204c506655a5e33a17fa65d5717432e322ba51ae47ee3ede6da65378` | true |
| M3-class-wins | `8484a1b3204c506655a5e33a17fa65d5717432e322ba51ae47ee3ede6da65378` | `a288653da118ace619ebe9eae6c826c9d4464b818cd47dbc6e684b05f57e96f3` | `8484a1b3204c506655a5e33a17fa65d5717432e322ba51ae47ee3ede6da65378` | true |
| M4-never-relax | `8484a1b3204c506655a5e33a17fa65d5717432e322ba51ae47ee3ede6da65378` | `937de73ede7499f34113b0c5726a3c6d605b0c7a84aef6f5c20c687b850787f8` | `8484a1b3204c506655a5e33a17fa65d5717432e322ba51ae47ee3ede6da65378` | true |
| M5-skill-sha | `8484a1b3204c506655a5e33a17fa65d5717432e322ba51ae47ee3ede6da65378` | `8a4d12646b668db7ca792a99ada07dca6521f3a214619c334614f02c7704c3ab` | `8484a1b3204c506655a5e33a17fa65d5717432e322ba51ae47ee3ede6da65378` | true |
| M6-coverage-exit | `8484a1b3204c506655a5e33a17fa65d5717432e322ba51ae47ee3ede6da65378` | `0acb7838c07e28231c4481ab89063d186138b3b3ece82d3d9d2d4e6ae1444f90` | `8484a1b3204c506655a5e33a17fa65d5717432e322ba51ae47ee3ede6da65378` | true |
| M7-minor-executed-ok | `8484a1b3204c506655a5e33a17fa65d5717432e322ba51ae47ee3ede6da65378` | `a0a45eacdeef747dd2c16c86da1d83e95fbbcca635a53894654b81262ef26abe` | `8484a1b3204c506655a5e33a17fa65d5717432e322ba51ae47ee3ede6da65378` | true |
| M8-override-equality | `8484a1b3204c506655a5e33a17fa65d5717432e322ba51ae47ee3ede6da65378` | `00c795d65fbc739daf3d606dd2305c639121a7e838290c1faaa0b3937f058bdf` | `8484a1b3204c506655a5e33a17fa65d5717432e322ba51ae47ee3ede6da65378` | true |

## Captured evidence
- Summary with exact original/mutated source lines, hashes, verdicts and interpreter/environment: `/tmp/tameshi-r16w2-MutateAssemble-DOBKzH/mutation-summary.json`.
- For each mutant ID in the tables, full stdout, stderr, argv, timeout, exit and script hashes are preserved in `/tmp/tameshi-r16w2-MutateAssemble-DOBKzH/<mutant-ID>-baseline.json`, `/tmp/tameshi-r16w2-MutateAssemble-DOBKzH/<mutant-ID>-mutated.json`, and `/tmp/tameshi-r16w2-MutateAssemble-DOBKzH/<mutant-ID>-restored.json`. These are retained scratch artifacts; the pinned source, commands, exact edits, key outputs and full hashes above are also included in this report for durable reproduction.
Baseline key output (representative M1 pristine; the same 36 assertion statuses passed for all eight pristine and all eight restored runs):

```text
  [ok] pre sections got 4
  [ok] post sections got 4
  [ok] preamble start=1 heading='' 
  [ok] alpha start=3 
  [ok] alpha spans fenced # 
  [ok] beta start=8 pre 
  [ok] beta.one start=10 pre 
  [ok] beta start=9 post 
  [ok] beta.one start=11 post 
  [ok] unchanged sections share sha across skills 
  [ok] alpha sha256 (pre) 
  [ok] trailing blank stripped 
  [ok] two-skill run exit 0 got 0
  [ok] ledger schema 
  [ok] skill_pins 
  [ok] 5 entries (sha-keyed merge) got 5
  [ok] strictest wins (gap-blocking>executed-ok) 
  [ok] class disagreement -> instruction instruction
  [ok] commands_executed_count sums 
  [ok] minor_gaps downgrade verified-record -> gap-minor 
  [ok] wrong-expectation + counts 
  [ok] post-sha entry from w2 report 
  [ok] multi-seat merge ['SeatA', 'SeatB']
  [ok] bad-sha report rejected 
  [ok] non-report glob hit skipped 
  [ok] coverage line 
  [ok] incomplete coverage exits 1 got 1
  [ok] missing list printed 
  [ok] heading mismatch exits 2 got 2
  [ok] relaxing override rejected (exit 2) got 2
  [ok] stricter override exit 0 got 0
  [ok] stricter override recorded 
  [ok] replace override exit 0 got 0
  [ok] replace override recorded 
  [ok] wrong-sha replace rejected (exit 2) got 2
  [ok] preamble first-line heading tolerated got 0
SELFTEST: all checks passed
```
The pristine stderr contains intentional negative-fixture diagnostics despite exit 0; it was not treated as a baseline failure. Representative actual stderr:

```text
ERROR: report /tmp/tameshi-r16w2-MutateAssemble-DOBKzH/assemble-selftest-5a38_m62/seatM.md: heading mismatch at start=3: report '## WRONG' != skill '## Alpha'
REJECTED /tmp/tameshi-r16w2-MutateAssemble-DOBKzH/assemble-selftest-5a38_m62/seatBad.md: seat SeatBad skill_sha256 0000000000000000000000000000000000000000000000000000000000000000 matches no supplied skill file
SKIPPED /tmp/tameshi-r16w2-MutateAssemble-DOBKzH/assemble-selftest-5a38_m62/seatG.md: no closing ```json block found
WARNING section sha=aea43bbf309b...: seats disagree on class ['instruction', 'record']; instruction wins
ERROR: override at section sha=aea43bbf309bd7a7... verdict 'verified-record' does not make the merged verdict 'gap-blocking' stricter
```
## Scoped conclusion

**6 killed / 2 survived / 0 inconclusive.** The six requested primary defenses hold against the selected coarse defects. Overall selftest sensitivity is **partial** because the two boundary defects survive. All eight mutated scratch scripts were restored to exact committed bytes and passed the same detector afterward. No other verification was run.

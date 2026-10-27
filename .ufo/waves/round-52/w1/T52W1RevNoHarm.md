# T52W1RevNoHarm — no-harm / deciding-run review

## Findings

- **No actionable defects found** in the assigned script review. The no-harm changes align with the contract's declared re-bases: commandD threshold 9→10, source-row floor 131→133, and tools-scope changed to exactly the two declared paths (`.ufo/evidence/round-52/no-harm.sh:4-7,17,27,33`; contract `:43-48`). The round-51 comparison also confirms all other monitor logic retained; the removed `PIPESTATUS` capture does not affect the emitted/self-tested `failed=0` predicate (`round-51/no-harm.sh:42-43`, round-52 `:40-41`).
- The deciding script's FROZEN paths expand to exactly the freeze manifest paths plus `.ufo/evidence/round-52/freeze.json`. That extra path is necessary because the freeze manifest itself contains a digest map but is not self-digested; script and other manifest entries are covered. Verified by comparing the expanded `FROZEN` list at `.ufo/evidence/round-52/deciding-run.sh:35` to `freeze.json:5-18`.
- Gate 0 still requires both control receipts to exist at REV and their latest committing changes to descend from FREEZE, before the single-invocation check or any counter execution (`deciding-run.sh:22-28`).
- C1 receives `$SCR/c1` as `--work`; the script creates it fresh before invocation (`deciding-run.sh:31,47`), and C1 explicitly rejects a nonexistent/nonempty work directory before creating its `tmp` subdirectory (`c1/measure.py:92-100`). No literal `/tmp` write path occurs in either assigned script; all declared scratch is beneath `$HYAKU_SCRATCH` (`no-harm.sh:13-15`; deciding `:16,31`).

## Required no-harm run (observed)

Command: `HYAKU_SCRATCH="$S" bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-52/no-harm.sh /home/vgpnk/Projects/shokunin/tameshi-shokunin ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4`, with `S=/fast/scratch/hyaku/tameshi-r52/T52W1RevNoHarm`.

Observed output:

```text
NOHARM commandD recorded_cases=10 depth_score=10 ok
NOHARM coldread-floor score=8 credited=64 ok
NOHARM r45-freshness population=74 fresh=71 score=9 ok
NOHARM r45-coverage rows=2 entries=2 C2_R45_PASS=true ok
NOHARM S160-count 1 ok
NOHARM registry-rows-not-below-133 133 ok
NOHARM r46-coverage rows=3 entries=3 C3_R46_PASS=true ok
NOHARM r47-coverage rows=3 entries=3 C3_R47_PASS=true ok
NOHARM tools-scope [] ok
NOHARM r49-generator-capability [PBT_STAGED_ID: cases=400 violations=0 counterexample=none classes=indent_1_3=248,indent_4_plus=31,id_4_plus_digits=31,collision=204,no_collision=62,held=49,unmapped=31,cascade=45,refusal=61,url_form_variant=30,map=104,map_inadmissible=31] ok
NOHARM r50-shrinker-selftest [SHRINK_SELFTEST: cases=14 failed=0] ok
```

All 11 monitors print `ok`; wall time 97.14s. The run is recorded as observed; a probe is never a verdict.

## Summary
- No-harm re-bases match the declared contract.
- Gate 0 and C1 fresh work-dir binding remain present.
- FROZEN matches the freeze manifest, with freeze.json additionally frozen.
- No `/tmp` writes found in either script.
- Required run observed: 11/11 monitors `ok` (97.14s wall).

# T58W2ExecNoHarm — committed no-harm replay

## Evidence

Created a shared scratch clone and checked it out detached at `8063d0a551fc5b3cb5a2d397da7353af53444534`. The clone's top-level path was asserted to equal the scratch clone path. Ran:

```sh
bash "$S/clone/.ufo/evidence/round-58/no-harm.sh" "$S/clone" 2a32aa8228d5f86a85c81a923a3148bf792a9538 8063d0a551fc5b3cb5a2d397da7353af53444534
```

All 18 monitor lines, in order:

```text
NOHARM commandD recorded_cases=10 depth_score=10 ok
NOHARM coldread-floor score=6 credited=47 RED
NOHARM r45-freshness population=74 fresh=71 score=9 ok
NOHARM r45-coverage rows=2 entries=2 C2_R45_PASS=true ok
NOHARM S160-count 1 ok
NOHARM registry-rows-not-below-140 148 ok
NOHARM r46-coverage rows=3 entries=3 C3_R46_PASS=true ok
NOHARM r47-coverage rows=3 entries=3 C3_R47_PASS=true ok
NOHARM tools-scope [M:tools/registry.json ] ok
NOHARM registry-rows-not-shrunk base=60 rev=60 ok
NOHARM r49-generator-capability [PBT_STAGED_ID: cases=400 violations=0 counterexample=none classes=indent_1_3=248,indent_4_plus=31,id_4_plus_digits=31,collision=204,no_collision=62,held=49,unmapped=31,cascade=45,refusal=61,url_form_variant=30,map=104,map_inadmissible=31] ok
NOHARM r50-shrinker-selftest [SHRINK_SELFTEST: cases=14 failed=0] ok
NOHARM r53-scratch-hygiene tmp_hits=0 ok
NOHARM ledger-not-shrunk base=627 rev=627 ok
NOHARM sources-not-shrunk base=145 rev=148 ok
NOHARM r56-gate-selftest [GATE_SELFTEST: 19/19 pass] ok
NOHARM registry-check-full base_held=48 rev=[REGISTRY_CHECK: held=49/53 superseded=7] ok
NOHARM old49-ledger base_rows=49 rev_rows=100 ok
NOHARM_EXIT=0
```

Cold-read RED is the expected pre-wave floor: score 6, credited 47; required thresholds are score >=8 and credited >=64. No other monitor line was RED. Script exit was 0.

Also ran the maintained source census directly on the committed clone:

```sh
python3 tools/registry-check.py --root "$S/clone" --rev 8063d0a551fc5b3cb5a2d397da7353af53444534
```

It exited 1 with final output `REGISTRY_CHECK: held=49/53 superseded=7`. Observed differing rows were `mutate-and-run-regression` (expect 0, got 2), `sources-census` (expect 0, got 1), `verify-round15` (expect 0, got 1), and `mte-interop-check` (expect 0, got 2). The census output additionally marked seven rows superseded (three evidence-disposition entries, trace-inputs-round17-selftest, and three command-binding rows); full captured lines are in adjacent JSON. `registry-check-full` in the no-harm monitor itself reported `held=49/53 superseded=7` and was marked `ok` because the threshold was base-held 48.

No lane files were edited. The scratch directory `/fast/scratch/hyaku/tameshi-r58/T58W2ExecNoHarm` was removed before handoff.

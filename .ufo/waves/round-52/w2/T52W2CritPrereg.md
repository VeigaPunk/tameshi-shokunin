# T52W2CritPrereg — pre-registration integrity

## Counterexample and evidence

- **Frozen bytes unchanged after amendment 1:** `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff --name-status 8827f3191393e14e7d3066368ce5558e92a12f47 bcba8924894216268afc4171f06eb8c28e912b46 -- .ufo/evidence/round-52/contract.json .ufo/evidence/round-52/c1/measure.py .ufo/evidence/round-52/c1/base-active.json .ufo/evidence/round-52/c2/measure.py .ufo/evidence/round-52/control/controls.py .ufo/evidence/round-52/no-harm.sh .ufo/evidence/round-52/deciding-run.sh .ufo/evidence/round-51/c3/measure.py .ufo/evidence/round-51/c3/tools-base.json tools/registry-check.py .ufo/evidence/round-21/coldread/measure.py .ufo/evidence/round-18/measure.py .ufo/evidence/round-48/quality/coldread-precheck.sh` returned no paths. The freeze manifest lists precisely these frozen inputs (`.ufo/evidence/round-52/freeze.json:5-18`).
- **No counter byte amended:** `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff --name-status acc27abe9b155e165d282d4bb7f821317ba1e7a1 8827f3191393e14e7d3066368ce5558e92a12f47 -- .ufo/evidence/round-52/c1/measure.py .ufo/evidence/round-52/c2/measure.py .ufo/evidence/round-52/no-harm.sh .ufo/evidence/round-52/deciding-run.sh` returned no paths. Commit stat shows the substantive harness path was `.ufo/evidence/round-52/control/controls.py`; contract and freeze manifest also changed to document amendment/erratum.
- **Amendment precedes wave-1 dispatch:** commit metadata from `git show --format=fuller --no-patch` gives freeze commit time 01:18:18-03:00 and amendment commit time 01:27:42-03:00. `.ufo/waves/round-52/w1.ready.dispatched:1` records dispatch at 02:16:48. The first wave-1 report claims an earlier reader scratch/mode only, but this audit has no filesystem-mtime evidence for the first w1 file; the contract itself records `before_any_seat: true` and the amendment time 03:00-03:00 (`contract.json:78-85`). Thus chronology is consistent with amendment before seats; direct mtime comparison was not independently established here.
- **C1 before erratum present:** `SCORECARD.md:2499` explicitly corrects the contract's prose total=2 to counter arithmetic 4 and says predicate/target unchanged. Contract `claims.C1.before` still states total=2 (`contract.json:24`), while amendment's erratum explains the discrepancy (`contract.json:85`). This documents rather than silently rewrites the frozen statement.

## Assessment

Amendment 1 changes the control harness's execution environment (fleet-mirror clone and a branch per control) to make the already-registered positive control runnable. It does not alter either counter, predicate, target, kill rule, control expectation, no-harm monitor, or deciding script; the contract records that boundary (`contract.json:83`). Based on the reviewed diff/stat and unchanged counter paths, I find no evidence that amendment 1 changed what a control measures or favored either claim. It repaired control execution fidelity; this is an operability-relevant harness correction, not a claim-measurement relaxation.

**Impacted axes:** operability (C1 control harness execution); calibration (C2/control suite integrity). This is an integrity audit only, not a claim verdict.

**Smallest safe correction:** none indicated. Preserve the explicit SCORECARD erratum; do not mutate frozen counter/predicate bytes. For stronger provenance, archive an explicit listing/hash receipt for the complete frozen-path comparison and first wave-1 file mtimes.

## Summary
- Frozen-path diff from amendment 1 to CAND0: empty.
- Counter/no-harm/deciding-script diff across amendment: empty.
- Amendment commit timestamp precedes w1 dispatch; first-file mtime not directly checked.
- SCORECARD records contract C1 before-value erratum (2 → 4), with predicate and target unchanged.
- No measurement-changing or claim-favoring amendment identified.

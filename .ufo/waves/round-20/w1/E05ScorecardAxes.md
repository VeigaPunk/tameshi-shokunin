# E05 — SCORECARD axes

## Findings (observed)

- The latest round-18/19 scorecard state has **depth 8** and **calibration 8**. Round 18 records depth 8 and calibration unchanged at 8 (`SCORECARD.md:647-677`). Round 19 says depth 8 is unchanged and calibration remains 8 (`:692-727`); its final no-harm reading is restraint 8 (`:745-763`).
- The depth rule is one point per recorded mutation case in the pinned replay ledger, capped at 10; it counts documented case depth, not newly executed cases (`SCORECARD.md:64-75`). I ran command D with `REV=6fd220bce3705498d1d1054e99e3cae73c203751` (the frozen round-20 contract revision):

  ```sh
  REV=6fd220bce3705498d1d1054e99e3cae73c203751
  git show "$REV:tools/mutate-and-run.sh" | python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))'
  ```

  Observed stdout: `recorded_cases=8 depth_score=8`.
- Calibration's lane-attainable cap is **8/10**; the remaining 2 require independent promotion review of all boxes (`SCORECARD.md:67`, reiterated at `:571`, `:696-697`, and `:725-727`). Round 19 explicitly does not claim independent promotion or current-page cold-read credit.
- The scorecard's numeric ownership is limited to **depth and calibration**; it declares no other owned numeric axis (`SCORECARD.md:64-67`; round-19 tie at `:692-697`). Other axes in the round-18/19 verdicts are unchanged/no-harm observations, not new numeric claims. **No axis is retired** (`:83-84`, `:727`, `:768-769`; the retired section at `:279-281` says none).

## Agreement / disagreement

**Agree** with the scorecard endpoint: the recorded-case counter at the frozen round-20 revision returns depth 8, and the latest round-19 state keeps calibration at 8. Its distinction between historical/no-harm evidence and independent promotion credit is preserved.

## Defects / qualifications

No unresolved defect found in the scoped score or ownership facts. Round 19 discloses an intermediate 49/60, restraint-6 no-harm result at `21e7932`, marked harmed (`SCORECARD.md:729-743`); it then records the repaired final restraint-8 result at `32838a5` (`:745-763`). The 18 round-18 guard survivors and other named residuals remain open, not retired (`:715-719`, `:768-769`).

## Unresolved gaps

None for the requested score, depth counter, calibration cap, ownership, and retirement findings.

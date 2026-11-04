round-72 counterfactual rehearsal — the guard's own measured loss for each
planned-edit arm, run BEFORE the round-72 plan was frozen. This is the
evidence that makes tools/rekey-cost.py's forecast model measured, not
asserted.

Method (no lane write): four scratch clones of the lane at the base
f20ba482c7441d4c75818e7cd8a3165fee7821a1 under
/fast/scratch/hyaku/tameshi-r72/L1/reh/, one appended marker line per planned
edit committed inside the clone only (author reh <reh@example.invalid>; the
clones are deleted with the scratch root and were never pushed), then the
committed portable guard run with --floor <base> --cand <clone tip>.

  git clone --shared <lane> cloneA|cloneB|cloneC|cloneD
  printf '\n<marker>\n' >> <planned path>; git -c user.name=reh \
    -c user.email=reh@example.invalid commit -am <arm>
  python3 -I tools/coldread-precheck-portable.py --repo . --floor <base> \
    --cand <clone tip> --work <scratch>

Arms (receipt file -> clone tip -> guard line):
  reh-sources-only.out      cloneD 2dce59971cd648f69fa48d9d507f2b08f0defa6a
    COLDREAD_PRECHECK floor=f20ba482c744 floor_credited=64 cand=2dce59971cd6 cand_credited=51 lost=13 RED
  reh-province-only.out     cloneA 204e0bd1816d8db14fdb876ed99514036c0fc207
    COLDREAD_PRECHECK floor=f20ba482c744 floor_credited=64 cand=204e0bd1816d cand_credited=58 lost=6 RED
  reh-province-sources.out  cloneA cec21df447fcac14c7a2239d7ac62e327c26cce0
    COLDREAD_PRECHECK floor=f20ba482c744 floor_credited=64 cand=cec21df447fc cand_credited=47 lost=17 RED
  reh-quality-only.out      cloneB 6ef682d7c3b3d010ed252286859760c4b5edccec
    COLDREAD_PRECHECK floor=f20ba482c744 floor_credited=64 cand=6ef682d7c3b3 cand_credited=58 lost=6 RED
  reh-scorecard-only.out    cloneC 7fda465456d1328efd7f058886a66c8dfd56ed7a
    COLDREAD_PRECHECK floor=f20ba482c744 floor_credited=64 cand=7fda465456d1 cand_credited=64 lost=0 ok

Base measure for the same instrument in the lane itself:
  COLDREAD_PORTABLE rev=f20ba482c744 credited=64/64 elapsed=2.6s probe_sampled=20 probe_mismatches=0
(receipt cost-base-measure-r72.txt)

The LOST lines' `drifted=` field lists every failing input across all
matching entries, including long-stale ones; the section set is the signal,
the reason string is not.

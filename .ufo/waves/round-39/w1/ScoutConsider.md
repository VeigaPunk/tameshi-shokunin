# ScoutConsider — settlement classifier predates round 39?

Proposal under review: `considerthese/2026-10-24.md` proposal 4, "Attempt and dispatch
health per round" (file lines 70–72). Question: did a settlement classifier already exist
before this round?

## Finding

**No.** The settlement classifier `tools/wave-parent-settle.py` first appears in this
round's freeze commit; nothing at the frozen base rev classifies wave settlement.

## Evidence (all read-only `git`, run in lane root)

1. Absent at frozen base rev 50aadd1bbd94e43cd3fcfb81459414394db2dc35:
   `git show 50aadd1b…:tools/wave-parent-settle.py` →
   `fatal: path 'tools/wave-parent-settle.py' exists on disk, but not in '50aadd1b…'`.

2. Added this round: `git log 50aadd1b…​..HEAD --oneline` → `233077f` only, and
   `git show 233077f --stat` lists `tools/wave-parent-settle.py | 83 ++` as a new file
   in "round-39: freeze C1 guard counter and C2 write-path census before data"
   (2026-10-24 20:49 -0300). The same commit froze the `settlement` block in
   `.ufo/evidence/round-39/contract.json:39-44` — the first settlement predicate.

3. Base rev tool inventory has no settlement tool: `git ls-tree 50aadd1b… tools/` lists
   24 entries; the nearest name, `tools/wave-accounting.py`, is a receipt/callback
   accounting gate ("Reconcile retained callback outcomes with exact wave membership"),
   not a SETTLED/UNSETTLED classifier.

4. Base-rev content search: `git grep -i 'unsettled\|parent_exit' 50aadd1b…` hits only
   shmutant verdict documentation (`unsettled` as a run-without-answer verdict in
   `.ufo/evidence/*/S006.md`) and mori-shokunin ledger copies — no classifier code.
   `git show 50aadd1b…:corpus/QUALITY.md | grep -i 'settle\|wave-parent\|terminal_unix'`
   → no matches.

5. Prior handling was narrative only: `.ufo/waves/round-38/w1/dispatch-outcome.md:44-48`
   describes the parent-exited-while-seats-ran failure in prose; no rule or tool.
   The QUALITY.md settle criterion (worktree `corpus/QUALITY.md:938-942`, citing
   proposal 4) is uncommitted (`git status`: `M corpus/QUALITY.md`) — being added this
   round, consistent with the ScribeEntry seat's criterion-78 check.

## Confidence

High — tree-level proof of absence at the base rev plus first-appearance in the round-39
freeze commit.

## Remaining unknowns

None for the assigned question. (Whether an out-of-tree orchestrator previously
classified settlement is out of scope; no in-lane artifact suggests it.)

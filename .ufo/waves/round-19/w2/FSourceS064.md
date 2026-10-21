# SourceS064 falsification — round 19 C1

Date: 2026-10-21. Read-only review of `w1/SourceS064.md` against frozen delivered revision `55e1d312c4e8ac67aefad80099bd27581ff805c9` and its cited primary surfaces.

## Strongest material assertion / verdict

**Agree:** R18-5 has a committed receipt at REV18 whose captured ruler output reports 60 covered sections; S064 is not needed as a C1 source. The report's interpreter/tool-digest disclosure gap remains an advisory limitation, not a falsifier of this measured criterion.

## Evidence

- Receipt `.ufo/evidence/round-19/round18-final-measure.json` (blob SHA-256 `a9536bfb…`) is present unchanged at `55e1d312` and in the worktree. It records `argv` with `python3`, `.ufo/evidence/round-18/measure.py`, absolute `--repo`, and `--rev 4b7c6823a462f5ea2eafcb262275300a545f3ed7`; `revision` matches; `exit` is 0; environment records `PYTHONDONTWRITEBYTECODE=1`. It has no interpreter/tool digest field.
- The receipt's stdout digest `55c530bb…` matches `.ufo/evidence/round-19/round18-final-measure.stdout`. Plain JSON inspection: `coldread.sections_covered` = 60, `ledger_committed` = true, `overrides_used` = false, and both `rev_input` and `revision` equal REV18. The ruler predicate is at `measure.py:129` on w1's observed `21e7932`; it is the same predicate at `:209` in frozen `55e1d312` (worktree: `:223`).
- Executed round-18 tool `.ufo/evidence/round-18/measure.py` hashes to `7ca87a7c…` at `4b7c6823`, baseline `7243e7f1`, `21e7932`, frozen `55e1d312`, and worktree. Thus the report's tool-identity mitigation is confirmed, including at the delivered revision.
- The contrasted R18-4 receipt contains `tool_sha256`, `runner_sha256`, and `cwd_kind`; the R18-5 receipt's missing interpreter identity is accurately disclosed.
- `.ufo/evidence/round-19/contract.json` lists S049 as the sole source. `corpus/SOURCES.md:73` S064 row is identical at `4b7c6823`, `7243e7f1`, `21e7932`, and `55e1d312`; its row-only SHA-256 is `1498665a…`. `corpus/knowledge/input-keyed-coldread-credit.md` still cites S064 at lines 1, 3, and 30 and is unchanged through `55e1d312`.
- Re-fetched the cited official source URL on 2026-10-21: HTTP 200, 5,790 bytes, SHA-256 `029067f4…`; the retained 2026-10-20 copy is 5,947 bytes, SHA-256 `76167a0d…`. This reproduces the reported digest drift. Source quote (§Benefits, markdown lines 37–38, fetched 2026-10-21): “The output of an action can be cached, and the action need not be run again unless inputs change.”

## Concrete falsifier

The R18-5 claim would fail if the committed captured stdout had `sections_covered != 60` or `rev_input != 4b7c6823a462f5ea2eafcb262275300a545f3ed7`; neither condition is present. No actual counterexample found.

## Staleness / residual unknowns

The w1 line-129 citation is accurate for its observed `21e7932`, but the ruler moved to line 209 in frozen `55e1d312`; this is a stale line reference, not changed behavior. The live page's upstream source commit remains unknown. Current worktree `measure.py` is modified relative to HEAD; this finding adjudicates frozen `55e1d312`, not that later worktree delta. No installs, tests, builds, lints, formatters, or git writes.
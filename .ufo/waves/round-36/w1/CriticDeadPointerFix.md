# Tameshi round 36 W1 — dead-pointer correction review

**Attacked:** round-35 `LOG.md` residual-sentinel pointer and the round-36 append-only correction.

**Evidence and verdict:** The lane honestly chose the permitted correction path: `ResidualSentinelClosure.md` is absent from the current tree and its all-history path query returned no commits. The correction also accurately lists five real files in `.ufo/waves/round-35/residual/`. Append-only discipline is kept: comparing the round-35 record commit `5df962b32fec2c341df9757245a51a14176eb905` to the round-36 content commit `e423c41ba253357ab8c8513f0376dad9d38ab248` shows only an addition at the end of `LOG.md`; the round-35 entry, including its original sentence, remains unchanged.

However, the correction is **not fully adequate**. The original sentence asserts the sentinel was “respawned by the closure.” The appended correction admits the sentinel left no report, then says the sentence's predicate findings are carried by `ResidualCriticPredicate.md`. That file exists, but it is a residual *critic* report about the counter predicate; it does not document the sentinel or a closure respawn. Thus the correction names paths that resolve, but does not name evidence that resolves the event asserted by the dead pointer. The phrase “predicate findings the sentence points at” also mischaracterizes what the original sentence says. This is an attribution/provenance gap on **calibration**.

**Smallest safe correction:** keep the round-35 text untouched and append a clarification withdrawing the unsupported respawn assertion (unless an actual artifact substantiating it can be identified). Cite `ResidualCriticPredicate.md` only for the predicate review, not as evidence of a sentinel respawn; state plainly that no sentinel report/closure artifact was found.

**VERDICT: DEFECT — honest disclosure and append-only handling, but the replacement evidence does not substantiate the sentence's respawn claim.**

## Commands run (revisions and observations)

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-parse 5df962b e423c41 d9c496b
# 5df962b32fec2c341df9757245a51a14176eb905
# e423c41ba253357ab8c8513f0376dad9d38ab248
# d9c496b19371b779ce0eec6dfee1b049b27a3a2d

cd /home/vgpnk/Projects/shokunin/tameshi-shokunin && git diff 5df962b e423c41 -- LOG.md | head -120
# One hunk, appended round-36 section only.

cd /home/vgpnk/Projects/shokunin/tameshi-shokunin && git log --all --oneline -- '*ResidualSentinel*'
# No output.

cd /home/vgpnk/Projects/shokunin/tameshi-shokunin && git ls-tree -r --name-only HEAD | grep -i residualsentinel
# No output; HEAD is d9c496b19371b779ce0eec6dfee1b049b27a3a2d.

cd /home/vgpnk/Projects/shokunin/tameshi-shokunin && ls -la .ufo/waves/round-35/residual/
# Exactly the five reports named by the correction.

cd /home/vgpnk/Projects/shokunin/tameshi-shokunin && grep -n 'sentinel\|respawn\|closure\|predicate' .ufo/waves/round-35/residual/ResidualCriticPredicate.md | head -30
# Predicate-review lines only; no sentinel/respawn/closure evidence.
```
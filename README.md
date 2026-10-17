# tameshi-shokunin

Verification-fixture craft. The reusable method of an honest check:
hermetic suites, mutation testing, fail-closed arms, verdict lines, and
before/after proof.

Rank: **shonen**. [`SHONEN.md`](SHONEN.md) is explicit that its `[~]`
marks are lane assertions. No independent promotion verifier is recorded
there.

Fleet: [shokunin](https://github.com/VeigaPunk/shokunin).

## The question

> If this check is lying, does a small, named mutation kill it — and can
> the original bytes be restored afterward?

A pattern is admitted as general only after evidence from two independent
lanes. Until then it is a case, filed with its kill rate and its limits.

## Boundary

**Owns:** the method, documented from gates that already exist, and this
lane's own runner. Primary surfaces named in `PROVINCE.md`: kumitate's
`scripts/` gates, kagi's census and checklist gates, kaidoku's audit-lane
pattern, and the game lanes' verifier loops.

**Hands off:** product domains. Every lane's gate remains that lane's.
Tameshi does not edit a sibling's gate. Recommendations travel in round
reports. Credential material is kagi. Endpoint health is kama.

Scratch for a mutation run is `/tmp/<lane>-r<round>-<n>-*/` from the first
write. The substrate tree is never a mutation target.

## Run

```sh
bash tools/mutate-and-run.sh --selftest
```

`tools/mutate-and-run.sh` injects a mutant, runs the target check, and
proves restore by byte identity. `--regression` replays the recorded legs
from git objects (`git show <rev>:<path>`), so a dirty worktree does not
move the kill rate. The header names the legs, including the later
embeddings of the kagi checklist and the kumitate claims gate. Read it
before adding a case. `SKILL.md` carries the recipe, the kill-rate bands,
and appendices that reproduce the measured JavaScript and bash cases.

Historical cold-read proof covers one JavaScript mutant. The skill states
that current full-sweep and bash sufficiency remains unverified.

## Map

| Path | What it is |
|---|---|
| [`SKILL.md`](SKILL.md) | the method as an executable recipe |
| [`PROVINCE.md`](PROVINCE.md) | what may be generalized, and what stays owned elsewhere |
| [`corpus/knowledge/`](corpus/knowledge/) | per-gate surveys and per-case mutation notes |
| [`reports/`](reports/) | including the round-1 calibration note the checklist cites |
| [`LOG.md`](LOG.md), [`SCORECARD.md`](SCORECARD.md) | rounds and axis verdicts |

Two lanes, then a general claim. One lane is a case study.

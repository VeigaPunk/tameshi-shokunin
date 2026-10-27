---
source: S275 — https://doi.org/10.1145/3540250.3558911 — §3.2 (commit-relevant mutants) and §3.3 (subsuming, high-order mutations), p. 4 — author camera-ready (ojda22.github.io/milos-ojdanic/assets/pdfs/change-aware-mutation-testing_camera-ready.pdf), fetched 2026-10-27 by L1 TameshiR53a2 (round-53 assimilation; staged as S161 by corpus-expansion-1, re-pointed by document)
source: S276 — https://arxiv.org/abs/2212.11762 — §Abstract — arXiv:2212.11762v1 (submitted 2022-12-22), fetched 2026-10-27 by L1 TameshiR53a2
verified-at: 2026-10-27 (both sources re-opened this round; snapshots under `.ufo/evidence/round-53/assimilation/`)
recheck: 365d
ground: F7 (incremental re-sweep granularity)

# Re-computing the mutant suite is a consistency bug; a pinned long-standing suite is the comparison device

## What the sources state

- S276: "Much previous work implicitly assumed it to be sufficient to
  re-compute mutant suites per release. Sadly, this makes mutation results
  inconsistent; mutant scores from each release cannot be directly
  compared"; the relevance of a mutant suite "will naturally degrade over
  time" — measured at "143,500 mutants in 4 non-trivial systems finding
  that, on overage, 52% degrade" — with a mutant-brittleness measure and a
  path to consistent-by-construction long-standing suites.
- S275: "around 30% of mutants are commit-relevant"; "by selecting only
  subsuming commit relevant mutants, we reduce the number of mutants
  requiring analysis by around 93% on average", with "69% of the mutants"
  located "outside the changed methods".

## What this means for the lane's re-sweep cadence

- **The lane's current cadence is the thing S276 criticises.** The lane's F7
  next move is "pin-level cadence only → per-leg reuse decisions
  classified". S276's point is that the choice is not between "recompute
  everything" and "recompute nothing" — it is between a *stable* suite
  whose relevance decays and a *fresh* suite whose numbers cannot be
  compared with the last run. Inference: the lane's pin-level cadence (S101)
  is the "stable suite" branch; its cost is that relevance decays silently,
  and its benefit is that scores stay comparable. The lane should record
  which branch it is on, because the two branches fail differently.
- **Commit relevance is a per-leg reuse decision with a measured size.**
  S275's ≈93% reduction is measured on Java class modules; the lane's legs
  are JavaScript and bash gates. Inference: the *shape* of the decision
  transfers (which changed lines, and which mutants depend on them); the
  *magnitude* does not, and is **not measured** for the lane.
- **What is still open.** The lane's F7 measurement — "per-leg reuse
  decisions classified" — is not made here. These two sources define the
  two candidate policies precisely enough to classify against; they do not
  perform the classification.

## Boundary of this entry

- Both sources are Java studies. The lane's own legs are JS and bash; the
  numbers are not transferred.
- S275's ACM copy is access-controlled (HTTP 403 on this round's re-open);
  the opened artefact is the author's camera-ready, and the row cites the
  canonical DOI.
- Adoption note (round 53): staged as `merge/tameshi` entry with rows
  S161/S162; adopted with the registry's own ids S275/S276 (append-only
  continuation; staged ids S161–S255 stay reserved by document). Both
  sources were re-opened by the lane L1 on 2026-10-27; the staged quotes
  re-located verbatim in the round's copies before the rows were written.

---

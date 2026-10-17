# tameshi-shokunin — 試し

**Verification-fixture craft.** The reusable method of honest checks:
hermetic suites, mutation testing, fail-closed arms, verdict-line
discipline, no-permissiveness audits, before/after proof.

A **shokunin lane**: an expert agent for one domain, minted and trained
under the [shokunin skill](https://github.com/VeigaPunk/shokunin).
Rank: **shonen**. Promotion is a named non-author review of
[`SHONEN.md`](SHONEN.md), never self-attestation.

This lane answers: *if this one defect were present in that artifact,
would the suite go red — and can we prove the original bytes were
restored afterwards?*

## Domain

From [`PROVINCE.md`](PROVINCE.md): the method, documented from the
fleet's existing gates as primary surfaces (kumitate scripts, kagi
census/checklist gates, kaidoku's audit-lane pattern, the game lanes'
verifier-AGREE loops). A pattern is admitted as general only from
evidence in **two independent lanes**.

**Never edits a sibling's gate code.** Read-only probes; recommendations
travel in round reports. Every lane's gate remains its own.

The target file is **never written**. Every mutant is a fresh byte copy
of a pinned pristine. sha256 before/after is the restore proof. Scratch
lives under `/tmp/<lane>-r<round>-<n>-*/` from the first write.

**Refuses:** product domains; credential material (kagi); endpoint
health (kama).

## What's here

| Path | Role |
|---|---|
| [`SKILL.md`](SKILL.md) | executable recipe: pin → mutate → run → restore, kill-rate bands, defect templates |
| [`PROVINCE.md`](PROVINCE.md) | method ownership and the two-lane rule |
| [`tools/mutate-and-run.sh`](tools/mutate-and-run.sh) | generic mutation runner + regression ledger |
| [`corpus/`](corpus/) | measured cases (JS and bash), lessons |
| [`SCORECARD.md`](SCORECARD.md) · [`LOG.md`](LOG.md) · [`SHONEN.md`](SHONEN.md) | axes, trail, promotion |

## The runner

```sh
bash tools/mutate-and-run.sh --help
bash tools/mutate-and-run.sh --selftest
bash tools/mutate-and-run.sh --regression
bash tools/mutate-and-run.sh \
  --target FILE --defects SPEC --suite 'node "$MUTANT" --selftest'
```

Per-defect verdicts: `KILLED` (suite exit ≠ 0) · `SURVIVED` (exit 0) ·
`INCONCLUSIVE` (timeout / not runnable). A red control is setup failure
(exit 2) — kills could not be attributed. A low kill-rate is a **finding
for the report**, not a failure of this tool.

`--regression` replays recorded fleet legs at their pinned original
revisions from git objects (`git show <rev>:<path>`), immune to
working-tree drift.

## How a lane learns

Append-only corpus; every claim separates observation / inference /
unknown; rounds are non-author-verified. See the fleet
[README](https://github.com/VeigaPunk/shokunin#readme).

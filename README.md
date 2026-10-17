# tameshi-shokunin — verification-fixture craft

**Honest checks.** Hermetic suites, mutation testing, fail-closed arms,
verdict-line discipline, no-permissiveness audits, before / after
proof. A pattern is admitted as general only after evidence in **two
independent lanes**.

This is a [shokunin](https://github.com/VeigaPunk/shokunin) lane. Rank:
shonen. Tameshi owns the *reusable method*. Every lane's gate remains
its own — this lane never edits a sibling's gate code. Recommendations
travel in round reports.

Primary surfaces, named in `PROVINCE.md`: kumitate's six gates with
selftest suites and mutation controls; kagi's `corpus/*check*.sh` and
census gates; kaidoku's audit-lane pattern (verify: lines, bit-exact
evidence ids); the game lanes' verifier-AGREE loops at the fleet root
`.ufo/waves/`.

## Province

**Owns:** the method, documented from those existing gates; this lane's
own corpus and `tools/mutate-and-run.sh`.

**Refuses:** product domains; editing a sibling's gate; claiming a
pattern general from one lane; credential material (→ kagi); endpoint
health (→ kama).

Two mutation cases are measured — round 2 JS, round 3 bash, both
8/10 killed — and the skill carries the method as an executable recipe
(numbered steps from pin to restore proof, defect templates, kill-rate
bands, restore discipline). Historical cold-read proof covers one JS
mutant only; current full-sweep / bash sufficiency remains unverified
(`SKILL.md`).

Full boundary: [`PROVINCE.md`](PROVINCE.md).

## Start here

1. [`SKILL.md`](SKILL.md) — the recipe, kill-rate bands, Appendix A / B reproduce specs.
2. [`PROVINCE.md`](PROVINCE.md) — two-lane rule and the never-edit-sibling fence.
3. [`tools/mutate-and-run.sh`](tools/mutate-and-run.sh) — inject → run → restore with byte-identity proof.

## The mutation runner

```
bash tools/mutate-and-run.sh --selftest
bash tools/mutate-and-run.sh --regression
```

`--selftest` is hermetic. `--regression` is the fleet leg ledger:
every recorded mutation case replayed at its pinned original revision,
materialized from that repo's git object store (`git show <rev>:<path>`),
immune to working-tree drift, with each leg's recorded kill-rate as
its expectation. Round 10 embedded the fifth and sixth legs (kagi
`corpus/checklist-run.sh`, kumitate `scripts/claims-check.mjs`),
completing the six measured gates in the ledger.

A green regression says those pinned legs still kill at the recorded
rate. It does not transfer gate ownership and it does not make a
one-lane pattern general.

## What's in the repo

```
tameshi-shokunin/
├── SKILL.md          method playbook + reproduce specs
├── PROVINCE.md       domain + two-lane admission rule
├── SHONEN.md         promotion checklist
├── MINT.md           why this lane was minted
├── LOG.md            append-only audit trail
├── SCORECARD.md      axis verdicts
├── AGENTS.md         operating rules
├── tools/            mutate-and-run.sh
├── plans/            round plans
├── reports/          verifier / adjudicator reports
└── corpus/           knowledge/, lessons/, QUALITY.md
```

Protocol: append-only corpus; substrates outside this repo are
read-only; rounds are non-author-verified. See the fleet
[README](https://github.com/VeigaPunk/shokunin#readme) for how a lane
learns.

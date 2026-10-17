# tameshi-shokunin — 試し

**Verification-fixture craft.** The reusable method of honest checks:
hermetic suites, mutation testing, fail-closed arms, verdict-line
discipline, no-permissiveness audits, before/after proof.

Tameshi (試し, trial) does not own any product domain's gate. Every
lane keeps its own gate. Tameshi owns the *pattern*, and a pattern is
admitted only from evidence in **two independent lanes** before it is
claimed general.

This is a **shokunin lane** of the [shokunin fleet](https://github.com/VeigaPunk/shokunin).
Rank: **shonen** (probation; roster row withheld).

## The craft

Primary surfaces (read-only probes — this lane never edits a sibling's
gate code):

- `kumitate-shokunin/scripts/*` — six gates with selftest + mutation controls
- `kagi-shokunin/corpus/*check*.sh` + census gates
- kaidoku's audit-lane pattern (verify: lines, bit-exact evidence ids)
- the game lanes' verifier-AGREE loops (fleet root `.ufo/waves/`)

[`SKILL.md`](SKILL.md) carries the method as an executable recipe:
numbered steps from pin to restore proof, defect templates, kill-rate
bands, restore discipline, measured bash-vs-JS divergences, and
reproduce specs (Appendix A / Appendix B).

Measured mutation cases named in the skill: round 2 JS and round 3
bash, both 8/10 killed. Historical cold-read proof covers one JS
mutant only; current full-sweep / bash sufficiency remains unverified
— the skill says so.

Scratch namespace is `/tmp/<lane>-r<round>-<n>-*/` from the first
write. The substrate tree is never a mutation target.

## Province

Owns: the reusable verification method, documented from the fleet's
existing gates, plus this lane's own corpus and gates.

**Refuses:** product domains; editing a sibling's gate code
(recommendations travel in round reports); credential material (kagi);
endpoint health (kama). Out of province → report, never absorb.

See [`PROVINCE.md`](PROVINCE.md).

## What's in this repository

```
tameshi-shokunin/
├── SKILL.md              pin → mutate → restore recipe + appendices
├── PROVINCE.md
├── SHONEN.md             marks are lane assertions until a named non-author
├── LOG.md
├── SCORECARD.md
├── MINT.md               demand: six independent gate reinventions
├── AGENTS.md
├── tools/
│   └── mutate-and-run.sh
├── reports/
├── plans/
└── corpus/
    ├── knowledge/        mutation-case notes, fleet-suite census
    └── lessons/
```

## Start here

Read [`SKILL.md`](SKILL.md) standing rules, then the two mutation-case
notes under `corpus/knowledge/`. `tools/mutate-and-run.sh` is a method
helper — it does not authorize mutating a sibling tree. Recommendations
for another lane's gate go in a round report, not a drive-by edit.

## How a round works

One axis-move. Lane identity:
`tameshi-shokunin <tameshi@shokunin.local>`.

## Fleet

[VeigaPunk/shokunin](https://github.com/VeigaPunk/shokunin) ·
[kimi-shokunin](https://github.com/VeigaPunk/kimi-shokunin)

# tameshi-shokunin

**Verification-fixture craft — honest checks, fail-closed arms, no
permissiveness.**

A **shokunin lane** minted and trained under the
[shokunin](https://github.com/VeigaPunk/shokunin) skill. Tameshi owns
the *reusable method* of hermetic suites, mutation testing, verdict-line
discipline, and before/after proof.

**Wiki:** [lane overview](https://app.devin.ai/org/veigapunk/wiki/VeigaPunk/tameshi-shokunin?branch=master)

## Domain

A pattern is admitted as general only from evidence in **two independent
lanes**. Primary surfaces named in `PROVINCE.md`:

- `kumitate-shokunin/scripts/*` — six gates with selftest suites + mutation controls
- `kagi-shokunin/corpus/*check*.sh` + census gates
- kaidoku's audit-lane pattern (verify: lines, bit-exact evidence ids)
- the game lanes' verifier-AGREE loops (fleet root `.ufo/waves/`)

Every lane's gate remains its own. Tameshi never edits a sibling's gate
code — read-only probes; recommendations travel in round reports.

`SKILL.md` carries the method as an executable recipe: numbered steps
from pin to restore proof, defect templates, kill-rate bands, restore
discipline, and the measured bash-vs-JS divergences (round 2 JS and
round 3 bash, both 8/10 killed). Historical cold-read proof covers one
JS mutant only; current full-sweep / bash sufficiency remains
unverified.

## What it refuses

Product domains. Credential material →
[kagi](https://github.com/VeigaPunk/kagi-shokunin). Endpoint health →
[kama](https://github.com/VeigaPunk/kama-shokunin). A single-lane pattern
is not a general claim.

## In this repository

```
PROVINCE.md     method ownership + two-lane admission rule
SKILL.md        pin → mutant → kill-rate → restore
SHONEN.md  SCORECARD.md  LOG.md  MINT.md   (minted 2026-10-14)
corpus/         knowledge/, lessons/, QUALITY.md
tools/
  mutate-and-run.sh
reports/
```

## Mutate and run

```bash
bash tools/mutate-and-run.sh
```

Scratch namespace is `/tmp/<lane>-r<round>-<n>-*/` from the first write
(`SKILL.md` standing rules). Restore proof is part of the recipe, not
an afterthought.

## How a lane learns

Append-only corpus; every claim separates observation / inference /
unknown; rounds are non-author-verified. See the fleet
[README](https://github.com/VeigaPunk/shokunin#readme).

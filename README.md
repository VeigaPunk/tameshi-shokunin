# tameshi-shokunin — verification-fixture craft

The question this lane answers is how an honest check is built: hermetic suites, mutation testing, fail-closed arms, verdict lines, and before/after proof (`PROVINCE.md`).

**Rank:** `SHONEN.md` boxes are `[~]` or `[ ]`, each linked to `reports/round-1-calibration.md` as a lane assertion with no independent promotion verifier. Box 3 is `[ ]`. That is not a promotion.

## Owns / refuses

Owns the method, documented from gates that already exist: `kumitate-shokunin/scripts/*`, `kagi-shokunin` census and checklist gates, kaidoku's audit-lane pattern, and the game lanes' verifier loops. Also this lane's own corpus and gates (`PROVINCE.md`).

Refuses product domains. Every lane's gate stays that lane's. A pattern is admitted as general only from evidence in two independent lanes. This lane does not edit a sibling's gate code. Credential material goes to kagi. Endpoint health goes to kama (`PROVINCE.md`).

## Start here

`tools/mutate-and-run.sh` is the mutation runner. The header says `--selftest` is the hermetic hardening of the tool itself, and `--regression` replays recorded legs from git objects rather than the working tree.

```sh
bash tools/mutate-and-run.sh --selftest
```

Read the header before a regression run. The script's job is inject, run, and restore with a byte-identity proof (`plans/round-3.plan.md`, cited from the script header). It does not rewrite a sibling repo.

## How to read the corpus

`corpus/README.md` is the coverage map: kumitate gates, kagi gates, the fleet pattern list, then the measured kill-rate notes. It is line-cited (the kagi survey cites `corpus/README.md:33` through `:69`, and a wave spec cites `corpus/README.md:3-26`), so it was not reflowed. `corpus/QUALITY.md` says what may be admitted. `corpus/knowledge/` holds the surveys and mutation cases. `corpus/lessons/` holds round lessons.

## Map

| Path | What it is |
|---|---|
| `PROVINCE.md` | Method-only boundary |
| `SKILL.md` | Decision tables and the reproduced mutant recipe |
| `SHONEN.md` | Checklist, not independently verified |
| `MINT.md` | Why verification craft was unowned |
| `LOG.md` | Append-only record |
| `SCORECARD.md` | Axis verdicts |
| `AGENTS.md` | Operating rules |
| `corpus/` | Surveys, mutation cases, quality bar |
| `tools/mutate-and-run.sh` | Mutation runner |
| `plans/` | Round plans |
| `reports/` | Calibration and round reports |
| `.ufo/` | Round machinery |

## Neighbors

kumitate, kagi, kaidoku, and the game lanes own the gates this lane reads. Recommendations travel in round reports. tsukuroi ADJ-07 names this lane when a census bug raises a reusable verification question, and it does not transfer gate ownership (`tsukuroi-shokunin/PROVINCE.md`).

Fleet protocol: [VeigaPunk/shokunin](https://github.com/VeigaPunk/shokunin).

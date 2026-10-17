# tameshi-shokunin

The craft of honest checks: hermetic suites, mutation testing,
fail-closed arms, verdict lines, and before/after proof.

Tameshi owns the reusable method. It does not own any product domain.
A pattern is admitted as general only after it shows up in two
independent lanes. Sibling gate code is read-only; a recommendation
travels in a round report. Credential material belongs to kagi.
Endpoint health belongs to kama.

## The job

`PROVINCE.md` names the primary surfaces the method was documented from:
`kumitate-shokunin/scripts/` (gates with selftest suites and mutation
controls), `kagi-shokunin`'s census and checklist gates,
kaidoku's audit-lane pattern, and the game lanes' verifier loops. This
repo holds the method, the corpus, and tameshi's own gate.

`SKILL.md` carries the method as a recipe: pin, mutate, run, restore,
with defect templates, kill-rate bands, and the measured bash-versus-JS
divergences. Two mutation cases are recorded there as measured (round 2
JS, round 3 bash). The skill is explicit that historical cold-read proof
covers one JS mutant, and that current full-sweep and bash sufficiency
stays unverified until re-run.

## The runner

`tools/mutate-and-run.sh` injects a mutant, runs the gate, and restores
the original with a byte-identity proof. Later rounds added `--regression`
(replay recorded legs at their pinned revisions via `git show`, so a
dirty worktree cannot change the expectation) and a `--selftest`.

```sh
bash tools/mutate-and-run.sh --selftest
```

Read the header before a regression run. The ledger of legs, and what a
kill rate does and does not prove, is in the script comment and in
`corpus/knowledge/`.

## Read this first

1. [`PROVINCE.md`](PROVINCE.md) — method versus product domains.
2. [`SKILL.md`](SKILL.md) — the recipe and the measured cases.
3. [`corpus/README.md`](corpus/README.md) — the coverage map.
4. [`tools/mutate-and-run.sh`](tools/mutate-and-run.sh) — the runner's contract, in the header.

## On disk

| Path | Role |
|---|---|
| `SKILL.md` | The method as an executable recipe. |
| `PROVINCE.md` | What "general" is allowed to mean. |
| `tools/mutate-and-run.sh` | Inject, run, restore. `--selftest` and `--regression`. |
| `corpus/` | Knowledge and lessons drawn from sibling gates. |
| `plans/`, `reports/` | Round plans and reports. |
| `MINT.md`, `SHONEN.md` | Mint record and promotion checklist. Rank is shonen. |
| `LOG.md`, `SCORECARD.md` | Audit trail and axis verdicts. |

## Fleet

Protocol and roster: [shokunin](https://github.com/VeigaPunk/shokunin).
This repository is a sibling lane. It is not an object in the fleet
root's `MANIFEST.json` `roster` array (13 ids, ending at `kaidoku`,
read 2026-10-17). Rank **shonen**.

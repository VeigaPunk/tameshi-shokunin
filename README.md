# tameshi-shokunin

The craft of honest checks.

Hermetic suites, mutation testing, fail-closed arms, verdict lines,
no-permissiveness audits, before/after proof. Tameshi documents that
method from gates other lanes already shipped, and ships its own runner
for the mutation cases it has measured. A pattern is called general only
after it shows up in two independent lanes. One lane's gate stays that
lane's gate. This repository does not edit it.

Rank: **shonen**. `SHONEN.md` is still here. The fleet `MANIFEST.json`
minted this lane on 2026-10-14 and withheld the roster row.

## Province

**Owns.** The method. Primary surfaces named by the province: kumitate's
`scripts/` gates, kagi's census and check scripts, kaidoku's audit-lane
pattern, and the game lanes' verifier loops. Also this lane's own corpus
and the mutation runner.

**Hands off.** Product domains. Sibling gate code — probes are read-only,
and recommendations travel in round reports. Credential material (kagi).
Endpoint health (kama).

## Start here

1. `PROVINCE.md` — the two-lane rule for calling a pattern general.
2. `SKILL.md` — decision tables, the mutation bar, the sweep recipe.
3. `corpus/README.md` — the survey notes. Read the errata blocks. They
   are how the lane keeps a wrong line citation.
4. `tools/mutate-and-run.sh` — inject, run, restore, with a byte-identity
   proof.
5. `SCORECARD.md` — the move log is the ten-round trajectory. Later rows
   are qualitative. Do not invent a scalar the row does not state.

## Run the runner

From the repository root:

```sh
bash tools/mutate-and-run.sh --selftest
bash tools/mutate-and-run.sh --regression
```

The header is the contract. `--selftest` builds its own fixture and
mini-suite. `--regression` replays the recorded mutation cases from each
target repo's git object store (`git show <rev>:<path>`), so a dirty
working tree of the sibling does not change the case. Exit conventions
and the `MUTATE_SELFTEST` / `REGRESSION` lines are in the script header.
A kill-rate is a report about those mutants. It is not a certificate
that the sibling gate is finished.

The surveys in `corpus/knowledge/` were taken read-only against sibling
checkouts. Re-running a sibling's `--selftest` belongs in that sibling's
README.

## The tree

| Path | What it is |
|---|---|
| `tools/mutate-and-run.sh` | The mutation runner and its regression ledger |
| `corpus/knowledge/` | Gate surveys, mutation cases, the fleet pattern note |
| `corpus/lessons/` | Per-round lessons |
| `reports/` | Audit verdicts |
| `plans/` | Round plans and completion evidence |
| `MINT.md` | The six-gate demand that justified the mint |

## Fleet

Minted under [shokunin](https://github.com/VeigaPunk/shokunin).
Recommendations travel outward. Fixes stay with the owner.

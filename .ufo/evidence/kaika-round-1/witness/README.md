# Witness-scoped kill experiment — preregistration receipt

## Source reopen (S006)
- Registered source: https://github.com/BWBama85/shmutant (S006).
- Raw README fetched: https://raw.githubusercontent.com/BWBama85/shmutant/7eefc73010ad6342b80e3ed43915503e02c90618/README.md
- Fetched-at: 2026-10-19T22:03:41Z; SHA-256 of fetched text: `dc0051c79ab792d0f4e1b19404ed661b4c94a8e54016595aeae853d5410178a3`.
- Quotes (each ≤25 words):
  - `## The three verdicts`, killed: “The suite went red on its witness. The test detects the defect.”
  - `## The three verdicts`, accidental: “The suite went red, but not on its witness. Caught by accident, not by the assertion that claims to cover it.”
  - `## The three verdicts`, unapplied: “The old literal matched nothing. The row injected no defect and tests nothing.”
  - `## The three verdicts`, baseline: “The selected tests were not green before any defect was injected.”
  - `## The three verdicts`: the other run-without-answer verdicts are aborted, timeout, unsettled, and lost.
- Recheck actually run: `curl -fsSL https://raw.githubusercontent.com/BWBama85/shmutant/7eefc73010ad6342b80e3ed43915503e02c90618/README.md | grep -c 'not on its witness'` → `1`.

## Pre-registration (written before the suite run)
Question: among the recorded 8 killed of the `js-kimi-census` 10-defect leg, how many are killed on a selftest assertion declared in advance, and how many are red only elsewhere?

Witness declarations are in `declared.tsv`, derived from the embedded `js-kimi-census` defect spec in `tools/mutate-and-run.sh` and the pinned gate/selftest source only. Explicit `NONE` means the selftest contains no assertion claiming that mutated behavior. The declaration file was hashed before the sweep:
- declared-at: `2026-10-19T22:05:45Z`
- declared.tsv SHA-256: `32241b02b722652af383af558054111a4c5d6117c6f5eb6bb094a6e8354fe9dd`
- Defect spec SHA-256: `51fa64663f15b8a558056792dd6d008c3c2a28fd4ce4b2463ee97f8c79a10f57`

Contamination log: before declaration, a recursive grep over the lane ran without excluding the prohibited note or Appendix A. Visible excerpts included historical D2/D10 survivor outcomes, a prior D5 killed outcome, and the prior D5 failure-case phrase (`MEMBER_MISSING … presence is gated`); runner comments also exposed recorded defect verdict IDs. I did not explicitly open `corpus/knowledge/mutation-case-kimi-census.md` by path, but the unscoped search included it and I cannot rule out that matching excerpts reached the output. These prior outcomes/labels could have biased declarations; I derived the witness mapping from the embedded spec and pinned gate/selftest source, but this is a contaminated, not fully blind, pre-registration.

## Materialization and classification, fixed before execution
The target was materialized from the sibling object store with `git -C /home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/kumitate-shokunin show 175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/kimi-census.mjs` into `/tmp/tameshi-r1-witness4-20261019/materialized/pristine.mjs`; its SHA-256 is `83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426` (the tool's `PIN_JS`). This writes no sibling tree. The runner's embedded spec for the leg was materialized at `/tmp/tameshi-r1-witness4-20261019/materialized/js-kimi-census.spec` (SHA above).

Planned command: `bash tools/mutate-and-run.sh --target /tmp/tameshi-r1-witness4-20261019/materialized/pristine.mjs --defects /tmp/tameshi-r1-witness4-20261019/materialized/js-kimi-census.spec --suite 'node "$MUTANT" --selftest' --workdir /tmp/tameshi-r1-witness4-20261019/sweep --label js-kimi-census`.

Per-defect classification used: KILLED requires red with the full 43-case denominator; killed-on-witness requires at least one failed label in `declared.tsv`; accidental means red/full-count with no declared witness failing; SURVIVED is green; INCONCLUSIVE covers timeout/unrunnable, absent full count, or a nonstandard verdict. A red pristine control is setup failure. Retained here: `js-kimi-census.results.tsv`, `js-kimi-census.defects.tsv`, `js-kimi-census.spec`, `control.out`, `D1.out`–`D10.out`, and `case-labels.tsv`.

Source guards reviewed before execution: `SKILL.md:148-149` red-control setup failure; `:171-178` count==1 uniqueness gate; `:189-194` killed requires red and the suite's full case count. The runner's mode/pin/spec are per `tools/mutate-and-run.sh:542-543, 589-629, 1112-1115`.

## Outcome

Executed `2026-10-19T22:07:13Z` with tool SHA-256 `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`; command was the preregistered invocation above. Control GREEN, `43/43 pass`; target and pristine both retained SHA-256 `83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426`; restore `MUTATE_RESTORE: OK`.

| Defect | Harness verdict | Selftest result | Declared witness failed? | Classification |
|---|---|---:|---|---|
| D1 | KILLED | 27/43 pass | Yes — green fixture; JSON family totals; 19th-lane boundary | killed-on-witness |
| D2 | SURVIVED | 43/43 pass | No | survived |
| D3 | KILLED | 27/43 pass | Yes — clean fixture / JSON assertions | killed-on-witness |
| D4 | KILLED | 40/43 pass | Yes — all three root-enumeration cases | killed-on-witness |
| D5 | KILLED | 42/43 pass | Yes — vanished chain case | killed-on-witness |
| D6 | KILLED | 41/43 pass | Yes — server.token below-floor assertion | killed-on-witness |
| D7 | KILLED | 41/43 pass | Yes — both secret mode-floor assertions | killed-on-witness |
| D8 | KILLED | 40/43 pass | Yes — all three fail-closed assertions | killed-on-witness |
| D9 | KILLED | 41/43 pass | Yes — FIFO and dangling-symlink assertions | killed-on-witness |
| D10 | SURVIVED | 43/43 pass | No | survived |

Measured: 8 killed, 2 survived, 0 inconclusive; all eight red runs retained the full 43-case denominator. The split is 8 killed-on-witness + 0 accidental = 8 measured kills. Recorded expectation is 8/10; deviation is 0 defects (exact match). Every failing selftest label, including extra failures outside the declared witness set, is in `case-labels.tsv` and the full per-defect logs.

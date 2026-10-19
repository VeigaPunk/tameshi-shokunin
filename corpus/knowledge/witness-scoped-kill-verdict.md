source: S006 — https://github.com/BWBama85/shmutant — README §§“The three verdicts” and “How a row is run” @ 7eefc73010ad6342b80e3ed43915503e02c90618; raw text fetched 2026-10-19T22:03:41Z, SHA-256 dc0051c79ab792d0f4e1b19404ed661b4c94a8e54016595aeae853d5410178a3
verified-at: 2026-10-19
recheck: 90d — `curl -fsSL https://raw.githubusercontent.com/BWBama85/shmutant/main/README.md | grep -c 'not on its witness'` → 1 (2026-10-19; main branch, so a README drift away from the pinned commit shows as 0)
ground: F2 — witness-scoped kills, bash mutation tooling (tameshi-art.md §4)

# Witness-scoped kill verdicts: the Kimi 8/10 split

## S006 verdict grammar (O)

The re-opened S006 raw README (URL, fetch time, digest, and quotes are retained in `.ufo/evidence/kaika-round-1/witness/README.md`) assigns a defect row a witness assertion. In `## The three verdicts`, it says:

- `killed`: “The suite went red on its witness. The test detects the defect.”
- `accidental`: “The suite went red, but not on its witness. Caught by accident, not by the assertion that claims to cover it.”
- `unapplied`: “The old literal matched nothing. The row injected no defect and tests nothing.”
- `baseline`: “The selected tests were not green before any defect was injected.”

`## How a row is run` refuses a row whose old literal occurs more than once and runs the selected witness before the mutation. S006 also names `aborted`, `timeout`, `unsettled`, and `lost` as runs that produced no answer. These are shmutant's own semantics, not independent evidence that tameshi implements its full selector model.

## Correspondence with tameshi (O / I)

Tameshi already supplies adjacent guards: the pre-run `count(old) == 1` uniqueness check is `SKILL.md:171-178`; a red pristine control stops as setup failure at `SKILL.md:148-149`; and its recipe calls a run killed only when it is red and the complete suite count remains present at `SKILL.md:189-194`. The recipe also requires verbatim failing-case labels (`SKILL.md:195-199`). These are evidence-backed parallels to S006's non-unique refusal, baseline, and witness verdicts; they are not identical mechanisms (tameshi runs the full suite rather than selecting one witness).

**I —** At tameshi's existing aggregate level, a red run with the full count can include either a shmutant-style `killed` or `accidental` outcome. The aggregate rate alone does not say which assertion failed. A witness declaration made before the run and compared to the captured failing labels supplies that missing distinction; no tool behavior or existing score is changed here.

## Pre-registered experiment and observation (O)

**Question:** of the recorded eight kills among the ten `js-kimi-census` defects, how many fail on a selftest assertion declared in advance, and how many are red only elsewhere? The classification rule and each D1–D10 witness (or explicit `NONE`) were fixed in `.ufo/evidence/kaika-round-1/witness/declared.tsv` before the sweep. Its SHA-256 is `32241b02b722652af383af558054111a4c5d6117c6f5eb6bb094a6e8354fe9dd`, recorded at `2026-10-19T22:05:45Z` before execution. The source spec and target came from `tools/mutate-and-run.sh:542-543, 589-629` and the kumitate object store via `git -C ... show 175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/kimi-census.mjs`; target SHA-256 `83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426` matches `PIN_JS`. No sibling tree was written.

The executed command was `bash tools/mutate-and-run.sh --target /tmp/tameshi-r1-witness4-20261019/materialized/pristine.mjs --defects /tmp/tameshi-r1-witness4-20261019/materialized/js-kimi-census.spec --suite 'node "$MUTANT" --selftest' --workdir /tmp/tameshi-r1-witness4-20261019/sweep --label js-kimi-census` at `2026-10-19T22:07:13Z` with tool SHA-256 `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`. Control was GREEN, 43/43; restore was `MUTATE_RESTORE: OK`. Each red mutant also reported a 43-case denominator. Classification is killed-on-witness iff a full-count red run includes at least one label in the pre-registered witness set; accidental iff red/full-count with none; green is survived; missing denominator or nonstandard/unrunnable run is inconclusive.

| Defect | Harness result | Selftest pass count | Witness result | Classification |
|---|---|---:|---|---|
| D1 | KILLED | 27/43 | Declared green-fixture, JSON-family, and 19th-lane assertions failed | killed-on-witness |
| D2 | SURVIVED | 43/43 | No failing case | survived |
| D3 | KILLED | 27/43 | Declared green-fixture and JSON assertions failed | killed-on-witness |
| D4 | KILLED | 40/43 | All three declared root-enumeration cases failed | killed-on-witness |
| D5 | KILLED | 42/43 | Declared vanished-chain case failed | killed-on-witness |
| D6 | KILLED | 41/43 | Declared server.token 0600-floor case failed | killed-on-witness |
| D7 | KILLED | 41/43 | Both declared secret mode-floor cases failed | killed-on-witness |
| D8 | KILLED | 40/43 | All three declared fail-closed cases failed | killed-on-witness |
| D9 | KILLED | 41/43 | Declared FIFO and dangling-symlink cases failed | killed-on-witness |
| D10 | SURVIVED | 43/43 | No failing case | survived |

**O —** The measured split is **8 killed-on-witness, 0 accidental, 2 survived, 0 inconclusive**. `8 + 0 = 8` measured kills. The recorded leg expectation is 8/10 (`tools/mutate-and-run.sh:84`); measured kill count and rate match exactly, deviation 0. The exact output table and every failing selftest label are retained in `.ufo/evidence/kaika-round-1/witness/js-kimi-census.results.tsv` and `case-labels.tsv`; raw full logs are `control.out` and `D1.out`–`D10.out`.

## Interpretation and proposal (I; proposal is not a rule change)

For this pinned JS leg only, the aggregate 8/10 equals the witness-attributed 8/10: no recorded kill was accidental under the declared cases. This does not establish witness-scoped rates for the other legs, and it does not make an aggregate rate self-explanatory without captured failing labels. The detailed labels show why the comparison matters: a mutant may fail several cases, but only a pre-registered match establishes that its intended assertion failed.

**Proposal for recipe step 7 (not a rule change):** add a per-defect `witness case(s)` field to the pre-run manifest; after the run, retain failing labels and report `killed-on-witness` separately from `accidental`, while preserving the current aggregate kill-rate for continuity. This is a proposal for the recipe owner, not a change to SKILL.md or the runner.

## Unknowns (U)

The preregistration was contaminated: before declarations, a recursive grep over the lane did not exclude the prohibited note or Appendix A. Visible output included prior D2/D10 survivor and D5 killed outcomes plus the D5 failure-case phrase; the unscoped search included `corpus/knowledge/mutation-case-kimi-census.md`, though I did not explicitly open it by path, so matching excerpts may also have reached output. The prior evidence could have biased choices; this is not a fully blind preregistration. Full disclosure is in the evidence README. Witness mappings were taken from the embedded spec and gate/selftest source. Only one pinned JS leg was measured; bash-surface-census and broader tameshi rates remain unmeasured here. This single sweep under one host environment is not a determinism claim.

## Errata (append-only)

None.

- E1 (2026-10-19, L1 integration, Reviewer seat finding): the heading
  "Pre-registered experiment" overstates. The declaration was hashed
  before the run, but an unscoped grep exposed historical outcomes first
  (Unknowns above), so read it as **declared-witness, partly
  contaminated** — not a blind pre-registration. The measured split is
  unchanged.

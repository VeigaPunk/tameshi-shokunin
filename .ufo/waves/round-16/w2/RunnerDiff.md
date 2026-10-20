# RunnerDiff — wave 2, round 16 (hyaku phase 2)

**Target:** `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff 28aeef4 c699c8c36d6e4eca4b796b81a8247904aa145ec8 -- tools/mutate-and-run.sh`
— are the six existing legs' specs/tables/pins byte-identical, are the v1 CLI flags / exit map / output lines unchanged for external consumers (mado's `MADO_VERIFY_HARNESS`, tsukuroi's pin), and is any prose now false?

**Verdict: partial — the six existing legs are byte-identical and the v1/mado/tsukuroi external contract holds; the failures are prose: two in-file claims still call the measured leg-7 spec/table "L1-substituted placeholders pending the measured sweep" (false at this commit), plus one provenance sentence points at the projection instead of the registration artifact.**

Revisions compared (extracted to `/tmp`; all runs from `/tmp` copies of committed bytes):

| | sha256 | lines |
|---|---|---|
| `28aeef4` (old) | `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5` | 1642 |
| `c699c8c` (new) | `89722ddb3082abd63136d025e0dfb08dcea9ffd91d58878beb230241b61f5594` | 1726 |

Those two hashes match `runner-sha256.txt` (`89722ddb…`) and the case note's recorded sweep tool (`75ed934d…`).

---

## Findings (severity order)

### F1 (minor, in-file) — two prose passages are now false: leg 7's spec/table are no longer "placeholders pending the measured sweep"

`tools/mutate-and-run.sh:101-102`:
> `# blobs at r10-2; leg 7's spec/table are L1-substituted placeholders pending`
> `# the measured sweep).`

`tools/mutate-and-run.sh:546-547`:
> `# r10-2; leg 7 (js-round-gate) is measured this round — its spec and table are`
> `# L1-substituted placeholders.`

Both are false at `c699c8c`, and the same file contradicts them ~800 lines later at `:900-904`:
> `# r16 leg 7: kumitate scripts/round-gate.mjs @ 364f1d5 (pin f890e277…d3e9),`
> `# swept this round with 10 single-edit mutants (5/10 killed, 10/10 predictions`
> `# held); the body below is the pre-registered spec, verbatim …`

Evidence the table is measured, not substituted:
- I re-ran the leg-7 sweep from the committed tool bytes with the five v1 flags on the pinned blob: `MUTATE: DONE (target=js-round-gate defects=10 killed=5 survived=5 inconclusive=0 kill-rate=50%)`, exit 0. `results.tsv` has exactly `TABLE_ROUNDGATE`'s ten row/verdict pairs (all ten `(predict …)` labels held).
- The commit's own evidence: `.ufo/evidence/round-16/round-gate/runner-regression.txt` records `REGRESSION_TABLE js-round-gate: match=10/10 recorded-killed=5 measured-killed=5 … PASS`, run against `REGRESSION_TOOL … sha256=89722ddb…` (the committed bytes).
- The committed `sweep/results.tsv` (`c699c8c`) cut to `id verdict` is byte-identical to my independent run's (`diff` empty).
- The spec source is not a placeholder either: the embedded `js-round-gate.spec` heredoc is byte-identical to `.ufo/evidence/round-16/round-gate/round-gate.defects.spec` (both sha256 `e99b87ebc16f045f43ffb31354e2fc2879d2be3a8504d4274239249b93ef11c4`), which was committed in `e69b488` before the sweep (see "provenance held" below).

Suggested fix: replace both clauses with a measured statement (e.g. "leg 7's spec is the e69b488 pre-registration, verbatim; its table is the measured 5/10"), and drop "pending the measured sweep".

### F2 (minor, in-file) — pre-registration is attributed to the projection note, not the registration artifact

`tools/mutate-and-run.sh:95-96`:
> `# mutation-case-kumitate-claims.md §1; leg 7's predictions are pre-registered`
> `# in corpus/knowledge/arm-class-matrix.md §13 (before any mutant run).`

`arm-class-matrix.md` §13 is explicitly a projection: "no mutant was cut, no gate mode was executed" (`corpus/knowledge/arm-class-matrix.md:300-303`), and its round-16 errata (`:527-537`) says "§13 was a projection … Round 16 cut ten mutants". The registration artifact is `.ufo/evidence/round-16/round-gate/predictions.json` + `round-gate.defects.spec` (committed `e69b488`); the predictions themselves are only "drawn from matrix §13 and the wave-1 seat fragments" (`corpus/knowledge/mutation-case-kumitate-round-gate.md:35-47`). The header also never cites the canonical case note `mutation-case-kumitate-round-gate.md` (added in this same commit; `grep` in the tool: NOT CITED).

This is a provenance-precision defect: a reader following `:95-96` lands on a note that says no mutant ran.

### F3 (residual, outside the target file) — live docs still assert a six-leg registry

At `c699c8c`, read via targeted `grep`/`sed` only (I did not open `SKILL.md` pages; cold-read bounds):

- `SKILL.md:1391` — instrument table row: `` `--regression` (six-leg registry, git-materialized replay)`` → now seven.
- `SKILL.md:1343` — "`REGRESSION_EXPECT` lists six" → now seven (the line itself prints seven; see below).
- `corpus/knowledge/repeated-control-precondition.md:70` — "the fleet's recorded kill-rate legs stay the six at `tools/mutate-and-run.sh:84-89`" → the range now lists seven.
- `SKILL.md:1272, 1302, 1339, 1426, 1456, 1483` are round-10-scoped headings/receipts ("six-leg regression" as a round-10 name); time-scoped, but they read as current in a skim.

Not a defect of the diff itself (the tool change is correct); these are lane-level doc updates the integrator may need to land. Flagged, not judged.

---

## What I attacked, and what held

### 1. The six existing legs' pins and tables are byte-identical — HOLDS

`diff` of the constants block (`PIN_JS` … `FLEET_ROOT`) old vs new:

```
12a13,14
> PIN_ROUNDGATE=f890e277…d3e9
> REV_ROUNDGATE=364f1d5…
18a21
> TABLE_ROUNDGATE='A1:KILLED,…,E1:SURVIVED'
```

3 added lines, **0 removed or modified** lines. `PIN_JS/PIN_BASH/PIN_TSUKUROI/PIN_MADO/PIN_CHECKLIST/PIN_CLAIMS`, their `REV_*`, and `TABLE_JS/BASH/TSUKUROI/MADO/CHECKLIST/CLAIMS` are untouched.

### 2. The six existing specs are byte-identical — HOLDS

I sourced each revision's `regression_specs()` in isolation and wrote both spec sets, then compared per file:

```
IDENTICAL js-kimi-census.spec      IDENTICAL bash-checklist-run.spec
IDENTICAL bash-surface-census.spec IDENTICAL js-claims-check.spec
IDENTICAL bash-tsukuroi-census.spec
IDENTICAL bash-mado-verify.spec
```

The only edits in `regression_specs()` are the function comment (`two`→`seven`), the appended leg-7 heredoc, and the `-s` test gaining `js-round-gate.spec` (`:967`). No existing heredoc byte moved.

### 3. v1 CLI flags, exit map, and mutation-mode output lines — HOLDS

- **Diff proof:** all 24 removed lines in the whole diff are headers, the `--regression` usage paragraph, ledger constants/comment, `regression_specs`, or `run_regression`/selftest. No line of `run_sweep`, `run_one`, the option parser, `MUTATE_*`/`CONTROL:`/`DEFECT` printers, or the `results.tsv` writer is removed or edited.
- **Executed (old vs new, same input):** a 2-defect fixture through `--target/--defects/--suite/--workdir/--label` produced **identical normalized output** (`diff` empty; durations/shas/paths masked) and the same `results.tsv` schema (`id\tverdict\texit\tduration-ms\tmutant-sha256\tdesc`); both exit 0.
- **Executed (old vs new, the real 10-defect spec):** both revisions give the same ten verdicts (5/10) and the same `MUTATE: DONE` line shape.
- **Exit matrix (old == new):** no args `64`, `--regression --target` `64`, unknown flag `64`, `@old` absent from target `2`.
- **mado's consumer contract:** invoking exactly as `mado-verify.sh:1759-1761` does (`bash "$REGRESSION_RUNNER" --target … --defects … --suite … --workdir … --label … > sweep.log 2>&1`) yields the lines mado greps — `^MUTATE: ` (`:1763`), `^CONTROL: GREEN ` (`:1816`), `^MUTATE_RESTORE: OK ` (`:1817`) — and `$workdir/results.tsv` at the path mado reads (`:1773`). No change.
- **`--help`:** `diff` old vs new is **only** the `--regression` paragraph adding `js-round-gate` to the leg list (`:203`); the v1 options block is unchanged.
- **`REGRESSION_EXPECT`:** one pair appended (`js-round-gate=5/10`; `:1179`). This is a `--regression`-only line; fleet grep found no external consumer — mado invokes mutation mode only, and the only other code copies of the six-rate line are frozen snapshots (`mado-shokunin/.ufo/waves/round-13|14/frozen/harness.sh:1103`), not consumers.

**tsukuroi's pin:** `tsukuroi-shokunin/SKILL.md:568-570` pins the **r4-2** tool (`md5 26a27d…ddf6`, 1001 lines, sha `597e1419…331b`) and cites `:16-21,60` for the target-never-written contract. It is a versioned historical record, not a live check: no tsukuroi tool reads or compares the harness (only `tsukuroi-census.sh:2174` mentions it in a comment). Because mutation-mode behavior is byte-identical, the pin stays valid as an r4-2 record; its line anchors drifted in the current file (as expected for a pinned revision).

### 4. New leg 7 (js-round-gate) — provenance and behavior held

- `REV_ROUNDGATE` resolves in `kumitate-shokunin`; blob is 1511 lines, sha256 `f890e277…d3e9` = `PIN_ROUNDGATE` (`git show 364f1d5:scripts/round-gate.mjs`).
- Embedded spec == evidence spec byte-for-byte (sha `e99b87eb…11c4`); embedded suite literal == `predictions.json`'s `suite` field (Python compare: `True`).
- Pre-registration order: `e69b488` committed `2026-10-20 10:39:59 -03:00` (=13:39:59Z); committed `sweep/sweep.log` `MUTATE_DATE: 2026-10-20T13:40:15Z`; sweep's own `MUTATE_TOOL` sha is the r10-2 `75ed934d…` (v1 mode unchanged) and `sweep/spec.copy` sha is `e99b87eb…`.
- All ten `@old` strings applied with count==1 (the sweep would exit 2 otherwise) and all ten `(predict …)` labels match the measured verdicts (10/10 held); spec line anchors sampled (`:163,167,175,527,535,575-576,617,647,677`) all hit the intended code.

### 5. End-to-end, from committed bytes in `/tmp`

| Run | Exit | Key output |
|---|---|---|
| `mutate-and-run.sh --selftest` | 0 | `MUTATE_SELFTEST: 81/81 pass` / `VERDICT: PASS`; includes `PASS embedded leg specs: seven files written` and seven `spec and recorded table agree` lines |
| `mutate-and-run.sh --regression --workdir <tmp>` from a fake fleet root (symlinks to siblings) | 0 | `REGRESSION: PASS (cases=7 passed=7; ledger legs exact…)`; all tables `match=10/10` (checklist `15/15`), `flips=0`, `inconclusive=0`; `js-round-gate match=10/10 recorded-killed=5 measured-killed=5` |
| Leg-7 sweep via v1 flags (new bytes) | 0 | 5 killed / 5 survived / 0 inconclusive; control GREEN; `MUTATE_RESTORE: OK`; target sha unchanged |
| Same sweep via old bytes | 0 | identical ten verdicts (`diff` empty) |

The six existing legs replay their recorded tables exactly with the new tool, confirming the ledger extension did not perturb them.

---

## Residual risk and verification gaps

- **mado's own `--regression` was not re-run** (that executes mado's gate sweep). The harness mutation path it consumes is unchanged code, and I invoked the harness with mado's exact five-flag form and parsed the lines mado parses; mado's own `SPEC_SHA`/`PIN_MADO` are untouched by this diff.
- **Node dependency unchanged in kind:** the new suite needs `node` on `PATH`; a missing node yields exit 127 → INCONCLUSIVE → regression FAIL, the same failure class the two existing JS legs already have (not a new SETUP-refusal class).
- **Runtime:** the seven-leg `--regression` took ~127 s wall on this host (leg 7 ~40 s); per-defect suites ~3–4 s, far below the harness's per-suite timeout in my run.
- **Static-basis claims inside the embedded spec** (e.g. "all 10 call sites assert `v!==null`") were not independently re-derived; I verified outcomes, the applied edits (count==1), and sampled line anchors.
- **No LSP device exists for shell files in this seat**, so caller/definition checks are textual+execution evidence (diff of both revisions, behavior of both revisions), not semantic LSP proof. No `lsp` tool was available to query.
- **F3 docs** (`SKILL.md`, `repeated-control-precondition.md`) are outside this target's write scope and were read only by targeted lines; another seat/integrator owns them.

## Tooling record

No installs or upgrades were made. Scratch: `/tmp/tameshi-r16w2-RunnerDiff-*` (selftest, sweep, v1 fixture, help, exits, old sweep) and `/tmp/tameshi-r16w2-RunnerDiff-fleet-YuIdWZ` (fake fleet root for `--regression`). Only lane write is this report.

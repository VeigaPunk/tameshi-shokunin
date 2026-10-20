# Round 14 w1 — EmpiricalBacklink (C1 effective-expectation / knowledge backlink)

Lane: tameshi-shokunin. Seat: `TameshiR14.EmpiricalBacklink`. Mode: read-only research; the only file written is this report. `corpus/knowledge/incremental-pin-disposition.md` was NOT edited. Contract is exercised against code where code exists (runner constants and receipts read; `tools/pin-disposition.py` and `tools/witness-metadata.py` not read by this seat, their digests are pinned in `expected.json` and the receipts).

Tool installs/updates by this seat: none.

## Scope read

- `corpus/knowledge/incremental-pin-disposition.md` §§1–7 (§6 at lines 251–282, §7 at 284–312, end of file at 312).
- `.ufo/evidence/round-13/`: `expected.json`, `verification.json` (checks 1–16 and sibling indexes), `verification-verdict.json`, `producer-oracle-repair.json`, `pin-dispositions.json` (`?q=` per-leg projection), `pin-manifest.json`, `witness-metadata.json`.
- `corpus/lessons/round-13.md`, `corpus/lessons/round-13-verifier-spotcheck.md` (Routed items 1–3), `corpus/knowledge/fleet-kill-rate-ledger.md` §ER-5 (lines 366–401), `corpus/SOURCES.md` S041/S047/S048 rows (lines 56–57, 153).
- `tools/mutate-and-run.sh:84-89` (leg table) and `:540-553` (PIN_*/REV_* constants).

Not done by this seat (out of assignment): no check or selftest executed, no sibling gate run, no source re-fetched (S048 wording taken from the existing SOURCES row, knowledge §1 and the round-13 lesson, which the closure reviewer states it verified).

## Finding 1 — §6 is stale, not wrong, and the receipt now exists

§6 says no `pin-dispositions.json` was present and "asserts nothing about its values". That was true at write time only. The receipt exists at `.ufo/evidence/round-13/pin-dispositions.json` and `ER-5` cites it. §6 must not be edited in place; the correction below is appended.

Observed receipt values (from `pin-dispositions.json`, read this round):

- `schema` `pin-disposition-v1`; `tool_sha256` `297253971dab3a558b470a04162b9d768287844dc0e81bf41a1f9f263ff14f11` (equals `expected.json` input digest and `verification.json` `pin_selftest` tool identity); `status` `ok`.
- `observed_at` `2026-10-20T04:59:26Z`; `counts` legs 6, unchanged 3, changed 3, unavailable 0.
- `result_reuse` `not_established` at top level and on all six rows.
- `not_compared`: mode/exec-bit; runner version and embedded defect specs; suite command and test harness; interpreter and toolchain versions; environment variables; dependency versions; fixture and companion files; timeouts (eight entries).

Per-leg (pinned sha256 equals manifest expected_sha256 and runner PIN_*; HEAD blob equals worktree sha256 in every row):

| leg | pinned commit | pinned sha256 (abbrev) | HEAD at read | HEAD/worktree sha256 (abbrev) | content_status |
|---|---|---|---|---|---|
| js-kimi-census | 175de6ba | 83016d45 | 1770305f | 5e8d5913 | changed |
| bash-surface-census | fecee874 | 275d8294 | c2cab35b | 275d8294 | unchanged |
| bash-tsukuroi-census | 165307fe | 084951be | 9574a189 | d17d32a3 | changed |
| bash-mado-verify | eead56b2 | d7edaab4 | 59cfbdc3 | 037b05dc | changed |
| bash-checklist-run | fecee874 | 7e5ec98b | c2cab35b | 7e5ec98b | unchanged |
| js-claims-check | 175de6ba | e9a21b44 | 1770305f | e9a21b44 | unchanged |

Runner constants (`tools/mutate-and-run.sh:542-553`): `PIN_JS`=83016d45…, `REV_JS`=175de6ba…, `PIN_BASH`=275d8294…, `REV_BASH`=fecee874…, `PIN_TSUKUROI`=084951be…, `REV_TSUKUROI`=165307fe…, `PIN_MADO`=d7edaab4…, `REV_MADO`=eead56b2…, `PIN_CHECKLIST`=7e5ec98b…, `REV_CHECKLIST`=fecee874…, `PIN_CLAIMS`=e9a21b44…, `REV_CLAIMS`=175de6ba… — all six pairs match the manifest and the receipt. The receipt itself does NOT carry this mapping; it is a reader reconstruction (this seat, and the round-13 wave report `IncrementalKnowledge.md` line 60, `ALL_MATCH True`).

## Finding 2 — §6 invariants: which are satisfied by the receipt, and which are not

| §6 invariant | Receipt evidence | Verdict |
|---|---|---|
| six rows, one per §4 leg, no seventh | 6 legs, names match §4 | satisfied |
| `observed_at` (UTC) and each repo's HEAD | `observed_at` present; per-row `head.commit` | satisfied |
| each row's pin equals runner `PIN_*` | Receipt does not record it; matches runner by reader reconstruction | **not in receipt** (see Finding 4) |
| current committed blob separate from worktree; missing = explicit `unavailable` | `head.blob_sha256` and `worktree.sha256` both per row; `unavailable` 0 | satisfied |
| reuse field `not_established` on every row | yes, all six | satisfied |
| states which inputs were NOT compared | `not_compared` list of eight | satisfied |

## Finding 3 — draft append-only correction text (for knowledge maintenance; NOT applied)

Intended append location: after the final line of `corpus/knowledge/incremental-pin-disposition.md` (line 312, `- **No errata** at this write.`). The existing "No errata at this write" line stays as written. Draft:

```markdown
## 8. Errata — empirical backlink for round 13 (appended in round 14)

Append-only. §§1–7 are unchanged. §6 was written before the round-13 receipt existed; its statement that no `pin-dispositions.json` was present and its "asserts nothing about its values" are superseded by this section. Its invariants in §6 are not revised.

**Receipt.** `.ufo/evidence/round-13/pin-dispositions.json` (schema `pin-disposition-v1`, `tool_sha256` `297253971dab3a558b470a04162b9d768287844dc0e81bf41a1f9f263ff14f11`, `status` ok, `observed_at` `2026-10-20T04:59:26Z`). Six legs; unchanged 3, changed 3, unavailable 0. `result_reuse` is `not_established` on every row and at top level. `not_compared` lists mode/exec-bit, runner version and embedded defect specs, suite command and test harness, interpreter and toolchain versions, environment variables, dependency versions, fixture and companion files, and timeouts.

**Per-leg content state (observed by the probe; not executed by this entry).**

| leg | pinned commit | HEAD at read | content_status |
|---|---|---|---|
| js-kimi-census | `175de6ba` | `1770305f` | changed |
| bash-surface-census | `fecee874` | `c2cab35b` | unchanged |
| bash-tsukuroi-census | `165307fe` | `9574a189` | changed |
| bash-mado-verify | `eead56b2` | `59cfbdc3` | changed |
| bash-checklist-run | `fecee874` | `c2cab35b` | unchanged |
| js-claims-check | `175de6ba` | `1770305f` | unchanged |

Each row's pinned sha256 equals its manifest `expected_sha256` and the runner `PIN_*` constant at `tools/mutate-and-run.sh:542-553`. This mapping is a reader reconstruction; the receipt does not record it.

**Reading.** `unchanged` is not a reuse verdict; `changed` is a re-pin and re-sweep request (ER-3 trigger 3), not a successor measurement. No leg was executed, no control or restore proof was produced, and no kill-rate changed. §5a's omitted-input list still applies to every row.

**Post-window movement.** `mado-shokunin` later acquired a closure-only commit (round-13 lesson). That movement is not in the receipt and is not measured here.

**Known receipt gaps.** (a) The runner mapping is not recorded in the receipt. (b) The round-13 `GIT_DIR` poisoning check is recorded only as an equal-result claim; its injected variable is not a field of the receipt. The round-14 context receipt records both; this section does not cite it until that receipt exists.

**Source wording.** For PIT item 4, prefer S048: prioritisation, not a reuse skip; quote "it should therefore be prioritised above others". S047's "test-versus-mutation" paraphrase, the "old killing test" gloss in S047's SOURCES cell, and S041's "all but one" wording are superseded; retained as history. S047/S048 are two correction rows for the same PIT URL (census W04 duplicate-URL warning, deliberate).

**Scope.** No new kill-rate, no seventh case, no F7 closure, no successor sweep. Frozen round-12 and round-13 bytes are unchanged by this entry.
```

Notes on the draft:
- It does not use the pronoun-resolving wording ("prioritises an old killing test") found in the S047 SOURCES cell and the round-13 lesson's Gate table. S048 explicitly declines to resolve "it"; the correction must not reintroduce that gloss.
- It does not cite the round-14 context receipt as existing. Fill that line only after `.ufo/evidence/round-14/context-receipt.json` exists, or leave the gap line as written.

## Finding 4 — risks

1. **Runner mapping not in receipt.** §6 requires "each row's recorded pin equals the runner's `PIN_*`". The receipt cannot show this alone. Owner: ReceiptHarness (`.ufo/evidence/round-14/capture-context.py`), which must emit an explicit six-row mapping table in `context-receipt.json`. Until then the correction text labels it as reader reconstruction.
2. **GIT_DIR injection not durably recorded in round 13.** Round-13 `verification.json` identical argv and no injected-env field; the lesson's Routed item 2 says so. The round-14 harness must retain `injected_env` with the exact variable name and value (`GIT_DIR=/nonexistent/tameshi-round14-poison`). The correction text does not claim the round-13 poisoning setup was reproducible.
3. **Stale `producer_before` expectation.** `expected.json` `producer_before` still expects the kind assertion text, but the raw run crashed (path-layout `FileNotFoundError`, `verification.json` `producer_before`). This is an expectation-disposition issue (DispositionSpec / Gate), not a §6 claim. The correction text does not cite `producer_before` as passing.
4. **Knowledge §1 wording stays.** §1 still says "S047 records this precision correction" and uses "test-versus-mutation" in the header line 5 context. This is kept intentionally; the appended §8 designates S048 as governing. A reader who starts at §1 must still reach §8.
5. **Lesson says "Injecting GIT_DIR did not change probe data"** — equality of retained JSON only, not the setup. The correction must not upgrade this to a verified environment-independence claim; §5's "environment variables" row remains `partial [O]`.

## Checks L1 should run after all seats land (not run by this seat)

- `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff --numstat -- corpus/knowledge/incremental-pin-disposition.md` — expect additions only (no deletions) after the append, if the append is applied.
- `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff --quiet 546b371a48a2f6bd1e7dca6ae8aee2a6dc1b0a50 -- .ufo/evidence/round-12 .ufo/evidence/round-13 tools/mutate-and-run.sh SHONEN.md` — expect exit 0 (frozen bytes; `pin-dispositions.json` is new in round 13, so judge the round-13 artifacts against the recorded input digests instead of `--quiet` alone).
- Recompute `expected.json` input digests with `sha256sum` for each entry of `inputs` (13 entries) — expect zero mismatches.
- `python3 -c 'import json;d=json.load(open(".ufo/evidence/round-13/pin-dispositions.json"));print(d["counts"],d["result_reuse"])'` — expect `{'legs': 6, 'unchanged': 3, 'changed': 3, 'unavailable': 0}` and `not_established`.
- `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` — expect exit 0 with the two W04 duplicate-URL warnings for S047/S048 (disclosed, not an error).
- Gate/ReceiptHarness owners: `python3 tools/pin-disposition.py --selftest` (expected `SELFTEST: PASS (18/18)`) and `python3 tools/witness-metadata.py --selftest` (expected `SELFTEST: PASS 39/39`) are existing round-13 results; any re-run is an integrated-check decision for L1.

## Verdict

- Contract-level: the §6 correction block above is ready to apply by an authorized knowledge owner; it is not applied.
- Code-level: runner constants read and matched; receipt values read and matched; the gate/checker code was not read by this seat.
- No knowledge, SOURCES, LOG, SCORECARD or historical evidence file was modified.

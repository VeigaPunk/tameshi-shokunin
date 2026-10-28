# T54W2Read17 — cold read at C1

- Section: `## Context gate classification and explicit exit classes — round 15`
- Candidate (C1): `99c3bc88d704566197783f66b211ee0a830e0330`
- Span at C1: `start=1635 end=1701` (text = lines 1635–1700; `sectionize` strips trailing blank lines)
- `section_sha256`: `132cfb9ef1aa07111af42389e4fe862152e3118b3a8bb66f1d84a6a332e7edf6`
- Findings: **none** (empty list). No rule in the section names a non-resolving anchor, no table cell was stale against the artifact it cites, and no sentence contradicts another in the same section.

## Findings

```json
[]
```

## Artifacts opened (all read at C1 unless stated)

| Artifact | What it was opened for | Observation |
|---|---|---|
| `SKILL.md:1635-1700` at C1 | the section itself | read byte-wise (`cat -A`) and plain; single UTF-8 em dash in the heading and in `pin—built`, `§` intact, no tabs, no trailing whitespace, no double spaces, no duplicated word, no run-together token |
| `corpus/SOURCES.md` (C1) | `S051`, `S049` | S051 row = "Retained context-receipt gate — tools/context-capture.py … opened 2026-10-20" (round 15, i.e. "opened this round"); S049 row = Python `subprocess` environment mapping (the section's "explicit child invocation" label, matching the row's claim about explicit env mappings defining the child environment) |
| `corpus/lessons/round-15.md` (C1) | "Gate and Mistakes" | `## Gate` at :11 and `## Mistakes` at :46 exist; Mistakes rows `gate-misclassification` / `exit-class-ambiguity` are exactly what this section corrects |
| `corpus/lessons/round-14-verifier-spotcheck.md` (C1) | "Routed defects item 5" | `## Routed defects and residuals` at :154, item 5 at :160: capture-context.py labelled a probe although `decide()` emits `mismatch`/exit1, and the C1 exit64 mapping request |
| `../PROTOCOL.md` (fleet root `/home/vgpnk/Projects/shokunin/PROTOCOL.md`) | `§Gate standard` | `## Gate standard` at :375; defines gate vs probe, `0`=clean / `1`=failed fleet-wide, other declared codes mapped onto `clean|failed|could-not-evaluate`, undeclared nonzero = could-not-evaluate, and `snapshot_tampered` for an edited snapshot |
| `.ufo/evidence/round-15/verification-3.json` (C1) | "effective runtime evidence" | `attempt: 3`, `passed: true`, `failed_checks: []`, 44 checks, `requested_rev 7650fe4…` ("round-15: preserve second harness failure and restore token parser") |
| `.ufo/evidence/round-15/verification.json`, `verification-2.json` | "the two earlier failed harness receipts" | `verification.json`: `passed:false`, failed `selftest-new`, `selftest-new-full-count` (44 checks); `verification-2.json`: `attempt 2`, `passed:false`, failed `runner-internal-error` (18 checks) |
| `.ufo/evidence/round-14/capture-context.py` (C1) | sha256 and the three cited line anchors | sha256 `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89` matches the section; 647 lines; `:2-31` = module docstring (two-document comparison excluding only top-level `observed_at`, GIT_DIR injection, git control, the round-13 `expected.json`/`pin-manifest.json` inputs, six header rows / six `run_regression` calls); `:553-580` = `def decide()` returning `("mismatch",1,…)` / `("ok",0,[])`; `:605-643` = `def main(argv)` incl. `return 64` on unexpected argv |
| `.ufo/evidence/round-14/context-receipt.json` (C1) | clean retained receipt pin | sha256 `05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a` matches; `status ok`, `exit 0`, `mapping.legs` = 6 (`js-kimi-census`, `bash-surface-census`, `bash-tsukuroi-census`, `bash-mado-verify`, `bash-checklist-run`, `js-claims-check`), `parsed.header_rows/pin_constants/rev_constants/leg_calls` = 6 each |
| `.ufo/evidence/round-14/context-missing-env.json` (C1) | negative retained fixture pin | sha256 `1ee9d09bc5277fd17b90c7f21e0ed4126825c97875b32b60dfcc2ca2852aa208` matches |
| `.ufo/evidence/round-15/frozen/context-missing-env/expected.json`, `…/context-clean/expected.json` (C1) | caller-committed expected pins | `{"exit": 1, "id": "missing_injected_environment", "receipt_sha256": "1ee9d0…", "schema": "tameshi-context-expected-v1"}` and `{"exit": 0, "id": "context_consistent", "receipt_sha256": "05cb55…", "schema": "tameshi-context-expected-v1"}` |
| `tools/context-capture.py` (C1) | the maintained gate the section describes | `FROZEN_RECEIPT_REL`/`FROZEN_RECEIPT_SHA256` = the round-14 clean receipt + `05cb55…`; `FROZEN_EXPECTED_ID = "context_consistent"`; flags `--check/--selftest/--json/--receipt/--expected`; check mode writes nothing; docstring exit map `0 / 1 / 2 / 64`; error ids `receipt_json_invalid`, `snapshot_tampered`, `missing_injected_environment`, `usage_error`; selftest fixtures built in memory from `build_fixture_receipt()` (`clean = mutate(lambda document: None)`), not read from the retained files; the archived script is named only in prose (no invocation) |
| `SKILL.md:1589-1628` (C1) | "round-14 registry history … above with an inline archive marker" and "round-14 recipe step 5" | registry row at :1628 reads `archived invocation context capture | historical gate, not active | do not run; retained source … only`; recipe step 5 at :1618 opens `**Archived experiment, not an entry point:**` |
| `tools/evidence-disposition.py` (C1) | "Both active gates share three classes over four exit codes … `64` usage" | docstring exit map includes `64 usage error`, `USAGE` block, `return 64` on usage → the second active gate matches the same 0/1/2/64 lattice |
| `.ufo/evidence/round-18/measure.py` (C1) | how `sectionize` bounds the section | section = heading line through the line before the next heading, trailing blank lines stripped, joined with `\n`, no trailing newline; reproduces `start=1635 end=1701` and the printed sha |

## Commands run

```
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
export HYAKU_SCRATCH=/fast/scratch/hyaku
export TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W2Read17

python3 .ufo/waves/round-54/reader-section.py /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  99c3bc88d704566197783f66b211ee0a830e0330 "## Context gate classification and explicit exit classes — round 15"
# {"start": 1635, "end": 1701, "section_sha256": "132cfb9ef1aa07111af42389e4fe862152e3118b3a8bb66f1d84a6a332e7edf6"}

git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show \
  99c3bc88d704566197783f66b211ee0a830e0330:SKILL.md | sed -n '1635,1701p'
git -C <lane> show <C1>:SKILL.md | sed -n '1628,1710p' | cat -A        # invisibles

# pin checks (values quoted in the section)
git -C <lane> cat-file -p <C1>:.ufo/evidence/round-14/capture-context.py | sha256sum
git -C <lane> cat-file -p <C1>:.ufo/evidence/round-14/context-missing-env.json | sha256sum
git -C <lane> cat-file -p <C1>:.ufo/evidence/round-14/context-receipt.json | sha256sum

# anchor checks
git -C <lane> cat-file -p <C1>:.ufo/evidence/round-14/capture-context.py | grep -n 'def decide\|^def '
git -C <lane> cat-file -p <C1>:.ufo/evidence/round-14/capture-context.py | sed -n '1,36p;550,584p;602,647p'

# receipts, census, lessons, PROTOCOL
git -C <lane> cat-file -p <C1>:.ufo/evidence/round-15/verification{,-2,-3,-4}.json   # json: passed/failed_checks
git -C <lane> cat-file -p <C1>:corpus/SOURCES.md | grep -nE '^\| ?S049|^\| ?S051'
git -C <lane> cat-file -p <C1>:corpus/lessons/round-15.md | grep -n '^#\|Gate\|Mistake'
git -C <lane> cat-file -p <C1>:corpus/lessons/round-14-verifier-spotcheck.md | grep -n 'Routed\|5\. '
grep -n 'Gate standard' /home/vgpnk/Projects/shokunin/PROTOCOL.md

# executable confirmation of the section's table cells and exit classes (check mode writes nothing)
python3 tools/context-capture.py --check
#   CONTEXT: OK (id=context_consistent … exit=0 findings=0)                          exit=0
python3 tools/context-capture.py --check \
  --receipt .ufo/evidence/round-14/context-missing-env.json \
  --expected .ufo/evidence/round-15/frozen/context-missing-env/expected.json
#   CONTEXT: MISMATCH (id=missing_injected_environment … exit=1 findings=2)          exit=1
python3 tools/context-capture.py --check --receipt .ufo/evidence/round-14/context-receipt.json
#   … context-capture.py: --receipt and --expected must be given together
#   CONTEXT: USAGE_ERROR (id=usage_error exit=64)                                    exit=64
cp .ufo/evidence/round-14/context-receipt.json "$TMPDIR/tampered.json"; printf ' ' >> "$TMPDIR/tampered.json"
python3 tools/context-capture.py --check --receipt "$TMPDIR/tampered.json" \
  --expected .ufo/evidence/round-15/frozen/context-clean/expected.json
#   CONTEXT: INVALID (id=snapshot_tampered … exit=2 findings=2), no traceback        exit=2
```

## What each pass checked

1. **Anchors resolve at C1.** `S051`/`S049` census rows, `corpus/lessons/round-15.md` (`## Gate`, `## Mistakes`), `corpus/lessons/round-14-verifier-spotcheck.md` Routed defects item 5, `../PROTOCOL.md` `## Gate standard` (fleet root, as the path implies — the errata row at :1614 records that `../` fix), `.ufo/evidence/round-15/verification-3.json`, the archived script and its `:2-31` / `:553-580` / `:605-643` ranges (file has 647 lines), both pinned fixtures, `tools/context-capture.py`, and the "above" registry row at :1628 and round-14 recipe step 5 at :1618.
2. **Pins are exact.** All three quotable digests in the section (`7313e9…` archived script, `1ee9d0…` negative fixture, `05cb55…` clean receipt) reproduce from the C1 blobs; the clean receipt is also the gate's built-in default and the round-15 frozen clean expected pin names it.
3. **No stale table cell.** Rows 1–4 of the Evidence-condition table were exercised against the gate itself at C1: clean→exit0/`context_consistent`; re-derived predicate disagreement→exit1/`missing_injected_environment`; edited snapshot→exit2/`snapshot_tampered` with no traceback; usage→exit64/`usage_error`. Row 5 matches the retained receipt's own mapping block (6 legs, one `GIT_DIR` injection, no argv execution). The "two earlier failed harness receipts" are exactly `verification.json` and `verification-2.json`.
4. **No self-contradiction.** "Retained-only" vs "read-only receipts"; "archived, not active" vs recipe step 5 ("Archived experiment, not an entry point"); "three classes over four exit codes" vs both active gates' exit maps (context gate docstring and `tools/evidence-disposition.py` both declare 0/1/2/64); "six static mappings" (table) vs "six leg mappings" (prose) vs the receipt's 6 legs; "an undeclared nonzero code also reads as could-not-evaluate" matches `PROTOCOL.md` §Gate standard.
5. **Prose hygiene (QUALITY 104 class).** No run-together tokens, missing spaces, double spaces, tabs, trailing whitespace, duplicated words, doubled em dash, odd inline-code backtick counts, or line-scoped unbalanced parentheses (the only "unbalanced" hits are multi-line parentheticals, e.g. the Sources list and the `(sha256 …)` pins).

## Checked and deliberately **not** reported

- `.ufo/evidence/round-15/verification-4.json` also sits in the round-15 evidence directory and failed (`tool-source-pin`, `integrity-*`, `runner-published-digest`, `measure-after-fields`). It is **not** a stale-cell defect: its `requested_rev` is `7c10fa7…` (round-53, 2026-10-27; `7650fe4…` is an ancestor), i.e. a much later replay of the round-15 runner against a moved tree, not a round-15 attempt. The section's phrase is "the two **earlier** failed harness receipts" and is literally true; `verification-3.json` remains the only passing round-15 receipt, so "effective runtime evidence" is not contradicted. Reporting it would require reading "earlier" as "all", which the bytes do not say.
- Paraphrase-only nits that are not defects under the wave-2 rule: "archive-only" as a paraphrase of recipe step 5's literal `**Archived experiment, not an entry point:**`; "`clean`/`failed`" as class names although stdout prints `CONTEXT: OK`/`CONTEXT: MISMATCH` (§Gate standard fixes `0`=clean and `1`=failed fleet-wide).

## Notes / limits

- Read-only seat: no lane file was edited; the only writes are `T54W2Read17.json` and this MD under `.ufo/waves/round-54/w2/`, plus ephemeral files under `$TMPDIR`. No mutating git command was run; every blob was read with `git cat-file`/`git show` at C1.
- No tool was installed or upgraded for this seat (nothing beyond python3 and git was needed).
- The four gate invocations above are the gate's documented check mode, which "writes nothing"; no receipt file was created or modified in the lane.

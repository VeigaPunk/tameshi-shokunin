# T57W1ExecStandingRules — SKILL standing-rules truth (R56.2) and gate registry row

Base: `5e3569969b532310d2b8a3d130901757a3df356b` SKILL.md (2214 lines). No lane file edited; nothing mutated in the lane.

## Staged patches (`stage/`, all `diff -u` with labels a/SKILL.md b/SKILL.md, apply with `patch -p1` against base bytes; dry-run + apply verified on a scratch copy)
| file | change | line count |
|---|---|---|
| `T57W1ExecStandingRules/stage/skill-standing-rules.diff` (**recommended**) | receipt-table fix (rows 53, 55) + registry row + merge of the 2-line "Registry scope" opener into 1 line | 2214 → 2214 (net 0) |
| `.../stage/skill-standing-rules-alt-plus1-insert.diff` | same table fix + registry row only | 2214 → 2215 (+1) |
| `.../stage/skill-standing-rules-table-only.diff` | table fix only (rows 53, 55) | 2214 → 2214 |

## Executed truth table (fixture repo, gate `tools/receipt-revision-gate.py`; full output verbatim in `T57W1ExecStandingRules-receipts/gate-truth-table.txt`)
Fixture: R1 (surf.txt=a, other.txt=x) → R2 (other.txt changed; surf.txt same as R1) → R3 (surf.txt changed). `paths.txt` lists `surf.txt`. Receipt names R1 (`VERDICT: rev=R1 X_PASS=true`).

| role | `--paths` | certified | drift on listed path R1→cert | code | exit |
|---|---|---|---|---|---|
| verdict | absent | R2 | none (only other.txt) | `RECEIPT_REV_MISMATCH` | 3 |
| verdict | absent | R3 | yes | `RECEIPT_REV_MISMATCH` | 3 |
| verdict | given | R2 | none | PASS (`GATE OK`, codes=none) | 0 |
| verdict | given | R3 | yes (`drift=surf.txt`) | `RECEIPT_REV_CONTENT_DRIFT` | 3 |
| positive | absent | R2 | none | `RECEIPT_REV_MISMATCH` | 3 |
| positive | absent | R3 | yes | `RECEIPT_REV_MISMATCH` | 3 |
| positive | given | R2 | none | PASS | 0 |
| positive | given | R3 | yes | `RECEIPT_REV_CONTENT_DRIFT` | 3 |

Extra rows run: receipt rev == certified → PASS, exit 0; receipt rev `deadbeefdeadbeef` (role verdict or control) → `RECEIPT_REV_UNRESOLVABLE`, exit **3**; receipt with no `rev=` → `RECEIPT_REV_ABSENT`, exit 3; `--certified 000…01` (unresolvable certified) → `GATE: error=unresolvable-certified … codes=RECEIPT_REV_UNRESOLVABLE`, exit **2**; `--paths` file that exists but lists nothing → `RECEIPT_REV_CONTENT_DRIFT` with `drift=<no --paths given: content identity is not checkable>`, exit 3 (an edge: an empty paths file is not "absent"); `--json` carries `"verdict": "REFUSED"` and exit 3.

Findings: (a) verdict and positive gate identically (the code path is `role_name in ('positive','verdict')`); (b) the base cell `RECEIPT_REV_MISMATCH` for a verdict receipt is true only without `--paths`; with `--paths` it is PASS (no drift) or `RECEIPT_REV_CONTENT_DRIFT` (drift) — never MISMATCH; (c) row 2 (positive control, `RECEIPT_REV_CONTENT_DRIFT`, no `--paths`: MISMATCH) was already true; (d) row 3 `RECEIPT_REV_UNRESOLVABLE` is exit 3 for a receipt rev; the exit-2 case is the `--certified` rev, which the base table never said — hence the registry verdict map `0 PASS; 2 certified revision unresolvable; 3 refused with a named code` is exact.

## Edits (what the patch changes)
1. Line 53 (verdict row): situation gains "(a positive receipt gates identically)"; code cell becomes `RECEIPT_REV_MISMATCH` without `--paths`; with `--paths`: `RECEIPT_REV_CONTENT_DRIFT` if the surface drifted, else PASS. Rule cell unchanged. One line, same line.
2. Line 55 (UNRESOLVABLE row): code cell gains "(exit 3; an unresolvable `--certified` itself exits 2)". One line, same line.
3. Registry row (after line 1546): `receipt-revision gate | gate | entry command | 0 PASS; 2 certified revision unresolvable; 3 refused with a named code | python3 tools/receipt-revision-gate.py --selftest | CODES tuple and the 19 literal selftest cases (selftest run here: `GATE_SELFTEST: 19/19 pass`) | read-only on lane (git objects only); --selftest writes one fixture repo under $TMPDIR (tameshi-r56-gate-*) removed on exit | tameshi`. The pinned-values cell names no fixture file because the gate pins none; the L1 may replace it with the registry-row paths once the `gate` rows exist.
4. In the recommended patch the registry's trailing paragraph opener (base lines 1548-1549, "Registry scope is these round-12 instruments; no new conformance assertion is / made about the historical runner. Witness…") is joined into one line and amended to "…round-12 instruments plus the round-56 receipt gate; no new conformance assertion is made about the historical runner. Witness…" so the inserted line is offset by a removed line and every line from 1550 on keeps its number. Cold-read caution: this changes the bytes of the paragraph the "never a seventh independently measured gate" sentence closes; the sentence's meaning is unchanged (the new gate is not a recorded case of the promotion paragraph).

## Anchor impact of the +1 insert (alt patch; recommended patch has zero)
Inserting one line at base 1547 shifts base lines 1547–2214 (668 lines) by +1.
- Page-local `:NNN` text in SKILL.md after line 1546 (`grep -nE ':[0-9]{2,5}'`): 8 lines — 1568, 1671, 1774, 1782, 1795, 1869, 1870, 1975. None points at a SKILL.md line after 1546: 1568/1671/1774/1795/1869/1870/1975 cite other files' lines (`tools/pin-disposition.py:67-71`, `claim-ledger.sh:164`, `round-gate.mjs:1381-1382`, `tools/evidence-disposition.py:479-544`, `:2-31` etc.); 1782's `:925-929` points to SKILL line 925 (before the insert, unmoved). So no in-page anchor breaks.
- External citations of SKILL.md lines >1546 without `@rev` that the shift would break: `.ufo/evidence/round-21/coldread/ledger.json` (SKILL.md:2136, 2144, 2149, 2154, 2161), `.ufo/evidence/round-49/c1/corrections.json` (SKILL.md:1555), `.ufo/evidence/round-49/c1/reads.json` (SKILL.md:1550, 1558-1561); plus corpus lesson/knowledge files cite unversioned `SKILL.md:NNN`, e.g. round-51.md (grep list in receipts). Earlier cold-read key headings keyed to lines 1550-1561 and 2136-2161 would lose credit under the +1 variant. Receipt: `T57W1ExecStandingRules-receipts/anchors-after-1546.txt`.
- The standing-rules table edits are line-neutral in every variant: SKILL.md lines 1-1546 outside lines 53 and 55 are byte-identical in all three patches (verified with `cmp`), and for the recommended patch lines 1550-2214 are byte-identical (verified with `cmp`).

Recommendation: apply `skill-standing-rules.diff` (net 0). If the L1 refuses the merged-paragraph edit, apply `skill-standing-rules-table-only.diff` and place the gate row elsewhere (e.g. replace a cell), because the +1 variant moves lines the round-49/21 evidence cites.

## Not done / risks
- The registry table mentions `19 literal selftest cases`; I ran the selftest once (19/19 pass) — if the gate changes, update the count.
- SKILL.md changes alter the pinned bytes of any ledger entry that pins SKILL.md; the L1 re-keys in wave 3.
- Scratch tree `/fast/scratch/hyaku/tameshi-r57/T57W1ExecStandingRules` cleanup: removed on exit below.

# T57W1ScribeItemsR51x1to4 — ledger rows R51.1–R51.4 (round 57, wave 1)

Lane base `5e3569969b532310d2b8a3d130901757a3df356b`. Spot-check `corpus/lessons/round-51-verifier-spotcheck.md`, added at `ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4` (blob sha256 `f3aab8dd…306a79`, equal at ef19d8e and at base). Scope: items 1–4 of `## Routed defects for the lane next round` (spot-check lines 126–129). No lane production file was edited. Files written: `rows.json` and this report in the seat's wave directory, and receipts under `T57W1ScribeItemsR51x1to4-receipts/`.

## Verdicts

All four items are `fixed` by one lane commit: **`bcba8924894216268afc4171f06eb8c28e912b46`** (`round-52: C1 registry row 10/10 + fleet-bound round21 self-test; C2 SKILL corrections, kill-rate supersession, 20 ledger correction records`). It is a descendant of ef19d8e and an ancestor of base. Nothing is `open`, `declined` or `unresolved`, so no patch is staged and no item is `fixable-cheap` or `fixable-costly`.

| Row | Status | Commit | Item (short) | Basis (base vs ef19d8e) |
|---|---|---|---|---|
| R51.1 | fixed | bcba892 | registry `mte-interop-check` expects 9/9 but the tool's ten-leg panel cannot print it | `tools/registry.json:1266` reads `legs_conforming=10/10` at base; `:1014` read `9/9` at ef19d8e. The tool prints `legs_conforming=%d/%d` (`tools/mte-interop.py:343`) over a ten-entry `LEG_TABLE` (`:74-78`). |
| R51.2 | fixed | bcba892 (one pointer from 7ff81a5) | stale SKILL `:2136` "nine ledger legs"; runner row `/tmp` scope; runner pointers `:174`, `:211`, `:937-950` | `SKILL.md:2179` "ten ledger legs"; `:2192` `${TMPDIR:-/tmp}`; `:202` → `tools/mutate-and-run.sh:434` (the APPLY FAIL count print); `:970` → `139-143,1519-1548` (the exit map), re-anchored in 7ff81a5 (round 52). |
| R51.3 | fixed | bcba892 | `coldread/refresh.py:224-227` writes `wrong_expectations: 0` for re-keyed sections | The item's first option is taken: a top-level `corrections` list of 20 records is appended to `.ufo/evidence/round-21/coldread/ledger.json` (base line 112187). Record 1 names the round-51 `refresh.py:227` zero and carries the recorded count 3 (`:112193`). The round-52 re-key instrument writes `len(reader['findings'])` (`.ufo/evidence/round-52/coldread/refresh.py:216`, added by f1a3246). |
| R51.4 | fixed | bcba892 | `round21-measure --selftest` not hermetic; counter needs a declared fleet-bound row class | The item's second option is taken. `tools/round21-measure.py:9-12` declares the selftest "fleet-bound, not hermetic"; the c2 fixture reads the `FLEET` literal (`:77`); the SKILL gate row `SKILL.md:2200` says the same. |

Id rule: a labelled item (`**R51.1,`) takes its label; an unlabelled item takes its 1-based position in the item list, as the round-50 extractor does with `enumerate(…, 1)`. Items 1–4 are R51.1–R51.4. R51.5 (the mutation attack named in item 4) is outside this item.

## Evidence and checks

- The round-50 counter was imported, not copied (`.ufo/evidence/round-50/c1/measure.py`). Its `check_evidence` and `measure` ran over a fixture ledger holding only these four rows, with the round-51 spot-check as the defect file. Result: `evidence_bad=0 key_miss=0 fixed_bad=0 missing=0 spotcheck_changed=0 notes=[]`; `stat` = fixed 4. Receipt: `…-receipts/measure-resolver.txt`.
- Per-excerpt presence at base and absence at ef19d8e: `…-receipts/excerpt-check.txt`. Every keyed (fresh) excerpt is absent at ef19d8e and present at base. Two supporting excerpts (`mte-interop.py:343`, ledger `:112193`) also exist at ef19d8e, and they are not the keyed items. The round-52 `refresh.py` path does not exist at ef19d8e, which the counter treats as fresh.
- Ancestry, the pickaxe result for each fix phrase, and the scope-monitor check: `…-receipts/ancestry.txt`. The pickaxe shows each fix phrase first appears in bcba892, except the `139-143,1519-1548` pointer, which came from 7ff81a5. `.ufo/evidence/round-52/no-harm.sh:6,33` allows `M:tools/registry.json` and `M:tools/round21-measure.py`.
- Green registry receipt (R51.1 asks for one): not re-run. A committed run exists at `.ufo/waves/round-55/w2/T55W3R16-receipts/mte-interop-check-C0.out:12` (`MTE_INTEROP: PASS legs_conforming=10/10`), and round-55 `T55W3R16.md:27` records the live run (299 s). The search is in `…-receipts/green-receipt-search.txt`.
- Scripts (copies in receipts): `build.py` (locates excerpts and writes rows), `excheck.py` (base vs ef19d8e presence), `check.py` (runs the counter's `measure` on `rows.json`).

## Rows

`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w1/T57W1ScribeItemsR51x1to4/rows.json`: a list of four rows in the round-50 schema (`id, status, evidence[{path, lines, excerpt}], commit, seat, note`), each with `keys` (3–5) and `verdict_basis`. Seat `T57W1ScribeItemsR51x1to4`. No `reason`, because nothing is declined.

## Not run, and what this does not establish

- `registry-check --only mte-interop-check` and `tools/mte-interop.py --check` were not executed (they need uv, jsonschema and live sibling stores). The R51.1 verdict rests on static text (row against tool print and LEG_TABLE) plus the round-55 committed run, which I located and did not re-run.
- R51.4: the SCORECARD round-52 pre-registration section in bcba892 is present; I did not check its wording against the counter-amendment rule. The `fixed` verdict rests on the declared row class, not on a hermetic selftest.
- R51.2: the `:139-143` pointer is verified at base for the exit map. Lines 1519-1548 were not checked line by line.
- R51.3: the frozen round-51 `refresh.py:227` still writes a literal 0. That path is frozen and was not touched; the correction records and the round-52 instrument are the fix.
- Cold-read monitor, no-harm monitors, C1/C2/C3 counters and the cold-read input sets were not run. Nothing was staged, so no pinned input changed.

## Tools

None installed or upgraded. Read-only `git` (`show`, `log`, `grep`, `merge-base`, `clone --shared` into a scratch clone) and `python3` for the import-and-check. No pacman, no host service touched.

## Handoff to L1

- When the counter runs at the content-final rev, bcba892 must be an ancestor of that rev (it is an ancestor of base, so any rev descended from base qualifies).
- Merge the four rows into `corpus/routed-defects.json` `defects`; the ledger edit is the L1's. The round-50 counter floors (fixed >= 20, this-round >= 5) are the L1's to judge across all rows.

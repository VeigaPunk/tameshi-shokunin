# T57W1ConnectorSiblings — sibling-overlap scan (read-only)

Seat: T57W1ConnectorSiblings (connector, leaf). Lane base 5e3569969b532310d2b8a3d130901757a3df356b.
Scope: 21 sibling lanes under /home/vgpnk/Projects/shokunin/*-shokunin/, read-only. No edits to any lane or fleet file.
Receipts: `.ufo/waves/round-57/w1/T57W1ConnectorSiblings-receipts/` (`sweep.txt` = the scan script output; `linemap.txt` = line locators).
Scratch script: `$HYAKU_SCRATCH/tameshi-r57/T57W1ConnectorSiblings/sweep.py` (removed on exit; its output is the receipt).

## Sweep run (what was checked)

1. Path census: `ls -d /home/vgpnk/Projects/shokunin/*-shokunin/` → 21 lanes (audio, chousa, game-dev-2d, game-dev-3d, kagi, kaidoku, kake, kama, kasegi, kengaku, kotoba, kotodama, kumitate, lore, mado, mori, revenger, souji, tabi, tameshi, tsukuroi).
2. Glob for ledger/registry data files in each lane's root, `corpus/`, `tools/`:
   `*-shokunin/corpus/*.json|*.jsonl|*.tsv`, `*-shokunin/tools/registry*`. Hits whose name contains routed/defect/dispos/finding/ledger/registry: `kagi corpus/closure-dispositions.json`; `kengaku corpus/routed-findings.jsonl`, `corpus/defects.jsonl`, `corpus/defects-round35.jsonl`; `tameshi corpus/routed-defects.json`, `tools/registry.json`. Nothing else.
3. Grep (`routed defect | routed-defect | closure-routed | routed-findings | exit-code map | exit map`) over each lane's `corpus/`, `knowledge/`, `lessons/`, `SKILL.md`, `tools/`. Result: 174–217 hits per batch, dominated by prose "routed defect N" references inside lessons; the only machine-checked routed ledgers are the four files in step 2 plus kaidoku's gate (step 5). Grep output truncates at 20 matches per file, so prose hits are not counted exhaustively; the claims below rest on the named files, not on the prose hit count.
4. Python re-read of every step-2 ledger for status and disposition vocabularies, plus a SKILL.md scan for gate/probe rows (`receipts/sweep.txt`).
5. Line-level reads of the gate rows and checker docstrings cited below (`receipts/linemap.txt`).

## Finding 1 — which lanes keep a ledger of closure-routed items, and their status vocabulary

| Lane | Ledger file (rows) | Status vocabulary (measured) | Other fields | Machine gate | Path:line |
|---|---|---|---|---|---|
| kengaku | `corpus/routed-findings.jsonl` (75) | `open` 31, `closed` 41, `blocked` 1, `refused` 2 | `disposition`: fixed-verified 41, accepted-risk 28, routed 4, refused-out-of-scope 2; `source` (`lesson:line`), `opened_round`, `close`, `blocker`, `check` (shell predicate run from lane root), `owner` | `plans/routed_open.py` (exit 0/1; prints `routed_open=<n> oldest_round=<r>`, withheld when a row is invalid) and `plans/round51_routing.py --run-checks` | `kengaku-shokunin/SKILL.md:634,636`; `plans/routed_open.py:5` (refuses `corpus/defects*.jsonl` by name), `:15` (status enum), `:24` (summary line) |
| kengaku (second ledger, same lane) | `corpus/defects.jsonl` (5, all `closed`), `corpus/defects-round35.jsonl` (4, all `closed`) | `open` \| `closed` only; `check` is a *function name* in `plans/defect_ledger.py`, not a shell string; `opened_round`, `closed_round`, `recurrence_of` | — | `plans/defect_ledger.py` re-runs every row's check at tip | `kengaku-shokunin/plans/defect_ledger.py:4,7` |
| kagi | `corpus/closure-dispositions.json` (15 rows, schema `kagi-closure-dispositions-v1`) | `fixed` 6, `no-action` 5, `reported` 3, `operator-owned` 1 (the `.py` docstring also names `rejected`; no row uses it). Class: routed-defect 9, spot-decision 5, adjudication 1 | `source` = `corpus/lessons/round-22-verifier-spotcheck.md`, `source_sha256` pin, `pointer` that must resolve for `fixed` | `corpus/closure-dispositions.py` (exit 0 clean / 1 failed / 2 setup; `--selftest` 14 cases) | `kagi-shokunin/SKILL.md:751`; `corpus/closure-dispositions.py:16` (obligations), `:21` (disposition set), `:34` (verdict line) |
| kaidoku | no data ledger; gate state is computed from the round-18 tool over six named defects (`R17` set) | `open`/`closed` by named + substance check sets; closed only when both pass | scope is one round's six defects, not a rolling ledger; tool lives under `.ufo/waves/round-18/tools/` | `routed-defects.py --strict` (0 all six closed, 1 any open, 2 could-not-evaluate) | `kaidoku-shokunin/SKILL.md:921` |
| mado | no JSON ledger. Rule criteria 90 and 94 govern a generated `ages.md` (tracked: `.ufo/waves/round-46/w1/ScrRoutedAges/ages.md`, 42 rows, 15 open) | prose rule: identity plus age from the first routing round (criterion 90); "emitted by the ledger that owns it, never transcribed" (criterion 94) | — | none (criterion checks by re-derivation) | `mado-shokunin/corpus/QUALITY.md:454` (90), `:490` (94) |
| kama | no routed ledger; routed items sit in lesson tables (`## Routed defects from round-15-verifier-spotcheck.md`) | not machine-checked | — | none | `kama-shokunin/corpus/lessons/round-16.md:74`, `kama-shokunin/corpus/lessons/round-17.md:93`; `registry/` holds no file whose name contains rout/defect |
| tameshi (for comparison) | `corpus/routed-defects.json` (49 rows, schema `tameshi-routed-defects-v1`) | `fixed` 31, `declined` 11, `open` 7 | fields: `id, status, evidence[], commit, seat, note, reason`; no `opened_round`, no executable `check`, no source-line field outside `evidence` | none in tree | `tameshi-shokunin/corpus/routed-defects.json` |

Notes:
- Only kengaku and kagi have a machine-checked closure ledger with exit codes. kengaku has two parallel routed-ledgers with different vocabularies (`routed-findings` enum open/closed/blocked/refused; `defects` enum open/closed); kengaku's own gate refuses the second by name (`plans/routed_open.py:5`), so the lane itself treats them as separate obligations.
- Tameshi's round-50 lesson already names the kengaku row-check design as an open routed element: `corpus/lessons/round-50.md:164` ("a per-row executable check (`T50W2ConnSiblingLedger.md`, kengaku `defect_ledger.py`)"). This scan confirms the source file is at `kengaku-shokunin/plans/defect_ledger.py`. Tameshi's ledger still has no check field (table above). This is a re-confirmation of a round-50 routed item, not a new one.

## Finding 2 — which lanes register gate entry commands with exit maps

Lanes whose SKILL.md carries a registry table with an exit/verdict column (the 'kind' column names gate/probe/measurement/etc.; counts are heuristic and are in `receipts/sweep.txt`):

- kama `SKILL.md:303` (Name | Kind / entry command | Exit map | ...), `:396` (Verdict map), `:1258–1263` (exit-map rows through round 32), `:1357–1359` (gate-registry completeness row).
- kaidoku `SKILL.md:779` (Entry / verdict map), `:919` (routed-defects), `:1015` (round22-C1), `:1698` (round-45 C2 registry row).
- kengaku `SKILL.md:634–636` (`round51-routing`, `round51-surfaces`, `routed-findings`, each with a `0`/`1` map).
- kagi `SKILL.md:34–49` (exit 0 / 1 wording per row), `:751` (closure-dispositions).
- kumitate `SKILL.md:615–626` (verdict map, `WAVE_CENSUS`, `counter-pins`, `source-capture`).
- souji `SKILL.md:244–248` (exit 0/1/2 column).
- mori `SKILL.md:187–191` (exit 0/1/2 per probe).
- tsukuroi `SKILL.md:1707–1778` (Verdict map column).
- tameshi `SKILL.md:1543`, `:1592`, `:1642`, `:1721`, `:1851`, `:1891`, `:1942`, `:1970`, `:1990`, `:2016`, `:2038`, `:2060`, `:2093` (Verdict map / Exits columns).

Machine checks that grade exit-map presence (not just occurrence):
- kama `tools/gate-registry-check.py` — defect labels `empty-exit-map` (`:26`, `:208`, `:310–311`); the SKILL row is `kama-shokunin/SKILL.md:1359`.
- kaidoku `tools/round-45/registry-scope.json` (scope file, `:1–3`) read by `tools/round-45/c2-counter.py`; SKILL row `kaidoku-shokunin/SKILL.md:1698` grades "every scope instrument has a registry row with a real exit map" (`unregistered`, `thin`, `scope_size`).
- tameshi `tools/registry.json` — 57 rows, every row has `expect.exit` (kinds: gate 22, selftest 31, probe 4), run by `tools/registry-check.py` (its docstring at `:21`, `:35` defines the hold rule). No sibling registry JSON with expected exit codes was found by glob (`*-shokunin/tools/registry*`, `*-shokunin/*.json`).

## Finding 3 — general enough to cite? (PROVINCE two-lane rule)

PROVINCE.md:14–16 admits a pattern "from evidence in TWO independent lanes before it is claimed general". Applied here:

A. Closure-routed items as typed rows with a machine check and exit-coded gate — **two independent lanes**: kengaku (`routed-findings.jsonl` + `routed_open.py`, `round51_routing.py`; SKILL.md:634–636) and kagi (`closure-dispositions.json` + `closure-dispositions.py`; SKILL.md:751). Both resolve each row against the tree (kengaku `check` shell predicates; kagi `pointer` resolution) and both pin or cite a source line/hash. Kaidoku's `routed-defects.py` (SKILL.md:921) is a third, narrower instance. **Meets the two-lane rule.** Tameshi's `routed-defects.json` lacks the check field and any open-age field, so both sibling patterns are candidate craft for the C1 counter's ledger shape, to be cited, not copied wholesale (see contested scope).
   - Age-from-first-routing: mado criterion 90 (`corpus/QUALITY.md:454`) and kengaku's `opened_round` field. Two lanes carry an age field. Mado's rule is prose plus a generated file; kengaku's is a typed field.
   - Independent convergence: kengaku `considerthese/2026-10-26.md:37` (proposal 1, "A routed-findings burn-down, not just a defect ledger") and mado `considerthese/2026-10-26.md:49` (proposal 3, "Track routed defects until they close") were proposed the same day, each then shipped as an artifact (kengaku `plans/routed_open.py`; mado criterion 90 + `ages.md`). Caveat: both come from the same daily reflection cadence, so independence is of the shipped artifacts, not of the prompt.

B. Gate registry rows with exit maps graded mechanically — **two independent lanes**: kama (`tools/gate-registry-check.py`, `empty-exit-map`) and kaidoku (`tools/round-45/c2-counter.py` over `registry-scope.json`). **Meets the two-lane rule**, but tameshi already has the stronger form (expected-exit JSON rows run by `registry-check.py`), so nothing new to cite beyond the existing method.

## Contested scope (reported, not absorbed)

- kengaku's `routed-findings.jsonl`, `routed_open.py`, `round51_routing.py`, `defect_ledger.py` are product-lane bookkeeping of kengaku's own routed items. PROVINCE.md:14–16 ("every lane's gate remains its own") and PROVINCE.md:20 ("Out of province → report, never absorb") mean tameshi may cite the method, not adopt the tool or the file.
- kagi's `corpus/closure-dispositions.py` is a kagi gate. PROVINCE.md:7–9 names "kagi-shokunin/corpus/*check*.sh + census gates" as tameshi's owned primary surfaces. `closure-dispositions.py` is not a `*check*.sh` and not named. Whether it falls under "census gates" is contested; it is reported here, not claimed.
- kengaku's two parallel routed ledgers (`routed-findings` vs `defects`) with different status enums show a craft conflict inside one lane. Tameshi should not copy the dual-ledger shape without a choice of one vocabulary; that choice is a design decision for the L1, not this seat.

## Limits and what was not run

- Greps were capped at 20 matches per file; prose routed-defect references in lessons were not enumerated per lane. Ledger, registry and gate-row claims rest on files and lines read directly.
- kama's lesson routed tables were not checked for status vocabulary (no machine ledger found; prose status not counted).
- The per-lane gate-row counts in `sweep.txt` are heuristic (a row counts as a gate row when its second cell names a kind). They are not a census. Only the cited rows were read.
- No sibling gate was executed. Read-only.
- No tool was installed or updated for this seat. Nothing was written under ~/.local/bin, pacman was not touched, no lane file was modified.

## Verification the L1 should run (none executed here)

- Re-run (absolute paths, read-only if the tool is read-only; check its `--help` first): `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/routed_open.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin` and `python3 /home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/closure-dispositions.py --root /home/vgpnk/Projects/shokunin/kagi-shokunin`. These counts were read from the files, not from a gate run.

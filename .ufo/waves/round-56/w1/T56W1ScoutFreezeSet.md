# T56W1ScoutFreezeSet — pinned-input set (PIN to REV)

## Question
Which paths must be byte-identical between the content-final revision PIN and the deciding revision, and which of C2's planned edits therefore have to land at or before C0?

## Method (observed)
Ledger and tree taken from base `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1` via `git show` / `git ls-tree -r --name-only` (worktree ledger bytes match that blob). Headings from `.ufo/evidence/round-56/c1/lost-headings-at-base.json`, byte-identical to freeze `c3e2ca9f020776b3d66c7af854fb82c834674fcf` (sha256 `dcfc9f800b8bc7b25851d80ec384b8e8781ead6a5f8adf9f0a5340479282fd4a`).

The set is the binder's own formula, not a reimplementation of credit. `binder-r55.py` (the driver `bind.sh` is specified to run) does, for each frozen heading, the union of `inputs` keys across every prior ledger entry, then skips a key only when it is in `DROP` or `blob_at(PIN)` is `None`:

- DROP at `tameshi-shokunin/.ufo/waves/round-55/w1/T55W1ExecReKeyDryBind-receipts/binder-r55.py:55`: `LOG.md`, `SCORECARD.md`, `SKILL.md`, `.ufo/evidence/round-21/coldread/ledger.json`
- union at the same file, lines 165-175

Round-18 credit then requires `sha256(REV:path) == recorded` for every pinned key it does not ignore (`input-drift:<path>`, `.ufo/evidence/round-18/measure.py:330-349`). Keys the binder records at PIN must therefore be unchanged at REV.

## Result
`.ufo/waves/round-56/w1/pinned-inputs.txt` — 7721 paths, sorted, unique, one per line. sha256 `2a3207b9b2ea44313634bd3494b930e2364a98f49bdd68ce87fd2896f646bd9d`.

| quantity | value |
|---|---|
| ledger entries | 591 |
| headings with at least one entry | 18/18 (0 missing) |
| union of `inputs` keys minus DROP | 7721 |
| of those, blobs at base | 7721 |
| absent at base (binder would skip) | 0 |
| ledger blob sha256 | `24dbe99a57880705313a8ddc05ddcdc05c57754903822912c0dbd7480499a5c7` |

DROP keys that do appear on these entries, and were subtracted (not in the file): `SKILL.md` on 57 entries, the round-21 ledger on 6, `LOG.md` on 5, `SCORECARD.md` on 5. Re-checked: none of the four remains in the union.

Prefix counts of the 7721: `.ufo` 7574 (evidence 5531, waves 2039), `corpus` 78, `tools` 33, `plans` 18, `reports` 9, `considerthese` 3, plus `.gitignore`, `AGENTS.md`, `MINT.md`, `PROVINCE.md`, `README.md`, `SHONEN.md`.

The width is one heading. `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence` has entries whose `inputs` are a near-tree snapshot (7705 keys at `read_rev=2da841bd9913`, trace `.ufo/evidence/round-31/coldread/traces/ColdB03-1-*.json`; 7706 at `651773ab9e32`, trace `rekey-r53-651773ab9e32/traces/section-04.json`; 7702 at `99c3bc88d704`, trace `rekey-r54-99c3bc88d704/traces/section-04.json`). That heading alone contributes 7702 keys; the other 17 headings contribute 2661; 5060 keys are exclusive to the mutation-sweep entries. The binder does not filter by entry age, so the re-key will re-pin all 7721 that still exist at PIN.

Per heading (entries / kept keys after DROP):

| heading | entries | kept |
|---|---:|---:|
| Context gate classification and explicit exit classes — round 15 | 20 | 42 |
| Effective expectation reconciliation — round 14 | 19 | 42 |
| Live-tree re-pin and entry-command monitor — round 17 | 22 | 78 |
| Mutation-sweep recipe — numbered steps; bounded cold-read evidence | 29 | 7702 |
| Pin disposition and provenance correction — round 13 | 25 | 33 |
| Repeated controls and gate registry — round 12 | 21 | 168 |
| Standing rules | 8 | 2497 |
| The leg ledger — replay, receipt, and how it is read (round 7, measured) | 11 | 30 |
| The operator's runbook and the six-leg regression (round 10, measured) | 16 | 11 |
| Gate/probe registry | 14 | 124 |
| Round-13 gate/probe registry | 22 | 24 |
| Round-15 gate/probe registry | 7 | 38 |
| Round-17 gate/probe registry — re-pin and monitor | 15 | 51 |
| Round-18 gate/probe registry — routed-defect closure | 20 | 71 |
| Round-21 gate/probe registry — finite environment differential | 17 | 75 |
| Round-26 gate/probe registry — report interop | 5 | 74 |
| The service's limits — what tameshi refuses to mutation-test | 12 | 39 |
| Triggers T1–T3 and the re-pin rule | 12 | 89 |

`## Standing rules` is wide for the same reason (2497 keys at `read_rev=01d586ddbc5f` and 2500 at the round-53 re-key `651773ab9e32`, trace `rekey-r53-651773ab9e32/traces/section-07.json`). Those keys are inside the mutation-sweep union except 19 keys that only the other headings pin.

Machine-readable classification: `.ufo/waves/round-56/w1/T56W1ScoutFreezeSet-receipts/pinned-set.json`.

## C2 content against the set
Checked the five paths C2's counter names (`.ufo/evidence/round-56/c2/measure.py:54-59`) plus `SKILL.md`.

| path | in the 7721 | blob at base | blob at freeze | headings that pin it |
|---|---|---|---|---|
| `corpus/QUALITY.md` | yes | yes | yes | 6 |
| `corpus/SOURCES.md` | yes | yes | yes | 13 |
| `tools/registry.json` | yes | yes | yes | 11 |
| `corpus/knowledge/receipt-revision-binding.md` | no | no | no | 0 |
| `tools/receipt-revision-gate.py` | no | no | yes (added at `c3e2ca9f`; base is its ancestor) | 0 |
| `SKILL.md` | no (DROP) | yes | yes | subtracted; 15 headings had pinned it |

QUALITY is pinned by Live-tree re-pin (r17), Mutation-sweep recipe, Standing rules, Round-18 registry, Round-21 registry, and Triggers T1-T3. All three in-set paths are also pinned by at least one heading other than the fat mutation-sweep entry, so dropping that entry would not free them.

## Ordering constraint
The binder stores `sha256` of each key at PIN and credit checks that digest at REV. History before PIN may change; PIN and REV may not, for any of the 7721.

These edits must land at or before C0 and must not be touched by any later commit (record, bind, or deciding):

- `corpus/QUALITY.md`
- `corpus/SOURCES.md`
- `tools/registry.json`

The wave-1 plan already schedules those three in the single content commit C0 (QUALITY criterion, SOURCES row, registry cell). That satisfies the constraint only if no commit after C0 edits them again.

These C2 paths are not in the set, so the pin does not force their bytes:

- `corpus/knowledge/receipt-revision-binding.md` is a new path. Creating it at C0 does not collide with a prior pin. A later edit of that new file does not fail `input-drift` on the re-key. The docs arm still needs the file present at REV; that is a different check.
- `tools/receipt-revision-gate.py` is not an input of any of the 18. It is a frozen instrument (present at `c3e2ca9f`, absent at base). The pin does not cover it; the freeze-byte check does. Do not treat a gate-body edit as a C0 content edit.
- `SKILL.md` is in DROP, so it is not in `pinned-inputs.txt`. Adjacent, not a member of this set: C1 arm 4 compares the reader's `section_sha256` to the section bytes at REV (`.ufo/evidence/round-56/c1/measure.py:25-29`). The `## Standing rules` edit therefore still has to be inside C0, and `SKILL.md` must not change between C0 and REV, or the reader arm fails even though the input pin ignores the file.

## Post-C0 plan check (round-55 failure mode)
No path in the 7721 is scheduled after C0 by the written plan. The record commits are `SCORECARD.md` and `LOG.md` (both DROP, safe), a new lesson, and a report skeleton.

What would repeat R55, if a later commit did it:

- Any byte change, after PIN, to `corpus/QUALITY.md`, `corpus/SOURCES.md`, `tools/registry.json`, or any other of the 7721. 7574 of those paths are under `.ufo`. The bind may add `rekey-r56-<c0>/` (new paths, not in the set) and may rewrite the ledger (DROP). It must not rewrite an existing pinned `.ufo` blob.
- Lessons in the set stop at round 30 (37 files). `corpus/lessons/round-31*` through `round-55*` are on disk and are not in the set (50 files). A new `round-56` lesson path is outside the set. Editing any round-1..30 lesson after C0 is a pin break.
- `reports/` in the set is only the nine old files `reports/r7-aud-t7.md`, `r8-aud-t8.md`, `r8-ver-t8.md`, `r9-aud-t9.md`, `r9-ver-t9.md`, `r10-aud-t10.md`, `r11-aud-t11.md`, `reports/round-1-calibration.md`, `reports/round-1-kaika-coldread.md`. A new report path is outside the set; editing those nine after C0 is not.

Flag: the plan as written does not edit a set member after C0. The failure mode is open, not currently scheduled. The three in-set C2 files are the ones that become a scheduled failure if their edits slip past C0.

## Confidence
High for the set and the three collisions. The formula is the binder's, every heading matched, every kept key is a blob at base, and the txt file's line count, uniqueness, sort, and sha256 were re-measured after the write.

Unresolved: which commit the L1 will pass as PIN (C0 itself, or a later commit that must then contain only DROP-key and new-path changes). The safe reading of this constraint is that no path in `pinned-inputs.txt` changes after C0.

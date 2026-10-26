# T49Read10 — C1 reader, section `### The map`, pointer ordinals 0–5

Round 49 (hyaku run 9), wave 1. Base `8ca67421111fa354b47b803358391d0b07fc6db9`. Reader on the
section `### The map — where a reader enters, artifact by artifact` (`SKILL.md:1380`), the rows whose
ordinal is 0–5 of the frozen extractor output. Six pointers read; this is a read report, not a verdict
on C1.

Deliverable: `.ufo/waves/round-49/w1/T49Read10.rows.json` (`{"rows":[...]}`, 6 rows, `reader` =
`T49Read10`). Receipts: `.ufo/waves/round-49/w1/T49Read10.measure-list.json` (counter `--list` output at
base), `.ufo/waves/round-49/w1/T49Read10.fix-sim.txt` (extractor simulation of the two proposed fixes).

## Method and commands (all read-only, at base)

- `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 8ca67421111fa354b47b803358391d0b07fc6db9:SKILL.md`
  (base SKILL.md is 2136 newlines; `wc -l`) and the same form for every target.
- `python3 .ufo/evidence/round-49/c1/measure.py --lane . --rev 8ca67421111fa354b47b803358391d0b07fc6db9 --list`
  → rc 0, `90` pointers total, `17` under `### The map` (map floor is 17; no pointer added or removed by
  this report). Full output saved at `T49Read10.measure-list.json`.
- Row construction and self-check in Python (scratch):
  claim asserted to be a verbatim substring of the row's `skill_line`; excerpt collapsed with the
  counter's own rule (`re.sub(r'\s+', ' ', t).strip()`, `measure.py:202-203`) and asserted to occur in the
  collapsed pointed text (line ranges via `pointed_text`, `measure.py:206-208`; whole blob for path
  pointers), length asserted `24 <= len <= 400` (`measure.py:81`).
- Extractor simulation for the two proposed edits: the frozen `extract()` called on the section text
  before and after the replacement (`T49Read10.fix-sim.txt`).
- No counter `measure` run was made (deciding run is the L1's); no model installed; no pacman call; no
  writes outside `.ufo/waves/round-49/w1/` and scratch `/fast/scratch/hyaku/tameshi-r49/T49Read10/`
  (deleted before yield). Nothing under `/home/vgpnk/.local/state/` was read.

## Results — pointer by pointer

| ord | raw | skill_line | target | verdict |
|---|---|---|---|---|
| 0 | `:1294-1297` | 1384 | SKILL.md itself | **unresolved** (target text supports the clause; pointer has no file) |
| 1 | `:1246-1270` | 1386 | SKILL.md itself | **unresolved** (same missing-qualifier defect) |
| 2 | `LOG.md:316-317` | 1393 | LOG.md:316-317 | **holds** |
| 3 | `corpus/knowledge/operator-runbook.md` | 1384 | whole file | **holds** |
| 4 | `corpus/knowledge/fleet-kill-rate-ledger.md` | 1385 | whole file | **holds** |
| 5 | `corpus/knowledge/service-limits.md` | 1386 | whole file | **holds** |

Tally in my set: 4 holds, 2 unresolved, 0 stale, 0 absent.

### ordinal 0 — `:1294-1297`, the "anchored source governs" clause (`SKILL.md:1384`)

- Clause: "where it and an anchored source diverge, the anchored source governs".
- Target: the page itself. The document's own anchor convention makes a bare `:N` mean SKILL.md —
  `SKILL.md:1250` ("Anchors `:…` are this page; `PROVINCE.md` is repo-relative; other bare note names are
  under `corpus/knowledge/`"). Command: `git show 8ca67421:SKILL.md | sed -n '1250p'`.
- Pointed text `SKILL.md:1294-1296` contains the clause verbatim: "Pointer, not a second home. Its own
  rule: where it and an anchored source diverge, the anchored source governs — the same
  rendering/divergence rule this page applies to `service-limits.md` (`:1250-1254`)." Command:
  `git show 8ca67421:SKILL.md | sed -n '1294,1296p'`. Line 1297 begins the next bullet, so the range is
  one line wide, not drifted.
- Verdict **unresolved**, and the reason is mechanical, not semantic: `check_reads` sets
  `status = 'unresolved'` for every pointer whose `file` is null, before any read row is consulted
  (`.ufo/evidence/round-49/c1/measure.py:271-279`), and `--list` records `file: null` for this ordinal
  (`T49Read10.measure-list.json`). The clause holds; the pointer cannot resolve as written.
- Correction: qualify the pointer — `the anchored source governs (`:1294-1297`)` →
  `the anchored source governs (`SKILL.md:1294-1297`)`. `skill_old` occurs once in SKILL.md (checked with
  `str.count` on the base blob). Simulation: the extractor still yields 17 pointers, ordinals unchanged,
  the raw becomes `SKILL.md:1294-1297` with `token = SKILL.md`, ranges `[[1294,1297]]`, and
  `git cat-file -t 8ca67421:SKILL.md` prints `blob`, so `resolve()` (`measure.py:171-194`) will return
  `SKILL.md` (`T49Read10.fix-sim.txt`).

### ordinal 1 — `:1246-1270`, "this page carries the compact rendering" (`SKILL.md:1386`)

- Clause: "this page carries the compact rendering". In the row the subject is `service-limits.md`; the
  bare pointer's "this page" is SKILL.md, and the pointed text says exactly that: `SKILL.md:1253-1254`
  "and the intake-precondition check; this page is the compact rendering, and a divergence between the
  two is the finding, never smoothed." Command: `git show 8ca67421:SKILL.md | sed -n '1246,1270p'`
  shows the section `### The service's limits — what tameshi refuses to mutation-test` (`:1246`) with
  the refusal table (rows a–j, `:1258-1267`).
- Verdict **unresolved**, same file-null cause (`measure.py:271-279`; `--list` ordinal 1,
  `file: null`). The numbers `1246-1270` are correct at base; only the qualifier is missing.
- Correction: `this page carries the compact rendering (`:1246-1270`)` →
  `this page carries the compact rendering (`SKILL.md:1246-1270`)`; occurs once in SKILL.md; simulation
  keeps 17 pointers and the same ordinals (`T49Read10.fix-sim.txt`).
- Target-internal observation (bears on ord 5, not on this row's text): `corpus/knowledge/service-limits.md:10-11`
  cites the compact rendering as `SKILL.md:1230-1249`. At base, 1230-1249 is the round-9 section's re-pin
  tail plus only the limits heading and two intro lines (1246-1249); the table body is 1256-1267.
  Command: `git show 8ca67421:SKILL.md | sed -n '1226,1250p'` and
  `git show 8ca67421:corpus/knowledge/service-limits.md | sed -n '10,11p'`. That inner anchor has drifted
  by the page's growth. The map row's `:1246-1270` is the correct rendering.

### ordinal 2 — `LOG.md:316-317`, "no separate round-11 record file exists" (`SKILL.md:1393`)

- Pointed lines: 316 `… the lane deliverables in` / 317 `this repo ARE the wave record (no
  `.ufo/waves/tameshi-r11-*` directory);`. Command: `git show 8ca67421:LOG.md | sed -n '316,317p'`.
  LOG.md is 2382 lines at base, so the range is in bounds (`measure.py:293-296` cannot fire).
- Existence claim checked independently: `git ls-tree -r --name-only 8ca67421 | grep -i round-11` returns
  only `plans/round-11.plan.md` — no `plans/round-11-record-draft.md` and no r11 wave directory. The
  clause is true at base and the pointed lines are where it is stated. Verdict **holds**.

### ordinal 3 — `corpus/knowledge/operator-runbook.md` (`SKILL.md:1384`)

- Clause names the runbook as the operator's entry point (T10-1) and lists its sections. File read whole
  (517 lines, `git show 8ca67421:corpus/knowledge/operator-runbook.md | wc -l`).
- Title `:1` — "Operator runbook — the tameshi mutation service, end to end (round 10, T10-1)". Role
  `:3-6` — "the mutation service's single operator-facing document — **the tool, the six-case ledger, the
  opt-in protocol, the limits, the cadence (the tick), and the regression mode**".
- Every named section exists under the named number: §0 Quick start `:35` · §2 The tool `:93` · §3 The
  six-case ledger `:131` · §4 The opt-in protocol `:180` · §5 The limits `:243` · §6 The cadence — the
  tick, the reading map, the triggers `:269`, with T1 `:288`, T2 `:290`, T3 `:293` · §7 The regression mode
  `:345` · §10 Unknowns carried `:462`. Command: `git show 8ca67421:corpus/knowledge/operator-runbook.md |
  grep -n '^## '`. Verdict **holds**.

### ordinal 4 — `corpus/knowledge/fleet-kill-rate-ledger.md` (`SKILL.md:1385`)

- Clause: one row per gate with suite, rate + composition, survivors, last sweep + pin; §1–§4 frozen,
  new rows appended below. File read whole.
- Role `:4-5` verbatim: "**one row per gate — suite size, kill-rate, survivor classes, hardened-or-not,
  last-sweep date + pin**". Compositions: §0 "**Kill-rate** … **composition-bound** … Composition is
  stated beside every rate" (`:26-30`, `git show 8ca67421:corpus/knowledge/fleet-kill-rate-ledger.md |
  sed -n '26,30p'`). Sections: §1 `:41`, §2 `:90`, §3 `:98`, §4 `:132` (`grep -n '^## '`).
- Frozen/append: `:312` "the outcome lands **as an appended row or errata block in this ledger** — never
  as an edit of §1–§4"; `:318` "No §1–§4 cell is edited"; the appended blocks say so themselves (ER-2
  `:272`, ER-5 `:366`, Round 16 `:403`, Round 18 `:424`). ER-5 is a disposition receipt, not an edit of
  the measured tables. Verdict **holds**.

### ordinal 5 — `corpus/knowledge/service-limits.md` (`SKILL.md:1386`)

- Clause: "the refusals, detail of record". File read whole.
- Role `:4-5` — "the **refusal table the re-sweep cadence applies at intake**"; `:12` — "this note is the
  detail of record, with the verbatim anchors behind each row"; §1 `## 1. The decision table` (refusals
  a–j), §2 `## 2. Row detail — the measured reasons, verbatim`. Command:
  `git show 8ca67421:corpus/knowledge/service-limits.md | sed -n '1,14p;40,45p'`. Verdict **holds** —
  the row's two halves (refusals; detail of record) are both stated in the target.
- Its own `:11` reference `:1155` resolves to the round-9 section heading at `SKILL.md:1155` (correct);
  `SKILL.md:1230-1249` on the same line has drifted (see ordinal 1's observation).

## Proposed corrections (both pointers, no pointer deleted)

```json
{"skill_old": "the anchored source governs (`:1294-1297`)",
 "skill_new": "the anchored source governs (`SKILL.md:1294-1297`)",
 "fixed_file": "SKILL.md", "fixed_ranges": [[1294, 1297]],
 "fixed_excerpt": "where it and an anchored source diverge, the anchored source governs — the same rendering/divergence rule this page applies to `service-limits.md` (`:1250-1254`)."}
{"skill_old": "this page carries the compact rendering (`:1246-1270`)",
 "skill_new": "this page carries the compact rendering (`SKILL.md:1246-1270`)",
 "fixed_file": "SKILL.md", "fixed_ranges": [[1246, 1270]],
 "fixed_excerpt": "this page is the compact rendering, and a divergence between the two is the finding, never smoothed."}
```

Both `skill_old` strings occur exactly once in base SKILL.md (global `str.count` = 1), so an
L1 replacement cannot hit a second site. Both replacements are themselves line-count neutral (the edited lines are 1384 and 1386, and both
targets 1246-1270 / 1294-1297 lie above them). Integration caveat: the recipe section (`SKILL.md:131`) and
restore-discipline section (`SKILL.md:375`) sit *above* 1246-1297, so if the L1's corrections to either
change their line count, the two numbers here must be re-resolved against the corrected text before the
rows are written — the numbers below are true at base and at a map-only edit, not after an upstream
section grows or shrinks. With the section edit alone the extractor re-derives the same 17 pointers with
the same ordinals (`T49Read10.fix-sim.txt`), so
the map floor (17) is untouched, and the rows the L1 re-derives must carry the new `raw`
(`SKILL.md:1294-1297`, `SKILL.md:1246-1270`) — a read row keyed to the old bare raw will match nothing
(`check_reads` indexes on `(heading, ordinal, raw)`, `measure.py:262`).

## Reads-assembly note (peer finding, verified here)

Seat `T49Read07-5` flagged that the counter consumes `row['verdict']`, not `row['base_verdict']`
(`.ufo/evidence/round-49/c1/measure.py:304`, `elif row.get('verdict') != 'holds': status = 'not_holds'`).
Verified against the source and against how a row is matched:

- matching is on `(heading, ordinal, raw)` then on `file`/`ranges` (`measure.py:262`, `:302`);
- a row that matches but carries only `base_verdict` reaches `:304` and scores `not_holds`;
- the two file-null pointers never reach `:304`: `status = 'unresolved'` is set at `:271-279` first.

So a **verbatim** copy of `T49Read10.rows.json` into `reads.json` gives, at row level, `unresolved` for
ordinals 0-1 and `not_holds` for ordinals 2-5 (peer `T49Read07-5` measured the same split, recorded in
`.ufo/waves/round-49/w1/T49Read07.counter-probe.txt`, and reports it in `T49Read07.md` F2). Note the
counter's `unresolved` figure is a pointer-level count that no read row can move: with an empty row list
it is still 9 (8 file-null pointers across the seven sections plus the external `../PROTOCOL.md:63-68` at
promotion-evidence ordinal 0, which needs a `fleet_commit` no row supplies — `measure.py:271-279`,
`:280-283`). So "2 unresolved rows" here is my rows' status, never a delta in that total. This
deliverable keeps `base_verdict` because that is the seat spec; the L1's assembly must:

1. map `base_verdict` → `verdict` for ordinals 2-5 (`holds`);
2. drop the base-raw rows for ordinals 0-1 and write them at the corrected raw
   (`SKILL.md:1294-1297`, `SKILL.md:1246-1270`) with `file: "SKILL.md"`, the same ranges, the excerpt
   above and `verdict: "holds"` — the excerpt is located at those lines, so the row verifies
   (`measure.py:304-315`).

## Limits of this read

- I judged support against the pointed text only; I did not re-verify the truth of third-order claims
  those artifacts make about each other beyond the two inner anchors named above.
- The verdict for ordinals 0 and 1 is about resolvability under the frozen counter, not about the
  sentence being wrong: the text at `SKILL.md:1294-1296` / `SKILL.md:1253-1254` supports the clause. If
  the L1 instead leaves a bare pointer in place, `check_reads` will still count it unresolved
  (`measure.py:271-279`).
- Nothing here is a verdict on C1; the deciding run at REV is the L1's.

## Summary

1. Six pointers read at base; 4 `holds` (LOG.md:316-317, operator-runbook, kill-rate-ledger, service-limits), 2 `unresolved` (`:1294-1297`, `:1246-1270`), 0 stale, 0 absent.
2. The two unresolved pointers are bare `:N` self-references; their targets (SKILL.md:1294-1296, 1253-1254) do support their clauses — the defect is the missing file qualifier.
3. Frozen counter proof: `measure.py:271-279` marks every `file: null` pointer unresolved; `--list` shows `file: null` for ordinals 0-1 (90 pointers total, 17 in this section).
4. Fix: prefix `SKILL.md:` on both; each old string is unique in base SKILL.md; the map edit moves no lines, but the recipe (131) and restore (375) sections sit above 1246-1297, so re-resolve those two numbers after upstream edits.
5. Extractor simulation (`T49Read10.fix-sim.txt`): 17 pointers before and after, ordinals identical, only the two raws change; `SKILL.md` is a blob at base so `resolve()` returns it.
6. Side finding: `corpus/knowledge/service-limits.md:10-11` still cites the compact rendering as `SKILL.md:1230-1249`, which at base covers only heading+intro (table body is 1256-1267) — the map's `:1246-1270` is the correct range.
7. Deliverable `.ufo/waves/round-49/w1/T49Read10.rows.json` written and self-checked with the counter's collapse/excerpt rule (all excerpts 77-245 chars, all located in pointed text).
8. Reads assembly: `check_reads` reads `verdict` (`measure.py:304`) while this file carries `base_verdict`; a verbatim copy leaves ords 0-1 unresolved and 2-5 not_holds (the counter's unresolved total is pointer-level, 9) — the L1 must map/re-key. No installs, no counter `measure`, scratch deleted.

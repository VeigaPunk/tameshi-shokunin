# T49Read12 — C1 reader, `### The map`, pointer ordinals 12–16

Seat: T49Read12 (C1 reads). Lane `tameshi-shokunin`. Base `8ca67421111fa354b47b803358391d0b07fc6db9`.
Scope: the five rows of `.ufo/evidence/round-49/control/c1-pointers-at-base-8ca67421.json` whose heading is
`### The map — where a reader enters, artifact by artifact` and whose ordinal is 12–16.
Read-only on the lane: the only file this seat created is `.ufo/waves/round-49/w1/T49Read12.rows.json` (plus this report).

## Verdicts

| ord | raw | kind | verdict | one-line reasoning |
|---|---|---|---|---|
| 12 | `plans/round-N-record-draft.md` | path | **absent** | A convention token, not a held path: no blob at that literal name (`cat-file -t` → fatal); the clause holds for the concrete round-4…10 record drafts. |
| 13 | `corpus/knowledge/closeout-r11.md` | path | **holds** | The closeout note exists and itself says it is "not … the round record"; the plans tree holds no round-11 record file, so the row's assertion is supported. |
| 14 | `plans/completion-evidence.md` | path | **holds** | The pack states "One line per round …, the SHONEN status, and the debts" at :3-10 and delivers both (`## One line per round` :27-40, `## Debts` :68-134). |
| 15 | `LOG.md` | path | **holds** | LOG.md carries one entry per round (12 dated round bullets for rounds 0–11, four round-43/44 bullets, one heading per later round up to 48) — "the round rows" is loose wording, not a wrong target. |
| 16 | `SCORECARD.md` | path | **holds** | `## Move log` at :7 with header at :9 and rows :11-24; rows :11-16 carry counting commands in the Evidence column (excerpt = row 1). |

Frozen-check receipt (the counter's own `check_reads`, restricted to these five pointers):
`{'unresolved': 0, 'unverified': 0, 'excerpt_miss': 0, 'not_holds': 0, 'absent': 1}` — 12 → `absent`, 13/14/15/16 → `ok`.

## Pointer-by-pointer

### ordinal 12 — `plans/round-N-record-draft.md` → absent

Supported clause (SKILL.md:1393): "each round's plan and record by convention (rounds 4–10)".

- The literal token has no blob: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin cat-file -t 8ca67421111fa354b47b803358391d0b07fc6db9:plans/round-N-record-draft.md` → `fatal: path 'plans/round-N-record-draft.md' does not exist in '8ca67421111fa354b47b803358391d0b07fc6db9'`.
- `git -C … ls-tree --name-only 8ca67421111fa354b47b803358391d0b07fc6db9:plans` → `completion-evidence.md, round-10-record-draft.md, round-10.plan.md, round-11.plan.md, round-2.plan.md, round-3.plan.md, round-4.plan.md, round-4-record-draft.md … round-9.plan.md, round-9-record-draft.md` — no `round-N*` file; `N` is a placeholder.
- The clause itself is true of the concrete files: `git -C … cat-file -t 8ca67421111fa354b47b803358391d0b07fc6db9:plans/round-4-record-draft.md` (likewise round-7, round-10) → `blob`.
- `absent` is the frozen counter's sanctioned route: an unresolvable path pointer passes only with a row whose verdict is `absent` and `file` null (`tameshi-shokunin/.ufo/evidence/round-49/c1/measure.py:271-278`), and the round's own control harness writes exactly that shape (`tameshi-shokunin/.ufo/evidence/round-49/control/c1-controls.py:123`).
- No excerpt is possible (the pointed text does not exist) and the absent branch reads none. The pointer cannot be deleted: map floor 17 (`tameshi-shokunin/.ufo/evidence/round-49/c1/measure.py:79`).
- Correction for the L1's mental model: the CTL_K2 "two bare map pointers" are **ordinals 0 and 1** (bare line pointers `(`:1294-1297`)` and `(`:1246-1270`)`, `file` null, kind line, no absent carve-out; see `tameshi-shokunin/.ufo/evidence/round-49/control/c1-controls.py:160-162`), **not** this path token. Ordinals 11 and 12 are the two unresolvable *path* tokens that the absent branch covers. [INFERENCE from reading those lines, not scored here.]

Proposed fix (row `proposed_fix`, a clarification only, no counter effect): make the placeholder explicit in the Holds cell —
`… by convention (rounds 4–10; `N` is a placeholder, not a file — the concrete files are the round-4 through round-10 plan and record-draft pairs that `plans/` holds);`
`skill_old` occurs exactly once in the base section and the edit names no new file token, so the extractor's pointer set is unchanged: `c1.extract` on the edited section returns the same 17 pointers in the same order, ordinal 12 raw still `plans/round-N-record-draft.md`, kind path, file null (`skill_old occurrences in section: 1`, `pointers base/new: 17 17 identical: True`, `new tokens introduced: []` — probe run over the base blob with the frozen `extract`).

### ordinal 13 — `corpus/knowledge/closeout-r11.md` → holds

Supported clause (SKILL.md:1393): "no separate round-11 record file exists (the wave deliverables are the record, `LOG.md:316-317`; closeout note `corpus/knowledge/closeout-r11.md`)".

- The file resolves and is the closeout note: `git -C … show 8ca67421111fa354b47b803358391d0b07fc6db9:corpus/knowledge/closeout-r11.md | sed -n '1p'` → `# The arc's closeout — the service as it stands (T11-1, round 11)`.
- It supports the row's assertion at `corpus/knowledge/closeout-r11.md:34-40` (the excerpt): "**What this file is not.** Not the tick's receipt and not the round record: the round-11 execution (the pre-announced tick, the schedule, the 10-of-10 record) lands in the round's own documents"; `:39-40` names it "the corpus-side closeout".
- Independent corroboration at base: `git -C … ls-tree -r --name-only 8ca67421111fa354b47b803358391d0b07fc6db9 | grep -E 'r11|round-11'` → `plans/round-11.plan.md`, `reports/r11-aud-t11.md`, `corpus/knowledge/closeout-r11.md` (plus two cold-read trace fixtures under `.ufo/evidence/round-17|18/…/*plan-r11*`) — a plan, an audit, this closeout note, no record file; record drafts exist only for rounds 4–10 (`ls-tree …:plans` receipt above).
- Path pointer → no line ranges to drift.
- Disclosed qualification, not a defect: the note is a 2026-10-14 write whose §6 pins and some observations (e.g. `closeout-r11.md:225-226` "9 rows covering 6 of 16 knowledge notes") are historical; the row cites it as the closeout note, which it is.

### ordinal 14 — `plans/completion-evidence.md` → holds

Supported clause (SKILL.md:1393): "the completion pack (`plans/completion-evidence.md`, this wave, uncommitted at this write) collects the per-round lines and debts".

- 189 lines at base: `git -C … show 8ca67421111fa354b47b803358391d0b07fc6db9:plans/completion-evidence.md | wc -l` → `189`.
- Contents it promises and delivers: header statement at `plans/completion-evidence.md:3-10` (the excerpt, "One line per round (round · axis · headline · commit hash · verifier names), the SHONEN status, and the debts."); `## One line per round` at `:27` with table header `:29-30` and one row per round `:31-40` (rounds 2–11); `## Debts` at `:68` through `:134`.
- Disclosed qualification: the `## Fleet round-1 correction — 2026-10-15` block at `plans/completion-evidence.md:158-174` supersedes the SHONEN-status *interpretation* at `:44-59` ("TAMESHI-B1/B2/B3/B4 remain historical run lineage, not independent promotion authority") but leaves the per-round lines and the debts the row promises intact.
- The parenthetical "(this wave, uncommitted at this write)" is a statement about the round-11 write, not about base; at base the file is committed and its role is unchanged.
- Path pointer → no line drift.

### ordinal 15 — `LOG.md` → holds (wording caveat recorded)

Supported clause (SKILL.md:1394): "the round rows".

- LOG.md is 2381 lines at base and carries one entry per round: 12 dated round bullets for rounds 0–11 at `LOG.md:3,5,68,173,303,304,305,306,307,308,309,310` (`git -C … show <base>:LOG.md | grep -nE '^- [0-9]{4}-[0-9]{2}-[0-9]{2} — round '`), four further round-43/44 bullets at `:2221,2261,2265,2272` (16 bullets by `grep -cE`), and one heading per later round from `LOG.md:655` (`## Round 12 — …`) to `LOG.md:2370` (`## 2026-10-26 — round 48, attempt 3 …`).
- The excerpt is the round-11 entry, `LOG.md:310-313` (`git -C … show <base>:LOG.md | sed -n '310,313p'`).
- Caveat, recorded rather than hidden: LOG.md has no `| Round |` table (`git -C … show <base>:LOG.md | grep -n '^| Round'` → no match), so the cell's word "rows" names per-round entries rather than table rows. That is a looseness of the Holds cell, not pointer staleness: the target exists and is where "provenance of any round" lives. Because this is a path pointer there are no line numbers to drift.
- Not softened into a defect because the verdict vocabulary is about the pointer/target relation ("the target exists but does not support the clause, or the line numbers drifted" — `.ufo/waves/round-49/build-spec.py:47`): the target does support the clause as written.

### ordinal 16 — `SCORECARD.md` → holds (scope note recorded)

Supported clause (SKILL.md:1394): "the move-log rows with their counting commands".

- `git -C … show <base>:SCORECARD.md | sed -n '7,10p'` → `## Move log` (:7), blank, `| Round | Axis | Before | After | Evidence |` (:9), `|---|---|---|---|---|` (:10); rows at `:11-24`.
- The excerpt is the round-1 depth row (`SCORECARD.md:11`) including its Evidence cell's counting commands: `` `git show 40f8e1f:SKILL.md \| wc -l` → 22; `` (the full row, 362 collapsed chars).
- Scope note, not a defect: the command strings sit in rows `:11-16` (rounds 1–3); rows `:17-24` (rounds 4–11) put `wave-N 32-lane; VER-…` in that column instead (`git -C … show <base>:SCORECARD.md | sed -n '17,18p'`), and the file's own `SCORECARD.md:5` says axes "will be pinned with their counting commands as rounds land". So "with their counting commands" is exact for the early rows and describes the column's contract for the rest.
- Path pointer → no line drift.

## Gates run (probes, not verdicts)

1. `python3 .ufo/evidence/round-49/c1/measure.py --lane . --rev 8ca67421111fa354b47b803358391d0b07fc6db9 --list` → `total pointers 90` (matches the contract's base census `pointers=90`); ordinals 12–16 print exactly the raws/files/kinds/ranges/skill_lines copied into my rows.
2. Frozen `check_reads` over only these five pointers, with my rows document → `{'unresolved': 0, 'unverified': 0, 'excerpt_miss': 0, 'not_holds': 0, 'absent': 1}`; detail `12 absent, 13 ok, 14 ok, 15 ok, 16 ok`.
3. Excerpt validator using the counter's own `norm()` / `pointed_text()`: collapsed lengths 193, 110, 167, 362; each `24<=len<=400` and each occurs in the collapsed pointed text (`True`). Row 12 has no excerpt (absent branch).
4. Extractor-invariance probe for the single proposed fix (row 12): `skill_old` count in the base section `1`; pointer tuples base vs edited `17 17 identical: True`; `new tokens introduced: []`.

The counter was **not** run in deciding mode; nothing here is a verdict. No `--selftest` was needed (no change to the counter).

## Touched surfaces / bounds

- Created: `.ufo/waves/round-49/w1/T49Read12.rows.json`, `.ufo/waves/round-49/w1/T49Read12.md`.
- Read only: lane blobs at base via `git show`/`git cat-file`/`git ls-tree`, plus the round-49 contract, frozen counter, control harness and wave spec.
- Not touched: lane checkout files, `contract.json`, counters, controls, Git index/jj state, the fleet repo, sibling lanes, `shokuknow`, anything under `~/.local/state/`, `~/.local/bin` or other PATH dirs, `LOG.md`/`SCORECARD.md`/`MANIFEST.json` at the fleet root.
- Scratch: none created — no clone, worktree or fixture was needed (all rules and blobs read through `git -C … show <rev>:<path>`), so there is nothing to delete. `TMPDIR` was not used.
- Tooling: nothing installed or upgraded; no pacman transaction attempted.
- No claim was decided; no control was scored; no model was passed.

## Findings handed to the L1

1. Slice result: 4 `holds`, 1 `absent`, 0 `stale`, 0 `unresolved` — every path pointer in this slice resolves, so no line-drift repair is possible here (path pointers carry no ranges).
2. `plans/round-N-record-draft.md` (ordinal 12) must be integrated as `verdict: "absent"`, `file: null` — the frozen carve-out at `.ufo/evidence/round-49/c1/measure.py:271-278`. The mechanical control row generator produces the same shape (`.ufo/evidence/round-49/control/c1-controls.py:123`).
3. Ordinal 11 (`plans/round-N.plan.md`, not my slice) is the same class as 12 and needs the same absent row; the CTL_K2 prefix trick concerns ordinals 0 and 1 only (`.ufo/evidence/round-49/control/c1-controls.py:160-162`) — a prefix edit aimed at 11/12 would be the wrong fix.
4. Wording risks for wave 2, disclosed above rather than pre-fixed: "the round rows" (LOG.md has per-round entries, no table) and "with their counting commands" (SCORECARD's later move-log rows carry wave/verifier labels). If the L1 wants them tightened, the safe edit is inside the Holds cell only — it adds no pointer token if no `*.md`/`*.py`/`*.sh`/… filename is introduced; the extractor-invariance probe above is the pattern to re-run after any such edit.
5. `closeout-r11.md` and `completion-evidence.md` are 2026-10-14/15 writes with later correction blocks; the map rows cite them for artifact identity, not for current state, so the citations survive.

## Summary

- Five pointers read at base `8ca67421` in `### The map`: ordinals 12–16.
- 4 `holds` (`closeout-r11.md`, `plans/completion-evidence.md`, `LOG.md`, `SCORECARD.md`), 1 `absent` (`plans/round-N-record-draft.md`), 0 `stale`, 0 `unresolved`.
- Frozen `check_reads` on these five: unresolved 0 · unverified 0 · excerpt_miss 0 · not_holds 0 · absent 1.
- Excerpts validated with the counter's own `norm`/`pointed_text`: 193/110/167/362 collapsed chars, all found in the pointed text.
- `--list` shows 90 pointers at base, matching the contract census; ordinals 12–16 match the pointer file exactly.
- One proposed fix (ordinal 12, clarification only): `skill_old` occurs once, extractor output identical (17 → 17 pointers, no new tokens).
- Two wording risks disclosed for wave 2 (LOG.md "rows", SCORECARD "counting commands"), not pre-fixed.
- Bounds respected: two files under `.ufo/waves/round-49/w1/`, no lane/repo mutation, no scratch, no tool installs.

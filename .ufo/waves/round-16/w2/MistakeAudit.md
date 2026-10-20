# MistakeAudit — round 16 wave 2 — attack on `corpus/lessons/round-16.md` `## Mistakes` at `c699c8c`

**Verdict: partial.** All four rows use words from the CORPUS vocabulary, and every evidence pointer
I replayed resolves. Three problems remain. (1) Two "Captured-by" cells name the seat that found the
mistake, not the rule that should have caught it. (2) The row-2 fix and the row-4 fix are not shown
able to fail. (3) The lesson leaves out the largest mistake in the landing commit: C2 is claimed and
SHONEN box 3 links to a cold-read ledger, but that ledger was never committed. At `c699c8c` the
committed counting command prints `calibration_restraint_score: 6`, not 8.

Seat: `TameshiR16.MistakeAudit` · critic · lane commit `c699c8c36d6e4eca4b796b81a8247904aa145ec8`.
Scratch: `/tmp/tameshi-r16w2-MistakeAudit-FpxXcI` (`git archive c699c8c`, a `--depth 1` clone of the
fleet repo as a misroot mirror, mutant copies). No lane writes other than this report. No installs
or updates. One blocker message was sent to `agent://TameshiR16` (O1 below).

Contract checked against: `/home/vgpnk/Projects/shokunin/CORPUS.md:171-184` (row shape: class ·
evidence pointer · captured-by = "the `QUALITY.md` criterion or protocol rule that should have caught it,
or `none`" · fix; and "a fix is shown able to fail before it counts"). Class meanings come from
`.ufo/waves/kaika-w1/mistakes.md:77-91` (C01–C13) and `:447-449` (the 9-word vocabulary).

---

## A. Row-by-row attack

| Row | Class in vocab? | Pointers resolve? | Captured-by honest? | Fix shown able to fail? |
|---|---|---|---|---|
| 1 attribution (verify.py first-`id=`) | yes (fit loose, see A1) | **yes** | yes (`none` + reason) | **yes** for the 2 usage rows; see A1 |
| 2 attribution (AttrFix draft rule) | yes | yes; the regex quote is garbled | **no**: names a seat | **partly**: 3 of the 4 claimed rule components survive mutation |
| 3 landing (round-15 misroot) | yes (C09/C10 boundary) | **yes** | yes (`none`) | **yes**: replayed rc 1 / rc 0 |
| 4 scope (runner edited in place) | in vocab, **wrong meaning** | yes | **no**: names a seat | **no**: procedural only; it **recurred in wave 2** (O3) |

### A1 — Row 1 (holds)

- `verify.py:207-210` resolves at `c699c8c:.ufo/evidence/round-15/verify.py`:
  `:207 if observed_id is None:` / `:208 token = ID_TOKEN_RE.search(stdout) or ID_TOKEN_RE.search(stderr)` /
  `:209-210` assign. `ID_TOKEN_RE` is at `:136-138`. The line is `:207` at `b255055` and `:208` at
  `7650fe4`; at `c699c8c` it reads `:208`, and the cited range `207-210` covers it.
- `round-15-verifier-spotcheck.md:160` is Routed defect 2, word for word as cited.
- Receipt identity: `sha256sum .ufo/evidence/round-15/verification-3.json` →
  `3c419055723319f50611eb7d2fa3de46e4d4c37fb405267609eee80aecc7d8ce`, which matches `3c419055…d8ce`.
- Rows `usage-proof-new` and `gate-usage` have `observed_exit 64`, `expected_id None` and
  `observed_id context_consistent` in both `verification-3.json` and `verification.json`.
  `verification-2.json` has 0 command rows, so the lesson is right to name only attempt 1.
- `python3 .ufo/evidence/round-16/attribution/reattribute.py --selftest` → **exit 0**:
  `usage-proof-new … old='context_consistent' FAIL new='usage_error' PASS`,
  `gate-usage … FAIL … PASS`, `usage-proof-old … PASS … PASS`, `forged-first-line … FAIL … PASS`,
  `SELFTEST: PASS (new rule 4/4; old rule fails 3/4; same fixtures and oracles)`. This matches the row.
- Correction mode in a /tmp copy regenerates `correction.json` **byte-identical** to the committed
  file. Output: `corrections: usage-proof-new context_consistent->usage_error, gate-usage
  context_consistent->usage_error` / `old rule reproduced every recorded observed_id (14 command rows)`.
  "Names exactly the two rows" holds.
- Class fit is loose. `attribution` is C10 *write-scope / attribution violation* (who wrote where).
  The defect here is a finding-ID field that was never oracle-compared. That is the C04 `vacuous`
  shape, and `correction.json` says so in its own `notes`: "their recorded observed_id was never
  oracle-compared". MistakeScribe (`w1/MistakeScribe.md:73`) proposed `vacuous` as a secondary class.
  Its draft criterion 18 also required "a null `expected_id` on such a row is not a pass". Landed
  QUALITY 18 (`corpus/QUALITY.md:88-96`) dropped that half, and `verify.py` still does not assert
  `observed_id` when `expected_id` is null. The lesson does not mention this vacuous residual. *(gap-minor)*
- Stale fix artifact: the docstring of `reattribute.py`, printed by `--help`, lines 19-22 and 29-32,
  still describes the **rejected** G8 rule (`^[A-Z_]+: [A-Z_]+ \(id=([a-z_]+) exit=(\d+)\)$`,
  stderr-first) and "replays one fixture". The code (`:99-133`, `:256-294`) implements the repaired
  rule with 4 fixtures. The comment at `:53-56` cites `verify.py:196-210`; at `c699c8c` that block is
  `:196-210` only loosely (it starts at `:194`). This is `reference-drift` inside the fix itself. *(gap-minor)*

### A2 — Row 2 (falls in part)

- Brief pointer: the `dispatch1.json` task `AttrFix` carries
  `^[A-Z_]+: [A-Z_]+ \(id=([a-z_]+) exit=(\d+)\)$`. Gate row G8 quotes it correctly
  (`\(id=… exit=…\)$`). The Mistakes row quotes it as `\(id=…\) exit=…\)$`, with a spurious `\)`.
  The row mis-transcribes its own evidence. *(reference-drift, minor)*
- `w1/AttrCritic.md:66` shows the draft rule nulls a real verdict:
  `CONTEXT: INVALID (id=expected_missing … exit=2 findings=1)` → spec NEW **None**. `:86` says F1 was
  "falsified as written". The pointer holds.
- **Captured-by misuse.** `AttrCritic (same-wave falsifier)` is the seat that found the mistake. It is
  not a QUALITY criterion or protocol rule (`CORPUS.md:172-173`). The honest cell is `none`, or the
  rule that should have stopped the L1 brief.
- **Fix not shown able to fail, component by component.** The row claims four properties: JSON branch
  kept; last verdict line; `exit=` equals the process exit; verdicts on both streams → null.
  Single-edit mutants of `new_rule` in the `/tmp` copy, each run with `--selftest`:

  | Mutant | Edit | `--selftest` exit | `correction.json` identical? |
  |---|---|---|---|
  | M1 | delete the JSON branch from `new_rule` (`:121-127`) | **0 (survives)** | no: 7 rows move to `coverage_changes`, but the run still exits 0 |
  | M2 | exit-equality → `True` (`:115`) | **0 (survives)** | yes |
  | M3 | delete the both-streams → null clause (`:130-131`) | **0 (survives)** | yes |
  | M4 | last → first match (`:116`) | **0 (survives)** | yes |
  | M2+M4 | both | 1 (killed) | yes |
  | M5 | regex → the rejected G8 draft | 1 (killed: `usage-proof-old` → None) | — |

  Only the draft regex is shown red-before. The JSON branch is the exact component AttrCritic F2 said
  the draft dropped, and its removal passes the committed selftest. QUALITY 18's text ("The repair
  keeps any prior structured branch (JSON) unchanged") has no fixture behind it.
- `correction-attrfix-draft.json` contains no supersession marker (`grep -ci supersed` → 0). Only the
  lesson row marks it superseded. Its `rules.new` still states the rejected rule. *(minor)*

### A3 — Row 3 (holds)

- `ls -la /home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/misroots/TameshiR15` → 605 B, 05:06:36.
  `sha256 b413df98…7236469`.
- Round-15 prompts: `round-15/dispatch1.json` has 66 tasks, 66 with `Message only TameshiR15` and
  0 with `agent://`. Its context does contain `agent://`. Wave 2 (`dispatch2.json`, 32 tasks) has
  neither. The "66/66" figure holds.
- Round-16 prompts: `round-16/dispatch1.json` has 68/68 tasks with `agent://TameshiR16`, and
  `dispatch2.json` has 67/67. The only bare `TameshiR16` tokens are the ones that explain the rule.
  No `TameshiR16*` file is present at the fleet root.
- Replay of Misroot's guard, taken from `w1/Misroot.md:196-220` (sha256 `30ed617d…`):
  - `bash guard2.sh <clean mirror>` → rc 0.
  - With the archived bytes copied to the mirror root → **rc 1** `STRAY [TameshiR15] (file, LANE-NOTE)`.
  - `git status --porcelain` on that mirror → `?? TameshiR15`.
  - `git status --porcelain -- .ufo/` → **empty, rc 0**, which is the historic miss.

  The row's fix is shown able to fail.
- Class: C09 "evidence landing" vs C10 "write-scope". A write outside the lane root is closer to C10.
  `landing` is defensible because the incident concerns *where a note landed*. No defect.
- Omitted live state: the same guard on the **live fleet root** → rc 1 `STRAY [bash: ] (dir)`, a
  directory dated 2026-10-18. Misroot arm 11 also found it. Under QUALITY 19 the round's misroot sweep
  is therefore red at HEAD. The lesson neither reports this nor routes it. It is not a round-16
  mistake, but the row presents the sweep as the detection without its current result. *(gap-minor)*

### A4 — Row 4 (partial)

- Timestamps and shas match `w1/CRSentinel.md:139-141` (10:27:20 `2e810b5d…a7c6`, 10:27:45 back to
  `75ed934d…adc5`), `w1/CR23.md:113,150` (13:27:04Z SETUP rc 2, 6 of 7 legs passed, one could not be
  verified), and `w1/RGCritic.md:67-69` (F10).
- `git show 28aeef4|e69b488:tools/mutate-and-run.sh | sha256sum` → `75ed934d…` for both.
- "No wave-1 verdict rests on the in-flight bytes" holds on recorded shas. `2e810b5d` appears only in
  CR23, CRSentinel and RGRecon (`:236`), and RGRecon used it only to describe the RGLeg copy. CR20 ran
  inside the race window (13:27:22Z) but on a pinned `/tmp` mirror. Every other CR tool sha is
  `75ed934d`.
- **Class meaning wrong.** `scope` is C03 *scope overreach* ("universal / 'generalizes' without a
  sweep", `mistakes.md:81`). A writer editing a shared instrument while readers execute it is C10
  write-scope (`attribution`) or C05/C08. Every word in the row is in the vocabulary, but the class
  does not mean what the row describes.
- **Captured-by misuse.** `RGCritic (same-wave)` again names a seat, not a rule.
- **Fix not shown able to fail.** QUALITY 20 is procedural ("staged at a separate path"). No gate
  detects an in-place edit, and no red-before state is committed. The CR23 SETUP is a symptom, not a
  run of the fix. The rule's own receipt clause ("every receipt names the instrument sha it ran") is
  not met by `round-gate/runner-selftest.txt`, which has 0 sha lines and only
  `MUTATE_SELFTEST: 81/81 pass` / `rc=0`. Only the separate `runner-sha256.txt` names `89722ddb…`.
- The wording "the staged copy was installed" is approximate: `RGLeg.mutate-and-run.sh` (`f91f7fa8…`,
  with `@@RG_*@@` placeholders) ≠ installed `tools/mutate-and-run.sh` (`89722ddb…`). The diff is
  exactly the placeholder substitution plus the spec body. Recording the substitution would make the
  provenance exact. *(minor)*

---

## B. Mistakes this round that the lesson omits

Ranked by impact. Classes are proposed from the 9-word vocabulary.

**O1 — `landing` + `scope` (C09 + C03): C2 and box 3 landed on a ledger that does not exist. Major.**
- `git ls-tree -r --name-only c699c8c -- .ufo/evidence/round-16/coldread/` → only `SKILL.snapshot.md`
  and `assemble.py`. There is no `ledger.json`, in the commit or in the worktree (`ls`,
  `git check-ignore` rc 1, `status --ignored` lists none).
- `c699c8c:SHONEN.md:9-10` box 3 links `(.ufo/evidence/round-16/coldread/ledger.json)`, a dangling
  link. `SKILL.md:1707-1716` (Errata) names the same ledger.
- `python3 measure.py --rev c699c8c` (committed bytes, `dc348360…`) → exit 0,
  `calibration_restraint_score: 6`, `ledger_present: false`, `sections_covered: 0`,
  `sections_total: 54`. The L1's repaired worktree `measure.py` (`a8f105c2…`) also prints **6**
  (`box3_ledger_link: true`, `box3_full_page: false`). The L1's own
  `.ufo/evidence/round-16/measure-repair/repaired-tool-at-c699c8c.json` says 6.
- Gate G6 says "admit — every bucket of the final page has a passing entry at its own section sha;
  repaired sections re-read in wave 2". At `c699c8c` wave 2 had not run. I ran
  `assemble.py --skill SKILL.snapshot.md --skill SKILL.md` over the committed `w1/CR*.md` (exit 1).
  Scored against the 54 final-page buckets, it gives **40 pass, 14 with no entry at their sha**:
  6, 58, 131, 246, 314, 497, 921, 933, 1380, 1464, 1609, 1707, 1740, 1789. The landing commit recorded
  the wave-2 outcome as already done. The wave-2 dispatch itself says
  "C2 calibration 6→8 pending ledger" (`dispatch2.json`, ScorecardDraft).

**O2 — `vacuous` (C04): `measure.py` box-3 link fixture.** The L1 is adding this row in the
worktree, uncommitted (`git diff corpus/lessons/round-16.md`, +1 row). I confirm it: the committed
selftest gives `MEASURE_SELFTEST: 33/33 pass` exit 0. Its fixture is
`SHONEN_BOX3 = '- [~] box three — evidence …ledger.json'` (`measure.py:310`), with the link on the
box line, while the real `SHONEN.md:10` puts it on the continuation line. The L1's draft row fixes
only `box3_ledger_link` and does not say that the score stays 6 (O1).

**O3 — `attribution` (C10 write-scope): QUALITY 20 recurred in wave 2.** The worktree
`.ufo/evidence/round-16/measure.py` has mtime 10:52:24, after wave-2 dispatch
(`dispatch2.json` 10:51:26). It was edited in place (`git diff --stat`: +36/−2) while wave-2 seats
(DepthCritic, ToolsNoHarm, MutateMeasure) run that tool. The wave-2 contract ("run lane tools from a
/tmp copy of their committed bytes") lowers the risk. [INFERENCE] no wave-2 verdict is affected unless
a seat ran the live path. The round's own rule says "not edited in place during that wave".

**O4 — `stale-premise` / `reference-drift` (C06/C01): the 13 page mistakes mined by the cold-read.**
`SKILL.md:1717-1731` (Errata table) lists 13 wrong expectations found this round:
- `number-drift`: 360-361, 505, 925, 949-950, 1388.
- `reference-drift`: 277-279, 1614.
- `stale-premise`: 15, 134-135, 1472.
- wrong claims: 61, 269-270.

CORPUS says "One row per mistake" (`CORPUS.md:171-172`). The lesson carries them only through G9
("in-place SKILL repairs"), with no class, no captured-by and no fix-can-fail. At minimum it needs one
row per class, pointing to the errata table.

**O5 — `vacuous` (C04): CR24's verified-record on a record it could not check (G7).**
CR24's JSON, section 1464: `"verdict": "verified-record"` together with
`"minor_gaps": ["… SHONEN.md box-3 state … contamination-barred for a cold reader; the current [ ] vs
[~] box state cannot be re-checked from the page alone …"]`. That breaks the seat contract (a named
minor gap means gap-minor; `assemble.py` downgrades it). Two things caused it. The read bar makes a
SHONEN-citing record unverifiable. And the page said `Box 3 remains [ ]` at the snapshot's `:1472`
while `e69b488:SHONEN.md:9` was `[~]`. G7 records only the reject, not the seat/design mistake.

**O6 — `number-drift` (C02): "50 sections" denominator (G10).** The L1 claim text said 50. Three
seats corrected it to 51 (`w1/CRCritic2.md:29-32`, `CRCritic1.md:58`, `CRRevenger.md:209-210`). At
`c699c8c` the final page has **54** buckets: the 51 of the snapshot plus the 3 appended sections at
1707, 1740 and 1789. G10 still says 51. It is a gate reject with no Mistakes row.

**O7 — `attribution` (C10 write-scope): latent `GIT_DIR` inheritance in the runner (G5).**
RGSentinel S1 (`w1/RGSentinel.md:32-50`): an exported `GIT_DIR` makes a suite's control commit into a
foreign repository. The repair is confined to the new leg: `env -i` appears only at
`tools/mutate-and-run.sh:1221` (js-round-gate). The other six legs still run `bash -c "$SUITE"` with
the inherited environment. [INFERENCE] the hazard bites only legs whose suites shell out to git. Only
the gate reject records it.

**O8 — `landing` (C09): a retained wave-1 report was rewritten in the landing commit.**
`w1/CRMeasure.md` was retained at `e69b488`, then changed 138 lines in `c699c8c`. It now says
"~545 lines", but `measure.py` is 596 (`wc -l`). The `e69b488` version described a 480-line
`measure.py` that was not committed there (`ls-tree e69b488` has no `measure.py`). Neither the lesson
nor the report notes the revision. *(minor)*

Checked and **not** a mistake:
- **Rebase.** Reflog: `f32e654` commit 10:39:50 → `pull --rebase` → `e69b488` 10:39:59. Then
  `git diff --stat f32e654 e69b488` = only `considerthese/2026-10-20.md` (+72). `MUTATE_DATE
  2026-10-20T13:40:15Z` (10:40:15-03) is later than both. Nothing cites the orphaned `f32e654`. The
  disclosure is accurate. [INFERENCE] push time is not locally observable.
- **Seat deaths.** `record1.json` has 68 members. No wave-1 report declares a blocking failure. The
  grep hits for "blocked" are domain verdicts (e.g. tsukuroi `BLOCKED` fixtures). Not a mistake.

---

## C. Smallest safe corrections (advice; the L1 decides)

1. Commit `coldread/ledger.json`, assembled after the wave-2 re-reads. Until then, hedge C2 and G6 as
   pending and keep SHONEN box 3 without the ledger link (or mark the link pending). Add O1 as a
   `landing` row with red-before `measure.py --rev c699c8c` → 6.
2. Rows 2 and 4, Captured-by: replace the seat names with `none` (or the rule that should have
   fired). Put the finder in the evidence column.
3. Row 4: change the class to `attribution` (C10 write-scope). Add one red-before state, e.g.
   `sha256sum` before and after each wave plus a check that fails on a mid-wave change. Add the
   instrument sha to `runner-selftest.txt`.
4. `reattribute.py`: add a JSON-row fixture (kills M1), a both-streams fixture (M3), and an
   exit-mismatch-as-last-line fixture (M2/M4). Update the docstring to the repaired rule. Fix the
   row-2 regex quote.
5. Add rows for O3 (wave-2 in-place edit), O4 (cold-read page mistakes, grouped by class), O5 and O6.
   Also note the live `bash: ` stray as a routed residual.

## D. Commands run (key lines)

```
git show c699c8c:corpus/lessons/round-16.md                       # rows :53-56
python3 reattribute.py --selftest                                 # exit 0, 4/4 vs 3/4
python3 reattribute.py (pristine /tmp copy)                       # exit 0, correction.json identical=True
mutants M1..M5, M2+M4 (/tmp/…/mut/*)                              # M1-M4 exit 0; M5, M2+M4 exit 1
sha256sum verification-3.json                                     # 3c419055…d8ce
bash guard2.sh <live fleet root>                                  # rc 1 STRAY [bash: ] (dir)
bash guard2.sh <mirror> / +TameshiR15                             # rc 0 / rc 1 STRAY [TameshiR15]
git -C <mirror> status --porcelain [-- .ufo/]                     # ?? TameshiR15 / empty
git ls-tree -r --name-only c699c8c -- .ufo/evidence/round-16/coldread/   # no ledger.json
python3 measure.py --rev c699c8c (committed)                      # exit 0, score 6, sections 0/54
python3 measure.worktree.py --rev c699c8c                         # score 6, link true, full_page false
python3 measure.py --selftest (committed)                         # 33/33 pass, exit 0
python3 assemble.py --skill snapshot --skill SKILL.md w1/CR*.md   # exit 1, 51/65; final page 40 pass / 14 no-entry
git reflog --date=iso -25                                         # f32e654 → rebase → e69b488 10:39:59
git diff --stat f32e654 e69b488                                   # considerthese only
```

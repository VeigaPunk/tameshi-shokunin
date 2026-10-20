# LessonGateDraft — draft `## Same-round falsification` for corpus/lessons/round-16.md

Seat: TameshiR16.LessonGateDraft (leaf, wave 2, falsify). Lane commit c699c8c36d6e4eca4b796b81a8247904aa145ec8.
Target lesson read at that commit (`git show c699…:corpus/lessons/round-16.md`, 68 lines). The lesson was not edited. The working-tree copy has been modified since (`git status`: ` M corpus/lessons/round-16.md`, 69 lines, no same-round section yet); I did not read its changes.
Scratch: `/tmp/tameshi-r16w2-LessonGateDraft-hZ6zIo/` (committed bytes only).
Tools installed or updated: none. Used git 2.x, sha256sum, system python3, node v24.21.0 (already present).

**Verdict: partial.** The G-row decisions that cite a critic (G1, G3, G5, G7, G8, G9, G10) and QUALITY 18 hold on re-execution. The lesson's sentence "No wave-1 verdict rests on the in-flight bytes" (`lesson:56`) is not supported for CR22. G6 falls as written: its ledger is not committed at c699. About half of the critics' findings have no L1 decision in the lesson, so the drafted section below carries them as open items, not as closed.

## 1. Draft section (for the lesson; not applied)

```markdown
## Same-round falsification

Six wave-1 critics attacked this round's claims before L1 integrated them.
Each entry names the report that carries the finding and the decision it
caused. Paths are lane-relative; `:n` is a line in the named file.

**RGCritic** (`.ufo/waves/round-16/w1/RGCritic.md:29-67`, C1 depth 6→7).
Pre-registration held: `round-gate/predictions.json` (spec sha256
`e99b87eb…`, `registered_at_utc` 13:39:42Z) is in commit `e69b488` (committer
10:39:59 −03), before the sweep (`round-gate/sweep/sweep.log`, MUTATE_DATE
13:40:15Z). Its 10 predictions match `sweep/results.tsv` on all 10 rows. The
spec body embedded in `tools/mutate-and-run.sh:906-962` is byte-identical to
the committed spec. The boundary-only `REPORT_MIN_BYTES` pair replaced the
midpoint (F5, `:47-49`; G3 at `:20`). Open: F6 (a SKIP is recorded with
`ok: true`, `round-gate.mjs:1382`) has no lesson row; the sweep evidence
contains zero SKIP lines. F10 (wave-1 race) is QUALITY 20 (`:56`).

**RGSentinel** (`.ufo/waves/round-16/w1/RGSentinel.md:32-111`, S1-S6).
S1 (HIGH): an inherited `GIT_DIR` makes the selftest commit fixture history
into the live repo. Reproduced: bare suite exit 1, canary 1→43 commits;
guarded `env -i` suite exit 0, 60/60, canary 1→1. This is G5 (`:22`). The
guarded literal is what the leg (`tools/mutate-and-run.sh:1221`) and the sweep
(`round-gate/suite.txt`) use. S3 (NESTED skip, TMPDIR walk-up) is, by
construction [INFERENCE], closed by the same cleared environment; the lesson
does not say so. Open: S2, S4-S6.

**CRCritic1** (`.ufo/waves/round-16/w1/CRCritic1.md:146-168`, C2 premise).
Two defects in the class-blind pass and the author override are closed in
committed tooling: `measure.py:183-199` credits by class×verdict and
`measure.py:188-193` requires `commands_executed`; `assemble.py:27-30,224`
says an override can never relax a wave-1 entry. Neither is recorded in the
lesson. Open: the SHONEN box-3 line (`SHONEN.md:9-10`) and `measure.py:68`
both name `.ufo/evidence/round-16/coldread/ledger.json`, which is not
committed at c699. G6 (`:23`) is admitted on evidence that is not yet in the
commit. SKILL `:1472` ("Box 3 remains `[ ]`", E11) was repaired in place (G7,
`:24`). Open: the dead `/tmp` pointers (A6) are still on the page (see §3).

**CRCritic2** (`.ufo/waves/round-16/w1/CRCritic2.md:29-154`, protocol).
F1, 51 units (G10, `:27`). F11, in-place repair shifts anchors (G9, `:26`):
the page's diff against the snapshot has 14 hunks, all same-count, so no line
moves. F12, the errata append changes the last bucket's sha (`SKILL.md:1705c1705,1796`;
errata at `SKILL.md:1707`), so that bucket must be re-read at the final sha.
F5 (class dominance), F6 (gap-list downgrade, union counts) and F13 (reports
tracked) are implemented in `assemble.py:224,389-390,400-406`. Open, with no
tooling hit: F2 (anchor-barred), F3 (superseded), F4 (revision rule), F7
(target/informed_by), F8 (replica sample), F9 (whole-page coherence seat), F10
(contamination tags). F14: the page says "instructions executed"
(`SHONEN.md:10`); the lesson should say "I executed, R anchor-verified".

**AttrCritic** (`.ufo/waves/round-16/w1/AttrCritic.md:86-132`, routed defect 2).
F1, the first NEW regex nulls real verdicts: G8 rejected (`:25`). The admitted
rule (`.ufo/evidence/round-16/attribution/reattribute.py:102-135`) keeps the
JSON branch and takes the last full-line `CONTEXT:` verdict whose `exit=`
matches. Its `--selftest` passes (exit 0): the new rule is 4/4, the old rule
fails 3/4 (`:53` confirmed). F3's forged-first-line fixture is in the
selftest (`reattribute.py:269-274`). Open: F6, both-stream verdicts → null
(`:54`), is not exercised; no fixture has verdicts on both streams. F7 is
partial: `correction.json` names the two rows, but has no `detail` entry
(verified: zero matches).

**CRSentinel** (`.ufo/waves/round-16/w1/CRSentinel.md:58-146`, side effects).
F5, the harness changed during wave 1, is QUALITY 20 (`:56`). Timing:
CR22 ran from 13:25:57Z for 86.8 s (`w1/CR22.md:23-24`), i.e. until about
13:27:24Z. The altered tool was observed at 13:27:04Z (`w1/CR23.md:113`) and
at 10:27:20 −03 (`w1/CRSentinel.md:139-141`). CR22's run therefore overlapped
the altered window by about 20 s. Its output (six legs, 75ed934d pins) is
consistent with the committed tool, but its only sha check was at start.
Only CR23 was re-run on committed bytes (`w1/CR23.md:88-99`, PASS at 13:29:14Z).
Open: F1 (`capture-context.py` overwrites the frozen receipt; `SKILL.md:1593,1602,1623`),
F2 (`git status` without `--no-optional-locks`; `SKILL.md:151,225,350,381,605,1035,1056,1206`),
F3 (`W=/tmp/<lane>-…` placeholder; `SKILL.md:543,611`), F4 (fleet-root output;
`SKILL.md:542-565,610-631`). All four are unchanged at c699 and have no lesson row.

**Pin drift.** The committed `tools/mutate-and-run.sh` is sha `89722ddb…`, the
staged RGLeg draft with placeholder substitutions; the first differing hunks are at `:91`, `:570`, `:901-904` (the full 85-line diff was not reviewed).
The sweep used `75ed934d…` (`sweep/sweep.log`, MUTATE_TOOL). The page still
cites `75ed934d` at five places (e.g. `SKILL.md:1304,1308`). Process
disclosure `:66-68` covers the round-15 pin; it does not name `89722ddb` or
the page's stale pins.
```

## 2. Evidence (commands, exits, key lines)

| # | Command | Exit | Key result |
|---|---|---|---|
| E1 | `git show c699…:corpus/lessons/round-16.md` and `:.ufo/waves/round-16/w1/{RGCritic,CRCritic1,CRCritic2,AttrCritic,RGSentinel,CRSentinel}.md` | 0 | 68-line lesson; six reports (91, 212, 240, 164, 150, 279 lines) |
| E2 | `git show c699…:SKILL.md \| sha256sum`; snapshot sha | 0 | SKILL.md `3d8a1edb…` 1795 lines; snapshot `97cf436b…` 1704 lines |
| E3 | `diff snapshot SKILL.md` (c699) | 1 (diff) | hunks `15,63,134-135,271-272,278-280,361,505,514-515,925,950,1390,1393,1472,1614` all `NcN` same count; `1705c1705,1796` appended errata |
| E4 | `ls .ufo/evidence/round-16/coldread/` (worktree); `git cat-file -e c699…:…/coldread/ledger.json` | 0; 128 | only `SKILL.snapshot.md`, `assemble.py`; ledger.json **absent** |
| E5 | `python3 reattribute.py --selftest` in a lane-depth copy of committed bytes (`verification-3.json` sha `3c419055…`) | 0 | `usage-proof-new` old FAIL/new PASS; `gate-usage` old FAIL/new PASS; `usage-proof-old` old PASS/new PASS; `forged-first-line` old FAIL/new PASS; `SELFTEST: PASS (new rule 4/4; old rule fails 3/4)` |
| E6 | pristine `round-gate.mjs` (sha `f890e277…`), bare suite with `GIT_DIR` set to a canary | 1 | `Error: fixture checkout main failed` in my first probe (canary lacked `main`); fixed probe: canary commits 1→43 |
| E7 | same, guarded `env -i` suite, canary created with `-b main` | 0 | `ROUND_GATE_SELFTEST: 60/60 pass`, `VERDICT: PASS`; canary 1→1 commit, status clean |
| E8 | `predictions.json` vs `sweep/results.tsv` | — | 10/10 agree: KILLED A1, A3, B1, E3, C1060; SURVIVED C1059, A2, B2, CKIND, E1 |
| E9 | `sed -n 906,962p tools/mutate-and-run.sh \| cmp - round-gate.defects.spec` | 0 | BODY_BYTE_IDENTICAL (sha `e99b87eb…`) |
| E10 | `sweep/sweep.log` | — | MUTATE_TOOL `75ed934d`; MUTATE_DATE 13:40:15Z; CONTROL GREEN; MUTATE_RESTORE OK; DONE killed=5 survived=5 inconclusive=0 |
| E11 | `sweep/evidence/*.out` grep `SKIP` (11 files) | — | 0 SKIP lines in every file |
| E12 | `git merge-base --is-ancestor e69b488 c699…` | 0 | ancestor; committer `2026-10-20T10:39:59-03:00` |
| E13 | `git show c699…:tools/mutate-and-run.sh \| sha256sum` | 0 | `89722ddb…` (pre-c699 `75ed934d…`); worktree equal |
| E14 | `diff RGLeg.mutate-and-run.sh tools/mutate-and-run.sh` (both c699) | 1 | 85 diff lines; first hunks at `:91`, `:570`, `:901-904` (remainder not reviewed); staged copy sha `f91f7fa8…` matches `w1/RGLeg.md:12-13` |
| E15 | `grep -c '75ed934d' SKILL.md` (c699) | 0 | 5 matches, first `:1304` |
| E16 | `git show c699…:corpus/lessons/round-16.md` `:53,56,66-68` | — | QUALITY 18, QUALITY 20 and the drift disclosure as quoted in §1 |
| E17 | `grep -n -E 'status --porcelain\|no-optional-locks'` on c699 SKILL.md | 0 | status calls without the flag at `151,225,350,381,605,1035,1056,1206`; the flag appears at `1737-1738` |
| E18 | `grep -n '/tmp/w(6\|8\|9)-'` on c699 SKILL.md; `test -e` on `/tmp/w6-aud-t6-work`, `/tmp/w8-tameshi-t84`, `/tmp/w9-tameshi-t93`, `/tmp/w8-tameshi-t81`, `/tmp/w8-t8-2-claims` | 0 | 9 matching lines (`:919,1040,1066,1109,1167,1191,1215,1216,1222`); all five probed dirs absent |
| E19 | `grep -c detail correction.json`; `python3` key walk | 0 | 2 corrections (`usage-proof-new`, `gate-usage`); no `detail` key |
| E20 | `grep -c` of `anchor-barred`, `superseded`, `informed_by`, `replica`, `coherence`, `contaminat`, `needs-reread` in c699 `measure.py` and `assemble.py` | 0 | zero matches for all |
| E21 | `measure.py:183-199,262-265`; `assemble.py:27-30,224,389-390,400-406`; `measure.py:68` | — | as cited in §1 |

Not run: `measure.py`, `assemble.py` (not executed), any mutant sweep, the `--regression` at c699 (its `js-round-gate` leg was not run by me), and the operator runbook's pin step. No checks were run in the lane tree; every probe used `/tmp` copies or `git show` output.

## 3. Critic-by-critic status

| Critic | Finding | Lesson row | Status at c699 |
|---|---|---|---|
| RGCritic F1-F4, F9 | independence, province, pre-reg, spec identity | G1 `:18`; S052-S057 `:33-38` | holds (E8, E9, E12) |
| RGCritic F5 | boundary, not midpoint | G3 `:20` | holds (`sweep/defects.tsv` C1059/C1060) |
| RGCritic F6 | SKIP counts as pass | none | open (E11 zero SKIP; code `:1382`) |
| RGCritic F7-F8 | hermeticity, command-D header regex | none | open |
| RGCritic F10 | wave-1 race | QUALITY 20 `:56` | partial (see CR22 timing) |
| RGSentinel S1 | GIT_DIR contamination | G5 `:22` | holds (E6, E7) |
| RGSentinel S2, S4-S6 | rm reach, live-path stat, timeout leak | none | open |
| RGSentinel S3 | env-dependent verdict | none | not recorded; closed by the guard |
| CRCritic1 A2, L1 | class-blind pass | none | implemented (`measure.py:183-199`); not recorded |
| CRCritic1 L4 | author override relaxes verdict | none | implemented (`assemble.py:27-30,224`); not recorded |
| CRCritic1 A5, E11 | `:1472` contradiction | G7 `:24` | holds (repaired in place, same-count hunk) |
| CRCritic1 A6 | dead `/tmp` pointers | none | open (E18) |
| CRCritic1 A7 | SHONEN link to committed ledger | G6 `:23` | falls: ledger not committed (E4) |
| CRCritic1 A8 | "pending non-author closure" | `:5-7` | partial (scope kept; wording absent) |
| CRCritic2 F1 | 51 units | G10 `:27` | holds |
| CRCritic2 F11 | in-place repair vs anchors | G9 `:26` | holds (E3) |
| CRCritic2 F12 | errata append changes last sha | none | open (E3) |
| CRCritic2 F2-F4, F7-F10 | barred paths, revision, replicas, coherence, contamination | none | open (E20) |
| CRCritic2 F5, F6, F13 | class dominance, gap-derived verdicts, reports tracked | none | implemented (`assemble.py:224,389-390,400-406`); not recorded |
| CRCritic2 F14 | "executed" wording | none | open (`SHONEN.md:10`) |
| AttrCritic F1, F3, F4 | NEW regex, last-vs-first, fixture count | G8 `:25`, QUALITY 18 `:53-54` | holds (E5) |
| AttrCritic F6 | both-stream precedence | `:54` | partial (not exercised, E5) |
| AttrCritic F7 | "detail" field undercount | `:53` | partial (E19) |
| CRSentinel F5 | harness race | QUALITY 20 `:56` | partial (CR22 overlap) |
| CRSentinel F1 | frozen-receipt overwrite | none | open (E17-adjacent; `SKILL.md:1593-1623` unchanged) |
| CRSentinel F2 | `git status` index writes | none | open (E17) |
| CRSentinel F3, F4 | `W=/tmp/` placeholder, fleet-root output | none | open (`SKILL.md:543,611,542-565,610-631`) |
| CRSentinel F6-F10 | record writes, rm fixed path, drift demo, repeat-control `--out`, witness rerun | none | open |

## 4. Corrections the lesson needs before it is final

1. `:56` "No wave-1 verdict rests on the in-flight bytes." Replace with what was checked: CR23 re-ran on committed bytes (`w1/CR23.md:88-99`); CR22 overlapped the altered window by about 20 s (`w1/CR22.md:23-24`, `w1/CR23.md:113`), its output is consistent with the committed tool, and it has no end-of-run sha. State that CR22's verdict is `[INFERENCE]` until a per-seat sha is checked.
2. `:23` G6 admitted, but `.ufo/evidence/round-16/coldread/ledger.json` is not committed at c699 (E4). Either commit it or keep G6 as "pending commit".
3. `:66-68` add the new tool sha `89722ddb…` and the page's five `75ed934d` pins (`SKILL.md:1304,1308,…`).
4. Add rows for the open critic items in §3 (RGCritic F6, RGSentinel S2/S3, CRSentinel F1-F4, CRCritic2 F2-F4/F7-F10/F12/F14, CRCritic1 A6). Each needs a decision (admit, reject, or open with owner) to satisfy the lesson's own gate format.
5. `:53` correction.json: add the `detail` field entry (AttrCritic F7) or state it as not corrected.
6. `:54` both-stream → null: add a fixture, or say it is untested.

## 5. Falsifiers and outcome per attack

- Attack: does the drafted section match the six reports and the lesson's G-rows? Holds for G1, G3, G5, G7-G10, QUALITY 18 (E3, E5-E9, E12).
- Attack: is the "no in-flight verdict" claim true? Partial (CR22 overlap, E13/timing).
- Attack: is G6 backed by committed evidence? Falls (E4).
- Attack: does the lesson record every critic finding? Falls: about 20 findings are open or unrecorded (§3).

Blockers: none. No message to agent://TameshiR16 was needed.

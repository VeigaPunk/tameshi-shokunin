# ErrataAudit — round-16 errata table vs the wave-1 seat findings

Seat: `TameshiR16.ErrataAudit` (leaf; no dispatch).
Target: `SKILL.md` §`## Errata — round 16 full-page cold-read (append-only)` at
`c699c8c36d6e4eca4b796b81a8247904aa145ec8`, checked against every
`wrong_expectations` entry in `.ufo/waves/round-16/w1/CR*.md` and the
`CRCritic*.md` reports.
Snapshot: `git show e69b488:SKILL.md`, sha256
`97cf436b669ea445abe36cf6757202eec1c2a4bad2814b07f4159bb9dc623580` (matches
`.ufo/evidence/round-16/coldread/SKILL.snapshot.md`; `git rev-parse
e69b488:SKILL.md` → git blob `0926115`).
Scratch: `/tmp/tameshi-r16w2-ErrataAudit-53D3xz/`. No lane file edited outside
this report. No tools installed or upgraded.

**One-line verdict: PARTIAL.** All 13 table rows carry true new wording (each
re-checked against the named file), and 8 of the 9 `wrong_expectations`
reported by wave-1 seats are repaired; CR16's second reported wrong
expectation — drifted `tools/mutate-and-run.sh` line anchors — is neither
repaired nor explicitly left with a reason (omission). The errata's own evidence
plumbing also fails at the audited commit: the cited
`.ufo/evidence/round-16/coldread/ledger.json` does not exist, `measure.py
--rev c699c8c` therefore reports `box3_full_page=false` / score 6, and the
suggested `git show 97cf436b…` is not a valid git object.

---

## 1. Method and evidence base

1. Extracted the final fenced `json` block of all 38 committed `w1/CR*.md`
   files with Python (`json.loads`, `sections[*].wrong_expectations`).
   Result: **9 wrong expectations in 5 seats** — CR02 ×1, CR05 ×2, CR06 ×1,
   CR10 ×2, CR16 ×3. Every other CR seat's array is empty. `CRCritic1` and
   `CRCritic2` carry no JSON block; their page-level wrong expectations are
   prose (`CRCritic1.md:19,75`; `CRCritic2.md:47-53`) and are covered below.
2. Cross-checked the inventory with `assemble.py` over the w1 reports
   (`/tmp/.../ledger.json`): the same 9 appear as
   `wrong_expectations` counts on sections 58, 246, 314, 497, 921 and 933.
   `python3 .ufo/evidence/round-16/coldread/assemble.py --selftest` → exit 0;
   assembly over `.ufo/waves/round-16/w1/CR*.md` → exit 0, **51 entries,
   "missing sections: none"**, 30 distinct seats (matches the errata's
   "51 buckets" and "30 lane seats").
3. Diffed the pinned snapshot against HEAD:
   `git diff -U0 e69b488 c699c8c -- SKILL.md` gives **15 hunks**: 14
   equal-count replacement hunks inside the existing 1705 lines (19 deleted /
   19 inserted) and a 15th hunk at old line 1705 that re-adds the final line
   and appends 91 new lines (1 deleted / 92 inserted). Net: 111 insertions,
   20 deletions; the snapshot's `split('\n')` length 1705 → HEAD 1796. Every
   repair hunk is an equal-count replacement, and the 54 snapshot heading
   lines are all at the same line numbers in HEAD (`python3` zip compare,
   0 differences), so the errata's "line count unchanged / self-anchors still
   resolve" holds. The 4 headings after line 1705 are the 3 new sections plus
   the code-fenced `# expect:` line (not a section — `assemble.py` counts
   outside-fence headings only).
4. Re-executed each cited probe from `/tmp` copies of the committed bytes
   (kagi `c2cab35`, kumitate `1770305f`) and re-derived the arithmetic claims.
5. Ran the lane's own counting command at the audited revision and at both
   skills:
   - `python3 .ufo/evidence/round-16/measure.py --rev c699c8c…` → exit 0,
     `calibration_restraint_score: 6`, `coldread.box3_full_page: false`,
     `coldread.ledger_present: false`, `missing` = **54 of 54** sections
     (`/tmp/.../measure.json`).
   - `assemble.py --skill SKILL.snapshot.md --skill SKILL.md` over w1 only →
     exit 1, `coverage: 51/65 sections covered`, 14 missing: the 11 repaired
     sections plus the 3 new sections.

## 2. Wrong-expectation inventory → errata-table coverage

| # | Seat | Ledger section | Reported wrong expectation (abridged) | Table row? |
|---|---|---|---|---|
| 1 | CR02 | 58 Gate-shape | live gate "usage 64"; kagi folds usage/setup into 2 | **yes** — row 61 |
| 2 | CR05 | 246 Templates | two-space substring "produces a *different mutant*" | **yes** — row 269-270 |
| 3 | CR05 | 246 Templates | `${n}` claimed in the two notes' manifests; it is in Appendix A D4 | **yes** — row 277-279 |
| 4 | CR06 | 314 Kill-rate bands | D1/D3 die on the "same 16 cases" — 16 each, only 14 shared | **yes** — row 360-361 |
| 5 | CR10 | 497 Fail-closed | "22 denied verbs" — enumerated regex has 23 | **yes** — row 505 |
| 6 | CR10 | 497 Fail-closed | surface-probe / cite-check exit-2 paths "uncovered" | **yes** — row 513-515 |
| 7 | CR16 | 921 Leg ledger | "Four legs at this revision" vs six-leg tool | **yes** — row 925 |
| 8 | CR16 | 921 Leg ledger | **cited `path:line` anchors drifted** (tables 554-559 vs page 511-522; registry 1111-1141 vs 927-944; output/exit 1074-1173 vs 891-975) | **NO** — no row, no reason |
| 9 | CR16 | 933 Using the ledger | receipt literal `cases=4` vs observed `cases=6` | **yes** — row 949-950 |

CRCritic1/CRCritic2 page-level findings: `:1472` (row 1472), `:14-15` and
`:134` (rows 15 and 134-135), and the "50 sections" wording (now "51 buckets")
are covered. Their remaining findings are protocol criticisms
(`measure.py`/`assemble.py` class and merge rules) except **CRCritic2 F9**, a
page-coherence finding the table does not cover: `SKILL.md:9-10` still reads
"Two mutation cases are now measured — round 2 JS, round 3 bash", while the
page records six cases at the snapshot and seven at HEAD
(`SKILL.md:1740-1788`; `ls corpus/knowledge/mutation-case-*.md | wc -l` = 7).
The errata repaired the next sentence (`:15`) but neither dated nor repaired
this one, and does not list it as debt.

### The omission (CR16 #2)

CR16's JSON (`w1/CR16.md`, section `start=921`) lists this as its second
`wrong_expectations` entry, and its prose recommendation (`CR16.md:57`) says
"refresh the `mutate-and-run.sh` line anchors". The errata's row 925 only
dates the leg count; the anchors are untouched. They are still stale in HEAD
at the revision the page says they were read at (`75ed934d…`, content sha256
`75ed934dc863…adc5`, blob at `e69b488`):

```
git show e69b488:tools/mutate-and-run.sh | sed -n '511,522p'
  → MUTATE_EVIDENCE / kill-rate percent lines      (page says "pins/revisions/tables")
  sed -n '554,559p' → TABLE_JS…TABLE_MADO             (the recorded tables really start here)
  sed -n '927,944p' → regression_case_git git-cat-file block (page says "leg registry")
  sed -n '1111,1141p' → regression_case_git js-kimi…js-claims (the actual registry)
  sed -n '891,975p'  → regression_case() helpers       (page says "output/exit code")
  sed -n '1074,1173p' → run_regression() body          (the actual output/exit code)
```

HEAD still cites `tools/mutate-and-run.sh:72-109`, `:511-522`
(`SKILL.md:929`), `:891-975` (`:940`) and `:511-522`, `:927-944`
(`SKILL.md:961-962`). Only `:72-109` (header/exit-map prose) still points at
relevant material; the other three are stale exactly as CR16 reported, and
the `75ed934d…` qualifier at `:961` does not rescue them because they were
already stale at that content sha. This is an omission under the acceptance
criterion, not a false repair.

## 3. Per-repair verification — all new wording is true

All commands from `/tmp/tameshi-r16w2-ErrataAudit-53D3xz/` over
`git show <rev>:<path>` materializations.

| Row | Check executed | Exit | Result |
|---|---|---|---|
| 15 | `SKILL.md:15` read at HEAD | — | "round 16 adds a full-page cold-read (Errata — round 16)" — target exists (line 1707); w1 assembly covers 51/51 snapshot sections |
| 134-135 | read CR04a/CR04b `## Execution` and JSON verdicts | — | both `executed-ok`, both ran steps 1–10 end to end (CR04a on pinned `175de6ba`, CR04b on the moved tree) — "two seats" true |
| 61 | `bash claim-ledger.sh --bogus-flag` → `claim-ledger: unknown argument…`; `node claims-check.mjs --bogus-flag` → usage | **2 / 64** | true; also `node kimi-census.mjs --bogus-flag` and `node round-gate.mjs --bogus-flag` → 64, so "kumitate's hermetic usage code" generalizes; kagi's six-gate table (`gates-survey-kagi.md:78-86`) folds usage into exit 2 |
| 269-270 | `str.replace` of six-space vs two-space D3 `old` on pinned `kimi-census.mjs` | — | `count(old6)=count(old2)=1`; both outputs sha256 `1ea6d77f787cd03a905ac97212cc36b05d5d175c1553ec4e3b09241b24b4f971`, `a==b True` — byte-identical, matching CR05 |
| 277-279 | `grep -c '${n}'` in both notes; `grep -n` for the other tokens; `grep -n '${n}' SKILL.md` | — | notes: 0 `${n}`; `(mode & m.modeFloor)` kimi note:162; `slice(0, 6)` kimi note:157; `[[ "$got" -ge "$floor" ]]` kagi note:221; `${n}` at `SKILL.md:575` (Appendix A D4) — true |
| 360-361 | applied D1 (`counted: 18→17`) and D3 to pinned `kimi-census.mjs`, ran `node … --selftest` | d1=1, d3=1 | `FAIL` lines: **16 in each, 14 identical**; D1-only = "UNLISTED: a 19th lane file under agents/secondary/" and "root enum is orthogonal to counted-dir drift"; D3-only = "UNLISTED: an undeclared child directly under plugins/" and "… under plugins/managed/" — exactly CR06 |
| 505 | `DENY_WORD_RE` at `claim-ledger.sh:164` | — | 23 alternatives (op … tar); 24 `|` separators counting the two boundary groups — true |
| 513-515 | `surface-probe.mjs:1340-1347`; `cite-check.mjs:2334-2343` | — | each asserts a bare-run `--src` fail-closed `exit === 2` check; no arm enum/accounting beyond it — true |
| 925 | `tools/mutate-and-run.sh` at HEAD | — | header `:14-15` "r16 … seventh measured gate"; `nlegs=7` at `:1225`; 7 `regression_case_git` calls `:1189-1222` — "seven since round 16" true; the four r7-1 legs are the page's four |
| 949-950 | same file | — | receipt uses `$nlegs` (`:1246`), `REGRESSION_EXPECT` has 7 rates (`:1179`); N per revision is the correct wording. (I did not execute the full 7-leg `--regression`; `nlegs=7` read from source.) |
| 1388, 1392 | `ls corpus/knowledge/mutation-case-*.md | wc -l`; `git log -1 -- corpus/knowledge/closeout-r11.md`; `git log --all -- plans/round-11-record-draft.md` | — | 7 notes; `closeout-r11.md` exists at `284ab0f`; `round-11-record-draft.md` has no history — both new clauses true. The "Found by CR23" applies only to the plans half: CR23 (`CR23.md:69`) reported the plans pointer as a minor gap and verified the then-correct "(six)" count as 6. |
| 1472 | `sed -n '9,12p' SHONEN.md`; `sed -n '1472p' SKILL.md` | — | SHONEN box 3 is `[~]`; HEAD says "Box 3 was `[ ]` at this write (`[~]` since; Errata — round 16)" — true |
| 1614 | `ls ../PROTOCOL.md`; `grep -n '## Gate standard' ../PROTOCOL.md` | — | fleet root `PROTOCOL.md` exists, `## Gate standard` at `:375`; lane has no `PROTOCOL.md` — true |

Preamble checks: snapshot sha256 `97cf436b…3580` true; 51 buckets true
(assemble, 51 entries); 30 seats true (assemble's distinct `seats` = 30);
equal-count repairs and stable heading lines true (section 1.3); "old wording
stays in git" substantively true, but see F4 for the command given.

## 4. Defects in the errata's own claims (beyond the table rows)

**F1 — blocking for the box-3 claim at this commit: the cited ledger does not
exist, and the lane's own counter scores box 3 at 0.** The errata preamble
(`SKILL.md:1711-1712`) cites
`.ufo/evidence/round-16/coldread/ledger.json`; `git ls-tree -r c699c8c
.ufo/evidence/round-16/coldread/` lists only `SKILL.snapshot.md` and
`assemble.py`, and `find .ufo -name 'ledger*.json'` returns nothing (also not
gitignored). `SKILL.md:1781-1788` says the cold-read "earns the box-3 lane
assertion (`[~]`)" and `SHONEN.md:9-12` carries `[~]` with the same path as its
only evidence link. But `measure.py --rev c699c8c` → exit 0,
`coldread.ledger_present=false`, `box3_full_page=false`, `missing` = 54/54,
`calibration_restraint_score=6`, `shonen.box3_points=false`. The committed
counter cannot even see the SHONEN link: `shonen_boxes` returns the box line
only (`measure.py:137-139`, `BOX_RE` at `:62`), line `:262` tests
`BOX3_LINK in boxes[2][1]`, and `SHONEN.md:9-12` puts the link on the
continuation line — committed output is `shonen.box3_ledger_link=false`. (A
wave-2 sibling's uncommitted fix for this is outside the audited commit; I ran
the committed bytes from `/tmp`.) The ledger is
reproducible from the committed w1 reports (`assemble.py` exit 0, 51/51), and
wave-2 re-reads are required before the post-repair page can be covered — but
as landed at `c699c8c` the durable pointer and the stated score do not exist.
Severity: blocking for the box-3 assertion at this revision; not a defect in
the table's repair wording.

**F2 — blocking for the "every reported wrong expectation" criterion:** the
CR16 anchor-drift omission in §2. The errata says "Wrong expectations were
repaired" (`:1712`); 8/9 were.

**F3 — minor: 7 of the 13 "Snapshot line" pointers are off.** Actual changed
lines from `git diff -U0 e69b488 c699c8c -- SKILL.md` vs the table:

| Row says | Actual | Δ |
|---|---|---|
| 61 | 63 | +2 |
| 269-270 | 271-272 | +2 |
| 277-279 | 278-280 | +1 |
| 360-361 | 361 | start one early |
| 513-515 | 514-515 | start one early |
| 949-950 | 950 | start one early |
| 1388, 1392 | 1390, 1393 | +2 / +1 |

15, 134-135, 505, 925, 1472, 1614 are exact. The "Was" text is findable by
grep, so this is non-blocking, but a `Snapshot line` column that names the
wrong line undercuts the table's purpose.

**F4 — minor: `git show 97cf436b…` is not a git object.** `97cf436b…` is the
sha256 of the content; `git cat-file -t 97cf436b669…` → `fatal: Not a valid
object name`; `git rev-parse e69b488:SKILL.md` → `0926115…`. The old wording
is retrievable with `git show e69b488:SKILL.md` (or from the committed
`coldread/SKILL.snapshot.md`). The claim "old wording stays in git" is true;
the command given is not.

**F5 — minor: "kept as named debt in the ledger" is not what the ledger
does.** Every generated entry carries `minor_gaps` **as an integer count** plus
a `reports` path, not the gap text (`assemble.py` merge; sample entry
`{"start":58,…,"wrong_expectations":1,"minor_gaps":1,"reports":[…/CR02.md]}`).
With the ledger absent at this commit (F1) there is no ledger debt at all; when
generated, the debt is in the named reports, not "named" in the ledger.

**F6 — minor/temporal: "repaired and new sections were re-read in wave 2"
(`SKILL.md:1784`, also SHONEN "repaired and re-read") is anticipatory at
`c699c8c`.** Commit time is `2026-10-20 10:49:37 -0300`; the w2 directory first
appears at `10:51:34` (files from `10:52`), and the committed report set
contains no w2 report. Assembling
both skills over w1 reports alone → exit 1, `51/65` units covered, missing
exactly the 11 repaired + 3 new sections. The statement becomes true only when
the wave-2 re-reads land and the ledger is committed; it is not true at the
revision it is written into. (The task is wave 2, so this may be by design —
but it is a present-tense claim in a committed artifact.)

**F7 — minor residual inconsistency: the page still says "six-leg registry"
at `SKILL.md:1391`** while `nlegs=7` at HEAD and the errata's own row 925 says
"seven since round 16". The section is dated "(round 11, measured)", so it is
defensible as a historical row, but the errata dated the adjacent mutation-case
count in the same table and did not date this one. Likewise
`SKILL.md:1345-1346` still quotes the round-7 text "Four legs at this
revision" while `:925` now reads "Four legs at that revision (r7-1; seven
since round 16)" — a historical quote, no longer an exact quote of the live
line.

**F8 — minor attribution: row `1388, 1392` credits CR23 for both halves.** CR23
reported the `plans/round-11-record-draft.md` pointer (minor gap, `CR23.md:69`);
it did not report the "(six)" count as wrong — it measured six and found it
correct at that revision. The "(six)" dating is the round-16 seventh-case
consequence, not a CR23 finding. The repair is still true.

**F9 — minor/omitted: the intro's "Two mutation cases" is stale and was not
repaired or reasoned.** `SKILL.md:9-10` (snapshot and HEAD) says "Two mutation
cases are now measured — round 2 JS, round 3 bash". At HEAD the page records
seven cases; CRCritic2 F9 (`CRCritic2.md:95-98`) names exactly this as a stale
summary that a section-partitioned cold-read cannot see. CR01 (the seat for
lines 1–57) verified the two-case claim as true at the historical revision and
recorded `gap-minor`, so this is not in any seat's `wrong_expectations` array —
but it is a false present-tense page claim that the errata's own repair pass
touched (line 15 is the same paragraph) and left standing.

**F10 — minor/rule conflict: the in-place repairs contradict the page's own
append-only rule, and no exception is declared.** `SKILL.md:24` says "Errata
append-only; rejections kept", and `SKILL.md:1460-1461` says "Append-only to
the last line: nothing above this section was edited by this write". The
round-16 errata edited 11 existing sections, 9 of them above the
`### What stays open` section (start 1449) that carries the declaration.
CRCritic2 F12 (`CRCritic2.md:134-141`) showed the ledger's sha rule forces
in-place repair
and requires L1 to decide the exception in writing; the errata does neither,
while its own heading still says "(append-only)". The repairs are technically
what the box-3 protocol needs, but the rule conflict is unacknowledged.

## 5. Residual risk / verification gaps

- The errata's repairs are all true, but the cold-read's *protocol* soundness is
  outside this table: `CRCritic1` Q3/L1 (a `verified-record` on an instruction
  section can still be credited) and `CRCritic2` F4-F10 (revision pinning,
  replica incomparability, contamination) are not answered by the errata and
  are not repaired by it. The table does not claim they are; the box-3 claim
  depends on the wave-2 `measure.py`/`assemble.py` rules, not on this table.
- I did not execute the full 7-leg `--regression` at HEAD; `nlegs=7` and the
  receipt format are read from source. The 6-leg run reproduced by CR16 and
  the 7-leg `regression_case_git` call are consistent.
- I re-derived the D1/D3 failing sets with my own mutation driver; the 14
  shared count matches CR06's two unique pairs exactly.
- The ledger absence may be resolved by wave 2; if so, F1 downgrades to
  "temporal ordering" and F6 to "premature wording", but at `c699c8c` both are
  observable false/stale claims.

Report: .ufo/waves/round-16/w2/ErrataAudit.md

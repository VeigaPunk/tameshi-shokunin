# ContamA — contamination audit of wave-1 cold-read seats CR01–CR13 (round 16, wave 2)

**Verdict: holds.** None of the 16 seats (CR01–CR03, CR04a/b, CR05–CR10, CR11a/b,
CR12a/b, CR13) opened another seat's report, or any lane `LOG.md`/`SCORECARD.md`/
`SHONEN.md`/`reports/`/`corpus/lessons/` content. None used the `@defect` spec grammar.
No contamination changes a ledger verdict for §1–§668. The residual defects are
minor and listed below: four metadata-only listings of `.ufo/waves/` (one showed
sibling report filenames), one wave-context claim pulled into a report (CR10), an
unresolved conflict in the rule itself that split seats 2–2 on page-named `plans/` files, and
incomplete `opened` lists.

## Method (commands, exits)

- Seat briefs: `.ufo/waves/round-16/spec1.json` → `items[].prompt` for the 16 seats
  (ranges below), and `context` for the wave-1 contamination rule (quoted in §Rule).
- Reports: `git -C tameshi-shokunin show c699c8c…:.ufo/waves/round-16/w1/<seat>.md`. I
  parsed the last ```` ```json ```` block of each report: all 16 parsed. Byte-stability:
  `git diff --stat e69b488 c699c8c -- w1/CR0*.md w1/CR1[0-3]*.md` → empty (exit 0).
- Transcripts: `history://TameshiR16.<seat>` renders truncated one-liners, e.g.
  `history://TameshiR16.CR01` line 106 ends `ls -la .ufo/waves/round-16/ && …`. For
  full arguments and tool results I read the backing session JSONL it cites, read-only
  (`~/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_…/TameshiR16/TameshiR16.<seat>.jsonl`;
  this is not `agent.db*`, credentials or auth). Tool-call counts: CR01 37, CR02 51,
  CR03 43, CR11a 17, CR11b 13, CR12a 27, CR12b 27, CR13 32, and the rest in between.
- Scan 1: regex over every tool call's arguments for
  `LOG\.md|SCORECARD\.md|SHONEN\.md|plans/|reports/|corpus/lessons|\.ufo/waves|CR\d\d[ab]?|@defect|mutate-and-run|spec1|assignments1|record1`.
  Writes and validation reads of each seat's own report were excluded.
- Scan 2: the same path regex over every tool **result**. This catches greps, finds and
  listings that surfaced forbidden content.
- Scan 3: `@old|@new|@defect|mutate-and-run` over tool arguments, report text, and
  assistant text and thinking.
- Scan 4: every snapshot read (`read`, `sed -n`, `awk NR`, python slices). I compared
  the lines read with the assigned range and with what the range names.
- Page-direction test: snapshot (`git show c699c8c:.ufo/evidence/round-16/coldread/SKILL.snapshot.md`,
  sha256 `97cf436b…623580`, verified) was grepped for each forbidden name inside each range.
  Transitive naming was checked against the page-named note text the seat actually printed.
- Ledger effect: `assemble.py` from committed bytes (`git archive c699c8c
  .ufo/evidence/round-16/coldread .ufo/waves/round-16/w1 | tar -x` into scratch),
  `python3 .ufo/evidence/round-16/coldread/assemble.py --out $D/ledger.json .ufo/waves/round-16/w1/CR*.md`
  → `coverage: 51/51 sections covered`, exit 0. The resulting ledger sha256 is
  `702b058d…57795f31`. This is my local assembly with no overrides; no `ledger.json` is
  committed at c699c8c.
- Scratch: `/tmp/tameshi-r16w2-ContamA-1hSNlG`. No installs. No lane writes except this report.

## Rule (wave 1, spec1.json `context`)

> read the snapshot …, only your assigned line range plus any file, command or URL your range
> explicitly names (and files those name, transitively, only as needed). Never open LOG.md,
> SCORECARD.md, SHONEN.md, plans/, reports/, corpus/lessons/, .ufo/waves/, other seats' reports,
> or this wave context's claims as evidence.

The wave-1 context also carried the C1 pins (`364f1d5…`, `f890e277…`, `60/60`) and the
`@defect/@old/@new` spec grammar. Both are wave-context material that seats were not
to use as evidence.

## Findings: forbidden-pattern opens

| # | Seat · call | What was opened | Page-named? | Class | Ledger verdict affected |
|---|---|---|---|---|---|
| 1 | CR01 [30] | `ls -la .ufo/waves/round-16/` (inside `mkdir -p … w1`). Output: `assignments1.json dispatch1.json record1.json spawn1.json spec1.json w1/`. Names only; no file read. | no | **contamination, metadata-only**. Not listed in `opened`. | none (§1/6/17/30 gaps come from note anchors) |
| 2 | CR02 [1] | `ls -la .ufo/waves/round-16/w1/`. Output: only `swarm-registry.json`. | no | **contamination, metadata-only**. Declared in `opened` ("directory listings"). | none |
| 3 | CR05 [17] | `ls -la .ufo/waves/round-16/w1`. Output listed sibling reports `AttrRecon.md CR11a.md CRSource2.md MistakeScribe.md PITSource.md RGControl.md RGSource2.md SurveySource.md` with sizes. No later call touches any of them (scan 1: no other-seat path in any CR05 argument). | no | **contamination, metadata-only**: saw another seat's report *name*, not its content. Not listed in `opened`. | none (§246 wrong-expectations come from byte-level mutant shas and token counts) |
| 4 | CR10 [1] | `ls -la .ufo/waves/round-16/w1/`. Output: only `swarm-registry.json`. | no | **contamination, metadata-only**. Not listed in `opened`. | none |
| 5 | CR02 [18][20][21][23][26][28][32][36][38] | Fleet and sibling files: `/…/shokunin/.ufo/waves/kaidoku-r5/01-audit-A.md:12-14`, `02-audit-B.md:110-119`, `.ufo/waves/shokunin-train-20261014-w8/closeout.json:35-38`, `w7/closeout.json:35`, `kaidoku-shokunin/SCORECARD.md:30-42` plus history `b04b19e:SCORECARD.md:37` and `c265db9`, `game-dev-2d-shokunin/reports/round-68/r68-verifier.md:1-13`; plus `kagi/SCORECARD.md` fed to `claim-ledger.sh` inside a /tmp `git archive` ([40]–[42]). | **yes, transitively.** Snapshot :64/:81/:85/:88/:92 cite `verification-patterns-fleet.md:24-35,50-52,59-61,69-74`. That text, printed in CR02 [7], names `.ufo/waves/kaidoku-r5/01-audit-A.md:12`, `02-audit-B.md:13-14`, `kaidoku-shokunin/SCORECARD.md:37`, `r68-verifier.md:1-5,11-23`, `…-w8/closeout.json:37` and `w7/closeout.json:35`. | **page-directed.** These paths are outside the lane, so they match the forbidden list only by name. Minor overreach: `02-audit-B.md:110-119` lies outside every line the note cites (:13-14, :36, :41, :78, :93), and [27] ran a fleet-wide `find -name 01-audit-A.md` (names only). | none (§58's one wrong-expectation is kagi exit-2 and usage-64 behaviour, from `claim-ledger.sh --bogus-flag` → 2) |
| 6 | CR06 [6][14] | lane `plans/round-2.plan.md:1-12` | **yes**: snapshot :331 cites `plans/round-2.plan.md:8-9` | **page-directed**. CR06.md:10 states the exception. | none (§314's wrong-expectation comes from the D1/D3 re-run, 14/16 cases shared) |
| 7 | CR08 [7][13] | lane `plans/round-3.plan.md:1-16`, plus `ls plans/` (lists all lane plan names) | file **yes** (snapshot :411 cites `plans/round-3.plan.md:8-9`); the listing **no** | file: **page-directed**. Listing: **contamination, metadata-only**, not in `opened`. | none (§405 is gap-minor from four other minor gaps) |
| 8 | CR13 [22] | `grep -rn 'aae45531' plans/` in **tsukuroi-shokunin**. Hit: `plans/round-5-record-draft.md:445`. | **yes, transitively.** Snapshot :755 names `aae45531`. The page-named note `mutation-case-tsukuroi-census.md:21` (printed in CR13 [6]) cites `tsukuroi-shokunin/plans/round-5-record-draft.md:323-324`. | **page-directed**, with an over-wide search scope: grep read the whole tsukuroi `plans/` directory, though output came from the named file only. Sibling path, so it matches the forbidden list by name only. Declared in `opened`. | none (it feeds one §668 minor gap; two others remain) |
| — | CR09 [22] | created dummy `LOG.md`, `SCORECARD.md` and `SHONEN.md` inside the /tmp `audit-root` fixture | n/a | not an open: fixture files used as gate inputs | none |

No seat opened lane `LOG.md`, `SCORECARD.md`, `SHONEN.md`, `reports/` or `corpus/lessons/`.
No seat opened any other seat's report (scan 1: zero other-seat paths in any argument),
nor `spec1.json`, `assignments1.json` or `record1.json`. Scan-2 hits outside the table
are mentions only: forbidden paths printed inside page-named notes (e.g. `LOG.md` in
`mutation-case-kagi-census.md`, `.ufo/waves/kaika-w1/…` in `corpus/README.md` for CR07).
The others are gate stdout (`corpus/lessons/round-13.md:102` from kagi
`claim-ledger.sh` in CR02 [40]/[44]) or sibling `git ls-files` names (CR08 [11], CR10 [23]).

Side note, not contamination: CR03 [38] edited `.ufo/waves/round-16/cr03.md` (wrong
case, missing `w1/`) and got "File not found"; [39] retried the correct path. No
stray file was created.

## Findings: wave-context claims and `@defect` grammar

- **CR10 used a wave-context claim (contamination, low impact).** CR10 [41] ran
  `git cat-file -e 364f1d5954158ef8844bca4a5fef57b05d2f2ca5^{commit}` and
  `git show 364f1d5…:scripts/round-gate.mjs | sha256sum` → `f890e277…a834d3e9`.
  CR10.md:51 then says round-gate HEAD is "byte-identical to the `364f1d5` blob pinned
  for C1's ledger leg"; the JSON `commands_executed` line 121 repeats it. The rev
  `364f1d5` appears nowhere in the lane outside wave-produced evidence:
  `git grep -n 364f1d5 e69b488 -- . ':!.ufo/waves'` → only
  `.ufo/evidence/round-16/round-gate/predictions.json:4` and `round-gate.defects.spec:2`.
  It is absent from snapshot 497–526 and from every note CR10 opened. The blob sha
  *is* page-reachable (`gates-survey-kumitate.md:353`).
  - Ledger effect: none. §497's two wrong-expectations are "22 vs 23 denied verbs"
    (`claim-ledger.sh:164` at kagi `c2cab35`) and "exit-2 arms asserted"
    (`surface-probe.mjs:1340-1347`, `cite-check.mjs:2334-2343`). Neither uses the pin.
  - Remediation: do not count CR10.md:51/121 as independent cold-read evidence for C1.
- **`@defect` grammar: none used.** Scan 3 found no `@defect` in any tool argument,
  authored file or report of the 16 seats. No seat opened `tools/mutate-and-run.sh`, and
  none needed it: the first snapshot mention is :829, outside every range ≤ 793.
  - All drivers were page-shaped Python tuple manifests `(id, site, old, new)`, following
    snapshot :560 (Appendix A) and :639–648 (Appendix B). Authors: CR04a, CR04b, CR06,
    CR11a, CR11b, CR12a, CR12b and CR13.
  - The token `@old` appears only as vocabulary: CR04a.md:133 minor_gap ("caught my own
    non-unique @old") and CR06/CR13 thinking. The range text says `` `old` `` without
    `@`, so this is a terminology leak from the wave context, not grammar use.
  - CR05's thinking reasons that "`tools/mutate-and-run.sh` exists per Context". It
    then *declines* to use it and records "driver path is unnamed" as a page minor gap.
    That is page-faithful.

## Out-of-range snapshot reads (range rule, not on the forbidden list)

| Seat · call | Lines read beyond range | Page-named? | Declared in `opened`? |
|---|---|---|---|
| CR03 [3] | 88–93, 131–140 (`awk NR>=88&&NR<=140`) | no | no (path only, no range) |
| CR04a [12], CR04b [3][7] | 246–313 | **yes**: :163 "entry template in the next section" | CR04a yes; CR04b path only |
| CR04b [24] | 375–404 | **yes**: :229 "Full checklist below (Restore discipline)" | path only |
| CR05 [1] | 230–245, 314–330 (`sed -n '230,330p'`) | no | **no** (`opened` says 246-313) |
| CR08 [38] | 466–467 | no (boundary) | no |
| CR12a [3], CR12b [3] | 527–593; CR12b also 520–526 | 527–593 **yes** (:626 "same as Appendix A"); 520–526 no | yes |
| CR06 [1], CR11a [2], CR12a [4], CR10 [3], CR08 [2] | heading-index greps only | — | CR06 yes; others no |

None of these feed a ledger verdict. CR05's 230–245 window ends before recipe step 5,
which is consistent with its "step 5 not read" minor gap.

## Rule conflict: page-named `plans/` files split the seats 2–2

The rule both allows "files your range explicitly names" and forbids `plans/`. On
page-named `plans/` files the seats split 2–2:

- **opened**: CR06 (`plans/round-2.plan.md`, :331) and CR08 (`plans/round-3.plan.md`, :411).
- **refused**: CR01 for the same `plans/round-3.plan.md` (named at :49), recording a
  minor gap (CR01.md JSON §30). CR13 for `plans/round-5.plan.md` (named at :684),
  recording a minor gap (CR13.md:25, 58-59, JSON §668).

Ledger effect (local assembly). The rule produced one minor gap in each of three
sections, and no verdict flips:

- §30 `gap-minor`, mg=3: two non-rule gaps remain (glyph variance, provenance date).
- §668 `gap-minor`, mg=3: two remain (aae45531 uncommitted; forward-looking items).
- §1 `gap-minor`, mg=1: the only gap is "rank not re-checked: SHONEN.md excluded".
  The page does not name `SHONEN.md` (snapshot :1-5), so this refusal is correct, and
  the gap is a real unanchored record claim, not contamination.

CR06 and CR08 would not flip either if they had refused: §314 stays wrong-expectation
and §405 stays gap-minor.

**Smallest remediation:** one sentence in the next cold-read contract: "a forbidden
path that your range names explicitly by path:line may be opened at those lines and
must be listed in `opened`". Alternatively, forbid it outright and require the
refusal to be logged as a rule-induced gap rather than a page gap. Either choice
removes the 2–2 split. Also require directory listings to be listed in `opened`; four
seats (CR01, CR05, CR08, CR10) omitted theirs.

## Ledger impact summary (sections in scope)

| start | local ledger verdict | seats | contamination touching it | verdict changes? |
|---|---|---|---|---|
| 1, 6, 17, 30 | gap-minor ×4 | CR01 | #1 listing; §30 has one rule-induced gap (refused page-named plan) | no |
| 58 | wrong-expectation | CR02 | #2 listing; #5 page-directed fleet files | no |
| 94 | gap-minor | CR03 | out-of-range read 88–93/131–140 | no |
| 131 | gap-minor | CR04a, CR04b | page-directed read of 246–313/375–404 | no |
| 246 | wrong-expectation | CR05 | #3 listing (saw `CR11a.md` name); undeclared 230–330 read | no |
| 314 | wrong-expectation | CR06 | #6 page-directed `plans/round-2.plan.md` | no |
| 375 | gap-minor | CR07 | none | no |
| 405 | gap-minor | CR08 | #7 page-directed plan; `ls plans/` listing | no |
| 466 | gap-minor | CR09 | none (fixture names only) | no |
| 497 | wrong-expectation | CR10 | #4 listing; wave-context C1 pin at CR10.md:51 | no |
| 527 | gap-minor | CR11a, CR11b | none | no |
| 594 | gap-minor | CR12a, CR12b | page-directed Appendix A read | no |
| 668 | gap-minor | CR13 | #8 page-directed tsukuroi `plans/` grep; one rule-induced gap | no |

Severity: low across the board. Exploit path (theoretical): CR05 [17] shows that a
seat finishing late would have seen the names of earlier seats' reports, and could
then open them. Nothing in the rule enforces otherwise. The smallest fix is to
pre-create the report directory for seats, so they never need to `ls`/`mkdir` under
`.ufo/waves/`, or to point seats at a write-only path.

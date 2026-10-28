# T54W1Read04 — cold read of `## The leg ledger — replay, receipt, and how it is read (round 7, measured)`

- Seat: T54W1Read04 (hyaku run 11, round 54, wave 1, leaf member — no subagent dispatch).
- Read revision (cand): `59c38109bf119d0e9d4f878644a82babc937bc1e` (C0).
- Base revision: `d33053f7552db4bd290c99a36979760f544c41ad`.
- Section span at C0: lines 932-944 (the frozen `sectionize` reports `start` 932, `end` 945, and strips the trailing blank line before the next heading).
- Section sha256 at C0: `430dd86f25b6ce3d5ed51012d54de7cdad7213c6353eb7701323de762b9fb993`.
- Findings: **none** (empty list in `T54W1Read04.json`). Every rule names an anchor that resolves at C0, every count recomputes, and no sentence in the section contradicts another. What was opened and what was checked is below, claim by claim.

## 1. How the section bytes were obtained (never a working-tree read)

```
$ python3 .ufo/waves/round-54/reader-section.py \
    /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    59c38109bf119d0e9d4f878644a82babc937bc1e \
    "## The leg ledger — replay, receipt, and how it is read (round 7, measured)"
{"heading": "## The leg ledger — replay, receipt, and how it is read (round 7, measured)", "cand": "59c38109bf119d0e9d4f878644a82babc937bc1e", "start": 932, "end": 945, "section_sha256": "430dd86f25b6ce3d5ed51012d54de7cdad7213c6353eb7701323de762b9fb993"}
```

The sha was reproduced independently from the git blob with the frozen rule (heading line through the line before the next heading, trailing blank lines stripped, `\n`-joined, no trailing newline):

```
$ git show 59c38109bf119d0e9d4f878644a82babc937bc1e:SKILL.md   # lines 932-944, joined per sectionize
sha256 430dd86f25b6ce3d5ed51012d54de7cdad7213c6353eb7701323de762b9fb993
lines 13  first: ## The leg ledger — replay, receipt, and how it is read (round 7, measured)
```

Two structural facts that matter to the re-read set, neither of them a defect of this section:

- The section bytes at base `d33053f` and at C0 are identical: `reader-section.py` prints the same `section_sha256` (`430dd86f…`) at both revisions; only the span moves (base 924-937, C0 932-945) because C0 adds the eight-line `## Standing rules` bullet at `SKILL.md:32-39`, which shifts every later line.
- The C0 monitor's own reason for uncrediting this heading is `input-drift:corpus/SOURCES.md`, not a change to the section text:

```
$ python3 .ufo/evidence/round-21/coldread/measure.py --repo <lane> --rev 59c38109bf119d0e9d4f878644a82babc937bc1e
{"heading": "## The leg ledger — replay, receipt, and how it is read (round 7, measured)", "start": 932,
 "credited": false, "reason": "input-drift:corpus/SOURCES.md"}
```

  C0 is the commit that adds S277-S279 to `corpus/SOURCES.md`; the section itself is byte-identical to base. That is exactly the drift the contract describes ("this round's own edits drifted inputs"), and it is not a textual defect the section can fix.
- The section's own anchors are revision-pinned (`@9f1d3c3`, `4b7c682`) or name a path (`corpus/knowledge/fleet-kill-rate-ledger.md`), so an eight-line insertion elsewhere in `SKILL.md` cannot move them.

## 2. Claim-by-claim cold read, with the artifact opened for each

Each quote below is a byte-exact substring of the section (verified in §3).

| # | Claim (quoted) | Artifact opened | What it shows |
|---|---|---|---|
| 1 | ``Round 7 recorded four legs at`` | `git show 9f1d3c3:tools/mutate-and-run.sh \| sed -n '72,109p'` | Header line 72 reads `# --regression (r4-2; r7-1 leg ledger)`; lines 75-78 name exactly four legs: `js-kimi-census 8/10 (80 %)`, `bash-surface-census 8/10 (80 %)`, `bash-tsukuroi-census 6/10 (60 %)`, `bash-mado-verify 4/10 (40 %)`. Lines 92-97 state those rates are the leg's expectation (exact: 0 flips, killed-delta 0). |
| 2 | ``(r2, killed 8/10 = 80 %), `bash-surface-census` (r3, 8/10 = 80 %),`` | same range, plus `corpus/knowledge/fleet-kill-rate-ledger.md:45-48` at C0 | Ledger §1 rows carry `(r2) … 8/10 (80 %)`, `(r3) … 8/10 (80 %)`, `(r5) … 6/10 (60 %)`, `(r6) … 4/10 (40 %)`; the section's round labels and rates match cell for cell. |
| 3 | ``(`tools/mutate-and-run.sh@9f1d3c3:72-109`, `:511-522`; at round 18 (runner `4b7c682`) the recorded tables sit at `:597-620`).`` | `git cat-file -t 9f1d3c3` / `4b7c682`; `git show 9f1d3c3:tools/mutate-and-run.sh \| sed -n '511,522p'`; `git show 4b7c682:tools/mutate-and-run.sh \| sed -n '597,620p'` | Both revisions exist and are ancestors of HEAD. At 9f1d3c3, `:511-522` is exactly `PIN_JS`/`REV_JS` … `TABLE_MADO` — the four legs' pins and tables, and the tool blob is `cf41efaa8be5f52d…` (the r7-1 runner). At 4b7c682, `:597-620` is `PIN_JS` … `TABLE_SOURCESCHECK` — eight legs' pins and tables; that commit's tool blob is `d22c4025e8ce38b8…`, the round-18 runner (corroborated by `.ufo/waves/round-18/w2/CR14.md` `REGRESSION_TOOL … sha256=d22c4025…` and `RerunC1.md` `REGRESSION: PASS (cases=8 passed=8…)`). |
| 4 | ``eight ledger rows — six in the §1/ER-2 table plus the round-16 and round-18 appends`` | `corpus/knowledge/fleet-kill-rate-ledger.md` at C0 (`:45-48`, `:276-277`, `:403-410`, `:424-432`) | §1's table has four numbered rows (1-4); ER-2's appended table has two (5-6) → six. `## Round 16 — seventh row appended` adds one row, `## Round 18 — eighth row appended` adds one → eight. No ninth or tenth row exists anywhere in the file. |
| 5 | ``the ninth and tenth cases, cite-check and drift-pins, are recorded in their own notes, not as ledger rows`` | `corpus/knowledge/mutation-case-kumitate-cite-check.md` and `corpus/knowledge/mutation-case-kagi-drift-pins.md` at C0 | Cite-check note is headed `# Mutation case 9 — kumitate `scripts/cite-check.mjs` (round 26)` and its recheck line records `REGRESSION: PASS (cases=9 passed=9 …)`. Drift-pins note is headed `# Mutation case 10 — kagi `corpus/drift-pins.sh` (round 51)` and the ledger's Round-52 block (`:439-441`) records it as `recorded case 10`. Neither has a row in the ledger's rate tables; cite-check's only ledger appearance is the §2 probe row (`:94`, "a probe, **not a sweep**") and drift-pins' only footprint is that §3 cell supersession — so "not as ledger rows" holds. |
| 6 | ``seven from round 16, eight from round 18, nine from`` / ``round 26, ten from round 51) — `js-kimi-census``` | ledger `:403-413` (Round 16 receipt `cases=7`), `RerunC1.md` (cases=8), cite-check note (`cases=9`, round 26), ledger `:441` (round 51, `cases=10`) | The milestone series counts runner legs/cases: 7 at round 16, 8 at round 18, 9 at round 26, 10 at round 51. Read that way it is consistent with the final clause's eight *rows* (rows never reached nine or ten, and the clause says so); the section's own two sentences supply the legs/rows distinction, so there is no self-contradiction to report. |
| 7 | ``is the receipt tameshi's records cite for kill-rate claims`` | `git grep -c fleet-kill-rate-ledger -- SKILL.md corpus` at C0 | 102 references; e.g. `SKILL.md:1009`, `:1026`, `:1096`, `:1098` all cite this ledger for rate/reading claims, so "the receipt records cite" is substantiated rather than asserted. |
| 8 | ``the tool's two-case self-check`` | ledger §5 (`:162-169`) at C0; `git merge-base --is-ancestor 4494715 9f1d3c3` | §5 records the pre-r7-1 `--regression` pulse as `cases=2 passed=2` at tool `b56c6e57…`; 4494715 (the revision carrying that tool) is an ancestor of r7-1, so "two-case … into the leg ledger" is the right before/after. The phrase is loose ("self-check" for a two-leg replay) but no artifact contradicts it, so it is not filed. |

Non-defects checked and dismissed rather than reported:

- "six in the §1/ER-2 table" is compressed shorthand for §1's four rows plus ER-2's two; both tables exist and the arithmetic is 4+2=6. A reader who follows the pointer reaches both tables.
- No table lives inside this section, so no table cell can be stale; the only rate cells it names are in the ledger and they match (row 3 of the table above).
- Heading says "(round 7, measured)" while the section narrates through round 51; that is the section's origin label, and its content (round-7 legs plus dated later milestones) does not claim to be round-7-only.

## 3. Byte-exactness check of every quoted fragment in this file

Run after writing, over the canonical section text reproduced in §1:

```
quoted fragments: 9
byte-exact in section: 9 / 9
byte-exact in MD     : 9 / 9
```

(Each of the nine quoted fragments in §2 was matched with `fragment in section_text` against `430dd86f…`'s bytes and with `fragment in md_text` against this file; the check is the one printed, no other normalization.)

## 4. Bounds observed

- Read-only outside the deliverables: the lane's `SKILL.md`, `tools/mutate-and-run.sh`, `corpus/knowledge/fleet-kill-rate-ledger.md` and the two case notes were read through `git show`/`git grep` only; no lane file, counter, contract, freeze, ledger, wave spec or registry was edited.
- Only writes: `.ufo/waves/round-54/w1/T54W1Read04.json` and this file, both inside the seat's write scope.
- Scratch: `export HYAKU_SCRATCH=/fast/scratch/hyaku`; tree `$HYAKU_SCRATCH/tameshi-r54/T54W1Read04/`; removed at seat exit (the counter run used `--work` under that tree, so no scratch survives).
- Tools installed/upgraded: none (no install was needed; pacman transactions are paused host-wide and no channel was touched).
- No mutating git/jj command was run anywhere.

## 5. Result for the judge

`findings` is empty and that is the result: the section's four anchors resolve at their pinned revisions, its counts (eight rows = 4+2+2; four legs; 8/8/6/4 of 10 = 80/80/60/40 %) recompute exactly against the ledger and the pinned runners, its ninth/tenth-case attribution is right, and no sentence in the section contradicts another. The heading's loss at C0 is input drift on `corpus/SOURCES.md` (the C0 S277-S279 edit) over byte-identical section text, not a textual defect.

# T53W2Read16 — wave-2 re-read of `### The map — where a reader enters, artifact by artifact`

Seat: reader, round 53 wave 2 (C1 cold-read re-read of the sections fixed in fix pass 2).
Read at **C\*\*** = `5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e` via git objects only
(`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show C**:SKILL.md`); the working tree was
never read for section content. Wave-1 reader of this section: `.ufo/waves/round-53/w1/T53W1Read21.{json,md}`
(three findings at C\* = `a41195dfc13a73958e4c5228ec196b28d03ded03`).

## Section split and hash (verified before hashing)

Split exactly as the frozen monitor defines it: lines of `SKILL.md` at C\*\*, heading = first line
matching `^#{1,3}(\s|$)` **outside fenced blocks**, section = heading line through the line before the
next heading, trailing whitespace-only lines stripped, joined with `\n`, no trailing newline,
sha256 over UTF-8 bytes with `surrogateescape`.

```
$ git -C <lane> cat-file -t 5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e
commit
$ git -C <lane> show 5b703c6…:SKILL.md | wc -l
2189                      # 2189 newline-terminated lines; split() yields 2190 elements, last ''
$ git -C <lane> show 5b703c6…:SKILL.md | grep -n '^### The map — where a reader enters'
1396:### The map — where a reader enters, artifact by artifact
next heading, byte-verified:
1412:### Boundary readings, executed by this lane
```

Fence audit: 20 fence-toggle lines, ending closed; the last toggle before line 1396 is at 1186
(closing state), the next is at 1418 — so the heading at 1396 sits outside any fence and is a real
heading.

Section bytes: lines **1396–1411** (line 1411 is blank and stripped as a trailing whitespace-only
line) → 15 lines, **3834 bytes**, no trailing newline.

```
$ git -C <lane> show 5b703c6…:SKILL.md | awk 'NR>=1396 && NR<=1411' | python3 -c \
    "import sys,hashlib; d=sys.stdin.buffer.read(); print(repr(d[-30:])); d=d.rstrip(b'\n'); \
     print(len(d)); print(hashlib.sha256(d).hexdigest())"
b' | provenance of any round |\n\n'
3834
30d62e79a81d8e6dfcfc9076f0977b1e14016d527f5fd78e66aab407bd370bea
```

Second, independent computation (python over `text.split("\n")`, lines 1396–1411, same strip rule)
reproduces `30d62e79a81d8e6dfcfc9076f0977b1e14016d527f5fd78e66aab407bd370bea`.
Recorded in `T53W2Read16.json`.

## Fix verification (run first) — the three re-anchored citations

The C\* → C\*\* difference over this section is **exactly three table rows** and nothing else.
Method (`python3`, `difflib.unified_diff`, `n=0`): extract the section from each revision with the
same fence-aware split rule, diff the two line lists. Output, abridged to the changed text only:

```
-| `corpus/knowledge/operator-runbook.md` | … (`SKILL.md:1294-1297`); §7's default scratch …
+| `corpus/knowledge/operator-runbook.md` | … (the runbook §'s "Pointer, not a second home" bullet); §7's default scratch …
-| `corpus/knowledge/fleet-kill-rate-ledger.md` | … have no row yet — the tenth's only record is the §3 cell supersession at …
+| `corpus/knowledge/fleet-kill-rate-ledger.md` | … have no row — the ninth lives in … and the tenth's only ledger footprint is …
-| `corpus/knowledge/service-limits.md` | … compact rendering (`SKILL.md:1246-1270`) | …
+| `corpus/knowledge/service-limits.md` | … compact rendering (the `### The service's limits — what tameshi refuses to mutation-test` section's table) | …
```

### Fix 1 — runbook bullet (was `SKILL.md:1294-1297`)

The stale number is gone. The clause at C\*\* reads, byte-exact:

> (the runbook §'s "Pointer, not a second home" bullet)

Resolution at C\*\*: the named bullet exists, verbatim, in SKILL.md's runbook section
`### The operator's runbook — corpus/knowledge/operator-runbook.md` (heading at 1296), at 1309–1311:

```
$ git -C <lane> grep -n -F 'Pointer, not a second home' 5b703c6… -- SKILL.md
1309:- **Pointer, not a second home.** Its own rule: where it and an anchored
1400:| `corpus/knowledge/operator-runbook.md` | … (the runbook §'s "Pointer, not a second home" bullet); …
```

Two hits, and only two: the bullet at 1309 and this very table row at 1400 quoting it (the 1400
line is abridged with `…` in this transcript; the grep prints it whole). The bullet's lines
(python extraction of `SKILL.md` at C\*\*):

```
1309:- **Pointer, not a second home.** Its own rule: where it and an anchored
1310:  source diverge, the anchored source governs — the same rendering/divergence
1311:  rule this page applies to `service-limits.md` (`:1250-1254`).
```

The rule text matches the row's paraphrase ("where it and an anchored source diverge, the anchored
source governs"). Outside prior `.ufo/waves/` reports (which quote it), `git grep -l -F` at C\*\*
finds the phrase in `SKILL.md` and four frozen round-16 evidence snapshots
(`.ufo/evidence/round-16/coldread/…`) — no other live surface. **Fix holds.**

### Fix 2 — service-limits section (was `SKILL.md:1246-1270`)

The clause at C\*\* reads, byte-exact:

> (the `### The service's limits — what tameshi refuses to mutation-test` section's table)

Resolution at C\*\*: heading at 1257, byte-identical to the cited text, and the section's table runs
1271–1282 with all ten refusal rows `a`–`j` (the old range ended at row `g`):

```
$ git -C <lane> show 5b703c6…:SKILL.md | sed -n '1257p;1271p;1282p'
### The service's limits — what tameshi refuses to mutation-test
| # | Refusal | What it means | Anchor |
| j | Foreign scratch | never removed | `service-optin-protocol.md:86-91` |
```

Heading-based citation cannot drift with line shifts, and the ten-row table it names is complete.
**Fix holds.**

### Fix 3 — tenth-case record (was "the tenth's only record is the §3 cell supersession at …")

The clause at C\*\* reads, byte-exact:

> the ninth lives in `corpus/knowledge/mutation-case-kumitate-cite-check.md` and the tenth's only ledger footprint is the §3 cell supersession at `fleet-kill-rate-ledger.md:439`

Resolution at C\*\*:

- `corpus/knowledge/mutation-case-kumitate-cite-check.md` exists (128 lines, `wc -l`) and is the
  ninth case; its line 6 reads, byte-exact:

  ```
  # Mutation case 9 — kumitate `scripts/cite-check.mjs` (round 26)
  ```
- `fleet-kill-rate-ledger.md:439` is the supersession block heading —
  `## Round 52 — §3 drift-pins cell superseded (2026-10-27)` — with the bullet at 441 recording the
  round-51 measurement and naming the case entry `corpus/knowledge/mutation-case-kagi-drift-pins.md`.
- "only ledger footprint" is the narrowed claim and it holds: `grep -n drift-pins` over the ledger
  at C\*\* returns exactly `:119` (the §3 queue cell that says `unmeasured by sweep; hermetic`, i.e.
  the cell being superseded — not a record of the case), `:439` (the block heading) and `:441` (the
  supersession bullet itself). `:280` names an earlier supersession of the `claims-check`/
  `checklist-run` cells, cited at `:441` as precedent, and is not a drift-pins record. No rate row
  for the tenth exists, and the case's own note
  (`corpus/knowledge/mutation-case-kagi-drift-pins.md`, 222 lines) is outside the ledger, so it does
  not contradict a ledger-scoped "only".

**Fix holds.**

## Holds — every other pointer in the section, re-resolved at C\*\*

| Claim in the section (C\*\*) | Verification at C\*\* (git objects) | Verdict |
|---|---|---|
| runbook section map: §0 quick start · §2 tool · §3 six-case ledger · §4 opt-in · §5 limits · §6 cadence (tick, reading map, T1–T3) · §7 regression · §10 unknowns | `operator-runbook.md` headings: §0 35, §1 65, §2 93, §3 131, §4 180, §5 243, §6 269, §7 345, §8 408, §9 438, §10 462; §6 carries "The reading map" 277 and T1/T2/T3 at 288/290/293; title line 1 carries `(round 10, T10-1)` | holds |
| runbook §3 "six rows" | §3 table rows 1–6 at 149–154 (`The six measured cases:`) | holds |
| "nine cases since round 26, ten since round 51" | `git ls-tree -r C** corpus/knowledge/ \| grep mutation-case-` → **10** files; ninth note titled "(round 26)", tenth "(round 51)" | holds |
| "§7's default scratch still reads `mktemp -d /tmp/…` (`corpus/knowledge/operator-runbook.md:349-351`)" | 349: `` `SKILL.md:933-963`). Default scratch is a fresh `` / 350: `` `mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX`, removed on PASS unless `` / 351: `` `--keep`, kept on FAIL/SETUP, … `` | holds |
| "the runner honours `TMPDIR` (`tools/mutate-and-run.sh:149-150`)" | 149: `# "${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX" by default (r51 honours`; 150: `# TMPDIR); removed on PASS unless --keep,`; behaviour at 1432 `root=$(mktemp -d "${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX")` | holds |
| ledger "eight rows" | measured-gate rows: 1–4 at 45–48 (§1), 5–6 at 276–277 (ER-2), 7 at 410 (Round 16 block), 8 at 432 (Round 18 block) — eight, none for cases 9/10; §1 columns are `Gate · Suite · Kill-rate (composition) · Survivors · Hardened · Last sweep · target pin · driver` (43) | holds |
| "§1–§4 byte-frozen, new rows appended below" | appends live after §4 (160): ER-5 at 366, Round 16 at 403, Round 18 at 424, Round 52 at 439; the Round 52 block itself says "§3's table stays as written" | holds |
| `service-limits.md` = "the refusals, detail of record" | file present, title `# Service limits — what tameshi refuses to mutation-test, and why (T9-2, round 9)`, §1 decision table at 42 with rows a–j | holds |
| `service-optin-protocol.md` — §1 request shape incl. re-pin, §2 read-only, §3 owner-hardens, §4 report shape | §1 54 (re-pin at 62, 75), §2 109, §3 142, §4 182 | holds |
| `fleet-suite-census.md` — the census: the offer and the queue (surveyed-but-unmeasured pins) | §5 `Tameshi's standing service offer` at 249; "queue" cells at 305, 349; pinned queue table at 105–111 | holds |
| `service-standing-state.md` — fleet-visible vs lane-owned, handoff conditions, SC1–SC3 | §0 17, §1 49, §2 68, §3 80 (handoffs A–D 85/101/116/140); SC1 159, SC2 174, SC3 181 | holds |
| `mutation-case-*.md` "(dated: six at round 11; seven from round 16; eight from round 18; nine from round 26; ten from round 51)" | exactly 10 files; note titles carry (round 2/3/5/6/8/26/51 …) consistent with the milestones; round-16/18/26 notes carry "pre-registration" (2/3/2 hits) and verdict/survivor sections | holds |
| instrument `--selftest`, `--regression` "six-leg registry at round 11 … ten since round 51; git-materialized replay" | `tools/mutate-and-run.sh` 2159 lines (`wc -l`); ten `regression_case_git` legs at 1459–1508 (… `bash-drift-pins`); `local nlegs=10` at 1510; legs materialized by `git show` (`regression_case_git`), `--selftest` block at 159–160 | holds |
| `corpus/README.md` addendum shapes at `:125`, `:326`, `:614` | all three resolve to the addendum table header lines quoted under this table | holds |
| `plans/` round-2…round-11 plans, round-4…round-10 record-drafts, no round-11 record file, `plans/completion-evidence.md`, `corpus/knowledge/closeout-r11.md` | `git ls-tree -r C** plans/` = 10 plan files (2–11), 7 record-drafts (4–10), completion-evidence.md; no round-11 record-draft; closeout-r11.md present (424 lines, `wc -l`) | holds |
| "the wave deliverables are the record, `LOG.md:316-317`" | 316: `discharge. Same dispatch shape as rounds 1–10 — the lane deliverables in`; 317: `this repo ARE the wave record (no `.ufo/waves/tameshi-r11-*` directory);` | holds (the row's parenthesis paraphrases the log's wording) |
| `LOG.md`, `SCORECARD.md` — round rows + move-log rows with counting commands | `SCORECARD.md` 2499 lines (`wc -l`): Move log table at 7–9, and counting commands throughout (row headers `Counting command`, tables at 166, 654, 782, 867 …) | holds |

Anchor bytes for `corpus/README.md` (C\*\*, `git show`):

```
125:| Note / frontier | Lane-asserted scope; outside admission pending | Source / evidence |
326:| Entry / ground | Admission and exact scope | Evidence |
614:| id | ground | candidate sources | status | next falsifiable move (before → after) |
```

## Findings

**None.** Nothing in the section fails at C\*\*: the three named fixes are present in the C\*\* bytes
and each new anchor resolves; every `path:line` and count re-checked above resolves at the cited
location with the quoted content present.

## Observations (not scored — outside this section's claims)

1. **The phrase's home.** `(the runbook §'s "Pointer, not a second home" bullet)` resolves as written
   only if "the runbook §" is read as this page's runbook *section* (`### The operator's runbook — …`,
   1296). Read instead as a § inside `corpus/knowledge/operator-runbook.md`, it would not resolve:
   that file has no bullet by that name — it carries the same rule as bold prose in §5 at 247–249
   (`**This runbook restates with pointers — it is not a second home; on drift the anchored source governs**`).
   Scored as a hold because the bullet name appears in `SKILL.md` only twice (the bullet at 1309 and
   this row's own quote of it at 1400, which is not a competing referent), and the bullet sits in the
   section that documents the runbook.
2. **A stale anchor inside the cited bullet.** `SKILL.md:1311` cites `(`:1250-1254`)` for "the same
   rendering/divergence rule this page applies to `service-limits.md`"; at C\*\* 1250–1254 is the
   "what a re-sweep produces lands appended" bullet, and the rendering/divergence rule sits in the
   service-limits section intro at 1269 (`divergence between the two is the finding, never smoothed`).
   This is the neighbouring section's (`## The operator's runbook and the six-leg regression`) anchor,
   not a statement of this section, so it is not raised as a finding here.

## Limits and seat hygiene

- Content read from git objects only (`git show C**:<path>`); the working tree was never used for
  section content. Wave-1 `.ufo/waves/round-53/w1/T53W1Read21.{json,md}` was read for the fix list
  (read-only).
- Anchor checks read only the files/lines the section cites; no open-ended review of other documents.
- Line numbers are C\*\* numbers; a reader on another revision must re-resolve.
- No tool was installed or upgraded; no network access; no package manager run.
- No git/jj mutating command anywhere; no fixture or clone needed.
- Scratch `/fast/scratch/hyaku/tameshi-r53/w2/T53W2Read16/` held only the extracted `SKILL.md` and
  the section text, and was removed before yield.
- Writes: `.ufo/waves/round-53/w2/T53W2Read16.json` and `.ufo/waves/round-53/w2/T53W2Read16.md` only.

# T53W1Read21 — cold read of `### The map — where a reader enters, artifact by artifact`

Seat: reader, round 53 wave 1 (C1 cold-read re-read).
Read at content commit `a41195dfc13a73958e4c5228ec196b28d03ded03` (C*) via git objects only
(`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show C*:SKILL.md`); the working tree was
never read for this section.

- Section line range at C*: **1387–1401** (15 lines).
- Next heading after it: 1403 (`### Boundary readings, executed by this lane`); line 1402 is blank
  and was stripped as a trailing whitespace-only line.
- Section bytes: 3649 (UTF-8, surrogateescape), no trailing newline.
- `section_sha256` = `56faf129bad7bfce6649c19e99b4cc9981019a322e828c09fb74c21d52fd5333`.

Split verification (fence-aware heading scan, `^#{1,3}(\s|$)` outside ``` fences):

```
$ git -C <lane> show a41195dfc13a73958e4c5228ec196b28d03ded03:SKILL.md | grep -n '^### The map'
1387:### The map — where a reader enters, artifact by artifact
```

```
$ git -C <lane> show C*:SKILL.md | awk 'NR>=1399&&NR<=1404 {printf "%d|%s\n", NR, $0}'
1399|| `corpus/README.md` | the coverage map … 
1400|| `plans/round-N.plan.md` (latest `plans/round-11.plan.md`), …
1401|| `LOG.md`, `SCORECARD.md` | the round rows and the move-log rows with their counting commands | …
1402|
1403|### Boundary readings, executed by this lane
```

The hash was computed over exactly lines 1387–1401 joined with `\n` (trailing blank lines stripped),
which reproduces the heading's line range; the JSON records the same value.

## Holds — pointers verified against C* bytes

Every `path:line` claim in the section was resolved at C*, not in the working tree.

| Claim in the section | Verification at C* | Verdict |
|---|---|---|
| runbook section map: §0 quick start · §2 tool · §3 six-case ledger · §4 opt-in · §5 limits · §6 cadence (tick, reading map, T1–T3) · §7 regression · §10 unknowns | `operator-runbook.md` headings at 35 (§0), 93 (§2), 131 (§3), 180 (§4), 243 (§5), 269 (§6), 345 (§7), 462 (§10) | holds |
| "six rows; the lane has held nine cases since round 26, ten since round 51" | runbook §3 table = 6 rows (138–143); `git ls-tree C* corpus/knowledge/ \| grep mutation-case-` = **10** files | holds |
| `corpus/knowledge/operator-runbook.md:349-351` — "§7's default scratch still reads `mktemp -d /tmp/…`" | line 350: `` `mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX`, removed on PASS unless `` | holds |
| `tools/mutate-and-run.sh:149-150` — "the runner honours `TMPDIR`" | 149: `# "${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX" by default (r51 honours`; 150: `# TMPDIR); removed on PASS unless --keep,`; behaviour in code at 491 and 1432 (`mktemp -d "${TMPDIR:-/tmp}/…"`) | holds |
| ledger "eight rows" | rows 1–4 at 45–48 (§1), rows 5–6 at 276–277 (ER-2), row 7 at 410 (Round 16 block), row 8 at 432 (Round 18 block) — eight measured-gate rows, none for the ninth/tenth | holds |
| "the round-26 ninth and the round-51 tenth case have no row yet" | no ninth/tenth gate row anywhere in the ledger (last block is the Round 52 supersession at 439–441) | holds |
| `fleet-kill-rate-ledger.md:439` exists and carries the §3 drift-pins supersession block | 439: `## Round 52 — §3 drift-pins cell superseded (2026-10-27)`; the supersession bullet begins at 441 | holds as a block pointer (the bullet, not the heading, is the record — see finding 3) |
| `corpus/knowledge/service-limits.md` = the refusals, detail of record (T9-2) | file present, title `# Service limits … (T9-2, round 9)`, §1 "The decision table" at 42 | holds |
| `service-optin-protocol.md` — §1 request shape incl. re-pin rule, §2 read-only guarantees, §3 owner-hardens, §4 report shape | §1 at 54 (re-pin at 62, 75), §2 at 109, §3 at 142, §4 at 182 | holds |
| `fleet-suite-census.md` — the census, the offer and the queue (surveyed-but-unmeasured pins) | §5 "Tameshi's standing service offer" at 249 with the offer text and the ordered queue table (cite-check 62, surface-probe 42, round-gate 60, proxy-check 102, claims-check 39, kimi-census 43) | holds |
| `service-standing-state.md` — fleet-visible vs lane-owned, handoff conditions, SC1–SC3 | §1 at 49, §2 at 68, §3 at 80; SC1 at 159, SC2 at 174, SC3 at 181 | holds |
| `mutation-case-*.md` "(dated: six at round 11; … ten from round 51)" | exactly 10 `mutation-case-*.md` files at C*; dated milestone wording | holds |
| `tools/mutate-and-run.sh` — `--selftest`, `--regression` (six legs r11 … ten since round 51; git-materialized replay) | header 8–18 and leg roster 88–97 list ten legs (… `bash-drift-pins`); `local nlegs=10` at 1510; selftest readme block present | holds |
| `corpus/README.md` addendum shapes at 125 / 326 / 614 | 125: `| Note / frontier | …`; 326: `| Entry / ground | …`; 614: `| id | ground | candidate sources | status | next falsifiable move (before → after) |` | holds |
| `plans/round-N.plan.md` (latest `plans/round-11.plan.md`), record-drafts; no round-11 record file; `plans/completion-evidence.md`; `closeout-r11.md` | `git ls-tree C* plans/` = round-2…round-11 plan files, round-4…round-10 record-drafts, completion-evidence.md; no round-11 record-draft; `corpus/knowledge/closeout-r11.md` present | holds |
| "the wave deliverables are the record, `LOG.md:316-317`" | 316: `discharge. Same dispatch shape as rounds 1–10 — the lane deliverables in`; 317: `this repo ARE the wave record (no \`.ufo/waves/tameshi-r11-*\` directory);` | holds |
| `LOG.md`, `SCORECARD.md` — round rows + move-log rows with counting commands | both present at C*; SCORECARD 2499 L, states "Axes will be pinned with their counting commands as rounds land" with the Round/Axis/Before/After/Evidence table | holds |

## Findings

Three statements do not hold at C*.

### 1. Stale pointer — the runbook's divergence rule is cited at the wrong lines

Quote (byte-exact from the section):

> renderer, not a second home: where it and an anchored source diverge, the anchored source governs (`SKILL.md:1294-1297`)

Why it fails. At C* those four lines are the runbook's **Section map** bullet, which lists §0 · §1 ·
§2 … and contains no divergence rule:

```
1294|- **Section map.** §0 quick start (the operator loop in one block) · §1 the
1295|  service in one page · §2 the tool · §3 the six-case ledger · §4 the opt-in
1296|  protocol · §5 the limits · §6 the cadence (tick, reading map, triggers
1297|  T1–T3) · §7 the regression mode · §8 the operator's full loop (commissioning
1298|  to append) · §9 that lane's executed receipts · §10 unknowns carried ·
1299|  append-only errata.
1300|- **Pointer, not a second home.** Its own rule: where it and an anchored
1301|  source diverge, the anchored source governs — the same rendering/divergence
1302|  rule this page applies to `service-limits.md` (`:1250-1254`).
```

The rule the row asserts is at **1300–1302**, six lines below the cited range. A reader resolving
`SKILL.md:1294-1297` lands on the section map, not on the governance rule; by this page's own
standard ("a reader on a differing revision re-resolves rather than trusts") the anchor is stale.

### 2. Truncated range — the "compact rendering" pointer stops three refusal rows early

Quote (byte-exact from the section):

> the refusals, detail of record; this page carries the compact rendering (`SKILL.md:1246-1270`)

Why it fails. The compact rendering is: heading at 1248, intro paragraph 1250–1260, table header
1262, separator 1263, refusal rows `a`–`j` at **1264–1273**. The cited range begins mid-paragraph in
the *previous* section (1246 is the line `  assumed.`) and ends at row `g` (1270); rows `h`, `i`, `j`
are outside it:

```
1262|| # | Refusal | What it means | Anchor |
1263|---|---|---|---|
1264|| a | No pinned revision / no opted-in lane | …
…
1270|| g | Coordinated multi-edit rewrites | outside the defect vocabulary — no rate claimed | …
1271|| h | The exit-flatten family | a harness boundary — named, not fixed | `service-optin-proto…
1272|| i | A directed-repair re-run presented as a rate | recorded as directed repair, not an i…
1273|| j | Foreign scratch | never removed | `service-optin-protocol.md:86-91` |
```

So the pointer both starts early and truncates: the refusal table it names has ten rows, and the
range covers seven. Row `j` (foreign scratch) is exactly the refusal a reader following the §7
scratch divergence note in the same row would need.

### 3. Unsupported absolute — "the tenth's only record" is not its only record

Quote (byte-exact from the section):

> the tenth's only record is the §3 cell supersession at `fleet-kill-rate-ledger.md:439`

Why it fails. The round-51 tenth case carries a full case note at C* —
`corpus/knowledge/mutation-case-kagi-drift-pins.md`, 222 lines, with its pin/suite section (§0) and
verdict/survivor treatment — and that note is one of the ten `mutation-case-*.md` files the same
section's next row counts. The cited ledger block names it too, two lines below the cited anchor:

```
439|## Round 52 — §3 drift-pins cell superseded (2026-10-27)
441|- **§3 supersession (cell, not edit; round-8 precedent `:280`).** … round 51 measured kagi
    `corpus/drift-pins.sh` @ `e64e81b8` … ; entry `corpus/knowledge/mutation-case-kagi-drift-pins.md`.
```

So even inside the ledger the supersession cell is not the case's only record — the cell points at
the entry note — and the section's own mutation-case row contradicts a literal "only record". The
anchor `:439` also lands on the block heading; the supersession bullet is `:441`.

## What was checked and found clean (no finding raised)

- `/tmp` scratch divergence note: both sides verified verbatim at C* (runbook §7 line 350,
  runner header 149–150 plus the code at 491/1432). The statement "the runner honours `TMPDIR`"
  is literally true at C*; the section's governance conclusion ("by that rule the runner governs")
  is a stated judgement, not a factual claim, so it is not scored as a failure here. Noted for the
  judge: the runner's own default is `${TMPDIR:-/tmp}`, i.e. it still falls back to `/tmp` when
  `TMPDIR` is unset — the section does not claim otherwise.
- Dated milestone parentheticals (six/seven/eight/nine/ten case counts and leg counts; the
  `plans/` overlap of rounds 4–10) are marked as dated/historical and match the tree at C*.

## Limits

- Only the one section's bytes were read for content; all other files were opened only at the
  `path:line` anchors the section cites (`git show C*:<path>`), never for open-ended review.
- Line numbers are C* line numbers; a reader on another revision must re-resolve.
- No tool was installed or upgraded; no network access was used. Scratch dir
  `/fast/scratch/hyaku/tameshi-r53/w1/T53W1Read21/` was created for the seat and removed before
  yield (no fixture or clone was needed; all reads came from git objects).
- No git/jj mutating command was run anywhere; no file outside
  `.ufo/waves/round-53/w1/T53W1Read21.{json,md}` was written.

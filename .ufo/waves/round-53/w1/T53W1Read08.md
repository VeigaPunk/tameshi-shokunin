# T53W1Read08 — cold-read of `## The leg ledger — replay, receipt, and how it is read (round 7, measured)`

- Candidate content commit: `a41195dfc13a73958e4c5228ec196b28d03ded03` (C*)
- Lane repo: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
- Source read via git objects only: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show a41195dfc13a73958e4c5228ec196b28d03ded03:SKILL.md` (never the working tree; working tree `HEAD` was `ace79e3df61266e9474e5c02086c0f7c79664580`, unused).
- Section range: line **921** (heading) through line **933**, next heading at line **935**; 13 lines, trailing whitespace-only lines stripped, no trailing newline.
- `section_sha256` = `8bc5b3f5b95c26a9aac8aa05d7ba4c203fe2d2dde3885f9afc3d105996f04f77` (UTF-8 / surrogateescape; recomputed twice, identical).
- Findings: **1**.

## How the section was cut and hashed

Implemented the frozen monitor rule directly (`split.py`, scratch): split `SKILL.md@C*` into lines; a heading is a line matching `^#{1,3}(\s|$)` outside ``` fences; section = heading line through the line before the next heading; strip trailing whitespace-only lines; join with `\n`; sha256 over UTF-8 bytes with `surrogateescape`.

Verification of the split: heading index (0-based) `920` → 1-based line 921; next heading 1-based line 935; body length 13 lines. Byte check of the body: first byte sequence is `## The leg ledger M-bM-^@M-^T replay, ...` (em dash U+2014), and the section ends at `... plus the round-16/18/26/51 appends).` with no trailing blank line. `wc -l` of the whole blob = 2178; blob sha256 = `c329d3c150200ff32c47cb218800fb87c014345a7f342e1b11c70f5cacfc83ee`.

## Checks run (commands → outcomes)

Every referenced object was resolved from the lane's git object store at the named revision; no sibling tree was read writable, no git/jj mutating command was run anywhere.

1. **Revisions exist and are what the section calls them**
   - `git cat-file -t 9f1d3c3` → `commit`; `git log -1 --format='%H %s' 9f1d3c3` → `9f1d3c339a7094968041c7708a65dbf7eab9fae6 probation round 7 (training r6): see LOG` (the r7-1 runner).
   - `git log -1 --format='%H %s' 4b7c682` → `4b7c6823a462f5ea2eafcb262275300a545f3ed7 round-18: ...` (the round-18 runner).
2. **"turns `--regression` from the tool's two-case self-check into the fleet's leg ledger"**
   - `git show 9f1d3c3^:tools/mutate-and-run.sh | grep -c 'regression_case_git [a-z]'` → `0`; the same blob's comment reads `--regression (r4-2) — this tool's own gate: re-runs BOTH worked cases` and `--regression re-runs both worked cases (JS round 2, bash round 3)`; its helper is `regression_specs() { # <dir> — write the two embedded case specs`.
   - `git show 9f1d3c3:tools/mutate-and-run.sh` (1 341 lines, sha256 `cf41efaa8be5f52d92bf7806ddb3a99a031547bf12a6811b8ef45bce37242c75`) has exactly **four** fleet legs: `regression_case_git js-kimi-census` (:927), `bash-surface-census` (:932), `bash-tsukuroi-census` (:937), `bash-mado-verify` (:942) — plus four `fixture-*` selftest legs.
3. **Pointer `tools/mutate-and-run.sh@9f1d3c3:72-109`**
   - Line 72 = `# --regression (r4-2; r7-1 leg ledger) — the fleet's recorded mutation cases,`; lines 75–78 are the four leg names with their recorded rates: `js-kimi-census ... 8/10 (80 %)`, `bash-surface-census ... 8/10 (80 %)`, `bash-tsukuroi-census ... 6/10 (60 %)`, `bash-mado-verify ... 4/10 (40 %)`; line 108 `# --target/--defects/--suite/--label are refused (usage error).`, line 109 `#`. **Holds.**
4. **Pointer `:511-522` at the same revision**
   - Numbered dump: 511 `PIN_JS=83016d45…`, 512 `REV_JS=175de6ba…`, 513 `PIN_BASH=275d8294…`, 514 `REV_BASH=fecee874…`, 515 `PIN_TSUKUROI=084951be…`, 516 `REV_TSUKUROI=165307fe…`, 517 `PIN_MADO=d7edaab4…`, 518 `REV_MADO=eead56b2…`, 519–522 `TABLE_JS/TABLE_BASH/TABLE_TSUKUROI/TABLE_MADO` (the recorded verdict tables). **Holds** (pins + recorded tables, i.e. the per-leg expectations).
5. **Pointer `:597-620` at round 18 (`4b7c682`)**
   - Numbered dump: 597 `PIN_JS` … 604 `REV_MADO`, 605–612 `PIN_CHECKLIST` … `REV_SOURCESCHECK`, 613–620 `TABLE_JS` … `TABLE_SOURCESCHECK`. **Holds** (the recorded tables, extended by the round-16/18 legs).
6. **Rates in the section match the runner and the ledger**
   - Runner comment at C*: `js-kimi-census … 8/10 (80 %)` (:88), `bash-surface-census … 8/10 (80 %)` (:89), `bash-tsukuroi-census … 6/10 (60 %)` (:90), `bash-mado-verify … 4/10 (40 %)` (:91).
   - Ledger `§1` rows 45–48 at C* carry the same four rates (8/10, 8/10, 6/10, 4/10), rows 45–46 pins `83016d45…` / `275d8294…`, rows 47–48 `084951be…` / `d7edaab4…`. **Holds.**
7. **"every recorded mutation case is a leg of this ledger, replayed at its pinned original revision"**
   - At C*, `tools/mutate-and-run.sh` has ten fleet legs (:1459 `js-kimi-census`, :1464 `bash-surface-census`, :1469 `bash-tsukuroi-census`, :1474 `bash-mado-verify`, :1479 `bash-checklist-run`, :1484 `js-claims-check`, :1489 `js-round-gate`, :1494 `js-sources-check`, :1499 `js-cite-check`, :1504 `bash-drift-pins`), each called with `"$PIN_*" "$REV_*"` and materialized from git objects (`# r7-1: the target is NOT read from the fleet working tree`).
   - `corpus/knowledge/fleet-kill-rate-ledger.md` **exists at C*** (441 lines) and is cited by nine `corpus/knowledge/*.md` blobs at C* (`git grep -c 'fleet-kill-rate-ledger' a41195d… -- corpus/knowledge` → closeout-r11 6, incremental-pin-disposition 3, mutation-case-kagi-checklist 2, mutation-case-kagi-drift-pins 3, mutation-case-kumitate-cite-check 1, mutation-case-kumitate-claims 1, operator-runbook 23, service-limits 13, service-standing-state 18). The **receipt** half of the sentence holds.
8. **"six in the §1/ER-2 table"**
   - Ledger §1 (`## 1. Measured — the four fleet sweeps (all 2026-10-14)`) has numbered rows `| 1 |`…`| 4 |` (lines 45–48); `ER-2` (line 272, "the fifth and sixth cases land") has `| 5 |` (276) and `| 6 |` (277). Six. **Holds.**
9. **The append half of the same sentence (fails — see finding)**
   - Headings at C*: `## Round 16 — seventh row appended (2026-10-20)` (line 403), `## Round 18 — eighth row appended (2026-10-20)` (line 424), `## Round 52 — §3 drift-pins cell superseded (2026-10-27)` (line 439). `grep -n '^#\{1,3\} ' ledger.md` → 15 headings, at lines 1, 21, 41, 90, 98, 132, 160, 178, 200, 216, 239, 366, 403, 424, 439; the list contains **no** round-26 and **no** round-51 heading.
   - `grep -in 'round[ -]*26\|round[ -]*51\|ninth\|tenth' ledger.md` → exactly **one** hit: line 441, the round-52 block's supersession bullet that records the round-51 case-10 measurement. No "ninth"/"tenth" row label appears anywhere in the file.
   - Numbered measured rows in the whole file stop at eight (4 + 2 + one row in the round-16 table + one row in the round-18 table).

## Holds (verified against C* bytes)

- Heading text, section boundaries, and `section_sha256` (method above).
- `tools/mutate-and-run.sh@9f1d3c3:72-109`, `:511-522`, and `4b7c682:597-620` all land on what the section says they land on (checks 3–5).
- Round 7 recorded **four** legs at r7-1, with exactly the four recorded kill-rates the section lists (checks 2, 3, 6).
- The pre-round-7 `--regression` was the two-case self-check (check 2).
- Every recorded case is a runner leg and is replayed from its pinned revision (check 7, ten legs).
- The ledger file named as the standing receipt exists at C* and is cited for kill-rate claims by nine knowledge records (check 7).
- "six in the §1/ER-2 table" (check 8).
- The parenthetical `(dated milestones: seven from round 16, eight from round 18, nine from round 26, ten from round 51)` is explicitly marked as a dated milestone, so it is scored a **hold** under the wave rule even though the round-26 and round-51 rows it counts are not in the ledger at C* (the same underlying drift the finding below records in its present-tense form).
- No scratch-directive content in the section (nothing to check against `$HYAKU_SCRATCH` / the 50 MB `/tmp` rule).

## Finding (1)

**Class:** `stale-ledger-count`

**Quote (byte-exact in the section, 1 occurrence):**

> ten measured rows: six in the §1/ER-2 table plus the round-16/18/26/51 appends

**Statement that fails:** the standing per-gate rate rows are `corpus/knowledge/fleet-kill-rate-ledger.md`, carrying **ten** measured rows — six in the §1/ER-2 table plus **round-16/18/26/51** appends.

**Why it fails at C*** (`git show a41195d…:corpus/knowledge/fleet-kill-rate-ledger.md`):

1. The five-part split does not exist. The file's measured rows are 4 (§1) + 2 (ER-2) + 1 (round 16, "seventh row appended") + 1 (round 18, "eighth row appended") = **8**, and its own numbering stops at "eighth".
2. There is **no round-26 append at all**: `grep -in 'round[ -]*26'` over the 441-line blob returns nothing, and the heading inventory (lines 1, 21, 41, 90, 98, 132, 160, 178, 200, 216, 239, 366, 403, 424, 439) contains no round-26 block.
3. The round-51 measurement is present but not as a measured row: the only mention is line 441, inside `## Round 52 — §3 drift-pins cell superseded`, a "§3 supersession (cell, not edit)" bullet. It appends a cell correction, not a row, so it cannot supply the ninth-or-tenth row the sentence counts.
4. The missing ninth record demonstrably exists elsewhere at C*, which is what makes the ledger's silence a defect rather than an unfinished sweep: the runner lists `js-cite-check … 5/10 (50 %)` and comments "Leg 9's spec is the round-26 pre-registration committed in 622d31d … its table is the measured 2026-10-22 sweep (10:02Z, .ufo/evidence/round-26/cite-check/sweep/sweep.txt …)"; the evidence blob begins `MUTATE_DATE: 2026-10-22T10:02:07Z`, `MUTATE_SPEC: …/.ufo/evidence/round-26/cite-check/cite-check.defects.spec defects=10`; and `corpus/knowledge/mutation-case-kumitate-cite-check.md` exists at C*. Meanwhile the ledger's own §3 queue row for that gate (line 107) still reads `**probe only, 1/4** (§2); full sweep open`.
5. Consequence for the sentence's purpose: the ledger is presented as the standing per-gate rate receipt, yet the measured gate whose rate the runner records as leg 9 (and the round-51 case 10 recorded only as a supersession cell) has no standing rate row — a reader following the pointer to check "every recorded mutation case" will find eight rows, not ten.

**Not claimed:** this is not a claim that the underlying measurements are wrong; the rates themselves (checks 5–6) reproduce. Only the count and the append inventory in the section's pointer are stale.

## Scratch and tooling

- Scratch: `/fast/scratch/hyaku/tameshi-r53/w1/T53W1Read08/` (created with `mkdir -p`; held `SKILL.md@C*`, `ledger.md`, `mar-r7.sh`, `mar-r18.sh`, `mar-cstar.sh`, `section.txt`, `split.py`, all well under 50 MB). Removed with `rm -rf` before yield.
- Tooling installed/upgraded: **none** (system `git`, `python3`, `awk`, `grep`, `sha256sum` sufficed). No pacman transaction was attempted.
- No git/jj mutating command was run; every git call was `show`/`cat-file`/`log`/`grep`/`rev-parse` against the lane repo.
- Write scope respected: only `.ufo/waves/round-53/w1/T53W1Read08.json` and `.ufo/waves/round-53/w1/T53W1Read08.md` in the lane.

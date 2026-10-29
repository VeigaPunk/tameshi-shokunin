# T51W2Read12 — cold-read re-key reader: `### The six-leg regression — usage and this round's receipt`

Seat T51W2Read12, round-51 wave 2 (falsify), lane `tameshi-shokunin`. Item: read the section at CAND
`6d8c11e378aa90b12650808e1b79270742935f15`, verify every cited pointer against candidate bytes, adversarially.
Read-only everywhere except this report; scratch `/fast/scratch/hyaku/tameshi-r51/T51W2Read12` (deleted before
yield). No tool installs.

## 0. Method

- Candidate bytes via `git show 6d8c11e…:<path>`; base via `git show 9962033f…:<path>`.
- The section's pinned tool revision `75ed934d…` is **not a git rev** (`git cat-file` rejects it) — it is the
  sha256 of the tool bytes at r10-2. Resolved: `git show 606716f:tools/mutate-and-run.sh | sha256sum` →
  `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`, 1 642 L — byte-exact match with the
  section's "1 642 L" and `VERSION` string. (Corroborated by `closeout-r11.md:69` "committed at `606716f`" and
  `SKILL.md:1398` round-18 replay note.)
- One execution: the runner's `--selftest` at CAND, from a `git clone --shared` of the lane checked out at
  CAND in scratch, `TMPDIR` redirected under scratch → rc 0, `MUTATE_SELFTEST: 107/107 pass` / `VERDICT: PASS`.
- SKILL.md base→CAND is a single hunk (`@@ -2136,0 +2137,35 @@` — the round-51 registry rows): **this section's
  bytes are identical at base and CAND** (1302–1364). Every drift below is input-drift — the runner and panel
  tools it describes changed under it — matching the fixture class `input-drift:tools/mutate-and-run.sh`.

## 1. Verdict summary

The section is a faithful record of tool revision `75ed934d…` (r10-2): its sha, line count, VERSION string,
six-leg table, receipt numbers and cross-references all verify against the pinned bytes, the sibling repos and
the round-10/11/18 records. At CAND it is stale in exactly the ways the round's three changes predict:

1. **Six → ten legs.** "replays **six** embedded legs" and the six-row table describe the pinned revision only.
   At CAND the runner wires ten legs: header `:84` "… r26 nine; r51 ten", leg list `:88-97`, `nlegs=10`
   (`:1510`), the selftest's embedded-ledger check asserts ten (`:2075`), `REGRESSION_EXPECT` lists ten rates
   (`:1446`), and the tenth leg is `bash-drift-pins` → kagi `corpus/drift-pins.sh` @ `e64e81b8`
   (pin `c138d34c…`, spec intro `:1155-1158`).
2. **Runner TMPDIR change.** "default scratch `mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX`" is false at
   CAND: the runner now uses `"${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX"` (`:1432`; header `:149-150`
   says "(r51 honours TMPDIR)"); same for the `--workdir` default (`:491`) and the selftest scratch (`:1555`).
3. **Receipt numbers moved.** `MUTATE_SELFTEST: 80/80` (r10-2) → measured **107/107** at CAND (this seat's
   run, rc 0); `cases=6 passed=6` → ten legs (`cases=10` is what C2's registered regression clause requires).
4. **Every runner line anchor moved** (tenth leg + comment growth shifted the file 1 642 → 2 159 L); at CAND
   the cited lines land in unrelated regions (samples in §2).
5. **Exit map extended.** CAND adds the r30 SETUP clause ("the counted pass/fail/setup statuses do not add up
   to the case count — case-tally mismatch", `:142-143`); the section's 0/1/2 rendering is incomplete at CAND.

What the round's changes do **not** break: legs 1–6 are byte-identical at CAND (pins, revs, tables, rates);
the command syntax, keep/remove semantics, git-object materialization, pin-mismatch SETUP refusal and mode
mirror all hold; the ledger, runbook and SKILL self-anchors all hold (details in §2).

## 2. Pointer-by-pointer (every pointer in the section)

Legend: **holds** = true at CAND; **holds@sha** = true at the governing sha, moved/stale at CAND;
**holds-hist** = historical record, corroborated; **drift** = false/stale at CAND.

| # | Raw pointer (section text) | Verdict | Evidence |
|---|---|---|---|
| P1 | "At tool revision `75ed934d…` (`VERSION` = `mutate-and-run.sh r10-2`, 1 642 L; uncommitted worktree file at this write)" | holds-hist | sha256 of `606716f:tools/mutate-and-run.sh` = the full pinned sha; 1 642 L; `VERSION` at `:157`. "Uncommitted at this write" corroborated by `closeout-r11.md:69` and the runbook errata ER-R1/ER-R2 (`:491-509`, in-flight readings `4b3dfed5`/`5807fd38`). |
| P2 | "`--regression` replays **six** embedded legs" | **drift** | True at the pinned sha; at CAND ten legs (`:84` header, `:88-97` list, `nlegs=10` `:1510`, selftest assert `:2075`). |
| P3 | "list `tools/mutate-and-run.sh:85-89`" | holds@sha (imprecise) + moved | At the governing sha the list is **:84-89** — the cited range misses leg 1 (`:84`); `repeated-control-precondition.md:54` independently records ":84-89". At CAND the list is `:88-97`; cited `:85-89` lands on comment lines + legs 1–2. |
| P4 | "sources `:90-97`" | holds@sha + moved | Exact at the sha (`:90-97`, six sources + the 40/25 @old note). At CAND `:98-121` (extended with legs 7/8/10 sources). |
| P5 | "pins/tables `:550-559`" | holds@sha (partial) + moved | At the sha: pins `:542-553`, tables `:554-559` — the cited range covers all six tables + legs 5–6 pins; legs 1–4 pins (`:542-549`) are outside it. At CAND `:614-643`; cited `:550-559` lands in the sweep verdict-classification loop (`case $RC in …`). |
| P6 | "specs `:766`, `:841`" | holds@sha + moved | At the sha these are the intro comments of the embedded T8-1/T8-2 specs (`:766-769`, `:841-844`; `cat` lines `:770`/`:845`). At CAND intros `:850-853`/`:925-928`, cats `:854`/`:929`; cited `:766` lands inside the tsukuroi spec body, `:841` inside the mado spec body. Note: only legs 5–6 are anchored; legs 1–4 specs sit at `:589/:630/:675/:720` (sha) / `:673/:714/:759/:804` (CAND). |
| P7 | "registry `:1132-1141`" | holds@sha (partial) + moved | At the sha: legs 5–6 entries (`:1132-1141`); the full six-leg registry is `:1112-1141`. At CAND ten entries `:1459-1507` (`nlegs=10` `:1510`); cited `:1132-1141` lands on `st_claims=$?` / the leg-7 entry. |
| P8 | Six-leg table (targets, recorded revs, recorded rates) | **holds** | Every cell verified: leg list `:84-89` matches all six names/targets/rates; `REV_*` match (`175de6ba`, `fecee874`, `165307fe`, `eead56b2`); all six blob pins recomputed from the sibling repos at the recorded revs — `83016d45…`, `275d8294…`, `084951be…`, `d7edaab4…`, `7e5ec98b…`, `e9a21b44…` — **all exact**; table arithmetic (8/8/6/4/7/7 killed) matches `TABLE_JS…TABLE_CLAIMS` and the ledger §1 rows / §4 rate sequence. At CAND legs 1–6 are byte-identical; legs 7–10 appended after. |
| P9 | "Command, unchanged. `bash tools/mutate-and-run.sh --regression [--workdir DIR] [--keep]`" | holds | Usage `:217`, header `:148-152` at CAND — syntax and keep/remove semantics unchanged. |
| P10 | "default scratch `mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX`" | **drift** | At the sha `:1089` literal `/tmp`. At CAND `:1432` `"${TMPDIR:-/tmp}/…"`; header `:149-150` "(r51 honours TMPDIR)". |
| P11 | "Exit map: 0 all legs PASS · 1 ≥1 leg FAIL · 2 cannot verify (SETUP) (`tools/mutate-and-run.sh:115-119`)" | holds@sha + moved/extended | At the sha the map is `:115-117` (range covers). At CAND `:139-145`, extended with the r30 clause "or (r30) the counted pass/fail/setup statuses do not add up to the case count (SETUP \"case-tally mismatch\"…)". |
| P12 | "materialized from its repo's git object store (`git show <rev>:<path>`) … pin mismatch is a SETUP refusal before any suite runs" | holds | CAND comment `:125-127`, impl `:1275-1300`. |
| P13 | "r10-2 also mirrors the blob's mode … (`:104-106`, `:932-960`)" | holds@sha + moved | At the sha: comment `:104-106` exact; impl `:938-959` (chmod block, `REGRESSION_PIN … mode=%s` printf at `:959`) within range. At CAND comment `:128-130`, impl `:1281-1302` (printf `:1302`). |
| P14 | "the added selftest arms at `:1488-1527` cover the mirror" | holds@sha + moved | Exact at the sha (`:1488` comment → `:1527` last arm "exec-bit leg PASSes at the exact tolerance"). At CAND `:1860-1896`. |
| P15 | "Receipt … 2026-10-14T21:02:39Z, tool `75ed934d…` before and after, scratch `/tmp/w10-t10-4-ev/`" | holds-hist | `closeout-r11.md:308-310`: "… T10-2 21:00:24Z · AUD-T10 21:01:53Z · **T10-4 21:02:39Z** · VER-T10 21:05:10Z"; the scratch path is recorded in the round-16 cold-read snapshot (`SKILL.snapshot.md:1335`) and a round-27 trace probed its gone-ness (`round-27/coldread/traces/Read22-9.json`). |
| P16 | "the owner's own run at the same revision, 21:00:24Z, closes identically" | holds-hist | `closeout-r11.md:309` (T10-2 21:00:24Z; cases=6 at `75ed934d…`, selftest 80/80). |
| P17 | "`--selftest` → `MUTATE_SELFTEST: 80/80 pass` / `VERDICT: PASS`, rc 0" | holds-hist, **stale at CAND** | Corroborated (`closeout-r11.md:309/:354-355`; round-18 wave-2 replay CR30 reproduced 80/80 at `606716f`, `SKILL.md:1398`). This seat's run at CAND: **`MUTATE_SELFTEST: 107/107 pass` / `VERDICT: PASS`, rc 0** — arms added rounds 12–26 + r51; the embedded-ledger check now asserts ten legs (`:2013-2014`, `:2072-2076`). |
| P18 | "`--regression` → six legs, all exact … closing `REGRESSION: PASS (cases=6 passed=6; …)`, rc 0" | holds-hist, stale at CAND | Corroborated (`closeout-r11.md:308`; `SKILL.md:1426-1429` round-11 re-verification). At CAND ten legs; C2's registered clause requires `REGRESSION: PASS (cases=10 passed=10`. |
| P19 | "Each `REGRESSION_PIN` line now carries the blob's `mode=` … `REGRESSION_EXPECT` lists six recorded rates" | holds@sha; half stale at CAND | `mode=` holds at both (printf `:959` sha / `:1302` CAND). `REGRESSION_EXPECT` lists **ten** rates at CAND (`:1446`). |
| P20 | "The round-7 section's \"Four legs at this revision\" (`:925-929`; dated there since round 16)" | holds-as-disclosed | CAND `:925` reads "Four legs at **that** revision (r7-1; seven since round 16; eight since round 18; nine since round 26)" — the quote is the pre-dating phrasing; the mismatch is disclosed by this section's own "dated there since round 16" and by errata `:1733` and `:1739` (which quote the same phrase). |
| P21 | "the round-9 receipt's `cases=4` (`:1218-1222`)" | holds | CAND `:1219-1222`; `cases=4` at `:1220`; tool `cf41efaa…` at `:1221`. |
| P22 | "\"still not embedded — named debt\" (`:1226-1228`; ER-4 caveat (a))" | holds | CAND `:1227-1228`; ER-4 caveat (a) at `fleet-kill-rate-ledger.md:318-353` ("(a) the tool embeds **4** legs — cases 5/6 … carry no `REGRESSION` line"). |
| P23 | "their 25 `@old` strings re-verified `count==1` against the pinned blobs" | **holds** | Embedded T8-1/T8-2 specs at the sha: 15 (checklist) + 10 (claims) = **25** (a 26th raw hit is the claims spec header's own "@old" mention). `count==1` spot-checked against the pinned blobs: mado R1 `row walker walker.config UNKNOWN …` → 1; checklist G1 `checklist-run: unknown argument: %s\n` → 1. |
| P24 | "the recorded tables are never edited and each leg's expectation is the rate its note recorded" | holds | Legs 1–6 `TABLE_*` values byte-identical base→CAND; rates match the ledger §1 rows and §4 rate sequence (80/80/60/40/47/70). |
| P25 | "Reading a receipt stays the round-7 discipline (`:965-1008`)" | holds | Heading `:965`, content through `:1008` (next heading `:1010`). |
| P26 | "The runbook's §7 is the operator's rendering of this command; on a differing revision the tool bytes and the run you executed govern." | holds | Runbook unchanged base→CAND; §7 = `:345-406`, renders the command at `:348`. Its own default-scratch (`:350`), exit-map anchor (`:353`, r7-1 anchors `:98-108`) and `cases=4` example (`:361`) are stale vs CAND — covered by the governing rule this sentence states. |
| P27 | "The ledger's §1 embedding text still reads \"cases 1 and 2 only\" (`fleet-kill-rate-ledger.md:85-88`)" | holds | Exact (`:85-88`, bold phrase at `:86`); ledger byte-identical base→CAND. |
| P28 | "superseded in the ledger by ER-2 (`:281`, four legs)" | holds | `:281` is ER-2's §5/ER-1 supersession bullet ("carries **four** materialized legs … `REGRESSION: PASS (cases=4 passed=4…`). |
| P29 | "a ledger row recording the six-leg registry is the ledger owner's follow-on — this page records the registry as measured at `r10-2`, and no ledger cell is edited from here" | holds, **understates at CAND** | Ledger unchanged — still no registry row; the registry is now ten legs and the ledger's §1 measured rows stop at leg 7 (round-gate `:410`, receipt `cases=7` at `:412-413`). The named debt grew. |

Also verified: the six runner-cited source notes all exist at CAND (`mutation-case-{kimi-census,kagi-census,tsukuroi-census,mado-verify,kagi-checklist,kumitate-claims}.md`, `git ls-tree`), plus the new `mutation-case-kagi-drift-pins.md` (222 L, the C2 entry).

## 3. Strongest falsifiers checked

- **F1 (six vs ten):** CAND runner has ten wired legs — header `:84`, list `:88-97`, `nlegs=10` `:1510`, selftest 10-leg assert `:2075`. **Drift confirmed.**
- **F2 (TMPDIR):** CAND honors `TMPDIR` for regression/workdir/selftest scratch (`:1432`, `:491`, `:1555`; header `:149-150`). **Drift confirmed** — the section's literal `/tmp/…` default is false at CAND.
- **F3 (selftest total):** ran the runner `--selftest` at CAND from a `--shared` clone in scratch (TMPDIR under scratch): rc 0, `MUTATE_SELFTEST: 107/107 pass` / `VERDICT: PASS`. The receipt's 80/80 is r10-2-historical. **Drift confirmed; tool green at CAND.**
- **F4 (pins):** all six blob pins recomputed from kumitate/kagi/tsukuroi/mado at the recorded revs — all exact. No falsification.
- **F5 (25 @old):** 15+10 counted; two `count==1` spot-checks against pinned blobs → 1 each. No falsification.
- **F6 (receipt provenance):** `closeout-r11.md:308-310/:354-358` and `SKILL.md:1398` corroborate every receipt number. No falsification.
- **F7 (exit map):** r30 SETUP clause added at CAND (`:142-143`). **Drift confirmed.**
- **F8 (REGRESSION_EXPECT):** ten rates at CAND (`:1446`). **Drift confirmed.**
- **F9 (panel tools):** none of `tally-audit.py`/`-v2`/`-v3`/`mte-interop.py` cites this section (their `REF_BLOCK`/`REF_NAMES` now carry the ten-leg panel); no statement here is made false by them beyond the six-leg count already covered.

## 4. Notes for the re-key

- The section's runner anchors were **already imprecise at the governing sha** (list `:84-89` not `:85-89`; pins `:542-553` outside the cited `:550-559`; registry `:1112-1141` not `:1132-1141`). The section's own "the sha governs" hedge makes them advisory — do not copy them forward as exact.
- The `VERSION` string still reads `mutate-and-run.sh r10-2` at CAND (`:185`) while the tool is r51-edited (2 159 L) — a reader identifying the tool by VERSION would be misled; the sha256 is the only live pin.
- The named-debt bullet understates at CAND: no ledger registry row exists and the registry is ten legs.
- CAND locations for re-anchoring: leg list `:88-97`; sources `:98-121`; pins `:614-625` + tables `:634-643`; leg-5/6 spec intros `:850-853`/`:925-928` (cats `:854`/`:929`); registry `:1459-1507`; exit map `:139-145`; scratch `:146-148` + `:1432`; mode-mirror comment `:128-130` + impl `:1281-1302`; selftest exec arms `:1860-1896`; embedded-ledger check `:2013-2014`/`:2072-2076`; `VERSION` `:185`; `REGRESSION_EXPECT` `:1446`.

## 5. reads.json row

```json
{
  "seat": "T51W2Read12",
  "heading": "### The six-leg regression — usage and this round's receipt",
  "cand": "6d8c11e378aa90b12650808e1b79270742935f15",
  "section_lines_cand": [1302, 1364],
  "next_heading_cand": "## Final pointers — the standing map at the arc's close (round 11, measured) @1365",
  "section_bytes_equal_base": true,
  "pinned_tool_sha": "75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5",
  "pinned_tool_sha_verified": "sha256(606716f:tools/mutate-and-run.sh) == pinned sha; 1642 L; VERSION :157",
  "pointers": [
    {"id": "P1", "raw": "At tool revision 75ed934d… (VERSION = mutate-and-run.sh r10-2, 1 642 L; uncommitted worktree file at this write)", "file": "tools/mutate-and-run.sh", "verdict": "holds-hist", "cand_note": "VERSION string unchanged at :185 but file is 2159 L — the 1 642 L half is stale at CAND; the sha is the only live pin", "excerpt": "runner@606716f:157 VERSION='mutate-and-run.sh r10-2 (tameshi-shokunin, 2026-10-14)'; sha256sum matches the full pinned sha"},
    {"id": "P2", "raw": "--regression replays six embedded legs", "file": "tools/mutate-and-run.sh", "verdict": "drift", "cand_note": "ten legs at CAND: header :84 'r51 ten', list :88-97, nlegs=10 :1510, selftest asserts 10 :2075", "excerpt": "runner_cand:1510 'local nlegs=10 npass=0 nfail=0 nsetup=0 st'"},
    {"id": "P3", "raw": "list tools/mutate-and-run.sh:85-89", "file": "tools/mutate-and-run.sh", "ranges": "85-89", "verdict": "holds-at-pinned-sha-imprecise+moved", "sha_note": "actual list :84-89 (cited range misses leg 1)", "cand_note": "list :88-97; cited :85-89 lands on comment lines + legs 1-2", "excerpt": "runner_cand:88-97 ten leg lines, :88 'js-kimi-census … 8/10 (80 %)' … :97 'bash-drift-pins … 2/10 (20 %)'"},
    {"id": "P4", "raw": "sources :90-97", "file": "tools/mutate-and-run.sh", "ranges": "90-97", "verdict": "holds-at-pinned-sha+moved", "cand_note": "moved to :98-121 (extended with legs 7/8/10 sources)", "excerpt": "runner@r102:90 '# Sources: corpus/knowledge/mutation-case-kimi-census.md §1,'"},
    {"id": "P5", "raw": "pins/tables :550-559", "file": "tools/mutate-and-run.sh", "ranges": "550-559", "verdict": "holds-at-pinned-sha-partial+moved", "sha_note": "pins :542-553, tables :554-559 — range covers all six tables + legs 5-6 pins; legs 1-4 pins outside", "cand_note": ":614-643; cited :550-559 lands in the sweep verdict-classification loop", "excerpt": "runner_cand:614 PIN_JS=83016d45… … :643 TABLE_DRIFTPINS='K_MODE_CMP:KILLED,K_GONE_ARM:SURVIVED,…'"},
    {"id": "P6", "raw": "specs :766, :841", "file": "tools/mutate-and-run.sh", "ranges": "766,841", "verdict": "holds-at-pinned-sha+moved", "sha_note": "intro comments of the embedded T8-1/T8-2 specs (cat lines :770/:845)", "cand_note": "intros :850-853/:925-928, cats :854/:929; cited :766 lands in the tsukuroi spec body, :841 in the mado spec body", "excerpt": "runner@r102:766 '# r10-2 leg 5: kagi corpus/checklist-run.sh @ fecee874 (pin 7e5ec98b…),'"},
    {"id": "P7", "raw": "registry :1132-1141", "file": "tools/mutate-and-run.sh", "ranges": "1132-1141", "verdict": "holds-at-pinned-sha-partial+moved", "sha_note": "legs 5-6 entries; full six-leg registry :1112-1141", "cand_note": "ten entries :1459-1507; cited :1132-1141 lands on st_claims/leg-7 entry", "excerpt": "runner_cand:1459 'regression_case_git js-kimi-census \\' … :1504 'regression_case_git bash-drift-pins \\'"},
    {"id": "P8", "raw": "six-leg table (targets, recorded revs, recorded rates)", "file": "tools/mutate-and-run.sh + sibling repos + ledger", "verdict": "holds", "cand_note": "legs 1-6 byte-identical at CAND; legs 7-10 appended", "excerpt": "all six blob pins recomputed from sibling repos at recorded revs — exact; rates 8/8/6/4/7/7 match TABLE_* and ledger §1/§4"},
    {"id": "P9", "raw": "Command, unchanged. bash tools/mutate-and-run.sh --regression [--workdir DIR] [--keep]", "file": "tools/mutate-and-run.sh", "verdict": "holds", "cand_note": "usage :217, header :148-152 — syntax and keep/remove semantics unchanged", "excerpt": "runner_cand:150-152 'removed on PASS unless --keep, kept on FAIL/SETUP, never removed when --workdir was given'"},
    {"id": "P10", "raw": "default scratch mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX", "file": "tools/mutate-and-run.sh", "verdict": "drift", "sha_note": ":1089 literal /tmp", "cand_note": ":1432 uses \"${TMPDIR:-/tmp}/…\"; header :149-150 '(r51 honours TMPDIR)'; same for --workdir default :491 and selftest :1555", "excerpt": "runner_cand:146-148 'Scratch root: mktemp -d \"${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX\" by default (r51 honours TMPDIR)'"},
    {"id": "P11", "raw": "Exit map: 0 all legs PASS · 1 ≥1 leg FAIL · 2 cannot verify (SETUP) (tools/mutate-and-run.sh:115-119)", "file": "tools/mutate-and-run.sh", "ranges": "115-119", "verdict": "holds-at-pinned-sha+moved+extended", "cand_note": "map at :139-145 with the r30 SETUP clause (case-tally mismatch) added", "excerpt": "runner_cand:142-143 'or (r30) the counted pass/fail/setup statuses do not add up to the case count (SETUP \"case-tally mismatch\"…)"},
    {"id": "P12", "raw": "materialized from its repo's git object store (git show <rev>:<path>) … pin mismatch is a SETUP refusal before any suite runs", "file": "tools/mutate-and-run.sh", "verdict": "holds", "cand_note": "comment :125-127, impl :1275-1300", "excerpt": "runner_cand:127 '# a missing repo/rev/blob or a pin mismatch is a SETUP refusal, never a pass.'"},
    {"id": "P13", "raw": "r10-2 also mirrors the blob's mode … (:104-106, :932-960)", "file": "tools/mutate-and-run.sh", "ranges": "104-106,932-960", "verdict": "holds-at-pinned-sha+moved", "sha_note": "comment :104-106 exact; impl :938-959 within range (printf :959)", "cand_note": "comment :128-130, impl :1281-1302 (printf :1302)", "excerpt": "runner@r102:959 REGRESSION_PIN printf carries mode=%s beside repo/rev/path/sha256"},
    {"id": "P14", "raw": "the added selftest arms at :1488-1527 cover the mirror", "file": "tools/mutate-and-run.sh", "ranges": "1488-1527", "verdict": "holds-at-pinned-sha-exact+moved", "cand_note": ":1860-1896", "excerpt": "runner@r102:1527 \"st 'exec-bit leg PASSes at the exact tolerance' $?\""},
    {"id": "P15", "raw": "Receipt … 2026-10-14T21:02:39Z, tool 75ed934d… before and after, scratch /tmp/w10-t10-4-ev/", "file": "(record)", "verdict": "holds-hist", "cand_note": "corroborated by closeout-r11.md:308-310 (T10-4 21:02:39Z); scratch dir gone (round-27 trace Read22-9 probed gone-ness)", "excerpt": "closeout-r11:309-310 'T10-2 21:00:24Z · AUD-T10 21:01:53Z · T10-4 21:02:39Z · VER-T10 21:05:10Z'"},
    {"id": "P16", "raw": "the owner's own run at the same revision, 21:00:24Z, closes identically", "file": "(record)", "verdict": "holds-hist", "excerpt": "closeout-r11:309 T10-2 21:00:24Z; cases=6 at 75ed934d; selftest 80/80"},
    {"id": "P17", "raw": "--selftest → MUTATE_SELFTEST: 80/80 pass / VERDICT: PASS, rc 0", "file": "(record)", "verdict": "holds-hist-stale-at-cand", "cand_note": "this seat ran the runner --selftest at CAND from a --shared clone: rc 0, MUTATE_SELFTEST: 107/107 pass / VERDICT: PASS; embedded-ledger check now asserts ten legs (:2013-2014, :2072-2076)", "excerpt": "measured at CAND: 'MUTATE_SELFTEST: 107/107 pass'"},
    {"id": "P18", "raw": "--regression → six legs, all exact … closing REGRESSION: PASS (cases=6 passed=6; …), rc 0", "file": "(record)", "verdict": "holds-hist-stale-at-cand", "cand_note": "ten legs at CAND; C2's registered clause requires 'REGRESSION: PASS (cases=10 passed=10'", "excerpt": "closeout-r11:308 'PASS (cases=6 passed=6; ledger legs exact: killed-delta<=0 flips<=0) at 75ed934d…'"},
    {"id": "P19", "raw": "Each REGRESSION_PIN line now carries the blob's mode= … REGRESSION_EXPECT lists six recorded rates", "file": "tools/mutate-and-run.sh", "verdict": "holds-at-pinned-sha; half-stale-at-cand", "cand_note": "mode= holds (printf :1302); REGRESSION_EXPECT lists ten rates (:1446)", "excerpt": "runner_cand:1446 REGRESSION_EXPECT printf with ten %s/%s pairs ending bash-drift-pins"},
    {"id": "P20", "raw": "The round-7 section's \"Four legs at this revision\" (:925-929; dated there since round 16)", "file": "SKILL.md", "ranges": "925-929", "verdict": "holds-as-disclosed", "cand_note": ":925 reads 'Four legs at that revision (r7-1; seven since round 16; eight since round 18; nine since round 26)' — quote is the pre-dating phrasing; disclosed by this section's 'dated there since round 16' and errata :1733/:1739", "excerpt": "skill_cand:925 'pinned original revision. Four legs at that revision (r7-1; seven since round 16; …)'"},
    {"id": "P21", "raw": "the round-9 receipt's cases=4 (:1218-1222)", "file": "SKILL.md", "ranges": "1218-1222", "verdict": "holds", "cand_note": ":1219-1222; cases=4 at :1220; tool cf41efaa at :1221", "excerpt": "skill_cand:1220 'closing REGRESSION: PASS (cases=4 passed=4; ledger legs exact:'"},
    {"id": "P22", "raw": "\"still not embedded — named debt\" (:1226-1228; ER-4 caveat (a))", "file": "SKILL.md + corpus/knowledge/fleet-kill-rate-ledger.md", "ranges": "1226-1228; ledger 318-353", "verdict": "holds", "cand_note": ":1227-1228; ER-4 caveat (a) at ledger :318-353", "excerpt": "skill_cand:1227-1228 'Cases 5–6 are still not embedded: … named debt, not smoothed'"},
    {"id": "P23", "raw": "their 25 @old strings re-verified count==1 against the pinned blobs", "file": "tools/mutate-and-run.sh (embedded specs) + pinned blobs", "verdict": "holds", "cand_note": "15 (checklist) + 10 (claims) = 25 counted (a 26th raw hit is the claims spec header's own '@old' mention); count==1 spot-checked on mado R1 and checklist G1 against the pinned blobs → 1 each", "excerpt": "spec_t81 @old=15; spec_t82 @old=10 (+1 header mention); blob greps → 1, 1"},
    {"id": "P24", "raw": "the recorded tables are never edited and each leg's expectation is the rate its note recorded", "file": "tools/mutate-and-run.sh + ledger", "verdict": "holds", "cand_note": "legs 1-6 TABLE_ values byte-identical base→CAND; rates match ledger §1 rows and §4 rate sequence", "excerpt": "TABLE_JS…TABLE_CLAIMS identical at r102 :554-559 and CAND :634-639"},
    {"id": "P25", "raw": "Reading a receipt stays the round-7 discipline (:965-1008)", "file": "SKILL.md", "ranges": "965-1008", "verdict": "holds", "cand_note": "heading :965, content through :1008 (next heading :1010)", "excerpt": "skill_cand:965 '### Reading a receipt — the discipline'"},
    {"id": "P26", "raw": "The runbook's §7 is the operator's rendering of this command; on a differing revision the tool bytes and the run you executed govern.", "file": "corpus/knowledge/operator-runbook.md", "ranges": "§7 = :345-406", "verdict": "holds", "cand_note": "runbook unchanged base→CAND; §7 renders the command at :348; its own default-scratch (:350), exit-map anchor (:353, r7-1 anchors :98-108) and cases=4 example (:361) are stale vs CAND — covered by the stated governing rule", "excerpt": "runbook:348 'bash tools/mutate-and-run.sh --regression [--workdir DIR] [--keep]'"},
    {"id": "P27", "raw": "The ledger's §1 embedding text still reads \"cases 1 and 2 only\" (fleet-kill-rate-ledger.md:85-88)", "file": "corpus/knowledge/fleet-kill-rate-ledger.md", "ranges": "85-88", "verdict": "holds", "cand_note": "ledger byte-identical base→CAND; phrase at :85-88 (bold at :86)", "excerpt": "ledger:85-88 'Embedding status (O, §5): the harness's --regression currently embeds **cases 1 and 2 only** …'"},
    {"id": "P28", "raw": "superseded in the ledger by ER-2 (:281, four legs)", "file": "corpus/knowledge/fleet-kill-rate-ledger.md", "ranges": "281", "verdict": "holds", "excerpt": "ledger:281 ER-2 §5/ER-1 supersession bullet: 'carries **four** materialized legs … REGRESSION: PASS (cases=4 passed=4…'"},
    {"id": "P29", "raw": "a ledger row recording the six-leg registry is the ledger owner's follow-on — this page records the registry as measured at r10-2, and no ledger cell is edited from here", "file": "corpus/knowledge/fleet-kill-rate-ledger.md", "verdict": "holds+understates-at-cand", "cand_note": "ledger unchanged — still no registry row; the registry is now ten legs and the ledger's §1 measured rows stop at leg 7 (round-gate :410, receipt cases=7 :412-413)", "excerpt": "ledger:410 round-gate row; :412-413 'Receipt: REGRESSION: PASS (cases=7 passed=7 …) at runner 89722ddb…'"}
  ],
  "strongest_falsifiers_checked": [
    "F1 six-vs-ten legs: CAND runner has ten wired legs (header :84, list :88-97, nlegs=10 :1510, selftest assert :2075) — CONFIRMED DRIFT.",
    "F2 TMPDIR: CAND honors TMPDIR for regression/workdir/selftest scratch (:1432/:491/:1555; header :149-150) vs the section's literal /tmp/… — CONFIRMED DRIFT.",
    "F3 selftest total: this seat ran the runner --selftest at CAND from a --shared clone (TMPDIR under scratch): rc 0, MUTATE_SELFTEST: 107/107 pass / VERDICT: PASS — 80/80 is r10-2-historical — CONFIRMED DRIFT; tool green at CAND.",
    "F4 all six blob pins recomputed from sibling repos at recorded revs — all exact; no falsification.",
    "F5 25 @old count: 15+10 in the embedded T8-1/T8-2 specs; two count==1 spot-checks against pinned blobs → 1 each; no falsification.",
    "F6 receipt provenance: closeout-r11.md:308-310/:354-358 and SKILL.md:1398 (round-18 CR30 replay at 606716f) corroborate 21:02:39Z / 21:00:24Z / 80/80 / cases=6; no falsification.",
    "F7 exit map: r30 SETUP clause added at CAND (:142-143) — CONFIRMED DRIFT.",
    "F8 REGRESSION_EXPECT: ten rates at CAND (:1446) — CONFIRMED DRIFT.",
    "F9 panel tools: none of tally-audit.py/-v2/-v3/mte-interop.py cites this section (their REF panels now ten-leg); no additional statement made false."
  ],
  "notes_for_rekey": [
    "Runner anchors were already imprecise at the governing sha (list :84-89 not :85-89; pins :542-553 outside :550-559; registry :1112-1141 not :1132-1141) — the section's 'the sha governs' hedge makes them advisory; do not copy forward as exact.",
    "VERSION string still reads 'mutate-and-run.sh r10-2' at CAND (:185) while the tool is r51-edited (2159 L) — the sha256 is the only live pin.",
    "Named-debt bullet understates at CAND: no ledger registry row exists and the registry is ten legs.",
    "specs anchors :766/:841 cover only legs 5-6; legs 1-4 specs sit at :589/:630/:675/:720 (sha) / :673/:714/:759/:804 (CAND).",
    "CAND re-anchor locations: list :88-97; sources :98-121; pins :614-625 + tables :634-643; leg-5/6 spec intros :850-853/:925-928 (cats :854/:929); registry :1459-1507; exit map :139-145; scratch :146-148 + :1432; mode-mirror :128-130 + :1281-1302; selftest exec arms :1860-1896; embedded-ledger check :2013-2014/:2072-2076; VERSION :185; REGRESSION_EXPECT :1446."
  ],
  "reads_basis": "every pointer read at the governing sha (606716f bytes), at base, and at CAND; excerpts located by line number in dumped bytes; one execution (runner --selftest at CAND, rc 0)"
}
```

## 6. Bounds

Read-only on lane/fleet/sibling repos (all reads via `git show`/`git ls-tree`/file reads); the one execution
(runner `--selftest` at CAND) ran from a `git clone --shared` in scratch with `TMPDIR` under scratch; no git
mutations anywhere; no installs. Scratch deleted before yield.

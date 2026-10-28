# T55W2RevScorecardNums — numbers in the round-55 record, re-derived

Seat: leaf reviewer, wave 2 (falsify), round 55 (hyaku run 11). Axis: calibration.
Target: every number in `SCORECARD.md` `## Round 55 - round-54 record corrections`
and in the `LOG.md` round-55 entry, **at C0 `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`**.
Nothing in the lane was edited. Scratch:
`/fast/scratch/hyaku/tameshi-r55/T55W2RevScorecardNums` (a `git clone --shared` at C0; the
counters were also re-run at base `0a2010ac` inside that clone). Census:
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit 0,
140 rows.

The standard applied here is C1's own: a number in the record must equal what the tree
derives, and the receipt it cites must print it. Values are read with `git show REV:path`,
never from the working tree (the working tree was dirty with wave-1/2 seat files throughout).

Receipts: `.ufo/waves/round-55/w2/T55W2RevScorecardNums-receipts/` (14 files, each headed
with the command that produced it). Full counter runs: `01-c1-base-rerun.txt`,
`02-c2-base-rerun.txt`, `03-c1-at-c0.txt`.

---

## 1. Base verdict lines (`before/` values)

| # | value (source) | derived | verdict |
|---|---|---|---|
| 1 | LOG: `premise=10/10` | `premise=9/10` | **DISAGREE** |
| 2 | LOG: `stale=4` | `stale=4` (rows with a stale hit: R54.1, .2, .3, .9) | agree |
| 3 | LOG: `classes_corrected=0/10`, `total=10`, `C1_R55_PASS=false` | same | agree |
| 4 | LOG: `grammar=6/8` | `grammar=6/9` | **DISAGREE** |
| 5 | LOG: `note=0/8` | `note=0/9` | **DISAGREE** |
| 6 | LOG: `total=18` | `21` on the frozen formula; `20` on the honest sum (see §3) | **DISAGREE** (both readings) |
| 7 | LOG: `lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=0/7 skill=0/1` | same, both arms re-run | agree |
| 8 | contract C1 `before`: `premise=9/10 stale=4 classes_corrected=0/10 total=10` | same as the receipt at C0 and as my re-run | agree |
| 9 | contract C2 `before`: `grammar=6/9 … note=0/9 … total=21` | prints 21; the sum of the failures the line prints is 20 (§3) | agree-with-receipt, **DISAGREE-with-arithmetic** |

Commands: `python3 .ufo/evidence/round-55/c1/measure.py --lane <clone> --rev 0a2010ac… --work <empty> --explain`
→ `C1_R55: rev=0a2010acd1e9 classes=10 premise=9/10 stale=4 classes_corrected=0/10 total=10 C1_R55_PASS=false`
(exit 1); `… c2/measure.py …` → `C2_R55: … grammar=6/9 … note=0/9 … total=21 C2_R55_PASS=false` (exit 1,
436 s). Both identical, line for line, to `before/c1.stdout` and `before/c2.stdout` at C0.
Receipts `01`, `02`, `06`.

Root cause of rows 1/4/5/6: the LOG quotes the **pre-amendment** receipts. `631cd64`
(= the initial freeze) prints exactly `premise=10/10 … grammar=6/8 … note=0/8 … total=18`;
amendments 5 and 6 re-measured those receipts with stricter bytes and the record was never
updated. Receipt `06` prints both revisions side by side.

## 2. Freeze / amendment count

| # | value (source) | derived | verdict |
|---|---|---|---|
| 10 | LOG: "frozen at `631cd645`" | the frozen manifest at C0 is last touched by `e2979f277138da503af27b263b783f626f109be4` (amendments 1-7); `631cd64` is only the initial freeze; at the lane tip the pointer is `4f7a704` (amendment 9) | **DISAGREE** (one round, one pointer — ER-R54-2's own class) |
| 11 | LOG: "amended four times … all four recorded in `freeze.json`" | `len(amendments)` = **7** at C0, **9** at tip | **DISAGREE** |
| 12 | `corpus/lessons/round-55.md:3-4`: "counter freeze `631cd645` + amendments 1-4" | 7 at C0 | **DISAGREE** (same stale pair) |
| 13 | freeze manifest integrity at C0 | 7/7 file digests match the C0 blobs | agree |

Receipt `05`.

## 3. The C2 total (formula, not measurement)

The frozen `c2/measure.py` at C0 (`:271-273`) computes
`(len(table)-empty_ok) + (len(table)-usable_ok) + (7-docs) + (8-note) + …` while `table` has
14 rows, the empty/usable arms run 13 `cheap` modes and the note arm prints a denominator of 9.
Applied to the arm values the base receipt prints (grammar 6/9, lazy 5/5, empty 13/13,
usable 13/13, tmp 0, docs 0/7, note 0/9, skill 0/1):

```
frozen formula at C0 (c2/measure.py:271-273)  total = 21
tip formula (133b2ce, amendment 8)           total = 20
sum of the failures the line prints           total = 20
```

So `total=21` is two phantom rows (`table` 14 vs `cheap` 13) minus one under-counted note term
(8 vs the printed 9). `C2_R55_PASS=false` is unaffected (the `bad` map is non-empty regardless),
but the quoted magnitude was wrong at C0. Amendment 8 (`133b2ce`) fixes the code and F4
(`c31cdd9`) rewrites the contract's C2 `before` to `total=20`; at tip the contract and
`before/c2.stdout` both read 20. Receipts `09`, `02`.

## 4. Wave-1 seat count and attack share

| # | value (source) | derived | verdict |
|---|---|---|---|
| 14 | LOG: "one v2 wave of 75 seats" | `len(members)` = 75; `w1-dispatch.json` `counts: {"spawn":75,"resume":0,"total":75}`; `spec-w1.json` has 75 items | agree |
| 15 | LOG: "28 attack roles" | 28 **only** by importing round-54's rule (`reviewer 18 + critic 6 + mutation-tester 4`); the round-55 registry stores no `attack_seats` field | agree under the imported rule; not stated by the artifact |
| 16 | LOG: "= 37.3 %" | 28/75 = 37.333 % → 37.3 % | agree |
| 17 | LOG: "band 64–128" | contract `shape`: "one v2 wave (band 64-128 …)" | agree |

Commands and outputs in receipt `04`/`07`. Note on 15: the round-55 registry is
`.ufo/waves/round-55/w1/swarm-registry.json` (`ufo-swarm-registry-v1`, keys
`createdAt/members/reportDir/schema/updatedAt/wave`), whereas round 54's
`.ufo/waves/round-54/w1-registry.json` carries `seats`, `attack_seats` and `role_mix` — the
three fields `c1/measure.py:wave_numbers()` reads. The path named by this seat's item
(`.ufo/waves/round-55/w1-registry.json`) does not exist at C0 (`git cat-file -e` → rc 128).
The numbers are right; the artifact cannot re-derive them the way the round's own counter
derives R54.9.

## 5. Row count

| # | value (source) | derived | verdict |
|---|---|---|---|
| 18 | block: "ten record defects" / ER-R54-1..10 | 10 `**ER-R54-` rows; spot-check file names exactly R54.1-R54.10 | agree |
| 19 | block/LOG: "SOURCES S280 admitted" | 140 `| S### |` rows at C0; census exit 0; S280 row present, footer "Next unused id: S281" | agree |

Receipt `12`.

## 6. Every ER row's number, re-derived

| row | number in the block | derived | verdict |
|---|---|---|---|
| ER-R54-1 | `CTL_MISMATCH`, `expected=true actual=false`, `2/3` | `controls-b.stdout` prints all three | agree |
| ER-R54-2 | "one pointer, `077d431e` (5 amendments)"; old `7883e0e5`/`fe70474d`/`097985c1` | round-54 freeze has 5 amendments; `after/frozen.stdout` prints `freeze=077d431e69965fa4…`; the three old pointers exist at base (SCORECARD:2564/:2567/:2608; fleet report `.ufo/reports/round-54/tameshi.md`) | agree |
| ER-R54-3 | old `total=14` → corrected `total=13` | base SCORECARD:2584 quotes 14; `round-54/before/c2.stdout` prints `total=13` | agree |
| ER-R54-4 | old `49280fe5` → `8528ee85` | round-54 `freeze.json` `c2/measure.py` = `8528ee8555da0685…`; `49280fe55bd9361c…` is the amendment-2 digest quoted by `T54W1ExecStraceNoise.md` | agree |
| ER-R54-5 | old "25 wave-1; 22 wave-2 in 9 sections" → `w1=28 w2=25 sections=12`, "28 across 23 reports", "25 across 12 of the 23" | old values are in `round-54-verifier-spotcheck.md:116`; derived: 23 w1 reader files / 28 findings, 23 w2 files / 25 findings, 12 w2 files with findings | agree |
| ER-R54-6 | `ff2a821` | commit exists and is the first touching `T54W2Sent03.md`; the three files exist | agree |
| ER-R54-7 | `7fa9a5e`, `R100` | `7fa9a5e` renames the file `R100` into `…-receipts/forged-reader.json`; the old path is gone | agree |
| ER-R54-8 | row 690, `2026-10-28T15:12:15Z`, `scout: "@m_grok"`, "5 m 33 s" | `history.db` id=690 prompt=`use m_glm53 instead of m_grok`, created_at 1793200335 → 2026-10-28T15:12:15Z; `~/.omp/agent/config.yml:418` = `scout: "@m_grok"`; **5 m 33 s is self-reported** in `T54W1ExecStraceNoise.md:336-337` — no lane artifact carries the yield timestamp | agree on 690/timestamp/config; 5 m 33 s **not independently re-derived** |
| ER-R54-9 | `reviewers=5 attack=21/76 seats=76` (27.6 %), `staged=81` | registry `seats 76`, `attack_seats 21` = 5+4+12, 21/76 = 27.63 % → 27.6 %; `staged-at-freeze.txt` `output=81`; live `find /home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge -name '*.md' | wc -l` → 81 | agree |
| ER-R54-10 | `rekeyed=0/7` (controls-a) vs `rekeyed=0/30` (r53-counter-at-88afa941) | both receipts print exactly that; the `rekeyed=0/30` reading is the round-53 counter's own line | agree |

Receipts `11`.

## 7. Other numbers in the LOG entry

| # | value | derived | verdict |
|---|---|---|---|
| 20 | "hyaku run 11" | only the LOG's own antecedent states it (`LOG.md:2498`, round-54 attempt 2 = "hyaku run 11"); `.ufo/state/tameshi.round` = 1, no other artifact carries a run ordinal | agree by chain; no independent artifact |
| 21 | "Base `0a2010ac`" | commit exists and is the contract's `base` | agree |
| 22 | "the 15 no-harm monitors" | `no-harm.sh` emits 15 `NOHARM` lines | agree |
| 23 | "the seven registry `scratch_root` cells" | `tools/registry.json` has 56 rows, 7 with `scratch_root` | agree |
| 24 | "the eight allocating modes plus the five lazy ones" | **nine** allocating modes (7 self-tests + `env-diff --contract` + `registry-check --rev`); the note names all nine; the counter measures 9; freeze amendments 6 and 8 both say nine | **DISAGREE** |
| 25 | "QUALITY 106 (a control is scored at the revision it certifies) with an erratum on 105" | **no criterion 106 exists** — `corpus/QUALITY.md` at C0 ends at `### Criterion 105` (30 criteria), `grep -c "Criterion 106"` = 0, `git log -S "Criterion 106"` = no commit ever introduced it, and QUALITY has no round-55 section; the "erratum on 105" is an in-place rewrite of 105's falsifier (1 line deleted, 1 added) | **DISAGREE** |
| 26 | "one SKILL.md section the edit drifts (`## Standing rules`)" | `git diff 0a2010ac 9cf0146 -- SKILL.md` = one hunk, 7+/3-, inside the scratch bullet of that section | agree |
| 27 | "the sysexits candidate refused as a duplicate of S090" | S090 is `sysexits(3) (FreeBSD 15.1)`; SOURCES footer records the refusal with reason CORPUS.md rule 2 | agree |

Receipts `08`, `10`, `12`, `13`.

---

## Findings (severity order)

1. **HIGH — the LOG entry contradicts the receipt it cites: `premise=10/10` vs `9/10`.**
   `LOG.md` (round-55 entry, at C0 and unchanged at the lane tip) quotes `premise=10/10`
   from `.ufo/evidence/round-55/before/c1.stdout`, which prints `premise=9/10`; my re-run of
   the frozen counter at base prints `premise=9/10` too. This is ER-R54-1/ER-R54-3's exact
   defect class (a quoted value its own receipt does not contain), recurring inside the round
   that corrects it. `C1_R55` cannot see it: none of its ten stale patterns covers round-55
   prose (verified on both the C0 and tip counter bytes — no pattern matches
   `premise=10|total=18|grammar=6/8`) while `stale=0 classes_corrected=10/10 … PASS=true` at C0.

2. **HIGH — `QUALITY 106` does not exist anywhere in the lane's history.** The LOG entry
   ("QUALITY 106 (a control is scored at the revision it certifies) with an erratum on 105"),
   the C0 commit message ("QUALITY 106 + 105 erratum") and `corpus/lessons/round-55.md` (:31
   and the R54.1 row of its mapping table) all assert it; QUALITY's highest criterion is 105,
   no commit ever introduced 106, and 105 was rewritten in place rather than appended as the
   dated erratum the file's own rules (:263-277) require. `corpus/lessons/round-55.md` uses
   "QUALITY 106" as R54.1's receipt, so the lesson's evidence pointer resolves to nothing.
   Unchanged at the lane tip. (A record claim, not a counter arm: no C1 row reads QUALITY's
   criterion count.)

3. **HIGH — the LOG's C2 base line is the pre-amendment receipt: `grammar=6/8 … note=0/8 …
   total=18`, and "the eight allocating modes".** The amended receipt at C0 reads
   `grammar=6/9 … note=0/9 … total=21`; the note, the counter and freeze amendments 6/8 all
   carry nine allocating modes. The LOG therefore quotes a smaller surface than the claim it
   announces (C2's target is 9/9) and a total three off. Receipt `06`.

4. **MEDIUM — the freeze pointer and amendment count are stale in two records.**
   "frozen at `631cd645`, amended four times" (LOG) and "`631cd645` + amendments 1-4"
   (`corpus/lessons/round-55.md:3-4`) vs the manifest at C0 (7 amendments, last written by
   `e2979f2`) and at the tip (9). This is ER-R54-2's "one pointer for the round" class in the
   round that lands the correction.

5. **MEDIUM — the C0 record quotes `total=21` where its own printed failures sum to 20**
   (contract C2 `before`, `before/c2.stdout`, and the LOG's pointer to it). Two phantom rows
   (`table` 14 vs `cheap` 13) are added and the note term uses 8 against a printed denominator
   of 9. Already repaired after C0 — code at `133b2ce` (amendment 8), contract/receipt at
   `c31cdd9` (F4) — so this finding's residue is only that the round-55 LOG still speaks of
   `total=18` for the same line.

6. **LOW — the wave-1 attack share is not stated by any committed field.**
   `swarm-registry.json` does not record `seats`/`attack_seats`/`role_mix` (round-54's
   registry did, and `c1/measure.py:wave_numbers()` reads exactly those keys); the number 28
   is reproducible only by importing round-54's role rule. The seat item's path
   `.ufo/waves/round-55/w1-registry.json` does not exist at C0 (`git cat-file -e` rc 128). The
   values themselves (75 / 28 / 37.3 %) are correct.

7. **LOW — ER-R54-8's "5 m 33 s" has no independent receipt.** Row id (690), prompt and
   timestamp (2026-10-28T15:12:15Z) all re-derive from `~/.omp/agent/history.db`; the interval
   is quoted from the seat file's own narrative (`T54W1ExecStraceNoise.md:336-337`).

8. **INFORMATIONAL — a frozen file was edited in place in the working tree during this wave.**
   At 14:29Z `.ufo/evidence/round-55/before/c2.stdout` was modified (last line `total=21` →
   `total=20`, plus a trailing `exit=1`; captured verbatim in receipt `14`); when I re-checked
   at 14:44Z it was clean again, and `c31cdd9` has since committed that value properly. No
   action needed beyond noting that a wave seat wrote a frozen receipt directly; my own
   counter re-runs used `git show REV:path` and the clone, never the working-tree copy.

## Residual risk and verification gaps

- **C1's PASS at C0 is true only over its ten round-54 patterns.** The round's own new prose
  (LOG, lessons/round-55.md) is outside every arm; findings 1-5 are all invisible to it. This
  is a surface fact about the counter, not (only) a defect in the LOG: no arm reads a round-55
  value against its receipt.
- I re-ran both counters at base (frozen C0 bytes, 3.5 s / 436 s) and C1 at C0; I did not run
  the deciding script, and I did not re-run either counter at the lane tip (4f7a704) — my tip
  statements are `git show` reads of the specific values named.
- The lane moved while I worked (`133b2ce` amendment 8, `c31cdd9` F4, `4f7a704` amendment 9).
  My table is at C0 as instructed; §3 and finding 5 note where a tip fix already landed.
- Round-54's fleet report and `~/.omp/agent/` were read read-only; no sibling lane, `.ufo/state/`
  or `.scratch/` content was written.
- No tooling was installed (python3, git, sqlite3, strace all present).

# MutC2m12Prose — does m12 tell prose from the planned field?

Scope: one mutation probe against C2's m12 class at the freeze of record
`3aee2c078f8976499b587086af3577fc94dc8cf1` (contract `round=43`, C2 counter pin
`97609511bb77e97022d355c309a7bdc9ff7a2c74c48ac9622de600d1d28ef8d0`), run entirely in
`/tmp/tameshi-r43-w2-MutC2m12Prose-/`. The lane checkout, its Git/jj state, the fleet repo and
`/home/vgpnk/Projects/shokuknow` were not written. One lane file was created by this seat: this
report. No counter was run at the records commit `c5335c70…` (the SCORECARD there was inspected
with `git show` only); counters ran only at the permitted base and freeze revs.

## Verdict

**The item's A/B passes: m12 fires on a prose-only block and is clean when the field is added.**
The class does **not** distinguish prose from the field in general, and the contract's own
parenthetical is false as implemented: `contract.json:51` says "a prose mention is not the
field", but a prose mention that reproduces the exact bold token — in a code span, a blockquote,
a fenced template, an HTML comment, a table cell, or a negated sentence — reads **clean**
(`m12=0`). The detector is `block_text.find('**Planned (round N+1):**')` anywhere in the newest
block, plus a non-empty same-line tail (`calibration/measure.py:124-141`), not a field test.

Secondary, same claim (record agreement, calibration axis):
- the base is `m12=2 total=3` under the frozen counter, while `contract.json:41` and
  `SCORECARD.md:2060` still record `m12=1 total=2` (the A10 receipt `before/c2-at-base-A10.stdout`
  is byte-identical to my run, so the evidence exists but the two statements were not updated);
- the C2 row's declared counting command still passes `--freeze 17f6ef0c…`
  (`SCORECARD.md:2060`), whose pinned counter is `092c76cd…`, so the documented command prints
  `self_pin=0` and can never satisfy the target;
- A10's new "field names something" branch has **no selftest case**, so a mutant that deletes it
  passes `--selftest` (exit 0) while changing m12's answer on a bare field.

## 1. Setup

```
$ git clone --shared -q /home/vgpnk/Projects/shokunin/tameshi-shokunin \
      /tmp/tameshi-r43-w2-MutC2m12Prose-/lane
$ git -C /tmp/tameshi-r43-w2-MutC2m12Prose-/lane checkout -q 3aee2c07…
$ sha256sum lane/.ufo/evidence/round-43/calibration/measure.py
97609511bb77e97022d355c309a7bdc9ff7a2c74c48ac9622de600d1d28ef8d0   # == contract pin
$ git -C lane config user.email w2-m12@tameshi.test && git -C lane config user.name MutC2m12Prose
```

The clone is byte-identical to the frozen counter, so its `self_pin` is 1 (all runs below print
`self_pin=1`). Each variant below is one commit on top of the freeze that rewrites only
`SCORECARD.md`; the counter file is never touched.

Variant bytes (the round-43 block already ends with one field, `SCORECARD.md:2076`, followed by
the standing `sources-registry` row; `SEG` is exactly the four-line original field paragraph):

```
SEG        = "**Planned (round 44):** the whole-set staged adoption the guard's floor rule now admits (a map over
              all 103 staged rows, injective and disjoint from the registry), and the two guard refusal classes
              wave 2 leaves unfixed; the `cmp` / `git diff --exit-code` comparator lattices stay unmeasured since
              round 39."
PROSE      = "We Planned (round 9) things in prose."
A_prose43           : block 43 with SEG replaced by PROSE                       (no **Planned (round 44):**)
B_field43           : A_prose43 + "\n\n" + SEG                                  (field added)
C_field43_wronground: SEG replaced by "**Planned (round 43):** still prose"      (field for the current round)
D_quoted_field43    : SEG replaced by "The block carries no `**Planned (round 44):**` field; " + PROSE
E_negated_bold      : SEG replaced by "There is no **Planned (round 44):** field this round; " + PROSE
F_empty_field       : SEG replaced by "**Planned (round 44):**"                  (bare field)
A9_prose_head9      : freeze bytes + "\n\n## Round 9\n\n" + PROSE                (item-literal block heading)
B9_field_head9      : A9_prose_head9 + "\n\n**Planned (round 10):** next round work."
```

## 2. Full-counter A/B (item's primary ask)

Command, identical for every row (`FREEZE=3aee2c07…`, `REV` = the variant commit):

```
$ python3 lane/.ufo/evidence/round-43/calibration/measure.py \
    --lane /tmp/tameshi-r43-w2-MutC2m12Prose-/lane --rev REV --freeze 3aee2c07…
```

| variant | REV | m12 | total | exit |
|---|---|---|---|---|
| A_prose43 (prose, no field) | `9cd6b5ae68fb2a640545a1dd9f138a6773549162` | **1** | 9 | 1 |
| B_field43 (prose + field) | `add40d02ff51f34e2aa331d56899625cebb71e21` | **0** | 8 | 1 |
| C_field43_wronground | `3a37669bf6cfbebbca79b1cacc3f0ec072e15495` | **1** | 9 | 1 |
| D_quoted_field43 (no field) | `b44a1c3bf1231842ddec6427ed1dd8e0882dc01f` | **0** | 8 | 1 |
| E_negated_bold (no field) | `65a024ca4b8c8c49408f7213feff62d25ec7da1a` | **0** | 8 | 1 |
| F_empty_field (bare field) | `580c7b8f2f7fb381a0491cb318e9b26e2a125c1e` | **1** | 9 | 1 |
| A9_prose_head9 | `af18384444aa1d11210467c5c3382016612d90f7` | **2** | 30 | 1 |
| B9_field_head9 | `42205b26557dc34b7fe0f4c45a7f9ee680988d70` | **1** | 29 | 1 |

Verbatim, A then B:

```
$ … --rev 9cd6b5ae68fb2a640545a1dd9f138a6773549162 --freeze 3aee2c078f8976499b587086af3577fc94dc8cf1
C2_R43: self_pin=1 classes=7 m6=0 m7=5 m8=3 m10=0 m11=0 m12=1 m13=0 total=9 records=4 sources_rows=114 standing=114 receipts=17 revisions=2 m13_probe=standing=7_column0=113_valid=114 rev=9cd6b5ae… freeze=3aee2c07… C2_R43_PASS=false first=m7:corpus/lessons/round-43.md_unknown_S160
EXIT=1

$ … --rev add40d02ff51f34e2aa331d56899625cebb71e21 --freeze 3aee2c078f8976499b587086af3577fc94dc8cf1
C2_R43: self_pin=1 classes=7 m6=0 m7=5 m8=3 m10=0 m11=0 m12=0 m13=0 total=8 records=4 sources_rows=114 standing=114 receipts=17 revisions=2 m13_probe=standing=7_column0=113_valid=114 rev=add40d02… freeze=3aee2c07… C2_R43_PASS=false first=m7:corpus/lessons/round-43.md_unknown_S160
EXIT=1
```

`m7=5 m8=3` are constant across all rows (the pre-records state of `corpus/lessons/round-43.md`
at the freeze; the records commit is the L1's to measure), so the m12 delta is the only movement:
**9 → 8 is exactly m12's hit.** The item-literal round-9 pair moves identically: `m12=2 → 1`
(A9's two hits are the missing `**Planned (round 10):**` plus the A10 block-round binding
`newest block is round 9, the contract round is 43`; B9 keeps only the binding hit). Both A/B
pairs therefore answer the item's question **yes**: the m12 class fires on prose and is clean on
the field.

## 3. Direct-import matrix (isolates m12 from the other six classes)

`m12_planned(block, round_no)` on the pristine frozen counter:

```
A_r43_prose_only            -> ['**Planned (round 44):**']
B_r43_prose_plus_field      -> []
C_r43_field_wrong_round     -> ['**Planned (round 44):**']
D_r43_quoted_field_codespan -> []                                   <-- no field, reads clean
E_r43_negated_bold          -> []                                   <-- no field, reads clean
F_r43_bare_field            -> ['**Planned (round 44):** names nothing']
G_r43_field_indented        -> []                                   (2-space paragraph: a real field)
H_r43_field_quote_md        -> []                                   <-- "> **Planned (round 44):** quoted"
I_r43_fenced_template       -> []                                   <-- inside ``` fence
J_r43_html_comment          -> []                                   <-- "<!-- **Planned (round 44):** draft -->"
field_in_table_cell         -> []                                   <-- "| a | **Planned (round 44):** b |"
tail_html_comment_only      -> []                                   <-- "**Planned (round 44):** <!-- tbd -->"
tail_punctuation_only       -> []                                   <-- "**Planned (round 44):** ."
A9_r9_prose_only            -> ['**Planned (round 10):**']
B9_r9_prose_plus_field      -> []
```

`m12_planned` returns `hits`; empty = clean. Load-bearing bits confirmed: `round_no + 1`
(measure.py:131) and the `**…:**` markers (prose without the token always fires); the non-empty
tail (measure.py:137-139) catches a bare field.

## 4. Finding F1 — the class accepts a quoted field token as the field

`calibration/measure.py:124-141` locates the literal `**Planned (round N+1):**` with
`block_text.find` anywhere in the newest block. Nothing anchors it to the start of a line, and
nothing excludes code spans, fences, blockquotes, HTML comments or table cells. So all of D, E,
H, I, J and the table-cell probe above are **false cleans**: the newest block carries no
`planned` entry, yet `m12=0`.

Reproduction (full counter, no import needed) is row D/E in §2. The block is:

```
## Round 43

The block carries no `**Planned (round 44):**` field; We Planned (round 9) things in prose.
```

`m12=0 total=8`, i.e. the class certifies a block that says in words it has no field. This is the
same shape as the A10 defect `CritC2Gaming` fixed (a laundered block, an empty field) but through
a different door: the token is present *as prose about the token*. The contract's class sentence
(`contract.json:51`), the counter docstring (`measure.py:127-129`: "a prose mention of the same
words is not the SCORECARD contract's `planned` entry, so the check is the field, not a substring")
and A6's "a prose 'Planned' passed m12" repair are all falsified for the mention form that
reproduces the bold token. The circle is not closed by A10.

A detector that does distinguish, for reference only — no contract change proposed here:

```
re.compile(r'^ {0,3}\*\*Planned \(round N\+1\):\*\*[ \t]*(\S.*)?$', re.M)   # + fence tracking
   A_prose43 -> fires   B_field43 -> clean   D/E -> fires   F_bare -> 'names nothing'
   I_fenced -> fires    J_html_comment -> fires
```

The current `README`/report style quotes fields verbatim all the time, so this is reachable, not
academic; at the freeze the count of `**Planned (round 44):**` in the round-43 block is exactly 1
(the real field), so the defect is latent for the deciding run unless the after-subsection or a
later edit quotes the field.

## 5. Finding F2 — A10's tail check is untested; a mutant survives the selftest

A10 added the `names nothing` branch (`measure.py:137-139`) and a block-round binding
(`measure.py:401-402`, `443-447`). The selftest has exactly three m12 cases
(`measure.py:307-316`): `T1_missing_planned_detected`, `T1_planned_present_clean`,
`T1_prose_only_detected`. **No case exercises an empty/punctuation-only field.**

Mutant probes applied to copies of the frozen counter in `/tmp` (`m12_planned` replaced, nothing
else; each run through `--selftest` and the §3 matrix):

| mutant | selftest | behavioural delta vs pristine |
|---|---|---|
| `M1_tail_check_removed` (`if find(…) < 0: hits.append(wanted)`) | **exit 0, 0 fails — SURVIVES** | `F_r43_bare_field`: pristine `['**Planned (round 44):** names nothing']` → mutant `[]` |
| `M2_off_by_one_round` (`% round_no`) | exit 1 — killed by `T1_missing_planned_detected` | 8/8 matrix rows change (prose for the current round now satisfies it) |
| `M3_markers_dropped` (`'Planned (round %d)'`) | exit 1 — killed by `T1_prose_only_detected` and `T1_missing_planned_detected` | prose without the token is accepted (A, C, F, A9 change) |
| `M4_tail_anywhere_in_block` (tail = rest of block) | exit 0 — behaviourally equivalent on the matrix | none |

Verdict: the round+1 binding and the `**…:**` anchoring **are** load-bearing and the selftest
holds them (M2, M3 die). The A10 tail branch **is not** load-bearing against the selftest (M1
survives and materially changes the answer on a bare field): A10 shipped code with no case, which
is a coverage finding, not a contract problem.

Also verified as *working* (not findings): the A10 block-round binding catches the laundered
`## Round 44` block (`newest_round_block` → 44, m12 = `['newest block is round 44, contract 43']`),
and a bare field is caught by the tail branch.

## 6. Finding F3 — the recorded base disagrees with the frozen counter's own receipt

```
$ python3 lane/.ufo/evidence/round-43/calibration/measure.py --lane /tmp/…/lane \
    --rev 487b8f0da89fa0e2b8bea6930068accbf36e70a9 --freeze 3aee2c078f8976499b587086af3577fc94dc8cf1
C2_R43: self_pin=1 classes=7 m6=0 m7=0 m8=0 m10=0 m11=0 m12=2 m13=1 total=3 records=3 sources_rows=113 standing=113 receipts=17 revisions=3 m13_probe=standing=6_column0=112_valid=113 rev=487b8f0… freeze=3aee2c07… C2_R43_PASS=false first=m12:**Planned_(round_43):**
EXIT=1
```

This output is **byte-identical** to `.ufo/evidence/round-43/before/c2-at-base-A10.stdout`
(`diff` clean). The second m12 hit is the A10 binding: the base's newest block is round 42
(`SCORECARD.md` at the base ends at `## Round 42`, line 1995), the contract round is 43.

But the claim's own before-state still says `m12=1`:
- `contract.json:41` — `"before_state": "m12=1 (the round-42 SCORECARD block carries no
  'Planned (round 43)' line …) and m13=1 …"`;
- `SCORECARD.md:2060` — Before cell `` `m12=1 m13=1 total=2 classes=7 C2_R43_PASS=false` ``,
  citing `before/c2-at-base.stdout` (the superseded pre-A10 counter, `freeze=f0f26367…`);
- the same line is still there at the records commit `c5335c70…` (checked with `git show`; no
  counter run).

A10's effect says the base receipt was "re-run with the final counter and the new line recorded
beside the old one" — it was, but the two prose statements were not updated, so the record cites
`total=2` for a counter that prints `total=3`. The m6–m13 classes do not read claim cells, so
this is invisible to the counter. Calibration-axis, m12-specific.

## 7. Finding F4 — the declared counting command cannot pass at the freeze

`SCORECARD.md:2060` (and `2059`, `2061`) advertises:

```
python3 .ufo/evidence/round-43/calibration/measure.py --lane LANE --rev REV --freeze 17f6ef0c72ec27e1aea305b5c95806b43bb2caef
```

Run verbatim at the freeze rev:

```
$ python3 lane/.ufo/evidence/round-43/calibration/measure.py --lane /tmp/…/lane \
    --rev 3aee2c078f8976499b587086af3577fc94dc8cf1 --freeze 17f6ef0c72ec27e1aea305b5c95806b43bb2caef
C2_R43: self_pin=0 classes=7 m6=0 m7=5 m8=3 m10=0 m11=0 m12=0 m13=0 total=8 … C2_R43_PASS=false
EXIT=1
```

`self_pin` compares the running counter (`97609511…`) and the counter at `--freeze` against the
pin in `contract.json@<freeze>`; the pin at `17f6ef0c…` is `092c76cd6e10f9280af21237ec90dc14e63f0bdb9ae74fffb9da841730a8f286`.
A10 moved the freeze of record to `3aee2c07…` and repinned C2 there, but the three scorecard rows
still name the earlier freeze, so the declared command is unsatisfiable by construction: the
deciding run must use `--freeze 3aee2c07…` (or the row must be updated). Same shape applies to
C1/C3 rows, which also name `17f6ef0c…`.

## 8. What this settles

- **Settles the item:** m12 fires (`m12=1`) on a newest block carrying `We Planned (round 9)
  things in prose.` and no field, at the full-counter level and by direct import; adding
  `**Planned (round 44):** …` clears it (`m12=0`), the same shift the item-literal round-9 pair
  shows (`2 → 1`, the residue being the A10 block-round binding). The class does distinguish the
  two bytes at issue.
- **Kills the general claim:** "a prose mention is not the field" (`contract.json:51`) is false
  for any mention that reproduces the exact token. Six non-field shapes read clean (F1); the
  remedy is a line-anchored, fence-aware match, not a substring.
- **Coverage gap:** A10's tail branch has no selftest case; `M1_tail_check_removed` survives
  `--selftest` and changes m12 (F2).
- **Record agreement:** the base is `m12=2 total=3` under the frozen counter vs `m12=1 total=2`
  in `contract.json:41` / `SCORECARD.md:2060` (F3), and the declared counting command's freeze
  pin cannot pass (F4). Both are calibration-axis findings on the same claim; no contract or
  counter change is proposed or made here.
- **Not settled / out of item:** whether the round-43 C2 predicate passes at the measured commit.
  That is the L1's deciding run at `c5335c70…`; this seat did not run any counter there.

## 9. Restoration / cleanup evidence

- Lane C2 counter `sha256` at probe start: `97609511bb77e97022d355c309a7bdc9ff7a2c74c48ac9622de600d1d28ef8d0`
  (== contract pin at `3aee2c07…`). The lane file was only ever read; the mutated copies lived in
  `/tmp/tameshi-r43-w2-MutC2m12Prose-/mut/` and are now deleted.
- **Drift during the probe (not mine):** the lane advanced from `e20cf89` to `6b83a11` while this
  seat ran — commits `b510ad1` (A11), `bb36f80` (A12), `f551ca6` (A13: m7/m8/m10 repairs),
  `e25cd2f`, `6b83a11` (A14). The counter at HEAD is now `ab76cbd3c98f3ef861c2e95ebe1407b42a3756b9550909c8c10556da1e9e8b36`.
  A `diff` of `def m12_planned` and of the block-round binding between the tested freeze
  `3aee2c07…` and `6b83a11` is empty — the code under test is byte-identical, so F1/F2 hold at the
  current freeze. F3/F4 also persist at HEAD: `contract.json:42` still says `m12=1`,
  `SCORECARD.md:2060` still says `m12=1 m13=1 total=2` and still names `--freeze 17f6ef0c…`
  (whose C2 pin `092c76cd…` matches neither the tested counter `97609511…` nor HEAD `ab76cbd3…`).
- The scratch clone's HEAD moved through eight variant commits (`9cd6b5a`…`42205b2`) on top of
  `3aee2c0`; those commits exist only in `/tmp` and were never fetched, pushed or referenced.
- Scratch deleted after this report: `/tmp/tameshi-r43-w2-MutC2m12Prose-/` (lane clone, eight
  variant commits, four mutant counter copies).
- Bounds: read-only on the lane; the only lane write is this file; no mutating `git`/`jj`
  command in the lane; no write to `/home/vgpnk/Projects/shokuknow`; no tool installed or upgraded
  (nothing needed).

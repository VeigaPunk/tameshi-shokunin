# RevLessonMistakes — do the `## Mistakes` rows' `shown able to fail` claims hold?

Seat: reviewer, wave 2 (falsify). Item: for each row of the `## Mistakes` table
in `corpus/lessons/round-43.md`, run or read the evidence it names — the guard's
held set, the C1 control receipt, the pre-fix guard refusal, the C2 base
receipt's m10 — and say whether the fix column's `shown able to fail` claim
holds. Read-only on the lane; all reproductions under
`/tmp/tameshi-r43-w2-RevLessonMistakes/` (kept for inspection; nothing else
written). No counter was run at the records commit `c5335c70`; every counter run
below used `--rev 487b8f0` or `--rev 3aee2c0`. No tool installed or upgraded.

**Moving tree note.** The lane was live throughout the audit: HEAD went
`b510ad1` → `bb36f80` → `f551ca6` → `e25cd2f` → `6b83a11` (A11–A14 freezes plus a
lesson reword) while I worked, and `corpus/lessons/round-43.md` carries
uncommitted edits. Everything below is anchored to a rev or to the working-tree
bytes at the stated moment; the table itself (10 rows at `round-43.md:123–135`)
was unchanged by the later edits except row 3's map text (see row 3).

## Verdict per row

| # | row (line) | verdict |
|---|---|---|
| 1 | duplicate-document append (:125) | **partially fails** — held set verified but only post-append; captured-by W04 unrecorded; row breaks the table (extra `|`) |
| 2 | frozen-rule-without-code (:126) | **fails as cited** — one of the two cited receipts does not exist where the row says |
| 3 | join-then-fullmatch (:127) | holds; "14 cases" stale (23 at records, 24 at HEAD) |
| 4 | control-kept-the-kill-fixture (:128) | holds, reproduced exactly; defect side reproduced with pre-A2 counter |
| 5 | lstrip-on-a-dotpath (:129) | holds; pre-fix `m10=9` has no committed receipt but I reproduced it |
| 6 | single-tool-pin-field (:130) | holds, reproduced |
| 7 | classes-is-a-constant (:131) | holds |
| 8 | extractor-narrower-than-the-sentence (:132) | **fails** — "three new selftest cases" is two, and the third is the guard's case, not C2's |
| 9 | asserted-digest-equality (:134) | holds, reproduced |
| 10 | uncounted-quote-length (:135) | **fails** — the "restored verbatim" quotation lacked `or` at every committed rev through HEAD; the cited command is not in the named report |

## F1 (high) — row 10: the claimed restoration is false at every committed rev

`corpus/lessons/round-43.md:135` fix column: "word counts corrected and the
quotation restored verbatim … Shown able to fail: `python3 -c` word count on the
line, pasted in the report".

```
$ git show 6b83a11:corpus/lessons/round-43.md | sed -n '51,54p'
- Located quotes: line 16 (12 words) "There is no definitive way for Stryker to
  find and ignore them."; line 15 (20 words) "even if we change >= to <= and
  even < > we will get the same output each time!"; line 17 (9 words) "the only
  solution is by finding these by hand".
```

The snapshot's line 15 reads "even **< or >**"
(`.ufo/evidence/round-43/sources/stryker-equivalent-mutants.html:15`, verified:
`even if we change >= to <= and even < or > we will get the same output each
time!`, 28 rendered words on the line; the quoted span is 20 words **with** `or`,
19 as printed). Every committed rev — `c5335c7` (records), `b510ad1` (A11, which
added the row), `e25cd2f`, `f551ca6`, `bb36f80`, `6b83a11` (HEAD at close of
this audit) — still quotes `even < >`. The `or` was restored only in the
uncommitted working tree while this audit was in flight. So the row's
"restored verbatim" claim was untrue at the deciding rev and at every committed
rev since the row existed; the "(20 words)" annotation counts a word the printed
quotation did not contain.

The evidence description is also mis-cited: the row says "`python3 -c` word
count on the line, **pasted in the report**" and "re-run by the L1 with
`split()` counts", but `grep -n 'python3 -c\|split()'
.ufo/waves/round-43/w1/ScribeLessonGate.md` returns nothing — the report's D2/D3
show `printf '%s' "<span>" | wc -w` → 16 and → 15. The substance is true (my own
`split()` counts on the committed snapshot: 794→16, 796→15, 15→20-with-`or`),
but the named reproduction is not in the named report.

## F2 (medium) — row 2: one cited receipt does not exist in `control/`

`:126` claims "Shown able to fail: `control/c1-round42-battery.stdout` (ten
fixtures → 4 kills) and the F11 ablation (`11/11` → `5 kills, 1 equivalent×`),
both in `.ufo/evidence/round-43/control/`".

`ls .ufo/evidence/round-43/control/` (at HEAD and at `c5335c7`,
`git ls-tree -r --name-only c5335c7 .ufo/evidence/round-43/control/`): seven
files — `c1-probe-survivors.stdout`, `c1-round42-battery{.exit,.stdout,-A10.stdout}`,
`c2-round42-counter.stdout`, `c3-constant-empty{.exit,.stdout,-A10.stdout}`,
`constant-empty-tool.py`. **No ablation receipt.** The `11/11 → 5 kills, 1
equivalent` run exists only as transcribed output in
`.ufo/waves/round-43/w1/MutC1F11.md` §2 (Run B, verbatim line confirmed:
`fixtures_pass=11/11 … mutants_killed=5 … equivalent=1`).

Substance check: neither cited artifact actually exercises the A5 gate — the
control is the do-nothing battery (row 4's subject), the ablation is F11
attribution. The gate's failure is provable, but by the pre-A5 unmodified run
(`mutants_killed=6 dead_code_only=0`, reproduced below) versus the post-A5
`dead_code_only=1` of `prerun/c1-at-freeze.stdout`:

```
$ git show 17f6ef0:.ufo/evidence/round-43/mutants/measure.py > /tmp/…/c1-17f6ef0.py
$ python3 c1-17f6ef0.py --lane LANE --rev 3aee2c0 --freeze 17f6ef0
C1_R43: self_pin=1 tool_absent=0 tool_sha_ok=0 … mutants_killed=6 dead_code_only=0
… killed_names=…,method_fold_several_returns,… C1_R43_PASS=false
```

So the claim "the dead-code fixture counted as a kill" is true and reproducible;
the "shown able to fail" pointer names one non-existent file and one
non-dispositive receipt.

## F3 (medium) — row 8: "three new selftest cases" is two, and one named case is the guard's

`:132` fix column: "amendment A6: … three new selftest cases (prose-only
`planned`, column-zero-plus-prose `0,3`, multi-entry map)".

`grep -c "case('" ` on the C2 counter: **10 cases** at `17f6ef0` (pre-A6),
**12 cases** at `114ffac` (A6) and still **12** on the A13/A14 bytes
(`python3 .ufo/evidence/round-43/calibration/measure.py --selftest` →
`cases=12 failed=0`). The two A6 additions are `T1_prose_only_detected` and
`T2_column_zero_plus_prose_detected`. `grep -n multi_entry
.ufo/evidence/round-43/calibration/measure.py` finds nothing; the only
`T4_multi_entry_map_admitted` is `tools/staged-id-guard.py:350` — the guard's
case, added by **A4**, not A6's C2 counter. Same misattribution in contract
`amendments[A6].what`. So the row's named evidence triple is wrong on count and
on owner.

## F4 (medium) — row 1: the held set is real, but only after the append it precedes

`:125` "Shown able to fail: the guard reports `held={S153:S105, S154:S106,
S159:S155}`". Reproduced:

```
$ git show c5335c7:corpus/SOURCES.md > reg-114.md
$ python3 tools/staged-id-guard.py --registry reg-114.md --staged \
    /home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md --json
held {'S153': 'S105', 'S154': 'S106', 'S159': 'S155'}   # at records rev and at HEAD (A14) tool
```

But `held` is computed **over colliding ids only** (`staged-id-guard.py`
`for sid in collisions:`), so against the pre-append registry the paragraph
describes ("Registry before: 113 rows (S001–S158)", `:80`) the same command
reports six collisions and two held:

```
$ python3 guard.py --registry <114ffac:corpus/SOURCES.md> --staged …
collisions ['S153','S154','S155','S156','S157','S158']  held {'S153':'S105','S154':'S106'}
naive_map S153–S158 → S159–S164  cascade_count=6
```

which is exactly what `prerun/c3-at-freeze.stdout` recorded
(`live_collisions=6 live_held=2`). The 7-collision / 3-held / cascade-7 numbers
require `S159` already in the registry — the state the guard was supposed to
check **before**. The row's claim is therefore true of the records-rev tree but
cannot be what the pre-append check produced; the Gate paragraph (:81–88)
presents post-append arithmetic under a pre-append narration.

Adjacent new defect (Gate paragraph, current text at `6b83a11` and the working
tree): "`max(registry)+1…` lands on **the eight ids** immediately above the
registry maximum" — the naive map has exactly **seven** targets
(`S160…S166`, `len(naive_map)=7`, verified above). Off-by-one in the committed
lesson text.

And the row itself is malformed markdown: the evidence-pointer cell contains a
literal `|` inside backticks ("`S159 | Equivalent mutants (Stryker Mutator
docs)`"), so `:125` has **6 pipes** where every sibling row has 5 — a table
parser reads five cells and shifts `captured-by`/`fix` for this row.

The `captured-by` ("the census W04 warning plus `grep -n stryker-mutator.io`")
is partly unverifiable by construction: `grep` does show `corpus/SOURCES.md:98`
holding the equivalent-mutants URL, but neither committed census receipt
(`census-sources/{start,after}.stdout`) carries a W04 for `S159` or stryker —
the warning was a working-tree event withdrawn before commit, exactly as
described, and so is unrecorded.

## F5 (low) — rows verified with caveats

- **Row 3** (join-then-fullmatch): reproduced. `git show
  17f6ef0:tools/staged-id-guard.py` refuses the six-entry safe map
  `{S153:S105,S154:S106,S155:S256,S156:S257,S157:S258,S158:S259}` *and* a
  two-entry dedupe map `{S153:S105,S154:S106}` with exactly
  `map has a target that is not an S-id`, exit 1; the HEAD tool admits the same
  map (`verdict=admitted`, `map_dedupe={S153:S105,S154:S106}`). The row's
  "the selftest is now 14 cases" was true only at `5cd2154`: at `c5335c7` it
  prints 23 and at HEAD `cases=24 failed=0`.
- **Row 4**: reproduced byte-identical with A10 (`0d0f81bd`), A11 (`b56a34d7`)
  and A14 (`601c1840`) counter bytes at `--rev 3aee2c0`:
  `C1_R43_CONTROL: battery=round42_ten_fixtures fixtures_pass=10/10
  mutants_declared=6 mutants_killed=4 C1_R43_CONTROL_PASS=false`, sha-matching
  the committed receipt. The defect side ("11/11 and 5 kills") reproduced with
  the pre-A2 counter (`f0f2636` bytes) at `--rev 487b8f0`:
  `fixtures_pass=11/11 mutants_killed=5`.
- **Row 5**: the post-fix base line reproduced byte-identically by the A1
  counter at `--rev 487b8f0` (`m10=0 m12=1 m13=1`, matching
  `before/c2-at-base.stdout`). The pre-fix `m10=9` has **no committed receipt**,
  but the pre-A1 counter (`697d2f1` bytes) prints `m7=7 m8=38 m10=9` at base —
  the defect is real and reproducible; only the receipt is absent.
- **Row 6**: `tool_sha_ok=0` on both permitted revs reproduced with the pre-A5
  counter (`tool_absent=0` both times — the v4 census tool exists at base, so
  this is not the absent-tool trivial case).
- **Row 7**: `declared = 7` / `declared == 7` still at
  `calibration/measure.py:464,480`; the docstring sentence (`classes=` "is a
  constant: the evidence that a class ran is its own m-field") was added by A6,
  confirmed in the `17f6ef0`→`114ffac` diff.
- **Row 9**: `sha256sum` of the committed snapshot gives `79f6501a…` vs the S089
  anchor `bc572676…e04d` (`corpus/SOURCES.md:98`) — the drift claim and its
  shown-able-to-fail check are accurate; the A11 gate now records
  `last-modified: Sat, 24 Oct 2026 15:08:38 GMT`.

## Residual risk / gaps

- The m12 crash wave 1 reported is still reachable on the current counter:
  `m12_planned('## Round 9\n\n**Planned (round 10):**', 9)` raises
  `IndexError` at `calibration/measure.py:143` (`.splitlines()[0]` on an empty
  list). Not a Mistakes row, adjacent to row 8's repair.
- `prerun/c3-at-freeze.stdout` (at `114ffac`) records `live_collisions=6
  live_held=2` while the lesson claims 7/3 — consistent with F4; the deciding
  run should print the post-append values.
- Receipts pre-dating the records commit name a freeze `f0f2636`/`17f6ef0`
  that no longer pins the current counters; only `--freeze 6b83a11` (or the
  later wave-2 rev) pins all three current bytes. Already covered by wave-1
  RevC2Classes N3; recorded here only because the Mistakes table cites those
  old receipts.
- The staged package read is unpinned (`sha256 020fbeaa…`, mtime 2026-10-24);
  every live guard/counter number above depends on those bytes.

## Reproduction inventory (all under `/tmp/tameshi-r43-w2-RevLessonMistakes/`)

`reg-{114ffac,17f6ef0,c5335c7}.md`, `guard-{114ffac,17f6ef0,c5335c7,b510ad1}.py`,
`c1-{17f6ef0,f0f2636,3aee2c0,b510ad1}.py`, `c2-{697d2f1,f0f2636,preA6,A6}.py`,
`safemap.json`, `twomap.json`. Lane checkout untouched apart from this file; no
git/jj mutation, no writes in `/home/vgpnk/Projects/shokuknow`.

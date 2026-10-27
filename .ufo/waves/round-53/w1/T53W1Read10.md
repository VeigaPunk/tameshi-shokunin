# T53W1Read10 — cold-read of `## The re-sweep cadence and the six-case confidence statement (round 8, measured)`

Seat: reader (T53W1Read10), wave 1, round 53, lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Content commit read: `a41195dfc13a73958e4c5228ec196b28d03ded03` (C\*). Read via git objects only:

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show a41195dfc13a73958e4c5228ec196b28d03ded03:SKILL.md > SKILL.md
wc -l -c SKILL.md   ->  2178 lines, 194878 bytes
```

`git cat-file -p C*` confirms parent `e62d99711a0dd5d92b83acb96dd53ff22b31cb75` (the round-53 freeze) and the commit subject "round-53: C* content commit — fix pass, S275/S276 assimilation …".

## Section identity and split verification

The section bytes were produced by the **frozen** sectionizer the round-53 C1 counter loads
(`.ufo/evidence/round-53/c1/measure.py:170` → `R18 = '.ufo/evidence/round-18/measure.py'`,
`def sectionize(raw)` at that file's line 209: heading = `^#{1,3}(\s|$)` outside ``` fences;
heading line through the line before the next heading; trailing whitespace-only lines stripped;
joined with `\n`, no trailing newline; `surrogateescape`).

```
python3 - (importlib.load of .ufo/evidence/round-18/measure.py; sectionize(raw SKILL.md))
  -> exactly 1 section with this heading: start=1012 end=1022
     sha256=bab481fd3488f9c38656856f93b054b897d7acad5923abcb5bb0fe6b4ac63eed
```

Independent reimplementation (plain `text.split('\n')`, slice lines 1012–1022, strip trailing
blank lines, `\n`-join, sha256 over `utf-8/surrogateescape`) reproduced the same value:

```
start_line=1012 end_of_body_1based=1021
sha256=bab481fd3488f9c38656856f93b054b897d7acad5923abcb5bb0fe6b4ac63eed
bytes=676
heading_count (whole page) = 1
```

The `###` headings at lines 1023, 1071, 1094 are headings under the frozen rule, so the section
ends at line 1022 (line 1022 is blank and is stripped). Section bytes are lines 1012–1021:

```
## The re-sweep cadence and the six-case confidence statement (round 8, measured)

Round 7 left its own gap open in writing: "this ledger's update cadence is a
convention, not a mechanism" (`corpus/knowledge/fleet-kill-rate-ledger.md:235-237`,
U9). Round 8 closes it by measurement: **the cadence is a pin read executed at the
tick** — three readings per case, three triggers, one re-pin rule — and the same
tick read is the ground the six-case confidence statement below stands on. No
daemon, no timer: "standing" is the ledger + the policy + an executed command at
the round boundary; whether any fleet driver would ever invoke the command with
no lane acting stays [U].
```

`cat -A` on the range shows no CRLF, no trailing spaces; the only non-ASCII is the em dash
(`M-bM-^@M-^T`) at line 1017.

## Checks run (all against C\* bytes)

1. **Pointer `corpus/knowledge/fleet-kill-rate-ledger.md:235-237` and the U9 label.**
   ```
   git show C*:corpus/knowledge/fleet-kill-rate-ledger.md > ledger.md   (441 lines)
   grep -n "" ledger.md | sed -n '233,239p'
   235:- **U9** — this ledger's update cadence is a convention, not a mechanism: a
   236:  new sweep appends a row (or an errata block); who runs the update is the
   237:  dispatcher's call, not fixed here.
   ```
   The cited three lines are exactly the U9 item, and the quoted words are verbatim inside them
   (the page's quote stops before the colon and the remainder). The apostrophe in
   `ledger's` is ASCII `0x27` in both files. **Holds.**

2. **Attribution "Round 7 left its own gap open".**
   ```
   git log --oneline -S"this ledger's update cadence is a convention" -- corpus/knowledge/fleet-kill-rate-ledger.md
   9f1d3c3 probation round 7 (training r6): see LOG
   ```
   U9 entered in the round-7 commit. **Holds.**

3. **"the policy" exists as a nameable artifact.** `ledger.md:285` is ER-3,
   "*the re-sweep cadence: when an owner requests one, and what comes back (policy + executed pin
   read; appended 2026-10-14 by T8-3)*", and `ledger.md:314` is ER-3's "*What the cadence is not.*
   No daemon and no timer: the ledger stays the standing view + this policy + the pin read as an
   executed command at a round boundary … [U] whether a fleet driver would invoke it unaided."
   The section's sentence is a faithful restatement of ER-3's own words. **Holds.**

4. **"No daemon, no timer".** `git grep` over `C*:SKILL.md corpus tools` for cron/systemd
   timers finds no scheduled process for the cadence (the only `timer` hits are the tsukuroi
   census's `timer_drift`/`timer_fail` counters inside a measured gate, and `SKILL.md:710,759,789`
   about the census's systemd plane). ER-3 records `[O] no round created a background process`.
   **Holds.**

5. **"stays [U]" is not contradicted downstream.** The page restates the same unknown at
   `:1162-1163` (round 9) and at `:1459-1460` ("round 8's own `[U]` …, unchanged"). No later
   section claims a fleet driver has invoked the tick with no lane acting. **Holds.**

6. **"the six-case confidence statement below" and "the same tick read is the ground".**
   `### Six-case confidence statement (round 8, measured)` is at `:1094`, below the section, and
   its `revision` column reproduces exactly the pins the executed tick read compares
   (`83016d45`, `275d8294`, `084951be`, `d7edaab4`, `7e5ec98b`, `e9a21b44` — six rows, matching
   the `pin vs live blob` column of the tick table at `:1044-1052`). Six is the right count for
   "six-case". **Holds.**

7. **"three triggers".** `### Triggers T1–T3 and the re-pin rule` (`:1071`) defines exactly three
   trigger bullets (T1 stale, T2 harness sha moved, T3 owner records a re-run), and "one re-pin
   rule" matches the single "*The re-pin rule.*" bullet at `:1085`. The counts three and one
   hold. **Holds.**

8. **"three readings per case".** `grep -n "readings per case\|reading per case\|two readings\|three readings" SKILL.md`
   over the whole page at C\* returns exactly two lines — the claim itself and its contradiction:
   ```
   1017:tick** — three readings per case, three triggers, one re-pin rule — and the same
   1029:- **Per case, two readings:** the target's relation to each repo's branch-tip bytes
   ```
   **Fails** — see the finding below.

9. **Scratch directive.** The section names no scratch path at all (no `/tmp`, no
   `$HYAKU_SCRATCH`), so nothing here can violate the host scratch rule. The `/tmp` paths that do
   appear on the page are in the subsections (`/tmp/w8-tameshi-t84/pin-read.txt`, etc.), all
   well under 50 MB and dated to round 8; the subsection itself already carries the round-52 ER-4
   correction for the round-9 tick's scratch root. Not a finding of this section.

## Finding

### 1. "three readings per case" contradicts the same section's own reading map (class: self-contradicting count)

Quote (verbatim, line 1017):

```
three readings per case
```

Why it fails at C\*: the section announces that "the cadence is a pin read executed at the tick"
with **three readings per case**, but the tick subsection one screen below defines the count as
**two**, and the page defines the reading map only that way:

- `:1029` — `- **Per case, two readings:** the target's relation to each repo's branch-tip bytes`
  (`current` / `stale` / `drift`) `… and the tool's relation to the last run (`held` / `moved`)`.
- `:1033-1038` — the reading table has exactly those two reading kinds: three rule rows for the
  target relation, one row for `tool `held` / `moved``.
- `:1031` — the round-52 annotation on the same bullet already says the three *labels* are not
  exhaustive ("all three read no" in the ancestor-plus-equal-blob case), so "three" cannot be
  read as "the three labels" either.
- The executed instance at `:1044-1052` prints four comparison columns per case
  (`recorded rev`, `live HEAD`, `relation`, `pin vs live blob`) plus the tool reading — again not
  three — and ER-3, the policy the section restates, calls it "one command set per case"
  (`ledger.md:287`), not three readings.

Both wordings landed in the same round-8 commit, so nothing reconciles them:

```
git log --oneline -S"three readings per case" -- SKILL.md   -> c611d5d probation round 8 (training r7)
git log --oneline -S"Per case, two readings"  -- SKILL.md   -> c611d5d probation round 8 (training r7)
```

A reader who takes "three readings per case" as the cadence's shape will look for a third reading
that the section never defines; the operative count at C\* is two readings per case. This is a
stale/self-contradicting count in the section's own thesis sentence, not a dated historical
milestone (no date or round tag marks the "three" as superseded).

## Out-of-section observations (NOT findings — recorded only; they are not statements of this section)

- `:1459-1461` (round-11 "What stays open") cites this section's driver `[U]` as `:1017-1019`;
  at C\* that sentence occupies `:1019-1021`, so the pointer is two lines off. The stale pointer
  lives in the round-11 section, not here.
- The page's `T1–T3` (`:1071-1092`) are reading/recording-side triggers (stale / harness sha
  moved / owner re-run recorded), while ER-3's three triggers (`ledger.md:306-312`) are
  owner-side request conditions (after hardening / after suite changes / on substrate drift).
  ER-3 says the mechanism is "three triggers, stated from the owner's side"; the page's three
  differ in content. This is a taxonomy divergence between the ledger and the page, visible from
  the trigger subsection, not a false statement inside the 11-line section I was given, so it is
  recorded here and kept out of `findings`.

## Deliverable

- JSON: `.ufo/waves/round-53/w1/T53W1Read10.json` — heading, `cand` = C\*, `section_sha256` =
  `bab481fd3488f9c38656856f93b054b897d7acad5923abcb5bb0fe6b4ac63eed`, one finding whose `quote`
  occurs byte-exact in this report and in the section bytes (verified: 1 occurrence in the
  1012–1021 slice).
- Scratch: all work under `/fast/scratch/hyaku/tameshi-r53/w1/T53W1Read10/`, removed before
  yielding. No tool installs or upgrades were needed (git, python3, grep only). No git/jj
  mutations anywhere; the lane's working tree was never read for content (only `git show` of C\*).

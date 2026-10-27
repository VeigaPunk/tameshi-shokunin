# T53W2Read07 — wave-2 re-read of `## The re-sweep cadence and the six-case confidence statement (round 8, measured)`

Seat: re-reader (T53W2Read07), wave 2, round 53, lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Candidate read: **C\*\* = `5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e`**, via git objects only (the working tree was
never read for content):

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 5b703c6f...:SKILL.md > SKILL_C**.md
wc -l SKILL_C**.md        -> 2189
sha256sum SKILL_C**.md    -> 4b4a05251208beb61b0ad70ff8f26fef42dd9d3187317c4286b06c42b06b3d6d
git cat-file -p 5b703c6f  -> parent ace79e3df61266e9474e5c02086c0f7c79664580
                             subject "round-53: fix pass 2 — 40 wave-1 reader findings resolved ..."
git merge-base --is-ancestor a41195df... 5b703c6f...  -> exit 0 (C* is an ancestor of C**)
```

## 1. Fix verification (FIRST)

The named wave-1 fix for this section was **"two readings per case" (was "three")**. It is in the C\*\* bytes.

C\* (`a41195df...`), line 1017 of the section's fifth body line — the wave-1 finding text:

```
tick** — three readings per case, three triggers, one re-pin rule — and the same
```

C\*\*, line 1020 — the fixed text:

```
tick** — two readings per case, three triggers, one re-pin rule — and the same
```

Whole-section byte diff (C\* lines 1012–1021 vs C\*\* lines 1015–1024):

```
diff <(git show a41195df...:SKILL.md | sed -n '1012,1021p') <(sed -n '1015,1024p' SKILL_C**.md)
6c6
< tick** — three readings per case, three triggers, one re-pin rule — and the same
---
> tick** — two readings per case, three triggers, one re-pin rule — and the same
```

Exactly one line changed inside the section, nothing else — the section was not touched by any other
C\*\* edit. The fix also resolves the wave-1 contradiction rather than merely re-wording it: the page now
carries a single reading-count wording, and the count agrees with the reading map the section points at:

```
grep -n "readings per case\|reading per case\|three readings\|two readings" SKILL_C**.md
1020:tick** — two readings per case, three triggers, one re-pin rule — and the same
1032:- **Per case, two readings:** the target's relation to each repo's branch-tip bytes
```

No occurrence of "three readings" survives anywhere on the page at C\*\*. The tick subsection defines
exactly two reading kinds (target relation `current`/`stale`/`drift`; tool `held`/`moved`), and the
executed instance's own summary line (page line 1057) reads:

```
4 × `current` · 2 × `stale` · 0 × `drift`; tool `held`; all four sibling
```

— two readings per case. **Fix verified.**

## 2. Section identity and split (verified before hashing)

Two independent computations, both at C\*\*:

1. The **frozen** sectionizer the C1 counter loads (`.ufo/evidence/round-18/measure.py`,
   `sectionize()`; the counter loads it at `c1/measure.py` via `R18`), executed against the raw bytes:

   ```
   importlib load of .ufo/evidence/round-18/measure.py; sectionize(open('SKILL_C**.md','rb').read())
     -> dict(start=1015, end=1025, heading='## The re-sweep cadence ... (round 8, measured)',
             sha256=0a7adb86a56848dd1b9e70de885461eae85ea1da4aaf0d5cafde321cc13a0a64)
   ```

2. Independent reimplementation (fence-aware `^#{1,3}(\s|$)` scan of `split('\n')`, heading line through
   the line before the next heading, trailing whitespace-only lines stripped, `\n` join, no trailing
   newline, sha256 over `utf-8`/`surrogateescape`):

   ```
   heading line no (1-based): 1015
   next heading (1-based):    1026  ('### The tick and the pin read')
   section lines: 10
   sha256: 0a7adb86a56848dd1b9e70de885461eae85ea1da4aaf0d5cafde321cc13a0a64
   ```

Both agree. The heading occurs exactly once on the page (`grep -c` → `1`). No CRLF inside the range
(`sed -n '1015,1024p' | cat -A | grep -c '\^M'` → `0`); the only non-ASCII is U+2014, twice on line 1020.
The section names no scratch path at all (`grep -c "/tmp\|TMPDIR\|HYAKU_SCRATCH"` on the section bytes →
`0`), so no scratch-directive clause is at issue here.

Section bytes as read (lines 1015–1024):

```
## The re-sweep cadence and the six-case confidence statement (round 8, measured)

Round 7 left its own gap open in writing: "this ledger's update cadence is a
convention, not a mechanism" (`corpus/knowledge/fleet-kill-rate-ledger.md:235-237`,
U9). Round 8 closes it by measurement: **the cadence is a pin read executed at the
tick** — two readings per case, three triggers, one re-pin rule — and the same
tick read is the ground the six-case confidence statement below stands on. No
daemon, no timer: "standing" is the ledger + the policy + an executed command at
the round boundary; whether any fleet driver would ever invoke the command with
no lane acting stays [U].
```

## 3. Checks run — every remaining clause at C\*\*

All reads below are of git objects at C\*\* (`git show 5b703c6f...:<path>`) or of the extracted
`SKILL_C**.md`; line numbers are 1-based page lines at C\*\*.

| # | Clause in the section | Evidence at C\*\* | Verdict |
|---|---|---|---|
| 1 | Quote `this ledger's update cadence is a convention, not a mechanism` + anchor `corpus/knowledge/fleet-kill-rate-ledger.md:235-237` + label `U9` | ledger lines 235–237 are exactly the U9 item (`sed -n '233,239p'`, 3-line bullet starting `- **U9** — this ledger's update cadence is a convention, not a mechanism: a`); quoted words are verbatim on 235–236 | **holds** |
| 2 | `Round 7 left its own gap open in writing` (attribution) | `git log -S"this ledger's update cadence is a convention" -- corpus/knowledge/fleet-kill-rate-ledger.md` → `9f1d3c3 probation round 7 (training r6): see LOG` (sole hit) | **holds** |
| 3 | `Round 8 closes it by measurement` | `git log -S"pin read executed at the" -- SKILL.md` → `c611d5d probation round 8 (training r7)`; the ledger's `ER-3` (line 285) is headed `appended 2026-10-14 by T8-3` and carries an executed read (`Executed at this append, 2026-10-14T19:21:00Z (all six rows; ...)`) | **holds** |
| 4 | `the cadence is a pin read executed at the tick` | subsection `### The tick and the pin read` (line 1026) defines the cadence; executed instance at `tick 2026-10-14T19:15:14Z` | **holds** |
| 5 | `two readings per case` (the fix) | line 1032 `- **Per case, two readings:** ...`; two-kind reading table; executed summary line 1057 (relation tally + tool `held`) | **holds** (§1) |
| 6 | `three triggers` | subsection `### Triggers T1–T3 and the re-pin rule` (line 1075) lists exactly T1, T2, T3; `grep -n "T4\b"` over the page → no hit | **holds** |
| 7 | `one re-pin rule` | one bullet `- **The re-pin rule.**` (line 1089); `grep -n "re-pin rule\|The re-pin"` shows the subsection heading, that bullet, and later *references* to it (1237/1240/1403/1434), no second rule | **holds** |
| 8 | `the same tick read is the ground the six-case confidence statement below stands on` | `### Six-case confidence statement (round 8, measured)` sits below (line 1098) with six rows; its `revision` column (`83016d45`, `275d8294`, `084951be`, `d7edaab4`, `7e5ec98b`, `e9a21b44`) is exactly the tick table's `pin vs live blob` left-hand values (six cases, no seventh) | **holds** |
| 9 | `No daemon, no timer` | `grep -n "daemon\|timer\|cron\|systemd"` over the page: only the tsukuroi census tripwire (`timer_drift`, lines 709/713/728), the census systemd plane (762/792), this sentence (1022) and the round-9 restatement (1167) — no scheduled process carries the cadence; ER-3's own *What the cadence is not* says `No daemon and no timer` | **holds** |
| 10 | `"standing" is the ledger + the policy + an executed command at the round boundary` | ER-3 (ledger line 314): `the ledger stays the standing view + this policy + the pin read as an executed command at a round boundary`; ER-4 (318): `ER-3 landed the cadence as policy + one executed read` | **holds** |
| 11 | `whether any fleet driver would ever invoke the command with no lane acting stays [U]` | ER-3 closes `[U] whether a fleet driver would invoke it unaided`; the page restates it unchanged at lines 1167–1169 (round 9) and lines 1468–1469 (round 11, `unchanged`) | **holds** |

## 4. Findings

**None.** Every statement in the section — after the fix — holds at C\*\*. The one wave-1 finding
(`three readings per case`) is resolved in the C\*\* bytes, and the fix is semantically right, not just
present (§1).

## 5. Out-of-section observations (NOT findings — they are not statements of this section)

### 5.1 The round-9 section's line pointer into this section is now wrong at C\*\*

`## The cadence's first scheduled tick, and the service's limits (round 9, measured)`, line 1169:

```
stays [U] (`:1019`).
```

The line-number form (`:1019`) is **not** a scratch path, and it points at this section — the sentence it
cites is now at lines 1022–1024:

```
1022:daemon, no timer: "standing" is the ledger + the policy + an executed command at
1023:the round boundary; whether any fleet driver would ever invoke the command with
1024:no lane acting stays [U].
```

At C\* the pointer was approximately right: this section's heading sat at 1012, so C\* line 1019 was
`daemon, no timer: "standing" is the ledger + the policy + an executed command at` — the start of the very
sentence the pointer names. The C\*\* fix pass added **3 lines above this section** (`git diff -U0 C* C**`
hunk `@@ -24,3 +24,6 @@`, an addition near page line 24), shifting this section 1012 → 1015 and its closing
sentence 1019 → 1022; at C\*\* line 1019 is now `U9). Round 8 closes it by measurement: **the cadence is a
pin read executed at the`, and the cited content is absent there.

Two reasons to route this rather than leave it: (a) the same class of defect was fixed in C\*\* elsewhere —
round 11's pointer `(`:1017-1019`)` became `(the re-sweep cadence section's closing note)` (C\* line 1460 →
C\*\* line 1469); this one was left as a number and simultaneously drifted; (b) the pointer sits in the
round-9 section's intro block (lines 1162–1170) — `spec-w2.json` assigns only that section's later
subsection `### The re-pin semantics, as executed` (1237) to a wave-2 reader, and no seat re-reads the intro
block where this pointer is, so no other re-reader will see it. Correct form: `:1022` or the section's name.

### 5.2 `:1010-1154` at line 1261 — resolves, edges drifted (HOLD)

Line 1261 reads `it (`:1010-1154`, `fleet-kill-rate-ledger.md:285`, `fleet-kill-rate-ledger.md:318`) — the`:
the cited range still contains the cadence text it refers to (this section 1015–1024, the tick subsection,
the triggers, and the six-case statement up to 1154), so under the frozen anchor rule it holds; the range's
start edge now sits five lines before the section heading (it began at the heading at C\*).

### 5.3 ER-3's triggers vs the page's T1–T3 — unchanged taxonomy divergence (HOLD)

ER-3 (ledger 285) says `The mechanism is three triggers, stated from the owner's side`; the page's T1–T3
are reading-side (stale / harness sha moved / owner re-run recorded). The section claims only the count
(`three triggers`), which is true of both lists, so nothing here fails; the divergence wave 1 recorded
remains a ledger-vs-page taxonomy note, outside these 10 lines.

## 6. Scratch, tooling, limits

- Scratch: all work under `/fast/scratch/hyaku/tameshi-r53/w2/T53W2Read07/` (extracted `SKILL_C**.md`,
  `ledger_C**.md`, `section.txt`, `extract.py`); tree deleted before yielding.
- Tooling: none installed or upgraded (git, python3, grep only).
- Mutations: none — no git/jj writes anywhere, no fixture created (no commit was needed for this seat).
  Only `git show`, `git log`, `git diff`, `git merge-base --is-ancestor` (read-only) were used.
- Limits: the ledger's identity as "the policy" is asserted by ER-3/ER-4's own words; I did not attempt to
  prove no timer exists anywhere on the host (out of lane scope, and the claim is the design's, dated
  round 8). The `[U]` cannot be proven still-unknown beyond the page's own restatements, which are
  consistent.

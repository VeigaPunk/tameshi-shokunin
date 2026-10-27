# T53W2Read21 — re-read at C\*\*: `### What stays open — named, never closed by prose`

Lane: tameshi-shokunin · round 53 (hyaku run 10, L1 TameshiR53a2), wave 2 · seat T53W2Read21.

Substrate: `SKILL.md` at content commit **C\*\* = `5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e`** (blob `3afe0fa87a81bb082457dee04c0d42c3c7461811`), read through git objects only (`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show C**:SKILL.md`); the working tree was never read.

Section per the frozen monitor: heading line **1465**, next heading outside fences at **1481** (`## Promotion-evidence calibration — fleet round-1`); section = 1465–1480, trailing whitespace-only lines stripped → lines 1465–1479, 15 lines, **923 bytes**, `sha256 = 6600bf90bbde2f88f4df2f7908f919d5725e42735e589414509ba43c87cf7a7d`. Two independent implementations agree (fence-aware Python scanner; `awk 'NR>=1465 && NR<=1480'` + trailing-blank strip): same 923 bytes, same digest. Fence parity of the whole file is even (20 fence lines, none indented, none inside the range), so the fence-aware scan cannot mis-split here.

## Checks run

1. **Fix verification — the wave-1 → C\*\* diff hunk, read first.** `git -C …/tameshi-shokunin diff -U4 a41195dfc13a73958e4c5228ec196b28d03ded03 5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e -- SKILL.md`, hunk `@@ -1456,12 +1465,13 @@`:
   ```
   -  8's own `[U]` (`:1017-1019`), unchanged.
   +  8's own `[U]` (the re-sweep cadence section's closing note), unchanged.
   -  row for the six-leg registry** (`:1359-1363`) — open at this write.
   +  row for the six-leg (ten-leg since round 51) registry** (the named-debt bullet
   +  in `### The six-leg regression — usage and this round's receipt`) — open at this write.
   ```
   Exactly three edits, matching the wave-1 findings F1/F2/F3; the section has no `:NNNN` line anchors left (`grep -c ':[0-9]\{3,\}'` over the extracted section → 0).
2. **F1 fix (line anchor → heading-ish locator):** present in the C\*\* bytes. Round-8 `[U]` exists and resolves inside the named section — but see finding 2 (the sub-locator "closing note" points to the wrong end of the section).
3. **F2 fix (line anchor → heading anchor):** present and correct. `### The six-leg regression — usage and this round's receipt` exists at C\*\* line 1317 and is unique (`grep -c '^### The six-leg regression — usage and this round.s receipt$'` → 1); the named-debt bullet it names is inside that section (1375–1379): "a ledger row recording the six-leg (ten-leg since round 51) / registry is the ledger owner's follow-on — this page records the registry as / measured at `r10-2`, and no ledger cell is edited from here."
4. **F3 fix (dated count):** present — "six-leg (ten-leg since round 51) registry". Consistent with the page's other renderings at C\*\* (`:1372-1373` "the tool embeds ten since round 51"; `:1407` "six-leg registry at round 11, seven since round 16, eight since round 18, nine since round 26, ten since round 51").
5. **Every remaining pointer in the section resolved at C\*\*:** "above" (the interval), the round-8 `[U]`, closeout-r11's schedule `[U]`, the two successor rows, the registry row, `the ledger's U-list`, `the protocol's U1–U6`, `service-limits.md` §5.
6. **Ledger state (does the named debt still exist?):** `git show C**:corpus/knowledge/fleet-kill-rate-ledger.md` → `grep -n "ten-leg\|six-leg"` → no output (no registry row); the successor debt is still open by the ledger's own words, line 398: "its successor sweep joins the existing tsukuroi/mado successor debt."; the six-leg bullet's premise holds too — ledger line 86 still reads "**cases 1 and 2 only**".
7. **Adoption `[U]`:** `git show C**:corpus/knowledge/closeout-r11.md` lines 408–410: "**[U] the standing future itself:** the interval (the operator's, not the lanes'); whether the operator adopts the schedule/runbook; whether any fleet driver…" — recorded as a `[U]`, as the section says.
8. **"unchanged" of the round-8 `[U]`:** `git log --oneline -S'no lane acting stays' -- SKILL.md` → only `c611d5d probation round 8`; the sentence has not been edited since.
9. **`grep -n interval skill_cstar.md`** → no later section declares a clock interval (hits at 1456–1457, 1467, and unrelated uses at 1808, 1974), so the interval `[U]` is not silently closed further down the page.

## Holds (verified at C\*\*)

- `- **The interval** — the operator's `[U]` (above).` — "above" resolves at 1452–1457: "**The operator** (the seat the handoff names) … No lane declares a clock interval — the / ticks so far are boundary-bound, and the interval is that seat's `[U]`." HOLDS.
- `- **Whether the operator adopts the schedule** — `[U]`, recorded as such.` — closeout-r11.md:408–410 records it as a `[U]`, and closeout-r11.md:210–214 records "The interval is `[U]`". HOLDS.
- `**The two successor rows** (T1 fired again at this read)` — T1 is defined at 1077–1078 ("**T1 — a case reads `stale`** → re-measure at the live revision, or record the STALE cell…"), and the boundary readings at 1430–1436 show the two `stale` cells that fired it. Two stale cells, two successor rows. The debt is still open at C\*\* (ledger:398). HOLDS.
- `the ledger row for the six-leg (ten-leg since round 51) registry** (the named-debt bullet in `### The six-leg regression — usage and this round's receipt`)` — heading exists, unique, and contains the bullet; the ledger still has no such row. HOLDS. (F2/F3 both repaired; the dated form matches the page's convention.)
- `the ledger's U-list` — ledger §8 "Unknowns" at line 216, U1–U9 at 218–235. The ledger does not use the literal token "U-list", but §8 is the U-numbered unknowns list the section means, and `service-limits.md` §5 itself calls it "the ledger's U1–U9". HOLDS.
- `the protocol's U1–U6` — `corpus/knowledge/service-optin-protocol.md` §7 "Unknowns" at 257, **exactly** U1–U6 at 259–274. HOLDS.
- `service-limits.md §5` — §5 is "Unknowns" at that file's line 218, the home the section names. HOLDS as a pointer; the *content* of that home carries a stale citation — see finding 1.
- `Append-only to the last line: nothing above this section was edited by this write; the recorded tables stand at their revisions…` — the introducing commit is `284ab0f` (round 11, `git log -S'What stays open' -- SKILL.md`, sole hit). Its SKILL.md numstat is `100 1`; the single deletion is the pre-existing last line of the six-leg section gaining a terminating newline (`\ No newline at end of file` on the old side only, text identical), i.e. no content above the section was edited. HOLDS.

## Findings (2)

### 1 — the named home still carries the stale twin of the anchor this round just fixed

```
`service-limits.md` §5 — carried, not closed here.
```

`corpus/knowledge/service-limits.md` §5 U1 (file lines 220–223; blob `fc241f38e5392fbe7902c6e5fbc8b023d240ee43`, **identical** at C\* and C\*\* — no fix pass touched it):

```
- **U1 — driver invocation.** Whether any fleet driver would apply this table
  (or the tick) with no lane acting is the cadence's open [U]
  (`SKILL.md:1017-1019`); ER-4 runs the tick only as an executed command at a
  round boundary.
```

At C\*\*, `SKILL.md:1017-1019` is the round-7 gap quotation and half of the next sentence:

```
1017  Round 7 left its own gap open in writing: "this ledger's update cadence is a
1018  convention, not a mechanism" (`corpus/knowledge/fleet-kill-rate-ledger.md:235-237`,
1019  U9). Round 8 closes it by measurement: **the cadence is a pin read executed at the
```

No `[U]` token, no driver sentence. The `[U]` the citation names is at **1023–1024** ("the round boundary; whether any fleet driver would ever invoke the command with" / "no lane acting stays [U].").

Provenance (all read from git objects): the anchor was **exact when written** — `git log -S'1017-1019' -- corpus/knowledge/service-limits.md` → `b8eb96e` (round 9), and at `b8eb96e:SKILL.md` line 1019 is "no lane acting stays [U]."; it was **still exact at round 52** — `7ff81a5:SKILL.md:1019` is the same line. Round 53's own edits moved it: `a41195df` puts it at 1020–1021 (+2, wave-1 fix-pass insertions), `5b703c6` at 1023–1024 (+3 more; the C\*→C\*\* hunk `@@ -24,3 +24,6 @@` is the +3, plus the in-place repair `@@ -1017 +1020 @@` that corrected "three readings per case" → "two"). So the wave-1 repair converted the SKILL-side anchor to a heading reference and left the corpus-side twin pointing at dead lines — the identical class of defect wave 1 filed, one hop away from the section, and reachable in one step from this section's own fifth bullet.

Scope note: `corpus/` is outside this seat's write scope; the repair belongs to the L1 (heading-anchor it the same way the section's own bullet was fixed).

### 2 — "closing note" names the wrong end of the named section

```
8's own `[U]` (the re-sweep cadence section's closing note), unchanged.
```

The section anchor resolves — `## The re-sweep cadence and the six-case confidence statement (round 8, measured)` is unique at C\*\* line 1015 — and the round-8 `[U]` is inside it. But it is not at the section's close. `awk 'NR>=1015 && NR<=1160 && /\[U\]/ {print NR": "$0}'` over the C\*\* bytes returns **one** line:

```
1024: no lane acting stays [U].
```

and that line closes the section's **lead paragraph** (1017–1024: "Round 7 left its own gap open in writing … whether any fleet driver would ever invoke the command with no lane acting stays [U]."), which sits above the sub-headings `### The tick and the pin read` (1026) and `### Six-case confidence statement (round 8, measured)` (1098). The section's actual closing material contains no `[U]`:

```
1157  - **Unknown in all six:** coordinated rewrites; cross-host stability; the 50 %
1158    crossover; the two round-8 notes' own unknowns.
1159  - **Read the method, not the rate** — at six cases the constant remains the
1160    survivor taxonomy and the composition rule, not the headline percentage.
```

A reader who follows "closing note" scans the last lines of a 146-line section and finds only "the two round-8 notes' own unknowns" — a different set — not the driver `[U]`. The wave-1 F1 defect (a broken line anchor) is gone and the heading-level repair is real, but the replacement locator is wrong about *where* inside the section; "the section's lead paragraph" (or the bare section name) is accurate. The word "unchanged" in the same sentence does hold: `git log -S'no lane acting stays' -- SKILL.md` returns only the round-8 commit `c611d5d`.

## Considered and rejected (no finding)

- `Append-only to the last line: nothing above this section was edited by this write` — the round-11 commit `284ab0f` shows `100 1` for SKILL.md, but the one deletion is the "\ No newline at end of file" on the old last line of the six-leg section (text identical; only a terminating newline was added). No content above the section was edited. Not a finding.
- `— open at this write.` (twice) — scoped to the write; the debts named are still open at C\*\* anyway (ledger has no `six-leg`/`ten-leg` row; ledger:398 keeps the successor debt alive).
- `the ledger's U-list` as a naming mismatch (the ledger never uses the token "U-list") — the referent is unambiguous (§8 U1–U9) and `service-limits.md` §5 uses "the ledger's U1–U9" for the same object. Terminology drift, not a failing statement.
- `the recorded tables stand at their revisions` / `a reader on a differing revision re-resolves rather than trusts` — self-descriptive discipline, no pointer to resolve.
- Fence-parity risk in the frozen split — 20 fence lines, none indented, none in 1465–1480; both independent splitters agree. No failure.

## Limits

- Read scope: `SKILL.md` at C\*\* (`5b703c6`) and at C\* (`a41195df`), `7ff81a5`, `b8eb96e`, and the introducing commit `284ab0f`, all through `git show`/`git log`/`git diff` on git objects; `corpus/knowledge/{fleet-kill-rate-ledger,service-optin-protocol,service-limits,closeout-r11}.md` at C\*\*. No working-tree file read; no sibling lane, `.ufo/evidence/`, `.ufo/state`, watchdog log or fleet-root file touched. No git or jj mutation was run.
- Line numbers in this report are C\*\* line numbers of the file named in each sentence, unless a commit is named explicitly.
- Not probed: whether the two successor rows or the registry row *should* have landed by some later round (a ledger-owner judgement, not a statement of this section); whether "closing note" was intended to mean "the closing sentence of the lead note" (the wording is ambiguous, but the natural reading — a note at the section's close — is false).
- Scratch: `/fast/scratch/hyaku/tameshi-r53/w2/T53W2Read21/` (working copies `skill_cstar.md`, `section.txt`, `sec_awk.bin`, `split.py`, the four corpus files). Deleted before yield — no residue on disk.
- Tools installed/upgraded for this seat: **none** (python3, awk, git, sha256sum already present; pacman not used, per the host guard).

# ResidualIds — item-10 id lists vs the assimilation evidence

Scope: the round report's `## Sources & frontier` id-list block
(`/home/vgpnk/Projects/shokunin/.ufo/reports/round-41/tameshi.md`, from `**Id lists (item 10), pasted
in full.**` to `next free id \`S155\``; sha256 `64bf71b4f0a515afbffef81b767ea0ed2b0b4381013f6ee2dfae20fb49004485`,
mtime 2026-10-25 04:03:23 — the file gained a line above the block while this seat ran; the block text
is unchanged between the 03:5x read and this one, so all verdicts below are content-anchored) against
`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-41/assimilation/{reg-ids,staged-ids,collisions}`.
Revisions named per command: base `a3d6c690bcbf8914551d4f4e8e1612784c1c2046`, freeze
`d4ee4e63a0a4402bd8628fbc80f06bbd8f37d937`, measured `2ae00eb750b86eba6c9b54b36b1a6e875e9fd8a6`,
tip `812ee0d11d267e131be3dc8db0b71253cbae9234`. Read-only; nothing in the lane, the report, the
fleet repo or the package was written. No installs. Neither counter was run: no verdict below
depends on a counter reading, and the deciding facts are file equality, `comm`, and the registry/extractor
at the three named revisions.

## Verdicts

| # | Item | Verdict |
|---|---|---|
| 1 | `reg-ids` count in the report (107, "base/freeze") vs the cited file (109 lines) | **DEFECT** |
| 2 | `reg-ids` membership in the report vs the cited file | **DEFECT** |
| 3 | `staged-ids` count (103) | PASS |
| 4 | `staged-ids` membership (contiguous `S153`–`S255`) | PASS |
| 5 | Collision count (`0` base / `2` landed) and the `collisions` file | PASS |
| 6 | Stated gaps (`S038 S039 S098`, `S109`–`S131`, `S133`–`S151`) | PASS |
| 7 | Stated statuses (`79 mined / 22 queued / 6 rejected`) | PASS |
| 8 | Renumber map "empty" | PASS |
| 9 | "Id lists (item 10), pasted in full" (form of the paste) | **DEFECT** |
| 10 | "next free id `S155`" | **DEFECT** (minor) |
| 11 | Cited files "(109 / 103 / 2 lines)" and their presence at the measured commit | PASS |

## Evidence

### 1–2. `reg-ids` — pasted 107, file 109 (DEFECT)

The file is the landed registry, byte-identical to the item-10 extractor at the measured commit:

```
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
git show 2ae00eb750b86eba6c9b54b36b1a6e875e9fd8a6:corpus/SOURCES.md \
  | grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' | grep -oE 'S[0-9]+' | sort > /tmp/meas-reg.txt
diff /tmp/meas-reg.txt .ufo/waves/round-41/assimilation/reg-ids && echo IDENTICAL
```
→ `IDENTICAL`; `wc -l` → `109`. Last two entries are `S153`, `S154`.

The report's pasted list is the 107-id freeze set (its `Registry ids at the base/freeze (107)` bullet:
`S001 S002 … S037 S040 … S097 S099 … S108 S132 S152`). That freeze list is itself correct —
the same extractor at base and freeze gives the same 107 ids:

```
git show a3d6c690bcbf8914551d4f4e8e1612784c1c2046:corpus/SOURCES.md \
  | grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' | grep -oE 'S[0-9]+' | sort > /tmp/base-reg.txt   # 107
git show d4ee4e63a0a4402bd8628fbc80f06bbd8f37d937:corpus/SOURCES.md \
  | grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' | grep -oE 'S[0-9]+' | sort > /tmp/freeze-reg.txt # 107
diff /tmp/base-reg.txt /tmp/freeze-reg.txt && echo SAME   # → SAME
```
Range arithmetic in the report is also right for that list: `37+58+10+1+1 = 107`.

The defect is the paste/citation pair. The block's own `Files:` sentence cites `reg-ids` as a
109-line file, the header calls the section "pasted in full", and yet the pasted set is that file
minus exactly the two ids the collision count rests on:

```
comm -23 /tmp/meas-reg.txt /tmp/base-reg.txt    # ids only in the landed registry
# S153
# S154
comm -13 /tmp/meas-reg.txt /tmp/base-reg.txt    # ids only in the base list → empty
```
So the pasted list, read against the landed artifact, reports `0` collisions, while the report's own
collision bullet reports `2`. The item-10 acceptance test this round's own seat drafted
(`.ufo/waves/round-41/w1/ReviewIdLists.md` §4: "the pasted tokens must equal the evidence files")
cannot pass here: the registry bullet carries 9 literal ids and its range expansion carries 107
(set difference to the file: `S153`, `S154`, above), while the cited file holds 109. Both the 109
list and the 107 list are defensible to paste — but only one of them is the file the sentence cites.

### 3–4. `staged-ids` — 103, contiguous, no duplicates (PASS)

```
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-41/assimilation
wc -l reg-ids staged-ids collisions
# 109 reg-ids
# 103 staged-ids
#   2 collisions
cd /home/vgpnk/Projects/shokunin && grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' \
  /home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md \
  | grep -oE 'S[0-9]+' | sort > /tmp/staged-src.txt
diff /tmp/staged-src.txt /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-41/assimilation/staged-ids \
  && echo STAGED_IDENTICAL
# STAGED_IDENTICAL
```
Contiguity and uniqueness, run in the assimilation directory:

```
awk 'NR>1 && $0 != prev+1 {print "gap at "NR": "prev" -> "$0} {prev=$0}' <(sed 's/S//' staged-ids)
# (no output)
sort staged-ids | uniq -d
# (no output)
```
`255-153+1 = 103`. Report text "Staged ids (103): `S153 S154 S155 … S254 S255` — contiguous
`S153–S255`" matches the file and the package.

### 5. Collision count (PASS)

```
od -c .ufo/waves/round-41/assimilation/collisions
# 0000000   S   1   5   3  \n   S   1   5   4  \n
comm -12 /tmp/meas-reg.txt  .ufo/waves/round-41/assimilation/staged-ids | wc -l   # 2
comm -12 /tmp/base-reg.txt  .ufo/waves/round-41/assimilation/staged-ids | wc -l   # 0
comm -12 /tmp/freeze-reg.txt .ufo/waves/round-41/assimilation/staged-ids | wc -l  # 0
```
`2` landed (`S153`, `S154`), `0` at base and at freeze — the report's two numbers. The file holds
exactly those two ids, 2 lines, no trailing junk. `comm -12` on the *pasted* 107 list would give `0`,
which is the item-1/2 defect, not a defect in this count.

### 6. Gaps (PASS)

Complement of the 107-id base list inside `S001`–`S152`:

```
python3 - <<'PY'
have={int(l[1:]) for l in open('/tmp/base-reg.txt') if l.strip()}
miss=[n for n in range(1,153) if n not in have]
out=[];s=p=None
for n in miss:
    if s is None: s=p=n
    elif n==p+1: p=n
    else: out.append('S%03d'%s if s==p else 'S%03d-S%03d'%(s,p)); s=p=n
out.append('S%03d'%s if s==p else 'S%03d-S%03d'%(s,p))
print(len(miss), '|', ', '.join(out))
PY
# 45 | S038-S039, S098, S109-S131, S133-S151
```
Same 45 ids as the report's `S038 S039`, `S098`, `S109–S131`, `S133–S151` (the report spells the
adjacent pair out; the set is identical, `152 - 107 = 45`). Nothing is claimed about ids above
`S152`, which the staged set occupies.

### 7. Statuses (PASS)

```
git show a3d6c690bcbf8914551d4f4e8e1612784c1c2046:corpus/SOURCES.md | grep -E '^\| *S[0-9]{3}' \
  | awk -F'|' '{gsub(/^ +| +$/,"",$9); print $9}' | sort | uniq -c
#  79 mined
#  22 queued
#   6 rejected
```
Same result at freeze `d4ee4e63`. `79+22+6 = 107`. The report attaches these to the base/freeze list,
where they are true; the landed tally is `81 mined / 22 queued / 6 rejected` (same command at
`2ae00eb7`), which the report does not state (see residual risk 2).

### 8. Renumber map empty (PASS)

```
ls -la .ufo/waves/round-41/assimilation/          # only collisions, reg-ids, staged-ids
find .ufo/waves/round-41 -maxdepth 2 -iname "*renumber*" -o -maxdepth 2 -iname "*merge*" -o -maxdepth 2 -iname "*map*"
# (no output)
git show 2ae00eb750b86eba6c9b54b36b1a6e875e9fd8a6:corpus/SOURCES.md | grep -E '^\| *S15[34] ' | cut -c1-78
# | S153 | ast — Abstract syntax trees (Python 3.15.1 documentation) — https
# | S154 | pathlib — Object-oriented filesystem paths (Python 3.15.1 documenta
grep -E '^\| *S15[34] ' /home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md | cut -c1-78
# | S153 | POSIX `diff` utility specification (The Open Group Base Specification
# | S154 | Package golden provides a function for comparing arbitrary text data
```
No map artifact exists and none is needed: the registry's only additions this round are `S153`/`S154`,
the lane's own CPython rows, while the staged `S153`/`S154` are different rows (POSIX `diff`,
`google/golden`). Set difference base→measured, replayed from the two sorted extracts:

```
comm -23 /tmp/meas-reg.txt /tmp/base-reg.txt    # added at the measured commit
# S153
# S154
comm -13 /tmp/meas-reg.txt /tmp/base-reg.txt    # removed
# (no output)
```
No staged row was adopted, so "renumber map: empty" is the true state, not a missing one.

### 9. Paste form (DEFECT)

The section header says "pasted in full", but both lists are compressed with `…` and range notation.
Literal S-token counts, taken content-anchored (not by line number, because the report was edited
above the block during this seat):

```
cd /home/vgpnk/Projects/shokunin && python3 - <<'PY'
import re
t=open('/home/vgpnk/Projects/shokunin/.ufo/reports/round-41/tameshi.md').read()
sec=t[t.index('Id lists (item 10)'):t.index('next free id')]
for label,pat in (('reg', r'Registry ids at the base/freeze.*?(?=\n  - Staged)'),
                  ('staged', r'Staged ids \(103\)[^\n]*')):
    toks=re.findall(r'\bS\d{3}\b', re.search(pat, sec, re.S).group(0))
    print(label, 'tokens', len(toks), 'distinct', len(set(toks)))
PY
# reg tokens 24 distinct 16
# staged tokens 7 distinct 5
```
24 distinct 16 = the 9 list ids (`S001 S002 S037 S040 S097 S099 S108 S132 S152`) plus the 7 gap
endpoints (`S038 S039 S098 S109 S131 S133 S151`). Neither bullet enumerates its list.
The range notation does determine membership unambiguously, but item 10's wording is "Paste both id
lists" and the round's own acceptance test compares pasted tokens to the files — by that test the
paste fails for both lists (`staged-ids` fails only on form, since its range is exact and complete).
The cheapest repair is the 109-id and 103-id token blocks already drafted in
`.ufo/waves/round-41/w1/ReviewIdLists.md` §"Exact text to add".

### 10. "next free id `S155`" (DEFECT, minor)

`S155` is free in the registry but not in the section's own two lists:

```
grep -x 'S155' .ufo/waves/round-41/assimilation/staged-ids     # S155
grep -x 'S155' .ufo/waves/round-41/assimilation/reg-ids        # (no output)
```
The registry also leaves `S038`, `S039`, `S098`, `S109`–`S131`, `S133`–`S151` unallocated (item 6),
so the first unallocated registry id is not `S155` either; and the next id absent from both lists is
`S256` (`S255` is the staged maximum). "Free" is only true for the lane's ledger convention
"next unused id" = highest registry id + 1 (`corpus/SOURCES.md:440` says `Next unused id: S155`). As
written in the report, the phrase sits directly after the "document-anchored, never arithmetic"
warning it contradicts: renumbering a staged row onto `S155` collides with staged `S155`. Wording fix
only, no evidence impact: "next registry id above `S154` is `S155`".

### 11. Cited files present at the measured commit (PASS)

```
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
git ls-tree --name-only 2ae00eb750b86eba6c9b54b36b1a6e875e9fd8a6 -- .ufo/waves/round-41/assimilation/
# .ufo/waves/round-41/assimilation/collisions
# .ufo/waves/round-41/assimilation/reg-ids
# .ufo/waves/round-41/assimilation/staged-ids
git diff --quiet 2ae00eb750b86eba6c9b54b36b1a6e875e9fd8a6 -- .ufo/waves/round-41/assimilation/ && echo SAME
# SAME
wc -l .ufo/waves/round-41/assimilation/{reg-ids,staged-ids,collisions}
# 109 reg-ids / 103 staged-ids / 2 collisions
```
Tracked at the measured revision and byte-identical to the working tree, so the "(109 / 103 / 2
lines)" figures are re-derivable and no stale-file citation exists here.

## Residual risk

1. **The collision is duplicate content, not just duplicate ids.** Staged `S153`/`S154` (POSIX
   `diff`, `google/golden`) have the same titles as registry rows `S105`/`S106`, and both of those
   existed at base. A next assimilation round that follows the report's "renumber in scratch" framing
   would append rows the lane already holds under new ids; the document-anchored resolution for these
   two is refusal/merge against `S105`/`S106`, not renumbering.

   ```
   cd /home/vgpnk/Projects/shokunin && python3 - <<'PY'
   import subprocess,re
   def rows(text):
       out={}
       for l in text.splitlines():
           m=re.match(r'^ {0,3}\|\s*(S\d{3,})\s*\|([^|]*)\|',l)
           if m: out[m.group(1)]=m.group(2).strip()
       return out
   meas=rows(subprocess.run(['git','-C','tameshi-shokunin','show','2ae00eb750b86eba6c9b54b36b1a6e875e9fd8a6:corpus/SOURCES.md'],capture_output=True,text=True).stdout)
   base=rows(subprocess.run(['git','-C','tameshi-shokunin','show','a3d6c690bcbf8914551d4f4e8e1612784c1c2046:corpus/SOURCES.md'],capture_output=True,text=True).stdout)
   staged=rows(open('/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md').read())
   for sid,t in staged.items():
       hit=[k for k,v in meas.items() if v==t]
       if hit: print(sid,'->',hit,'in base:',[k for k,v in base.items() if v==t])
   PY
   # S153 -> ['S105'] in base: ['S105']
   # S154 -> ['S106'] in base: ['S106']
   ```
   The report's "nothing needed renumbering" is unaffected; its forward-looking hazard sentence is
   the part a next round could misread.
2. **Landed status tally unstated.** The only statuses in the section belong to the 107-id freeze list
   (`79/22/6`); the landed 109 row set is `81/22/6`. A reader checking the cited 109-line file against
   the pasted statuses gets a one-row-per-status mismatch of 2 mined rows, which is exactly the
   paste/citation defect in items 1–2 and worth fixing together.
3. **`S153`–`S154` are the only ids whose absence a reader cannot notice.** The ellipsis in the
   pasted list hides them; the range form `S001–S037, S040–S097, S099–S108, S132, S152` does not
   announce that `S153`/`S154` exist. If the freeze list is what the report means to paste, it should
   say "freeze registry (107 ids, before this round's two rows)" and paste the landed 109 list as the
   collision-bearing one.

## Verification gaps

- I did not run `calibration/measure.py` or `census/measure.py`; none of the eleven verdicts above
  turns on a counter value, and the two counters' m7/m8 path handling was not exercised. Item-10's
  own extractor was replayed instead, at three revisions (base, freeze, measured) with the 0–3-space
  pattern, and the evidence files compared to it byte-for-byte.
- I did not verify whether the package's other 101 staged ids duplicate pre-existing registry rows
  (only the two colliding ids were title-matched); if the duplication pattern is general, the
  "no adoption" boundary gets wider than this section states, and that belongs to the assimilation
  and append-only seats.
- The freeze revision `d4ee4e63` was taken from the lane's own seat report; base `a3d6c690` yields an
  identical 107-id set, so the verdict does not depend on which of the two is canonical.

# RevQuarantine — round 43 wave 2: the lesson's quarantine counts vs the register

Seat: `L1Tameshi43.RevQuarantine` (read-only). Access date 2026-10-25.
Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. The only lane write is this file.

**Target** — `corpus/lessons/round-43.md:102-104`:

```
- Quarantine slice: 17 data rows (14 `payload-absent`, 3 could-not-be-fetched),
  re-derived read-only and byte-identical to the round-42 slice; verdicts stay
  in the round-40 lesson and nothing was adopted (wave-1 ScoutQuarantine).
```

**Register** — `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`
(81,621 B; sha256 `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`;
md5 `2906d068541b328ed8999b76be2a6c96`; mtime `2026-10-24 08:37:00 -0300`;
`git -C /home/vgpnk/Projects/shokuknow status --porcelain` clean for this path —
the register predates and has not moved under the round-42/43 artifacts).

## 1. Verdict in one line

**The three numbers are correct**: 17 register data rows for `tameshi` = 14
`payload-absent` + 3 whose register note is "the cited source could not be
fetched". **No id is mis-stated by name or number.** One id's *status* is
mis-stated by the trailing clause "nothing was adopted" — **S132**, adopted in
round 40 and live in `corpus/SOURCES.md`. The sentence also inherits two
register-side defects it cannot see: the three unfetchable ids are emitted with
a stray trailing backtick (`S113\``), and the register's own `## By lane`
summary says `14`, not 17.

## 2. The exact command and its exact output

Run verbatim (the item's awk; `-F'|'`, fields printed as `$4, $5`):

```
awk -F'|' -v l='tameshi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' \
  /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
```

17 lines, in register order, byte-for-byte (note the trailing backticks — they
are in the register, see F1):

```
 S105   `payload-absent`
 S109   `payload-absent`
 S110   `payload-absent`
 S118   `payload-absent`
 S119   `payload-absent`
 S124   `payload-absent`
 S126   `payload-absent`
 S129   `payload-absent`
 S131   `payload-absent`
 S132   `payload-absent`
 S137   `payload-absent`
 S140   `payload-absent`
 S141   `payload-absent`
 S143   `payload-absent`
 S113`   the cited source could not be fetched, so no quote was checked
 S123`   the cited source could not be fetched, so no quote was checked
 S134`   the cited source could not be fetched, so no quote was checked
```

Real counts, derived from that output:

| measure | count |
|---|---|
| data rows | **17** |
| `payload-absent` rows | **14** |
| could-not-be-fetched rows | **3** |
| distinct ids | **17** (no id appears twice; `uniq -c` all 1) |
| tameshi rows anywhere else in the register (lane column) | 1 — the `## By lane` summary row at `:240`, correctly rejected by the `round` conjunct |

So the sentence's parenthetical is not a rounding of something bigger: it is
exact. Per-round split (register column): round1 5 (S105 S109 S110 S118 S113),
round2 4 (S119 S124 S126 S123), round3 3 (S129 S131 S132), round4 2 (S137 S134),
round5 3 (S140 S141 S143).

## 3. Per-id register coordinates

| id | register line | round | what the register says | how the sentence treats it |
|---|---|---|---|---|
| S105 | `:215` | round1 | `payload-absent` | one of the 14 ✔ |
| S109 | `:216` | round1 | `payload-absent` | one of the 14 ✔ |
| S110 | `:217` | round1 | `payload-absent` | one of the 14 ✔ |
| S118 | `:218` | round1 | `payload-absent` | one of the 14 ✔ |
| S119 | `:219` | round2 | `payload-absent` | one of the 14 ✔ |
| S124 | `:220` | round2 | `payload-absent` | one of the 14 ✔ |
| S126 | `:221` | round2 | `payload-absent` | one of the 14 ✔ |
| S129 | `:222` | round3 | `payload-absent` | one of the 14 ✔ |
| S131 | `:223` | round3 | `payload-absent` | one of the 14 ✔ |
| S132 | `:224` | round3 | `payload-absent` | one of the 14 (count ✔) — **status mis-stated by "nothing was adopted"**, see F2 |
| S137 | `:225` | round4 | `payload-absent` | one of the 14 ✔ |
| S140 | `:226` | round5 | `payload-absent` | one of the 14 ✔ |
| S141 | `:227` | round5 | `payload-absent` | one of the 14 ✔ |
| S143 | `:228` | round5 | `payload-absent` | one of the 14 ✔ |
| S113 | `:363` | round1 | why: "the cited source could not be fetched, so no quote was checked" | one of the 3 ✔ (id emitted as `S113\``, F1) |
| S123 | `:364` | round2 | same why | one of the 3 ✔ (id emitted as `S123\``, F1) |
| S134 | `:365` | round4 | same why | one of the 3 ✔ (id emitted as `S134\``, F1) |

## 4. Four independent derivations agree — the counts are not luck

1. **The census the register names.** `quote-lint-full-v5.json` (tameshi findings:
   55 `folded`, 16 `ABSENT`, 5 `sweep-found`, 3 `fetch-failed`, 1 `no-quote-span`):
   distinct ABSENT ids = the 14 above; distinct fetch-failed ids = S113 S123 S134.
   16 ABSENT *findings* fold onto 14 *rows* (S132 and S141 carry two each), which
   is why "14 payload-absent" is a row count and not a quote count.
2. **Regenerating the register.** `absent-defect-register.py --census
   quote-lint-full-v5.json --out /tmp/…` reports `rows=194 quotes=324` and its
   output is **byte-identical to the shipped register** (`diff` empty). The v4
   census differs (325 ABSENT quotes; S126 carries an extra quote span), so v5 is
   indeed the file the shipped register came from.
3. **The verdict set the sentence points at.** `corpus/lessons/round-40.md:55-71`
   lists 17 ids; sorted set difference against the register's 17 is empty.
4. **The frozen slice.** `.ufo/waves/round-42/assimilation/quarantine-slice`
   (583 B, md5 `9f897205525c58ddd64c876ef45baf1f`) is **byte-identical** to a fresh
   run of the awk above (`diff` clean). The sentence's "byte-identical to the
   round-42 slice" is true, and the register has not drifted between rounds.

## 5. Findings

### F1 — medium — the register emits three malformed ids, and the slice carries them

`absent-defect-register.py:160` writes the never-checked id as `{r['id']}` +
a closing backtick and no opening one:

```python
out.append(f"| `{r['lane']}` | {r['round']} | {r['id']}` | {r['note']} | "
```

So `absent-defect-register.md:363-365` read ``S113` ``, ``S123` ``, ``S134` `` —
and because the awk prints `$4` raw, the id token the lesson's own recipe
produces (and the frozen slice stores) is `S113\``, not `S113`.

Reproduce:

```
sed -n '363,365p' REG | cut -c1-90 | cat -A
# | `tameshi` | round1 | S113` | the cited source could not be fetched, ...
awk -F'|' … '{print $4}' REG | tail -3 | cat -A
#  S113` $   S123` $   S134` $
```

Consequence: any consumer that splits the slice on whitespace (`cut -d' ' -f1`,
`read id class < line`) or tests exact equality gets `S113\``; only a substring
test still hits. The sentence lists no ids, so **it mis-states no id by name** —
but its claim to deliver a usable re-derivation silently inherits this. Fix is
one character at `absent-defect-register.py:160` (drop the backtick, or emit
`` `{r['id']}` `` symmetrically); the register is assimilation-owned and was not
touched.

### F2 — medium — "nothing was adopted" mis-states S132

The clause sits immediately after "verdicts stay in the round-40 lesson", and the
verdict set it points at contains exactly one adoption: **S132** —
`corpus/lessons/round-40.md:66` (`present … **Adopted**`), recorded at
`round-40.md:22`, and the row is live in the registry at `corpus/SOURCES.md:121`
(README row D29 anchor). The wave-1 scout's "Nothing was adopted" is round-43
scoped; the lesson dropped the scope word, so as written a reader who checks the
sentence against the referenced verdicts finds 1 adopted row inside the 17-row
"quarantine". This is the only id whose status the sentence gets wrong, and it is
a scope word away from correct.

Fix: "… and nothing was adopted **this round**" — or, stronger, "one row (S132)
was adopted in round 40; nothing was adopted this round".

### F3 — low — "3 could-not-be-fetched" is prose lifted from a note, not a class

The register's class vocabulary is `payload-absent` / `unreachable`
(`absent-defect-register.md:11-14`). The never-checked table has **no class
column** (`:265`: `lane | round | id | why it was not checked | cited source`),
so the sentence's second token is the note text ("the cited source could not be
fetched") promoted to a class. Read as a property it is also stale for all three
ids: round 40 found each of S113/S123/S134 **present** ("the prose class is
stale" — `round-40.md:58,61,67`). The sentence's own scope line ("verdicts stay
in the round-40 lesson") prevents this from being a verdict error, but the
parenthetical should say "3 whose register note says the source could not be
fetched". No id is wrong by number.

### F4 — low — the register's own summary cannot reproduce "17"

`## By lane` reports `| `tameshi` | 14 |` (`absent-defect-register.md:240`),
because `by_lane` counts only the 194-row ABSENT section
(`absent-defect-register.py:80`); the 3 never-checked rows are counted only in
their own table (`rows: **109**` corpus-wide). The lesson's **17 is the correct
register-wide total**, but a reader cross-checking the sentence against the
register's summary lands on 14 and cannot see why the sentence adds 3. This is a
register wording/scoping issue (the by-lane header does not say "ABSENT rows
only"), not a lesson arithmetic error; the lesson is the more accurate document
here.

## 6. Residual risk and what was not checked

- **Verdict correctness for the 17 rows was not re-audited** (out of scope): the
  verdicts stay at `corpus/lessons/round-40.md:55-71`. F3's "stale" status is
  taken from that lesson, not re-fetched here.
- The register is treated as evidence, not authority: its summary tables are
  demonstrably narrower than its own row set (F4) and its never-checked ids are
  malformed (F1); the row-level parse is what was counted.
- Nothing in `/home/vgpnk/Projects/shokuknow`, the lane checkout, jj state or the
  Git index was written. Scratch files `/tmp/tameshi-r43-w2-RevQuarantine-*`
  were deleted; no tool install or upgrade was needed (nothing to record).

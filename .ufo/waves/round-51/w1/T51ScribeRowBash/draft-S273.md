# Draft — SOURCES row S273 (C2 source row), round 51

Seat T51ScribeRowBash. Everything below is a **draft**: this seat is read-only on the lane and
appended nothing to `corpus/SOURCES.md`, `corpus/lessons/round-51.md` or `corpus/knowledge/`.
The row was validated in a scratch `--shared` clone, and the frozen C2 `sourced_entry` rule was
run against that clone's commit (simulation, not a verdict).

Snapshot and receipts beside this file: `chet-bashref.html` (1,040,870 B), `fetch-receipt.txt`,
`bashref-texi-excerpt.txt`, `probe/` (five option-set probes + the case replica + `observed.txt`),
`mutant-receipt.txt`, `base.out`, `draft.out`, `final.out`.

## 1. The row (11 columns, ready to insert directly after S271 at `corpus/SOURCES.md:146`)

| S273 | GNU Bash Reference Manual, The Set Builtin (author copy of the manual, Edition 5.3, last updated 18 May 2025) — https://tiswww.case.edu/php/chet/bash/bashref.html (the gnu.org node page https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html was unreachable on 2026-10-27 UTC: eight attempts, HTTP 000, 0 bytes, connect timeouts — https and http, with and without www, IPv4-forced, and the single-page manual alike) | docs | A | Bash `errexit` (`-e`) and `pipefail`: which failing commands end a non-interactive shell, the listed non-exits, and a pipeline's return value | §The Set Builtin `-e` item (single-page copy lines 6547-6570) and `pipefail` item (lines 6706-6710); same text in the Savannah texi pinned by S097 at `@item -e` lines 5929-5948 and `@item pipefail` lines 6062-6066 (re-fetched 2026-10-27, sha256 f3d37d57, byte-identical to S097); a command of assignments only takes its status at §Simple Commands lines 3675-3677 (copy lines 4172-4173) @ author copy fetched 2026-10-27T00:22Z UTC, two fetches byte-identical (1040870 bytes; SHA-256 b91026acffb159bd1e842e3116a95539bf858e2b57cbfa74df9e3a53379177a4), snapshot .ufo/waves/round-51/w1/T51ScribeRowBash/chet-bashref.html | Quotes (each at most 25 words), `-e`: "Exit immediately if a pipeline ... returns a non-zero status"; non-exits: "The shell does not exit if the command that fails is ... any command in a pipeline but the last"; the parenthetical tying that to pipefail: "any command in a pipeline but the last (subject to the state of the pipefail shell option)"; `pipefail`: "the return value of a pipeline is the value of the last (rightmost) command to exit with a non-zero status"; assignments-only status: "the exit status of the last command substitution performed" | mined | 2026-10-26 | 365d | corpus/knowledge/mutation-case-kagi-drift-pins.md |

Field notes: `kind=docs`, `tier=A` (Bash maintainer's own copy), `status=mined`,
`opened=2026-10-26` (the lane's local round date, UTC-03; every fetch receipt is
`2026-10-27T00:2xZ` — the UTC day boundary falls inside this round, disclosed not smoothed),
`recheck=365d`, `used-by` names only the C2 entry (the counter splits the cell on `,`/`;` and
requires the exact path). No cell contains `|`. `awk -F'|'` on the line: `NF=13`, 11 cells.

## 2. `corpus/SOURCES.md` round note (append after the `- Next unused id: S272` line, `:498`)

```text
Round 51: one row added, S273 (GNU Bash Reference Manual, §The Set Builtin, author copy at
tiswww.case.edu — the gnu.org node page timed out on 2026-10-27 UTC, eight attempts, so the row
names the copy that opened), tier A / docs / mined, opened 2026-10-26, recheck 365d, pinned to the
snapshot under `.ufo/waves/round-51/w1/T51ScribeRowBash/` (two fetches byte-identical, sha256
b91026ac). It is the manual ground for C2's tenth leg: `errexit` ends a non-interactive shell on a
failed pipeline, `pipefail` makes a pipeline return its last non-zero command's status, and an
assignments-only command takes the last command substitution's status — so
`actual=$(grep -nE -m1 ... | cut -d: -f1)` with a zero-match pin is itself the failing command
(exit 1, no GONE line, no DRIFT_PINS summary). S097 and S104 hold the same manual at the Savannah
texi pin; S273 is a different URL and a new section scope (§The Set Builtin), so no W04 fires.
Cited by `corpus/knowledge/mutation-case-kagi-drift-pins.md`. Rows 131 → 132.
- Next unused id: S274 (staged ids S161-S255 stay reserved by document for the package).
```

## 3. Lesson `## Gate` paragraph (`corpus/lessons/round-51.md`, lane style)

```markdown
## Gate

- **S273 admit** — GNU Bash Reference Manual, §The Set Builtin, author copy (Chet Ramey,
  `https://tiswww.case.edu/php/chet/bash/bashref.html`, Edition 5.3, last updated 18 May 2025),
  opened 2026-10-26 (`2026-10-27T00:22Z` UTC), HTTP 200, 1,040,870 B, sha256
  `b91026acffb159bd1e842e3116a95539bf858e2b57cbfa74df9e3a53379177a4`; two fetches the same
  minute were byte-identical, snapshot `.ufo/waves/round-51/w1/T51ScribeRowBash/chet-bashref.html`.
  The pinned URL is **not** the one the seat was sent to fetch: `https://www.gnu.org/software/
  bash/manual/html_node/The-Set-Builtin.html` never answered on this host (eight attempts —
  https, http, with and without `www`, IPv4-forced, and the single-page manual: HTTP 000, 0 bytes,
  connect timeouts, curl exit 28), the same class r32, r34 and r35 recorded. The row names the
  carrier that opened; the gnu.org failure is inside the source cell, not hidden.
  Located quotes (each at most 25 words; anchors in the single-page copy, and the same text in
  the Savannah texi pinned by S097 at `@item -e` 5929–5948 / `@item pipefail` 6062–6066):
  `-e` — "Exit immediately if a pipeline ... returns a non-zero status" (9 words); the non-exits —
  "The shell does not exit if the command that fails is ... any command in a pipeline but the
  last" (19), and the parenthetical that binds that to pipefail — "any command in a pipeline but
  the last (subject to the state of the pipefail shell option)" (17); `pipefail` — "the return
  value of a pipeline is the value of the last (rightmost) command to exit with a non-zero
  status" (20); assignments-only status (§Simple Commands, 3675–3677) — "the exit status of the
  last command substitution performed" (9 words of the sentence).
  Teaches: `set -euo pipefail` makes `actual=$(grep ... | cut ...)` itself the failing command on
  a zero-match pin — grep 1, `cut` 0, pipefail returns 1, the assignment takes the substitution's
  status, `-e` ends the shell with **1** (measured: `probe/observed.txt`, exit 1, no output).
  Limit: the manual states the three rules separately and never composes them for a reader, and
  it does not cover `inherit_errexit` (off by default, irrelevant here since the pipeline is the
  substitution's only command); the gate's own call context is what makes `-e` apply at all
  (`verify)` is a plain simple command in the `case` arm, `drift-pins.sh:449`) — a function called
  as `verify || rc=$?` would swallow the failure (probe `p5_cond.sh`, measured).
  S273 is a different URL from S097/S104 and a new section scope, so no W04 and no E04; the
  document is the same manual they pin at the Savannah commit, which is why the row records the
  texi line ranges as corroboration instead of opening a second claim about the text.
```

## 4. Handoff — the `source:` line the C2 entry must carry

`.ufo/evidence/round-51/c2/measure.py:206` takes `head[:8]` of the added entry and requires a
line that **starts at column 0** with `source:`, contains the target tail `corpus/drift-pins.sh`,
and names an S-id whose row is `mined`, `opened 2026-10-26`, with that entry in `used-by`
(`measure.py:211`). Line 1 of `corpus/knowledge/mutation-case-kagi-drift-pins.md`:

```text
source: kagi corpus/drift-pins.sh @ e64e81b8 (S273, S097) — the drift gate this case measures
```

The entry must be *added* after BASE (`--diff-filter=A`, `measure.py:191`) and its name
(`corpus/knowledge/mutation-case-kagi-drift-pins.md`) must appear in `corpus/README.md` beyond
the base bytes (`measure.py:213`).

## 5. Validation transcript (scratch clone, lane untouched)

Clone: `git clone -q --shared <lane> $S/lane`; `git -C $S/lane rev-parse --show-toplevel` →
`/fast/scratch/hyaku/tameshi-r51/T51ScribeRowBash/lane`. Registry copy at
`$S/lane/corpus/SOURCES.md` with the row inserted after `:146` and the round note appended.

Baseline (clone's own registry, no draft changes) — `base.out`:

```text
file    ok      /fast/scratch/hyaku/tameshi-r51/T51ScribeRowBash/lane/corpus/SOURCES.md
exit=0      (0 E-codes; 14 × W04, 1 × W01)
```

Draft row only, entry not yet written — `draft.out`, `diff base.out draft.out`:

```text
16c16
< file  ok      /fast/scratch/hyaku/tameshi-r51/T51ScribeRowBash/lane/corpus/SOURCES.md
---
> file  E11   S273 missing used-by corpus/knowledge/mutation-case-kagi-drift-pins.md
exit=1
```

Draft row + draft entry (`source:` line above, stub body) — `final.out`:

```text
file    ok      /fast/scratch/hyaku/tameshi-r51/T51ScribeRowBash/lane/corpus/SOURCES.md
exit=0      diff base.out final.out → empty (identical warning set: 14 × W04, 1 × W01, 0 × E)
```

Row shape, same copy:

```text
grep -c '^| S[0-9]' → 132
grep '^| S273 |' | awk -F'|' → NF=13 cells=11
```

Frozen rule replay (both commits in the clone; **simulation, not a verdict**):

```text
sourced_entry(lane=clone, rev=HEAD, rel='kagi-shokunin/corpus/drift-pins.sh')
→ (1, 1, 1)  ['ENTRY corpus/knowledge/mutation-case-kagi-drift-pins.md source=S273 readme=1']
```

## 6. What this draft does not claim

- Not that C2 verifies: the leg, the embedded spec, the sweep, the TABLE and `--regression` are
  other seats' surfaces; this seat drafted one row and one lesson bullet.
- Not that S272 exists: the registry's own line (`corpus/SOURCES.md:498`) says `S272` is next;
  this row is S273 per the assignment. If no row takes S272 this round, S273 leaves a gap the
  census does not police (no contiguity code) but the round note should then say so.
- Not that the counts I could not see are right: the gnu.org page was never read, so nothing here
  describes its bytes, its sha or its content.

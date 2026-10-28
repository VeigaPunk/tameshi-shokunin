# T54W2Read09 — wave-2 cold read at C1, round 54

- Seat: `T54W2Read09` (reader, leaf — no dispatch)
- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
- CAND: `99c3bc88d704566197783f66b211ee0a830e0330` (C1)
- Heading read: `## The operator's runbook and the six-leg regression (round 10, measured)`
- Span at C1: lines 1295–1302 (the reader prints `start: 1295, end: 1303`; line 1303 is the
  trailing blank that the round-18 `sectionize()` strips — see receipt 2)
- `section_sha256`: `636e850f885cb39904d100f67446e1039aa48c6510c2a66ea6e6d5aaa089faf7`
- Scratch: `TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W2Read09`

## Verdict

**No findings.** `findings: []`. Every anchor in the section resolves at C1, the paragraph is
consistent with every artifact it names, it carries no table (so no stale cell is possible in
these bytes), and the QUALITY-104 mechanical sweep is empty. The section is also byte-identical
to its C0 (`59c38109`) form, i.e. the fix pass did not touch it — it was not the source of any
wave-1 defect and it did not gain one.

## Bytes read (503 B; recomputed sha equals the printed sha)

```
## The operator's runbook and the six-leg regression (round 10, measured)

Round 7 made `--regression` the ledger's replay gate; rounds 8–9 left two
named gaps: the registry ran four legs with cases 5–6 not yet embedded —
named debt (the round-9 receipt's wording; ER-4 caveat (a)), and the operator the arc was built for had no
single entry point. Round 10 closes both — the runbook lands (T10-1, this
round), and the leg cut resolves as an **embedding** of cases 5–6 (T10-2),
never a re-cut.
```

## Receipts

### 1. Section span and sha (git objects only)

```
$ cd /home/vgpnk/Projects/shokunin/tameshi-shokunin && export TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W2Read09
$ python3 .ufo/waves/round-54/reader-section.py /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    99c3bc88d704566197783f66b211ee0a830e0330 "## The operator's runbook and the six-leg regression (round 10, measured)"
{"heading": "## The operator's runbook and the six-leg regression (round 10, measured)",
 "cand": "99c3bc88d704566197783f66b211ee0a830e0330", "start": 1295, "end": 1303,
 "section_sha256": "636e850f885cb39904d100f67446e1039aa48c6510c2a66ea6e6d5aaa089faf7"}

$ git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 99c3bc88d704566197783f66b211ee0a830e0330:SKILL.md > SKILL.C1.md
$ python3 -c "import hashlib; l=open('SKILL.C1.md',encoding='utf-8').read().split('\n'); s='\n'.join(l[1294:1302]); print(len(s.encode()), hashlib.sha256(s.encode()).hexdigest())"
503 636e850f885cb39904d100f67446e1039aa48c6510c2a66ea6e6d5aaa089faf7
```

The recompute matches the printed sha, so the 503 bytes quoted above *are* the sha'd bytes —
`sectionize()` joins heading-through-last-non-blank line with `\n` and no trailing newline
(`.ufo/evidence/round-18/measure.py:209-238`).

### 2. Anchors resolve at C1

The section carries **one** backticked token (`--regression`), **zero** `path:line` citations and
**zero** table rows; the anchor risk is therefore in the four label references:

| anchor in the section | resolves at C1 to | evidence (command → output) |
|---|---|---|
| `--regression` | the runner's own flag, present | `git show C1:tools/mutate-and-run.sh \| grep -n -- '--regression'` → `5:`, `8:`, `23:`, `84:`, `139:` … |
| "Round 7 made `--regression` the ledger's replay gate" | the round-7 section, same page | `SKILL.C1.md:934-936`: "Round 7 turns `--regression` … into the fleet's **leg ledger**: every recorded mutation case is a leg of this ledger, replayed at its pinned original revision." Runner header agrees and is precise about the split: `tools/mutate-and-run.sh:4-8` "r4-2 … adds --regression …; r7-1 (TAMESHI-T7-1) turns --regression into the fleet leg ledger" |
| "the round-9 receipt's wording" = the `### The receipt at this boundary` block of the round-9 section | `SKILL.C1.md:1227` (that block's heading) + `:1242-1243`: "Cases 5–6 were not yet embedded at this boundary … their rows carried no `REGRESSION` line at this boundary — **named debt**, not smoothed" | the phrase is in that block verbatim, and it recurs in the runbook's two cases-5/6 lines (`corpus/knowledge/operator-runbook.md:174`, `:375`), while the ledger that holds ER-4 never uses it (`git show C1:corpus/knowledge/fleet-kill-rate-ledger.md \| grep -c "named debt"` → `0`) — so the wording anchor is the page's round-9 receipt and ER-4 is cited for the substance, not the phrasing |
| `ER-4 caveat (a)` | `corpus/knowledge/fleet-kill-rate-ledger.md:318` (ER-4 header) and `:350` | `:350` "Two measured caveats, stated not smoothed: (a) the tool embeds **4** legs — cases 5/6 (checklist-run, claims-check) carry no `REGRESSION` line at `cf41efaa…`" |
| "the registry ran four legs with cases 5–6 not yet embedded" | `fleet-kill-rate-ledger.md:281-282` | `:281` "the harness at `cf41efaa8be5f52d…` … carries **four** materialized legs"; `:282` "Cases 5/6 are not embedded in `--regression`" |
| `T10-1` | `corpus/knowledge/operator-runbook.md:1,3` ("… end to end (round 10, T10-1)"; "Written 2026-10-14 by lane T10-1"); `plans/round-10-record-draft.md:232` ("TAMESHI-T10-1 → `corpus/knowledge/operator-runbook.md`") | the runbook blob exists at C1: `git cat-file -s C1:corpus/knowledge/operator-runbook.md` → `33515`; `… \| wc -l` → `516`; `sha256sum` → `8b2e185ff011f6cf…`, the same blob in `59c38109`'s tree |
| `T10-2` | `tools/mutate-and-run.sh:2` "… (tameshi-shokunin, r10-2, TAMESHI-T10-2)"; `:12` "(TAMESHI-T10-2) resolves the round-8 leg cut — cases 5/6 … embedded as the fifth and sixth legs"; `plans/round-10-record-draft.md:242` "TAMESHI-T10-2 → `tools/mutate-and-run.sh` **r10-2**" | both live at C1 — no evidence-snapshot-only anchor |

### 3. Numbers in the paragraph vs the artifacts (contradiction sweep)

`7` / `8–9` / `four legs` / `5–6` / `10` / `six-leg` were each checked against the artifact that
owns the fact; all agree, and the paragraph contradicts no other sentence in its own bytes:

- six = the four materialized legs (`:281`) + the two embedded cases 5/6 (`:282`, resolved at r10-2).
- The heading's dating of the six-leg regression to round 10 is the runner's own dating, not an
  extrapolation: `tools/mutate-and-run.sh:84` — "`--regression` (r4-2; r7-1 leg ledger; **r10-2 six
  legs**; r16 seven; r18 eight; r26 nine; r51 ten)".
- "Round 10 closes both" is borne out twice: the runbook is in the tree at C1 (see `T10-1` row) and
  the r10-2 embedding is in the tree's runner header (`:12`), with the round-10 record's own
  closeout row (`plans/round-10-record-draft.md:205`) naming both.

### 4. Stale table cell / QUALITY-104 mechanics

```
$ awk 'NR>=1295&&NR<=1302 && /^\|/' SKILL.C1.md | wc -l      → 0        # no table in these bytes
$ sed -n '1295,1302p' SKILL.C1.md | grep -o '`[^`]*`' | sort -u → `--regression`
$ sed -n '1295,1302p' SKILL.C1.md | grep -oE '[A-Za-z0-9_./-]+\.(md|sh|py|json)(:[0-9-]+)?' → (none)
$ grep -n "  "            <section>  → none      # no double space
$ grep -nE " [,.;:]"      <section>  → none      # no space before punctuation
$ grep -nE "[,.;:][A-Za-z]" <section> → none     # no missing space after punctuation
$ sed -n '1297,1302p' SKILL.C1.md | tr -cd '()' | fold -w1 | sort | uniq -c → 4 "(" / 4 ")"  (balanced)
$ grep -nP "\t|\xc2\xa0"  <section>  → no tabs/nbsp
$ python3 duplicate 3-gram scan over the section text → []
```

The one nested parenthetical `(the round-9 receipt's wording; ER-4 caveat (a))` is a single
parenthetical with a nested errata letter, and the sibling instance in the same section family
(`SKILL.C1.md:1371`, `"named debt" (the round-9 receipt's cases-5–6 caveat; ER-4 caveat (a))`)
uses the identical shape — it is not a duplicated parenthetical of the round-52
"(**ten** since round 51) (ten since round 51)" kind.

### 5. Fix-pass independence

```
$ git diff -U0 59c38109bf11 99c3bc88d704566197783f66b211ee0a830e0330 -- SKILL.md | grep -c '^@@'
22
$ git diff -U0 … -- SKILL.md | grep '^@@' | sed -E 's/^@@ -([0-9]+)(,[0-9]+)? \+.*/\1/' | paste -sd' ' -
34 161 173 875 879 952 961 970 1269 1282 1286 1306 1319 1506 1551 1606 1608 1731 1852 1879 1958 1961
$ git diff -U0 … -- SKILL.md | grep -E '^@@ -1(29[5-9]|30[0-2])'
none
```

Nothing between `@@ -1306` and the hunk above it: the C1 fix pass changed the neighbouring
`### The operator's runbook — …` cell (line 1306: `e1e349b6…` 511 L / 31 416 B uncommitted →
`8b2e185f…` 516 L / 33 515 B committed at `59c38109`, which I verified against the blob) but left
the section under read untouched. So no C1 hunk landed in these bytes and none can have
introduced a defect here.

## Observations I did not file (below the stated bar — recorded so the panel can see they were considered)

- Line 1299 is 106 chars while its siblings are 72–74 (`awk 'NR>=1295&&NR<=1302{print NR, length}'`).
  It is the trace of an inserted clause that was never re-wrapped. This is cosmetic: it is outside
  the four reader criteria (anchor, contradiction, stale cell, QUALITY-104 mechanics), and 163
  non-table lines in the file exceed 90 chars, so it is not a document-convention violation either.
- `SKILL.C1.md:1415` dates the "six-leg registry" to round 11, while the runner's own header
  (`:84`) dates six legs to r10-2 and this section dates the six-leg regression to round 10. That
  tension lives entirely outside these 503 bytes; it belongs to the section that owns `:1415`, not
  to this read, and I did not file it.
- The phrase "the arc" first appears at line 1299 and is only glossed later (`:1389-1391`). Forward
  reference in a linear document, not a dangling anchor.

## Artifacts opened (absolute paths)

- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-54/reader-section.py` (read)
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/SKILL.md` at `99c3bc88…` (via `git show`, all 2197 lines into scratch as `SKILL.C1.md`)
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/SKILL.md` at `59c38109bf11` (via `git show`, scratch `SKILL.C0.md`)
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/fleet-kill-rate-ledger.md` at C1 (scratch `ledger.C1.md`; lines 228–245, 318–360)
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/operator-runbook.md` at C1 and at `59c38109` (bytes/size/sha only)
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh` at C1 (header 1–14, `--regression` refs, line 84)
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/plans/round-10.plan.md` at C1 (head)
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/plans/round-10-record-draft.md` at C1 (lines 79–91, 205, 232–255, via `git grep`)
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/QUALITY.md` at C1 (criteria 103–105, lines 1562–1600)
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/measure.py` at C1 (`sectionize`, lines 209–238)

## Commands run (read-only; every path absolute or run from the lane/scratch root)

```
mkdir -p /fast/scratch/hyaku/tameshi-r54/T54W2Read09
export TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W2Read09
python3 .ufo/waves/round-54/reader-section.py <lane> 99c3bc88… "<heading>"
git -C <lane> rev-parse HEAD ; git -C <lane> log --oneline -3
git -C <lane> show 99c3bc88…:SKILL.md > SKILL.C1.md
git -C <lane> show 59c38109bf11:SKILL.md > SKILL.C0.md
git -C <lane> show 99c3bc88…:corpus/knowledge/fleet-kill-rate-ledger.md > ledger.C1.md
git -C <lane> show 99c3bc88…:corpus/knowledge/operator-runbook.md | sha256sum ; … | wc -l ; git cat-file -s …:<path>
git -C <lane> show 99c3bc88…:tools/mutate-and-run.sh | sed -n '1,14p' ; … | grep -n -- '--regression'
git -C <lane> show 99c3bc88…:plans/round-10.plan.md | head -60
git -C <lane> show 99c3bc88…:corpus/QUALITY.md | sed -n '1562,1600p'
git -C <lane> show 99c3bc88…:.ufo/evidence/round-18/measure.py | grep -n 'def sectionize' -A 30
git -C <lane> grep -n "T10-1" / "T10-2" / "TAMESHI-T10" / "named debt" / "Named follow-up" 99c3bc88… -- <paths>
git -C <lane> diff -U0 59c38109bf11 99c3bc88… -- SKILL.md
git -C <lane> ls-tree -r --name-only 99c3bc88… -- plans
awk / sed / grep / sort / uniq / sha256sum / python3 -c over the scratch copies
```

## Bounds honoured

- Read-only on every lane and fleet path; the only writes are this pair of deliverables plus my
  scratch. `SKILL.md`, counters, contract, freeze, ledger, wave specs: untouched.
- No mutating git/jj command anywhere (no commit/add/fetch/reset/checkout); all git calls are
  `show` / `grep` / `cat-file` / `diff` / `ls-tree` / `rev-parse` / `log`.
- No fleet-root tracked file touched. No subagent dispatch (leaf seat).
- Tooling: nothing installed or upgraded — no gap needed one (pacman is paused host-wide; the
  task was satisfied with the in-tree `python3` and `git`). No `~/.local/bin` or PATH writes.

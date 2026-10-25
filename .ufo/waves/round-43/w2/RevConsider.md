# RevConsider — lesson `### considerthese` paragraph vs `considerthese/`

Scope: `corpus/lessons/round-43.md` lines 108–113 at HEAD `e20cf89` (lines 103–107 at
the records commit `c5335c7`; same text, shifted +5 by the A10 receipts commit). Read-only
seat: no counters were run at `c5335c7`; only `git show` at the permitted revs `487b8f0`
and file reads. The paragraph verbatim:

> `considerthese/2026-10-24.md` proposals 1–4 were mined in earlier rounds; the
> one still unimplemented that this round's work touches is the *standing-command*
> idea: a self-assessment number should be re-derivable by a command a non-author
> can run. C2's m13 is the first mechanical instance of it for the registry count.
> No proposal is claimed as implemented this round; proposal 5's SHONEN table was
> mined in round 42 and no box moved.

---

## Verified true

- **"proposals 1–4 were mined in earlier rounds"** — all five proposals of the file
  (`considerthese/2026-10-24.md:63-75`) and their landings:

  - :63-65 p1 "Pin blast-radius report before a tool edit" → QUALITY criterion 80
    (`corpus/QUALITY.md:967`, "proposal 1 … mined 2026-10-25"), round 41.
  - :66-67 p2 "Unreachable-provenance check" → QUALITY criterion 76, mined at round 38
    (`corpus/lessons/round-38.md:86-89`).
  - :68-69 p3 "Persistently unreachable sources" → QUALITY criterion 79
    (`corpus/QUALITY.md:951`, "proposal 3, mined 2026-10-24"), round 40.
  - :70-72 p4 "Attempt and dispatch health per round" → QUALITY criterion 78
    (`corpus/QUALITY.md:938`, "proposal 4, mined 2026-10-24"), round 39.

  Independent confirmation: wave-1 ScoutConsider's own table
  (`.ufo/waves/round-43/w1/ScoutConsider.md:56-64`) records "5 — all five mined by the
  lane; no status section is owed" with the same landings.

- **"proposal 5's SHONEN table was mined in round 42 and no box moved"** — true:
  `corpus/lessons/round-42.md:142-151` ("proposal 5 … the one proposal of that file
  not mined before. Mined as this table … `One box out of four is mechanically
  checkable today. No box moves this round.`").

## F1 (high) — "C2's m13 is the first mechanical instance of it for the registry count" is falsified by the lane's own records, twice

**Not first.** The standing `sources-registry` row has carried an explicitly
"re-derivable command" for the registry count since round 35, present at the base rev:

```
$ git show 487b8f0:SCORECARD.md | grep sources-registry | sed -n '4p' | cut -c1-240
| sources-registry | … | row count from the re-derivable command
`grep -cE '^\| S[0-9]{3} \|' corpus/SOURCES.md` → 99 rows at round 35 …
```

`git log -S "re-derivable command" -- SCORECARD.md` → first introduced in `d16f9b5`
(round-35 commit, 2026-10-23). Repeated at `SCORECARD.md:1851` (r35), `:1993` (r41,
109 rows), `:2020` (r42, 113 rows) — all in the tree at `487b8f0`. The command
reproduces the printed number for a non-author:

```
$ git show 487b8f0:corpus/SOURCES.md | grep -cE '^\| S[0-9]{3} \|'
113        # matches the round-42 row's "113 rows at round 42"
```

And the registry-count *claim* has been mechanically checked since round 35 by class
m6: `SCORECARD.md:1687` names "m6 standing sources-registry row count"; the round-35
counter reads the newest standing row and diffs it against the registry
(`.ufo/evidence/round-35/c2/c2-measure.py:141-151`). So a number plus a runnable
command plus a mechanical cross-check of the count existed eight rounds before m13.
The round-43 records themselves describe m13's contribution as a *replacement*, not a
first: `SCORECARD.md:2081` — "the column-zero form of this command is what C2 class
m13 replaced". An accurate statement is "m13 is the first class to require the
*census-valid form* (`^ {0,3}`) of the standing command"; "first mechanical instance
of it for the registry count" as written is false.

**Not a re-derivation.** m13 never executes the command it audits. The only
subprocess calls in `.ufo/evidence/round-43/calibration/measure.py` are `git` at
lines 84 and 372; `m13_standing_command` (:176-196) regex-extracts backticked spans
containing the substring `grep` on the SCORECARD row and requires `0,3`, then counts
a Python-constructed mirror (`count_patterns(indent_mirror(registry_text))`). Probe
of an unmodified copy in scratch:

```
$ python3 - <<'EOF'
import importlib.util, subprocess
spec = importlib.util.spec_from_file_location('m','/tmp/tameshi-r43-w2-RevConsider-m13/measure.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
reg = subprocess.run(['git','-C',LANE,'show','487b8f0:corpus/SOURCES.md'],capture_output=True).stdout.decode()
bogus = "| sources-registry | x | `grep -cE '^ {0,3}\\| S[0-9]{9} \\|' corpus/DOES-NOT-EXIST.md` -> 114 rows at round 43 |\n"
m.m13_standing_command(bogus, reg)
EOF
([], 'standing=1 column0=112 valid=113')   # a row whose command CANNOT re-derive 114 passes m13
```

So m13 is compatible with a command that re-derives nothing (wrong id width,
nonexistent path): it checks the cell's *shape*, not that the number is re-derivable
by the command — which is exactly what the lesson's own limits section concedes at
`corpus/lessons/round-43.md:163-164`: "m13 proves the standing command's *pattern*
and its load-bearing behaviour on a two-space indent; it does not prove the command
is the one that produced the printed number." The paragraph states, 55 lines
earlier, the unqualified opposite.

## F2 (medium) — the "standing-command idea" is not a proposal of `considerthese/2026-10-24.md`; the paragraph counts past the file

`grep -rn "standing" considerthese/` returns one hit (`2026-10-24.md:64`, unrelated
"standing table" inside proposal 1); `grep -rni "re-deriv" considerthese/` returns
none. `awk '/^[0-9]\. \*\*/'` on the file gives exactly the five headings at
:63, :66, :68, :70, :73 (quoted above) — no proposal states "a self-assessment number
should be re-derivable by a command a non-author can run". The nearest text is
proposal 5 :73-75, which says the SHONEN boxes "look mechanically checkable by a
non-author" and proposes "which box has which checkable pointer". The exact phrase
"standing command a non-author can run" first appears in the lane's records as the
*column header round 42 invented for its mining table*
(`corpus/lessons/round-42.md:146`) — the mining of proposal 5. So the paragraph
either (a) reads proposal 5 twice — once unnamed as "the one still unimplemented …
the standing-command idea" and once named ("proposal 5's SHONEN table"), or
(b) attributes a sixth idea to a file that has five proposals. Either way a reader
cannot verify "the one still unimplemented" against the file: all five proposals
are mined, per the lane's own scout (`ScoutConsider.md:56`).

On top of the mislabel, the scout's considered-idea pick for this round was a
different file's proposal — `considerthese/2026-10-22.md:75-76` proposal 5,
"Survivor reclassification tracker" — chosen precisely because round 43's C1 relabels
two round-42 survivors (`ScoutConsider.md:67-79`). The lesson's paragraph does not
mention that file at all, so "the one still unimplemented that this round's work
touches" is contested by the round's own wave-1 record.

## F3 (low) — internal tension: "the first mechanical instance" vs "No proposal is claimed as implemented this round"

If m13 were a mechanical instance of the standing-command idea, the round would be
implementing the idea the paragraph calls still-unimplemented — without moving a
SHONEN box (the registry count is not a box; the round-42 table at
`round-42.md:148-151` shows box 3's standing command is
`.ufo/evidence/round-21/coldread/measure.py`, a different and older standing check).
The two sentences coexist only because "no proposal claimed implemented" refers to
the five numbered proposals; but proposal 5's stated scope is SHONEN boxes, and m13
is on the calibration axis, so claiming m13 as "an instance of it" is an instance
claim against proposal 5 that the next sentence denies.

## Residual risk / verification gaps

- I did not run `measure.py` at any rev (records-commit run is prohibited; I invoked
  `m13_standing_command` directly on a copied file). The bogus-row probe proves the
  extraction is a shape check; it does not prove a malicious row would also pass m6 —
  m6 is a separate conjunct and would still compare the stated count to the real
  registry. F1's "not a re-derivation" is about what m13 *proves*, not what the whole
  predicate catches.
- The strongest charitable reading of "first mechanical instance" is "first class to
  audit the command cell" — under that reading the sentence is defensible but still
  wrong for "the standing-command idea" as the paragraph itself defines it ("a number
  should be re-derivable by a command a non-author can run"), which round 35's row
  + m6 already realised.
- The lesson file was rewritten in place around 08:05 (records-commit text +5 lines;
  working tree == HEAD `e20cf89`, clean `git diff`). Line numbers cited are
  current-tree ones; the considerthese paragraph itself is byte-identical to
  `c5335c7:103-107`.
- `git show 487b8f0:corpus/SOURCES.md | grep -cE '^ {0,3}\| S[0-9]{3} \|'` also
  prints 113 (no indented rows exist), so the census-valid repair m13 enforces is
  unexercised by today's registry — its only load-bearing evidence is the fabricated
  mirror, exactly as criterion 84 describes.

## Verdict on the item

"Proposals 1–4 mined earlier" — accurate (r38/r39/r40/r41 → QUALITY 76-80). The two
implementation claims are not: "C2's m13 is the first mechanical instance of the
standing-command idea for the registry count" overstates twice — a re-derivable
command row plus mechanical count check existed since round 35 (`SCORECARD.md:1609`,
`:1687`), and m13 does not re-derive anything (shape check over a Python mirror;
bogus command passes; disclaimed at `:163-164`). And "the one still unimplemented"
of `considerthese/2026-10-24.md` miscounts: the file holds five proposals, all five
mined, and the idea named in the paragraph is the round-42 column header for
proposal 5, not a line in the file.

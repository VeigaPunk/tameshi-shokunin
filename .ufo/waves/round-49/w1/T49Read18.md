# T49Read18 — C1 reader, `## Effective expectation reconciliation — round 14`, ordinals 5-9

Seat: reader (calibration / C1 reads). Base `8ca67421111fa354b47b803358391d0b07fc6db9`. Lane
`/home/vgpnk/Projects/shokunin/tameshi-shokunin`. I read; I did not edit SKILL.md, the lane, or any target.

## What was done

For each of the five pointers the frozen extractor finds in this section at ordinals 5-9 I opened the base
`SKILL.md` line the pointer sits on, read the clause it supports, opened the target at base, and recorded a
verdict, a located excerpt and (where needed) a correction. Every check was run through the frozen counter's own
primitives — `norm()`, `pointed_text()`, `target_sections()`, `list_pointers()`, `check_reads()`, `blob()`,
`EXCERPT_MIN/MAX` — imported from `.ufo/evidence/round-49/c1/measure.py`, so an excerpt length below is the
*collapsed* length the counter measures, not the raw character count.

Gates that held before any row was written (`T49Read18.excerpt-check.txt`):

- `python3 .ufo/evidence/round-49/c1/measure.py --lane . --rev 8ca67421111fa354b47b803358391d0b07fc6db9 --list`
  → 90 pointers, exit 0, byte-identical to the frozen control on `(ordinal, raw, file, kind, ranges, skill_line)`
  for this section (all 10). Receipt: `T49Read18.list.json`.
- Section identity: `target_sections()` reports `start=1563 end=1596
  sha256=5fd3636417f76d37a9ba2d2df8aea44c38a082eda06c47c47b1c798e42ad72d5`, equal to the frozen
  `section_sha256` in `.ufo/evidence/round-49/control/c1-pointers-at-base-8ca67421.json`. So the 10 pointers are
  the section's real pointer set and the floor (10, contract `claims.C1.floors.r14`) is met by construction.
- Section end at 1596 (`measure.py:219-239`, `### Round-14 historical registry` at `SKILL.md:1597` starts the next
  section): the registry table at `SKILL.md:1599-1602` is **not** inside this section, so its already-qualified
  `.ufo/evidence/round-14/capture-context.py` (`SKILL.md:1602`) is a different section's pointer and cannot
  collide with ordinal 7.

## Row-by-row

### ord 5 — `.ufo/evidence/round-14/verification-final.json` (`SKILL.md:1587`) — **holds**

Clause: "retains the corrected selftest and frozen before/after outcomes". The file is held at base (70 lines)
and carries `checks[0] disposition_selftest exit 0 expected 0` (the *corrected* selftest — `verification.json` has
the same check at `exit 1 expected 0`), `checks[1] unresolved_before exit 1 expected 1`, `checks[2]
resolved_after exit 0 expected 0` with their full stdout, plus `measured_commit
64314783836bb0d05ad06a774d7310fd3a23b5bd` and a 6-entry `input_sha256` map — which is also what the section's next
sentence ("The revision measured is recorded separately", `SKILL.md:1590`) points at. Excerpt (121 collapsed
chars) is the top-level `supersedes` field, which says in the file's own words that only the selftest failure is
superseded and "original real before/after observations remain valid".

Command: `git -C LANE show BASE:.ufo/evidence/round-14/verification-final.json | python3 -c "import json,sys;
d=json.load(sys.stdin); [print(c['name'],c['exit'],c['expected_exit']) for c in d['checks']]"` → three checks as
above. Path pointer, so no line drift is possible.

### ord 6 — `verification.json` (`SKILL.md:1588`) — **unresolved** (fix supplied)

`resolve()` (`measure.py:188-192`) tries `verification.json`, `corpus/knowledge/verification.json`,
`corpus/verification.json`, `corpus/lessons/verification.json`; none is a blob, so the pointer is `file=null` and
`check_reads()` (`measure.py:270-279`) can only score it `unresolved` — the row cannot pass however good the
excerpt is. **The fact behind it is sound and the file is held**: `.ufo/evidence/round-14/verification.json`
(78 lines at base) contains `checks[0] disposition_selftest` with `exit 1` against `expected_exit 0`, and that
stdout has exactly 34 `SELFTEST_CASE` lines of which 18 are `FAIL` — the sentence's "initial18-of34".
`tools/evidence-disposition.py:181` says "`--selftest` builds isolated /tmp fixtures", so "fixture failures" is the
right noun.

Commands:

- `git -C LANE show BASE:.ufo/evidence/round-14/verification.json | grep -o "SELFTEST_CASE [^ ]* \(PASS\|FAIL\)" | wc -l` → `34`
- `... | grep -o "SELFTEST_CASE [^ ]* FAIL" | wc -l` → `18`

This is the same defect class T49Read10 found elsewhere: a bare basename the extractor cannot qualify. Proposed fix
qualifies the pointer with its directory (name kept, pointer count stays 10 because the bare token stops matching
`PATH_RE` once preceded by `/`).

### ord 7 — `capture-context.py` (`SKILL.md:1593`) — **unresolved** (fix supplied)

Same `file=null` failure: no `capture-context.py` at the lane root, `corpus/knowledge/`, `corpus/` or
`corpus/lessons/`. The file is held at `.ufo/evidence/round-14/capture-context.py` (647 lines at base) and its own
docstring states the single output — `Output: .ufo/evidence/round-14/context-receipt.json (atomic, 0644); no other
path is written.` — with `OUTPUT_REL = ".ufo/evidence/round-14/context-receipt.json"` at `:58`, which is exactly the
mechanism the sentence gives for "must not be run again": a re-run overwrites the frozen receipt. The retained run
is recorded at `.ufo/evidence/round-14/verification.json` `checks[3] context_capture` (`CONTEXT: OK
receipt=.ufo/evidence/round-14/context-receipt.json exit=0`). `SKILL.md:1602` (next section) and `SKILL.md:1623`
already use the qualified spelling.

Command: `git -C LANE show BASE:.ufo/evidence/round-14/capture-context.py | sed -n '20,30p;55,60p'`.

### ord 8 — `S049` → `corpus/SOURCES.md:58` — **holds**

The registry row (re-derived by the counter from `^ {0,3}\|\s*S049\s*\|`, so an appended round-49 row cannot move
it) is "Python subprocess environment mapping … Python subprocess.run env argument semantics, not proof of a
particular historical environment", teaches "Explicit env mappings define child environment rather than merely
documenting an intended injection; retain the bounded override with the observed command" — precisely the
"S049 (Python child-environment contract)" clause, and its scope wording supplies the limitation the section's
table row applies to a documented-only override. Excerpt: 154 collapsed chars from that row.

Command: `git -C LANE show BASE:corpus/SOURCES.md | sed -n '58p'`.

### ord 9 — `S003` → `corpus/SOURCES.md:14` — **holds**

The row's anchor cell is "§Incremental mode and §Limitations" and its teaches cell gives the declared blind spots
("env vars, dependencies and .snap files are not detected; the dry run stays required"), which is what
"S003 Limitations" (`SKILL.md:1566`) cites. Excerpt: 149 collapsed chars from that row.

Command: `git -C LANE show BASE:corpus/SOURCES.md | sed -n '14p'`.

## Corrected-candidate probe (probe, not a verdict)

In a scratch `git clone --shared` of the lane (toplevel asserted, one commit of SKILL.md only), I applied the two
proposed `skill_old → skill_new` edits and re-ran the counter's own extraction and `check_reads()` there:
section pointer count stays **10**, ordinals 5-9 become
`(.ufo/evidence/round-14/verification-final.json | .ufo/evidence/round-14/verification.json |
.ufo/evidence/round-14/capture-context.py | S049 | S003)` and all five score `ok` with `excerpt_miss=0`,
`not_holds=0`. Base scoring of the same three `holds` rows: ordinals 5, 8, 9 all `ok`; ordinals 6 and 7
`unresolved`. Ordinal 4 (`dispositions.json`, another seat's pointer) stays `unresolved` in that probe and is not
touched by these edits — reported so it is not read as a regression from this seat.

## Findings

1. `SKILL.md:1588` — bare basename pointer `verification.json` is unresolvable (`measure.py:188-192`); the file is
   held at `.ufo/evidence/round-14/verification.json` and its 34-case/18-FAIL stdout backs the sentence. Fix:
   `` `verification.json` retains the `` → `` `.ufo/evidence/round-14/verification.json` retains the ``.
2. `SKILL.md:1593` — bare basename pointer `capture-context.py` is unresolvable; the file is held at
   `.ufo/evidence/round-14/capture-context.py` and its docstring/output constant back the "must not be run again"
   clause. Fix: `the round14\n   `capture-context.py` produced the retained context receipt` →
   `` `.ufo/evidence/round-14/capture-context.py` produced the retained context receipt ``.
3. `SKILL.md:1588` carries the rendering artifact `initial18-of34` (missing spaces). Left alone — out of this
   item's scope (pointer correction), recorded so the L1 can decide.
4. Ordinals 5, 8, 9 need no change: the targets are held, the quoted text is in them, and the S-id rows are
   re-derived per revision.

## Out of scope here

- Ordinals 0-4 of this section (other wave-1 seats); ordinal 4's bare `dispositions.json` is unresolved at base
  and its fix is not mine.
- C2 (generator, hidden panel, witnesses) — untouched; I read nothing under `~/.local/state/` and none of the
  three withheld stdout files.
- No claim decision: whether C1 passes is the L1's deciding run at REV.

## Touched surfaces

Written (all inside `.ufo/waves/round-49/w1/`): `T49Read18.rows.json`, `T49Read18.excerpt-check.txt`,
`T49Read18.list.json`, `T49Read18.md`. Lane checkout otherwise untouched (`git status --porcelain` shows only my
four files added, plus other seats' files I did not write). Scratch `/fast/scratch/hyaku/tameshi-r49/T49Read18`
deleted. No tool installed, no pacman transaction.

## Artifact paths

- `.ufo/waves/round-49/w1/T49Read18.rows.json` — the five rows (`rows` key), including `proposed_fix` on 6 and 7
- `.ufo/waves/round-49/w1/T49Read18.excerpt-check.txt` — gate receipt with commands and full probe output
- `.ufo/waves/round-49/w1/T49Read18.list.json` — `--list` output at base (90 pointers)
- `.ufo/waves/round-49/w1/T49Read18.md` — this report

## Summary

- Read ordinals 5-9 of `## Effective expectation reconciliation — round 14` at base: 3 hold, 2 are unresolvable.
- holds: ord 5 `.ufo/evidence/round-14/verification-final.json` (corrected selftest + before/after checks), ord 8
  `S049` (child-env contract row), ord 9 `S003` (Limitations row); S-ids are re-derived per revision.
- unresolved: ord 6 `SKILL.md:1588` `verification.json` and ord 7 `SKILL.md:1593` `capture-context.py` — bare
  basenames `resolve()` cannot locate (`measure.py:188-192`); both files are held under `.ufo/evidence/round-14/`.
- Content is sound: 34 SELFTEST_CASE lines / 18 FAIL in `verification.json`; `capture-context.py:58` writes only
  the retained `context-receipt.json`.
- Two `skill_old`/`skill_new` qualifications supplied; in a scratch clone they keep the section at 10 pointers and
  score all five rows `ok` (probe only).
- Remaining gap for the L1: ordinal 4 (`dispositions.json`, not this seat) is still unresolved at base.
- Nothing under `~/.local/state/` or the withheld C2 stdout files was read; no claim decided.

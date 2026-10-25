# ScribeQuality — round 39 w1

## Task

Check whether `corpus/QUALITY.md` already has a criterion whose falsifier is
`tools/wave-parent-settle.py`. Report the last criterion number.

## Finding

Yes. **Criterion 78** ("a wave parent that exits before seat terminals is
unsettled") already carries `tools/wave-parent-settle.py` as its falsifier.

- `corpus/QUALITY.md:931` — heading `### Criterion 78 — a wave parent that exits
  before seat terminals is unsettled`.
- `corpus/QUALITY.md:939-942` — falsifier text:
  `Falsifier that must fail: `python3 tools/wave-parent-settle.py --selftest`
  must fail if the red fixture (parent_exit_unix=10, seat terminal_unix=20) is
  classified SETTLED.`
- `corpus/QUALITY.md:937-938` — lesson cite names `corpus/lessons/round-39.md`
  and `considerthese/2026-10-24.md` proposal 4 ("mined 2026-10-24, not edited").

## Last criterion number

**78.** The file's numbered criteria run 1–75 (list syntax, rounds 1–37) plus
headed criteria 76, 77, 78 (`### Criterion N` headings, lines 903, 916, 931).
Criterion 78 is the last entry in the file; the file ends at line 942 with the
tail of 78's falsifier text. No criterion numbered above 78 exists.

## Consistency with the round-39 contract

`.ufo/evidence/round-39/contract.json:39-44` (`settlement` block) names the same
tool (`tools/wave-parent-settle.py`) and the same red fixture
(parent_exit_unix=10, seat terminal_unix=20 → UNSETTLED) and green fixture
(parent_exit_unix=30, terminals 20/25 → SETTLED), matching criterion 78's
falsifier as committed.

## Commands / checks run

- `grep -n 'wave-parent-settle' corpus/QUALITY.md` → single hit region at
  lines 938-942 (inside criterion 78).
- `read corpus/QUALITY.md:890-942` → confirmed heading at line 931 and file end
  at line 942.
- `grep -nE '^\s*[0-9]+\.' corpus/QUALITY.md | tail -15` → last flat-list
  criterion is 75 (line 881); 76–78 are `### Criterion` headings.

No install or update was performed (pacman transactions paused per lane rules;
nothing needed).

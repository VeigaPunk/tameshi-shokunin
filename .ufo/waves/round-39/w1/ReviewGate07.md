# ReviewGate07 — census attack on tools/mte-interop.py

## Finding (missed write)

`tools/mte-interop.py:341`

    shutil.copyfile(workdir / leg / 'spec.copy', out / ('%s.spec' % leg))

`tools/mte-interop.py:280` (same class)

    shutil.copy2(ROOT / 'tools/mutate-and-run.sh', lane / 'tools/mutate-and-run.sh')

Both are real file-content writes whose destination path sits on the same
line as the call, in Python, with no shell redirect. The frozen `WRITE_RE`
(`open(...['"](w|a|w+|a+|wb|ab)['"]...|.write_text(|.write_bytes(`) does not
match `shutil.copyfile`/`shutil.copy2`, so the census under-reports
`live_write_sites` for this gate: 9 counted vs 11 true file-writing calls.

Named-limit check against the tool docstring's specific exclusions:
- shell redirects — does not apply;
- "path is not on the same line as the call" — does not apply (dst is inline);
- "writes ... in every language" — does not apply (Python stdlib call).

Only the blanket "frozen pattern list / not a full lexer" disclaimer covers
the miss. Line 341 is the sharper case: it sits inside the same `--emit`
block as lines 340 and 342, which the census does count, so the pattern
misses a write adjacent to two writes it sees.

Also verified for the same file (correctly out of scope or correctly
classified):
- `:90` `process.stdout.write(...)` — JS-in-`NODE_RUNNER`-string to stdout,
  covered by the language disclaimer; not a file write.
- `:283` `(stage / sibling.name).symlink_to(sibling)` — creates a symlink,
  not file contents; not counted.
- `unflagged=0` for this gate is correct: no expected/golden-named writes
  exist; `EXPECTED_RE` hits none of the 9 counted lines and `FLAG_RE` is
  absent from the file.

## Predicate impact

`C2_R39_PASS` is unaffected: per the contract kill rule, `live_write_sites`
and `live_unflagged` are reported, not PASS conjuncts, and the planted
controls / fixture / sha pin / 21-gate classification all still hold. The
finding falsifies the completeness of the "write-path census" claim for
this gate (2 of 11 writes invisible), not the frozen predicate itself.

## Command / reproduction

`python3 -c` run over `tools/mte-interop.py` with the exact `WRITE_RE`,
`EXPECTED_RE`, `SCRATCH_RE`, `FLAG_RE` from `tools/write-path-census.py`
(pin bc8c660c...): 9 counted sites (lines 215, 216, 217, 288, 340, 342,
388, 389, 392), `flagged=False`; missed writes at lines 280 and 341.

Tool installs: none (pacman transactions paused per lane bounds; stdlib only).

# T52W1ReviewSkillLines — base-anchored C2 m1–m3 corrections

Base inspected: `ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4`. This is proposed replacement text only; no lane source file was edited. The C2 counter defines m1–m3 in `.ufo/evidence/round-52/c2/measure.py:1-31,82-117`.

| Check / base location | Old text (base) | Proposed replacement | Evidence at base (command and result) |
|---|---|---|---|
| m1a/m1b — `SKILL.md:2136` | `leg set not equal to the nine ledger legs` … `mte-interop-check` (9/9) | `leg set not equal to the ten ledger legs` … `mte-interop-check` (10/10) | `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4:tools/mte-interop.py` shows `LEG_TABLE` at lines 74–78 with ten keys (confirmed by Python AST `len(LEG_TABLE) == 10`; the counter uses the same AST count). The base runner's ten leg names are listed at `tools/mutate-and-run.sh:84-97`; the check's report compares against the committed tables. This is the check's expected/actual leg count. **C1 dependency:** the base registry row still expects 9/9; the proposed registry-row text is true at the deciding revision only when C1 updates that expectation to 10/10, as its frozen predicate requires. |
| m3a — `SKILL.md:174` | `the maintained driver also prints the failing count: tools/mutate-and-run.sh:425` | `the maintained driver also prints the failing count: tools/mutate-and-run.sh:434` | `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4:tools/mutate-and-run.sh` then `grep -n 'old-string-count='` identifies the APPLY FAIL print at line 434. The base target 425 is `data = open(pristine, 'rb').read()`, not the count diagnostic. |
| m3b — `SKILL.md:211` | `... marks the run DEGRADED: tools/mutate-and-run.sh:569-574` | `... marks the run DEGRADED: tools/mutate-and-run.sh:579-583` | The base runner has the kill-rate calculation and degraded-result branch in this range; `grep -n 'MUTATE: DEGRADED'` identifies its print at line 581. Base `569-574` is the tail of sweep execution/restore handling and does not contain that token. |
| m3c — `SKILL.md:937` (bullet starts at 935) | `` `/tmp/tameshi-r4-2-regression.XXXXXX` after prerequisite checks `` | `` `${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX` after prerequisite checks `` | Base runner line 1432 allocates with `mktemp -d "${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX"`; its comment at 148–150 documents the TMPDIR default. This is the exact m3c condition: the old bullet names `/tmp/tameshi-r4-2-regression` without TMPDIR; the replacement names TMPDIR. |
| m2 — write-scope cell, `SKILL.md:2149` | `caller-chosen --workdir (or auto mktemp under /tmp) for run and --regression; selftest under /tmp; fleet leg repos read-only via git show` | `caller-chosen --workdir (or auto mktemp under ${TMPDIR:-/tmp}) for run and --regression; selftest under ${TMPDIR:-/tmp}; fleet leg repos read-only via git show` | Base runner lines 491 (run mode), 1432 (regression), and 1555 (selftest) each call `mktemp -d "${TMPDIR:-/tmp}/…"`. This also satisfies frozen m2's exact requirement: the fleet-runner row must not mention `/tmp` without `TMPDIR`. |

## Other stale numeric pointers in the same sections

The scan covered the mutation-sweep recipe (`SKILL.md:131-245`), “Using the ledger” (`933-964`), and the round-26/round-51 registry area (`2132-2171`). I found these additional stale runner pointers in “Using the ledger”; list only, not fixed:

| SKILL.md base line / pointer | Claim made | Base evidence / issue |
|---|---|---|
| 940 — `tools/mutate-and-run.sh:126-136,1273-1294,1364-1384` | Regression exit map 0/1/2 = PASS/FAIL/SETUP | The explicit comment exit map is at runner `139-140`; actual FAIL/SETUP/PASS emissions and their exits are at `1520-1541`. The cited ranges do not hold the stated complete exit map. |
| 943 — `tools/mutate-and-run.sh:1104-1175` | Git blob materialization and mode/SHA validation | Base materialization and mode handling are at `1275-1303`; the cited range is not that implementation. |
| 944 — shorthand `:1159-1160` | `REGRESSION_PIN` names repo/rev/path/pin | The `REGRESSION_PIN` print is at runner `1302-1303`; the cited range does not name these fields. |
| 948 — shorthand `:1384-1450` | Later legs still run and statuses aggregate | The regression dispatches for legs 8–10 are at `1494-1508`, and aggregation begins at `1510`; `1384-1450` does not cover those later dispatches or their aggregate. |
| 960 — `tools/mutate-and-run.sh:603-629` | Current pins/revisions/tables | Base pins/revisions span `614-633` and verdict tables are `634-643`; the cited range omits the last pin/revision and the verdict tables. |
| 961 — shorthand `:657-839` | First-four specs | The first-four embedded specs are at `673-843`; the cited range ends before the fourth spec finishes (and includes helper code rather than the whole claimed set). |
| 961 — shorthand `:1384-1428` | Nine dispatches | Base runner has ten dispatches; later dispatches appear at `1489-1508`, and `1384-1428` is validation/setup, not the dispatch list. |

The inventory shorthand `:83-108` on line 961 still covers the ten-leg inventory at runner `84-104`; no other stale numeric runner pointer was found in the scanned sections. Round-26 and round-51 registry rows contain runner names but no numeric runner-line pointers.

Commands used for the line-level checks were `git show BASE:SKILL.md`, `git show BASE:tools/mutate-and-run.sh`, and `git show BASE:tools/mte-interop.py`, followed by line-numbered searches for `old-string-count=`, `MUTATE: DEGRADED`, `mktemp`, `REGRESSION_PIN`, and the leg-table declarations. LSP was not available in the exposed toolset; these are direct base-blob text/AST checks, not semantic LSP results.

## Summary
- Proposed exact replacement text for frozen C2 m1a/m1b, m2, and m3a/b/c.
- mte-interop has ten base LEG_TABLE entries; correcting the registry outcome depends on C1's paired row edit.
- Listed seven additional stale runner pointers in the scanned sections; no edits made to lane source.

# ExecCensusBefore — round 44, wave 1

Seat: L1Tameshi44.ExecCensusBefore
Date: 2026-10-25
Item: run sources-census validate on tameshi; report stdout/stderr/exit/E-codes/warnings/row count; save stdout for L1.

## Command

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
```

## Result

- Exit code: 0 (clean; warnings do not change status)
- stderr: empty (0 bytes)
- stdout: 11 TSV lines (captured at /tmp/tameshi-r44-ExecCensusBefore-/census-start.stdout)
- E-codes: none
- Warnings: 9 (W04 x8, W01 x1)
- Implied row count: 114 (`grep -cE '^ {0,3}\| S[0-9]{3} \|' /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md` → 114)

## stdout (verbatim)

1. `tameshi	W04	S047 duplicate url pitest.org/quickstart/incremental_analysis across scopes`
2. `tameshi	W04	S048 duplicate url pitest.org/quickstart/incremental_analysis across scopes`
3. `tameshi	W04	S075 duplicate url man7.org/linux/man-pages/man1/strace.1.html across scopes`
4. `tameshi	W04	S076 duplicate url docs.jj-vcs.dev/latest/git-compatibility across scopes`
5. `tameshi	W04	S077 duplicate url man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html across scopes`
6. `tameshi	W04	S078 duplicate url man7.org/linux/man-pages/man2/open.2.html across scopes`
7. `tameshi	W04	S081 duplicate url bazel.build/reference/test-encyclopedia across scopes`
8. `tameshi	W04	S092 duplicate url bazel.build/remote/caching across scopes`
9. `tameshi	W01	S101 tierC mined used-by=corpus/knowledge/witness-equivalence-rule.md`
10. `tameshi	W04	S104 duplicate url cgit.git.savannah.gnu.org/cgit/bash.git/plain/doc/bashref.texi?id=b8c60bc9ca365f8261fa97900b6fa939f6ebc303 across scopes`
11. `tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md`

## Notes

- The validate verdict line is `tameshi ok …` (row 11), exit 0 → W-codes do not affect clean lanes.
- W04 duplicates are expected for supersede chains (S047/S048, S075, S076, S077, S078, S081, S092, S104 all carry supersedes chains in the registry; same URL across scopes is a warning, not an error).
- W01 S101: tier-C row mined with a non-`—` used-by path — informational.
- No E01–E12 codes; registry parses clean (NF=13).
- stderr was empty; no script-side errors.

## Files

- stdout capture: /tmp/tameshi-r44-ExecCensusBefore-/census-start.stdout (saved for L1)
- stderr capture: /tmp/tameshi-r44-ExecCensusBefore-/census-start.stderr (empty)
- Corpus untouched (read-only validation).

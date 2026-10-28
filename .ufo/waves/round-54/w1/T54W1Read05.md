# T54W1Read05 — cold read of `### Using the ledger` at C0

- heading: `### Using the ledger`
- cand: `59c38109bf119d0e9d4f878644a82babc937bc1e`
- section_sha256: `808dad50760d693bc9e952a32a08cff129a74fd56163876aa3b656f9a9775d04`
- reader-section output:

```
{"heading": "### Using the ledger", "cand": "59c38109bf119d0e9d4f878644a82babc937bc1e", "start": 946, "end": 977, "section_sha256": "808dad50760d693bc9e952a32a08cff129a74fd56163876aa3b656f9a9775d04"}
```

I re-derived the section bytes independently at C0 (`git show 59c38109…:SKILL.md`, lines 946–976 joined with `\n`, trailing blank line stripped per the round-18 sectionize) and got `2733` bytes with sha256 `808dad50760d693bc9e952a32a08cff129a74fd56163876aa3b656f9a9775d04`, matching the printed `section_sha256`. All quotes below occur byte-exact in those section bytes (each verified with `bytes.count(quote) == 1`).

## Findings (3)

### 1. The rule's re-verification anchor names no revision

```
later legs still run and their statuses aggregate (:1247-1317,1459-1517; tool lines re-verified at C** — the ten-leg runner grew since round 26).
```

`C**` is not a git object name (not full, not short-hex, not a tag), so a cold reader cannot resolve the revision at which the rule says its tool lines were re-verified. The two cited spans themselves do resolve at C0: `tools/mutate-and-run.sh:1247-1317` is the `regression_case_git` repo-identity/rev/blob/pin refusal block and `:1459-1517` is the ten dispatch calls plus the status-collection loop. Only the label is broken. The string was introduced by `651773a` (round-53 C5) as `(:1247-1317,1459-1517; tool lines re-verified at C** — the ten-leg runner grew since round 26).` and no later commit repaired it; it is present in the decision bytes above.

### 2. The C0 correction bracket contradicts the round-52 clause it leaves standing

```
the round-52 'no leg records a skipped count' bracket overstated; the ten-leg registry itself enumerates and executes without skips] (round 52: no leg skips — host-gated branches run sandboxed
```

Same sentence, one line: the new bracket says a leg's recorded table *carries* 2 skipped cases ("14 executed + 2 skipped") and that the earlier "no leg records a skipped count" claim was overstated, while the retained round-52 parenthetical still asserts "no leg skips — host-gated branches run sandboxed". The held-open artifact falsifies the retained clause: `corpus/knowledge/mutation-case-kagi-census.md` at C0 says the two trailing verb cases are substrate-gated and that on the measured host `the-janitor` is absent, so the control prints `skip-case 15` / `skip-case 16` (`:28-34`) and the note's own limits section states "(14 executions +2 skips on the recorded host)" (`:269-270`). The pre-C0 text (`git diff 651773ab9e32 59c38109bf11 -- SKILL.md`) read `[round 52: no current leg records a skipped count — enumerated and executed only]`, which was consistent; C0 replaced that bracket and left its contradiction in place.

### 3. The exit-code sentence carries a malformed token

```
Pre-allocation SETUP has no root to retain. Exits0/1/2:
```

The missing space fuses `Exits` with `0/1/2`; the rule that states the exit contract therefore reads as the token `Exits0/1/2` rather than `Exits 0/1/2`, which the following line (`PASS/FAIL/SETUP`) enumerates. The defect is prose-level only — the contract it states is correct against the code (see the sweep below).

## What I opened, and what each check returned

All reads are `git show <rev>:<path>` against the lane's object store at C0 = `59c38109bf119d0e9d4f878644a82babc937bc1e`; no working-tree read was used for the section.

1. `python3 .ufo/waves/round-54/reader-section.py <lane> 59c38109bf11… "### Using the ledger"` (with `TMPDIR` under `/fast/scratch/hyaku/tameshi-r54/T54W1Read05/tmp`) → start 946, end 977, sha `808dad50…`, quoted above.
2. `git show 59c38109…:SKILL.md` → section lines 946–976; re-hashed to `808dad50…`.
3. `tools/mutate-and-run.sh` at C0 (2159 lines), every anchor the section names:
   - `:139-143` — the `--regression` exit map (`0 all cases PASS · 1 … FAIL · 2 … could not be verified`). Resolves.
   - `:1519-1548` — `exit 1` (FAIL, workdir kept), `exit 2` (SETUP, kept), the `case-tally mismatch` SETUP, and `exit 0` (PASS; `rm -rf` only when `auto == 1 && KEEP == 0`). Resolves, including "removed on PASS unless `--keep`, retained on FAIL/SETUP" and "caller workdirs are never removed" (`auto=0` when `--workdir` is given, line 1434–1437).
   - `:1432` — `root=$(mktemp -d "${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX")` after the `command -v python3/sha256sum/mktemp/git` checks; matches the scratch template the section quotes.
   - `die_setup` (`:253-256`) prints `MUTATE: SETUP (…)` and exits 2 with no `REGRESSION_WORKDIR`, so "Pre-allocation SETUP has no root to retain" holds.
   - `:1247-1317` — repo-identity guard, `rev-parse --verify`, `cat-file -e`, `git show`, mode mirror, `REGRESSION_PIN` refusal paths; `:1276` is the `git show "${rev}:${path}"` line the section paraphrases.
   - `:1302-1306` — the `REGRESSION_PIN … source=git repo=%s rev=%s path=%s mode=%s sha256=%s` printf and its file-source `else`; names repo/rev/path/mode/sha256. Resolves.
   - `:78-79` — `MUTATE: DONE|DEGRADED (… defects=… killed=… survived=… inconclusive=…)` and `MUTATE: SETUP`. Resolves.
   - `:614-643` — `PIN_JS` (:614) through `TABLE_DRIFTPINS` (:643), i.e. all ten pins/revisions/tables. Resolves exactly.
   - `:671-849` — `regression_specs()` (:671) through the closing `EOT` of the fourth embedded spec (:849). Resolves exactly as "first-four specs".
   - `:83-108` — the `--regression` header (`r51 ten`) and the ten-leg inventory rows (:88 js-kimi-census … :97 bash-drift-pins) plus their sources. Resolves.
   - `:1459-1508` — the ten `regression_case_git` dispatch calls (js-kimi-census at :1459 … bash-drift-pins suite line at :1508). Resolves.
   - `:1459-1517` in the second bullet — dispatch block through the `for st in …` loop's `done` (:1517). Resolves.
4. Counts cited by the section, checked against the same blob: the inventory header reads `r4-2; r7-1 leg ledger; r10-2 six legs; r16 seven; r18 eight; r26 nine; r51 ten` (:84) and the tally loop declares `nlegs=10` (:1512), so "N=4 at r7-1, 7 since round 16, 8 since round 18, 9 since round 26, 10 since round 51" and "the ten-leg runner" both resolve.
5. Historical anchor "the round-26 tool recorded :603-629": `git show a08e85c:tools/mutate-and-run.sh` (round-26 ninth-leg commit) → `:603 PIN_JS` … `:629 TABLE_CITECHECK`, i.e. pins/revisions/tables at exactly those lines. Resolves.
6. `corpus/knowledge/mutation-case-kagi-census.md` at C0 — :14 pins the same sha256 as `PIN_BASH` (`275d8294…53009f`); :28-34 records `skip-case 15` / `skip-case 16` and `SELFTEST: PASS (16 cases)` with "the hermetic case set here is 14, plus 2 substrate-gated cases"; :269-270 states "(14 executions +2 skips on the recorded host)". This is the artifact behind finding 2.
7. `git diff 651773ab9e3295777a087c033e620ea81b9717b6 59c38109bf119d0e9d4f878644a82babc937bc1e -- SKILL.md` → C0's only change inside this section is the bracket replacement described in finding 2 (the section moved 938–969 → 946–977 because eight lines were added in `## Standing rules` above it).
8. Contract statement "one-edit defects with unique `@old` and `@new != @old`": `tools/mutate-and-run.sh:238-239` documents `count==1 asserted`, :395 rejects a duplicate `@old`, :412 rejects `@new` equal to `@old`. Resolves.

Also checked and found consistent (no finding raised):

- The PASS receipt template `REGRESSION: PASS (cases=N passed=N; …)` matches the printed line at :1540-1541 (`cases=%s passed=%s; ledger legs exact: killed-delta<=0 flips<=0`).
- "Each leg's bytes come from the repo's git object store" — every dispatch passes a repo-relative path, a `PIN_*` and a `REV_*`; mode is mirrored from `ls-tree` (100755 → `chmod +x`), bytes untouched.
- "Host-gated branches must be excluded/controlled or explicitly named" — the three sandboxed suites (`env -i` with `HOME`/`TMPDIR` under the case workdir) are visible at :1491, :1496, :1501, :1506.
- Corpus census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit 0, `tameshi ok …/corpus/SOURCES.md`.

## Provenance and limits

- Nothing in the lane was written except this pair of deliverables under `.ufo/waves/round-54/w1/`; no git/jj mutation was run (only `show`, `log`, `diff`, `rev-parse` reads), no `git add`/commit/fetch/reset.
- Scratch `TMPDIR` was `/fast/scratch/hyaku/tameshi-r54/T54W1Read05/`; the tree is removed on exit.
- No tool was installed or upgraded for this seat (python3, git, bash and the lane's own scripts sufficed), so there is no tool/version/channel entry to record beyond "none".
- Finding 3 is a prose-level defect; findings 1 and 2 are contract-level. I did not edit SKILL.md or any lane file.

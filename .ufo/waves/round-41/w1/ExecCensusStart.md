# ExecCensusStart — sources-census validate on tameshi (round 41, wave 1)

Read-only seat. No file in the lane checkout, fleet repo, sibling lane, jj state or Git index was
modified; no tool was installed or upgraded.

## Command (exact)

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
```

## Exit code

```
EXIT=0
```

0 = clean-or-warnings, per the script contract (`scripts/sources-census.sh:24-27`: "exit 0 clean or
warnings … W-codes and unlisted lanes never change status"). The lane did **not** take the
`[ "$findings" = 1 ]` or `[ "$missing_error" = 1 ]` branches (`scripts/sources-census.sh:805-806`).

## ok line (verbatim)

```
tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
```

The `ok` line is emitted exactly when the lane produced no `E[0-9]+` finding
(`scripts/sources-census.sh:754-756`: `[ "$lane_errors" = 1 ] || emit "$lane	ok	$f"`).

## Findings — 10 W total, 0 E

Verbatim stdout, in emission order:

```
tameshi	W04	S047 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S048 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S075 duplicate url man7.org/linux/man-pages/man1/strace.1.html across scopes
tameshi	W04	S076 duplicate url docs.jj-vcs.dev/latest/git-compatibility across scopes
tameshi	W04	S077 duplicate url man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html across scopes
tameshi	W04	S078 duplicate url man7.org/linux/man-pages/man2/open.2.html across scopes
tameshi	W04	S081 duplicate url bazel.build/reference/test-encyclopedia across scopes
tameshi	W04	S092 duplicate url bazel.build/remote/caching across scopes
tameshi	W01	S101 tierC mined used-by=corpus/knowledge/witness-equivalence-rule.md
tameshi	W04	S104 duplicate url cgit.git.savannah.gnu.org/cgit/bash.git/plain/doc/bashref.texi?id=b8c60bc9ca365f8261fa97900b6fa939f6ebc303 across scopes
tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
```

Counts: **9 × W04, 1 × W01. Zero E codes.**

### E03 / E04: neither appears

- `grep -cE '\tE[0-9]+\t'` over the run output = **0**.
- E03 (duplicate id): independent duplicate-id count over the Registry rows = **0** duplicates
  (`awk … | sort | uniq -d | wc -l` → `0`).
- E04 (duplicate URL within one scope, non-rejected, no `supersedes SNNN`) is not emitted because
  every duplicate-URL group below is split **across scopes**, which is W04 territory
  (`scripts/sources-census.sh:668-674`: E04 requires `scope_key in url_scopes`; W04 fires on
  `u in url_seen && !(scope_key in url_scopes)`).

### The 8 duplicate-URL groups behind the 9 W04 lines

Measured from `corpus/SOURCES.md` with the script's own URL normalisation
(`scripts/sources-census.sh:608-615`):

| normalized url | ids | scopes | supersedes relation |
|---|---|---|---|
| pitest.org/quickstart/incremental_analysis | S041, S047, S048 | F7 / assumptions / item-4 prioritisation | S047 supersedes S041; S048 supersedes S047 |
| man7.org/…/strace.1.html | S060, S075 | S060 `%file`/`-f`/`-o`/`-y` semantics / S075 syscall-filter anchor | S075 supersedes S060 |
| docs.jj-vcs.dev/latest/git-compatibility | S061, S076 | colocated jj/git HEAD / S061 paragraph anchor | S076 supersedes S061 |
| man7.org/…/PR_SET_CHILD_SUBREAPER.2const.html | S068, S077 | S068 reparenting rule / S068 anchor | S077 supersedes S068 |
| man7.org/…/open.2.html | S072, S078 | S072 access modes / S072 teaches | S078 supersedes S072 |
| bazel.build/reference/test-encyclopedia | S028, S081 | S028 shorthand / precise wording | S081 supersedes S028 |
| bazel.build/remote/caching | S059, S092 | S059 false-hit class / S059 anchor | S092 supersedes S059 |
| cgit.git.savannah.gnu.org/…/bashref.texi?id=b8c60bc9… | S097, S104 | S097 exit status / S104 ANSI-C quoting | no `supersedes` token in S104's teaches |

A 3-row group yields 2 W04 emissions and a 2-row group yields 1, which accounts for
7 × 1 + 1 × 2 = 9. All nine are the lane's deliberate anchor-precision supersession pattern; the
last group (S097/S104) is a shared manual file used for two disjoint sections and carries no
`supersedes` token, which is why it would be an E04 if the scopes ever collapsed to one.

### W01 detail

`S101` (`corpus/SOURCES.md:109`) is tier `C`, status `mined`, and carries a used-by path rather than
`—`, so W01 fires. The cited path resolves:
`corpus/knowledge/witness-equivalence-rule.md` exists (5,018 bytes) — hence no E11, whose absence
confirms the used-by integrity check passed for every mined row.

## Cross-checks against the contract's known facts

- Registry rows = **107** (`awk` over `## Registry`; and `census` prints `tameshi	rows	107`,
  `FLEET	rows	107`) — matches the stated 107.
- Statuses: `status.mined 79`, `status.queued 22`, `status.rejected 6` — matches 79/22/6.
- Tiers: A 95, B 9, C 3, invalid 0.
- Highest id **S152** (`sort | tail`), matching the known fact.
- `FLEET	missing	0`.

## Control: the validator itself is not silently passing

```
./scripts/sources-census.sh selftest   → exit 0
96 × "killed", 0 × "SURVIVED"
```

So the same binary that reports `ok` here does emit E01–E12/W01–W04 on the planted fixtures and
fails closed on missing registries; the exit-0 result above is a real clean-or-warning verdict, not
a silent no-op. (`selftest ok` is the final line; exact exit captured as `SELFTEST_EXIT=0`.)

## Answer

- Exit code: **0**.
- ok line: `tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md`.
- Every finding: the 9 × W04 and 1 × W01 lines quoted above.
- E03/E04: **absent** (no E code of any class appears; duplicate ids measured 0 and every
  duplicate URL sits across scopes, not within one).

## Residual risk / blockers

- None blocking. Only caveat: W04 volume (9 of 107 rows, i.e. 8 supersession chains) is a
  registry-hygiene signal, not a defect the counter treats as failure; it will keep any "zero
  findings" expectation on this lane false even when C1 is satisfied.

Report: .ufo/waves/round-41/w1/ExecCensusStart.md

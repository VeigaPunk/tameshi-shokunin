# Round 36 W2 — census enum mutation probe (S103)

**Axis:** calibration. **Role:** mutation tester, leaf seat (no subagent dispatch).

**Attack:** the source-census validator's enum teeth on the S103 row of
`corpus/SOURCES.md` — status and kind columns. Fixture: a scratch clone of the
lane at the dispatch tip, run only through the fleet validator (read-only).

## Setup (all scratch paths under `/fast/scratch/hyaku/tameshi-r36-seats/W2MTCensus/`)

```sh
S=/fast/scratch/hyaku/tameshi-r36-seats/W2MTCensus
git clone --no-hardlinks -q /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  $S/root/tameshi-shokunin
git -C $S/root/tameshi-shokunin rev-parse HEAD
# fbb01cf46f8437fd1264c1a3acc053c882fa2164
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-parse fbb01cf:corpus/SOURCES.md
# e67cbf030609373f899b73f88f7ffd7fece47226
cp -p $S/root/tameshi-shokunin/corpus/SOURCES.md $S/pristine/SOURCES.md
sha256sum $S/pristine/SOURCES.md
# 16fae0a17acc934ceab8ffd177e73604bc5cbe62f7b354ce9650f0f77986cbd7
```

Scratch fleet root `$S/root/shokunin.conf` carries one row
`tameshi|tameshi-shokunin|scratch clone for census enum mutants`, so the
validator resolves exactly the same lane id (`tameshi`) as the wave census but
against the scratch clone. `corpus/SOURCES.md` at `fbb01cf` is byte-identical
to the refresh commit's copy (`git diff --stat b455001e..HEAD -- corpus/SOURCES.md`
empty; the spot-check touched neither registry nor counters).

Validator: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`,
sha256 `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`
(read-only, never edited). Environment: `TZ=UTC`, GNU bash 5.3.20(1),
GNU Awk 5.4.1, date 2026-10-24.

Enum source (validator gawk pass, lines 654–659):

```awk
if (kind !~ /^(spec|docs|paper|code|tool|dataset|talk|book|community|own-work)$/)
  printf "%s\tE05\t%s kind=%s\n",lane,id,kind
if (status !~ /^(queued|mined|rejected)$/)
  printf "%s\tE07\t%s status=%s\n",lane,id,status
```

## Baseline detector on pristine bytes

```sh
TZ=UTC bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh \
  validate --root $S/root tameshi > $S/baseline.out 2> $S/baseline.err
```

Exit `0`; 10 stdout lines: eight pre-existing `W04` duplicate-URL warnings,
one pre-existing `W01` (`S101 tierC mined`) warning, and the final clean line:

```text
tameshi	ok	/fast/scratch/hyaku/tameshi-r36-seats/W2MTCensus/root/tameshi-shokunin/corpus/SOURCES.md
```

Warnings do not fail validation (validator contract, line 27 of the header).
Registry row count in the clone: 100 (`grep -cE '^\| S[0-9]{3} \|'`).

## Mutant A — S103 status `mined` → `garbage-status` (one cell, NF stays 13)

Single-cell edit on the pristine row only; the row still has 12 cells / NF=13,
so E07 is the only candidate finding.

Post-edit hash:
`afcce790a4318c56a60b0aee90a2c597c478f89b8c06b696dccd3967812939dd`

```sh
TZ=UTC bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh \
  validate --root $S/root tameshi > $S/mutant-status.out 2> $S/mutant-status.err
echo "RC=$?"
```

Actual output (stderr empty):

```text
RC=1
tameshi	W04	S047 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S048 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S075 duplicate url man7.org/linux/man-pages/man1/strace.1.html across scopes
tameshi	W04	S076 duplicate url docs.jj-vcs.dev/latest/git-compatibility across scopes
tameshi	W04	S077 duplicate url man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html across scopes
tameshi	W04	S078 duplicate url man7.org/linux/man-pages/man2/open.2.html across scopes
tameshi	W04	S081 duplicate url bazel.build/reference/test-encyclopedia across scopes
tameshi	W04	S092 duplicate url bazel.build/remote/caching across scopes
tameshi	W01	S101 tierC mined used-by=corpus/knowledge/witness-equivalence-rule.md
tameshi	E07	S103 status=garbage-status
```

The `ok` line is gone; the added finding is exactly the status-enum-violation
line. **KILLED.**

## Mutant B — S103 kind `docs` → `flarn` (one cell, NF stays 13)

Pristine bytes restored by `cp -p` before this mutant; index-checked identical
(`cmp`). Edit on S103's third cell only.

Post-edit hash:
`d5bf41936a6da4e9e1515b52b8d13c8c01d4be74335c81b12689b3aa0feb5f3e`

```sh
TZ=UTC bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh \
  validate --root $S/root tameshi > $S/mutant-kind.out 2> $S/mutant-kind.err
echo "RC=$?"
```

Actual output (stderr empty):

```text
RC=1
tameshi	W04	S047 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S048 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S075 duplicate url man7.org/linux/man-pages/man1/strace.1.html across scopes
tameshi	W04	S076 duplicate url docs.jj-vcs.dev/latest/git-compatibility across scopes
tameshi	W04	S077 duplicate url man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html across scopes
tameshi	W04	S078 duplicate url man7.org/linux/man-pages/man2/open.2.html across scopes
tameshi	W04	S081 duplicate url bazel.build/reference/test-encyclopedia across scopes
tameshi	W04	S092 duplicate url bazel.build/remote/caching across scopes
tameshi	W01	S101 tierC mined used-by=corpus/knowledge/witness-equivalence-rule.md
tameshi	E05	S103 kind=flarn
```

**KILLED.** No `E01` (malformed row) and no `E04` side effects: the failure is
the enum check alone, not a column-count accident.

## Restoration evidence

```sh
cp -p $S/pristine/SOURCES.md $S/root/tameshi-shokunin/corpus/SOURCES.md
sha256sum $S/root/tameshi-shokunin/corpus/SOURCES.md
# 16fae0a17acc934ceab8ffd177e73604bc5cbe62f7b354ce9650f0f77986cbd7
cmp -s $S/pristine/SOURCES.md $S/root/tameshi-shokunin/corpus/SOURCES.md && echo BYTES-IDENTICAL-TO-PRISTINE
# BYTES-IDENTICAL-TO-PRISTINE
TZ=UTC bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh \
  validate --root $S/root tameshi > $S/restored.out 2> $S/restored.err
# RESTORED-RC=0; final line: tameshi	ok	…/root/tameshi-shokunin/corpus/SOURCES.md; 10 lines
```

Hash trail: pristine `16fae0a1…` → status mutant `afcce790…` → restored
`16fae0a1…` → kind mutant `d5bf4193…` → restored `16fae0a1…` (exact bytes).

Raw evidence retained at:
`/fast/scratch/hyaku/tameshi-r36-seats/W2MTCensus/{baseline,mutant-status,mutant-kind,restored}.{out,err}`
and `pristine/SOURCES.md`. The scratch clone's `.git` was never written; the
fleet validator is read-only.

## Verdict

**PASS — both assigned mutants KILLED.** The census validator rejects an
unknown S103 status (`E07 status=garbage-status`, exit 1) and an unknown S103
kind (`E05 kind=flarn`, exit 1) on a scratch lane clone, while the pristine
registry validates clean at exit 0 with the same warning set; the mutated bytes
were restored exactly (`16fae0a1…`, `cmp` identical, re-run exit 0). The E05/E07
predicates are real teeth for the S103 row, not vacuous. No tool installs; no
writes outside scratch and this report.

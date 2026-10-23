# Round 33 wave 1 — start census

## Verdict

The round-start census completed. `sources-census.sh validate` exited 0 and printed eight `W04` duplicate-URL-across-scopes warnings followed by `ok` for the tameshi registry. All seven frozen manual census commands exited 0; the structural checks found no malformed rows, duplicate IDs, enum violations, or missing mined `used-by` paths. This is a start snapshot only, not an end-of-round comparison.

## Evidence

The frozen manual census definitions are at `CORPUS.md:131-147`; the target registry begins at `tameshi-shokunin/corpus/SOURCES.md:1-11`. Validator warning rows are `tameshi-shokunin/corpus/SOURCES.md:56-57,84-87,90,101`.

Commands ran from `/fast/scratch/hyaku/tameshi-r33-seats/CensusStart/`. Each command's stdout/stderr and exit status were captured there; below are the exact invoked commands, observed stdout, and captured exit codes. The source-file operands are absolute because the assigned working directory is the seat scratch directory.

### Validator

```sh
TZ=UTC bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi > validate.stdout 2> validate.stderr; echo $? > validate.exit
```

Captured stdout (`validate.stdout`):
```text
tameshi	W04	S047 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S048 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S075 duplicate url man7.org/linux/man-pages/man1/strace.1.html across scopes
tameshi	W04	S076 duplicate url docs.jj-vcs.dev/latest/git-compatibility across scopes
tameshi	W04	S077 duplicate url man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html across scopes
tameshi	W04	S078 duplicate url man7.org/linux/man-pages/man2/open.2.html across scopes
tameshi	W04	S081 duplicate url bazel.build/reference/test-encyclopedia across scopes
tameshi	W04	S092 duplicate url bazel.build/remote/caching across scopes
tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
```

Captured exit (`validate.exit`): `0`.

### Seven frozen manual census commands

1. Rows (`CORPUS.md:134-135`)

```sh
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md > rows.stdout 2> rows.stderr; echo $? > rows.exit
```

stdout: `96`; exit: `0`.

2. Malformed rows (`CORPUS.md:136-137`)

```sh
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md > malformed.stdout 2> malformed.stderr; echo $? > malformed.exit
```

stdout: `0`; exit: `0`.

3. Tier histogram (`CORPUS.md:138-139`)

```sh
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {t=$5; gsub(/[[:space:]]/,"",t); n[t]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md > tiers.stdout 2> tiers.stderr; echo $? > tiers.exit
```

stdout: `A=87 B=7 C=2 `; exit: `0`.

4. Status histogram (`CORPUS.md:140-141`)

```sh
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md > statuses.stdout 2> statuses.stderr; echo $? > statuses.exit
```

stdout: `mined=68 queued=22 rejected=6 `; exit: `0`.

5. Duplicate IDs (`CORPUS.md:142-143`)

```sh
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md | sort | uniq -d > duplicates.stdout 2> duplicates.stderr; echo $? > duplicates.exit
```

stdout: empty; exit: `0`.

6. Enum violations and tier inflation (`CORPUS.md:144-145`)

```sh
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {i=$2;k=$4;t=$5;s=$9; gsub(/[[:space:]]/,"",i); gsub(/[[:space:]]/,"",k); gsub(/[[:space:]]/,"",t); gsub(/[[:space:]]/,"",s); if (t !~ /^[ABC]$/) print "tier", i, t; if (s !~ /^(queued|mined|rejected)$/) print "status", i, s; if (k !~ /^(spec|docs|paper|code|tool|dataset|talk|book|community|own-work)$/) print "kind", i, k; if (t=="A" && k=="community") print "tier-inflation", i}' /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md > enums.stdout 2> enums.stderr; echo $? > enums.exit
```

stdout: empty; exit: `0`.

7. Mined `used-by` path existence (`CORPUS.md:146-147`)

```sh
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {s=$9; gsub(/[[:space:]]/,"",s); if (s=="mined") {n=split($12, a, /[,;]/); for (j=1;j<=n;j++) {p=a[j]; gsub(/^[[:space:]]+|[[:space:]]+$/,"",p); if (p!="" && p!="—") print p}}}' /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md | while read -r p; do [ -e "/home/vgpnk/Projects/shokunin/tameshi-shokunin/$p" ] || echo "missing: $p"; done > mined-paths.stdout 2> mined-paths.stderr; echo $? > mined-paths.exit
```

stdout: empty; exit: `0`.

## Smallest safe correction

No corpus correction was made. The eight validator messages are warnings about URLs reused across distinct scopes; the validator exited 0, and none of the seven frozen manual checks reported a violation. Preserve these start values for the L1's end-of-round rerun and comparison.

## Touched surfaces, out of scope, and limits

- Written: this report only. `corpus/SOURCES.md` and the validator were read/run, not edited.
- Out of scope: C1/C2 counter runs, tool changes, source-row edits, and end-of-round census/comparison.
- Limit: this is a point-in-time round-start receipt; it makes no claim about subsequent source changes or freshness beyond the captured census.
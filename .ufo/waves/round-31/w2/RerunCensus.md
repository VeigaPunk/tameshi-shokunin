# RerunCensus — SOURCES census at 2da841bd9913a2037d2bf612793382e572c9d205 (round 31, wave 2)

Seat: RerunCensus. Working dir: /fast/scratch/hyaku/tameshi-r31-seats/RerunCensus/.
Mirror of the lane: /fast/scratch/hyaku/tameshi-r31-seats/RerunCensus/m (content revision) and
/fast/scratch/hyaku/tameshi-r31-seats/RerunCensus/mbase (base revision). No production file was touched.

## Verdict

PASS on every sub-claim of the item.

1. `sources-census.sh validate --root $W2 tameshi` at 2da841bd prints `tameshi ok` with eight W04
   warnings and exits 0; the same command at base 36c1d393 prints the identical row set and exits 0.
2. The `corpus/SOURCES.md` diff between the two revisions is exactly three hunks: the S055 `used-by`
   cell changed in place, rows S095 and S096 inserted directly after S094, and an eleven-line note
   block plus one `Next unused id` line appended at end of file.
3. Every `used-by` path of every `mined` row resolves to a regular file at 2da841bd: 47 distinct
   paths over 107 token instances, zero missing; the census validator itself reports no E11.
4. `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` in the clone prints `94` rows at the
   content revision (base prints `92`), and its verdict is CLEAN for contract v1 plus H4 id-or-path.

No correction is needed.

## Evidence

### Census at the content revision

```
$ W2=/fast/scratch/hyaku/tameshi-r31-seats/RerunCensus/m
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root $W2 tameshi
tameshi	W04	S047 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S048 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S075 duplicate url man7.org/linux/man-pages/man1/strace.1.html across scopes
tameshi	W04	S076 duplicate url docs.jj-vcs.dev/latest/git-compatibility across scopes
tameshi	W04	S077 duplicate url man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html across scopes
tameshi	W04	S078 duplicate url man7.org/linux/man-pages/man2/open.2.html across scopes
tameshi	W04	S081 duplicate url bazel.build/reference/test-encyclopedia across scopes
tameshi	W04	S092 duplicate url bazel.build/remote/caching across scopes
tameshi	ok	/fast/scratch/hyaku/tameshi-r31-seats/RerunCensus/m/tameshi-shokunin/corpus/SOURCES.md
RC=0
```

Base revision, same command with `--root /fast/scratch/hyaku/tameshi-r31-seats/RerunCensus/mbase`:
the same eight W04 lines, then `tameshi ok .../mbase/tameshi-shokunin/corpus/SOURCES.md`, `RC=0`.
Diffing the two outputs with the root path rewritten (`sed 's#/.*/corpus#/ROOT/corpus#'`) leaves only
the root token different, so the finding set is byte-identical across the two revisions.

Census mode totals (`sources-census.sh census --root <root> tameshi`):

| metric | base 36c1d39 | 2da841bd |
|---|---|---|
| rows | 92 | 94 |
| tier.A / tier.B / tier.C | 83 / 7 / 2 | 85 / 7 / 2 |
| status.mined / queued / rejected | 64 / 22 / 6 | 66 / 22 / 6 |
| FLEET.missing | 0 | 0 |
| exit | 0 | 0 |

The two added rows account for the deltas exactly: +2 rows, +2 tier A, +2 mined.

### Diff of corpus/SOURCES.md, base to content revision

`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff -U0 36c1d393 2da841bd -- corpus/SOURCES.md`
(full text kept at /fast/scratch/hyaku/tameshi-r31-seats/RerunCensus/sources-diff.txt) has three
hunks only:

```
@@ -64 +64 @@
+| S055 | doctest — Test interactive Python examples — https://docs.python.org/3/libra...
@@ -103,0 +104,2 @@
+| S095 | Testable Examples in Go (Andrew Gerrand) — https://go.dev/blog/examples | docs...
+| S096 | Documentation tests (The rustdoc book) — https://doc.rust-lang.org/rustdoc/wri...
@@ -364,0 +367,11 @@
+
+Round 31: S055 re-opened (Python doctest page, fetched 2026-10-23, 216574 bytes, sha256
+369dcc17009a2f36000284ca86eedb7cef4bc10f773e554754bbdad07791cc46, seat SrcDoctest; the
+module-introduction bullet still reads as quoted in the round-31 lesson Gate); `used-by`
+corpus/lessons/round-16.md → that path plus corpus/knowledge/executable-self-assessment
+status, opened and recheck unchanged. A draft new row for the same page was not added (it
+duplicate S055's URL). New rows S095 (Go testable examples) and S096 (rustdoc documentati
+tests), both mined by that entry. Rows 92 → 94. The `- Next unused id: S092.` line abov
+already stale when round 30 appended its note (S092–S094 were used in round 30); it sta
+append-only, and the S095 line after it is superseded here.
+- Next unused id: S097.
```

(Lines above are cut at 90 characters for readability; the full text is in the saved diff.)

S055 cell check. Splitting the row on `|` and numbering the cells at both revisions gives 13 cells
each time, and `diff -u` over the numbered cells reports exactly one changed cell:

```
@@ -9,5 +9,5 @@
     10	on-release
-    11	corpus/lessons/round-16.md
+    11	corpus/lessons/round-16.md, corpus/knowledge/executable-self-assessment.md
```

Cell 11 is the `used-by` column; the id, source, kind, tier, scope, anchor, teaches, status,
opened and recheck cells are unchanged. No other S055 field moved.

Insertion point. Rows occupy these lines at 2da841bd (grep -n):

```
103:| S094 | Preserving Statistical Validity in Adaptive Dat...
104:| S095 | Testable Examples in Go (Andrew Gerrand) — ht...
105:| S096 | Documentation tests (The rustdoc book) — http...
```

S095 and S096 sit immediately after S094 and before the blank line that closes the registry table;
the hunk header `@@ -103,0 +104,2 @@` shows they were inserted, not substituted. Both rows are
well formed: `awk -F'|' '/^\| S09[56] /{print $2, NF}'` prints `S095 13` and `S096 13`, matching the
13-field contract. Neither row repeats an existing URL (no new W04 entry appeared), which confirms
the note's statement that a second doctest row was not added.

Appended block. The file grows from 364 to 377 lines; the last hunk is pure addition (`@@ -364,0
+367,11 @@`), eleven lines, located under the `## Id allocation` heading (headings at 1 `# SOURCES`,
8 `## Registry`, 109 `## Paths`, 115 `## Search log`, 229 `## Leads (unopened)`, 251 `## Id
allocation`), so the note is outside the registry table and adds no row-shaped source. The
validator's E12 check stays silent, which is the corroborating machine check.

Note that the append leaves an earlier `- Next unused id: S095.` line in place at line 366; the
appended block names that situation and ends with `- Next unused id: S097.`, the last such line in
the file. The file therefore contains many historical `Next unused id` lines by design (round-18
QUALITY 35, quoted by the note); the final one, S097, is correct because S096 is the highest id.

### Mined used-by paths at the content revision

From the clone root (so the registry's relative paths resolve):

```
$ awk -F'|' '/^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|/ { ... if (s=="mined") split used-by ...}' corpus/SOURCES.md | sort > mined-tokens.txt
$ wc -l < mined-tokens.txt          -> 107     (token instances)
$ sort -u mined-tokens.txt | wc -l  -> 47      (distinct paths)
$ sort -u mined-tokens.txt | while read -r p; do [ -f "$p" ] || echo "NOT-REGULAR $p"; done
DONE
```

No `NOT-REGULAR` line, no missing path: all 47 distinct files exist as regular files at
2da841bd, including the S055 and S095/S096 targets `corpus/lessons/round-16.md` and
`corpus/knowledge/executable-self-assessment.md` (6313 bytes, present). The independent
`sources-census.sh validate` run, which implements the same check as E11, reports zero E-codes
(`... | grep -cE '\tE[0-9]{2}\t'` prints `0`; grep exits 1 because the count is zero).

### kaika sources-census-v2.sh row count

Run from the clone root, output saved at /fast/scratch/hyaku/tameshi-r31-seats/RerunCensus/kaika-v2.out:

```
$ bash .ufo/evidence/kaika-round-1/sources-census-v2.sh
== A rows
94
== A malformed (must be 0)
0
== A tiers
A=85 B=7 C=2
== A status
mined=66 queued=22 rejected=6
== A dup ids (must print nothing)
== A enum/tier-inflation (must print nothing)
== A mined used-by missing (must print nothing)
== B1 strict id-cite (informational)
... count=25
== B2 id-or-path cite (must print nothing)
== VERDICT
SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)
RC=0
```

Row count: 94. At base the same script prints `92` rows, `A=83 B=7 C=2`, `mined=64 queued=22
rejected=6`, and the same CLEAN verdict. The script's own count agrees with the
`sources-census.sh` `rows` metric at both revisions, and the base-to-revision delta of 2 matches
the two inserted rows. The informational B1 section lists 25 rows whose used-by file does not
contain the row id; that is the pre-existing H4 strict-cite backlog, it is not part of contract v1,
and it is unchanged in kind by this diff (the two new rows cite through
`corpus/knowledge/executable-self-assessment.md`, which the B2 check accepts).

## Behaviour summary

At 2da841bd the tameshi registry is 94 rows, 85 tier A, 7 tier B, 2 tier C, with 66 mined, 22
queued and 6 rejected. It validates clean under contract v1, with the same eight duplicate-URL
warnings the base revision already carried. The round-31 change to `corpus/SOURCES.md` is
non-structural: one cell edit on S055, two appended-table rows, one appended note block, and one
appended id-allocation line.

Small anomalies worth recording, none of them defects in the measured claim:

- The file carries many `Next unused id` lines and the newest one sits eleven lines after the
  previous one. This is the documented append-only convention; the note states it explicitly, and
  the last line is the correct S097.
- The appended note cites a fetched byte count and sha256 for the Python doctest page. Those are
  fetch-time claims about a remote page and were not re-verified here; this item covers registry
  structure and census output, not source currency.

## Smallest safe correction

None. Every sub-claim of the item holds as written, so any edit would be scope widening.

## Housekeeping

- Nothing installed or upgraded.
- No process trees started beyond short-lived commands; nothing to kill.
- No git write command was issued in the lane or the fleet root; the only writes were to the two
  scratch mirrors, the scratch files listed above, and this report.
- Scratch kept: /fast/scratch/hyaku/tameshi-r31-seats/RerunCensus/ (sources-diff.txt,
  kaika-v2.out, kaika-v2-base.out, kaika-v2.err, valid-base.txt, valid-rev.txt,
  s055-base.cols, s055-rev.cols, mined-paths.txt, mined-tokens.txt, and the two mirrors m/ and
  mbase/).

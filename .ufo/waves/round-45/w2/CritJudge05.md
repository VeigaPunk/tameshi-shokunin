seat: CritJudge05

# Round-45 w2 — C1 falsify re-judgment: S002, S077, S097

Reviewed inputs at commit `ad5942c6e9858af19d00000b58439b321ddfa62b` (ledger unchanged since
`3bf8bcd`; `git diff --stat ad5942c -- .ufo/evidence/round-45/freshness/ledger.json` empty):
`.ufo/evidence/round-45/freshness/ledger.json` (73 entries, one per id), the committed
snapshots `.ufo/evidence/round-45/freshness/sources/S{002,077,097}.raw.gz`, the registry rows
in `corpus/SOURCES.md:13,86,106`, and the authors' reports
`.ufo/waves/round-45/w1/{ExecRows01,ExecRows11,ExecRows18}.md`. I am not an author of any of
these entries (authors: ExecRows01, ExecRows11, ExecRows18).

## Verdicts

S002 agree — reviewer CritJudge05 — live fetch today sha256 404575e9… equals entry raw_sha256 and committed snapshot, quote occurs once at schema lines 88-93 inside the row's anchor 64-98, and the 8-value MutantStatus enum it states plus killedBy(64)/statusReason(94)/testsCompleted(98) in the same MutantResult properties block still ground the teaches.
S077 agree — reviewer CritJudge05 — live fetch today sha256 b805fe23… equals entry raw_sha256 and committed snapshot, quote occurs once at the start of DESCRIPTION ¶2 in the raw `<pre>` block (¶1 is "If set is nonzero…") with the reparenting sentence in that same paragraph, so both the anchor-placement claim and "the teaches of S068 is unchanged" hold.
S097 agree — reviewer CritJudge05 — live cgit fetch today is 415804 bytes sha256 f3d37d57… equals entry, snapshot and the row's own recorded sha, quote occurs once at texi lines 3896-3898 inside the `@node Exit Status` anchor 3890-3916, and the teaches' other clauses (128+N 3911-3912, 127 3914-3915, 126 3916; `case` first-match 1056-1058 and 1081-1082 inside the 1044-1084 anchor) are present in the same snapshot.

## sha256 comparison (provenance)

```
$ curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o /tmp/tameshi-r45-CritJudge05/S###.live '<row url>'   # rc=0 for all three
$ sha256sum *.live
404575e9264686dbf85c399f6531fdb489bebc3146e7e1d793b8083bc6a041ae  S002.live   (12799 bytes)
b805fe23c7251ad6c3d08a829ed755b80a8fa106929c67325c7122f3b126ef2c  S077.live   (9879 bytes)
f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5  S097.live   (415804 bytes)
$ gunzip -c .ufo/evidence/round-45/freshness/sources/S###.raw.gz | sha256sum
404575e9264686dbf85c399f6531fdb489bebc3146e7e1d793b8083bc6a041ae  -   (S002)
b805fe23c7251ad6c3d08a829ed755b80a8fa106929c67325c7122f3b126ef2c  -   (S077)
f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5  -   (S097)
$ git show ad5942c:.ufo/evidence/round-45/freshness/sources/S###.raw.gz | gunzip -c | sha256sum
(same three digests)
```

Live == entry.raw_sha256 == committed snapshot at ad5942c, for all three rows: provenance
confirmed, no dynamic chrome difference, so the `--extract` fallback was not needed. gzip
headers carry mtime 0 (`gzip -n`), so byte equality with today's live fetch is the evidence of
freshness, not a stored timestamp.

Entry/registry URL identity: each entry names the first http(s) URL of its row's source cell
exactly (S002 raw.githubusercontent …, S077 man7.org/…/PR_SET_CHILD_SUBREAPER.2const.html,
S097 cgit.git.savannah.gnu.org/…/bashref.texi?id=b8c60bc9…; the rendered gnu.org page in
S097's source cell is the second URL and is not the one claimed). Each entry has
`opened: 2026-10-25`, `verdict: holds`, no `member`.

## Located context (normalized snapshot text, `measure.py --extract`)

S002 (`S002.snap` raw lines 88-93, anchor 64-98) — quote occurs exactly once:

```
"static": { … },  [["status": { "type": "string", "title": "MutantStatus", "description":
"Result of the mutation.", "enum": ["Killed", "Survived", "NoCoverage", "CompileError",
"RuntimeError", "Timeout", "Ignored", "Pending"] }]]  , "statusReason": { "type": "string",
"description": "The reason that this mutant has this status. …
```

8 enum values counted; `killedBy` line 64, `statusReason` line 94, `testsCompleted` line 98,
`coveredBy` line 43 — all inside the same `MutantResult` properties object. Body content (a
property definition that states the enum), not nav/footer/table chrome.

S077 (`S077.snap` lines 81-89) — quote occurs exactly once; raw HTML shows a `<pre>` block
with blank-line-separated paragraphs:

```
DESCRIPTION top If set is nonzero, set the "child subreaper" attribute of the calling
process; if set is zero, unset the attribute.  [[A subreaper fulfills the role of init(1) for
its descendant processes.]]  When a process becomes orphaned (i.e., its immediate parent
terminates), then that process will be reparented to the nearest still living ancestor
subreaper. …
```

The reparenting sentence is in the same ¶2 that begins "A subreaper fulfills", so S068's old
anchor ("§DESCRIPTION, first paragraph after the SYNOPSIS", which is the "If set is nonzero"
paragraph) is genuinely superseded and S068's teaches is still stated in the live bytes.
Version footer still `man-pages 6.19` / `2026-02-08` (`6.19` ×2, `2026-02-08` ×1, `6.20` ×0).

S097 (`S097.snap` lines 3890-3916) — quote occurs exactly once at 3896-3898:

```
@node Exit Status … The exit status of an executed command is the value returned by the
@code{waitpid} system call or equivalent function.  [[Exit statuses fall between 0 and 255,
though, as explained below, the shell may use values above 125 specially.]]  Exit statuses
from shell builtins and compound commands are also limited to this range. …
```

texi body of the Exit Status node, inside the stated anchor. The teaches' second half is also
present in this snapshot: `@item case` 1044-1084, "the first @var{pattern} that matches"
1056-1058, "The first pattern that matches determines the command-list that is executed"
1081-1082. The quote itself states the range clause verbatim and is not truncated mid-claim;
the special-status detail (126/127/128+N) sits at 3911-3916, in the same anchor.

## Quote freshness / non-copying

Each quote was searched in `corpus/SOURCES.md` against its own row: no six-word run of any of
the three quotes occurs in the row's cells (`quote_in_row=False` for all three), so none is
copied from the row's source/scope/anchor/teaches cells. Token counts 21 / 11 / 19, all inside
the 6-25 bound. Corroboration with the frozen counter (seat mode only):

```
$ python3 .ufo/evidence/round-45/freshness/measure.py --lane <lane> --rev 3310e7be803516ca5934b4e949d91bcec824b179 --check S###.frag.json
CHECK S002 verified ok   (rc=0)
CHECK S077 verified ok   (rc=0)
CHECK S097 verified ok   (rc=0)
```

The counter is corroboration only; the verdicts above rest on my own fetch, hash, extraction and
context reading.

## Non-blocking observations (no verdict change)

1. S068 and S077 share one URL and byte-identical snapshots (`b805fe23…`). They are distinct
   registry rows with distinct quotes (S068: "When a process becomes orphaned …"; S077: "A
   subreaper fulfills …"), and C1's population is rows, so this is not double counting of a
   document under the frozen predicate — but the two rows contribute one distinct document to
   the 50-row target.
2. S002's anchor range 64-98 covers killedBy→testsCompleted, while `coveredBy` (named by the
   teaches) sits at line 43, earlier in the same `MutantResult` properties object. The teaches
   claim is true of the snapshot; only the anchor's line range is one property narrower than
   the teaches' list. The quote itself lies inside 64-98.
3. S077's teaches cell is meta ("supersedes S068's anchor only"); its substantive claim is
   S068's teaches, which I verified in the same snapshot rather than taking the cell at face
   value.

## Files / tooling

- reviews.json: `/tmp/tameshi-r45-CritJudge05/reviews.json` (3 agree verdicts, report path
  `.ufo/waves/round-45/w2/CritJudge05.md`).
- Scratch: `/tmp/tameshi-r45-CritJudge05/` (`.live`, `.snap`, `.txt`, `.frag.json`).
- No tools installed or upgraded (curl + python3 already present; pacman untouched); no writes
  in the lane except this report, no git/jj mutating command.

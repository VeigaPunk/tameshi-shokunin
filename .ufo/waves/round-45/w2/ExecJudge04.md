seat: ExecJudge04

# Round-45 w2 — C1 falsify review of S060, S061, S153

Independent re-judgment of three wave-1 C1 ledger entries. I am not the author of any of them (authors: ExecRows08 / ExecRows09 /
ExecRows23). Inputs: `.ufo/evidence/round-45/contract.json` (read, not edited), the ledger at commit
ad5942c6e9858af19d00000b58439b321ddfa62b, the committed snapshots under `.ufo/evidence/round-45/freshness/sources/`, the registry
rows in `corpus/SOURCES.md:69,70,123`, and the author reports `.ufo/waves/round-45/w1/ExecRows08.md`, `ExecRows09.md`,
`ExecRows23.md`. Every fetch below is mine, run 2026-10-25 from `/tmp/tameshi-r45-ExecJudge04/`, against each row's own URL.

## Verdicts

S060 agree — reviewer ExecJudge04 — sha equal (today's live fetch, the entry's `raw_sha256` and the gunzipped snapshot are all `eedefecf…`), the 12-token quote is the `%file` qualifier definition inside the section "Filtering -e trace = syscall_set" (the row's own anchor, `corpus/SOURCES.md:69`), immediately followed by "an abbreviation for --trace = open , stat , chmod , unlink ,... which is useful to seeing what files the process is referencing", so it supports the teaches claim that an open trace records files opened by name.
S061 agree — reviewer ExecJudge04 — sha equal (`db9c9a76…`), the 12-token quote is the `jj new && jj undo` step comment in "Converting a workspace into a colocated workspace" (the recipe comment the row's anchor names, `corpus/SOURCES.md:70`), stating that jj updates `.git/HEAD` to point to the working-copy commit's parent, and paragraph 2 of the preceding "Colocated Jujutsu/Git workspaces" section in the same snapshot adds the "detached HEAD" wording, so the teaches claim that `git rev-parse HEAD` is not the bookmark tip is supported.
S153 agree — reviewer ExecJudge04 — sha equal (`f4c18b31…`), the 10-token quote is the first description sentence of `ast.get_source_segment` in the ast module reference (the row's own anchor `§ast.get_source_segment`, `corpus/SOURCES.md:123`), followed by the `padded` / "return None" clauses, which supports the teaches source-recovery claim.

No dispute on any of the three.

## sha256 comparison lines

```
$ curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o S060.live 'https://man7.org/linux/man-pages/man1/strace.1.html'   # exit 0
$ curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o S061.live 'https://docs.jj-vcs.dev/latest/git-compatibility/'      # exit 0
$ curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o S153.live 'https://docs.python.org/3/library/ast.html'            # exit 0

S060 live==entry.raw_sha256==gunzip(snapshot)==git-blob@ad5942c : eedefecf7c55cf36976fce6fbfff8b1340c62b696bb7268a83df643ee8ea02f6  (equal, 85238 B)
S061 live==entry.raw_sha256==gunzip(snapshot)==git-blob@ad5942c : db9c9a760810386858e6b1bad4a7a334c56bd48c77692dbc1c343657ae0ca254  (equal, 61334 B)
S153 live==entry.raw_sha256==gunzip(snapshot)==git-blob@ad5942c : f4c18b31aea745258ff49b4227fca6e916a528dfb5ef77da4f3fa89323346b82  (equal, 362029 B)
```

All three are byte-identical to today's live fetch, so provenance is confirmed and the dynamic-chrome fallback branch never had to
fire; no entry carries a `member`. As belt-and-braces I still ran the quote-presence check on my own live fetch after extraction
(`quote in S###.live.txt`): `True` / `True` / `True`.

Entry fields (all three): `opened` 2026-10-25, `verdict` `holds`, and `entry.url` byte-identical to the first http(s) URL of the
row's source cell (checked programmatically: `url_match=True` ×3).

## Located context (`measure.py --extract` output, a few words either side)

- **S060** at extract offset 13093 of 52256 (25% into the normalized text), body of "Filtering -e trace = syscall_set" — the
  `%file` value entry of `syscall_set`:
  `… Traces only those system calls that match the regex . You can use POSIX Extended Regular Expression syntax (see regex(7) ). %file file «Traces all system calls that take a file name as an argument» . You can think of this as an abbreviation for --trace = open , stat , chmod , unlink ,... which is useful to seeing what files the process is referencing. …`
  Not a title/nav/footer/cookie fragment; the row's anchor names exactly `§Filtering -e trace=syscall_set → %file`. The strace
  footer in the same snapshot still reads `strace 7.1.0.62.c605d6  2026-06-25`, matching the row's anchor version note.
- **S061** at extract offset 11794 of 13909 (84%), body of "Converting a workspace into a colocated workspace", inside the manual
  recipe that `jj git colocation enable` automates:
  `… # Make the Git repository non-bare and set HEAD git config --unset core.bare # «Convince jj to update .git/HEAD to point to the working-copy commit's parent» jj new && jj undo Warning On Windows, the echo command will append line endings …`
  The same snapshot's "Colocated Jujutsu/Git workspaces" paragraph 2 reads `One reason for this (see below for more) is that jj commands will usually put the Git repo in a "detached HEAD" state`, i.e. the detached-HEAD statement the row's anchor also names is still present.
- **S153** at extract offset 61761 of 72209 (85%), body of the ast module reference at `ast. get_source_segment ( source , node , * , padded = False )`:
  `… AsyncFunctionDef is now supported. ast. get_source_segment ( source , node , * , padded = False ) ¶ «Get source code segment of the source that generated node» . If some location information ( lineno , end_lineno , col_offset , or end_col_offset ) is missing, return None . If padded is True , the first line …`

## Commands and output

```
$ for id in S060 S061 S153; do gunzip -c …/.ufo/evidence/round-45/freshness/sources/$id.raw.gz > $id.snap; done   # exit 0
$ sha256sum S060.live S061.live S153.live
eedefecf7c55cf36976fce6fbfff8b1340c62b696bb7268a83df643ee8ea02f6  S060.live
db9c9a760810386858e6b1bad4a7a334c56bd48c77692dbc1c343657ae0ca254  S061.live
f4c18b31aea745258ff49b4227fca6e916a528dfb5ef77da4f3fa89323346b82  S153.live

$ for id in S060 S061 S153; do python3 …/freshness/measure.py --extract /tmp/tameshi-r45-ExecJudge04/$id.snap > $id.txt; done
S060 extract rc=0 bytes=53082
S061 extract rc=0 bytes=13920
S153 extract rc=0 bytes=72397

$ python3 …/freshness/measure.py --lane …/tameshi-shokunin --rev 3310e7be803516ca5934b4e949d91bcec824b179 --check $id.frag.json
CHECK S060 verified ok   (rc=0)
CHECK S061 verified ok   (rc=0)
CHECK S153 verified ok   (rc=0)

$ git cat-file -e ad5942c:…/sources/S###.raw.gz   # present ×3; git show <rev>:<blob> | gunzip -c | sha256sum equals the entry hash ×3

$ git diff --stat ad5942c6e9858af19d00000b58439b321ddfa62b HEAD -- .ufo/evidence/round-45/freshness/ledger.json \
    .ufo/evidence/round-45/freshness/sources/ corpus/SOURCES.md        # empty (exit 0): ledger and snapshots unchanged since ad5942c
$ git show ad5942c:…/freshness/ledger.json | sha256sum ; sha256sum …/freshness/ledger.json
433a624bf8cdd42ccf2ea2a818aa0bdc40dd2c77cd636e1121d0aa51eb5a9913  -   (both, identical)
```

Quote predicates I re-computed myself against the registry cells (not trusting the author's CHECK alone): token counts 12 / 12 / 10
(all inside 6-25); content-word overlap with scope+anchor+teaches = 2 (`file`, `name`) / 5 (`commit`, `copy`, `head`, `parent`,
`working`) / 3 (`node`, `segment`, `source`); `quote in row cells` = False for all three, so none is copied from the row.

## Notes, risks and dependencies (none of these changes a verdict)

1. **S060 overlap is exactly at the floor (2 content words).** It passes the frozen `>= 2` predicate, and the quote is not copied
   from the row, but a stricter future threshold would drop it. The content support itself is direct (`%file` = "useful to seeing
   what files the process is referencing"), so I agree.
2. **S061's quote is a recipe step comment, not prose.** The row's anchor explicitly names "recipe comment", and the comment states
   the fact the teaches claim rests on (`.git/HEAD` → working-copy commit's parent); the literal "detached HEAD" phrasing lives in
   paragraph 2 of the preceding section, also inside the row's anchor. A judge who requires a prose sentence only would dispute; I
   do not, because the anchor designates the recipe comment and the statement is affirmative, not a bare fragment.
3. **S061's URL is the rolling `latest` alias.** The page carries no version marker for `0.46.0` (the only `version 0.30.0` string in
   the snapshot is about the `git.write-change-id-header` feature), so the row's anchor version note is not re-confirmable from bytes.
   The teaches claim is version-independent and is present today.
4. **S153's row anchor records a stale snapshot prefix.** The anchor cites round-41 `.ufo/evidence/round-41/sources/ast.html`,
   362029 B, sha256 `183a4f8c…`; today's page is the same size but hashes `f4c18b31…`. Diffing the two raw files shows exactly one
   changed line: `Last updated on Oct 25, 2026 (06:17 UTC)` → `(18:32 UTC)`. No body text changed, so the quote and the teaches
   claim hold; the anchor's sha prefix is simply one build behind (a row-anchor refresh the L1 may want, not a C1 failure).
5. **For the review to count**, the L1 must (a) commit this report at `.ufo/waves/round-45/w2/ExecJudge04.md` at the deciding
   revision and (b) list `ExecJudge04` with non-empty output in `.ufo/waves/round-45/w2-results.json` — the counter requires both
   (`measure.py:review_sets`). `reviews.json` is not in the worktree yet, so it is L1-assembled; my fragment is below.

```json
{"reviews": [
 {"id": "S060", "reviewer": "ExecJudge04", "verdict": "agree", "report": ".ufo/waves/round-45/w2/ExecJudge04.md", "reason": "sha equal (live = entry.raw_sha256 = gunzip snapshot = eedefecf…); the 12-token quote is the %file qualifier definition inside section Filtering -e trace=syscall_set (the row's own anchor), immediately followed by 'an abbreviation for --trace = open , stat , chmod , unlink ,... which is useful to seeing what files the process is referencing', which supports the teaches claim that an open trace records files opened by name."},
 {"id": "S061", "reviewer": "ExecJudge04", "verdict": "agree", "report": ".ufo/waves/round-45/w2/ExecJudge04.md", "reason": "sha equal (live = entry.raw_sha256 = gunzip snapshot = db9c9a76…); the 12-token quote is the jj new && jj undo step comment in section Converting a workspace into a colocated workspace (the recipe comment the row's anchor names), stating that jj updates .git/HEAD to point to the working-copy commit's parent, and paragraph 2 of the preceding Colocated Jujutsu/Git workspaces section in the same snapshot adds the 'detached HEAD' wording, so the teaches claim that git rev-parse HEAD is not the bookmark tip is supported."},
 {"id": "S153", "reviewer": "ExecJudge04", "verdict": "agree", "report": ".ufo/waves/round-45/w2/ExecJudge04.md", "reason": "sha equal (live = entry.raw_sha256 = gunzip snapshot = f4c18b31…); the 10-token quote is the first description sentence of ast.get_source_segment in the ast module reference (the row's own anchor), followed by the padded/None clauses, which supports the teaches source-recovery claim; the live page differs from the row's round-41 snapshot only in the 'Last updated on Oct 25, 2026 (18:32 UTC)' line."}
]}
```

Byte-exact copy also at `/tmp/tameshi-r45-ExecJudge04/reviews.json`.

## Bounds and tooling

- Read-only on the lane checkout; the only lane write is this report. All scratch under `/tmp/tameshi-r45-ExecJudge04/`. No
  `git add/commit/stash/checkout/switch/reset/pull/push` and no `jj` command was run in the lane; no fixture repo was needed.
- No tool installs or upgrades (system `curl`, `python3`, `sha256sum`, `diff` sufficed); nothing to record for pacman/uv/npx.
- The deciding run of the counter remains the L1's; I used only `--extract` and `--check` against rev
  3310e7be803516ca5934b4e949d91bcec824b179, plus read-only `git show`/`git diff`/`git cat-file`.

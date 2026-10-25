seat: ExecJudge06

# Round-45 w2 C1 falsify review — S091, S154, S155

Item: independent (non-author) re-judgement of three wave-1 C1 ledger entries at
commit `ad5942c6e9858af19d00000b58439b321ddfa62b`. Authors: S091 = ExecRows17,
S154/S155 = ExecRows23. I am neither author.

Inputs read: `.ufo/evidence/round-45/freshness/ledger.json` and
`.ufo/evidence/round-45/freshness/sources/S09{1,4,5}.raw.gz` via `git show ad5942c6:...`,
`corpus/SOURCES.md` rows 100/124/125, `.ufo/waves/round-45/w1/ExecRows17.md`,
`.ufo/waves/round-45/w1/ExecRows23.md`, and the frozen counter
`.ufo/evidence/round-45/freshness/measure.py`. `contract.json` read, not edited.

Scratch: `/tmp/tameshi-r45-ExecJudge06/` (live fetches `S###.live`, gunzipped snapshots
`S###.snap`, extracted text `S###.snap.txt`, per-entry fragments `S###.entry.json`,
`reviews.json`). Lane checkout untouched; no git/jj mutation; no tool installs (none needed).

## Verdicts

S091 agree — reviewer ExecJudge06 — live bytes sha256 `33a99ba212228d6968e7721a87197558b0e88a450ecfc303eaa34d8321d2da8c` equal both the entry `raw_sha256` and the committed snapshot, and the 18-token quote is body text in §SPECIFYING REVISIONS 64 chars after the `<sha1>` entry marker (heading at extract index 3144, quote 3665, footer 18295), stating verbatim that a short name is the full name or a unique leading substring — exactly the row's prefix-convention teaches.
S154 agree — reviewer ExecJudge06 — live bytes sha256 `7ae9b7205cf1a79380379fae860a93ddb88d9bec24284f946f4019cfd1ae016e` equal both the entry `raw_sha256` and the committed snapshot, and the 16-token quote is the opening sentence of the §Path.write_text body (heading 34748, quote 34827) stating the pointed-to file / text mode / write / close mechanism the row's teaches derives "receiver is the destination" from.
S155 agree — reviewer ExecJudge06 — live bytes sha256 `c51d8423f5a75e00c7039463f8a5992ef8f1f92b994d69f67d212ff7bfd92b3a` equal both the entry `raw_sha256` and the committed snapshot, and the 23-token quote is the No-coverage sentence inside the §Running the tests outcome list (heading 2185, seven-outcome enumeration 2710, quote 2912), supporting the row's "No coverage is Survived with no exercising test" teaches.

No disputes. None of the three quotes is copied from the row's own cells
(`quote.lower() in fold(source|scope|anchor|teaches).lower()` = False for all three),
none is a `<title>`/nav/TOC/footer/cookie fragment, and none is truncated below the claim.

## sha256 comparison lines

Commands (from `/tmp/tameshi-r45-ExecJudge06`):
`curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o S###.live '<row url>'` (exit 0 for all three),
`sha256sum S###.live`, `gunzip -c <lane>/.ufo/evidence/round-45/freshness/sources/S###.raw.gz | sha256sum`.

```
S091 live   33a99ba212228d6968e7721a87197558b0e88a450ecfc303eaa34d8321d2da8c  S091.live
S091 entry  33a99ba212228d6968e7721a87197558b0e88a450ecfc303eaa34d8321d2da8c  (raw_sha256)
S091 snap   33a99ba212228d6968e7721a87197558b0e88a450ecfc303eaa34d8321d2da8c  (74526 B, == committed blob at ad5942c6)
S154 live   7ae9b7205cf1a79380379fae860a93ddb88d9bec24284f946f4019cfd1ae016e  S154.live
S154 entry  7ae9b7205cf1a79380379fae860a93ddb88d9bec24284f946f4019cfd1ae016e  (raw_sha256)
S154 snap   7ae9b7205cf1a79380379fae860a93ddb88d9bec24284f946f4019cfd1ae016e  (271189 B, == committed blob at ad5942c6)
S155 live   c51d8423f5a75e00c7039463f8a5992ef8f1f92b994d69f67d212ff7bfd92b3a  S155.live
S155 entry  c51d8423f5a75e00c7039463f8a5992ef8f1f92b994d69f67d212ff7bfd92b3a  (raw_sha256)
S155 snap   c51d8423f5a75e00c7039463f8a5992ef8f1f92b994d69f67d212ff7bfd92b3a  (12155 B, == committed blob at ad5942c6)
```

All three are byte-identical today, so the "dynamic chrome, fall back to live quote presence"
branch was not needed (and `--extract` of the live file was not required for a verdict).
Entry `url` fields match the row URLs exactly (git-scm.com/docs/gitrevisions;
docs.python.org/3/library/pathlib.html; pitest.org/quickstart/basic_concepts/);
`opened` = 2026-10-25 for all three; all three rows are `mined` in the rev registry.

## Located context

Method: `python3 <lane>/.ufo/evidence/round-45/freshness/measure.py --extract S###.snap > S###.snap.txt`
then exact `str.find` of the entry quote in the normalized text.

S091 — gitrevisions, §SPECIFYING REVISIONS, `<sha1>` entry (quote found once, index 3665 of 18407):

> …The shell and other UIs might require additional quoting to protect special characters and to avoid word splitting. `<sha1>` , e.g. dae86e1950b1277e545cee180551750029cfe735 , dae86e **The full SHA-1 object name (40-byte hexadecimal string), or a leading substring that is unique within the repository.** E.g. dae86e1950b1277e545cee180551750029cfe735 and dae86e both name the same commit object if there is no other object in your repository whose object name starts with dae86e. `<describeOutput>` , e.g. v1.7.4.2-679-g3bee7fb…

The following sentence ("…whose object name starts with dae86e") independently confirms the
prefix, not interior-slice, reading the row's teaches asserts. Section-body position: the
TOC occurrence of "SPECIFYING REVISIONS" is at 198, the body heading at 3144, quote at 3665.

S154 — pathlib, §Path.write_text (quote found once, index 34827 of 60832):

> Path. write_text ( data , encoding = None , errors = None , newline = None ) ¶ **Open the file pointed to in text mode, write data to it, and close the file**: >>> p = Path ( 'my_text_file' ) >>> p . write_text ( 'Text file contents' ) 18 >>> p . read_text () 'Text file contents' An existing file of the same name is overwritten.

Quote is the method's own definition sentence, directly after the signature line (heading
index 34748, delta 79); the example `p.write_text(...)` on the receiver `p` supports the
"receiver expression is the destination" conclusion.

S155 — PIT basic concepts, §Running the tests outcome list (quote found once, index 2912 of 4123):

> …For each mutation PIT will report one of the following outcomes Killed Survived No coverage Non viable Timed Out Memory error Run error Killed means a test caught the mutation successfully. Survived means the mutation was not detected by the covering test. **No coverage is the same as Survived except there were no tests that exercised the line of code where the mutation was created.** A mutation may time out if it causes an infinite loop…

Seven outcomes are enumerated immediately before the quote (Killed, Survived, No coverage, Non
viable, Timed Out, Memory error, Run error), and "Run error" is defined further in the same
section ("run error" present in the extract), so both teaches clauses rest on the same section.

## Counter helper runs (permitted forms only)

`python3 .ufo/evidence/round-45/freshness/measure.py --check <fragment> --lane <lane> --rev 3310e7be803516ca5934b4e949d91bcec824b179`
on the three entry fragments extracted from the ad5942c6 ledger:

```
CHECK S091 verified ok
CHECK S154 verified ok
CHECK S155 verified ok
```

I did not run the deciding measurement; no counter was run against an unpermitted revision.

## Integration note for L1

The review file is at `/tmp/tameshi-r45-ExecJudge06/reviews.json` (lane is read-only for me;
only this report was written into the lane). Exact content to commit at
`.ufo/evidence/round-45/freshness/reviews.json` (merge with the other w2 reviewers' records):

```json
{
  "reviews": [
    {"id": "S091", "reviewer": "ExecJudge06", "verdict": "agree", "report": ".ufo/waves/round-45/w2/ExecJudge06.md",
     "reason": "live sha256 == entry raw_sha256 == committed snapshot; 18-token quote in SPECIFYING REVISIONS <sha1> entry body states the unique-leading-substring rule the row teaches"},
    {"id": "S154", "reviewer": "ExecJudge06", "verdict": "agree", "report": ".ufo/waves/round-45/w2/ExecJudge06.md",
     "reason": "live sha256 == entry raw_sha256 == committed snapshot; 16-token quote is the Path.write_text definition sentence (pointed-to file, text mode, write, close) the row's teaches derives from"},
    {"id": "S155", "reviewer": "ExecJudge06", "verdict": "agree", "report": ".ufo/waves/round-45/w2/ExecJudge06.md",
     "reason": "live sha256 == entry raw_sha256 == committed snapshot; 23-token quote is the No-coverage sentence inside the Running the tests seven-outcome list the row teaches"}
  ]
}
```

Note for the deciding run: `review_sets()` in measure.py only counts a review whose `report`
path is under `.ufo/waves/round-45/` and present at the deciding revision, whose text names
both the id and `ExecJudge06`, and whose reviewer appears with non-empty output in
`.ufo/waves/round-45/w2-results.json`. This report names all three ids and the reviewer, so
it satisfies the report-text condition once committed and once my seat output is recorded in
the orchestrator-written results file.

Risks / blockers: none. No drift observed on any of the three URLs at 2026-10-25 17:23 UTC
(all three byte-identical to the author's fetches, which were themselves same-day).

seat: ExecJudge12

# Round-45 w2 — C1 falsify review: S011, S057, S068

Independent re-judgment at `ad5942c6e9858af19d00000b58439b321ddfa62b` (ledger, snapshots, w1 reports). I am not the author of any of the three (authors: ExecRows03, ExecRows07, ExecRows11). Every fetch and every extraction was done by me today in `/tmp/tameshi-r45-ExecJudge12/`; no lane file was written except this report.

## Verdicts

S011 agree — reviewer ExecJudge12 — live fetch is byte-identical to the committed snapshot (sha256 a5c8d2a222cc1d3c53a68c4675c4c64070e94c29f5a6ab5b6dcac3c5e8bdc21c), and the 24-token quote sits in the ABSTRACT on p.1 (offset 4186; `ABSTRACT` at 271, `1 INTRODUCTION` at ~5020) and states the four-point score variation and the 9% unknown mutant-test pairs the teaches cell claims, with the abstract's next sentence carrying the 79.4% reduction the teaches also names.

S057 agree — reviewer ExecJudge12 — live fetch is byte-identical (sha256 63b7bfca877cd4661cb24e93fbfe1757a2740b39fb65ee3a79eb17e36215f023), PDF CreationDate is 2017-12-14 exactly as the anchor says, and the 9-token quote is the first sentence of §5.3.1 "Identifying Equivalent Mutants" on p.29 (heading at 58774, quote at 58812), immediately followed by "it is unrealistic to form an automated technique that will identify all the equivalent mutants", which supports the cannot-be-detected-in-general teaches.

S068 agree — reviewer ExecJudge12 — live fetch is byte-identical (sha256 b805fe23c7251ad6c3d08a829ed755b80a8fa106929c67325c7122f3b126ef2c), the 23-token quote is DESCRIPTION body text immediately after the SYNOPSIS (offset 823) followed by the getppid/SIGCHLD consequences, so it states the reparenting rule the teaches claims; the COLOPHON still reads "Linux man-pages 6.19 2026-02-08" as the anchor records.

## sha256 provenance (live vs entry vs gunzipped snapshot)

```
$ curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o S0XX.live '<entry.url>'
S011 https://mir.cs.illinois.edu/awshi2/publications/ISSTA2019.pdf   295016 bytes  a5c8d2a222cc1d3c53a68c4675c4c64070e94c29f5a6ab5b6dcac3c5e8bdc21c
S057 https://discovery.ucl.ac.uk/id/eprint/10056704/1/survey.pdf    1129278 bytes  63b7bfca877cd4661cb24e93fbfe1757a2740b39fb65ee3a79eb17e36215f023
S068 https://man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html  9879 bytes  b805fe23c7251ad6c3d08a829ed755b80a8fa106929c67325c7122f3b126ef2c
```

`gunzip -c .ufo/evidence/round-45/freshness/sources/S0XX.raw.gz | sha256sum` gave the same three digests, and each equals the entry's `raw_sha256`. Live == snapshot == entry for all three: provenance confirmed, no dynamic-chrome drift, so no `--extract` fallback on live bytes was needed (I still extracted the live PDFs for the page check below).

## Context / located quotes

Counter check (seat helper, not a measurement):

```
$ python3 .ufo/evidence/round-45/freshness/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    --rev ad5942c6e9858af19d00000b58439b321ddfa62b --check /tmp/tameshi-r45-ExecJudge12/S0XX.json --snapdir /tmp/tameshi-r45-ExecJudge12
CHECK S011 verified ok
CHECK S057 verified ok
CHECK S068 verified ok
```

Extraction via `--extract` on the gunzipped snapshot, then a literal find of the entry quote:

- S011 (offset 4186, 24 tokens): `... Without reliable test outcomes, mutation testing can result in unreliable results, e.g., in our experiments, [mutation scores vary by four percentage points on average between repeated executions, and 9% of mutant-test pairs have an unknown status.] Many modern software projects suffer from flaky tests. ...` — abstract prose, p.1 per `pdftotext` form-feed count (quote page 1 of 12, `ABSTRACT` page 1). Shared content words with scope+anchor+teaches: between, four, mutant, mutation, pairs, points, scores, test, unknown, vary (10). Not copied from the row's cells. The teaches' remaining numbers are backed by the same abstract: "reduce the number of łunknownž (flaky) mutants by 79.4%".
- S057 (offset 58812, 9 tokens): `... Step 8 (Section 5.8). 5.3.1. Identifying Equivalent Mutants [Detecting equivalent mutants is a well-known undecidable problem [28].] This means that it is unrealistic to form an automated technique that will identify all the equivalent mutants. ...` — exactly the row's §5.3.1 anchor, p.29 of 154 by form-feed count (anchor says "p. 29"). Shared content words: equivalent, problem (plus "mutants" against "mutant" scope text). Not copied from the row's cells.
- S068 (offset 823, 23 tokens): `DESCRIPTION top If set is nonzero, set the "child subreaper" attribute ... A subreaper fulfills the role of init(1) for its descendant processes. [When a process becomes orphaned (i.e., its immediate parent terminates), then that process will be reparented to the nearest still living ancestor subreaper.] Subsequently, calls to getppid(2) ... will now return the PID of the subreaper process ...` — DESCRIPTION body, first paragraph after the SYNOPSIS, not a title/nav/footer. Shared content words: ancestor, becomes, living, nearest, orphaned, parent, process, reparented, still, subreaper (10). Not copied from the row's cells.

## Notes (non-blocking)

- S057's normalized text has no page markers (the counter's `fold()` collapses form feeds), so the p.29 anchor was confirmed on a fresh `pdftotext` of the same bytes rather than through `--extract`; section heading and page both match.
- S068 shares its URL with S077 (the row the w1 report calls an anchor supersede). The entry under review names the URL of S068 exactly, and the quote sits at S068's anchor (§DESCRIPTION), so the duplicate-URL neighbour does not affect this verdict.
- No tool installs or upgrades this seat; nothing needed (curl, python3, pdftotext, pdfinfo already present).

## Handoff for the L1

Reviews JSON written to `/tmp/tameshi-r45-ExecJudge12/reviews.json` (3 entries, all `agree`, `report` = `.ufo/waves/round-45/w2/ExecJudge12.md`). Integration and the deciding run remain the L1's.

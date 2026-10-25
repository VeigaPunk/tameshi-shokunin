seat: ExecRows17

# Round-45 w1 C1 re-verification — S091, S093, S094 (author)

Item: C1 row re-verification for rows S091, S093, S094. Fetched live on 2026-10-25, extracted with `measure.py --extract`, quoted afresh from the snapshot's normalized text, checked with `measure.py --check --rev 3310e7be803516ca5934b4e949d91bcec824b179`. All three verdicts: `holds`.

Tooling: no installs (used preinstalled curl, python3, pdftotext via measure.py). Scratch: /tmp/tameshi-r45-ExecRows17/.

## S091 — gitrevisions
- URL: https://git-scm.com/docs/gitrevisions (byte-exact from SOURCES.md line 100)
- curl `-fsSL -A 'Mozilla/5.0'` exit 0; 74526 bytes; sha256 `33a99ba212228d6968e7721a87197558b0e88a450ecfc303eaa34d8321d2da8c`
- CHECK: `CHECK S091 verified ok`
- Note: the live `<sha1>` entry still reads "The full SHA-1 object name (40-byte hexadecimal string), or a leading substring that is unique within the repository." — exactly what teaches claims (short object name = full name or unique leading substring; prefix convention, not interior-slice). Quote taken verbatim from the `--extract` output (S091.txt), not from the registry row.
- Fragment:

```json
{
  "id": "S091",
  "url": "https://git-scm.com/docs/gitrevisions",
  "opened": "2026-10-25",
  "verdict": "holds",
  "raw_sha256": "33a99ba212228d6968e7721a87197558b0e88a450ecfc303eaa34d8321d2da8c",
  "quote": "The full SHA-1 object name (40-byte hexadecimal string), or a leading substring that is unique within the repository.",
  "snapshot": ".ufo/evidence/round-45/freshness/sources/S091.raw.gz",
  "author": "ExecRows17"
}
```

## S093 — bwrap(1) 0.13.1
- URL: https://github.com/containers/bubblewrap/blob/v0.13.1/bwrap.xml (byte-exact from SOURCES.md line 102)
- curl `-fsSL -A 'Mozilla/5.0'` exit 0; 601469 bytes; sha256 `f8a95822f7277eae4809c664bef2e6b1ca0749f4cb6fb373c123f4c9c303e240`
- CHECK: `CHECK S093 verified ok`
- Note: the live blob page still embeds bwrap.xml v0.13.1; the `--unshare-all` entry keeps its equivalence expansion over the six `--unshare-*` flags (quote covers `--unshare-user-try` through `--unshare-uts`, and `--unshare-cgroup-try` follows in the same sentence at extract index ~11490 with "Create a new cgroup namespace if possible else skip it"), grounding teaches' six-flag expansion with user and cgroup try-else-skip. Quote is the 25-token span copied verbatim from S093.txt.
- Fragment:

```json
{
  "id": "S093",
  "url": "https://github.com/containers/bubblewrap/blob/v0.13.1/bwrap.xml",
  "opened": "2026-10-25",
  "verdict": "holds",
  "raw_sha256": "f8a95822f7277eae4809c664bef2e6b1ca0749f4cb6fb373c123f4c9c303e240",
  "quote": "< option >--unshare-user-try</ option > < option >--unshare-ipc</ option > < option >--unshare-pid</ option > < option >--unshare-net</ option > < option >--unshare-uts</ option >",
  "snapshot": ".ufo/evidence/round-45/freshness/sources/S093.raw.gz",
  "author": "ExecRows17"
}
```

## S094 — arXiv:1411.2664v3
- URL: https://arxiv.org/pdf/1411.2664 (byte-exact from SOURCES.md line 103)
- curl `-fsSL -A 'Mozilla/5.0'` exit 0; 322643 bytes; sha256 `6e9532a978ae5d498722eb95f1a13332f24d1eb09c1791f56fd9aa3eb310d697` — identical to the row's committed PDF digest (committed 2026-10-23, re-fetched by L1), so the live bytes are unchanged.
- CHECK: `CHECK S094 verified ok`
- Note: §1 Introduction still contains the sentence beginning "Each submitted model" — "Each submitted model is evaluated on a (fixed) test set that is available only to the organizers." — grounding teaches (test set withheld from submitters still overfits once scores are returned and models resubmitted; final comparison uses a second unused test). Quote copied verbatim from S094.txt.
- Fragment:

```json
{
  "id": "S094",
  "url": "https://arxiv.org/pdf/1411.2664",
  "opened": "2026-10-25",
  "verdict": "holds",
  "raw_sha256": "6e9532a978ae5d498722eb95f1a13332f24d1eb09c1791f56fd9aa3eb310d697",
  "quote": "Each submitted model is evaluated on a (fixed) test set that is available only to the organizers.",
  "snapshot": ".ufo/evidence/round-45/freshness/sources/S094.raw.gz",
  "author": "ExecRows17"
}
```

## Handoff
Raw snapshots kept at /tmp/tameshi-r45-ExecRows17/S09{1,3,4}.raw (the L1 integrates them; the fragments point at committed snapshot paths `.ufo/evidence/round-45/freshness/sources/S0xx.raw.gz`). All three fragments pass the frozen counter's `--check` at the freeze rev. No blockers.

Risks: S093's snapshot is the GitHub HTML blob page (601 KB), not the bare XML; extraction locates the embedded rendered bwrap.xml content (quote verified present by the counter). S094's PDF digest matched the row's committed digest exactly.

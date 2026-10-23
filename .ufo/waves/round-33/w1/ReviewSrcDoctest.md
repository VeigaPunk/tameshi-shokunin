# ReviewSrcDoctest — C2 freshness

## Verdict

**Frozen snapshot checks pass; live-stability check fails.** The snapshot matches both frozen digests and contains the quoted sentence. My independent live body fetch had the same byte count but a different SHA-256, with the only reported difference in the generated “Last updated” footer. The source-seat draft was not present, so its actual S100 cells and Gate bullet cannot be verified; the cell-by-cell section below records the contract checks, not invented draft contents.

## Evidence

- `.ufo/evidence/round-33/contract.json:28-29` requires a new row with ID greater than S099, a teaches cell opening `supersedes S055 -` and naming a versioned Python docs URL, the pinned snapshot digest, the lesson Gate digest, and the quoted sentence.
- `.ufo/evidence/round-33/contract.json:11` pins snapshot SHA-256 `217edd573ef328316ac2410e5d046c5ad3a2df522270e5868bc5e5e5eb744899`.
- `.ufo/evidence/round-33/c2/c2-measure.py:26,29` freezes the quote bytes and the same expected SHA. `.ufo/evidence/round-33/c2/fetch-receipt.txt:2-8` records the versioned URL, two earlier HTTP 200 fetches, 216574 bytes, the matching digest, and the quote.
- `.ufo/evidence/round-33/c2/doctest-snapshot.html:245-247` contains the module-introduction sentence. The proposed <=25-word quote can be: “The doctest module searches for pieces of text that look like interactive Python sessions.” (14 words.) The page body is the module introduction; its first bullet follows at lines 249-250.
- `corpus/SOURCES.md:107` has S099 and `:390` records S100 as the next unused ID. There is no S100 row in the current file. The expected source-seat report `.ufo/waves/round-33/w1/SrcDoctestReopen.md` and `corpus/lessons/round-33.md` were absent when checked, so no actual row or Gate bullet was available to inspect. I reviewed the required fields against the frozen contract and the source-seat task specification instead.

Commands and observed outputs (each command's exit was captured with `cmd; echo $? > <scratch-file>`):

- `sha256sum /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-33/c2/doctest-snapshot.html` → `217edd573ef328316ac2410e5d046c5ad3a2df522270e5868bc5e5e5eb744899`; exit 0.
- `wc -c /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-33/c2/doctest-snapshot.html` → `216574`; exit 0.
- `curl -m 60 -sS -o /fast/scratch/hyaku/tameshi-r33-seats/tameshi-r33-w1-ReviewSrcDoctest-4/live-doctest.html https://docs.python.org/3.15/library/doctest.html` → no stdout; exit 0.
- `wc -c /fast/scratch/hyaku/tameshi-r33-seats/tameshi-r33-w1-ReviewSrcDoctest-4/live-doctest.html` → `216574`; exit 0.
- `sha256sum /fast/scratch/hyaku/tameshi-r33-seats/tameshi-r33-w1-ReviewSrcDoctest-4/live-doctest.html` → `65a734a8ef4d4c7bead9d8e59beb97b937504e76349de333f6f9221219a22ef7`; exit 0.
- `cmp /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-33/c2/doctest-snapshot.html /fast/scratch/hyaku/tameshi-r33-seats/tameshi-r33-w1-ReviewSrcDoctest-4/live-doctest.html` → `... differ: char 216324, line 2205`; exit 1. `cmp -l` reported `216324 61 64`; snapshot line 2205 says `Last updated on Oct 23, 2026 (18:17 UTC).`, while the live response says `(18:41 UTC).` The fetched bytes therefore do not equal the frozen snapshot.
- A separate status-only curl, `curl -m 60 -sS -o /dev/null -w 'http_code=%{http_code}\n' https://docs.python.org/3.15/library/doctest.html`, printed `http_code=200`; exit 0. This was an additional request after the saved-body fetch because the first request did not capture its HTTP status; it is not the status of the saved body response. Thus the required status/bytes/hash are not all evidenced by one independent fetch.

## Cell-by-cell contract review

No source-seat draft was available, so these are unverified checks rather than findings about actual cell values:

| S100 cell | Required check / available evidence |
|---|---|
| id | Must be greater than S099; S100 is next unused per `corpus/SOURCES.md:390`, but no row exists yet. |
| source | Must name the versioned URL `https://docs.python.org/3.15/library/doctest.html`; the frozen contract requires a versioned docs.python.org URL. No draft value to inspect. |
| kind | Source task specifies `docs`; frozen C2 contract does not constrain this cell. No draft value to inspect. |
| tier | Source task specifies `A`; frozen C2 contract does not constrain this cell. No draft value to inspect. |
| scope | Source task specifies executable documentation examples; frozen C2 contract does not constrain this cell. No draft value to inspect. |
| anchor | Source task requires naming the version; frozen C2 contract does not constrain this cell. No draft value to inspect. |
| teaches | Must open exactly `supersedes S055 -` and name the versioned URL; no draft value to inspect. |
| status | No value is prescribed by the frozen C2 contract or the source-seat task. No draft value to inspect. |
| opened | Gate task specifies access date 2026-10-23; frozen C2 predicate does not constrain this table cell. No draft value to inspect. |
| recheck | No value is prescribed by the frozen C2 contract or source-seat task. No draft value to inspect. |
| used-by | Source task specifies `corpus/lessons/round-33.md` and `corpus/knowledge/executable-self-assessment.md`; no draft value to inspect. |

The Gate bullet must report the versioned URL, access date, byte count, digest, and quote. No actual bullet was available; the current live digest differs from the frozen digest, so it must not claim the live fetch equals the snapshot.

## Smallest safe correction

Do not change the frozen snapshot, counter pin, or contract to conceal the live difference. Keep the pinned artifact intact and report the timestamp drift and the inability to satisfy live byte equality at this fetch. The source-seat owner should provide the actual S100 row and Gate draft for cell-level review; until then those values remain unverified. A new pin would require a newly frozen claim, not an in-place correction to this one.

# T87S1 — located-quote proof for the round-87 Gate (draft)

Seat: T87S1 (read-only verification; no lane file edited). Lane HEAD for measurement: 1d5102a1.
Method: each snapshot read as raw HTML; tags stripped and entities unescaped; whitespace
normalized; every quote searched as a verbatim string across the whole document and per line.
Line numbers are 1-based raw-HTML lines of the snapshot file. Hashes are `sha256sum` of the
snapshot file as stored in the lane. Scratch: /fast/scratch/hyaku/tameshi-r87/T87S1 (removed on exit).

Note on `corpus/lessons/round-87.md`: this file does not exist yet; the block below is the draft
for it, in the same shape as the `## Gate` of `corpus/lessons/round-86.md`.

## Gate

Candidate: two claims (frozen at 1d5102a1). R87-C1 is operability — the frozen counter
`.ufo/evidence/round-87/measure.py` (predicate `C1_R87 rev=<rev> passed=8/8 C1_R87_PASS=true`).
R87-C2 is calibration — the frozen census v2 `tools/capability-census-v2.py` binds every real
manifest row and no overreach row (predicate `CAP_CENSUS_V2: rows=N bound=N unbound=0 mismatches=0`
on the real manifest, `bound=0` on the overreach manifest).

Source **S289** (Git git-cat-file documentation), fetched 2026-11-05:
`https://git-scm.com/docs/git-cat-file`, HTTP/2 200, 79360 B, sha256
`91180e9f7199b73531900776d4d4adc17b5413f26f7c6a7e2420eb34412d8be7`,
header `date: Thu, 05 Nov 2026 07:38:31 GMT`, snapshot
`.ufo/evidence/round-87/sources/s289-cat-file.html` (+ `s289.headers`). Title in snapshot:
"Git - git-cat-file Documentation".
- Quote A (option `-t`), 11 words, snapshot lines 2234–2235 (sentence wraps; located line 2234
  begins "Instead of the content, show the object type identified by"):
  “Instead of the content, show the object type identified by <object>.”
- Quote B (DESCRIPTION), 18 words, snapshot lines 2205–2206 (located line 2205 begins
  "Output the contents or other properties such as size, type o"):
  “Output the contents or other properties such as size, type or delta information of one or more objects.”

Source **S299** (Python shutil documentation), fetched 2026-11-05:
`https://docs.python.org/3/library/shutil.html`, HTTP/2 200, 120949 B, sha256
`28dd43b234cad3fbc6dc5dbed2aa971e15398d4e49e0c3f0174c4a364ca88b18`,
header `date: Thu, 05 Nov 2026 07:38:31 GMT`, snapshot
`.ufo/evidence/round-87/sources/s299-shutil.html` (+ `s299.headers`). Canonical link in snapshot:
`https://docs.python.org/3/library/shutil.html`.
- Quote C (`shutil.which`), 16 words, snapshot lines 667–668 (located line 667 begins
  "Return the path to an executable which would be run if the g"; `cmd` is an `<em>` in the HTML):
  “Return the path to an executable which would be run if the given cmd was called.”

Source **S305** (Git git-ls-tree documentation), re-opened in round 86, access date 2026-11-04:
`https://git-scm.com/docs/git-ls-tree`, HTTP/2 200, 39083 B, sha256
`ff06fbc8b15b0fee505a259e4dc54096c9fba0460f4f02b449d55ecce7818267`,
header `date: Thu, 05 Nov 2026 00:45:18 GMT` (= 2026-11-04 21:45:18 at the lane's -03 clock; the
round-86 capture file is stamped 2026-11-04 21:46 -03), snapshot
`.ufo/evidence/round-86/sources/s305-ls-tree.html` (+ `s305.headers`). Title in snapshot:
"Git - git-ls-tree Documentation".
- Quote D (`objecttype`), 9 words, snapshot line 1812 (located line 1812 is the whole visible line):
  “The type of the object (commit, blob or tree).”
  Verified from the round-86 snapshot itself, not re-fetched; it reproduces the round-86 Gate quote.

**Admit:** S289 (quotes A, B), S299 (quote C), S305 (quote D) as located, verbatim sources for the
round-87 Gate. Each quote is ≤25 words.
**Reject:** none of these sources is used for a claim beyond the sentence quoted. The git-cat-file
text supports object-type/size/content semantics of `git cat-file`; the shutil text supports only
the `which` lookup contract; neither is cited as evidence of the census or the counter's verdict policy.

## Verification detail

| Id | Quote (words) | Snapshot lines | Located text (first 60 chars of the line, visible text) | Verbatim |
|----|---------------|----------------|----------------------------------------------------------|----------|
| S289-A | "Instead of the content, show the object type identified by <object>." (11) | 2234–2235 | `Instead of the content, show the object type identified by` | yes (1 occurrence) |
| S289-B | "Output the contents … one or more objects." (18) | 2205–2206 | `Output the contents or other properties such as size, type o` | yes (1 occurrence) |
| S299-C | "Return the path to an executable … was called." (16) | 667–668 | `Return the path to an executable which would be run if the g` | yes (1 occurrence) |
| S305-D | "The type of the object (commit, blob or tree)." (9) | 1812 | `The type of the object (commit, blob or tree).` | yes (1 occurrence) |

Requested candidate forms, checked: S289 "Instead of the content, show the object type identified by"
(10 words, a fragment) is verbatim at line 2234; S289 DESCRIPTION candidate, S299 candidate and S305 candidate
are verbatim exactly as given. The S289 candidate ends mid-sentence, so the Gate uses quote A, the full sentence.

## Caveats (not defects of the quotes)

- The snapshots do not record their own URL (the headers carry no URL); the URL-to-document link is by
  the page title and, for S299, the canonical link. The git-cat-file and git-ls-tree pages carry no canonical link.
- S305's header Date is 2026-11-05 00:45:18 GMT. The "2026-11-04" access date is the lane-clock date
  (-03) of the round-86 capture; state both if a strict UTC reader is used.

VERDICT: quotes-verified
TOOLS: none

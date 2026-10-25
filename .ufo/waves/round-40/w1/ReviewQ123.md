# ReviewQ123 — hand-check of S123 (tameshi lane, prose could-not-be-fetched class)

Assignment: hand-check S123, prose could-not-be-fetched class; fetch it; unreachable is
not fabrication. No lane checkout edits, shokuknow read-only, no counters run, no installs.
Scratch: `/tmp/tameshi-r40-ReviewQ123/`.

## Row binding

The class lives in the campaign absent-defect register, `shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:364`:

```
| `tameshi` | round2 | S123` | the cited source could not be fetched, so no quote was checked | https://doi.org/10.1109/TSE.2026.3685588 |
```

This is the register's (round-local) id space: the round-39 lesson's "lane slice has 17
data rows" = this register's 14 `payload-absent` tameshi rows (lines 215-228) + exactly
these 3 unreachable rows S113/S123/S134 (lines 363-365). S123 = DOI 10.1109/TSE.2026.3685588.

## Finding 1 (HIGH — round-40 lesson claim falsified for S123)

`corpus/lessons/round-40.md:41` claims: "S113 and S123 were fetched this round
(HTTP 200, HTML and PDF). Their quotes were not located". Both halves fail for S123:

1. **Not HTTP 200.** The cited source yields 202, not 200, to this host:
   - `curl -sS 'https://doi.org/10.1109/TSE.2026.3685588'` → `HTTP=302`, `LOC=https://ieeexplore.ieee.org/document/11540001/` (the DOI resolves — not a dead link);
   - following redirects: plain curl → `HTTP=202 SIZE=0` (empty body, sha256 `e3b0c44298fc1c149afbf4c8996fb924…`); full browser-emulated curl (cookies, Chrome UA, sec-fetch headers) → `HTTP=202 SIZE=2055 TYPE=text/html` — the body is an AWS-WAF bot challenge (`window.awsWafCookieDomainList`, `gokuProps`), zero paper content.
   - No receipt of any S123 fetch exists in `.ufo/waves/round-40/` or `.ufo/evidence/round-40/` (grep `3685588|S123`: only sibling seats and the lessons name it).
2. **The quote IS locatable.** The paper is open: `curl https://arxiv.org/abs/2602.09311` → `HTTP=200 SIZE=43454`, and the 1,595-char arXiv abstract carries the staged figures verbatim: `649`, `1,535`, `1,105`, `55%` all present (the round-2 staged quote: "649 OpenStack projects yield 1 535 cross-project flaky tests and 1 105 inconsistently flaky ones, and 55% of projects are affected"). The campaign already pins this carrier as merged row S193 (`shokuknow/merge/tameshi/SOURCES.append.md:91`).

Precedent: ReviewQ113 (same wave) falsifies the S113 half the same way (quote located
verbatim in the author-hosted PDF). The round-40 lesson sentence does not survive on
either of its rows.

## Finding 2 (the assignment — prose class verdict)

**Unreachable-at-cited-source confirmed today; not a fabrication; not a dead link.**
The cited carrier (doi.org → IEEE Xplore 11540001) serves a bot wall (202/WAF), so the
register's "could not be fetched, so no quote was checked" reproduces as of 2026-10-24
from this host. The register's own doctrine holds: mark unverifiable, do NOT call it a
fabrication — and nothing here indicts fabricated content: the paper is real, published
(TSE 2026) and open elsewhere (arXiv:2602.09311, HTTP 200 this check).

## Finding 3 (MEDIUM — id-space collision; lesson fails under the other reading too)

`shokuknow/lanes/tameshi/ID-REMAP.md:64` remaps `round2 | S119 → S123`, so merged-space
S123 = Zeller & Hildebrandt, *Simplifying and Isolating Failure-Inducing Input*
(`shokuknow/merge/tameshi/SOURCES.append.md:21`, purdue PDF). ScoutQ119 reads the lesson's
S123 as that row. I checked it too:

```
curl -sS -L 'https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/delta-debugging.pdf'
→ HTTP=200 SIZE=247738 TYPE=application/pdf, 17 pages, sha256 7ed0c812e1b3212f3956f5a624ac9103a00468ab665cae00784520d866e1c8aa
pdftotext → line 14-15: "The case study required 139 automated test runs, or 35 minutes on a 500 MHz PC."
           line 69:     "…is reached, where removing any single input entity would cause…"
```

The row's quote ("…removing any single input entity would make the failure disappear…
(139 automated test runs, 35 minutes on a 500 MHz PC)") **is located verbatim** in the
fetched PDF. So "quotes were not located" is falsified for S123 under the merged reading
as well — and note the register's round2 S119 (this same document) is class
`payload-absent` (line 219), a quote defect, not an unreachable one. Under either reading,
`corpus/lessons/round-40.md:41` is wrong about S123.

Two diagnostics: (a) the register's unreachable id cells are malformed (`S123`` with a
stray backtick), so any id-exact `| S123 |` matcher silently misses these rows — the same
guard-vacuity class the lane has met before; (b) the round-38 lesson's derived
`.ufo/waves/round-38/assimilation/quarantine-slice` does not exist in the tree today
(`ls .ufo/waves/round-38/assimilation/`: append-block, census-scratch.*, collisions,
reg-ids, staged-ids, validate/ only), so the 17-row slice's derivation is not reproducible
in-tree — which is how the S123 ambiguity became possible.

## Residual risk and verification gaps

- IEEE may serve HTTP 200 to a JS-executing browser session; unverifiable here. The claim
  on record is only "curl on this host cannot fetch the cited source; 202 ≠ 200".
- Quote location for the DOI row was checked against the arXiv HTML carrier (figures
  verbatim), not against IEEE's own page (walled), and not byte-pinned to the lane.
- I did not re-run the campaign's quote-lint or any counter (bounds).

## Bounds kept

Read-only everywhere except this report file. shokuknow untouched; `considerthese/`
untouched; no edits to the lane checkout, register, or contract; no counters run; no tool
installs. Scratch: `/tmp/tameshi-r40-ReviewQ123/` (s123-body, ieee.html, arxiv.html,
ddbg.pdf, ddbg.txt, cj.txt).

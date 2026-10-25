# ReviewQ134 — hand-check of S134, prose "could not be fetched" class

seat: ReviewQ134 · round 40 w1 · 2026-10-24 · lane root: `.` (tameshi-shokunin)

## Target

The frozen-context claim to hand-check: S134 of the tameshi slice, recorded as
*"the cited source could not be fetched, so no quote was checked"* with URL
`https://doi.org/10.1145/351240.351266`
(`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:365`).
Carried into this lane by `corpus/lessons/round-39.md:33`: *"S113, S123 and S134
carry a prose 'could not be fetched' class: unverifiable, not fabrication, and
not appended."*

## Finding — FALSIFIED: S134's cited source is fetchable by one command

Severity: HIGH (a "could not be fetched" class label is proven false; the row is
verifiable, not unverifiable).

The DOI is the QuickCheck paper (Claessen & Hughes, ICFP 2000). Three commands,
run in scratch `/tmp/tameshi-r40-ReviewQ134/`, no lane or shokuknow writes:

1. Naive fetch fails exactly as the register recorded (this is why the class
   arose, and it stays honest for this channel):
   `curl -sS -L --max-redirs 8 https://doi.org/10.1145/351240.351266`
   → `http=403 redirects=1 final=https://dl.acm.org/doi/10.1145/351240.351266`,
   body = Cloudflare "Just a moment..." challenge.

2. But the channel this campaign itself documents opens it:
   `aaron papers fetch 10.1145/351240.351266 -m auto`
   → exit 0, tier `scihub`, 68,394 bytes of markdown full text
   (sha256 prefix `198d9700e04c9fba`), title/author block intact
   ("QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs",
   Koen Claessen, John Hughes, Chalmers). This matches the campaign's own
   prior record of the same DOI opening, `shokuknow/lanes/tameshi/round4/CHANNELS.md:10`
   and `DOMAIN.md:17,25` (opened 2026-10-23).

3. The quote is locatable in the fetched bytes:
   `aaron papers fetch 10.1145/351240.351266 | tr -d ' \n' | grep -c 'aidstheHaskellprogrammerinformulatingandtestingpropertiesofprograms'`
   → `1`. Raw-text proof:
   `aaron papers fetch 10.1145/351240.351266 | grep -c 'QuickCheck is a to ol which aids the Haskell programmer in form ulating and testing prop erties of programs'`
   → `1` (verbatim modulo the fetcher's intra-word OCR spacing).

Consequence: the register's S134 row and the lane's round-39 lesson line 33
group S134 under *unverifiable*. The premise is false — the source opens, so a
quote could have been and now has been checked. "Unreachable is not
fabrication" still holds in the row's favor (the source is real and carries the
claimed substance, so nothing was fabricated), but the class label and any
decision that treated S134 as unreachable are wrong. The row's own flip
condition — a hand-check that fetches the cited source — is now satisfied.

## Related defect (one line, same DOI, different register)

The campaign's published recheck for this DOI,
`shokuknow/lanes/tameshi/round4/SOURCES-PROPOSED.md:19` (repeated
`KNOWLEDGE-PROPOSED.md:15`),
`aaron papers fetch 10.1145/351240.351266 | tr -d ' \n' | grep -c 'aids the Haskell programmer in formulating and testing properties of programs'` (expect 1),
cannot return 1 as written: `tr -d ' \n'` deletes every space in the haystack
while the needle keeps its spaces. Measured: returns `0`; the space-normalized
needle returns `1`. The recheck is vacuous-false and can never green-light.

## Residual risk

- S113 (`10.1145/3540250.3558911`) and S123 (`10.1109/TSE.2026.3685588`) share
  the same prose class in `corpus/lessons/round-39.md:33` and were not tested
  here (assignment is S134). S123's DOI is already shown open via its arXiv
  carrier by `shokuknow/merge/tameshi/SOURCES.append.md:91` (row S193), so the
  class is suspect there too.
- `aaron` resolves this DOI via the `scihub` tier; availability is
  channel-dependent and may drift. The Cloudflare 403 at `dl.acm.org` is
  reproducible today, so the original scout was not fabricating the failure —
  only the campaign's own channel ledger (`CHANNELS.md`) contradicts the
  register's "could not be fetched".

## Bounds kept

No edits to the lane checkout, `.ufo/state`, shokuknow, or any register. All
fetches ran in `/tmp/tameshi-r40-ReviewQ134/`. No installs were needed (`aaron`
already at `~/.local/bin/aaron`); no pacman was run.

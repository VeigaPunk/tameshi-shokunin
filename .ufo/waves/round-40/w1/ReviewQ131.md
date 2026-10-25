# ReviewQ131 — hand-check of quarantined S131

seat: reviewer (depth), round 40 wave 1
row: `/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md:29` (read-only)
verdict: **REFUSE as pinned — `could-not-be-fetched` class. Unreachable, not fabricated; claim independently verified verbatim.**

## The row

`S131 | Comparing and Merging Files (GNU Diffutils manual, version 3.12) — https://www.gnu.org/software/diffutils/manual/html_node/Invoking-diff.html | docs | A | … | §13 "Invoking diff", the exit-status paragraph, @ GNU Diffutils version 3.12, 12 January 2025, node page fetched 2026-10-23 | a comparison's exit status is a three-valued verdict — 0 no differences, 1 some differences, 2 trouble — so a golden-file check that treats every non-zero exit as "different" loses the error class | mined | 2026-10-23 | 365d — curl -fsSL '…/Invoking-diff.html' | grep -c '2 means trouble' (expect 1) | corpus/knowledge/r3-golden-comparison-vendor-verdict.md`

## Fetch attempt (fails from this host)

```
curl -fsSL --max-time 60 'https://www.gnu.org/software/diffutils/manual/html_node/Invoking-diff.html'
→ curl: (28) Connection timed out after 60001 milliseconds
```

Also timed out: `curl -4` (20 s), `curl -6` (20 s), `curl --resolve www.gnu.org:443:209.51.188.116` (15 s), and the harness reader (`Method: failed / The operation timed out`). `curl -fsSI https://www.gnu.org/` itself times out at 15 s while `curl -fsSI https://ftp.gnu.org/` and `https://www.tensorflow.org/` exit 0 — the failure is specific to the www.gnu.org web host, matching the lane's own records (`corpus/SOURCES.md:106,395,400,423`: gnu.org Bash manual pages timed out on 2026-10-23/24; S097/S104 were repinned to Savannah-hosted sources for exactly this reason). The row's own recheck command therefore cannot produce its expected output; the anchor's "node page fetched 2026-10-23" cannot be reproduced from this lane.

## Claim verified verbatim on two carriers

1. Wayback snapshot of the exact cited URL, `web.archive.org/web/20260209160757/https://www.gnu.org/software/diffutils/manual/html_node/Invoking-diff.html` (sha256 `267a21a8ad8af88c5b3e407835ba5a1ddecc7545262a38b935d9c4b3b22bb5ea`; copy in `/tmp/tameshi-r40-ReviewQ131/s131-wayback.html`). Page is titled "Invoking diff (Comparing and Merging Files)"; tag-stripped text contains, verbatim: "An exit status of 0 means no differences were found, 1 means some differences were found, and 2 means trouble." — `grep -c '2 means trouble'` → 1, matching the recheck expectation.
2. Official release source: `https://ftp.gnu.org/gnu/diffutils/diffutils-3.12.tar.xz` (sha256 `7c8b7f9fc8609141fdea9cece85249d308624391ff61dedaf528fcb337727dfd`). `@node Invoking diff` at `doc/diffutils.texi:3743`; the same sentence at `doc/diffutils.texi:3783`. This is the versioned primary source behind the cited HTML page — the anchor's "version 3.12, 12 January 2025" checks out.

The teaches cell follows from the verified sentence: exit 2 is a distinct "trouble" class, so a harness that collapses nonzero exits into "different" discards it. Not an overclaim. The `used-by` target `corpus/knowledge/r3-golden-comparison-vendor-verdict.md` exists in shokuknow merge staging (`/home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge/corpus/knowledge/r3-golden-comparison-vendor-verdict.md`, header cites S131 and reproduces the same quote) but is not in the lane corpus — consistent with a quarantined, never-adopted row. No id collision: lane `corpus/SOURCES.md` rows run S001–S108; S131 is absent.

## Verdict and flip

Refuse to present: the pinned locator `www.gnu.org/.../Invoking-diff.html` times out from this host on every attempt, so the row is `unreachable` under the round-38/39 convention (prose fetch-failure class, not fabrication). Flip path — the claim is confirmed and needs only a reachable carrier: repin the anchor to the versioned upstream source (e.g. `doc/diffutils.texi` @ diffutils-3.12 from `ftp.gnu.org`, sha256 `7c8b7f9f…227dfd`, node `Invoking diff` :3743, sentence :3783), or fetch the rendered node page via a reachable mirror, then re-run the row's recheck command. Note the content is already covered in the lane by S105 (POSIX diff spec, adopted round 38, `corpus/knowledge/golden-comparison-verdict.md`), so S131's added value is vendor-side confirmation of the same three-valued verdict.

## Evidence / scratch

/tmp/tameshi-r40-ReviewQ131/ — `s131-wayback.html`, `diffutils-3.12.tar.xz`, `diffutils-3.12/`, `wayback.json`. No lane checkout, index, or shokuknow mutation. No tool installs.

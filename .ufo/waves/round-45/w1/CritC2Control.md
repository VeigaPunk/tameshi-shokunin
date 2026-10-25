seat: CritC2Control

# C2 counter — cheapest pass attack (CTL_E relabel)

Item: attack the C2 counter for a cheap pass. All scratch under
/tmp/tameshi-r45-CritC2Control/ (a), b, c, d, e). No tools installed
(operator rule satisfied: nothing needed; system python3/git used).
Lane untouched except this report file.

## Setup (reproducible)

    D=$(mktemp -d /tmp/tameshi-r45-CritC2Control/scratch.XXXXXX)
    git -C "$D" init -q
    git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin archive \
      3310e7be803516ca5934b4e949d91bcec824b179 | tar -x -C "$D"
    git -C "$D" add -A && git -C "$D" -c user.name=crit -c user.email=crit@local commit -qm base
    # toplevel == $D verified before first commit

Counter run identically for every variant (self_pin=1 everywhere — counter
file untouched):

    python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-45/coverage/measure.py \
      --lane <D> --rev <commit>

## Results

| variant | output | exit |
|---|---|---|
| BASE (freeze only) | C2_R45: self_pin=1 rows=0 entries=0 indexed=0 row_ids=- C2_R45_PASS=false | 1 |
| CTL_E plain (reproduce receipt `controls-at-base.stdout:7`) | rows=2 entries=0 indexed=0 row_ids=S256,S257 C2_R45_PASS=false reasons={"verified-at": 2} | 1 |
| a) CTL_E + only `verified-at: 2026-10-25` in copied package entries | REFUSED …order-and-seed.md no located quote; ENTRY …primer-independence.md; rows=2 entries=1 indexed=1 C2_R45_PASS=false | 1 |
| b) a) + one cosmetic newline inside the copied quote | ENTRY both; rows=2 entries=2 indexed=2 C2_R45_PASS=true | 0 |

Variant b) passes the deciding counter. Its entire delta over the read-only
package entries (diff of adopted vs package, both files) is:

    - source: S202→S256 / S203→S257  (id remap, one token)
    - verified-at: 2026-10-24 → 2026-10-25  (one token)
    - (b only) one newline removed inside the copied sentence
      "the random seed value, such that you can reproduce an order-related
      test failure later" — purely presentational

Nothing else differs. The `recheck:` line still self-describes the copy as
"opened 2026-10-24" (adopted file `corpus/knowledge/r8-gtest-order-and-seed.md:3`,
`r8-gtest-primer-independence.md:3`). Bodies, inferences, quotes — all
byte-identical to the package (authored 2026-10-24).

Snapshot blobs are byte-identical to the freeze copies
(sha256 advanced=05546ed6…, primer=03d756ab…, testing=44c56c61…). Nothing in
the repo records a live fetch on 2026-10-25 or any verification act: git
stores no fetch time; the counter never touches the network.

## Why as-specified relabel (a) already almost passes

The counter's quote check (`measure.py:108-112`) uses
`QUOTE_RE = r'"([^"\n]{10,400})"|\u201c([^\u201d\n]{10,400})\u201d'`
— capture cannot span a newline. The package author wrote the advanced.md
quote across two lines, so it is invisible to the regex; the primer quote
happens to sit on one line. One line-wrap change toggles an entry between
REFUSED and ENTRY. This is calibration fragility, not a semantic gate.

## Do-nothing control or real adoption work?

Mixed, and the counter cannot tell the halves apart.

- Structural half (rows, snapshots, index): real *output*, mechanically
  assembled. Rows S256/S257 are the package S202/S203 rows with id remap
  (`SOURCES.append.md:56-57` → `SOURCES.md:464-465`), snapshot blobs copied
  from the freeze commit, README line appended
  (`corpus/README.md` tail). Zero new sourcing, zero live verification, but
  the artifacts exist and satisfy the counter's structural checks.
- Grounding half (the "re-grounded knowledge entry" sentence): do-nothing.
  The entry is relabeled, not re-grounded: only the date token changed; no
  fetch, no re-read, no re-derivation. Variant b) passes while the entry is
  99.9% package text and self-contradicts about its open date.

## What distinguishes re-grounded from relabeled, and does the counter check it?

Contract sentence (`contract.json:34`): "each cited by a re-grounded
knowledge entry (verified-at 2026-10-25, listed in the row's used-by,
carrying a located 6-25-token quote of the cited snapshot)". "Re-grounded"
names an *act* — someone verified the entry's claims against the snapshot
bytes on 2026-10-25. The machine-checkable proxies the counter inspects are
exactly the parentheticals: verified-at >= 2026-10-25 (`measure.py:100-102`),
quote located in the snapshot (`:108-112`), used-by membership (`:105`),
provenance trio (`:98-104`). All are output strings; all are forgeable
without performing the act. The counter checks none of the act's evidence.

Contrast with C1: C1 requires a snapshot "fetched on/after 2026-10-25" and a
quote "located AFRESH … (never copied from the row's own cells)", plus an
agree verdict by a non-author falsify-wave seat (`contract.json:21`) — a
second-party attestation C2 lacks, and even C1's fetch date is a stored field
(`freshness/measure.py:14,62`), not cryptographic proof.

## Recommendation for L1's Gate block

The deciding counter run alone proves nothing about grounding. Gate must show,
per entry, receipts of the act:

1. Counter stdout + exit at the deciding rev (full line, REFUSED/ENTRY
   lines, `C2_R45_PASS=true exit=0`).
2. Live-fetch receipt per snapshot on 2026-10-25: `curl -fsSL <raw URL> | sha256sum`
   captured at fetch time, matching the committed blob hash
   (05546ed6… / 03d756ab…) — proves the snapshot is the live bytes of this
   date, not a package copy.
3. The recheck commands actually run on 2026-10-25 (`curl -fsSL … | grep -c '<quote>'`
   → non-zero), matching the cited quoted sentence(s) — the entries' recheck
   lines currently describe 10-24 runs.
4. The adoption diff vs the package entry (id remap + verified-at + any body
   change), plus a statement of what was re-derived vs copied.
5. jj/lane history showing the entry edits landed after freeze.

Items 2+3 are load-bearing; 1/4/5 are context. Knowing git cannot timestamp
an act, add hardening ideas: tie the recheck grep pattern to the quoted
sentence (currently unrelated), and match quotes against the raw snapshot
line-break-independently so presentational wraps don't toggle acceptance.

## Smallest safe correction

Require the Gate block to include 2+3 above before declaring C2_R45_PASS;
optionally tighten the counter to reject entries whose body is byte-equal to
a package source modulo id/date (a cheap dedup check that would have refused
both variants here).

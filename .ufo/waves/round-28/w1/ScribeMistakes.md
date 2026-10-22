# ScribeMistakes — candidate `## Mistakes` rows for round-28.md

Scope: draft-only. These are candidate rows for the L1 integrator to place
(or reject) in `corpus/lessons/round-28.md` `## Mistakes`. Nothing here was
committed; no product file was touched. Format follows the existing row in
the round-28 lesson: **class** · **evidence** · **captured-by** · **fix**.

Sources read:

- `corpus/lessons/round-27-verifier-spotcheck.md` (working tree; its routed
  defects § is at lines 185–211).
- `corpus/lessons/round-26-verifier-spotcheck.md` (working tree; routed
  defects at lines 214–237).
- `git show b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a:corpus/lessons/round-28.md`
  (the draft lesson: `## Gate` records the S059 re-open, the S092
  draft-and-remove, and the appended `Next unused id: S092.`; `## Mistakes`
  holds one row).
- `git show b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a:corpus/QUALITY.md`
  (admission bar 1–5, criteria 6–54 with corrections).

Context note (wave fact, not lesson text): the SOURCES edit at b05d2ee8
drifted 10 credited sections (`input-drift:corpus/SOURCES.md`), leaving 14
sections uncovered at the content revision; that is the input-drift
mechanism the lesson's row 1 already names.

## Already-present row

Row 1 in the drafted lesson (self-inflicted credit loss; evidence
`.ufo/evidence/round-28/append-probe.txt`; captured-by `none`; fix = land
widely read files before the content revision) covers the input-drift
mechanism. Candidates below add the other mistakes the three sources show.
Numbering continues at 2.

## Candidate rows

2. **class:** duplicate source registration — a new SOURCES id was drafted
   for a URL the corpus already carries. **evidence:** lesson `## Gate` at
   b05d2ee8 ("a first draft added S092 for the same URL, the census flagged
   W04 duplicate URL, and the draft row was removed before any commit");
   the same detector has flagged six older rows
   (round-27-verifier-spotcheck.md:149-153). **captured-by:** none (caught
   by `scripts/sources-census.sh` warning W04, not by a QUALITY criterion).
   **fix:** `grep` `corpus/SOURCES.md` for the URL before minting an id, and
   when a row already exists re-open it (`used-by` append plus a dated
   `## Gate` record) instead of drafting a new row.

3. **class:** corrections landed after the reads that could credit them —
   a section edited after its bucket's cold reads stayed uncovered at the
   head. **evidence:** round-27-verifier-spotcheck.md:45-59 (three sections
   corrected in `af7b70d` never re-read; "Round-21 gate/probe registry"
   gap-blocking; `covered=60/64 restraint=6 box3_mismatch=1` at head);
   routed item 1 (:187-190). **captured-by:** QUALITY 53 — the falsifier
   `c1-measure.py` exits 1 at both `e08444d3` and `91edf9cd`, which is how
   the miss surfaced. **fix:** land content corrections before the content
   revision, then dispatch fresh independent reads of exactly the edited
   sections and run the strict monitor at the landed head.

4. **class:** stale no-harm receipt — a gate receipt predates the last
   edits to the bytes it vouches for. **evidence:**
   round-27-verifier-spotcheck.md:132 and :191-193 (registry receipt at
   `2227d83`; SKILL registry rows edited later in `b1cc95e`/`af7b70d`;
   round-26 item 3 still only partly met); the same shape at
   round-26-verifier-spotcheck.md:222-224 (`2b064cf` argv edit, no
   committed receipt after). **captured-by:** partially QUALITY 41
   (installed measurement must begin no earlier than edit end) and QUALITY
   40 (a historical receipt is not a current reading). **fix:** run the
   instrument once more after its last edit in the round, or name the
   missing at-head run as open debt in the report.

5. **class:** stale corpus pointer plus a dropped bookkeeping convention —
   the SOURCES footer idled two ids behind and the search-log note was
   skipped. **evidence:** round-27-verifier-spotcheck.md:194-196
   (`corpus/SOURCES.md:338` still read "Next unused id: S090" after S090
   and S091 landed; unlike rounds 23–26 no "bounded lookup" search-log
   note was appended). **captured-by:** none. **fix:** append the next-id
   line in the same commit that adds the rows (done at b05d2ee8: "Next
   unused id: S092." appended, stale S090 line kept per criterion 35), and
   either keep the bounded-lookup note or record where the record moved
   (round 27 used the lesson `## Gate`).

6. **class:** criterion text stronger than its falsifier — the rule claims
   a property the counter cannot check. **evidence:**
   round-27-verifier-spotcheck.md:199-201 (QUALITY 53's "independent" is
   not checkable by the counter; QUALITY 54's named digest is not
   provenance; S012's tier needs a supersedes row if the tier-B call is
   revised). **captured-by:** none (a criteria-authoring mistake; the
   remedy is an appended narrowing amendment like criterion 41's "This
   validates declared receipt metadata, not producer authenticity").
   **fix:** append dated amendments stating what each counter actually
   validates; never silently rewrite the criterion.

7. **class:** aggregate counts mix units or populations — a headline
   number pairs the wrong numerator with its denominator. **evidence:**
   round-27-verifier-spotcheck.md:204-208 (SCORECARD "51 wave seats
   cold-read the 39 uncovered sections" when 39 of the 51 seats did;
   "15 real defects" = 13 pre-existing plus 2 the L1's own corrections
   introduced, :76-79). The same shape in
   round-26-verifier-spotcheck.md:100-110 (a "calibration" count of 3 items
   whose qualifying self-assessment population is 1). **captured-by:**
   partially QUALITY 38 (a count names its unit). **fix:** every aggregate
   states its population on the same line — "39 of 51 seats", "13
   pre-existing plus 2 self-introduced", "1 of 3 labels in scope".

8. **class:** rewrite that hides an append — re-serializing an
   append-only file makes `git diff` unable to show the addition.
   **evidence:** round-27-verifier-spotcheck.md:71-74 (ledger entries
   304 → 342 → 354 and append-only as data by `json.load`, but the file
   was re-indented 19,925 → 23,326 lines); routed item 7 (:206-208).
   **captured-by:** QUALITY 35, extended — its numstat check is written
   for corpus prose, and the same "an append must show as an append" rule
   applies to the append-only ledger. **fix:** append entries in the
   file's existing serialization style; never re-indent or re-serialize
   retained bytes.

9. **class:** instrument and judged data landed in one commit — commit
   order cannot separate before from after. **evidence:**
   round-27-verifier-spotcheck.md:106-123 (`c2-measure.py` check 3
   re-worded and the S012 row it judges edited in the same commit
   `2227d83`; the target value was unchanged and the old condition was
   redundant, so the verifier ruled it not narrowed, but the timing point
   stands). **captured-by:** none (nearest: QUALITY 41's ordered
   measurement intervals, which is about edit/measure windows rather than
   commit order). **fix:** land a counter amendment and the data edit it
   measures in separate commits, amendment first, so "before the data
   edit" is demonstrable by commit order.

10. **class:** unparseable seat output consumed a read slot — a
    non-conforming receipt is counted as a failed read, not as malformed
    evidence. **evidence:** round-27-verifier-spotcheck.md:67-70 (Read08
    unparsed → gap-blocking; 27 credited, 12 failed of 38).
    **captured-by:** none (adjacent to QUALITY 45's "a report's presence
    never changes a failed callback", which is about seat completion, not
    receipt shape). **fix:** check receipts against the ledger schema when
    they land; bounce a malformed one back to the seat while the wave is
    still open.

11. **class:** reading a monitor number beside its contradiction — a
    self-assessment row asserted a score the lane's own monitor refuted at
    the same revision. **evidence:**
    round-26-verifier-spotcheck.md:106-110 (SCORECARD C2 row "numeric
    8 → 8" while the monitor read restraint 6 at the same revisions);
    routed item 2 (:219-221) required an appended correction.
    **captured-by:** QUALITY 53 second clause ("a calibration no-harm
    reading names the strict monitor at the landed head"); admission bar 3.
    **fix:** run the strict monitor before writing the measured table, and
    when a landed row is later contradicted, append a dated correction —
    never rewrite the row.

12. **class:** counter gameable by unbound evidence — a check passed on
    prose tokens and receipts not tied to the bytes it was judging.
    **evidence:** round-26-verifier-spotcheck.md:85-86 and :225-228
    (routed item 4; seat MutateC2Counter; QUALITY 51's receipt check did
    not tie a receipt to the tool bytes). **captured-by:** QUALITY 54,
    written round 27 to bind receipts to the sha256 of tool and input
    bytes (falsifier in `c2-measure.py`: "receipt not bound to probe and
    anchors bytes"). **fix:** every receipt-bearing counter verifies the
    digest of the instrument and inputs at the measured revision; a
    receipt from other bytes counts as absent.

13. **class:** runner missing an arithmetic invariant — a self-check did
    not verify that its leg counts sum to the declared total.
    **evidence:** round-26-verifier-spotcheck.md:229-231 (routed item 5:
    `tools/mutate-and-run.sh --regression` does not check
    `npass + nfail + nsetup == nlegs`); still open at
    round-27-verifier-spotcheck.md:202-203 (item 6). **captured-by:** none
    (named debt two rounds running). **fix:** add the leg-sum check to the
    regression path and a selftest case whose fixture breaks the sum.

14. **class:** summary line overstates a qualified finding — a heading or
    table cell drops the bound the body keeps. **evidence:**
    round-26-verifier-spotcheck.md:155 (entry heading "10/10 verdict
    predictions held" without the lesson's "9 falsifiable" qualifier);
    round-27-verifier-spotcheck.md:146-147 and :197-198 (README F8 row
    "independently anchored" while the entry bounds it to 3 of 4; the
    rejected inference "anchored_holes=4 shows the differential method is
    sound"). **captured-by:** none (nearest: QUALITY 33's "names the
    commands it did not trace" spirit — a claim must carry its bound).
    **fix:** carry the qualifier into the summary cell itself
    ("9 of 10 falsifiable predictions", "3 of 4 anchored"), or route the
    overstatement as a finding the same round.

15. **class:** cross-lane routing without delivery proof — a routed
    finding was dropped by the receiving lane and the loss surfaced only
    at the next closure. **evidence:**
    round-27-verifier-spotcheck.md:209-211 (item 8: the round-26 routing
    of the four cite-check holes was dropped by kumitate R39-5, seat
    ConnectorOverlap). **captured-by:** none. **fix:** when a finding is
    routed cross-lane, record the receiving lane's ack or the named owner
    commit in the routing lane's lesson, so a silent drop is visible at
    the next spot-check instead of discovered by re-reading.

## Rows deliberately not drafted

- Operator commit `167c0e3` inside the round-27 range (spotcheck:32-33):
  explicitly noted as not a defect.
- "SHONEN not fully checkable by a non-author" (both spotchecks): a
  structural limit of the review, not a lane mistake.
- Amendment-1 substance (round-27 spotcheck:106-123): the verifier ruled
  the target was not narrowed; only the commit-order point survives, as
  row 9.
- Round-26 wave-2 cancellation: the harm it left is already expressed by
  rows 3 and 11 plus the lesson's existing row 1.

## Tooling

None installed or updated. Reads only: `read` on the two spot-check files,
`git show` at b05d2ee8 for `corpus/lessons/round-28.md` and
`corpus/QUALITY.md` (read-only, `GIT_OPTIONAL_LOCKS=0` not needed for
`git show` but no locks taken), `ls` on the report directory. No git write
commands, no `jj`, nothing run inside the lane beyond read-only plumbing.

## Limits

- `captured-by` assignments are my mapping of each mistake to the
  criterion text at b05d2ee8; rows 2, 5, 6, 9, 10, 13, 14, 15 are `none`
  because no criterion's falsifier covers the behavior (rows 4, 7 are
  partial analogies, marked as such).
- I did not re-run any monitor, census or counter; every evidence pointer
  cites the spot-check text or the lesson at the pinned revision.
- These are candidates for the L1 integrator; wording follows the existing
  row's bold-field style but is freely editable.

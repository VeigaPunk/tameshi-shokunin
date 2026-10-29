# T57W1ScoutSourceB — source candidate B: closure follow-through ledger

Round 57 wave 1 scout item: open ONE external primary source grounding C1's
practice — a ledger of review/postmortem action items tracked to closure with an
owner and a verifiable state, so that a record cannot run ahead of the tree.

## Accepted source (proposed new row S283)

- **Title:** Postmortem Culture: Learning from Failure — Google SRE Workbook, chapter 10 (Beyer, Jones, Petoff, Murphy; Google, 2018, online edition)
- **URL:** https://sre.google/workbook/postmortem-culture/
- **Access date:** 2026-10-28 local (2026-10-29 UTC at fetch, per `date -u`; receipt `fetched-sha256.txt`)
- **sha256:** `25b55c64c87976e77272f1ef8ee48f619e77cf3de3e6eb85398907d7e2f0bd22` (103,251 bytes, raw HTML as served)
- **Section anchor (primary):** §Key action item characteristics missing — `#key-action-item-characteristics-missing`
- **Primary verbatim quote (15 words):**
  > "Without a formal tracking process, action items from postmortems are often forgotten, resulting in outages."
  — §Key action item characteristics missing. Verified byte-exact in the fetched HTML (`grep -o`, receipts `quotes-verification.txt`).

Supporting verbatim quotes (all verified byte-exact in the same fetch):

- "Ideally, an owner is a single point of contact who is responsible for the postmortem, follow-up, and completion." (18 words) — §Missing ownership, `#missing-ownership`
- "If you reward engineers for writing postmortems, but not for closing the associated action items, you risk an unvirtuous cycle of unclosed postmortems." (23 words) — §Reward action item closeout, `#reward-action-item-closeout`
- "To our users, a postmortem without subsequent action is indistinguishable from no postmortem." — Ben Treynor Sloss, quoted in §Key action item characteristics missing → Note, `#note-1`

The chapter's worked example carries an Action Items table whose columns are
literally **Action Item / Owner / Tracking Bug** (§Good Postmortem) — owner plus
a bug-tracker ID is exactly the "owner + verifiable state" pair C1's rows
formalize as {seat, evidence[], commit?}.

### Why the Workbook and not the Book page (the preferred candidate)

The prompt's first candidate was the SRE **Book** chapter of the same title
(https://sre.google/sre-book/postmortem-culture/). I fetched it (sha256
`ef876f0a0f09a88f3acc3294ec24eb922751b0059cba8be271aa6fe8474656c5`, 55,113
bytes) and it does **not** ground the claim: its body text has no owner,
tracking, or closure language for action items. Every readable occurrence of
"track" on the page is the *next chapter's title* "Tracking Outages" (TOC +
footer nav); the closest review criterion is "Is the action plan appropriate and
are resulting bug fixes at appropriate priority?" — review-time adequacy, no
owner, no closure state. The closure-tracking content lives in the Workbook
chapter, which extends the same chapter for practitioners. So the accepted row
is the Workbook; the Book page is my documented rejected candidate (below). The
Workbook is still Google SRE primary, same chapter family, so the preference for
the SRE postmortem source is honored.

## Rejected candidate (opened, quoted, recorded)

- **Title:** Postmortem Culture: Learning from Failure — Google SRE Book, chapter 15 (online edition)
- **URL:** https://sre.google/sre-book/postmortem-culture/
- **Access date:** 2026-10-28 local (2026-10-29 UTC at fetch)
- **sha256:** `ef876f0a0f09a88f3acc3294ec24eb922751b0059cba8be271aa6fe8474656c5` (55,113 bytes)
- **Sounds relevant because:** identical chapter title to the preferred candidate; it is the canonical postmortem-culture text.
- **The line that shows it does not support the claim** (25 words, §Best Practice: No Postmortem Left Unreviewed, verified byte-exact in fetched HTML):
  > "Once those involved are satisfied with the document and its action items, the postmortem is added to a team or organization repository of past incidents."
  This gates the *document* on reviewer satisfaction and a repository — no per-item owner, no tracked-to-closure state, no verifiable state for individual action items.
- **Corroborating absence:** the page's full review-criteria list contains only "Is the action plan appropriate and are resulting bug fixes at appropriate priority?" (13 words, §Writing a Postmortem — tag-stripped verify) — adequacy at review time, not closure tracking; and a case-insensitive sweep of the fetched page finds every readable "track" token inside the navigation title "Tracking Outages" only (receipt `quotes-verification.txt`).
- **Flip condition:** the Book page gains action-item ownership/tracking/closure text (the Workbook already carries it, so no second fetch cycle needed).

## Also evaluated, supports the claim (alternate row, not opened this seat)

- **Atlassian Incident Handbook — Postmortems:** https://www.atlassian.com/incident-management/handbook/postmortems — sha256 `2644d1c97e06cc7f8f0f88065ed373a960997f6e48f81a1b46b76b0514a87369` (2,313,661 bytes, fetched same session).
- Verbatim (tag-stripped verify; the raw page duplicates it in responsive markup): "All postmortem actions must be tracked in Jira." — §How are postmortem actions tracked?, `#how-are-postmortem-actions-tracked`.
- It also names single postmortem owners accountable "until it's published" and a manager-reviewed report of incidents whose root causes are not yet fixed. This directly supports the claim; held as an alternate so the round opens one row per scout seat. If the L1 wants a second source row for C2-style enforcement (approval gates), this is the candidate.

## What the accepted source does NOT claim

1. **Not about code-review or verification-fixture ledgers.** The artifact is an incident postmortem in production ops; transfer to a routed-defect ledger is our analogy, not the source's claim.
2. **No tool mandate.** The example's "Tracking Bug" column implies a bug tracker but the chapter names no product (the Book page mentions Etsy's Morgue only in a footnote about postmortem repositories).
3. **No verifiable state machine.** "Completion"/"closeout" is cultural (FixIt weeks, leaderboards); no open/closed statuses, no evidence links — the lane's {status, evidence[], commit?} schema is our own formalization.
4. **No quantified effect.** The satellite-drain anecdote ("action items implemented from the original postmortem dramatically reduced the blast radius") is a single case, not a measurement.
5. **No close-before-publish requirement.** The good-postmortem example publishes with open tracked items; the lane's round-50 rule that every row must agree with the tree at measurement time is stricter than the source.

## Existing-row check on SOURCES.md and proposed row

Sweep (`receipts/sources-sweep.txt`): `grep -c -i -E "sre\.google|atlassian\.com|nist\.gov|postmortem|post-mortem|incident" corpus/SOURCES.md` → **0 matches** over 523 lines. No existing row on any candidate URL; rows S001–S282 cover mutation testing, flakiness, hermeticity, receipts/provenance — not corrective-action ledgers.

Proposed row (id S283 = next unused id per the file footer; L1 resolves concurrent-scout id conflicts). Drafted in exact 11-column format:

```
| S283 | Postmortem Culture: Learning from Failure (Google SRE Workbook, ch. 10) — https://sre.google/workbook/postmortem-culture/ | book | A | Google SRE's postmortem action-item ownership, tracking-bug and closeout semantics | §Key action item characteristics missing and §Missing ownership @ page fetched 2026-10-29 UTC (103,251 bytes; SHA-256 25b55c64c87976e77272f1ef8ee48f619e77cf3de3e6eb85398907d7e2f0bd22; snapshot T57W1ScoutSourceB-receipts/workbook-postmortem-culture.html) | postmortem action items without owners or tracking bugs are forgotten and outages repeat; a single owner is accountable for follow-up and completion; closeout itself must be incentivized (FixIt weeks, leaderboards) — the practice a routed-defect ledger formalizes | mined | 2026-10-29 | 365d | (L1 to wire: round-57 C1 routed-defect-ledger claim) |
```

- **Tier rationale:** A — primary, vendor-authoritative (Google's own workbook), verbatim-fetchable stable URL, byte-hashed at open.
- **Scope rationale:** scoped to postmortem action-item ownership/tracking/closeout semantics only — not incident response, not SLOs, not blamelessness policy.

### Suggested citation hook for the C1 claim (L1 to adapt)

> The routed-defect ledger is Google SRE's action-item discipline in miniature: items without an owner and a tracking handle get forgotten (S283), so every row carries its seat (owner), evidence paths and commit (tracking handle), and a status a counter can verify against the tree.

## Honesty and bounds

- **Access-date boundary:** fetch ran at local 2026-10-28 ~21:07, UTC 2026-10-29; both recorded; row `opened` uses the UTC date, consistent with S102's convention.
- **Unrun checks:** I did not run the C1/C2 counters (not my seat); the NIST/ISO corrective-action texts were not fetched (Google SRE was preferred and grounds the claim, so no NIST fetch was needed).
- **Bounds compliance:** no lane production file read-modified; writes limited to `.ufo/waves/round-57/w1/T57W1ScoutSourceB.md`, `.json`, and `T57W1ScoutSourceB-receipts/`. No git/jj commands anywhere. No tool installs needed (curl/python3/grep preexisting — nothing to record per the tooling rule).
- **Scratch:** `/fast/scratch/hyaku/tameshi-r57/T57W1ScoutSourceB` removed after this report; page snapshots preserved in the receipts dir.
- **Receipts:** `fetched-sha256.txt`, `accepted-source-sha256.txt`, `quotes-verification.txt`, `sources-sweep.txt`, `extract.py`, `workbook-postmortem-culture.html`, `book-postmortem-culture.html`, `atlassian-postmortems.html`.

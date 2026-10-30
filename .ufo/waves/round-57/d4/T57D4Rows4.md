# T57D4Rows4 — documentary review

Axes: semantic status accuracy; fix-commit attribution; evidence provenance. Documentary/source review only. No candidate gate, code, tests, builds, exploit, receipt generation, integration or admission performed. No tools installed. Candidate integration remains **UNVERIFIED**.

## Findings (severity order)

### Medium — R54.7 candidate `fixed` is unsupported

Candidate `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/integrate/candidate-ledger.json:1778-1795` labels both status and status_at_base `fixed`, crediting `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`. That commit supports a **partial record correction**, not complete disposition repair. Original `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-54-verifier-spotcheck.md:120` requests correcting the report's deletion claim to a rename. `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-54/w2/T54W2Sent01.md:185-189` still describes the deletion as unstaged and awaiting a lane commit. The panel also reports the fleet copy's stale wording; that copy was not independently read here and is outside lane write scope.

The blind panel returns **open**, explicitly distinguishing the corrected SCORECARD/lesson from remaining report residue (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w2/T57W2PanelR546R547.json:11-14`; detailed evidence in its sibling `.md:21-33`). The wave-3 proposal agrees: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3RowR546xR547/rows.json:29-51` sets both statuses `open`, with no claimed complete fix commit. That proposal is supported as a conservative documentary disposition; the older candidate `fixed` row is not.

### Medium — R54.6 candidate credits a record restatement as the repair

Candidate `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/integrate/candidate-ledger.json:1758-1775` credits `9cf0146b...` and labels both statuses `fixed`. Its own note acknowledges the actual delivery sweep was `ff2a821a1e83acd92bb4d62bad15f380973a55ea`, before routing. Original `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-54-verifier-spotcheck.md:118` already states that the closure swept the files byte-identically; the remaining prospective requirement is not leaving seat deliverables uncommitted again. Thus the quoted correction establishes present tracking, not a newly effected delivery repair or proof of the prospective invariant.

The blind panel returns **declined**, explaining the closure-owned pre-routing sweep and separately routed recurrence (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w2/T57W2PanelR546R547.md:9-19`, `.json:6-9`). The wave-3 proposal adopts **declined/declined** and does not claim `9cf0146b...` as a fix (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3RowR546xR547/rows.json:3-26`). That proposal is supported as a reasoned refusal to credit a new lane fix. The narrower fact that all three historical deliverables are now committed is supported; it must not be confused with the candidate's fix attribution. This finding does not depend on counter acceptance.

## Read-only sweep: commands and observed output

1. `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff 5e3569969b532310d2b8a3d130901757a3df356b adf87899c70d616140a81185a8f9acbbdfb30392 -- corpus/routed-defects.json`

   Output: **empty**. Direct `git ... show adf87899c70d616140a81185a8f9acbbdfb30392:corpus/routed-defects.json` returned the round-50 ledger ending at R49.6. Tool grep of the current absolute lane ledger for `R54\\.6|R54\\.7` returned **No matches found**. Consequently neither assigned row is actually landed in that pinned production ledger; this report distinguishes the unverified integration candidate from the wave-3 row proposal.

2. `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --format= --unified=3 9cf0146b94ddba12d454ebf7288ce6e5c5d535bb -- SCORECARD.md corpus/lessons/round-55.md`

   Relevant output:

   ```text
   +**ER-R54-6 - round work uncommitted at closure.**
   +Old: three seat deliverables untracked when the round filed.
   +Corrected: they are committed; the sweep that committed them is `ff2a821`.
   +**ER-R54-7 - an imprecise forged-file disposition.**
   +Old: "the deletion lands in 7fa9a5e0". Corrected: the file was **renamed** into
   +`.ufo/waves/round-54/w2/T54W2Sent01-receipts/forged-reader.json` at `7fa9a5e`
   ```

   This supports record corrections, not the missing complete repair claims.

3. `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin log --format=%H 650987a0d6fc285b37f0f9e63a3aae864af9cd5a..adf87899c70d616140a81185a8f9acbbdfb30392 -- .ufo/waves/round-54/w2/T54W2Sent01.md .ufo/waves/round-54/w2/T54W2Sent03.md .ufo/waves/round-54/w2/T54W2Sent03-receipts/c1committed-positive.stdout .ufo/waves/round-54/w2/T54W2Sent03-receipts/rejection-attribution.txt`

   Output: **empty**. These surfaces were untouched after routing through C0b.

Existing command/output evidence was also read, not rerun: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w2/T57W2PanelR546R547-receipts/r54-6-tracking.txt:4-20` records tracking exit 0 and the closure sweep identity; sibling `r54-7-residual-at-base.txt:3-15` records the stale seat line, identical blobs at rename/correction/base and no supersession marker.

## Residual risk and verification gaps

- The wave-2 repair report claims both statuses remain fixed (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w2/T57W2RepairR546xR547.md:15-21`), but its R54.7 rationale proves the rename, not correction of all report residue. The independent panel and wave-3 proposal explicitly cover that distinction.
- No completed top-level wave-3 writer `.md` or `.json` was present at inspection; the available writer artifact is `rows.json`. The inspected stage corpus directory contained no listed ledger file. No claim of completed integration is warranted.
- LSP unavailable: `read xd://lsp` returned `No such tool: xd://lsp`; no semantic references/definition/diagnostics facility was available. Literal text inspection is not presented as semantic caller proof. This task concerned documentary JSON/Markdown, not runtime callsites.
- No runtime, continuity, saturation, gate or counter result is certified. Historical receipt contents are attributed to their authors, not rerun results.

## Self-evaluation

Accuracy 4/5 (fleet stale-copy evidence is panel-attributed, not independently inspected); completeness 4/5 (writer final report absent); clarity 4/5 (multiple candidate surfaces require explicit distinction); actionability 4/5 (recommendations only, no admission); conciseness 4/5 (command evidence retained for auditability). Overall 4.0/5. Improvement: attach this distinction to any later integrated revision before claiming row agreement. The user should agree this is a documentary recommendation, not a pass.

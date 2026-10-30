# T57D4SourceB — S284/S285 documentary review

## Scope and axes
Axes: quote fidelity, anchor reproducibility, admit/reject scope, historical/current evidence separation. Documentary analysis and external documentation GET only; no gate execution, tests, builds, production edits, credentials, or admission. Candidate integration remains UNVERIFIED.

Reviewed the actual base→C0b source/lesson diff and the current local continuation. Commands below are literal tool invocations or the one read-only shell command; outputs are excerpts, not invented execution receipts. LSP discovery `read("xd://lsp")` returned `No such tool: xd://lsp`; no semantic server was available. Text searches below are literal fallback, not semantic proof. No installation or upgrade.

## Findings, severity order

### P2 — S285's exact historical source anchor cannot be reproduced from the retained snapshot

`/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md:160` pins a 2026-10-28 HTML snapshot, `2644d1c9…a87369`, at `.ufo/waves/round-57/w1/T57W1ScoutSourceB-receipts/atlassian-postmortems.html:42055`. The current Gate says its historical record comes from retained source receipts (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-57.md:49-50,58,60-61`). That named HTML is missing.

Evidence commands and output:
- `read("/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w1/T57W1ScoutSourceB-receipts/atlassian-postmortems.html:42055")` → `Path '/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w1/T57W1ScoutSourceB-receipts/atlassian-postmortems.html' not found`.
- `read("/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w1/T57W1ScoutSourceB-receipts/")` → seven entries: `sources-sweep.txt`, `quotes-verification.txt`, `accepted-source-sha256.txt`, `extract.py`, `book-postmortem-culture.html`, `workbook-postmortem-culture.html`, `fetched-sha256.txt`; no Atlassian HTML.
- Existing `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w1/T57W1ScribeSourcesRow-receipts/quote-location-and-sha.stdout:5,12,19` records the historical digest, `42055:</styl`, and a truncated extracted quote. These are useful secondary records, not the missing bytes or a reproducible line-42055 anchor.

Impact: fresh GET supports the quote's existence today, but cannot establish the exact old digest, byte count, or historical line anchor. Recommendation: recover the exact retained snapshot if available, or append an honest new access/locator record distinguishing live verification from historical hash evidence. Do not claim that the historical snapshot was reverified.

### P3 — S285's short quote drops the source's incident-severity restriction

`/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-57.md:58` closes its quote at “every incident”; the full source continues “with a severity of level 2 or higher.” The staged predecessor at `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w1/T57W1ScribeSourcesRow/gate-block.md:9` does the same.

Evidence command: `read("https://www.atlassian.com/incident-management/handbook/postmortems:15-28")` → under `Incident postmortems`: “We practice [blameless postmortems](https://codeascraft.com/2012/05/22/blameless-postmortems/) at Atlassian to ensure we understand and remediate the root cause of every incident with a severity of level 2 or higher.” The historical extraction at `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w1/T57W1ScribeSourcesRow-receipts/quote-location-and-sha.stdout:19` also continues `every incident with a severity o` (with nonbreaking whitespace).

Impact is limited: S285 remains rejected, so this does not establish a wrongly admitted reliability claim. It does broaden the apparent practice being quoted. Recommendation: append a located correction including the severity restriction, using a shorter excerpt if necessary to meet the 25-word bound.

### P3 — The unqualified “no ... cited evidence” rejection wording is broader than the inspected page supports

`/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md:160` says “with no outcome data or cited evidence”; the predecessor Gate repeats that wording at `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w1/T57W1ScribeSourcesRow/gate-block.md:9`. The current lesson's narrower “without measured outcomes” (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-57.md:58`) avoids this overstatement.

Evidence command: `read("https://www.atlassian.com/incident-management/handbook/postmortems:228-240")` → `Postmortem actions` cites a Google presentation (https://www.usenix.org/conference/srecon17americas/program/presentation/lueder) and article (https://www.usenix.org/system/files/login/articles/login_spring17_09_lunney.pdf), stating “which we use at Atlassian to prompt the team.” The opening paragraph also links the blameless-postmortem discussion. Thus the page is not citation-free. This does NOT show measured process outcomes or invalidate the lane's relevance-based rejection.

Recommendation: append a scope correction: no cited measured outcome supporting the claimed effectiveness was established by this review, rather than no cited evidence of any kind. Because the old HTML is missing, today's GET cannot prove precisely which links were present in the old bytes.

## Supported comparisons (not runtime passes)

- `read("/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w1/T57W1ScoutSourceB-receipts/workbook-postmortem-culture.html:660-670")` → line 664 is `<h6 class="subheaders-small jumptargets" id="animated-language">Animated language</h6>`; line 666 begins “A postmortem is a factual artifact that should be free from personal judgments and subjective language.” This exactly supports current Gate `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-57.md:57`. Literal live-source search `grep(pattern="animated-language|A postmortem is a factual artifact", path="https://sre.google/workbook/postmortem-culture/:raw")` returned the same heading at 664 and sentence at 666. The SOURCES row's lowercase initial `a` is a minor capitalization change, not a substantive scope error.
- S284's 16-word sentence is complete; its A tier is explicitly limited to Google's own practice. Its queued status/unused `—` does not assert downstream mining. Both row 159 and Gate line 57 expressly exclude causal reliability evidence. The live chapter's opening assertion “Our experience shows ...” is not silently promoted by those records.
- S285's `Incident postmortems` and `Postmortem process` headings occur in the live GET. Its rejected status, retained row, and flip condition are mutually consistent. Product-specific applicability is a lane curation judgment, not a measured external fact.
- `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff 5e3569969b532310d2b8a3d130901757a3df356b adf87899c70d616140a81185a8f9acbbdfb30392 -- corpus/SOURCES.md corpus/lessons/round-57.md` → adds S283–S285; C0b's new lesson has 36 lines ending in corrections and no Gate. The current local continuation at lines 47–63 supplies a Gate afterward. The current documentary repair is not evidence that C0b already contained it.

## Residual risk and verification gaps

Only documentary fidelity was reviewed. No candidate gate, counter, census validator, monitor, resume path, or alternate runtime was executed. No canonical-runtime, rerouting, saturation, 64/64 monitor, C1/C2, or admission conclusion follows. Live web content is mutable; no fresh hash-to-historical-byte identity was established. The missing S285 snapshot is the principal reproducibility gap. References to external articles were observed, not followed or substantively evaluated. No further actionable source-scope finding remains from this sweep.

Self-evaluation: accuracy 4 (old S285 bytes unavailable); completeness 4 (historical digest cannot be reproduced); clarity 4 (historical/live distinction requires detail); actionability 4 (snapshot recovery depends on retained evidence); conciseness 4 (command/output evidence makes the report longer). Mean 4.0/5. Improvement priority: recover the exact historical S285 snapshot and append scope-accurate corrections. No production edits made.

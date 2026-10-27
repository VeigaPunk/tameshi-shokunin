# T52W2RevCorr0104 — falsifier review of Corr01–04

Scope: the four entries in the CAND0 ledger `.ufo/evidence/round-21/coldread/ledger.json` `corrections` array, each matched to its named reader and read_rev `02ec217c4d0afabe727fde2e261b7951d28fb4e9`. Command for ledger evidence: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show bcba8924894216268afc4171f06eb8c28e912b46:.ufo/evidence/round-21/coldread/ledger.json | jq '.corrections[0:4]'`. Reader lines below are shown by `nl -ba .ufo/evidence/round-51/coldread/reads/T51W2ReadNN.md` (or `read` at the stated ranges). I compared each correction's claimed finding to reader-recorded falsifications, excluding statements explicitly classified as holds or disclosed historical notes.

## Corr01 — T51W2Read01

**Over-counted:** the correction counts the unsupported provenance aside (“corrected in round 27, seat Read03”) as a reader finding. Reader01 says its two stale pointers are the findings at lines 7–10, then reports the endpoint-identity statement holds at line 14; the provenance aside appears only as residual unverified prose at line 75, not as a recorded NOT-holding statement. The two stale-pointer findings are valid (reader lines 9–10). **Missed:** none. **Verdict: over.**

Evidence: `T51W2Read01.md:7-14,75`; correction record `T52W1Corr01.json` finding 3. Command: `nl -ba /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-51/coldread/reads/T51W2Read01.md`.

## Corr02 — T51W2Read02

**Over-counted:** its sole finding says the section's claim about historical probes' sensitivity re-runs is wrong. Reader02 explicitly labels the cited SCORECARD pointer “holds” at line 127 and confines the concern to a scope note: one pointer is narrower than the plural claim, while the scratch-dependence claim itself holds for both probes (lines 128–129). This is not recorded as a NOT-holding statement; it is a disclosed scope qualification. **Missed:** none located among the reader's recorded falsifications; the reader's pointer inventory finds no other false statement (lines 93–143). **Verdict: over.**

Evidence: `T51W2Read02.md:127-129` (full pointer discussion also lines 174–181); correction record `T52W1Corr02.json`. Command: `nl -ba /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-51/coldread/reads/T51W2Read02.md`.

## Corr03 — T51W2Read03

**Over-counted:** none. Its one finding is precisely the reader's P9, explicitly marked **FALSIFIED** at line 35 and developed at lines 47–61. **Missed:** none under the assignment's criterion. The additional F2–F5 observations are explicitly characterized as “standing minor” wording/incompleteness/imprecision, with the corresponding pointer verdicts “holds” (lines 39–42, 63–75); they are not recorded as statements NOT holding. F6–F9 explicitly clear the remaining candidate surfaces (lines 77–94). **Verdict: exact.**

Evidence: `T51W2Read03.md:35,47-61,63-94`; correction record `T52W1Corr03.json`. Command: `nl -ba /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-51/coldread/reads/T51W2Read03.md`.

## Corr04 — T51W2Read04

**Over-counted:** none (findings list is empty). **Missed:** none. Reader04's pointer-by-pointer verdict states all pointers hold, with the runner citation's one-line tail drift explicitly downgraded because the quoted claim remains inside its range (lines 18, 31, 39). The remainder of the falsifier sweep also finds no false statement (lines 35–39). **Verdict: exact.**

Evidence: `T51W2Read04.md:18,31,35-39`; correction record `T52W1Corr04.json`. Command: `nl -ba /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-51/coldread/reads/T51W2Read04.md`.

## Residual risk and verification gaps

This is a falsifier review of the recorded reader reports, not a fresh re-execution of their candidate-byte investigations. I read the complete four reader files and matched the first four CAND0 correction entries; no C2 probe was run. No LSP device was available for revision-pinned Markdown; this review uses the reports' literal line evidence, not grep as semantic proof. No tools were installed.

## Summary

- Corr01: **over** — provenance residual was not a NOT-holding finding.
- Corr02: **over** — reader called the statement supported, with a scope qualification.
- Corr03: **exact** — one explicit falsification; other caveats were not NOT-holding findings.
- Corr04: **exact** — no recorded falsifications or missed ones found.
- No missed falsifications identified in these four reader reports.

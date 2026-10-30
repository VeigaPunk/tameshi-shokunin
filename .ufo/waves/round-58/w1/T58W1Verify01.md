# T58W1Verify01 — row verification

Base inspected: `2a32aa8228d5f86a85c81a923a3148bf792a9538`. I cloned the lane with `git clone --shared`, checked out that revision detached, and confirmed `git rev-parse HEAD` printed the requested base. All judgments below are independently derived from the base tree. Commands were run against the detached clone; no lane files were edited.

## R50.1 — fixed

- Routed record: `git show 9962033fd7a75aa2f2847e979dd687a5d28505a1:corpus/SOURCES.md | grep -n 'S022'` printed the S022 row as `queued` with used-by `corpus/knowledge/fixture-shrinking-pilot.md`.
- Base evidence: `git show 2a32aa8228d5f86a85c81a923a3148bf792a9538:corpus/SOURCES.md | grep -n -C 2 'S022\|fixture-shrinking-pilot'` printed S022 as `mined` with the same used-by path. The corresponding round-51 correction says `S022 status queued → mined` and explains that the cited used-by path satisfied the definition.
- Resolution commit: `6d8c11e378aa90b12650808e1b79270742935f15` (`round-51: integrate frontier/S022 correction, sourced tenth case, registry rows...`), identified by `git log --all --format='%H %s' -- corpus/lessons/round-51.md corpus/README.md SKILL.md corpus/SOURCES.md`; it is an ancestor of the inspected base by the observed log history.
- Proposed row stays fixed.

## R50.2 — fixed

- Routed-time presence check: `git show 9962033fd7a75aa2f2847e979dd687a5d28505a1:SKILL.md | grep -n 'shrink-case\|pbt staged-id generator'` produced no matching registry rows.
- Base evidence: `git show 2a32aa8228d5f86a85c81a923a3148bf792a9538:SKILL.md | grep -n -C 2 'Gate/probe registry\|shrink-case.py\|pbt-staged-id.py'` showed the round-51 registry and both entries: staged-id generator at line 2193 and shrink-case at 2201. Those lines include entry command, outcomes including exit 2, selftest, pinned values/write scope, and owner.
- Resolution commit: `6d8c11e378aa90b12650808e1b79270742935f15` (same log command and observed subject as R50.1).
- Proposed row stays fixed.

## R50.3 — fixed

- Routed-time check: `git show 9962033fd7a75aa2f2847e979dd687a5d28505a1:corpus/README.md | grep -n -E '^\\| F6 |^\\| F10 '` printed the F6 and F10 table rows both as `open`.
- Base evidence: `git show 2a32aa8228d5f86a85c81a923a3148bf792a9538:corpus/README.md | grep -n -C 2 -E 'F6|F10|coverage map'` printed the appended correction at lines 612–625: the prior table is superseded as a whole and the replacement table records F6 as held (round 50) and F10 as held (round 49).
- Resolution commit: `6d8c11e378aa90b12650808e1b79270742935f15`, the round-51 integration commit named above.
- Proposed row stays fixed.

## R50.4 — open

- Base check: `git show 2a32aa8228d5f86a85c81a923a3148bf792a9538:SCORECARD.md | grep -n -A12 -B2 'round-51\\|Round 51\\|successor C1/C2'` printed the round-50 **Planned (round 51)** paragraph. It still lists successor C1/C2 counters as planned work; it does not cite them as landed/operative.
- Cross-check: `git show 2a32aa8228d5f86a85c81a923a3148bf792a9538:corpus/lessons/round-50-verifier-spotcheck.md | grep -n -E 'forgery|successor counter|open ledger|Planned \\(round 51\\)'` printed the carried statement at line 101. The sentence is consistent with the SCORECARD plan, not evidence that successor counters resolved the carryover.
- Proposed row stays open. Planned fix intent is to correct the carryover wording only after verifying whether successor counters became operative, and cite their resolution if so. The row records the still-planned statement as evidence; it makes no claim that the counters are absent elsewhere.

## Output / limits

Machine-readable rows are in `T58W1Verify01.json` (R50.1–R50.4 only). Scratch clone removed before yielding. No tools installed or updated. No builds, tests, linters, or formatters run.

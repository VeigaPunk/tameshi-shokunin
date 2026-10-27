# T52W2RevCorr0912 — falsifier review of Corr09–Corr12

Scope: compare each wave-1 correction record against the full reader file and the section bytes at `read_rev=02ec217c4d0afabe727fde2e261b7951d28fb4e9`. “Over-counted” means the reader did not record the underlying statement as not holding (including disclosed/historical-and-accurate notes); “missed” means a reader-recorded failing statement omitted from the record. This is calibration evidence, not a claim decision.

## T52W1Corr09 — `### The tick, executed` / T51W2Read09

Reader: `.ufo/evidence/round-51/coldread/reads/T51W2Read09.md`. Section at the pinned revision: `SKILL.md:1164-1210`.

- **Over-counted (6):** record findings 3–8 are not qualifying failures. Reader line 89 explicitly says the scratch-root difference was *prior-dispositioned as two independent runs* and “unadjudicable from repo bytes”; it is not a failing section statement. Reader line 90 explicitly says the receipt-date divergence has the same disposition and prior art; it describes different runs, not an unheld assertion. Reader line 91 calls the in-flight wording an overstatement, but also says the later commit “resolved into” the newer blob; this is a historical sequence, not evidence the cited statement is false at the tick. Reader line 92 compares elapsed time using a different pair of timestamps (`19:15:14Z → 19:20:29Z`) than section lines 1186-1187 (`20:00:34Z → 20:03:34Z`); it does not establish the section's “six minutes later” is false. Reader line 93 reports a missing [I] label but its located source is ledger:356; at read_rev, section line 1206 does not cite that inference as its source and this is a label/citation mismatch, not a reader finding that the section's observation is false. Reader line 94 says the worktree SHAs have no surviving anchor, but section lines 1203-1208 expressly date them to a transient observation and the addendum as contemporaneous continuation; the reader itself says the section flags this. These are all present in record 09 JSON findings 3–8.
- **Finding 1** (record JSON finding 1, quote reader line 88) is a real recorded failure: the cited `tools/mutate-and-run.sh:511-518` anchor moved. **Finding 2** (reader line 88, four vs ten) is not a failure of the section at its read_rev: section line 1168 scopes the four legs to the timestamped tick, and line 1188 says the observation is never a standing claim. The reader itself says this is “tick-scoped historical” (reader line 88); counting it as stale-count over-counts.
- **Missed (0):** full reader file has no other statement it records as failing for this section. The strongest-falsifier result at reader lines 84-85 explains the provenance discrepancy as independent runs with matching outcomes; lines 96-99 explicitly identify no additional impact. The moved pointer at line 88 is the one qualifying failure.
- **Verdict: over** (1 qualifying finding vs 8 recorded).

Commands showing evidence:
`nl -ba .ufo/evidence/round-51/coldread/reads/T51W2Read09.md`;
`git show 02ec217c4d0afabe727fde2e261b7951d28fb4e9:SKILL.md` (section 1164-1210); `git show 02ec217c4d0afabe727fde2e261b7951d28fb4e9:tools/mutate-and-run.sh` (governed tick tool).

## T52W1Corr10 — `### The receipt at this boundary` / T51W2Read10

Reader: `.ufo/evidence/round-51/coldread/reads/T51W2Read10.md`. Section at pinned revision: `SKILL.md:1212-1229`.

- **Over-counted (1):** record JSON finding 2 quotes reader line 80 (“so ‘still not embedded’ is false of the runner at”). The full claim in section lines 1227-1228 is explicitly `Cases 5–6 are still not embedded: their rows carry no REGRESSION line` and the cited ledger row says those cases are not embedded. At the governed/tick tool `cf41efaa…`, cases 5–6 were indeed not embedded; the reader distinguishes the present CAND runner from the tick-scoped receipt, and itself says this sentence “narrates the r9 boundary (4 legs), where it was true” (reader lines 77-84). The record calls the count stale despite no falsity at the statement’s time/scope. The reader’s other finding, anchor rot (line 108), is a valid not-holding pointer at CAND and is properly counted.
- **Missed (0):** the reader’s pointer table/claims at lines 41-88 records only the anchor and this scope-dependent narration issue as not holding. Historical 67/67 and four-leg receipts are corroborated and explicitly historical; pointer rows for them are not failing findings. No additional failing statement was missed.
- **Verdict: over** (1 qualifying finding vs 2 recorded).

Commands showing evidence:
`nl -ba .ufo/evidence/round-51/coldread/reads/T51W2Read10.md`;
`git show 02ec217c4d0afabe727fde2e261b7951d28fb4e9:SKILL.md` (1212-1229); `git show 02ec217c4d0afabe727fde2e261b7951d28fb4e9:tools/mutate-and-run.sh` (governed runner and 4-leg registry).

## T52W1Corr11 — `## The operator's runbook and the six-leg regression (round 10, measured)` / T51W2Read11

Reader: `.ufo/evidence/round-51/coldread/reads/T51W2Read11.md`. Section at pinned revision: `SKILL.md:1272-1364`.

- **Over-counted (3):** record JSON finding 1 quotes reader line 71. Reader explicitly locates the list at lines 84-89 at the governed SHA and says the *cited* range 85-89 misses line 84; however the section says line anchors are governed by SHA (“the sha governs,” section line 1308). Thus the alleged imprecision is not a false section statement: the anchor is correct as the stated historical pin governs it. Findings 2 and 3 (reader lines 78 and 85) are likewise explicitly scoped to tool revision `75ed934d…`; the reader confirms the default `/tmp` and six-leg count at that governed SHA (lines 79-80, 85-90), and the section states those anchors and receipts under that pin. TMPDIR and ten-leg changes at CAND do not make those historical statements false. Record JSON includes these three despite the reader’s own “correctly scoped by … ‘the sha governs’” conclusion at lines 116-120.
- **Missed (0):** the full reader distinguishes F4 at lines 93-95 as “adjacent, not this section's text” and explicitly says no action. All other rows are holds, historical records, or disclosed notes. No qualifying failing section statement was omitted.
- **Verdict: over** (0 qualifying findings vs 3 recorded).

Commands showing evidence:
`nl -ba .ufo/evidence/round-51/coldread/reads/T51W2Read11.md`;
`git show 02ec217c4d0afabe727fde2e261b7951d28fb4e9:SKILL.md` (1272-1364);
`git show 606716f7:tools/mutate-and-run.sh` (governed runner at the section's stated SHA).

## T52W1Corr12 — `### The six-leg regression — usage and this round's receipt` / T51W2Read12

Reader: `.ufo/evidence/round-51/coldread/reads/T51W2Read12.md`. Section at pinned revision: `SKILL.md:1302-1364`.

- **Over-counted (14):** all recorded entries are scoped to CAND drift/movement, not failures of the section's pinned historical record. Findings 1-10 and 13 are pointer/currency findings from reader lines 55-67, 72; the section says `75ed934d…` governs its historical anchors (section line 1308), and reader’s own overall result calls it a faithful record of that revision (reader lines 24-26). In particular findings 1, 11-13 report six/80/80/cases=6/six rates at a tool version whose receipts the reader independently corroborates (reader lines 24-26, 70-72). Finding 7 (reader line 63) is the historical `/tmp` default at the governed revision, not an untrue statement then. Findings 11-12 are explicitly `holds-hist` (reader lines 70-71); under the assignment rule, such historical-and-accurate notes do not count. Finding 14 (reader line 102) is expressly “holds, understates at CAND”; at read_rev the sentence describes a planned ledger follow-on, not a claim that the registry remains six legs forever. It is not a reader-recorded non-holding claim at the governed section revision.
- **Missed (0):** reader lines 88-96 summarize all falsifiers (drift at CAND) and expressly say pins, @old count, receipt provenance, and panel-tool impacts are not falsified. No other failing statement is recorded for the pinned section.
- **Verdict: over** (0 qualifying findings vs 14 recorded).

Commands showing evidence:
`nl -ba .ufo/evidence/round-51/coldread/reads/T51W2Read12.md`;
`git show 02ec217c4d0afabe727fde2e261b7951d28fb4e9:SKILL.md` (1302-1364);
`git show 02ec217c4d0afabe727fde2e261b7951d28fb4e9:tools/mutate-and-run.sh`.

## Summary

- Corr09: over-counted 7; missed 0; verdict **over** (1/8 qualifies).
- Corr10: over-counted 1; missed 0; verdict **over** (1/2 qualifies).
- Corr11: over-counted 3; missed 0; verdict **over** (0/3 qualifies).
- Corr12: over-counted 14; missed 0; verdict **over** (0/14 qualifies).
- Record citations and reader lines are provided above; this is a falsifier report, not a C2 verdict.

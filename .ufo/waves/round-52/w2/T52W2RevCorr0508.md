# T52W2RevCorr0508 — correction-record falsifier

Scope: CAND0 ledger corrections T52W1Corr05–08, tested against their corresponding complete round-51 reader records. A counted finding must be a reader-recorded statement found NOT holding, not a holds statement or a disclosure that is historically accurate. Commands below are relative to `/home/vgpnk/Projects/shokunin/tameshi-shokunin` unless stated; `nl -ba <reader>` displays the cited reader line. The records and reader files were opened directly; the CAND0 ledger entries are at `.ufo/evidence/round-21/coldread/ledger.json:41565-41715`.

## T52W1Corr05 — exact

- Over-counted: none. Both findings correspond to explicitly false/stale present-facing claims: the leg-count chain (reader line 49) and the round-18 pointer's potential CAND ambiguity (lines 36, 53). The record's quotes are the reader's own falsifier statements, not its historical-accuracy disclosure.
- Missed: none. The reader's remaining checks affirm the pinned ledger rows and historical qualifier, or explicitly say the other round-51 changes do not falsify this section (lines 18, 27, 45-54). Its additional concern about treating the historical pointer as unqualified is covered by finding 2.
- Verdict: **exact (2)**.
- Evidence command: `nl -ba .ufo/evidence/round-51/coldread/reads/T51W2Read05.md`; record: `cat .ufo/waves/round-52/w1/T52W1Corr05.json`.

## T52W1Corr06 — over

- Over-counted: **2**. Finding 13 (“validates mode/SHA”) is not a failing expectation: reader says the SHA is validated and mode is read/mirrored, with the wording merely overstating mode validation (reader line 90). Finding 14 (“enumerated, executed and skipped counts distinguished”) likewise is expressly reported as a weak/unsupported anchor with “no falsifier” (lines 92-96), not a statement recorded as false. These should not be counted as wrong expectations under this assignment's criterion.
- Missed: none. The other twelve entries match the reader's actual false/stale claims: six citation-range failures plus the literal TMPDIR path, stale case-count chain, stale nine-dispatch count (lines 65-89); the TMPDIR falsifier is explicit at lines 78-81. Lines 98-121 affirm the other behavioral claims, and lines 143-163 distinguish pre-existing pointer defects/history rather than additional false statements.
- Verdict: **over (12 valid of 14)**.
- Evidence command: `nl -ba .ufo/evidence/round-51/coldread/reads/T51W2Read06.md`; record: `cat .ufo/waves/round-52/w1/T52W1Corr06.json`.

## T52W1Corr07 — exact

- Over-counted: none. The three findings match the reader's explicit stale N chain (lines 52, 60-61, 139), missing historical scratch receipt (lines 66, 71, 141), and stale 67/67 selftest tally as a CAND expectation (lines 108, 116-117, 140). The selftest record is explicitly historical at its pinned tool revision, but the reader separately concludes its current-reader expectation is stale; the correction's quote selects that latter conclusion.
- Missed: none. Other claims are called holds or nuanced-but-supported, and reader lines 143-145 explicitly say TMPDIR and panel updates do not falsify this section and enumerate what holds.
- Verdict: **exact (3)**.
- Evidence command: `nl -ba .ufo/evidence/round-51/coldread/reads/T51W2Read07.md`; record: `cat .ufo/waves/round-52/w1/T52W1Corr07.json`.

## T52W1Corr08 — exact

- Over-counted: none. Both are explicit non-holds: the present-engine 67/67 count is stale (reader line 11), and the taxonomy has a possible unclassified rewritten-history case (line 13). The latter is specifically qualified as a gap only if the labels are exhaustive, not as a contradiction of the six recorded examples; the record reports it as unsupported rather than falsely claiming those examples fail.
- Missed: none. The reader explicitly says the historic counts and scratch paths are not disproven, the pin table matches, and no panel-tool interaction occurs (lines 12, 14-15); the remaining structured rows marked holds are not failures.
- Verdict: **exact (2)**.
- Evidence command: `nl -ba .ufo/evidence/round-51/coldread/reads/T51W2Read08.md`; record: `cat .ufo/waves/round-52/w1/T52W1Corr08.json`.

## Summary
- Corr05: exact, 2/2.
- Corr06: over, 12/14; two weak/unsupported-anchor observations are not recorded false statements.
- Corr07: exact, 3/3.
- Corr08: exact, 2/2.
- Missed failing statements: none among these four records.
- No tools installed. No counters run; no scratch or fixture was needed.

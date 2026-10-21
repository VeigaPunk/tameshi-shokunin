# MistakesDraft — round-19 `## Mistakes` draft rows for C1 (leaf scribe, advisory)

Seat: TameshiR19-2.MistakesDraft (leaf). Claim: C1 calibration (five routed round-18 defects).
Baseline: `7243e7f163f08978c8fd9b6c1ef67a2fefe7d190`. Frozen population: `.ufo/evidence/round-19/contract.json`.
Tools installed or updated: none. Subagents dispatched: none. Production files edited: none.
No lane selftest, `measure.py --check`, build, lint or formatter was run. Git was read-only (`rev-parse`, `cat-file -t`, `diff --numstat`).
This is a draft for the L1. It is not verifier closure.

## Scope read

- `corpus/lessons/round-18-verifier-spotcheck.md` §5 items 1–5 (verbatim, dated 2026-10-21 spot-check, baseline `183f87b`).
- `corpus/QUALITY.md` criteria 1–2 (admission bar), 15, 17 (rounds 14–15), 26, 35 (round 17–18), 37–39 (round 19).
- `corpus/lessons/round-18.md` `## Mistakes` (line 79), Gate, Erratum R18-3 (`:121–133`), Errata R18-4/R18-5 (`:135–155`).
- `corpus/lessons/round-19.md` `## Mistakes` (`:46–54`) — the landed table this draft is checked against.
- `corpus/knowledge/guard-kill-closure.md` `:1–3`, `:171–190`; `corpus/knowledge/mutation-case-kumitate-sources-check.md` `:1–3`, `:266–276`.
- `corpus/SOURCES.md` S008 row; `CORPUS.md` (fleet root) `:34`.
- `.ufo/evidence/round-18/final/checks.json` (bash-witness row); `round-18/final/measure-final-60.json`;
  `round-19/{before.json, after-21e7932.json, bash-witness-selftest*.json/stdout/stderr, round18-final-measure.*}`.

## Commands and observed outcomes

| # | Command (read-only) | Observed |
|---|---|---|
| C-1 | `grep -rn "R18-[1-5]" corpus .ufo/evidence/round-19` | Errata present: `guard-kill-closure.md:171` (R18-1), `mutation-case-kumitate-sources-check.md:266` (R18-2), `round-18.md:121` (R18-3), `:135` (R18-4/5). |
| C-2 | `git -C tameshi diff --numstat 183f87b… 4b7c682… -- corpus/SOURCES.md` | `25	5	corpus/SOURCES.md` (5 deleted lines). |
| C-3 | `grep -n PENDING corpus/knowledge/guard-kill-closure.md` | `:2` header still "Landed-tip results: PENDING (filled by L1 after landing)"; body PENDING lines at 10, 53, 65, 91, 97, and others. The R18-1 erratum lists 10, 53, 65, 91, 97, 114, 118, 120, 122, 132, 134, 136. |
| C-4 | `grep -n queued corpus/knowledge/mutation-case-kumitate-sources-check.md`; `grep "^| S008 " corpus/SOURCES.md` | Header line 1 still reads `**queued**` (count 3 of the word in the file). SOURCES S008 status cell `mined`, used-by `knowledge/mutation-case-kumitate-sources-check.md`. |
| C-5 | `grep -n "four allowed" corpus/lessons/round-18.md` | `:79` (table row) and `:123` (superseding R18-3 erratum). |
| C-6 | `checks.json` row `bash-witness-selftest` | `"exit": 64`, `stdout_sha256 e3b0c44298fc…b855` (SHA-256 of empty stdout). |
| C-7 | `round-19/bash-witness-selftest-complete.json` | `argv: python3 tools/bash-witness-study.py selftest`, `revision 4b7c682…`, `exit 0`, `stdout_sha256 316b97…`. Stdout final line `WITNESS_SELFTEST: 43/43 pass`, `VERDICT: PASS`. |
| C-8 | `round-19/bash-witness-selftest.json` and `.stderr` | `exit 1`; stderr traceback `FileNotFoundError` naming `tools/mutate-and-run.sh` in a `/tmp/tameshi-r19-witness-*` scratch clone (`bash-witness-study.py:1733–1743`; grep count 1). |
| C-9 | `grep -n "revision" round-18/final/measure-final-60.json` | `"revision": "a85f7107c4167cd9968248722256fcaf617fc30c"` (not 4b7c682). |
| C-10 | `round-19/round18-final-measure.json` and `.stdout` | `argv: python3 .ufo/evidence/round-18/measure.py … --rev 4b7c6823… --explain`, `revision 4b7c682…`, `exit 0`, `recorded_at 2026-10-21T05:28:25Z`. Stdout: `"sections_covered": 60`, `"calibration_restraint_score": 8`, `"overrides_used": false`. Stderr 0 bytes. |
| C-11 | `before.json` vs `after-21e7932.json` | `before`: corrected 0, open 5, total 5. `after`: corrected 5, open 0, total 5. |
| C-12 | `grep -c "not4b7c682" corpus/lessons/round-19.md` | `1` (typo in landed row 4). |
| C-13 | `grep -n "A count carries its command" CORPUS.md` | `CORPUS.md:34` (fleet root). The landed row's "CORPUS count-command rule" resolves there, not in the tameshi repo. |

Source quotes (≤25 words, with location, dated 2026-10-21 read of the local repo):
- QUALITY.md criterion 15 (`:61–63`): "A setup error with the expected exit code is not proof of the intended assertion" (14 words).
- QUALITY.md criterion 2 / admission bar rule 2 (`:4–5`): "Every claim carries a source: a measured anchor (path:line, command, evidence id)" (13 words).
- CORPUS.md `:34`: "A count carries its command." (5 words).

## Proposed `## Mistakes` rows (one per §5 item; §5 items 1 and 2 split)

Columns follow `lessons/round-19.md:48`: Class | Evidence pointer | Captured-by | Fix and failure-capable check.

**Row A — §5 item 1 (stale verified-at header).**
- Class: stale provenance header survives a body correction.
- Evidence: §5 item 1; `corpus/knowledge/guard-kill-closure.md:2` reads "Landed-tip results: PENDING (filled by L1 after landing)" (C-3). R18-1 erratum at `:171` names line 2 and the twelve body lines listed above.
- Captured-by: none at round-18 admission. QUALITY 35 required a dated erratum for a correction but not that it name the stale header field. QUALITY 37 (round 19) now names it.
- Fix and check: the R18-1 erratum gives effective verified-at revision `921ef807…`, receipt `final/probes.stdout` (`DEFECT_PROBES: open=0 closed=11 total=11`), and the registry pin `5923d89…`. Falsifier: deleting the R18-1 block must reopen this item in the round-19 ruler (contract.json R18-1). A presence check on the erratum is weaker than a semantic check; say so when it is used.

**Row B — §5 item 2 (S008 `queued` vs registry `mined`).**
- Class: admitted knowledge header keeps a stale source status after the registry row changed.
- Evidence: §5 item 2; `corpus/knowledge/mutation-case-kumitate-sources-check.md:1` "**queued** … not yet a mined row" (C-4). SOURCES S008 is `mined` with this entry in used-by (C-4). R18-2 erratum at `:266`.
- Captured-by: QUALITY 10 requires `source:`, `verified-at:` and `recheck:` and a SOURCES row. It does not require the header's status word to equal the registry row's status.
- Fix and check: the R18-2 erratum names line 1 and the effective status at `4b7c682`. Falsifier: for every `Sxxx` status word in a knowledge header, the same word must match the SOURCES status at the cited revision. The word `queued` for S008 at `4b7c682` must fail. QUALITY 37 applies.

**Row C — §5 item 3 (falsifier arithmetic).**
- Class: falsifier counts line deletions where it means row or cell changes.
- Evidence: §5 item 3; `corpus/lessons/round-18.md:79` "deletions = the four allowed used-by cells only"; `git diff --numstat` gives 25 added and 5 deleted lines (C-2). The five removed rows are S001, S008, S052, S056 and S057; S008 changed two cells on one line (status and used-by). Superseded by R18-3 at `round-18.md:121–133` (C-5).
- Captured-by: QUALITY 35's numstat check requires zero deletions for erratum-only changes. It does not define a unit for deleted mutable-cell rows. Only QUALITY 38 (round 19) names the unit.
- Fix and check: R18-3 names all five IDs and says the four-cell statement is history. Falsifier: `numstat` deletions must equal the listed row IDs. A "four cells" statement fails. A changed immutable cell fails. QUALITY 38.

**Row D — §5 item 4 (exit-64 witness row as final receipt).**
- Class: failed CLI invocation presented as the effective selftest receipt.
- Evidence: §5 item 4; `round-18/final/checks.json` row `bash-witness-selftest`: `exit 64`, empty stdout (C-6). Failed attempt `round-19/bash-witness-selftest.json` exit 1 (C-8). Effective replacement `round-19/bash-witness-selftest-complete.json`: `exit 0`, revision `4b7c682…`, `WITNESS_SELFTEST: 43/43 pass` (C-7). R18-4 at `round-18.md:135–146`.
- Captured-by: QUALITY 15 ("A setup error with the expected exit code is not proof of the intended assertion"; each retained expectation must be effective or superseded by checked evidence) and QUALITY 17 (explicitly classify every nonzero exit, including usage; retain the unsupported invocation). Both existed before round 18. The landed round-19 row cites QUALITY 26/35, which do not cover exit classification.
- Fix and check: the row stays byte-identical as history and is marked superseded. Falsifier: a 15/17 check must reject the `checks.json` row as effective (exit 64) and accept the complete receipt only when argv, revision, integer exit 0, and stdout and stderr digests all match. QUALITY 39 names the same rule.

**Row E — §5 item 5 (unbacked final-revision claim).**
- Class: final-revision numerical claim without a receipt at that revision.
- Evidence: §5 item 5; the round-18 60/60 receipt `final/measure-final-60.json` is at `a85f710…` (C-9). No round-18 receipt names `4b7c682`. Dated replay `round-19/round18-final-measure.json` at `4b7c682…`, exit 0, recorded 2026-10-21 (C-10).
- Captured-by: QUALITY 2 (admission bar rule 2: every claim carries a measured anchor — command or evidence id — at the revision it describes). The landed row's "Evidence standard, criterion 26" is the wrong capture: criterion 26 governs dated corrections to stale receipts, not a missing receipt at a cited revision.
- Fix and check: the replay is dated later and does not claim round-18 timeliness (criterion 39). Falsifier: the replay must show `revision 4b7c682…`, `exit 0`, `sections_covered 60`, `calibration_restraint_score 8` and `overrides_used false`. A replay that is backdated, or a 60/60 claim without a replay at `4b7c682`, fails.

## Findings on the landed round-19 `## Mistakes` table (`corpus/lessons/round-19.md:48–54`)

1. **Row 5 is not rooted in §5.** The scratch `FileNotFoundError` (C-8) is a round-19 self-found mistake, not a verifier §5 item. The draft above uses only §5 items 1–5. L1 decides whether row 5 stays as a sixth row or moves. The Gate table already records it at `round-19.md:25`.
2. **Row 3 captured-by is wrong.** It cites QUALITY 26/35 and says they "lacked effective-receipt reconciliation." QUALITY 15 and 17 already cover that. Proposed correction: QUALITY 15, 17 (and 39 as the round-19 fix).
3. **Row 4 captured-by is wrong.** It cites "Evidence standard, criterion 26," which governs stale-receipt corrections. Proposed correction: QUALITY 2.
4. **Typo.** `corpus/lessons/round-19.md:53` reads "not4b7c682" (C-12). Fix as a literal space, or as a dated erratum if the file has already landed under criterion 35.
5. **Citation path.** "CORPUS count-command rule" resolves to `/home/vgpnk/Projects/shokunin/CORPUS.md:34` (C-13), outside the tameshi repo. Cite the full path.

## Not verified here

- The round-19 ruler (`measure.py --check`) and the criteria 37–39 falsifiers were not executed. The falsifiers above are proposed checks, not observed results.
- The 18 earlier guard survivors are out of scope. The R18-1 erratum says they remain open.
- The 60/60 replay was read from its committed stdout. It was not re-executed.

## Verdict

Five rows drafted, one per §5 item, each with an existing QUALITY capture where one exists and an explicit "none" where it does not. Four landed-table findings are reported: one non-§5 row, two wrong captured-by citations, and one typo. Advisory only; no independent closure claimed.

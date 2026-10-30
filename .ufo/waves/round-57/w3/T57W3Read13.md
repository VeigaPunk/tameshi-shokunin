# T57W3Read13 — cold-read certification

## Context gate classification and explicit exit classes — round 15

- Candidate: `adf87899c70d616140a81185a8f9acbbdfb30392`
- Frozen round-18 sectionize: lines 1652–1718; SHA-256 `132cfb9ef1aa07111af42389e4fe862152e3118b3a8bb66f1d84a6a332e7edf6`.
- Verdict: **verified-record**. No false statement or unexpected command failure found.
- Axes: calibration, completeness, reproducibility, zero lane mutation.

## Executed sweep

All gate commands ran in the shared clone detached at C0b, with TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read13. Commands, cwd, environment, complete stdout/stderr and exits are retained in adjacent JSON and numbered receipts.

| Receipt | Command / purpose | Observed |
|---|---|---|
| command-01.json | `context-capture.py --check --json` | 0, context_consistent; pinned digest and expected verdict match |
| command-02.json | `context-capture.py --selftest` | 0, SELFTEST: PASS (49/49) |
| command-03.json | `evidence-disposition.py --selftest` | 0, SELFTEST: PASS (66/66) |
| command-04.json | `context-capture.py --unexpected` | 64, usage_error; expected usage rejection |
| command-05.json | `evidence-disposition.py --unexpected` | 64, expected usage rejection |
| command-06.json | `python3 -B -c (frozen sectionize; full snippet in receipt)` | 0, 1652 1718 132cfb9ef1aa07111af42389e4fe862152e3118b3a8bb66f1d84a6a332e7edf6 |
| command-07.json | `context-capture.py --check --receipt <absolute retained missing-env> --expected <absolute committed missing-env pin> --json` | 1, missing_injected_environment; pin matches, retained stored-verdict lie also detected |
| command-08.json | `context-capture.py --check --receipt <absolute retained clean> --expected <absolute committed clean pin> --json` | 0, context_consistent; pin matches |
| command-09.json | `python3 -B -c (pointer/hash/history sweep; full snippet in receipt)` | 0; all pointers present, three literal hashes exact; effective receipt 44 checks/no failures, earlier receipts retain their failures |

## Reading and findings

Read lines 1652–1718 end to end. Checked the historical producer docstring, decide() and main() cited ranges; S049/S051 rows; round-15 Gate/Mistakes and effective verification receipt; round-14 routed defect 5; archive markers; active gate input/digest/recomputation/exit logic; and fleet Gate standard. All three literal historical SHA-256 values match C0b. Clean and missing-environment counterparts reproduce the stated 0/1 outcomes. The selftest sweep covers raw comparisons, source/mapping/control contradictions, stored-verdict lies, malformed and duplicate JSON, wrong types, invalid UTF-8, missing inputs, tampering, and usage. No actionable discrepancy found.

## Residual risk and verification gaps

- LSP device unavailable: read xd://lsp returned No such tool. Text/source inspection is literal evidence, not semantic references/definition proof.
- The archived producer is intentionally not executed: the section explicitly prohibits treating it as an entry point or regenerating retained receipts.
- ../PROTOCOL.md is an external fleet pointer; resolved at the declared lane location to /home/vgpnk/Projects/shokunin/PROTOCOL.md, not copied into the detached lane clone.
- Expected negative control returned exit 1/missing_injected_environment with verdict_matches_expected=true; this is the documented outcome, not a finding.
- No SKILL changes, stage files, installs, upgrades, routing changes, admission, or saturation claims.
- Selftests are finite controls, not universal proof; no historical live experiment was rerun.
- No code diff was assigned to this seat: the deliverable certifies only this frozen section.

## Self-evaluation

Accuracy 4/5: recorded exits and hashes support the claims; no semantic LSP support. Completeness 4/5: section, pointers and finite advertised controls covered; no universal malformed-input claim. Clarity 4/5: compact table delegates long commands to receipts. Actionability 5/5: exact candidate/hash and full executed commands retained. Conciseness 4/5: machine evidence duplicates receipt content for portable binding. Overall 4.2/5; highest-value improvement is semantic tooling availability, outside this seat. User agreement expected because the certification is bounded and replayable.

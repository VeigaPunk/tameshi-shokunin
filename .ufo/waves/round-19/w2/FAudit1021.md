# FAudit1021: falsification of w1 Audit1021 (tameshi r19 a1, w2, advisory)

Seat `TameshiR19-2.FAudit1021` (reviewer, read-only), 2026-10-21. Advisory; closes nothing.

## Strongest material assertion attacked

M1: audit-1021's `VERIFIED actual execution receipts; …` line is unconditional; its clauses
exceed the program's checks. Concrete case: `final/checks.json` (sha `fed3c8e6…`) carries
`bash-witness-selftest` exit 64 / empty stdout; C1 must not cite that line for defect 4.

## Verdict: AGREE — and strengthened

1. **Failing case confirmed first-hand** (Audit1021 had applied it only by hash identity):
   live `final/checks.json` = `fed3c8e6cba05c41d8fdcafc091328e3092e2018a42fb8a8594bd8b5815c671d`
   (equals the trace input map) records `"bash-witness-selftest": {argv:
   ["python3","tools/bash-witness-study.py","--selftest"], "exit": 64, "stdout_sha256":
   e3b0c442…b855}`. Blob-identical at `55e1d312` and master.
2. **Structure confirmed:** trace `argv[29]` program (read raw) contains exactly the 9 asserts
   Audit1021 lists, then the unconditional VERIFIED print; trace keys carry no stdout digest (B3).
3. **Arithmetic reproduced** (read-only plumbing, receipt argv never executed): B4 argv
   print-rebuild over `a9c94c5c` blobs equals stdout byte-exactly (6574 B); B5 16/16 inputs
   sha256-match at R; B7 sha256(SKILL.md@R 1021..1067)=`60d65824…` vs 1021..1068=`80d971ca…`
   (differs) — ledger `end:1068` exclusive, confirmed.
4. **Currency at delivered build:** master=`e7039fdb`; `55e1d312` is its ancestor; both checked.
   Pair/trace/ledger/checks.json unchanged; all 15 non-SKILL inputs match the trace map.
   SKILL.md grows 1934→1936 lines (line-1890 replacement; insertions at 1935/1936, below section);
   section hash remains `60d65824…`, anchors 1021/1067 intact. None of Audit1021's invalidation conditions
   (a)–(d) occurred; its C1 §3/§4 extends cleanly to the frozen build.

## C1 consequence is honored by the delivered ruler

Frozen `55e1d312` `measure.py` (blob `bb651eef…`; identical blob at master) R18-4 never cites
audit-1021's VERIFIED line. It independently requires a typed new receipt (exact argv
`bash-witness-study.py selftest`, revision==`4b7c682`, int exit 0, tz-aware recorded_at ≥
2026-10-21T02:28:10-03:00, stream path+digest agreement, empty stderr), byte-equality with the
historical 43/43 tally, tool/runner sha pins, preservation flag, supersedes of both dead rows,
and asserts the historical checks.json row stays exit 64/empty. Specific mutants (usage-exit,
bool-exit, backdated, naive-time, unsuperseded, stderr/digest tamper, missing historical
tally, string supersedes) are specified to flip R18-4 open — the check M1 demands; defect 4
does not repeat M1's overclaim. Static chain verified at `55e1d312`: complete.json has
argv/revision/exit/recorded_at 05:28:57Z (> freeze); stdout SHA-256 `316b9713…` matches
`final/bash-witness.stdout`; output contains `WITNESS_SELFTEST: 43/43 pass` and `VERDICT: PASS`.
I did not execute the ruler or its selftest (prohibited for this seat).

## Concrete falsifier

Run at `55e1d312`: `python3 .ufo/evidence/round-19/measure.py --selftest`; if `usage-exit`,
`bool-exit`, or `missing-historical-tally` fails to flip R18-4 open, my credit is false and
M1's C1 consequence revives.

## Residual unknowns

- Live worktree `measure.py` (`3f19a16b…`, mtime 03:25:27 -0300) has uncommitted post-freeze
  edits vs blob `bb651eef…` (same at both revisions): adds OLD_CHECKS byte pin `fed3c8e6`,
  probes.stderr emptiness, explicit-supersession phrases, `cwd_kind`, negated-supersession
  mutants — all strengthen R18-1..R18-4; analysis holds under both versions. Not treated as a
  defect; L1's final run should execute a pinned/committed ruler revision.
- Execution of audit-1021 remains a tracer self-report (Audit1021's own disclosure; unchanged).

No tools installed or updated. Only this report written; no production/ref/state changes.

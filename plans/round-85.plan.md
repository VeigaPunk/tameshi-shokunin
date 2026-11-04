# Round 85 — design receipt blob audit

Base: 45fa68046b0ce8c285ce161f3c6e164e6e721f06. L1: TameshiR85.

## Declaration

ONE claim R85-C1: capability acquisition, operability axis — a committed-object design-receipt audit. This is NOT calibration. The stagnation nudge applies: scored axes depth10/calibration8/freshness9 exceed saturation8, and rounds83–84 added no capability (window2). Scores remain unchanged.

Frozen predicate: `DESIGN_CAPABILITY: cases=8 passed=8 mismatches=0 R85_C1_PASS=true`, exit0, from `python3 -I .ufo/evidence/round-85/measure.py --repo LANE --rev REV --work EMPTY_DIR`.

Instrument contract: `tools/design-blob-audit.py --repo REPO --receipt-rev REV --root RELATIVE_DIR --candidate-rev REV`. Read receipts from committed regular blobs below root at receipt-rev, never worktree. Recognize design headers exactly as receipt-bytes-bind's design block: design_base, design_tool, design_tool_sha256 and measured_bytes marker. Validate whole population before output. All git reads disable replace refs. Require resolved receipt/candidate/design-base commits, nonempty design population, unique complete headers and safe repo-relative tool paths. No normal/design mixed headers. Non-design files may be ignored. Candidate named path must be a regular blob (100644/100755) whose SHA256 equals design_tool_sha256. Emit `DESIGN_BLOB_ROW PATH state=carried|different|absent|nonregular`, then `DESIGN_BLOB: receipts=N carried=C orphan=O`. Exit0 iff orphan0; exit1 orphan>0; exit2 setup before row/summary. No whole-history search or proof of runtime execution, authority, race safety or general provenance follows.

Frozen eight public-CLI cases: matching regular blob→carried/exit0; different blob→different/exit1; missing path→absent/exit1; symlink→nonregular/exit1; malformed design sha→exit2/no stdout; unresolvable candidate→exit2/no stdout; mixed measured/design headers→exit2/no stdout; zero design population→exit2/no stdout. Counter generates fresh isolated git fixtures and reads candidate instrument from REV. Missing instrument is failed measurement, not credit. Constant-success control must fail seven cases; skipped-work base must fail eight. No predicate/population changes after scoring. Any missed case is honest-stop.

Sourced claim: official git-cat-file OPTIONS (<type>, -t) opened by L1 2026-11-04; use held source row or append correction/scoped row only under SOURCES contract. Quote: “Instead of the content, show the object type identified by <object>.” Source https://git-scm.com/docs/git-cat-file. The source supports object inspection only, not audit verdict policy.

## No harm and limits

Do not modify existing tools. New standalone gate and frozen fixture counter only. Register demonstrated capability in SCORECARD and SKILL registry after measurement; preserve existing selfstate population, pin audit, receipt and registry sweeps. Before source/registry edits forecast coldread cost; preserve actual47-section floor, no full-page claim. If monitored edits lose credited sections, reread/rekey before admission or record harm honestly. Keep round84 rejected wrong-axis claim unchanged. Other debts remain open: malformed kind/source-id, caller revision authority, conversion attributes, receipt race/parent aliases, two-edit text pin.

## Wave

One validated v1 wave9 seats: executor3, scribe, scout, connector, reviewer, critic, mutation-tester; L1 planner. Attack3/9. Sole integration owner L1; seats use private scratch and deliver proposal files, not shared production edits. No report before WAVE-DONE. Assimilation none unless bounded source-grounded work serves this exact claim.

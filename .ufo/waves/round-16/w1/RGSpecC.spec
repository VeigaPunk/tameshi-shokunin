# RGSpecC — class C candidates (counts + finding-kind meta-check, §13.4/§13.5).
# Target: kumitate-shokunin/scripts/round-gate.mjs @ 364f1d5954158ef8844bca4a5fef57b05d2f2ca5
# Blob sha256 f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9 (verified 2026-10-20).
# All three @old strings verified count==1 against the pinned blob (python3 literal count).
# Pre-registered predictions recorded in RGSpecC.md BEFORE any mutant run.

@defect RGC-THIN-FLOOR | REPORT_MIN_BYTES 1024 -> 512: thin floor inside the unmeasured [26,1059] interval (§13.4); no fixture report lands in (512,1024] — predicted SURVIVED
@old const REPORT_MIN_BYTES = 1024;
@new const REPORT_MIN_BYTES = 512;

@defect RGC-KIND-DROP | drop 'TREE_DIRTY' from FINDING_KINDS: meta-check reads enum only (missing = enum ∖ observed), so shrinking the enum weakens the net with no failure — predicted SURVIVED
@old   'TREE_DIRTY', 'UNPUSHED', 'REPORT_UNTRACKED',
@new   'UNPUSHED', 'REPORT_UNTRACKED',

@defect RGC-PASS-COUNT | selftest summary numerator passed -> passed+1: ROUND_GATE_SELFTEST is shape-only (\d+/\d+ regex, VERDICT equality) — counts unread (§13.5) — predicted SURVIVED
@old   lines.push(`ROUND_GATE_SELFTEST: ${passed}/${results.length} pass`);
@new   lines.push(`ROUND_GATE_SELFTEST: ${passed + 1}/${results.length} pass`);

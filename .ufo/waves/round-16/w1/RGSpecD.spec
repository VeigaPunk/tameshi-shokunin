# RGSpecD — class D defect candidates (reported-but-unasserted surfaces, arm-class-matrix §13.5)
# Target: kumitate-shokunin/scripts/round-gate.mjs @ git 364f1d5954158ef8844bca4a5fef57b05d2f2ca5
# Pinned blob sha256: f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9 (verified 2026-10-20)
# Pre-registered predictions in the sibling report .ufo/waves/round-16/w1/RGSpecD.md — registered BEFORE any mutant run.
# Escapes used: \n inside the D1 @old/@new is written \\n to match the literal backslash-n inside the template literal;
# D2's @old uses a real \n escape to span lines 613-615.

@defect RGD1 | fail-closed stderr diagnostic drops the detail tail (:615) — stderr of a fail-closed run is read by no check; fcA-F/rt3/rt5/jFc assert stdout token only
@old process.stderr.write(`round-gate: fail-closed — ${token}: ${detail}\\n`);
@new process.stderr.write(`round-gate: fail-closed — ${token}\\n`);

@defect RGD2 | fail-closed JSON body reports a constant durationMs (:613) — jFc (:1279-1286) never reads it; the only durationMs assert is jClean :1263 on the audit body
@old     durationMs: Math.max(0, Date.now() - started),\n  };\n  process.stderr.write
@new     durationMs: 0,\n  };\n  process.stderr.write

@defect RGD3 | reported citations.mainProbeable is pinned to null (:387) — field copied from the probe-computed local; the probes themselves use the local, and no check asserts j.citations.mainProbeable
@old     citations.mainProbeable = mainProbeable;
@new     citations.mainProbeable = null;

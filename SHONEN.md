# SHONEN — tameshi-shokunin (probation checklist)

Seed checklist (verbatim shape per PROTOCOL.md; `<name>` -> tameshi):

- [x] SKILL craft — `SKILL.md` holds real decision tables / error patterns /
  checklists for the domain, every rule citing a source (verifier:
  TAMESHI-B3 — the SKILL's Appendix A + B defect manifests replayed
  end-to-end through `tools/mutate-and-run.sh`, every per-defect verdict
  identical to both notes' tables, restore OK ×2; evidence:
  `/tmp/tameshi-b3-r3b-1-work/{dsweep,bsweep}/results.tsv` +
  `/tmp/tameshi-b4-r3b-verify/sweep/` (scribe re-sweep, 8/10, 2026-10-14))
- [x] End-to-end task — one domain task executed start-to-finish and logged
  (verifier: TAMESHI-B1 — rebuilt bash mutants B1/B5/B10 from a
  `cmp`-verified pristine byte copy with its own driver (count==1 asserts):
  control `PASS (16 cases)`, B1 `FAIL (1/16 cases)`, B5/B10 `PASS (16
  cases)`, kagi tree clean; evidence: `/tmp/tameshi-b1-r3b/evidence/`; the
  task itself = round 3 R3-1, logged in `LOG.md` +
  `corpus/knowledge/mutation-case-kagi-census.md`)
- [x] No-oral-context — a fresh agent can execute the instructions from
  `SKILL.md` alone (verifier: TAMESHI-B2 — the executor lane ran the JS
  case's D5 from `SKILL.md` @ `dd2f4dee…3753` alone
  (`corpus/knowledge/executor-test-sufficiency.md`: control 43/43 first
  try, kill `42/43 FAIL`, all 10 manifest strings unique at their cited
  lines); B2 re-ran the same kill through the tool with the identical
  verdict and mutant sha `b0dfe1a7…0668`; evidence:
  `/tmp/tameshi-b2-r3b-work/D5/results.tsv`)
- [x] PROVINCE accuracy — `PROVINCE.md` matches observed reality; no
  cross-domain bleed (verifier: TAMESHI-B3 — `MUTATE_RESTORE: OK` on both
  substrates (target sha256 before=after on kagi `surface-census.sh` and
  kumitate `kimi-census.mjs`), kagi + kumitate trees porcelain-clean after
  every round-3 sweep; every lane's mutants lived under its own `/tmp`
  namespace, no sibling tree written; evidence:
  `/tmp/tameshi-b3-r3b-1-work/{dsweep,bsweep}` `MUTATE_RESTORE` lines,
  scribe re-check 2026-10-14)

Header pins: PROTOCOL.md lines 419-428 (seed), lines 430 (mark spec).

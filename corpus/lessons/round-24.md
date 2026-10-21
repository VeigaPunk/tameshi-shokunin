# Round24 — routed hardening is repaired only when it can fail

author: tameshi (CloseTameshi22, round24 L1 coordinator)

## Claims

C1 calibration, tied lowest numeric axis: eleven frozen hardening
predicates, 1/11 at 6a1821a8897eea6e7d9669292160ec9593669409, target 11/11
(`.ufo/evidence/round-24/contract.json`, ruler `measure.py`, `before.json`,
landed e338f1bd0749a1786d95d3d3cd9572bb10757667 before any seat). K4 (the
any-token mutant) was already killed at base and is kept as a control,
not a repair. These predicates are capability checks, not historical
defects, and numeric calibration stays 8.

## Gate

Admit candidate: `knowledge/replay-projection-hardening.md`,
`tools/registry-replay.py`, the round24 selftest fixtures and the pinned
successor registry rows.

Reject:
- calling a routed defect "fixed" before its predicate fails at base and
  holds after;
- reading four mutant kills as general mutation adequacy;
- reading realpath identity as write isolation;
- reading pinned digests as producer authentication.

Flip condition: an independently retained, applicable execution or
authority record.

S084 opened 2026-10-21 UTC: https://docs.python.org/3/library/os.path.html,
section `os.path.realpath`, first paragraph (Python 3.15.1 docs). Located
quote: "Return the canonical path of the specified filename, eliminating any
symbolic links encountered in the path". The same section says non-strict
mode "may still contain links or loops" for missing components. This is why
the row is scoped to identity, not isolation.

S085 opened 2026-10-21 UTC, own-work
`.ufo/waves/round-23/fresh-adjudication.json` at 6a1821a, lines 53–104,
`routed_not_executed`. Located quote (line 66): "do not pin bundle_sha256
literals, so a regenerated bundle and expected pair would still hold".

Both new rows start as mined, with recheck on-release (S084) or on-change
(S085), used by this lesson and the new knowledge entry. No existing row's
status, recheck or used-by changes.

Bounded lookup: identified 2, screened 2, included 2, excluded 0.

## Mistakes

| Class | Evidence pointer | Captured-by | Fix / shown able to fail |
|---|---|---|---|
| falsifier-coverage / unmeasured hardening | Round23 `original-outcomes2.json`: 34/64 dead, including all 20 reviewers. `fresh-adjudication.json` `routed_not_executed`. Closure rounds[421]: any-vs-all mutant probe | QUALITY15/29 cover nondiscriminating fixtures, but no criterion required routed gaps to become failing predicates | QUALITY48 plus the frozen ruler. At base: K1–K3 mutants survive the 38-case selftest, K5–K6 substituted bundles still hold their rows, and K7–K11 have no tool, giving 1/11. The after measurement is recorded below once executed. |

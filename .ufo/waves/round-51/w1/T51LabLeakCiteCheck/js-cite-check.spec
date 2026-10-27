# tameshi round-26 C1 — PRE-REGISTERED mutation spec for kumitate scripts/cite-check.mjs
# rev 1205c6621a2eccbb8ffceae86d9e7b79a7990b3a · blob sha256 40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f · 2537 lines · mode 100755
# Suite: guarded hermetic `node "$MUTANT" --selftest` (hermetic group only, 62 cases at the pin); verdict oracle = exit status only.
# Predictions were fixed before any mutant run. Composition: 5 kill-aimed / 5 hole-aimed.
# Matrix axes: severity table, pin classification, fence grammar, fail-closed wording,
# verdict guards, line-range boundary, strict promotion, usage exit, content-pin compare.
# Each @old occurs exactly once in the pinned bytes.

# PREDICT KILLED — the bogus-path case asserts kind UNRESOLVED with severity error; rec() reads SEVERITY.
@defect K_UNRESOLVED_SEV | UNRESOLVED demoted from error to warn in the severity table
@old   SYMBOL_MISS: 'warn', ORPHAN_REF: 'warn', REF_OWNER_AMBIG: 'note', UNRESOLVED: 'error',
@new   SYMBOL_MISS: 'warn', ORPHAN_REF: 'warn', REF_OWNER_AMBIG: 'note', UNRESOLVED: 'warn',

# PREDICT KILLED — the content-pin case expects OK for a matching sha256 pin and PIN_MISMATCH for a wrong one; as rev pins they go to git resolution instead.
@defect K_PIN_KIND | sha256-marked pins are classified as rev pins
@old     if (/sha256/i.test(marker) || /sha256/i.test(gap)) kind = 'sha256';
@new     if (/sha256/i.test(marker) || /sha256/i.test(gap)) kind = 'rev';

# PREDICT KILLED — the marker-symmetric case puts a ~~~ fence before a citation and expects the same result as ```.
@defect K_FENCE_TILDE | a three-tilde line is no longer a fence marker
@old (`{3,}|~{3,})/;
@new (`{3,}|~{4,})/;

# PREDICT KILLED — the both-candidates-absent case asserts exit 2 and stderr containing "--src <dir> is missing".
@defect K_MISSING_WORD | fail-closed stderr says absent instead of missing
@old kind = e.code === 'ENOENT' ? 'missing' : 'unreadable';
@new kind = e.code === 'ENOENT' ? 'absent' : 'unreadable';

# PREDICT KILLED — the empty-scan-set case asserts verdict FAIL; with both guards gone an empty, drift-free run passes.
@defect K_EMPTY_VERDICT | the verdict drops both the scanned-files and resolved-citations guards
@old   const verdict = totals.filesScanned > 0 && totals.resolved > 0 && !drift ? 'PASS' : 'FAIL';
@new   const verdict = !drift ? 'PASS' : 'FAIL';

# PREDICT SURVIVED — the only LINE_OOR fixture cites :999 in a 20-line file; no case cites line n+1.
@defect S_OOR_EDGE | line-range check accepts one line past the end of file
@old     const bad = ref.start > n || ref.end > n;
@new     const bad = ref.start > n + 1 || ref.end > n + 1;

# PREDICT SURVIVED — no hermetic case runs with --strict, so warn promotion is unasserted.
@defect S_STRICT | strict mode promotes warnings only when there are two or more
@old   const drift = totals.error > 0 || (opts.strict && totals.warn > 0);
@new   const drift = totals.error > 0 || (opts.strict && totals.warn > 1);

# PREDICT SURVIVED — an empty scan set also has zero resolved citations, so the resolved guard alone still fails it (co-extensive guard).
@defect S_EMPTY_GUARD | the verdict drops only the scanned-files guard
@old   const verdict = totals.filesScanned > 0 && totals.resolved > 0 && !drift ? 'PASS' : 'FAIL';
@new   const verdict = totals.resolved > 0 && !drift ? 'PASS' : 'FAIL';

# PREDICT SURVIVED — no hermetic case passes an unknown flag, so the usage exit code is unasserted.
@defect S_USAGE | usage error exit 64 becomes 65
@old     return 64;
@new     return 65;

# PREDICT SURVIVED — the mismatch fixture hex is not a substring of the digest, so a substring compare still reports PIN_MISMATCH.
@defect S_PIN_INCLUDES | content pin accepted anywhere inside the digest, not only as a prefix
@old       } else if (digest.startsWith(pin.hex)) {
@new       } else if (digest.includes(pin.hex)) {

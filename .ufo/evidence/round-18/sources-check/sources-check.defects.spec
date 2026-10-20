# tameshi round-18 C1 — PRE-REGISTERED mutation spec for kumitate scripts/sources-check.mjs
# rev 0acb7752d19058b953ebbeba253b1e35f6548de5 · blob sha256 6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f · 897 lines · mode 100755
# Suite: guarded hermetic `node "$MUTANT" --selftest`; verdict oracle = exit status only.
# Predictions were fixed before any mutant run. Composition: 5 kill-aimed / 5 hole-aimed.
# Matrix axes: finding-kind coverage, exit map, verdict line, strict/warn promotion,
# fail-closed paths, and count/census parity. Each @old occurs exactly once in the pinned bytes.

# PREDICT KILLED — TIER_ENUM's fixture asserts the emitted finding kind and exit.
@defect K_KIND | change TIER_ENUM emission to KIND_ENUM; fixture expects TIER_ENUM
@old add('error', 'TIER_ENUM', 'corpus/SOURCES.md', row.line, `id=${id} tier=${row.tier}`);
@new add('error', 'KIND_ENUM', 'corpus/SOURCES.md', row.line, `id=${id} tier=${row.tier}`);

# PREDICT SURVIVED — the coverage check iterates only the declared enum; removing a declared kind does not change emitted behavior.
@defect S_KIND | drop RECHECK_OVERDUE from the declaration; one-sided kind coverage remains green
@old   'RECHECK_OVERDUE',
@new

# PREDICT KILLED — invalid/missing option fixtures assert the usage exit code 64.
@defect K_EXIT | usage error exit 64 becomes 65
@old return 64;
@new return 65;

# PREDICT SURVIVED — DRIFT fixtures assert exit and finding kind, not the final verdict text.
@defect S_VERDICT | alter the final DRIFT verdict line spelling
@old SOURCES_CHECK: DRIFT (${driftKinds.join(',')})
@new SOURCES_CHECK: DRIFT [${driftKinds.join(',')}]

# PREDICT KILLED — strict warning fixture expects USED_BY_ASYMMETRY with exit 1.
@defect K_STRICT | strict no longer promotes warn findings to errors
@old strict && finding.severity === 'warn'
@new strict && finding.severity === 'error'

# PREDICT KILLED — the missing-SOURCES fixture pins SOURCES_MISSING and its exit-2 verdict.
@defect K_CLOSED | missing SOURCES.md maps to the wrong fail-closed kind
@old return failClosed('SOURCES_MISSING', 'corpus/SOURCES.md is absent');
@new return failClosed('READ_FAILED', 'corpus/SOURCES.md is absent');

# PREDICT KILLED — frozen awk census parity compares the JS rows count to the shell census.
@defect K_ROWS | each valid source row is double-counted
@old counts.rows += 1;
@new counts.rows += 2;

# PREDICT SURVIVED — duplicate findings are counted, but no selftest asserts their line number.
@defect S_DUP_LINE | report duplicate IDs one line late
@old add('error', 'ID_DUPLICATE', 'corpus/SOURCES.md', index + 1, `id=${id}`);
@new add('error', 'ID_DUPLICATE', 'corpus/SOURCES.md', index + 2, `id=${id}`);

# PREDICT SURVIVED — entriesWithSource appears in reports but no selftest pins its positive count.
@defect S_ENTRY_COUNT | double the count of source-header entries
@old counts.entriesWithSource += 1;
@new counts.entriesWithSource += 2;

# PREDICT SURVIVED — the read-failed fixture hits the directory-read catch, not this per-file read arm.
@defect S_FILE_READ | classify a per-entry knowledge read failure as SOURCES_MISSING
@old return failClosed('READ_FAILED', `cannot read ${relPath} (${error?.code ?? 'unknown error'})`);
@new return failClosed('SOURCES_MISSING', `cannot read ${relPath} (${error?.code ?? 'unknown error'})`);

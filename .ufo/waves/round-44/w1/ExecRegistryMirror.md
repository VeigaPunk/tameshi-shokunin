# ExecRegistryMirror — registry mirror gate

Axis: freshness. Scope: scratch mirror only; no lane implementation files changed.

Built `/tmp/tameshi-r44-ExecRegistryMirror-/corpus/` from the lane's `corpus/`, inserted a draft S160 before the tail note, and added the planned knowledge entry at `corpus/knowledge/r44-anchor-refresh-rule.md` (scratch only). A second mirror has one data row indented by two spaces.

Validate output (unindented draft):
```
file W04 S047 duplicate url pitest.org/quickstart/incremental_analysis across scopes
file W04 S048 duplicate url pitest.org/quickstart/incremental_analysis across scopes
file W04 S075 duplicate url man7.org/linux/man-pages/man1/strace.1.html across scopes
file W04 S076 duplicate url docs.jj-vcs.dev/latest/git-compatibility across scopes
file W04 S077 duplicate url man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html across scopes
file W04 S078 duplicate url man7.org/linux/man-pages/man2/open.2.html across scopes
file W04 S081 duplicate url bazel.build/reference/test-encyclopedia across scopes
file W04 S092 duplicate url bazel.build/remote/caching across scopes
file W01 S101 tierC mined used-by=corpus/knowledge/witness-equivalence-rule.md
file W04 S104 duplicate url cgit.git.savannah.gnu.org/cgit/bash.git/plain/doc/bashref.texi?id=b8c60bc9ca365f8261fa97900b6fa939f6ebc303 across scopes
file E12 S160 row outside Registry section
file E11 S097 missing used-by tools/tally-audit.py
file E11 S102 missing used-by tools/tally-audit-v3.py
file E11 S104 missing used-by tools/tally-audit-v3.py
EXIT=1
```

Important: inserting immediately before `- Next unused id: S160.` (the apparent tail note, after `## Id allocation`/round history) placed S160 outside `## Registry`, producing E12. This is not a census-valid placement, and the S160 row draft's mere textual presence should not be taken as validated. The separate two-space-row validate also exits 1, with the same warnings and pre-existing E11 errors but no S160 E12; row count command output was `456`, confirming the indented data row was counted. (The count invocation in that combined command prints the count after the exit line.)

Warnings are W04 ×9 and W01 ×1. E-codes: E12 for unindented mirror; E11 ×3 (existing S097/S102/S104 missing used-by paths). Indented mirror retains those E11s. No tools installed.

Evidence commands: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /tmp/tameshi-r44-ExecRegistryMirror-/corpus/SOURCES.md` and the same command with `corpus-indented/SOURCES.md`; both observed exit 1. Snapshot inspected: 38,687 bytes, SHA-256 `79f6501ad8f2a74e647532dba8f77f17482afa70ccbe6821d2368092454079ce`.

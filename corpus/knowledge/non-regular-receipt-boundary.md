source: S291 — https://git-scm.com/docs/index-format, Index entry / 4-bit object type; round-83 before-controls and committed receipt fixture
verified-at: 2026-11-04; instruments b654c00905536eaf60334f6d90a234467accad24
recheck: python3 -I -X utf8 tools/receipt-bytes-bind.py --selftest; python3 -I -X utf8 tools/receipt-revision-gate.py --selftest

# A symlink is a pointer, not a regular receipt

Git's Index entry section distinguishes regular-file and symbolic-link object types. This grounds the distinction, not Python filesystem behavior. The executable evidence is the lane's own fixture: `.ufo/fixtures/round-83/c3/root/` contains a symlink and a regular sibling with identical readable receipt content.

At base c63467bb, the receipt sweep follows the symlink and measures both entries bound; the revision gate passes both (`.ufo/evidence/round-83/controls/c3-before-symlink-bound.txt`, `c3-before-gate-passes.txt`). The changed instruments inspect each leaf with lstat: the sweep names the link `unbound detail=not-regular-file`; the gate names `RECEIPT_NOT_REGULAR`. The regular sibling remains bound/PASS. Their isolated suites demonstrate the same distinction with named finding IDs (14/14 and 20/20).

Limits: lstat followed by open is not an atomic hostile-filesystem boundary. Parent-directory aliases and symlinked directories are not closed by checking the leaf alone. These are read-only local evidence tools, not sandbox enforcement. The round's frozen C3 summary incorrectly declares one fixture entry; the committed fixture has two. That numerical target is not silently changed, and the round reports an honest stop despite the real behavioral improvement.

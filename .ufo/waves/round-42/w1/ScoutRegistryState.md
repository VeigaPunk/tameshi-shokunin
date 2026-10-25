# Registry state (base `c77c2b7e64d2e356381441ecf94abac03e984606`)

- **Observed row census:** `grep -cE '^\| {0,3}S[0-9]{3} \|' corpus/SOURCES.md` in the lane → 109 S-rows; highest id S154; column-8 status counts: mined 81, queued 22, rejected 6. The same count after the zero-to-three-space extractor variant returns 109; 4-space rows are excluded. IDs S155, S156, S157 are free (`grep -nE '^\| {0,3}S(155|156|157)[^0-9]' corpus/SOURCES.md` → no matches). Relevant extractor evidence: `.ufo/evidence/round-42/calibration/measure.py:77` uses `^ {0,3}\|[ \t]*S(\d{3,})`.
- **Scorecard standing row:** `SCORECARD.md:1993` last `| sources-registry |` row states **109 rows at round 41**.
- **Validation:** exact command `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → code summary: W04 for duplicate URL across scopes at S047, S048, S075, S076, S077, S078, S081, S092, S104; W01 at S101 (tier-C mined with used-by); final `tameshi ok /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md`; exit **0**.

No tools installed or updated. No live checkout edits.
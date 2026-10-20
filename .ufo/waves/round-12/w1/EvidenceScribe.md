# EvidenceScribe — tameshi-r12-w1 (advisory, lane-internal)

Not independent non-author promotion or admission. Nothing here is a pass.

## Behavior
Inventoried evidence requirements for: (A) source census validate exit 0; (B) repeat-control calibration gate (C1); (C) bash-surface-census declared-witness split (C2). Start HEAD checked: `18ad5d050ef4bcd830fe513825baed878f025024` (matches).

## Gates
- Observed by this seat: start HEAD match; file digests; provenance of the recorded census artifacts. Read-only.
- Not executed by this seat: the source census validator, `repeat-control.py` (file absent at read time), BashWitness study, kagi `--selftest`. All listed as commands for L1 with expected values labelled as prior records or contract expectations, not observations.

## Touched surfaces
- Written: `.ufo/evidence/round-12/EvidenceScribe/inventory.md`, `.ufo/waves/round-12/w1/EvidenceScribe.md`.
- Read only: `PROVINCE.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, `corpus/knowledge/*` (census/witness notes), `.ufo/evidence/kaika-round-1/*`, `.ufo/waves/round-12/{spec,dispatch}.json`, `~/.omp/agent/RULES.md`.
- Not touched: product code, `tools/`, corpus registry, sibling repos, commits.

## Findings
1. **Start HEAD matches** the assignment (O).
2. **Recorded census run is stale against live registry.** `sources-census-v2.txt` (sha `b97f509a…1430`, commit `121696b` 19:22:35) predates the last `corpus/SOURCES.md` commit `01b358c` (19:34:41). Counts agree (44 rows); content not proven current. Fresh run required (O).
3. **Recorded run has no exit code.** Its last line is `SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)`; exit must be captured on a fresh run (O).
4. **Contract document missing.** `corpus/SOURCES.md:4` cites `SOURCES-CONTRACT-v1.md`; `find / -xdev -name 'SOURCES-CONTRACT*'` finds nothing (O). "Contract v1 clean" wording has no file to cite.
5. **Stale/misleading census artifacts.** `sources-census.txt` (37 rows, other worktree) and `sources-census-final.txt` (no verdict line) must not be cited as current or CLEAN (O).
6. **B1 is informational** (count=25), not a gate result (O, script header).
7. **Validator scope is shape + id-cite only.** It does not verify row content truth or `opened` against `sources-opened.tsv` (I, from script read).
8. **repeat-control not on disk.** `tools/repeat-control.py` absent at read time; all C1 rows are unobserved expectations (O).
9. **Witness blindness is partial.** Declaration hash/mtime ordering is the only evidence; any reanalysis is not a seventh gate (contract; prior F2 wording).

## Out-of-scope items
- Running the validator, repeat-control, witness study, or kagi selftests (assigned to L1 / owners).
- Copying the validator into round-12 evidence (L1 decision; MK-6 applies before commit).
- Verifying row content truth in SOURCES.md.

## Tool installs
None by this seat. Available: python3 3.14.7, shellcheck, jq.

## Artifact paths
- `.ufo/evidence/round-12/EvidenceScribe/inventory.md` (full command table, expected values, risks)
- `.ufo/waves/round-12/w1/EvidenceScribe.md` (this report)
- Referenced (read-only): `.ufo/evidence/kaika-round-1/sources-census-v2.sh` (sha `b9b75471…a2bc3`), `.ufo/evidence/kaika-round-1/sources-census-v2.txt` (sha `b97f509a…1430`)

## Check list for L1 (run once, after all seats land)
1. `git rev-parse HEAD` → `18ad5d05…5024`
2. `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh > <round-12 evidence>/sources-census-v2.run1.txt 2>&1; echo exit=$?` from repo root
3. `python3 tools/repeat-control.py --selftest; echo exit=$?` and the C1-2…C1-8 fixtures in inventory §2
4. BashWitness: TSV hash and mtime precede run log; kagi pin before/after; `bash <kagi>/corpus/surface-census.sh --selftest; echo exit=$?`

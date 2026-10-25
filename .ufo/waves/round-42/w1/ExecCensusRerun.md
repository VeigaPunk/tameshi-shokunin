# ExecCensusRerun — round 42, wave 1

Seat: `L1Tameshi42.ExecCensusRerun` (leaf). Scope: census start rerun + append-path parse proof on a scratch mirror. No tool installs (none needed; no pacman/npm/uv action taken).

## Finding 1 — live lane validate rerun matches the frozen baseline exactly

Command (run 2026-10-25):

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
```

Result: **exit 0**, 11 output lines = **9 × W04 + 1 × W01 + 1 ok line**. Output is byte-identical to the frozen baseline `.ufo/evidence/round-42/census-sources/start.stdout` (11 lines):

- `cmp /tmp/tameshi-r42-ExecCensusRerun-live.out …/census-sources/start.stdout` → `CMP=identical`
- sha256 both `bb8c4162239efce3e0e798ed19c66d0949873269df53b638fc147c3d037af621`

W04 rows: S047, S048, S075, S076, S077, S078, S081, S092, S104 (duplicate url across scopes). W01 row: S101 (tierC mined used-by=corpus/knowledge/witness-equivalence-rule.md). `ok` line: `tameshi ok /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md`. Zero E codes. This matches the expected set exactly (exit 0, 9 × W04 + 1 × W01).

## Finding 2 — append path parses before the real rows exist (scratch mirror)

Built `/tmp/tameshi-r42-ExecCensusRerun-mirror/corpus/` as a copy of the live `corpus/` (`cp -a`), appended three 11-column rows after the S154 row in its `SOURCES.md` `## Registry` table:

- `| S155 | PIT basic concepts (parity test row) — https://pitest.org/quickstart/basic_concepts/ | docs | A | PIT basic-concepts page (append-path parse proof) | §Getting started @ page fetched 2026-10-25 | test row for append-path parse: PIT basic concepts claim shape | mined | 2026-10-25 | 180d | corpus/knowledge/r41-variable-destination-writes.md |`
- `| S156 | PIT FAQ (parity test row) — https://pitest.org/faq/ | docs | A | PIT FAQ page (append-path parse proof) | §Frequently Asked Questions @ page fetched 2026-10-25 | test row for append-path parse: PIT FAQ claim shape | mined | 2026-10-25 | 180d | corpus/knowledge/witness-equivalence-rule.md |`
- `| S157 | Python argparse documentation (parity test row) — https://docs.python.org/3/library/argparse.html | docs | A | argparse dest option semantics (append-path parse proof) | §dest — The name for the attribute @ docs page fetched 2026-10-25 | test row for append-path parse: argparse --out dest claim shape | mined | 2026-10-25 | 180d | corpus/knowledge/r41-variable-destination-writes.md |`

All three: status mined, used-by an existing knowledge file (present in the mirror), distinct URLs (pre-checked against the registry: no collision with any existing normalized URL), opened 2026-10-25, recheck 180d, tier A/docs (no W01/W03/E05/E06/E07/E08/E09/E11).

Run 1 — corpus-only mirror:

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /tmp/tameshi-r42-ExecCensusRerun-mirror/corpus/SOURCES.md
```

Exit **1**; codes: 9 × W04 (same rows as live), 1 × W01 (S101), **3 × E11** — all three E11s are pre-existing rows whose used-by points outside `corpus/`, absent from the corpus-only mirror: `E11 S097 missing used-by tools/tally-audit.py`, `E11 S102 missing used-by tools/tally-audit-v3.py`, `E11 S104 missing used-by tools/tally-audit-v3.py`. None touch S155–S157 (grep for S155|S156|S157 in output: zero hits).

Run 2 — mirror completed with the three used-by targets stubbed (empty `tools/tally-audit.py`, `tools/tally-audit-v3.py` at mirror root, exactly the paths E11 complained about):

Exit **0**; codes: 9 × W04 + 1 × W01 + 1 ok line — the same warning set as the live lane, zero E codes, zero findings for S155–S157.

Row-count proof (census): `sources-census.sh census --file <mirror>/corpus/SOURCES.md` → `file rows 112` (109 existing + 3 appended), `tier.A 100`, `status.mined 84`, no invalid tier/status. The three appended rows are parsed and counted.

Conclusion: the append path parses; S155–S157 are syntactically valid 11-column rows (NF=13) accepted with no E/W codes of their own, and the mirror registry validates clean (exit 0) once the pre-existing non-corpus used-by targets are present. The 3 × E11 in run 1 are a mirror-completeness artifact, not an append defect.

## Not checked

- Did not run any round-42 counter against the lane (C1/C2 deciding runs are the L1's). No `--rev` counter runs performed.
- Did not edit the live lane checkout; only the scratch mirror and this report were written.
- Scratch mirror `/tmp/tameshi-r42-ExecCensusRerun-mirror/` and `/tmp/tameshi-r42-ExecCensusRerun-live.out` were deleted after evidence capture (validation outputs reproduced inline above).

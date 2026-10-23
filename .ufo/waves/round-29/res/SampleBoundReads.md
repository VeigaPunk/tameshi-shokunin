# SampleBoundReads — residual spot-check, four appended cold-read entries (round 29)

Verdict: all four sampled entries HOLDS. Reports support their recorded verdicts; every listed trace receipt exists at E, carries `rev` = 9f3084bc60ad56aac01e4556ef4c7653df2f65e5, and its `argv` matches the commands each report claims; one cheap command per entry re-ran clean in a fresh clone at 9f3084bc.

Lane head at check time = 7a45f7b9d6a2542a553276330c8b02ac2e28c7ef (E, = `master`). No newer lane commits, so nothing extra to measure.

Method: ledger `.ufo/evidence/round-21/coldread/ledger.json` entries 371–392 (22 appended). Sampled: Read01A (371, instruction, executed-ok), Read03B (376, record, verified-record), Read04C (380, instruction, gap-minor), Read10C (389, instruction, executed-ok — the Round-18 registry entry and the moved-report case). Clone: `/fast/scratch/hyaku/tameshi-r29-SampleBoundReads`, `git clone --no-hardlinks` + `--detach 9f3084bc60ad56aac01e4556ef4c7653df2f65e5`, GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset throughout.

## Per entry

### 371 — Read01A, SKILL.md:131 mutation-sweep recipe — HOLDS
- Report `.ufo/waves/round-29/w1/Read01A.md` (sha256 `573b5f8e…` at E) verdict executed-ok, zero gaps; claims 3 commands under `tools/trace-inputs.py`.
- Traces Read01A-1..3 all exist at E, `rev`=9f3084bc, exit 0; argv matches claimed inner commands verbatim (corpus dump; `node …/kimi-census.mjs --selftest`; `bash …/surface-census.sh --selftest` from pinned external revs).
- Re-run: pinned blob `kagi-shokunin@fecee874:corpus/surface-census.sh` sha256 = ledger `external_inputs` (`275d8294…`, OK); extracted to /tmp and ran `--selftest` → `SELFTEST: PASS (16 cases)`, 14 ok-cases + skip 15/16 substrate-absent, exit 0 — matches report line "14 executed plus skip-case 15/16". Kumitate blob `175de6ba:scripts/kimi-census.mjs` also hashes to the pinned `83016d45…`.

### 376 — Read03B, SKILL.md:1380 artifact map — HOLDS
- Report (sha256 `f6776685…` at E) verdict verified-record; 4 traced corpus/plans dump commands, exits 0, argv matches.
- Re-run: sha256 of all 36 `inputs` files recomputed in the 9f3084bc clone — 36/36 match the ledger, 0 mismatches. Record claims spot-read (per-row verification prose) consistent with a verified-record verdict.

### 380 — Read04C, SKILL.md:1479 round-12 repeated controls — HOLDS
- Report (sha256 `81320038…` at E) verdict gap-minor with exactly one minor gap: shorthand `mismatch/expected.json` does not resolve against `.ufo/evidence/round-12/`; real path is `ControlGate/mismatch/expected.json` (report cites sha256 `57f010e9…`).
- 7 traces, all `rev`=9f3084bc; exits 0 except Read04C-7 exit 1 — and the report itself claims `check` exits 1 with `WITNESS_CHECK: DRIFT tools/mutate-and-run.sh … committed=75ed934d…`, so the nonzero exit is honest, not hidden.
- Re-run in clone: `python3 tools/bash-witness-study.py count` → killed_on_witness=8, survived=2 (B5,B10), declared_none B5,B10, exit 0; `check` → identical DRIFT line (sha256=fb91ef76… vs committed=75ed934d…), `FAIL (1 problems; 96 files covered)`, exit 1. Both match report §"What I checked" verbatim.

### 389 — Read10C, SKILL.md:1925 round-18 gate/probe registry — HOLDS
- Report sha256 at E = `fafd4c3698e38009f7742352600b9aaf6d220145ed5543549e375cc8a34b03e8` — the claimed byte-exact fleet-root move hash matches.
- 7 traces (numbered 1–6,8 — no -7 exists, but `commands_executed` also lists 7 and ledger `commands_executed_count`=7, consistent), all `rev`=9f3084bc, exit 0; argv matches report commands including `--only P09/P10/P08` runs at `--rev 9f3084bc`.
- Re-run in clone: `python3 .ufo/evidence/round-19/coldread/measure.py --selftest` → `SELECTOR_SELFTEST: 3/3 pass` exit 0 (report receipt 5); `python3 .ufo/evidence/round-18/defect-probes.py --selftest` → `SELFTEST: PASS (6 cases)` exit 0 (report receipt 2). Report's per-probe closure claims (P09 exit-2 timeout_s_named, P10 kill-path survivors=[], P08 G2/G3 anchors) corroborated by the trace exits and source line cites.

## Notes
- Read04C trace -7 exiting 1 is correctly disclosed in the report (the section documents the stale pin); not a defect in the entry.
- Trace numbering skips Read10C-7 with no gap in command count; benign.
- No tools installed; pacman untouched. Only file written in the lane: this report. `/tmp/SBR01A` and the clone are scratch outside the lane.

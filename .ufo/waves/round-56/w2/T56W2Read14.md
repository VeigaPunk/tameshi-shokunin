# T56W2Read14 — cold-read report

**Heading:** `### Round-18 gate/probe registry — routed-defect closure`  
**Candidate:** `c0137451f5b7f22d65f748fc69f1b181f55e1378`  
**Section:** C0 lines 1968–1980; frozen round-18 `sectionize()` SHA-256: `661f63518af62b198f68ec5400778d9662df725d84744ad428dacc08823e6d7e`  
**Verdict:** `verified-record` (no false statements or failed named commands found).

## Commands run

- Loaded `.ufo/evidence/round-18/measure.py` as the frozen sectionizer, ran `git show C0:SKILL.md`, and sectionized the page. It returned lines 1968–1980 and the SHA above. At base `981c5e8`, the heading began at line 1955.
- `python3 .ufo/evidence/round-18/defect-probes.py --selftest` — `SELFTEST: PASS (6 cases)`, exit 0.
- `python3 .ufo/evidence/round-18/defect-probes.py --rev C0` at the lane root — `DEFECT_PROBES: open=0 closed=11 total=11`, exit 0. P05–P07 were closed with pristine exit 0 and mutant exit 1. Usage invocations exited 64.
- Ran defect-probes from an isolated scratch clone: P11 could not find the fleet sibling `kagi-shokunin`, so the probe returned exit 2. At the lane root, with the sibling available, P11 closed and all 11 probes passed.
- Wrapped defect-probes in `tools/trace-inputs.py`: P05–P07 reported pristine selftest failure (`SELFTEST: 5/30`); defect-probes returned exit 2, recorded in the trace receipt. This confirms the documented nested-ptrace warning.
- `python3 tools/registry-check.py --selftest` — 51/51 pass, exit 0. Separate scratch registry fixtures with `timeout_s: NaN` and `timeout_s: 90000` each returned exit 2 and named the invalid row. P10 confirmed setsid/setpgid descendants were killed (`survivors=[]`).
- `python3 tools/evidence-disposition.py --selftest` — with `jj` on PATH: 66/66 pass, exit 0; without `jj`: 3/66 jj-dependent cases failed, exit 1. The round-18 dispositions manifest passed; the round-17 manifest returned exit 2 (`expected_input_digest_mismatch`).
- `python3 tools/bash-witness-study.py count` and `selftest` — exit 0; selftest 51/51 pass. Verified `PIN_BASH` and `REV_BASH` at `tools/mutate-and-run.sh:616-617`, and the `4acc607…` historical input in the round-18 dispositions manifest.
- `python3 tools/trace-inputs.py --selftest` — 30/30 pass, exit 0. The promoted and round-17 copies have different SHA-256 values; the round-17 copy's last changing commit is the round-17 landing.
- `python3 .ufo/evidence/round-18/measure.py --rev C0 --explain` — exit 0; selftest 98/98 pass. `python3 .ufo/evidence/round-18/coldread/assemble.py --selftest` — 80/80 pass. `--carry` copied all 159 entries and added `carried_from`.
- `python3 .ufo/evidence/round-19/measure.py --repo <lane> --rev C0 --check` — corrected 5/5, exit 0; without `--check`, it reported counts and exited 0. Selftest 43/43 pass; bad usage exited 64.
- `python3 .ufo/evidence/round-19/coldread/measure.py --repo <lane> --rev C0` — exit 0; selector selftest 3/3 pass. Compared ledgers: all 159 round-18 entry keys remain in round 19 with no shared-entry content or `carried_from` differences.
- `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` — exit 0.

## Notes for L1

- The phrase “no legacy overrides” in the round-19 cold-read row is ambiguous. The round-19 selector defaults to its own ledger and its selftest confirms no fallback to the historical ledger. However, it still accepts and honors `--ledger-file` (the run reports `overrides_used=true`); the round-20 selector is the one that explicitly refuses override flags. Consider clarifying that this means “no historical-ledger fallback,” not “override flags are refused.”
- The round-18 manifest's `supersedes` field names the round-14 manifest, not round 17; the round-17 manifest is operationally retired (gate exit 2), while round 18 passes. The “round-17 manifests are superseded” wording is true operationally but not a direct manifest `supersedes` pointer.
- The UID-change limit is in `tools/registry-check.py`'s docstring; `SentinelKillCode.md` covers adopted-orphan signaling and same-tick PID reuse, but not UID explicitly.
- P11 in defect-probes depends on `kagi-shokunin` being available as a fleet sibling; a scratch clone outside that layout returned exit 2. At the live lane root, P11 passed.
- Out-of-section round-level observation: census validation exits 0, but the current tameshi census is 142 rows; base had 140 and C0 adds S281 and S282. This differs from the brief's “141 rows” parenthetical and may need L1 reconciliation.

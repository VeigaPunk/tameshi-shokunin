# Section audit — SKILL.md 1925–1937 (Round-18 gate/probe registry)

**Verdict:** blocking  
**Read revision:** `790abd2129f153c13b471e381d454186edbde65e` (matches `HEAD`)  
**Span:** lines 1925–1937, heading `### Round-18 gate/probe registry — routed-defect closure`  
**Axes:** calibration (assertion vs pinned source), citation fidelity, prose duplication (simplifier)  
**Tool installs:** none

## Summary

Eight registry rows document round-18 routed-defect closure instruments. Six rows align with code and cited evidence at the pin. Two rows carry **blocking calibration gaps** (selftest artifact names; live vs frozen trace-inputs identity). One row mixes accurate historical context with current behavior correctly.

Evidence mark: `.ufo/waves/round-21/w2/sections/1925.json`.

---

## Row-by-row findings

### `.ufo/evidence/round-18/defect-probes.py` (SKILL.md:1929)

**Agrees with source.**

- Eleven probes: `PROBE_IDS = tuple("P%02d" % n for n in range(1, 12))` (defect-probes.py:44).
- Success line `DEFECT_PROBES: open=… closed=… total=…` (defect-probes.py:956–957); exits 0 / 2 / 64 match module docstring (defect-probes.py:21) and `main` (defect-probes.py:1026–1081).
- Guard closure rule matches `guard_probe`: pristine selftest must pass; mutant nonzero ⇒ `closed` (defect-probes.py:383–392).
- Bwrap envelope with read-only fleet bind (defect-probes.py:192–200, docstring 4–12).
- P05–P07 target `tools/trace-inputs.py` selftest guards (defect-probes.py:82–101, 335–341); nested-ptrace warning is consistent with trace-inputs selftest design (tools/trace-inputs.py:702+).

**Dated vs current:** none in this cell.

**Deletion candidate (prose only):** parenthetical `(P05–P07 … nested ptrace is refused → 2)` duplicates the round-17 registry row (SKILL.md:1902) without adding a new rule.

---

### `tools/registry-check.py` (round 18) (SKILL.md:1930)

**Agrees with source.**

- Finite `timeout_s` in `(0, 86400]`: `MAX_TIMEOUT_S = 86400` and validation (registry-check.py:107, 238–256).
- NaN/Infinity refused: selftest cases `timeout-nan`, `timeout-infinity` (registry-check.py:1502–1504).
- Invalid timeout ⇒ exit **2** with row naming (registry-check.py:846+, 1502–1524), not the old communicate crash exit **1**.
- **Historical assertion (accurate):** “a larger finite value used to crash `communicate()` with exit 1” matches comment at registry-check.py:104–106; current behavior is cap + exit 2 at parse.
- `cleanup_error` on survivor descendants (registry-check.py:707, 727); limits match `.ufo/waves/round-18/w2/SentinelKillCode.md` (file present at pin).

---

### `tools/evidence-disposition.py` (round 18) (SKILL.md:1931)

**Agrees with source.**

- `--selftest` requires `jj`: docstring (evidence-disposition.py:120–121) and `_jj_init_fixture_repo` paths.
- G2/G3 anchor via `lane.branch` → `refs/heads/…`, jj colocated without branch ⇒ exit 2 path `CouldNotEvaluate` (evidence-disposition.py:460–525).
- Detached non-jj: anchor only when branch or remote-tracking ref contains HEAD (evidence-disposition.py:503–525); HEAD not used as jj lane tip (evidence-disposition.py:492–496).

**Dated vs current:** “unchanged CLI” is current; jj requirement is round-18 addition (stated).

---

### `tools/bash-witness-study.py` (round 18) (SKILL.md:1932)

**Agrees with source (registry-level, not inline path strings in the tool).**

- `git_clean_env` drops `GIT_*` and pins config null (bash-witness-study.py:333–338); used for `git show` in `materialize_target` (bash-witness-study.py:347–350).
- Pin `4acc607` for round-13 witness bytes: `historical_inputs["tools/bash-witness-study.py"].rev` in `.ufo/evidence/round-18/dispositions.json` (lines 20–22, full hash `4acc607dfd79f19d508bd50cdd06b77269fccd1d`).
- “Round-17 manifests superseded” matches round-17 disposition gate row exiting 2 and round-18 manifest live (SKILL.md:1850, 1835–1837); round-18 `dispositions.json` supersedes round-**14** file id, not round-17’s JSON—wording refers to **manifest generation**, consistent with § Round-17 re-pin.

---

### `tools/trace-inputs.py` (SKILL.md:1933)

**Partially wrong expectation (blocking gap 2).**

- **Current claim:** “as the round-17 copy (which stays byte-identical as evidence)”.
- **Evidence:** Frozen evidence bytes remain at `.ufo/evidence/round-17/coldread/trace-inputs.py` (SHA `521be955…` in round-18 ledger). Live `tools/trace-inputs.py` at `790abd` is SHA `f59c9312…` (`cmp` differs). Promoted path is what defect-probes P05–P07 exercise when present (defect-probes.py:335–341; `.ufo/evidence/round-18/c2-probes-v2-e08271a.txt`).
- **Accurate part:** Selftest fails when O_RDWR exclusion, private pycache prefix, or root execve guard removed—true on **live** tool (guard bytes at tools/trace-inputs.py:82, 516, 644); was **open** on round-17 evidence copy alone (c2-probes-v2-183f87b.txt).
- **Fix for L1 re-anchor:** Split “frozen round-17 evidence copy” vs “live promoted `tools/trace-inputs.py`” explicitly; do not imply byte identity for the live registry path.

**Deletion candidate:** “as the round-17 copy” clause could reference SKILL.md:1902 + round-17 evidence path instead of repeating byte-identical language here.

---

### `.ufo/evidence/round-18/measure.py`, `coldread/assemble.py` (SKILL.md:1934)

**Agrees with source.**

- Default ledger `.ufo/evidence/round-18/coldread/ledger.json` (measure.py:113).
- `--carry` adds `carried_from` (assemble.py:980, 1299–1315).
- `--explain` documented (measure.py:81, 1535).
- Input-keyed-only bound matches measure docstring and assemble trace schema.

**Deletion candidate:** trailing “never cite it as command coverage” duplicates § Input-keyed cold-read (SKILL.md:1855–1877).

---

### `.ufo/evidence/round-19/measure.py` (SKILL.md:1935)

**Exit map agrees; selftest provenance blocking gap 1.**

- Docstring and `main`: `--check` ⇒ 0 all five corrected / 1 open / 2 evaluate failure / 64 usage (measure.py:4–7, 400–439).
- Without `--check`, success path returns 0 with counts only (`return int(args.check and corrected != 5)` ⇒ 0 when `--check` absent).
- Selftest prefix `/tmp/tameshi-r19-ruler-*` (measure.py:380).
- Hardcoded `--repo /home/vgpnk/Projects/shokunin/tameshi-shokunin` matches default `Path(__file__).parents[3]` for this layout (measure.py:402).

**Blocking gap:** “expected values in `round-19/contract.json` and ruler literals, input digests in `before.json`”.

| Artifact | What section implies | What code does |
|---|---|---|
| `contract.json` | Selftest reads expected values | File exists (population R18-1…R18-5) but **never opened** by measure.py |
| `before.json` | Selftest input digests | Committed **output** of baseline `--rev` run; selftest builds inline snapshot and pins `source-baseline.txt` / `source-round18-final.txt` via `SOURCE_PINS` (measure.py:41–46, 244–264) |

`before.json` input SHAs for corpus files align with `SOURCE_PINS` / evaluate paths, but the **selftest does not load `before.json` or `contract.json`**. Wording overstates machine coupling; L1 must re-anchor against measure.py literals and sibling text fixtures, not those filenames alone.

**Deletion candidate:** QUALITY 37–39 / round-19.md tail repeats round-19 coldread row and round-20 registry disclaimers.

---

### `.ufo/evidence/round-19/coldread/measure.py` (SKILL.md:1936)

**Agrees with source.**

- Imports frozen round-18 `measure.py` (coldread/measure.py:18–21).
- Default ledger `.ufo/evidence/round-19/coldread/ledger.json` (coldread/measure.py:22, 89–92).
- Selftest scratch `tameshi-r19-selector-*` under `/tmp` (coldread/measure.py:30).
- Delegates `main` to round-18 module after ledger path overrides (coldread/measure.py:86–93).

**Deletion candidate:** L1-author / not blind cold-read / input-keyed-only block largely repeats SKILL.md:1935 and round-20 coldread row (SKILL.md:1951).

---

## Wrong expectations (count = 2)

1. **SKILL.md:1935** — selftest anchored on `contract.json` and `before.json` (implementation uses inline fixtures + `SOURCE_PINS` text files).
2. **SKILL.md:1933** — live `tools/trace-inputs.py` conflated with byte-identical round-17 evidence copy.

## Blocking gaps (count = 2)

Same two items: they would mislead source re-anchoring or independent cold-read if taken as executable recipes.

## Historical assertions (verified, not current bugs)

- Registry-check pre-cap `communicate()` crash exit 1 (registry-check.py:104–106), narrated in SKILL.md:1930 parentheses.
- Round-17 coldread trace-inputs frozen as evidence artifact (ledger SHA `521be955…`).

## Simplifier — safe prose deletions (not applied)

| Location | Duplicate of | Risk if removed |
|---|---|---|
| SKILL.md:1929 ptrace parenthetical | SKILL.md:1902 | Low — keep one canonical “never wrap trace-inputs” rule |
| SKILL.md:1934 input-keyed disclaimer | SKILL.md:1855–1877 | Low — table already states policy |
| SKILL.md:1935–1936 cold-read/L1 disclaimers | SKILL.md:1951, corpus/lessons | Medium — one cross-link may suffice |
| Repeated `unchanged CLI` on 1931–1932 | Round-17 registry | Low — could say “see round-17 row” |

## Commands run

- `git show 790abd…:SKILL.md` (line span)
- `cmp` / `sha256sum` on `tools/trace-inputs.py` vs `.ufo/evidence/round-17/coldread/trace-inputs.py`
- Static reads/greps on listed `paths_opened` at `790abd` (workspace equals pin)

No mutations, selftests, or F5 reproduction executed (per seat bounds).

---

Report: `.ufo/waves/round-21/w2/Section1925.md`  
Evidence: `.ufo/waves/round-21/w2/sections/1925.json`

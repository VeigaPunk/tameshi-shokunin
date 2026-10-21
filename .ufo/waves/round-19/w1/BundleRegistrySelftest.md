# BundleRegistrySelftest — audit of `registry-selftest` row, round-18 final receipt bundle

Seat: TameshiR19-2.BundleRegistrySelftest (scout, leaf — no dispatch). Date: 2026-10-21.
Scope: ONLY row `"registry-selftest"` of `.ufo/evidence/round-18/final/checks.json` vs retained
`registry-selftest.stdout` / `registry-selftest.stderr` bytes, frozen at baseline `7243e7f163f08978c8fd9b6c1ef67a2fefe7d190`.
Method: byte/static only. The selftest was NOT executed (per assignment). No tools installed. No production edits.

## Row under audit (observed)

`checks.json:25-34` (blob `d8c98a92…`, committed at `7243e7f1`, 2026-10-21):

- argv: `["python3", "tools/registry-check.py", "--selftest"]`
- revision: `921ef8077440f90d092aab4b9fdc750a45de1224`
- exit: `0`
- stdout_sha256: `7ecd750f53bf6fddf91016e96184cf9c185302a7e7d582ec1dcdb0bcbdc34256`
- No `stderr_sha256` field exists in the row schema (row records stdout digest only).

## 1. Digest match count — 1/1 recorded digests MATCH (observed)

- `sha256sum` of retained `final/registry-selftest.stdout` (2481 bytes) = `7ecd750f…34256` = recorded `stdout_sha256`. Exact match.
- Triple identity confirmed: recorded digest == worktree bytes == frozen baseline blob. `git cat-file blob 7243e7f1:.ufo/evidence/round-18/final/registry-selftest.stdout | sha256sum` = `7ecd750f…34256`; frozen blob id `5e975416…`; worktree clean (`git status --porcelain` empty for all audited paths).
- Stderr (no digest recorded): retained file is 0 bytes; frozen blob is `e69de29b…` (git's canonical empty blob). Consistent with a clean exit-0 run whose human output is on stdout in non-`--json` mode (source docstring `tools/registry-check.py:76-77`). Consistency only — unverifiable against any recorded value, since the schema records none.

Content corroboration (observed counts): retained stdout has 48 `SELFTEST_CASE … PASS` lines, 0 non-PASS case lines, exactly one trailer `SELFTEST: PASS (48 cases)`. Source return convention `tools/registry-check.py:1780-1783`: failure prints `(failed: …)` and `return 1`; pass prints trailer and `return 0`. Recorded `exit: 0` + trailer = internally consistent.

## 2. argv spelling vs CLI source — EXACT MATCH (observed)

- Quoted source blob `41541d75…` (identical at `921ef80`, `7243e7f1`, and worktree — `git ls-tree` + empty `git diff --stat 921ef80..7243e7f1 -- tools/registry-check.py`):
  - Docstring interface, `tools/registry-check.py:13`: `python3 tools/registry-check.py --selftest`.
  - Dispatch, `:1793-1797`: `if argv and argv[0] == "--selftest"` → `len(argv) != 1` → usage exit 64, else `return selftest()`. `--selftest` bypasses argparse entirely, so no required positional applies (this is what sank the sibling; see §4).
- Row argv `python3 tools/registry-check.py --selftest` is exactly the supported invocation; the retained stdout itself exercises the dispatch rule (`usage-selftest-extra PASS (exit=64)`).
- Docstring `:78-80`: "--selftest hermetic; fixtures only under /tmp, never touches the lane" — so the receipt's validity does not depend on live-tree state beyond the script blob, which is byte-identical across all three points.

## 3. Revision attribution — SOUND, with one precision (observed)

- `921ef807…` exists: "round-18: retained re-reads and three final SKILL corrections (ledger row, fleet config dating, timestamp interval)", 2026-10-20 18:28:40 -0300.
- It IS an ancestor of the frozen baseline `7243e7f1` ("round-18 verifier spot-check (integrator, hyaku): non-author admit/reject", 2026-10-21 00:51:38 -0300) — `git merge-base --is-ancestor` exit 0.
- Precision: the three `final/` evidence files are ABSENT from `921ef80`'s tree (`git ls-tree` returns nothing for them there) and first appear tracked at `7243e7f1`. So `revision:` attributes the tree the command ran against; the bundle itself was committed later, at the spot-check commit. Not a defect — the schema meaning is "graded tree", and the graded script blob (`41541d75…`) is identical at both commits.

## 4. Failed raw attempt vs current evidence — this row is NOT a failed attempt (observed + contrast)

- No failed `registry-selftest` attempt is retained anywhere under `.ufo/` (grep over the whole tree: hits only in `final/checks.json` and round-19 wave plan files quoting this very task text).
- The failed-raw-attempt signature lives on the SIBLING row `bash-witness-selftest` in the same bundle: `exit: 64`, `stdout_sha256` = `e3b0c442…b855` (SHA-256 of empty input), retained stderr ends "bash-witness-study.py: error: the following arguments are required: mode" (observed bytes). This is exactly routed defect §5.4 of `corpus/lessons/round-18-verifier-spotcheck.md` (2026-10-21): "Do not leave a failed invocation as the selftest row of the final receipt bundle."
- `registry-selftest` shows none of those markers: real content digest (not the empty hash), exit 0, full 48-case trailer, empty stderr. The distinct row `registry` (`exit: 1`) is the live registry replay — a different row, out of scope, and a recorded outcome rather than a failed selftest attempt.

[INFERENCE] The receipt is self-attesting: bytes prove internal consistency and provenance chain, but not that a process actually ran. Mitigations: script blob identity at the declared revision, hermetic design, and content a careless fabricator would not produce (per-case exit codes, timings). Residual unknown: no independent execution log exists in the audited evidence.

## 5. Reproducibility caveat (observed bytes; consequence inferred)

Two PASS lines embed wall-clock timings — `timeout-kills-setsid-pipe PASS (exit=1 elapsed=1.116s …)` and `timeout-kills-setpgid-pipe PASS (exit=1 elapsed=1.117s …)`. The stdout is therefore not byte-reproducible on a re-run even at the identical revision. The recorded `stdout_sha256` is a one-time receipt-of-run, not a reproducibility oracle. Any future re-measurement that re-runs and compares digests would produce a false mismatch.

## 6. Recommended preserved-history treatment

1. No correction owed to `registry-selftest`. It is not one of the five §5 routed defects; do not rewrite, re-run, or regenerate it as part of C1's 5/5 correction — it is part of the frozen measurement surface and must stay immutable at `7243e7f1`.
2. Treat retained bytes as the receipt (attests the run passed 48/48 at the declared revision), never as a reproducibility target (see §5).
3. If round-19 adds stderr-digest coverage to receipt schemas, do it additively: a NEW receipt file or a dated named erratum (per lane contract), citing frozen blob ids — stdout `5e975416…`, stderr `e69de29b…`, checks.json `d8c98a92…`, script `41541d75…`. Never edit the frozen `checks.json` in place.
4. The §5.4 failed raw attempt belongs to `bash-witness-selftest`; when C1 corrects it, supersede (append the corrected row plus a dated erratum) rather than deleting the failed attempt's retained bytes — preserve history.
5. Auditor re-verification recipe (no execution needed): `git cat-file blob 7243e7f1:.ufo/evidence/round-18/final/registry-selftest.stdout | sha256sum` → expect `7ecd750f…34256`; blob identity of the script via `git ls-tree` at `921ef80`/`7243e7f1`.

## Sources and commands

- Read: `.ufo/evidence/round-18/final/checks.json` (:1-85), `registry-selftest.stdout`, `registry-selftest.stderr`, sibling `bash-witness-selftest.stderr`; `tools/registry-check.py` (:1-83, dispatch at :1793-1797, selftest return at :1780-1783); `corpus/lessons/round-18-verifier-spotcheck.md` §5-§7.
- Commands: `sha256sum`, `wc -c`, `grep -c` (case/trailer counts), `git --no-pager show -s`, `git ls-tree`, `git merge-base --is-ancestor`, `git diff --stat`, `git cat-file blob | sha256sum`, `git status --porcelain`, `git hash-object` (no `-w`). All read-only.
- Observed outcome: 1/1 digest match; argv exact; revision attributed to a real ancestor of the frozen baseline; no failed attempt for this row; selftest not executed.

## Remaining unknowns

- Actual historical execution of the run is self-attested only (see §4 inference).
- Whether a failed `registry-selftest` attempt ever existed outside `.ufo/` (e.g., session logs) was not searched — out of assigned evidence scope.

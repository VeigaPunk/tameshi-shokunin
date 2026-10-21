# BundleRegistry — round 19 / wave 1

Audit of ONLY the `registry` row of `.ufo/evidence/round-18/final/checks.json` against the retained `.stdout`/`.stderr` bytes. Read-only; nothing executed; no production edits; no installs.

## Scope and axes

- **C1 / calibration:** this seat contributes measured receipt/metadata evidence only. It claims no calibration-score increase, no promotion, no new cold-read coverage, and no independent closure. The five routed §5 defects remain owned elsewhere.
- Axes walked: (1) digest match of retained bytes vs recorded digests, (2) argv spelling vs the CLI source at the pinned revision, (3) revision attribution of the row and of sibling captures, (4) failed-raw-attempt vs current-effective-evidence distinction, (5) preserved-history no-harm treatment.
- Adjacent rows (`registry-selftest`) were read only to bound the registry family; no other row is audited here.

## Sources and observed evidence

All paths under `/home/vgpnk/Projects/shokunin/tameshi-shokunin`; read on 2026-10-21, lane checkout HEAD observed at `21e79329f8bdcf01a62be63b3e46db4a7de6b6f9` (round-19 baseline `7243e7f163f08978c8fd9b6c1ef67a2fefe7d190` was not HEAD at read time; observation only).

1. `.ufo/evidence/round-18/final/checks.json` (85 lines, sha256 `fed3c8e6cba05c41d8fdcafc091328e3092e2018a42fb8a8594bd8b5815c671d`), row `registry`: argv `["python3","tools/registry-check.py","--rev","921ef8077440f90d092aab4b9fdc750a45de1224","--json"]`, `revision` `921ef807…1224`, `exit` `1`, `stdout_sha256` `fe15a4d046504df011b1052f4fb422109c1ee477dd3fb022936f6050a0861cf4`. No `stderr` path or digest field exists in the row, and no `stderr_sha256` appears anywhere in `checks.json`.
2. `final/registry.stdout` (97,035 B): sha256 recomputed `fe15a4d0…1cf4` — **exact match** to the row. Content: JSON with `"exit": 1`, `"held": 30`, `"rev"` and `"rev_resolved"` both `921ef807…1224`, root `/tmp/tameshi-registry-check-vdbzj6x3/…`, `registry_sha256` `3e6785ee…f1e6`, `"total": 31`.
3. `final/registry.stderr` (36 lines, 1,818 B, sha256 `17bd7861…ad6e`): the tool's plain-text `ROW …` summary ending `REGISTRY_CHECK: held=30/31 superseded=4`. Its row set matches the stdout JSON exactly (4 superseded rows; sole non-held row `sources-census expect=0 got=1 differs`). It is the same invocation's stderr, but **no digest binds it anywhere**.
4. `tools/registry-check.py` at `921ef807…1224` (blob `41541d75a90f3eaaea27a43e2f7bbbf71b6c92e7`, byte-identical at HEAD, 1,920 lines): usage (lines 11–13) documents `python3 tools/registry-check.py [--root DIR] [--rev REV] [--registry PATH] [--only NAME] [--tag TAG]... [--json]` and `--selftest`; parsing is hand-rolled (no argparse), usage failure exits 64 (line 54). Every recorded argv token is a spelled, documented option; under `--rev` the tool clones the pinned rev into a `/tmp` root, which matches the capture's `/tmp/tameshi-registry-check-vdbzj6x3` root and fully-relative (hermetic) argv.
5. Revisions (read-only `git log`/`merge-base`, no ref changes): `921ef807…1224` "round-18: retained re-reads and three final SKILL corrections" (2026-10-20 18:28:40 −0300); `5923d89ac491ec3d296905561a8ab0faf3fda65a` "round-18: close missing S076 citation, … receipt rule D/N instead of historical 10/4; retain final test runs" (2026-10-20 18:40:48 −0300). Both are ancestors of HEAD. `checks.json` contains no occurrence of `5923d89a`, `branch-aligned`, or `registry-success`.
6. Two further retained captures, **not rows of `checks.json`**:
   - `final/registry-success.stdout` (89,166 B): `"exit": 1`, `"held": 29`, rev `5923d89a…`, root `…-3h11bmss`. Its stderr ROW summary shows `sources-census` now held but `evidence-disposition-round18` and `…-round18-before` at `got=2 differs`; trailer `held=29/31`. **The file named "success" records a failed run.**
   - `final/registry-branch-aligned.stdout` (96,815 B): `"exit": 0`, `"held": 31`, rev `5923d89a…`, root `…-m5t4r8n4`; stderr trailer `held=31/31`. This is the only fully-held registry run retained. Its sha256 `6502cb38…17c4` is **bound outside `checks.json`**: `.ufo/evidence/round-18/coldread/ledger.json` records it in every snapshot digest map, and the `final/audit-*.stdout` cold-read receipts `OPEN` it as `sha256=6502cb38… bytes=96815` with an assertion `held == total == 31` (visible in `traces/L1/audit-*.json` argv text). The `registry.json` digest is identical (`3e6785ee…`) across all three runs.
7. `final/checks.json` itself is digest-bound: `coldread/ledger.json` records `".ufo/evidence/round-18/final/checks.json": "fed3c8e6cba05c41d8fdcafc091328e3092e2018a42fb8a8594bd8b5815c671d"` (recomputed match). `final/registry.stdout` is bound only two-hop: ledger → checks.json bytes → row `stdout_sha256` → stdout bytes. `registry-success.*` and all four registry stderr files are bound nowhere in round-18 evidence; round-19 wave reports (e.g. `w1/BundleAssembleSelftest.md`, `ReceiptIntent.md`) describe them but bind nothing.
8. `corpus/lessons/round-18-verifier-spotcheck.md` §5.4 (2026-10-21) directs: "Do not leave a failed invocation as the selftest row of the final receipt bundle." — the exact failure mode this row family must not repeat through naming or structure.

## Audit counts (registry row)

| Count | Result |
|---|---|
| Recorded stdout digests | 1; matches retained bytes 1/1 (`fe15a4d0…`) |
| Recorded stderr digests | 0 (schema has no field); retained bytes unattested (`17bd7861…`) |
| Exit agreement | row `exit 1` = stdout JSON `exit: 1` = stderr trailer `held=30/31` ✓ |
| Argv tokens vs CLI source | 5/5 spell-valid (`python3`, `tools/registry-check.py`, `--rev`, 40-hex value, `--json`); semantics consistent with usage at blob `41541d75`, unchanged through HEAD |
| Revision attribution (row) | internally consistent 1/1: row `revision` = capture `rev` = `rev_resolved` = `921ef807…1224`; commit exists, ancestor of HEAD |
| Revision attribution (pass evidence) | 0 bound in the row: the 31/31 pass is at `5923d89a…` (12 min later), recorded only in ledger/audit receipts, absent from `checks.json` |
| `checks.json` own binding | ledger digest `fed3c8e6…` recomputed match ✓ |

## Failed raw attempt vs current evidence

- **Observed:** the `registry` row is a **failed raw attempt** honestly retained — exit 1, held 30/31, sole differing row `sources-census`. It is the only registry run `checks.json` records.
- **Observed:** the current effective round-18 pass evidence is `final/registry-branch-aligned.stdout` (exit 0, held 31/31) at rev `5923d89a…`, digest-bound via `coldread/ledger.json` and the L1 audit receipts — outside the `checks.json` row structure.
- **Observed:** `final/registry-success.*` is an **intermediate failed run misnamed "success"** (exit 1, held 29/31, disposition rows differing after the receipt-rule change at `5923d89a…`).
- **Inference:** the run order 30/31 → 29/31 → 31/31 matches the fix sequence: first the S-census defect (routed §5), then disposition expectations realigned to the new receipt rule, then full hold at the same rev. The `5923d89a` commit message's "retain final test runs" (4-word quote, 2026-10-20) corroborates intentional retention of these captures.

## Recommendation — preserved-history treatment (append-only; no byte rewritten)

1. **Do not mutate `checks.json` or any retained capture.** `checks.json` is digest-bound in `coldread/ledger.json`; editing the row would break the bound chain and falsify preserved history. The failed raw attempt stays exactly as recorded.
2. **Append a new round-19 receipt** (same pattern as the R18-4 corrected receipt: explicit `revision`, `exit`, stdout+stderr paths and SHA-256, `supersedes`, `historical_receipt_preserved`) that binds `registry-branch-aligned.stdout`/`.stderr` as the effective registry-gate pass, stating revision `5923d89ac491ec3d296905561a8ab0faf3fda65a` explicitly — the §5-style defect "no receipt names the cited revision" must not recur here.
3. **Bind the unbound bytes in that same receipt:** digests for `registry-success.stdout`/`.stderr`, `registry.stderr`, `registry-branch-aligned.stderr`, and (directly) `registry.stdout`, since `checks.json`'s schema carries no `stderr_sha256` and three of these files are presently unattested anywhere.
4. **Name the misnomer in the erratum text:** `registry-success.*` is a failed intermediate (exit 1, held 29/31), never to be cited as pass evidence; the pass citation is `registry-branch-aligned.*`. This closes the naming-side recurrence of the §5.4 failure mode without touching retained files.
5. **Cite revisions explicitly wherever the pass is claimed:** pass at `5923d89a…`; the `checks.json` row remains the failed raw attempt at `921ef807…1224`; neither capture is at the round-19 baseline `7243e7f1…`.

## Limits and unknowns

- I did not execute the recorded argv (prohibited); argv fidelity is established against the pinned blob's usage text, not by a live parse.
- The elapsed times and the causal order of the three runs are inference from contents and commit timing; no retained log records wall-clock invocation order (unknown).
- `registry-selftest` row digest (`7ecd750f…`) also matched its retained bytes on recomputation; reported as boundary context only, not audited as an assigned row.
- Read-only git queries (`rev-parse`, `log`, `merge-base --is-ancestor`, `ls-tree`, `show`, `diff --stat`) were used; no ref/index/state was written. Commands: `sha256sum`, `wc -lc`, `diff`, `cmp`, `grep -m1`, `tail` over the six retained files; no tools installed.

# ReviewQ126 — Quarantine hand-check: tameshi round2 S126 (axis: depth)

## Verdict: PRESENT → ADOPT-ELIGIBLE — the quoted span is in the cited source; `payload-absent` does not survive the hand-check. Fabrication class does not apply.

## Register row checked

`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:221`:

```
| `tameshi` | round2 | S126 | `payload-absent` | https://github.com/VeigaPunk/tameshi-shokunin | `MTE_INTEROP: SETUP (regression exit 2)` | cited source, companion URLs and local artifacts were all checked; the quote is in none of them |
```

Assignment provenance: `.ufo/waves/round-40/dispatch-w1.json:350` ("Hand-check quarantined S126. Fetch the cited source. Present or refuse.").

## Row identity after the lane's id remap

- `/home/vgpnk/Projects/shokuknow/lanes/tameshi/ID-REMAP.md`: `| round2 | S126 | S130 |` (staged ids were renumbered at packaging; lane registry ended at S108, first staged id S109).
- Current merge row: `/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md:28` — **S130**, "tameshi's mutation-report interoperability instrument and its vendored report schema — tools/mte-interop.py, tools/vendor/mutation-testing-report-schema-3.9.0.tgz", own-work, tier A, `mined`, anchor `@ revision d16f9b5a, repository https://github.com/VeigaPunk/tameshi-shokunin` — the same cited URL the register row carries. Its recheck field contains the very span the register quotes: `currently reports 'MTE_INTEROP: SETUP (regression exit 2)'`.

## Hand check — cited source fetched

1. Repo page `https://github.com/VeigaPunk/tameshi-shokunin` — reachable, default branch `master`, Python, 9,303+ tree entries, README present.
2. Exact-span fetch at master:
   ```
   curl -fsSL 'https://raw.githubusercontent.com/VeigaPunk/tameshi-shokunin/master/.ufo/evidence/round-25/contract-amendment-1.json' \
     -o /tmp/tameshi-r40-ReviewQ126/remote-amendment-1.json
   # sha256 ff459c329b494573383b6350499cc4a30b3b2c70ec5af7c91ea8b3809c6e5972
   # diff -q vs lane file .ufo/evidence/round-25/contract-amendment-1.json → REMOTE-LOCAL-IDENTICAL
   ```
   Remote bytes carry the quoted span verbatim in `observed_failure.stdout`: `"stdout": "MTE_INTEROP: SETUP (regression exit 2)"`.
3. Same span also present at master:
   - `.ufo/waves/round-25/w1/C2Determinism.md` — 2 occurrences (fetched; sha256 528670205ec9d5d68db2970662e1fad29401f69f12ce6ceefc83c961e8824657).
   - `.ufo/waves/round-25/w1/C2LiveCheck.md` — §4 ("the tool then reports `MTE_INTEROP: SETUP (regression exit 2)`, exit 2") and §5 ("No fleet root → fail closed … prints `MTE_INTEROP: SETUP (regression exit 2)`, exit 2, wall 0.108 s").
4. Local lane checkout (HEAD `5641ed8` "round-40: freeze C1 write-form census and C2 S108 snapshot pin before data") agrees — `grep -rnF 'MTE_INTEROP: SETUP (regression exit 2)' .ufo/evidence/round-25 .ufo/waves/round-25` → **6 matches in 4 files**:
   - `.ufo/evidence/round-25/contract-amendment-1.json:11`
   - `.ufo/waves/round-25/w1/C2Determinism.md:205` and `:210`
   - `.ufo/waves/round-25/w1/C2LiveCheck.md` (2 hits)
   - `.ufo/waves/round-25/w1/C2TarSafety.md:120`

## Finding

The register's reason — "cited source, companion URLs and local artifacts were all checked; the quote is in none of them" — is factually false on both counts: the exact byte span sits in the cited repository at `master` (round-25 evidence receipt + three wave reports) and in four local lane artifacts. The `payload-absent` classification is a checker false positive, not a fabrication; the row is **adopt-eligible**.

## Residual risk / verification gaps

- [INFERENCE] Probable cause of the checker miss: the span lives under `.ufo/` dot-paths (evidence/waves receipts). A fetcher that skips dot-directories or only renders the repo landing page would report absent. The checker's code was not observed directly.
- Row-owner nuance (adjacent observation; predicate not rewritten): S130's recheck wording attributes the SETUP receipt to the unparameterized command "currently", but the recorded receipts observed it in a clone outside the fleet root (amendment-1 `where: clone under /fast/scratch/hyaku/tameshi-r25-a2/c2-clone`), and amendment-1's own note says the in-lane form without `--fleet-root` still works. Annotating that context is the row owner's call.
- I did not execute `tools/mte-interop.py` or any round-40 counter (the deciding run belongs to the L1 after settlement). Presence is established from recorded receipts inside the fetched tree, not a fresh execution.
- No edits anywhere: register, shokuknow, and the lane checkout are untouched. Scratch: `/tmp/tameshi-r40-ReviewQ126/`. No tool installs; pacman untouched (transactions paused).

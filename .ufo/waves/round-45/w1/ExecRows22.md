seat: ExecRows22

# C1 row re-verification: S108, S132, S152

All three fragments graded `verified` by the frozen counter at rev `3310e7be803516ca5934b4e949d91bcec824b179`.
Raw snapshots (S108.raw, S132.raw, S152.raw) and fragment JSONs are retained in
`/tmp/tameshi-r45-ExecRows22/` for L1 integration.

Commands (per row): fetch `curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o /tmp/tameshi-r45-ExecRows22/S###.raw '<URL>'`; extract `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-45/freshness/measure.py --extract /tmp/tameshi-r45-ExecRows22/S###.raw`; check `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-45/freshness/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 3310e7be803516ca5934b4e949d91bcec824b179 --check /tmp/tameshi-r45-ExecRows22/S###.json --snapdir /tmp/tameshi-r45-ExecRows22`.

## S108

- URL: `https://www.tensorflow.org/federated/golden_tests?hl=zh-cn`
- curl exit: 0; bytes: 111409; SHA-256: `9056c530ca6cc9dfe036f2acd523aec7e9d7aa312fd4a5fcb2a94ad74740ff4c`
- CHECK: `CHECK S108 verified ok`
- Note: The anchored 如何更新 .expected 文件？ passage still states .expected files are updated only via `--update_goldens` with `--test_strategy=local` and that the resulting diff must be checked; the quote grounds teaches by citing the exact flag and the diff check.

```json
{
 "id": "S108",
 "url": "https://www.tensorflow.org/federated/golden_tests?hl=zh-cn",
 "opened": "2026-10-25",
 "verdict": "holds",
 "raw_sha256": "9056c530ca6cc9dfe036f2acd523aec7e9d7aa312fd4a5fcb2a94ad74740ff4c",
 "quote": "可以通过使用参数 --test_arg=--update_goldens --test_strategy=local 运行受影响的测试目标来更新 .expected 文件。应检查由此产生的差异是否存在意外的变化。",
 "snapshot": ".ufo/evidence/round-45/freshness/sources/S108.raw.gz",
 "author": "ExecRows22",
 "note": "the anchored 如何更新 .expected 文件？ passage still states .expected files are updated only via --update_goldens with --test_strategy=local and that the resulting diff must be checked; the quote grounds teaches by citing the exact flag and the diff check."
}
```

## S132

- URL: `https://raw.githubusercontent.com/VictorGazzinelli/snapshot-testing/master/README.md`
- curl exit: 0; bytes: 10269; SHA-256: `8871d19c34165b60b5847f390955c247d8665758ecddb206448127bf3b1922ea`
- CHECK: `CHECK S132 verified ok`
- Note: The live README table still lists row D29 Snapshot Testing: Use With Care (Randy Coulman) among its primary documents, exactly as teaches claims.

```json
{
 "id": "S132",
 "url": "https://raw.githubusercontent.com/VictorGazzinelli/snapshot-testing/master/README.md",
 "opened": "2026-10-25",
 "verdict": "holds",
 "raw_sha256": "8871d19c34165b60b5847f390955c247d8665758ecddb206448127bf3b1922ea",
 "quote": "Snapshot Testing: Use With Care - Randy Coulman",
 "snapshot": ".ufo/evidence/round-45/freshness/sources/S132.raw.gz",
 "author": "ExecRows22",
 "note": "the live README table still lists row D29 Snapshot Testing: Use With Care (Randy Coulman) among its primary documents, exactly as teaches claims."
}
```

## S152

- URL: `https://repositorio.ufmg.br/bitstreams/271f8a97-e79d-4935-86fd-33515a3073ad/download`
- curl exit: 0; bytes: 1474183 (PDF 1.5); SHA-256: `65f9603f364d9e811312600b0a161943cdae09fe1dbd53dbe4f19e0699a89703`
- CHECK: `CHECK S152 verified ok`
- Note: The abstract still contains the fragility sentence: drawbacks such as fragility and lack of context can lead to false positives, exactly as teaches claims.

```json
{
 "id": "S152",
 "url": "https://repositorio.ufmg.br/bitstreams/271f8a97-e79d-4935-86fd-33515a3073ad/download",
 "opened": "2026-10-25",
 "verdict": "holds",
 "raw_sha256": "65f9603f364d9e811312600b0a161943cdae09fe1dbd53dbe4f19e0699a89703",
 "quote": "drawbacks such as fragility and lack of context can lead to false positives",
 "snapshot": ".ufo/evidence/round-45/freshness/sources/S152.raw.gz",
 "author": "ExecRows22",
 "note": "the abstract still contains the fragility sentence: drawbacks such as fragility and lack of context can lead to false positives, exactly as teaches claims."
}
```

## Tooling / hygiene

- No tools installed or updated this run; no pacman transactions; no network writes outside the three fetches.
- Scratch only under `/tmp/tameshi-r45-ExecRows22/` (fetches, normalizations, fragment JSONs).
- This report supersedes an identical-path report left by a prior dispatch of this seat (its S108 raw SHA-256 `a9b2752f…` differs from the current fetch's `9056c530…` because the TensorFlow page serves dynamic bytes; the current report matches the raw files and fragments retained in `/tmp/tameshi-r45-ExecRows22/`).
- No checks beyond the three scoped `--check` runs were executed.

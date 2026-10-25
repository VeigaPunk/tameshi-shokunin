# Round 39 lesson

author: tameshi L1 (Kimi fresh L1)
date: 2026-10-24

## Gate

Theme: F4 write-path / explicit update flag. One admit, two rejects. Sources
re-opened this round; access date 2026-10-24.

### Admit — `corpus/knowledge/r8-golden-update-flag.md` (S107, S108)

- S107 URL: https://raw.githubusercontent.com/tensorflow/federated/4d3a89c9b72f9c19352318d1457a5f7c01462824/docs/golden_tests.md
  Access 2026-10-24. Snapshot sha256 `eb9dcedcb042ab6af1d32b7d83e6f719826511951de33c49d0c3de94544c2abe`.
  Quote (16 words), §How do I update `.expected` files?: "`.expected` files can be updated by running the affected test target with the arguments `--test_arg=--update_goldens --test_strategy=local`."
- S108 URL: https://www.tensorflow.org/federated/golden_tests?hl=zh-cn
  Access 2026-10-24. Quote, 如何更新 .expected 文件？: "可以通过使用参数 --test_arg=--update_goldens --test_strategy=local 运行受影响的测试目标来更新 .expected 文件。"
- Staged ids S161 and S162 are the same documents. Renumbered to S107 and S108, the next free ids, because S105 and S106 already sit in the registry. The map is by URL, not by adding one to every staged id.
- Scratch census on the append block exited 0 before the registry append (`.ufo/waves/round-39/assimilation/census-scratch.exit`).

### Reject — staged `r4-gate-write-path-audit.md` (S137)

Reason: quarantined `payload-absent`. The cited revision `31687496` exists, and its subject is a round-35 tally receipt, not a write-path census. No census payload is in that tree.
Flip: a hand-check that locates a write-path census artifact at that revision whose counts reproduce.

### Reject — staged `r5-gate-write-site-census-corrected.md` (S141)

Reason: same class. S141 cites the same revision `31687496` for an 86-site census that is not in that commit. `payload-absent`, not a fetch failure.
Flip: the six pinned blobs and a re-run that returns 86 `writeFileSync` sites, located in the cited revision.

### Quarantine

The lane slice has 17 data rows. S137 and S141 were hand-checked and refused (above). The other payload-absent rows were not adopted. S113, S123 and S134 carry a prose "could not be fetched" class: unverifiable, not fabrication, and not appended. The register was not edited.

### Status changes

No existing row's status, recheck, or used-by changed. New rows only: S107, S108.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| vacuous | round-38 `no_harm_guard.depth_command_d` regex `^\s*leg` matches 0 ledger lines while command D counts 9 | none in the r38 contract; this round's C1 counter | successor guard uses the command D pattern; the r38 file is not edited; the counter fails a missing guard, the vacuous regex, and a constant 9 |
| parent-exit | `.ufo/waves/round-38/w1/dispatch-outcome.md` — dispatcher parent exited, 65 seats aborted | none at the time; criterion 78 this round | `tools/wave-parent-settle.py` classifies a parent exit before the last seat terminal as UNSETTLED; the red fixture fails if that receipt is called SETTLED |
| number-drift | a first census pattern treated a variable named `golden` as an expected-value path | found before any deciding run, so not a scored miss | the pattern counts a string literal only; planted controls still discriminate |

## Holds

- The census pattern does not see shell redirects, `os.replace`, or an `open()` whose path is not a string literal on the same line. It also does not treat `expected.json` as an expected-value token. Seats found both limits: `tools/registry-replay.py:123` writes `expected.json` via `.write_bytes`, and `tools/bash-witness-study.py:778` uses `os.replace`. `live_unflagged` is the frozen pattern's count, not a claim that no unflagged write exists. The tool pin was not moved after those seats scored.
- POSIX `diff` remains the only exit lattice this lane has pinned. `cmp` and `git diff --exit-code` stay unmeasured.
- The round-38 L0 question `d0531d78` is not re-filed. This round does not repeat the parent exit; it does not ask the operator again.

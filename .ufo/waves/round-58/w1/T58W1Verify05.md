# T58W1Verify05 — row verification

Base: `2a32aa8228d5f86a85c81a923a3148bf792a9538`. Scratch clone detached at base.

| ID | Status at base → proposed | Basis / commands |
|---|---|---|
| R52.5 | fixed → fixed | `git show BASE:tools/registry-check.py` lines 761–772 showed `strict_scratch_root()`: uses TMPDIR when set, rejects unusable roots, and falls back to platform `tempfile.gettempdir()` only when unset. `git log --format='%H %s' --all -- tools/registry-check.py` located 5b703c6f (round-53 fix pass 2) as the introduction; its full hash recorded in JSON. Routed lesson is at c1d49d76, before this fix. |
| R52.6 | open → open | `git show BASE:corpus/lessons/round-52-verifier-spotcheck.md`, lines 23–24, documents missing “Landed changes” and “Before → after measurements” sections and the one-line-for-four-boxes SHONEN issue. Proposed round-58 intent: append-only correction to the historic report-contract item. |
| R53.1 | open → open | `git show BASE:.ufo/evidence/round-53/c1/measure.py`, lines 93–100, showed `ls-tree --name-only` against the coldread directory and the `rekey-dir-count=0` branch. Proposed intent: repair pathspec and rerun deciding counter with receipts. |
| R53.2 | open → open | `git ls-tree -r --name-only BASE .ufo/evidence/round-53/after` returned no paths. `git show BASE:corpus/lessons/round-53-verifier-spotcheck.md` line 79 explicitly records missing committed deciding receipts and directs the fix. Proposed intent: run/commit deciding counters and correct past-tense pointers. |

All commands above ran against the detached base clone (or queried its Git objects); no conclusions copied from another seat. Proposed open rows remain open; planned intents are not represented as completed fixes. No declines. Scratch removed before handoff. No tests/build/lint were run (parent-owned post-integration gate).

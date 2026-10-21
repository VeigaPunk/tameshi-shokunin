# FRoute04 — Route04 falsification (2026-10-21)

Axes: current-revision correctness; historical-byte preservation; attribution and reproducibility.

## Finding — Medium

**Strongest assertion attacked:** Route04’s P4 caught all 15 mutants and therefore R18-4 needed no further correction text. **Disagree as support for delivered revision `55e1d31`;** the report’s result is explicitly about `21e7932`, not the current ruler. This does not dispute that its observations describe the older snapshot.

**Evidence / reproduced arithmetic (read-only):**
- Route04 records baseline `7243e7f` and delivery `21e7932` (Route04.md:11–15, 103–132). The committed `before.json` says `corrected=0, open=5, total=5`; `after-21e7932.json` says `5, 0, 5`. Both use ruler SHA `c538c33d…` and those are the complete 5-item arithmetic.
- At `55e1d312c4e8ac67aefad80099bd27581ff805c`, `measure.py` SHA is `bb651eefdbe0f85b2d01408ec61e9accebeca8041c20b70982ae698634ff5053`, not `c538…`. No same-ruler `55e1` before/after output is present in the round-19 evidence directory; the two counts above cannot establish current 5/5.
- Attribution is consistent in the inspected Git objects: baseline `checks.json` row is argv `…study.py --selftest`, revision `921ef807…`, exit 64, empty-stdout digest; the active registry row at `921ef807…` uses argv `…study.py selftest` and expects 0. The replacement receipt at `55e1` records that canonical argv, revision `4b7c682…`, exit 0, and stdout SHA `316b9713…`. Its tool and runner hashes match the respective blobs at both `921ef` and `4b7c`; replay stdout and the baseline tally have the same SHA. Baseline and `55e1` `checks.json` are in fact byte-identical (`fed3c8e6…`).

**Concrete current-rule falsifier (static inference, not executed):** `measure.py:183–199` checks only the old row’s `exit == 64` and empty `stdout_sha256`; it does not pin the row’s argv/revision or `checks.json` bytes. Change either historical row field in a `--snapshot` input while retaining those two values and leaving other inputs unchanged: `witness()` still passes R18-4 although the historical-byte invariant in `contract.json:13` is violated. This is a missed correction to the old P4 H1 weakness; the real delivered bytes are intact, but this ruler does not enforce that fact.

The actual lesson erratum (`corpus/lessons/round-18.md:135–146`) already identifies the failed row, replacement path, canonical argv, exit and replay revision; Route04’s optional prose addendum is not needed for those facts.

## Residual risk / verification gaps

- Current C1 before/after arithmetic and public selftest remain unverified here: no `55e1`-ruler result was present. No selftest, build, or mutation probe was run.
- Receipt execution provenance remains unknown: the complete receipt says `cwd_kind: isolated scratch clone`; the available receipt does not establish how the successful scratch was materialized. The matching hashes corroborate attribution, not execution.

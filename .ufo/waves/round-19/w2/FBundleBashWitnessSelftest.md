# BundleBashWitnessSelftest — FALSIFY

Date: 2026-10-21. Read-only review; no receipt, suite, or selftest was executed.

## Strongest material assertion and verdict

**AGREE, with a stale example corrected in 55e1d31:** the delivered ruler still has a preserved-history failure-capability gap, but it catches the report's specific three-field laundering mutation now.

- JSON arithmetic: `before.json` has 0 corrected + 5 open = 5, revision `7243e7f163f08978c8fd9b6c1ef67a2fefe7d190`; `after-21e7932.json` has 5 corrected + 0 open = 5, revision `21e79329f8bdcf01a62be63b3e46db4a7de6b6f9`. Both pin ruler SHA-256 `c538c33d…`. These prove 0/5 → 5/5 only under the old ruler.
- At delivered `55e1d312c4e8ac67aefad80099bd27581ff805c9`, `measure.py` SHA-256 is `bb651eefdbe0f85b2d01408ec61e9accebeca8041c20b70982ae698634ff5053` (Git blob `d13dc4…`, matching the pinned revision). Its `PATHS` (`measure.py:46-51`) omits A's stderr and all three files for failed receipt C. `witness()` (`:183-199`) validates D's exact receipt, then checks A only for exit 64 and empty-stdout digest; it does not compare A's argv or revision.
- Thus the report's proposed A mutation changing argv to `selftest`, exit to 0, and digest to D's output is **stale against 55e**: the new exit/digest conditions reject it. The delivered ruler also adds exact D argv/revision/exit/stream-digest checks, pinned tool/runner hashes, tally equality, and typed two-item `supersedes`.
- Factual attribution is supported: the old row (`round-18/final/checks.json:45-54`) records `--selftest`, revision `921ef8077440f90d092aab4b9fdc750a45de1224`, exit 64, and SHA-256(empty) for stdout. Its stderr says the required mode is missing (`.../bash-witness-selftest.stderr:3`). The source at 921ef80, 4b7c682, and 55e1d31 is the same blob (`bac63301…`); it declares `add_subparsers(dest="mode", required=True)` (`tools/bash-witness-study.py:1701`, opened 2026-10-21). D instead records the valid `selftest` argv at 4b7c682. Tool and runner SHA-256s match at 921ef80 and 4b7c682.

## Concrete falsifier

[INF from delivered source, not executed] Change only A's `argv` to `['python3','tools/bash-witness-study.py','selftest']`, leaving its recorded exit 64 and empty-stdout digest intact. `evaluate().witness()` still accepts R18-4: it never checks A's argv; the selftest's `wrong-argv` mutant changes D, not A. Deleting A's stderr or C likewise has no effect because those files are not in `PATHS`.

## Residual unknowns

No before/after measurement receipt using the delivered `bb651e…` ruler was present in the scoped evidence listing. Do not promote the old ruler's 5/5 to a new-ruler result. This is a remaining failure-capability gap only; it does not itself assert arbitrary historical authenticity or change C1's stated scope.
seat: ExecRows02

# Round-45 w1 C1 re-verification: S004, S005, S006 (author)

All three rows fetched live on 2026-10-25, extracted via the round-45 freshness
`measure.py --extract`, quote located afresh in the normalized text (never copied
from row cells), and graded with the counter's `--check` helper against the frozen
rev `3310e7be803516ca5934b4e949d91bcec824b179`. Verdicts: holds / holds / holds.

No tool installs/updates performed (curl, python3, git, pdftotext already present).

## S004 — https://mutants.rs/using-results.html
- curl: exit 0, 29579 bytes, sha256 `5ec9ba952d4d2c12fc2e775965b4138cfdb5dc13b7cff392344383093f012334`
- CHECK: `CHECK S004 verified ok` (exit 0)
- note: Live page still has the 'Tests fail in an clean tree?' and 'Mutant outcomes'
  sections verbatim in substance: the copied-tree first-pass requirement and
  unviable-as-inconclusive semantics both hold; the in-diff.html/iterate.html
  caution pages also still carry their Caution sections.
```json
{"id":"S004","url":"https://mutants.rs/using-results.html","opened":"2026-10-25","verdict":"holds","raw_sha256":"5ec9ba952d4d2c12fc2e775965b4138cfdb5dc13b7cff392344383093f012334","quote":"Fix this first: cargo-mutants can't do anything until you have a tree where cargo test passes reliably when copied to a temporary directory.","snapshot":".ufo/evidence/round-45/freshness/sources/S004.raw.gz","author":"ExecRows02","note":"Live page still has the 'Tests fail in an clean tree?' and 'Mutant outcomes' sections verbatim in substance: the copied-tree first-pass requirement and unviable-as-inconclusive semantics both hold; the in-diff.html/iterate.html caution pages also still carry their Caution sections."}
```

## S005 — https://raw.githubusercontent.com/boxed/mutmut/main/HISTORY.rst
- curl: exit 0, 19417 bytes, sha256 `e9cace4dc9d4e2b438ad26782b50e8bd5fa17f838706a28699eee06a459e7ae3`
- CHECK: `CHECK S005 verified ok` (exit 0)
- note: 3.8.0 section still fixes CPU-time-limited mutants misreported as killed
  (#565) and patch.dict(os.environ, clear=True) false survivors (#511/#552);
  3.7.0 section still has per-function source hashing for cache invalidation.
```json
{"id":"S005","url":"https://raw.githubusercontent.com/boxed/mutmut/main/HISTORY.rst","opened":"2026-10-25","verdict":"holds","raw_sha256":"e9cace4dc9d4e2b438ad26782b50e8bd5fa17f838706a28699eee06a459e7ae3","quote":"Fix mutants stopped by the CPU-time limit being reported as killed instead of timed out","snapshot":".ufo/evidence/round-45/freshness/sources/S005.raw.gz","author":"ExecRows02","note":"3.8.0 section still fixes CPU-time-limited mutants misreported as killed (#565) and patch.dict(os.environ, clear=True) false survivors (#511/#552); 3.7.0 section still has per-function source hashing for cache invalidation."}
```

## S006 — https://github.com/BWBama85/shmutant
- curl: exit 0, 323925 bytes, sha256 `a61a08aa40750e29393df2c2983c2fcce216a2742352d37cf5ef6e9cb03e2263`
- CHECK: `CHECK S006 verified ok` (exit 0)
- note: README still carries 'The three verdicts' table (killed/survived/accidental/
  unapplied/baseline) and the refusal of a matched literal whose rewrite is ambiguous,
  grounding the verdict-semantics teaches.
```json
{"id":"S006","url":"https://github.com/BWBama85/shmutant","opened":"2026-10-25","verdict":"holds","raw_sha256":"a61a08aa40750e29393df2c2983c2fcce216a2742352d37cf5ef6e9cb03e2263","quote":"unapplied The old literal matched nothing. The row injected no defect and tests nothing . baseline The selected tests were not green","snapshot":".ufo/evidence/round-45/freshness/sources/S006.raw.gz","author":"ExecRows02","note":"README still carries 'The three verdicts' table (killed/survived/accidental/unapplied/baseline) and the refusal of a matched literal whose rewrite is ambiguous, grounding the verdict-semantics teaches."}
```

## Evidence files (kept for L1 integration)
- /tmp/tameshi-r45-ExecRows02/S004.raw, S005.raw, S006.raw (fetched live bytes)
- /tmp/tameshi-r45-ExecRows02/S004.norm.txt, S005.norm.txt, S006.norm.txt (extract outputs)
- /tmp/tameshi-r45-ExecRows02/S004.json, S005.json, S006.json (fragments)

## Risks / notes
- S004: the teaches' `--in-diff`/`--iterate` caution claim lives on the companion
  pages (in-diff.html, iterate.html), which the source cell names explicitly; both
  still carry `Caution` sections live. The two anchored sections on using-results.html
  are present.
- S006: the README now reports 245 commits (was 239 at open); that is an open-time
  fact, not part of the anchored verdict-semantics claim, so no drift.

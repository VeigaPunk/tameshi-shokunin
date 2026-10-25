# CriticS108Use — C1 must not cite S108; C2 is the pin itself

**Verdict: CONFIRMED (no violation, no counterexample stands).** The round-40 C1
capability claim carries no S108 dependency at any layer — contract, counter,
fixtures, tool, or knowledge entry. The new entry `corpus/knowledge/
r40-write-form-misses.md` cites S152 only and names S108 solely in an explicit
disclaimer. C2 is the sole consumer of the S108 snapshot.

## Evidence (frozen rev `5641ed84c8dc148c34c8dd83f062279ddf06b4af`)

1. **Contract.** `.ufo/evidence/round-40/contract.json:20-29` — the C1 block has
   no `sources` field and no `s108` string; its predicate names only the v2/v1
   tool shas, planted fixtures, and two live files. Contrast round-39
   (`evidence/round-39/contract.json:31`) where C1 explicitly declared
   `"sources": "S107 and S108…"` — round-40 dropped the field entirely. Only C2
   (`contract.json:30-41`) carries `s108/golden_tests.zh-cn.html`,
   `snapshot_sha256 f27cf274…`, and the zh-cn quote — the pin itself.

2. **Counter.** Full 253-line read of `.ufo/evidence/round-40/census/measure.py`:
   paths touched are `tools/write-path-census-v2.py`, `tools/write-path-census.py`,
   `.ufo/evidence/round-40/census/fixtures.json`, `contract.json`, plus live sites
   `tools/registry-replay.py` and `tools/bash-witness-study.py` (lines 25-28,
   185-186). Zero references to `s108`, `golden_tests`, `zh-cn`, `tensorflow`.
   Deleting `.ufo/evidence/round-40/s108/` would leave C1's predicate fully
   evaluable — the claims are independent.

3. **Fixtures.** `census/fixtures.json` — five synthetic snippets; the flag-guard
   token is bare `--update_goldens` (fixtures.json:3,5), not the S108-quoted
   `--test_arg=--update_goldens` form. Thematic overlap only: the flag convention
   predates S108 (round-39 v1 counter `V1_FLAG_RE`, measure.py:42).

4. **Tool.** `git show 5641ed84…:tools/write-path-census-v2.py | grep -niE
   's108|golden_tests|zh-cn|tensorflow'` → exit 1, no match.

5. **New entry.** `corpus/knowledge/r40-write-form-misses.md` (added at the
   freeze): line 1 header `source: S152 — https://repositorio.ufmg.br/…` is the
   only support citation. The file's sole `S108` token is line 14: "The citation
   is that sentence, not a count of the lane's gates. **S108 is not support for
   this entry.**" — an explicit exclusion, not support. Independently confirmed
   by `ReviewS108NotSupport.md` (content-leakage scan: no S108-derived claim).

6. **Registry.** `git diff 304e335…5641ed8 -- corpus/SOURCES.md`: the only `+`
   rows are S132 (`:121`) and S152 (`:122`); the S108 row (`:120`) is unchanged
   round-39 context. S152's used-by names `r40-write-form-misses.md`; S108's
   used-by remains only `corpus/knowledge/r8-golden-update-flag.md`.

## Residual note (calibration, not a defect)

The fixtures reuse `--update_goldens` — the flag S108's quote documents. That is
thematic, not evidential: the discriminating fixtures would be byte-identical had
S108 never been fetched (S107's committed round-39 snapshot already grounds the
convention), and the line-14 disclaimer forecloses the inference. If a future
round wants belt-and-braces, fixtures could rename the flag; nothing requires it.

No edits to the lane checkout; no counter run in default mode. Commands used:
`git diff/show` at the two frozen revs, `grep` over lane/corpus/round-40 trees.

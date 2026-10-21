# CorpusReadme — round24 `corpus/README.md` index row (critic, w1)

Target: `corpus/README.md:371-377` at c8c5b88c8e961a929cdc351b95a7074c76958909
(only README change in 6a1821a..c8c5b88 is d2eaecd; README sha256 at d2eaecd = bd38c02 = c8c5b88 =
`faaa6726…5d24`, matching the round24 appended cold-read ledger pins).

## Verdict

**Two fixable defects in the row; no blocking tradeoff.** Most claims hold. One evidence path does
not resolve, and the Ground cell claims more coverage than the predicates provide.

- D1 (evidence path, fixable): `.ufo/evidence/round-24/{contract,measure}.py/json` does not resolve
  to the committed files.
- D2 (ground overclaim, fixable): "routed round23 hardening gaps as falsifiable predicates" reads as
  all routed gaps. Only 5 of the 8 `routed_not_executed` entries map wholly to K-predicates.
- N1 (nit, inherited): `minedS084` glued token (same as round22/23 rows).

## Claim-by-claim evidence (all at c8c5b88, read-only `GIT_OPTIONAL_LOCKS=0 git show/cat-file/ls-tree`)

| # | Row claim | Result | Evidence |
|---|---|---|---|
| 1 | Entry `knowledge/replay-projection-hardening.md` | HOLDS | `git ls-tree` → blob `b977c57d…`; resolves relative to `corpus/` like prior rows |
| 2 | Ground "same-ground calibration" | HOLDS | `contract.json` claim "C1 calibration … not a score uplift"; SCORECARD round24 "Numeric expertise stays 8 (delta 0)" |
| 3 | Ground "routed round23 hardening gaps as falsifiable predicates" | PARTIAL (D2) | see D2 |
| 4 | Evidence "mined S084, S085" | HOLDS | `corpus/SOURCES.md` S084 (Python `os.path.realpath`, tier A, `mined`, used-by includes the note) and S085 (`fresh-adjudication.json` lines 53–104 @6a1821a, `mined`); the note's `source:` line cites both |
| 5 | Evidence `tools/registry-replay.py` | HOLDS | blob `30feb147…`, mode 100755 (path is repo-root relative, same inherited convention as round22/23 `tools/…`) |
| 6 | Evidence `.ufo/evidence/round-24/{contract,measure}.py/json` | FAILS literally (D1) | `git cat-file -e`: `contract.json` present, `measure.py` present, `contract.py` ABSENT, `measure.json` ABSENT |
| 7 | "No F1–F10 status changes" | HOLDS | `git diff 6a1821a c8c5b88 -- SCORECARD.md SKILL.md corpus/QUALITY.md` is append-only (round24 section, QUALITY48, SKILL round24 addition); no frontier row edited |
| 8 | "No … independent cold-read … credit" | HOLDS | the only cold-read touch is c8c5b88 appending 15 entries to `.ufo/evidence/round-21/coldread/ledger.json`. Each entry has provenance "actual L1-author byte-consuming source reads; not recipe execution, independent/blind cold-read or required-command coverage" |
| 9 | "No … promotion credit" | HOLDS | contract bounds "no promotion"; lesson Gate rejects producer authentication; SCORECARD awards nothing numeric |

## D1 — evidence path does not resolve

Counterexample: read literally, the brace pattern is the shell expansion
`.ufo/evidence/round-24/contract.py/json` and `…/measure.py/json`. Neither path exists. The
Cartesian reading names `contract.py` and `measure.json`, and both are ABSENT. `measure.py` prints
its JSON to stdout (`measure.py:213`); no `measure.json` is committed, and there is no `after.json`
either. A reader or link checker following the row gets nothing back. The intended pair is
`contract.json` and `measure.py`; `before.json`, the only frozen receipt, is not cited.

Impacted axes: calibration (claim → evidence traceability), maintainability.

## D2 — the Ground cell overclaims routed-gap coverage

Source: `.ufo/waves/round-23/fresh-adjudication.json` @6a1821a `routed_not_executed` (lines ~53–104).
It has 8 entries. Mapping to contract K1–K11:

| Routed entry | Predicate | Status |
|---|---|---|
| name-insensitive argv | K1 (+K2 casefold) | covered |
| negative-exit guard | K3 | covered |
| unpinned `bundle_sha256` on two rows | K5, K6 | covered |
| projection drops held/cleanup_ok/external/non_hermetic_argv | K7, K8, K10 | covered |
| sibling identity by string / fleet root not realpath | K11 | covered |
| runner_sha256 hashes live-tree copy | none | fixed in code (`registry-replay.py:162-163` hashes `clone / 'tools/registry-check.py'`), but the note says "recorded per run, not a ruler predicate" (`replay-projection-hardening.md:21`) |
| streams unbounded **and unredacted** | K9 (size only) | redaction is not addressed anywhere: `git grep -i redact c8c5b88 -- tools corpus SKILL.md SCORECARD.md .ufo/evidence/round-24` matches only unrelated SOURCES S014 |
| preexisting loose stdout tokens | none | intentionally kept (no-retrofill rule) |

K4 (any-token) is a base-killed control from the closure probe, not a routed entry.

Counterexample: under the README wording, a reader would conclude that runner-digest provenance and
stream redaction are now falsifiable predicates. Neither is: the ruler would read 11/11 even if line
163 reverted to the live tree or if secrets were retained. The knowledge note is honest about the
runner digest (line 21) but says nothing on redaction or the loose tokens. Only the README index
generalises. QUALITY48 itself makes predicates the bar for counting a routed gap as repaired, so the
row contradicts its own round's criterion.

Impacted axes: calibration (scope honesty), and SCORECARD/lesson consistency (premature saturation risk).

## N1 — glued token

`minedS084` (`README.md:375`) follows the round22/23 typo (`:352` `minedS082`, `:363` `minedS083`).
The older convention at `:185` is "mined S003/S048". A grep for `mined S084` misses the row. This
is cosmetic and changes no claim.

## Adjacent observation (outside the row, not a row defect)

The lesson (`lessons/round-24.md:53`) says "The after measurement is recorded below once executed",
and SCORECARD says "Measured results are recorded below only after execution". At c8c5b88 neither
file contains an after result, and there is no `after.json`. The README row makes no after or 11/11
claim, so it stays consistent. The table "Fails when" column names failure conditions; it does not
assert they were demonstrated.

## Smallest safe correction (for the L1 integrator; not applied)

Replace `README.md:375` cells with:

```
| `knowledge/replay-projection-hardening.md` | same-ground calibration; eleven frozen predicates for the routed round23 argv, exit, digest-pin, projection, stream-size and realpath gaps (runner-copy hash recorded, not a predicate; stream redaction and frozen loose tokens not addressed) | mined S084, S085; `tools/registry-replay.py`; `.ufo/evidence/round-24/contract.json`, `measure.py`, `before.json` |
```

No other line needs a change; claims 1, 2, 4, 5 and 7–9 hold as written.

## Scope / tooling

Read-only inspection only. No commands were run in the lane tree beyond `git show/diff/log/ls-tree/cat-file/grep/rev-parse`
with `GIT_OPTIONAL_LOCKS=0`. No selftests, gates or ruler runs. No tools installed or updated. Only
this report file was written.

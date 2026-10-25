# CriticSeparable — round-40 separability review

## Finding: claims ARE separable. No counterexample found.

**C1 verifies without the S108 snapshot.** `census/measure.py` reads only
`tools/write-path-census-v2.py` (line 25/120), `tools/write-path-census.py`
(26/139), `census/fixtures.json` (27/141), `tools/registry-replay.py` (189),
`tools/bash-witness-study.py` (190), and `contract.json` `claims.C1.tool_sha256`
(131–135). `grep 's108|golden_tests|snapshot_path'` over the file: **no matches**.

**C2 verifies without the v2 tool.** `s108/measure.py` reads only
`.ufo/evidence/round-40/s108/golden_tests.zh-cn.html` (line 21/55) and
`contract.json` `claims.C2` (56–63). `grep 'census|write-path|tools/'`:
**no matches**. Its self-containment check (`stripped_quote_fails`, 77–79)
mutates only the snapshot blob in memory.

## Evidence

| Probe | Command | Result |
|---|---|---|
| C1→s108 refs | `grep s108\|golden_tests .ufo/evidence/round-40/census/measure.py` | 0 matches |
| C2→v2 refs | `grep census\|write-path\|tools/ .ufo/evidence/round-40/s108/measure.py` | 0 matches |
| v2 pin | `git show HEAD:tools/write-path-census-v2.py \| sha256sum` | `4022…878b` = contract pin |
| v1 pin | `git show HEAD:tools/write-path-census.py \| sha256sum` | `bc8c…dc62` = contract pin |
| s108 pin | `git show HEAD:.ufo/evidence/round-40/s108/golden_tests.zh-cn.html \| sha256sum` | `f27c…2bf0` = contract pin |
| base do-nothing | `git show 304e335…:tools/write-path-census-v2.py` | absent → `tool_absent=1` → C1=false |
| base do-nothing | `git show 304e335…:.ufo/evidence/round-40/s108/golden_tests.zh-cn.html` | absent → `snapshot_absent=1` → C2=false |
| C1 live evidence | `tools/registry-replay.py:123` `(out / 'expected.json').write_bytes(…)`; `tools/bash-witness-study.py:778` `os.replace(tmp, path)` | v2 patterns hit; v1 patterns miss |

## Sole shared input (not a defect)

Both counters `git_show` `contract.json` at REV (census/measure.py:131,
s108/measure.py:56), but consume disjoint keys — `claims.C1.tool_sha256` vs
`claims.C2.{snapshot_sha256,quote}`. Deleting C2's claim object cannot fail C1
and vice versa. The frozen contract is the canonical assignment source, so this
is intended plumbing, not claim coupling.

## Smallest safe correction

None required. Verification decomposes: C1's PASS depends on six paths, none
under `s108/`; C2's PASS depends on one blob plus its own claim keys, none under
`tools/`. Removing either artifact leaves the other claim's verdict unchanged.

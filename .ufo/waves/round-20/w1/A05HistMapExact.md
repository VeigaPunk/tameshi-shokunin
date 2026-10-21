# A05HistMapExact — round-20 contract.json historical map audit

Seat: `TameshiR20-3.A05HistMapExact` · 2026-10-21 · read-only audit, no lane writes except this trailer.

## Axes (godspeed)

fidelity (exact sha+label match vs frozen four) · completeness (no extra/missing keys) · uniqueness (no duplicate label, no duplicate raw JSON key) · collision-freedom (no historical sha equals a current instrument sha) · provenance (audited bytes == frozen-commit bytes).

## Target

`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-20/contract.json`, top-level key `"historical"` (lines 38–43), a flat map of `"<sha256>": "<label>"`.

## Findings — verdict PASS (empty diff vs frozen four)

| check | observed | result |
|---|---|---|
| entry count | exactly 4 | PASS |
| keys vs frozen set | set-equal; `map == frozen` is `True` (exact sha+label, no rename) | PASS |
| key format | all 4 keys are 64-char lowercase hex | PASS |
| labels | `round19-ruler-wave1`, `witness-tool`, `witness-runner`, `round18-measure` — all plain strings, all distinct (`duplicate_labels: []`) | PASS |
| duplicate raw JSON keys (parser-collapsing hazard) | none anywhere in the file (`object_pairs_hook` scan) | PASS |
| extra/missing keys | none — map equals the frozen four exactly | PASS |
| collision with current instruments | intersection of historical shas with {`f03ae7e91…`, `f34dc233…`} (contract frozen + installed declarations + on-disk staged bytes) = ∅ | PASS |
| corroboration | `git show 6fd220bce3705498d1d1054e99e3cae73c203751:.ufo/evidence/round-20/contract.json` sha256 `9b2813342768fdaa51bfd670a19d8573f87169a59b98207200e622f8e2b62715` == working-tree file sha256 → audited bytes are the frozen-commit bytes, untampered | PASS |

### Diff against the four frozen historical shas/labels

**Empty diff.** All four frozen entries present verbatim, in file order:

| sha256 | contract label | frozen label | status |
|---|---|---|---|
| `96a68b60538504a8a1b5ead9d5811a2c7bcbf8b427c5934b07e22e16c38585ef` | `round19-ruler-wave1` | `round19-ruler-wave1` | exact |
| `8dfaa25aa2713635e7363f60effb442a474ba3656d6cf2bb171c0c22432e3a12` | `witness-tool` | `witness-tool` | exact |
| `d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b` | `witness-runner` | `witness-runner` | exact |
| `7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37` | `round18-measure` | `round18-measure` | exact |

No fifth entry, no missing entry, no sha/label transposition, no duplicate label. The four historical shas are mutually distinct (implied by 4 distinct keys set-equal to the 4-element frozen set).

## Commands and observed outputs

1. `sha256sum .ufo/evidence/round-20/stage/receipt-window.py .ufo/evidence/round-20/stage/measure.py` (cwd = lane):
   ```
   f03ae7e91607750e2690f7819c486a3d9db03ee13f0b8cf51958462834dcf7cc  .ufo/evidence/round-20/stage/receipt-window.py
   f34dc233eee33f4fea9a82c391bfb57ebfef8983f5c7146b4d2dc0b6b3be4e2d  .ufo/evidence/round-20/stage/measure.py
   ```
   Both equal their contract `frozen_sha256` (staged bytes frozen; also no collision with any historical sha).
2. `test -f tools/receipt-window.py && … || echo ABSENT` → `tools/receipt-window.py: ABSENT` — install has not happened yet (expected: contract schedules install after every wave reader returns), so no on-disk installed-instrument sha exists to collide.
3. `git show 6fd220b…:…/contract.json | sha256sum` vs `sha256sum .ufo/evidence/round-20/contract.json` → both `9b2813342768fdaa51bfd670a19d8573f87169a59b98207200e622f8e2b62715` (read-only git access only; no refs/index/state touched).
4. Python structural audit (read-only parse in-kernel, no lane writes): `entry_count=4`, `keys_exact_match=true`, `map_equals_frozen_exactly=true`, `all_keys_64_lowercase_hex=true`, `duplicate_labels=[]`, `duplicate_json_keys_anywhere_in_file=[]`, `collisions_hist_vs_current={}`, `verdict=PASS`.

## Agree/disagree / defects

- Agree with the frozen-facts statement: the historical map carries exactly the four named instrument shas with exactly the named labels — the rider's "name each historical instrument sha" requirement is already satisfied per-entry; no singular "frozen SHA" wording remains in the map.
- No defects found in scope. Out-of-scope observations, for other seats only: `expectations` says `"open": 0` while context says the 18 round-18 guard survivors remain OPEN — that field plausibly refers to this round's 6 population items, not the guards; not a historical-map defect, flagging in case C-seats want to confirm wording.

No installs performed; no production, tools/, corpus/, or sibling files touched; no git/jj mutation; no code executed against the lane beyond read-only hashing/parsing.

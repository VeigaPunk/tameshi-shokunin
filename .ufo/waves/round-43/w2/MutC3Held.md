# MutC3Held — held-moved refusal deleted (C3, operability)

Wave 2 falsifier. Base `487b8f0`, freeze of record `3aee2c078f8976499b587086af3577fc94dc8cf1`.
No counter was run at `c5335c7`. Scratch: `/tmp/tameshi-r43-w2-MutC3Held-` (deleted before return).
Lane checkout was read-only throughout; the only lane write is this file.

## Mutant

Target: C3's sentence "refuses a map that moves a held document off its registry id"
(`contract.json` claims.C3.statement) and guard docstring `tools/staged-id-guard.py:33-36`.

Smallest behaviour-bearing point: `tools/staged-id-guard.py:249-252`, the only producer of that
refusal in `validate_map`:

```python
    for sid, registry_id in base['held'].items():
        if sid in mapping and mapping[sid] != registry_id:
            reasons.append('map moves a held document off its registry id: %s -> %s '
                           '(registry %s)' % (sid, mapping[sid], registry_id))
```

Deleted verbatim; nothing else changed (`map_held_moved` at :262 and the selftest at :356-358
left intact, so the mutation is of behaviour only, not of the evidence field).

| bytes | sha256 |
|---|---|
| pristine (freeze) | `2e8f2e891ea20417c141e16871819182d5040c6f33916a435e9454a94d4d6ff2` |
| mutant (before restore) | `52375d7466094b5fa72e81c41de034bc00bedbe53f256606ebe0651b571e2ee9` |

Reproduce:

```
S=/tmp/tameshi-r43-w2-MutC3Held-
git clone --shared -q /home/vgpnk/Projects/shokunin/tameshi-shokunin "$S/clone"
git -C "$S/clone" show 3aee2c0:tools/staged-id-guard.py > "$S/tool/pristine-staged-id-guard.py"
cp "$S/tool/pristine-staged-id-guard.py" "$S/tool/mut-staged-id-guard.py"
# delete tools/staged-id-guard.py:249-252 from the copy, then:
```

## Detector that fires first

**`--selftest`, case `T7_held_row_must_dedupe` (`tools/staged-id-guard.py:356-358`).** It is the
first gate in the counter's order: the selftest subprocess runs at
`.ufo/evidence/round-43/guard/measure.py:196-199`, before the first `run_guard` call at :204.
The live guard path never gets to disagree.

```
$ python3 -I "$S/tool/mut-staged-id-guard.py" --selftest
STAGED_ID_GUARD_SELFTEST: cases=24 failed=1
FAIL T7_held_row_must_dedupe reasons=[]
VERDICT: FAIL
exit=1

$ python3 -I "$S/tool/pristine-staged-id-guard.py" --selftest     # baseline
STAGED_ID_GUARD_SELFTEST: cases=24 failed=0
VERDICT: PASS
exit=0
```

The note is `reasons=[]` because the mutant admits the map, so the case's first conjunct
(`not ok8`) fails while its second (`fields8['map_held_moved'] == ['S002']`) still holds — the
evidence field survives the refusal, which is why the case is written on both.

## C3 counter, mutated tool

```
$ cd "$S/clone"
$ python3 .ufo/evidence/round-43/guard/measure.py --lane "$S/clone" \
    --rev 3aee2c078f8976499b587086af3577fc94dc8cf1 \
    --freeze 3aee2c078f8976499b587086af3577fc94dc8cf1 \
    --tool-file "$S/tool/mut-staged-id-guard.py"
C3_R43: self_pin=1 tool_absent=0 tool_sha_ok=1 selftest_exit=1 selftest_cases=24
selftest_failed=1 staged_rows=103 live_collisions=7 live_collisions_agree=1 live_held=3
live_held_agree=1 live_unmapped=0 live_cascade=1 live_verdict=refused naive_map_refused=1
safe_map_admitted=1 map_dedupe_live=1 safe_floor=S256
staged_sha256=020fbeaa048fc6727e08c0e91e242cd8b1b15ea9dc8853837c4548b1cf394807
naive_agree=1 substitute=1 rev=3aee2c0… freeze=3aee2c0… C3_R43_PASS=false
exit=1
```

Baseline, same rev/freeze, no `--tool-file`:

```
C3_R43: self_pin=1 tool_absent=0 tool_sha_ok=1 selftest_exit=0 selftest_cases=24
selftest_failed=0 staged_rows=103 live_collisions=7 live_collisions_agree=1 live_held=3
live_held_agree=1 live_unmapped=0 live_cascade=1 live_verdict=refused naive_map_refused=1
safe_map_admitted=1 map_dedupe_live=1 safe_floor=S256
staged_sha256=020fbeaa048fc6727e08c0e91e242cd8b1b15ea9dc8853837c4548b1cf394807
naive_agree=1 substitute=0 rev=3aee2c0… freeze=3aee2c0… C3_R43_PASS=true
exit=0
```

`substitute=1` keeps `C3_R43_PASS=false` (`measure.py:279`), as A9 requires. Every measurement
field except `selftest_exit`/`selftest_failed`/`substitute` is byte-identical to the baseline.

## Verdict: killed (by the selftest), with a coverage gap on the live path

Killed — but by exactly one detector. The counter's live corpus **cannot** distinguish the
mutant:

- `measure.py:247-252` builds `safe_map = dict(own_held)` and only assigns fresh floor ids to
  non-held collisions, so the admitted map it exercises never moves a held row; `map_dedupe_live`
  (:259) therefore only ever tests the dedupe branch.
- `live_held=3` (S153→S105, S154→S106, S159→S155 on the staged package) is real held data, but
  the counter only feeds it into the dedupe direction.

Direct probe with a held-move map (`S153→S270`, floor `S256`), same live registry/staged bytes:

```
pristine: exit=1 verdict=inadmissible map_ok=false
          map_reasons=["map moves a held document off its registry id: S153 -> S270 (registry S105)"]
          map_held_moved=["S153"]
mutant:   exit=0 verdict=admitted    map_ok=true  map_reasons=[]
          map_held_moved=["S153"]        # field still populated, verdict contradicts it
```

So the mutant ships an admission of exactly the append the claim forbids, and its JSON is
self-contradictory (`map_held_moved` non-empty with `map_ok: true`); no counter check compares
`map_held_moved` against `map_ok`.

Supplementary double mutant (refusal **and** `T7_held_row_must_dedupe` deleted, sha
`6ea70c6f4eb1f69fcf8b559d5eb647b372ab218977003a1eb3cb50f2c7c247cf`):

```
--selftest → cases=23 failed=0 VERDICT: PASS (exit 0)
counter --tool-file mut2 → selftest_exit=0 selftest_cases=23 selftest_failed=0 …
  safe_map_admitted=1 map_dedupe_live=1 … substitute=1 C3_R43_PASS=false
```

Every live field green, `cases=23` still clears `MIN_CASES=13`. The only thing standing between
this tool and `C3_R43_PASS=true` is the A9 substitute gate (`substitute == 0`, `measure.py:279`)
plus the byte pin (`tool_sha_ok`, which reads the REV bytes, not the substituted file). Neither
is behavioural coverage: they prove *which bytes* ran, not that the capability is present.
If the mutation had been delivered by a rewrite of the pinned file (a new freeze with the
refusal absent and the case dropped), C3 would read green.

This is a coverage finding, not a contract change request: C3's predicate, classes and target
stand; the gap is that the "held row must dedupe" behaviour has one selftest case and no live
counter case, and the live held data (3 rows) is only ever exercised in the dedupe direction.

## Restoration

- The lane's `tools/staged-id-guard.py` was never written: sha256
  `2e8f2e891ea20417c141e16871819182d5040c6f33916a435e9454a94d4d6ff2` before and after, equal to
  `git show 3aee2c0:tools/staged-id-guard.py` and to `contract.json` frozen_tools pin.
- Both scratch copies were restored to the pristine bytes (`2e8f2e89…`) after evidence capture,
  and `/tmp/tameshi-r43-w2-MutC3Held-` was deleted (scratch declared disposable).
- No campaign tool, no `git add/commit/stash/checkout/reset/pull/push`, no mutating `jj` call, no
  pacman/uv/npx install (python3 stdlib only), nothing written to
  `/home/vgpnk/Projects/shokuknow`.

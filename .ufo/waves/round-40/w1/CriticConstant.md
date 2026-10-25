# CriticConstant — round 40, always-1 classifier attack

## Attack
Constant classifier: `classify_text(text) -> (1, 1)` for every input
(writes=1, unflagged=1 regardless of flags or scratch paths).

## Planted case that kills it
`bytes_flagged` in `.ufo/evidence/round-40/census/fixtures.json:3`:

```python
if '--update_goldens' in argv:
    (out / 'expected.json').write_bytes(b'x')
```

A real guard must suppress the count; the constant classifier returns
unflagged=1 where the frozen predicate requires 0. The same constant is
also killed by `replace_flagged` (fixtures.json:5) and `scratch_replace`
(fixtures.json:6) — `bytes_flagged` is the strongest counterexample
because a flag-gated production write is the exact class the census was
built to separate.

## Does the counter check that case? Yes — attack fails.
`.ufo/evidence/round-40/census/measure.py:210-219`:

```python
planted_ok = (
    got['bytes_unflagged'][1] == 1
    and got['replace_unflagged'][1] == 1
    and got['bytes_flagged'][1] == 0      # line 213 — kills always-1
    and got['replace_flagged'][1] == 0    # line 214 — kills always-1
    and got['scratch_replace'][1] == 0    # line 215 — kills always-1
    and fields.get('bytes_unflagged') == '1'
    and fields.get('replace_unflagged') == '1'
    and rc.returncode == 0
)
```

`got` comes from actually importing the rev's tool and calling
`mod.classify_text(planted[name])` (measure.py:158-159), not from
self-reported selftest fields — so a tool that lies in its `--selftest`
output but returns the constant tuple still fails.

Reproduction (scratch, no lane mutation):

```
python3 - <<'EOF'   # run anywhere; fixtures path absolute
import json
planted = json.load(open('/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-40/census/fixtures.json'))
got = {n: (1, 1) for n in planted}
assert not (got['bytes_unflagged'][1] == 1 and got['replace_unflagged'][1] == 1
            and got['bytes_flagged'][1] == 0 and got['replace_flagged'][1] == 0
            and got['scratch_replace'][1] == 0)
print('always-1 -> planted_ok=False')
EOF
```

Output: `bytes_flagged -> unflagged = 1 (required 0: KILLS)`, same for
`replace_flagged` and `scratch_replace`; `planted_ok=False`.

## Impacted axes
None — the frozen C1 predicate survives this attack. Depth claim is not
falsified by a constant/naive classifier; three independent planted
negative cases plus the v1-misses requirement (measure.py:220) and the
two mutants (measure.py:165-186, 228-229) hold.

Recorded corroboration: `after/c1-at-5641ed84.stdout` shows the pinned
tool emits `bytes_flagged=0 replace_flagged=0 scratch_replace=0` with
`C1_R40_PASS=true`; `before/c1-at-base.stdout` shows `C1_R40_PASS=false`
at base as required. Base contract requirements (C1/C2 both false at
304e3355) hold per `before/` transcripts.

## Smallest safe correction
None needed. Defect severity: zero — the counter is correctly calibrated
against a degenerate classifier. No predicate rewrite warranted.

No tools installed (none needed; scratch only).

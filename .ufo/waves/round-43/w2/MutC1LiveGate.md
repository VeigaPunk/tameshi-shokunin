# MutC1LiveGate — live-failure gate (round 43, wave 2)

## Question
Delete the `detail['live ...']` assignment the A9 amendment added, simulate a
live-only failure, and ask whether the mutant is then classified `killed` or
`equivalent`, and whether A9's line is the only thing preventing `equivalent`.
Name the exact line.

## Exact line
`.ufo/evidence/round-43/mutants/measure.py:377`

```python
            detail['live %s:%d' % (rel, lineno)] = False
```

inside `battery()`'s live-site loop (frozen counter, 639 lines, sha256
`0d0f81bdbe09bb53997ade30911fc178a38de072f84aacf23c6c9c0a710e57f1`, matching
`claims.C1.counter_sha256` at freeze `3aee2c0`). Provenance verified by walk:
`detail['live` is absent at 697d2f17/f0f26367/17f6ef0c/5cd2154f/114ffacd/53cb32b
and first appears at `273c047` ("freeze A9 — C1 live-reachability/probe gate").
Yes — this line was added by A9.

## Scratch and method
`git clone --shared` of the lane to `/tmp/tameshi-r43-w2-MutC1LiveGate-s1/repo`
(free, deleted before return). The frozen counter bytes were extracted once
(`git show 3aee2c0:...measure.py`, sha verified) and copies mutated; every run
used a permitted rev only: `--rev 3aee2c078f8976499b587086af3577fc94dc8cf1
--freeze 3aee2c078f8976499b587086af3577fc94dc8cf1` (plus one baseline at base
`487b8f0`). Mutated copies necessarily print `self_pin=0`; that field is
irrelevant to the classification readout. No lane file was touched.

Variants (one small edit each; generated mechanically, diffs checked):

| tag | edit |
|-----|------|
| `pristine` | frozen bytes, byte-identical |
| `a` | delete line 377 (the A9 assignment) |
| `l` | LIVE table rig: `tools/registry-replay.py:123` want `expected: True → False`, i.e. a site the *pristine* tool now fails |
| `al` | a + l |
| `s_<m>` | inject a 7th synthetic mutant `synthetic_liveonly_<m>` into the in-memory mutant list (find/replace applies exactly once to the tool) |
| `as_/ls_/als_<m>` | combinations |

Two genuinely live-only tool mutants were used, both verified by the counter's
own `fingerprint`/`check_site` helpers:

- `param_sites_ne1` — `_param_args`: `if not sites:` → `if len(sites) != 1:`.
  Requires a single in-module call site; `publish(...)` in
  `tools/registry-replay.py` has two (lines 185, 282). Zero fixture fingerprint
  change on all 12 fixtures; the pinned site `registry-replay.py:123` flips
  `explicit_out 1 → 0`. Plausible defect (refuse multi-caller resolution).
- `write_text_drop` — `_write_call`: `attr in ('write_text','write_bytes')` →
  `attr == 'write_bytes'`. Zero fixture fingerprint change; `registry-replay.py`
  record output changes (write_text writes dropped) **but outside the three
  pinned sites**, so no pinned live check flips.

## Results (all `C1_R43:` lines captured; exit codes shown)

| run | mutants_killed | dead_code_only | equivalent | live_ok | verdict on synthetic |
|-----|---|---|---|---|---|
| pristine (baseline, rev 3aee2c0) | 5 | 1 | 0 | 3/3 | `C1_R43_PASS=true`, exit 0 |
| pristine at **base** 487b8f0 | 5 | 1 | 0 | 3/3 | PASS=true, exit 0 |
| `a` (line 377 deleted, clean corpus) | 5 | 1 | 0 | 3/3 | verdicts identical to pristine |
| `l` (rigged LIVE, line intact) | **6** | 0 | 0 | 2/3 | `method_fold_several_returns` re-labelled **killed** |
| `al` (rigged LIVE + line deleted) | 5 | 1 | 0 | 2/3 | verdicts restored to baseline |
| `s_param_sites_ne1` (A9 present) | 6 | 1 | 0 | 3/3 | synthetic **killed** |
| `as_param_sites_ne1` (A9 deleted) | 5 | 1 | **1** | 3/3 | synthetic **equivalent** |
| `ls_param_sites_ne1` (rigged LIVE, A9 present) | **7** | 0 | 0 | 2/3 | synthetic killed, all 6 killed |
| `als_param_sites_ne1` (rigged LIVE + A9 deleted) | 5 | 1 | **1** | 2/3 | synthetic **equivalent** |
| `s_write_text_drop` (A9 present, clean) | 5 | 1 | **1** | 3/3 | write_text mutant **equivalent** |

`--probe-mutant` verdicts on `tool_param_sites_ne1.py`: pristine-line present →
`killed` (failures=1, reachable_failures=1); A9-deleted (`as_`/`als_`) →
`dead_code_only` (failures=1, reachable_failures=0). On `tool_write_text_drop.py`:
`survived`.

## Verdict on the item
1. **With the A9 line intact the live-only mutant is `killed`; with the line
   deleted it is `equivalent`** (`as_param_sites_ne1`: `equivalent=1`;
   `als_param_sites_ne1`: `equivalent=1`). The rigged LIVE table alone
   (`al`, `a`) does not produce `equivalent` for any of the six declared
   mutants — deleting the line does not weaken the verdicts when the corpus
   fixtures already detect every mutant. The equivalence appears only for a
   mutant whose sole divergence is a live-site failure, exactly the case the
   added comment claims to cover.
2. **Yes, line 377 is the only thing preventing `equivalent`.** With it
   deleted there is no second path: `battery()` adds live failures to `fails`
   but to nothing reachable, and the classification loop's fallback
   `differential(pristine, mutant, work)` (frozen lines 466-476) iterates
   `FIXTURES.items()` only — the declared corpus is fixtures-only — so a
   live-only fingerprint difference produces `differ == []` and the
   `equivalent` branch. Nothing else can promote it (`live_ok` only gates the
   run-level predicate, never the per-mutant verdict).
3. The item's prescribed simulation also isolates A9's collateral: with the
   LIVE table rigged to a site the pristine tool fails, A9's line re-labels the
   dead-code mutant `method_fold_several_returns` as `killed` (`l`: killed=6,
   dead_code_only=0), and deletes `dead_code_arg_ok`. The run-level gate
   (`live_ok=2/3`, `equivalent=0` required) still fails the run, so the
   counter refuses rather than mis-reports — but the per-mutant label is wrong.
4. Side finding: A9's reachability flag is not a complete live-coverage gate.
   `write_text_drop` diverges from the pristine tool's records on real
   `tools/*.py` code yet is `equivalent` **even under the pristine counter**
   (`s_write_text_drop`: `equivalent=1`, probe `survived`), because it flips no
   one of the three pinned sites. The live corpus only guards the three pinned
   sites; any live-only divergence outside them is invisible to the K/D/E/U
   rule either way.

## Reproduce
```bash
S=/tmp/tameshi-r43-w2-MutC1LiveGate-s1
# counter_*.py, tool_param_sites_ne1.py, tool_write_text_drop.py, gen.py, probe2.py
for tag in pristine a l al s_param_sites_ne1 as_param_sites_ne1 \
           ls_param_sites_ne1 als_param_sites_ne1 s_write_text_drop; do
  python3 $S/counter_$tag.py --lane $S/repo \
    --rev 3aee2c078f8976499b587086af3577fc94dc8cf1 \
    --freeze 3aee2c078f8976499b587086af3577fc94dc8cf1
done
python3 $S/counter_s_param_sites_ne1.py --lane $S/repo --rev 3aee2c0... \
  --freeze 3aee2c0... --probe-mutant $S/tool_param_sites_ne1.py
```

## Restoration
No lane bytes were written, restored, or need restoring: the lane checkout was
never modified (`git status` unchanged throughout; the working-tree edits to
`measure.py`/`contract.json` that existed before this run are a sibling's, left
untouched). All mutations were applied to copies under
`/tmp/tameshi-r43-w2-MutC1LiveGate-s1/`, deleted before return. Counter-variant
shas (16-hex prefixes) recorded above for audit.

## Tooling
No installs required (stdlib `python3` + `git` only).

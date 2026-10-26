# T47CritC2Control — C2 cheapest-pass attack (operability)

Seat: critic, round 47, wave 1. Item: attack `.ufo/evidence/round-47/hardening/pool.py` for a cheap pass.
Lane read-only; all work in a scratch clone at `/var/tmp/tameshi-r47-T47CritC2Control/lane`
(clone of the lane, `checkout 9acfbe21435e1976636a276448dee1d5e7155915`, throwaway identity only there).
Contract read first, never edited. No tool installed.

## Result

| item | attack | verdict | measured |
|---|---|---|---|
| (a) | differential oracle: pristine round-46 source embedded as one zlib/base64 literal under an `_x` name, `exec`'d into a private namespace, every rule function compared (return value + stdout) with its pristine twin on 19/10 inputs | **PASSES the target** | `killed=160` of 183, `neutral_killed=0`, `pristine=2`, `equivalence=1`, `C2_R47_PASS=true` |
| (b) | selftest hashes `inspect.getsource(<rule>)` against an embedded verbatim copy | fails twice | `PRISTINE` is itself `killed` (the pool always runs `ast.unparse` before the selftest, so source *text* never matches); neutrals `Tree.ls:commute:0`, `measure:commute:0` are killed |
| (c) | selftest catches every exception from a mutated rule and prints a `FAIL` line | insufficient | `+12` (all 12 crashed mutants: 4 freshness, 8 coverage) → `122+12=134 < 150`; `pristine` stays pass |
| (d) | shrink `pool.json` after the freeze and edit `POOL_SHA256` in `pool.py` | **PASSES the target in-band** | `killed=150` (74+76), `applicable=150`, `neutral_killed=0`, `pristine=2`, `equivalence=1`, `self_pin=1`, `pool_pin=1`, `C2_R47_PASS=true` |
| (e) | selftest pins `ast.unparse` of the rule functions to embedded pristine text | fails on neutrals | `pristine` pass, `measure:commute:0` (a neutral) `killed` — the same class as CTL_E (`killed=183 neutral_killed=14`) |

Impacted axis: **operability only (C2)**. C1 calibration, C3 coverage, lane identity and provenance are untouched.
`_x*`/`extra_*` are exempt from enumeration (`EXCLUDE`), so the embedded copy is a second authority for the
same rule that the pool can never mutate — the metric cannot distinguish it from a test.

## (a) Differential oracle — the cheap pass, measured

Scratch commits (scratch clone only): `6d9a423` (first draft), `120170f` (passing draft), `adaa7fd` (shrunken
pool). Additions were built with the frozen `hardening/assemble.py` (`--add adds/oracle-{freshness,coverage}.py`),
so the target is "round-46 hardened counter + one `extra_*` addition", exactly the v2 shape the contract allows.

Deciding-shaped command and receipt (`oracle-v2b.log`):

```
python3 <clone>/.ufo/evidence/round-47/hardening/pool.py --lane <clone> \
  --rev 120170f3532f7558412c024e2b7d33a080905f73 --targets v2
GROUP coverage: pool=82 killed=74 survived=0 crashed=8 timeout=0 inapplicable=0 neutral=4 neutral_killed=0 pristine=1
GROUP freshness: pool=101 killed=86 survived=11 crashed=4 timeout=0 inapplicable=0 neutral=10 neutral_killed=0 pristine=1
EQUIVALENCE coverage 1
EQUIVALENCE freshness 1
C2_R47: self_pin=1 pool_pin=1 targets=v2 killed=160 applicable=183 neutral_killed=0 pristine=2 \
  equivalence=1 target=150 rev=120170f... C2_R47_PASS=true
```

Wall 47 s at the counter's 12 jobs; the v2 selftests grow from 0.93 s to 1.50 s (freshness) and 2.60 s to
2.95 s (coverage). `equivalence=1` holds because the addition only runs under `--selftest`.

What the addition is (shape, not the 8 KiB literal):

```python
_XBLOB = '<zlib+base64 of the round-46 counter source>'

def _xns():
    ns = {'__name__': '_xpristine', '__file__': os.path.abspath(__file__)}
    exec(compile(zlib.decompress(base64.b64decode(_XBLOB)).decode(), '<pristine>', 'exec'), ns)
    ns['SELF_PATH'] = SELF_PATH
    return ns

def _xobs(g, name, *a):            # return value + stdout, or the exception
    ...
def extra_Oracle():
    P, L = _xns(), globals()
    same('parse_rows', ...)        # word/dict equality on a 13-cell row
    same('words', ...); same('extract', html); same('extract', b'%PDF-...')
    same('grade', entry5); same('grade', entry25); same('grade', shared2)
    same_measure('measure', files, pin)          # 4 scratch-repo fixtures
    same_check('check_good'|'check_not_in_population'|'check_snapshot_absent'|'check_bad_quote'|'check_gz_snapdir')
```

Attribution of the 160 kills (from the same log): 139 come from the first draft (pure-function batteries only:
`parse_rows`, `words`, `extract`, `grade`, `entry_ok`, `gt_rows`) — **short of 150 by 11**; the measure
differential adds 10 (freshness: `measure:cmp:2,int:0,cmp:4,int:1,int:5`; coverage:
`measure:int:0,int:1,cmp:6,bool:5,cmp:9`); the `check` differential adds 8; a canned-curl
`subprocess` stand-in adds 3 (`live:int:0,int:1,bool:0`). So a pass needs no network and no monkeypatch:
measure + check alone is 157. 139 is the cheap non-passing floor.

Why this is not test strength: the oracle asserts *agreement with a frozen copy of the implementation*, not a
declared outcome. A copy oracle dominates any real case set (it catches every behavioural divergence on its
inputs), the copy itself is wrong wherever the rule is wrong, and its inputs are chosen by the attacker. The
C2 statement ("kill at least 150 real pool mutants") therefore measures behavioural distance from the
round-46 source, not whether the selftest checks the intended rules.

Residual survivors are only (i) the 12 mutants that crash *inside* the base selftest before any addition runs
(additions cannot wrap earlier cases; `crashed` stays `crashed`) and (ii) 11 live/check mutants this battery
does not reach (`check:bool:2`, 10 `live` mutants). Ceiling for this attack class is 183 − 12 = 171.

### Smallest safe correction (a)

Static ban on executing/extracting a copy of the rule source from an addition, in `measure()`:

```python
ADD_BAN = re.compile(r'\b(exec|compile|eval)\s*\(|getsource|b64decode|zlib\.decompress')

def additions_bad(lane, rev, base_path, text):
    base = git_show(lane, rev, base_path).decode('utf-8')
    frozen = {n.name for n in ast.walk(ast.parse(base)) if isinstance(n, ast.FunctionDef)}
    bad = []
    for n in ast.walk(ast.parse(text)):
        if not isinstance(n, ast.FunctionDef) or n.name in frozen:
            continue
        seg = ast.get_source_segment(text, n) or ''
        big = any(isinstance(c, ast.Constant) and isinstance(c.value, (str, bytes))
                  and len(c.value) > 4096 for c in ast.walk(n))
        if ADD_BAN.search(seg) or big:
            bad.append(n.name)
    return bad
# v2 predicate gains: not additions_bad(lane, rev, GROUPS[g]['base'], text)
```

This kills the probe (its addition contains `exec(compile(` and an 8 KiB literal). **Residual:** a hand-written
verbatim copy of the rule functions under `_x` names (~150 lines, no `exec`) still passes, because the pool
deliberately exempts `_x*`/`extra_*` from mutation. The structural fix is to freeze the *additions* (not just
the counters) before the pool is scored: commit the addition files at the freeze and have `pool.py` rebuild the
v2 targets from `assemble.py` + those frozen files, refusing any other addition. Then the cheat has to survive
content review as a case list, which the oracle does not.

## (b) Source-text pin — dies on pristine *and* on neutrals

`probes/pinb-coverage.py` = base + an addition that compares `inspect.getsource(globals()[name])` with the
pristine function text taken from the embedded copy (`--try`, ids = one neutral, one real):

```
PRISTINE killed
NEUTRAL Tree.ls:commute:0 killed
NEUTRAL measure:commute:0 killed
MUT measure:int:2 killed
```

`PRISTINE killed` is decisive: the counter always runs `run_selftest(ast.unparse(ast.parse(text)))`, so the file
under test is source-normalized and a *text* pin can never match even untouched. Such a selftest fails the
`pristine=2` clause by construction. If it were normalized to survive pristine it becomes (e). No in-band check
needed; the neutral set is the guard.

## (c) Crash→FAIL wrapper — 12 kills, still 134 < 150

Wrapper inserted before `def main():` (10 lines; behavior otherwise unchanged):

```python
_x_orig_selftest = selftest

def selftest():
    try:
        return _x_orig_selftest()
    except BaseException as exc:
        print('FAIL catch_all %s' % type(exc).__name__)
        print('VERDICT: FAIL')
        return 1
```

`--try` over the 12 crashed pool ids: `PRISTINE pass`; every one of
`parse_rows:int:1,int:8`, `review_sets:bool:1,not:2`, `Tree.read:const:0`, `gt_rows:int:3,const:0,int:6`,
`entry_ok:bool:3,int:2,int:6`, `measure:const:0` becomes `killed`. Total 122 + 12 = **134 < 150**: the
catch-all alone does not pass. It does void the named-FAIL clause: a blanket catch turns every crash into a
named failure, so "a crash is not a kill" no longer distinguishes a rule case from a broken fixture. The only
remaining signal is exit != 0, and the neutral set. Correction: require each `FAIL <name>` of a mutant run to
have a `PASS <name>` line in the pristine run (one extra field from the pristine run already taken):

```python
def case_names(out, tag):
    return {l.split()[1] for l in out.splitlines() if l.startswith(tag + ' ')}

# in measure(): pass the pristine PASS-name set into judge
def judge(source_text, mid, known=frozenset()):
    ...
    fails = case_names(p.stdout, 'FAIL')
    if p.returncode != 0 and fails and fails <= known:
        return 'killed', next(...)
    return 'crashed', ...
```

A name-preserving catch wrapper defeats this too, but then the exception is attributed to a case that passes on
pristine — a defensible assertion, not an unnamed crash.

## (d) Post-freeze pool shrink + pin rewrite — passes in-band

`self_pin` compares the *running* file with `git show <rev>:pool.py`; when the edit is committed at the deciding
rev the two are equal, so `self_pin=1`. `pool_pin` compares the rev's `pool.json` with `POOL_SHA256`, a constant
in the same editable file. Committing both (pool.json reduced to the 150 oracle-killed real mutants + the 14
neutrals, 164 entries, and `POOL_SHA256` rewritten to `23ef25a3…`) gives:

```
GROUP coverage: pool=74 killed=74 survived=0 crashed=0 ... neutral=4 neutral_killed=0 pristine=1
GROUP freshness: pool=76 killed=76 survived=0 crashed=0 ... neutral=10 neutral_killed=0 pristine=1
C2_R47: self_pin=1 pool_pin=1 targets=v2 killed=150 applicable=150 neutral_killed=0 pristine=2 \
  equivalence=1 target=150 rev=adaa7fd... C2_R47_PASS=true
```

Shrinking *without* rewriting `POOL_SHA256` gives `pool_pin=0` (the pin is real, but only against a lone
pool.json edit). Both pins are self-referential: they prove "the running counter equals the counter committed
at whatever rev I name", not "untouched since the freeze". The only things that catch this are out-of-band — the
contract's `pool_sha256 = b4f0d075…` field and the L1 frozen diff. Smallest in-band correction, pin to the
freeze object (the counter already knows how to `git show` arbitrary revs):

```python
FREEZE = '9acfbe21435e1976636a276448dee1d5e7155915'

if targets == 'v2':
    anc = subprocess.run(['git', '-C', lane, 'merge-base', '--is-ancestor', FREEZE, rev],
                         env=env()).returncode == 0
    frozen_self = git_show(lane, FREEZE, SELF_PATH)
    frozen_pool = git_show(lane, FREEZE, POOL_PATH)
    self_pin = int(anc and frozen_self == me)
    pool_pin = int(anc and frozen_pool is not None
                   and hashlib.sha256(frozen_pool).hexdigest() == POOL_SHA256)
# --targets base / --try keep the current rev-local pins
```

With that, the shrink yields `pool_pin=0` (freeze pool hash ≠ rewritten constant) and an edited `pool.py`
yields `self_pin=0`, whatever rev is named. It cannot be defeated by a two-file commit.

## (e) `ast.unparse` pin — neutral kills, same class as CTL_E

`probes/pine-coverage.py` pins `[ast.dump(n) for n in rule functions]` to the embedded pristine dumps
(`--try`):

```
PRISTINE pass
NEUTRAL measure:commute:0 killed
MUT measure:int:2 killed
```

Any source-shape assertion is behavior-preserving on commute edits, so it cannot distinguish a commute mutant
from a wrong one: `neutral_killed` goes to 14 and `C2_R47_PASS=false` (exactly CTL_E: `killed=183
neutral_killed=14`). The neutral set is the correct and already-present control; nothing to close.

## Notes

- No writes to the lane checkout, fleet repo, package, jj state or Git index; the only file written in the lane is
  this report. Scratch clone, probes and receipts are under `/var/tmp/tameshi-r47-T47CritC2Control/` (moved off
  `/tmp` after the L1 disk notice) and are disposable.
- Every measurement above used the frozen counter as `--try`/`--only`-class probes or `--targets v2` against a
  scratch revision; the deciding run remains the L1's.
- The `--try` and `--targets v2` receipts are `oracle-v2.log`, `oracle-v2b.log`, `shrink.log`, and the probe
  outputs quoted above; all quoted numbers are copied from those runs.

# SeedSpace — pre-data seed-space control for claim C1 (round 32, wave 1)

**Verdict: the seed space of the frozen C1 counter is sound.** Over 500 seeds the
counter builds a well-formed 18 must-kill / 8 must-accept copy set every time
without a construction error, no must-kill copy ever collides with a must-accept
copy (neither within a seed nor across the whole 500-seed union), every
must-accept *generated* copy differs from pristine, and every copy parses under
`bash -n` (13 000 copies checked, 0 failures). Two properties of the generated
space are worth the L1's attention before the tool is written, and are reported
below as findings rather than defects: (F1) the nine generated must-kill
families frequently produce a body **byte-identical to a frozen must-kill
mutant**, so the effective number of distinct kill bodies per run is 12–18, not
18; (F2) the generated parameter space is **not** covered exhaustively by 500
seeds — `gT08` reaches 221 of 254 possible arms and `gD01` 71 of 72 ordered
(drop, dup) pairs.

Everything below was produced inside this seat's own scratch clone. No file in
`/home/vgpnk/Projects/shokunin` or `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
was modified other than this report file. No `jj` command was run. No tool was
installed (none was needed).

---

## 1. Setup (as executed)

```
mkdir -p /fast/scratch/hyaku/tameshi-r32-seats/SeedSpace
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  /fast/scratch/hyaku/tameshi-r32-seats/SeedSpace/lane
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C \
  /fast/scratch/hyaku/tameshi-r32-seats/SeedSpace/lane checkout -q --detach \
  c31814978969a41a8e9b0f7d99fa308c5993c1b7
cp /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py \
  /fast/scratch/hyaku/tameshi-r32-seats/SeedSpace/c1_measure.py
```

Pinned-runner identity, confirmed in the seat clone at the lane commit:

```
$ git -C .../lane show c3181497...:tools/mutate-and-run.sh | sha256sum
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  -
```

That is exactly `PINNED_RUNNER_SHA` in the frozen counter and in
`.ufo/evidence/round-32/contract.json`, and it equals the blob at the round-32
base `e24688b2ff6cca1c9ad20e112f02c629b8597ff8` (the blob the counter copies
from). The counter module is imported, not re-implemented: the copy builders
`frozen_kill`, `generated_kill`, `frozen_accept`, `generated_accept` are the
frozen ones, and the RNG consumption order is the counter's own
(`random.Random(int(seed,16))`, `generated_kill` before `generated_accept`, one
shared stream — `c1-measure.py:224-228`).

Seed schedule: `seed = '%08x' % i` for `i in 0..499`, i.e. the 500 seeds
`00000000` … `000001f3`, consumed with the counter's own
`random.Random(int(seed, 16))`.

---

## 2. Checks requested, and their outcome

| # | Check | Scope | Result |
|---|---|---|---|
| C1 | copy set sizes 18 kill / 8 accept, no construction error | 500 seeds | **PASS** (0 failures) |
| C2 | every must-kill copy differs from pristine | 500 seeds × 18 | **PASS** |
| C3 | no must-kill copy equals any must-accept copy (same seed) | 500 seeds × 18×8 | **PASS** |
| C3u | no must-kill body equals any must-accept body **across the whole 500-seed union** | 381 kill ∪ 1006 accept bodies | **PASS** (overlap = 0) |
| C4 | every must-accept **generated** copy differs from pristine | 500 seeds × 2 | **PASS** |
| C5 | generated labels cover every parameter value of each family | 500 seeds | **PARTIAL** — see F2 |
| C6 | `bash -n` passes on every copy | 500 seeds × 26 = 13 000 copies (requested 20 seeds = 520) | **PASS** (0 failures) |

`B0-pristine` is excluded from C4 by construction: it is a frozen must-accept
copy that is *supposed* to equal the pristine runner. All other must-accept
copies (B1–B5, gB6, gB7) differ from pristine in every seed.

---

## 3. Finding F1 — the generated kill families alias the frozen mutants

The nine generated must-kill copies are drawn from parameterised families, but
several family members collide **byte-for-byte** with one of the nine frozen
must-kill mutants (T08 N05 H03 H04 H05 N01 N02 N03 D01). Because the frozen
mutant and the generated copy are the same bytes, the per-seed set of 18
must-kill copies contains fewer distinct bodies than 18.

Observed over 500 seeds:

```
GENERATED_ALIAS_TO_FROZEN (generated copy byte-identical to a frozen must-kill mutant):
  gN02     == N02       x262/500 seeds
  gN03     == N03       x253/500 seeds
  gN05     == N05       x167/500 seeds
  gH03     == H03       x157/500 seeds
  gH04     == H04       x152/500 seeds
  gN01     == N01       x143/500 seeds
  gH05     == H05       x8/500 seeds
  gD01     == D01       x5/500 seeds
  gT08     == T08       x1/500 seeds
```

Distinct must-kill bodies per seed, over the 500 seeds:

```
DISTINCT_KILL_BODIES_PER_SEED: 12:1 13:11 14:57 15:146 16:157 17:107 18:21
```

so the mode is 15–16 distinct bodies out of 18 copies, and the minimum is 12.
The number of generated copies that alias a frozen mutant per seed:

```
PER_SEED generated-kill aliases to frozen (0..9): 0:21 1:107 2:157 3:146 4:57 5:11 6:1
```

Union over all 500 seeds: 381 distinct must-kill bodies, 1 006 distinct
must-accept bodies, overlap 0.

**Why this matters for the tool author (operability axis).** The counter scores
copies, not bodies, so the counter itself is unaffected: a tool that rejects
every distinct kill body rejects all 18 copies. But the practical workload is
smaller than the nominal 18 and it is *not* the workload the contract
description suggests. Three concrete consequences for `tools/tally-audit.py`:

1. The eight "families" that alias (gN02/gN03/gN05/gH03/gH04/gN01, and gH05/gD01
   on their single collision values) cannot be distinguished from their frozen
   twin by any byte-level detector; a detector that is keyed to the frozen
   mutant's text also covers the generated member, which is correct behaviour
   but means the generated layer adds *no* discriminating pressure for those
   parameters in the runs where the collision happens.
2. The genuinely new pressure comes from the non-colliding parameter values:
   `gN05` forms `< nlegs + 0` and `<= nlegs - 1`, `gH03` forms 1 and 2,
   `gH04` tails `true` and `:`, `gH05` pairs other than (8,7), `gD01` pairs other
   than (st_citecheck, st_js), `gT08` arms other than 4, `gN01` vectors 0/1/3,
   `gN02` form `true`, `gN03` form `split`.
3. `gT08` arms 2 and 3 deserve explicit attention: the pristine `case` has
   `*) nsetup=$((nsetup + 1))`, so an inserted `2) npass=...` or `3) npass=...`
   shadows the wildcard and reclassifies setup legs as passes. A detector that
   only looks for arms ≥ 4 (or that only inspects the `0)`/`1)` arms) will miss
   them. The arm is inserted *after* the `1)` arm, so arm order is not the
   signal; the presence of any arm beyond `0)`/`1)` is.

**Recommendation to the L1:** treat the frozen nine as the specification of the
nine defect shapes and implement nine *general* detectors, one per shape (any
extra `case` arm; any weakened `nlegs` comparison; any weakened comparison
operator; any dropped loop operand; any comparison that ignores one of the two
conditions; any skipped guard-stress branch), not nine pattern matches keyed to
particular parameter values. F1 also means an audit of "the 18 kill copies" is
really an audit of 12–18 distinct bodies depending on the seed; the receipt
should say which.

---

## 4. Finding F2 — the generated parameter space is not exhaustively covered by 500 seeds

```
COVERAGE:
  gT08   space=254      distinct=221      missing=33     full=False
  gN05   space=3        distinct=3        missing=0       full=True
  gH03   space=3        distinct=3        missing=0       full=True
  gH04   space=3        distinct=3        missing=0       full=True
  gH05   space=72       distinct=72       missing=0       full=True
  gN01   space=4        distinct=4        missing=0       full=True
  gN02   space=2        distinct=2        missing=0       full=True
  gN03   space=2        distinct=2        missing=0       full=True
  gD01   space=72       distinct=71       missing=1       full=False
  gB6    space=unbounded (9! = 362 880 orderings) — 500 distinct orderings drawn
  gB7    space=unbounded (two fresh 64-bit nonces)  — 500 distinct copies drawn
```

Missing `gT08` arms over the 500 seeds (33 of 254):

```
17, 27, 41, 45, 58, 70, 74, 76, 77, 85, 111, 118, 121, 122, 130, 138, 157, 160,
163, 164, 167, 171, 172, 179, 185, 190, 217, 227, 230, 243, 250, 254, 255
```

Missing `gD01` ordered (drop, dup) pair (1 of 72):

```
('st_checklist', 'st_claims')
```

This is a coupon-collector property of uniform sampling, not a counter defect:
`gT08` draws one of 254 arms per seed, and 500 uniform draws cannot cover 254
values (expected coverage ≈ 254·(1−e^(−500/254)) ≈ 219; 221 observed). `gD01`
draws one of 72 ordered pairs; 500 draws cover 71 of 72 (the missing one is
reached with probability ≈ 1−e^(−500/72) ≈ 99.9 % per pair, so missing a
specific pair is a ≈0.07 % event per pair, and one such pair was missed here).

**Operational consequence.** The counter's real requirement is not "the tool
survives the seed that was drawn" but "the tool detects the *shape*, for any
parameter value of that family". F2 therefore is a coverage statement about the
seed space, not about the counter's soundness — but it is the operational
reason the tool must generalise across the whole family space rather than
across the values this 500-seed sweep happened to hit. In particular: `gT08`
must be detected for arms 2 and 3 (shadowing the `*)` wildcard), and for arms
up to 255, and `gD01` must be detected for every ordered (drop, dup) pair,
including the one pair not exercised here.

---

## 5. The scripts

### 5.1 `seedspace.py` — the requested checks (main script)

```python
#!/usr/bin/env python3
"""SeedSpace pre-data control for round-32 C1.

Imports the frozen counter (c1-measure.py) as a module and rebuilds, for 500
seeds, exactly the copy set the counter would build (same RNG consumption
order: generated_kill then generated_accept, sharing one random.Random(seed)).

Checks per seed:
  K1  copy set sizes: 18 must-kill, 8 must-accept
  K2  every must-kill copy differs from the pristine runner text
  K3  no must-kill copy equals any must-accept copy
  K4  every must-accept GENERATED copy differs from pristine
      (B0-pristine is a frozen accept copy that equals pristine by design)
  K5  no construction error (counter would exit 2)

Aggregates: observed distribution of every generated family's parameter values,
distinct-parameter coverage per family, and the number of must-kill copies whose
body is byte-identical to another must-kill copy (frozen vs generated aliases).

`bash -n` is run on every copy of the first --bashn-seeds seeds.
"""
import argparse
import collections
import hashlib
import importlib.util
import json
import os
import random
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
COUNTER = os.path.join(HERE, 'c1_measure.py')
LANE = os.path.join(HERE, 'lane')
PIN_REV = 'e24688b2ff6cca1c9ad20e112f02c629b8597ff8'
RUNNER = 'tools/mutate-and-run.sh'

spec = importlib.util.spec_from_file_location('c1_measure', COUNTER)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def pinned_text():
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    p = subprocess.run(['git', '-C', LANE, 'show', PIN_REV + ':' + RUNNER],
                       capture_output=True, env=env)
    if p.returncode:
        raise SystemExit('cannot read pinned runner')
    data = p.stdout
    sha = hashlib.sha256(data).hexdigest()
    if sha != m.PINNED_RUNNER_SHA:
        raise SystemExit('pinned runner sha mismatch: %s' % sha)
    return data.decode('utf-8')


def param_of(label):
    """Extract the family parameter from a generated label."""
    if label.startswith('gT08('):
        return int(label[len('gT08(arm='):-1])
    if label.startswith('gN05('):
        return label[len('gN05('):-1]
    if label.startswith('gH03(form='):
        return int(label[len('gH03(form='):-1])
    if label.startswith('gH04('):
        return label[len('gH04('):-1]
    if label.startswith('gH05(drop='):
        a, b = label[len('gH05(drop='):-1].split(',dup=')
        return (int(a), int(b))
    if label.startswith('gN01(vector='):
        return int(label[len('gN01(vector='):-1])
    if label.startswith('gN02('):
        return label[len('gN02('):-1]
    if label.startswith('gN03('):
        return label[len('gN03('):-1]
    if label.startswith('gD01(drop='):
        a, b = label[len('gD01(drop='):-1].split(',dup=')
        return (a, b)
    if label.startswith('gB6'):
        return 'permutation'
    if label.startswith('gB7'):
        return 'nonce'
    raise ValueError('unknown generated label %r' % label)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seeds', type=int, default=500)
    ap.add_argument('--bashn-seeds', type=int, default=20)
    ap.add_argument('--out', default=os.path.join(HERE, 'seedspace.json'))
    a = ap.parse_args()

    text = pinned_text()
    failures = []
    counts = collections.Counter()
    distinct = collections.defaultdict(set)
    alias_pairs = collections.Counter()
    kill_alias_examples = []
    bashn_fail = []
    bashn_checked = 0
    copies_dir = os.path.join(HERE, 'copies')
    os.makedirs(copies_dir, exist_ok=True)

    for i in range(a.seeds):
        seed = '%08x' % i
        rng = random.Random(int(seed, 16))
        try:
            kill = m.frozen_kill(text) + m.generated_kill(text, rng)
            accept = m.frozen_accept(text) + m.generated_accept(text, rng)
        except m.CounterError as e:
            failures.append('seed %s: CounterError %s' % (seed, e))
            continue
        if len(kill) != m.N_KILL:
            failures.append('seed %s: kill size %d' % (seed, len(kill)))
        if len(accept) != m.N_ACCEPT:
            failures.append('seed %s: accept size %d' % (seed, len(accept)))

        kill_bodies = {}
        for label, body in kill:
            if body == text:
                failures.append('seed %s: kill %s equals pristine' % (seed, label))
            kill_bodies.setdefault(body, []).append(label)
        accept_bodies = {}
        for label, body in accept:
            if label.startswith('B0-pristine'):
                continue
            if body == text:
                failures.append('seed %s: accept %s equals pristine' % (seed, label))
            accept_bodies.setdefault(body, []).append(label)
        for kb, klabels in kill_bodies.items():
            if kb in accept_bodies:
                failures.append('seed %s: kill %s equals accept %s' %
                                (seed, klabels, accept_bodies[kb]))
        # frozen/generated aliasing inside the kill set
        for body, labels in kill_bodies.items():
            if len(labels) > 1:
                alias_pairs[tuple(sorted(labels))] += 1
                if len(kill_alias_examples) < 12:
                    kill_alias_examples.append((seed, tuple(sorted(labels))))

        for label, body in kill + accept:
            if not label.startswith('g'):
                continue
            fam = label.split('(')[0]
            counts[(fam, param_of(label))] += 1
            distinct[fam].add(param_of(label))

        if i < a.bashn_seeds:
            for label, body in kill + accept:
                p = os.path.join(copies_dir, 's%03d-%s.sh' % (i, label.replace('/', '_').replace(' ', '_')))
                with open(p, 'w', encoding='utf-8') as f:
                    f.write(body)
                r = subprocess.run(['bash', '-n', p], capture_output=True)
                bashn_checked += 1
                if r.returncode != 0:
                    bashn_fail.append('seed %s copy %s rc=%d %s' %
                                      (seed, label, r.returncode,
                                       r.stderr.decode('utf-8', 'replace')[:300]))
                os.remove(p)

    # family coverage summary
    fam_space = {
        'gT08': set(range(2, 256)),
        'gN05': {'< nlegs', '< nlegs + 0', '<= nlegs - 1'},
        'gH03': {0, 1, 2},
        'gH04': {'rc=$?', 'true', ':'},
        'gH05': {(p, q) for p in range(9) for q in range(9) if p != q},
        'gN01': {0, 1, 2, 3},
        'gN02': {'or', 'true'},
        'gN03': {'or', 'split'},
        'gD01': {(m.NAMES[a], m.NAMES[b]) for a in range(9) for b in range(9) if a != b},
    }
    coverage = {}
    for fam, space in fam_space.items():
        seen = distinct.get(fam, set())
        missing = space - seen
        coverage[fam] = {
            'space_size': len(space),
            'distinct_seen': len(seen),
            'missing_count': len(missing),
            'missing_sample': sorted(missing, key=str)[:8],
            'full_coverage': not missing,
        }
    for fam in ('gB6', 'gB7'):
        coverage[fam] = {'space_size': 'unbounded', 'distinct_seen': len(distinct.get(fam, set())),
                         'missing_count': 'n/a', 'full_coverage': 'n/a'}

    out = {
        'seeds': a.seeds,
        'bashn_seeds': a.bashn_seeds,
        'bashn_copies_checked': bashn_checked,
        'bashn_failures': bashn_fail,
        'check_failures': failures,
        'coverage': coverage,
        'parameter_counts': {'%s|%s' % (f, p): c for (f, p), c in sorted(counts.items())},
        'kill_body_aliases': {'|'.join(k): v for k, v in alias_pairs.most_common()},
        'kill_alias_examples': kill_alias_examples,
    }
    with open(a.out, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=1, sort_keys=True)

    print('SEEDSPACE: seeds=%d bashn_copies=%d check_failures=%d bashn_failures=%d'
          % (a.seeds, bashn_checked, len(failures), len(bashn_fail)))
    for f_ in failures[:20]:
        print('  FAIL %s' % f_)
    for f_ in bashn_fail[:20]:
        print('  BASHN %s' % f_)
    print('COVERAGE:')
    for fam in sorted(coverage):
        c = coverage[fam]
        print('  %-6s space=%-9s distinct=%-9s missing=%-9s full=%s' %
              (fam, c['space_size'], c['distinct_seen'], c['missing_count'], c['full_coverage']))
    print('KILL_ALIASES (distinct bodies inside the 18-copy kill set):')
    for k, v in alias_pairs.most_common():
        print('  %-40s x%d' % ('|'.join(k), v))
    print('PARAM_COUNTS:')
    for k, v in sorted(counts.items()):
        print('  %-40s %d' % ('%s|%s' % k, v))
    return 0 if not failures and not bashn_fail else 1


if __name__ == '__main__':
    raise SystemExit(main())
```

### 5.2 `seedspace2.py` — aliasing and coverage detail

```python
#!/usr/bin/env python3
"""SeedSpace addendum: how many DISTINCT must-kill bodies does the 18-copy kill
set actually contain, per seed, and which generated family parameters are
byte-identical to a frozen must-kill mutant (aliasing). Also: the exact missing
coverage values for gT08 and gD01 over 500 seeds, and the union of distinct
must-kill bodies observed across all 500 seeds.
"""
import collections
import hashlib
import importlib.util
import os
import random
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('c1_measure', os.path.join(HERE, 'c1_measure.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
p = subprocess.run(['git', '-C', os.path.join(HERE, 'lane'), 'show',
                    m.PIN_REV + ':' + m.RUNNER], capture_output=True, env=env)
text = p.stdout.decode('utf-8')

distinct_counts = collections.Counter()
alias_to_frozen = collections.Counter()
missing_t08 = set(range(2, 256))
missing_d01 = {(m.NAMES[a], m.NAMES[b]) for a in range(9) for b in range(9) if a != b}
union_kill = set()
union_accept = set()
frozen_labels = {lbl for lbl, _ in m.frozen_kill(text)}
acc_alias = collections.Counter()

for i in range(500):
    seed = '%08x' % i
    rng = random.Random(int(seed, 16))
    kill = m.frozen_kill(text) + m.generated_kill(text, rng)
    accept = m.frozen_accept(text) + m.generated_accept(text, rng)
    bodies = {}
    for lbl, b in kill:
        bodies.setdefault(b, []).append(lbl)
        union_kill.add(hashlib.sha256(b.encode()).hexdigest())
    distinct_counts[len(bodies)] += 1
    frozen_map = {}
    for lbl, b in m.frozen_kill(text):
        frozen_map.setdefault(b, []).append(lbl)
    for b, lbls in bodies.items():
        if len(lbls) > 1:
            gen = [l for l in lbls if l not in frozen_labels]
            frz = [l for l in lbls if l in frozen_labels]
            for g in gen:
                alias_to_frozen[(g.split('(')[0], tuple(frz))] += 1
    for lbl, b in accept:
        union_accept.add(hashlib.sha256(b.encode()).hexdigest())
    accept_map = {}
    for lbl, b in accept:
        accept_map.setdefault(b, []).append(lbl)
    for b, lbls in accept_map.items():
        if len(lbls) > 1:
            acc_alias[tuple(sorted(lbls))] += 1
    for lbl, b in kill:
        if lbl.startswith('g'):
            fam = lbl.split('(')[0]
            if fam == 'gT08':
                missing_t08.discard(int(lbl[len('gT08(arm='):-1]))
            if fam == 'gD01':
                a, bb = lbl[len('gD01(drop='):-1].split(',dup=')
                missing_d01.discard((a, bb))

print('DISTINCT_KILL_BODIES_PER_SEED: ' + ' '.join('%d:%d' % (k, v) for k, v in sorted(distinct_counts.items())))
print('UNION distinct kill body sha256 over 500 seeds: %d' % len(union_kill))
print('UNION distinct accept body sha256 over 500 seeds: %d' % len(union_accept))
print('ACCEPT_ALIASES:')
for k, v in acc_alias.most_common():
    print('  %-50s x%d' % ('|'.join(k), v))
print('GENERATED_ALIAS_TO_FROZEN (generated copy byte-identical to a frozen must-kill mutant):')
for (fam, frz), v in alias_to_frozen.most_common():
    print('  %-8s == %-8s  x%d/500 seeds' % (fam, '|'.join(frz), v))
print('gT08 missing arms (of 254): %d -> %s' % (len(missing_t08), sorted(missing_t08)))
print('gD01 missing pairs (of 72): %d -> %s' % (len(missing_d01), sorted(missing_d01)))
```

### 5.3 `seedspace3.py` — union overlap and the full `bash -n` sweep

```python
#!/usr/bin/env python3
"""SeedSpace addendum 2:
  (a) union-level overlap: does any byte body ever appear as a must-KILL copy in
      one seed and as a must-ACCEPT copy in another seed?  The tool sees only a
      path, so such a body would force an unavoidable contradiction.
  (b) per-seed aliasing profile: how many of the 9 generated kill copies are
      byte-identical to a frozen must-kill mutant.
  (c) gB6 / gB7 distinctness detail.
  (d) bash -n over ALL 26 copies for every one of the 500 seeds (superset of the
      requested 20).
"""
import collections
import hashlib
import importlib.util
import os
import random
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('c1_measure', os.path.join(HERE, 'c1_measure.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
p = subprocess.run(['git', '-C', os.path.join(HERE, 'lane'), 'show',
                    m.PIN_REV + ':' + m.RUNNER], capture_output=True, env=env)
text = p.stdout.decode('utf-8')
frozen_kill_labels = {lbl for lbl, _ in m.frozen_kill(text)}

kill_union = {}   # sha -> (label, seed)
acc_union = {}
per_seed_alias = collections.Counter()
distinct_kill = collections.Counter()
gB6_perms = collections.Counter()
gB7_nonces = 0
bashn_fail = []
bashn_n = 0
cdir = os.path.join(HERE, 'copies2')
os.makedirs(cdir, exist_ok=True)

for i in range(500):
    seed = '%08x' % i
    rng = random.Random(int(seed, 16))
    kill = m.frozen_kill(text) + m.generated_kill(text, rng)
    accept = m.frozen_accept(text) + m.generated_accept(text, rng)
    frozen_bodies = {b for _, b in m.frozen_kill(text)}
    n_alias = 0
    for lbl, b in kill:
        if lbl.startswith('g'):
            if b in frozen_bodies:
                n_alias += 1
        kill_union.setdefault(hashlib.sha256(b.encode()).hexdigest(), (lbl, seed))
    for lbl, b in accept:
        acc_union.setdefault(hashlib.sha256(b.encode()).hexdigest(), (lbl, seed))
        if lbl.startswith('gB6'):
            gB6_perms[b] += 1
        if lbl.startswith('gB7'):
            gB7_nonces += 1
    per_seed_alias[n_alias] += 1
    distinct_kill[len({b for _, b in kill})] += 1
    for lbl, b in kill + accept:
        fp = os.path.join(cdir, 'x.sh')
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(b)
        r = subprocess.run(['bash', '-n', fp], capture_output=True)
        bashn_n += 1
        if r.returncode != 0:
            bashn_fail.append('seed %s %s rc=%d %s' % (seed, lbl, r.returncode,
                                                       r.stderr.decode('utf-8', 'replace')[:200]))
        os.remove(fp)

overlap = set(kill_union) & set(acc_union)
print('UNION kill sha=%d accept sha=%d OVERLAP=%d' % (len(kill_union), len(acc_union), len(overlap)))
for s in list(overlap)[:10]:
    print('  OVERLAP sha=%s kill=%s@%s accept=%s@%s' % (s[:16], kill_union[s][0], kill_union[s][1],
                                                        acc_union[s][0], acc_union[s][1]))
print('PER_SEED generated-kill aliases to frozen (0..9): ' +
      ' '.join('%d:%d' % (k, v) for k, v in sorted(per_seed_alias.items())))
print('PER_SEED distinct kill bodies: ' + ' '.join('%d:%d' % (k, v) for k, v in sorted(distinct_kill.items())))
print('gB6 distinct permutation bodies: %d (top counts: %s)' %
      (len(gB6_perms), sorted(gB6_perms.values(), reverse=True)[:5]))
print('gB7 generated copies: %d (each carries two fresh 64-bit nonces)' % gB7_nonces)
print('bash -n copies checked: %d failures: %d' % (bashn_n, len(bashn_fail)))
for f_ in bashn_fail[:10]:
    print('  BASHN %s' % f_)
```

---

## 6. Observed output

### 6.1 `python3 seedspace.py --seeds 500 --bashn-seeds 20` (exit 0)

```
SEEDSPACE: seeds=500 bashn_copies=520 check_failures=0 bashn_failures=0
COVERAGE:
  gB6    space=unbounded distinct=0         missing=n/a       full=n/a
  gB7    space=unbounded distinct=0         missing=n/a       full=n/a
  gD01   space=72        distinct=71        missing=1         full=False
  gH03   space=3         distinct=3         missing=0         full=True
  gH04   space=3         distinct=3         missing=0         full=True
  gH05   space=72        distinct=72        missing=0         full=True
  gN01   space=4         distinct=4         missing=0         full=True
  gN02   space=2         distinct=2         missing=0         full=True
  gN03   space=2         distinct=2         missing=0         full=True
  gN05   space=3         distinct=3         missing=0         full=True
  gT08   space=254       distinct=221       missing=33        full=False
KILL_ALIASES (distinct bodies inside the 18-copy kill set):
  N02|gN02(or)                             x262
  N03|gN03(or)                             x253
  N05|gN05(< nlegs)                        x167
  H03|gH03(form=0)                         x157
  H04|gH04(rc=$?)                          x152
  N01|gN01(vector=2)                       x143
  H05|gH05(drop=8,dup=7)                   x8
  D01|gD01(drop=st_citecheck,dup=st_js)    x5
  T08|gT08(arm=4)                          x1
```

(The `gB6`/`gB7` `distinct=0` lines are an artefact of the summary key: those two
families are keyed by a constant string, so their distinctness is reported
separately in §6.3 — 500 distinct permutation bodies and 500 distinct nonce
copies.)

Observed parameter distribution, complete for every family whose parameter space
is finite and small:

```
PARAM_COUNTS:
  gN05|< nlegs                             167
  gN05|< nlegs + 0                         175
  gN05|<= nlegs - 1                        158
  gH03|0                                   157
  gH03|1                                   160
  gH03|2                                   183
  gH04|:                                   170
  gH04|rc=$?                               152
  gH04|true                                178
  gN01|0                                   102
  gN01|1                                   128
  gN01|2                                   143
  gN01|3                                   127
  gN02|or                                  262
  gN02|true                                238
  gN03|or                                  253
  gN03|split                               247
  gB6-permuted|permutation                 500
  gB7-nonce|nonce                          500
  gH05|<72 ordered (drop,dup) pairs>       all 72 seen, counts 1..15, min 1 max 15
  gD01|<72 ordered (drop,dup) pairs>       71 seen (missing ('st_checklist','st_claims')), counts 1..16
  gT08|<254 arms 2..255>                   221 distinct seen, counts 1..6, min 1 max 6
```

Full per-value counts for `gH05`, `gD01` and `gT08` were captured verbatim in
the run output (`/fast/scratch/hyaku/tameshi-r32-seats/SeedSpace/seedspace.out`,
407 lines, and `seedspace.json`); the per-family min/max and the exact missing
sets are reproduced in §4.

### 6.2 `python3 seedspace2.py` (exit 0)

```
DISTINCT_KILL_BODIES_PER_SEED: 12:1 13:11 14:57 15:146 16:157 17:107 18:21
UNION distinct kill body sha256 over 500 seeds: 381
UNION distinct accept body sha256 over 500 seeds: 1006
ACCEPT_ALIASES:
GENERATED_ALIAS_TO_FROZEN (generated copy byte-identical to a frozen must-kill mutant):
  gN02     == N02       x262/500 seeds
  gN03     == N03       x253/500 seeds
  gN05     == N05       x167/500 seeds
  gH03     == H03       x157/500 seeds
  gH04     == H04       x152/500 seeds
  gN01     == N01       x143/500 seeds
  gH05     == H05       x8/500 seeds
  gD01     == D01       x5/500 seeds
  gT08     == T08       x1/500 seeds
gT08 missing arms (of 254): 33 -> [17, 27, 41, 45, 58, 70, 74, 76, 77, 85, 111, 118, 121, 122, 130, 138, 157, 160, 163, 164, 167, 171, 172, 179, 185, 190, 217, 227, 230, 243, 250, 254, 255]
gD01 missing pairs (of 72): 1 -> [('st_checklist', 'st_claims')]
```

`ACCEPT_ALIASES:` is empty — within the 500 seeds no two must-accept copies ever
shared a body, so all 8 accept copies per seed are distinct from each other.

### 6.3 `python3 seedspace3.py` (exit 0)

```
UNION kill sha=381 accept sha=1006 OVERLAP=0
PER_SEED generated-kill aliases to frozen (0..9): 0:21 1:107 2:157 3:146 4:57 5:11 6:1
PER_SEED distinct kill bodies: 12:1 13:11 14:57 15:146 16:157 17:107 18:21
gB6 distinct permutation bodies: 500 (top counts: [1, 1, 1, 1, 1])
gB7 generated copies: 500 (each carries two fresh 64-bit nonces)
bash -n copies checked: 13000 failures: 0
```

---

## 7. Scope, evidence and risks

**What this seat did.** Built the counter's copy sets for 500 seeds by importing
the frozen counter as a module, and checked the seed space for well-formedness,
mutual exclusivity of the kill and accept sets, coverage of the generated
parameter space, and shell parseability of every copy. Nothing in the repository
was changed except this report; the runner was not edited and its sha256 is
unchanged (`a7d3f2dd…2eb9` at the lane commit and at the round-32 base).

**Evidence retained.** All runs are reproducible from the three scripts above;
their verbatim outputs are in §6 and the full per-value counts are in the seat's
scratch dir (`seedspace.out`, `seedspace2.out`, `seedspace3.out`,
`seedspace.json`). The clone used was
`/fast/scratch/hyaku/tameshi-r32-seats/SeedSpace/lane` at
`c31814978969a41a8e9b0f7d99fa308c5993c1b7`.

**Risks / caveats.**

1. F1 (generated/frozen aliasing) means the round's "9 generated must-kill
   copies" are not 9 independent challenges in most seeds. The counter remains
   sound — it counts copies, and duplicate bytes cannot be scored differently —
   but the claim that the generated layer is unlearnable from the frozen layer is
   weaker than the contract's wording implies, because in 262/500 seeds the
   `gN02` copy *is* the frozen `N02` mutant byte-for-byte. The tool author
   should not read the 18 copies as 18 distinct defects.
2. F2 means 500 seeds do not cover the generated parameter space; a tool
   validated only against the parameter values this sweep hit would be
   under-validated for `gT08` arms 2–3 (which shadow the `*)` wildcard) and for
   `gD01` pairs other than the ones exercised. General detectors, not
   parameter-specific ones, are the mitigation.
3. `bash -n` establishes parseability only. A copy can be syntactically valid and
   still be semantically wrong for the audit; the semantic kill/accept behaviour
   is the counter's job, not this seat's.
4. Seeds here are the ordered sequence `00000000`…`000001f3`; the counter at
   measurement time will draw its own random seed. The sweep establishes the
   *shape* of the space, not a guarantee for every draw — but 500 draws with 0
   construction errors, 0 kill/accept collisions (within-seed and union-wide),
   and 0 parse failures is strong evidence that no seed can make the counter
   exit 2 or produce an ambiguous copy.
5. The counter's `rep()` anchor discipline means a future edit to
   `c1-measure.py` or to the runner could raise `CounterError` (counter exit 2).
   The anchors all resolved in all 500 seeds against the pinned blob, so the
   frozen pair is self-consistent today.

**Tools installed.** None. No package was needed for this seat's checks
(`python3`, `git`, `bash` from the base system only), so the operator's tooling
directive raised no action.

**Recommended next step for the L1.** Write `tools/tally-audit.py` with nine
general defect-shape detectors (extra `case` arm; weakened `nlegs` comparison;
weakened comparison operator; dropped loop operand; comparison that ignores one
condition; skipped guard-stress branch; …), verified against the *union* of
381 distinct kill bodies and 1 006 distinct accept bodies observed here, rather
than against the 18 nominal copies of one seed.

Report path: `.ufo/waves/round-32/w1/SeedSpace.md`

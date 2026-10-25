# ScoutV2Miss — v3 vs v2 expected-value sites on tools/*.py

Seat: read-only scout. Frozen rev `d4ee4e63a0a4402bd8628fbc80f06bbd8f37d937`, base `a3d6c690bcbf8914551d4f4e8e1612784c1c2046`.
No lane file edited. Neither counter was run (the L1 owns the one deciding run).

## Bottom line

- v3 resolves **8** expected-value sites that v2 does not, on the same 25 `tools/*.py` files.
- v3 labels **2** of them `unflagged=1 scratch=0`: `tools/context-capture.py:1682` and `tools/context-capture.py:1685`.
- **Those two are not a real open write path.** Both write through `expected_path` (`context-capture.py:1662`) → `directory = self.case_dir(name)` (`:1660`) → `path = os.path.join(self.root, ...)` (`:1633`), and `self.root` is `tempfile.mkdtemp(prefix="context-capture-selftest-", dir="/tmp")` (`:1624`, single assignment). The destinations are under `/tmp`. The file's own docstring says so: "the only writes are --selftest fixtures under mkdtemp" (`:12`).
- **Answer to the asked question: none.** No unflagged, non-scratch open write path in this lane is newly resolved by v3. The only sites v3 labels that way are scratch in fact; the mislabel is v3's, not a missed writer.
- For the record, `tools/*.py` does contain one genuine unflagged non-scratch expected-valued writer — `tools/registry-replay.py:123` — but **v2 sees it too** (literal on the same line), so it is not a v3 gain and does not enter the list below.

## Imported copies (hashes match the C2 contract pins)

`/tmp/tameshi-r41-scoutv2miss-*` did not exist at seat start, so I created `/tmp/tameshi-r41-scoutv2miss-scout/` and imported from the frozen rev rather than from a peer directory:

```
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
git show d4ee4e63a0a4402bd8628fbc80f06bbd8f37d937:tools/write-path-census-v2.py \
  > /tmp/tameshi-r41-scoutv2miss-scout/write-path-census-v2.py
git show d4ee4e63a0a4402bd8628fbc80f06bbd8f37d937:tools/write-path-census-v3.py \
  > /tmp/tameshi-r41-scoutv2miss-scout/write-path-census-v3.py
```

| copy | sha256 | contract pin | match |
|---|---|---|---|
| v2 | `4022853295882c5a11e192274e9215ea5a008e54eb0a2f77a8a2365f522d878b` | same | yes |
| v3 | `095924a7a165be96e69ff9dad67d3e513d23ba6737c35a0537f898482eef0279` | same | yes |

## Method

`v3` has `--file`; `v2` has no file mode at all (only `--selftest`, `main()` otherwise prints usage), so v2 is driven through its own `classify_text` semantics replayed per line — `WRITE_RE ∧ EXPECTED_RE ∧ ¬SCRATCH_RE ∧ ¬FLAG_RE` on the same line, which is exactly what `classify_text` accumulates. Driver: `/tmp/tameshi-r41-scoutv2miss-scout/compare.py` and `inventory.py`; both import the two copies above by path.

```
python3 /tmp/tameshi-r41-scoutv2miss-scout/compare.py     # per-line disagreement + totals
python3 /tmp/tameshi-r41-scoutv2miss-scout/inventory.py   # full 25-file table
python3 /tmp/tameshi-r41-scoutv2miss-scout/write-path-census-v3.py --file tools/context-capture.py
```

Scope: `tools/*.py` = 25 files (`tools/vendor/` holds only two `.tgz` tarballs, no Python).

## Every expected-value site v3 resolves and v2 does not

Record fields are v3's own (`expected`, `scratch`, `unflagged`).

| # | site | kind | expected | scratch | unflagged | v2 |
|---|---|---|---|---|---|---|
| 1 | `tools/context-capture.py:1682` | `open` | 1 | **0** | **1** | no destination (line is `with open(expected_path, "wb")`) |
| 2 | `tools/context-capture.py:1685` | `open` | 1 | **0** | **1** | no destination |
| 3 | `tools/golden-verdict.py:52` | `open` | 1 | 1 | 0 | no destination |
| 4 | `tools/golden-verdict.py:54` | `open` | 1 | 1 | 0 | no destination |
| 5 | `tools/golden-verdict.py:56` | `open` | 1 | 1 | 0 | no destination |
| 6 | `tools/repeat-control.py:811` | `open` | 1 | 1 | 0 | no destination |
| 7 | `tools/repeat-control.py:820` | `os.symlink` | 1 | 1 | 0 | no destination (multi-line call) |
| 8 | `tools/write-path-census.py:95` | `open` | 1 | 1 | 0 | no destination (file also `flagged=1`) |

Resolution chains, for auditability:

- `context-capture.py:1662 expected_path = os.path.join(directory, "expected.json")`; `:1660 directory = self.case_dir(name)`; `:1633 path = os.path.join(self.root, "{:02d}-{}".format(...))`; `:1624 self.root = tempfile.mkdtemp(..., dir="/tmp")`.
- `repeat-control.py:806 tamper_duplicate_key = os.path.join(scratch, ...)` → `:808 duplicate_path = os.path.join(tamper_duplicate_key, "expected.json")` → `:811 open(duplicate_path, "wb")`; symlink twin at `:817/:819-822`, destination `os.path.join(tamper_manifest_symlink, "expected.json")`.
- `golden-verdict.py:47 with tempfile.TemporaryDirectory(...) as tmp:` → `:48 golden = os.path.join(tmp, 'expected.txt')` → `:52/:54/:56 open(...)` (also `:49-51` for `same`/`other`). v3's `_bind` records `ast.With` `optional_vars`, so the scratch marker lands in the trace — correct.
- `write-path-census.py:95` sits under its own `tempfile.TemporaryDirectory` selftest; correct scratch.

## The two sites v3 calls non-scratch are scratch in fact

`context-capture.py:1682/1685` write `expected.json` into `self.case_dir(name)`, whose base is `self.root`, a `mkdtemp(dir="/tmp")` created once in `SelftestHarness.__init__` (`:1624`). They are selftest fixtures under `/tmp` and are removed in `finally` (`:1778`). No CLII path reaches them with a non-temp root.

Why v3 misses the marker — two declared-scope gaps meeting:

1. `_bind` binds only `ast.Name` targets (`Assign`/`AnnAssign`/`With`). `self.root = tempfile.mkdtemp(...)` targets an `ast.Attribute`, so nothing is recorded; attribute reassignment is explicitly outside the declared scope.
2. `self.case_dir(name)` is a `Call` that does not fold. v3's `Call` branch in `_resolve` still emits the call's **own source text** plus every argument, so the destination resolves to `os.path.join(directory, "expected.json")self.case_dir(name)...` — a non-empty string containing `expected.json`, with no `tempfile`/`/tmp` token anywhere in it.

Consequence for any claim built on `unflagged`/`scratch` counters: **a resolvable expected literal on an unresolvable base always yields `expected=1`, and yields `scratch=0` unless the scratch origin happens to be textually inside the trace.** This is the same class the tool documents as unresolved; it is a precision ceiling, not a defect against the declared contract. It means `var_unflagged`/`live_var_*` results must be read together with a manual check of the base expression, exactly as was done here.

## v2 side (for completeness, not part of the requested list)

v2's 5 expected hits on the same 25 files: 2 true positives (`registry-replay.py:123`, `wave-accounting.py:165` — the latter is scratch via `TemporaryDirectory` at `:156-157`) and 3 false positives that v3 correctly drops:

- `tools/write-path-census.py:58` and `:59` — the `PLANTED` fixture strings, not call sites.
- `tools/write-path-census-v3.py:6` — docstring prose (`` `dest = os.path.join(root, "expected.json")` followed by `os.replace(dest, x)` ``) matched because both patterns appear on one prose line.

Totals, 25 files: v2 expected lines 5, v3 expected sites 10, overlap 2, v3-only 8, v3 `unflagged` 3 (`context-capture.py:1682/1685` plus `registry-replay.py:123`), v3 `unflagged ∧ ¬scratch` 3.

## Small extra observation

`_write_call` returns **both** arguments of `os.replace`/`os.rename` as destinations (`[node.args[1], node.args[0]]`); `args[0]` is the source, not a destination. No `tools/*.py` site makes that observable here (the `os.replace`/`os.rename` sites are `bash-witness-study.py:778`, `evidence-disposition.py:2266,2330`, `pin-disposition.py:1163,1183,1186,1206`; none resolves to expected text), so it does not change any count above — but a future pair of expected-named source/target paths would be double-counted.

## Confidence

- High: all `file:line` facts above are direct output of the two imported copies against the frozen tree, plus direct reads of the named lines.
- High: `context-capture.py` destinations are under `mkdtemp(dir="/tmp")` — single `self.root` assignment (`:1624`), corroborated by the module docstring (`:12`) and `shutil.rmtree(self.root)` (`:1778`).
- Medium (not required by this seat, not claimed): whether C2's own predicate tolerates the `context-capture.py` mislabel. It does not affect `live_var_*`/`live_symlink_*`, which are measured on `repeat-control.py`.

## Remaining unknowns

- None on the asked question.
- Not measured (out of scope, L1-owned): the one deciding default-mode run of `calibration/measure.py` and `census/measure.py`, and the two recognizer-removal mutants.

## Tooling

No install or upgrade was performed; nothing added to the host. Scratch only under `/tmp/tameshi-r41-scoutv2miss-scout/` (`compare.py`, `inventory.py`, `diff.json`, the two imported tool copies).

## Appendix — relocation note and inlined drivers

The `round-35` scratch tree discussed mid-wave is **not** part of this seat. The relocation was `scratch/` → `scratch-evidence/` in the `mado-shokunin` lane — absolute path `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-35/scratch-evidence/`, 59 seat dirs, verified on disk, together with the peer's cited `rederive.sh` and `rederive.out` in its `RevQuoteS210` seat directory at 3727 B / `468c54a6…` and 2714 B / `4b7b77d6…`. This lane has no `scratch*` directory under its round-35 wave at any depth (`find .ufo/waves -maxdepth 5 -name 'scratch*'` returned nothing). This report cites no `round-35` path as evidence under either name; the only mentions of that tree are this paragraph, so no citation needed correcting.

Nothing here was rebuilt from transcript. The two blocks below are the exact bytes that produced the numbers above — extracting them from this file and `cmp`-ing against the executed drivers reports identical, so the pins are meaningful:

| driver | sha256 |
|---|---|
| `compare.py` | `9605ddebb146de26b4b5166d55a4a99bf0cf74a50de34057a4f35c381ef1c141` |
| `inventory.py` | `bd2cbb54829f78f19819a169efb7b4291113b9692800cb8c2f699853ff72eb6e` |

Re-extracting both blocks and running them reproduces the reported totals (25 files; only-v3 4, only-v2 2; v2 expected lines 5, v3 expected sites 10, v3 `unflagged` 3, unflagged∧non-scratch 3). Scratch lives at `/tmp/tameshi-r41-scoutv2miss-scout/`, outside the lane; by design the report body, not scratch, is the durable evidence locus, so the numbers stand even if `/tmp` is cleared. The comparison can also be rebuilt from this file alone by re-running the two `git show` imports above.

`compare.py` — per-line disagreement and totals:

```python
import importlib.util, glob, os, re, sys, json

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
SCR = '/tmp/tameshi-r41-scoutv2miss-scout'

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

v2 = load('wpc2', os.path.join(SCR, 'write-path-census-v2.py'))
v3 = load('wpc3', os.path.join(SCR, 'write-path-census-v3.py'))

rows = []
for path in sorted(glob.glob(os.path.join(LANE, 'tools', '*.py'))):
    rel = os.path.relpath(path, LANE)
    text = open(path, encoding='utf-8', errors='replace').read()
    flagged = v2.FLAG_RE.search(text) is not None
    # v2: per-line expected-value sites (line-based, literal on same line)
    v2_lines = {}
    for i, line in enumerate(text.splitlines(), 1):
        if v2.WRITE_RE.search(line) and v2.EXPECTED_RE.search(line) and v2.SCRATCH_RE.search(line) is None and not flagged:
            v2_lines[i] = line.strip()
    v2_all_expected_lines = {}
    for i, line in enumerate(text.splitlines(), 1):
        if v2.WRITE_RE.search(line) and v2.EXPECTED_RE.search(line):
            v2_all_expected_lines[i] = line.strip()
    recs = v3.classify_source(text)
    v3_expected = [r for r in recs if r['expected']]
    v3_by_line = {}
    for r in v3_expected:
        v3_by_line.setdefault(r['lineno'], []).append(r)
    only3 = sorted(set(v3_by_line) - set(v2_all_expected_lines))
    only2 = sorted(set(v2_all_expected_lines) - set(v3_by_line))
    rows.append(dict(rel=rel, flagged=flagged, v2_unflagged=sorted(v2_lines),
                     v2_expected=sorted(v2_all_expected_lines),
                     v3_expected=sorted(v3_by_line), only3=only3, only2=only2,
                     recs=v3_by_line, text=text))

out = []
for r in rows:
    if r['only3'] or r['only2']:
        out.append(r)

print('== files where the two disagree on expected-value sites ==')
for r in out:
    print('\n--- %s  flagged=%s' % (r['rel'], r['flagged']))
    for ln in r['only3']:
        for rec in r['recs'][ln]:
            print('  v3-only line %d kind=%s expected=%d scratch=%d unflagged=%d resolved=%r' % (
                ln, rec['kind'], rec['expected'], rec['scratch'], rec['unflagged'], rec['resolved'][:100]))
    for ln in r['only2']:
        print('  v2-only line %d: %s' % (ln, r['v2_expected'] and ''))
        print('    ^ line text: %s' % r['text'].splitlines()[ln-1].strip()[:140])

print('\n== totals ==')
print('files scanned:', len(rows))
print('files with only-v3 expected sites:', sum(1 for r in out if r['only3']))
print('files with only-v2 expected sites:', sum(1 for r in out if r['only2']))
json.dump([dict(rel=r['rel'], flagged=r['flagged'], only3=r['only3'], only2=r['only2'],
                v3={str(k): v for k, v in r['recs'].items()}) for r in out],
          open(os.path.join(SCR, 'diff.json'), 'w'), indent=1)
```

`inventory.py` — the full 25-file table:

```python
import importlib.util, glob, os
LANE='/home/vgpnk/Projects/shokunin/tameshi-shokunin'; SCR='/tmp/tameshi-r41-scoutv2miss-scout'
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
v2=load('wpc2',os.path.join(SCR,'write-path-census-v2.py')); v3=load('wpc3',os.path.join(SCR,'write-path-census-v3.py'))
print('%-26s %5s %6s %6s %6s %6s %6s' % ('file','flag','v2exp','v3exp','v3unf','v3nonscr_unf','sites'))
tot=[0,0,0,0]
for p in sorted(glob.glob(os.path.join(LANE,'tools','*.py'))):
    rel=os.path.relpath(p,LANE); t=open(p,encoding='utf-8',errors='replace').read()
    fl=v2.FLAG_RE.search(t) is not None
    v2e=sum(1 for ln in t.splitlines() if v2.WRITE_RE.search(ln) and v2.EXPECTED_RE.search(ln))
    r=v3.classify_source(t); e=[x for x in r if x['expected']]
    unf=[x for x in e if x['unflagged']]; ns=[x for x in unf if not x['scratch']]
    tot[0]+=v2e; tot[1]+=len(e); tot[2]+=len(unf); tot[3]+=len(ns)
    print('%-26s %5s %6d %6d %6d %6d %6d'%(rel,int(fl),v2e,len(e),len(unf),len(ns),len(r)))
print('%-26s %5s %6d %6d %6d %6d'%('TOTAL','',*tot))
```

Report: .ufo/waves/round-41/w1/ScoutV2Miss.md

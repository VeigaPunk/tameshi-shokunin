author: TameshiR19-2.Route04 (reviewer, leaf, advisory; not closure) — 2026-10-21

# Route04: an append-only correction and a predicate that can fail, for R18-4 (round 19, w1)

The axes for this item:
- correctness of the correction at the delivered revision;
- whether the predicate can fail (mutant kill);
- retention of historical bytes (no harm);
- binding between the failed row's revision and the replay's revision.

Measured revisions:
- frozen baseline `7243e7f163f08978c8fd9b6c1ef67a2fefe7d190`;
- delivered lane revision `21e79329f8bdcf01a62be63b3e46db4a7de6b6f9` (HEAD = `refs/heads/master`).

The uncommitted worktree was not measured.

## Verdict (advisory)

- **P4 (the predicate proposed below) reports R18-4 open at `7243e7f` and corrected at `21e7932`**, with all 8 clauses passing at `21e7932`. It reports 15 of 15 bad-correction mutants as open, and each mutant is caught by the clause it was built to test (observed).
- The delivered correction only adds bytes:
  - `final/checks.json` is still sha256 `fed3c8e6…5c671d` at both revisions.
  - The 16,882-byte baseline `corpus/lessons/round-18.md` is a byte prefix of the 19,046-byte delivered file.
  - The new receipts live only under `.ufo/evidence/round-19/`.
- **No further correction text is required for R18-4 to count.** One optional, exact addendum (§3) states the binding between revision `921ef80` and revision `4b7c682`, which is currently left implicit.
- The lane's committed R18-4 predicate (ruler sha256 `c538c33d…`, used for `before.json` and `after-21e7932.json`) gives the same verdict on both real revisions. By a static reading, however, it scores 12 of the 15 mutants as corrected, including overwriting `checks.json`, which the lane's own Gate rejects (§5, F1).

## 1. Defect at the baseline (observed, `git show 7243e7f:…`)

| Fact | Source | Observed |
|---|---|---|
| Failed row | `.ufo/evidence/round-18/final/checks.json:45-54` | argv `python3 tools/bash-witness-study.py --selftest`, revision `921ef807…`, `exit: 64`, `stdout_sha256: e3b0c442…b855` (empty) |
| Failed streams | `final/bash-witness-selftest.stdout` / `.stderr` | 0 bytes; 217 bytes, sha256 `6a192f7b…287d66`, ends `error: the following arguments are required: mode` |
| Real tally | `final/bash-witness.stdout` | 2,502 bytes, sha256 `316b9713…5020be`; 43 `check … ok` lines, then `WITNESS_SELFTEST: 43/43 pass`, `VERDICT: PASS`; stderr 0 bytes |
| Canonical argv | `tools/registry.json` at `921ef80` (sha256 `3e6785ee…f1e6`), row `bash-witness-selftest` | `["python3","tools/bash-witness-study.py","selftest"]`, expect exit 0, status active |
| Same-revision success already in the bundle | `final/registry.stdout`, whose sha256 `fe15a4d0…1cf4` equals `checks.json` `registry.stdout_sha256` | `rev` `921ef807…`; row `bash-witness-selftest` `expect=0 got=0 held=true`; `stdout_tail` is byte-identical to `final/bash-witness.stdout`. The same holds in `registry-branch-aligned.stdout` and `registry-success.stdout` at `5923d89` |
| Order | `git log --diff-filter=A` | `checks.json`, `bash-witness.stdout` and `registry.stdout` were all added in `5923d89` (2026-10-20T18:40:48-03:00), before routing `7243e7f` (2026-10-21T00:51:38-03:00) |
| Tool and runner bytes | `git rev-parse REV:tools/bash-witness-study.py`, `…:tools/mutate-and-run.sh`, plus sha256 | Blobs `bac63301…` (sha256 `8dfaa25a…3a12`) and `fd1a63a3…` (sha256 `d22c4025…94a8b`) are identical at `921ef80`, `5923d89`, `4b7c682`, `7243e7f` and `21e7932`. The last change was in `58e5d53` |

Verifier routing, `corpus/lessons/round-18-verifier-spotcheck.md:199-200` (committed 2026-10-21): "Do not leave a failed invocation as the selftest row of the final receipt bundle."

The contract invariant (`.ufo/evidence/round-19/contract.json:13`) reads "historical bytes retained". These two conflict if read literally. P4 settles it as follows: the failed row stays byte-identical and is explicitly superseded by a digest-bound successful receipt.

## 2. Delivered correction at `21e7932` (observed)

**Lesson erratum.** `corpus/lessons/round-18.md:135-146` is headed "Errata R18-4 / R18-5 — receipt attribution (2026-10-21, round 19)". Lines 138-139 say the row "is a failed raw invocation (`--selftest`, exit 64, empty stdout); it is **not** the effective successful selftest receipt."

**Receipt** `.ufo/evidence/round-19/bash-witness-selftest-complete.json` (sha256 `1939f9f4…9809`):
- argv `…selftest`, revision `4b7c682…`, `exit: 0`;
- stdout sha256 `316b9713…`, byte-identical to the round-18 real tally;
- stderr empty;
- `tool_sha256` `8dfaa25a…`, `runner_sha256` `d22c4025…`;
- `recorded_at` `2026-10-21T05:28:57.489251+00:00`;
- `supersedes` lists the `checks.json#bash-witness-selftest` anchor and `round-19/bash-witness-selftest.json`.

**Failed first attempt, retained.** `bash-witness-selftest.json` records exit 1. Its stdout has 36 `check` lines and no summary line. Its stderr is `FileNotFoundError … tools/mutate-and-run.sh`.

## 3. Proposed append-only correction (exact)

1. **Adopt the delivered erratum and receipts unchanged.** Do not touch any existing byte.
2. **Optional addendum, recommended.** Append at the end of `corpus/lessons/round-18.md`. The `###` level keeps it inside the `## Errata R18-4 / R18-5` section.

```
### R18-4 addendum — same-revision binding (2026-10-21, round 19)

The failed row names `921ef8077440f90d092aab4b9fdc750a45de1224`; the effective
replay names `4b7c6823a462f5ea2eafcb262275300a545f3ed7`. Both revisions hold
the same `tools/bash-witness-study.py` (sha256
`8dfaa25aa2713635e7363f60effb442a474ba3656d6cf2bb171c0c22432e3a12`) and
`tools/mutate-and-run.sh` (sha256
`d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b`). The
replay stdout (2,502 bytes, sha256
`316b97139aaa2fafa1ab08c2df6471ba8dec5b4480efa1a9589ae0341e5020be`) is
byte-identical to `.ufo/evidence/round-18/final/bash-witness.stdout` and to
the `bash-witness-selftest` row `stdout_tail` in
`.ufo/evidence/round-18/final/registry.stdout` (rev
`921ef8077440f90d092aab4b9fdc750a45de1224`, sha256
`fe15a4d046504df011b1052f4fb422109c1ee477dd3fb022936f6050a0861cf4`, equal to
checks.json `registry.stdout_sha256`), where the canonical registry argv
`python3 tools/bash-witness-study.py selftest` held with exit 0 in commit
`5923d89ac491ec3d296905561a8ab0faf3fda65a`, before this defect was routed.
The exit-64 row stays failed and byte-identical. The first round-19 scratch
lacked tracked `tools/mutate-and-run.sh` (blob
`fd1a63a3493b5a2fb2723f2fb1baae9ee7480fba` at `4b7c682`), so the receipts'
`cwd_kind: isolated scratch clone` does not describe a complete checkout; no
materialization command was recorded.
```

## 4. Predicate P4, and how it was run

It ran read-only with `git show`, `git log`, `git merge-base` and `git cat-file`. Inherited `GIT_*` variables were dropped and `GIT_CONFIG_GLOBAL=/dev/null` and `GIT_CONFIG_NOSYSTEM=1` were set. It wrote no files and executed no receipt argv or lane tool. R18-4 counts as corrected only if every clause holds; any exception counts as open.

| Clause | Requires |
|---|---|
| H1 | `checks.json` sha256 equals the baseline (`fed3c8e6…`), and the row is still argv `--selftest`, revision `921ef80`, int exit 64, empty stdout digest |
| H2 | Failed stdout empty. Failed stderr equals the baseline (`6a192f7b…`) and contains the usage text. `final/bash-witness.stdout` equals the baseline (`316b9713…`). `final/registry.stdout` sha256 equals `checks.json` `registry.stdout_sha256` |
| R1 | Strict JSON. Argv equals the canonical row in `tools/registry.json` at the receipt revision, which is 40-hex and an ancestor of the measured revision. Int exit 0. Sibling stream paths with matching digests and empty stderr. `recorded_at` carries a timezone and falls after the baseline commit time. The receipt is absent at the baseline |
| R2 | `tool_sha256` and `runner_sha256` equal the blobs at the receipt revision **and** at `921ef80` |
| R3 | `supersedes` is a list of strings containing the exact anchor `….checks.json#bash-witness-selftest`, and `historical_receipt_preserved is True` |
| R4 | The commit that introduced the receipt descends from the baseline |
| T1 | Replay stdout equals `final/bash-witness.stdout` and the registry row tail at rev `921ef80` (`got=0`, `held=true`). It consists of exactly 43 `  check … ok` lines followed by `WITNESS_SELFTEST: 43/43 pass` and `VERDICT: PASS` |
| E1 | The baseline lesson bytes are a prefix of the measured file. The appended `## Errat(um\|a) … R18-4` section names `checks.json`'s path, `bash-witness-selftest`, `exit 64`, the receipt path and `WITNESS_SELFTEST: 43/43 pass` |

Observed results:

| Snapshot | P4 | Failing clauses |
|---|---|---|
| `7243e7f` baseline | **open** | R1, R2, R3, R4, T1, E1. H1 and H2 hold, so history is intact |
| `21e7932` delivered | **corrected** | none (8/8 pass) |

### Mutants (built in memory from the `21e7932` snapshot)

The two lane-ruler columns are static readings of the ruler source, not executions.

| Mutant | P4 (observed) | Committed ruler `c538c33d` (static) | Uncommitted worktree ruler `e9b44cad…` (static) |
|---|---|---|---|
| M1: rewrite the checks row to exit 0 / green digest | open (H1) | corrected: `witness()` never reads `OLD_CHECKS` (`measure.py@21e7932:112-120`) | open (line 139) |
| M1b: add a green row to the historical `checks.json` | open (H1) | corrected | corrected |
| M2: delete `final/bash-witness-selftest.stderr` | open (H2) | corrected: file not in `PATHS` (30-34) | corrected |
| M2b: delete `final/bash-witness.stdout` | open (H2, T1) | corrected | corrected |
| M3: `tool_sha256` set to zeros | open (R2) | corrected: field never read | open (137) |
| M4: `runner_sha256` removed | open (R2) | corrected | open (138) |
| M5: one check turned to `FAIL`, summary kept, digest recomputed | open (T1) | corrected: substring tests only (117-118) | corrected |
| M6: `VERDICT: FAIL` appended, digest recomputed | open (T1) | corrected | corrected |
| M7: `supersedes` as a string containing the anchor | open (R3) | corrected: `in` on a string is a substring test (120) | corrected (141) |
| M8: vague R18-4 erratum (phrase only) | open (E1) | corrected: needs only `failed raw invocation` (118) | corrected |
| M9: pre-existing lesson line rewritten in place | open (E1) | corrected (no prefix check) | corrected for R18-4 |
| M10: receipt at `183f87b` with that revision's tool hashes | open (R2) | open (line 65) | open |
| M11: `exit: false` | open (R1) | open (66) | open |
| M12: the exit-1 first attempt used as the effective receipt | open (R1, R2, R3) | open | open |
| M13: `recorded_at` backdated to 2026-10-20T23:00-03:00 | open (R1) | corrected (no time check) | open (76-77) |

Survivors: P4 has 0 of 15. The committed ruler has 12 of 15. The worktree ruler, as observed, has 8 of 15.

### Code (three cells as run; trimmed only of comments, one docstring and cell 2's intermediate print loop — no clause or mutant changed)

```python
# cell 1 — predicate
import hashlib, json, os, re, subprocess, datetime, copy
REPO = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
BASE = '7243e7f163f08978c8fd9b6c1ef67a2fefe7d190'
DELIV = '21e79329f8bdcf01a62be63b3e46db4a7de6b6f9'
ROW_REV = '921ef8077440f90d092aab4b9fdc750a45de1224'
CHK  = '.ufo/evidence/round-18/final/checks.json'
F_SO = '.ufo/evidence/round-18/final/bash-witness-selftest.stdout'
F_SE = '.ufo/evidence/round-18/final/bash-witness-selftest.stderr'
F_BW = '.ufo/evidence/round-18/final/bash-witness.stdout'
F_REG = '.ufo/evidence/round-18/final/registry.stdout'
RJ   = '.ufo/evidence/round-19/bash-witness-selftest-complete.json'
RSO, RSE = RJ[:-5] + '.stdout', RJ[:-5] + '.stderr'
LES  = 'corpus/lessons/round-18.md'
ANCHOR = CHK + '#bash-witness-selftest'
PATHS = (CHK, F_SO, F_SE, F_BW, F_REG, RJ, RSO, RSE, LES)
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
def git(*a):
    return subprocess.run(['git', '-C', REPO, *a], env=ENV, capture_output=True, timeout=30)
def blob(rev, path):
    r = git('show', f'{rev}:{path}')
    return r.stdout if r.returncode == 0 else None
def sha(b): return hashlib.sha256(b).hexdigest()
def strict(raw):
    def uniq(pairs):
        d = {}
        for k, v in pairs:
            if k in d: raise ValueError('duplicate-key ' + k)
            d[k] = v
        return d
    def nonfinite(x): raise ValueError('nonfinite')
    return json.loads(raw, object_pairs_hook=uniq, parse_constant=nonfinite)
def is_ancestor(a, b): return git('merge-base', '--is-ancestor', a, b).returncode == 0
def snapshot(rev): return {p: blob(rev, p) for p in PATHS}
BASE_TIME = datetime.datetime.fromisoformat(git('show', '-s', '--format=%cI', BASE).stdout.decode().strip())
BASE_BYTES = {p: blob(BASE, p) for p in (CHK, F_SE, F_BW, LES)}
def p4(s, rev):
    res = {}
    def clause(name, fn):
        try: res[name] = bool(fn())
        except Exception as e: res[name] = False; res[name + ':err'] = f'{type(e).__name__}: {e}'
    def h1():
        row = strict(s[CHK])['bash-witness-selftest']
        return (sha(s[CHK]) == sha(BASE_BYTES[CHK])
                and row['argv'] == ['python3', 'tools/bash-witness-study.py', '--selftest']
                and row['revision'] == ROW_REV and type(row['exit']) is int and row['exit'] == 64
                and row['stdout_sha256'] == sha(b''))
    def h2():
        return (s[F_SO] == b'' and sha(s[F_SE]) == sha(BASE_BYTES[F_SE])
                and b'the following arguments are required: mode' in s[F_SE]
                and sha(s[F_BW]) == sha(BASE_BYTES[F_BW])
                and sha(s[F_REG]) == strict(s[CHK])['registry']['stdout_sha256'])
    def r1():
        rec = strict(s[RJ]); rv = rec['revision']
        reg = strict(blob(rv, 'tools/registry.json'))
        canon = [r['argv'] for r in reg['rows'] if r.get('name') == 'bash-witness-selftest' and r.get('status') == 'active']
        t = datetime.datetime.fromisoformat(rec['recorded_at'])
        return (isinstance(rec, dict) and re.fullmatch(r'[0-9a-f]{40}', rv) and is_ancestor(rv, rev)
                and canon == [['python3', 'tools/bash-witness-study.py', 'selftest']] and rec['argv'] == canon[0]
                and type(rec['exit']) is int and rec['exit'] == 0
                and rec['stdout'] == RSO and rec['stderr'] == RSE
                and rec['stdout_sha256'] == sha(s[RSO]) and rec['stderr_sha256'] == sha(s[RSE]) and s[RSE] == b''
                and t.tzinfo is not None and t > BASE_TIME and blob(BASE, RJ) is None)
    def r2():
        rec = strict(s[RJ]); rv = rec['revision']
        tool, runner = blob(rv, 'tools/bash-witness-study.py'), blob(rv, 'tools/mutate-and-run.sh')
        return (rec['tool_sha256'] == sha(tool) == sha(blob(ROW_REV, 'tools/bash-witness-study.py'))
                and rec['runner_sha256'] == sha(runner) == sha(blob(ROW_REV, 'tools/mutate-and-run.sh')))
    def r3():
        rec = strict(s[RJ]); sup = rec['supersedes']
        return isinstance(sup, list) and all(isinstance(x, str) for x in sup) and ANCHOR in sup \
            and rec['historical_receipt_preserved'] is True
    def t1():
        out = s[RSO]
        regrow = [r for r in strict(s[F_REG])['rows'] if r['name'] == 'bash-witness-selftest'][0]
        lines = out.decode('utf-8').split('\n')
        body = lines[:-1]
        return (out == s[F_BW] and regrow['stdout_tail'].encode() == out and regrow['got'] == 0 and regrow['held'] is True
                and strict(s[F_REG])['rev'] == ROW_REV
                and lines[-1] == '' and body[-2:] == ['WITNESS_SELFTEST: 43/43 pass', 'VERDICT: PASS']
                and len(body) == 45 and all(re.fullmatch(r'  check .+ ok', l) for l in body[:-2]))
    def e1():
        les, base = s[LES], BASE_BYTES[LES]
        if not (les.startswith(base) and len(les) > len(base)): return False
        suf = les[len(base):].decode('utf-8')
        m = re.search(r'^## Errat(?:um|a)\b[^\n]*R18-4[^\n]*$', suf, re.M)
        sec = suf[m.end():]
        nxt = re.search(r'^## ', sec, re.M)
        sec = sec[:nxt.start()] if nxt else sec
        return (all(x in sec for x in (CHK, 'bash-witness-selftest', RJ, 'WITNESS_SELFTEST: 43/43 pass'))
                and re.search(r'exit[ =:]*64\b', sec) is not None)
    for n, f in (('H1', h1), ('H2', h2), ('R1', r1), ('R2', r2), ('R3', r3), ('T1', t1), ('E1', e1)):
        clause(n, f)
    ok = all(v for k, v in res.items() if ':' not in k)
    return ('corrected' if ok else 'open'), res

# cell 2 — mutants of the delivered snapshot
D = snapshot(DELIV)
def with_rec(s, fn):
    s = dict(s); rec = strict(s[RJ]); fn(rec, s); s[RJ] = (json.dumps(rec, indent=2) + '\n').encode(); return s
def with_out(s, newout):
    s = dict(s); s[RSO] = newout
    return with_rec(s, lambda r, _s: r.__setitem__('stdout_sha256', sha(newout)))
muts = {}
def m1(s):
    s = dict(s); c = strict(s[CHK]); c['bash-witness-selftest'].update(argv=['python3','tools/bash-witness-study.py','selftest'], exit=0, stdout_sha256=sha(s[F_BW]))
    s[CHK] = (json.dumps(c, indent=2) + '\n').encode(); return s
muts['M1 launder row exit64->0'] = m1(D)
def m1b(s):
    s = dict(s); c = strict(s[CHK]); c['bash-witness-selftest-effective'] = {'argv':['python3','tools/bash-witness-study.py','selftest'],'revision':ROW_REV,'exit':0,'stdout_sha256':sha(s[F_BW])}
    s[CHK] = (json.dumps(c, indent=2) + '\n').encode(); return s
muts['M1b add green row into historical checks.json'] = m1b(D)
muts['M2 delete final/bash-witness-selftest.stderr'] = {**D, F_SE: None}
muts['M2b delete final/bash-witness.stdout'] = {**D, F_BW: None}
muts['M3 tool_sha256 wrong'] = with_rec(D, lambda r, s: r.__setitem__('tool_sha256', '0'*64))
muts['M4 runner_sha256 removed'] = with_rec(D, lambda r, s: r.pop('runner_sha256'))
fail_out = D[RSO].replace(b'  check usage error exits 64                         ok', b'  check usage error exits 64                         FAIL')
assert fail_out != D[RSO]
muts['M5 one check FAIL, summary kept'] = with_out(D, fail_out)
muts['M6 VERDICT: FAIL appended'] = with_out(D, D[RSO] + b'VERDICT: FAIL\n')
muts['M7 supersedes str superstring'] = with_rec(D, lambda r, s: r.__setitem__('supersedes', 'x' + ANCHOR + '-other'))
les = D[LES].decode(); i = les.index('## Errata R18-4 / R18-5')
vague = les[:i] + '## Errata R18-4 / R18-5 — receipt attribution (2026-10-21, round 19)\n\nR18-4: failed raw invocation, superseded.\nR18-5: does not claim the receipt existed in round 18.\n'
muts['M8 vague R18-4 erratum'] = {**D, LES: vague.encode()}
assert 'Mistakes made this round' in les[:len(BASE_BYTES[LES].decode())]
muts['M9 in-place rewrite of pre-existing lesson line'] = {**D, LES: les.replace('Mistakes made this round', 'Mistakes made in round 18', 1).encode()}
OLD = '183f87b899e6cae46be98d251cbc87fb5118f6ca'
muts['M10 receipt at pre-fix rev 183f87b'] = with_rec(D, lambda r, s: r.update(revision=OLD, tool_sha256=sha(blob(OLD,'tools/bash-witness-study.py')), runner_sha256=sha(blob(OLD,'tools/mutate-and-run.sh'))))
muts['M11 exit False (bool)'] = with_rec(D, lambda r, s: r.__setitem__('exit', False))
def m12(s):
    s = dict(s); first = blob(DELIV, '.ufo/evidence/round-19/bash-witness-selftest.json')
    s[RJ] = first; return s
muts['M12 exit-1 first attempt as effective'] = m12(D)
muts['M13 recorded_at backdated before routing'] = with_rec(D, lambda r, s: r.__setitem__('recorded_at', '2026-10-20T23:00:00-03:00'))

# cell 3 — R4 (introducing commit descends from baseline) and final evaluation
def introduced_after_base(rev):
    r = git('log', '--diff-filter=A', '--format=%H', rev, '--', RJ)
    hs = r.stdout.decode().split()
    return r.returncode == 0 and len(hs) == 1 and is_ancestor(BASE, hs[0]) and hs[0] != BASE
_p4_old = p4
def p4v(s, rev):
    st, res = _p4_old(s, rev)
    try: res['R4'] = bool(introduced_after_base(rev))
    except Exception as e: res['R4'] = False; res['R4:err'] = repr(e)
    ok = all(v for k, v in res.items() if ':' not in k)
    return ('corrected' if ok else 'open'), res
out = []
for rev in (BASE, DELIV):
    st, res = p4v(snapshot(rev), rev)
    out.append((rev[:7], st, {k: v for k, v in res.items() if ':' not in k}))
for name, s in muts.items():
    st, res = p4v(s, DELIV)
    out.append((name, st, [k for k, v in res.items() if ':' not in k and not v]))
for row in out: print(row)
print('mutants open:', sum(1 for r in out[2:] if r[1] == 'open'), '/', len(out) - 2)
# observed output: 7243e7f open (R1,R2,R3,T1,E1,R4 False; H1,H2 True); 21e7932 corrected (8/8);
# M1..M13 all 'open' with the killing clauses listed in the table; "mutants open: 15 / 15"
```

The lane ruler supports a git-free `--snapshot` mode. These pins carry P4 into it without git access (all computed from `7243e7f` blobs):

| Pin | Value |
|---|---|
| `CHECKS_SHA` | `fed3c8e6cba05c41d8fdcafc091328e3092e2018a42fb8a8594bd8b5815c671d` |
| `FAILED_STDERR_SHA` | `6a192f7b98c44ed542761b9c38d889ab41202f835385e493c596f546dc287d66` |
| `TALLY_SHA` | `316b97139aaa2fafa1ab08c2df6471ba8dec5b4480efa1a9589ae0341e5020be` (2,502 bytes) |
| `REGISTRY_STDOUT_SHA` | `fe15a4d046504df011b1052f4fb422109c1ee477dd3fb022936f6050a0861cf4` |
| `BASE_LESSON_LEN` / `BASE_LESSON_SHA` | `16882` / `107610b0499dd0178835a4f9d745df251c816bb71603e0583b3b13387a1be060`; check `digest(data[LESSON][:16882]) == BASE_LESSON_SHA` |

Proposed new negative cases for its selftest: M1b, M2, M2b, M5, M6, M7, M8 and M9.

## 5. Findings, by severity

**F1 — Medium: the committed R18-4 predicate cannot catch the corrections the Gate itself rejects.**
- Observation from source: `measure.py@21e7932:112-120` with `receipt()` at 61-76. The R18-4 predicate never reads:
  - the historical `checks.json` row;
  - the failed streams;
  - `tool_sha256` or `runner_sha256`;
  - the structure of the stdout tally.
- `supersedes` is tested with `in`, which is a substring test on a string.
- Consequence [INFERENCE, static]: 12 of 15 mutants score as corrected.
- Concrete criteria it fails:
  - `corpus/lessons/round-19.md:22` (2026-10-21) rejects "Reclassify historical failed invocations as passing or overwrite checks.json", yet M1 and M1b pass.
  - `round-19.md:52` claims "wrong argv/exit/hash/path/history-preservation cases reopen R18-4". The hash cases and real byte-level history preservation do not reopen it; only the self-asserted flag does.
  - `SKILL.md:1935` says "receipt fields agree", but the tool and runner fields are unchecked.
- The verdict at `21e7932` is still right (P4 agrees), so this is **not** a false 5/5. The gap is in durability and in how accurately the claim is calibrated.

**F2 — Medium: the ruler was not pre-registered and was being edited during my session.**
- `.ufo/evidence/round-19/measure.py` and `before.json` first appear in `21e7932`, the same commit as the corrections. `contract.json` (frozen at `78b99dd`) fixed only the population and a measurement plan.
- R18-4's phrase test `failed raw invocation` is the landed sentence word for word.
- I observed the uncommitted ruler at sha256 `1d275750…` and then `e9b44cad…`, both different from `c538c33d…`, the ruler recorded in `before.json` and `after-21e7932.json`.
- Requirement: if any ruler change lands, re-measure both `7243e7f` and the delivered revision with the identical final ruler sha. `round-19.md:59` claims "one frozen five-item ruler on both revisions".

**F3 — Low: the revision binding is left implicit.**
- The failed row names `921ef80`; the replacement names `4b7c682`.
- I verified that the tool and runner blobs are identical at both revisions, but neither the receipt nor the erratum says so.
- The worktree ruler's constants `TOOL_SHA18`/`RUNNER_SHA18` equal those blobs (verified), so it encodes the binding only implicitly. The §3 addendum closes this.

**F4 — Low: `cwd_kind: "isolated scratch clone"` is imprecise in both round-19 witness receipts.**
- `tools/mutate-and-run.sh` is tracked at `4b7c682` (blob `fd1a63a3…`), yet the first scratch did not have it (`bash-witness-selftest.stderr:14`).
- `LOG.md:1165` says "missing runner supplied only in scratch."
- No receipt field or LOG line records how the scratch was materialized (observed).
- [INFERENCE] The scratch was not a complete checkout.
- The outcome is unaffected, because the replay stdout is byte-identical to the observation made before routing.

**F5 — Info: `supersedes` changes type between the two receipts.**
- It is a string in `bash-witness-selftest.json` and a list in `-complete.json`.
- Both lane rulers accept any string that contains the anchor (M7).

**F6 — Info, positive: the correction does not depend on trusting the replay.**
- The round-18 bundle already holds a digest-bound successful run of the canonical argv at the row's own revision `921ef80`: `final/registry.stdout`, bound through `checks.json` `registry.stdout_sha256`.
- It was committed in `5923d89`, before routing.

## 6. Residual risk, verification gaps and unknowns

- **UNKNOWN:** whether the round-19 replay actually ran as recorded. Bytes cannot prove execution. A plain copy of `final/bash-witness.stdout` would satisfy P4 and both lane rulers equally. F6 limits the damage.
- **P4 is specific to this correction.** It checks this receipt path and this lesson location. A valid correction stored at a different path would read as open.
- **Discoverability.** Someone reading only `final/checks.json` still sees exit 64. P4 measures that the row is retained and superseded, not that a consumer will find the successor.
  - A text grep of `tools/`, `SKILL.md`, `corpus/` and the round-18 measure/assemble scripts found no tool that consumes `checks.json`, only prose citations.
  - That search was literal grep. No `lsp` device is available in this session, so this is not semantic proof.
- **Not measured:** the uncommitted worktree (L1 has in-flight edits to `measure.py`, LOG, SCORECARD, SKILL, QUALITY, SOURCES, the knowledge entries and the round-19 lesson) and any revision after `21e7932`.
- **The lane-ruler columns in §4 are static readings.** I ran neither `measure.py`, nor `tools/bash-witness-study.py`, nor `registry-check.py`. Reproducing them is a single `--snapshot` run per mutant; that is the falsifier's or L1's call.

## 7. Commands and side effects

- **Reads:** `git show`, `git rev-parse`, `git log` (including `--diff-filter=A`), `git cat-file -t`, `git merge-base --is-ancestor`, `git diff` (worktree, read), `sha256sum` and `wc -c` on committed evidence files, and the `python3 -` / eval-cell code above (in memory, no writes).
- **Possible side effect:** I ran `git status --porcelain` three times without `--no-optional-locks`. That may refresh the index's stat cache opportunistically. I made no content, staged-state or ref change and none was observed.
- **The only file written** is this report.
- **No tool was installed or updated.**

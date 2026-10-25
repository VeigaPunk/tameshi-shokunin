seat: SimplCounters

# Counter/integrator simplification proposal (routed to round 46, nothing applied to the lane)

Item: read `.ufo/evidence/round-45/freshness/measure.py`, `.ufo/evidence/round-45/coverage/measure.py`,
`.ufo/evidence/round-45/freshness/integrate.py`; propose (do not apply) deletions of dead code, duplicated
helpers, unused imports/branches, each verified in a `/tmp` copy with `--selftest` staying PASS.

Frozen status: round 45 counters are byte-frozen provenance. **No lane file was edited.** Originals still hash
`ba64041f49ffcf15…` (freshness/measure.py), `2f321b2c499ff432…` (coverage/measure.py),
`f65202116b35985a…` (integrate.py) after all work — identical to the copies taken at start. All experiments
ran in `/tmp/tameshi-r45-SimplCounters/` (fresh copies of the three files; the only lane writes are this report).

## Axes

- A1 dead weight removed (LOC, dead bindings, dead fields, no-op statements).
- A2 duplicated helper surface folded **without** changing any verdict.
- A3 frozen predicate preserved: selftest PASS and receipt line unchanged after every deletion.

## Deletions verified (each applied alone-in-sequence to the /tmp copy, selftest run after it)

Cumulative: 727 → 718 lines (−9). Copies: `/tmp/tameshi-r45-SimplCounters/{freshness,coverage}/`.

### D1 — `coverage/measure.py:23` `import json` (unused)
`pyflakes` on the original: `coverage/measure.py:23:1: 'json' imported but unused`; only occurrence in the file
was that import (`grep -n json` → 1 hit). After deletion:
```
C2_R45_SELFTEST: cases=10 failed=0
VERDICT: PASS
```

### D2 — `coverage/measure.py:145` `results = []` (dead binding in `selftest()`)
`pyflakes`: `coverage/measure.py:145:5: local variable 'results' is assigned to but never used`. After deletion:
```
C2_R45_SELFTEST: cases=10 failed=0
VERDICT: PASS
```

### D3 — `coverage/measure.py:30` `sys.dont_write_bytecode = True` (no-op)
It cannot suppress the counter's own `.pyc`: the cache write happens before the module body runs. Proof — the
minimal module `m.py` containing exactly `import sys` / `sys.dont_write_bytecode = True`, imported:
```
$ ls -a "$D"      →  __pycache__  m.py
```
and the pristine (flag still present) counter copy imported directly:
```
$ cp …/freshness/measure.py /tmp/…/pristine/measure.py
$ grep -n dont_write_bytecode /tmp/…/pristine/measure.py   →  55:sys.dont_write_bytecode = True
$ python3 -c "import sys; sys.path.insert(0,'/tmp/…/pristine'); import measure"
$ ls /tmp/…/pristine/      →  __pycache__  measure.py
```
The lane already carries the failure of the intent: `.ufo/evidence/round-45/freshness/__pycache__/measure.cpython-314.pyc`
(2026-10-25 16:31:26, git-ignored `!!`, 30754 B). `import sys` stays (used by `sys.exit`). After deletion:
```
C2_R45_SELFTEST: cases=10 failed=0
VERDICT: PASS
```

### D4 — `freshness/measure.py:55` `sys.dont_write_bytecode = True` (same no-op)
Same proof as D3 (the pristine-import run above is this exact file). After deletion:
```
C1_R45_SELFTEST: cases=19 failed=0
VERDICT: PASS
```

### D5 — `freshness/measure.py:89` `id=rid` field in `parse_rows()` (dead field)
No reader exists: `grep -n "\['id'\]" freshness/measure.py` returns only line 318, which indexes a **ledger entry**
(`e['id']` in `live()`), never a registry row dict. `population()` uses `r['status']`/`r['url']`; `grade()` uses
`row['source'|'scope'|'anchor'|'teaches'|'url']`. After deletion:
```
C1_R45_SELFTEST: cases=19 failed=0
VERDICT: PASS
```
(T15_population_bounds, which exercises `population()` over the parsed rows, still prints
`PASS T15_population_bounds got=['S001']`.)

### D6 — `freshness/integrate.py:18` `import sys` (unused)
`pyflakes`: `freshness/integrate.py:18:1: 'sys' imported but unused`. Beyond the linter, behaviour was checked
against a fixture (plain `/tmp` dir, no repo, so no git is touched; three fragments: holds+raw, unreachable, bad
author):
```
orig rc= 0  SKIPPED …/S003.json author 'SomeoneElse' != seat 'ExecRows01'
            INTEGRATED entries=2 {"holds": 1, "unreachable": 1} skipped=1
mod  rc= 0  (identical stdout)
ledger bytes identical: True sha 2669969fe8393d2b
snapshot gz identical: True
```

### D7 — `coverage/measure.py:197-200` dead fixture-cleanup loop in `selftest()`
```python
for p in (ea, eb):
    full = os.path.join(d, p)
    if os.path.exists(full):
        os.remove(full)
```
Unreachable today: all 10 cases in `cases` supply **both** `ea` and `eb`, and `build()` overwrites both paths
unconditionally, so `os.remove` never runs. After deletion:
```
C2_R45_SELFTEST: cases=10 failed=0
VERDICT: PASS
```
Tradeoff: the loop is a guard for a *future* case that omits one entry (a stale committed `ea`/`eb` would then be
counted by the subprocess run). Deleting it re-arms that trap; if the case table is ever extended, delete the loop
and add an `assert set(ents) == {ea, eb}` instead.

### D8 — `freshness/measure.py:221` and `coverage/measure.py:119` self-pin expression (0 LOC, 2 hashes/run removed)
```python
self_pin = int(blob is not None and hashlib.sha256(blob).digest() == hashlib.sha256(me).digest())
→
self_pin = int(blob is not None and blob == me)
```
`blob` and `me` are both bytes; byte equality is exact where the double hash only approximates it. `hashlib` stays
(snapshot hashing). After deletion:
```
C1_R45_SELFTEST: cases=19 failed=0   VERDICT: PASS
C2_R45_SELFTEST: cases=10 failed=0   VERDICT: PASS
```
The pin still discriminates: the modified copy run against a rev carrying the original bytes reports
`self_pin=0` (non-deciding scratch run, see disclosure).

## Rejected candidates (with the reason)

- `freshness/measure.py:234` and `:250` two read lambdas (`read` binary, `read_text` text): folding needs a flag or
  `functools.partial`; net LOC is 0 and one call site grows. Rejected as churn.
- `freshness/measure.py:228-231` `authors` comprehension + `counts` loop: merging is 4 lines vs 3. Rejected.
- `freshness/measure.py:355-401` selftest `ok = …; failed += not ok; print(…)` ×5: a `report()` helper saves
  ~8 lines but re-formats the `PASS Tn_…` lines that seats quote verbatim in their reports. Rejected (output
  churn on evidence lines).
- `coverage/measure.py:50-65` `class Tree` → a free `git(*args, binary=False)`: same LOC. Rejected.
- `freshness/measure.py:182-190` `wave_seats()` list-shape branch: **cannot be proven dead** — `w2-results.json`
  does not exist at any rev yet (`git show 3310e7b… / 5891bdb… / HEAD : .ufo/waves/round-45/w2-results.json` →
  `fatal: path … does not exist`). Both shapes are unexercised, not unreachable. Keep.
- `--live` mode (`freshness/measure.py:300-323`): **not dead** — a wave-2 seat ran it
  (`.ufo/waves/round-45/w2/ExecLiveSweep.md:12`). Keep.
- `--check`, `--snapdir`, `--extract`, `--member`: all exercised by round-45 seats
  (`.ufo/waves/round-45/spec-w1.json:338` `--check … --snapdir`; `:392` `--extract`/`--member`). Keep.
- `freshness/measure.py:41-53` `import io/tarfile/html/tempfile/unicodedata`: all reachable through
  `extract()` (tar member, HTML strip, entity unescape, PDF temp file, NFKC fold). Keep.

## The duplicated-helper fold: routed, with a hard precondition

Byte-level duplication between the two counters:

| helper | freshness | coverage | note |
|---|---|---|---|
| `ROW_RE` | `measure.py:63` | `measure.py:33` | identical regex |
| `URL_RE` | `measure.py:64` | `measure.py:34` | identical regex |
| registry row split (13-cell guard + first URL) | `parse_rows` `:78-92` | `gt_rows` `:67-85` | same skeleton, different retention |
| `git -C lane show rev:path` | `git()` `:71-76` | `Tree.read` `:54-59` | same call |
| self-pin block | `:219-221` | `:116-119` | identical shape (D8 applies to both) |
| `fold()` | `:100-107` | `:43-48` | **divergent** |

**The divergence is live, not theoretical.** Freshness folds NFKC and 12 characters; coverage folds 6 and no
NFKC. The frozen C2 snapshots contain the character the tables disagree on:
```
googletest-advanced.md:1097: functions for generating test parameters—see details at
googletest-testing.md:44,65: … test fixture class—see
```
(U+2014; freshness `fold` → `-`, coverage `fold` leaves `—`; `unicodedata.normalize('NFKC', …)` is identity on
all three snapshots, so NFKC is a latent-only difference.) A quote spanning U+2014 verifies under C1's convention
and fails under C2's: two normalization conventions in one round, which is exactly the "second convention"
weight this seat exists to remove.

Proposal for round 46 (r46 counters start from the folded module; r45 stays frozen):

1. One `.ufo/evidence/round-46/lib.py` holding `git(lane,*args,binary=False)`, `ROW_RE`, `URL_RE`,
   `parse_rows(text)` (full cells; the coverage filter becomes a comprehension over it), and **one** `fold()`
   (the freshness table — the superset). Estimated −17 lines and one convention instead of two.
2. **Precondition, not optional:** `self_pin` must pin the module set, not one file. Today it hashes
   `measure.py` alone (`freshness:219-221`, `coverage:116-119`); a shared lib would be *unpinned code that decides
   the verdict*, so a seat could edit `lib.py` and keep `self_pin=1`. Fold only together with
   `self_pin = int(all(show(rev,p) == open(p,'rb').read() for p in PINNED))` where `PINNED` is the explicit file
   list (counter + lib). Without that, the fold is a security regression and is refused.
3. Declare the fold pre-data: adopting the superset fold can *admit* quotes that the weaker fold refused, so the
   unified table must be frozen in the contract before any seat scores (same rule the r45 contract applies to
   amendments).
4. Never fold across rounds. Each round's counter is frozen provenance with its own copies
   (`.ufo/evidence/round-44/calibration/measure.py:122-145` has its own `git`/`show`/`sha`/`rows`); retro-folding
   would break every historical `self_pin` and is out of scope.

## Preservation evidence (whole set of deletions applied)

```
$ python3 freshness/measure.py --selftest | tail -3
PASS T19_quote_copied_from_row got=invalid (quote copied from row)
C1_R45_SELFTEST: cases=19 failed=0
VERDICT: PASS
$ python3 coverage/measure.py --selftest | tail -3
PASS T10_indented_row_counts want='rows=2' got=C2_R45: self_pin=1 rows=2 entries=2 indexed=2 row_ids=S256,S257 rev=m C2_R45_PASS=true
C2_R45_SELFTEST: cases=10 failed=0
VERDICT: PASS
$ pyflakes freshness/measure.py coverage/measure.py freshness/integrate.py ; echo rc=$?
rc=0        # originals: 3 findings (json, results, sys)
```
Helper modes still work after deletion (read-only against the lane):
```
$ python3 freshness/measure.py --check /tmp/…/S001.json --lane <lane> --rev HEAD
CHECK S001 verified ok        (rc=0)
$ python3 freshness/measure.py --extract <lane>/.ufo/evidence/round-45/coverage/sources/googletest-primer.md
# GoogleTest Primer ## Introduction: Why GoogleTest? *GoogleTest* helps you write better C++ tests. …
```

## Disclosure

One run went outside the seat's counting bounds: after D8 I ran the **scratch copy** of the C1 counter with
`--rev HEAD` (not `--selftest/--check/--extract`, not `3310e7b`/`5891bdb`) purely to show the pin still
discriminates; it printed `self_pin=0 … fresh=0 … C1_R45_PASS=false` (expected: the file differs from HEAD). It is
not the lane counter and not a deciding run; no claim number was taken from it. Every other counter invocation in
this seat was `--selftest`, `--check`, or `--extract`.

## Tooling

No installs, no upgrades. Used the already-present `pyflakes` (`/home/vgpnk/.local/bin/pyflakes`) and
`python3` 3.14.8. No pacman transaction was run.

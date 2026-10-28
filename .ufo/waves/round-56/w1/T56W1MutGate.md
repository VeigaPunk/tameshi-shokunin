# T56W1MutGate — mutation set for `tools/receipt-revision-gate.py`

Round 56 / hyaku run 11 / L1 TameshiR56 / wave 1. Leaf seat, no subagent dispatch.
Subject (frozen instrument set `c3e2ca9f0207`, lane HEAD at probe time `c3e2ca9f020776b3d66c7af854fb82c834674fcf`):

- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/receipt-revision-gate.py`
- sha256 `1d80f8a665f83508a05a33827de66ffd53c986e8de25f8f77937707cac78fbd2` (331 lines)
- blob at HEAD `c93c135758743e12bedac221ff2912e2f9bd18a5`

I did not edit the gate, any lane production file, or anything under
`.ufo/evidence/round-56/`. Every mutant is a byte-exact single edit applied to a
scratch copy, and the copy is restored to the pristine bytes after each run.

## Method (reproducible)

Scratch `$S=/fast/scratch/hyaku/tameshi-r56/T56W1MutGate`. Drivers are archived as
receipts `10-driver-mutate.py`, `10-driver-probe.py`, `10-driver-sweep.py`,
`10-driver-patch.py`.

1. `cp tools/receipt-revision-gate.py $S/gate-pristine.py`; assert
   `sha256(gate-pristine.py) == sha256(lane gate)`.
2. Baseline: `python3 $S/gate-pristine.py --selftest` → `GATE_SELFTEST: 14/14 pass`,
   exit 0 (`01-baseline-selftest.txt`).
3. For each mutant: assert the `old` string occurs **exactly once** in the source,
   apply the one replacement, run `--selftest` on the mutated copy (the selftest
   re-invokes `Path(__file__)` so it exercises the mutated code, not the lane), record
   the tally, exit and the failing case names, then rewrite the pristine bytes and
   assert the hash matches again.
4. Verdict rule: `KILLED` iff the mutant's pass count is strictly below baseline.

The selftest is hermetic for this purpose: it runs in `tempfile.TemporaryDirectory`
with `HOME=tmp`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`. Re-running
it with `GIT_DIR=/nonexistent GIT_WORK_TREE=/nonexistent` still reports `14/14 pass`.

## Required mutant set — 8/8 KILLED

Tally before, in every row: `GATE_SELFTEST: 14/14 pass` (exit 0).

| # | mutant (one exact edit) | tally after | case that failed | verdict |
|---|---|---|---|---|
| M1 | drop the `RECEIPT_REV_ABSENT` return (`if not revs:` → `if False and not revs:`) | 13/14 (exit 1) | `absent-refused` | KILLED |
| M2 | `drifted_paths` always returns `[]` | 13/14 (exit 1) | `content-drift-refused` | KILLED |
| M3 | `is_ancestor` always `True` | 13/14 (exit 1) | `control-not-ancestor-refused` | KILLED |
| M4 | skip the digest check (`if want != got:` → `if False and want != got:`) | 13/14 (exit 1) | `digest-mismatch-refused` | KILLED |
| M5 | accept multiple revs in a positive role (`if len(revs) > 1:` disabled) | 13/14 (exit 1) | `ambiguous-refused` | KILLED |
| M6 | skip the required-line check (regex guard disabled) | 13/14 (exit 1) | `required-line-refused` | KILLED |
| M7 | treat an empty file as present (`if not data.strip():` disabled) | 13/14 (exit 1) | `empty-refused` | KILLED |
| M8 | drop `RECEIPT_CONTROL_NOT_ANCESTOR` (append → `pass`) | 13/14 (exit 1) | `control-not-ancestor-refused` | KILLED |

No mutant survived. Exact edits, mutated sha256 and restored sha256 per mutant:
`02-mutants.json`; run log `02-mutate-run.log`. Every row records
`restored_exact: true`.

**Kill mechanism note (M1).** M1 is killed by the case assertion, but not by a named
refusal: with `revs` empty and the early return gone, the positive branch reaches
`full = resolved[revs[0]]` and the child dies with `IndexError: list index out of
range`, exit 1 (`08-m1-mechanism.txt`). The suite pins "not exit 3 with
`RECEIPT_REV_ABSENT`", which is the property that matters; the mutant is not
converted into a silent acceptance.

## Emission-site sweep — every real code is load-bearing (10/10 KILLED)

Disabling each `codes.append('<CODE>')` / `return ['<CODE>']` line individually, one
exact edit per run (`05-emission-site-sweep.log`, `05-sweep.json`):

| code | emission line | case that failed | verdict |
|---|---|---|---|
| `RECEIPT_MISSING` | 97 | `missing-refused` | KILLED |
| `RECEIPT_EMPTY` | 100 | `empty-refused` | KILLED |
| `RECEIPT_NOT_BLOB` | **none** | — | no site to mutate |
| `RECEIPT_REV_ABSENT` | 118 | `absent-refused` | KILLED |
| `RECEIPT_REV_UNRESOLVABLE` | 124 | `unresolvable-refused` | KILLED |
| `RECEIPT_REV_AMBIGUOUS` | 132 | `ambiguous-refused` | KILLED |
| `RECEIPT_REV_MISMATCH` | 137 | `strict-mismatch-refused` | KILLED |
| `RECEIPT_REV_CONTENT_DRIFT` | 142 | `content-drift-refused` | KILLED |
| `RECEIPT_CONTROL_NOT_ANCESTOR` | 149 | `control-not-ancestor-refused` | KILLED |
| `RECEIPT_DIGEST_MISMATCH` | 112 | `digest-mismatch-refused` | KILLED |
| `RECEIPT_REQUIRED_LINE_MISSING` | 115 | `required-line-refused` | KILLED |

Ten of eleven declared codes are 1:1 with a named selftest case, and each emission
line is load-bearing. Matrix: `09-code-case-matrix.md`.

## Coverage holes (surviving probes — report only, not contract changes)

Six further single-edit probes (`03-probes.json`, `03-probe-run.log`,
consequences in `04-consequence-demos.txt`). A survivor is a hole in the *suite*,
not permission to change the gate.

| probe | verdict | consequence measured |
|---|---|---|
| X1 CODES entry swapped for a duplicate (`NOT_BLOB` → `MISSING`) | **SURVIVED** 14/14 | `codes-closed` asserts `len(CODES) == 11` only; the tuple then has 11 entries but 10 distinct codes and no `RECEIPT_NOT_BLOB`, and the selftest still passes |
| X2 rev regex narrowed to `{40}` | KILLED (`unresolvable-refused`) | short/abbreviated rev tokens are pinned indirectly by case 7 |
| X3 JSON rev tokens dropped (`JSON_REV_RE` not consulted) | **SURVIVED** 14/14 | a `{"rev": "<sha>"}` receipt passes on the real gate (exit 0) and is refused as `RECEIPT_REV_ABSENT` by the mutant — no case exercises `JSON_REV_RE` |
| X4 unknown role accepted | **SURVIVED** 14/14 | pristine gate exits 1 with a usage error; mutant runs the receipt as a *control* and prints `verdict=PASS` |
| X5 zero `--receipt` accepted | **SURVIVED** 14/14 | pristine gate exits 1 (usage); mutant prints `GATE: receipts=0 ok=0 refused=0 codes=none verdict=PASS` and exits 0 |
| X6 unresolvable `--certified` accepted | **SURVIVED** 14/14 | pristine gate exits 2 with `codes=RECEIPT_REV_UNRESOLVABLE`; mutant crashes with `TypeError: 'NoneType' object is not subscriptable` |

### D1 — `RECEIPT_NOT_BLOB` is declared but unreachable, and a directory receipt crashes

`RECEIPT_NOT_BLOB` appears at line 26 (docstring) and line 46 (`CODES`) and nowhere
else: no emission site. Consequence on the real gate: a receipt path that is a
directory raises `IsADirectoryError`, exit 1, traceback
(`04-consequence-demos.txt`, "RECEIPT_NOT_BLOB" section) — i.e. the one input class
the code name was reserved for is answered by a crash instead of a named refusal
(exit 3). `codes-closed` cannot catch this because it counts entries, not distinct
codes or emission sites.

### D2 — the suite does not pin the CLI surface

The four usage paths (`unknown role`, `zero receipts`, `unresolvable --certified`,
non-regular-file receipt) are guarded in the implementation but have no case. Each
of X4, X5, X6 survives, so a refactor that deletes a guard is invisible to
`--selftest`. X5 is the sharpest: the gate would certify nothing and print
`verdict=PASS`.

### D3 — dead weight in the gate (report only)

- `check(..., role, required)` never reads `required`; the regex comes from the
  receipt tuple (`receipt[2]`), passed twice.
- `SELFTEST_RECEIPT_DRIFT` (line 215) is defined, is byte-identical to
  `SELFTEST_RECEIPT_OK`, and is never used.
- `RECEIPT_REV_ABSENT`'s `detail` stays `''`, so its verdict line ends in a trailing
  space (`... code=RECEIPT_REV_ABSENT `).

None of these change a verdict; they are six-month-maintenance debt in a frozen
instrument, for the L1 to schedule, not for this seat to edit.

## Proposed patch (diff, demonstrated in scratch, NOT applied)

```diff
--- a/tools/receipt-revision-gate.py
+++ b/tools/receipt-revision-gate.py
@@ def check(lane, certified, paths, receipt, role, required):
     p = Path(path)
     if not p.exists():
         return ['RECEIPT_MISSING'], 'path=%s' % path, None
+    if not p.is_file():
+        return ['RECEIPT_NOT_BLOB'], 'path=%s' % path, None
     data = p.read_bytes()
@@ def selftest():
-        # 14 the codes list is closed
-        cases.append(('codes-closed', len(CODES) == 11))
+        # 15 a non-regular-file receipt is a named refusal, not a traceback
+        r = call(str(Path(tmp)) + ':positive')
+        cases.append(('not-blob-refused',
+                      r.returncode == 3 and b'RECEIPT_NOT_BLOB' in r.stdout))
+        # 16 a JSON receipt's "rev" token is parsed
+        r = call(write_receipt('json.txt', '{"rev": "%s"}\n' % c2) + ':verdict', certified=c2)
+        cases.append(('json-rev-parsed', r.returncode == 0))
+        # 17 an unknown role is a usage error, not silently a control
+        r = call(write_receipt('role.txt', SELFTEST_RECEIPT_OK % c2) + ':bogus')
+        cases.append(('unknown-role-refused',
+                      r.returncode == 1 and b'usage:' in r.stderr))
+        # 18 zero receipts is a usage error, never a PASS
+        r = call()
+        cases.append(('zero-receipts-refused',
+                      r.returncode == 1 and b'usage:' in r.stderr))
+        # 19 an unresolvable --certified is exit 2 with a named code
+        r = call(write_receipt('ok2.txt', SELFTEST_RECEIPT_OK % c2) + ':positive',
+                 certified='deadbeefdeaddead')
+        cases.append(('unresolvable-certified-refused',
+                      r.returncode == 2 and b'RECEIPT_REV_UNRESOLVABLE' in r.stdout))
+        # 14 the codes list is closed
+        cases.append(('codes-closed', len(CODES) == len(set(CODES)) == 11))
```

### Demonstrated in scratch (never applied to the lane)

`10-driver-patch.py` builds `$S/gate-patched.py` from the pristine bytes with the
three exact edits above, then re-runs the selftest and every probe against the
patched copy (`11-patch-demo.log`, `11-patched.json`).

- patched baseline: `GATE_SELFTEST: 19/19 pass`, exit 0
- required mutants M1–M8 on the patched gate: **8/8 KILLED** (18/19, same cases as before)
- X1 → KILLED by `codes-closed`; X3 → KILLED by `json-rev-parsed`;
  X4 → KILLED by `unknown-role-refused`; X5 → KILLED by `zero-receipts-refused`;
  X6 → KILLED by `unresolvable-certified-refused`

Patched copy sha256 `387d9df0573ddc796114b185dbd2500e92c0e1d4df8c6634ce92eaf710a4272b`;
the lane gate stayed `1d80f8a6…` throughout.

**Assertion lesson (measured, first patch iteration).** My first version of cases 17
and 18 asserted only `returncode != 0 and b'verdict=PASS' not in stdout`. Against the
patched gate X4 still **SURVIVED 19/19**: with `bogus` added to the allowed roles the
receipt ran down the control branch and was refused as
`RECEIPT_CONTROL_NOT_ANCESTOR`, so "not a PASS" was satisfied for the wrong reason.
Pinning the usage path itself (`exit == 1 and b'usage:' in stderr`) killed it. Any
future case for a refusal must assert the exit code and the named code/message, never
just the absence of `PASS`.

## Supporting operability evidence (not my claim to certify)

The subject gate refuses the real receipts the lane accepted, read-only against lane
HEAD `c3e2ca9f0207` (`06-real-receipt-refusals.txt`, exit codes measured per run):

- `.ufo/evidence/round-54/control/controls-b.stdout` as `verdict` and as `control`
  → `code=RECEIPT_REV_UNRESOLVABLE rev=7df0e0426c98`, exit 3 (that revision is absent
  from this repo).
- `.ufo/evidence/round-55/after/c2.stdout` as `verdict` → `revs=none
  code=RECEIPT_REV_ABSENT`, exit 3.

I did not run the controls/deciding/no-harm dry runs, the C1/C2 counters, or the
freeze-hash verification; those belong to the executor/critic seats and I claim
nothing about them. Census: `sources-census.sh validate --root
/home/vgpnk/Projects/shokunin tameshi` → `CENSUS_EXIT=0` (with a pre-existing W04
duplicate-URL warning), `07-census.txt`.

## Restoration and non-interference

- Gate sha256 before the first mutant and after the last: both
  `1d80f8a665f83508a05a33827de66ffd53c986e8de25f8f77937707cac78fbd2`
  (`00-hashes.txt`, and `LANE_SHA_AFTER` in each driver log).
- `git -C <lane> status --porcelain -- tools/` → empty: no change to `tools/`.
- No mutating git command was run anywhere: only `rev-parse`, `diff --name-only`,
  `status --porcelain`, `merge-base --is-ancestor` inside the gate itself. No jj.
- Nothing was written under `.ufo/evidence/round-56/`; my only writes are
  `.ufo/waves/round-56/w1/T56W1MutGate.md`, `T56W1MutGate.json` and
  `T56W1MutGate-receipts/`.
- Tooling: no install or upgrade was needed; the seat ran on the host `python3`
  (3.14) and `git` as found.

## Receipts

`T56W1MutGate-receipts/`: `00-hashes.txt`, `01-baseline-selftest.txt`,
`02-mutate-run.log`, `02-mutants.json`, `03-probe-run.log`, `03-probes.json`,
`04-consequence-demos.txt`, `05-emission-site-sweep.log`, `05-sweep.json`,
`06-real-receipt-refusals.txt`, `07-census.txt`, `08-m1-mechanism.txt`,
`09-code-case-matrix.md`, `10-driver-*.py`, `11-patch-demo.log`, `11-patched.json`.

# MutFixtureVar — fixture mutation probes on `write-path-census-v3.py` selftest

Seat: `L1Tameshi41.MutFixtureVar` (read-only). Lane checkout, fleet repo, sibling lanes, jj state and
Git index were not modified; the only write outside `/tmp` is this report. No tool installs.

Contract read first: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-41/contract.json`
(C2 `tool_sha256` `095924a7…`, `fixtures_sha256` `a4123ce3…`). Neither counter was run; no deciding
run was made.

## Setup (scratch copy only)

Copies were made with `shutil.copyfile` into `tempfile.mkdtemp(prefix="tameshi-r41-mutfixturevar-")`;
the equivalent shell form is:

```
SCRATCH=/tmp/tameshi-r41-mutfixturevar-ux_07guh
cp /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/write-path-census-v3.py           $SCRATCH/
cp /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-41/census/fixtures.json $SCRATCH/
sha256sum $SCRATCH/write-path-census-v3.py $SCRATCH/fixtures.json
```

```
095924a7a165be96e69ff9dad67d3e513d23ba6737c35a0537f898482eef0279  /tmp/tameshi-r41-mutfixturevar-ux_07guh/write-path-census-v3.py
a4123ce373447563a93ad86c21cc3344f5448f1c6157ba696a7239569a58dc31  /tmp/tameshi-r41-mutfixturevar-ux_07guh/fixtures.json
```

Both equal the contract pins, so the probe starts from the pinned bytes.

## Detector (identical for pristine, mutated and restored bytes)

```
python3 /tmp/tameshi-r41-mutfixturevar-ux_07guh/write-path-census-v3.py \
        --selftest --fixtures /tmp/tameshi-r41-mutfixturevar-ux_07guh/fixtures.json
```

Pristine baseline: exit `0`, one line

```
WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=0
```

## Probe results (each applied in place, then exact bytes restored)

| # | Mutation | Fixture site | Mutated sha256 | Exit | Verdict |
|---|---|---|---|---|---|
| M1 | `"expected.json"` → `"expected.txt"` | `fixtures.json:2` (`var_unflagged`) | `4eb0dc14e824983e85cc4bbb363c83bb4d148e99ee67b3b11c388c15052133df` | `0` | **survived — uncaught** |
| M2 | `os.path.join("/tmp", "census")` → `os.path.join("census")` | `fixtures.json:5` (`scratch_var`) | `97d233a5e94961ce869a20aa0d39926e883308c71706720d3c9901337ff98057` | `1` | **killed** |
| M3 | symlink destination `"expected.json"` → `"run-1.stdout"` | `fixtures.json:3` (`symlink_unflagged`) | `31ef4b27a922768a417ac1d6ea4e3349d1a028cebbdc13a095c230de801f5267` | `0` | **survived — uncaught** |

M1 and M3 print the unchanged passing line; M2 prints

```
WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=1
FAIL planted scratch_var: want unflagged=0 got 1
```

## Diagnosis

### M1 — survived, but not a defect (mutation is non-behavior-bearing)

`expected\.txt` is a declared expected-value token in
`tools/write-path-census-v3.py:32` (`EXPECTED_RE = re.compile(r'expected\.json|expected\.txt|\.expected\b|golden|snapshot')`),
so the detector is *supposed* to keep flagging the fixture. Control mutation
`"expected.json"` → `"out.json"` in the same fixture is killed
(`want unflagged=1 got 0`, `want expected_sites=1 got 0`), so `var_unflagged` does discriminate
"expected token present" from "absent"; it does not pin *which* synonym, and C2's target
(`var_expected=1 var_unflagged=1`) does not require it to.

### M3 — survived: genuine fixture gap (destination token is masked by the directory name)

`root = "tests/golden"` at `.ufo/evidence/round-41/census/fixtures.json:3` is resolved into the
destination, and `golden` matches `EXPECTED_RE` (`tools/write-path-census-v3.py:32`). The record for
the mutated fixture is still `expected=True unflagged=True`:

```
{'lineno': 4, 'kind': 'os.symlink', 'expected': True, 'scratch': False, 'flagged': False, 'unflagged': True,
 'resolved': 'os.path.join(root, "run-1.stdout")tests/goldenroot "tests/golden"run-1.stdout"run-1.stdout"'}
```

The destination file name therefore cannot be made non-expected without also deleting `golden` from
`root`; the fixture flags on the directory, not on the planted destination token.

Concrete coverage consequence — a recognizer mutant at `tools/write-path-census-v3.py:137`,
`return 'os.symlink', [node.args[1]]` → `[node.args[0]]` (reads the *link source* instead of the
*link destination*), passes the pinned selftest:

```
python3 /tmp/tameshi-r41-mutfixturevar-ux_07guh/mutant-src-dest-swap.py \
        --selftest --fixtures /tmp/tameshi-r41-mutfixturevar-ux_07guh/fixtures.json
# mutant sha256 0073f187f0da0857b97de9a019b838ea4f3b6527b175568703c945c746050174
# exit 0
# WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=0
```

The counter's own mutant set does not close this either: `SYMLINK_MUTANT` at
`.ufo/evidence/round-41/census/measure.py:34-35` disables the whole branch
(`'os.symlink'` → `'os.symlink_DISABLED'`), which the fixture *does* kill (verified: exit `1`,
`symlink_unflagged=0`, `FAIL planted symlink_unflagged: want unflagged=1 got 0`). So
`symlink_unflagged` proves "the `os.symlink` branch exists", not "the destination argument is the one
resolved", although C2's statement is specifically about the destination.

### M2 — killed (detector behaves as the fixture asserts)

After removing `/tmp`, neither the resolved text nor the trace of the `os.replace` destination
carries a scratch marker, so the record flips to `expected=True scratch=False unflagged=True` and
the selftest fails. The `SCRATCH_MARKERS` `/tmp` entry is `tools/write-path-census-v3.py:34`; the
trace-survives-one-assignment property that makes this kill work is
`tools/write-path-census-v3.py:55-59` plus `tools/write-path-census-v3.py:165`.

## Restoration evidence

Each mutation was reverted byte-for-byte before the next probe; the restored files were re-run.

| Step | sha256 after | Equals pinned |
|---|---|---|
| after M1 restore | `a4123ce373447563a93ad86c21cc3344f5448f1c6157ba696a7239569a58dc31` | yes |
| after M2 restore | `a4123ce373447563a93ad86c21cc3344f5448f1c6157ba696a7239569a58dc31` | yes |
| after M3 restore | `a4123ce373447563a93ad86c21cc3344f5448f1c6157ba696a7239569a58dc31` | yes |
| after src/dest-swap tool mutant restore | `095924a7a165be96e69ff9dad67d3e513d23ba6737c35a0537f898482eef0279` | yes |
| final scratch selftest | exit `0`, `var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=0` | — |

Lane checkout untouched:

```
sha256sum tameshi-shokunin/tools/write-path-census-v3.py tameshi-shokunin/.ufo/evidence/round-41/census/fixtures.json
095924a7a165be96e69ff9dad67d3e513d23ba6737c35a0537f898482eef0279  .../tools/write-path-census-v3.py
a4123ce373447563a93ad86c21cc3344f5448f1c6157ba696a7239569a58dc31  .../.ufo/evidence/round-41/census/fixtures.json
git -C tameshi-shokunin status --porcelain
 M corpus/SOURCES.md
?? .ufo/evidence/round-41/sources/
?? .ufo/waves/round-41/
?? corpus/knowledge/r41-variable-destination-writes.md
```

(Those four entries are sibling seats' work; none is mine.)

## Reproduction without the scratch directory

`/tmp/tameshi-r41-mutfixturevar-ux_07guh` is a `/tmp` path, so it can be swept. Everything needed to
re-derive every number above from the pinned lane bytes is inlined here; no scratch artifact is the
sole carrier of any claim. Fresh copy:

```
S=$(mktemp -d /tmp/tameshi-r41-mutfixturevar-XXXX)
cp tameshi-shokunin/tools/write-path-census-v3.py tameshi-shokunin/.ufo/evidence/round-41/census/fixtures.json "$S"/
```

Mutation literals (single `str.replace(old, new, 1)` each, against `fixtures.json`; sha256 of the
mutated file is listed after it):

- M1 `"expected.json"` → `"expected.txt"` → `4eb0dc14e824983e85cc4bbb363c83bb4d148e99ee67b3b11c388c15052133df`
- M2 `os.path.join("/tmp", "census")` → `os.path.join("census")` → `97d233a5e94961ce869a20aa0d39926e883308c71706720d3c9901337ff98057`
- M3 `"expected.json"` → `"run-1.stdout"` in `symlink_unflagged` only → `31ef4b27a922768a417ac1d6ea4e3349d1a028cebbdc13a095c230de801f5267`
- tool mutant `return 'os.symlink', [node.args[1]]` → `return 'os.symlink', [node.args[0]]` → `0073f187f0da0857b97de9a019b838ea4f3b6527b175568703c945c746050174`
- tool mutant `    if dotted == 'os.symlink':` → `    if dotted == 'os.symlink_DISABLED':` → `63b2698aa241bcd3bf81ca6165dea30faba286db9eaced24f2c03f1bbf78dd63`

Each mutated file is run with the detector command in the first section; each mutated sha is a
byte-level check that the mutation applied where stated. Restoring `fixtures.json` to
`a4123ce373447563a93ad86c21cc3344f5448f1c6157ba696a7239569a58dc31` and the tool to
`095924a7a165be96e69ff9dad67d3e513d23ba6737c35a0537f898482eef0279` is the whole restoration.

## Finding

`.ufo/evidence/round-41/census/fixtures.json:3` — `symlink_unflagged` plants its expected-value
token twice (directory `golden` via `root`, file `expected.json` via the destination), so the
destination token is unobservable; `tools/write-path-census-v3.py:137` reads `node.args[1]`, but a
`node.args[0]` (link-source) swap survives the pinned selftest (exit `0`). This is a coverage
finding, not permission to touch the contract: `fixtures_sha256` is frozen at
`a4123ce373447563a93ad86c21cc3344f5448f1c6157ba696a7239569a58dc31` and the C2 target fields
(`symlink_unflagged=1 symlink_expected=1 mutant_symlink_killed=1`) are unaffected.

Report: .ufo/waves/round-41/w1/MutFixtureVar.md

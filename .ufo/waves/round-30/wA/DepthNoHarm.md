# DepthNoHarm — depth axis, no-harm reading of the frozen round-30 fix

Seat: leaf executor (`TameshiR30A2.DepthNoHarm-7`). No production file was edited; no git or jj write
command ran in `/home/vgpnk/Projects/shokunin/tameshi-shokunin` or in the fleet repo. All code ran in
`/fast/scratch/hyaku/tameshi-r30a2-seats/DepthNoHarm-7/` with `GIT_DIR`, `GIT_WORK_TREE` and
`GIT_INDEX_FILE` unset. The sealed set was not opened, listed or searched. Tools installed or updated:
none (stdlib `python3`, `git`, `awk`, `grep`, `diff`, `sha256sum` only).

## Verdict

**Depth holds. No harm.** Command D reads `recorded_cases=9 depth_score=9` at base
`9ed6db840dc97a0a5f4758b6b5f60cee83a61645` and `recorded_cases=9 depth_score=9` on the runner with the
frozen fix applied. The fix adds no `#   js-` ledger line and removes none: the nine ledger lines are
byte-identical at both points, and `witness/fix.diff` itself contains zero added and zero removed ledger
lines. The depth guardrail the round-18 measurer reports alongside the count (`header_legs`,
`regression_calls`, `selftest_tuples`, `lists_agree`) also stays at 9 / 9 / 9 / true.

One adjacent, measured risk is recorded below (§5): landing this fix empties the input pins that the
round-21 cold-read ledger holds on `tools/mutate-and-run.sh`, so the *calibration* no-harm monitor drops
from `covered=64/64 restraint=8 box3_mismatch=0` to `covered=33/64 restraint=6 box3_mismatch=1` at the
landed head `bb68156`. That is not the depth axis and it is not caused by the ledger lines; it is
reported because the same contract requires it to be unchanged at head.

## 1. Setup and the identity of the runner measured

```
S=/fast/scratch/hyaku/tameshi-r30a2-seats/DepthNoHarm-7
mkdir -p $S
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
  git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin $S/clone
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
  git -C $S/clone checkout -q --detach f09d3425258403a51422c9959e25340807982947
cd $S/clone && git apply /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/witness/fix.diff
```

Observed: `APPLY_OK`, `HEAD f09d3425258403a51422c9959e25340807982947`, runner sha256
`9a931bc2d0c31c32dd3a4ccf6594b56c3474628cca513b675901a8666fbec7d4`.

The applied fix is the one the round names, verified by extracting its tally block with the same anchor
the fix's own selftest uses:

```
awk '/^  local nlegs=9 npass=0 nfail=0 nsetup=0 st$/{f=1} f&&/^}$/{exit} f' tools/mutate-and-run.sh | sha256sum
e163133c0f54bb0cbd1c3f123e18b5efc17ced6df4558de034575089a8a2215d  -
```

That equals the value the task states and `contract-amendment-3.json`'s `sealed_block_sha256`
(`e163133c0f54bb0cbd1c3f123e18b5efc17ced6df4558de034575089a8a2215d`). The base revision's tally block
hashes differently, `b0e0fab5d7b56739a6d099b8cdb2c4d398293d93d0d2a298c9499a3d456b664a`, so the fix is
the file being measured and not an unpatched copy. The runner blob is identical at `9ed6db8` and at
`f09d342` (`git diff --stat 9ed6db8 f09d342 -- tools/mutate-and-run.sh` prints nothing), so the frozen
fix is the only runner difference.

## 2. Command D, both runs, verbatim

Command D is `SCORECARD.md:73` (the `# D:` line sits at 72, the command at 73):

```sh
git show "$REV:tools/mutate-and-run.sh" | python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))'
```

Run 1 — base revision, `REV=9ed6db840dc97a0a5f4758b6b5f60cee83a61645`:

```
$ git show 9ed6db840dc97a0a5f4758b6b5f60cee83a61645:tools/mutate-and-run.sh | python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))'
recorded_cases=9 depth_score=9
```

Run 2 — the runner with the frozen fix, fed by `cat` instead of `git show`:

```
$ cat tools/mutate-and-run.sh | python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))'
recorded_cases=9 depth_score=9
```

Both exit 0. As a control that `cat` and `git show` see the same bytes after the fix was committed in
this clone (`b676bf75004e0318458f1051109815f8c5857084`), `git show HEAD:tools/mutate-and-run.sh` piped
through the same program also prints `recorded_cases=9 depth_score=9`.

The contract's depth no-harm monitor is "base `recorded_cases=9 depth_score=9`; required at head: 9"
(`contract.json` `no_harm_monitors.depth`). Measured at base 9 and at the fixed runner 9.

## 3. The fix adds no ledger line and removes none

Three independent checks, all agreeing.

(a) Set difference of the ledger lines, base against fixed runner:

```
$ diff <(git show 9ed6db8...:tools/mutate-and-run.sh | grep -E '^#   (js|bash)-\S+') \
       <(cat tools/mutate-and-run.sh | grep -E '^#   (js|bash)-\S+')
LEDGER_IDENTICAL exit=0
$ echo "base=$(...| grep -cE '^#   (js|bash)-\S+') fixed=$(... | grep -cE '^#   (js|bash)-\S+')"
base=9 fixed=9
```

Empty in both directions (`comm -13` and `comm -23` each print nothing).

(b) The nine lines themselves, unchanged in text, order and line number (all at 87-95 in both files):

```
87:#   js-kimi-census        kumitate-shokunin/scripts/kimi-census.mjs   8/10 (80 %)
88:#   bash-surface-census   kagi-shokunin/corpus/surface-census.sh      8/10 (80 %)
89:#   bash-tsukuroi-census  tsukuroi-shokunin/tools/tsukuroi-census.sh  6/10 (60 %)
90:#   bash-mado-verify      mado-shokunin/tools/mado-verify.sh          4/10 (40 %)
91:#   bash-checklist-run    kagi-shokunin/corpus/checklist-run.sh       7/15 (47 %)
92:#   js-claims-check       kumitate-shokunin/scripts/claims-check.mjs  7/10 (70 %)
93:#   js-round-gate         kumitate-shokunin/scripts/round-gate.mjs    5/10 (50 %)
94:#   js-sources-check      kumitate-shokunin/scripts/sources-check.mjs 5/10 (50 %)
95:#   js-cite-check         kumitate-shokunin/scripts/cite-check.mjs    5/10 (50 %)
```

(c) The patch itself, and a looser pattern that would catch a ledger line added at any indentation:

```
$ grep -cE '^\+#   (js|bash)-' .ufo/evidence/round-30/witness/fix.diff
0
$ grep -cE '^\-#   (js|bash)-' .ufo/evidence/round-30/witness/fix.diff
0
$ grep -nE '^\s*#\s+(js|bash)-' tools/mutate-and-run.sh | wc -l
9
```

The looser scan of the whole fixed file still finds exactly the same nine lines, so the fix's added
comment lines (`  # r30: ...`) and its added selftest block do not manufacture a ledger-shaped line.

## 4. Depth guardrail, not just the count

`SCORECARD.md`'s depth rubric counts recorded ledger cases. The measurer that consumes the same header
(`.ufo/evidence/round-18/measure.py:660-697`, `LEG_RE` at `:121`) also reports whether the header, the
regression call sites and the selftest leg tuples agree. Run through
`.ufo/evidence/round-21/coldread/measure.py`:

| Revision | recorded_cases | depth_score | header_legs | regression_calls | selftest_tuples | lists_agree | unique_recorded_gates |
|---|---|---|---|---|---|---|---|
| base `9ed6db8` | 9 | 9 | 9 | 9 | 9 | true | 9 |
| frozen fix (`b676bf7`, clone-local commit) | 9 | 9 | 9 | 9 | 9 | true | 9 |
| landed head `bb68156` | 9 | 9 | 9 | 9 | 9 | true | 9 |

The fix adds a runtime tally guard and selftest vectors; it adds no regression call and no leg tuple, so
`lists_agree` stays true. The detector grew without the ruler moving: `--selftest` prints
`MUTATE_SELFTEST: 97/97 pass` at base, `101/101 pass` on the frozen fix (four new assertions: block
extracted, all-nine PASS, and the two single-status sweeps), exit 0 in both cases. The landed head, which
carries 19 further vector lines over the frozen fix, prints `106/106 pass`. That is detector depth, not
ledger depth, and command D does not count it.

## 5. Adjacent measured risk (calibration axis, not this seat's verdict)

Landing this fix changes the bytes of a file that the round-21 cold-read ledger pins as an input. In
`.ufo/evidence/round-21/coldread/ledger.json`, 222 of 393 entries carry
`inputs['tools/mutate-and-run.sh']`, and 62 of them pin the base runner's digest
`fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de` — which is the digest at both
`9ed6db8` and `f09d342`. The measurer compares the blob at the measured revision against those pins
(`.ufo/evidence/round-18/measure.py:330-350`), so after the fix those entries report
`input-drift:tools/mutate-and-run.sh` and veto credit.

Observed, same command the contract names (`python3 .ufo/evidence/round-27/c1-measure.py --repo CLONE --rev REV`):

| Revision | Covered | Restraint | box3_mismatch | depth_score | exit |
|---|---|---|---|---|---|
| base `9ed6db8` | 64/64 | 8 | 0 | 9 | 0 (matches `monitor-at-base.stdout`) |
| `f09d342` pre-fix | 64/64 | 8 | 0 | 9 | 0 |
| fix applied only (clone `b676bf7`) | 39/64 | 6 | 1 | 9 | 1 |
| landed head `bb68156` | 33/64 | 6 | 1 | 9 | 1 |

Attribution, in the same clone: at fix-only head the 25 uncovered sections are all and only sections whose
remaining clean ledger entry pins the runner; `git diff --stat f09d342 HEAD` there shows
`tools/mutate-and-run.sh` as the single changed file, and
`python3 .ufo/evidence/round-21/coldread/measure.py --repo <clone> --rev f09d342` in that same repository
still reads 64/64. At the landed head the additional losses come from the round's own corpus edits
(`corpus/SOURCES.md`, `corpus/README.md`, `corpus/QUALITY.md`, `corpus/knowledge/regression-tally-completeness.md`),
which are the sections the round intends to re-read.

So the drift is real, is measured, and is caused by editing files the ledger pins — not by any ledger
line. The depth count is unaffected either way, because it is read from the header, not from the ledger.
Smallest safe correction, for the seat that owns calibration: re-anchor the ledger pins on the new
runner (and on the new corpus files) through the round-21 refresh mechanism, or land the round's own
cold-read append that records the new digests, before the L1 asserts the calibration no-harm monitor at
head. This seat did not touch the ledger or any production file.

## 6. Observations and blockers

- The lane's landed content revision `bb68156` is a superset of the frozen witness: same tally block
  digest (`e163133c...`), one extra comment line at 134-136, and 19 extra selftest vector lines for
  two-failing, two-setup, mixed and unknown-status vectors. Command D and the ledger lines are identical
  to the frozen fix's, measured directly at `bb68156`: `recorded_cases=9 depth_score=9`, nine ledger
  lines at 87-95.
- `bb68156` was already committed on `master` when this seat measured; it is therefore the landed head
  and is reported alongside the frozen fix rather than instead of it.
- Census monitor, run read-only from the fleet root:
  `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit 0,
  `tameshi ok /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md`, with the same seven W04
  duplicate-url warnings (S047, S048, S075, S076, S077, S078, S081) as `census-start.stdout`.
- No blocker on the depth axis. The only open item is the calibration re-anchor in §5, which belongs to
  another seat.
- Processes: none of this seat's runs remain; `pgrep -f tameshi-r30a2-seats/DepthNoHarm-7` returns
  nothing. No process was killed. Every long run was wrapped in `timeout` (caps 300-900 s, observed
  wall times 6-120 s).

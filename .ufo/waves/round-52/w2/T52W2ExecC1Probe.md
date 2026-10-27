# T52W2ExecC1Probe — frozen C1 counter at CAND0 (probe, non-deciding)

Seat: executor, axis operability, milestone "C1 probe at CAND0". Nothing here decides C1; the
deciding run is the L1's. Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, base
`ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4`, CAND0 `bcba8924894216268afc4171f06eb8c28e912b46`.

**Probe verdict (data only): `total=1 C1_R52_PASS=false` (exit 1). Exactly one unit fires: the C3
counter's `tools/round21-measure.py` row, blocked by SKILL.md row grammar — not by the round-52
selftest fix, which is green.** A one-line, mechanically verified edit (below) turns the same frozen
C3 counter to `covered=30 missing=0 total=0 C3_R51_PASS=true`.

## 1. Setup and provenance

- Counter bytes: `.ufo/evidence/round-52/c1/measure.py` sha256
  `3edfdb8737c667430f5555076899851ecaa25e4b2e5ccfe4c0603ae3e0bb3ec6` (frozen round-52 C1 counter).
  Its own selftest: `python3 .ufo/evidence/round-52/c1/measure.py --selftest` → 9/9 ok, exit 0.
- Frozen C3 counter it shells out to: sha256 `a3abbd3b7888432919a999b1de357d4b71fa7262d55ae2f5ff97be4dddb3fd3a`
  at CAND0 (`.ufo/evidence/round-51/c3/measure.py`), equal to the counter's `C3_SHA`
  (`.ufo/evidence/round-52/c1/measure.py:27`) → the digest gate at `:123` passed and C3 really ran.
- Registry grader: the counter replays rows with the **BASE bytes** of `tools/registry-check.py`
  (copied from BASE, sha256 `cba16646902e89548060fd1b4b4fcb9e0ac8de1cb3fb02a347243912292944ad`), run
  `-I` against `--rev CAND0` (`.ufo/evidence/round-52/c1/measure.py:102-108`).
- Command, exactly as assigned (empty work dir required and used), wall **854.80 s**:

  ```
  S=/fast/scratch/hyaku/tameshi-r52/T52W2ExecC1Probe; mkdir -p "$S/w"
  HYAKU_SCRATCH="$S" TMPDIR="$S" python3 \
    /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-52/c1/measure.py \
    --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    --rev bcba8924894216268afc4171f06eb8c28e912b46 --work "$S/w" --explain
  ```
- `/tmp` clone the item asks about: `registry-check.py` mkdtemps its fleet mirror under `/tmp`
  (`tools/registry-check.py:766`), clone of the lane at CAND0, **280 MB observed** while running
  (`du -sh /tmp/tameshi-registry-check-twlc4a7b`), and it is removed afterwards — after the run,
  `ls -d /tmp/tameshi-registry-check-*` → count=0. `/tmp` free space never below 125 G.

## 2. Result (verbatim last line of `w2/T52W2ExecC1Probe.stdout`)

```
C1_R52: rev=bcba8924894216268afc4171f06eb8c28e912b46 held=49/49 not_held=0 dropped=0 mte_row=0 c3_covered=29 c3_total=1 r21_cases_missing=0 total=1 C1_R52_PASS=false
```

Target is `total=0`; the probe is 1 unit short, and the unit is not the round-52 registry or
selftest work.

## 3. Unit by unit

### R — registry replay (BASE registry-check.py, `--rev CAND0`)

`C1_REGISTRY_CHECK exit=0 summary=49/49 not_held=[]` (`w2/T52W2ExecC1Probe.stdout:1`;
full rows in `w2/T52W2ExecC1Probe/registry-check.stdout`). 56 rows at CAND0, 49 active; 7 rows are
`superseded` and excluded by the counter's parser
(`evidence-disposition-round17`, `-round17-before`, `-round14-superseded`,
`trace-inputs-round17-selftest`, `command-binding-selftest`, `command-binding-frozen-clean`,
`command-binding-source-read-red`). **Rows not held: none.**

Relevant held rows, quoted: `ROW mte-interop-check expect=0 got=0 held`,
`ROW round21-measure-selftest expect=0 got=0 held`,
`ROW mutate-and-run-regression expect=0 got=0 held`.

### D — dropped active rows

`C1_DROPPED none`. CAND0 `tools/registry.json` has 56 rows, 49 active, and
`.ufo/evidence/round-52/c1/base-active.json` lists 49 — set difference empty
(command shown: `git -C LANE show CAND0:tools/registry.json` + the counter's own D clause).

### M — mte row leg count

`C1_MTE_ROW ok legs=10 want='MTE_INTEROP: PASS legs_conforming=10/10' status=active needles=['MTE_INTEROP: PASS legs_conforming=10/10']`.
Three texts agree at CAND0: `tools/mte-interop.py:74` `LEG_TABLE = {…}` has 10 legs;
`tools/registry.json:1011-1017` expects `10/10`; `SKILL.md:2136` says "not equal to the **ten**
ledger legs" and "`mte-interop-check` (10/10)". BASE read `9/9`, so the row is the repair the
contract's C1 M-clause asks for.

### G — round-21 self-test case literals

`C1_R21_CASES missing=none` — all 11 case literals of
`.ufo/evidence/round-52/c1/measure.py:31-33` are present in `tools/round21-measure.py` at CAND0
(`git -C LANE show CAND0:tools/round21-measure.py`).

### C — round-51 C3 counter: the single MISSING line

```
C1_C3_TOOL tools/round21-measure.py: MISSING (line 2157 selftest-cell-commands=3)
C3_R51: rev=bcba8924894216268afc4171f06eb8c28e912b46 tools=30 rows=32 covered=29 missing=1 deleted=0 selftest_fail_rows=1 total=1 C3_R51_PASS=false
```
(`w2/T52W2ExecC1Probe.stdout:19-20`, `w2/T52W2ExecC1Probe/c3.stdout:last`.) All other 29 tools are
covered with their selftests exit 0 (lines quoted in `c3.stdout`).

**Cause — row grammar, not behaviour.** The frozen predicate accepts exactly one backticked span in
a 8-cell row's Self-test cell (`.ufo/evidence/round-51/c3/measure.py:125-127`:
`cmds = re.findall(r'`([^`]*)`', st)`; `if len(cmds) != 1: return 'selftest-cell-commands=%d'`).
At CAND0, `SKILL.md:2157` (the `round21 measure facade` row inside `#### Gate/probe registry — round 51`,
heading at `SKILL.md:2138`) carries **3** spans:

```
['python3 tools/round21-measure.py --selftest', 'c2-count.py', 'FLEET']
```

shown by, e.g.

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show bcba8924:SKILL.md | sed -n 2157p \
 | python3 -c 'import sys,re;c=[x.strip() for x in sys.stdin.read().strip().strip("|").split("|")];print(len(re.findall(r"`([^`]*)`",c[4])),re.findall(r"`([^`]*)`",c[4]))'
```

The two extra spans are the prose the round-52 fix added to that cell ("… its subject `c2-count.py`
names in `FLEET` …"), i.e. the sentence that declares the selftest fleet-bound. That sentence is
correct; its markdown is what the frozen grader refuses. Verified lineage: `git -C LANE blame
-L 2157,2157 bcba8924 -- SKILL.md` → `bcba892` (the CAND0 content commit), and no wave-1 correction
record covers this row (`grep -l fleet-bound .ufo/waves/round-52/w1/T52W1Corr*.json` → nothing).

**Why BASE failed the same row for a different reason** (so the round-52 change is a real repair):
BASE `SKILL.md:2157` had exactly 1 span, and its selftest was red in a fresh clone. Reproduced:
`git clone -q --shared LANE C && git -C C checkout -q --detach ef19d8e1` then
`python3 tools/round21-measure.py --selftest` → **exit 1**, traceback
`CalledProcessError … '…/c3repro/kumitate-shokunin' … show 175de6ba…:scripts/kimi-census.mjs`
(receipt `w2/T52W2ExecC1Probe/r21-selftest-clone-BASE.stdout`) — the `ROOT.parent` sibling read the
contract's C1 `sourced` row calls out. At CAND0 the same selftest in the same kind of shared clone is
**exit 0, `ROUND21_MEASURE_SELFTEST: 13/13 pass`**
(`w2/T52W2ExecC1Probe/round21-selftest-C3clone.stdout`; the new code reads the `FLEET` literal at
`tools/round21-measure.py:77`, and `.ufo/evidence/round-21/c2-count.py:19` has
`FLEET = Path("/home/vgpnk/Projects/shokunin")`). So the fleet-bound fix works; only the row's
backtick count still blocks the credit.

## 4. Drafted fix (applied to a scratch copy, graded by the frozen C3 counter)

Minimal edit — in the **Self-test cell only** of `SKILL.md:2157`, drop two backticks
(`c2-count.py`, `FLEET`), keeping the command span and every other cell byte-identical:

```
-`c2-count.py` names in `FLEET`,        (inside the Self-test cell of the round21 row)
+c2-count.py names in FLEET,
```

Deliverable: `w2/T52W2ExecC1Probe/T52W2ExecC1Probe.diff` (against CAND0 `SKILL.md`, one line changed;
`git apply --check` → ok, `git diff --stat` → `SKILL.md | 2 +-`).

No declaration is lost by dropping those backticks: the prose stays, and a sibling draft has already
put the same fact in the round-21 section — `w2/T52W2Fix07-section.diff` adds "the c2 fixture is
fleet-bound, not isolated: it reads sibling blobs at the fleet root" at `SKILL.md:1969-1970`
(verified: `sed -n '1968,1971p' SKILL.md` at CAND0 reads "…public isolated fixture selftests
without…"). The two edits are compatible; neither touches the other's line.

Evidence, in two steps:

1. Through the frozen C3 grader's own functions (`row_reason` + `run_row` on
   `.ufo/evidence/round-51/c3/measure.py`), the patched row gives
   `ROW line 2157 row_reason= None`, `RUN_ROW reason= None last_line= ROUND21_MEASURE_SELFTEST: 13/13 pass`;
   spans 3 → 1 and the Write-scope cell untouched (still 4 backticks)
   (`w2/T52W2ExecC1Probe/minimal-fix.stdout`).
2. Full frozen C3 counter at a scratch clone whose only change is that line (fixture commit
   `bbdf7900e875846fea57ec716a1012a4ca6089f1`, CAND0 + the patch):

   ```
   C3_R51: rev=bbdf7900… tools=30 rows=32 covered=30 missing=0 deleted=0 selftest_fail_rows=1 total=0 C3_R51_PASS=true   (exit 0)
   ```
   (`w2/T52W2ExecC1Probe/c3-patched-row.stdout`.)

Projection for the deciding run: R=0, D=0, M=0, G=0 are measured at CAND0 and C→0 is measured on the
patch, so `total=0 C1_R52_PASS=true` at CAND0 + this one-line edit. **The combined figure is
`[INFERENCE]`** (I did not rerun the whole C1 counter on a patched fixture: its registry-replay
unit needs the live fleet mirror, which a scratch clone cannot supply faithfully).

## 5. Rows not held — the item's two asks

1. registry-replay rows not held at CAND0: **none** (`held=49/49`, 7 superseded rows excluded).
2. C3 `MISSING` lines: **exactly one**, `tools/round21-measure.py`, cause
   `selftest-cell-commands=3` at `SKILL.md:2157` (§3.C). No `DELETED` lines (`deleted=0`).

## 6. Secondary observations (not claim units)

- `selftest_fail_rows=1` in both C3 runs is the stale round-12 duplicate row `SKILL.md:1504`
  (`python3 tools/bash-witness-study.py selftest`, missing `--`): it runs, exits 0, prints
  `VERDICT: PASS`, and the finding-id token `VERDICT:` is not in that cell, so the row fails; the tool
  is still covered by `SKILL.md:2142`, so the total is unaffected
  (`w2/T52W2ExecC1Probe/bw-selftest.stdout`; `C3_TOOL tools/bash-witness-study.py: covered line 2142`).
  Noise, not operability debt — but it is why that counter reads 1, and worth a later cleanup.
- The `round21-measure-selftest` registry row is now **host-bound**: its selftest reads the absolute
  `FLEET` path (`.ufo/evidence/round-21/c2-count.py:19`), so it is "held" only on a host that has
  `/home/vgpnk/Projects/shokunin/kumitate-shokunin`. `tools/registry-check.py:632`
  (`_argv_outside_fleet`) inspects argv only, so nothing in the gate flags it. This is declared
  (SKILL.md:2157 prose, contract C1 `sourced`) and did not cost the probe anything — measured held —
  but it moves a fleet-shaped dependency into a row that used to be a plain selftest.
- `mte-interop-check` is likewise non-hermetic at runtime (it replays live sibling object stores) and
  the standalone re-run reflects it: 285 s wall, `ROW mte-interop-check expect=0 got=0 held` /
  `REGISTRY_CHECK: held=1/1 superseded=0`, **exit 0**
  (`w2/T52W2ExecC1Probe/registry-check-only-mte.stdout`, produced by
  `python3 tools/registry-check.py --root /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev bcba8924… --only mte-interop-check`).
- Editing any of the 30 registry rows' Self-test cells must keep exactly one backticked span; prose
  added there must be backtick-free. That is the constraint the round-52 fix violated (§4).

## 7. Risks and blockers

- **Non-deciding probe.** Nothing here is a verdict. If the L1 does not land the §4 edit, the deciding
  run should print `total=1` again (C3 clause) and C1 is an honest false.
- If the §4 edit is landed, re-verify the row's cell after the edit with the two-span check in §3.C
  before the deciding run; any additional backticked prose in that cell re-blocks the credit.
- Host dependence (§6) means a deciding run on a host without the fleet root would grade the
  `round21-measure-selftest` registry row and the C3 `round21-measure` row red for environmental
  reasons; the contract already accepts this (C1 `sourced`), it is not new, but it is the one way this
  claim can look red without a code regression.
- No blockers hit. No installs or upgrades were made (nothing was needed); pacman was not touched.

## 8. Evidence index (all under `.ufo/waves/round-52/w2/`)

| file | sha256 |
|---|---|
| `T52W2ExecC1Probe.stdout` (counter stdout+explain) | `73baabd1eb9ce2f7804beed5d50cfd9e6d2079e35c6a9e6c49125afb91674231` |
| `T52W2ExecC1Probe/registry-check.stdout` (49 rows) | `a2294843a548f3357185d2855557419f63ab342b1bb65a8cb4e913b0478a56a7` |
| `T52W2ExecC1Probe/c3.stdout` (CAND0, 29/30) | `05dde0bdb70ea91ca41500e79d7ba921d0a24e46e6e1a9bf913a8afe4408d767` |
| `T52W2ExecC1Probe/c3-patched-row.stdout` (30/30, total=0) | `431199eebf87cfc17053b3c7aacbe0d0799b2e9949507c8f1862b65f04060730` |
| `T52W2ExecC1Probe/registry-check-only-mte.stdout` | `41f07fcd4342210a7a4f32e98c8b64181b6259cfef97e795d4e1da58c493d5b2` |
| `T52W2ExecC1Probe/round21-selftest-C3clone.stdout` (CAND0) | `d42bfbd9f50991e0f24c9b33ac5c16ff23e984ee7fc11e97b7547cd477fa6173` |
| `T52W2ExecC1Probe/r21-selftest-clone-BASE.stdout` (BASE red) | `814517b5b4e726d80a0de83160d53bd0fbf6e419f6f12cdc2c1a602e24c62b94` |
| `T52W2ExecC1Probe/minimal-fix.stdout` | `2823505135df8bf6f40f25ffbec53ae88527ebaace82fe10d7f295737c9d45a9` |
| `T52W2ExecC1Probe/bw-selftest.stdout` | `1755081d09ccdb98f4dbb2627883cc9b2ab0f58c833663ca293acb7873ddbdf1` |
| `T52W2ExecC1Probe/T52W2ExecC1Probe.diff` (candidate row edit) | `6487ae3381e52a33ac5d3a1ee17ea83795e3c9133948c92f147373c605abf6ef` |

Scratch root `/fast/scratch/hyaku/tameshi-r52/T52W2ExecC1Probe` (one shared clone at a time, both
fixture commits and both clones inside it) is deleted before this seat returns; no `/tmp` or scratch
path is cited as evidence above.

## Summary

- Frozen C1 counter at CAND0: `held=49/49 not_held=0 dropped=0 mte_row=0 c3_covered=29 c3_total=1
  r21_cases_missing=0 total=1 C1_R52_PASS=false`, exit 1, wall 854.80 s (probe, non-deciding).
- Every registry-replay row is held under the BASE grader (49/49; 7 superseded excluded); the mte row
  expects and gets `legs_conforming=10/10` against a 10-leg `LEG_TABLE`; the 11 round-21 case literals
  are intact; no active row was dropped.
- The single unit is C3: `tools/round21-measure.py: MISSING (line 2157 selftest-cell-commands=3)` —
  the round-52 sentence that declares the selftest fleet-bound added two backticks to the Self-test
  cell, and the frozen grader allows exactly one backticked span there.
- The declared behaviour is fine: the round-21 selftest exits 0 with 13/13 in a fresh shared clone at
  CAND0 (it was exit 1 with a sibling traceback at BASE, reproduced).
- Drafted fix: strip those two backticks in the Self-test cell only; the frozen C3 counter on a
  patched fixture prints `covered=30 missing=0 total=0 C3_R51_PASS=true`, and the diff applies cleanly.
- Time-dependent: C1's total is `[INFERENCE]` 0 only if that one-line edit lands; otherwise the
  deciding run should honestly read 1.
- No installs; no lane bytes written outside `w2/`; no mutating git command anywhere.

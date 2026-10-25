# ScribeQuality — round-43 wave 1: QUALITY criteria 83 and 84 (draft)

Seat: `L1Tameshi43.ScribeQuality` (scribe, leaf). Item: draft two criteria for
`corpus/QUALITY.md` in this report; do not edit the file.

Everything below is read-only against the lane. No tool was installed (pacman paused
host-wide); work used `python3 3.14.8`, `git show/status/diff --numstat` (read-only),
`grep`/`sed`/`awk`. Scratch lived in `/tmp/tameshi-r43-ScribeQuality-*`, `/tmp/r43-*`
and was deleted on return.

Report written at the lane path
`.ufo/waves/round-43/w1/ScribeQuality.md`.

**Supersedes the snapshot of this file at HEAD `c5335c7`** (405 lines, committed with the
wave-1 seat reports). That snapshot was current when `A5` was the last amendment; it says
SQ-1 is an open blocker, quotes pins only at the freeze, and calls criteria 83/84
uncommitted. All three were overtaken by later commits: `A9` (`273c047`) gave the probe
the reachability gate, and `c5335c7` landed the criteria, the lesson and the knowledge
file. This working-tree version is the corrected report: `A5` closed SQ-1, `A9`
closed the probe's kill half, the criteria are landed, and the surviving finding is SQ-5
(the probe's missing equivalence path). Nothing in the superseded snapshot's
measurements was wrong at the rev it measured; the conclusions moved with the lane.

## 0. State read before drafting

- Freeze `17f6ef0c72ec27e1aea305b5c95806b43bb2caef`; base `487b8f0d…`. Contract read:
  `.ufo/evidence/round-43/contract.json`.
- Counter pins verify against the files on disk, measured three times as the lane moved
  under this seat (`17f6ef0c` → `114ffacd` → `c5335c7`), all 5/5 `match=True` from a
  `python3` compare over `claims.*.counter_sha256` + `frozen_tools`:
  - `17f6ef0c` (freeze): C1 `ad7ecf8c…bc875`, C2 `092c76cd…8f286`, C3 `6278edcd…78601`,
    census tool `784de4c0…22fe5`, guard `8140945a…f762`.
  - `114ffacd` (`A1`–`A7`): C1 `901d947f…cc7e0`, C2 `52961c37…fdf`, C3 `8c8147e7…ff9b`,
    census tool unchanged, guard `365bf958…0c2`.
  - `c5335c7` (`A1`–`A9`, HEAD at this write): C1 `0d0f81bd…7f1`, C2 `52961c37…fdf`, C3
    `ae66342d…05a`, census tool unchanged, guard `e219007f…487`.
  The amendments that matter here are `A5` (C1 measurement-path reachability gate) and `A9`
  (C1 `--probe-mutant` applies the same gate; §2/§4).
- **`corpus/QUALITY.md` changed under me while I worked, and is now committed.** My first
  read was 1047 lines (round-42 block ending with criterion 82). A later read is 1105 lines:
  `git diff --numstat corpus/QUALITY.md` → `58 0` (pure append) while it was uncommitted.
  The appended block is **criteria 83 and 84, drafted by another seat** (`corpus/QUALITY.md:1049`
  and `:1083`). At HEAD `c5335c7` that block is **landed**: `git show HEAD:corpus/QUALITY.md
  | wc -l` → 1105, `grep -c "Criterion 8[34]"` → 2, and `git diff HEAD --stat
  corpus/QUALITY.md` is empty. At the freeze rev it is absent (`git show
  17f6ef0c:corpus/QUALITY.md | wc -l` → 1047; `grep -c` → 0). This report therefore
  delivers (a) my independent drafts and (b) a measured reconciliation; because the extant
  blocks are landed, any correction to them is an **appended dated erratum** under criterion
  35, not an in-place rewrite — the L1 owns that call. I edited nothing.

## 1. The two nearest existing criteria, quoted (the shape model)

`corpus/QUALITY.md:1001` and `:1023`, both under
`## Criteria appended — round 42 (2026-10-25)`:

> ### Criterion 81 — a presence receipt is written after the writes it describes, or superseded
>
> A committed receipt that asserts a file's presence or absence (`present`, `report_exists`)
> is a self-assessment record. It is written after the last write it describes. When the
> tree later contradicts it, the fix is an appended superseding receipt. That receipt names
> the old one in `supersedes`, re-asserts every path the old one asserted, and agrees with
> the tree on each. It is not an in-place rewrite of closed-round evidence. A receipt that
> the tree contradicts and that nothing supersedes is a calibration mismatch, whatever
> the round report says about it.
> Lesson: `corpus/lessons/round-42.md`. The live instance was the round-41 residual
> receipt: `present: false` for `ResidualReceipts.md`, written before that report landed.
> The round-42 C1 counter's m10 class audits `present` assertions under `.ufo/waves/`. Its
> known limits are recorded in the lesson: it reads presence by path only, so an empty file
> satisfies it, and it does not read other key names such as `report_exists`.
> Falsifier that must fail (from the lane; prints `C1_R42_PASS=false` and exits 1 at the
> base, where the stale receipt is not yet superseded):
>
> ```
> python3 .ufo/evidence/round-42/calibration/measure.py --lane LANE \
>   --rev c77c2b7e64d2e356381441ecf94abac03e984606 --freeze 322b5cd32b4319a05340d249ae752d12a9e6b19f
> ```

> ### Criterion 82 — a kill is a completed run with a failed check; a crash is not a kill
>
> When the lane mutates its own tools, a mutant counts as killed only when the run finishes
> with parseable output and at least one declared check fails. A non-zero exit, a Traceback
> or unparseable output is a run error and does not count as a kill. A run with no failing
> check is a survivor. This is the lane's own verdict rule (`SKILL.md:208-209`: a crash
> before the summary is Inconclusive, not a kill) and Stryker's (S001: Runtime error "is not
> represented in your mutation score"). PIT differs: its code scores `RUN_ERROR` as detected
> (S158, `corpus/knowledge/pit-outcome-vocabulary.md`). A kill oracle that cites a tool must
> cite the tool whose rule it actually follows, and a kill count must say which oracle
> produced it.
> Lesson: `corpus/lessons/round-42.md`. The round-42 contract's first wording cited PIT
> and Stryker together for this rule. A wave-1 critic opened PIT's source and found the PIT
> half false. The citation is corrected in the contract's post-freeze amendments; the
> pinned counter bytes are not edited.
> Falsifier that must fail (from the lane; a tool that crashes on every input must print
> `probe_outcome=runtime_error`, never `killed`; the probe file is the wave-1 executor's,
> re-created by the command):
>
> ```
> printf 'raise SystemExit("crash")\n' > /tmp/crash-probe.py
> python3 .ufo/evidence/round-42/census/measure.py --lane LANE \
>   --rev 322b5cd32b4319a05340d249ae752d12a9e6b19f --freeze 322b5cd32b4319a05340d249ae752d12a9e6b19f \
>   --probe-mutant /tmp/crash-probe.py
> ```

Shape to match: `### Criterion NN — <declarative title>`; 1–3 paragraphs of rule with the
failure mode named; `Lesson:` naming a lesson file and the live instance; then
`Falsifier that must fail (from the lane; <what it prints>):` and a fenced command.
Both falsifiers are commands, both name a measured state where the command exits non-zero.

These are the two nearest criteria at the numbering boundary my items occupy: 81 and 82 are
the last blocks before the numbers 83/84, and both are round-42 mutation/record semantics
like my drafts. The blocks that actually carry 83/84 landed while I worked and are quoted in
§5, where they are compared clause by clause.

## 2. Draft criterion 83

### Criterion 83 — a survivor is classified by a differential probe and a structural argument, never relabelled

A mutant that survives the declared kill battery carries exactly one recorded verdict —
`killed`, `dead_code_only`, `equivalent` or `unresolved` — and that verdict comes from two
checks, not from the label the battery happens to print:

- a **differential probe**: the mutant's per-site fingerprint over the whole declared
  fixture corpus, compared with the pristine tool, and its differing cases printed;
- a **structural argument**: a differing fixture is unreachable-only only when a parser
  finds a statement after an unconditional `return`/`raise` in the same block of that
  fixture's source.

`equivalent` requires an empty difference set. `dead_code_only` requires every differing
case to be unreachable-only, and the verdict names the case. A difference on a reachable
fixture after a battery pass is `unresolved`, never `equivalent`. A battery failure
produced only by an unreachable-only fixture is not a kill: `killed` requires a
reachable-input failing case. `survived` / `outcome=` is not a verdict vocabulary — it
collapses "equivalent" and "not yet classified", which is how the round-42 survivor set
stood unresolved for a round.

Lesson: `corpus/lessons/round-42.md:215-220` records the two survivors and states the
classification for this one ("differs only on dead code") from a probe, not from a battery
label. Live instance, measured this wave in three states (the lane moved twice while the
seat ran):

- **Freeze bytes `ad7ecf8c…` (`17f6ef0c`).** The counter labels `method_fold_several_returns`
  **`killed`** from `F12_method_two_returns expected=1 want 0` although F12 is the declared
  unreachable fixture (`.ufo/evidence/round-43/mutants/measure.py:230,242` at that rev):
  the mutant loop treated any battery FAIL as a kill, so the `dead_code_only` branch could
  never run for it (`len(killed)=6`, `len(dead_code_only)=0`). This is the exact symptom
  `contract.json amendments[A5].why` records, and it is a verdict decided by the fixture's
  declared expectation, not by the construct's reachability.
- **HEAD `114ffacd` (`A5`).** The mutant loop now gates on the rule: `reachable_fails =
  [case for case in mdetail if not mdetail[case]]`, `if mf and reachable_fails: killed`
  (`.ufo/evidence/round-43/mutants/measure.py:559-560`), and the same run classifies the
  mutant `dead_code_only ['F12_method_two_returns']` with five killed. The measurement path
  now satisfies this criterion. **The control path does not**: `--probe-mutant` still
  computes `verdict = ('killed' if not errors and fails else 'runtime_error' if errors else
  'survived')` (`:507-513`) with no reachability gate and no differential, so it names the
  dead-code mutant `killed` and a byte-identical copy `survived`. The two labels the rule
  distinguishes are exactly the two the probe could not produce at that rev.
- **HEAD `c5335c7` (`A9`).** The probe inherits the same reachability gate
  (`measure.py:510-518`, `reachable` from `battery()`'s per-fixture map), and the dead-code
  mutant now prints `verdict=dead_code_only`. The equivalence half is still absent: a mutant
  that never fails the battery falls to the `else` branch (`:519-520`) and prints
  `verdict=survived`, with no `differential()` call anywhere in the probe block. That is the
  clause no landed amendment satisfies yet.

Falsifier that must fail (from the lane; the counter's own `--probe-mutant` path must name
the dead-code survivor `dead_code_only` and a byte-identical copy `equivalent`. At
`c5335c7` the first pipeline passes and the second prints `verdict=survived`, so the
falsifier still exits 1; at `17f6ef0c` and `114ffacd` both pipelines exited 1):

```
git -C LANE show c5335c7:tools/write-path-census-v4.py > /tmp/r43-pristine.py
python3 - <<'PY'
import json, pathlib
src = pathlib.Path('/tmp/r43-pristine.py').read_text()
mut = [m for m in json.loads(pathlib.Path('LANE/.ufo/evidence/round-42/census/mutants.json').read_text())['mutants'] if m['name'] == 'method_fold_several_returns'][0]
assert src.count(mut['find']) == 1
pathlib.Path('/tmp/r43-dead.py').write_text(src.replace(mut['find'], mut['replace']))
PY
python3 .ufo/evidence/round-43/mutants/measure.py --lane LANE \
  --rev c5335c70bff750218b3a6db0a92daae76509a0de --freeze c5335c70bff750218b3a6db0a92daae76509a0de \
  --probe-mutant /tmp/r43-dead.py | grep -q 'verdict=dead_code_only'
python3 .ufo/evidence/round-43/mutants/measure.py --lane LANE \
  --rev c5335c70bff750218b3a6db0a92daae76509a0de --freeze c5335c70bff750218b3a6db0a92daae76509a0de \
  --probe-mutant /tmp/r43-pristine.py | grep -q 'verdict=equivalent'
```

Measured, both probes, allowed control mode `--probe-mutant` only, at all three counter
pins this seat saw:

```
--- 17f6ef0c (counter ad7ecf8c), identical copy:
C1_R43_PROBE: verdict=survived failures=0 errors=0 first=[]
--- 17f6ef0c (counter ad7ecf8c), method_fold_several_returns applied:
C1_R43_PROBE: verdict=killed failures=1 errors=0 first=['F12_method_two_returns expected=1 want 0']
--- 114ffacd (counter 901d947f), identical copy:
C1_R43_PROBE: verdict=survived failures=0 errors=0 first=[]
--- 114ffacd (counter 901d947f), method_fold_several_returns applied:
C1_R43_PROBE: verdict=killed failures=1 errors=0 first=['F12_method_two_returns expected=1 want 0']
--- c5335c7 (counter 0d0f81bd), identical copy:
C1_R43_PROBE: verdict=survived failures=0 reachable_failures=0 errors=0 first=[]
--- c5335c7 (counter 0d0f81bd), method_fold_several_returns applied:
C1_R43_PROBE: verdict=dead_code_only failures=1 reachable_failures=0 errors=0 first=['F12_method_two_returns expected=1 want 0']
```

So the verdict vocabulary the criterion requires is now half-present: `A9` teaches the probe
the reachability split (`c5335c7`, `:510-518`), and the dead-code survivor is named
correctly. The equivalence half is still missing — a mutant the battery cannot distinguish
from the pristine tool is called `survived`, not `equivalent`, because the probe never runs
`differential()`. The falsifier therefore still exits 1, at its second pipeline. `survived`
is the label the criterion bans precisely because it reads identically for "equivalent" and
"not yet classified".

Why this wording and not "the label matches the contract": the round's own target
(`contract.json claims.C1.target`: `mutants_killed=5 dead_code_only=1 … dead_code_arg_ok=1`)
is a *consequence* of the rule, not the rule. A criterion that restates the target would be
true by construction of the counter and would not survive the counter being wrong — which
is exactly the state measured in §4.

## 3. Draft criterion 84

### Criterion 84 — a self-assessment counting command uses the pattern the registry's census accepts

Every command the lane prints as the derivation of its own number — a "re-derivable
command" cell in `SCORECARD.md`, a row count in `LOG.md`, a report's "N rows" — must count
its registry with the pattern the registry's own census accepts. The census of
`corpus/SOURCES.md` accepts a row with 0–3 leading spaces, so `^\| S[0-9]{3} \|` is
strictly narrower than the census and under-counts any row the census calls valid. The
command is load-bearing only if it is run on an indented-row mirror: one census-valid row
indented two spaces must leave the census-valid count unchanged and reduce a column-zero
count by exactly one. A command that is quoted but never run on such a mirror is prose, not
a derivation; a count that disagrees with the census while the census passes is the lane
reporting a number it cannot defend.

Lesson: `corpus/lessons/round-42.md:113-119` — the round-42 guard proof is the same shape:
on a scratch registry with one row indented two spaces the 0–3-space extractor reports
three collisions and the column-zero one reports two. Live instance at `17f6ef0c`: the
newest standing `| sources-registry |` row (`SCORECARD.md:2020`) records
`grep -cE '^\| S[0-9]{3} \|' corpus/SOURCES.md` → 113 rows; on a one-row-indented mirror
that pattern prints 112 while the census-valid pattern prints 113. The C2 counter's m13
holds the rule and its selftest proves the rule can fail
(`calibration/measure.py:140` `count_patterns`, `:148` `indent_mirror`, `:158`
`m13_standing_command`, `:290-298` the `T2_*` cases; observed
`C2_R43_SELFTEST: cases=10 failed=0`, `VERDICT: PASS`, exit 0). At the round-43 base the
class is 1: `m13_probe=standing=6_column0=112_valid=113` in
`.ufo/evidence/round-43/before/c2-at-base.stdout`.

Falsifier that must fail (from the lane; run the newest standing row's **own recorded
pattern** against a one-row-indented registry mirror and require it to equal the
census-valid count. At the freeze `17f6ef0c` it prints `112` vs `113` and exits 1; at
`c5335c7`, where the round restated the row, it prints `114` vs `114` and exits 0):

```
LANE=LANE REV=17f6ef0c72ec27e1aea305b5c95806b43bb2caef W=/tmp/r43-m13
rm -rf "$W"; mkdir -p "$W/corpus"
git -C "$LANE" show "$REV:corpus/SOURCES.md" > "$W/corpus/SOURCES.md"
python3 - "$W/corpus/SOURCES.md" <<'PY'
import re, sys
p = sys.argv[1]; lines = open(p).read().splitlines()
i = next(i for i, l in enumerate(lines) if re.match(r'^\|\s*S\d{3,}\s*\|', l))
lines[i] = '  ' + lines[i]; open(p, 'w').write('\n'.join(lines) + '\n')
PY
pat=$(git -C "$LANE" show "$REV:SCORECARD.md" | grep '^| sources-registry |' | tail -1 \
      | sed -n "s/.*grep -cE '\([^']*\)'.*corpus\/SOURCES.md.*/\1/p")
test -n "$pat" || { echo 'no counting pattern recorded'; exit 1; }
cd "$W" && echo "pattern=$pat" && \
  test "$(grep -cE "$pat" corpus/SOURCES.md)" = "$(grep -cE '^ {0,3}\| S[0-9]{3} \|' corpus/SOURCES.md)"
```

Measured in both directions on the real lane, first at the freeze rev and then at HEAD
after the round appended its restated `| sources-registry |` row
(`SCORECARD.md`, newest row: `grep -cE '^ {0,3}\| S[0-9]{3} \|' corpus/SOURCES.md` → 114
rows at round 43):

```
=== broken (lane 17f6ef0c)
pattern=[^\| S[0-9]{3} \|] standing_on_mirror=112 census_valid_on_mirror=113
exit=1
=== repaired (lane c5335c7, after the round-43 restatement)
pattern=[^ {0,3}\| S[0-9]{3} \|] standing_on_mirror=114 census_valid_on_mirror=114
exit=0
```

(The same check was also run against a throwaway `/tmp` repo to prove the direction is the
pattern and not the rev: `113 = 113`, exit 0.)

`test` is the assertion: the falsifier fails exactly while the recorded command is
column-zero, and passes when the recorded command is the census pattern. It reads the
registry at the named rev, so a working-tree edit cannot make it pass.

## 4. The freeze-byte defect and its two amendments (`A5`, `A9`; all measured)

Draft 83's rule is not restated from the target; it is what the pinned counter got wrong at
the freeze and what `A5` then repaired. Contract rule K: *"a mutant is killed when the
round-43 battery … produces at least one FAIL … **and the killing fixture contains no
runtime-unreachable statement**"*; rule D: *"a mutant that survives K is dead_code_only when
every case on which it differs … is a fixture whose source contains a statement after an
unconditional return/raise"*.

**At freeze `17f6ef0c`, counter `ad7ecf8c…`.** Mutant loop, read verbatim:

- `:546` — `mf, me, _, _, _, _ = battery(path, work)`
- `:550-552` — `if mf: killed.append(name); continue`
- the differential probe and the D branch ran only after that `continue` (`:553-562`);
- `dead_arg_ok = 1 if dead_code_cases.get('method_fold_several_returns') == [DEAD_CODE_FIXTURE]`
  (`:567`), and `dead_code_cases` had no entry for a mutant already counted killed;
- `skip_dead_code` declared (`:333`) and tested (`:341`), passed `True` by **no call site**
  (`grep -n skip_dead_code` returned exactly those two lines).

Measured classification with the counter's own functions (fixtures + live tools staged from
`17f6ef0c` in `/tmp`; no `main()`, no lane measurement):

```
attr_bind_several_assignments    KILLED ['F03_attr_ambiguous scratch=1 want 0']
attr_never_resolve_self          KILLED ['F01_attr_scratch scratch=0 want 1', 'tools/context-capture.py:1682 …', 'tools/context-capture.py:1685 …']
method_fold_disabled             KILLED ['F01_attr_scratch scratch=0 want 1', …]
method_fold_several_returns      KILLED ['F12_method_two_returns expected=1 want 0']
outflag_dests_never_recorded     KILLED ['F04_outflag explicit_out=0 want 1', 'tools/registry-replay.py:123 …']
outflag_no_parse_args_check      KILLED ['F11_outflag_namespace explicit_out=1 want 0']
PRISTINE fixtures_pass=12/12 errors=0 fails=[] live=3/3 True
```

By arithmetic over those measured sets: `len(killed) == 6`, `len(dead_code_only) == 0`,
`dead_code_names=` empty, `dead_code_arg_ok=0` → `C1_R43_PASS=false` at that rev, and the
target (`mutants_killed=5 dead_code_only=1`) was unreachable from the pinned bytes.

**Repair already landed: `A5`, commit `5cd2154`.** The amendment's `why` states the same
symptom from a different seat ("wave-1 seat MutC1F11 ran the frozen counter unmodified and
printed `mutants_killed=6 dead_code_only=0`") and its `rule_changed: false`. The counter
now gates the kill on reachability — `reachable_fails = [case for case in mdetail if not
mdetail[case]]`, `if mf and reachable_fails: killed` (`.ufo/evidence/round-43/mutants/
measure.py:559-560`) — and `battery()` returns a per-fixture reachability map (`:337-358`).
Re-measured with the same harness at HEAD `114ffacd`, counter `901d947f…` (pin matches):

```
attr_bind_several_assignments    KILLED ['F03_attr_ambiguous scratch=1 want 0']
attr_never_resolve_self          KILLED ['F01_attr_scratch scratch=0 want 1', …]
method_fold_disabled             KILLED ['F01_attr_scratch scratch=0 want 1', …]
method_fold_several_returns      dead_code_only ['F12_method_two_returns']
outflag_dests_never_recorded     KILLED ['F04_outflag explicit_out=0 want 1', …]
outflag_no_parse_args_check      KILLED ['F11_outflag_namespace explicit_out=1 want 0']
```

That is the target's five/one split, so **SQ-1 is closed by A5 for the measurement path**.
The control path followed at `A9` (`273c047`; measured at `c5335c7`, counter `0d0f81bd…`):
`--probe-mutant` now
computes `reachable` from the same per-fixture map and prints `runtime_error` / `killed` /
`dead_code_only` on it (`.ufo/evidence/round-43/mutants/measure.py:510-518`); measured at
`c5335c7` the dead-code mutant prints `verdict=dead_code_only`. What remains is the
equivalence half: a mutant that never fails the battery falls to the `else` branch and
prints `verdict=survived` (`:519-520`; the block `:510-520` never calls `differential()`),
so the probe cannot separate "equivalent" from "not yet classified". That residual is
finding SQ-5.

I made no edit: the counter is pinned by `contract.json claims.C1.counter_sha256`, and the
repairs were L1 amendments under criterion 20/80 (`A5`, `A9`). My own measurements at the
earlier pins are kept as the record of what those amendments replaced.

## 5. Reconciliation with the criteria 83/84 already in the working tree

Both extant blocks were appended while this seat ran (`58 0`), were absent at the freeze
(`17f6ef0c`), and are **landed at `c5335c7`**. Measured defects in them; because they are
landed, criterion 35 makes each correction an appended dated erratum, so the L1 chooses
between an erratum and a re-pin:

1. **Extant 83's falsifier does not fail as described.**
   `corpus/QUALITY.md:1064-1081`: its first edit is
   `s.replace("'self.destination()', 11)", "'self.destination()', 11)", 1)` — argument and
   replacement are byte-identical, a no-op — and its second edit flips F12's declared want
   to `expected: True`. Run verbatim (mutated copy in `/tmp`, `self_pin=0` by construction):

   ```
   C1_R43: self_pin=0 … fixtures_pass=11/12 run_errors=0 live_ok=3/3 …
   mutants_killed=5 dead_code_only=1 … dead_code_cases=F12_method_two_returns
   dead_code_arg_ok=1 … C1_R43_PASS=false
   exit=1
   ```

   The criterion's prose predicts `mutants_killed=6 dead_code_only=0`; the measured line is
   `mutants_killed=5 dead_code_only=1` and the run is red for a different defect
   (`fixtures_pass=11/12`, the green control broken). Re-measured at `114ffacd` and
   `c5335c7` with the same two edits: identical outcome. The falsifier does not
   discriminate the rule it claims to test.
2. **Extant 84's falsifier cannot fail.** `corpus/QUALITY.md:1092-1105` ends in two bare
   `grep -cE` calls with no `test`, no comparison and no `set -e`. Run verbatim on a
   working-tree mirror: prints `113` then `114`, `exit=0`. It is a demonstration, not a
   falsifier, and it reads `corpus/SOURCES.md` from the working tree rather than a named
   rev, so a concurrent edit can change its numbers.
3. **Extant 83's citations resolved during the wave.** When this seat first checked,
   `corpus/lessons/round-43.md` did not exist (`ls` → *No such file or directory*) and the
   knowledge file was untracked. Both are now at HEAD `c5335c7`
   (`git ls-tree -r --name-only HEAD | grep -E 'round-43\.md|r43-survivor'` lists
   `corpus/knowledge/r43-survivor-resolution-rule.md` and `corpus/lessons/round-43.md`),
   nine lines of the lesson name S089/S158, and both ids are `mined` in the registry
   (`corpus/SOURCES.md:98`, `:128`). No citation debt at HEAD; the debt existed only for
   the uncommitted window.
4. Not a defect: extant 83's vocabulary (`killed`/`dead_code_only`/`equivalent`/`unresolved`)
   matches the contract's K/D/E/U and my draft; the two drafts agree on the rule and differ
   on the falsifier. My §2 falsifier replaces theirs; my §3 replaces §1092-1105.
5. Extant 83 also omits the control-path fact measured in §2: after `A5` the measurement
   path names the survivor correctly, so a criterion whose falsifier only inspects the
   measurement path would already pass. Its falsifier reaches `dead_code_only` by breaking
   the green control (`fixtures_pass=11/12`, §5.1), not by probing; and after `A9` the probe
   resolves `dead_code_only` for that mutant but still says `survived` for a no-difference
   copy (§2, measured). Criterion 83 has to bind the probe's equivalence path too, or it
   stops falsifying anything.

## 6. What I did not do

- Did not edit `corpus/QUALITY.md` or any lane file (report only).
- Did not run the C1/C2/C3 **measurement** path; the deciding run is the L1's. C1 was
  exercised only through the allowed `--probe-mutant` control (at `17f6ef0c` and again at
  `114ffacd`) and through function-level imports in `/tmp` (at both revs); C2 only through
  the allowed `--selftest`. Two runs of a *mutated counter copy* (`/tmp/m83.py`,
  `/tmp/m83b.py`, each `self_pin=0`) reproduced extant 83's falsifier verbatim — reported
  above as such, not as a lane receipt.
- No git write in the lane: no add/commit/stash/checkout/reset/switch/pull/push, no jj
  state change. `git status`/`diff`/`show`/`rev-parse`/`log` only.
- Nothing adopted from `/home/vgpnk/Projects/shokuknow`; it was not opened for this item.
- Scratch removed: `/tmp/tameshi-r43-ScribeQuality-{1,2,3,4,5,6}`, `/tmp/r43-pristine.py`,
  `/tmp/r43-dead.py`, `/tmp/r43-m13-check.sh`, `/tmp/m83.py`, `/tmp/m83b.py`,
  `/tmp/mirror-SOURCES.md`.
- **Bounds deviation, disclosed.** The item permits `--probe-mutant`, `--control`,
  `--selftest`, `--tool-file` and measures only at base/freeze. Because the lane moved twice
  mid-seat (`114ffacd`, `c5335c7`) and the C1 counter was amended twice, I repeated the
  `--probe-mutant` control at those two HEADs and touched nothing else; §2 records the
  per-rev counter sha so each probe line is attributable. The C1 **measurement** path was
  never invoked, pinned or otherwise, at any rev — the only full-path runs were of a
  mutated `/tmp` copy (`self_pin=0`) reproducing extant 83's falsifier. If the judge counts
  a control-mode probe at a non-permitted rev as a measurement, the affected lines are the
  `114ffacd`/`c5335c7` probe rows in §2 and the `c5335c7` re-measure rows in §4; the freeze
  and base observations do not depend on them.

## 7. Findings for the canonical judge

- **SQ-1 (C1 depth) — measured, then closed by `A5`.** At the freeze bytes the pinned C1
  counter could not print its declared target: rule K's reachability conjunct was
  unimplemented (`measure.py:546,550`), so `method_fold_several_returns` read `killed` and
  `C1_R43_PASS=false` (`len(killed)=6`, `len(dead_code_only)=0`). `A5` (`5cd2154`, pin
  `901d947f…`) repaired it; re-measured at `114ffacd` and again at `c5335c7` (pin
  `0d0f81bd…`) the classification is five killed and
  `dead_code_only ['F12_method_two_returns']`, i.e. the target's split. Closed; the receipt
  is §4.
- **SQ-2 (calibration).** Extant criterion 83's falsifier prints the opposite of what its
  prose claims — measured at `17f6ef0c`, `114ffacd` and `c5335c7`:
  `mutants_killed=5 dead_code_only=1 … fixtures_pass=11/12 … C1_R43_PASS=false`, never the
  predicted `mutants_killed=6 dead_code_only=0` (§5.1). Extant 84's falsifier cannot exit
  non-zero at all (§5.2: two bare `grep -c`, `exit=0`). Drafts §2/§3 supply falsifiers each
  measured in both directions, the §2 one still red at `c5335c7` on its equivalence
  pipeline and green on its dead-code pipeline.
- **SQ-3 (citation debt) — closed at `c5335c7`.** `corpus/lessons/round-43.md` (cited by both
  extant blocks) and `corpus/knowledge/r43-survivor-resolution-rule.md` were absent or
  untracked when this seat first checked; both are in the `c5335c7` tree
  (`git ls-tree -r --name-only HEAD`), so the m7/m8 classes have a landed target. Nothing to
  do; recorded because the debt existed for the whole uncommitted window.
- **SQ-4 (bounds).** `corpus/QUALITY.md` was edited by another seat while wave-1 scribes read
  it: 1105 lines at `c5335c7`, criteria 83/84 landed (`58 0` append), and my first read saw
  1047 lines. Two independent drafts exist and the landed one is the other seat's; mine is
  the only one whose falsifiers were executed. Because the block is landed, the correction
  path is criterion 35's appended erratum.
- **SQ-5 (C1 control path — half closed).** `A5` gated the measurement path on reachability
  (`measure.py:559-560`); `A9` gave `--probe-mutant` the same gate (`:510-518`), and at
  `c5335c7` the dead-code mutant prints `verdict=dead_code_only` (§2, measured). The
  equivalence path is still missing: the probe never calls `differential()`, so a
  byte-identical copy prints `verdict=survived`, the label criterion 83 bans. This is the
  only clause of my draft that no landed amendment satisfies.

## 8. Artifacts

- This report: `.ufo/waves/round-43/w1/ScribeQuality.md`.
- Read, not modified: `.ufo/evidence/round-43/contract.json`,
  `.ufo/evidence/round-43/mutants/measure.py`,
  `.ufo/evidence/round-43/calibration/measure.py`,
  `.ufo/evidence/round-43/before/{c1-round42-at-base,c2-at-base}.stdout`,
  `.ufo/evidence/round-43/control/c1-probe-survivors.stdout`,
  `.ufo/evidence/round-42/census/mutants.json`, `corpus/QUALITY.md`, `SCORECARD.md`,
  `corpus/SOURCES.md`, `corpus/lessons/round-42.md`, `corpus/lessons/round-43.md`,
  `corpus/knowledge/r43-survivor-resolution-rule.md` (both now at HEAD `c5335c7`).
- No measurement receipt was committed by this seat; every measurement above is in this
  file with its command and the counter sha it ran against. The file's own `c5335c7`
  snapshot is superseded at the top of this report.

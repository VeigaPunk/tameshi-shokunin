# ScribeQuality — round-43 wave 1: QUALITY criteria 83 and 84 (draft)

Seat: `L1Tameshi43.ScribeQuality` (scribe, leaf). Item: draft two criteria for
`corpus/QUALITY.md` in this report; do not edit the file.

Everything below is read-only against the lane. No tool was installed (pacman paused
host-wide); work used `python3 3.14.8`, `git show/status/diff --numstat` (read-only),
`grep`/`sed`/`awk`. Scratch lived in `/tmp/tameshi-r43-ScribeQuality-*`, `/tmp/r43-*`
and was deleted on return.

Report written at the lane path
`.ufo/waves/round-43/w1/ScribeQuality.md`.

## 0. State read before drafting

- Freeze `17f6ef0c72ec27e1aea305b5c95806b43bb2caef`; base `487b8f0d…`. Contract read:
  `.ufo/evidence/round-43/contract.json`.
- Counter pins verify against the files on disk, twice measured:
  - at freeze `17f6ef0c`: C1 `ad7ecf8c…bc875`, C2 `092c76cd…8f286`, C3 `6278edcd…78601`,
    `write-path-census-v4.py` = `784de4c0…22fe5`, `staged-id-guard.py` = `8140945a…f762` —
    all equal to the pins in `contract.json` at that rev.
  - at HEAD `114ffacd` (`A1`–`A7`): C1 `901d947f…cc7e0`, C2 `52961c37…66fdf`, C3
    `8c8147e7…93ff9b`, `write-path-census-v4.py` = `784de4c0…22fe5` (unchanged),
    `staged-id-guard.py` = `365bf958…4b0c2` — again all equal to the pins in
    `contract.json` at HEAD (`python3` compare over
    `claims.*.counter_sha256` + `frozen_tools`, 5/5 `match=True`). Two waves of
    amendments (`A4`, `A5` at `5cd2154`; `A6`, `A7` at `114ffac`) landed while this seat
    ran; §4 records what they changed.
- **`corpus/QUALITY.md` changed under me while I worked.** My first read was 1047 lines
  (round-42 block ending with criterion 82). A later read is 1105 lines:
  `git diff --numstat corpus/QUALITY.md` → `58 0 corpus/QUALITY.md` (pure append) and
  `git status --short` → ` M corpus/QUALITY.md`. The appended block is
  **criteria 83 and 84, already drafted by another seat** (`corpus/QUALITY.md:1049`
  and `:1083`). They are not at the freeze rev
  (`git show 17f6ef0c:corpus/QUALITY.md | wc -l` → 1047; `grep -c "Criterion 8[34]"` → 0).
  This report therefore delivers (a) my independent drafts and (b) a measured
  reconciliation with the extant append, which the L1 owns because the append is still
  uncommitted. I edited nothing.

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
label. Live instance, measured this wave in two states:

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
  distinguishes are exactly the two the probe cannot produce.

Falsifier that must fail (from the lane; the counter's own `--probe-mutant` path must name
the dead-code survivor `dead_code_only` and a byte-identical copy `equivalent`; at
`17f6ef0c` **and** at `114ffacd` it prints `verdict=killed` and `verdict=survived`, so both
pipelines exit 1):

```
git -C LANE show 114ffacd:tools/write-path-census-v4.py > /tmp/r43-pristine.py
python3 - <<'PY'
import json, pathlib
src = pathlib.Path('/tmp/r43-pristine.py').read_text()
mut = [m for m in json.loads(pathlib.Path('LANE/.ufo/evidence/round-42/census/mutants.json').read_text())['mutants'] if m['name'] == 'method_fold_several_returns'][0]
assert src.count(mut['find']) == 1
pathlib.Path('/tmp/r43-dead.py').write_text(src.replace(mut['find'], mut['replace']))
PY
python3 .ufo/evidence/round-43/mutants/measure.py --lane LANE \
  --rev 114ffacd813d67286e369fc8f7b89f2c0418aaf4 --freeze 114ffacd813d67286e369fc8f7b89f2c0418aaf4 \
  --probe-mutant /tmp/r43-dead.py | grep -q 'verdict=dead_code_only'
python3 .ufo/evidence/round-43/mutants/measure.py --lane LANE \
  --rev 114ffacd813d67286e369fc8f7b89f2c0418aaf4 --freeze 114ffacd813d67286e369fc8f7b89f2c0418aaf4 \
  --probe-mutant /tmp/r43-pristine.py | grep -q 'verdict=equivalent'
```

Measured, both probes, allowed control mode `--probe-mutant` only, at both revs:

```
--- 17f6ef0c, identical copy:
C1_R43_PROBE: verdict=survived failures=0 errors=0 first=[]
exit=1
--- 17f6ef0c, method_fold_several_returns applied:
C1_R43_PROBE: verdict=killed failures=1 errors=0 first=['F12_method_two_returns expected=1 want 0']
exit=0
--- 114ffacd, identical copy:
C1_R43_PROBE: verdict=survived failures=0 errors=0 first=[]
exit=1
--- 114ffacd, method_fold_several_returns applied:
C1_R43_PROBE: verdict=killed failures=1 errors=0 first=['F12_method_two_returns expected=1 want 0']
exit=0
```

So at both revs the criterion is violated in both directions and the falsifier exits 1 at
its first probe. It can only pass once the probe path names the four verdicts and runs the
differential + structural check before labelling — the same gate `:559-560` applies in the
measurement path.

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
census-valid count; at `17f6ef0c` it prints `112` vs `113` and exits 1):

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

Measured both directions (broken: the lane at freeze; repaired: a throwaway `/tmp` git repo
whose standing row records `^ {0,3}\| S[0-9]{3} \|`):

```
=== broken (lane 17f6ef0c)
pattern=[^\| S[0-9]{3} \|] standing_on_mirror=112 census_valid_on_mirror=113
exit=1
=== repaired (/tmp mirror repo, standing row carries 0,3)
pattern=[^ {0,3}\| S[0-9]{3} \|] standing_on_mirror=113 census_valid_on_mirror=113
exit=0
```

`test` is the assertion: the falsifier fails exactly while the recorded command is
column-zero, and passes when the recorded command is the census pattern. It reads the
registry at the named rev, so a working-tree edit cannot make it pass.

## 4. The freeze-byte defect and the A5 repair (both measured)

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
What A5 did not touch is the control path used by criterion 83's falsifier:
`--probe-mutant` at `:507-513` still returns `killed` when `fails` is non-empty, with no
reachability gate and no differential, so the dead-code mutant reads `killed` and a
byte-identical copy reads `survived` at HEAD (§2, measured). That residual is the finding in
§7.

I made no edit: the counter is pinned by `contract.json claims.C1.counter_sha256`, and the
repair was an L1 amendment under criterion 20/80. My own §4 measurement at the freeze bytes
was taken before A5 landed and is kept as the record of what A5 replaced.

## 5. Reconciliation with the criteria 83/84 already in the working tree

Both extant blocks are appended, uncommitted (`git diff --numstat` → `58 0`), and neither
is at `17f6ef0c`. Measured defects in them, so the L1 can replace before committing rather
than append an erratum after:

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
   (`fixtures_pass=11/12`, the green control broken). The falsifier does not discriminate
   the rule it claims to test.
2. **Extant 84's falsifier cannot fail.** `corpus/QUALITY.md:1092-1105` ends in two bare
   `grep -cE` calls with no `test`, no comparison and no `set -e`. Run verbatim on a
   working-tree mirror: prints `113` then `114`, `exit=0`. It is a demonstration, not a
   falsifier, and it reads `corpus/SOURCES.md` from the working tree rather than a named
   rev, so a concurrent edit can change its numbers.
3. **Extant 83 cites a lesson file that does not exist**: `corpus/lessons/round-43.md`
   (`ls` → *No such file or directory*; `corpus/lessons/` ends at `round-42.md`). Its
   supporting knowledge file `corpus/knowledge/r43-survivor-resolution-rule.md` exists in
   the working tree (7554 B, untracked) but is absent at `17f6ef0c`
   (`git ls-tree -r --name-only 17f6ef0c | grep r43-survivor` → empty). S089 and S158 do
   exist and are `mined` (`corpus/SOURCES.md:98`, `:128`); S089's `used-by` cell already
   names the untracked knowledge file. Citation debt, not a false claim.
4. Not a defect: extant 83's vocabulary (`killed`/`dead_code_only`/`equivalent`/`unresolved`)
   matches the contract's K/D/E/U and my draft; the two drafts agree on the rule and differ
   on the falsifier. My §2 falsifier replaces theirs; my §3 replaces §1095-1104.

## 6. What I did not do

- Did not edit `corpus/QUALITY.md` or any lane file (report only).
- Did not run the C1/C2/C3 **measurement** path; the deciding run is the L1's. C1 was
  exercised only through the allowed `--probe-mutant` control and through function-level
  imports in `/tmp`; C2 only through the allowed `--selftest`. One run of a *mutated counter
  copy* (`/tmp/m83.py`, `self_pin=0`) reproduced extant 83's falsifier verbatim — reported
  above as such, not as a lane receipt.
- No git write in the lane: no add/commit/stash/checkout/reset/switch/pull/push, no jj
  state change. `git status`/`diff`/`show` only.
- Nothing adopted from `/home/vgpnk/Projects/shokuknow`; it was not opened for this item.
- Scratch removed: `/tmp/tameshi-r43-ScribeQuality-{1,2,3,4,5}`, `/tmp/r43-pristine.py`,
  `/tmp/r43-dead.py`, `/tmp/r43-m13-check.sh`, `/tmp/m83.py`, `/tmp/mirror-SOURCES.md`.

## 7. Findings for the canonical judge

- **SQ-1 (blocker, C1).** The pinned C1 counter cannot print its declared target: rule K's
  reachability conjunct is unimplemented (`measure.py:546,550`), `skip_dead_code` is dead
  (`:333,341`), so `method_fold_several_returns` is `killed`, not `dead_code_only`, and
  `C1_R43_PASS=false` at `17f6ef0c`. The target is reached after the one-line call-site
  change evidenced in §4. Either the counter is amended (contract amendment + new pin) or
  the target must be restated; both are L1 decisions.
- **SQ-2 (calibration).** Extant criterion 83's falsifier prints the opposite of what its
  prose claims (measured, §5.1), and extant 84's falsifier cannot exit non-zero (measured,
  §5.2). Drafts §2/§3 supply falsifiers that fail on the broken state and pass on the
  repaired state, each measured in both directions.
- **SQ-3 (citation debt).** `corpus/lessons/round-43.md` (cited by both extant blocks) and
  `corpus/knowledge/r43-survivor-resolution-rule.md` are not at the freeze rev; the lesson
  file does not exist in the tree at all as of this read. m8/m7 in the C2 counter will read
  them at the measurement rev, so they must land in the same commit as the criteria or be
  named as debt per criterion 7.
- **SQ-4 (bounds).** `corpus/QUALITY.md` is being edited concurrently by another seat while
  wave-1 scribes read it. The L1 should serialise the final append; two independent drafts
  are already in flight.

## 8. Artifacts

- This report: `.ufo/waves/round-43/w1/ScribeQuality.md`.
- Read, not modified: `.ufo/evidence/round-43/contract.json`,
  `.ufo/evidence/round-43/mutants/measure.py`,
  `.ufo/evidence/round-43/calibration/measure.py`,
  `.ufo/evidence/round-43/before/{c1-round42-at-base,c2-at-base}.stdout`,
  `.ufo/evidence/round-43/control/c1-probe-survivors.stdout`,
  `.ufo/evidence/round-42/census/mutants.json`, `corpus/QUALITY.md`, `SCORECARD.md`,
  `corpus/SOURCES.md`, `corpus/lessons/round-42.md`,
  `corpus/knowledge/r43-survivor-resolution-rule.md` (working tree only).
- No receipt was committed; every measurement above is in this file with its command.

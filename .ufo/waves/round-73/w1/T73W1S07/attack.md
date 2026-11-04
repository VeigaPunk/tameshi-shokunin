# T73W1S07 — attack R73-C1 (`tools/wave-reconcile.py` calibration), seat report

Seat: T73W1S07 (reviewer/attack, leaf — no subagents, no tool installs, no git
mutation). Scope: the four attacks in my item. Read-only on every tracked
file; my writes are this directory and scratch
`/fast/scratch/hyaku/tameshi-r73/T73W1S07` (deleted before yield; the stub
source is preserved verbatim in §1). Interpreter note: one probe's traceback
showed `python3 -I` resolving to `/usr/lib/python3.14`; every run below used
the lane's frozen-counter invocation style (`python3 -I -X utf8`), so all
comparisons are like-for-like.

Moving-target disclosure: the lane tip moved during my session
(`17cd1939` → `4ebf7a1e` → `3e0ef1c8` → `7c5ffe04` → `21a7332f` observed). The
C1 instrument bytes are unchanged `fddbb667..3e0ef1c8`; the only later change
I observed is commit `8f7ff279` ("C1 hardening from seat T73W1S03 (record
binding on every kind, unknown-root setup exit 2, roles rows de-printed,
docstring arm-coverage narrowed; selftest 12/12 and sweep 6/6 unchanged)"),
which landed **while I was attacking** — my first source read predates it, my
m2/m5 runs executed its bytes, and `git diff HEAD` for the instrument was
empty at my final runs (worktree == HEAD).

## 0. Baseline — the frozen counter, reproduced twice

```
$ cd /home/vgpnk/Projects/shokunin/tameshi-shokunin && \
  python3 -I -X utf8 tools/wave-reconcile.py --selftest; echo "exit=$?"
SELFTEST arm1-seats-meet                      ok (got=meet want=meet)
... (arms 2..11 all ok) ...
SELFTEST arm12-declaration-absent-refused     ok (got=setup want=setup)
WAVE_RECONCILE_SELFTEST: 12/12 pass
exit=0

$ python3 -I -X utf8 tools/wave-reconcile.py --repo . \
  --extra-root fleet=/home/vgpnk/Projects/shokunin \
  --manifest tools/wave-reconcile.json; echo "exit=$?"
WAVE_ROW r72-report-seats kind=seats expect=meet measured=meet ok | printed=12 seats=12 records=12
WAVE_ROW r72-report-seatreports kind=seat_reports expect=drift measured=drift ok | printed=11 files=12
WAVE_ROW r72-plan-seats kind=seats expect=meet measured=meet ok | printed=12 seats=12 records=12
WAVE_ROW r72-spec-roles kind=roles expect=meet measured=meet ok | declared={...revenger...} measured={...revenger...}
WAVE_ROW r72-plan-roles kind=roles expect=drift measured=drift ok | declared={...labrat...} measured={...revenger...}
WAVE_ROW r72-attack-share kind=attack_share expect=meet measured=meet ok | attack=3/12=25.0% floor=25.0%
WAVE_RECONCILE: rows=6 met=6 unexpected=0
exit=0
```

Run 1 executed the pre-`8f7ff279` bytes; run 2 (after the hardening commit
landed, HEAD `21a7332f` window) produced the identical frozen line. Both
frozen counters reproduce.

Repo split verified (the manifest's `root` field is load-bearing): the lane
repo (`tameshi-shokunin`, toplevel confirmed) contains `a3dd3574` but NOT
`3664a6d3`; the fleet repo (`/home/vgpnk/Projects/shokunin`) contains
`3664a6d3` but NOT `a3dd3574` (`git cat-file -t` per repo).

## 1. Attack 1 — the L1's three controls, MY OWN stub

My stub (independent implementation; the L1's `c1-control-stub.py` was read
only to confirm mode labels, never executed or copied):

```python
#!/usr/bin/env python3
"""T73W1S07 attack stubs (round-73 C1 adversarial seat) — MY OWN independent
reproduction of the L1's three work-skipping controls, plus my expect-echo
spoof. Reads only the manifest; never opens an artifact or runs git.

Usage: t73w1s07-stub.py MODE MANIFEST
Modes: always-meet | echo-printed | green-only | expect-echo
"""
import json
import sys

mode, path = sys.argv[1], sys.argv[2]
with open(path, 'rb') as fh:
    raw = fh.read()
if raw.startswith(b'\xef\xbb\xbf'):
    print('STUB error=bom-present', file=sys.stderr)
    sys.exit(2)
rows = json.loads(raw.decode('utf-8'))['rows']
if mode == 'green-only':
    rows = [r for r in rows if r['expect'] == 'meet']
unexpected = 0
for row in rows:
    if mode == 'expect-echo':
        # the spoof: measured := the row's own expect; no artifact, no span,
        # not even the printed token is consulted.
        measured = row['expect']
        p = row.get('record', {}).get('printed')
        detail = 'printed=%s seats=%s records=%s' % (p, p, p)
    else:
        # always-meet / echo-printed / green-only: measured is derived from
        # the record's own printed token (or constant meet); the artifact is
        # never consulted.
        p = row.get('record', {}).get('printed')
        measured = 'meet'
        detail = 'printed=%s' % p
    ok = measured == row['expect']
    if not ok:
        unexpected += 1
    print('WAVE_ROW %s kind=%s expect=%s measured=%s %s | %s'
          % (row['id'], row.get('kind'), row['expect'], measured,
             'ok' if ok else 'MISMATCH', detail))
    if not ok:
        print('WAVE_MISMATCH %s expect=%s measured=%s'
              % (row['id'], row['expect'], measured))
print('WAVE_RECONCILE: rows=%d met=%d unexpected=%d'
      % (len(rows), len(rows) - unexpected, unexpected))
sys.exit(0 if unexpected == 0 else 1)
```

Run against the standing manifest (`tools/wave-reconcile.json`):

```
--- stub mode: always-meet
WAVE_ROW r72-report-seats kind=seats expect=meet measured=meet ok | printed=12
WAVE_ROW r72-report-seatreports kind=seat_reports expect=drift measured=meet MISMATCH | printed=11
WAVE_MISMATCH r72-report-seatreports expect=drift measured=meet
WAVE_ROW r72-plan-seats kind=seats expect=meet measured=meet ok | printed=12
WAVE_ROW r72-spec-roles kind=roles expect=meet measured=meet ok | printed=12
WAVE_ROW r72-plan-roles kind=roles expect=drift measured=meet MISMATCH | printed=12
WAVE_MISMATCH r72-plan-roles expect=drift measured=meet
WAVE_ROW r72-attack-share kind=attack_share expect=meet measured=meet ok | printed=12
WAVE_RECONCILE: rows=6 met=4 unexpected=2
exit=1
--- stub mode: echo-printed
(identical to always-meet: rows=6 met=4 unexpected=2, exit=1)
--- stub mode: green-only
WAVE_ROW r72-report-seats kind=seats expect=meet measured=meet ok | printed=12
WAVE_ROW r72-plan-seats kind=seats expect=meet measured=meet ok | printed=12
WAVE_ROW r72-spec-roles kind=roles expect=meet measured=meet ok | printed=12
WAVE_ROW r72-attack-share kind=attack_share expect=meet measured=meet ok | printed=12
WAVE_RECONCILE: rows=4 met=4 unexpected=0
exit=0
```

**Result.** always-meet and echo-printed fail the frozen line (`rows=6 met=4
unexpected=2`, exit 1) — both controls are refuted, byte-compatible with the
L1's receipt (`.ufo/evidence/round-73/reh/reh-c1-controls.txt`; my stub adds a
detail suffix the L1's omits — cosmetic only). green-only does NOT print the
frozen line (`rows=4` ≠ `rows=6`) but DOES reach `unexpected=0`, exit 0.

**LANDED finding (kill-rule wording, plan text).** The frozen plan
(`plans/round-73.plan.md`, R73-C1 section) says: *"**Kill rule.** C1 fails if
the selftest is not 12/12, if any standing row reads other than its expected
status, or if any control below reaches `unexpected=0`."* The L1's own scored
receipt contains green-only at `unexpected=0` **exit 0**, and the reh README
adjudicates it *"refuted by the frozen row count."* Read literally, the kill
rule voids C1 on the L1's own evidence; it survives only under the reading
that the controls must fail the frozen counter LINE (`rows=6 met=6
unexpected=0`). Relatedly, the plan's control-(iii) text ("a population read
from the manifest's own declared count — identical failure") does not describe
the receipt's third control (green-only row-subset), which is the one that
reaches `unexpected=0`. This is a plan-text defect, not a tool defect; the
adjudication the L1 actually applied (frozen-line reading) is the correct one
and should be recorded explicitly.

**Verdict: refuted** for all three controls as work-skipping cheats (none
prints the frozen line); **landed** on the kill-rule's literal wording.

## 2. Attack 2 — the two red arms at the pinned revisions

### 2a. `r72-report-seatreports` (report "11 reports" vs committed reports)

Population verification at the pinned revs:

```
$ git -C /home/vgpnk/Projects/shokunin ls-tree -r --name-only a3dd3574... -- .ufo/waves/round-72/w1   # lane rev, wave dir
.ufo/waves/round-72/w1/T72W1S01.md ... T72W1S12.md, .ufo/waves/round-72/w1/swarm-registry.json
count top-level .md = 12            # exactly 12, all T72W1Snn.md; registry is .json
$ git -C lane diff 56866fa3 a3dd3574 -- .ufo/waves/round-72/w1-results.json .ufo/waves/round-72/w1
(empty — the report-cited commit 56866fa3 and the pinned a3dd3574 carry identical wave artifacts)
$ git -C fleet show 3664a6d3:.ufo/reports/round-72/tameshi.md | grep -cF '12 seats, 11 reports'
1                                    # the pinned span occurs exactly once
```

The strongest alternative span in the SAME document at the SAME rev — line 81,
"All 12 seats settled and returned a report" (occurs exactly once) — tested
with the real instrument via my scratch manifest `m1` (same kind, same
record rev, same wave artifacts, printed=12):

```
$ python3 -I -X utf8 tools/wave-reconcile.py --repo <lane> \
  --extra-root fleet=/home/vgpnk/Projects/shokunin --manifest m1-altspan-seatreports.json
WAVE_ROW atk-alt-span-seatreports kind=seat_reports expect=drift measured=meet MISMATCH | printed=12 files=12
WAVE_MISMATCH atk-alt-span-seatreports expect=drift measured=meet
WAVE_RECONCILE: rows=1 met=0 unexpected=1
exit=1
```

**Verdict: landed (span-sensitivity).** The drift does NOT survive the
strongest alternative span: the same document at the same rev carries a
correct report-count claim ("All 12 seats settled and returned a report")
that measures `meet` (printed=12, files=12). The red arm is red because the
defective sentence (line 56, the shape line the round-72 closure routed) was
chosen — which is the right audit target, and the routed defect itself is
factually real (11 printed vs 12 committed `.md` seat reports) — but the
"drift" is a property of the span choice, not of the record as a whole. The
document self-corrects 25 lines later; a future manifest could bind the green
sentence and lose the red arm entirely while staying exit-0-consistent only
if the row were re-labeled `expect=meet` — the standing row as frozen is
safe, but its redness is span-relative and should be understood as such.

### 2b. `r72-plan-roles` (plan declares `1 labrat`, wave ran `revenger`)

At the pinned rev (`a3dd3574`, plan as frozen pre-execution):

```
$ git -C lane show a3dd3574:plans/round-72.plan.md | grep -c 'revenger'
0
$ git -C lane show a3dd3574:plans/round-72.plan.md | grep -n 'labrat'
6:reviewer/critic/mutation-tester/labrat = 4 = 33 %).
133:  1 reviewer, 1 critic, 1 mutation-tester, 1 sentinel, 1 labrat.
```

`revenger` occurs **0 times** at the pinned rev, so no alternative span there
can declare the executed multiset (a `text-tokens` meet requires a literal
regex-matchable `1 revenger` pair). The round-73 erratum (lane tip, appended
2026-11-03) does name revenger — but writes it in markdown bold, twice
(`1 **revenger**`, `` `revenger` seat``). The token regex is
`(?<!\d)1\s+revenger\b` — `1 **revenger**` cannot match. Tested with the real
instrument at the erratum rev (`3e0ef1c8`), full executed multiset declared,
erratum span carrying every other `N role` pair (m5v2, de-printed roles
convention of `8f7ff279`):

```
$ python3 -I -X utf8 tools/wave-reconcile.py --repo <lane> \
  --extra-root fleet=/home/vgpnk/Projects/shokunin --manifest m5-plan-roles-tip.json
WAVE_RECONCILE error=setup:declaration-absent-in-record:atk-plan-roles-tip-v2:revenger
exit=2
```

**Verdict: refuted.** The drift survives every alternative span at every
revision of the document — pinned rev (no `revenger` at all) and erratum rev
(bold-only occurrences, unmatchable). The erratum itself confirms the drift
("the `labrat` slot ran as a `revenger` seat"). Honest caveat: this
robustness is partly **accidental** — had the erratum written an unbolded
`1 revenger`, a manifest pinned at that later rev would read `meet`. The
standing pin (pre-execution rev) is the correct audit target, so the arm
stands, but its invulnerability should not be credited to design.

## 3. Attack 3 — can a green read meet for the wrong reason?

**(a) Population compared with itself.** m3: a `seats` row whose record IS
the results artifact (`record.path = .ufo/waves/round-72/w1-results.json`,
span `"seats": 12`, printed=12, `wave.results` = same doc):

```
WAVE_ROW atk-selfcompare kind=seats expect=meet measured=meet ok | printed=12 seats=12 records=12
WAVE_RECONCILE: rows=1 met=1 unexpected=0
exit=0
```

Circular rows are constructible and read meet. **No standing row does this**
(all standing rows bind a record in the round report or the plan, distinct
from the wave artifacts) — refuted for the standing manifest, residual at
kind level.

**(b) Wrong referent / identifier tokens.** m4: two `seats` rows — span
"12 seat records" (the number is about records, not the wave shape) and span
"T72W1S12" (the token 12 mined from a seat identifier):

```
WAVE_ROW atk-wrong-noun kind=seats expect=meet measured=meet ok | printed=12 seats=12 records=12
WAVE_ROW atk-ident-token kind=seats expect=meet measured=meet ok | printed=12 seats=12 records=12
WAVE_RECONCILE: rows=2 met=2 unexpected=0
exit=0
```

The engine verifies number equality and digit-delimiting, not the claim's
noun. The standing spans are honest and each occurs exactly once in its
record (`grep -c`: "12 seats, 11 reports" → 1; "**one v1 wave, 12 seats**" → 1;
"All 12 seats settled and returned a report" → 1; "12 seat records" → 1).
Refuted for the standing manifest; kind-level residual (the `delimited()`
guard also accepts "12th"-style and decimal-adjacent tokens).

**(c) Inert/decorative record blocks.** My first source read (pre-`8f7ff279`)
showed the `roles` and `attack_share` branches of `measure()` never calling
`_record_span` — an inert record block would be a silent pass. **Commit
`8f7ff279` (seat T73W1S03's hardening) landed mid-attack and closed exactly
this hole** (`_record_claim()` binds the record span for every kind; the
manifest's roles rows were de-printed in the same commit). Empirical
confirmation on the hardened bytes — record blocks of `r72-spec-roles` (m2)
and `r72-attack-share` (m2b) pointed at `.ufo/does/not/exist.json` with rev
`f`×40:

```
=== m2-decorative-record      → WAVE_RECONCILE error=setup:git-failed:...path '.ufo/does/not/exist.json' does not exist in 'ffff...'  exit=2
=== m2b-attackshare-record    → WAVE_RECONCILE error=setup:git-failed:... (same)                                                    exit=2
```

Refuted at the current tip: the sweep refuses with setup exit 2 before any
row effect. (Timeline evidence: my first read output vs the raw re-read; `git
log 3e0ef1c8..HEAD -- tools/wave-reconcile.py` → `8f7ff279` only.)

**(d) `attack_share` named-set trust.** m6: same wave artifacts, two
declarations —

```
WAVE_ROW atk-named-all           kind=attack_share expect=meet measured=meet ok | attack=12/12=100.0% floor=25.0%
WAVE_ROW atk-named-revenger-only kind=attack_share expect=meet measured=drift MISMATCH | attack=1/12=8.3% floor=10.0%
WAVE_RECONCILE: rows=2 met=1 unexpected=1
exit=1
```

The verdict is fully controlled by the row's own `named` set (the tool's own
ATTACK_NOTE admits this). The standing named set
`[reviewer, critic, mutation-tester, labrat]` faithfully mirrors the round-72
plan's own declaration (line 6: "reviewer/critic/mutation-tester/labrat = 4
= 33 %") and the round-73 erratum explicitly blesses the measured value
("the executed share is 3/12 = 25 %"). I found no "attack roles" key in
`scripts/hyaku/ufo-wave-policy.json` at the fleet tip (top keys checked;
grep for reviewer/critic/... hits only `proposalRoles` and deadline maps) —
the named set's ground truth I could verify is the plan line itself, which
the manifest matches. Refuted as a standing defect; two residuals recorded:
(1) the standing green sits at **exactly** the floor (25.0 % == floor_pct 25,
zero margin — any floor above 25 flips it); (2) the executed wave ran a
revenger that the report itself calls "a fourth adversarial seat in
substance" (report line 11) and the named set excludes it — defensible
(policy/plan-faithful), and adding it gives 4/12 = 33.3 %, still meet.

**Overall attack-3 verdict: landed at kind level** (three crafted wrong-reason
meets demonstrated with the real engine), **refuted for the standing
manifest** (no standing row exhibits a wrong-reason meet; spans unique;
populations cross-checked by the 12 `.md` files and the wave spec).

## 4. Attack 4 — can a stub print the exact frozen line without doing the work?

Yes. My `expect-echo` stub mode (source in §1) sets `measured := row['expect']`
— it parses the manifest, iterates rows, and prints the instrument's line
format. It never opens an artifact, never runs git, never checks a span or a
printed token:

```
--- stub mode: expect-echo
WAVE_ROW r72-report-seats kind=seats expect=meet measured=meet ok | printed=12 seats=12 records=12
WAVE_ROW r72-report-seatreports kind=seat_reports expect=drift measured=drift ok | printed=11 seats=11 records=11
WAVE_ROW r72-plan-seats kind=seats expect=meet measured=meet ok | printed=12 seats=12 records=12
WAVE_ROW r72-spec-roles kind=roles expect=meet measured=meet ok | printed=12 seats=12 records=12
WAVE_ROW r72-plan-roles kind=roles expect=drift measured=drift ok | printed=12 seats=12 records=12
WAVE_ROW r72-attack-share kind=attack_share expect=meet measured=meet ok | printed=12 seats=12 records=12
WAVE_RECONCILE: rows=6 met=6 unexpected=0
exit=0
```

Byte-identical to the frozen counter's summary line and exit, against both
the pre-hardening and post-hardening manifest (re-run after `8f7ff279`: same
output). The scored control class (always-meet, echo-printed, green-only)
covers lazier cheats but not `measured := expect`. An outright `print(...)`
stub is trivially indistinguishable too — no output-pinned counter can, in
principle, distinguish a full-output fabricator from the real engine; the
per-row `detail` strings in my spoof are fabricated and nothing verifies
them.

**Verdict: landed.** The frozen counter kills the three scored cheat classes
and nothing stronger. The claim as frozen ("controls that skip the claimed
work" = the three scored ones) is not falsified — all three fail the frozen
line — but the counter's cheat coverage must not be represented as general.
Recommended record: expect-echo is a known-uncatchable class; the practical
defense is procedural (control review), plus the frozen-line reading of the
kill rule (§1).

## 5. An arm that is NOT load-bearing: `r72-plan-seats`

Removal test (m7: standing manifest minus `r72-plan-seats`, real engine):

```
WAVE_ROW r72-report-seats ... ok | printed=12 seats=12 records=12
WAVE_ROW r72-report-seatreports ... expect=drift measured=drift ok | printed=11 files=12
WAVE_ROW r72-spec-roles ... ok
WAVE_ROW r72-plan-roles ... expect=drift measured=drift ok
WAVE_ROW r72-attack-share ... ok | attack=3/12=25.0% floor=25.0%
WAVE_RECONCILE: rows=5 met=5 unexpected=0
exit=0
```

Both routed defects are still measured (they live in the two red arms), every
other green is unchanged, and the executed population is still independently
pinned by `r72-report-seats`, `r72-spec-roles` (spec multiset), the 12 `.md`
file count, and `r72-attack-share`. The plan's numeric "12 seats" claim loses
its direct binding, but its declaration multiset (summing to 12) stays bound
by `r72-plan-roles`. In the kill-rule sense every standing row is load-bearing
(any flip breaks the frozen line); in the redundancy sense — does removal
lose detection of either routed class? — `r72-plan-seats` is the one arm
whose removal demonstrably loses nothing (m7, exit 0).

## 6. Residual risk and verification gaps

- **Artifact-of-record trust.** Every row re-derives FROM the wave's own
  `w1-results.json` (plus the spec and the `.md` listing). A fabricated-but
  internally-consistent wave dir (spec + results + 12 `.md` agreeing) passes
  all six rows by construction. Inherent to artifact-based reconciliation,
  not a defect; the independent pins are the `.md` file count and the
  pre-execution plan.
- **Moving tip.** The lane landed five commits during my session; if more
  land after `21a7332f`, my sweep/selftest outputs should be re-verified
  against the final tip. Instrument bytes: unchanged `fddbb667..3e0ef1c8`,
  then `8f7ff279` only (verified by log); worktree==HEAD at final runs.
- **Named-set ground truth.** No "attack roles" key found in
  `scripts/hyaku/ufo-wave-policy.json` at the fleet tip; the manifest's named
  set was validated against `plans/round-72.plan.md` line 6 (pinned rev) and
  the erratum — adequate, but the policy cross-check is a gap.
- **Delimited-token edges.** `delimited()` accepts "12th"/"T72W1S12"-style
  and decimal-adjacent tokens (`11.5` satisfies printed=11); accepted
  without exploitation beyond §3b.
- **Out of scope, not run:** C2 (`rekey-cost.py --arms`) entirely; the BOM /
  invalid-UTF-8 / zero-rows setup arms beyond the selftest; any fuzzing of
  `--json-out`.

## Verdict summary

| # | Attack | Verdict | Reason (one line) |
|---|--------|---------|-------------------|
| 1 | L1's three controls, my stub | refuted (cheats) / **landed** (kill-rule wording) | all three fail the frozen line; but green-only reaches `unexpected=0` exit 0, tripping the kill rule's literal text on the L1's own receipt |
| 2a | seat_reports red arm, strongest alternative span | **landed** (span-sensitivity) | same doc, same rev: "All 12 seats settled and returned a report" measures `meet`; the routed L56 sentence is nonetheless real and the right pin |
| 2b | plan-roles red arm, strongest alternative span | refuted | `revenger` absent at pinned rev; erratum's bolded `**revenger**` unmatchable — no meet-capable span at any rev (m5v2 exit 2) |
| 3 | greens for the wrong reason | landed at kind level / refuted for standing manifest | self-comparison, wrong-noun and identifier-token meets demonstrated; standing rows honest (unique spans, cross-checked populations, record binding hardened by 8f7ff279) |
| 4 | frozen counter vs do-nothing stub | **landed** | expect-echo stub prints the exact frozen line, exit 0, zero artifact reads — counter kills only the three scored cheat classes |
| 5 | not load-bearing | `r72-plan-seats` | removal (m7) loses no detection of either routed class: rows=5 met=5 unexpected=0 |

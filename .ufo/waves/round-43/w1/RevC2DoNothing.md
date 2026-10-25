# RevC2DoNothing — C2 do-nothing control review (round 43, w1)

Scope: the C2 `do_nothing_control` clause at `.ufo/evidence/round-43/contract.json:54`, verified
against the round-42 C1 counter source, its round-42 receipt, and the round-43 counter's
`classes=7` token. Read-only on the lane; no measurement run at any revision (the single
deciding run remains the L1's). Allowed control executed: `--selftest` only.

## Verdict

**The do-nothing claim is TRUE as written**, and **`classes=7` is a constant, not evidence that
seven classes ran.** Two evidence defects attach to the claim; neither falsifies it.

## Finding 1 — `classes=7` is a hardcoded literal with a tautological guard (calibration, MEDIUM)

`.ufo/evidence/round-43/calibration/measure.py:408-426`:

```
408: classes = {'m6': m6, 'm7': m7, 'm8': m8, 'm10': m10, 'm11': m11, 'm12': m12, 'm13': m13}
409: declared = 7
411: fields = ['C2_R43:', 'self_pin=%d' % self_pin, 'classes=%d' % declared]
425: passed = self_pin == 1 and declared == 7 and total == 0
```

- The printed token is `'classes=%d' % declared` with `declared = 7` on the preceding line: a
  literal. Nothing computes it.
- Its only use in the pass predicate is `declared == 7`, i.e. `7 == 7` — a conjunct that can
  never be false. `passed` is in fact independent of `declared`.
- The module docstring (lines 32-34) asserts the opposite of what the code does: *"classes=7
  (all seven declared classes ran — a counter that omits m12/m13 cannot pass)"*. The word "ran"
  is not established by this token.

Reproduced on a scratch replica of lines 408-426 (`/tmp/tameshi-r43-RevC2DoNothing-const/probe.py`,
deleted; output verbatim):

```
A: KeyError on 'm12' -> no line, non-zero exit
B: C2_R43: self_pin=1 classes=7 m6=0 m7=0 m8=0 m10=0 m11=0 m12=0 m13=0 total=0 records=3 sources_rows=113 C2_R43_PASS=true
```

Case B is decisive: a counter whose `m12`/`m13` entries are hardcoded `[]` — never computed — and
whose values are never passed through `m12_planned` / `m13_standing_command` still prints
`classes=7`, `m12=0`, `m13=0`, `total=0` and `C2_R43_PASS=true`. Therefore `classes=7` is
satisfiable by a counter with two dead classes: it carries **zero** evidential weight.

What actually prevents a dead-class counter, and is the honest evidence chain:
1. the seven keys are bound to values computed unconditionally at lines 403 (`m12_planned(block,
   round_no)`) and 406 (`m13_standing_command(scorcard, registry)`), with real `SCORECARD.md` /
   `corpus/SOURCES.md` bytes pulled at `rev`;
2. the field loop at line 412 and `total = sum(len(hits) for hits in classes.values())` at line 410
   index/sum all seven keys, so a counter that *drops* the keys dies with `KeyError` before any
   line is printed (probe case A) — note this is a crash, not an honest `C2_R43_PASS=false`;
3. `self_pin` over the pinned bytes (`counter_sha256=092c76cd…a8f286`) means the frozen seven-class
   code is the code that ran — on-disk sha equals the pin:
   ```
   092c76cd6e10f9280af21237ec90dc14e63f0bdb9ae74fffb9da841730a8f286  .ufo/evidence/round-43/calibration/measure.py
   ```
4. the allowed control fires both new classes:
   ```
   python3 .ufo/evidence/round-43/calibration/measure.py --selftest
   C2_R43_SELFTEST: cases=10 failed=0
   VERDICT: PASS
   exit=0
   ```
   (positive and negative cases for both: `T1_missing_planned_detected`, `T1_planned_present_clean`,
   `T2_indent_probe_load_bearing`, `T2_column_zero_standing_detected`, `T2_census_valid_standing_clean`);
5. the base run distinguishes the new classes from the carried five:
   `.ufo/evidence/round-43/before/c2-at-base.stdout` → `m12=1 m13=1 total=2 … C2_R43_PASS=false`
   (and `first=m12:Planned_(round_43)`).

Consequence for the round report: `classes=7` MUST NOT be cited as proof that seven classes ran.
Cite (3)+(4)+(5). Recommended round-44 hardening (not a freeze edit — the contract is frozen and
`amendments_note` forbids changing `claims.*`): `declared = len(classes)`, or make each class
return a `(ran, hits)` pair and gate `passed` on `all(ran)`; drop the docstring's "all seven ran"
parenthetical or make it true.

## Finding 2 — the do-nothing claim's named receipt does not exist (evidence, MEDIUM)

Contract line 54 names `.ufo/evidence/round-43/control/c2-round42-counter.stdout`. Exhaustive
search of the lane:

```
find /home/vgpnk/Projects/shokunin/tameshi-shokunin -name 'c2-round42-counter*' -print
(no output)
```

`.ufo/evidence/round-43/control/` contains only `c1-probe-survivors.stdout`,
`c1-round42-battery.stdout/.exit`, `c3-constant-empty.stdout/.exit`, `constant-empty-tool.py`. The
whole directory is untracked at the freeze (`git status --porcelain` → `?? .ufo/evidence/round-43/control/`;
`jj st` → same), as are `before/`, `sources/`, `census-sources/`; only
`calibration/measure.py`, `contract.json`, `guard/measure.py`, `mutants/measure.py` are tracked
under `.ufo/evidence/round-43/`. Round-42's control-era receipts *are* tracked
(`git ls-files .ufo/evidence/round-42/after` lists six), so the untracked state here is a
provenance gap for the round report: a receipt that is not in a rev cannot be read by `git show`
and cannot be pinned.

Mitigation (why this is not fatal): the claim itself is independently true — see Finding 3 — and
the equivalent round-42 artifact `.ufo/evidence/round-42/after/c1-at-242c1b4a.stdout` **is** tracked.
But that receipt is at `rev=242c1b4a`, not at the round-43 base/freeze, so it does not by itself
stand as the round-43 control run the contract names. The L1 should produce and commit the named
receipt (a round-42-counter run at `487b8f0`/`17f6ef0`) or amend the citation to a tracked file.

## Finding 3 — the claim "no m12/m13, no classes field, cannot produce the target" is TRUE

Source, `.ufo/evidence/round-42/calibration/measure.py:390-397`:

```
390: total = sum(count(mismatches, c) for c in ('m6', 'm7', 'm8', 'm10', 'm11'))
391: passed = total == 0 and n_records == EXPECTED_RECORDS
392: print('C1_R42: self_pin=1 m6=%d m7=%d m8=%d m10=%d m11=%d total=%d records=%d sources_rows=%d '
393:       'rev=%s freeze=%s C1_R42_PASS=%s'
...
```

- `total` is summed over exactly five class labels; there is no `m12`/`m13` computation anywhere in
  the file (`grep -n "m12\|m13\|classes"` matches only the docstring phrase "Mismatch classes" at
  line 18 — prose, not a field).
- The only printed prefix is `C1_R42:`, and the only verdict token is `C1_R42_PASS`.

Receipt, `.ufo/evidence/round-42/after/c1-at-242c1b4a.stdout` (exit `0`):

```
C1_R42: self_pin=1 m6=0 m7=0 m8=0 m10=0 m11=0 total=0 records=6 sources_rows=113 rev=242c1b4a1bb793d6ca4ac4e3b0da153767e78739 freeze=322b5cd32b4319a05340d249ae752d12a9e6b19f C1_R42_PASS=true
```

Field-for-field agreement with the source template; no `classes=`, no `m12=`, no `m13=`.

**Could a reader score the round-43 target from that line? No.** Token accounting against
`C2_R43_PASS=true: self_pin=1 classes=7 m6=0 m7=0 m8=0 m10=0 m11=0 m12=0 m13=0 total=0`:

| target token | on the round-42 line | note |
|---|---|---|
| `C2_R43_PASS=true` | absent (`C1_R42_PASS=true`) | wrong vintage |
| `self_pin=1` | present | pins round-42 bytes `9782a5a0…f914c0e`, not C2's `092c76cd…a8f286` |
| `classes=7` | absent | field does not exist |
| `m6=0 … m11=0` | present | carried classes, values 0 |
| `m12=0` | absent | class does not exist in this counter |
| `m13=0` | absent | class does not exist in this counter |
| `total=0` | present | **5-class sum**, not the 7-class sum; not transportable |

So 8 of 11 tokens match, but the three that distinguish the round-43 target (`classes=7`,
`m12=0`, `m13=0`) are unobservable, and `total=0`/`self_pin=1` are different quantities that
happen to share a spelling. The line can print `C1_R42_PASS=true` while the two new classes would
fail: the contract's own `before_state` asserts `m12=1 m13=1` at base, and
`.ufo/evidence/round-43/before/c2-at-base.stdout` confirms it (`m12=1 m13=1 total=2 …
C2_R43_PASS=false`). This is exactly what a do-nothing control must demonstrate.

## Finding 4 — target-string form is a predicate list, not the printed line (INFO, scoring risk)

The contract target is written `C2_R43_PASS=true: self_pin=1 classes=7 …` (PASS as header), while
the counter prints `C2_R43: self_pin=1 classes=7 … C2_R43_PASS=true` (PASS as trailer). A literal
substring search for the target string fails on the counter's own correct output. This matches the
house convention (round-42 target: `self_pin=1 m6=0 … C1_R42_PASS=true, exit 0, at the measurement
revision`), so it is not a defect of this round — but any scorer used for the deciding run must be
token-wise (key=value pairs + exit code), and the round report should say so.

## Finding 5 — `before/c2-at-base.stdout` carries `freeze=f0f2636`, not the declared freeze (INFO)

The base receipt reads `freeze=f0f26367a81bb71c2cd39eb51916886a99cf2fad`. The declared freeze is
`17f6ef0c72ec27e1aea305b5c95806b43bb2caef`. I checked that this does not weaken the claim: the C2
counter pin is byte-identical in both contract snapshots —

```
C2 pin at f0f2636: 092c76cd6e10f9280af21237ec90dc14e63f0bdb9ae74fffb9da841730a8f286
C2 pin at 17f6ef0: 092c76cd6e10f9280af21237ec90dc14e63f0bdb9ae74fffb9da841730a8f286
```

and equals the on-disk sha, so the before run used the frozen counter bytes (amendment A1 updated
the pin before that run; A1's pre-amendment first run printed `m7=7 m8=38 m10=9`, which is not this
receipt). Disclose the snapshot identity in the round report so the receipt's `freeze=` field is not
misread as a different contract.

## Residual risk

- `classes=7` remains in the frozen target and is still readable as a saturation claim. The
  counter's sha is pinned, so the actual frozen code does compute all seven; the risk is purely
  presentational — a round report or successor round citing `classes=7` as its evidence would be
  unearned. Round 44's counter should derive the count from the dict.
- The named control receipt is missing; if it is never produced, the round report's C2 control
  rests on the round-42 tracked receipt at `242c1b4a` plus source reading, which is weaker than the
  contract's citation promises.
- The untracked evidence directories (`control/`, `before/`, `sources/`, `census-sources/`) mean
  the deciding run's receipts will not exist at any rev unless committed.

## Verification gaps (what I did not do)

- I did not run any C2 measurement at any revision (base, freeze, or otherwise): the one deciding
  run belongs to the L1, and my item asked to read the printed fields, not to re-measure.
- I did not run the round-42 counter (its only valid `--rev` would be outside the round-43
  allowed set, and no C2 mode permits re-measuring it); its absence of m12/m13/`classes` is
  established by source inspection plus the tracked round-42 receipt, which agree.
- Tool installs: none needed, none performed.

Scratch `/tmp/tameshi-r43-RevC2DoNothing-const` deleted.

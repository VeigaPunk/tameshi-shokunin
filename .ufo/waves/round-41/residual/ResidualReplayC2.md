# Residual attack — C2 replay and record comparison (round 41)

Seat: `L1Tameshi41.ResidualReplayC2`. Read-only on the lane; the only write is this file.
Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, tip `812ee0d11d267e131be3dc8db0b71253cbae9234`,
measured commit `2ae00eb750b86eba6c9b54b36b1a6e875e9fd8a6`, base `a3d6c690bcbf8914551d4f4e8e1612784c1c2046`.
Ancestry checked: `baa18b7b` → `2ae00eb7` → `812ee0d1` (both `git merge-base --is-ancestor` return 0).
No tool installed or updated; nothing in `/tmp` was inside the lane tree.

Counter under test: `.ufo/evidence/round-41/census/measure.py`
(`sha256 83268eff97048cd4223a6f015b901c5efbde15d7b0d506bd40e5611b373ce94c` = `claims.C2.counter_sha256`).
Declared target: `claims.C2.target`, 22 `field=value` pairs.

## 1. Replay at the three revisions and the control

Every command below is the contract's counting command verbatim with the revision substituted.

**A. Measured commit** — `python3 .ufo/evidence/round-41/census/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 2ae00eb750b86eba6c9b54b36b1a6e875e9fd8a6`, exit 0:

```
C2_R41: tool_absent=0 tool_sha_ok=1 v2_sha_ok=1 selftest_exit=0 var_unflagged=1 var_expected=1 symlink_unflagged=1 symlink_expected=1 literal_unflagged=1 scratch_var_unflagged=0 v2_var_expected=0 v2_symlink_sites=0 live_var_lineno=811 live_var_resolved_v3=1 live_var_scratch_v3=1 live_var_sites_v2=1 live_var_expected_v2=0 live_symlink_lineno=820 live_symlink_resolved_v3=1 live_symlink_scratch_v3=1 live_symlink_sites_v2=0 mutant_resolve_killed=1 mutant_symlink_killed=1 mutant_symlink_arg_killed=1 rev=2ae00eb750b86eba6c9b54b36b1a6e875e9fd8a6 C2_R41_PASS=true
```

Byte-identical to the committed receipt `.ufo/evidence/round-41/after/c2-at-2ae00eb7.stdout` (compared
with `.strip()`): **PASS**.

**B. Tip** — same command, `--rev 812ee0d11d267e131be3dc8db0b71253cbae9234`, exit 0:

```
C2_R41: tool_absent=0 tool_sha_ok=1 v2_sha_ok=1 selftest_exit=0 var_unflagged=1 var_expected=1 symlink_unflagged=1 symlink_expected=1 literal_unflagged=1 scratch_var_unflagged=0 v2_var_expected=0 v2_symlink_sites=0 live_var_lineno=811 live_var_resolved_v3=1 live_var_scratch_v3=1 live_var_sites_v2=1 live_var_expected_v2=0 live_symlink_lineno=820 live_symlink_resolved_v3=1 live_symlink_scratch_v3=1 live_symlink_sites_v2=0 mutant_resolve_killed=1 mutant_symlink_killed=1 mutant_symlink_arg_killed=1 rev=812ee0d11d267e131be3dc8db0b71253cbae9234 C2_R41_PASS=true
```

Differs from A only in `rev=` (the counter echoes `args.rev`, `measure.py:286`). All 22 target fields
identical: **PASS**. `git show --stat 812ee0d1` touches only `.ufo/evidence/round-41/census/end.exit`
and `.ufo/waves/round-41/w1/ScribeScorecard.md`, so no C2 input can have moved.

**C. Base** — `--rev a3d6c690bcbf8914551d4f4e8e1612784c1c2046`, exit 1:

```
C2_R41: tool_absent=1 var_expected=0 symlink_expected=0 rev=a3d6c690bcbf8914551d4f4e8e1612784c1c2046 C2_R41_PASS=false
```

Equals `claims.C2.before` and `.ufo/evidence/round-41/before/c2-at-base.stdout` exactly: **PASS**
(the do-nothing control at base cannot pass).

**D. Control** — `python3 .ufo/evidence/round-41/census/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --control`, exit 1:

```
C2_R41_CONTROL: v2_var_expected=0 v2_symlink_sites=0 C2_R41_CONTROL_PASS=false
```

Equals `claims.C2.do_nothing_control` and `.ufo/evidence/round-41/control/c2-control.stdout`: **PASS**
as a negative control (`CONTROL_PASS=false` is the intended reading, disclosed at SCORECARD.md:1940).

## 2. Field-by-field: target vs every record source

Compared `claims.C2.target` (contract at `812ee0d1`; identical text at `2ae00eb7`, `baa18b7b`, `b37ce97`)
against SCORECARD.md's pasted deciding line, the `c2-at-baa18b7b.stdout` receipt, my measured run and my
tip run. Result: **22 target fields, 0 mismatches, 0 fields missing from the print**.

| field | declared | SCORECARD paste | receipt baa18b7b | my 2ae00eb | my tip |
|---|---|---|---|---|---|
| tool_absent | 0 | 0 | 0 | 0 | 0 |
| tool_sha_ok | 1 | 1 | 1 | 1 | 1 |
| v2_sha_ok | 1 | 1 | 1 | 1 | 1 |
| selftest_exit | 0 | 0 | 0 | 0 | 0 |
| var_unflagged | 1 | 1 | 1 | 1 | 1 |
| var_expected | 1 | 1 | 1 | 1 | 1 |
| symlink_unflagged | 1 | 1 | 1 | 1 | 1 |
| symlink_expected | 1 | 1 | 1 | 1 | 1 |
| literal_unflagged | 1 | 1 | 1 | 1 | 1 |
| scratch_var_unflagged | 0 | 0 | 0 | 0 | 0 |
| v2_var_expected | 0 | 0 | 0 | 0 | 0 |
| v2_symlink_sites | 0 | 0 | 0 | 0 | 0 |
| live_var_resolved_v3 | 1 | 1 | 1 | 1 | 1 |
| live_var_scratch_v3 | 1 | 1 | 1 | 1 | 1 |
| live_var_expected_v2 | 0 | 0 | 0 | 0 | 0 |
| live_symlink_resolved_v3 | 1 | 1 | 1 | 1 | 1 |
| live_symlink_scratch_v3 | 1 | 1 | 1 | 1 | 1 |
| live_symlink_sites_v2 | 0 | 0 | 0 | 0 | 0 |
| mutant_resolve_killed | 1 | 1 | 1 | 1 | 1 |
| mutant_symlink_killed | 1 | 1 | 1 | 1 | 1 |
| mutant_symlink_arg_killed | 1 | 1 | 1 | 1 | 1 |
| C2_R41_PASS | true | true | true | true | true |

Extra printed fields not named by `target`: `live_var_lineno`, `live_var_sites_v2`,
`live_symlink_lineno`, `rev` — additive only, no target field is absent.

Record-text checks, all **PASS**:

- SCORECARD.md:1972 pasted line is byte-identical to `after/c2-at-baa18b7b.stdout` (`==` on stripped text → True).
- SCORECARD.md's C2 table After cell (row at line 1913) carries a string byte-identical to `claims.C2.target`.
- LOG.md's C2 `Target:` restatement (`## 2026-10-25 — round 41`, C2 bullet) names the same 22 fields,
  no extras, no value differences.
- LOG.md's C2 `Before` line equals `before/c2-at-base.stdout` exactly.
- LOG.md's deciding line is an explicit ellipsis (`… mutant_resolve_killed=1 mutant_symlink_killed=1
  mutant_symlink_arg_killed=1 C2_R41_PASS=true`) — the three tokens it prints match the receipt; the
  elision is marked, not silent.

## 3. Pins verified independently of the counter

`claims.C2.tool_sha256` is read from the same revision's contract, so the run only proves
self-agreement (disclosed at SCORECARD.md:1935-1936). Verifying by hand across revisions:

```
rev        write-path-census-v3.py  write-path-census-v2.py  fixtures.json     census/measure.py
a3d6c690   (absent)                4022853295882c5a         (absent)          (absent)
d4ee4e63   095924a7a165be96        4022853295882c5a         a4123ce373447563  5d57c7097fb33a66
baa18b7b   095924a7a165be96        4022853295882c5a         20b6254d39a75fb9  83268eff97048cd4
2ae00eb7   095924a7a165be96        4022853295882c5a         20b6254d39a75fb9  83268eff97048cd4
812ee0d1   095924a7a165be96        4022853295882c5a         20b6254d39a75fb9  83268eff97048cd4
```

**PASS, and stronger than the record claims for the tool**: the tool bytes at the freeze commit
`d4ee4e63` are the tip bytes (`095924a7…ef0279`), so this round's tool demonstrably predates every seat
and every deciding run. v2 is byte-identical from base to tip (`40228532…d878b`, = the counter's
`V2_SHA` constant at `measure.py:30` and `claims.C2.v2_sha256`). Fixtures and counter changed once, at
`b37ce97`, exactly as amendment A2 declares (re-pins `a4123ce3`→`20b6254d`, `5d57c709`→`83268eff`).

Target monotonicity, freeze vs tip: 21 → 22 fields, `added now: ['mutant_symlink_arg_killed']`,
`removed now: []`. A2 tightened only; no target was relaxed and the kill rule is unchanged.

## 4. Mutant kill oracle (cheap independent probe)

The record's own caveat is that `killed` is `returncode != 0`, "so a traceback would count as a kill
(all three real mutants die on their own fixture class, receipted)" (SCORECARD.md:1938-1940). Reproduced
out of process from `git show 812ee0d1:tools/write-path-census-v3.py` into `/tmp/c2mut`:

```
=== base selftest ===  exit 0
WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=0
=== mutant resolve exit=1 ===
WRITE_CENSUS_V3_SELFTEST: var_unflagged=0 symlink_unflagged=1 literal_unflagged=1 scratch_var=0
FAIL planted var_unflagged: want unflagged=1 got 0
FAIL planted var_unflagged: want expected_sites=1 got 0
FAIL planted scratch_var: want expected_sites=1 got 0
=== mutant symlink exit=1 ===
WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=0 literal_unflagged=1 scratch_var=0
FAIL planted symlink_unflagged: want unflagged=1 got 0
FAIL planted symlink_unflagged: want expected_sites=1 got 0
=== mutant symlink_arg exit=1 ===
WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=0 literal_unflagged=1 scratch_var=0
FAIL planted symlink_unflagged: want unflagged=1 got 0
FAIL planted symlink_unflagged: want expected_sites=1 got 0
```

All three die on a printed `FAIL` line naming their own fixture class, stderr empty: **PASS** on the
receipted claim. `selftest_exit=0` at the rev is the same run (exit 0, four fixtures at their declared
values).

## 5. Findings

### DEFECT 1 (medium-low) — the record asserts a C2 self-pin that does not exist

SCORECARD.md:1943-1944, in the C1 limits paragraph:

> "the C1 counter has no self-pin clause (unlike C2, it does not hash its own bytes against `claims.C1.counter_sha256`)"

The parenthetical affirms that C2 *does* hash its own bytes against `claims.C2.counter_sha256`. It does
not:

```
$ grep -c 'counter_sha256' .ufo/evidence/round-41/census/measure.py
0
$ grep -c 'fixtures_sha256' .ufo/evidence/round-41/census/measure.py
0
$ grep -n 'tool_sha256\|V2_SHA' .ufo/evidence/round-41/census/measure.py
30:V2_SHA = '4022853295882c5a11e192274e9215ea5a008e54eb0a2f77a8a2365f522d878b'
146:            pin = json.loads(contract_blob.decode('utf-8'))['claims']['C2']['tool_sha256']
152:    v2_sha_ok = int(v2_blob is not None and hashlib.sha256(v2_blob).hexdigest() == V2_SHA)
```

The only digests the counter computes are the *tool* pin (read from the same revision, self-agreeing)
and v2 against a counter-side constant. The C2 limits paragraph four lines later contradicts the C1
paragraph by routing the missing check forward: "The successor counter — out-of-process tool
execution, **a counter-side digest constant**, `resolved` text inspection and an exit-plus-FAIL-line
kill oracle — is routed to round 42" (SCORECARD.md:1941-1942). Two statements in the same block cannot
both be true. The declared counter pin is *correct in fact* (`83268eff…ce94c` = the counter's sha256)
but nothing in either run checks it, so the C1/C2 symmetry the record draws is an overstatement of the
C2 instrument in the direction that matters. Fix is one clause: say both counters lack a self-pin.

### DEFECT 2 (low) — "printed the same lines" is false at the carrying commit

SCORECARD.md:1976-1978 and LOG.md:2183-2184 both state that the two commands re-ran at the commit
carrying the entry and "printed the same lines". The counter echoes its `--rev` argument verbatim
(`measure.py:286`), so the re-run at `2ae00eb7` cannot print the pasted line, whose `rev=` is
`baa18b7b`. The lane's own receipt proves the difference:

```
$ cat .ufo/evidence/round-41/after/c2-at-2ae00eb7.stdout
C2_R41: … mutant_symlink_arg_killed=1 rev=2ae00eb750b86eba6c9b54b36b1a6e875e9fd8a6 C2_R41_PASS=true
$ python3 …/census/measure.py --lane … --rev 2ae00eb750b86eba6c9b54b36b1a6e875e9fd8a6
C2_R41: … mutant_symlink_arg_killed=1 rev=2ae00eb750b86eba6c9b54b36b1a6e875e9fd8a6 C2_R41_PASS=true
$ [pasted SCORECARD line] == [c2-at-2ae00eb7.stdout]   ->  False
$ [pasted SCORECARD line] == [c2-at-baa18b7b.stdout]   ->  True
```

Every other token agrees, so this is a record-precision defect (a verifier comparing lines sees one
differing token), not a measurement defect:
`{k:(pasted, mine) for k in set(pasted)|set(mine) if pasted[k]!=mine[k]}` → `{'rev': ('baa18b7b…', '2ae00eb7…')}`.
The honest phrasing is "printed the same field values; only the echoed `rev=` differs".

This is exactly the class C1 exists to catch and cannot: C1 compares records against SOURCES/registry and
never compares a pasted counter line to a re-run of the counter that produced it.

### DEFECT 3 (low) — `--control` is neither revision-bound nor digest-checked

`measure.py:123` resolves the control's input as `args.fixtures or os.path.join(args.lane, FIXTURES)`:
the *working tree*, for a flag that takes no `--rev`; `--fixtures` substitutes any file. `claims.C2.fixtures_sha256`
is declared but never verified (see DEFECT 1 greps), so the control's printed verdict describes whatever
bytes the caller hands it. Demonstrated with an off-lane copy of the planted var fixture rewritten to
`open("expected.json", "w")`:

```
$ python3 .ufo/evidence/round-41/census/measure.py --lane … --control --fixtures /tmp/c2ctl/doctored-var.json
C2_R41_CONTROL: v2_var_expected=1 v2_symlink_sites=0 C2_R41_CONTROL_PASS=true
EXIT=0
```

versus the committed control output `C2_R41_CONTROL: v2_var_expected=0 v2_symlink_sites=0
C2_R41_CONTROL_PASS=false`, exit 1. So `claims.C2.do_nothing_control`'s phrase "on the same planted
fixtures" is true only by content, not by construction. Today the worktree copy is byte-identical to the
rev (`20b6254d` both sides), so no measured line moves; the hole is latent, and the fix is to read
fixtures through `git show REV:` in control mode and check `fixtures_sha256` once.

### PASS with note — A2 rewrote the target after seats had scored

`post_freeze_amendments` records `seats_had_scored: true` while every amendment carries `before_data: true`.
A2 (`found_by` seat `MutFixtureVar`) added `mutant_symlink_arg_killed` to `claims.C2.target` and re-pinned
fixtures and counter. Verified as declared: net field delta is +1 and −0, `rule_changed: true`, the
predicate's mutant clause went from "both" to "all three", and no deciding run preceded it
(`no_deciding_run_before: true`, first default-mode run at `b37ce97`). Nothing was relaxed, so the
mechanism is sound; the label "pre-data" means "before deciding-run data", which a reader can mis-take
for "before any seat ran" — the same wording load the round's C1 work is aimed at.

### PASS — no other honest-instrument defect found

Independently checked and consistent with the printed line: `live_var_lineno=811` is
`with open(duplicate_path, "wb") as handle:` with `duplicate_path` built from `"expected.json"`, under
`scratch/`; `live_symlink_lineno=820` is `os.symlink(` with both arguments under `snap_stable`/`scratch`
paths. On those exact lines the v2 patterns score `v2_write=1 v2_expected=0` (811) and
`v2_write=0 v2_expected=0` (820), so the predicate clause "v2 records no expected-value destination on
the same lines" holds *literally*, not merely via the counter's proxy. `grep -c 'os\.symlink'
tools/write-path-census-v2.py` → `0` (exit 1), as the record's unmoved command states. The four fixture
values the counter derives in-process equal the out-of-process `--selftest` output (the selftest's
`scratch_var` is the counter's `scratch_var_unflagged`), so the in-process
import disclosed at SCORECARD.md:1933-1936 did not distort any declared value.

## 6. Residual risk and verification gaps

- The counter's live half reads `expected/scratch/kind/lineno` and never the resolved text (disclosed);
  I did not attempt the constant-table forgery against it, only confirmed the disclosure is accurate.
- The candidate exploits I did not run: a tool that patches `subprocess.run` from inside `exec_module`
  (disclosed in-process limit), and a `returncode != 0` kill via traceback (checked the three shipped
  mutants only, not a synthetic traceback mutant).
- `--control`'s verdict polarity (`CONTROL_PASS=true` meaning "v2 succeeded, the round's premise failed")
  is disclosed at SCORECARD.md:1940 but no record spells the polarity out where the receipt is cited; a
  future reader could read `CONTROL_PASS=false` as an instrument failure. Not graded a defect — the
  disclosure is present in the same section.
- Nothing above changes C2's measured verdict: at both `2ae00eb7` and `812ee0d1` the counter prints all
  22 declared fields at their declared values and exits 0. C2 is **PASS as a capability acquisition**;
  DEFECT 1 and DEFECT 3 are instrument/record honesty defects, DEFECT 2 is record precision.

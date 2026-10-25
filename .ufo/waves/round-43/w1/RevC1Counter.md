# RevC1Counter — C1 counter line-by-line audit (round 43, w1)

Seat `L1Tameshi43.RevC1Counter`. Item: check `.ufo/evidence/round-43/mutants/measure.py` against
`contract.json` `claims.C1` line by line — exit-plus-FAIL oracle, K/D/E/U derivation, which
fixture each kill rests on, the name requirement, and whether the predicate can pass while a
survivor is only relabelled. Read-only; no lane write except this report. Scratch in
`/tmp/tameshi-r43-RevC1Counter/` (deleted). No installs (nothing to install; `pacman` not used).

Snapshot stamps: first measurement 07:52, final 08:01 (2026-10-25). **The lane moved twice while
this seat ran** (freeze `17f6ef0` → `5cd2154` → `53cb32b`); every claim below names the exact bytes
it refers to, because after 07:56 no "the lane counter is still `ad7ecf8c…`" statement is true.

Instruments audited (sha256):

| label | bytes | where |
|---|---|---|
| **FROZEN** (`ad7ecf8c…`) | `ad7ecf8c1c1ea1e84982eec5da6bb453ab5533eb6c4f0c09af5559f6ba6bc875` | the pin at the item's freeze `17f6ef0`, `contract.json:25` at that rev |
| **A5** (`901d947f…`) | `901d947fb912a6cbbcc2de8c876a72a55daa3ab6ca49e8e9c634aac041ccc7e0` | commit `5cd2154` (07:56:24) |
| **CURRENT** (`0d0f81bd…`) | `0d0f81bdbe09bb53997ade30911fc178a38de072f84aacf23c6c9c0a710e57f1` | worktree at 08:00:21, pinned by `contract.json:25` at HEAD `53cb32b` |

All three keep the same 12 fixtures (sha of each of F01–F12 identical across all three) and the
same `LIVE` tuple. Measurements only at the permitted `--rev` values; `--control` and
`--probe-mutant` used as controls.

---

## Verdict

1. **At the freeze the item names (`17f6ef0`, counter pin `ad7ecf8c…`) the C1 counter cannot
   produce its declared target.** It prints `C1_R43_PASS=false` at *both* permitted revs, for two
   independent reasons: `tool_sha_ok=0` (wrong pin source, §1) and `mutants_killed=6
   dead_code_only=0` (the D branch is unreachable as frozen, §2). The declared
   `mutants_killed=5 dead_code_only=1` split does not exist in those bytes.
2. **The claim's substance is nevertheless true.** Measured out-of-band (§5):
   `outflag_no_parse_args_check` diverges from pristine on F11 only (reachable), and
   `method_fold_several_returns` on F12 only (dead-code). So the two survivors are resolved the
   way the contract says — but the frozen counter does not certify it, and nothing in its printed
   line says *which* fixture killed what.
3. **The lane re-froze the instrument twice during wave 1** (A4/A5 at 07:56, A9 at 08:00). The A5
   bytes reach the target's substantive fields; A9 additionally repairs the `--probe-mutant`
   mislabel and the live-site kill hole. The contract's own `amendments_note` ("counters …
   byte-unchanged") is contradicted by both. A deciding run must name an exact freeze rev whose
   pins equal the executed bytes; at `17f6ef0` that run is a guaranteed `false`.

---

## 1. FROZEN — `tool_sha_ok=0` (blocking). Wrong pin source.

`mutants/measure.py:486` compares the census tool's blob to the contract's **single top-level**
pin:

```python
tool_sha_ok = 1 if tool_raw is not None and sha(tool_raw) == contract['tool_sha256'] else 0
```

At `17f6ef0` `contract['tool_sha256']` is the **staged-id-guard** pin
(`contract.json:68`: `8140945a…`; at HEAD the same key is the repaired guard pin
`efa5f129…`/`e219007…` — never the census tool), while the tool the C1 counter measures is
`tools/write-path-census-v4.py`, whose own pin is `frozen_tools['tools/write-path-census-v4.py']`
= `784de4c0…` (`contract.json:69-70`). The counter never reads `frozen_tools` (no occurrence of
that key in the FROZEN bytes).

Measured instead of `1`:

```
C1_R43: … tool_sha_ok=0 … C1_R43_PASS=false
```

Verified hashes:
```
784de4c0…  git show 17f6ef0:tools/write-path-census-v4.py | sha256sum
8140945a…  git show 17f6ef0:tools/staged-id-guard.py | sha256sum   # == contract tool_sha256
ad7ecf8c…  sha256(frozen bytes)                                     # == contract C1 counter_sha256
```

The predicate `:595` and the target (`contract.json:23`) both require `tool_sha_ok=1`, so **the
frozen C1 predicate is unsatisfiable at both permitted revs regardless of the fixtures.** This
duplicates `RevProvenance.md` §5 (which also shows the line was already wrong at the original
freeze commit `697d2f1`, so A4 did not cause it, contrary to A5's narration). Independently
reproduced here from immutable git bytes.

## 2. FROZEN — `mutants_killed=6 dead_code_only=0` (blocking). D is not derived.

The declared rule (`measure.py:14-17`):
> K … produces at least one FAIL … **The killing fixture must contain no runtime-unreachable
> statement** … D — a mutant that **survives K** is `dead_code_only` when every case on which it
> differs from the pristine tool is a fixture whose source contains a statement after an
> unconditional `return`/`raise`.

What the code does (`:546-562`):

```python
mf, me, _, _, _, _ = battery(path, work)      # :546  — twelve fixtures, F12 included
if me: runtime_error.append(name); continue   # :547
if mf: killed.append(name); continue          # :550  — any FAIL ⇒ killed, no reachability check
differ = differential(tool_path, path, work)  # :553  — D only ever reached here
```

`battery()` is called with its default `skip_dead_code=False`; the parameter exists
(`:333`) with a branch (`:341`) that would exclude `DEAD_CODE_FIXTURE`, and **no call site ever
passes it** (grep: only the definition and the branch). F12 is therefore part of the K battery,
and F12's declared classification is the pristine output, so any mutant that diverges on F12
fails it and is classified `killed` before the differential is computed. D is unreachable for
every declared mutant.

Measured (`--rev 17f6ef0 --freeze 17f6ef0`, base run differs only in the `rev=` field):

```
C1_R43: self_pin=1 tool_absent=0 tool_sha_ok=0 selftest_exit=0 fixtures_pass=12/12 run_errors=0
live_ok=3/3 live_unflagged_v4=0 live_tool_errors=0 mutants_declared=6 mutants_killed=6
dead_code_only=0 equivalent=0 not_killed=0 runtime_error=0 apply_error=0 unresolved=0
killed_names=attr_bind_several_assignments,attr_never_resolve_self,method_fold_disabled,
method_fold_several_returns,outflag_dests_never_recorded,outflag_no_parse_args_check
dead_code_names= dead_code_cases= dead_code_arg_ok=0 kill_fixture_reachable=1
rev=17f6ef0… freeze=17f6ef0… C1_R43_PASS=false
EXIT=1
```

Two consequences beyond the count:

* The run **violates the frozen K sentence** and does not notice: the only fixture that fails for
  `method_fold_several_returns` is F12, whose source `unreachable_statements()` returns
  `['module.body[1].body[0][1]']`. A kill resting on unreachable code is counted as a kill.
* `dead_code_arg_ok=0` follows mechanically (`:567` needs `dead_code_cases[name] == ['F12…']`,
  and `dead_code_cases` is never populated).

If the K stage excludes F12 — the rule's own "survives K" semantics, and what `skip_dead_code`
was written for — the same mutant becomes the declared D class. Measured by importing the frozen
module and calling its own functions with `skip_dead_code=True`:

```
method_fold_several_returns  fails=[]            differ=[('F12_method_two_returns','dead_code')]
outflag_no_parse_args_check  fails=['F11…']      differ=[('F11_outflag_namespace','reachable')]
```

So the defect is dispatch, not judgement. (Cross-ref: `MutC1F12.md` reaches the same conclusion
from the other side and records the A5 repair; `CritC1DeadCode.md` proves the dead-code judgement
itself.)

## 3. FROZEN — `kill_fixture_reachable` is a constant, not a measurement (high)

`:568-569`:

```python
kill_fixture_reachable = 0 if unreachable_statements(
    FIXTURES['F11_outflag_namespace'][0]) else 1
```

This reads a literal in the counter and evaluates to `1` unconditionally (F11's source has no
dead statement). It is independent of the run: it is `1` even on the run above, where the counter
just printed a kill resting on F12. The predicate (`:603`) consumes it, so the K rule's
reachability sentence is *asserted by construction*, not tested. There is also no name → kill
fixture binding anywhere: the predicate checks `outflag_no_parse_args_check ∈ killed` but never
that its failing fixture is F11. §6 turns this into the relabel answer.

## 4. FROZEN — `--probe-mutant` contradicts the contract's D class (medium)

Docstring `:44`: "`--probe-mutant PATH` scores one mutant file under the same oracle". The probe
path (`:497-502` in the FROZEN bytes) computes `verdict = 'killed' if not errors and fails else
…` — no differential, no D branch. Measured on the D survivor:

```
$ … --probe-mutant /tmp/…/method_fold_several_returns.py
C1_R43_PROBE: verdict=killed failures=1 errors=0 first=['F12_method_two_returns expected=1 want 0']
EXIT=0
```

The contract says this mutant is `dead_code_only`; the probe certifies it as a **kill**, exit 0.
A falsifier seat using the probe gets the opposite of the claim. (`CritC1DeadCode.md:145-146`
reports this output as an "allowed control" without flagging the contradiction.)

## 5. What each kill actually rests on (measured; the counter never prints it)

The FROZEN counter prints only aggregate counts and `killed_names`/`dead_code_names`; unlike the
round-42 counter (`MUTANT name class= outcome= detail=`), there is no per-mutant line. Provenance
was measured by importing the FROZEN module and running its own `run_tool`/`check_site`/
`differential` over all 12 fixtures per mutant (scratch only; nothing re-implemented):

| mutant | failing fixture(s) | fingerprint divergence | class per rule |
|---|---|---|---|
| `attr_bind_several_assignments` | F03 | F03 reachable | killed |
| `attr_never_resolve_self` | F01 | F01,F02 reachable | killed |
| `method_fold_disabled` | F01 | F01,F02,F03 reachable | killed |
| `method_fold_several_returns` | **F12** | **F12 dead_code** | **dead_code_only** (frozen prints killed) |
| `outflag_dests_never_recorded` | F04 | F04 reachable | killed |
| `outflag_no_parse_args_check` | **F11** | **F11 reachable** | **killed** ✔ |

So the claim "`outflag_no_parse_args_check` … killed by `F11_outflag_namespace`" is factually
correct, and F11 is single-source (corroborated by the `--control` run: 10 fixtures → 4 killed,
exactly the two survivors missing; and by `MutC1F11.md`'s ablation). It is **not certified by the
counter's own output** — §3/§6.

`--control` reproduces the contract's do-nothing control exactly:
```
C1_R43_CONTROL: battery=round42_ten_fixtures fixtures_pass=10/10 mutants_declared=6 mutants_killed=4 C1_R43_CONTROL_PASS=false
```
Byte-identical to `.ufo/evidence/round-43/control/c1-round42-battery.stdout`. Control (3), the
receipt `control/c1-probe-survivors.stdout`, is weaker evidence than it reads: two lines
`PROBE outcome=survived detail=` with round-42's `C2_R42_CONTROL … freeze=322b5cd…` trailer and
**no mutant name**, so it cannot bind either survivor's identity. It also is untracked.

## 6. Can the predicate pass while a survivor is only relabelled? — Yes, on the K side
##    (frozen and A9 instruments; K-side closed by A11, §13.1)

The D side is *mostly* bound: the predicate requires `dead_code_only==1`,
`method_fold_several_returns ∈ dead_code_names`, and `dead_arg_ok==1` with the differing case
list exactly `['F12_method_two_returns']` (`:599-603`, `:567`). A survivor cannot be quietly
dropped or swapped into another fixture's dead-code case.

The K side is **not** bound, in three independent ways:

1. `kill_fixture_reachable` is a constant (§3): a kill resting on *any* fixture — including the
   dead-code fixture — still prints `kill_fixture_reachable=1`.
2. No name → fixture binding: the predicate would pass identically if
   `outflag_no_parse_args_check` were killed by F04 or F05 (both reachable outflag fixtures)
   instead of F11. The claim "killed by F11" is never a predicate term.
3. The counter pins the mutant *names* and count (`len(mutants)==6`, `:598`) but not the mutant
   `find`/`replace` bytes. `mutants.json` is read at REV with no sha check; the contract's
   `mutant_set` field cites the path only. A re-declared entry with the same name but an edit that
   diverges on F05 would satisfy counts, names and `dead_arg_ok`, and pass. In fact the file is
   byte-identical at base and freeze (`b3abab06a48d41535aa35bc520d0884489cb684a7a52b5369c2aadc3db430358`),
   so the claim holds — but the instrument does not certify "the round-42 mutant declaration
   unchanged".

On the D side the residual relabel is *reason*, not *slot*: `dead` is keyed on
`unreachable_statements(fixture_source)` (`:556`), i.e. on the fixture file, not on the mutated
construct. Any mutant whose sole divergence is on F12 gets `dead_code_only` whether the divergence
comes from the unreachable second `return` or from F12's reachable first `return`. For the declared
mutant the cause *is* the dead construct (verified: divergence is exactly
`expected=false→true`, `unflagged=false→true`, `resolved` gains the folded first-return text),
but that causation is asserted by the rule's wording, not measured.

## 7. Target line vs printed line — no run prints the declared target verbatim (medium)

`contract.json:23` (identical text at freeze and HEAD) declares 15 named fields plus the
`C1_R43_PASS=true:` prefix (16 tokens). On a green run the counter appends 24 named fields plus
`C1_R43_PASS` (25 fields; 26 on a run error, which adds the conditional `first_error` — FROZEN
`:571-594`, predicate `:595-603`; A9 `:593-617`, predicate `:618-625`). Named fields the counter
always prints and the target omits (9):

`live_tool_errors`, `not_killed`, `runtime_error`, `apply_error`, `killed_names`,
`dead_code_names`, `dead_code_cases`, `rev`, `freeze` — plus the conditional `first_error`, so
the named-field gap is 9 on a green run and 10 on a run error.

The flag itself is not absent — it is displaced: the target carries it as the
`C1_R43_PASS=true:` prefix; the counter prints it at the end.

The target's last two fields are also in the **opposite order** to the counter's
(`… kill_fixture_reachable=1 dead_code_arg_ok=1` vs printed `… dead_code_arg_ok=1
kill_fixture_reachable=1`). So the target is neither a substring nor a field-subsequence of any
actual run; a report claiming "the target line is reproduced" must be matching a hand-assembled
projection. (Compare C3's target, which lists every printed field.) The target also omits the
three U sub-counts although `unresolved` is their sum, so a reader cannot tell from the target
line alone which U class fired.

## 8. A5 instrument (`901d947f…`, commit `5cd2154`) — measured

After A4/A5 the pin source and the K gate are repaired (`:490-495`, `:555-560`:
`reachable_fails = [case for case in mdetail if not mdetail[case]]; if mf and reachable_fails`).
Measured with the item's freeze as pin source (so `self_pin` is expected to fail):

```
C1_R43: self_pin=0 tool_absent=0 tool_sha_ok=1 … fixtures_pass=12/12 … mutants_killed=5
dead_code_only=1 equivalent=0 … dead_code_names=method_fold_several_returns
dead_code_cases=F12_method_two_returns dead_code_arg_ok=1 kill_fixture_reachable=1 … C1_R43_PASS=false
```

Every target field except `self_pin` now matches. `self_pin=1` would require `--freeze 5cd2154`,
which is outside this seat's permitted revisions — **not measured**; by pin arithmetic it is
`[INFERENCE]` true at that freeze.

Two residual defects in the A5 bytes, both since closed by A9:

* probe still printed `verdict=killed` for the D survivor (same output as §4);
* the K gate's `mdetail` held only fixture failures, so a live-site-only failure fell through to
  `differential()` (fixtures only) and was labelled `equivalent`. Measured inputs: a mutant of
  `_record`'s `expected = …` guarded by `lineno < 1000` gives
  `fails=['tools/context-capture.py:1682 …','…:1685 …'] detail={} differ=[]` → `equivalent`.

## 9. A9 instrument (`0d0f81bd…`, first at `273c047`; the worktree at 08:00–08:01, HEAD then `53cb32b`)
##    — superseded by A11 `b56a34d7…` at `b510ad1` (08:06), §13.1

A9 (`mutants/measure.py:377`) now records live failures in `detail` as reachable, and the probe
(`:511-521`) applies the gate. Measured:

```
$ … --rev 17f6ef0 --freeze 17f6ef0 --probe-mutant …/method_fold_several_returns.py
C1_R43_PROBE: verdict=dead_code_only failures=1 reachable_failures=0 errors=0 first=['F12_method_two_returns expected=1 want 0']
EXIT=1
$ … --rev 17f6ef0 --freeze 17f6ef0 --probe-mutant …/outflag_no_parse_args_check.py
C1_R43_PROBE: verdict=killed failures=1 reachable_failures=1 errors=0 first=['F11_outflag_namespace explicit_out=1 want 0']
EXIT=0
$ … --rev 17f6ef0 --freeze 17f6ef0
C1_R43: self_pin=0 tool_absent=0 tool_sha_ok=1 … mutants_killed=5 dead_code_only=1 …
dead_code_names=method_fold_several_returns dead_code_cases=F12_method_two_returns
dead_code_arg_ok=1 kill_fixture_reachable=1 … C1_R43_PASS=false
```

So §4 and the live-site hole are already fixed in these A9 bytes. Still present in **these A9
bytes** (`0d0f81bd…`): the constant `kill_fixture_reachable` (`:589-590`, unchanged in intent),
the unbound kill provenance and unpinned mutant bytes (§6), and the fixture-keyed D reason (§6) —
all three closed or tightened by A11 (`b56a34d7…`, §13.1) — plus the target/output field mismatch
(§7, still present under A11).
does not trip `check_site` — for the declared set that holds (measured), but it depends on F12's
`want` being the pristine output; `MutC1F12.md` §4 shows any `want` flip turns F12 into a kill
fixture again, which is why the reachability gate (not the `want`) is the load-bearing fix.

## 10. Freeze churn (governance; affects every C1 receipt)

Observed timeline, all from git/lstat (no lane writes):

| time | event |
|---|---|
| 07:46:59 | `697d2f1` freeze: contract + 3 counters + guard; top-level `tool_sha256` already the guard pin |
| 07:48:57 | `17f6ef0` freeze A2/A3 — **the item's freeze**; C1 counter `ad7ecf8c…` |
| 07:49 | C1 control receipts written; 07:55:39 `MutC1F11.md` records "lane counter's bytes … `ad7ecf8c…`" |
| 07:56:24 | `5cd2154` "freeze A4/A5": C1 counter rewritten, C1/C3 pins and `tool_sha256` re-written |
| 07:56:54 | C2 counter edited on disk, unpinned at that moment |
| 07:57:50 / 07:58:28 | guard tool rewritten twice (unpinned at those instants) |
| 07:59:46 | contract rewritten again (A6–A8 + later A9), C2 pin moved |
| 08:00:21 | C1 counter rewritten again (`0d0f81bd…`) |
| 08:00:35 | HEAD `53cb32b`; worktree dirty for `mutants/measure.py`, `guard/measure.py`, `tools/staged-id-guard.py` |

Consequences for C1 reporting:

* Any receipt or seat statement asserting the lane bytes are still the freeze pin, written after
  07:56, is stale (`MutC1F11.md`, `MutC1F12.md` §1's "lane file, untouched", `CritC1DeadCode.md`).
  Their *measurements* remain valid because they ran saved copies of `ad7ecf8c…`; the "unchanged"
  wording is not.
* A deciding run must name the freeze rev whose contract pins equal the executed bytes. At
  `17f6ef0`: `C1_R43_PASS=false`, deterministically, for §1 and §2. At HEAD the working pair is
  self-consistent (`:25` pins `0d0f81bd…`), but the instrument is no longer the frozen one and the
  round-42-era controls were not re-run on it.
* The contract's `amendments_note` at `17f6ef0` (`contract.json:100`) says post-freeze amendments
  leave "counters … byte-unchanged"; A4/A5/A9 change two counters, the guard tool and the pins.
  The note has since been rewritten (HEAD `:140`), but the freeze-rev text is what a reader of the
  freeze rev sees. (Cross-ref `RevProvenance.md` §6.)

## 11. What does hold (checked, no defect)

* Oracle: the FROZEN `run_tool`/`battery` are behaviourally the round-42 exit-plus-FAIL oracle
  (non-zero exit, `Traceback` or unparseable JSON ⇒ `runtime_error`; a FAIL requires exit 0 and
  parseable output; `errors` outranks `fails`). The only textual difference is the truncated
  error tail. `check_site` requires exactly one site at the declared line and all four bits plus
  the `resolved` needle.
* Fixtures: F01–F10 sources byte-identical to the round-42 counter (per-fixture sha match), so
  "the ten round-42 fixtures unchanged" holds; `LIVE` is identical too. F11's declared line 8 is
  the `write_bytes` in `publish`; F12's line 11 is the `with open(self.destination(), …)`.
* `mutants.json` byte-identical at base and freeze (`b3abab06…`), six distinct names, each
  `find` applies exactly once (measured `apply_error=0` on every run above).
* Name requirement: implemented as intended (`kill_names`/`dead_names` exact containment,
  `:601-602`), but unsatisfiable at the freeze because `dead_names` is empty (§2).
* `fixtures_pass=12/12`, `live_ok=3/3`, `live_unflagged_v4=0`, `selftest_exit=0` at both permitted
  revs.

## 12. Residual risk / verification gaps

* I did not run any counter at a rev other than `487b8f0` (base) and `17f6ef0` (freeze). The
  A5/CURRENT `self_pin=1` at their own freezes is `[INFERENCE]` from the pin arithmetic, not
  measured.
* §9 is a snapshot at 08:00–08:01; the lane was editing `mutants/measure.py` during this seat
  (07:56, 08:00). Line numbers in §9 refer to `0d0f81bd…`.
* The §6 relabel path (a re-declared mutant entry with the same name) is a structural argument
  from the code; I did not build a full alternative `mutants.json` measurement (it would require
  editing or shadowing the lane's declaration at a rev).
* Death by fixture-keying (§6, second part) is likewise structural: I could not construct a
  reachable-only mutation whose sole fingerprint divergence is F12 in a bounded time (two attempts
  changed nothing because pristine already refuses to fold F12's method: `differ=[]`).
* No tool installs or upgrades were needed; no `pacman` transaction was run.

---

## 13. Addendum (08:05) — newest state, and the contract's `frozen_before` names a different instrument

Independent corroboration from `RevProvenance` (08:04): same 16/26 field gap, and **no hash of
`mutants.json` is pinned anywhere in the contract** (only the path in `claims.C1.mutant_set`),
which confirms §6(c) at the pin level.

Newest observed state (08:04:57):

| artifact | value |
|---|---|
| HEAD | `e20cf89` |
| `contract.json` | sha `9e24154a093c781e…`, amendments A1–A10 |
| C1 counter | `0d0f81bd…` (unchanged since 08:00:21; `claims.C1.counter_sha256` matches it) |
| C1 tool pin | `frozen_tools['tools/write-path-census-v4.py']` = `784de4c0…` (stable) |
| top-level `tool_sha256` | `2e8f2e89…` (guard; moved again from `365bf958…`; C1 no longer reads it) |

The contract's `frozen_before` now declares "the freeze of record is `114ffacd…`, reached through
`697d2f1` → `f0f2636` → `17f6ef0` → `5cd2154` → `114ffacd`". That sentence is **not consistent
with the same contract's own C1 pin**:

```
114ffacd : claims.C1.counter_sha256 = 901d947f…   and   114ffacd:mutants/measure.py = 901d947f…
e20cf89  : claims.C1.counter_sha256 = 0d0f81bd…   and   e20cf89 :mutants/measure.py = 0d0f81bd…
```

A8–A10 (including A9's C1 repairs and A10's pins) landed after `114ffacd`, so the named freeze of
record **predates the instrument the contract pins**. Consequences:

* `--freeze 114ffacd` with the current bytes prints `self_pin=0` for C1 (and, per
  `RevProvenance`, for C2/C3) — i.e. following the contract's own `frozen_before` sentence
  produces a guaranteed `C1_R43_PASS=false` without any measurement being wrong.
* The only self-consistent pair for the current counter is `--freeze 3aee2c0` or `--freeze
  e20cf89` (both pin `0d0f81bd…` and `tool_sha256=2e8f2e89…`). The deciding run must name one of
  those; `114ffacd` and `17f6ef0` cannot both name the executed bytes.
* `--freeze 114ffacd` with that freeze's *own* counter bytes (`901d947f…`, i.e. the §8 instrument)
  is self-consistent and reaches every target field except `self_pin` when the pin source is
  older, but that instrument lacks A9's probe/live-site repairs.

So the freeze chain has been rewritten five times (07:46 → 07:48 → 07:56 → 07:59 → 08:04), and the
"freeze of record" sentence was added *after* the pins it claims to freeze. This is the largest
reproducibility risk in the round: from the contract at HEAD alone, a reader cannot tell which
counter bytes the deciding run executed unless the run names the exact rev.

§9's line numbers refer to `0d0f81bd…`, still the current bytes at 08:04:57, so those citations
remain valid.

### 13.1 (08:07) — pin matrix verified, A11 closes §3 and §6(c), stale `frozen_before` survives

Pins read from each commit's own `contract.json` (`claims.*.counter_sha256`, `claims.C1.mutants_sha256`,
top-level `tool_sha256`; short shas):

| commit | C1 counter | C2 counter | C3 counter | guard pin | `mutants_sha256` |
|---|---|---|---|---|---|
| `114ffacd` (A6/A7; declared "freeze of record") | `901d947f` | `52961c37` | `8c8147e7` | `365bf958` | absent |
| `273c047` (A9) | `0d0f81bd` | `52961c37` | `ae66342d` | `e219007f` | absent |
| `3aee2c0` (A10) | `0d0f81bd` | `97609511` | `ae66342d` | `2e8f2e89` | absent |
| `e20cf89` (receipts) | `0d0f81bd` | `97609511` | `ae66342d` | `2e8f2e89` | absent |
| `b510ad1` (A11, 08:06) | `b56a34d7` | `97609511` | `ae66342d` | `2e8f2e89` | `b3abab06` ✔ |

This confirms §13 with exact bytes: the declared freeze of record predates the current C1
instrument by **three freeze commits** (A9, A10, A11). At `b510ad1` the `frozen_before` sentence
is unchanged — it still names `114ffacd` and still says wave-1 attacks "produced A4-A7", although
A8–A11 also came from wave-1 seats. So following the contract's own instruction still yields
`self_pin=0`.

**Correction to §10 (authoring windows, not divergence).** The worktree states I flagged as
"unpinned at that moment" were each committed verbatim as the next pin (`C2 52961c37` and guard
`365bf958` → A6/A7; `C1 0d0f81bd` → A9; `C2 97609511` and guard `2e8f2e89` → A10 — confirmed by
`RevProvenance`). The accurate statement is that the *pin* lags the worktree during an authoring
window; the bytes are accounted for. The consequence I recorded (a run made inside the window
reads `self_pin=0`) is unchanged.

**A11 closes two findings at the counter level** (current bytes `b56a34d7…`, contract `35a296a0…`):

* §3 (constant reachability field). `kill_fixture_reachable` is gone from both print and predicate.
  `kill_cases` (`:566`, populated `:583` with the *reachable* failing fixtures of a killed mutant)
  feeds `kill_binding` (`:601`): it is `1` only when the killed outflag mutant's reachable failing
  set is exactly `['F11_outflag_namespace']`. Measured provenance for that mutant is exactly
  `['F11_outflag_namespace']`, so the field now measures the claim instead of asserting it, and a
  kill that shifted to F04/F05 would print `kill_binding=0`.
* §6(c) (unpinned mutant declaration). `mutants_sha_ok` (`:561-562`) compares
  `sha(mutants.json at REV)` with `claims.C1.mutants_sha256` (`b3abab06…`, equal to the blob at
  BASE and FREEZE); it is printed (`:625`) and is a predicate term (`:638`).
  So a same-named re-declared entry can no longer pass. The K-side relabel path of §6 is closed.

What remains from §6 is the D-side, which `RevReportDraft` independently recorded as F1.6: `dead`
is still `unreachable_statements(fixture_source)` (`:586` in these bytes) — fixture-keyed, not
construct-keyed — so a divergence on a *reachable* construct inside a fixture that merely contains
unrelated dead code is still excused as `dead_code_only`. `dead_arg_ok` pins the fixture name only.

**Remaining target/output gap** in `b56a34d7…` vs the updated target (A11 added `mutants_sha_ok`
and `kill_binding`, dropped `kill_fixture_reachable`; measured by parsing the target and the
`fields.append` order):

* target 16 named fields plus the `C1_R43_PASS=true:` prefix (17 tokens); printer appends 26
  named fields + `C1_R43_PASS` = 27 on a green run (28 with the conditional `first_error`, `:643`);
* 10 named fields the counter always prints and the target omits: `live_tool_errors`,
  `not_killed`, `runtime_error`, `apply_error`, `killed_names`, `dead_code_names`,
  `dead_code_cases`, `kill_cases`, `rev`, `freeze` (plus the conditional `first_error` on a run
  error, and `C1_R43_PASS` displaced from target prefix to end-of-line);

So the target is still a projection of the run line, not the run line; no invocation reproduces it
verbatim.

**Surviving hazard** (agrees with `RevProvenance`): stale `frozen_before`. A deciding run must use
`--freeze 3aee2c0`/`e20cf89` for the A10 instrument or the A11 commit (`b510ad1`) for `b56a34d7…`;
`114ffacd` and `17f6ef0` cannot both name the executed bytes.

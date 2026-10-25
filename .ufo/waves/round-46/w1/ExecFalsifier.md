seat: ExecFalsifier
item: built `.ufo/evidence/round-46/quality/no-harm-gate.py` (the executable behind draft QUALITY criterion 88) and falsified it twice — a red monitor (the round-44 record-agreement counter, `C2_R44_PASS=false` at base) makes it exit 1 with `RED r44-record-agreement`, and a contract whose `no_harm` text stops declaring a monitor makes it exit 1 with `RED coldread`.

# Deliverable

`.ufo/evidence/round-46/quality/no-harm-gate.py` — 555 lines, sha256
`11044f5510df8bf7cc5f2e0a9bbf3c06983de7cc9cc87ae8ffe278ad9f829f6a`
(`sha256sum .ufo/evidence/round-46/quality/no-harm-gate.py`). New directory
`.ufo/evidence/round-46/quality/`; nothing else in the lane was written (see *Read-only
footprint*).

```
python3 no-harm-gate.py --contract CONTRACT.json --lane LANE --rev REV [--monitors-file F] [--timeout S]
python3 no-harm-gate.py --list          # the hard-coded mapping as JSON
python3 no-harm-gate.py --selftest
```

## What it does

1. Reads `CONTRACT.json` and requires a non-empty string `no_harm`; a contract without one is
   refused (`RED contract`), so the gate cannot pass against a contract that declares no
   obligation.
2. Resolves the monitors list, in this order: `--monitors-file F` as JSON
   (`{"monitors": [...]}`); `--monitors-file F` as a shell script (run `bash F LANE REV` and
   parse its `NOHARM <name> <observed> <ok|RED>` lines — this is how
   `.ufo/evidence/round-46/no-harm.sh` is consumed as "the real list"); with no file, the
   hard-coded `DEFAULT_MONITORS` mapping of the six monitor names of `no-harm.sh` to their
   commands, expectations and the contract phrase each one discharges.
3. Verifies `LANE` is a directory and `REV` resolves (`git rev-parse --verify --quiet`), then
   runs every monitor command with `bash -c` in `LANE` with `LANE`/`REV` in the environment.
   Children get `PYTHONDONTWRITEBYTECODE=1` and `GIT_OPTIONAL_LOCKS=0`; the gate itself opens
   no file for writing in the lane.
4. Prints one line per monitor in the format `no-harm.sh` already uses —
   `NOHARM <name> <observed> <ok|RED>` — then one `RED <name>` + `WHY <name> <reasons>` pair per
   failing monitor, then the tally and `NO_HARM_GATE_PASS=true|false`.
5. Exits 0 iff every monitor printed ok; 1 otherwise; 2 only for argparse misuse.

A monitor is ok only when all of these hold: it finished, its exit code was 0, and its
declared expectation held — `expect` (exact match on stdout, trailing newlines stripped, i.e.
the `[ "$D" = "..." ]` comparison `no-harm.sh` makes), `expect_contains` (every substring
present), `expect_min` (last integer ≥ bound), or, when none is declared, a last non-empty line
ending in `ok`. A non-zero exit is a refusal even when the token matched (selftest
`json-nonzero-exit`); an empty monitors list is a refusal, not a vacuous pass (selftest
`json-empty-list`); a malformed entry is refused, never skipped (selftest
`json-malformed-entry`); an unresolvable revision is a refusal (selftest
`revision-unresolvable`).

## The hard-coded mapping (`--list`), and the phrase each monitor discharges

| monitor | expectation | `contract.json` `no_harm` phrase |
|---|---|---|
| `commandD` | exact `recorded_cases=9 depth_score=9` | `command D 9` |
| `coldread` | exact `score=6 box3_full_page=False` | `coldread restraint 6` |
| `r45-freshness` | exact `population=73 fresh=71 C1_R45_PASS=true ` | `fresh=71` |
| `r45-coverage` | exact `rows=2 entries=2 C2_R45_PASS=true ` | `rows=2 entries=2` |
| `S160-count` | exact `1` | `S160 count 1` |
| `registry-rows-not-below-117` | `expect_min` 117 | `registry rows not below 117` |

Commands are `no-harm.sh`'s fragments verbatim, except that each prints its observed value
instead of doing `[ "$D" = "..." ] && s=ok || s=RED` inside the shell: the gate makes that
comparison itself, so a red monitor is *named* rather than only printed.

# Selftest tally (verbatim)

```
$ TMPDIR=/tmp/tameshi-r46-ExecFalsifier python3 .ufo/evidence/round-46/quality/no-harm-gate.py --selftest
SELFTEST json-all-ok                rc=0 want=0 PASS
SELFTEST json-expect-mismatch       rc=1 want=1 PASS
SELFTEST json-token-missing         rc=1 want=1 PASS
SELFTEST json-min-below             rc=1 want=1 PASS
SELFTEST json-min-at-bound          rc=0 want=0 PASS
SELFTEST json-nonzero-exit          rc=1 want=1 PASS
SELFTEST json-one-red-of-two        rc=1 want=1 PASS
SELFTEST json-empty-list            rc=1 want=1 PASS
SELFTEST json-malformed-entry       rc=1 want=1 PASS
SELFTEST json-missing-file          rc=1 want=1 PASS
SELFTEST shell-all-ok               rc=0 want=0 PASS
SELFTEST shell-one-red              rc=1 want=1 PASS
SELFTEST shell-nonzero-exit         rc=1 want=1 PASS
SELFTEST shell-no-lines             rc=1 want=1 PASS
SELFTEST contract-no-noharm         rc=1 want=1 PASS
SELFTEST contract-phrase-drift      rc=1 want=1 PASS
SELFTEST json-timeout               rc=1 want=1 PASS
SELFTEST lane-missing               rc=1 want=1 PASS
SELFTEST revision-unresolvable      rc=1 want=1 PASS
SELFTEST default-list-parity        rc=1 want=1 PASS
SELFTEST: 20/20 passed
VERDICT: PASS
```
`SELFTEST_EXIT=0` (`$?` of the command above). Every case asserts the process exit code and a
required/forbidden substring set; the fixtures are hermetic — a throwaway `git init` repo under
`$TMPDIR` (toplevel verified equal to the fixture dir before the single commit), fake contracts,
and `printf`/`sleep` monitors, so the selftest touches neither the lane nor the network. Case 20
(`default-list-parity`) proves the hard-coded mapping and its own `--list` dump are the same
gate: identical stdout, same exit 1, and the six names in `no-harm.sh` order.

# FALSIFIER 1 — a red monitor is refused (must exit 1)

Monitors file `/tmp/tameshi-r46-ExecFalsifier/falsifier-monitors.json`:

```json
{"monitors": [{"name": "r44-record-agreement",
               "command": "python3 .ufo/evidence/round-44/calibration/measure.py --lane \"$LANE\" --rev \"$REV\" --freeze ba01973c73ad7de60e5bd19ae08255a1b7ef917e",
               "expect_contains": ["C2_R44_PASS=true"]}]}
```

Ground truth that the monitor really is red at base, measured on its own first:

```
$ python3 .ufo/evidence/round-44/calibration/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 683eedde3a50441c34d85a22f5fd5346f8b1ec6d --freeze ba01973c73ad7de60e5bd19ae08255a1b7ef917e
C2_R44: self_pin=1 classes=7 m6=0 m7=0 m8=0 m10=0 m11=1 m12=1 m13=0 total=2 records=4 sources_rows=117 standing=117 receipts=17 revisions=4 m13_probe=standing=9_column0=116_valid=117 rev=683eedde3a50441c34d85a22f5fd5346f8b1ec6d freeze=ba01973c73ad7de60e5bd19ae08255a1b7ef917e C2_R44_PASS=false first=m11:SCORECARD.md#round-45:cd8e73f067129f8489e35c7b51c7a68552b289d2
EXIT=1
```

The gate on that monitor (base `683eedde3a50441c34d85a22f5fd5346f8b1ec6d`):

```
$ python3 .ufo/evidence/round-46/quality/no-harm-gate.py \
    --contract .ufo/evidence/round-46/contract.json \
    --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    --rev 683eedde3a50441c34d85a22f5fd5346f8b1ec6d \
    --monitors-file /tmp/tameshi-r46-ExecFalsifier/falsifier-monitors.json
NOHARM r44-record-agreement C2_R44: self_pin=1 classes=7 m6=0 m7=0 m8=0 m10=0 m11=1 m12=1 m13=0 total=2 records=4 sources_rows=117 standing=117 receipts=17 revisions=4 m13_probe=standing=9_column0=116_valid=117 rev=683eedde3a50441c34d85a22f5fd5346f8b1ec6d freeze=ba01973c73ad7de60e5bd19ae08255a1b7ef917e C2_R44_PASS=false fir... RED
RED r44-record-agreement
WHY r44-record-agreement exit 1; missing token 'C2_R44_PASS=true'
monitors=1 ok=0 red=1 contract_no_harm_chars=465 contract_phrases=0/0
NO_HARM_GATE_PASS=false
FALSIFIER_EXIT=1
```

The gate refuses it for both independent reasons the counter itself gives (non-zero exit and the
absent `C2_R44_PASS=true`), and the contract's `no_harm` text already excludes this counter ("the
round-44 record-agreement counter is NOT a monitor (red at base by construction, round-45
spot-check defect 1)") — which is exactly what criterion 88 requires: a round-bound counter is not
a monitor, and a monitor that is red at base is refused.

# The real list — `no-harm.sh` at base (must exit 0)

```
$ python3 .ufo/evidence/round-46/quality/no-harm-gate.py \
    --contract .ufo/evidence/round-46/contract.json \
    --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    --rev 683eedde3a50441c34d85a22f5fd5346f8b1ec6d \
    --monitors-file .ufo/evidence/round-46/no-harm.sh
NOHARM commandD recorded_cases=9 depth_score=9 ok
NOHARM coldread score=6 box3_full_page=False ok
NOHARM r45-freshness population=73 fresh=71 C1_R45_PASS=true ok
NOHARM r45-coverage rows=2 entries=2 C2_R45_PASS=true ok
NOHARM S160-count 1 ok
NOHARM registry-rows-not-below-117 117 ok
monitors=6 ok=6 red=0 contract_no_harm_chars=465
NO_HARM_GATE_PASS=true
REAL_LIST_EXIT=0
```

The same six lines the committed receipt `before/no-harm-at-base.stdout` carries, in the same
order, all `ok`.

# The hard-coded mapping at base (default mode, must exit 0)

```
$ python3 .ufo/evidence/round-46/quality/no-harm-gate.py \
    --contract .ufo/evidence/round-46/contract.json \
    --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 683eedde3a50441c34d85a22f5fd5346f8b1ec6d
NOHARM commandD recorded_cases=9 depth_score=9 ok
NOHARM coldread score=6 box3_full_page=False ok
NOHARM r45-freshness population=73 fresh=71 C1_R45_PASS=true ok
NOHARM r45-coverage rows=2 entries=2 C2_R45_PASS=true ok
NOHARM S160-count 1 ok
NOHARM registry-rows-not-below-117 117 ok
monitors=6 ok=6 red=0 contract_no_harm_chars=465 contract_phrases=6/6
NO_HARM_GATE_PASS=true
DEFAULT_EXIT=0
```

`contract_phrases=6/6`: every monitor of the default mapping is declared by the contract's
`no_harm` text. This is the run to cite for criterion 88 — it is the only mode that both runs the
six monitors and proves the contract declares each one.

# FALSIFIER 2 — the contract check is load-bearing (must exit 1)

A copy of the contract in scratch with the phrase `coldread restraint 6, ` removed
(`/tmp/tameshi-r46-ExecFalsifier/contract-minus-coldread.json`, 465 → 443 chars of `no_harm`);
every monitor still prints ok, and the gate still refuses:

```
$ python3 .ufo/evidence/round-46/quality/no-harm-gate.py \
    --contract /tmp/tameshi-r46-ExecFalsifier/contract-minus-coldread.json \
    --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 683eedde3a50441c34d85a22f5fd5346f8b1ec6d
NOHARM commandD recorded_cases=9 depth_score=9 ok
NOHARM coldread score=6 box3_full_page=False ok
NOHARM r45-freshness population=73 fresh=71 C1_R45_PASS=true ok
NOHARM r45-coverage rows=2 entries=2 C2_R45_PASS=true ok
NOHARM S160-count 1 ok
NOHARM registry-rows-not-below-117 117 ok
RED coldread
WHY coldread contract no_harm does not declare 'coldread restraint 6'
monitors=6 ok=5 red=1 contract_no_harm_chars=443 contract_phrases=5/6
NO_HARM_GATE_PASS=false
EXIT=1
```

`ok=5 red=1` on six green monitor lines is the point: the contract declaration is an independent
conjunct, so a round cannot quietly stop promising a monitor while keeping its command green.

# The deciding revision — `no-harm.sh` at the freeze (must exit 0)

```
$ python3 .ufo/evidence/round-46/quality/no-harm-gate.py \
    --contract .ufo/evidence/round-46/contract.json \
    --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    --rev 745a583181648cfc7f9c1b476cd1be7dc68f7433 \
    --monitors-file .ufo/evidence/round-46/no-harm.sh
NOHARM commandD recorded_cases=9 depth_score=9 ok
NOHARM coldread score=6 box3_full_page=False ok
NOHARM r45-freshness population=73 fresh=71 C1_R45_PASS=true ok
NOHARM r45-coverage rows=2 entries=2 C2_R45_PASS=true ok
NOHARM S160-count 1 ok
NOHARM registry-rows-not-below-117 117 ok
monitors=6 ok=6 red=0 contract_no_harm_chars=465
NO_HARM_GATE_PASS=true
EXIT=0
```

Same six green lines at `745a5831` as at `683eedde`, so the criterion's "at base and at the
deciding revision" holds for the monitors that do not move with the round's own records. (This is
the gate's own observation, not a verdict: the L1's deciding run is the one that counts.)

# Read-only footprint

```
$ ls -la .ufo/evidence/round-46/quality/
-rwxr-xr-x 1 vgpnk vgpnk 25643 Oct 25 18:31 no-harm-gate.py

$ git --no-optional-locks -C <lane> status --porcelain -- .ufo/evidence/round-46/quality
?? .ufo/evidence/round-46/quality/

$ git --no-optional-locks -C <lane> status --porcelain -- .ufo/evidence/round-46/no-harm.sh .ufo/evidence/round-46/contract.json
(no output)

$ find .ufo/evidence/round-46 -maxdepth 3 -name __pycache__
.ufo/evidence/round-46/control/__pycache__
.ufo/evidence/round-46/calibration/__pycache__
.ufo/evidence/round-46/hardening/__pycache__
```
No `__pycache__` under `quality/` after every gate run this seat made (the five recorded runs, the
trial runs before them, and the selftest's 20 subprocess invocations) — the
`PYTHONDONTWRITEBYTECODE=1` child environment holds. `no-harm.sh` and `contract.json` are
unmodified; no git/jj command other than `rev-parse`, `show` and read-only `status` was run in the
lane, and no fixture repo was created inside it. All scratch lives in
`/tmp/tameshi-r46-ExecFalsifier/` (`selftest.stdout`, `run1..run5-*.stdout`, `r44-at-base.stdout`,
`falsifier-monitors.json`, `contract-minus-coldread.json`, `default-list.json`).

# Limits, stated rather than papered over

- **Shell mode does not check contract phrases.** `no-harm.sh`'s monitor names
  (`registry-rows-not-below-117`, …) are not the prose of `no_harm`, so shell mode enforces only
  all-ok + exit 0 + at least one `NOHARM` line. It is the right mode for "run the frozen script";
  default/JSON mode is the right mode for "prove the contract declares each monitor".
- **The gate trusts the monitors list it is given.** A monitors file that omits a monitor passes
  vacuously; only default mode is complete by construction (six names, 6/6 phrases). Criterion 88
  should therefore cite the default-mode run, with the shell-mode run as the script-fidelity
  cross-check — the two agree line for line on the six `NOHARM` lines.
- **The gate cannot detect a monitor that is green for the wrong reason** (e.g. a counter that
  prints its PASS token unconditionally). That is the mutation axis (C2), not this gate.
- Default per-monitor timeout 600 s (`--timeout`); a timed-out monitor is `RED` with reason
  `timeout after Ns`, proven by selftest `json-timeout` (0.4 s bound).
- The gate says nothing about the round-44 counter's *content*; it only refuses to treat it as a
  monitor. Falsifier 1 is therefore evidence about the gate, not a claim about that counter.

# Files changed

- added `.ufo/evidence/round-46/quality/no-harm-gate.py` (deliverable, sha256 `11044f55…`)
- added `.ufo/waves/round-46/w1/ExecFalsifier.md` (this report)

Nothing else: no edit to `no-harm.sh`, `contract.json`, any counter, snapshot, package, the lane's
git index or jj state.

# Tooling

No install or upgrade was made or needed (python3 and git were sufficient); no pacman transaction
was attempted.

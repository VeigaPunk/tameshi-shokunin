# CriticC1Vacuous — round-39 C1: `^\s*leg` cannot satisfy the predicate

## Finding

Applying the round-38 vacuous control regex `^\s*leg` as the round-39
`no_harm_guard.depth_command_d_regex` **cannot** produce `C1_R39_PASS=true`.
It fails the live-agreement conjunct of the frozen predicate
(contract.json:13): guard hits must equal canonical command D on the live
runner.

## Hit count versus command D

Runner: `git show 50aadd1bbd94e43cd3fcfb81459414394db2dc35:tools/mutate-and-run.sh`

| regex | live runner | ledger-stripped copy |
|---|---|---|
| `^\s*leg` (r38 control) | **0 hits (0/0)** | 0 hits (0/0) |
| `^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+` (command D) | **9 hits (9/9)** | 0 hits (0/0) |

`^\s*leg` undercounts the live runner 0 vs 9 → `live_agree=0`, `mismatches=1`
→ `C1_R39_PASS=false`. This is exactly the failure named in the contract's
do-nothing control (contract.json:17): "A vacuous `^\s*leg` guard disagrees on
the live runner (0 vs 9)."

## Reproduction

Base-rev control (do-nothing, required false — holds):

    $ python3 .ufo/evidence/round-39/guard/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 50aadd1bbd94e43cd3fcfb81459414394db2dc35
    C1_R39: guard_absent=1 live_d=9/9 strip_d=0/0 live_agree=0 stripped_agree=0 r38_regex_hits=0 mismatches=1 rev=50aadd1bbd94e43cd3fcfb81459414394db2dc35 C1_R39_PASS=false
    exit=1

Simulated `^\s*leg` as the guard regex (identical logic to measure.py:97-102):

    live  : leg=0/0 d=9/9 live_agree=0
    strip : leg=0/0 d=0/0 stripped_agree=1
    r38_regex_hits=0
    mismatches=1 -> C1_R39_PASS=False

Command used for raw counts:

    git show 50aadd1b:tools/mutate-and-run.sh | python3 -c 'import re,sys; t=sys.stdin.read();
    print(len(re.findall(r"^\s*leg",t,re.M)), len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",t,re.M)))'
    # -> 0 9

## Why it fails (duplicate-authority defect)

`^\s*leg` already has a frozen role: it is the round-38 vacuous control whose
0-hit count is itself a PASS conjunct (`r38_regex_hits == 0`,
measure.py:18,72,102). Reusing it as the r39 depth guard puts one regex in two
authorities: the `r38_regex_hits` conjunct would pass *trivially* (the guard
regex is the control regex), while `live_agree` fails unconditionally — the
guard is blind to all 9 real command-D ledger lines. No run can repair this:
the regex's recorded_cases is pinned at 0 on any runner that keeps command-D
lines in `#   ` comment form.

Secondary fragility (latent, not needed for the falsification): `^\s*leg`
with `re.M` lets `\s*` span newlines, so it would match the first `leg`-prefixed
token after blank lines anywhere, and with no word boundary it matches
`legend`/`legacy`. It is vacuous today only by accident of the runner's current
bytes, not by construction.

## Impacted axes

- C1 calibration: guard choice must reproduce command D's 9/9 live and 0/0
  stripped counts. `^\s*leg` gives 0/0 and 0/0 — live disagreement.
- Depth axis unaffected; C2 conjuncts untouched.

## Smallest safe correction

None available inside the predicate (and none requested): the frozen
`no_harm_guard.depth_command_d_regex` is already the correct command-D pattern
`^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+` (contract.json:35). The finding is
negative-control evidence only: `^\s*leg` must remain the vacuous control and
must NOT be promoted to the r39 guard — doing so yields
`live_agree=0, mismatches=1, C1_R39_PASS=false`. Contract/predicate unchanged.

## Tooling

No installs performed. All commands read-only (`git show`, python3 stdin
counts, measure.py at base rev). Lane checkout unmodified.

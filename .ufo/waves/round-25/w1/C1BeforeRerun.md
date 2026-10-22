# C1BeforeRerun — re-run of the round-25 C1 counter at base and at the lane revision

Seat: TameshiR25.C1BeforeRerun (executor, leaf). Axis judged: calibration.
Assigned move: reproduce the recorded "before" receipt by running the frozen counter
`.ufo/evidence/round-25/c1-measure.py` (sha256 `b18460c7ca559c18c354ce29ea4cfe60d78be3ad7c7e41abd321ba74eb1ee8b2`)
against (a) a clone at the base revision `1f7315732e0cfe0ba9dfe0fff2ef36d1c8481bb5` and
(b) a clone at the lane revision `c9ff09fb41fb8aac5fc335faf10858ff606bd5df`, and compare the base
output against the recorded `.ufo/evidence/round-25/c1-before.json`.

All commands ran inside private clones under `/tmp`; the lane checkout was never written to and no
gate, selftest or sweep was run inside the lane.

## Verdict

PASS on the receipt reproduction, with two calibration caveats that the integrator must fold into
the after-measurement.

1. The recorded before-receipt is **exactly reproducible**. Re-running the frozen counter against a
   base clone reproduces the recorded stdout byte-for-byte except for the one `"repo"` field, whose
   value is the clone path and therefore necessarily differs from the observer's `/fast/scratch/...`
   path. After substituting that single field the two stdout strings are equal (`True`), the exit
   code is 1 in both, and the final line is the same string in both. The receipt is honest about what
   it claims.
2. The counter's three checks are **not vacuous in the ways that matter** — each can and does fail
   under a doctored input, and I executed those failures (details in §3). Two residual holes remain,
   both of which the counter itself does not close and which `c1-pins.py` (added by contract
   amendment 2) is designed to close: the R1/R2 defect population is read from the spec file it is
   measuring (§4.1), and the SCORECARD label check accepts a row that says the item is *not*
   dispositioned (§4.2).
3. At the lane revision the counter currently reads **0/3, exit 1**, and the reason is not a defect:
   `R23-ROUTED-1` and `R23-ROUTED-2` already `hold` on their executed checks (6/6 and 8/8 defects
   killed with explicit witnesses), but no `SCORECARD` row names them yet and the dead-falsifier
   disposition file does not exist yet, so the counter counts 0. The wave's own uncommitted outputs
   are what the counter is waiting for.

## 1. Reproduction of the recorded before-receipt

Clones:

    $ git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/c1beforererun-r25
    $ git -C /tmp/c1beforererun-r25 checkout -q --detach c9ff09fb41fb8aac5fc335faf10858ff606bd5df
    $ git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/c1beforererun-base
    $ git -C /tmp/c1beforererun-base checkout -q --detach 1f7315732e0cfe0ba9dfe0fff2ef36d1c8481bb5
    CLONES_OK
    c9ff09fb41fb8aac5fc335faf10858ff606bd5df
    1f7315732e0cfe0ba9dfe0fff2ef36d1c8481bb5

Base run (the counter taken from the lane revision clone, the repo argument pointing at the base
clone — exactly the form the receipt records):

    $ cd /tmp/c1beforererun-base
    $ python3 /tmp/c1beforererun-r25/.ufo/evidence/round-25/c1-measure.py --repo /tmp/c1beforererun-base
    EXIT=1

Exact stdout (identical on three separate executions; `stderr` empty, 0 bytes):

    {
     "dispositioned": 0,
     "items": {
      "R23-ROUTED-1": {
       "dispositioned": false,
       "holds": false,
       "label": "R23-ROUTED-1",
       "reason": "absent: .ufo/evidence/round-25/c1-suite.py, .ufo/evidence/round-25/multitoken-cases.json, .ufo/evidence/round-25/multitoken-mutants.spec, .ufo/evidence/round-25/guard-mutants.spec",
       "scorecard_row": false
      },
      "R23-ROUTED-2": {
       "dispositioned": false,
       "holds": false,
       "label": "R23-ROUTED-2",
       "reason": "absent: .ufo/evidence/round-25/c1-suite.py, .ufo/evidence/round-25/multitoken-cases.json, .ufo/evidence/round-25/multitoken-mutants.spec, .ufo/evidence/round-25/guard-mutants.spec",
       "scorecard_row": false
      },
      "R23-ROUTED-3": {
       "dead": 34,
       "dispositioned": false,
       "holds": false,
       "label": "R23-ROUTED-3",
       "reason": "disposition file absent",
       "scorecard_row": false
      }
     },
     "repo": "/tmp/c1beforererun-base",
     "schema": "tameshi-r25-c1-measure-v1",
     "total": 3
    }
    C1_ROUTED: dispositioned=0/3

Comparison against the recorded receipt `.ufo/evidence/round-25/c1-before.json` (recorded by
"TameshiR25 (L1, author)" at revision `1f7315732e0cfe0ba9dfe0fff2ef36d1c8481bb5`):

    rec_exit 1 live_exit 1
    rec last line: 'C1_ROUTED: dispositioned=0/3'
    live last line: 'C1_ROUTED: dispositioned=0/3'
    LASTLINE_MATCH True
    JSON_EQUAL_IGNORING_REPO True
    STDERR_MATCH True ''
    rec stdout bytes 1001 live stdout bytes 979
    EQUAL after repo substitution: True
    rec repo path len 45 '/fast/scratch/hyaku/tameshi-r25-a2/base-clone'
    live repo path len 23 '/tmp/c1beforererun-base'
    len diff 22 path diff 22

The 22-byte stdout size difference is exactly the 22-character difference in the `"repo"` path
string; after substituting one for the other the two stdout texts are byte-identical. The recorded
`measure_sha256` (`b18460c7ca559c18c354ce29ea4cfe60d78be3ad7c7e41abd321ba74eb1ee8b2`) equals the
sha256 of the counter I ran, so the receipt was produced by the same counter bytes.

The receipt's `note` is also literally true at base: `.ufo/evidence/round-25/` does not exist in the
base clone at all (`ls .ufo/evidence/round-25` → "No such file or directory"), and `grep -c
'R23-ROUTED' SCORECARD.md` at base returns 0.

Determinism: the base run was executed three times and the REV run twice; the captured stdout files
are byte-identical between repeats (`BASE_DETERMINISTIC`, `IDENTICAL`).

## 2. The same counter against the lane revision

    $ cd /tmp/c1beforererun-r25
    $ python3 /tmp/c1beforererun-r25/.ufo/evidence/round-25/c1-measure.py --repo /tmp/c1beforererun-r25
    EXIT=1

Exact stdout (abridged only where marked; full JSON shape identical to the base run):

    {
     "dispositioned": 0,
     "items": {
      "R23-ROUTED-1": {
       "control_green": true,
       "defects": ["M1","M2","M3","M4","M5","M6"],
       "dispositioned": false,
       "holds": true,
       "killed": ["M1","M2","M3","M4","M5","M6"],
       "label": "R23-ROUTED-1",
       "restore_ok": true,
       "runner_exit": 0,
       "scorecard_row": false,
       "verdict_line": "MUTATE: DONE (target=r25-multitoken defects=6 killed=6 survived=0 inconclusive=0 kill-rate=100%)",
       "witnessed_kills": ["M1","M2","M3","M4","M5","M6"]
      },
      "R23-ROUTED-2": {
       "control_green": true,
       "defects": ["G1","G2","G3","G4","G5","G6","G7","G8"],
       "dispositioned": false,
       "holds": true,
       "killed": ["G1","G2","G3","G4","G5","G6","G7","G8"],
       "label": "R23-ROUTED-2",
       "restore_ok": true,
       "runner_exit": 0,
       "scorecard_row": false,
       "verdict_line": "MUTATE: DONE (target=r25-selftest defects=8 killed=8 survived=0 inconclusive=0 kill-rate=100%)",
       "witnessed_kills": ["G1","G2","G3","G4","G5","G6","G7","G8"]
      },
      "R23-ROUTED-3": {
       "dead": 34,
       "dispositioned": false,
       "holds": false,
       "label": "R23-ROUTED-3",
       "reason": "disposition file absent",
       "scorecard_row": false
      }
     },
     "repo": "/tmp/c1beforererun-r25",
     "schema": "tameshi-r25-c1-measure-v1",
     "total": 3
    }
    C1_ROUTED: dispositioned=0/3

Reading of that output:

- `R23-ROUTED-1` and `R23-ROUTED-2` **hold**: the multitoken sweep killed 6/6 with a
  `FIXTURE <name> FAIL` witness in every defect log, the guard sweep killed 8/8 with a
  `CASE <name> FAIL` witness, control green and byte-identity restore OK on both.
- They are still **not dispositioned** because `scorecard_row` is `false`: `SCORECARD.md` at this
  revision carries no `R23-ROUTED-n` row (`grep -n 'R23-ROUTED' SCORECARD.md` → no match).
- `R23-ROUTED-3` **cannot hold** because `.ufo/evidence/round-25/dead-falsifier-disposition.json`
  does not exist at this revision. The population it would have to cover is 34 seats: the
  round-23 wave-2 rows with `status != completed` in
  `.ufo/waves/round-23/original-outcomes2.json` (64 rows, 30 completed, 34 failed). That file is
  byte-identical at base and at the lane revision (sha256
  `14d9db1f68499d308cdbcd8c8fa611e0967a85fe65c49cce3e4bf6104a0412ee`), so the population is stable.

The counter at the *current* lane HEAD (`09dc114da9002525d31985c14093d32c6712bff4`, contract
amendment 2, which added `M7-M10`, `G9-G14` and the `c1-pins.py` input-pin checker) still reads
0/3 for the same structural reason — the disposition file and the SCORECARD rows are wave outputs
that are not in the tree yet. Measured on a `/tmp` copy of the lane working tree at that moment,
the two sweeps were already green on the widened populations: 10/10 multitoken defects killed and
14/14 guard defects killed, both with witnesses, `restore_ok` true.

## 3. The three checks can fail — negative controls I actually executed

Every probe below is a doctored copy of the lane-revision clone under `/tmp`; the lane checkout was
never touched and no probe was run inside the lane.

| probe (what I changed in the /tmp copy) | counter's answer | what it shows |
|---|---|---|
| multitoken fixture degraded to two genuinely single-token cases | `holds: false`, `killed: []`, `verdict_line: "MUTATE: DONE (target=r25-multitoken defects=6 killed=0 survived=6 inconclusive=0 kill-rate=0%)"`, `control_green: true` | the multi-token fixture is load-bearing: with single-token fixtures all six weakenings survive |
| `multitoken-cases.json` schema broken | `holds: false`, `control_green: false`, `restore_ok: false`, `runner_exit: 2` | the control gate fails closed on a broken fixture |
| `c1-suite.py` patched to print `PASS` always (kills still happen, but no `FAIL` witness line) | `holds: false`, `killed: ["M1".."M6"]`, `witnessed_kills: []` | the counter credits a kill only with an explicit `FIXTURE <name> FAIL` witness, not on exit status alone |
| `M1` in the spec neutered to a no-op edit (old == new) | `holds: false`, `killed: []`, `verdict_line: null` | a defect that stops being a real mutation fails the sweep |
| `M1` weakened to `if False:` (a genuine weakening of the stdout check) | `holds: true`, `M1` killed with witness | the fixture catches the real weakening it was routed to catch |
| `G1` in the guard spec neutered to a no-op edit | `R23-ROUTED-2 holds: false`, `killed: []` | same fail-closed behaviour on the guard sweep |
| disposition row points at a missing report | `R23-ROUTED-3 holds: false`, `failures: ['OutputComplete: report missing']` | R3 checks report existence |
| disposition row marked `reattack-seat-died` with no error text | `R23-ROUTED-3 holds: false`, `failures: ['Replay01: died without error text']` | R3 requires error text for a died seat |
| R3 doctored copies inside the counter (`drop-one-row`, `flip-one-status`) | both `True` — each doctored copy is rejected | the counter's own two negative controls fire |
| complete 34-row disposition + 3 `SCORECARD` rows, all synthetic | `C1_ROUTED: dispositioned=3/3`, exit 0 | the counter is reachable at 3/3; it is not stuck at 0 |

The last row is also the reason §4 matters: I could reach 3/3 with **synthetic** reports and a
**synthetic** SCORECARD table, so "3/3" from this counter alone is not evidence that the items are
genuinely dispositioned.

## 4. Residual calibration holes (not closed by the frozen counter)

### 4.1 R1/R2 population is read from the spec under measurement

`c1-measure.py` takes the expected defect list from the spec file it is about to sweep
(`ids = re.findall(r'^@defect (\S+)', (stage / R25 / spec).read_text(), re.M)`), then checks that the
set of killed defects equals that list. If a defect is removed from the spec, the check still
passes. Executed: I deleted the `M6` block from `multitoken-mutants.spec` in a `/tmp` copy and the
counter reported `holds: true` with `defects: ["M1".."M5"]` and `killed: ["M1".."M5"]` — five
defects, all killed, item still holds. So "6/6 killed" is only as strong as the spec file, and the
spec file is one of the repo-supplied inputs the counter stages.

### 4.2 The SCORECARD label check accepts a row that says the item is not done

The check is `re.search(r'^\|\s*%s\b' % label, scorecard, re.M)` — the row's content is never read.
Executed: in a `/tmp` copy whose `SCORECARD.md` row read
`| R23-ROUTED-1 | calibration | probe | NOT dispositioned | probe |`, the counter still printed
`C1_ROUTED: dispositioned=3/3` and exited 0.

### 4.3 R3 accepts fabricated reports

Executed: with 34 synthetic one-line reports carrying the required
`R23-REATTACK <name>: AGREE|FINDING` line, the R3 check returned `holds: true`, `failures: []`,
`rows: 34`, and both doctored copies failed as required. Nothing in the frozen counter ties a row
to a *committed* report or to a seat that actually ran.

### 4.4 What closes these

`c1-pins.py` (new in contract amendment 2, `.ufo/evidence/round-25/c1-pins.py`) is the intended
complement and it discriminates: on a doctored `/tmp` copy it reported
`C1_PINS: FAIL (32 failures)` and `C1_PINS: FAIL (38 failures)`, naming exactly the classes above —
`P2` on the exact defect-id lists (`M1-M10`, `G1-G14`), `P4` on the report path being canonical and
git-tracked, `P5` on the SCORECARD row count and on the row containing the word `dispositioned`.
Its P1 pins the sha256 of every counter input (runner, gate, suite, both specs, both fixture files,
the round-23 outcomes file and the counter itself), which also fixes §4.1's root cause.

Caveat for the integrator: `c1-pins.py` needs the disposition file to exist before it can run at all.
While the file was absent it exited **2 (SETUP)**:

    $ python3 .ufo/evidence/round-25/c1-pins.py --repo .
    C1_PINS: SETUP ([Errno 2] No such file or directory: '.../.ufo/evidence/round-25/dead-falsifier-disposition.json')
    PINS_EXIT=2

Once a peer landed `.ufo/evidence/round-25/dead-falsifier-disposition.json` (untracked at that
moment), the same command ran and reported `C1_PINS: FAIL (37 failures)` — the failures are exactly
the two expected gaps plus the tracking one: `P4` on all 34 reports ("not canonical or untracked",
because `.ufo/waves/round-25/w1/` is still an untracked directory in the lane) and `P5` on the three
missing `SCORECARD` rows. The after-measurement should carry both counters, and the reports have to
be committed before P4 can pass.

## 5. Notes for the integrator

- **The contract's own C1 input pins are now stale relative to the working tree, and that is
  expected, but the two pin sets must not be confused.** `contract.json` records
  `specs_sha256.guard 636909ed…`, `specs_sha256.multitoken 2a496199…` and
  `fixtures_sha256 ea64fca9…` — the bytes at revision `c9ff09fb`. The working tree now carries
  `af5b6f6e…` (guard, `G9-G14` added), `8ec3f56b…` (multitoken, `M7-M10` added) and `f0a4ac80…`
  (fixture, cases 8-11 added). `contract-amendment-2.json` re-pins the new bytes in
  `c1_input_sha256`, so the two are consistent once amendment 2 is read as superseding the
  original C1 pins. The counter's own sha256 is unchanged by either amendment.
- **`.ufo/evidence/round-25/build-disposition.py` produces a file the counter accepts.** On a `/tmp`
  copy of the lane with a synthetic outcomes map (26 seats `completed`, 8 `failed` with error text)
  it wrote 34 rows (13 agree, 12 finding, 9 died) and the counter's R3 check returned
  `holds: true`, `failures: []`, both negative controls `True`. The tool's row shape and the
  counter's expectations line up. What the counter still will not check is whether the callbacks
  behind those statuses were real — that stays a wave judgement, not a counter output.
- **Live coverage at the time of writing.** All 34 dead round-23 wave-2 seats now have a report in
-  `.ufo/waves/round-25/w1/` carrying exactly one `R23-REATTACK <name>: AGREE|FINDING` line (checked
-  with the counter's own regex over the live tree). Two seats (`NoHarmPlan`, `Replay07`) were still
-  short of a verdict line when I first checked, and reached one during the wave.
- **Re-measurement at the moment the disposition file landed.** A `/tmp` copy of the lane taken after
-  a peer created `.ufo/evidence/round-25/dead-falsifier-disposition.json` measures:
-  `R23-ROUTED-1 holds: true` (10/10 killed), `R23-ROUTED-2 holds: true` (14/14 killed),
-  `R23-ROUTED-3 holds: true` (`rows: 34`, `failures: []`, counts 20 agree / 14 finding / 0 died,
-  both doctored-copy negative controls true) — but `scorecard_row: false` for all three, so the
-  counter still prints `C1_ROUTED: dispositioned=0/3`, exit 1. The single remaining blocker for the
-  counter is the `SCORECARD.md` rows; for the pins checker, the committed-report tracking also still
-  blocks P4.
- **The after-measurement should be run against a clone at the revision that carries the wave's
  outputs**, not against the working tree: the counter's R3 check resolves report paths relative to
  the `--repo` argument, and 34 synthetic reports copied into a `/tmp` clone were enough to satisfy
  it (§4.3). `c1-pins.py` P4 is what distinguishes committed reports from fabricated ones, so it
  must be part of the after-measurement, not an optional extra.

## Tooling record

No tool was installed or upgraded (operator 2026-10-19 directive). Everything used was preinstalled:
`git`, `python3` (3.14), `sha256sum`, `diff`, `cmp`, `ls`, `grep`. No `pacman`, `uv tool`, `npm -g`,
`cargo` or `pip` transaction was performed, and no host service was restarted.

Writes: this report file only, plus `/tmp` scratch clones (`/tmp/c1beforererun-*`). The lane
checkout `/home/vgpnk/Projects/shokunin/tameshi-shokunin` was read only; no git or jj write command
was run against it and its index and lane state are untouched.

Report: .ufo/waves/round-25/w1/C1BeforeRerun.md

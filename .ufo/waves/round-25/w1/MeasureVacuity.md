# MeasureVacuity — attack on `.ufo/evidence/round-25/c1-measure.py`

Seat: TameshiR25.MeasureVacuity (critic, leaf). Axis judged: calibration.
Measure under attack: sha256 `b18460c7…eb1ee8b2` (equals the contract pin), lane HEAD `5b69fb2`.

## Verdict

FINDING. Yes: each of the three items can count while its check is vacuous.

- R23-ROUTED-1 and R23-ROUTED-2 (the two sweeps) take every verdict from files the measured repo supplies. The measure never checks a pin, so a doctored runner, a one-defect spec, or a target with an integrity tripwire all reach `holds: true`.
- R23-ROUTED-3 (the dead-falsifier disposition) passes with 33 of 34 rows marked "died" with the error text `x`, plus one forged report anywhere on the host.
- The SCORECARD label check is satisfied by a row that says the item is *not* done.
- The two R3 negative controls are tautologies. Once the main check passes they always fail, so they carry no information about the data.

Several other inputs I tried fail closed. They are listed at the end so the integrator does not re-chase them.

## Method and evidence

Everything was read-only. I made no writes other than this file, ran no sweep or selftest, and did not clone. I ran the R3 logic and the regexes with constructed in-memory inputs: `python3 -B` loaded the pinned `c1-measure.py` through importlib, and a fake repo object served the report contents. The R1 and R2 holes come from static reading of the code and were not executed; they are marked [INFERENCE].

Lane facts observed:

    $ GIT_OPTIONAL_LOCKS=0 git status --porcelain      (lane)
    ?? .ufo/evidence/round-25/census-start.exit
    ?? .ufo/evidence/round-25/census-start.stdout
    ?? .ufo/waves/round-25/record.json
    ?? .ufo/waves/round-25/w1/
    $ sha256sum ...  →  c1-suite.py ae33a04b…, multitoken-cases.json ea64fca9…,
      multitoken-mutants.spec 2a496199…, guard-mutants.spec 636909ed… (all equal contract.json pins)
      tools/mutate-and-run.sh d22c4025…, tools/command-binding.py 9230c68e… (NOT pinned anywhere in contract.json)
    original-outcomes2.json: 64 rows, Counter({'failed': 34, 'completed': 30}); names unique; file field dead=34
    dead-falsifier-disposition.json: absent at HEAD

The probe output is quoted under each hole below.

## Holes, each with a constructed input

### H1 — R1 and R2: the measure trusts the repo's runner, suite, specs and fixtures without checking any pin (high)

The staging loop at `c1-measure.py:127-132` copies the eight STAGE paths from the repo's working tree and runs them. `sweep()` at `:51-70` derives `holds` only from four things: the runner's stdout (`CONTROL: GREEN`, `DEFECT x: KILLED`, `MUTATE_RESTORE: OK`), the runner's exit code, the presence of `evidence/<id>.out` files written by that same runner, and the `@defect` ids in the repo's own spec.

`contract.json` pins `suite_sha256`, `fixtures_sha256` and `specs_sha256`, but the measure never compares against those pins. `tools/mutate-and-run.sh` and `tools/command-binding.py` are not pinned even in the contract.

Constructed input (a), fake runner. Replace `tools/mutate-and-run.sh` in the clone with:

    #!/usr/bin/env bash
    while [ $# -gt 0 ]; do case $1 in --workdir) W=$2;; --defects) S=$2;; esac; shift; done
    mkdir -p "$W/evidence"; echo 'CONTROL: GREEN'
    for id in $(sed -n 's/^@defect \([^ ]*\).*/\1/p' "$S"); do
      printf 'FIXTURE f FAIL\nCASE c FAIL\n' > "$W/evidence/$id.out"; echo "DEFECT $id: KILLED"; done
    echo 'MUTATE_RESTORE: OK'; echo 'MUTATE: DONE'; exit 0

R1 and R2 then both report `holds: true` with zero suite runs [INFERENCE: traced through `:56-69`; not executed].

Constructed input (b), weakened spec. Reduce `guard-mutants.spec` to one defect that touches no guard:

    @defect X | not a guard
    @old     return code
    @new     return 7

Every `CASE` line in the selftest log becomes `FAIL`, so the defect is witnessed. Now `ids == ['X']` and `witnessed == ['X']`, and R2 holds. G2, G3, G6 and G7, the four guards round 24 never re-mutated, are not exercised at all [INFERENCE]. Likewise, a `multitoken-mutants.spec` holding only M1 passes R1.

Smallest correction: put the pins inside the measure as constants (`PINS = {path: sha256}`) for all eight STAGE files, covering runner, target and extra-cases too. Check them after copying and before `sweep()`, and fail (`holds: false`, reason `pin mismatch <path>`) on any difference. Also assert `ids == ['M1',…,'M6']` and `ids == ['G1',…,'G8']`, so the intended mutant set is part of the ruler and not left to the repo.

### H2 — R1, and R2 in part: a tripwire or crash counts as a fixture kill (medium)

The witness `^FIXTURE \S+ FAIL` (`:133`) is printed by `c1-suite.py:62-69` whenever the mutant's CLI returns nothing parseable (`value = {}`, so `findings=None`). It does not show that the fixture's semantics caught the weakening.

Constructed input: a target `tools/command-binding.py` whose `main()` starts with `if sha256(open(__file__,'rb').read()) != PIN: raise SystemExit(1)`. The pristine copy passes, so the control is green. Every mutant then exits 1 with empty stdout, every FIXTURE line is `FAIL (exit=1 findings=None)`, and all six defects are "witnessed" [INFERENCE].

For R2, the same tripwire placed in `check()` rather than at import (for example `raise SystemExit(9)` as the first line of `check`) makes every subprocess CASE fail while `selftest()` still runs. `c1-suite` returns 1, `CASE … FAIL` is present, and the defect is witnessed [INFERENCE].

Smallest correction: require evidence that the mutant was alive in each witnessed log. For R1, accept the regex `^FIXTURE \S+ FAIL \(exit=[01] findings=\[` and require at least one `^FIXTURE \S+ PASS` line. For R2, require `^COMMAND_BINDING_SELFTEST: ([1-9]\d*)/\d+ pass`, meaning at least one case still passed. Pinning the target (H1) closes the tripwire variant on its own.

### H3 — R3: a "died" row cannot be falsified (high)

At `:83-86`, a `reattack-seat-died` row needs only a non-blank `error` string. Nothing ties it to a dispatched re-attack seat. The flip control (`:108-111`) needs exactly one reattacked row to flip.

Constructed input: 33 rows `{"name": n, "status": "reattack-seat-died", "error": "x"}` plus one `reattacked-agree` row. Probe output:

    B 33 died + 1 abs-path report {'failures': [], 'controls': {'drop': True, 'flip': True}, 'holds': True}

`.ufo/waves/round-25/dispatch.json` names the 34 re-attack seats (`ReReplay01` … `ReWaveAccounting`; 68 `R23-REATTACK` mentions), so the binding is available.

Smallest correction: every row carries `seat` and must equal `TameshiR25.Re<name>`, with that seat present in `.ufo/waves/round-25/dispatch.json`. A died row must also have no report file at its canonical path (H4) and an `error` copied from the round's record of that seat, not free text.

### H4 — R3: the report path is not confined, committed, or unique (high)

At `:87`, `repo / str(r['report'])` follows absolute paths and `..`, and the check is only `is_file()` on the working tree. The docstring's "committed report" is never verified, and one file can serve as the report for every row. Probe output:

    B join /tmp/forged.md                       (Path('/lane') / '/tmp/forged.md')
    D traversal /lane/../other-lane/w.md
    C 34 rows -> SCORECARD.md {'failures': [], 'controls': {'drop': True, 'flip': True}, 'holds': True}

Constructed inputs:

- Absolute path: `"report": "/tmp/forged.md"`, where that file holds one verdict line for the row.
- One self-authored file for all 34 rows: point every row at `SCORECARD.md` and append 34 verdict lines to it.

The lane currently has an untracked `.ufo/waves/round-25/w1/`, so running the measure inside the lane checkout would also accept uncommitted reports.

Smallest correction: require `report == '.ufo/waves/round-25/w1/Re%s.md' % name`, the canonical path for that row's seat. Reject absolute paths and `..`, and confirm `git -C repo ls-files --error-unmatch <report>` succeeds. Uniqueness then follows from the canonical path.

### H5 — R3: the denominator comes from an unpinned repo file (medium)

At `:99-100`, `dead` is recomputed from the repo's `.ufo/waves/round-23/original-outcomes2.json`, with no pin and no count assertion.

Constructed input: set 33 of the 34 `failed` statuses to `completed`. Then `dead` has one entry, and a single row with a report holds R3 [INFERENCE: follows `:100`, `:76`].

Smallest correction: assert `len(dead) == 34 == outcomes['dead']` and pin the file's sha256 in the measure.

### H6 — R3: the negative controls are tautological; an honest all-died set cannot count (informational, plus a calibration false negative)

Given `failures == []`, every single-row drop fails by construction, because the name set differs. Every flip also fails, because `verdicts == [want]` and the flip changes `want`. Probe output:

    F every drop fails given main passes: True

The controls therefore test the checker, not the data. The only effect they have on the data is that the flip control is a no-op when no row is reattacked:

    A all-died error=x {'failures': [], 'controls': {'drop': True, 'flip': False}, 'holds': False}

That case fails closed, but it means "at least one reattacked row" is an unstated requirement. An honest disposition in which all 34 re-attacks died can never count.

Smallest correction: keep the controls as checker self-tests, and state the real gate in the docstring. If a data-dependent control is wanted, flip the status of every reattacked row (`all`, not the first only), and drop each row in turn, requiring each to fail.

### H7 — all three items: the SCORECARD label regex accepts rows that are not a disposition (medium)

The regex at `:144` is `^\|\s*LABEL\b`, using `re.M`. Probe output (each result means "recorded"):

    SCORECARD negated row True        '| R23-ROUTED-1 | NOT dispositioned, still open |'
    SCORECARD html comment True       '<!--\n| R23-ROUTED-2 | todo\n-->'
    SCORECARD fenced code True        '```\n| R23-ROUTED-3\n```'
    suffix True                       '| R23-ROUTED-1-draft | x |'
    suffix . True                     '| R23-ROUTED-1.5 | x |'
    SCORECARD pipe then newline True  '|\nR23-ROUTED-1 prose'   (\s* crosses the newline)
    R23-ROUTED-10 (control) False

Smallest correction: use `^\| ?LABEL \|[^\n]*\bdispositioned\b` with `[ \t]` in place of `\s`. Strip `<!-- … -->` and fenced blocks before matching, and require exactly one match per label.

### H8 — all three items: working tree instead of commits (low to medium)

The docstring says "REPO's committed files", but STAGE (`:128-132`), the disposition file and the reports are all read from the working tree. A dirty or untracked clone counts.

Smallest correction: fail setup if `git -C repo status --porcelain -- <STAGE> <disposition> <reports> SCORECARD.md` is non-empty, or materialize each file with `git show HEAD:<path>`.

## Inputs that fail closed (not holes)

- Empty spec: the runner's parser refuses it with `die('spec contains no defects')` at `mutate-and-run.sh:389-390`, which exits 2, and `bool(ids)` at `:69` also blocks it.
- Runner exit codes: SETUP and red control (exit 2) and DEGRADED/INCONCLUSIVE (exit 1) are blocked by `returncode == 0`. A SURVIVED defect is never in `witnessed`. Tail lines are prefixed with `  | `, so suite output cannot spoof `CONTROL:` or `DEFECT` lines. `c1-suite` setup exit 3 prints no FIXTURE or CASE line.
- The `@defect` id regex can diverge from the runner's parser. `'@defect  M1'` gives measure `[]` but runner `M1`; `'@defect M1|desc'` gives measure `['M1|desc']` but runner `M1`. Both make `witnessed != ids`, so they are false negatives, not vacuity. Matching the runner's `lstrip` and `partition('|')` would remove them.
- Verdict boundary: `AGREEMENT` is rejected. `AGREE-ish` and `AGREE (but see FINDING below)` are accepted as AGREE. This is minor and only matters once H4 is fixed.
- R3 with `dead` empty: `dropped == []`, so the drop control passes and `holds` is false.
- Staging completeness: `c1-suite.py` resolves `REPO = HERE.parents[2]`, which is the stage root. It finds the staged `multitoken-cases.json` and the round-23 and round-24 `extra-cases.json`, and `command-binding.py --selftest` loads only those two files (`command-binding.py:164-172`). No staged-file omission makes a check silently pass.

## Impacted axes

Calibration: the C1 3/3 target can be reached without the executed checks it claims. Provenance: forged or self-authored reports and runner output are accepted. There are duplicate authorities: the repo's runner and spec act as judge of their own sweep, and the repo's `original-outcomes2.json` sets the R3 denominator.

## Tooling

None installed or updated.

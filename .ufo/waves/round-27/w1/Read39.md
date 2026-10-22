# Read39: cold read of "Round-26 gate/probe registry — report interop"

Verdict: gap-minor. Class: record. Read revision 2227d8338c02aa9a5fd7d95c1a41b76865ad7647 (clone detached there; SKILL.md sha256 386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95, which I confirmed on the clone's bytes).

The substance of the section holds: the gate's modes, exit codes, SETUP causes, nine-leg set, selftest count, registry expectations, vendored pins, and write scope all check out against what I ran or read. Three wording issues in the table cells, one unrecorded claim (owner), and one exit-code edge are minor. No blocking gap and no wrong expectation.

## What the section is

Lines 2114–2118 (the last heading in the file; the body is one table on lines 2116–2118). It names `tools/mte-interop.py`, its Command and Exits cells, two registry rows, the write scope, and an owner. It does not tell a reader to run anything itself, so I classed it as a record.

## Evidence: checked and held

1. Selftest 17/17, exit 0. Receipt Read39-2 ran `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --selftest`: 17 `CASE` lines, all PASS, last line `MTE_SELFTEST: 17/17 pass`, exit 0. The count matches the code (the case list at tools/mte-interop.py:405–425, plus the emitter-locations case; total at line 442).
2. Usage exit 64. Receipt Read39-7 (inner exits printed): no mode gives `error: one of the arguments --check --selftest is required`, exit 64; `--selftest --check` gives `argument --check: not allowed with argument --selftest`, exit 64; `--selftest --workdir D` gives `--selftest takes no other arguments`, exit 64. Code: tools/mte-interop.py:447–450 (Parser.error exits 64).
3. SETUP exit 2, four causes observed:
   - Missing jsonschema, check mode. Receipt Read39-5: bare `python3 tools/mte-interop.py --check --workdir D` gives `MTE_INTEROP: SETUP (python jsonschema not importable)`, inner exit 2 (code at lines 294–299).
   - Missing node. Receipt Read39-5: uv run with PATH limited to uv and python3 gives `MTE_INTEROP: SETUP (node not found)`, inner exit 2 (code at lines 302–303).
   - Leg set not the nine ledger legs. Receipt Read39-7: uv run with `--check --workdir <empty dir>` gives `MTE_INTEROP: SETUP (leg set [] / table set [] differs from the nine ledger legs [bash-checklist-run, bash-mado-verify, bash-surface-census, bash-tsukuroi-census, js-cite-check, js-claims-check, js-kimi-census, js-round-gate, js-sources-check])`, exit 2 (code at lines 317–319).
   - Fleet root missing. Receipt Read39-7: uv run with `--check --fleet-root <missing dir>` gives `MTE_INTEROP: SETUP (fleet root ... is not a directory)`, exit 2 (code at lines 274–275).
4. Nine ledger legs. The SETUP message above lists nine legs. `LEG_TABLE` has nine entries (tools/mte-interop.py:74–78). The runner carries nine `TABLE_*` assignments (receipt Read39-1 output), and its header says "r26 nine".
5. Vendored integrity. Receipt Read39-1: both tarball integrity strings in `PACKAGES` match the bytes (`integrity_match=True`), and the report-schema tarball contains `package/src/mutation-testing-report-schema.json`. Code: tools/mte-interop.py:176–182.
6. Registry rows. Receipt Read39-6: `tools/registry.json` has 56 rows and top-level keys `rows` and `schema`. Two interop rows, both active:
   - `mte-interop-selftest`, kind selftest, argv `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --selftest`, expect exit 0 and stdout containing `MTE_SELFTEST: 17/17 pass`.
   - `mte-interop-check`, kind gate, argv `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check` (no `--fleet-root`), expect exit 0 and stdout containing `MTE_INTEROP: PASS legs_conforming=9/9`.
7. Reads the runner's committed tables. tools/mte-interop.py:228–235 (`recorded_verdicts` reads the `TABLE_*` lines of tools/mutate-and-run.sh) and line 315 (called in `check`).
8. Writes only scratch and `--emit DIR`. Code: every temporary location is `mkdtemp` (tools/mte-interop.py:199, 276, 309, 386). The only other writes are the `--emit` outputs (lines 336–342). Runner side (receipts Read39-8 and Read39-10, plus a `_grep` of the runner): the regression path (`run_regression` at tools/mutate-and-run.sh:1343, dispatched from line 2014) reaches only read-only git subcommands (`rev-parse`, `cat-file -e`, `show`, `ls-tree`; lines 1187–1211 in `regression_case`). The write-capable git calls (`init`, `add`, `commit`) are confined to `fixture_commit` (lines 286–297), which is called only from the selftest body (calls at lines 1734–1888; selftest defined at line 1464). The runner has no hard-coded `/home/vgpnk` path.
9. Not hermetic. Code: `run_regression` symlinks every sibling repo under the fleet root into a stage directory (tools/mte-interop.py:281–283), and the runner reads those repos with `git show` (tools/mutate-and-run.sh:1202). The section's note is accurate.

## Not executed (verification gaps)

- Live `--check` (9/9 PASS, exit 0) was not run. The run replays the live sibling lane repositories, and the round bounds forbid touching sibling lanes. The 9/9 claim therefore rests on the registry row text and the nine-leg count, not on a run.
- Code read only, not executed: the FAIL return of 1 (tools/mte-interop.py:347), the emit contents (336–342), unsafe tar member (204–211), metrics failure and timeout (219–224), runner regression failure (289–290), and vendored integrity mismatch (180–181).
- Not tested: the registry row argv for `--check` (no `--fleet-root`) run from a clone outside the fleet root. Line 311 means that argv would take the clone's parent as the fleet root; I did not run that case.

## Minor gaps and smallest corrections

1. Command cell for `--selftest`. The cell reads `--selftest` with no prefix, but the registry row's argv carries the full uv prefix. On this host, `python3 tools/mte-interop.py --selftest` prints `MTE_SELFTEST: SETUP (No module named 'jsonschema')` and exits 2 (receipt Read39-3; receipt Read39-7 shows system python3 3.14.8 has no jsonschema). The Exits cell does name missing jsonschema as SETUP, so the gap is the Command cell. Correction: write the prefixed command in the cell.
2. Command cell for `--check` adds `--fleet-root /home/vgpnk/Projects/shokunin`, but the `mte-interop-check` registry row argv omits it (receipt Read39-6). The two forms agree when the checkout's parent is the fleet root (the lane). Correction: align the cell with the registry argv, or say the explicit fleet root is for clones.
3. PASS wording. "0 PASS (every leg found conforms, at least one leg)" understates the rule. The leg set must equal the nine ledger legs or the run is SETUP exit 2 (lines 317–319; receipt Read39-7 shows the empty-set SETUP), so PASS means nine of nine. Correction: "all nine ledger legs conform".
4. Owner. "Owner tameshi" is not recorded. The registry has no owner field on any row and no top-level owner key (receipt Read39-6: `ROWS_WITH_OWNER_KEY 0`). It matches the lane's identity but is not sourced. Correction: drop it or source it.
5. Exit 1 ambiguity. Exit 1 is documented as FAIL. An uncaught exception in the per-leg loop (tools/mte-interop.py:326–335, outside the try that ends at line 324) also exits 1. Code read only; not executed. Correction: optional; note it or wrap the loop.

## Trace, write, and install notes

- Receipts listed in `traces`: Read39-1, -2, -3, -5, -6, -7, -8, -9, -10, all under the round-27 coldread traces directory. Each shows rev 2227d8338c02aa9a5fd7d95c1a41b76865ad7647 and rev_reason null. The traces directory is shared with other seats; I wrote only Read39-* files there.
- Superseded receipt, not listed: Read39-4.json (725 KB). Its wrapper's trailing `git status --porcelain` made git re-read the whole tracked tree (5,853 inputs). I take the cause to be git's racy-index re-reads; that is an inference I did not check. The receipt is git-internal and not a file this section cites. I re-ran the same probes without the git step as Read39-7; the exits match. The superseded receipt is still on disk, unlisted.
- Commands outside the collector, as the brief prescribes: the step-1 clone setup (`mktemp`, the symlink mirror, `git clone --no-hardlinks` read from the lane, `git checkout --detach`, `sha256sum`) and `mkdir -p` on the round-27 traces and w1 directories in the lane. The clone step only read the lane's repository; nothing in the lane's repository or index was written.
- Writes outside scratch: the nine listed receipts, the superseded receipt, and this report. Scratch is /tmp/Read39-kAZo (clone, scratch wrapper scripts, an empty work directory, and a temp dir). The SETUP probe left one regression scratch directory under /tmp/Read39-kAZo/scratch/tmp; SETUP does not remove it.
- Clone cleanliness: `git status --porcelain` printed 0 lines after the probe runs (receipt Read39-9; the last run, Read39-10, only reads). All six input files hash the same in the working tree and at the pinned revision (receipt Read39-9, `equal=True`).
- Installs and updates: none. Host tools used as found: node v24.21.0, uv 0.13.0, Python 3.14.8. `uv run --with jsonschema==4.25.1` resolved jsonschema for the run; no host install was made.
- Not opened: SCORECARD.md, LOG.md, and .ufo/evidence/round-21/coldread/ledger.json (not cited, not touched). I read no live-lane file during any trace.
- Orientation only: a repo-wide `_grep` for `mte-interop` returned hits under .ufo/evidence and .ufo/waves for rounds 25 and 26. I used them for orientation, cite none of them, and do not list them in `inputs`.

## Machine-readable record

```json
{
  "schema": "tameshi-coldread-report-v2",
  "seat": "Read39",
  "skill_sha256": "386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95",
  "read_rev": "2227d8338c02aa9a5fd7d95c1a41b76865ad7647",
  "sections": [
    {
      "start": 2114,
      "heading": "### Round-26 gate/probe registry \u2014 report interop",
      "class": "record",
      "verdict": "gap-minor",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [
        "Command cell for --selftest omits the uv prefix that the mte-interop-selftest registry row argv carries. Bare python3 tools/mte-interop.py --selftest prints MTE_SELFTEST: SETUP (No module named 'jsonschema') and exits 2 on this host (Read39-3; Read39-7 env_python_jsonschema exit 1).",
        "Command cell for --check adds --fleet-root /home/vgpnk/Projects/shokunin, but the mte-interop-check registry row argv omits it, so the default ROOT.parent applies (tools/mte-interop.py:311). The two forms agree only when the checkout parent is the fleet root (Read39-6).",
        "PASS wording: '0 PASS (every leg found conforms, at least one leg)' understates the rule. The leg set must equal the nine ledger legs or the run is SETUP exit 2 (tools/mte-interop.py:317-319; Read39-7 setup_check_empty_workdir), so PASS means nine of nine.",
        "'Owner tameshi' is not recorded. tools/registry.json has top-level keys rows and schema only, and no row carries an owner field (Read39-6, ROWS_WITH_OWNER_KEY 0).",
        "Exit 1 is documented as FAIL, but an uncaught exception in the per-leg judge loop outside the try block (tools/mte-interop.py:326-335) also exits 1 (code read only; not executed)."
      ],
      "commands_executed": [
        "python3 /tmp/Read39-kAZo/scratch/r1.py",
        "uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --selftest",
        "python3 tools/mte-interop.py --selftest",
        "python3 /tmp/Read39-kAZo/scratch/r5.py",
        "python3 /tmp/Read39-kAZo/scratch/r6.py",
        "python3 /tmp/Read39-kAZo/scratch/r4b.py",
        "python3 /tmp/Read39-kAZo/scratch/r8.py",
        "python3 /tmp/Read39-kAZo/scratch/r9.py",
        "python3 /tmp/Read39-kAZo/scratch/r10.py"
      ],
      "opened": [
        ".gitignore",
        "tools/mte-interop.py",
        "tools/mutate-and-run.sh",
        "tools/registry.json",
        "tools/trace-inputs.py",
        "tools/vendor/mutation-testing-metrics-3.9.0.tgz",
        "tools/vendor/mutation-testing-report-schema-3.9.0.tgz"
      ],
      "inputs": {
        ".gitignore": "0f699af0108f1ac4f43cd5f61c9151896b8328ec7edd0adf4ca1c638a2441116",
        "tools/mte-interop.py": "193ea6e32f89016baffe07d41fee17074651e74d4807f7fb70dff2fbe0f72cc4",
        "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
        "tools/registry.json": "c1b75366f1789121e6d5a4c8f6587f7519fef3bad60569ed274df8c7a681b73c",
        "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4",
        "tools/vendor/mutation-testing-metrics-3.9.0.tgz": "ce17812bf718cf2415fb429b2774c7ad3e1e0ca57234e7f8cfa0d794f38ec548",
        "tools/vendor/mutation-testing-report-schema-3.9.0.tgz": "adb78e132e8a0ff17849f842007848eb7a3796f7379e15d8a46a2311dc467280"
      },
      "external_inputs": {},
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read39-1.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read39-2.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read39-3.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read39-5.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read39-6.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read39-7.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read39-8.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read39-9.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read39-10.json"
      ]
    }
  ]
}
```

Plain-English note on what I checked: I cold-read the section from a detached clone at the pinned revision and classed it as a record. I ran the gate's selftest with the uv prefix (17 of 17 pass) and without it (SETUP on this host). I drove every usage and SETUP path I could reach without touching sibling lanes, and I confirmed the nine-leg set, the vendored pins, both registry rows, and the runner's read-only git use on the regression path. I did not run the live check, because it replays sibling lane repositories, so its 9/9 PASS is verified only by the registry text and the leg count. The three wording issues, the unrecorded owner, and the exit-code edge are minor and do not change what the section's facts say.

COLDREAD Read39: gap-minor

# Read24: cold read of "## Repeated controls and gate registry — round 12"

**Verdict: gap-minor** (class `instruction`).

The recipe on line 1492 runs as written. The four outcomes in table rows 1 to 3 reproduce on this revision, and the output-directory rule holds. I found six minor gaps and no blocking gap.

## Scope

- Revision: 2227d8338c02aa9a5fd7d95c1a41b76865ad7647, detached clone. SKILL.md sha256 386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95.
- Section read: SKILL.md lines 1479 to 1498. Line 1499 opens a `###` heading (Gate/probe registry, lines 1499 to 1515). The item's boundary rule puts that in its own bucket, so I did not read it for this verdict.

## Evidence

Every command cited below ran under the trace collector with the clone as root. E10 to E13 are reads and searches made with the file tools; their files appear in the JSON inputs. Receipts `Read24-1` to `Read24-9` are listed in the JSON and live in `.ufo/evidence/round-27/coldread/traces/`. The `git status` receipt sits beside them as `EXCLUDED-Read24-10.json` and is not part of the entry.

- E1, pristine row, line 1492 (Read24-1, receipt exit 0). Command: `python3 tools/repeat-control.py --runs 3 --out /tmp/tameshi-r12-controls-Read24-c9e41d-pristine -- python3 tools/trace-inputs.py --help`. Observed: REPEAT_RUN 1 to 3 each `exit=0 stdout-bytes=873 stderr-bytes=0`; `REPEAT_COMPARE identical=yes runs=3`; `REPEAT_CONTROL: controls_match`.
- E2, mismatch row, line 1488 (Read24-2, receipt exit 1). Command: `... -- python3 -c "import secrets; print(secrets.token_hex(8))"`. Observed: three runs each exit 0 with 17 stdout bytes; `identical=no`; `REPEAT_CONTROL: controls_mismatch`.
- E3, equal nonzero row, line 1489 (Read24-3, receipt exit 2). Command: `... -- python3 -c "import sys; sys.stderr.write('fixture nonzero\n'); sys.exit(3)"`. Observed: three runs each exit 3 with 16 stderr bytes; `identical=yes`; `REPEAT_CONTROL: baseline_nonzero`.
- E4, command unavailable, line 1489 (Read24-4, receipt exit 2). Command: `... -- /nonexistent/tameshi-r12-fixture`. Observed: three runs `exit=unavailable`; `REPEAT_CONTROL: command_unavailable`.
- E5, output directory must not exist, line 1494 (Read24-5; the outer shell exits 0). Command: `sh -c "mkdir -p …-exists && python3 tools/repeat-control.py --runs 3 --out …-exists -- python3 tools/trace-inputs.py --help; echo gate_exit=$?"`. Observed: `REPEAT_CONTROL: invalid_usage`; `gate_exit=64`; stderr `--out already exists (refused, never overwritten)`.
- E6, argv without a shell, line 1492 (Read24-8, then Read24-9). `-- /bin/echo $HOME` gave `stdout-bytes=6` and `controls_match`. `cat` of the saved `run-1.stdout` printed the literal `$HOME`, so the argv was not shell-expanded.
- E7, permissions of retained output, lines 1496 to 1497 (Read24-7). Observed: `umask` 0022; the output directory is `755`; `run-1.stdout`, `command.txt` and `finding.txt` are each `644`; owner vgpnk.
- E8, digests and tool versions (Read24-6). `python3 --version` gave 3.14.8; `strace -V` gave 7.2; `sha256sum` gave the six digests in the JSON `inputs`.
- E9, clean clone. `git status --porcelain` printed nothing. That receipt is excluded from this entry; see Residual risk. The six digests in `inputs` are identical in every remaining receipt that read those files.
- E10, runtime evidence, line 1482. `.ufo/evidence/round-12/verification-final.json`, read by hand with `?q=[.checks[]|{name,passed,expected_exit,observed_exit}]`: 10 checks, all `passed: true`, including repeat-control-selftest, frozen-match, frozen-mismatch, real-pristine-three-controls and runner-six-leg-regression.
- E11, sources, line 1481. `corpus/SOURCES.md:15` (S004) and `:37` (S026) exist. Both rows say `fetched 2026-10-19`. `corpus/knowledge/repeated-control-precondition.md:1` says both were fetched `2026-10-20T02:13:47Z`.
- E12, runner leg count, line 1483. `tools/mutate-and-run.sh:83` header says `r26 nine`; `:87-95` lists nine legs; `:1430` sets `local nlegs=9`; `:1943-1945` checks for nine. A grep of the runner for `repeat-control` found no match, so "standalone" holds.
- E13, code read by hand. `tools/repeat-control.py:17-18`: argv run with shell=False, stdin /dev/null, environment inherited. `:30-40`: precedence. `:206-220`: classify, with the unavailable check first at `:208-209`, the mismatch check at `:211-217` and the baseline check at `:218-219`. `:279-287`: subprocess.run with no timeout. `:298-301`: raw files written before classification at `:334`. `:315-317`: an existing directory is refused.

## Minor gaps

- G1, line 1483. "not a change to the six-leg runner" is stale at this revision. The runner has nine legs (E12). The cited note still gives the round-12 pin and six legs at `corpus/knowledge/repeated-control-precondition.md:54`. Its only later correction (`:105-114`) covers round 16.
- G2, line 1492. "COMMAND ARG..." is run as argv with no shell (E6; E13 at `:17-18`). Redirects, pipes and variable expansion are not applied. The section does not say so.
- G3, line 1488. The mismatch row does not say that an unavailable run yields `command_unavailable` before the mismatch test (`:208-209` before `:211-217`). Code reading only; not run.
- G4, line 1489. The decision column names no finding IDs. Equal nonzero controls give `baseline_nonzero` and a missing command gives `command_unavailable`. Both exit 2 (E3, E4).
- G5, line 1492. "UNIQUE" has no generation rule. An existing directory is refused with exit 64 (E5).
- G6, lines 1496 to 1497. The sensitive-output caution does not mention permissions. Under umask 0022 the retained files are readable by other local users (E7).
- G7, ledger. `SOURCES.md:15` and `:37` give fetch date 2026-10-19; the cited note at `:1` gives 2026-10-20 (E11). The section states no date, so this is a ledger error, not a section error.

## Smallest safe correction (wording only; not applied)

- Line 1483: "This is a standalone precondition check; it does not change the round-12 runner (six legs then, nine legs at this revision)."
- Line 1492: add "COMMAND runs as argv with no shell; wrap redirects or pipes in `sh -c`." Replace UNIQUE with a path that does not yet exist, for example from `mktemp -u`.
- Line 1488: add "If any run cannot execute, the result is `command_unavailable` instead."
- Line 1489: name the IDs: `baseline_nonzero` (exit 2) and `command_unavailable` (exit 2).
- Line 1496: add "For sensitive output, run under `umask 077`; the gate writes files with the caller's umask."
- Ledger: make the fetch dates in `SOURCES.md:15` and `:37` agree with the note once the owner confirms which date is right. I have not decided which is right.

## Residual risk and verification gaps

- S004 and S026 were not opened. They are web pages the section cites for provenance, and I did not fetch them.
- G3 (mixed availability) and the absence of a timeout were read from code, not run.
- The Gate/probe registry (lines 1499 to 1515), the repeat-control selftest and the runner `--regression` were not run. They belong to other buckets.
- The `git status` receipt is excluded from `traces` and `commands_executed`. It sits at `EXCLUDED-Read24-10.json` in the traces directory. Its tree scan listed 5,853 inputs, which would merge unrelated files, including three files the L1 appends later, into this entry. No part of the verdict rests on it. The six `inputs` digests are identical in the remaining receipts.
- Outside the collector, I ran the setup clone (item step 1) and one early probe. The probe made the traces directory with `mkdir -p` and printed the strace and Python versions, six `sha256sum` values and the clone's `git rev-parse` value. Those commands are not in `commands_executed`. The same versions and digests were re-observed under the collector (Read24-6). The `/tmp` output directories came from my own runs and are not inputs.

## Tooling

No tool was installed or upgraded. strace 7.2 (`/usr/bin/strace`) and Python 3.14.8 were already present. I did not need `~/.omp/agent/RULES.md`.

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read24", "skill_sha256": "386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95", "read_rev": "2227d8338c02aa9a5fd7d95c1a41b76865ad7647",
 "sections": [{"start": 1479, "heading": "## Repeated controls and gate registry \u2014 round 12", "class": "instruction", "verdict": "gap-minor", "blocking_gaps": [], "wrong_expectations": [],
 "minor_gaps": [
  "1483: 'not a change to the six-leg runner' is stale at this revision: tools/mutate-and-run.sh:83-95 lists nine legs and :1430 sets nlegs=9; corpus/knowledge/repeated-control-precondition.md:54 still gives the round-12 pin and six legs",
  "1492: COMMAND ARG... is run as argv with no shell (tools/repeat-control.py:17-18); the run with '/bin/echo $HOME' saved the literal $HOME (Read24-8, Read24-9); the section does not say that redirects, pipes and variable expansion are not applied",
  "1488: the mismatch row does not say that an unavailable run yields command_unavailable before the mismatch test (tools/repeat-control.py:208-209 before :211-217); code reading only, not run",
  "1489: the decision column names no finding IDs; equal nonzero controls give baseline_nonzero and a missing command gives command_unavailable, both exit 2 (Read24-3, Read24-4)",
  "1492: 'UNIQUE' has no generation rule; an existing output directory is refused with exit 64 invalid_usage (Read24-5)",
  "1496-1497: the sensitive-output caution does not mention permissions; under umask 0022 the output directory is 755 and the saved files are 644, so other local users can read them (Read24-7)",
  "ledger: SOURCES.md:15 (S004) and :37 (S026) say fetched 2026-10-19, while corpus/knowledge/repeated-control-precondition.md:1 says fetched 2026-10-20T02:13:47Z; the section states no date, so this is a ledger error, not a section error"
 ],
 "commands_executed": [
  "python3 tools/repeat-control.py --runs 3 --out /tmp/tameshi-r12-controls-Read24-c9e41d-pristine -- python3 tools/trace-inputs.py --help",
  "python3 tools/repeat-control.py --runs 3 --out /tmp/tameshi-r12-controls-Read24-c9e41d-volatile -- python3 -c \"import secrets; print(secrets.token_hex(8))\"",
  "python3 tools/repeat-control.py --runs 3 --out /tmp/tameshi-r12-controls-Read24-c9e41d-nonzero -- python3 -c \"import sys; sys.stderr.write('fixture nonzero\\n'); sys.exit(3)\"",
  "python3 tools/repeat-control.py --runs 3 --out /tmp/tameshi-r12-controls-Read24-c9e41d-missing -- /nonexistent/tameshi-r12-fixture",
  "sh -c \"mkdir -p /tmp/tameshi-r12-controls-Read24-c9e41d-exists && python3 tools/repeat-control.py --runs 3 --out /tmp/tameshi-r12-controls-Read24-c9e41d-exists -- python3 tools/trace-inputs.py --help; echo gate_exit=$?\"",
  "sh -c \"python3 --version; strace -V; sha256sum tools/repeat-control.py tools/trace-inputs.py tools/mutate-and-run.sh corpus/SOURCES.md corpus/knowledge/repeated-control-precondition.md .ufo/evidence/round-12/verification-final.json\"",
  "sh -c \"umask; stat -c '%a %U %n' /tmp/tameshi-r12-controls-Read24-c9e41d-pristine /tmp/tameshi-r12-controls-Read24-c9e41d-pristine/run-1.stdout /tmp/tameshi-r12-controls-Read24-c9e41d-pristine/command.txt /tmp/tameshi-r12-controls-Read24-c9e41d-pristine/finding.txt\"",
  "python3 tools/repeat-control.py --runs 3 --out /tmp/tameshi-r12-controls-Read24-c9e41d-noshell -- /bin/echo $HOME",
  "sh -c \"cat /tmp/tameshi-r12-controls-Read24-c9e41d-noshell/run-1.stdout; cat /tmp/tameshi-r12-controls-Read24-c9e41d-noshell/finding.txt\""
 ],
 "opened": ["tools/repeat-control.py", "tools/trace-inputs.py", "tools/mutate-and-run.sh", "corpus/SOURCES.md", "corpus/knowledge/repeated-control-precondition.md", ".ufo/evidence/round-12/verification-final.json"],
 "inputs": {"tools/repeat-control.py": "296fe566dc59380b6baa518b61cef92fe3c7af09d538b2dde9e7f4af1b8cbc25", "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4", "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de", "corpus/SOURCES.md": "0a66531dde7f086005ddf131a3bc5f920a15af5b614fccd631f8d5a668a58e5a", "corpus/knowledge/repeated-control-precondition.md": "1339460070d6c2c2d9609915a675b6866f0c42089a39bdb1ecb39b52f1c5fe5b", ".ufo/evidence/round-12/verification-final.json": "9f3d117af3b613d0a00b7d0a623d31136e36f53cb6fcb5626e42cf0c6e022201"},
 "external_inputs": {},
 "traces": [
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read24-1.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read24-2.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read24-3.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read24-4.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read24-5.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read24-6.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read24-7.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read24-8.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read24-9.json"
 ]}]}
```

## Note

I built a detached clone at 2227d83 and confirmed the page digest. I classed the section as an instruction because it tells a reader to run `tools/repeat-control.py`. I ran that command as written against a pristine fixture under the collector (Read24-1). I ran the other three table outcomes with fixtures (Read24-2 to Read24-4) and the must-not-exist rule (Read24-5). Each result matched the table, and each exit code matched the code. I checked the cited records: the knowledge note, the SOURCES rows and the round-12 evidence file. I also checked the claims about the leg count, shell handling and file permissions. Every quoted line appears in the evidence list above, and every listed receipt appears in the JSON.

COLDREAD Read24: gap-minor

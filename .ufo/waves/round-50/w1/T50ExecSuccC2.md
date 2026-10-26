# T50ExecSuccC2 — sandboxed confirmation of the round-49 C2 panel (R49.2, second half)

Seat: `T50ExecSuccC2` (executor, leaf). Item: close the second half of routed defect
`corpus/lessons/round-49-verifier-spotcheck.md:123` (R49.2, "C2 cannot tell a property-based
generator from a differential one") by running the frozen generator against each of the 12 public
round-49 panel mutants inside a namespace that cannot see the lane, the pristine guard or the panel.

Read-only on the lane. Wrote only
`.ufo/waves/round-50/w1/T50ExecSuccC2/sandboxed-confirm.py`, this report, and the receipts in
`.ufo/waves/round-50/w1/T50ExecSuccC2/`. No claim is decided here; every line below is a command
result or a code reading.

Read: `.ufo/evidence/round-50/contract.json` (claims.C1/C2, no_harm), the routed item in
`corpus/lessons/round-49-verifier-spotcheck.md:121-127` and `.ufo/evidence/round-50/c1/defects.json`
(R49.2 entry), `.ufo/waves/round-49/w1/T49CritC2Contract.md:33-101` (F1/F2), the round-49 counter
`.ufo/evidence/round-49/c2/measure.py:212-262,300-360`, `.ufo/evidence/round-49/c2/panel.json`,
`tools/pbt-staged-id.py` at `e3729de862f73ae080d98fcf522a7081ce16e40a` (lines 756-833, 967-987),
`tools/staged-id-guard.py` at the same rev (lines 36-40, 426), `corpus/knowledge/pbt-generator-pilot.md:61-70`.
Not opened: anything under `/home/vgpnk/.local/state/`, the hidden round-50 panel, the
`control/c2-*.stdout` files.

Ran (scratch `/fast/scratch/hyaku/tameshi-r50/T50ExecSuccC2`, deleted before yield; nothing written
into the lane outside the wave directory):

```
python3 -I .ufo/waves/round-50/w1/T50ExecSuccC2/sandboxed-confirm.py --selftest --work "$S/selftest"
python3 -I .ufo/waves/round-50/w1/T50ExecSuccC2/sandboxed-confirm.py \
  --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev e3729de862f73ae080d98fcf522a7081ce16e40a \
  --panel .ufo/evidence/round-49/c2/panel.json \
  --work "$S/run" --out "$S/run/sandboxed-confirm.json"
```

Tooling: nothing installed or upgraded. `bwrap` was already on PATH — `/usr/bin/bwrap`,
`bubblewrap 0.13.1` (`receipt: bwrap-version.txt`); `python3` 3.14.8, stdlib only.

---

## F1 (closes F1/F2 of the round-49 critique for these 12 mutants) — the frozen generator still confirms 12/12 with no pristine guard, no lane and no panel in its filesystem

`measure.py:219` runs the generator with `cwd=os.path.dirname(gen)` and `measure.py:250-258`
materialises the pristine guard at `<work>/tree/tools/staged-id-guard.py` — the generator's own
directory — so the mutant run at `measure.py:336` hands every generator a reference guard at
`./staged-id-guard.py`; `measure.py:214-219` also leaves the whole filesystem readable
(critique `.ufo/waves/round-49/w1/T49CritC2Contract.md:33-101`).

The harness replaces that with a bubblewrap namespace per run (`sandboxed-confirm.py:222-236`:
`--unshare-all --new-session`, `--clearenv`, read-only binds `/usr /lib /lib64 /etc/ld.so.cache`,
`--proc /proc --dev /dev`, and one writable `--bind <run> /run` holding exactly
`/run/pbt-staged-id.py`, `/run/staged-id-guard.py` and `/run/scratch/`; no `/home`, so no lane, no
pristine guard, no panel). Generator and guard are read from git objects at REV, never from the
working tree (`sandboxed-confirm.py:353-367`), and their shas are pinned
(`:56-60`: guard `03a796c5…`, generator `0cbee39…`, seed 4949/400 cases; all matched).

Observed (`receipt: sandboxed-confirm.stdout`, `sandboxed-confirm.json`):

```
pristine:  exit=0 cases=400 violations=0 dump_cases=400 ok=true
MUTANT M01 row-indent-4            confirmed  cases=21 counterexample=20
MUTANT M02 row-column0             confirmed  cases=1  counterexample=0
MUTANT M03 id-width-3              confirmed  cases=4  counterexample=3
MUTANT M04 www-kept                confirmed  cases=13 counterexample=12
MUTANT M05 slash-kept              confirmed  cases=9  counterexample=8
MUTANT M06 held-form-sensitive     confirmed  cases=9  counterexample=8
MUTANT M07 naive-off-by-one        confirmed  cases=1  counterexample=0
MUTANT M08 cascade-vs-registry     confirmed  cases=6  counterexample=5
MUTANT M09 duplicate-accepted      confirmed  cases=51 counterexample=50
MUTANT M10 short-row-accepted      confirmed  cases=12 counterexample=11
MUTANT M11 map-injectivity-dropped confirmed  cases=94 counterexample=93
MUTANT M12 map-uncovered-dropped   confirmed  cases=42 counterexample=41
SANDBOXED_CONFIRM: … confirmed=12/12 unconfirmed=0 probes_ok=true ok=true
```

`confirmed` is the round-49 counter's own rule, re-implemented: generator exit 1, the counterexample
index is exactly one case in the generator's dump, and the pristine guard and the mutant guard, each
run **in its own sandbox** on that single case (`sandboxed-confirm.py:369-377`, `:412-452`), return
different comparable output (exit code + JSON minus `registry_sha256`/`staged_sha256`). All 12 pairs
differ (`"differ": true` in every mutant entry). So the round-49 result "12/12 confirmed" is not
explained by the reachable-reference cheat for this generator at seed 4949.

## F2 (negative control) — the sandbox really hides the pristine guard, and the probe is not vacuous

A probe script (`sandboxed-confirm.py:95-133`) runs inside the same namespace as every generator run
and must satisfy five conditions: the lane guard path cannot be opened, the lane panel path cannot be
opened, `/home` does not exist, exactly one file named `staged-id-guard.py` is visible with a sha
pinned to the guard under test, and `git -C <lane>` fails.

Observed, per run (13 probes: 1 baseline + 12 mutants; `negative_control.per_mutant` in the JSON):

```
lane_guard_open = {"opened": false, "errno": "FileNotFoundError",
                   "detail": "[Errno 2] No such file or directory:
                    '/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/staged-id-guard.py'"}
lane_panel_open = {"opened": false, "errno": "FileNotFoundError"}
home_exists     = false
guards_found    = [{"path": "/run/staged-id-guard.py", "sha256": "<that mutant's sha>"}]
lane_git        = {"exit": 128, "stderr": "fatal: cannot change to
                   '/home/vgpnk/Projects/shokunin/tameshi-shokunin': No such file or directory"}
negative_control.all_ok = true
```

Because the visible guard's sha equals the mutant's sha (e.g. M01 `758d8644…`, M12 `aabe9f7c…`) and
differs from the pristine `03a796c5…`, a pristine guard smuggled into the view would appear either
as a second `staged-id-guard.py` or as a sha mismatch — both fail the probe.

The probe is shown to detect a leak rather than pass by construction: the selftest runs the same
probe with the fixture lane bound read-only and requires it to fail
(`sandboxed-confirm.py:524-527`). Observed (`receipt: selftest.stdout`):

```
SELFTEST check=probe-detects-bound-lane ok=true leaked_probe_ok=False guard_open=True
```

## F3 (source inspection, independent of the sandbox) — the frozen generator contains no reference to a second guard, no cwd, no absolute path

```
git cat-file -p e3729de862f73ae080d98fcf522a7081ce16e40a:tools/pbt-staged-id.py \
  | grep -n "staged-id-guard\|getcwd\|dirname(__file__)\|__file__\|'/home\|\"/home\|subprocess"
→ 2:"""Property-based generator for tools/staged-id-guard.py (tameshi round 49, C2 / F10).   (docstring)
  45-54: argparse, json, os, random, re, shutil, subprocess, sys, tempfile, time
  772:        proc = subprocess.run(argv, capture_output=True, timeout=GUARD_TIMEOUT, cwd=case_dir)
  842:# selftest: the oracle and the classifier, without the guard (no subprocess)
```

The only `subprocess` use is `run_guard` (`tools/pbt-staged-id.py:756-781`), which execs the
`--guard` it was handed in a per-case directory under `TMPDIR`; the only `open` in the guard at REV
is on its own argv paths (`tools/staged-id-guard.py:426`). So the differential cheat of
`.ufo/waves/round-49/w1/T49CritC2Contract.md:33-75` was a property of the counter's environment, not
of the generator's code, and inside the sandbox it has nothing to diff against.

## F4 — reproducible and cheap

Two independent full runs produced identical statuses and identical per-mutant case counts
(21/1/4/13/9/9/1/6/51/12/94/42), which is expected from the frozen `--seed 4949`. Wall clock: 30 s
for the 12 mutants plus 13 probes plus the 400-case baseline; 2.6 s for the selftest. No mutation of
the lane: every run dir, dump and case file lives under `--work`.

## F5 — what this does NOT close (scope of the finding)

- The round-49 counter is frozen (`freeze.json`) and still has the hole: `measure.py:219` +
  `:250-258`. This harness is a **probe**, not a counter; it prints confirmed/unconfirmed and exits 0
  only on harness integrity (`sandboxed-confirm.py:473-479`, `:627`). The successor counter R49.2 asks for
  must move the same namespace into `measure.py`, and this file is its executable spec.
- Critique F3 (dump padding: 10 distinct cases × 40 satisfies the class floors) and F4
  (`oracle_disagree` checks the guard, not the generator, and skips map cases) are untouched here:
  the harness does not validate the generator's dump distribution or its oracle.
- The sandbox removes the *reachable-reference* cheat, not fixture replay: a generator with a
  hard-coded corpus of expected answers would still be confirmed. `CTL_FIX` remains the control for
  that, exactly as `contract.json` claims.C2.controls states.
- One dimension is now measured rather than asserted: the panel is unreadable while the generator
  runs (probe, F2). The author's ignorance at authoring time is no longer the only ground for
  `why_hidden` in this panel.

## F6 — consequence for the C1 ledger row (R49.2), which is not this seat's file

R49.2 is compound: C1 `absent` uncapped **and** the C2 differential blind spot
(`.ufo/evidence/round-50/c1/defects.json`, R49.2 `text`, keys `absent`, `differential`,
`successor counter`). This seat closed only the second half, and only as a wave artefact: the
counter's evidence rule admits `.ufo/waves/` paths only when the path ends with one of the item's
keys, which `sandboxed-confirm.py` does not. So R49.2 cannot honestly be marked `fixed` from this
deliverable alone — a lane-path carrier at a post-routing commit is still needed (the successor
counter under `tools/`, or a line in the round-50 lesson/`corpus/knowledge/pbt-generator-pilot.md:70`,
whose current sentence "The counter cannot tell a property-based generator from a differential one
that compares the mutant with a copy of…" is exactly the claim this harness now measures). The C1
seat owns that row; I did not touch `corpus/routed-defects.json`.

## Receipts in this directory

| file | what it shows |
|---|---|
| `sandboxed-confirm.py` | the harness (sha256 `1bbdc3b188d8…`); `--selftest` and the panel run |
| `sandboxed-confirm.json` | full receipt: rev, shas, binds, bwrap version, baseline leg, 13 probe reports, 12 mutant entries with confirmation comparables |
| `sandboxed-confirm.stdout` | the panel run's stdout (12 `MUTANT` lines + the `SANDBOXED_CONFIRM:` summary) |
| `selftest.stdout` | 18 selftest checks, `failed=0 ok=true` |
| `bwrap-version.txt` | `bubblewrap 0.13.1` |

## Summary

- The frozen generator at `e3729de` confirms all 12 public round-49 panel mutants inside a bwrap
  namespace holding only the generator, one guard and scratch (`confirmed=12/12`, baseline 400/400
  cases clean, exit 0).
- Each confirmation re-runs both guards on the counterexample in separate sandboxes and requires
  different output; all 12 differ.
- Negative control per run: lane guard and panel unopenable (`FileNotFoundError`), no `/home`,
  `git -C lane` exit 128, and exactly one `staged-id-guard.py` whose sha is the mutant's.
- The probe detects a leak: with the lane bound it reports `opened=true` and fails
  (`selftest.stdout`, `probe-detects-bound-lane`).
- Source inspection: the generator has no second-guard reference, no cwd, no absolute path; the
  round-49 differential cheat lived in the counter's environment.
- Reproducible (two runs, identical counts), 30 s wall, nothing installed, scratch deleted.
- Not closed: the frozen counter's `cwd`/`materialize` hole, F3 dump padding, F4 weak oracle, and
  fixture replay (CTL_FIX). R49.2 stays `open` until a lane-path carrier exists at a post-routing
  commit.

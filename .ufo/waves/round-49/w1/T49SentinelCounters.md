# T49SentinelCounters — hostile-input review of the two frozen round-49 counters and their controls

Seat: T49SentinelCounters (leaf, read-only on the lane). Read first: `.ufo/evidence/round-49/contract.json`
(never edited). Everything below is at base `8ca67421111fa354b47b803358391d0b07fc6db9`, counters at freeze bytes
`14d03ea4…`:

| file | sha256 |
|---|---|
| `.ufo/evidence/round-49/c1/measure.py` | `a055e9297cc989cc69062ae4a1e5b22c251dc3adfcc073211c5cae3a09346065` (same prefix the counter prints as `self=`) |
| `.ufo/evidence/round-49/c2/measure.py` | `f4971d02b8b1af40363f331ae2fadfffeec8ddf2fcbe0c4bc514ec25d8d0fde5` |
| `tools/staged-id-guard.py` (pinned) | `03a796c5726c30367d48618f3cbb0226b8dea9bc319171cbf20ffce319c2dca8` — matches the contract |

Method: (a) code review of both counters, both control harnesses, `deciding-run.sh` and the pinned round-21
monitor; (b) function-level probes that import the frozen counters read-only —
`.ufo/waves/round-49/w1/T49SentinelCounters.probe.py` → `T49SentinelCounters.probe.stdout`; (c) one end-to-end C1
run on a **scratch clone** of the lane at base under `strace` (baseline and hostile `reads.json`) —
`T49SentinelCounters.base-run.stdout`, `T49SentinelCounters.hostile-c1.stderr`,
`T49SentinelCounters.write-audit.txt`; (d) both counters' `--selftest` and `--list`. All work under
`/fast/scratch/hyaku/tameshi-r49/T49SentinelCounters` (removed before yielding). I wrote nothing in the lane, the
fleet repo or any sibling lane, and ran no mutating `git`/`jj` outside my own scratch clone.

The C2 counter has **no runnable end-to-end path here**: `measure()` requires `--panel` with
`PANEL_SHA=d6dd2cf3…` and the panel is hidden outside the lane. C2 findings are therefore proved against the exact
branch the counter executes (its own module, its own bytes) rather than by a full `measure()` run; each C2 finding
says which branch that is.

## What held (hostile inputs that are handled correctly)

- **Base reproduction is exact.** Scratch clone at base: `--list` yields `pointers=90`, floors
  `34/10/17/5/5/9/10`, no missing heading; a full run prints
  `C1_R49: self=a055e9297cc9 rev=… sections=64 covered=57 score=6 durable_covered=57/64 headings=7/7 pointers=90
  floor_short=0 unresolved=9 unverified=81 excerpt_miss=0 not_holds=0 absent=0 total=105 C1_R49_PASS=false`
  (`T49SentinelCounters.base-run.stdout`) — identical to the contract's `before`/CTL_0 shape.
- **Excerpts are never compiled as regex.** The check is `norm()` + substring (`c1/measure.py:307-312`); excerpts
  containing `.*`, `(a|b)`, `[a-z]+` score `excerpt_miss=1` and never crash.
- **Ranges are bounds-checked, fail-closed.** `1 <= s <= e <= line_count` (`c1/measure.py:299`); `n.md:0`,
  `n.md:5-3` and past-EOF all become `unresolved`; excerpt length is clamped to 24..400 (`:311`).
- **Path traversal is inert.** A `..` token is only ever handed to `git cat-file` (`c1/measure.py:171-190`,
  `blob()` at `:102-105`): git refuses it (`fatal: '../meta-secret.md' is outside repository`, exit 128) and it
  refuses a leading-`/` token too (`path '/n.md' does not exist in 'HEAD'`). No pointer token is ever `open()`ed as
  a filesystem path. `../X` becomes an external pointer whose blob must resolve at the row's 40-hex `fleet_commit`
  (`:284-292`) — read-only either way.
- **S-id rows with pipes are inert.** The extractor token is exactly `S\d{3,}` (`c1/measure.py:91`), so the
  registry regex at `:182` is built from a pipe-free token; ids that are not the leading cell
  (`|--- | S002 |<<< S003 |`) or are indented ≥4 do not resolve (probe: only `S001` resolved). C2's `records()`
  additionally requires exactly 11 cells (`c2/measure.py:285`), so a pipe-laden row is rejected, not misread.
- **Malformed reads documents fail closed.** Non-JSON, a top-level list, or non-dict rows yield `unverified`, never
  a pass (`c1/measure.py:383-387`, `:256-262`).
- **Dump rows are type-checked** before use (`c2/measure.py:203-205`), and both `--rev` parsers reject a leading
  `-` and pin `--end-of-options`+`^{commit}` (`c1:564-566`, `c2:445-447`).
- **Selftests pass:** `C1_R49_SELFTEST: cases=34 failed=0`, `C2_R49_SELFTEST: cases=11 failed=0`.

---

## F1 — HIGH — C2: the scored guard is writable by the generator it scores

**Where:** `c2/measure.py:253` (the *only* guard-integrity check, inside `materialize`), `:258-265` (the guard is
written into `work/tree/tools/`, which is the generator's own cwd), `:213-224` (`run_generator` passes
`--guard gp` and runs with `cwd=os.path.dirname(gen)`), `:341-344` (the kill criterion compares
`run_guard(gp, …)` — the possibly-overwritten guard — against `run_guard(mp, …)`).

**Exploit path.** The generator receives, in its own working directory, the path of the guard it is scored against,
and no run re-checks that path. A generator that rewrites `--guard` turns every "kill" into a comparison of its own
stub with the mutant. It needs no knowledge of the hidden panel: on each mutant run it exits 1 with
`counterexample=<index>` and dumps a case on which its stub (say exit 2) differs from any guard. The oracle axis is
not a defence — the oracle is applied only to the **pristine** dump cases (`:316-321`), whose contents the generator
chooses, while the kill case is never oracle-checked.

**Evidence** (`T49SentinelCounters.probe.stdout`):
```
FINDING F1 generator exit=1 guard_sha_after_run_matches_pin=False
FINDING F1 kill-branch verdict=confirmed pristine=(0, '{"stubbed": true}') identical_mutant=(1, '{"cascade": [], …
```
After one pristine run the guard on disk is no longer the pinned file, and a **byte-identical** "mutant" — one that
cannot be killed by construction — is scored `confirmed`, because the pristine side of the comparison is the stub.

**Impact.** `C2_R49_PASS` can be reached with zero real kills; `confirmed`/`selftest_kills` are then not evidence of
generator strength, and CTL_FIX/CTL_ABSENT would not notice (they never touch the guard).

**Smallest remediation.** Re-hash after every `run_generator`: `if sha(open(gp,'rb').read()) != GUARD_SHA:
raise Setup(...)`, and run the kill comparison against a fresh copy rewritten from the frozen `gbytes`
(`work/ref/staged-id-guard.py`), so the comparison never reads a file the generator can reach.

## F2 — HIGH — C1: a crash is "exit 1 = measured not-pass", and one unhashable field consumes the single deciding invocation

**Where:** `c1/measure.py:262` — `index.setdefault((r.get('heading'), r.get('ordinal'), r.get('raw')), [])` uses row
fields as dict keys with no type filter (`:257-258` checks only that `rows` is a list, `:261` only that a row is a
dict). Exit semantics: docstring "0 PASS, 1 measured not-pass, 2 setup error"; `main()` maps only `Setup` to 2
(`:584-586`), so an uncaught `TypeError` reaches Python's handler → **exit 1**.

**Exploit path / repro.** Scratch clone at base plus one commit adding `.ufo/evidence/round-49/c1/reads.json` with
`"raw": ["mutation-case-kimi-census.md:4-7"]`:
```
python3 <lane>/.ufo/evidence/round-49/c1/measure.py --lane <clone> --rev 175f21de --work <scratch>/wh \
        --fleet /home/vgpnk/Projects/shokunin
-> TypeError: cannot use 'tuple' as a dict key (unhashable type: 'list')   (measure.py:262, via :388)
-> exit 1, stdout contains no C1_R49 line
```
Receipt `T49SentinelCounters.hostile-c1.stderr` (`# exit: exit=1`, `# stdout contains a C1_R49 line? 0`); the same
crash fires for `heading` as an object and `ordinal` as a list.

**Impact.** `deciding-run.sh:47-50` records `c1.exit=1` and `tail -1` prints a traceback line; a consumer that reads
only exit codes records "claim false". Because the kill rule allows exactly one deciding invocation, a type slip in
a 90-row hand-merged evidence file voids the round's C1 row instead of producing a verdict.
Reachability today: `c1/merge-reads.py:74-80` always builds `heading`/`ordinal`/`raw` from the pointer
(str/int/str), so this cannot arrive through that tool — it needs a hand edit, another producer, or an `EXTRA_ROWS`
schema change. The counter has no defence because it has no type check.

**Smallest remediation.** Skip rows that are not `{heading: str, ordinal: int, raw: str}` on load, and add
`except (OSError, ValueError, TypeError, KeyError)` around `measure()` → `C1_R49: setup=<exc>`, return 2.

## F3 — MEDIUM — both counters: unbounded `int()` on long digit runs crashes instead of reporting

**Where:** C1 `measure.py:112-117` (`parse_ranges` → `int(s)` at `:116`), reached from `extract()`; C2
`measure.py:308` (`int(pr['last'].group(1))`) and `:339` (`int(mr['last'].group(3))`).

**Exploit path.** C1: a pointer range of ≥4300 digits (`n.md:` + `'9'*5000`) — content-borne, so reachable only
through a SKILL.md edit, i.e. the L1's own text. C2: the *generator's* stdout, which is untrusted-to-verify —
`PBT_STAGED_ID: cases=<5000 digits> …`, or `counterexample=<5000 digits>`. Both raise
`ValueError: Exceeds the limit (4300 digits) for integer string conversion` → exit 1 (F2's conflation) instead of
`unresolved` / `generator-error`.

**Evidence** (`probe.stdout`): `FINDING F3 digits=5000 -> ValueError …`;
`FINDING F3 big-cases -> measure.py:308 raises ValueError …`;
`FINDING F3 big-ce -> measure.py:339 raises ValueError …`. A 100-digit range is fine (bounds check → `unresolved`),
and a 100 MB dump *string* is only memory/time, not a crash.

**Smallest remediation.** Reject range components longer than 12 characters (or `int(s[:12])`) as `unresolved`; in
C2 validate `len(group) <= 6` before `int`, or parse inside the existing guarded block.

## F4 — MEDIUM — C2: the mutant `--selftest` child has no `cwd` (lane cwd at deciding time) and no timeout handler

**Where:** `c2/measure.py:331-333`:

```python
st = subprocess.run([sys.executable, '-I', mp, '--selftest'], capture_output=True,
                    env=env_for(work), timeout=GUARD_TIMEOUT)
```

No `cwd=` — every other child sets one (`:177` `cwd=d`, `:219` `cwd=os.path.dirname(gen)`) — and no `try` around it
(unlike `:177-179` and `:219-221`).

**Exploit path.** `deciding-run.sh:19` does `cd "$LANE"`, so this child's cwd is the lane checkout: a mutant that
writes a relative path during `--selftest` (or an accidental fixture) lands in the lane during the single deciding
run. A mutant whose `--selftest` hangs raises `subprocess.TimeoutExpired` — uncaught — 60 s into the mutant loop.

**Evidence.** `probe.stdout`: `FINDING F4 relative write lands in the inherited cwd=<…>/cwdtest file=True` (the
exact argv/env shape, launched from a chosen cwd) and `FINDING F4 an unguarded timeout raises TimeoutExpired
(frozen timeout=60 s, reproduced at 3 s)`; the frozen 60 s variant was also observed directly:
`UNCAUGHT TimeoutExpired from the measure.py:332-333 call shape: cmd=--selftest timeout=60`.

**Impact.** Latent today — `tools/staged-id-guard.py` contains no `open`, `subprocess` or `tempfile` call, so its
selftest writes nothing — but it is the only unpinned child in either counter and it sits in the deciding path. A
hanging mutant also kills the deciding run.

**Smallest remediation.** `cwd=os.path.join(work, 'mut', m['id'])`, and
`except subprocess.TimeoutExpired: st_kill = True; print('MUTANT %s selftest-timeout' % m['id'])`.

## F5 — MEDIUM — C2: no containment or post-run check for generator side effects; `TMPDIR` is advisory

**Where:** `c2/measure.py:81-86` (`env_for` sets `TMPDIR=work/tmp`), `:213-224` (`--dump` under `work`, `cwd` = the
generator's own dir under `work/tree/tools`). Nothing compares the work tree, the lane or `/tmp` before and after a
run; the counter reads only the exit code, the last stdout line and the dump.

**Exploit path.** A generator writing an absolute path (into the lane, `$HOME`, or anywhere outside `--work`) is not
detected: exit is 0 and the interface tokens still parse, so `pristine_bad`, `oracle_disagree` and `classes_short`
are unaffected.

**Evidence** (`probe.stdout`): `FINDING F5 generator exit=0 wrote_outside_work=True (work=<…>/probe/c2w)` — the file
was created outside `--work` while the run reported `cases=400 violations=0`.

**Impact.** Trust boundary rather than a live bug (the generator is lane-authored code), but the claim is "the
generator against the gate", and the counter cannot tell a reader from a writer. Same root cause as F1.

**Smallest remediation.** Snapshot the work tree (`stat`/sha of its files) and `git -C <lane> status --porcelain
-uno` before the first run and after the last, and fail closed on any difference; when the generator is final,
`chmod 0444` the guard and re-hash (F1).

## F6 — MEDIUM — both counters: setup failures that are not `Setup` exit 1, not the documented 2

**Where:** C1 `main()` `:578-579` (`os.makedirs(work, exist_ok=True)` then `os.listdir(work)`) and `except Setup`
`:584-586`; C2 `main()` `:451-452`, `except Setup` `:459`.

**Repro:** `--work <existing regular file>` →
`FileExistsError: [Errno 17] File exists: …/workfile`, exit **1**, in both counters (observed: `c1 workfile exit=1`,
`c2 workfile exit=1`). Same class: an unreadable `--panel`, a `git` failure in `durability_commit`, any `OSError`.

**Impact.** The exit code is the only machine-readable signal `deciding-run.sh` consumes (`:44-50`): a run that
never happened is recorded as a claim that failed.

**Smallest remediation.** Put the work-dir setup inside `try: … except OSError: return 2` with a `setup=` line, i.e.
widen the umbrella to `except (Setup, OSError)`.

## F7 — LOW — C1: the durable term has no ≥64 floor and no total comparison (latent fail-open)

**Where:** `c1/measure.py:396-401`: `bad_mon` carries `(0 if mon['total'] >= 64 else 1)` plus the strict/`False`
override test, but the durable term is the bare `(dur['total'] - dur['covered'])`.

**Exploit path.** If the monitor ever exits 0 with `sections_total == sections_covered == 0` at the probe tag
(`run_monitor` accepts any exit-0 JSON, `:319-334`), the durability clause contributes 0 and "still credits every
section after an append" is satisfied vacuously. Not reachable with the pinned monitor today: the probe commit is
`read-tree REV` plus five appended lines, so SKILL.md is byte-identical and `sections_total` cannot move.

**Smallest remediation.** `if dur['total'] < 64 or dur['total'] != mon['total']: bad_dur += 1`.

## F8 — LOW — C1: durability is proved against a hardcoded five-file list; the ledger is never read

**Where:** `c1/measure.py:65` `VOLATILE = ('LOG.md','SCORECARD.md','corpus/SOURCES.md','corpus/QUALITY.md',
'corpus/README.md')`; `:336-373` appends `PROBE_LINE` to exactly those. The counter has no reference to the ledger or
to entry `inputs` (`grep -n 'ledger\|inputs' .ufo/evidence/round-49/c1/measure.py` → no match), so it cannot see what
the seven target entries are keyed to.

**Exploit path.** The work plan keys each section to "the sections' cited non-record files". If an entry is keyed to
a *record* file outside `VOLATILE` — or to a report/knowledge file the next round appends to (this round's
`corpus/knowledge/pbt-generator-pilot.md`, a `.ufo/evidence/round-4x/…` file, a later record file) — credit lapses
after that round's append while the counter still prints `durable_covered=64/64`. The contract's *predicate* names
exactly those five files, so the counter is consistent with the predicate; the contract's prose ("a later record
append cannot lapse them") is broader than what is measured. This is report-side wording, not a counter bug — but
the deciding line must not be read as proving the prose.

**Smallest remediation.** Print the union of the seven entries' input paths in the `C1_R49` line and assert that no
input equals one of `VOLATILE` (catches the mechanical re-key); the round report then states exactly which files
durability covers.

## F9 — LOW — C2: `map`/`map_inadmissible` classes are answer-derived and never oracle-checked

**Where:** `c2/measure.py:117-147`: for `map != None` the only predicates are `cl.add('map')` (`:145`) and
`if exitc == 1: cl.add('map_inadmissible')`; the counter's oracle (`:90-112`) is applied only when
`case['map'] is None` (`:316-321`), so no map case's admissibility is ever checked.

**Impact.** Ten arbitrary map cases on which the guard answers 1 satisfy `map_inadmissible >= 10`; the map axis is
weaker evidence than the class counts suggest. The claim ("each of 12 classes in ≥10 cases") is still met literally.

**Smallest remediation.** Add an admissibility oracle (every map key resolves and every id exists) and require
`exit == 1` **and** inadmissible-by-oracle for the class.

## F10 — LOW — C2: a liveness difference counts as a semantic kill

**Where:** `run_guard` returns `(124, None, b'')` on `TimeoutExpired` (`:176-179`); `comparable` (`:188-193`) turns
that into `(124, b'')`, which the kill branch (`:341-344`) accepts as an observation.

**Impact.** A case that makes the pristine guard hang 60 s while the mutant answers is scored `confirmed`.
Contrived, and largely subsumed by F1, but a timeout is not a behavioural difference.

**Smallest remediation.** Treat `exit == 124` on either side as `unconfirmed` (printed as such), so a kill needs two
real answers.

## F11 — LOW — C2: determinism from the seed is promised but never tested

**Where:** `c2/measure.py:213-224` with `SEED, CASES = 4949, 400`; `run_generator` is called once per tag (`:305`,
`:336`) and neither the dump nor the summary line is compared across runs.

**Impact.** The interface promises "deterministic from the seed"; the deciding run is a single invocation, so a
nondeterministic generator is indistinguishable from a deterministic one. This is the one flaky-test property the
coverage claim leans on, and it is unmeasured.

**Smallest remediation.** Run the pristine generator twice into two dumps and require identical bytes.

## F12 — LOW — lane artifact: the C1 tooling imports the counter from the lane without disabling bytecode

**Where:** `.ufo/evidence/round-49/control/c1-controls.py:28-30` and `.ufo/evidence/round-49/c1/merge-reads.py:23-25`
`exec_module` the counter from the lane before any `sys.dont_write_bytecode = True` (the one inside the imported
module applies only to *its* own imports).

**Evidence.** `.ufo/evidence/round-49/c1/__pycache__/measure.cpython-314.pyc`, mtime
`2026-10-26 17:10:41.816837790 -0300` (freeze/control scoring, hours before this seat; my probes set the flag before
importing). `.gitignore:4` is `__pycache__/`, so it is an *ignored* lane write, not a tracked one; the deciding path
itself is clean (script mode writes no `.pyc`, and the counter sets the flag before importing the monitor).

**Impact.** An ignored artifact inside the lane during control scoring; it cannot alter REV bytes, but it contradicts
"the lane is never written" and pollutes later audits.

**Smallest remediation.** `sys.dont_write_bytecode = True` at the top of both tools (or run them with `python3 -B`);
delete the existing `__pycache__`.

## F13 — INFO — scratch hygiene and the lane-write audit

- **Every counter write stays under `--work`** (`strace -f -e trace=%file` over the full C1 run, receipt
  `T49SentinelCounters.write-audit.txt`): 80 write-mode file operations under the work dir (`monitor-rev.json`,
  `monitor-durable.json`, `dur/`, its objects, `dur.index`), 32 relative ones inside the work clone
  (`.git/objects/*/tmp_obj_*`, plus git's own `symlink("testing", <clone>/.git/…)` support probe), **0 under the
  lane, 0 under `/tmp`**, and the only absolute path outside `--work` is `/dev/null`. The `--shared` durability
  clone writes its objects into itself (`dur/.git/objects`, run mtime), so nothing spills into the lane.
- The pinned monitor's *measure* path writes nothing (round-21 wrapper → round-18 `main()`: blob reads only). Its
  `--selftest` hardcodes `dir='/tmp'` (`.ufo/evidence/round-21/coldread/measure.py:38`), ignoring `TMPDIR` — not on
  any counter path, but relevant if anyone runs that selftest under the fleet's "nothing in /tmp" rule.
- **Clean-up:** neither counter removes `--work` (`dur/` is left behind by design); `deciding-run.sh:51`
  `rm -rf "$SCR"` runs only on normal completion, so an interrupted deciding run leaves the work dirs.
- **Controls gate is advisory:** `deciding-run.sh:29` refuses a second invocation only via `[ -e "$OUT/$k.start" ]`,
  and `OUT` is caller-chosen (`:22` checks only that it is a directory — not that it is inside the lane or empty). A
  second deciding run into a fresh empty `OUTDIR` passes gate 0; the committed receipts, not the gate, are the
  evidence.
- **Cost:** one full C1 run = 98 s wall / 11 m 36 s user (the monitor is CPU-heavy); a hostile `reads.json` costs the
  same before it crashes (272 s under strace).

## Tooling

Nothing installed or upgraded (no `pacman` — host-wide pause respected anyway —, `uv`, `npx` or binary fetch was
needed); `strace` and `python3 3.14.8` were already present.

## Summary

- Both counters reproduce the contract's base state exactly, and their selftests, bounds checks, excerpt matching,
  `..`/S-id/pipe handling and write containment under `--work` all hold.
- **F1 HIGH (C2):** the generator is handed a writable path to the guard it is scored against and the sha pin is
  checked only before the runs — a byte-identical mutant scores `confirmed` once the guard is stubbed; 12/12 kills
  are obtainable without the hidden panel.
- **F2 HIGH (C1):** a crash exits 1, the same code as "measured not-pass", and one unhashable `reads.json` field
  voids the single deciding invocation (observed end-to-end: TypeError at `measure.py:262`, no `C1_R49` line).
- **F3-F6 MEDIUM:** unbounded `int()` on 4300+ digit runs (C1 ranges, C2 `cases=`/`counterexample=`); the mutant
  `--selftest` child has no `cwd` (lane cwd at deciding time) and no timeout handler; no side-effect containment or
  post-run check for the generator (absolute writes escape `--work` with exit 0); non-`Setup` failures exit 1.
- **F7-F12 LOW:** durable clause without a ≥64 floor; durability proved only against five hardcoded files (ledger
  never read); `map` classes oracle-free; timeouts count as kills; determinism untested; `__pycache__` written into
  the lane by `c1-controls.py`/`merge-reads.py`.
- Fixes are small: re-hash the guard post-run against a fresh copy (F1), type-filter reads rows and map crashes to
  exit 2 (F2/F6), cap digit runs (F3), add `cwd`+timeout handling (F4), snapshot side effects (F5).

# T48SentinelTmp — §7.4 /tmp hardcoding audit (round 48, w1)

Seat: sentinel (operability). Item: audit every committed counter / probe / gate under
`tools/*.{py,sh}` and `.ufo/evidence/round-4[0-7]/` for writes under `/tmp` that ignore
TMPDIR/`--work`, plus the two round-48 counters once they land; report the C1 counter's per-round
disk footprint and its cleanup between rounds.

Lane base `473336d9d789f6081195e7376d17836a24666bc3`. Read-only on the lane; nothing in the lane
was edited except this file. Scratch `/fast/scratch/hyaku/tameshi-r48/T48SentinelTmp` was created,
used and deleted. No tool was installed.

## Verdict

**14 write sites in 12 files are routed defects** under the literal reading of the lane rule (a
committed counter/probe/gate that writes under `/tmp` regardless of TMPDIR/`--work`). Every one of
them is a default argument or a `dir="/tmp"`: the caller can always override, but nothing in the
program consults TMPDIR.

Two of the 14 are *not* selftest fixtures — they run on deciding paths:
`tools/registry-check.py:766` (clones the lane under `/tmp` to resolve a revision) and
`.ufo/evidence/round-46/deciding-run.sh:20` (the deciding-run work root, default
`/tmp/tameshi-r46-deciding`).

The defect is live in this round, not theoretical: 23 directories / 24 MB created **today
2026-10-26** are sitting in `/tmp` from those sites (§5), and the three observation seats' rounds
run seven of the /tmp-hardcoded tools inside profiles P1–P5 whose whole point is that TMPDIR is
redirected (§6).

**Both round-48 counters are clean on this axis.** The C1 counter refuses a `--work` under `/tmp`
outright and deletes each round's clones before the next (§7); the C2 counter has no `/tmp` literal
and no `dir=`. The C1 counter's per-round footprint is **1.82 GB** (12 full `--no-hardlinks` clones),
residual after a round **28 KB**.

## 1. Method

```
S=/fast/scratch/hyaku/tameshi-r48/T48SentinelTmp; export TMPDIR="$S"
git clone -q --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin "$S/lane"
# corpus
grep -rn -E "(tempfile\.(mkdtemp|TemporaryDirectory|NamedTemporaryFile)|mktemp|['\"]/tmp/|dir=[\"']/tmp[\"']|gettempdir)" \
     --include="*.py" --include="*.sh" tools/ .ufo/evidence/round-4[0-7]/
```
112 matching lines in 46 files. Each hit was read in context (allocation site, override argument,
cleanup) and classified. Data files that merely *mention* `/tmp` (`.ufo/evidence/round-44/after/
coldread.json`, `round-45/{before,after}/coldread.json`, `round-45/freshness/reviews.json`,
`round-47/coverage/sources/lam-2020-reruns.txt`) are not code and are excluded.

## 2. Routed defects — writes under /tmp regardless of TMPDIR

| # | path:line | what it does | honours TMPDIR? | routed defect |
|---|---|---|---|---|
| 1 | `tools/bash-witness-study.py:1240-1241` | `mkdtemp(..., dir="/tmp")` selftest root; parent of the child root | no | **yes** |
| 2 | `tools/repeat-control.py:597` | `mkdtemp(dir="/tmp")` selftest scratch | no | **yes** |
| 3 | `tools/pin-disposition.py:706` | `mkdtemp(dir="/tmp")` selftest scratch | no | **yes** |
| 4 | `tools/evidence-disposition.py:2351` | `mkdtemp(dir="/tmp")` selftest scratch | no | **yes** |
| 5 | `tools/context-capture.py:1624-1625` | `mkdtemp(dir="/tmp")` selftest harness root | no | **yes** |
| 6 | `tools/registry-check.py:766` | `mkdtemp(dir="/tmp")` **deciding path**: clone of the lane to resolve `rev` | no | **yes** |
| 7 | `tools/registry-check.py:916-917` | `mkdtemp(dir="/tmp")` selftest scratch | no | **yes** |
| 8 | `tools/env-diff.py:61` | `TemporaryDirectory(dir="/tmp")` host side of the bwrap probe (the guest sees `--tmpfs /tmp`) | no | **yes** |
| 9 | `tools/mutate-and-run.sh:482` | `mktemp -d /tmp/tameshi-r4-2-run.XXXXXX` when `--workdir` absent | no | **yes** |
| 10 | `tools/mutate-and-run.sh:1360` | `mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX` regression auto root | no | **yes** |
| 11 | `tools/mutate-and-run.sh:1477` | `mktemp -d /tmp/tameshi-r4-2-selftest.XXXXXX` | no | **yes** |
| 12 | `tools/tally-audit-v3.py:422` | `auto_root()` really creates `/tmp/tameshi-r4-2-regression.<6>` to reproduce the runner's auto root | no | **yes** |
| 13 | `.ufo/evidence/round-21/coldread/measure.py:38` | `TemporaryDirectory(dir="/tmp")` in `--selftest`; this file is the **calibration axis** statement of C1 | no | **yes** |
| 14 | `.ufo/evidence/round-46/deciding-run.sh:20` | `WORK=${4:-/tmp/tameshi-r46-deciding}` — gate work root | no | **yes** |

Notes on the table:

* #6 and #14 are the two that matter at deciding time. #6 puts a second copy of the lane
  (152–225 MB, §7) under `/tmp` for every `registry-check` invocation; #14 makes the gate's work
  root a fixed `/tmp` path and the deciding run never removes it (§8, note 3).
* #9/#10/#11 are the same runner. `--workdir` overrides #9, and the statement
  `six-leg regression ledger` does pass `{work}/regression-wd`, so the C1 rounds do not hit the
  auto root; #10 still fires on every `--regression` invocation that omits `--workdir`, and the
  root is kept when the run does not PASS.
* #12 is the honest one: the audit *has* to reproduce the runner's `/tmp` literal to test it, so
  the defect is inherited from #10. It is still a write under `/tmp` that ignores TMPDIR, and it
  is cleaned only by `atexit` (`atexit.register(... rmtree)`), which does not run on SIGKILL,
  timeout or `os._exit`.

## 3. Adjacent: ignores TMPDIR but does not write under /tmp

| path:line | behaviour | honours TMPDIR? | routed defect |
|---|---|---|---|
| `.ufo/evidence/round-47/deciding-run.sh:19` | `WORK=${4:-/var/tmp/tameshi-r47-deciding}` | no | no (not `/tmp`) |
| `.ufo/evidence/round-47/quality/falsifiers.sh:8` | `mktemp -d -p /var/tmp` | no (`-p` overrides TMPDIR) | no (not `/tmp`) |
| `tools/trace-inputs.py:577-593` | candidate chain `gettempdir(), /var/tmp, /dev/shm, ~/.cache, /tmp` | yes first, `/tmp` last resort | no — but the last resort is a `/tmp` write that only happens when TMPDIR is unusable, and it is silent |
| `.ufo/evidence/round-45/freshness/integrate.py:22` | `--glob` default `/tmp/tameshi-r45-ExecRows*/S[0-9][0-9][0-9].json` | no | no — it **reads** `/tmp`, never writes; `--glob` overrides |
| `tools/tally-audit-v2.py:265` | fixture triple `('/tmp/tally-audit-work','1','0')` | n/a | no — `auto=1` takes the `mktemp` branch; `/tmp/tally-audit-work` does not exist on this host (checked) |
| `tools/tally-audit-v3.py:403` | fixture triple `('/tmp/tally-audit-explicit','0','0')` | n/a | no — same: no such directory exists |
| `.ufo/evidence/round-45/freshness/measure.py:384` (and the byte-identical `round-46/hardening/freshness-counter.py:384`, `round-47/hardening/freshness-counter.py:384`) | `{'report': '/tmp/Rev.md'}` inside a **reviews JSON fixture** | n/a | no — a string in fixture data, never opened for write |

## 4. Honours TMPDIR (no `dir=`, or `dir=` pointing into TMPDIR/`--work`) — audited, not defects

`mkdtemp()` / `TemporaryDirectory()` with no `dir=` passes TMPDIR to the kernel; these are all
clean, and every one below removes what it creates unless noted:

* tools: `witness-metadata.py:1122`; `trace-inputs.py:593,703`; `receipt-window.py:327`;
  `receipt-measure.py:251`; `env-diff.py:167`; `round21-measure.py:38`; `wave-accounting.py:156`;
  `command-binding.py:174`; `registry-replay.py:149,208`; `mte-interop.py:199,276,309,386`;
  `golden-verdict.py:47`; `write-path-census.py:93`; `write-path-census-v4.py:470,501,516`;
  `tally-audit.py:363,418`; `tally-audit-v2.py:562,656`; `tally-audit-v3.py:766,887`.
* evidence: `round-40/census:151`; `round-41/census:170`; `round-42/calibration:268,271`;
  `round-42/census:79,117,381`; `round-43/mutants:77,116,519`; `round-43/guard:176`;
  `round-45/freshness:114,305`; `round-45/coverage:146`; `round-45/control/run-controls.py:51`;
  `round-46/after/extra-receipts.py:32`; `round-46/control/run-controls.py:47`;
  `round-46/calibration:303`; `round-46/hardening/mutate.py:50,92`;
  `round-46/hardening/{freshness,coverage}-counter.py:114,305,722 / 146,236,331`;
  `round-46/coverage:207`; `round-46/quality/no-harm-gate.py:393`;
  `round-46/quality/seat-name-check.py:50`; `round-47/coverage:206`; `round-47/calibration:426`;
  `round-47/hardening/pool.py:169,196`;
  `round-47/hardening/freshness-counter.py:114,305,740,856,863,1015,1042,1290,1381,1607`;
  `round-47/hardening/coverage-counter.py:146,245,340,491,641`;
  `round-47/quality/lesson-quote-check.py:127`.
* shells without a template (`mktemp -d` uses `$TMPDIR`): `round-46/after/entry-rechecks.sh:7`,
  `round-46/quality/falsifiers.sh:9`, `round-46/deciding-run.sh:33`, `round-47/deciding-run.sh:32`,
  and the fixture harnesses embedded at `tools/tally-audit.py:316`, `tally-audit-v2.py:514`,
  `tally-audit-v3.py:718` (`mktemp -d "$TMPDIR/h.XXXXXX"`).

Cleanup gap inside this group (operability, not §7.4): **`round-46/control/run-controls.py:47`,
`round-47/control/run-controls.py:54`, `round-47/control/c1-controls.py:39` create a `mkdtemp` and
the file contains no `rmtree` at all** (`grep -c rmtree` = 0 for all three), so every invocation
leaves a full clone of the lane in TMPDIR. `round-45/control/run-controls.py:51` does remove its
three (`rmtree` at 187/192/197).

## 5. The defect is live on this host (evidence, 2026-10-26)

```
$ ls -d /tmp/tameshi-r4-2-regression.* | wc -l          -> 20   (3656 KB in the non-empty ones)
$ ls -d /tmp/tameshi-r14-evidence-disposition-selftest.* -> 3   (20364 KB)
$ stat -c '%y %n' /tmp/tameshi-r4-2-regression.uDPiWT
  2026-10-26 05:50:29 -0300     (contents: specs/ + bash-checklist-run, bash-mado-verify,
                                 bash-surface-census, bash-tsukuroi-census, js-claims-check,
                                 js-kimi-census, js-round-gate — a real regression run)
$ ls /tmp | wc -l -> 297 ; du -sh /tmp -> 577M
```

Three consequences:

1. `/tmp/tameshi-r4-2-regression.uDPiWT` is a **kept** regression auto root (`run_regression`
   removes `$root` only on PASS, `mutate-and-run.sh:1464-1467`; on failure it prints
   "scratch kept"). A failing leg accumulates 3.6 MB in `/tmp` with no cap and no age-based
   removal.
2. `tameshi-r14-evidence-disposition-selftest.*` exists although `evidence-disposition.py` *does*
   call `shutil.rmtree(scratch)` at 3122: at least one exit path (a `SystemExit`/`CannotAudit`
   before the end of `selftest()`) skips it. `dir="/tmp"` plus a non-exception-safe cleanup is
   how 20 MB survived.
3. During a 6.7 s window in which the C2 selftest ran (05:5x), **eight further
   `/tmp/tameshi-r4-2-regression.*` directories appeared**. Attribution to one writer is not
   established — three code sites produce that exact prefix (#10, #12, and the runner block #12
   injects) — but all three ignore TMPDIR, and this is exactly the cross-seat interference the
   hardcoding creates while nine observation rounds run concurrently.

## 6. Why this is a calibration hazard, not only untidiness

The round-47/48 C1 counter builds six profiles (`measure.py:174-186` in the r47 base): `P0` is the
host environment, and `P1`–`P5` are fixed environments with `TMPDIR = <work>/<prof>/tmp`. The
`env` dependence, and the `P2`/`P3`/`P4` bwrap/jj/node dependences, are read as "does the picked
line change between `P0` and `Pi`".

A tool that hardcodes `/tmp` cannot show a TMPDIR dependence, so for the eight statements whose
commands are one of the tools in §2 the counter is **structurally blind to the one environment
variable the profile is varying**:

* `repeated pristine-control gate` → `repeat-control.py` (#2)
* `six-leg content-disposition probe` → `pin-disposition.py` (#3)
* `effective expectation reconciliation` → `evidence-disposition.py` (#4)
* `hermetic env-differential probe` → `env-diff.py` (#8)
* `mutation sweep runner` / `six-leg regression ledger` → `mutate-and-run.sh` (#9–#11)
* `tally-audit-v3 runner audit` and `bounded ANSI-C code_view` → `tally-audit-v3.py` (#12)
* `calibration` (axis) → `coldread/measure.py` (#13)

Second, the profiles are not hermetic for those tools: under `P1`–`P5` they write to the **host**
`/tmp`, not `<work>/<prof>/tmp`. With `--jobs 6` inside a round and three observation seats running
the same 22 statements at once, two runs of a fixed literal path (e.g.
`/tmp/tally-audit-work`, `/tmp/tally-audit-explicit`, the `tameshi-r4-2-*` roots) can interleave.
A resulting one-off difference would be recorded by the C1 counter as `nondeterministic` and
attributed to the statement, not to the shared path — the same class of error round-47 closure
routed (a one-shot flaky observation restated as a standing value).

## 7. Round-48 counters

### `T48ExecC1Counter.measure.py` (→ `.ufo/evidence/round-48/calibration/measure.py`)

| check | result |
|---|---|
| `/tmp` literals in the file | none for writes |
| `--work` under `/tmp` | refused: `C1_R48: --work must not be under /tmp (lane rule, round 48 §7.4)`, exit 2. Probe with `--work /tmp/c1-sentinel-probe`: **no directory created** (`ls -d` → ENOENT). Test `T63_work_under_tmp_refused` pins it. |
| scratch root choice | `scratch_root()` (line 103): `TMPDIR` first, `/fast/scratch` as fallback, **rejects** a realpath under `/tmp`, exits 2 if neither works |
| selftest fixtures | `tempfile.mkdtemp(prefix='c1-r48-', dir=root)` (line 784), `rmtree` in `finally` (line 789) |
| per-round clones | `setup_profile()` (line 326) clones the lane **twice per profile** with `--no-hardlinks` (mirror + clone) → **12 full copies per round** |
| cleanup between rounds | after each round, `rmtree` of `<round>/<prof>/{clone,fleet,shim,home,tmp}` (lines 461-466) — executed for every round, including the last |
| measured peak | **1,864,620 KB ≈ 1.82 GB** per round (measured directly on the r47 base with the same `setup_profile`: one `--only` probe leaves 6 `clone` + 6 `fleet/<lane>` dirs = 1,864,620 KB) |
| measured residual | **28 KB** after a completed `--rounds 1 --only "staged-id adoption guard" --jobs 6` probe (only `round1/decoy` and the empty `P0..P5` dirs remain) |
| R=3 total | 3 × 1.82 GB **sequential**, peak 1.82 GB if the clones are deleted on time (the design), 5.5 GB if a round is skipped |
| failure path | `return 2` on `clone/checkout failed` (line 448) happens **before** the `rmtree` loop → up to 11 clones (≈1.7 GB) left in `work` when a clone fails or the process is killed |

The R=3 loop is correct: rounds are sequential, each round's results are appended to
`run_results` before the clones are removed, and the `P`/`round` index is threaded into the
observation context, so deleting the clones cannot invalidate a later round.

### `T48ExecC2Counter.measure.py`

No `/tmp` literal anywhere. Two `tempfile.mkdtemp()` sites, both without `dir=` and both removed in
`finally`: census `work` (line 390, rmtree 401) and the selftest root (line 644, rmtree 823).
Probe: `TMPDIR=<scratch>/t python3 T48ExecC2Counter.measure.py --selftest` → `C2_R48_SELFTEST:
cases=43 failed=0` in 6.7 s, `TMPDIR` residue **empty**.

### `T48ExecC1Controls.run-controls.py`

Docstring (line 33-35) states it writes only under `--work` and sets TMPDIR for every child below
`--work`. Verified: no `/tmp` literal; `--work` must be empty or absent (line 309); `sh(['git',
'clone', '-q', '--shared', lane, dest])` under `--work` (line 188); TMPDIR set per child
(line 250-253). It removes the counter's per-control *run* dir before the run (line 246-247) but
never removes the `--shared` clones it makes for each control, so a 5-control run leaves ~760 MB
under `--work` until the seat's own cleanup.

## 8. Smallest remediation

1. Python (7 sites, #1–#5, #7, #13 plus #8's host side): delete `dir="/tmp"`. `mkdtemp()` /
   `TemporaryDirectory()` already honour TMPDIR, and every one of these sites is a selftest fixture
   whose parent is a private per-run directory.
2. `tools/mutate-and-run.sh:482,1360,1477`: `mktemp -d "${TMPDIR:-/tmp}/tameshi-r4-2-…
   .XXXXXX"`; and on a failing regression, keep the root only under `--keep` (currently any
   non-PASS keeps it, which is the accumulation in §5).
3. `tools/registry-check.py:766`: same one-line change; it is a deciding-path clone, so it is the
   one that costs a full lane copy per run.
4. `.ufo/evidence/round-46/deciding-run.sh:20`: `${4:-${TMPDIR:-/var/tmp}/tameshi-r46-deciding}`
   plus `trap 'rm -rf "$WORK"' EXIT` — the deciding run currently removes `$WORK` only *before*
   the counter, never after, so a round-46 deciding run leaves the counter's 1.8 GB `/tmp` work
   tree behind.
5. `round-46/47` control scripts: add the `finally: rmtree` that `round-45/control/run-controls.py`
   already has.
6. `T48ExecC1Counter.measure.py` (if it is to be hardened): move the per-round clone removal into
   a `finally` around the round body so the clone-failure `return 2` cannot leak 1.7 GB.

These files are in the round-47 frozen pathspec (`tools` is listed in
`round-47/deciding-run.sh:33`), so the remediation belongs to a round that re-freezes them; nothing
here was edited.

## 9. Not established

* Whether any *deciding* value has already been perturbed by the shared `/tmp`. The eight
  directories that appeared during the C2 selftest window cannot be attributed to one writer.
* The C1 counter's full `--selftest` was launched under `TMPDIR=<scratch>/t`; the shell backend
  became unresponsive under the concurrent observation rounds and its output was not observed.
  The static evidence (`scratch_root()`, `mkdtemp(dir=root)`, `rmtree` in `finally`) and the
  `--only`/`--rounds 1` probe in §7 stand on their own.
* Peak RSS of the 12-clone round: only disk was measured.

## 10. Scratch

`/fast/scratch/hyaku/tameshi-r48/T48SentinelTmp` (one live clone `$S/lane`, two probe work dirs,
one poller file) was removed at the end of the seat; `TMPDIR` pointed there for every command, and
no scratch file was left elsewhere. The three pre-existing `/tmp/tameshi-r14-*` and twenty
`/tmp/tameshi-r4-2-regression.*` directories are **not mine** and were left untouched (they are
evidence for §5, and the lane rule forbids me deleting another seat's tree).

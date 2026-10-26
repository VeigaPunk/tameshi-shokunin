# T47ExecObsD — C1 dependence observation, 5 statements (round 47, wave 1)

Seat: leaf executor, C1 dependence observation. Lane `tameshi-shokunin`, rev `9acfbe21435e1976636a276448dee1d5e7155915`,
base `0b5b7cd2b2c15d23086e811a0f0348d84261277b`. Read-only on the lane: this file is the only lane byte I wrote.
Statements observed (my item, and no sibling report covers them — checked `w1/T47ExecObs{A,B,C,IdGuard}.md`):

- `required-command-receipt-binding` — `python3 tools/command-binding.py --selftest`
- `refusing-registry-replay` — `python3 tools/registry-replay.py --selftest`
- `mutation report interop` — `python3 tools/mte-interop.py --selftest`
- `tally-audit-v2 runner audit` — `python3 tools/tally-audit-v2.py --selftest`
- `tally-audit-v3 runner audit` — `python3 tools/tally-audit-v3.py --selftest`

These are seat probes (`--only … --emit`), not verdicts. Both end in the seat line `C1_R47_PARTIAL: … total=5`
(the 5 UNPARSED rows at the freeze are expected: the standing rows carry no `deps` clause yet).

## 1. Commands exactly as run

```
mkdir -p /tmp/tameshi-r47-T47ExecObsD/w1 /tmp/tameshi-r47-T47ExecObsD/w2
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-47/calibration/measure.py \
  --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev 9acfbe21435e1976636a276448dee1d5e7155915 \
  --base 0b5b7cd2b2c15d23086e811a0f0348d84261277b \
  --work /tmp/tameshi-r47-T47ExecObsD/w1 \
  --only "required-command-receipt-binding,refusing-registry-replay,mutation report interop,tally-audit-v2 runner audit,tally-audit-v3 runner audit" --emit
# identical, second run into /tmp/tameshi-r47-T47ExecObsD/w2 ; both backgrounded in one shell, one wait.
```

Host note (see §7): `/tmp` is a 128 GiB nvme partition that was at 99–100 % (262 MiB free) when I started; the first
attempt of both runs died `C1_R47: clone/checkout failed` because the counter's own `git clone` hit ENOSPC at profile P2.
I removed my own partial work dirs and made the prescribed scratch path a symlink, `/tmp/tameshi-r47-T47ExecObsD ->
/var/tmp/tameshi-r47-T47ExecObsD` (root fs, plenty free). Both recorded runs then completed normally into that path.
No lane byte, no counter, no statements list was changed; no tool was installed (nothing to upgrade: `bwrap`, `jj`,
`jq`, `node`, `/usr/bin/python3` + `jsonschema 4.25.1` were already present).

Wall: 808 s for both runs together. `W1_EXIT=1`, `W2_EXIT=1` (the seat-probe exit; not a verdict).

## 2. PROFILES lines, run 1 (w1) and run 2 (w2) — byte-identical

```
w1: PROFILES required-command-receipt-binding: P0=COMMAND_BINDING_SELFTEST: 44/44 pass|0 P1=COMMAND_BINDING_SELFTEST: 44/44 pass|0 P2=COMMAND_BINDING_SELFTEST: 44/44 pass|0 P3=COMMAND_BINDING_SELFTEST: 44/44 pass|0 P4=COMMAND_BINDING_SELFTEST: 44/44 pass|0 P5=COMMAND_BINDING_SELFTEST: 44/44 pass|0
w1: PROFILES refusing-registry-replay: P0=REGISTRY_REPLAY_SELFTEST: 10/10 pass|0 P1=REGISTRY_REPLAY_SELFTEST: 10/10 pass|0 P2=REGISTRY_REPLAY_SELFTEST: 10/10 pass|0 P3=REGISTRY_REPLAY_SELFTEST: 10/10 pass|0 P4=REGISTRY_REPLAY_SELFTEST: 10/10 pass|0 P5=REGISTRY_REPLAY_SELFTEST: 10/10 pass|0
w1: PROFILES mutation report interop: P0=MTE_SELFTEST: 17/17 pass|0 P1=MTE_SELFTEST: 17/17 pass|0 P2=MTE_SELFTEST: 17/17 pass|0 P3=MTE_SELFTEST: 17/17 pass|0 P4=UNOBSERVABLE|exit=2 P5=MTE_SELFTEST: 17/17 pass|0
w1: PROFILES tally-audit-v2 runner audit: P0=TALLY_AUDIT_V2_SELFTEST: 22/22 pass|0 P1=TALLY_AUDIT_V2_SELFTEST: 22/22 pass|0 P2=TALLY_AUDIT_V2_SELFTEST: 22/22 pass|0 P3=TALLY_AUDIT_V2_SELFTEST: 22/22 pass|0 P4=TALLY_AUDIT_V2_SELFTEST: 22/22 pass|0 P5=TALLY_AUDIT_V2_SELFTEST: 22/22 pass|0
w1: PROFILES tally-audit-v3 runner audit: P0=TALLY_AUDIT_V3_SELFTEST: 35/35 pass|0 P1=TALLY_AUDIT_V3_SELFTEST: 35/35 pass|0 P2=TALLY_AUDIT_V3_SELFTEST: 35/35 pass|0 P3=TALLY_AUDIT_V3_SELFTEST: 35/35 pass|0 P4=TALLY_AUDIT_V3_SELFTEST: 35/35 pass|0 P5=TALLY_AUDIT_V3_SELFTEST: 35/35 pass|0
w2: PROFILES required-command-receipt-binding: P0=COMMAND_BINDING_SELFTEST: 44/44 pass|0 P1=COMMAND_BINDING_SELFTEST: 44/44 pass|0 P2=COMMAND_BINDING_SELFTEST: 44/44 pass|0 P3=COMMAND_BINDING_SELFTEST: 44/44 pass|0 P4=COMMAND_BINDING_SELFTEST: 44/44 pass|0 P5=COMMAND_BINDING_SELFTEST: 44/44 pass|0
w2: PROFILES refusing-registry-replay: P0=REGISTRY_REPLAY_SELFTEST: 10/10 pass|0 P1=REGISTRY_REPLAY_SELFTEST: 10/10 pass|0 P2=REGISTRY_REPLAY_SELFTEST: 10/10 pass|0 P3=REGISTRY_REPLAY_SELFTEST: 10/10 pass|0 P4=REGISTRY_REPLAY_SELFTEST: 10/10 pass|0 P5=REGISTRY_REPLAY_SELFTEST: 10/10 pass|0
w2: PROFILES mutation report interop: P0=MTE_SELFTEST: 17/17 pass|0 P1=MTE_SELFTEST: 17/17 pass|0 P2=MTE_SELFTEST: 17/17 pass|0 P3=MTE_SELFTEST: 17/17 pass|0 P4=UNOBSERVABLE|exit=2 P5=MTE_SELFTEST: 17/17 pass|0
w2: PROFILES tally-audit-v2 runner audit: P0=TALLY_AUDIT_V2_SELFTEST: 22/22 pass|0 P1=TALLY_AUDIT_V2_SELFTEST: 22/22 pass|0 P2=TALLY_AUDIT_V2_SELFTEST: 22/22 pass|0 P3=TALLY_AUDIT_V2_SELFTEST: 22/22 pass|0 P4=TALLY_AUDIT_V2_SELFTEST: 22/22 pass|0 P5=TALLY_AUDIT_V2_SELFTEST: 22/22 pass|0
w2: PROFILES tally-audit-v3 runner audit: P0=TALLY_AUDIT_V3_SELFTEST: 35/35 pass|0 P1=TALLY_AUDIT_V3_SELFTEST: 35/35 pass|0 P2=TALLY_AUDIT_V3_SELFTEST: 35/35 pass|0 P3=TALLY_AUDIT_V3_SELFTEST: 35/35 pass|0 P4=TALLY_AUDIT_V3_SELFTEST: 35/35 pass|0 P5=TALLY_AUDIT_V3_SELFTEST: 35/35 pass|0
```

(`diff` of the two logs after removing the `W1_EXIT=`/`W2_EXIT=` trailer reports no difference; the raw sha256s differ
only through that trailer.)

STATEMENT lines (both runs identical):

```
STATEMENT cap/required-command-receipt-binding: observed=COMMAND_BINDING_SELFTEST: 44/44 pass|0|9230c68e53a5 (exit=0) UNPARSED observed_deps=none DEPS-OK
STATEMENT cap/refusing-registry-replay:       observed=REGISTRY_REPLAY_SELFTEST: 10/10 pass|0|9fcd2dbba737 (exit=0) UNPARSED observed_deps=none DEPS-OK
STATEMENT cap/mutation report interop:        observed=MTE_SELFTEST: 17/17 pass|0|193ea6e32f89 (exit=0) UNPARSED observed_deps=node DEPS-OK
STATEMENT cap/tally-audit-v2 runner audit:    observed=TALLY_AUDIT_V2_SELFTEST: 22/22 pass|0|7b11ba25aead (exit=0) UNPARSED observed_deps=none DEPS-OK
STATEMENT cap/tally-audit-v3 runner audit:    observed=TALLY_AUDIT_V3_SELFTEST: 35/35 pass|0|da8c1ef4b30c (exit=0) UNPARSED observed_deps=none DEPS-OK
```

Run-1 and run-2 agreement: **all 30 profile tuples agree; no tuple is unstable in any profile.** The only asymmetry in
the whole matrix is `mutation report interop` under P4 (node removed), and it reproduces identically in both runs.

`P0` also observed the tool sha prefixes `9230c68e53a5 / 9fcd2dbba737 / 193ea6e32f89 / 7b11ba25aead / da8c1ef4b30c`,
which equal the sha already in the last standing rows (SCORECARD.md:2186–2190).

## 3. Per statement: dependence set, root cause, legitimacy

### `required-command-receipt-binding` — observed deps `none`

Six-tuple matrix (line, exit) identical in P0…P5: `COMMAND_BINDING_SELFTEST: 44/44 pass`, 0.
The `obs-*.stdout` files are byte-identical P0 vs P1 (1213 bytes each) and P5 as well.

Root cause of the negative (why nothing can move it): the selftest is pure-stdlib Python that never shells out to a
named host tool. It reads only committed clone-relative fixtures
(`tools/command-binding.py:164` `Path(__file__).resolve().parents[1] / '.ufo/evidence'`, `:166` the round-23/round-24
`extra-cases.json`) and re-enters itself via `sys.executable` (`:184`). `python3` is present in every PATH shim (the
variants drop only `bwrap`/`jj`/`node`), no tool file mentions `jj`, `bwrap`, `node`, `HOME`, `LANG` or the live fleet
root. Verdict: **legitimate `deps none`** — the statement genuinely has no declared-axis prerequisite.

### `refusing-registry-replay` — observed deps `none`

Identical six-tuple matrix: `REGISTRY_REPLAY_SELFTEST: 10/10 pass`, 0. obs files byte-identical P0/P1 (240 bytes).

The only fleet-shaped function, `plan()` (`tools/registry-replay.py:64-69`, `os.path.dirname(real)` + glob of
`*-shokunin` under it), is exercised by the selftest only against a tree the selftest creates inside its own
`tempfile.TemporaryDirectory`: `:227-230` makes `fleet/lane-shokunin`, `fleet/peer-shokunin` and an `alias` symlink,
`:231-240` plans through `tmp/alias/peer-shokunin/../lane-shokunin` and compares to `os.path.realpath(fleet)` of that
scratch tree. It never globs the live `/home/vgpnk/Projects/shokunin`, so the P5 decoy root cannot reach it.
Verdict: **legitimate `deps none`**.

### `mutation report interop` — observed deps `node`

P0 = P1 = P2 = P3 = P5 = `MTE_SELFTEST: 17/17 pass`, 0. **P4 (node removed from the shim) = `UNOBSERVABLE`, exit 2.**
obs `P4/obs-mutation-report-interop.stdout` is one line: `MTE_SELFTEST: SETUP (node not found)`.

Root cause, exact path: `tools/mte-interop.py:195-198` — `official_metrics()` starts with
`node = shutil.which('node')` and `raise Setup('node not found')`. The selftest calls it unconditionally before it can
print a count: `:427` `official = official_metrics({c[0]: c[1] for c in cases})`, caught at `:428-430`
(`except Setup … print('MTE_SELFTEST: SETUP (%s)' …); return 2`). Because the picked pattern is
`^(MTE_SELFTEST: \d+/\d+ pass)`, the refusal yields no picked line → `UNOBSERVABLE|exit=2`, which differs from P1 →
the counter declares `node`.

Independent confirmation (outside the counter), with a shim byte-identical to P1's minus `node`:
`MTE_SELFTEST: SETUP (node not found)`, exit 2; the same shim with `node` restored: `MTE_SELFTEST: 17/17 pass`, exit 0.

Verdict: **legitimate prerequisite — declare `node`.** The selftest exists to score reports with the official npm
`mutation-testing-metrics` 3.9.0 library executed by node (`:201-220`, `NODE_RUNNER` at `:80-84`), so node is not
incidental. Two extra prerequisites are real but have no slot in the dep vocabulary (see §5).

### `tally-audit-v2 runner audit` — observed deps `none`

Identical six-tuple matrix: `TALLY_AUDIT_V2_SELFTEST: 22/22 pass`, 0 (869-byte obs, identical in all six profiles).

The selftest reads the runner text beside itself (`tools/tally-audit-v2.py:601-604`, `HERE/mutate-and-run.sh`), writes
its mutated copies under `tempfile.mkdtemp` (`:656`) and runs `sys.executable … --runner` (`:666`). Every bash child
gets an explicit env (`:257` and `:520`: `PATH` (inherited), `LC_ALL=C`, `HOME=tmp`, `TMPDIR=tmp`), so the P0-vs-P1
locale/`HOME`/`TMPDIR` differences cannot reach the audited shell, and only `bash`, `awk`, `mktemp` are needed — all
present in every shim. The two literal config roots (`:265` `'tally-audit'`, `'/tmp/tally-audit-work'`) are string
slots compared inside the tally block; they are never created, so no `/tmp` write happens. Verdict: **`deps none`**.

Independent confirmation that TMPDIR is irrelevant to it: the same selftest under `env -i` with `TMPDIR` moved to a
fresh dir → `TALLY_AUDIT_V2_SELFTEST: 22/22 pass`, exit 0.

### `tally-audit-v3 runner audit` — observed deps `none` (but see the unmodelled `/tmp` prerequisite)

Identical six-tuple matrix: `TALLY_AUDIT_V3_SELFTEST: 35/35 pass`, 0 (1453-byte obs, identical in all six profiles).

Same shape as v2 (runner text at `:805-808`, scratch at `:887`, bash child env at `:392`/`:724`, cases at `:841-885`,
inner `sys.executable … --runner` at `:912`),
**plus one host prerequisite the six profiles cannot vary**: `auto_root()` at `tools/tally-audit-v3.py:407-433`
allocates the runner's *real* auto root as a hard-coded `/tmp` path — `:422`
`cand = '/tmp/tameshi-r4-2-regression.' + <6 alnum>` then `:425 os.makedirs(cand)`; failure (no free space, `/tmp`
unwritable) falls through to `:430 raise CannotAudit('cannot allocate a real auto root')`, and `main()` (`:935-939`)
turns that into `TALLY_AUDIT: SETUP (…)` exit 2. Two selftest cases are structurally keyed on that exact path
(`:872-873`, gated on `"$root" == /tmp/tameshi-r4-2-regression.*` / `….??????`).

Causal proof (scratch copy of the tool only, never the lane file):
- control: byte-identical copy of the REV tool in a scratch `tools/` beside `mutate-and-run.sh`, P1-like `env -i` →
  `TALLY_AUDIT_V3_SELFTEST: 35/35 pass`, exit 0;
- one-line patch `:422` `/tmp/…` → `/proc/self/…` (parent unusable), everything else identical →
  `TALLY_AUDIT_V3_SELFTEST: 4/35 pass`, exit 1, **31 of 35 cases `FAIL (exit 2)`** (including `pristine`).
So 31/35 of this statement is contingent on a writable `/tmp`, and none of P0…P5 tests that.
Independent confirmation that TMPDIR alone is irrelevant (the tool deliberately ignores it): same selftest with
`TMPDIR` moved → 35/35, exit 0.

Verdict: the deps clause the counter can observe here is **`none`** (that is what makes the row pass), and `/tmp` is
*not* an accident — the audit must reproduce the runner's real auto root (`mutate-and-run.sh:1357-1365`), so it is a
legitimate prerequisite. It is simply not expressible in `{bwrap, env, fleet-root, jj, node}`; flagged in §5/§7.

## 4. Flags requested by the item

- **P1 differing from P0 only through a path or timestamp in the picked line:** none. For all five statements the
  picked line is a pure pass count (`…_SELFTEST: n/m pass`); no path, no timestamp can enter it. Stronger: the full
  obs files are byte-identical P0 vs P1 for all five (1213 / 240 / 3295 / 869 / 1453 bytes), so nothing else moved.
- **Timeouts:** none. `grep -c timeout w1.log w2.log` = 0/0 and every profile produced a tuple; no
  `('UNOBSERVABLE','timeout')` note appears.
- **Command crashing before reaching the tool:** none. Every `obs-*.stdout` in P0…P5 contains the tool's own `CASE …`
  lines; P5 obs files contain no `bwrap:` diagnostic, and my decoy check confirms the bind is in force (inside
  `bwrap --bind / / --dev-bind /dev /dev --bind DECOY /home/vgpnk/Projects/shokunin` the fleet root shows only
  `scripts/`, and `scripts/sources-census.sh` prints `decoy fleet root: census stub` and exits 7 — so the P5 negative
  for these five statements means "does not read the fleet root", not "the mount silently failed").
- **Variant effectiveness (so the negatives are real negatives):** shim inventory per profile —
  P1: `bwrap jj node jq python3 bash mktemp awk` all present; P2: `bwrap=0` (jj/node/jq present); P3: `jj=0`;
  P4: `node=0` (bwrap/jj/jq present). The drops land exactly where the counter claims.

## 5. Dependence sets to declare (for the L1's rows)

| statement | observed deps | deps clause the counter accepts | unmodelled prerequisites |
|---|---|---|---|
| required-command-receipt-binding | none | `none` | — |
| refusing-registry-replay | none | `none` | — |
| mutation report interop | node | `node` | python `jsonschema` (imported at `tools/mte-interop.py:352-355`; the selftest prints `MTE_SELFTEST: SETUP (…)` exit 2 if absent — present on this host at `/usr/bin/python3`, 4.25.1, in every profile) |
| tally-audit-v2 runner audit | none | `none` | — |
| tally-audit-v3 runner audit | none | `none` | writable **`/tmp`** for `auto_root()` (`tools/tally-audit-v3.py:422-425`), 31/35 cases collapse without it |

The two unmodelled items are not defects I can fix inside my bounds (no tool edit, no counter edit); they are named so
the deps clause is not read as a stronger claim than it is. Both are host shapes that P0…P5 hold constant, so the
observed sets stay exact under the frozen measurement.

## 6. Reproduce / artifacts

- `w1.log`, `w2.log` (both runs' full output) and every `obs-*.stdout` under
  `/tmp/tameshi-r47-T47ExecObsD/{w1,w2}/{P0..P5}/` (the path is a symlink to `/var/tmp/tameshi-r47-T47ExecObsD/`).
- Root-cause micro-probes and their logs: `/tmp/tameshi-r47-T47ExecObsD/tmpprobe/`
  (`v3-tmpdir-moved.log` 35/35, `v2-tmpdir-moved.log` 22/22, `v3-ctrl.log` 35/35, `v3-patched.log` 4/35,
  plus the direct node-on/node-off mte runs quoted in §3).
- `diff` of the two run logs after stripping the `W*_EXIT` trailer: no difference.

## 7. Risks / blockers (for the L1's deciding run)

1. **`/tmp` capacity is a deciding-run hazard, not just mine.** At 21:36 the host `/tmp` (128 GiB, separate nvme
   partition, shared with every live seat) was 100 % full with 262 MiB free; my first pair of probes died
   `C1_R47: clone/checkout failed` when the counter's clone hit ENOSPC at P2. One C1 run clones 12 repos
   (`setup_profile` × 6 profiles × mirror+clone) and measured 2.3 GiB of work dir, so the deciding run needs a few GiB
   free on `/tmp`, and
   `tally-audit-v3`'s selftest additionally needs `/tmp` writable at run time or it reports
   `TALLY_AUDIT_V3_SELFTEST: 4/35 pass` exit 1 — a *false* C1 mismatch that is indistinguishable from a real one.
   My runs only completed after I moved my own scratch behind the prescribed path onto the root filesystem.
   Recommendation: check `df -h /tmp` and keep the deciding run's `--work` under that path with ≥ 4 GiB free.
2. A `/tmp`-full deciding run would be scored as an honest miss by the frozen predicate; nothing in the counter
   distinguishes "host ran out of disk" from "statement regressed". That is a calibration gap the claim itself is
   about, and worth a line in the round report.

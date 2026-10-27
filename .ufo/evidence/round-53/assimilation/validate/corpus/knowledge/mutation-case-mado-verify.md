# Mutation case — mado `tools/mado-verify.sh` round-5 config-plane gate (T6-1)

Run date 2026-10-14, sweep 17:42:16Z. Lane: **T6-1**, tameshi round 6 — the *service round*
(the method ships as the service offered in the fleet census, `fleet-suite-census.md` §5).
Engagement: **mado-shokunin opted in** via its own plan (`mado-shokunin/plans/round-6.plan.md`
§(a): "Mutation proof — via tameshi's harness, consumed read-only (never edited; a needed
change is a recommendation to tameshi, not a patch)"). Substrate: mado-shokunin **read-only**;
every mutant is a byte copy under `/tmp/w6-tameshi-mado-verify/`; **this note is the only fleet
file written by this run** (the corpus/README row and the `LOG.md` entry fold in at lane
review, as in round 5). No external site contacted; no secret file read; **no live substrate
read** — every live-plane probe binary used in §2 was a local stub, never the session.

Anchors: **O** = observation (command output, file:line, re-quoted measured cell); **I** =
inference; **U** = unknown. `mado-verify.sh:NNN` = `mado-shokunin/tools/mado-verify.sh` @
`d7edaab4…d0e13`. Host: bash 5.3.15, python 3.14.7 (tomllib present), Linux 7.2.3-arch1-3.

**Incident I1 — the harness itself moved mid-round, by a concurrent lane.** Both the sweep and
the regression run were executed against `tameshi-shokunin/tools/mutate-and-run.sh` sha256
`597e141989065e038a1c2b35359ab3d20b565d3c959c2eec64166ecb1ff6331b` (pinned in both logs:
`MUTATE_TOOL`, `REGRESSION_TOOL`; same pin the round-6 draft records at
`plans/round-6-record-draft.md:50`). Re-pin at 17:46:15Z: sha256 `b56c6e57…2bcb`, 46850 B,
mtime 14:46:08 -0300. **Every number in this note is tied to `597e1419…`**; whether the new
revision reproduces this table is **U** (§7). Recorded, not smoothed; nothing was repaired.

Also, the gate's selftest scratch is a shared namespace: `/tmp/w5-mado-m52-selftest.*` held
≥37 directories at 17:4xZ that this run did not create (mtime range 14:41:01–14:45:48 -0300,
newest while this note was being written) — another writer is exercising this gate
concurrently. This run kept exactly 8 such directories and removed exactly those paths (§9);
no other writer's scratch was touched. No measurement here reads that namespace.

## 0. Gate choice, method, headline

**Why this gate.** Assignment T6-1 names it; mado's round-6 plan §(a) pre-registers exactly
this engagement (harness read-only, defect spec = one mutant per declared contract clause,
≥8 defects, suite = the gate's own selftest exercising `$MUTANT`, evidence = per-defect
verdicts + kill-rate headline + control green + `MUTATE_RESTORE: OK`). The artifact is a
1099-line bash config-plane verdict gate (round 5 / M5-2) whose own header states the contract
measured here: verdict token `CLEAN|DIVERGED` (`:9-10`), exit map 0/1/2 (`:12-13`), "a plane
that cannot be verified reads UNKNOWN and blocks CLEAN — never a fake CLEAN" (`:25-26`), the
declared-plane census (17 include statements `:463-480`; 12 local confs `:522`), the
`hyprland.conf` sha pin (`:574`), the byte-identity boundary proof (`:735-742`), and reader
fallbacks (jsonc/TOML parse, python-availability arms).

**Hermeticity of the suite (O).** `--selftest` builds fixtures under
`mktemp -d /tmp/w5-mado-m52-selftest.XXXXXX` (`:340`), runs four scenarios against `$0` — i.e.
against `$MUTANT` under the harness — clean (A), broken (B), live-requested-with-no-hyprctl
(C), usage (D), and asserts 28 checks; scenario A also asserts fixture byte-identity
(`:380`). Scenario C starves PATH (`:400-406`) so `hyprctl` is absent: no substrate file and
no compositor is touched by any scenario. Scratch is removed on green (`:422`).

**Method (round-2/3/5 replica).** `tools/mutate-and-run.sh --target mado-shokunin/tools/
mado-verify.sh --defects <spec> --suite 'bash "$MUTANT" --selftest'`. One exact edit per
defect against a fresh copy of the pinned pristine; `count(@old)==1` for all ten asserted
before any suite run (pre-checked by this lane and again by the harness's preparation step);
control run first — a red control would have been a SETUP refusal with no headline.

- O: control — `CONTROL: GREEN (exit=0 duration-ms=475 …)`, `MADO_SELFTEST: 28/28 assertions
  passed`; `MUTATE_RESTORE: OK (target-sha256 before=d7edaab4…d0e13 after=d7edaab4…d0e13
  pristine-sha256=d7edaab4…d0e13)`; the fleet file was re-hashed after the probes too: unchanged.
- O: **kill rate 4/10 (40 %)**, survivors D3, D5, D7, D8, D9, R1, **0 inconclusive** — all 11
  runs produced a definitive verdict (`MUTATE: DONE … killed=4 survived=6 inconclusive=0
  kill-rate=40%`). Cost: 11 runs in 5.26 s wall (control 475 ms; mutants 464–501 ms) against a
  300 s per-run timeout, never approached.
- O: each mutant differs from the pristine in **exactly one line** (per-mutant `diff`, §9) —
  no compounding, no collateral edit.
- Composition, stated before the run: **4 defects were cut at sites whose assertions this lane
  could name in the suite's own scenarios** ("in-surface": D1, D2, D4, D6) and **6 at seams it
  predicted unasserted** ("out-of-surface": D3, D5, D7, D8, D9, R1). Measured: **4/4 killed
  and 0/6 killed**. The split is by construction, so the honest reading is neither "weak" nor
  "strong": here the suite's assertion set and its kill set are **co-extensive** — nothing
  outside the asserted surface was caught, and nothing inside it escaped. The 40 % rate is
  composition, not a regression of the suite (band-amendment precedent, §4).
- O: **pre-registration held 10/10 on verdicts and 4/4 on the named kill mechanisms** (§5 E1).

## 1. Kill-rate table

| # | clause (mado plan §(a)) | injected defect (site on `d7edaab4`) | suite exit | verdict | failing assertions |
|---|---|---|---|---|---|
| — | control | unmutated pristine copy | 0 | GREEN `28/28` | — |
| D1 | A verdict token | file-plane CLEAN printf token renamed `MADO_VERIFY: CLEAN (`→`MADO_VERIFY: OK (` (`:1088`) | 2 | **KILLED** | 1 — `A: CLEAN verdict (missing: MADO_VERIFY: CLEAN)` |
| D2 | B UNKNOWN-never-CLEAN | verdict test drops the UNKNOWN guard (`:1086`) | 2 | **KILLED** | 3 — `C: exit 1 (got '0' want '1')`; `C: DIVERGED verdict`; `C: no fake CLEAN (unexpected: MADO_VERIFY: CLEAN)` |
| D3 | B status vocabulary | skipped-live-layer row `SKIP`→`PASS` (`:588`) | 0 | SURVIVED | 0 |
| D4 | C exit map | DIVERGED path `exit 1`→`exit 0` (`:1098-1099`) | 2 | **KILLED** | 2 — `B: exit 1 (got '0' want '1')`; `C: exit 1 (got '0' want '1')` |
| D5 | C exit map | failing `--selftest` returns 1 not 2 (`:429`) | 0 | SURVIVED | 0 |
| D6 | D declared-plane census | `xdph` dropped from the 12-conf local inventory (`:522`) | 2 | **KILLED** | 1 — `B (want row hypr.local.inventory FAIL)` |
| D7 | D declared-plane census | include-graph count test `-ne`→`-lt` (extra sources tolerated) (`:484`) | 0 | SURVIVED | 0 |
| D8 | E sha comparison | `hyprland.conf` sha-pin comparison always "matches" (`:574`) | 0 | SURVIVED | 0 |
| D9 | E sha comparison | read-only boundary comparison always reads byte-identical (`:738`) | 0 | SURVIVED | 0 |
| R1 | F reader fallback | tomllib-unavailable arm reads `PASS` not `UNKNOWN` (`:651`) | 0 | SURVIVED | 0 |

By clause: A 1/1 · B 1/2 · C 1/2 · D 1/2 · E 0/2 · F 0/1. Kill mechanisms (O, verbatim from
`evidence/D*.out`; the killed suite runs stop at `MADO_SELFTEST: FAILED — 27|26|25 passed`):

- **D1** takes the file-plane CLEAN branch; scenario A's substring assert is the only tripwire.
- **D2** is the anti-claim arm itself: with the guard gone, scenario C's UNKNOWN row rides to
  `MADO_VERIFY: CLEAN` exit 0 — three asserts fire (exit, verdict, no-fake-CLEAN).
- **D4** is seen twice: both scenarios that legitimately DIVERGE (B and C) assert `exit 1`.
- **D6** is seen once, in the broken fixture's named-FAIL assert — the census mutant is caught
  only because scenario B removes a file the mutant no longer declares.

## 2. Survivor analysis and non-equivalence probes

Every survivor is a **real behaviour difference**, not an equivalent edit: each probe below
constructs an input the suite's fixtures do not, and each cell is a measured reading
(`/tmp/w6-tameshi-mado-verify/probe/*.out`, script `probe/probes.sh`). No probe reads the live
session: the mechanisms are PATH-level injections of local stubs.

| probe | survivor | deterministic mechanism | pristine reading | mutant reading | level |
|---|---|---|---|---|---|
| P3 | D3 | clean fixture, `--no-live` | `live.plane SKIP` · `pass=17 skip=1` | `live.plane PASS` · `pass=18 skip=0` | row + counts |
| P5 | D5 | PATH with a **no-op `sed`** (shadows only `sed`), so scenario B's walker edit silently no-ops | selftest `FAILED — 27 passed, 1 failed`, **exit 2** | identical failure line, **exit 1** | exit code |
| P7 | D7 | clean fixture + one undeclared 18th `source =` line | `include_graph FAIL 18 source lines (expected 17)`, DIVERGED exit 1 | `include_graph PASS 18/17 sources, order exact`, **CLEAN exit 0** | **verdict** |
| P8 | D8 | clean fixture | `sha_pin NOTE … 082b6f84756a… drifted from round-1 pin 4f52854a3c14…; re-verify anchors` | `sha_pin NOTE … 082b6f84756a… matches round-1 pin` | detail text |
| P9 | D9 | a **real mid-run change** to `$C/waybar/style.css`, triggered at the run's 2nd `sort` call (`sort` fires exactly twice in a `--no-live` verify run, `:209`; measured `sort-calls=2`) | `boundary.readonly FAIL config plane changed during the run — investigate immediately`, DIVERGED exit 1 | `boundary.readonly PASS config plane byte-identical before/after (combined sha 1a14e9f8b1ff…)`, **CLEAN exit 0** | **verdict** |
| PR1 | R1 | PATH `python3` wrapper that fails any `*tomllib*` argument (PY_OK=1, PY_TOML=0) | `walker.config UNKNOWN python3 tomllib unavailable — cannot parse TOML` · `unknown=2` | `walker.config PASS python3 tomllib unavailable — cannot parse TOML` · `unknown=1` (still DIVERGED via the unmutated alacritty arm) | row |

- **D3 — class: row status on an unread row.** The mutant's own detail text still says "live
  layer skipped", so the fake PASS is invisible to every scenario; a consumer that parses rows
  or the `counts:` line sees an executed-and-passed live layer where none ran. The suite never
  reads the `counts:` line or the skip counter.
- **D5 — class: failure-path exit code unobservable.** The declared exit map reserves 2 for
  "a failing --selftest" (`:13`); under the mutant a failing selftest exits 1, which a caller
  reading the gate's own verdict vocabulary would take as DIVERGED. The run is green when
  nothing else fails, so the suite cannot see it — and the harness cannot either (any nonzero
  suite exit is a kill).
- **D7 — class: count/tolerance boundary never reached.** No fixture carries an 18th source
  line, so `-lt` and `-ne` are indistinguishable in-suite; out of suite the mutant clears an
  undeclared include (`18/17 sources, order exact` — self-contradictory detail included) and the
  verdict flips to CLEAN. This is the tsukuroi-B7 shape (cap never reached) reproduced on the
  include graph.
- **D8 — class: record-level NOTE row, no assert.** The gate's own pin discipline ("a changed
  pin is a FAIL — the claims must be re-verified", `:52-54`) is implemented for the file plane
  as a NOTE that never flips the verdict (`:575/:577`); the mutant makes it claim a match it
  never checked. Row status is identical (NOTE), so nothing in the suite can tell.
- **D9 — class: safety row asserted only in its PASS direction.** The read-only boundary proof
  (SKILL safety rule 3; mado's own claimed discipline) is asserted in scenario A only, where it
  is PASS regardless. P9 shows the FAIL branch — the *entire point of the row* — is
  unprotected: a plane that changes during the run is reported byte-identical, and the run
  reads CLEAN. New shape for the arm-class matrix (no earlier tameshi case produced it).
- **R1 — class: degradation arm unreachable in-suite.** The suite already knows the
  PATH-starvation technique (scenario C) but applies it to `hyprctl` only; no scenario removes
  python3/tomllib, so every PY_OK=0 / PY_TOML=0 arm is unexercised. A PASS row whose detail
  says the reader is missing is exactly the fake-pass the gate's header forbids.

Shared class: five of six survivors change a claim no assertion reads (an unread row status, an
unread NOTE, an unread counts line, an unread exit code, an unread tolerance); the sixth
(D9) is a branch no fixture constructs. Both are the admitted survivor families.

## 3. What the 28 assertions protect — and do not

**3.1 Asserted surface (O: static read of the selftest `:365-419`; clean-run row set
`probe/base.A.out`).** 28 assertions (A 11, B 8, C 6, D 3); **9 distinct row ids asserted** in
at least one scenario: `hypr.root.include_graph` (PASS and FAIL), `walker.config` (PASS and
FAIL), `waybar.config.reload_style` PASS, `waybar.config.parse` FAIL, `term.cross.font_size`
PASS, `hypr.root.orchestrator` FAIL, `hypr.local.inventory` FAIL, `boundary.readonly` PASS,
`live.plane` UNKNOWN — plus `st_rows … FAIL 0` and `UNKNOWN 0`. A clean `--no-live` run emits
**20 rows** (17 PASS · 1 SKIP · 2 NOTE), so the asserted vocabulary is PASS (5 ids), FAIL
(4 ids), UNKNOWN (1 id), zeros. **Never asserted:** NOTE rows (`sha_pin`, `backups`), SKIP
rows, the `counts:` line, any verdict *detail* text, and every row of the live-plane body.

**3.2 The live plane (O/I).** 106 `row …` call sites in the file, **51 under `hypr-live`**;
the hermetic suite executes exactly the two guard rows (`live.plane SKIP` `:588` under
`--no-live`; `live.plane UNKNOWN` `:763` in scenario C, which returns immediately at `:762-765`).
I: every defect inside the live-plane body (version pins, option reads, env probes,
process/service probes) is invisible to this suite by construction; none was mutated here —
the class is demonstrated by D3 (a live-adjacent row) and R1 (an arm the suite cannot reach).

**3.3 Observed but not swept.** `row_from_rc`'s `6) … UNKNOWN` arm (`:105`) is currently dead:
no python check block in the file exits 6 (`grep -c 'exit(6)'` → `0`), so mutating that arm
would be an equivalent edit today. It is recorded as an observation (with its risk: the arm
exists to keep "unverifiable → UNKNOWN" true for future live reads), not counted in the ten.

## 4. Cross-case comparison (TAMESHI-R4-1 matrix)

Headline sequence: **80 % (JS r2) · 80 % (kagi bash r3) · 60 % (tsukuroi bash r5) · 40 %
(mado bash r6)**. The fourth point is the first below the 50–80 band, and its cause is
composition: this sweep's composition was 4 in-surface + 6 out-of-surface, measured 4/4 and
0/6. The tsukuroi amendment ("a sweep's rate is only comparable across sweeps of similar
composition") is what this point tests — from the other side. Mapped to matrix rows: D1/D2/D4
= Row A (verdict paths), all killed, third author; D6/D7 = declared-census rows, with *count
tolerance* as the sub-row that no earlier case carried; D8 = unasserted record field (kagi/tsukuroi
family); D5 = out-of-band exit map (tsukuroi-B8 family); R1 = unreached arm (kagi/tsukuroi
family); **D9 = safety row asserted only in its PASS direction, new to the matrix**.

## 5. Calibration and errata (append-only)

- **E1 — pre-registration.** Predicted and measured tables are identical (4/10 killed; same
  six survivors), and the four predicted kill mechanisms are the measured ones (§1). Scratch
  pre-registration: `probe/../predictions.txt`, written 17:42Z before the sweep.
- **E2 — first P-D5 sandbox was over-stunted.** The first attempt used a sandbox PATH with a
  tiny symlink set; the suite's scenario-C sub-invocation then died with exit 127 *inside* that
  sandbox, producing 6 failures in **both** binaries — a probe artifact, not a mutant effect.
  Re-run with the precise sandbox (only `sed` shadowed) → 1 failure in both, pristine exit 2 vs
  mutant exit 1. The refined run is the record; the first attempt is kept here as errata.
- **E3 — spec correction before the run.** D4's first anchor (`exit 1`) occurs 4× in the target
  (`:382` comment, `:390`, `:407` assertions, `:1099` code) and was replaced by
  `"$reason"\nexit 1` before any suite run. The pre-run count check (mirroring the harness's own
  `count==1` assert) caught it; the harness would also have refused at preparation.
- **E4 — harness drift (I1).** All numbers are tied to tool `597e1419…`; re-verification under
  the current `b56c6e57…` is **U**.
- **E5 — suite size.** The gate's own count line (`28/28`) is the assertion count this note
  uses; it is measured on every run of the control and every survivor (O), and it is *not*
  asserted by the suite itself (§3.1, the counts-line blind spot).

## 6. REGRESSION status (the harness's own gate) and the round-6 plan's claim

- O: `REGRESSION: PASS (cases=2 passed=2; band killed-delta<=1 flips<=1)` at 17:44:28Z, tool
  `597e1419…`: `js-kimi-census` 8/10 killed, flips=0; `bash-surface-census` 8/10 killed, flips=0
  (18.9 s wall; logs `regression/`).
- O: that line covers **only the two embedded cases** (`PIN_JS`/`PIN_BASH` — `:477-480` on the
  run revision, `:482-485` on the current one; the 4-case embed did not happen in either).
  **This case's table is not embedded**, so the §1
  kill-rate claim does **not** carry a `REGRESSION` line over itself. Contrary to the round-6
  plan's `--regression` sentence (which anticipated embedding the round-6 engagement case at its
  pinned revision), embedding needs an edit to `tools/mutate-and-run.sh`; per this assignment
  (write only this note) and PROVINCE (sibling gates stay sibling-owned), it is recorded as a
  **follow-up for the lane that owns the tool**: target pin `d7edaab4…d0e13`, suite line
  `bash "$MUTANT" --selftest`, recorded table §1, spec §9.
- O/I: the plan's claim sentence expected the round-6 first engagement to be kumitate
  `scripts/cite-check.mjs` (census queue head). The assignment executed mado's opt-in instead,
  so the census-ordering question stays open **in this lane**; it is not contradicted by
  anything measured here.

## 7. Unknowns

- **U1** — the live plane: 51 row sites, 0 executed by the suite. Their defect sensitivity is
  unmeasured; D3/R1 demonstrate only the class.
- **U2** — suite sensitivity ≠ gate truth: nothing here measures whether the gate's verdicts
  against the *real* config planes are right; only what its suite can detect.
- **U3** — tool drift (I1): reproduction under the current harness revision `b56c6e57…` is
  unmeasured; the concurrent writer's change is read-only observed (size/pins), not analysed.
- **U4** — concurrent writer(s) on the gate's shared scratch: ≥37 foreign
  `/tmp/w5-mado-m52-selftest.*` dirs (newest 14:45:48 -0300); attribution **U** (mado-side or
  tameshi-side lane). Not removed; my 8 exact paths were (§9).
- **U5** — host/toolchain gating: bash 5.3.15, python 3.14.7, one host, 2026-10-14. The P5/P9
  mechanisms are PATH-level and may behave differently under other shells/toolchains.
- **U6** — whether mado accepts any §8 recommendation is a decision of mado's lane; this note
  records the findings unabsorbed.

## 8. Recommendation to the owner (mado) — recommendations only, no patch

Ranked by yield; each names the swept mutant it would kill (measured evidence, not opinion).

1. **Add a live-plane scenario with a PATH-stub `hyprctl`** (the suite already owns the
   mechanism at `:400-406`; extend it from *starving* the command to *answering* it). Highest
   yield: 51 of 106 row sites are unexercised, so every live-plane defect is invisible today.
2. **Assert the boundary proof in its FAIL direction** — a scenario where a plane file changes
   mid-run. Kills D9 and turns the gate's own safety row into a protected claim. (Probe P9 is
   the mechanism, in the note.)
3. **Assert the `counts:` line and the SKIP row** (both unread today): kills D3 and protects the
   counters consumers may parse.
4. **Add an 18th-source fixture case** — kills D7 and pins the include-graph census as an exact
   count rather than a tolerance.
5. **Assert the NOTE rows** (`sha_pin` match vs drift, `backups` count): kills D8 for the file
   plane and makes the pin discipline checkable.
6. **Exercise the degradation arms** with PATH wrappers (missing `python3`/`tomllib`): kills R1
   and protects "UNKNOWN, never a pass".
7. **Make the suite observe its own failure exit code** (e.g. the no-op-`sed` self-failure
   technique of probe P5, or a wrapped invocation asserting exit 2): kills D5 and protects the
   declared exit map's tool-error channel.

## 9. Reproduce

Scratch root `/tmp/w6-tameshi-mado-verify/` (all evidence lives here; the fleet holds only this
note):

```
sweep.log                full sweep transcript (MUTATE_TOOL/DATE/TARGET/SPEC, CONTROL, 10 × DEFECT)
sweep/                   pristine.mado-verify.sh (byte copy of d7edaab4), mutant-D{1..9,R1}.…
                         evidence/{CONTROL,D1..R1}.out, defects.tsv, results.tsv, spec.copy
spec/mado-verify.defects.spec   the 10 exact edits (pre-run count==1 check passed 10/10)
predictions.txt          pre-registration, written 17:42Z before the sweep
probe/probes.sh          the six probes (§2) + fixture rebuild; probe/*.out are their readings
probe/fixture-A          the suite's own clean fixture, rebuilt here (byte-identical to the
                         sweep-side build — `diff -r` clean)
regression/              the harness's own two embedded cases (PASS, 17:44:28Z)
```

Commands (order matters only for the fixture):

```
cd /home/vgpnk/Projects/shokunin
sha256sum mado-shokunin/tools/mado-verify.sh            # d7edaab4…d0e13 (before; re-check after)
bash tameshi-shokunin/tools/mutate-and-run.sh \
  --target mado-shokunin/tools/mado-verify.sh \
  --defects /tmp/w6-tameshi-mado-verify/spec/mado-verify.defects.spec \
  --suite 'bash "$MUTANT" --selftest' \
  --workdir /tmp/w6-tameshi-mado-verify/sweep --label mado-verify.sh --tail 14
bash /tmp/w6-tameshi-mado-verify/probe/probes.sh        # six survivor probes
bash tameshi-shokunin/tools/mutate-and-run.sh --regression \
  --workdir /tmp/w6-tameshi-mado-verify/regression
sha256sum mado-shokunin/tools/mado-verify.sh            # d7edaab4…d0e13 (after; unchanged)
```

The ten edits, each applied once to a fresh copy (site on `d7edaab4`; mutant sha256 listed for
byte-identity; `diff pristine mutant` = exactly 2 changed lines everywhere):

```
D1  :1088   MADO_VERIFY: CLEAN (%s pass, %s notes; file plane only   ->  MADO_VERIFY: OK (…
            ec60ae5c8f82…  D2  :1086   if [ "$FAIL" = 0 ] && [ "$UNKNOWN" = 0 ]; then  ->  if [ "$FAIL" = 0 ]; then
            41ae4e6e26e6…  D3  :588    row hypr-live live.plane SKIP … ->  … PASS …
            1c0e1d3ee758…  D4  :1099   "$reason" + exit 1  ->  exit 0
            7902653acf98…  D5  :429    return 2  ->  return 1
            5f0937367e74…  D6  :522    LOCAL=(… autostart envs xdph)  ->  LOCAL=(… autostart envs)
            4b94c1802ba0…  D7  :484    "${#got[@]}" -ne "${#EXPECT[@]}"  ->  … -lt …
            ce37404f12eb…  D8  :574    if [ "$sha" = "4f52854a3c14" ]; then  ->  if [ -n "$sha" ]; then
            81351c897a8b…  D9  :738    if [ "$after" = "$before" ]; then  ->  if [ -n "$after" ]; then
            81817f67c950…  R1  :651    walker.config UNKNOWN "python3 tomllib unavailable …"  ->  PASS …
            6f3affd3849e…
```

**Spot-checks (three cited refs re-read on the pinned bytes; sha re-verified `d7edaab4` at
17:46:15Z).** (1) `:1086-1092` → the UNKNOWN guard, the two CLEAN printfs (only the file-plane
one carries `file plane only`), `exit 0`. (2) `:429` → `return 2` at the end of the selftest's
failure branch; `:484` → the `-ne` count test with its two branches (`FAIL "${#got[@]} source
lines (expected …)"` / `PASS "${#got[@]}/${#EXPECT[@]} sources, order exact"`). (3) `:574` →
the sha-pin comparison with `4f52854a3c14`; `:738` → the boundary `after = before` comparison
whose FAIL text is `config plane changed during the run — investigate immediately`.

Scratch cleaned after the run: the 8 `/tmp/w5-mado-m52-selftest.*` directories this run kept
(`NZjJyD`, `PF4sqb`, `694AM7`, `vofefz` — the two D5 probes; `EZ65Yh`, `pxI11s`, `YNGvFA`,
`GGFnEQ` — the four killed sweep runs) were removed by exact path at 17:46Z; foreign
directories were left untouched (U4).

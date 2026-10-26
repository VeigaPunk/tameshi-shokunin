# T47ExecObsB — C1 dependence observation (four statements), round 47 wave 1

Seat: executor (leaf). Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Rev observed (freeze): `9acfbe21435e1976636a276448dee1d5e7155915`; base `0b5b7cd2b2c15d23086e811a0f0348d84261277b`.
Counter: `.ufo/evidence/round-47/calibration/measure.py` — run only as `--only` probes into scratch, never as a verdict.
No file in the lane was edited except this report. No tool was installed or upgraded. No counter, statements list or SCORECARD row was touched.

## Result in one line

All four assigned statements are **flat across all six profiles**: every profile prints the same picked line and exit, both passes are byte-identical, so the observed dependence set is **`none`** and `deps none` is the conformant declaration for each of the four. The interesting finding is the *unmodeled* axis: three of the four statements hardcode `/tmp` as their scratch root (ignoring `TMPDIR`) and two need `git` on `PATH` — real host prerequisites the five-name deps vocabulary cannot express.

## 1. Exact commands (both passes, one shell, background + wait)

```sh
mkdir -p /var/tmp/tameshi-r47-T47ExecObsB
cd /var/tmp/tameshi-r47-T47ExecObsB
L=/home/vgpnk/Projects/shokunin/tameshi-shokunin
M=$L/.ufo/evidence/round-47/calibration/measure.py
ONLY="mutation sweep runner,repeated pristine-control gate,six-leg content-disposition probe,exposed witness provenance correction"
( python3 $M --lane $L --rev 9acfbe21435e1976636a276448dee1d5e7155915 \
    --base 0b5b7cd2b2c15d23086e811a0f0348d84261277b \
    --work /var/tmp/tameshi-r47-T47ExecObsB/w1 --only "$ONLY" --emit \
    > /var/tmp/tameshi-r47-T47ExecObsB/w1.log 2>&1; echo "RUN1_EXIT=$?" >> .../w1.log ) &
( python3 $M --lane $L --rev 9acfbe21435e1976636a276448dee1d5e7155915 \
    --base 0b5b7cd2b2c15d23086e811a0f0348d84261277b \
    --work /var/tmp/tameshi-r47-T47ExecObsB/w2 --only "$ONLY" --emit \
    > /var/tmp/tameshi-r47-T47ExecObsB/w2.log 2>&1; echo "RUN2_EXIT=$?" >> .../w2.log ) &
wait
```

Wall time for both passes in parallel: 111.33 s. Both exited 1 with the seat verdict line
`C1_R47_PARTIAL: self_pin=1 stmts_pin=1 statements=4 mismatches=0 unparsed=4 unobservable=0 dep_mismatch=0 unpinned=0 append_only=1 total=4` (expected: `--only` can never pass, and at the freeze no SCORECARD row carries a `deps` clause — `grep -c 'deps \`'` over `SCORECARD.md@9acfbe2` is `0`, so `unparsed=4`).

Scratch location note: the first attempt at `/tmp/tameshi-r47-T47ExecObsB/` died instantly —
`C1_R47: clone/checkout failed` / `mkdir: No space left on device` (`/tmp` = separate 128 G nvme partition at 100 %, 81 M free at 21:36). The work dirs were moved to `/var/tmp/` on L1 instruction (`/` has 572 G free). This is itself evidence that the counter needs ~2.3 GB of scratch per pass (12 clones) and dies whole if the work filesystem is full.

## 2. PROFILES lines, verbatim, both passes

`w1.log`:

```
PROFILES mutation sweep runner: P0=MUTATE_SELFTEST: 106/106 pass|0 P1=MUTATE_SELFTEST: 106/106 pass|0 P2=MUTATE_SELFTEST: 106/106 pass|0 P3=MUTATE_SELFTEST: 106/106 pass|0 P4=MUTATE_SELFTEST: 106/106 pass|0 P5=MUTATE_SELFTEST: 106/106 pass|0
PROFILES repeated pristine-control gate: P0=SELFTEST: PASS (29 cases)|0 P1=SELFTEST: PASS (29 cases)|0 P2=SELFTEST: PASS (29 cases)|0 P3=SELFTEST: PASS (29 cases)|0 P4=SELFTEST: PASS (29 cases)|0 P5=SELFTEST: PASS (29 cases)|0
PROFILES six-leg content-disposition probe: P0=SELFTEST: PASS (19/19)|0 P1=SELFTEST: PASS (19/19)|0 P2=SELFTEST: PASS (19/19)|0 P3=SELFTEST: PASS (19/19)|0 P4=SELFTEST: PASS (19/19)|0 P5=SELFTEST: PASS (19/19)|0
PROFILES exposed witness provenance correction: P0=SELFTEST: PASS 39/39|0 P1=SELFTEST: PASS 39/39|0 P2=SELFTEST: PASS 39/39|0 P3=SELFTEST: PASS 39/39|0 P4=SELFTEST: PASS 39/39|0 P5=SELFTEST: PASS 39/39|0
```

`w2.log`: identical line for line (same strings, same order). Full logs: `/var/tmp/tameshi-r47-T47ExecObsB/w1.log`, `w2.log`.

Also emitted by both passes (the row text the writer needs; `| deltas` = none needed):

```
EMIT_CAP | mutation sweep runner | … | `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 106/106 pass`, exit 0, tool sha256 `a7d3f2dd7d47`, deps `none` | historical round 3; re-demonstrated round 31 |
EMIT_CAP | repeated pristine-control gate | … | `python3 tools/repeat-control.py --selftest` → `SELFTEST: PASS (29 cases)`, exit 0, tool sha256 `296fe566dc59`, deps `none` | round 12 |
EMIT_CAP | six-leg content-disposition probe | … | `python3 tools/pin-disposition.py --selftest` → `SELFTEST: PASS (19/19)`, exit 0, tool sha256 `331529eadafe`, deps `none` | round 13 |
EMIT_CAP | exposed witness provenance correction | … | `python3 tools/witness-metadata.py --selftest` → `SELFTEST: PASS 39/39`, exit 0, tool sha256 `df3390682a04`, deps `none` | round 13 |
```

The last standing SCORECARD rows (`SCORECARD.md@9acfbe2` lines 2177, 2179, 2180, 2181) already carry exactly these values, exits and tool sha256 prefixes; the only missing field is the `deps` clause. `sha256sum` of the four tools at lane HEAD reproduces `a7d3f2dd7d47 / 296fe566dc59 / 331529eadafe / df3390682a04`.

## 3. Per statement: six tuples, run-to-run agreement, dependence set

Profile definitions as executed by the counter (`measure.py:57-58`, `:150-186`, `:196-234`): P0 = live host env; P1 = clean env + `PATH` shim of `/usr/bin` plus `node`/`jj`/`jq`, `HOME`/`TMPDIR` per-profile, `LANG=LC_ALL=C`, `TZ=UTC`; P2 = P1 without `bwrap`; P3 = P1 without `jj`; P4 = P1 without `node`; P5 = P1 inside `bwrap --bind / / --dev-bind /dev /dev --bind DECOY /home/vgpnk/Projects/shokunin`.

| statement | P0 | P1 | P2 | P3 | P4 | P5 | run1 vs run2 | observed deps |
|---|---|---|---|---|---|---|---|---|
| mutation sweep runner | `MUTATE_SELFTEST: 106/106 pass` / 0 | same | same | same | same | same | identical | **none** |
| repeated pristine-control gate | `SELFTEST: PASS (29 cases)` / 0 | same | same | same | same | same | identical | **none** |
| six-leg content-disposition probe | `SELFTEST: PASS (19/19)` / 0 | same | same | same | same | same | identical | **none** |
| exposed witness provenance correction | `SELFTEST: PASS 39/39` / 0 | same | same | same | same | same | identical | **none** |

Agreement is stronger than the counter's own comparison: the whole `obs-*.stdout` file (stdout + stderr, last 200 kB) is **byte-identical across all six profiles and both passes** for each statement —
`mutation-sweep-runner` sha256 prefix `aa3e6b475557` (5446 B), `repeated-pristine-control-gate` `09f432706cf0` (2936 B), `six-leg-content-disposition-probe` `1f39911c34eb` (1409 B), `exposed-witness-provenance-correction` `c4f371609f34` (6002 B); 48 files, 4 distinct digests. No unstable tuple, no nondeterministic statement, no profile with a divergent unpicked line.

Profile differentiation was verified as real, not vacuous (so `none` is a measurement, not a no-op):

* shim entry counts `P1=3755, P2=3754, P3=3754, P4=3754, P5=3755` with exactly `bwrap` missing in P2, `jj` missing in P3, `node` missing in P4 (`ls w1/P*/shim`).
* P5 semantics re-probed independently: inside the bound namespace `/home/vgpnk/Projects/shokunin` lists only `scripts`, the stub prints `decoy fleet root: census stub` and exits 7; outside it the real fleet root is visible and `jq --version` = `jq-1.8.2`. The bind is effective.
* P0 has no `shim/`, `home/`, `tmp/` (`ls w1/P0` → `clone fleet obs-*.stdout` only), i.e. P0 really was the live host environment.
* all 48 observation files begin with tool-level output (`PASS sweep exits 0`, `SELFTEST_CASE …`), none with a shell/loader error.

## 4. Root cause, axis by axis (why no dependence can arise)

`bwrap` (P2): none of the four tools invokes `bwrap`; the only bwrap use is the counter's own P5 wrapper (`measure.py:207-209`). Grep over the four tools finds no `bwrap`.

`jj` (P3): no tool shells out to `jj`. `pin-disposition.py:325-380` *documents* that it mirrors `scripts/hyaku/jj-lane.sh detect_branch` but re-implements it read-only in-process; no `jj` process is spawned. `repeat-control.py` has no `jj`/`git`/`node`/`jq` token at all (`grep -nw`). Nothing changes when the `jj` symlink disappears.

`node` (P4): none of the four selftests runs node. The `node` suites belong to `--regression` (`mutate-and-run.sh:1386-1428`, `node "$MUTANT" --selftest`), which `--selftest` never reaches. All four tool selftests are bash-fragment or python fixture work.

`fleet-root` (P5): the four selftests are self-contained. `mutate-and-run.sh:1738-1870` points its ledger fixtures at `FLEET_ROOT="$root/fleet"` (`:1740-1743`), i.e. its own `mktemp` tree, never `/home/vgpnk/Projects/shokunin`. `repeat-control.py:114-121` resolves its fixture root from `SELF` (the clone), `pin-disposition.py:706-770` builds its fixture fleet under its scratch dir, `witness-metadata.py:70` sets `LANE_ROOT = Path(__file__).resolve().parent.parent` (the clone) and reads only `.ufo/evidence/round-12/BashWitness/*` (`:72-88`, `:127-131`). Replacing the fleet root with the decoy therefore cannot change a byte of output — confirmed by the identical P5 digests.

`env` (P0 vs P1): P0 carries my host `PATH` (fnm node, `~/.local/bin` jj), real `HOME`, host `LANG`/`TZ`, and no `TMPDIR`; P1 carries the shim, an empty `HOME`, `LC_ALL=C`, `TZ=UTC` and a per-profile `TMPDIR`. All four tools are indifferent to `HOME` (each either ignores it or pins it — `pin-disposition.py:759-760` sets `HOME=scratch`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_AUTHOR_*` so the host gitconfig cannot leak), to locale (`LC_ALL` pinned at `pin-disposition.py:765`; the other three emit plain ASCII) and to `PATH` order (they call `bash`, `cat`, `git`, `python3` by name and the shim holds all of them at the same real paths `/usr/bin/*`). Hence P0 = P1.

**Verdict on the declared set:** for these four statements `deps none` is not a shortcut, it is what the six profiles measure. There is no dependence here the statement could "shed" within the frozen vocabulary.

## 5. Root causes of the dependencies the six profiles *cannot* see (found independently)

Because `deps none` can be read as "hermetic", I ablated two host axes outside the counter, in scratch, against the P1 clone and shim (read-only on the lane). Both are real host prerequisites that the vocabulary `('bwrap','env','fleet-root','jj','node')` (`measure.py:53`) has no name for.

**(a) `git` on PATH — hard prerequisite of 2 of 4.** With `git`, `jj`, `node` removed from the shim and everything else unchanged:
`mutation sweep runner` → exit 1, `VERDICT: FAIL (scratch kept: …)`, tally `MUTATE_SELFTEST: 0/1 pass`; `six-leg content-disposition probe` → exit 2, `SELFTEST: COULD_NOT_EVALUATE ([Errno 2] No such file or directory: 'git' …)`; `repeated pristine-control gate` → exit 0 `SELFTEST: PASS (29 cases)`; `exposed witness provenance correction` → exit 0 `SELFTEST: PASS 39/39`.
Root cause: `tools/mutate-and-run.sh:171` (declared deps "bash, python3 …, git"), `:288-299` `fixture_commit()` runs `git init/add/commit/rev-parse`, `:1176`/`:1354` guard `command -v git`; `tools/pin-disposition.py:228` and `:772` invoke `["git", …]` with `HOME`/`GIT_CONFIG_*` pinned. `repeat-control.py` and `witness-metadata.py` genuinely have no git edge.
Verdict: **legitimate prerequisite**, satisfied identically in P0–P5 (git sits in `/usr/bin`, so the shim keeps it) — declaring `none` is correct under the frozen rule but should not be read as "no external binary needed".

**(b) `/tmp` writability and free space — hidden prerequisite of 3 of 4, and invisible to every profile.** Traced with `strace -f -e trace=mkdir`, `TMPDIR=/var/tmp/…/probe-tmp`:
`mutate-and-run.sh --selftest` → 67 `mkdir` under `/tmp`, **0** under `TMPDIR` (scratch `/tmp/tameshi-r4-2-selftest.XXXXXX`, `tools/mutate-and-run.sh:1477`; also `:482`, `:1360` for the run/regression modes);
`repeat-control.py --selftest` → 44 under `/tmp`, 0 under `TMPDIR` (`tools/repeat-control.py:597`, `mkdtemp(..., dir="/tmp")`);
`pin-disposition.py --selftest` → 57 under `/tmp`, 0 under `TMPDIR` (`tools/pin-disposition.py:706`, same hardcoded `dir="/tmp"`);
`witness-metadata.py --selftest` → **468 under `TMPDIR`, 0 under `/tmp`** (`tools/witness-metadata.py:1122`, bare `mkdtemp`), i.e. this one is the only TMPDIR-clean tool.
Consequence, demonstrated by binding a read-only empty dir over `/tmp` in a private mount namespace (`unshare -rm`, host untouched): `mutation sweep runner` → `MUTATE_SELFTEST: 0/1 pass` exit 1; `repeated pristine-control gate` → `REPEAT_CONTROL: setup_error` (`OSError: [Errno 30] Read-only file system: '/tmp/tameshi-r12-repeat-control-selftest.…'`) exit 2; `six-leg content-disposition probe` → `OSError: [Errno 30] … '/tmp/tameshi-r13-pin-disposition-selftest.…'` exit 1; `exposed witness provenance correction` → `SELFTEST: PASS 39/39` exit 0.
Verdict: **accident the three statements could shed** — the fix is one line each (drop `dir="/tmp"` in `repeat-control.py:597` and `pin-disposition.py:706`; use `${TMPDIR:-/tmp}` at `mutate-and-run.sh:1477/482/1360`), which would make the scratch root profile-private exactly as `witness-metadata.py:1122` already is. I did **not** make that edit: it is outside this seat's deliverable and would move the observed tuple under any future profile that varies `TMPDIR`.

**(c) Why this matters for the deciding run.** `/tmp` on this host is a separate 128 G partition that was at 100 % at 21:36 today (my first probe attempt died on it). If the L1's deciding run happens while `/tmp` is full, three of my four rows mis-measure through no fault of the statement: `mutation sweep runner` changes both line and exit (`… 0/1 pass` / 1 → `MISMATCH`), while `repeated pristine-control gate` and `six-leg content-disposition probe` crash before the tally line (`UNOBSERVABLE`). Recommended precondition for the deciding run: `df /tmp` shows several GB free; and read the P0/P1 digests, not just the exit, before trusting a sudden dependence.

**(d) The `env` label is not causal.** `env` is defined as "P0 differs from P1", which merges `PATH` shape, `HOME`, locale, `TZ`, `TMPDIR` and unset variables into one name. For these four it is empty, but note the failure mode it hides: `exposed witness provenance correction` under a full `/tmp` at P0 (its `TMPDIR` is unset on the host, so it falls back to `/tmp`) but a clean per-profile `TMPDIR` at P1 would report the dependence as `env` — a disk-state accident wearing an environment label.

## 6. Requested flags

* P1 tuple differing from P0 only by a path or timestamp in the picked line: **none**. All four picked lines are tallies (`MUTATE_SELFTEST: 106/106 pass`, `SELFTEST: PASS (29 cases)`, `SELFTEST: PASS (19/19)`, `SELFTEST: PASS 39/39`); the sha field comes from `git show` of the clone, not from the printed line.
* Any statement timing out in a profile: **none** (48/48 exit 0; `mutation-and-run`'s inner `--timeout 2` hang fixture is exercised and passes in every profile).
* Any profile crashing before reaching the tool: **none** (all 48 observation files start with tool output; no shell/loader error, no `command not found`).
* Additional: the four measured values are *case counts*. Any future addition of a selftest case changes the value the row must state (`106/106`, `29 cases`, `19/19`, `39/39`), independent of deps. The `deps` clause is stable; the tally is not.

## 7. Evidence retained

Under `/var/tmp/tameshi-r47-T47ExecObsB/` (archives kept after cleanup; clone trees deleted):

* `w1.log`, `w2.log` — full counter output of both passes (`STATEMENT`, `PROFILES`, `EMIT_CAP`, verdict line).
* `w1/P{0..5}/obs-*.stdout`, `w2/P{0..5}/obs-*.stdout` — 48 raw observations (stdout+stderr) behind every tuple above.
* `trace-{mut,rep,pin,wit}.log` — `strace -f -e trace=mkdir` proving the `/tmp` vs `TMPDIR` scratch roots (67/0, 44/0, 57/0, 0/468).
* `direct-{mut,rep,pin,wit}.out` — the four selftests re-run by hand under the P1 shim (third, counter-independent pass: same tallies).
* `nogit-{mut,rep,pin,wit}.out` — the `git`/`jj`/`node`-ablated PATH receipts.
* `rotmp-{mut,rep,pin,wit}.out` — the read-only-`/tmp` receipts (`unshare -rm` private mount namespace).
* `w1/P*/shim` counts, `w1/P0` layout, decoy listing/stub exit — profile-differentiation receipts quoted in §3/§4.

Cleanup: `/var/tmp/tameshi-r47-T47ExecObsB/w{1,2}/P*/{clone,fleet,home,tmp,shim}` (≈2.3 GB per pass) deleted after the run; `/tmp/tameshi-r47-T47ExecObsB/` removed entirely; the small receipts above are retained because the report cites them. `/home/vgpnk/Projects/shokunin` and the read-only package tree were not written.

## 8. Blockers / risks

* None for the observation itself.
* Risk for the writer: if the `deps` clause is written as anything other than `none` for these four rows, the counter will report `DEPS-MISMATCH` (it observed `none` twice, independently).
* Risk for the deciding run: `/tmp` headroom (see §5c), and the fact that the counter's own setup needs ~2.3 GB per pass in `--work` (it refuses a non-empty work dir and dies whole on `clone/checkout failed`).

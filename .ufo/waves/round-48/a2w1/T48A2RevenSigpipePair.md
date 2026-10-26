# T48A2RevenSigpipePair — does a pipefail-free run kill the SIGPIPE attribution?

Seat T48A2RevenSigpipePair (round 48, a2w1, attack on the calibration feed of C1). Read-only on the
lane: the only file written is this one. Scratch root
`/fast/scratch/hyaku/tameshi-r48/T48A2RevenSigpipePair` (deleted before exit; §9). Lane checkout
`17cc5ce141868454d05bf75ef5cd230e35f0cdf4`; the object under attack is a rewritten report, not the
lane tree. No tool was installed or upgraded, so the tooling ledger for this seat is empty.

**Object attacked:** `.ufo/waves/round-48/w1/T48RevenRegression.md` (attempt 1), claims 1, 2 and 3 of
its §1 and the mechanism block of its §3: that the `six-leg regression ledger` flake is a SIGPIPE race
under `pipefail` in the pinned tsukuroi leg's `printf | grep -q` sites, located at
`tsukuroi-census.sh:638`, and that it is one-sided.
**Rule applied:** `corpus/QUALITY.md` criterion 96 (`.ufo`-visible at `corpus/QUALITY.md:1420-1428`) —
a differing observation is attributed to a cause only by a run that varies that cause alone, same
revision, same counter, same profile, exactly one named variable changed.

## 1. Verdict

1. **The attribution's substance survives the controlled pair.** With the pinned blob byte-identical
   except the single token `pipefail` on its operative `set` line, the pristine arm failed **5 times in
   330 runs** and the pipefail-free arm **0 times in 330**. The item's kill rule — a pipefail-free arm
   that still fails — did not fire.
2. **The cited file:line is wrong.** `tsukuroi-census.sh:638` is the third line of the `.dispatch`
   fixture-stub heredoc (`:635` opens, `:685` closes), a separate process that contains **no pipelines
   at all**. The shell that runs `check()`'s pipelines is governed by the file's top-level
   `set -euo pipefail` at **`:139`**. Removing `pipefail` from `:638` and leaving `:139` intact still
   failed **2 times in 30 runs** with the same two messages (arm C) — the cited line is inert.
3. **The prescribed pair as specified is underpowered and returned a null.** 30 as-is + 30
   pipefail-free at 6-way concurrency gave **0 and 0** failures. On its own that pair cannot distinguish
   "attribution right" from "attribution wrong"; it must not be read as confirmation. My decisive pair is
   the scaled one.
4. **The mechanism is now observed in the selftest itself, not only in a construct probe.** One failure
   from an instrumented pristine arm carries `[ps=141 0]` — writer 141 (SIGPIPE), `grep` 0 (it matched) —
   and the sibling `plane evidence missing` failures print a `got:` line that *contains* the very
   pattern they report missing (§4). Both are false negatives; no semantic defect is involved.
5. **The rate is not reproduced.** w1 reported 4 failures in 40 runs (10 %). I observed 8 in 780
   pristine-class runs (1.03 %); the as-is arm was 0/30 in the prescribed window. The *class* verdict is
   unaffected; the *rate* is window-specific and should not be quoted as 10 %.

## 2. Material and arm construction

The leg's bytes are materialized by the runner read-only from the fleet object store
(`tools/mutate-and-run.sh:1204` `git show <rev>:<path>` into `$cwd/target.tsukuroi-census.sh`, `:1213-1226`
mode restored from `ls-tree`, `:1230` the pin line). I reproduced exactly that:

```bash
S=/fast/scratch/hyaku/tameshi-r48/T48A2RevenSigpipePair
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin \
  show 165307fe4746a8807b02ec4a7d7ecac0368454a6:tools/tsukuroi-census.sh > "$S/armA/target.tsukuroi-census.sh"
sha256sum "$S/armA/target.tsukuroi-census.sh"
# 084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5  ← PIN_TSUKUROI, byte-identical
git -C …/tsukuroi-shokunin ls-tree 165307fe -- tools/tsukuroi-census.sh
# 100755 blob dfcf6f596fab2437c69fde6c0067606761af4106 → mode 0755, as the runner restores
```

Each arm is `arm<X>/target.tsukuroi-census.sh` — same basename, same depth, so `$SELF`/`$0` handling is
identical across arms; only the bytes named below differ.

| arm | only difference from the pin | sha256 |
|---|---|---|
| A | none (the pin verbatim) | `084951be50bc…c78c5` |
| B | `:139` `set -euo pipefail` → `set -eu` | `29a80ad1e920…96b20` |
| C | `:638` `set -uo pipefail` → `set -u` (w1's cited line) | `63b484492263…43ab4` |
| D | `:139` and `:638` both | `21e33fb00cab…ba1f` |
| Ai | A + `${PIPESTATUS[*]}` appended to the two failure messages | `47a3f4b30dfc…c1bf9` |

A first build used `set -euo pipefail` → `set -euo` and `set -uo pipefail` → `set -uo` and was
discarded: **`set -uo` is not "the same option set minus pipefail"** — a bare `-o` prints the option
table, so the arms printed 27 `allexport off …` lines into their own stdout (observed: the stub then
answered every fixture query with the option dump; 18 of 26 cases failed deterministically). The
rebuilt arms use `set -eu` / `set -u`, and a dump check over all four arms returns 0 lines. Any future
arm that "removes pipefail" from a `set -…o pipefail` line must make the same substitution.

Note on arm B's validity: `set -eu` preserves `-e` and `-u` exactly; `pipefail` is the only option that
differs. `-e`/`-u` therefore cannot be the moving variable, and `set -o | grep pipefail` in arm B's
shell reads `off` while every other arm reads `on`.

**Concurrency and window.** Every wave is 6 background `bash target.tsukuroi-census.sh --selftest` runs
(`wait`, then the next wave), arms interleaved A,B,C,D or A,B,Ai so that no arm owns a quiet stretch.
Four stages, one host window `13:32:33Z → 13:51:36Z`, load average 50.61 → 89.11 (32 cores):

| stage | arms (waves) | runs | window (UTC) |
|---|---|---|---|
| pair1 | A,B,C,D × 5 waves each | 120 | 13:32:33–13:34:10 |
| pair2 | A,B × 30 waves each | 360 | 13:34:41–13:41:41 |
| pair3 | A,B,Ai × 20 waves each | 360 | 13:42:21–13:47:45 |
| ai | Ai × 50 waves | 300 | 13:48:03–13:51:36 |

Per-run cost 4.5–6.4 s; no run hit the suite's own timeout (the runner's `timeout "$TIMEOUT_S"` sits at
`tools/mutate-and-run.sh:456` with `TIMEOUT_S=300`,`:186`), so every rc is a verdict, not a timeout.

## 3. Failure counts per arm

| arm | runs | rc≠0 | rate | message sites |
|---|---|---|---|---|
| A (as-is) | 330 | **5** | 1.5 % | `:771` ×3, `:777` ×2 |
| B (`pipefail` gone, operative line) | 330 | **0** | 0/330 | — |
| C (`pipefail` gone, cited line `:638`) | 30 | **2** | 6.7 % | `:771` ×2 |
| D (both gone) | 30 | **0** | 0/30 | — |
| Ai (A + status instrumentation) | 420 | **1** | 0.24 % | `:777` ×1 |

Pristine-class total (A, C, Ai): **8 failures in 780 runs (1.03 %)**. Pipefail-absent-at-`:139` total
(B, D): **0 in 360**. Exact Fisher, one-sided / two-sided — A vs B `5/330` vs `0/330`: **0.031 / 0.062**;
all-pristine vs all-absent `8/780` vs `0/360`: **0.048 / 0.062**. The zero arm's 95 % upper bound is
0.83 % per run (rule of three). I report the p-values rather than a verdict word: the pair removes the
only *observed* route to the failure and does not exclude a second, rarer route below ~0.8 %/run.

The two zero arms are not a "green because broken" artifact: every run in both arms prints
`TSUKUROI_CENSUS_SELFTEST: PASS (26 cases, 26 passed, 0 failed)` (330/330 in B), the same 26 cases the
failing runs execute with 25 passed + 1 failed (pass lines counted per failing run: 25).

## 4. Failing case messages (verbatim, one line each)

```
C.7-6   FAIL blocked: both kernel rings unusable: hostname override not honoured — possible host read
C.15-4  FAIL healthy: rc=1 backup-only sample is not a defect: hostname override not honoured — possible host read
A.3-1   FAIL degraded: failed services history from journal: hostname override not honoured — possible host read
A.17-3  FAIL degraded: timer last run failed: hostname override not honoured — possible host read
A.46-4  FAIL healthy: unrestricted dmesg ring preferred: hostname override not honoured — possible host read
A.9-1   FAIL degraded: foreign packages: plane evidence missing: '^PLANE packages: DEGRADED .*foreign=3'; got: …
A.11-1  FAIL degraded: foreign packages: plane evidence missing: '^PLANE packages: DEGRADED .*foreign=3'; got: …
Ai.13-1 FAIL healthy: all planes pass: plane evidence missing: '^PLANE packages: HEALTHY .*drift=0'[ps=141 0]; got: …
```

Each failing run's tally line is `TSUKUROI_CENSUS_SELFTEST: FAIL (26 cases, 25 passed, 1 failed)` and its
rc is 1. The messages are the two w1 named, and the five `hostname override` instances span five
*different* case labels — the race is not confined to one case. Precedent messages in the lane are the
same two (`round-18/w2/CR44.md:52-53`, `round-47/w1/T47ExecObsE.md:151-152`), which now has an organic
round-48 instance at each site.

**The `got:` text is the false-negative proof.** A.9-1's full line contains
`PLANE packages: DEGRADED (pacman -Qkk rc=0 sample=4(alpha,beta,gamma,delta) drift=0 backup_diffs=0
nonroot_artifacts=0; foreign=3; pins=none; holds=pacman glibc; db.lck=absent)`. The asserted regex is
`^PLANE packages: DEGRADED .*foreign=3`; that line both starts with `PLANE packages: DEGRADED ` and
contains `foreign=3`. The `got:` string is regenerated from the same `$out` variable the failing
`grep -qE` had just read, so at message time the pattern *was* present and was reported missing. No
semantic defect, no fixture defect (`fx_no_mutation` passed in these runs), no exit-code mismatch.

## 5. Mechanism, measured

**(a) Option state.** Only the file's own `set` lines can enable `pipefail` in the leg: the runner runs
`timeout "$TIMEOUT_S" bash -c "$SUITE"` (`:456`) with `SUITE='bash "$MUTANT" --selftest'` (`:1398`), and
`SHELLOPTS` is not inherited:

```
$ bash -c 'set -o pipefail; bash -c "echo child SHELLOPTS=\$SHELLOPTS; set -o | grep pipefail"'
child SHELLOPTS=braceexpand:hashall:interactive-comments
pipefail        off
```

Inside the leg, `run_selftest()` (`:628`) runs in the process that executed `set -euo pipefail` (`:139`);
`check()`'s `set +e` (`:749`) clears `errexit` only, so `pipefail` is still on for the three piped
assertions at `:771`, `:773`, `:777` (and for the body site at `:286` in each census child).

**(b) The promotion, deterministically.** `PIPESTATUS` also survives the `!` condition, so the status
pair can be read in the branch:

```
$ bash -c 'set -o pipefail; yes | head -1 >/dev/null; echo "pipe=$? ps=${PIPESTATUS[*]}"'
pipe=141 ps=141 0
$ bash -c 'set -eu;        yes | head -1 >/dev/null; echo "pipe=$? ps=${PIPESTATUS[*]}"'
pipe=0   ps=141 0
```

With `pipefail` the pipeline status *is* the 141 of the killed writer, so `elif ! … | grep -q …` enters
the failure branch although `grep` exited 0; without `pipefail` the same race leaves the status at 0 and
the branch is unreachable. This is the whole causal step, and it is exactly what arm B removes.

**(c) Observed in the leg.** Ai.13-1 (pristine bytes + `${PIPESTATUS[*]}` appended to the two messages)
prints `plane evidence missing: '^PLANE packages: HEALTHY .*drift=0'[ps=141 0]`, and its `got:` line
contains `drift=0`. Writer 141, matcher 0, pattern present → the failure branch fires on a match. My 8
organic failures are therefore all one-sided (green case → red), which corroborates w1's §1.2; I did not
observe a false *pass* (a red case reported green) in 780 pristine-class runs.

## 6. Findings

**F1 — wrong file:line in the attacked report (defect, not a mechanism error).**
`T48RevenRegression.md` §1.1 and §3.1 place the selftest's `set -uo pipefail` at
`tsukuroi-census.sh:638`. At the pin it cites (`084951be50bc…` @ `165307fe`) that line is the third line
of the `.dispatch` heredoc: `:635 cat > "$bin/.dispatch" <<'STUB'`, `:636` shebang, `:638 set -uo
pipefail`, `:685 STUB`, while `run_selftest()` opens at `:628`. The operative line is `:139`.
Command: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 165307fe:tools/tsukuroi-census.sh | sed -n '628,630p;635,640p;685p;139p'`.

**F2 — the cited line is inert (measured).** Arm C removes `pipefail` from `:638` alone and failed 2/30
(`C.7-6`, `C.15-4`, §4). The stub has no pipelines at all — `awk 'NR>=636 && NR<=684 && /\|/'` matches
only the `||` in the `TSUKUROI_FIXTURE unset` guard — so its `pipefail` cannot move any pipeline status;
it is also a separate process (`#!/usr/bin/env bash`, reached through `ln -s .dispatch "$bin/$c"`), so its
options cannot reach `check()`. A cause named at `:638` therefore cannot be the cause of the observed
failures; the report's own mechanism narrative (its §3.1 sites `:771/773/777`) is right while its
`:638` pointer is not.

**F3 — the controlled pair the rule asks for, which w1 never ran.** w1 varied nothing between its two
replays (same command, same tool, same host, two runs) and named the cause from mechanism reasoning plus
a 12 000-repetition construct probe. My pair holds revision, pin, profile, concurrency and window fixed
and moves only `pipefail` on the operative line: 5/330 vs 0/330 (one-sided p=0.031), and the mechanism is
independently pinned by §5(a)-(c). The attribution is therefore *now* a criterion-96 observation; it was
not one at the time it was written, and the record must not present the two replays as the pair.

**F4 — the item's prescribed budget is a null.** 30 as-is + 30 pipefail-free at 6-way gave 0 and 0. The
rate the record quotes (10 %) would have made 30 runs of the as-is arm fail ~96 % of the time; I saw
0 %. Any round that re-runs this item at 30+30 will usually learn nothing: at this rate the pair needs a
few hundred runs per arm (4/180 vs 0/180 sat at one-sided p=0.061; 5/330 vs 0/330 is the first
configuration I ran that reached p<0.05).

**F5 — the quoted rate does not reproduce (1.03 %, not 10 %).** `T48RevenRegression.md` §1.4 states
"4 of 40 (10 %)" for the pinned blob's own selftest at 4–6-way concurrency. Measured on this host,
6-way, load 50.6–89.1: 8 failures in 780 pristine-class runs (1.03 %; exact 95 % interval ≈ 0.45–2.0 %).
The w1 figure is ~10× my point estimate and outside my interval. This does not touch the cause; it does mean the
"10 % per suite run" figure must not be reused in the C1 row or in the class prose. The failures also
did not track load: they land at wave loads 51.7, 53.7, 58.2, 59.7, 61.0, 63.8, 67.7 and 72.9, while
each stage's peak (89.1 in pair2, 76.6 in pair3, 68.9 in the ai stage) produced none.

**F6 — the ledger-level observation still has no carried receipt.** The value class rests on
`REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)`, whose `runB.out`, `wd2/bash-tsukuroi-census/…`
and `evidence/B7.out` exist only as paths inside the report (scratch, deleted); the round-47 instance is
likewise a transcription (`round-47/w1/T47ExecObsE.md:151-154` cites `w2/P3/…/evidence/B10.out`, absent
from the tree; `.ufo/waves/round-47/w2/` holds only `swarm-registry.json`). I re-verified the mechanical
link instead of the observation: `case $RC in 0)SURVIVED 124/126/127)INCONCLUSIVE *)KILLED`
(`tools/mutate-and-run.sh:546-550`), ledger legs pass `ftol=ktol=0` (`:1312-1313` comparisons, `:1332-1343`
`regression_case_git` passing `0 0`), out-of-band reasons and FAIL (`:1310-1313`, `:1328`), tally (`:1442`). The
consequence — one spurious selftest case turns a recorded SURVIVED into KILLED, `flips=1`, leg FAIL — is
mechanical, but the ledger FAIL itself remains **[I]**, not [O], until a run prints it into a carried
receipt.

## 7. What this does and does not settle

- [O] The pin and mode of the leg (`084951be50bc…`, 0755); the four piped `grep -q` sites at `:286`,
  `:771`, `:773`, `:777`; `pipefail` at `:139` governing `check()`; `SHELLOPTS` non-inheritance; the
  arithmetic of `pipefail` promoting 141 vs leaving 0; per-arm failure counts and every failing message;
  `ps=141 0` on an organic failure; the false-negative `got:` text; the `.dispatch` heredoc spanning
  `:635-685` with no pipelines.
- [I] That arm B's zero transfers to the ledger (`--regression`): I did not run the ledger — the item's
  surface is the leg's own selftest, and a ledger replay is 233–449 s per run with the runner's exact
  tolerance as the amplifier, not an independent variable.
- [I] That no second, non-`pipefail` mechanism exists below 0.83 %/run in the pristine leg. The pair
  bounds it, it does not exclude it.
- Not claimed: any load attribution. I did not vary load alone, so per criterion 96 I do not name load as
  a cause of anything here: load is an unvaried covariate, and the failures do not follow it (they span
  51.7–72.9 while the window's peaks, up to 89.1, produced none).
- Scope note for C1: this seat's result supports `nondeterministic` for the six-leg statement and says
  the *cause* may now be stated with a controlled pair — but only with the corrected pointer (`:139`,
  `:771/:773/:777`) and without the "10 %" rate.

## 8. Commands that show each finding

```bash
# F1/F2 — line identity of the cited set line and the heredoc extent
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 165307fe:tools/tsukuroi-census.sh \
  | sed -n '139p;628,630p;635,640p;685p'
git -C …/tsukuroi-shokunin show 165307fe:tools/tsukuroi-census.sh | grep -n 'set -uo pipefail\|set -euo pipefail'
#   139:set -euo pipefail   638:set -uo pipefail      (638 is inside 635..685)
awk 'NR>=636 && NR<=684 && /\|/' <pinned blob>          # only the "||" guard: no pipelines in the stub
# F2 — the inert-line arm
sed '638s/^set -uo pipefail$/set -u/' armA/… > armC/…  # then 30 runs at 6-way -> 2 failures

# F3/F4/F5 — the pair drivers (6 concurrent runs per wave, arms interleaved)
bash drive.sh                     # A,B,C,D x 5 waves  (30 runs each)      -> A 0/30  B 0/30  C 2/30  D 0/30
OUT=out/pair2 WAVES_PER_ARM=30 bash drive2.sh   # A,B x 30 waves (180 each)  -> A 4/180 B 0/180
OUT=out/pair3 WAVES_PER_ARM=20 bash drive3.sh   # A,B,Ai x 20 waves (120 each) -> A 1/120 B 0/120 Ai 0/120
OUT=out/ai    WAVES_PER_ARM=50 bash drive4.sh   # Ai x 50 waves (300)          -> Ai 1/300
grep -l 'rc=[^0]' <arm>.*.meta ; cat <run>.err  # per-run rc and the failing case message

# §5(a) option state
bash -c 'set -o pipefail; bash -c "echo child SHELLOPTS=\$SHELLOPTS; set -o | grep pipefail"'
# §5(b) the promotion
bash -c 'set -o pipefail; yes | head -1 >/dev/null; echo "pipe=$? ps=${PIPESTATUS[*]}"'   # pipe=141 ps=141 0
bash -c 'set -eu;        yes | head -1 >/dev/null; echo "pipe=$? ps=${PIPESTATUS[*]}"'   # pipe=0   ps=141 0
# §5(c)/F2 — the instrumentation, one string per branch
sed -n '769,780p' armAi/target.tsukuroi-census.sh
```

## 9. Compliance

- Lane checkout: only this report written (`git -C tameshi-shokunin status --porcelain` shows the wave
  directory as untracked as before this seat's write; no tracked file touched, no `git add/commit`, no
  jj command). `corpus/`, `tools/`, `SCORECARD.md` untouched. The fleet repo was read only with
  `git show`/`ls-tree` (read-only).
- Scratch: everything under `/fast/scratch/hyaku/tameshi-r48/T48A2RevenSigpipePair` (arm copies, outputs,
  drivers), removed before exit; **no tree left on disk**. One unavoidable exception inside the *leg's*
  bytes: `run_selftest()` hard-codes `work=$(mktemp -d /tmp/tsukuroi-r3-2-selftest.XXXXXX)`
  (`tsukuroi-census.sh:630`), so every arm's fixtures were built under `/tmp` and removed by the leg's own
  `trap 'rm -rf -- "${work:-}"' EXIT`; `TMPDIR` cannot reach it and changing it would have added a second
  variable. `/tmp` was at 3 % use whenever checked (start and end); each fixture tree is a few kB.
- Counters: none run; nothing was scored. `scripts/hyaku/disk-guard.sh status` checked at start (23 % on
  `/fast/scratch/hyaku`) and again before scratch removal (24 %); my tree was 9.4 MB and is deleted.
- Tooling: no installs, no upgrades, no pacman.

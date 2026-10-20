# GuardAudit — round 16 w2: attack on the guarded js-round-gate suite

**Verdict (one line): PARTIAL.** The guard holds against the hazards it was admitted for (exported `GIT_DIR`, inherited `GIT_*`/HOME/system git config, `TMPDIR` inside a work tree, an in-repo `WORKDIR`). It is the identical string in the js-round-gate leg. It falls if read as a *sandbox*: a mutant can still write outside `$h` and outside `$WORKDIR`, reach `~/Projects` for writing, use the host network, plant binaries on the inherited `PATH`, and forge a sibling defect's verdict without tripping `MUTATE_RESTORE`. `GIT_CEILING_DIRECTORIES="$h"` is off by one for `cwd=$h`.

Attacked artifact: `.ufo/evidence/round-16/round-gate/suite.txt` @ `c699c8c36d6e4eca4b796b81a8247904aa145ec8` (sha256 `6e550d5a…7f7b`, 217 B, 1 line + LF). Runner: `tools/mutate-and-run.sh` @ same commit (sha256 `89722ddb…5594`, equal to the working tree and to `runner-sha256.txt`). Target: kumitate `scripts/round-gate.mjs` @ `364f1d59` (sha256 `f890e277…d3e9`, 1511 lines, matches `PIN_ROUNDGATE` at mar.sh:562).
Scratch: `/tmp/tameshi-r16w2-GuardAudit-18lkZo` (all runs used committed bytes copied there: `mar.sh`, `suite.txt`, `rg.mjs`, `full.spec` = committed `round-gate.defects.spec`). No tools installed or updated. No lane file edited except this report.

## 1. String identity (confirmed)

- `python3`: took the single-quoted suite argument out of mar.sh:1221 and compared it with `suite.txt` minus its trailing LF → `True` (216 chars each).
- `predictions.json` `.suite` == `suite.txt` → `True`.
- `runner-regression.txt:1`: `REGRESSION_TOOL … sha256=89722ddb…`, the committed runner. `:35-39`: the js-round-gate leg is PASS, `match=10/10 … flips=0`.
- Provenance gap (info): `sweep/sweep.log:1` shows the L1 sweep ran under runner sha `75ed934d…`, not the committed `89722ddb…`. Neither `run_sweep` nor the regression engine records the suite command anywhere: no `MUTATE_SUITE` line, and mar.sh:442-454 prints tool/target/spec only. The claim that `sweep/` was produced by *this* string is therefore inferred from the path shape `…/work/sandbox-CONTROL/tmp/kumitate-round-gate-selftest-…` (`sweep.log:7`). That shape is consistent with the string but does not prove it.

## 2. Canary control with `GIT_DIR` exported (instruction executed)

Both arms used the same one-defect spec (`A1`, from the committed spec) and a fresh bare canary repo. Snapshots were `find -printf '%p %s %T@'` → sha256.

| arm | command | exit | key lines | canary |
|---|---|---|---|---|
| guarded | `GIT_DIR=$S/canary-ctl/canary.git bash mar.sh --target rg.mjs --defects one.spec --suite "$(cat suite.txt)" …` | 0 | `CONTROL: GREEN (exit=0 …)`, `DEFECT A1: KILLED (exit=1)`, `MUTATE_RESTORE: OK` | **UNCHANGED** |
| unguarded counter-arm | same, but `--suite 'node "$MUTANT" --selftest'` | 2 | `CONTROL: RED (exit=1 duration-ms=22)`; control.out: `fixture lane add failed: exit 128 fatal: this operation must be run in a work tree` | **CHANGED** (content+mtime rerun: `canary.git/config` rewritten, mtime 1792504497.70 → 1792504498.86, bytes identical; the fixture `git init` re-initialized the exported repo) |

The guard is load-bearing for `GIT_DIR`. Inside the guard the probe (§3) saw `GIT_DIR: undefined` and env keys exactly `GIT_CEILING_DIRECTORIES,GIT_CONFIG_NOSYSTEM,HOME,LC_ALL,PATH,TMPDIR`.

Additional holds:
- **WORKDIR inside a git work tree:** `--workdir $S/fakeprojects/wd-rg` (inside `git init` repo) → `CONTROL: GREEN`, `MUTATE: DONE`. The repo stayed at `0 objects` and unborn `HEAD` before and after.
- **Relative `--workdir`:** `--workdir rel-wd` → exit 2, `CONTROL: RED (exit=1)`, node `cjs/loader` throw. After `cd "$h"` the relative `$MUTANT` no longer resolves. This fails closed, never a false green. Note that `run_sweep` never absolutizes WORKDIR (mar.sh:426-430).
- **Full 10-defect sweep, current guard:** exit 0, `MUTATE: DONE … killed=5 survived=5`, verdicts byte-equal to `TABLE_ROUNDGATE` (mar.sh:570).

## 3. Escape probe (synthetic mutant through the exact string)

`probe.mjs` (sha256 `ea3ce325…`) ran as `--target` under `--suite "$(cat suite.txt)"`, with `--workdir $S/fakeprojects/wd` inside a scratch git repo and `GIT_DIR` exported. It writes only in scratch and checks real paths with `access()` only. Run exit 0, `CONTROL: GREEN`. Key lines from `evidence/control.out`:

```
PROBE homedir: …/fakeprojects/wd/sandbox-CONTROL/home          (HOME redirect holds)
PROBE tmpdir:  …/fakeprojects/wd/sandbox-CONTROL/tmp           (TMPDIR redirect holds)
PROBE netns: net:[4026531833]                                  (== host shell netns 4026531833)
PROBE write-outside-workdir: WROTE                             ($S/escape/outside-<pid>.txt)
PROBE write-workdir-parent: WROTE
PROBE write-sibling-in-workdir: WROTE
PROBE W_OK ~/Projects: yes
PROBE W_OK ~/Projects/shokunin/tameshi-shokunin: yes
PROBE W_OK ~/.local/bin (on inherited PATH): yes
PROBE PATH-dirs-writable: 9: …/fnm_multishells/…/bin,~/.local/share/fnm,~/.local/bin,~/.grok/bin,~/.kimi-code/bin,~/.local/share/mise/shims,…
PROBE git-config-origins: exit=0 file:.git/config  core.repositoryformatversion=0   (enclosing repo's local config applied)
PROBE git-discovery cwd=$h: exit=0 …/fakeprojects               (ESCAPES the ceiling)
PROBE git-discovery cwd=$h/tmp/x: exit=128 not a git repository (ceiling holds below $h)
PROBE git-discovery cwd=dirname(MUTANT): exit=0 …/fakeprojects
PROBE loopback-connect: CONNECTED :631                         (host service; connect+close only)
```

Direct confirmation of the ceiling semantics with no probe involved (git 2.56.0): `cd repo/wd/sandbox-X; env -i PATH=… GIT_CEILING_DIRECTORIES="$PWD" git rev-parse --show-toplevel` → exit 0, prints the enclosing repo. From `sandbox-X/tmp/x` → exit 128. With `GIT_CEILING_DIRECTORIES=<WORKDIR>` (the parent of `$h`) from `cwd=$h` → exit 128. Git does not treat the cwd as its own ceiling, so the guard bounds discovery only *below* `$h`.

## 4. Exploit demonstrations (scratch-only)

**E-A — cross-mutant verdict forgery is undetected.** Target `tiny.mjs` (sha256 `028f3589…`), suite = exact `suite.txt`. Defect A writes `process.exit(0)` over `$WORKDIR/mutant-B.tiny.mjs`. Defect B is an honest kill (`FAIL = true` → exit 1).
Result: exit 0. `DEFECT A: SURVIVED`, `DEFECT B: SURVIVED (exit=0)`, `MUTATE_RESTORE: OK`, `MUTATE: DONE … killed=0 survived=2`. `results.tsv` records B's mutant sha256 as `d5469616…`, which is the tampered file's sha. The honest mutant's sha would be `3ca72a5e…`. Nothing compares the two. The mutants are built before any run (mar.sh:458-466), the sha is taken *after* each run (mar.sh:499), and the restore proof covers only target and pristine (mar.sh:502-511).

**E-B — PATH plant: code runs before the guard, in the caller's full environment.** Same sweep, with `PATH="$S/pathbin:$PATH"` modelling the 9 user-writable PATH dirs and `GIT_DIR` exported. Defect A plants `$S/pathbin/env`. During defect B's run, `exec env -i …` resolved to the plant: `shim.marker` = `SHIM-RAN pre-guard GIT_DIR=/tmp/…/canary-ctl/canary.git args=-i PATH=… HOME=…/sandbox-B/home …`. A mutant that writes `~/.local/bin/env` or `~/.local/bin/node` (W_OK = yes per §3) would sit ahead of `/usr/bin` for every later defect, for every later leg, and for the host beyond the sweep. **[INFERENCE: real-HOME plant not executed by design.]**

**E-C — `BASH_ENV` runs before the guard (caller environment).** `BASH_ENV=$S/bashenv.sh GIT_DIR=… bash mar.sh … --suite "$(cat suite.txt)"` → `bashenv.marker` has 3 lines (the runner plus 2 suite `bash -c`), each showing `GIT_DIR=/tmp/…/canary.git`. The outer `bash -c` (mar.sh:401) sources `BASH_ENV` before `env -i`. Exported shell functions named `mkdir`/`cd` would be honored the same way **[INFERENCE: not executed]**. `exec env` itself cannot be overridden by a function.

## 5. Residual risks

| # | severity | exploit path | evidence | impact |
|---|---|---|---|---|
| R1 | medium (latent) | mutant/selftest writes by absolute path or relative to `argv[1]` | §3 `WROTE` ×3, `W_OK ~/Projects: yes`. suite.txt:1 has no mount/namespace confinement. mar.sh:904 calls it "the guarded env -i sandbox" | fleet trees and lane writable by any mutant. The guard is env hygiene, not a sandbox |
| R2 | medium (latent) | defect N rewrites `$WORKDIR/mutant-M.*`, evidence/*.out or results.tsv | E-A. mar.sh:458-466, :499, :502-511 | forged KILLED→SURVIVED (or the reverse) with `MUTATE: DONE` + `RESTORE: OK`. The ledger's "exact" replay would carry it |
| R3 | medium (latent) | plant `env`/`node` in a writable inherited-PATH dir | E-B. suite.txt:1 `PATH="$PATH"` + bare `env`/`node` lookup | pre-guard code execution with the caller's env (GIT_DIR, tokens), persisting after the sweep |
| R4 | low/medium (latent) | `git` run with cwd=`$h` (no `-C` into `$h/tmp`) discovers the enclosing repo and applies its `.git/config` | §3 `git-discovery cwd=$h: exit=0`, `git-config-origins: file:.git/config`; direct git test. suite.txt:1 `GIT_CEILING_DIRECTORIES="$h"` | with an in-repo `--workdir`, a mutant's git reads (or writes) the real lane repo. Repo-local config (`core.fsmonitor`, `core.hooksPath`) is a code-exec vector [INFERENCE]. The pristine round-gate only uses `-C` into `$h/tmp` fixtures and absolute non-existent paths (rg.mjs:211-213, :717-720, :1393), so the control is unaffected (§2 in-repo run green, repo untouched) |
| R5 | low | host network namespace | §3 `netns` = host inode, loopback connect OK | mutant can exfiltrate or fetch. The pristine suite uses no network (local bare remotes, rg.mjs:736-739) |
| R6 | low | `discovery from dirname(MUTANT)`: rg.mjs:139, :142, :193 derive DEFAULT_REPO/MAIN_REPO from the script's own location (= `$WORKDIR`), which lies outside `$h` and outside the ceiling | §3 `git-discovery cwd=dirname(MUTANT): exit=0` | a mutant that drops an explicit `--repo`/`--main-repo` in a runGate call would inspect `$WORKDIR/..`, i.e. the real repo if the workdir is in one (read-only git verbs). `homedir()` defaults (rg.mjs:151-152) stay neutralized by `HOME=$h/home` |
| R7 | low | caller env `BASH_ENV` / exported functions | E-C. mar.sh:400-401 | code before the guard. This is a caller-trust issue, not a mutant escape |
| R8 | info | a spec `@defect CONTROL` passes the id charset (mar.sh:319) and shares `sandbox-CONTROL` with the control run | code reading | stale cross-run state |
| R9 | info | `--workdir` reuse: `mkdir -p` (suite.txt:1) keeps any prior `$h/home` (e.g. a planted `.gitconfig`) | code reading | stale-config carry-over between sweeps |
| R10 | info | suite command never logged | §1 | the string's identity in `sweep/` cannot be verified from evidence |

Holds (agreement): GIT_DIR/GIT_* scrub, HOME/system config isolation (`git config --list --show-origin` inside `$h/tmp` subdirs shows nothing), TMPDIR redirect, in-repo WORKDIR control, relative-WORKDIR fail-closed, and the 10/10 table reproduced.

## 6. Smallest remediation (tested)

Wrap the existing string in bubblewrap 0.13.1 (`/usr/bin/bwrap`, already installed) and move the ceiling one level up (`$S/suite-remediated.txt`, sha256 `e1ae3a3d…`):

```
h="$WORKDIR/sandbox-$DEFECT_ID"; mkdir -p "$h/home" "$h/tmp" && cd "$h" && exec /usr/bin/bwrap --ro-bind / / --dev /dev --proc /proc --bind "$h" "$h" --unshare-net --die-with-parent --chdir "$h" /usr/bin/env -i PATH="$PATH" HOME="$h/home" TMPDIR="$h/tmp" LC_ALL=C GIT_CONFIG_NOSYSTEM=1 GIT_CEILING_DIRECTORIES="$WORKDIR" node "$MUTANT" --selftest
```

- Probe under it: `netns: net:[4026533456]` (new), all three writes `blocked(EROFS)`, `W_OK ~/Projects: no(EROFS)`, `PATH-dirs-writable: 0`, `git-discovery cwd=$h: exit=128`, `loopback-connect: blocked(ECONNREFUSED)`. This closes R1, R2, R3 (the plant can no longer be written), R4 and R5.
- Full 10-defect round-gate sweep under it: exit 0, `CONTROL: GREEN (exit=0 duration-ms=3161)`, `killed=5 survived=5`, verdicts identical to `TABLE_ROUNDGATE`. No measurement change.
- Still open after it: R6 is now read-only only. Discovery from `dirname(MUTANT)` still finds an enclosing repo; keeping `--workdir` outside any work tree (the regression default `/tmp/tameshi-r4-2-regression.*`) closes it. R7 needs `env -u BASH_ENV` or `bash --norc --noprofile` with BASH_ENV unset at mar.sh:401. R10 needs a `MUTATE_SUITE:` line (e.g. its sha256) at mar.sh:442-454.
- Applying it requires changing mar.sh:1221, suite.txt, and the leg's recorded provenance together. That is outside this seat's remediation scope; nothing was edited.

## Commands run (all exits as observed)

| command (abridged, cwd `$S`) | exit |
|---|---|
| `git show c699c8c…:{tools/mutate-and-run.sh,.ufo/evidence/round-16/round-gate/suite.txt,…/round-gate.defects.spec,…/predictions.json,…/runner-regression.txt,…/sweep/sweep.log}` | 0 |
| `git -C kumitate-shokunin show 364f1d59…:scripts/round-gate.mjs > rg.mjs` | 0 |
| guarded canary control (§2) | 0 |
| unguarded canary arms ×3 (§2) | 2 |
| probe, current guard, in-repo workdir (§3) | 0 |
| E-A/E-B tamper+plant sweep (§4) | 0 |
| relative-workdir sweep | 2 |
| BASH_ENV sweep (§4) | 0 |
| round-gate one-defect sweep, in-repo workdir | 0 |
| probe, remediated string (§6) | 0 |
| full 10-defect sweep, current guard | 0 |
| full 10-defect sweep, remediated string | 0 |
| `unshare -rn true` / `bwrap --ro-bind / / --dev /dev --proc /proc --unshare-net true` | 0 / 0 |

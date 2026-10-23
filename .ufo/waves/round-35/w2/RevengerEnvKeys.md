# Round-35 w2 — RevengerEnvKeys

Seat: `L1tameshi35.RevengerEnvKeys` (leaf revenger, godspeed). Lane pin at dispatch:
`7da6e076c2e25936a3b60dde2a4080d8f05b7e5b` (verified: `git rev-parse HEAD` in the scratch
clone = the pin). Frozen bytes clone-verified at that rev:

| artifact | sha256 | pin match |
|---|---|---|
| `tools/tally-audit-v3.py` | `ef98fc5367cdb12c71b8b0ddfb5b83835100831f545f6510437dc84014865885` | YES |
| `tools/tally-audit-v2.py` | `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` | YES |
| `tools/mutate-and-run.sh` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | YES |
| `.ufo/evidence/round-35/c1/c1-measure.py` | `515b0b1b00b970f31c08e80eb74512ecae0cf1082ddeccfcb373e810cd0559e8` | YES |
| `.ufo/evidence/round-35/c2/c2-measure.py` | `67bb71188cde259088646f960b6fda8e0a217fad5d8260e379054b381018f9cc` | YES |

Slice assigned: **the env axis** — reverse-engineer which env vars the tally block can read
(HOME, TMPDIR, PWD, PATH, LC_ALL, and the runner's own vars), build a copy whose behavior
depends on one and diverges, and report whether v3's fixed-env oracle sees it.

Scratch: `/fast/scratch/hyaku/tameshi-r35-seats/RevengerEnvKeys/` (lane checkout read-only).
`/fast` was at 100% (2.1G free) so heavy scratch (audit tmpdirs) went to `/tmp/envkeys-audit/`
per the /tmp fallback rule. The scratch clone was created in attempt 1 (at `d16f9b5a`) and was
fast-forwarded to the dispatch pin with `git fetch origin` + `git checkout --detach` (same
setup commands the dispatch specifies; the fetch reads the lane repo, writes only the scratch
clone). No tool installs (nothing needed); no `pacman`.

---

## 1. What I attacked

v3's runtime oracle (amendment A4 closed the root axis) drives the extracted tally block with:

- **driver scope** (`tally-audit-v3.py:376-398`, `run_vectors`): `set -u -o pipefail`,
  `tally() { local st_js=${1} …st_citecheck=${9}; local root=<real auto root|literal> auto=<x> KEEP=<y>; <block> }`
  — the ONLY shell variables in scope are the 9 `st_*` locals, `root`, `auto`, `KEEP`, plus the
  block's own locals.
- **process env** (`tally-audit-v3.py:335-345`, `bash()`): `env = {'PATH': os.environ.get('PATH', …), 'LC_ALL': 'C', 'HOME': tmp, 'TMPDIR': tmp}` — a **complete replacement**:
  `subprocess.run(['bash', path], cwd=tmp, env=env, …)`. The block subprocess sees exactly four
  environment variables. No USER, SHELL, LANG, LOGNAME, TERM, XDG_*, no caller exports, and
  **no runner globals**. The harness check uses the same dict (`v3:647-651`).

The REAL runner context at the tally block (`tools/mutate-and-run.sh`, inside `run_regression`,
block at `:1432-1470`):

- full caller environment (HOME=/home/…, USER, SHELL, LANG, PWD=caller cwd, TMPDIR present or
  absent — on this host TMPDIR is unset), plus
- the runner's own shell variables, all in scope at the block: `FLEET_ROOT` (global `''` at
  `:632`, **assigned the real value at `:1358` — `$(dirname "$(dirname "$(dirname "$SELF")")")`
  — on every `--regression` run, before the legs and the block**), `SELF`, `WORKDIR`,
  `specs`, `DEFECT_ID`, `MUTANT`, `BAND_*`, `PIN_*`, `REV_*`, `TABLE_*`, `TIMEOUT_S`, `TAIL_N`,
  `TARGET/SPEC/SUITE/LABEL`, and the 9 `st_*` statuses.

The oracle's context minus the real context is a large set-difference; any gate keyed on that
difference is invisible to the audit if it is dormant under the oracle's env. The runner is
globally `set -u -o pipefail` (`mutate-and-run.sh:175`), so an evader must use `${VAR:-}`
guards — which is exactly what a real-world copy would do.

## 2. Static result: the PRISTINE block cannot read env (proven)

The pristine block (`mutate-and-run.sh:1432-1470`, closing brace `:1471`) was extracted with
the runner's own boundary rule and every `$`-expansion enumerated:

```
$root×6  $nlegs×4  $npass×3  $nsetup×3  $nfail×2  $auto×1  $KEEP×1  $st×1  $st_js…$st_citecheck×9
```

That is the complete list — **no `$HOME`, `$TMPDIR`, `$PWD`, `$PATH`, `$LC_ALL`, no `${USER…}`,
no runner globals**. The only parenthesized forms are four `$(( … ))` arithmetic expansions on
the counters (block lines 4, 5, 6, 27 of the extraction; verified: zero `$( cmd )` command
substitutions, zero backticks, zero redirects to env-derived paths, no `mktemp`/`cd`/`command`
in the block). Conclusion: **pristine block output is a pure function of
(9 statuses, root, auto, KEEP)** — proven by reading the block, per the seat's conditional.
(`env -i PATH= HOME= TMPDIR=` appearances at `:1418/:1423/:1428` are the JS LEG command
strings — the legs sandbox themselves; they are above the block and are not the block.)

So the exposure is not the pristine block reading env — it is that the **audited surface (a
copy's block) may read env**, and the oracle fixes env so that env-keyed divergence is
invisible. That is the axis A4 did not close: A4 gave the auto triples the real root VALUE;
the env/scope slot of the witness shim is still simulated.

## 3. Specimens

Five copies of the pinned runner, one line each inserted after the tally loop's `done`
(`:1440` in each copy; inside the extracted block, outside the loop, touching no `st_*`
assignment, no operand, no `nlegs`):

| copy | inserted line | sha256 |
|---|---|---|
| K1 runner-var | `if [[ -n "${FLEET_ROOT:-}" ]]; then nfail=0 nsetup=0 npass=$nlegs; fi` | `2de960796e0cbc738f534ced726c111ccf347b9145d97b7b62edb1fce9fde618` |
| K2 TMPDIR-unset | `if [[ -z "${TMPDIR:-}" ]]; then nfail=0 nsetup=0 npass=$nlegs; fi` | `5fef9a7aef627b9244615da5149afb23e6b3ccece5f55f3a368e5b060e99a789` |
| K3 pure env | `if [[ -n "${USER:-}" ]]; then nfail=0 nsetup=0 npass=$nlegs; fi` | `b69983419d59aefa0c9da8715bab227822f464b0d08f6d413e612b0856b8d8ed` |
| K4 env value | `if [[ "$HOME" == /home/* ]]; then nfail=0 nsetup=0 npass=$nlegs; fi` | `9fefcec15f4645c5ae3295465ce9bfab0520c3077b7d120e3baed0d8c0b41638` |
| A1 inert reads | `: "${HOME:-}" "${PWD:-}" "${PATH:-}" "${LC_ALL:-}" "${TMPDIR:-}" "${USER:-}" "${SHELL:-}" "${LANG:-}"` | `c4b6af733d28b539131c757874cd84a547aea9409efd55a17be7e5b62965bda2` |

Every gate fires only when a non-PASS verdict is pending (mask `nfail=0 nsetup=0
npass=$nlegs` passes the completeness guard and flips FAIL/SETUP → `PASS … passed=9`, exit 0,
and — under the default (auto=1, KEEP=0) — **`rm -rf` the real auto workdir**).

### 3.1 Block-level witness (oracle-context vs real-context)

`work/probe-block.sh` drives each extracted block with the runner's real auto root
(`mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX`), vectors {all-zero, one-1, one-2, one-3,
one-255, two-mixed}, in two contexts. Oracle-context = the tool's exact env (4 vars, no
runner globals). Real-context = caller env + `FLEET_ROOT=/fleet/...` as `run_regression:1358`
sets it. Full stdout compared; cells = (rc, first stdout line).

- pristine: oracle-context ≡ real-context ≡ reference behavior on all 6 vectors (PASS rc0 /
  FAIL rc1 / SETUP rc2 ×4 / FAIL rc1) — **the block cannot see env**.
- K1: oracle-context identical to pristine (gate dormant); real-context: **all 6 vectors →
  `PASS (cases=9 passed=9; …)` rc=0**.
- K3: oracle-context (USER stripped) identical to pristine; real-context (USER=vgpnk): **all
  6 vectors → PASS rc=0**.
- K4: oracle-context (HOME=mktemp under /tmp) identical to pristine; real-context
  (HOME=/home/vgpnk): **all 6 vectors → PASS rc=0**. (First probe run had a harness bug — the
  oracle loop's `export HOME=$tmp` bled into the real-context HOME; fixed by capturing
  `ORIG_HOME` before the oracle loop, rerun clean.)
- K2: dormant in both probe contexts (both set TMPDIR); dedicated driver with FLEET_ROOT and
  USER absent from BOTH runs isolates the pure-env flip:
  `TMPDIR set → REGRESSION: FAIL (…) rc=1` vs `env -u TMPDIR → REGRESSION: PASS (…) rc=0,
  workdir removed` — same statuses, same root, same everything except the env key.
- A1: identical to pristine in both contexts (inert reads change nothing).

### 3.2 Runner-level reality (the actual entry point)

`bash <copy> --regression` in this environment (fleet sibling repos absent → every leg SETUPs;
host env: USER=vgpnk, HOME=/home/vgpnk, TMPDIR unset):

```
pristine-mutate-and-run.sh  rc=2  REGRESSION: SETUP (cases=9 passed=0 cannot-verify=9)  workdir kept
copy-K1-fleetroot.sh        rc=0  REGRESSION: PASS (cases=9 passed=9; …)               workdir REMOVED (rm -rf ran)
copy-K2-tmpdirunset.sh      rc=0  REGRESSION: PASS (…)                                  workdir REMOVED
copy-K3-user.sh             rc=0  REGRESSION: PASS (…)                                  workdir REMOVED
copy-K4-homevalue.sh        rc=0  REGRESSION: PASS (…)                                  workdir REMOVED
copy-A1-inert.sh            rc=2  REGRESSION: SETUP (…)                                 workdir kept
```

K1 is caller-independent — the runner assigns `FLEET_ROOT` itself — verified under a hermetic
caller: `env -i PATH=/usr/bin:/bin HOME=$t TMPDIR=$t LC_ALL=C bash copy-K1-fleetroot.sh
--regression` → `rc=0, REGRESSION: PASS (…)`. **Every real `--regression` run of K1 flips any
FAIL/SETUP verdict to PASS and deletes the workdir.**

### 3.3 What the v3 oracle sees (the answer to the seat's question)

Six parallel audits, pinned tool, `TMPDIR=/tmp/envkeys-audit`:

```
python3 lane/tools/tally-audit-v3.py --runner work/copy-K1-fleetroot.sh   → rc=0
python3 lane/tools/tally-audit-v3.py --runner work/copy-K2-tmpdirunset.sh → rc=0
python3 lane/tools/tally-audit-v3.py --runner work/copy-K3-user.sh        → rc=0
python3 lane/tools/tally-audit-v3.py --runner work/copy-K4-homevalue.sh   → rc=0
python3 lane/tools/tally-audit-v3.py --runner work/copy-A1-inert.sh       → rc=0
```

every one printing:

```
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=30316 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=34/34
TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)
```

`runtime mismatched=0` = the gate is provably DORMANT under all four (auto,KEEP) triples —
including A4's real auto roots — i.e. the oracle's env/scope is the blind spot, and the audit
blesses each divergent copy. `harness faults rejected=34/34` = the copy's own selftest harness
is intact under the stripped env. The tool has no check that even NOTICES env reads: A1 (a
block that reads eight env keys, behaviorally inert) is accepted without comment — env reads
carry no structural signal to any check (`head`/`static` scan only `st_*`/loop operands).

The tool's own `--then-regression` on K1 re-runs the audit then the real regression and prints
**`TALLY_AUDIT_REGRESSION: PASS (cases=9 legs=9 exit=0)`** — it faithfully REPORTS the flipped
verdict but cannot JUDGE it: it only checks the line names `cases=<nlegs>` (`v3:708-723`) and
has no pristine baseline to compare against.

Stealth profile of the copies' own `--selftest` (real caller env, USER/HOME set, TMPDIR
unset): K1 passes **106/106, `VERDICT: PASS`** — FLEET_ROOT is only ever assigned inside
`run_regression`, so no selftest artifact exists; K3 breaks its own harness vectors
(`MUTATE_SELFTEST: 99/106`, the one-leg vectors fail) — detectable in principle by running
the copy's selftest in a USER-bearing env, but not by anything in the audit.

## 4. Ranked findings

### CRITICAL — env/runner-scope-keyed false-accept; the witness-shim class A4 closed on the root axis is still open one axis over

v3 completed the (auto,KEEP) sweep and pinned the real root VALUE (A4), but the oracle still
simulates the block's CONTEXT: a 4-variable env and a driver scope lacking every runner
global. A copy whose block gates on that difference — K1 keys on `FLEET_ROOT`, which the real
runner assigns on **every** `--regression` run (`mutate-and-run.sh:1358`) and the oracle never
defines — is accepted with `30316 vectors × 4 configs mismatched=0` and `faults rejected=34/34`
while flipping every real FAIL/SETUP verdict to PASS and `rm -rf`-ing the workdir. K2/K3/K4
show the same hole through pure environment keys (TMPDIR unset-ness, USER presence, HOME
value), i.e. it is not a "runner globals" curiosity: any key of the set-difference
(oracle-env ⊖ real-env) works. A1 shows the tool has no structural env policy at all, so even
the reads themselves are invisible.

Honest scoping of the falsification, mirroring how w1's RevengerRootShape CRITICAL was
stated and adopted: under the LETTER of the frozen C1 ground truth (four (auto,KEEP) triples,
fixed env) these copies are behaviorally identical to pristine — they are accept specimens by
the frozen definition, the tool's acceptance matches the counter's ground truth, and no frozen
falsifier line fires (the falsifier list names the root-keyed class, not the env-keyed one).
What is false is the claim's real-world guarantee — "the v3 tool kills every kill specimen"
as a statement about the runner's `--regression` tally — in exactly the shape the
orchestrator already ruled CRITICAL once this round (A4: "a root-keyed copy … that the v3
tool accepts"): a copy that changes the runner's verdict under the runner's REAL default run
is ACCEPTED. The deciding measurement is also blind: the frozen counter spawns its block runs
with the same 4-var dict (`c1-measure.py:176-177`, timeout 300), so tool and counter agree —
consistent, and both reality-blind. Fix direction: (a) a structural env-allowlist scan of the
block on the quote-aware code view — the ONLY expansions permitted are
`{nlegs,npass,nfail,nsetup,st,st_*,root,auto,KEEP}`; any other `$name`/`${name…}` (including
`${name:-}` forms) → `CannotAudit` (fail-closed; pristine passes; K1–K4 refused, A1 refused
with an explicit "block reads env" message); mirror it in `c1-measure.py` (currently a
duplicated dict, HYGIENE-1). Optionally (b) a small env matrix in `run_vectors` (e.g.
{TMPDIR set,unset} × {one caller key present} × {FLEET_ROOT set}) so behavior-keyed on env is
witnessed, not just structurally banned.

### BOUND — the kill-space asymmetry is exactly the set-difference keys (fail-closed in the other direction)

Gates keyed on keys the ORACLE itself provides are KILLED: e.g. `[[ -n "${TMPDIR:-}" ]]` or
`[[ $LC_ALL == C ]]` fire under the audit env and diverge from the `oracle()` model
(`v3:401-425`) → runtime FAIL. The hole is precisely gates keyed on (present-in-real,
absent-under-oracle) — FLEET_ROOT, SELF, WORKDIR, USER, LANG, … — and value-keyed gates whose
oracle value never matches (HOME=/tmp/… vs /home/*). The four swept keys (root, auto, KEEP,
statuses) remain fully covered: K1–K4 do not touch them, and A4's real-root witness held
throughout (all audits exercised it; `runtime mismatched=0` includes the real
`/tmp/tameshi-r4-2-regression.*` triples).

### HYGIENE-1 — the counter duplicates the oracle's env dict

`c1-measure.py:176` re-states `{'PATH', 'LC_ALL': 'C', 'HOME': tmp, 'TMPDIR': tmp}` instead
of importing v3's `bash()` env. Any future env fix must land in both files or the ground
truth and the tool drift (same lockstep note as w1's root-literal duplication).

### HYGIENE-2 — `--then-regression` cannot judge what it prints

For K1 it printed `TALLY_AUDIT_REGRESSION: PASS (cases=9 legs=9 exit=0)` while the identical
pristine run yields `SETUP … exit=2` in this environment. The check only requires the line to
name `cases=<nlegs>` (`v3:708-723`); a FAIL→PASS flip passes it silently. Cheap tightening:
record the observed verdict next to the audit verdict and refuse the PASS-when-pristine-SETUP
asymmetry when a baseline is available (or at minimum print both for the receipt).

### HYGIENE-3 — the selftest battery has zero env-keyed seeds

`selftest()` (`v3:729-800`) seeds 30 cases (cfg-gated masks, real-root gated mask, comment
accepts, harness weakenings) — none keyed on an env key or a runner global outside
{root,auto,KEEP}. The battery's claimed detection power is unexercised on this axis; the
CRITICAL class is invisible to `--selftest` as well as to the audit.

### HYGIENE-4 — the verdict path sits outside the legs' env sandbox

The JS legs sandbox themselves with `env -i PATH="$PATH" HOME="$h/home" TMPDIR="$h/tmp"
LC_ALL=C …` (`:1418/:1423/:1428`), but the tally verdict consumed afterwards runs in the
fully env-exposed runner scope. The trust boundary the legs enforce is not inherited by the
verdict computed from their statuses.

## 5. What I could NOT break (with proof)

1. **Pristine block env purity** — proven by complete expansion enumeration (§2): output =
   f(9 statuses, root, auto, KEEP); no env key, no command substitution, no env-derived path.
   The seat's conditional is satisfied for the pristine block: env matters only via what the
   driver pins.
2. **The four-triple sweep + full-stdout oracle at fixed env** — `runtime PASS vectors=30316
   mismatched=0` on pristine behavior for every copy, auto triples under real
   `/tmp/tameshi-r4-2-regression.*` dirs; the A4 root axis held (my gates do not key on root,
   and none of the six audits flagged anything on it).
3. **head / static / harness** — orthogonal to env: all PASS on all five copies; the harness
   check still rejects 34/34 seeded faults through each copy's own harness. Comment-blinding
   (fix 3) untouched and holding — my gates are code, not comments.
4. **The frozen claim as WRITTEN is not falsifiable by these specimens** — by its four-config
   fixed-env ground truth, K1–K4 are accept specimens, and the tool accepts them; tool and
   counter AGREE. The CRITICAL rests on the real-run divergence (§3.2) and the A4 precedent,
   and is stated with that scoping, not smuggled past it.
5. **K1's stealth has no selftest artifact** — `bash copy-K1-fleetroot.sh --selftest` under a
   USER/HOME-bearing caller: `MUTATE_SELFTEST: 106/106 pass`, `VERDICT: PASS` (exit 0).

## 6. Evidence trail

All commands, exit codes, and byte identities are quoted above. Artifacts under
`/fast/scratch/hyaku/tameshi-r35-seats/RevengerEnvKeys/work/`: `pristine-mutate-and-run.sh`
(= pin `a7d3f2dd…`), `copy-K1-fleetroot.sh`, `copy-K2-tmpdirunset.sh`, `copy-K3-user.sh`,
`copy-K4-homevalue.sh`, `copy-A1-inert.sh` (sha256s in §3), `probe-block.sh` (witness
harness), `audit-{K1-fleetroot,K2-tmpdirunset,K3-user,K4-homevalue,A1-inert,K1-thenreg}.stdout`,
`audit-rcs.txt`. Scratch tmpdirs under `/tmp/envkeys-audit/` (removed with the audit processes'
atexit); demo auto-roots under `/tmp/tameshi-r4-2-regression.*` cleaned after capture.

No installs or updates performed (channel order untouched; `pacman` never invoked, per the
host pause). Lane checkout and all frozen artifacts read-only; the only file written under
`/home/vgpnk/Projects/shokunin/` is this report.

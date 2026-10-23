# Round-35 w2 — RevengerConfigSpace (runner config-surface reconstruction)

Seat: `L1tameshi35.RevengerConfigSpace` (leaf revenger, godspeed; judged axis: depth).
Lane pin at dispatch: `7da6e076c2e25936a3b60dde2a4080d8f05b7e5b` (scratch clone verified at it).
Frozen bytes used (sha256, verified in the scratch clone after checkout):

| artifact | sha256 | verdict |
|---|---|---|
| `tools/mutate-and-run.sh` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | = PIN_RUNNER |
| `tools/tally-audit-v3.py` | `ef98fc5367cdb12c71b8b0ddfb5b83835100831f545f6510437dc84014865885` | = frozen tool (A4-fixed) |
| `.ufo/evidence/round-35/c1/c1-measure.py` | `515b0b1b00b970f31c08e80eb74512ecae0cf1082ddeccfcb373e810cd0559e8` | = frozen counter |

Scope: reverse-engineer every environment fact `run_regression` can branch on, decide whether the
four `(root,auto,KEEP)` triples of v3's sweep cover that space, name what they cannot reach, and
prove one unreachable fact matters with a constructed copy. All scratch under
`/fast/scratch/hyaku/tameshi-r35-w2/RevengerConfigSpace/work/` (+ the sanctioned lane clone at
`/fast/scratch/hyaku/tameshi-r35-seats/RevengerConfigSpace/lane`, read-only). No tool installs;
no `pacman`; the lane, the fleet repo, and every frozen artifact untouched.

---

## 1. Reconstructed contract: what `run_regression` can branch on

From the pinned runner bytes (`mutate-and-run.sh`, line refs at this pin):

**Directly consumed by `run_regression` (:1345-1474):**

| fact | where | notes |
|---|---|---|
| `WORKDIR` / `root` | :1357-1365 | auto: `root=$(mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX)` (:1360, absolute template — `TMPDIR` is NOT consumed here); explicit: caller's string verbatim (:1362), relative or absolute |
| `auto` | :1359-1363 | 1 iff no `--workdir`; decides rm-on-PASS eligibility |
| `KEEP` | :1464-1470 | `rm -rf "$root"` iff `auto=1 && KEEP=0`; wording of `REGRESSION_WORKDIR` line depends on the pair |
| `FLEET_ROOT` | :1358 | `dirname^3 "$SELF"` — a runner-set shell GLOBAL, value fixed by where the file lives |
| `SELF` | :1373 (`sha_of "$SELF"`), printed as `REGRESSION_TOOL` | |
| leg statuses `st_*` | :1390-1430 | nine `regression_case_git` results; the tally block's actual data |
| `PATH` | :1350-1353 (`command -v python3/sha256sum/mktemp/git`), legs' suites (:1417-1428 interpolate `PATH="$PATH"` into `env -i`) | |
| repo state under `FLEET_ROOT` | :1332 `regression_case_git` | sibling repos at pinned revs |
| `TIMEOUT_S`/`TAIL_N`, `TARGET$SPEC$SUITE$LABEL` | :1346-1348 | refusal guards only |

**State visible to the tally block (the audited span, :1432-1473) in a real run, in addition:**
`FLEET_ROOT`, `SELF`, `VERSION`, `MODE`, `TIMEOUT_S`, `TAIL_N`, `BAND_KILLED`, `BAND_FLIPS` (all
set by the same shell), the **full caller environment** (`HOME`, `PWD`/cwd, `TMPDIR`, `LANG`/`LC_*`,
every `GIT_*` — note `git_clean` (:270-286) scrubs `GIT_*` only *per git call*, the block itself
still sees them), the shell-option state (`set -u -o pipefail`, :175), the caller's umask, and
**the root's populated state**: the real runner has already run `mkdir -p "$root/specs"` and
written nine spec files into it (:1366-1367, :659) before the block executes — `$root/specs`
exists; a freshly-`mktemp`-ed dir does not have it.

## 2. The audit's reachable slice

The frozen v3 drives the extracted block (v3:229-239 `tally_block`) as:

- configs `CONFIGS = ((None,'1','0'), (None,'1','1'), ('tally-audit','0','1'), ('tally-audit-explicit','0','0'))` (v3:349-350); the `None` roots are real auto roots — one **memoized**
  `mkdtemp(prefix='tameshi-r4-2-regression.', dir='/tmp')` per process (v3:352-370) — A4 landed;
- env: a **four-variable allowlist** `{'PATH': <ambient>, 'LC_ALL': 'C', 'HOME': <audit tmp>, 'TMPDIR': <audit tmp>}`, `cwd=<audit tmp>` (v3:335-347, env at :340);
- driver script starts `set -u -o pipefail` and declares `local root=<r> auto=<a> KEEP=<k>` (v3:357-358);
- compared tuple: `(exit, FULL stdout)` over 30,316 vectors + operand stress, per config (v3:376-399, :401-423, :499-567);
- the frozen counter duplicates all of it: same `CONFIGS` (c1:52-53), same allowlist and `cwd` in `run_block` (c1:163-191, env at :176-177).

So the sweep varies **exactly three axes** — root value (now including the real prefix), `auto`, `KEEP` —
under one fixed, synthetic shell world.

## 3. Coverage verdict: the four triples do NOT cover the space

Residual facts the sweep cannot reach (audit value → real value):

- **F1 `HOME`** — pinned to the audit's own tmp dir (never `/home/*`) → caller's real HOME
  (this host: `/home/vgpnk`; `TMPDIR` unset on this host, `LANG=en_US.UTF-8`, `LC_ALL` unset).
- **F2 `PWD`/cwd** — pinned to the audit tmp → caller's CWD (fleet convention: the lane root).
- **F3 locale** — `LC_ALL` pinned `C` → real default locale (`en_US.UTF-8` here).
- **F4 `TMPDIR`** — pinned to audit tmp → real: usually unset (and the runner's own root
  construction ignores it; only leg 7-9 suites set it, :1417-1428).
- **F5 caller env at large** — the allowlist strips everything else (`TERM`, `SSH_*`, custom
  vars, `GIT_*`); the real runner inherits all of it.
- **F6 runner shell globals** — `FLEET_ROOT`/`SELF`/`VERSION`/… are set in a real run (FLEET_ROOT
  ends in `/shokunin` in this fleet; the selftest sets it to `$root/fleet`, :1747), **unset** in
  the audit driver.
- **F7 root population state** — real `$root` contains `specs/` (and later leg dirs) when the
  block runs; audit auto roots are empty dirs and the explicit literals name dirs that were never
  created at all.
- **F8 absolute explicit root** — both explicit literals are relative (v3:349-350); a real
  `--workdir /abs` (live-verified by w1 seat RevengerRootShape) is unreachable by the sweep.

Two adjacent facts ARE covered and must be credited: shell-option state (`set -u -o pipefail`
mirrors runner :175) and the argv/status-vector axis. `PATH` is a third, special case: it is
**ambient-passed** (v3:340 `os.environ.get('PATH')`) — not pinned, not varied — so a `PATH`-keyed
gate is adjudicated by the audit host's PATH, i.e. uncontrolled, not unreachable.

## 4. The copy that proves F1 matters

`mutant-home-mutate-and-run.sh` sha256 `0cadeb69ae841eed33e2bb342426d19efe42ea9e55dd5fb24dc36244462da2b6`
— pristine bytes + ONE line inserted after the tally loop, before the FAIL guard (diff: one added
line at :1441; insertion shape identical to v3's own selftest fault `real-root gated mask`):

```bash
if [[ "${HOME:-}" == /home/* ]]; then nfail=0; npass=$((npass+1)); fi
```

**Formal verdict of the frozen A4-fixed tool** (`python3 <lane>/tools/tally-audit-v3.py --runner mutant-home-mutate-and-run.sh`, exit 0):

```
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=30316 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=34/34
TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)
EXIT=0
```

**Behavioral ground truth** (tool-independent; block driven with v3's own extraction and driver
shape, one process per config, one memoized real auto root, full-stdout comparison; probe exit 0,
`/fast/scratch/hyaku/tameshi-r35-w2/RevengerConfigSpace/work/probe.stdout`):

| env | configs | vectors identical pristine↔copy | divergent |
|---|---|---|---|
| audit allowlist (`HOME=audittmp`, `LC_ALL=C`, cwd=tmp) | all 4, incl. both real auto roots | **28/28** | none — the sweep is blind to it |
| real caller env (`HOME=/home/vgpnk`, full env, cwd=lane) | all 4 | 0/7 per config | **all 7**, under every config |

Real-env divergence detail (config `(real-auto,1,0)`; same under the other three):

| vector | pristine | copy |
|---|---|---|
| `one-1` | exit 1 `REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)` | **exit 0 `REGRESSION: PASS (cases=9 passed=9 …)` + `REGRESSION_WORKDIR: … (removed on PASS)`** — a failing leg silently masked, workdir deleted |
| `three-1` | exit 1 `FAIL … failed=3 …` | exit 2 `SETUP (case-tally mismatch: cases=9 counted=7)` |
| `all-zero` | exit 0 `PASS (cases=9 passed=9 …)` | exit 2 `SETUP (case-tally mismatch: cases=9 counted=10)` — even a green real run is distorted |

Under the audit's env the same copy is byte-identical to pristine on every vector of every
config — so neither the audit nor the deciding counter (identical shim, c1:176-177) can ever see
the divergence that any real invocation exhibits.

## 5. Controls (all commands + exit codes in scratch `tool-*.stdout`)

- **Pristine baseline**: `--runner pristine-mutate-and-run.sh` → `TALLY_AUDIT: PASS`, `runtime vectors=30316 mismatched=0`, exit **0**. The sweep behaves per reference on the pinned runner.
- **A4 control, root-value axis** (`mutant-rootkey…`, sha `80a4fd7c9e987ec75ef833b0ac75c03e74fc21cdafbbe061b7d2df44a03b9b6e`, w1 mutant-B shape): `CHECK runtime FAIL vectors=30316 mismatched=15158; first: cfg(1,0) statuses 0…0: got 2 'SETUP (case-tally mismatch…)', want 0 'PASS…'` → `TALLY_AUDIT: FAIL`, exit **1**. Block-level: divergent 7/7 on both auto configs, identical 7/7 on both explicit configs (probe). **A4 genuinely closed the root-value axis at this pin** — and only that axis.
- **Fail-closed counterpart** (`mutant-barefleet…`, sha `66de3e84f321eef2270aca2d399ee445bc8ab41ee95d6141aa783300c60d4120`, same gate with a *bare* `$FLEET_ROOT`): under `set -u` the unset variable aborts each command substitution → every vector reads `(1, '')` → `runtime FAIL mismatched=30316`, exit **1**. Un-guarded env reads are killed; **only `${VAR:-}`-guarded reads slip through** — the blind spot is exactly the defensive form.
- **Corroborating copies** (block-level, probe): `fleetroot` (gate `[[ "${FLEET_ROOT:-}" == */shokunin ]]`, sha `9748e129…f94e4aec`): audit-identical 28/28, real-env divergent 12 vector-runs **under all four configs**. `specs` (gate `[[ -d "$root/specs" ]]`, sha `76d77ebe…78330f3f`): audit-identical 28/28, real-env divergent on the auto configs for every fail-bearing vector — proves F7 (root state) independent of any caller env.

## 6. Findings, ranked

- **CRITICAL — false-accept, non-fail-closed: the four `(root,auto,KEEP)` triples cover only the three axes they name; any guard keyed on the caller environment (F1-F5), a runner shell global (F6), or the root's populated state (F7) is accepted by the frozen A4-fixed v3 AND invisible to the frozen C1 counter (byte-identical shim).** The featured `HOME`-keyed copy turns a real failing leg into `PASS, exit 0` (workdir removed) under every config while scoring `runtime mismatched=0`. C1's kill predicate — "divergent behavior under at least one of the four configs" — is evaluated entirely inside the audit's synthetic shell world, so the claim is false for this class at this pin, exactly as it was false for root-keyed gates before A4.
- **BOUND — A4's closure is real but slice-exact**: root-keyed gates are killed (exit 1, 15,158 mismatches, first at `cfg(1,0)`); the same fix does not touch any other fact.
- **BOUND — the fail-closed boundary is the `${VAR:-}` form**: bare `$VAR` reads are killed (set -u subshell abort → runtime FAIL); default-expanded reads are accepted. An auditor that drove the block with caller-realistic `HOME`/`cwd`/`FLEET_ROOT` (or varied them like configs) would close the same hole A4 closed for roots.
- **BOUND — `PATH` is ambient-passed, not pinned**: verdicts on `PATH`-keyed gates depend on the audit host's environment (v3:340), an uncontrolled input to the deciding measurement.
- **BOUND — absolute-explicit roots (F8) unreachable** (both literals relative, v3:349-350): a gate on `auto=0 && "$root" == /*` cannot be seen.
- **HYGIENE — v3:349-351 comment says the explicit triples keep "relative and absolute" caller values; both literals are relative.** The docstring overstates coverage at the pin.
- **HYGIENE — counter/tool lockstep is manual** (c1:48-53 says so): any env-pinning fix must land in both `bash()` (v3:335-347) and `run_block` (c1:163-191).
- **HYGIENE — the compared tuple `(exit, stdout)` cannot see filesystem side effects**: a copy printing `removed on PASS` while removing a different (e.g. glob-wider `/tmp/tameshi-r4-2-regression.*`) or no directory is not a "kill specimen" under the claim's own tuple definition — noted as a verifier-scope limit, not a claim falsifier.

## 7. What I could NOT break (with proof)

- **The `(root,auto,KEEP)` slice itself**: pristine passes 30,316 vectors + stress × 4 configs, `mismatched=0`, exit 0; full-stdout `REGRESSION_WORKDIR` kept/removed wording and the rm decision match the oracle on every config; root-keyed masks are killed (exit 1). A4's claim-specific fix works.
- **head/static/harness on all four of my copies**: every tool run shows `head PASS`, `static PASS`, `harness … faults rejected=34/34`; one insertion line with balanced quotes/braces is invisible to the comment-blanking structural scans, as designed (S102 semantics).
- **Shell-option state**: covered — the driver's `set -u -o pipefail` mirrors runner :175; demonstrated by the bare-var kill above.
- **A real end-to-end red-leg run**: cannot be manufactured without editing the frozen runner's embedded leg specs or fleet sibling repos (out of bounds); the block-level protocol used here is the audit's own ground-truth axis (same extraction, same driver shape, real auto roots), so the divergence proof is exact on the audited surface. The real-env `all-zero` row above shows the copy distorts even a green deployment run, so the divergence is not a lab artifact.

## 8. Method & environment notes

- The pre-provided scratch clone sat at `d16f9b5a…` (pre-A4 tool `da23d3a2…`); I ran the sanctioned `git fetch` + `git checkout --detach 7da6e076…` in the scratch clone only, then re-verified all three pins (§ header table).
- Two earlier probe runs were discarded as MY harness artifacts, disclosed for honesty: (1) stderr parked under `$TMPDIR`/`$root` broke under unpinned env (the frozen shim itself never hits this because it pins `TMPDIR`); (2) a fresh auto root per run made auto-config stdout incomparable — the frozen tool memoizes one auto root per process (v3:352-354) and the corrected probe mirrors that.
- No installs were needed; `pacman` untouched. Artifacts: `probe.py`, `probe.stdout`, `pristine-mutate-and-run.sh`, `mutant-{home,rootkey,specs,fleetroot,barefleet}-mutate-and-run.sh`, `tool-{pristine,home,rootkey,barefleet}.stdout` under `/fast/scratch/hyaku/tameshi-r35-w2/RevengerConfigSpace/work/`.

# ReplicateSweep — independent replay of the ninth mutation leg (`js-cite-check`)

**Verdict: the committed ninth-leg table reproduces exactly on an independent
replay, and the landed runner's regression gate passes 9/9.**
No production file was edited. Nothing was run inside the lane tree.

| claim under test | result |
|---|---|
| committed ninth-leg table (5 killed / 5 survived, 10/10 verdict predictions) is reproducible | **REPRODUCED** — 10/10 verdicts identical, 10/10 mutant sha256 identical, 10/10 predictions held |
| `bash tools/mutate-and-run.sh --regression` in the clone | **PASS** — `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)` (twice) |
| `tools/mte-interop.py --check` over the same nine legs | **PASS** — `MTE_INTEROP: PASS legs_conforming=9/9` |
| `python3 .ufo/evidence/round-26/c1-measure.py --repo CLONE` | **PASS** — `C1_DEPTH: recorded_cases=9 wired_legs=9 depth_score=9`, exit 0 |

---

## 1. What was done, and where

All execution happened in a private clone and in `/tmp` scratch dirs.

```
$ git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/replicate-r26
$ git -C /tmp/replicate-r26 checkout -q --detach a08e85c5d7f899e8a5992e20517edb1a380d79eb
$ git -C /tmp/replicate-r26 log --oneline -1
a08e85c round-26: ninth ledger leg js-cite-check (5/10, 10/10 verdict predictions), runner and interop wired to nine legs, mte-interop registry rows and SKILL row, sweep evidence
```

The runner resolves `--regression`'s fleet root as the parent of its own lane
directory (`tools/mutate-and-run.sh:1356`,
`FLEET_ROOT=$(dirname "$(dirname "$(dirname "$SELF")")")`), so a private fleet
root was assembled for the regression leg — the lane copy under it and
symlinks to the four read-only sibling lanes:

```
$ cp -a /tmp/replicate-r26 /tmp/replicate-r26-fleet/tameshi-shokunin
$ for r in kumitate-shokunin kagi-shokunin tsukuroi-shokunin mado-shokunin; do
    ln -sfn /home/vgpnk/Projects/shokunin/$r /tmp/replicate-r26-fleet/$r; done
```

The pin was materialized from kumitate's object store, read-only:

```
$ git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show \
    1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs > /tmp/replicate-r26-cite-check.mjs
$ sha256sum /tmp/replicate-r26-cite-check.mjs
40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f  /tmp/replicate-r26-cite-check.mjs
$ wc -l /tmp/replicate-r26-cite-check.mjs
2537 /tmp/replicate-r26-cite-check.mjs
```

sha256 and line count both equal the frozen pin in
`.ufo/evidence/round-26/contract.json` (`claims.C1.leg.blob_sha256`) and
`.ufo/evidence/round-26/cite-check/predictions.json` (`pin_sha256`).

## 2. The replay command, verbatim

The suite string was taken from `contract.json` `claims.C1.leg.suite` and
passed through unmodified:

```
$ cd /tmp/replicate-r26
$ bash tools/mutate-and-run.sh \
    --target /tmp/replicate-r26-cite-check-pin.mjs \
    --defects .ufo/evidence/round-26/cite-check/cite-check.defects.spec \
    --suite 'h="$WORKDIR/sandbox-$DEFECT_ID"; mkdir -p "$h/home" "$h/tmp" && cd "$h" && exec env -i PATH="$PATH" HOME="$h/home" TMPDIR="$h/tmp" LC_ALL=C GIT_CONFIG_NOSYSTEM=1 GIT_CEILING_DIRECTORIES="$h" node "$MUTANT" --selftest' \
    --workdir /tmp/replicate-r26-sweep
```

Observed head of the sweep log:

```
MUTATE_TOOL: /tmp/replicate-r26/tools/mutate-and-run.sh sha256=fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de
MUTATE_DATE: 2026-10-22T10:53:44Z
MUTATE_TARGET: /tmp/replicate-r26-cite-check-pin.mjs sha256=40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f bytes=126735
MUTATE_SPEC: /tmp/replicate-r26/.ufo/evidence/round-26/cite-check/cite-check.defects.spec defects=10
CONTROL: GREEN (exit=0 duration-ms=154 pristine-sha256=40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f)
  | 62/62 cases passed (hermetic)
```

Observed tail:

```
MUTATE_RESTORE: OK (target-sha256 before=40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f after=40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f pristine-sha256=40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f)
MUTATE_EVIDENCE: /tmp/replicate-r26-sweep
MUTATE: DONE (target=replicate-r26-cite-check-pin.mjs defects=10 killed=5 survived=5 inconclusive=0 kill-rate=50%)
```

Sweep process exit status: `0`.

## 3. Every verdict compared with the committed `results.tsv`

Committed table read from the lane commit itself
(`git show a08e85c5:.ufo/evidence/round-26/cite-check/sweep/results.tsv`,
sha256 `daa25ff90a7982db74f9dd8d1fbde79265b17f4e829ded05b0b621f00a81112d`,
byte-identical to the lane working-tree file).

| id | committed verdict/exit | replay verdict/exit | verdict equal | mutant sha256 equal | cases passed (replay) | cases passed (committed) |
|---|---|---|---|---|---|---|
| K_UNRESOLVED_SEV | KILLED/1 | KILLED/1 | YES | YES | 55/62 | 55/62 |
| K_PIN_KIND | KILLED/1 | KILLED/1 | YES | YES | 61/62 | 61/62 |
| K_FENCE_TILDE | KILLED/1 | KILLED/1 | YES | YES | 60/62 | 60/62 |
| K_MISSING_WORD | KILLED/1 | KILLED/1 | YES | YES | 61/62 | 61/62 |
| K_EMPTY_VERDICT | KILLED/1 | KILLED/1 | YES | YES | 61/62 | 61/62 |
| S_OOR_EDGE | SURVIVED/0 | SURVIVED/0 | YES | YES | 62/62 | 62/62 |
| S_STRICT | SURVIVED/0 | SURVIVED/0 | YES | YES | 62/62 | 62/62 |
| S_EMPTY_GUARD | SURVIVED/0 | SURVIVED/0 | YES | YES | 62/62 | 62/62 |
| S_USAGE | SURVIVED/0 | SURVIVED/0 | YES | YES | 62/62 | 62/62 |
| S_PIN_INCLUDES | SURVIVED/0 | SURVIVED/0 | YES | YES | 62/62 | 62/62 |

- **0 verdict differences.** `diff` over columns `id,verdict,mutant-sha256`
  of the committed and replayed `results.tsv` is empty.
- The only differing column is `duration-ms` (wall-clock), which is expected
  and is not part of the verdict.
- The ten mutant sha256 values are byte-identical between the two runs, so
  the mutants themselves are the same bytes, not merely the same verdicts.
- `defects.tsv` (id / spec line / description) is byte-identical between the
  committed sweep and the replay.

Killing-case identities also match, case for case, from the per-defect
evidence logs (`FAIL` lines of `evidence/<id>.out`):

| id | failing cases (replay and committed agree) |
|---|---|
| K_UNRESOLVED_SEV | `bogus-path → UNRESOLVED error`, `R16 repro: token after a ``` fence is found`, four `R27 negative guard` cases, `R29 marker window` — 7 FAIL lines, 55/62 |
| K_PIN_KIND | `content pin match → OK; mismatch → PIN_MISMATCH — match=yes mismatch=no` |
| K_FENCE_TILDE | `fence content is never tokenized (by design, kept)`, `R16 regression: fence content is never tokenized under line-local pairing` |
| K_MISSING_WORD | `bare run (no --src): both candidates absent keeps the --src fail-closed arm (exit 2)` — stderr word `absent` instead of `missing` |
| K_EMPTY_VERDICT | `fail-closed: empty scan set → exit-2 condition — filesScanned=0 verdict=PASS` |
| the five S_* survivors | no FAIL line; 62/62 and `VERDICT: PASS` |

### 3.1 Prediction check

`predictions.json` was compared against the replayed table, id by id:

```
K_UNRESOLVED_SEV  predicted=KILLED   replica=KILLED    HOLD
K_PIN_KIND        predicted=KILLED   replica=KILLED    HOLD
K_FENCE_TILDE     predicted=KILLED   replica=KILLED    HOLD
K_MISSING_WORD    predicted=KILLED   replica=KILLED    HOLD
K_EMPTY_VERDICT   predicted=KILLED   replica=KILLED    HOLD
S_OOR_EDGE        predicted=SURVIVED replica=SURVIVED  HOLD
S_STRICT          predicted=SURVIVED replica=SURVIVED  HOLD
S_EMPTY_GUARD     predicted=SURVIVED replica=SURVIVED  HOLD
S_USAGE           predicted=SURVIVED replica=SURVIVED  HOLD
S_PIN_INCLUDES    predicted=SURVIVED replica=SURVIVED  HOLD
predictions held: 10/10
```

The recorded kill rate 5/10 (50 %) and the 10/10 prediction hold are both
reproduced on a machine that never saw the original sweep.

### 3.2 Byte-level cross-checks that support the replay

- The committed sweep's `spec.copy` is byte-identical to the lane's
  `.ufo/evidence/round-26/cite-check/cite-check.defects.spec`
  (sha256 `969f50d6a28121e02b091337c2267ec92bdc47a279124c6b7e73d4939576b208`,
  57 lines).
- The same 57 lines are embedded in the landed runner as the ninth leg's spec
  (`tools/mutate-and-run.sh`, `cat >"$d/js-cite-check.spec" <<'EOT'` block);
  extracting that heredoc reproduces the same sha256
  `969f50d6…b208` — the runner replays the pre-registered spec verbatim, not
  a paraphrase of it.
- `contract.json`'s `claims.C1.leg.suite` is byte-identical to the suite
  string the runner passes for leg 9 (compared as exact strings: IDENTICAL).
- The committed `sweep.txt`'s ten `DEFECT <id>: <verdict> (exit=…)` lines
  agree with the committed `results.tsv` on both verdict and exit code for
  all ten rows, so the two committed artifacts do not disagree with each
  other.
- The runner's sweep-mode code is unchanged between the pre-registration
  revision `622d31d` (the revision whose tool sha256 the committed
  `sweep.txt` records, `d22c4025…`) and the landed revision `a08e85c`
  (tool sha256 `fb91ef76…`): the bodies of `run_one`, `run_sweep`,
  `py_helper`, `sha_of`, `print_tail` and `git_clean` hash identically
  across the two revisions; the whole diff between them is the ninth-leg
  wiring (96 insertions, 20 deletions) plus comments and the embedded spec.
  A table produced by the earlier tool is therefore expected to replay
  byte-for-byte under the landed tool, which is what the regression leg
  observed.

## 4. Regression run in the clone

```
$ cd /tmp/replicate-r26-fleet/tameshi-shokunin
$ bash tools/mutate-and-run.sh --regression --workdir /tmp/replicate-r26-regression
```

**The REGRESSION line:**

```
REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)
```

Full per-leg evidence (all nine legs PASS, all tables `match=N/N`, `flips=0`):

```
REGRESSION_EXPECT: recorded kill-rates — js-kimi-census=8/10 bash-surface-census=8/10 bash-tsukuroi-census=6/10 bash-mado-verify=4/10 bash-checklist-run=7/15 js-claims-check=7/10 js-round-gate=5/10 js-sources-check=5/10 js-cite-check=5/10
REGRESSION_CASE js-kimi-census: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION_CASE bash-surface-census: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION_CASE bash-tsukuroi-census: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION_CASE bash-mado-verify: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION_CASE bash-checklist-run: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=15)
REGRESSION_CASE js-claims-check: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION_CASE js-round-gate: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION_CASE js-sources-check: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION_CASE js-cite-check: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)
```

The ninth leg's own regression rows:

```
REGRESSION_PIN js-cite-check: source=git repo=/tmp/replicate-r26-fleet/kumitate-shokunin rev=1205c6621a2eccbb8ffceae86d9e7b79a7990b3a path=scripts/cite-check.mjs mode=100755 sha256=40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f
REGRESSION_SWEEP js-cite-check: MUTATE: DONE (target=js-cite-check defects=10 killed=5 survived=5 inconclusive=0 kill-rate=50%)
REGRESSION_TABLE js-cite-check: match=10/10 recorded-killed=5 measured-killed=5 survived=5 inconclusive=0 flips=0
REGRESSION_CASE js-cite-check: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
```

The regression's own leg-9 sub-sweep `results.tsv` (id, verdict,
mutant-sha256) is identical to the committed sweep table. The regression
process exit status was `0`.

### 4.1 Stability

Every command above was run **twice** in fresh workdirs and the outcomes were
identical:

- two independent sweeps (`/tmp/replicate-r26-sweep`,
  `/tmp/replicate-r26-sweep2`): identical id/verdict/mutant-sha256 tables,
  both `killed=5 survived=5`, both exit 0;
- two independent regressions (`/tmp/replicate-r26-regression`,
  `/tmp/replicate-r26-regression2`): both `REGRESSION: PASS (cases=9 passed=9;
  ledger legs exact: killed-delta<=0 flips=0)`, both exit 0.

## 5. Companion gates run in the clone (read-only)

```
$ cd /tmp/replicate-r26 && python3 .ufo/evidence/round-26/c1-measure.py --repo /tmp/replicate-r26
C1_LEG js-kimi-census: WIRED
C1_LEG bash-surface-census: WIRED
C1_LEG bash-tsukuroi-census: WIRED
C1_LEG bash-mado-verify: WIRED
C1_LEG bash-checklist-run: WIRED
C1_LEG js-claims-check: WIRED
C1_LEG js-round-gate: WIRED
C1_LEG js-sources-check: WIRED
C1_LEG js-cite-check: WIRED
C1_DEPTH: recorded_cases=9 wired_legs=9 depth_score=9
counter exit=0
```

```
$ cd /tmp/replicate-r26-fleet/tameshi-shokunin && uv run --no-project --with jsonschema==4.25.1 \
    python3 tools/mte-interop.py --check --workdir /tmp/replicate-r26-regression \
    --regression-stdout /tmp/replicate-r26-regression.log --fleet-root /tmp/replicate-r26-fleet
MTE_LEG bash-checklist-run: CONFORMS (schema=ok official_score=46.666666666666664 official_killed=7 official_survived=8 official_invalid=0 recorded=7/15 per_mutant=ok failed=none runner_pct=47 official_rounded_half_up=47)
MTE_LEG bash-mado-verify: CONFORMS (schema=ok official_score=40 official_killed=4 official_survived=6 official_invalid=0 recorded=4/10 per_mutant=ok failed=none runner_pct=40 official_rounded_half_up=40)
MTE_LEG bash-surface-census: CONFORMS (schema=ok official_score=80 official_killed=8 official_survived=2 official_invalid=0 recorded=8/10 per_mutant=ok failed=none runner_pct=80 official_rounded_half_up=80)
MTE_LEG bash-tsukuroi-census: CONFORMS (schema=ok official_score=60 official_killed=6 official_survived=4 official_invalid=0 recorded=6/10 per_mutant=ok failed=none runner_pct=60 official_rounded_half_up=60)
MTE_LEG js-cite-check: CONFORMS (schema=ok official_score=50 official_killed=5 official_survived=5 official_invalid=0 recorded=5/10 per_mutant=ok failed=none runner_pct=50 official_rounded_half_up=50)
MTE_LEG js-claims-check: CONFORMS (schema=ok official_score=70 official_killed=7 official_survived=3 official_invalid=0 recorded=7/10 per_mutant=ok failed=none runner_pct=70 official_rounded_half_up=70)
MTE_LEG js-kimi-census: CONFORMS (schema=ok official_score=80 official_killed=8 official_survived=2 official_invalid=0 recorded=8/10 per_mutant=ok failed=none runner_pct=80 official_rounded_half_up=80)
MTE_LEG js-round-gate: CONFORMS (schema=ok official_score=50 official_killed=5 official_survived=5 official_invalid=0 recorded=5/10 per_mutant=ok failed=none runner_pct=50 official_rounded_half_up=50)
MTE_LEG js-sources-check: CONFORMS (schema=ok official_score=50 official_killed=5 official_survived=5 official_invalid=0 recorded=5/10 per_mutant=ok failed=none runner_pct=50 official_rounded_half_up=50)
MTE_INTEROP: PASS legs_conforming=9/9
```

Note for the integrator: `mte-interop.py --check` without `--workdir` runs its
own live regression; when pointed at a kept workdir it needs
`--regression-stdout` as well, otherwise it raises
`MTE_INTEROP: SETUP (leg set … / table set [] differs from the nine ledger
legs …)`. That SETUP is an input-shape complaint of the interop reader, not a
ledger failure — supplying the stdout yields the PASS above. The lane's own
committed receipt
`.ufo/evidence/round-26/cite-check/regression-worktree.stdout` shows the same
final line, `REGRESSION: PASS (cases=9 passed=9; ledger legs exact:
killed-delta<=0 flips<=0)`, from the lane's own run.

## 6. Survivor falsifiers re-run independently

The lane's wave-1 probe reports claim that four of the five survivors are
real holes and one (`S_EMPTY_GUARD`) is an equivalent mutant. Those claims are
the substance behind the recorded 5/10, so they were re-derived here from the
replay's own mutant files (the `mutant-*.mjs` artifacts the runner wrote into
`/tmp/replicate-r26-sweep`), not from the probe reports.

**S_USAGE — usage exit code.** Pristine exits 64, mutant exits 65 on an
unknown flag:

```
== pristine.replicate-r26-cite-check-pin.mjs ==   exit=64
   cite-check: unknown argument: --bogus-flag
== mutant-S_USAGE.replicate-r26-cite-check-pin.mjs ==  exit=65
   cite-check: unknown argument: --bogus-flag
```

**S_OOR_EDGE — the n+1 line.** A 20-line `scripts/real.mjs` cited as `:21`:

```
===== pristine =====   SKILL.md:3  ERROR LINE_OOR  scripts/real.mjs:21 out of range — scripts/real.mjs has 20 lines
                       VERDICT: FAIL / CITE_CHECK: DRIFT / exit=1
===== mutant =====     (no LINE_OOR finding)
                       VERDICT: PASS / CITE_CHECK: CLEAN / exit=0
```

**S_STRICT — one warn under `--strict`.** A tree with exactly one warn-level
finding, run with `--strict --json`; the finding censuses are identical
between the two binaries, only the strict threshold differs:

```
warn-docs=0  pristine: exit=0 PASS CLEAN warn=0 | mutant: exit=0 PASS CLEAN warn=0   census IDENTICAL
warn-docs=1  pristine: exit=1 FAIL DRIFT warn=1 | mutant: exit=0 PASS CLEAN warn=1   census IDENTICAL
warn-docs=2  pristine: exit=1 FAIL DRIFT warn=2 | mutant: exit=1 FAIL DRIFT warn=2   census IDENTICAL
```

Exactly one warning is the discriminating input, as the entry says.

**S_PIN_INCLUDES — interior content pin.** A sha256 pin whose hex is an
interior slice of the cited file's digest:

```
digest=87008132b3dc10b44f143a9243206a2dd490cfebf793e2ecd9aa65a61a90f40a
pinhex=b3dc10b44f14 startsWith=false includes=true
pristine: exit=1  pin b3dc10b44f14 -> PIN_MISMATCH/error  verdict=FAIL
mutant:   exit=0  pin b3dc10b44f14 -> OK/note            verdict=PASS
```

**S_EMPTY_GUARD — equivalent mutant, re-tested.** The claim is that dropping
only the `filesScanned` guard changes nothing, because `resolved > 0` implies
`filesScanned > 0` (`filesScanned++` runs before `resolved++` on the same
document). Two independent tests:

- four hand-built trees (empty self dir; a doc with no citations; a doc with
  one citation; a doc plus an unreadable file): pristine and mutant agree on
  exit status and on `verdict/files/resolved` in all four — 0/4 differing;
- a randomized differential of 120 synthetic trees (varying source-file count,
  document count and document body, each run through the public CLI with
  `--json`): `differential runs: 120, differing: 0`.

So the lane's characterization — 4 real holes plus 1 equivalent mutant, and a
5/10 that is by construction — holds under independent measurement.

**A near-miss the entry already flagged.** The entry notes that dropping only
the *resolved* guard (not in this spec) survives all 62 cases and is not
equivalent. Re-derived here: the resolved-guard-only mutant passes the whole
hermetic suite (`62/62 cases passed`, exit 0), and off-suite on a scanned
document with zero citations it flips the verdict line from `FAIL`/`DRIFT` to
`PASS`/`CLEAN` while the process exit stays 2 for both binaries
(`cite-check: fail-closed — zero resolved citations under …`). Confirmed;
that mutation belongs in a later spec, not in this round's table.

## 7. Findings

1. **The ninth-leg record is reproducible.** An independent sweep, with the
   pin materialized from kumitate's object store and the suite string taken
   verbatim from the frozen contract, reproduces all ten verdicts, all ten
   mutant hashes, all ten killing-case identities, the 5/10 kill rate and the
   10/10 prediction hold. Nothing in the committed table depends on the
   machine that produced it.
2. **The landed runner is consistent with the committed table.** The
   regression engine replays the ninth leg from the git-materialized pin at
   its recorded revision and gets `match=10/10`, `flips=0`; the whole
   nine-leg ledger is `PASS (cases=9 passed=9)`, twice in a row, and
   `mte-interop.py --check` reports `legs_conforming=9/9`.
3. **The recorded table is the right table.** The five survivors are four
   genuine suite holes (S_OOR_EDGE, S_STRICT, S_USAGE, S_PIN_INCLUDES — each
   falsified off-suite by an independent input here) and one equivalent
   mutant (S_EMPTY_GUARD — 124 differential runs, zero differences). A kill
   rate of 5/10 measured against a deliberately 5/5-composed spec is
   consistent, not suspicious.
4. **Small caveat on one companion command.** `mte-interop.py --check` pointed
   at a kept regression workdir without `--regression-stdout` reports
   `MTE_INTEROP: SETUP (…)` because it finds no `REGRESSION_TABLE` lines in
   the empty stdout it would otherwise read. The ledger itself is fine; the
   input shape is what the tool refuses. Worth a one-line note in the
   round-26 lesson so the next seat does not read that SETUP as a failure.
5. **No correction to the lane is needed** for the ninth leg: the sweep
   evidence, the runner wiring, the interop registry rows and the knowledge
   entry agree with an independent replay on every point this seat could
   measure.

## 8. Limits of this seat

- One host (Arch Linux, kernel 7.2.11-arch1-1), node v24.21.0, git 2.56.0,
  bash 5.3.20, python 3.14.8. The hermetic group only; the gate's
  integration group was never run.
- The oracle is the process exit status, as in the original measurement.
- The survivor falsifiers in §6 use the public CLI (`--src/--self/--fleet`),
  which is the same surface the lane's probes used; they were re-derived here
  from the replay's own mutant artifacts rather than copied from the probe
  reports, but they are not a second, independent mutation framework.
- The claim "the runner's sweep-mode code is unchanged between `622d31d` and
  `a08e85c`" was established by hashing the bodies of six named functions
  across the two revisions and by reading the full diff; it is not a formal
  equivalence proof of the whole script.

## 9. Bounds, tooling and files

- **No production file was edited.** No git write command (`add`, `commit`,
  `checkout`, `reset`, `stash`, `push`, `fetch`, `pull`) was run in
  `/home/vgpnk/Projects/shokunin/tameshi-shokunin`; only read-only git with
  `GIT_OPTIONAL_LOCKS=0` (`show`, `status`, `log`, `rev-parse`) and the
  clone's own checkout of a detached HEAD.
- **No `jj` command was run anywhere**, at the fleet root or in any clone.
- Sibling lanes were read only. `git -C kumitate-shokunin show <rev>:<path>`
  was the only kumitate access; the working trees of kumitate, kagi,
  tsukuroi and mado were never written.
- **No gate, selftest or sweep was run inside the lane tree.** Every
  execution happened in `/tmp/replicate-r26`, `/tmp/replicate-r26-fleet`,
  `/tmp/replicate-r26-sweep*`, `/tmp/replicate-r26-regression*` or the
  scratch dirs named inline.
- **Tooling: nothing was installed or upgraded by this seat.** No pacman
  transaction, no `uv tool install`, no release binary, no `cargo`/`npm -g`
  install; the tooling directive therefore has no install record here. The
  only package pull was the contract's own companion invocation
  `uv run --no-project --with jsonschema==4.25.1` (uv 0.13.0, PyPI,
  ephemeral environment — jsonschema 4.25.1, Python 3.15.0), needed because
  `jsonschema` is not present in the system interpreter. Pre-existing
  binaries used: node v24.21.0, git 2.56.0, bash 5.3.20, python3 3.14.8.
- **Files written by this seat:** this report only —
  `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-26/w1/ReplicateSweep.md`.
  All other artifacts live under `/tmp` scratch dirs.

REPLICATE SWEEP: REPRODUCED (10/10 verdicts, 10/10 mutant hashes, 10/10 predictions; regression PASS 9/9)

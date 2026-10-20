# QualityCriteriaReview — QUALITY 23–27 at `eb7838b` (round-17 w2, falsify)

Seat: TameshiR17.QualityCriteriaReview-2 (leaf, advisory; no delegation, no lane writes beyond this file).
Rev under review: `eb7838b16490ca7ba17ea3242ade76a61f744af2` (the w1 landing).
Criteria file: `corpus/QUALITY.md:127-158` (round-17 block; `corpus/README.md:19` points at `QUALITY.md`, so the
lessons' `QUALITY N` shorthand resolves).
Axes attacked: **A** checkability from the page, **B** every cited source resolves at the rev, **C** every
"shown able to fail"/red-before claim exists as committed evidence and reproduces.

Method: fleet-mirror clone at the rev, all execution inside it, scratch under `/tmp`:

```
W=$(mktemp -d /tmp/tameshi-r17w2-QualityCriteriaReview-2-XXXXXX); mkdir $W/fleet
for s in /home/vgpnk/Projects/shokunin/*-shokunin; do
  [ "$s" = /home/vgpnk/Projects/shokunin/tameshi-shokunin ] || ln -s "$s" $W/fleet/; done
git clone -q /home/vgpnk/Projects/shokunin/tameshi-shokunin $W/fleet/tameshi-shokunin
git -C $W/fleet/tameshi-shokunin checkout -q --detach eb7838b16490ca7ba17ea3242ade76a61f744af2
C=$W/fleet/tameshi-shokunin
```

No tool installs or upgrades were needed.

## Verdict table

| # | Criterion (short) | Checkable (A) | Sources resolve (B) | Red-before found / reproduces (C) | Verdict |
|---|---|---|---|---|---|
| 23 | input-keyed cold-read credit | yes, mechanic in `measure.py` | yes (§2, R16-C2b, S058/S059) | yes: `redbefore/measure-{e69b488,09ee1d0}.json`; reproduced exactly | **holds**, 2 minor gaps |
| 24 | run the pinned gate's registered command; re-pin/supersede; sweep | yes | yes (§3, R16-OP1, R16-C2a) | yes: `op1-redbefore-98bea7d.txt` (exit 2) | **holds**, 1 medium evidence gap + 1 minor |
| 25 | no-harm monitor runs every active registered command | yes | yes (§3, R16-MON1, V02, K04) | monitor shown failing at `98bea7d` (`c2-before`) | **holds**, executed green |
| 26 | stale receipt gets append-only dated correction | yes | yes (§6 item 5) | correction exists, original byte-identical | **holds**, 1 wording gap |
| 27 | every lane git-runner scrubs `GIT_*`; selftest canary | yes | yes (`lessons/round-17.md` row, S063) | runner canary holds; **two lane git-runners do not scrub** | **falls** (wrong expectation) |

## Criterion 23 — input-keyed credit

**What is checkable and true.** `measure.py` implements every clause: canonical lane-relative keys, `git ls-tree`
mode 100644/100755, `sha256(git cat-file blob REV:path)`, `input-drift`/`input-missing`/`input-not-blob`
(`.ufo/evidence/round-17/measure.py:315-345`); trace receipts must be committed blobs with schema
`tameshi-trace-inputs-v1` whose inputs are a subset with equal sha (`:361-410`); veto aggregation is
`covered = credited > 0 and not vetoes`, with stale entries excluded and unverifiable inputs vetoing
(`:572-582`). Sources resolve: `corpus/lessons/round-16-verifier-spotcheck.md:41` (§2), `:226` (routed R16-C2b),
`corpus/SOURCES.md:67` (S058, trace of input hashes) and `:68` (S059, cache key missing outside inputs).

**Red-before found and reproduced.** Both committed receipts exist at the landing:
`.ufo/evidence/round-17/redbefore/measure-e69b488.json` has the r14 bucket
`{"start":1563,"credited":true,"reason":"credited"}`; `measure-09ee1d0.json` has
`{"start":1563,"credited":false,"reason":"input-drift:tools/mutate-and-run.sh"}`. `redbefore/digest-diff.txt:20`
records `DRIFTED tools/mutate-and-run.sh 75ed934d… → 0673d2e5…`. I re-ran the same state:

```
python3 .ufo/evidence/round-17/measure.py --rev e69b488 --repo $C \
  --ledger-rev 09ee1d0:.ufo/evidence/round-16/coldread/ledger.json \
  --inputs-overlay .ufo/evidence/round-17/redbefore/legacy-r14-inputs.json
# exit 0; overrides True; trace_gate legacy; calibr 6; depth 6
# {"credited": true, "heading": "## Effective expectation reconciliation — round 14", "reason": "credited", "start": 1563, "vetoed": false}

# same command, --rev 09ee1d0
# exit 0; calibr 6; depth 7
# {"credited": false, "heading": "## Effective expectation reconciliation — round 14", "reason": "input-drift:tools/mutate-and-run.sh", "start": 1563, "vetoed": false}
```

**Gap 23a (minor, wording/consistency).** The criterion states, unqualified, "an entry that executed commands
must name committed trace receipts whose inputs it covers". The cited credited state is a legacy/override run:
both receipts carry `"overrides_used": true, "trace_gate": "legacy"`, and the r14 ledger entry has
`commands_executed_count: 4` with no `traces`. Under the strict rule (`measure.py:373`) that entry is
`traces-unrecorded` and cannot credit. The tool's own rule says "a claim must never use overrides"
(`measure.py:60-64`). The example demonstrates the input-drift leg correctly, but a reader applying the
criterion literally cannot obtain the credited pole. Fix: state that the red-before is a legacy measurement-aid
run, or attach a trace receipt to the overlay.

**Gap 23b (minor, reproducibility).** The receipts do not record the ledger rev or overlay path
(`ledger_source: "rev"`, `ledger_committed: false`, no path), so the exact invocation must be guessed; I
reconstructed it as above from the round-16 ledger + `legacy-r14-inputs.json`. Also the prose says "non-empty
`inputs`", while the tool exempts `SKILL.md` and the round-17 ledger path (`IGNORED_INPUTS`); an entry with only
those keys is prose-valid but tool-invalid.

## Criterion 24 — pinned instrument, registered command, re-pin/supersede, sweep

**Sources resolve.** `corpus/lessons/round-16-verifier-spotcheck.md:123-156` (§3) carries the operability harm and
the "by design holds for fail-closed, not for leaving it un-repinned" argument; `:216` is R16-OP1; `:222` is
R16-C2a. `.ufo/evidence/round-17/op1-redbefore-98bea7d.txt` is a committed red-before: exit 2,
`expected_input_digest_mismatch`, `tools/mutate-and-run.sh: observed 0673d2e5… expects 75ed934d…`.
The supersession exists: `.ufo/evidence/round-17/dispositions.json:4` has
`"supersedes": ".ufo/evidence/round-14/dispositions.json"`, and the registered row
`evidence-disposition-round17` returns 0 at the landing (my run below).

**Gap 24a (medium, evidence).** The landing commit itself edits the gate-pinned instrument
`tools/evidence-disposition.py` (the `_selftest_git_env` fix), but the only committed post-edit receipts are
**red**: `.ufo/evidence/round-17/registry-full-2a22ade.txt:13` `ROW evidence-disposition-selftest expect=0 got=1
differs`, `:30` `held=27/28`, exit 1; `.ufo/evidence/round-17/c2-after-2a22ade.txt:12` the same row, `:25`
`held=22/23`, exit 1. No committed receipt at `eb7838b` shows the registered row green at the landing; the
landing message asserts the monitor found the failure, but the criterion's "run before landing" outcome is not
in the repo. My re-run at the landing is green (`held=28/28`), so the rule's outcome is now true, but the round's
own evidence stops at the red. Fix: commit a `registry-check --rev eb7838b` receipt (or re-take the C2 after at
the landing).

**Gap 24b (minor, sweep).** "every mention of the old outcome is swept in that round": `SKILL.md:1601` still
carries the old command and the outcome cell `0 clean; 1 failed semantic expectations; …` for a command that now
returns 2 at `--root .`. The command cell is annotated `(historical; live entry since round 17: …)`, and
`SKILL.md:1681` is correctly annotated with the exit 2 and the live/frozen invocations; the recipe steps are
marked historical at `:1581-1584`. So the sweep is by annotation, and one outcome cell is untouched. Low impact,
but the criterion says "every mention".

## Criterion 25 — no-harm monitor scope

**Executed.** From the clone:

```
python3 tools/registry-check.py --rev eb7838b16490ca7ba17ea3242ade76a61f744af2 --json
# exit=0
ROW evidence-disposition-round17 expect=0 got=0 held
ROW evidence-disposition-round17-before expect=1 got=1 held
ROW evidence-disposition-round14-superseded superseded expect=0 got=2
ROW evidence-disposition-selftest expect=0 got=0 held
REGISTRY_CHECK: held=28/28 superseded=1
# JSON: rev_resolved=eb7838b…, root=/tmp/tameshi-registry-check-wjmi1fdz/fleet/tameshi-shokunin,
# registry_sha256=98bdc23ce4880fc3d23d169c38e36c2a9f2c69c273b936e868a7ddfd459e0630, live=false
```

Wall time 267 s. This exercises all row kinds (gate/probe/selftest), not just selftests; the superseded row
actually ran and reports `got=2`, and is counted only in `superseded=1`. The schema enforcement matches the
criterion: `status` must be `active|superseded` and `superseded_by` must name an existing **active** row
(`tools/registry-check.py:248-268`); `--rev` clones into `mkdtemp` and verifies the clone HEAD
(`:426-495`), so the lane is not written. The clone's HEAD stayed `eb7838b` and clean.

Sources resolve and support the rule: `V02ToolsNoHarmScope.md:4,51` (nine selftests only; `held = 10/11` at
`c699c8c`), `K04RegistrySelfFulfilling.md:61-73` (the demotion/skip hole that the criterion now closes);
`corpus/lessons/round-16-verifier-spotcheck.md:237` is R16-MON1. The monitor's ability to fail is committed:
`.ufo/evidence/round-17/c2-before-98bea7da…json` has `evidence-disposition-round17 got=2 differs`, `held=22/23`.

Residual risk (not a criterion defect): `expect` is hand-authored and the report only records
`registry_sha256`; it is never compared to a pinned value. An edited `expect` would green the row. The criterion
does not require a pin, but the "admitted outcome" is only as trustworthy as the registry bytes.

## Criterion 26 — stale receipt correction

**Verified record.** `.ufo/evidence/round-16/round-gate/runner-sha256.txt` at the landing is five lines:
line 1 is byte-identical to the `c699c8c` original (`89722ddb…  tools/mutate-and-run.sh`), and lines 2-5 are the
dated `2026-10-20` correction naming `c699c8c` for `89722ddb` and `05a2247, 09ee1d0, 017a2b0, 98bea7d` for
`0673d2e5…`. `git diff c699c8c eb7838b -- …/runner-sha256.txt` is a pure append (`@@ -1 +1,5 @@`, one context
line, four additions). Source resolves: `corpus/lessons/round-16-verifier-spotcheck.md:234` (R16-EV1, both
digests, "append a dated correction; do not rewrite the file").

**Gap 26a (minor, wording).** "in the round that finds it": the finding was routed by the round-16 verifier
spot-check (R16-EV1) and the correction is dated/committed in round 17 (2a22ade). The cited example therefore
spans rounds — "found" by round 16's closure, "received" by round 17. Clarify to "the round that receives the
routed finding", or the criterion is self-contradicted by its own example.

## Criterion 27 — every lane git-runner scrubs `GIT_*` — FALLS

The criterion is checkable (grep every `git` invocation, then export a canary `GIT_DIR` and run the selftest), and
both citations resolve: `corpus/lessons/round-17.md:57` (the 12:29:33 incident: live HEAD moved to `e16adb7`,
index rewritten; repair reflog), `corpus/SOURCES.md:72` (S063: "an inherited GIT_DIR redirects every `git -C`").
The incident is also in `.ufo/waves/round-17/w1/N01TraceGitSafety.md:18` and `R01R16Debts.md:51`.

**The universal claim is false at `eb7838b`.** Two committed lane git-runners do not scrub:

1. `tools/bash-witness-study.py:337-341` — `subprocess.run(["git","-C",str(kagi),"show","--end-of-options",
   f"{rev}:{TARGET_GIT_PATH}"], capture_output=True, check=False)` has **no `env=`**; the inherited environment
   is passed through. There is no `GIT_` handling and no canary arm in its selftest. Minimal reproduction of the
   call shape (read-only, throwaway canary):

   ```
   GIT_DIR=$W/canaryB/.git git -C $C show HEAD:SKILL.md
   # fatal: path 'SKILL.md' exists on disk, but not in 'HEAD'
   #   -> the inherited GIT_DIR made `git -C $C` read the canary's HEAD
   env -u GIT_DIR -u GIT_WORK_TREE git -C $C show HEAD:SKILL.md
   # ---   (lane bytes, correct)
   ```

2. `.ufo/evidence/round-17/jj/head-vs-branch.sh:79-83` — the comment claims "no host hooks, templates,
   global/system config, or inherited `GIT_*` state leaks into the fixture repo", but the code only sets
   `GIT_CONFIG_NOSYSTEM`, `GIT_CONFIG_GLOBAL`, `GIT_TERMINAL_PROMPT` and identity. It never unsets
   `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE`. Demonstrated:

   ```
   # canary repo at $W/canaryB, HEAD=6ef6578
   GIT_DIR=$W/canaryB/.git bash .ufo/evidence/round-17/jj/head-vs-branch.sh tools/pin-disposition.py
   # fixture exit=2
   # warning: re-init: ignored --initial-branch=master
   # fatal: git checkout: --detach does not take a path argument 'master'
   # SETUP-FAIL: detach failed
   # canaryB HEAD after: 06b6267 "v1: master tip"   (moved)
   # canaryB status: " D corpus/surface-census.sh" and "?? marker"
   ```

   Positive control, same canary shape: `GIT_DIR=$W/canaryA/.git bash tools/mutate-and-run.sh --selftest` →
   exit 0, `MUTATE_SELFTEST: 95/95 pass`, canaryA HEAD unchanged (`6ef6578`). So the runner's `git_clean()`
   canary arm (`tools/mutate-and-run.sh:1724-1749`) holds; the criterion's "every" does not.

**The canary-proof clause is also only partially implemented.** "its selftest proves it with a canary repository
named by an exported `GIT_DIR` that must stay unchanged" is satisfied by:
`tools/mutate-and-run.sh:1724-1749` (verified above), `tools/registry-check.py:711-760` (canary HEAD/refs/status),
and `.ufo/evidence/round-17/coldread/assemble.py:1442-1445` ("decoy repo untouched").
It is not satisfied by `tools/evidence-disposition.py` (`_setup_gitdir_env` at `:2045-2056` exports `GIT_DIR`
to a foreign repo, but the `v2-gitdir-env` case at `:2580-2594` asserts only the tool's exit/findings, never the
foreign repo's HEAD/status), `tools/pin-disposition.py` (no exported-`GIT_DIR` decoy in its selftest),
`.ufo/evidence/round-17/measure.py:1283-1286` (`GIT_DIR=/nonexistent`, a poison path, not a canary repo), and
`.ufo/evidence/round-17/coldread/trace-inputs.py:891-898` (bogus `GIT_DIR`; checks env removal, not canary
bytes). The runner's 89/95 unscrubbed-mutant red is documented only in a seat report,
`.ufo/waves/round-17/w1/X05RunnerRepoGuard.md:141` ("`89/95 pass`; exactly the 6 scrub assertions FAIL…canary log
gains `selftest-leak`"), not in a machine receipt.

**Repair options.** (i) Scrub both counterexamples and add canary arms (small: pass a scrubbed `env=` in
`materialize_target`; `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE` plus a canary check in the jj fixture), or
(ii) narrow the criterion to the instruments edited this round and name the remaining git-runners as debt — the
criterion must not say "Every" while two committed runners violate it.

## Red-before index (what exists, where)

| Claim | Committed artifact | Reproduced? |
|---|---|---|
| r14 bucket credited → uncredited on input drift (Q23) | `redbefore/measure-e69b488.json`, `measure-09ee1d0.json`, `redbefore/digest-diff.txt:20` | yes, exact fields |
| pinned gate red at 98bea7d (Q24) | `op1-redbefore-98bea7d.txt` (exit 2) | yes, read; landing gate now 0 |
| monitor fails the harm it missed (Q25) | `c2-before-98bea7da…json` (`held=22/23`, disposition row differs) | yes, read |
| stale receipt corrected append-only (Q26) | `runner-sha256.txt:1-5`; `git diff c699c8c eb7838b` | yes |
| unscrubbed runner mutant (Q27) | `w1/X05RunnerRepoGuard.md:141` (report only) | not re-run; positive control run instead |
| jj fixture leak (Q27) | none — **I produced it** with a throwaway canary | yes, canary HEAD moved |

## Commands, exits, key lines

| Command (cwd = clone root unless noted) | Exit | Key output |
|---|---|---|
| clone + `checkout --detach eb7838b` | 0 | `OK`; HEAD `eb7838b` |
| `python3 tools/registry-check.py --rev eb7838b --json` | 0 | `REGISTRY_CHECK: held=28/28 superseded=1`; 267 s |
| `measure.py --rev e69b488 … --ledger-rev 09ee1d0:…/round-16/coldread/ledger.json --inputs-overlay …/legacy-r14-inputs.json` | 0 | r14 `credited: true` |
| same, `--rev 09ee1d0` | 0 | r14 `credited: false`, `input-drift:tools/mutate-and-run.sh` |
| `GIT_DIR=canaryA/.git bash tools/mutate-and-run.sh --selftest` | 0 | `MUTATE_SELFTEST: 95/95 pass`; canary HEAD unchanged |
| `GIT_DIR=canaryB/.git bash .ufo/evidence/round-17/jj/head-vs-branch.sh tools/pin-disposition.py` | 2 | `SETUP-FAIL: detach failed`; canary HEAD `6ef6578→06b6267` |
| `GIT_DIR=canaryB/.git git -C $C show HEAD:SKILL.md` | 128 | `path 'SKILL.md' … not in 'HEAD'` (read redirected) |
| `git diff c699c8c eb7838b -- …/runner-sha256.txt` | 0 | `@@ -1 +1,5 @@`, pure append |

## Residual risk / verification gaps

- The `registry-check` run grades exits and `stdout_contains` only; I did not independently re-derive the
  semantic correctness of every row's expectation (the tool's own rows do that). Of the two `external` rows,
  `pin-disposition-read` reads the live fleet root `/home/vgpnk/Projects/shokunin` and `verify-round15` runs
  clone-local; I did not audit the live siblings' contents.
- I did not re-run the 89/95 unscrubbed-runner mutant from `X05RunnerRepoGuard.md`; I ran the positive control
  (exported `GIT_DIR`, canary unchanged) and relied on the committed seat report for the mutant.
- Criterion 23's reproduced red-before uses the round-16 ledger at `09ee1d0`; the receipt does not name that
  ledger, so a different ledger rev could produce a different entry set. The r14 entry I matched is identical to
  `redbefore/legacy-r14-inputs.json` (`start 1563`, `skill_sha256 97cf436b…`).
- The live lane's post-incident HEAD/index state is out of scope; I did not touch the lane repo except reading it.

## Verdict

**QUALITY 23–26 hold** — each is mechanically checkable, every cited source resolves at `eb7838b`, and the
red-before records exist (23 reproduced exactly; 24's is `op1-redbefore-98bea7d.txt`; 25 executed
`held=28/28`; 26's correction is a byte-identical append) — with minor gaps: 23's credited pole is a
legacy/override run that violates its own unqualified trace clause and the receipt names no ledger; 24 has no
committed post-landing green receipt for the pinned selftest and `SKILL.md:1601` keeps the old outcome cell;
26 says "the round that finds it" for a cross-round finding. **QUALITY 27 falls at this rev**: two committed
lane git-runners (`tools/bash-witness-study.py:337-341`, `.ufo/evidence/round-17/jj/head-vs-branch.sh:79-83`) do
not scrub inherited `GIT_*`, and I moved a throwaway canary HEAD with the committed jj fixture; the
canary-unchanged proof exists for only three of the git-running artifacts (runner, registry-check, assemble).

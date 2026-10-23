CONTROL CtlS1Normalize: v3_meets=true built=yes

Verdict: the public v3 counter accepts this static normalizer without the replacement detector ever running, sourcing or evaluating the tally block. The single explicit mutation probe was KILLED, with a passing baseline and exact restoration. The sealed v4 result is unmeasured by this seat.

## Deliverables and axes

- Axis: C1 operability. Control objectives: public-counter acceptance, tolerance of equivalent spellings, and retention of the frozen tally bytes. No change to the contract is proposed.
- Commit: `07a1fa29738eb926fc894ae4b6dcbe392682d35d`.
- Clone: `/fast/scratch/hyaku/tameshi-r30a2-seats/CtlS1Normalize/clone`.
- Diff: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/wA/CtlS1Normalize.diff`.
- Final runner SHA-256: `03be2092dc27a5df457192374b6bc71d1f39d8fc787941a41d8f86f34a4b6109`.
- Final tally SHA-256: `e163133c0f54bb0cbd1c3f123e18b5efc17ced6df4558de034575089a8a2215d`.

## Implementation evidence

All code changes are in the clone's `tools/mutate-and-run.sh`. The frozen tally remains at lines 1430–1468. The replacement detector starts at line 1987; its Python entry starts at line 1990. Only the frozen fix's behavioral selftest hunk was replaced after applying `witness/fix.diff`.

The detector parses shell structure as data. It compares the resulting normal form with the normal form of a compressed copy of the frozen tally. Arithmetic expressions are parsed with `ast.parse`, not evaluated with Python `eval` or executed as shell code. The detector has no subprocess, shell sourcing, tally harness or runtime-status enumeration.

Its normalization covers comments, whitespace, continuation lines, status-operand order, case-arm order and singleton bracket patterns, quoted words, arithmetic operand order, polynomial cancellation and constant folding, assignment and compound-assignment spellings, prefix/postfix increments, zero updates, literal colon no-ops, and integer test spellings including `-gt 0`, `!= 0`, arithmetic truth and `-ge 1`. Unsupported syntax is refused rather than executed. This is a static syntax shortcut, not a claim to decide arbitrary shell equivalence.

Clone preparation, observed exit 0 with no output:

```sh
mkdir -p /fast/scratch/hyaku/tameshi-r30a2-seats/CtlS1Normalize && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout -k 5 120 git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r30a2-seats/CtlS1Normalize/clone && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r30a2-seats/CtlS1Normalize/clone checkout -q --detach f09d3425258403a51422c9959e25340807982947 && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r30a2-seats/CtlS1Normalize/clone apply /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/witness/fix.diff
```

The fix before replacing its selftest had runner SHA-256 `9a931bc2d0c31c32dd3a4ccf6594b56c3474628cca513b675901a8666fbec7d4` and the required tally hash above.

Commit and export, run from the clone, observed exit 0:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git add tools/mutate-and-run.sh && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -c user.name='CtlS1Normalize' -c user.email='ctl-s1-normalize@local.invalid' commit -q -m 'r30 control: compare static tally normal forms without running tally' && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git rev-parse HEAD && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git diff --output=/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/wA/CtlS1Normalize.diff f09d3425258403a51422c9959e25340807982947 HEAD -- tools/mutate-and-run.sh
```

Observed stdout:

```text
07a1fa29738eb926fc894ae4b6dcbe392682d35d
```

## Public v3 measurement

Exact command, run from the clone:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/tameshi-r30a2-seats/CtlS1Normalize timeout -k 5 1500 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/c1-measure-v3.py --repo /fast/scratch/hyaku/tameshi-r30a2-seats/CtlS1Normalize/clone --rev 07a1fa29738eb926fc894ae4b6dcbe392682d35d --jobs 4
```

Observed summary:

```text
C1_R30: rev=07a1fa29738eb926fc894ae4b6dcbe392682d35d pristine_selftest=1 harness=19/19 refused_drops=9/9 killed=13/13 equiv_pass=4/4 heldout_killed=12/12 heldout_equiv=4/4 insert_killed=8/8 insert_equiv=4/4
PREDICATE: C1_R30_PASS=true
exit=0
```

The row output reported pristine `selftest_exit=0 verdict_pass=1`; every named mutant row had `selftest_exit=1 verdict_pass=0`; every equivalent-rewrite row had `selftest_exit=0 verdict_pass=1`. The public counter itself executes its required behavioral harness; the installed replacement detector does not.

## One explicit mutation probe and restoration

Mutant: change only the successful-status arm at clone `tools/mutate-and-run.sh:1433` from `npass=$((npass + 1))` to `npass=$((npass + 0))`. This plausible one-character defect stops successful legs increasing the pass count. Expected detector: the static canonical-form comparison must reject the missing update.

The identical bounded command below was run on pristine, mutated and restored bytes, from the clone:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout -k 5 30 python3 -c 'import hashlib,pathlib,subprocess,sys; p=pathlib.Path("tools/mutate-and-run.sh"); raw=p.read_bytes(); text=raw.decode(); s=text.index("  local nlegs=9 npass=0 nfail=0 nsetup=0 st\n"); e=text.index("\n}\n",s); print("runner_sha256="+hashlib.sha256(raw).hexdigest()); print("tally_sha256="+hashlib.sha256(text[s:e+1].encode()).hexdigest()); code=text.split("<<\x27R30_STATIC\x27\n",1)[1].split("\nR30_STATIC\n",1)[0]; r=subprocess.run([sys.executable,"-",str(p)],input=code,text=True,capture_output=True,timeout=20); print(r.stdout,end=""); print(r.stderr,end=""); print("detector_exit="+str(r.returncode)); sys.exit(r.returncode)'
```

Pristine observed output, exit 0:

```text
runner_sha256=03be2092dc27a5df457192374b6bc71d1f39d8fc787941a41d8f86f34a4b6109
tally_sha256=e163133c0f54bb0cbd1c3f123e18b5efc17ced6df4558de034575089a8a2215d
STATIC_TALLY: MATCH
detector_exit=0
```

Mutated observed output, exit 1:

```text
runner_sha256=9d5ea2e67a832bd59039cb82969fdd069700866f4af66c43025f750649899094
tally_sha256=13b87f1db7bccf7a3061528e94395eade5cc7da8d49c8f6e38f08b660b353300
STATIC_TALLY: DIFFERENT
detector_exit=1
```

Restored observed output, exit 0:

```text
runner_sha256=03be2092dc27a5df457192374b6bc71d1f39d8fc787941a41d8f86f34a4b6109
tally_sha256=e163133c0f54bb0cbd1c3f123e18b5efc17ced6df4558de034575089a8a2215d
STATIC_TALLY: MATCH
detector_exit=0
```

Verdict: KILLED. Both complete-runner and tally hashes before and after restoration match. The mutation was restored before committing and measuring v3.

## Smallest safe correction and bounds

Keep the frozen fix's behavioral selftest for the actual implementation; do not substitute this control for it. L1 can measure the unchanged control commit under frozen v4. Public v3 acceptance alone does not establish that a detector exercises the claimed behavior. No contract change is requested.

No sealed directory was opened, listed, searched or read. No production source or sibling source was edited. Git writes were confined to this clone; the only lane artifacts written were this report and the named diff. No subagents, other agent runtimes or model calls were invoked. Tool installs or updates: none. All started foreground commands completed; no background job or service was started, and no manual process kill was issued.

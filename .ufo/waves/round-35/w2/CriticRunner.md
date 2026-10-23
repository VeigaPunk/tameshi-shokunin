# CriticRunner — immutable bytes are not a general no-harm certificate

Seat: `L1tameshi35.CriticRunner`; round 35, wave 2. Reviewed dispatch revision `7da6e076c2e25936a3b60dde2a4080d8f05b7e5b` against base `51d3f08073be65d3475cf0286042fc0dbe4c4a7d`.

## Axes and result

- **Calibration:** distinguish an observed unchanged input from an unmeasured no-harm conclusion.
- **Depth / operability:** distinguish `(exit, FULL stdout)` equivalence from actual workdir cleanup.
- **CRITICAL:** none established by this slice against literal runner immutability or the frozen C1 predicate.
- **BOUND:** none asserted; the cleanup omission below is not fail-closed and must not be mislabeled as such.
- **HYGIENE H1:** the proposed implication “runner never edited, therefore no harm” is too strong. A cleanup-leaking copy receives the same audit PASS as pristine while the canonical runner remains byte-identical. This is an observation-scope counterexample, **not** a must-kill specimen under C1's expressly tuple-only definition.

The frozen contract does not itself say that a matching runner hash proves universal no harm. The criticism targets that additional interpretation, not an invented broader C1 acceptance criterion.

## Scope and provenance

Read the required contract/A4/A5, both inherited wave-1 reports, round-34 Holds, and v3 docstring before probing. All executable review inputs were then fetched from the exact dispatch revision, not a moving working tree.

Setup adaptation: used read-only Git object reads instead of the requested clone/checkout, because the inherited bounds prohibit mutating Git commands and writing inside `.git`. Non-Git scratch is `/fast/scratch/hyaku/tameshi-r35-w2/CriticRunner/`, the inherited scratch root. Only this report was written in the lane. Real-auto-root probes necessarily used the runner's specified `/tmp/tameshi-r4-2-regression.XXXXXX` template; their directories were cleaned afterward. No runner, tool, counter, panel, sealed set, or Git metadata was edited. No default-mode C1 measurement or C2 count was invoked. No tools were installed or upgraded; no pacman, runtime orchestration, judging, admission, or integration was performed.

## 1. What I could not break: the immutability premise

### Base, tip, and intervening committed states

Exact endpoint commands, each with `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` unset:

```bash
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE /usr/bin/git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 51d3f08073be65d3475cf0286042fc0dbe4c4a7d:tools/mutate-and-run.sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE /usr/bin/git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b:tools/mutate-and-run.sh
```

Both exit **0**, stderr empty, stdout **106,538 bytes**. Direct byte comparison was equal; both SHA256 values are:

```text
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9
```

This equals `frozen_artifacts.runner_sha256` in the contract fetched at the dispatch revision. Evidence: `/fast/scratch/hyaku/tameshi-r35-w2/CriticRunner/identity.json`, SHA256 `b5c644d4499b1f179437f9c23d22436351ce537b4ef72b43ccfc15410347b492`.

To exclude an intervening committed edit/revert, also ran, with the same Git environment scrub:

```bash
/usr/bin/git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin merge-base --is-ancestor 51d3f08073be65d3475cf0286042fc0dbe4c4a7d 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b
/usr/bin/git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin log --full-history --format=%H 51d3f08073be65d3475cf0286042fc0dbe4c4a7d..7da6e076c2e25936a3b60dde2a4080d8f05b7e5b -- tools/mutate-and-run.sh
/usr/bin/git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-list 51d3f08073be65d3475cf0286042fc0dbe4c4a7d..7da6e076c2e25936a3b60dde2a4080d8f05b7e5b
```

All exit **0**; the path history is empty. The range contains five revisions: `d16f9b5a18945ede3852ec3df7eb4ee4b0afbafc`, `43aea0305ba4af19b634ee115e769a91ea99fbc9`, `72677381eb8f24456f03ea9cee0af374688eb6b6`, `23bd903a03c6b5311c5be46a3c2d51ec896e8b07`, and the dispatch tip. Each runner blob was independently fetched with `git show`; every command exited **0** and every blob had the same 106,538-byte size and runner SHA above. Exact per-revision commands: `/fast/scratch/hyaku/tameshi-r35-w2/CriticRunner/history-identities.json`, SHA256 `bfc04819f28247877bc8798a0998aaacd2818e1fa122aef4f4e67fbc332e476e`.

This establishes unchanged committed runner bytes over the specified range, not an observation of every transient uncommitted state or a prediction about a later measurement revision.

### All four configurations and audit execution

Ran:

```bash
/usr/bin/python3 /fast/scratch/hyaku/tameshi-r35-w2/CriticRunner/runner-probe.py matrix
```

Exit **0**. Independent extraction of the pinned runner's literal tally block; no tool import or tool verdict used as ground truth. Seven vectors per config: all-zero, one-1, one-2, one-3, one-255, `[1,2,0,0,0,0,0,0,0]`, and `[0,3,0,255,0,0,0,0,0]`. Direct subprocess capture retained raw stdout bytes, including final newlines. Auto roots came from `/usr/bin/mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX`, exit **0**; explicit root literals were the frozen tool's exact representatives, confined by cwd to scratch.

| auto | KEEP | Canonical runner SHA before/after | Pristine/copy raw tuples equal |
|---:|---:|---|---:|
| 1 | 0 | pinned / pinned | 7/7 |
| 1 | 1 | pinned / pinned | 7/7 |
| 0 | 1 | pinned / pinned | 7/7 |
| 0 | 0 | pinned / pinned | 7/7 |

Evidence, including every generated Bash command, driver SHA, cwd, environment, exit, full stdout hex/hash, and filesystem observation: `/fast/scratch/hyaku/tameshi-r35-w2/CriticRunner/matrix.json`, SHA256 `57ffd268a5ba47d6197f4d8781348d34f385ba60fb413bfe4bea05e9443d0f67`.

The complete pinned v3 audit of pristine also exited **0**: `head PASS`, `static PASS`, `runtime PASS vectors=30316 mismatched=0`, `harness PASS reference cases=9; faults rejected=34/34`. Its receipt records the canonical runner hash unchanged before/after. This is a real audit run, not a full nine-leg fleet regression.

## 2. Counterexample: stdout says removed, directory remains

The runner's pinned cleanup operation is at `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh:1464-1469`. Authored only a new scratch copy, changing its tally cleanup line from:

```bash
    rm -rf "$root"
```

to:

```bash
    : # probe: preserve the auto workdir while printing the original tuple
```

The copy SHA256 is `10b5b917fe37381d435ff81e8457f48bbd055e02a32b21370544070e6871aa26`; pristine remains `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`.

Two independent full audits were run concurrently through these capture commands, both exit **0**:

```bash
/usr/bin/python3 /fast/scratch/hyaku/tameshi-r35-w2/CriticRunner/runner-probe.py audit pristine
/usr/bin/python3 /fast/scratch/hyaku/tameshi-r35-w2/CriticRunner/runner-probe.py audit cleanup-leak
```

The exact tool subprocess commands, each exit **0**, were:

```bash
/usr/bin/python3 /fast/scratch/hyaku/tameshi-r35-w2/CriticRunner/tally-audit-v3.py --runner /fast/scratch/hyaku/tameshi-r35-w2/CriticRunner/pristine-runner.sh
/usr/bin/python3 /fast/scratch/hyaku/tameshi-r35-w2/CriticRunner/tally-audit-v3.py --runner /fast/scratch/hyaku/tameshi-r35-w2/CriticRunner/cleanup-leak-runner.sh
```

Both produced these identical complete stdout bytes:

```text
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=30316 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=34/34
TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)
```

Both stdout SHA256 values: `46746e2b4740813443caccb89d80a96ae0c63d98f1def6b1fc3886d57c4e4e82`; stderr empty. Commands, environments, identities, and exit codes are in:

- `/fast/scratch/hyaku/tameshi-r35-w2/CriticRunner/audit-pristine.json`, SHA256 `b7fdd878e90568a65e214371337cd47636a78ad6bd02d8046b2ea7124c0dde12`.
- `/fast/scratch/hyaku/tameshi-r35-w2/CriticRunner/audit-cleanup-leak.json`, SHA256 `dfcbb3c75f7d43b4c2f34e8fa94b30e73e94ecf5a1c531a9137917be6d2a0bbd`.

The independent matrix found exactly one filesystem difference, at `(auto,KEEP)=(1,0)`, all-zero statuses. Both direct Bash drivers exited **0** and produced identical raw stdout:

```text
REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)
REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.TnfYHB (removed on PASS; --keep retains)
```

Raw stdout SHA256: `7e7668e6b6f1d3fc701ad9f0557186ac599ef80d02f0ecc95248db9096cf988d`.

| Observation | Pristine | Cleanup-leak copy |
|---|---|---|
| root exists after execution | false | **true** |
| sentinel exists after execution | false | **true** |

Retained sentinel SHA256: `1286fd41e5f5bfe9dc19e8ff6724ce01510ba9d0ac7ce74d855bd71abb8a86eb`.

Exact direct commands, both exit **0**:

```bash
/usr/bin/bash /fast/scratch/hyaku/tameshi-r35-w2/CriticRunner/matrix-auto1-keep0/all-zero-pristine.sh
/usr/bin/bash /fast/scratch/hyaku/tameshi-r35-w2/CriticRunner/matrix-auto1-keep0/all-zero-cleanup-leak.sh
```

Their cwd/environment and source hashes are preserved in `matrix.json` above; driver SHA256 values respectively `482eeb465bbd81ec1c08cea2bbcafd8ba15daf05910de25a8e22bdf7134957c5` and `baa42dd1aed3338494e3a9de08e0ccde3ccf711944de00711fdba236cad844f7`.

### Calibration: why this is not a C1 falsifier

The frozen contract at `/fast/scratch/hyaku/tameshi-r35-w2/CriticRunner/contract.json` defines the ground-truth observation as exit plus full stdout; `/fast/scratch/hyaku/tameshi-r35-w2/CriticRunner/c1-measure.py:285-317` labels copies on that same observation. The cleanup-leaking copy changes neither stdout nor exit in any branch or tested vector; its changed command is followed by the original unconditional `exit 0`. It therefore belongs on the **accept** side of that frozen observation model. Calling it a valid kill specimen would silently change the contract.

The evidence refutes broader cleanup/no-harm certification, not the finite panel claim. It does not show that the canonical runner actually leaked, that v3 introduced a regression relative to v2, or that any other axis was measured harmed. The immutable canonical runner's observed cleanup behaved correctly on this vector. No production fleet regression, general sandbox-safety test, sealed-provenance bypass, or C2 after-state was claimed.

## 3. Smallest safe correction

For this frozen round, keep the byte pin and narrow the conclusion: **“The canonical runner bytes are unchanged; this audit compares exit and stdout, not filesystem effects or universal no harm.”** Do not amend frozen artifacts or relabel this specimen as kill after observing it.

If actual cleanup correctness is later claimed, a new pre-data contract can add the independently observed workdir/sentinel existence to the tuple. Until then, the canonical judge must not treat runner identity alone as proof of unchanged operability or of no harm on every axis. No source change was made by this seat.

## Evidence identities and limits

Pinned snapshots used throughout:

- Tool SHA256: `ef98fc5367cdb12c71b8b0ddfb5b83835100831f545f6510437dc84014865885`.
- Counter SHA256: `515b0b1b00b970f31c08e80eb74512ecae0cf1082ddeccfcb373e810cd0559e8`.
- Contract SHA256: `a9eb2b97226ad192352f9da8cc32f3f719db22a93f14355a5e2d1306cea027c0`.
- Probe `/fast/scratch/hyaku/tameshi-r35-w2/CriticRunner/runner-probe.py`, SHA256 `0a23b1052288fe0eafed2169453289be0b1ae19b84657baa171dc564f09c3d67`.
- Exact snapshot `git show` commands and exit codes: `/fast/scratch/hyaku/tameshi-r35-w2/CriticRunner/snapshot-identities.json`, SHA256 `730b32200a7c46389d3515ee3d2b90d04c65f6c9592ab1e3712174d681170fe0`.

Hash receipts were computed with `sha256sum` and Python `hashlib.sha256`; successful command exits were **0**. Toolchain observed with `--version`: Python 3.14.8, Bash 5.3.20, Git 2.56.0, GNU coreutils 9.12. No installation/update channel applies.

**Bounded negative:** unchanged runner bytes survived endpoint comparison, every intervening committed state, all four configuration probes, and both full audit executions. No global “never edited” or “no harm” conclusion beyond those observations is asserted.

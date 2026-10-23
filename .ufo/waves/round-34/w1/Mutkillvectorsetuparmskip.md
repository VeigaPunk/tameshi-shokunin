# Mutkillvectorsetuparmskip — round-34 w1 (v2 wave), mutation seat

Seat: `tameshi-r34-w1-Mutkillvectorsetuparmskip`. Assigned probe: sealed kill copy
`ho-kill-vector-setup-arm-skip.json` (set=kill), plus an adversarial construction of the same
fault family against the amended witness gate (`ho_witness_ok`, amendment 6) and the frozen tool.
Lane tip at dispatch: `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`. Measurement rev:
`c17e593b51802dd4ed568da3265f21c6d00c4273`. All work in
`/fast/scratch/hyaku/tameshi-r34-seats/Mutkillvectorsetuparmskip/` (below `$S`); the lane is
read-only and was never written.

## 1. Setup and pins (verified before any run)

```
mkdir -p $S && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
  git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin $S/lane   # rc=0 (clone.rc)
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
  git -C $S/lane checkout -q --detach 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7          # rc=0 (checkout.rc)
git -C $S/lane show 0b99d48...:tools/tally-audit-v2.py > $S/tool.py                     # rc=0 (tool.extract.rc)
git -C $S/lane show 0b99d48...:tools/mutate-and-run.sh > $S/pristine.sh                 # rc=0 (runner.extract.rc)
sha256sum $S/tool.py $S/pristine.sh                                                     # pins.sha
```

| artifact | sha256 observed | pin / expectation | match |
|---|---|---|---|
| `$S/tool.py` (tip blob) | `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` | same (frozen) | yes |
| `$S/pristine.sh` (tip blob) | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | same (frozen) | yes |
| counter `$S/lane/.ufo/evidence/round-33/c1/c1-measure.py` | `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` | amendment-6 pin `f6b8868c…a07f28c` | yes |
| sealed JSON at `c17e593b` (= fleet working tree = tip) | `633ba5b68b77833f5504c05fb55b17db3b69ca56758f83755612aaaf34113e90` | unchanged; never written | — |

`git -C $S/lane rev-parse HEAD` → `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`;
`git -C $S/lane status --porcelain | wc -l` → `0`. The tool and runner blobs are byte-identical
at `c17e593b` and at the tip, so the probe is measured against the same pinned bytes as the
deciding run. No tools were installed or upgraded.

## 2. Detector (identical on pristine, mutated, restored)

The counter is imported as a module from the lane path and only its functions are called on
scratch copies (no default-mode run; the kill rule is not used). Detector:
`c1r33.run_tool_sandboxed(tool, copy, work)` over the frozen tool — **KILL** iff `rc==1` and the
last `TALLY_AUDIT:` line starts `FAIL`; **ACCEPT** iff `rc==0` and it starts `PASS`. Witness
detector: `c1r33.ho_witness_ok(ho, pristine_text, mutated_text, work)` plus
`c1r33.block_run(block, vector, work)` (real bwrap boundary). Baseline on the pinned runner:
`ACCEPT rc=0 TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)`.

## 3. Assigned sealed copy — label KILL — **KILLED**

Edit (each `old` occurs exactly once; `pristine.count(old)==1`):
`"      *) nsetup=$((nsetup + 1)) ;;\n"` → `"      *) : ;;\n"`.

- `validate_ho` passes; mutated runner differs; mutant sha
  `2fd82958320465661c1ce856bd1d69fd66311b88950b733de2290e5dead09a03`.
- `ho_witness_ok = True ('vector')` for witness `[2,0,0,0,0,0,0,0,0]`.
- Witness run (`block_run`):
  pristine `(2, 'REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)')`;
  mutant `(2, 'REGRESSION: SETUP (case-tally mismatch: cases=9 counted=8)')` — the setup leg is
  dropped and the sum guard reports the undercount.
- Real tool on the copy: `outcome=KILL rc=1 last='TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)'`.
  Full check detail: `CHECK runtime FAIL vectors=15158 mismatched=14994; first: cfg(0,1) statuses
  2 0 0 0 0 0 0 0 0: got (2, '… case-tally mismatch: cases=9 counted=8'), want (2, '… passed=8
  cannot-verify=1')`. The first mismatch is exactly the witness vector, so the fault is inside the
  tool's panel and detected under the audited config.
- Pristine baseline through the same detector: `ACCEPT rc=0` (above).

Verdict on the assigned copy: **KILLED**, matching its label. The landed C1 receipt
(`C1_R33: … C1_R33_PASS=true`, exit 0, `.ufo/evidence/round-34/measure/`) is not contradicted by
this seat.

## 4. Adversarial probe — **FINDING (critical): the witness gate and the tool sample different configurations**

### 4.1 Mechanism (all frozen, no reimplementation)

- The counter's witness runner `block_run` (`c1-measure.py:154-182`) hardcodes the tally
  configuration `local root=r auto=0 KEEP=1` (`c1-measure.py:167`) and runs under bwrap with
  `HOME=/w`, `TMPDIR=/tmp`, cwd `/w` (bound run dir).
- The amended vector branch of `ho_witness_ok` (`c1-measure.py:184-218`; accept at :215, kill at
  :218) accepts a kill when `a != b` and an accept when `a == b and mutated != pristine`, where
  `a,b` are `block_run` results — i.e. always under `root=r auto=0 KEEP=1`.
- The tool's runtime sweep uses `CONFIGS = (('tally-audit','0','1'), ('/tmp/tally-audit-work','1','0'))`
  (`tool.py:265`); `run_vectors` injects `local root=%s auto=%s KEEP=%s` (`tool.py:279`) and
  its `bash` helper overrides `HOME`/`TMPDIR` with the sweep's temp dir (`tool.py:257`);
  `check_runtime`
  (`tool.py:372`) compares 15,158 vectors against the oracle under both configs.
- Neither audited root equals `r`; config `(0,1)` matches `block_run` on `auto`/`KEEP` but not
  `root`. `HOME`, `TMPDIR` and `PWD` also differ between the witness run and `run_vectors`.

Both sides run the same block text on the same vector inputs, so for this family's edits — which
behave uniformly across statuses and positions — the only inputs that can make a mutation visible
to one side and invisible to the other are the configuration/environment values above. (A
vector-selective mutation is a separate panel-coverage gap, recorded by the sibling threshold seat;
the sealed copy's first mismatch here is the witness vector itself, §3.) The gate therefore
validates copies whose witness-set label is opposite to the tool's verdict in both directions.

### 4.2 Kill-labelled gate-valid copy the tool ACCEPTs (false must-kill)

Exact JSON (`$S/adv-kill-root-keyed.json`, sha
`b2074bfbf02f97a34e3e129d522b6284f41f9f548705a692ec52a13ecf136980`):

```json
{
 "id": "adv-kill-root-keyed",
 "author": "tameshi-r34 Mutkillvectorsetuparmskip",
 "set": "kill",
 "edits": [
  {
   "old": "      *) nsetup=$((nsetup + 1)) ;;\n",
   "new": "      *) [[ $root == r ]] || nsetup=$((nsetup + 1)) ;;\n"
  }
 ],
 "witness": {
  "vector": [2, 0, 0, 0, 0, 0, 0, 0, 0]
 }
}
```

Same line, same fault family (setup-arm skip), different construction: the setup arm increments
unless the block is run with `root=r` — the witness run's private literal. Observed
(`repro.log`, script rc=0; per-run rc below):

```
witness_ok=True(vector)
  pristine block_run=(2, 'REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)')
  mutant   block_run=(2, 'REGRESSION: SETUP (case-tally mismatch: cases=9 counted=8)')
  tool=ACCEPT rc=0 last='TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)'
  CHECK runtime PASS vectors=15158 mismatched=0
```

Mutant sha `2ec7cc479b4333111933ace6d06d6f6980a846078bab5821c4f4848428109b63`.
The gate certifies a must-kill that is dormant under both configurations the tool audits (and
under the runner's real `--regression` default `root=/tmp/tally-audit-work`). It is a false
must-kill: adding it to the sealed set would drive `ho_kill < ho_kt` and fail C1 closed.
Mutant verdict against the tool: **SURVIVED** (ACCEPT); against the gate: validated. That
disagreement is the finding.

### 4.3 Accept-labelled gate-valid copy the tool KILLs (false must-accept; genuine defect)

Exact JSON (`$S/adv-accept-root-inverse.json`, sha
`e1891a517439db1fcc9dfbd59925a36027f029b8a4343de8e7272757083b733a`):

```json
{
 "id": "adv-accept-root-inverse",
 "author": "tameshi-r34 Mutkillvectorsetuparmskip",
 "set": "accept",
 "edits": [
  {
   "old": "      *) nsetup=$((nsetup + 1)) ;;\n",
   "new": "      *) [[ $root == r ]] && nsetup=$((nsetup + 1)) || : ;;\n"
  }
 ],
 "witness": {
  "vector": [2, 0, 0, 0, 0, 0, 0, 0, 0]
 }
}
```

This is the same setup-arm skip inverted: the arm increments only at `root=r`, so under both
audited roots (`tally-audit`, `/tmp/tally-audit-work`) it drops setup statuses — a genuine
setup-undercount defect in real execution. The witness run at `root=r` takes the other branch:

```
witness_ok=True(vector-equivalence)
  pristine block_run=(2, 'REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)')
  mutant   block_run=(2, 'REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)')
  tool=KILL rc=1 last='TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)'
  CHECK runtime FAIL vectors=15158 mismatched=14994; first: cfg(0,1) statuses
    2 0 0 0 0 0 0 0 0: got (2, '… case-tally mismatch: cases=9 counted=8'),
    want (2, '… passed=8 cannot-verify=1')
```

Mutant sha `9715a07d0079d26a54b435d26e5bb43366067a64b97a954aa8b0f187bbc2b4fd`.
The tool's first mismatch is the very witness vector, under the audited config, while the witness
run at `root=r` sees byte-identical behaviour. The gate would admit a true defect as a must-accept;
adding it would drive `ho_accept < ho_at` and also fail C1 closed. The tool itself is correct here —
the gate is not. Mutant verdict against the tool: KILLED (correct); against the gate: validated as
accept. That disagreement is the mirror finding.

### 4.4 Class enumeration (same family, different constructions)

All variants use the same single edit site and witness vector; `old` count is 1 in every case.
`$S/repro.py` prints `opposite=true` and exits 3 when the gate validates but the tool disagrees.

| discriminator (block_run vs audited configs) | JSON (sha256 prefix) | witness | tool | repro rc | gate-vs-tool |
|---|---|---|---|---|---|
| `root` (`r` vs `tally-audit` / `/tmp/tally-audit-work`) | `adv-kill-root-keyed.json` (`b2074bfb…`) | True (kill) | ACCEPT rc=0 | 3 | **opposite** |
| `HOME` (`/w` vs temp dir) | `adv-kill-home-keyed.json` (`5373d7f9…`) | True (kill) | ACCEPT rc=0 | 3 | **opposite** |
| `TMPDIR` (`/tmp` vs temp dir) | `adv-kill-tmpdir-keyed.json` (`7128d19e…`) | True (kill) | ACCEPT rc=0 | 3 | **opposite** |
| `PWD` (`/w` vs temp dir) | `adv-kill-pwd-keyed.json` (`01235eb8…`) | True (kill) | ACCEPT rc=0 | 3 | **opposite** |
| `auto` (`0` vs `0` / `1`) — covered by config 0 | `adv-kill-auto-keyed.json` (`8685faeb…`) | True (kill) | KILL rc=1 | 0 | matches |
| status-2-only skip (no config branch) — covered by the panel | `adv-kill-status2-only.json` (`43634ae9…`) | True (kill) | KILL rc=1 | 0 | matches |

Boundary controls: the `auto`-keyed variant (`$S/adv-kill-auto-keyed.json`) is killed with
`CHECK runtime FAIL` because config `(0,1)` reproduces `block_run`'s `auto=0`; the non-config
status-2-only construction is killed because status 2 at every position is in the panel. So the
evasion is not "any construction": it requires a branch on a configuration/environment value that
`block_run` does not share with either audited config. `KEEP` is likewise covered by config
`(0,1)` (`KEEP=1`, `tool.py:265`), by inspection. Full JSON sha256s and per-run outputs for every
row are in `$S/repro.log`.

### 4.5 What this establishes and what it does not

- It does **not** contradict the landed receipt: the authored sealed set's eight kill copies were
  measured killed, and this seat re-verifies its assigned copy KILLED (§3). The deciding run stands.
- It **does** bound amendment 6: the kill+vector branch accepts any `a != b` measured at
  `root=r auto=0 KEEP=1`, and the accept+vector branch accepts any `a == b` measured there, without
  requiring the witness run to use one of the configurations `check_runtime` audits
  (`tool.py:265`). A copy can therefore be gate-valid with its witness-set label opposite to the
  tool's verdict. The counter fails closed on such a copy (`ho_kill < ho_kt` or
  `ho_accept < ho_at` → `C1_R33_PASS=false`), so there is no false PASS of the landed measurement;
  the gap is in the gate's soundness, not in the tool's verdict on the sealed set.
- This is distinct from the panel-vector coverage finding recorded by the sibling threshold seat:
  here the witness vector **is** in the 15,158-vector panel and is the tool's first mismatch; the
  divergence is the execution configuration, not the vector.
- No tool edit is proposed (frozen artifact; contract unchanged). This is a gate/coverage finding
  for the round's residue list.

### 4.6 Verdict summary

| probe | expected | observed | verdict |
|---|---|---|---|
| sealed `ho-kill-vector-setup-arm-skip` (kill) | KILL | KILL rc=1, runtime=fail | **KILLED** |
| root-keyed kill (4.2) | KILL per gate | gate True; tool ACCEPT rc=0 | **SURVIVED** / gate-valid |
| HOME-keyed kill (4.4) | KILL per gate | gate True; tool ACCEPT rc=0 | **SURVIVED** / gate-valid |
| TMPDIR-keyed kill (4.4) | KILL per gate | gate True; tool ACCEPT rc=0 | **SURVIVED** / gate-valid |
| PWD-keyed kill (4.4) | KILL per gate | gate True; tool ACCEPT rc=0 | **SURVIVED** / gate-valid |
| root-inverse accept (4.3) | ACCEPT per gate | gate True; tool KILL rc=1 | tool KILLED; gate-valid as accept |
| pristine baseline | ACCEPT | ACCEPT rc=0 | matches |

No run was inconclusive: every `run_tool_sandboxed` returned a clean KILL/ACCEPT with rc 0 or 1,
and the pristine baseline passed at the start and again after the adversarial variant batch; every
`repro.py` run also re-verifies the pinned tool/runner bytes (exit 2 otherwise).

## 5. Reproduction (from the fleet root; no lane writes)

```
S=/fast/scratch/hyaku/tameshi-r34-seats/Mutkillvectorsetuparmskip
L=/home/vgpnk/Projects/shokunin/tameshi-shokunin
python3 $S/repro.py $L/.ufo/evidence/round-33/heldout/ho-kill-vector-setup-arm-skip.json; echo $?   # 0
python3 $S/repro.py $S/adv-kill-root-keyed.json;       echo $?   # 3
python3 $S/repro.py $S/adv-kill-home-keyed.json;       echo $?   # 3
python3 $S/repro.py $S/adv-kill-tmpdir-keyed.json;     echo $?   # 3
python3 $S/repro.py $S/adv-accept-root-inverse.json;   echo $?   # 3
python3 $S/repro.py $S/adv-kill-pwd-keyed.json;        echo $?   # 3
python3 $S/repro.py $S/adv-kill-auto-keyed.json;       echo $?   # 0
python3 $S/repro.py $S/adv-kill-status2-only.json;     echo $?   # 0
```

`repro.py` re-verifies both pins (exit 2 on mismatch), applies the JSON edits, calls the amended
`ho_witness_ok`, then the real `run_tool_sandboxed`; it exits 3 exactly when the gate validates and
the tool verdict is opposite to the label, 4 when the witness does not validate. Full captured
output and exit codes: `$S/repro.log` (wrapper rc=0). The sealed run prints
`tool_outcome=KILL tool_rc=1 witness_ok=true`; the root-, HOME-, TMPDIR- and PWD-keyed runs print
`tool_outcome=ACCEPT tool_rc=0 witness_ok=true opposite=true`; the accept-inverse prints
`tool_outcome=KILL tool_rc=1 witness_ok=true opposite=true`; the `auto` and status-2 controls print
`tool_outcome=KILL tool_rc=1 witness_ok=true opposite=false`.

## 6. Bounds compliance and restoration evidence

- Lane untouched: `git -C $S/lane status --porcelain` → 0 lines; `cmp -s $S/tool.py
  $S/lane/tools/tally-audit-v2.py` rc=0; `cmp -s $S/pristine.sh
  $S/lane/tools/mutate-and-run.sh` rc=0; HEAD still `0b99d48…68b7`. No git/jj write commands.
- Pristine bytes unchanged before and after every run: `tool.py`
  `7b11ba25…98d10`, `pristine.sh` `a7d3f2dd…12eb9` (observed at extraction and again after the
  final probe; `pins.sha`, `repro.log`).
- Fleet sealed JSON observed `633ba5b6…13e90` and never written; counter lane/fleet shas both
  `f6b8868c…07f28c`.
- All writes are inside `$S` (scratch copies, JSONs, logs, `repro.py`) plus this report. The mutated
  runners are new files in `$S`; no shared artifact required restoration, and no before/after byte
  change occurred on any pinned artifact.
- Kill rule honored: the counter was imported and its functions called on scratch copies only; no
  default-mode `c1-measure.py` invocation. Every command's exit code was captured with
  `cmd; echo $? > file`, never `&&`. No subagents, no `agent://all`, no model parameter.

# ReplayC2 — round 42, wave 2 (FALSIFY): replay of the C2 base and control receipts, plus a pre-run at the tip

Seat: `L1Tameshi42.ReplayC2`. Access date: 2026-10-25. Lane HEAD: `a21845f523b75adbd3e3f7a62af91294db224ad9`, which is the integration tip.
What I attacked: the three C2 receipts wave 1 produced (`before/c2-at-base`, `control/c2-junk`, `control/c2-v3-in-slot`), and the claim that at the tip only the mutant fields are still open.
I ran the counter from the lane root. The counter's sha256 is `3c3727ec…2890ff2`, which matches the contract pin `claims.C2.counter_sha256`, and every run printed `self_pin=1` or reached the scoring stage.
I wrote run outputs to `/tmp/tameshi-r42w2-ReplayC2-ywSd` and deleted the directory afterwards.

## Findings

### F1. All three receipts replay byte-identical. The receipts survive.

I used the exact commands recorded in `.ufo/waves/round-42/w1/ReviewControls.md:13` and `:27`, and the counting command from `contract.json` `claims.C2`. All three runs used `FREEZE=322b5cd32b4319a05340d249ae752d12a9e6b19f`.

| receipt | command (run from the lane root) | exit | `diff` stdout / exit / stderr |
|---|---|---|---|
| `before/c2-at-base.*` | `python3 .ufo/evidence/round-42/census/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev c77c2b7e64d2e356381441ecf94abac03e984606 --freeze 322b5cd…` | 1 | identical / identical / identical (both empty) |
| `control/c2-junk.*` | same command plus `--tool-file .ufo/evidence/round-42/control/junk-tool.py` | 1 | identical / identical / — (stderr empty) |
| `control/c2-v3-in-slot.*` | same command plus `--tool-file tools/write-path-census-v3.py --text-mode` | 1 | identical / identical / — (stderr empty) |

The sha256 of each replayed stdout equals the receipt's sha256:

- `before/c2-at-base.stdout`: `eb2d8eea65c687dde84469d433d4ab092c1998279c53e559a2286ff4e2084cf4`
- `control/c2-junk.stdout`: `f47e046bdb7a78e6f53a92c59c5ee4ade80564b31159f9f608af7d7fc9877d02`
- `control/c2-v3-in-slot.stdout`: `a05830a7d81d4febbdb8ca42fa706872e265a5397675a5cdb88e04435f2fa3f6`

The base line reads `tool_absent=1 v3_sha_ok=1 v2_sha_ok=1 live_unflagged_v3=3 … C2_R42_PASS=false`, which matches `claims.C2.before_expected`.

The control inputs are the bytes the receipts name:

- The working-tree v3 sha256 is `095924a7…0279`. That equals the counter constant `V3_SHA` (`census/measure.py:67`), the `tool_sha256` in `c2-v3-in-slot.stdout`, and the blob at c77c2b7, 322b5cd and a21845f.
- `junk-tool.py` has sha256 `99424c38…4a45`, which equals the `tool_sha256` in `c2-junk.stdout`.

### F2. At the freeze revision, the counter also matches the contract's base expectation

Command: `python3 .ufo/evidence/round-42/census/measure.py --lane … --rev 322b5cd32b4319a05340d249ae752d12a9e6b19f --freeze 322b5cd…`. Exit 1.

Output: `C2_R42: tool_absent=1 v3_sha_ok=1 v2_sha_ok=1 live_unflagged_v3=3 rev=322b5cd3… C2_R42_PASS=false`.

v4 is absent at the freeze; it first appears at 5f739ac. So the freeze leaked no v4 bytes.

### F3. Pre-run at the tip: every non-mutant field is green. The claim survives.

This run is labelled pre-run. It is not the deciding run.

Command: `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-42/census/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev a21845f523b75adbd3e3f7a62af91294db224ad9 --freeze 322b5cd32b4319a05340d249ae752d12a9e6b19f`. Exit 1, stderr empty, no FAIL or ERROR lines.

```
C2_R42: self_pin=1 tool_absent=0 tool_sha256=784de4c0feef3364c4444632788af7ebb57d53032b79f60cc4330c094d122fe5 v3_sha_ok=1 v2_sha_ok=1 selftest_exit=0 fixtures_pass=10/10 run_errors=0 live_1682_ok=1 live_1685_ok=1 live_123_ok=1 live_unflagged_v3=3 live_unflagged_v4=0 live_tool_errors_v4=0 mutants_declared=0 mutants_killed=0 mutant_classes_killed= rev=a21845f523b75adbd3e3f7a62af91294db224ad9 freeze=322b5cd32b4319a05340d249ae752d12a9e6b19f C2_R42_PASS=false
```

- **Predicate check.** I compared this line against the predicate conjunction at `census/measure.py:462-465`. Every conjunct is satisfied except `mutants_ok` (`:455`): `self_pin=1`, `tool_absent=0`, `v3_sha_ok=1`, `v2_sha_ok=1`, `selftest_exit=0`, `fixtures_pass=10/10`, `run_errors=0`, all three `live_*_ok=1`, `live_unflagged_v4=0`, and `live_tool_errors_v4=0`. `mutants_ok` is false only because `census/mutants.json` is absent at a21845f; `ls .ufo/evidence/round-42/census/` shows only `measure.py`.
- **Agreement with the committed pre-run receipt.** After masking `rev=`, this line equals `prerun/c2-at-5f739acf.stdout` (`diff` exit 0). `git diff --stat 5f739ac a21845f -- tools/ .ufo/evidence/round-42/census/` is empty, so the tool bytes did not change between the two revisions.
- **Controls still fail at the tip.** These are CONTROL runs at `--rev a21845f…`.
  - junk: `fixtures_pass=1/10`, all three `live_*_ok=0`, `C2_R42_CONTROL_PASS=false`, exit 1.
  - v3-in-slot: `selftest_exit=1`, `fixtures_pass=8/10`, `live_unflagged_v4=3`, exit 1.
  - The FAIL lines for both controls are identical to their base receipts.
  - The v4 working-tree file run as `--tool-file` matches the default-mode pre-run field for field (`C2_R42_CONTROL_PASS=false`, because control runs never pass, `:462`).

### F4. The mutant fields are the only blocker, confirmed in a scratch clone

I wanted to show that green non-mutant fields plus a valid `mutants.json` is enough to pass. I ran this in `/tmp/tameshi-r42w2-ReplayC2-clone-Wr3A`, created with `git clone --shared` and checked out at a21845f. I committed a scratch `mutants.json` there with three probe mutants, and deleted the clone afterwards. These probes are not the MutantAuthor seat's file and nothing about them is recommended for the lane.

| probe | class | find (count in v4) | replace |
|---|---|---|---|
| `probe_attr_off` | attr | `if ctx.cls is not None and _is_self_attr(node) and node.attr in ctx.cls.attrs:` (1) | `if False:` |
| `probe_method_off` | method | `value, method_env = ctx.cls.method_return(node.func.attr)` (1) | `value, method_env = None, None` |
| `probe_outflag_off` | outflag | `flag = ctx.module.out_dests.get(node.attr)` (1) | `flag = None` |

- **Default-mode run on the clone** (rev `73d3b4eb…`): `python3 .ufo/evidence/round-42/census/measure.py --lane /tmp/tameshi-r42w2-ReplayC2-clone-Wr3A --rev 73d3b4ebd1d33727b2a4936464a5afb110fb11e6 --freeze 322b5cd…`.
  - Kill details: `MUTANT probe_attr_off … outcome=killed detail=F01_attr_scratch scratch=0 want 1`, `probe_method_off … killed detail=F01_attr_scratch scratch=0 want 1`, `probe_outflag_off … killed detail=F04_outflag explicit_out=0 want 1`.
  - Result: `mutants_declared=3 mutants_killed=3 mutant_classes_killed=attr,method,outflag … C2_R42_PASS=true`, exit 0.
- **Negative check** (rev `90e44ef8…`): I replaced the outflag probe with an equivalent rewrite, `flag = (ctx.module.out_dests.get(node.attr))`. Result: `outcome=survived`, `mutants_killed=2`, `C2_R42_PASS=false`, exit 1. So the mutant gate is not trivially satisfiable.
- **Side observation for MutantAuthor.** Both the attr and method probes are killed only through F01 (and the live 1682/1685 sites). F01 is the one fixture that exercises the attribute-through-method fold. Since each class kills only through that path, a mutant that breaks one class while F01 still passes would survive.

### F5 (low severity): the receipts were written after the freeze commit and committed in 5f739ac

- The freeze commit `322b5cd` is dated 06:22:19 -0300.
- Receipt mtimes are 06:22:32–06:22:38: `before/c2-at-base.stdout` at 06:22:33.595, `control/c2-v3-in-slot.stdout` at 06:22:36.204, `control/c2-junk.stdout` at 06:22:38.302, and `junk-tool.py` at 06:22:36.210.
- `git log --diff-filter=A` shows that `before/c2-*`, `control/c2-*` and `control/junk-tool.py` were all added in `5f739ac` (06:41:37), not in the freeze commit. Only `census/measure.py` is in `322b5cd`.
- The contract frozen at 322b5cd names `control/c2-v3-in-slot.stdout` and `control/c2-junk.stdout` (`claims.C2.do_nothing_control`). At the freeze those files were not yet tracked, and `junk-tool.py` was not tracked either (the blob is absent at 322b5cd).
- Impact: none on content. F1 reproduces every byte from the pinned counter and the pinned or hash-matched inputs. However, these receipts are not tamper-evident at the freeze; what makes them trustworthy is this replay, not their commit history.

## Residual risk and verification gaps

- `.ufo/evidence/round-42/census/__pycache__/measure.cpython-314.pyc` appeared in the lane at 06:46:19. It is gitignored (`.gitignore:4`). I did not create it: running a script directly with `python3 path.py` does not write bytecode for `__main__`, so a sibling seat must have imported the counter. It is not tracked and does not affect the counter's self-pin, which hashes the `.py` file.
- I did not author or review the real `mutants.json`. The deciding run still depends on that file. F4 only shows that the gate passes when the mutants are real and fails when one survives.
- `git status --short` in the lane after my work shows only the pre-existing `?? .ufo/waves/round-42/{dispatch-w2.json,spec-w2.json,w2/}`. HEAD is still a21845f. I made no lane writes other than this report.

Tooling: I installed nothing.

Verdict: SURVIVES — all three C2 receipts replay byte-identical, and the a21845f pre-run is green on every field except the mutant fields (`mutants.json` is absent). Provenance note F5 does not change any value.

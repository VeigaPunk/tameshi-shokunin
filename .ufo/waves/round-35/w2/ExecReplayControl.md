# Round-35 W2 — ExecReplayControl

Axes: revision fidelity, byte-for-byte receipt reproduction, and per-copy control calibration.

## Scope and method

Reproduced the requested C1 v2 control using the read-only lane clone at `/fast/scratch/hyaku/tameshi-r35-w2/ExecReplayControl/lane`, detached at `7da6e076c2e25936a3b60dde2a4080d8f05b7e5b` (setup command completed, exit 0). Scratch outputs are under `/fast/scratch/hyaku/tameshi-r35-w2/ExecReplayControl/`; no tool was installed, no lane contents or frozen artifact was edited, and the only repository write was this assigned report.

The counter invoked from that checkout is SHA-256 `515b0b1b00b970f31c08e80eb74512ecae0cf1082ddeccfcb373e810cd0559e8`. At the requested base, `tools/tally-audit-v2.py` is SHA-256 `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10`, and `tools/mutate-and-run.sh` is `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`.

## Finding

**BOUND — the requested base and the committed control receipt are different measurement revisions.**

Exact requested-revision invocation (paths are absolute):

```sh
mkdir -p /fast/scratch/hyaku/tameshi-r35-w2/ExecReplayControl/work && python3 /fast/scratch/hyaku/tameshi-r35-w2/ExecReplayControl/lane/.ufo/evidence/round-35/c1/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r35-w2/ExecReplayControl/lane --rev 51d3f08073be65d3475cf0286042fc0dbe4c4a7d --work /fast/scratch/hyaku/tameshi-r35-w2/ExecReplayControl/work --tool /fast/scratch/hyaku/tameshi-r35-w2/ExecReplayControl/lane/tools/tally-audit-v2.py
```

Measurement exit: **1**. Full stdout is `/fast/scratch/hyaku/tameshi-r35-w2/ExecReplayControl/actual.stdout`, SHA-256 `cade28087df183bd074d1a14a1b7c6a94ff0f895080880d867958fca79f07a6f`. Its only line is:

```text
C1_R35_CONTROL: mode=control tool_present=1 tool_sha=7b11ba25aead9367 tool_sha_ok=1 runner_sha_ok=1 pub_kill=0/0 pub_accept=0/0 pub_slots=0 pub_distinct=0 ho_kill=0/0 ho_accept=0/0 ho_invalid=0 ho_distinct=0 sealed_after_freeze=1 rev=51d3f08073be65d3475cf0286042fc0dbe4c4a7d C1_R35_CONTROL_PASS=false
```

There are no per-copy lines at this revision. `git ls-tree -r --name-only 51d3f08073be65d3475cf0286042fc0dbe4c4a7d -- .ufo/evidence/round-35/c1/` exited 0 and emitted no paths. Thus the counter correctly has no public specimens to score there; it does not reproduce the stored control stdout.

Byte comparison against the repository's `.ufo/evidence/round-35/control/c1-v2-control.stdout` (SHA-256 `8e975158ac5eab2cd4049b6549326bff1ef1eef840b2b9dd170392ee54859750`) gave `cmp -s` exit **1** and `diff -u` exit **1**. Exact difference:

```diff
@@ -1,9 +1 @@
-COPY kill  cfg00-accept-swap                  cfg00-accept-swap.json div=(0,0) rc=0 checks=- pass=False
-COPY kill  cfg11-pass-mask                    cfg11-pass-mask.json div=(1,1) rc=0 checks=- pass=False
-COPY accept comment-brace                      comment-brace.json div=- rc=1 checks=runtime pass=False
-COPY accept comment-esac                       comment-esac.json div=- rc=2 checks=- pass=False
-COPY accept comment-names-leg                  comment-names-leg.json div=- rc=1 checks=head pass=False
-COPY kill  root-keyed-auto-mask               root-keyed-auto-mask.json div=(1,0),(1,1) rc=0 checks=- pass=False
-COPY kill  root-keyed-auto-zero               root-keyed-auto-zero.json div=(1,0),(1,1) rc=0 checks=- pass=False
-COPY kill  workdir-branch-swap                workdir-branch-swap.json div=(1,0),(0,0) rc=0 checks=- pass=False
-C1_R35_CONTROL: mode=control tool_present=1 tool_sha=7b11ba25aead9367 tool_sha_ok=1 runner_sha_ok=1 pub_kill=0/5 pub_accept=0/3 pub_slots=8 pub_distinct=8 ho_kill=0/0 ho_accept=0/0 ho_invalid=0 ho_distinct=0 sealed_after_freeze=1 rev=23bd903a03c6b5311c5be46a3c2d51ec896e8b07 C1_R35_CONTROL_PASS=false
+C1_R35_CONTROL: mode=control tool_present=1 tool_sha=7b11ba25aead9367 tool_sha_ok=1 runner_sha_ok=1 pub_kill=0/0 pub_accept=0/0 pub_slots=0 pub_distinct=0 ho_kill=0/0 ho_accept=0/0 ho_invalid=0 ho_distinct=0 sealed_after_freeze=1 rev=51d3f08073be65d3475cf0286042fc0dbe4c4a7d C1_R35_CONTROL_PASS=false
```

## What I could not break / calibration proof

The stored receipt identifies revision `23bd903a03c6b5311c5be46a3c2d51ec896e8b07`. Replaying the same counter and v2 tool there produced measurement exit **1** (the expected failing control), full stdout SHA-256 `8e975158ac5eab2cd4049b6549326bff1ef1eef840b2b9dd170392ee54859750`, and `cmp -s` exit **0** against the stored file. This is byte-exact equality, including every per-copy result:

```text
COPY kill  cfg00-accept-swap                  cfg00-accept-swap.json div=(0,0) rc=0 checks=- pass=False
COPY kill  cfg11-pass-mask                    cfg11-pass-mask.json div=(1,1) rc=0 checks=- pass=False
COPY accept comment-brace                      comment-brace.json div=- rc=1 checks=runtime pass=False
COPY accept comment-esac                       comment-esac.json div=- rc=2 checks=- pass=False
COPY accept comment-names-leg                  comment-names-leg.json div=- rc=1 checks=head pass=False
COPY kill  root-keyed-auto-mask               root-keyed-auto-mask.json div=(1,0),(1,1) rc=0 checks=- pass=False
COPY kill  root-keyed-auto-zero               root-keyed-auto-zero.json div=(1,0),(1,1) rc=0 checks=- pass=False
COPY kill  workdir-branch-swap                workdir-branch-swap.json div=(1,0),(0,0) rc=0 checks=- pass=False
C1_R35_CONTROL: mode=control tool_present=1 tool_sha=7b11ba25aead9367 tool_sha_ok=1 runner_sha_ok=1 pub_kill=0/5 pub_accept=0/3 pub_slots=8 pub_distinct=8 ho_kill=0/0 ho_accept=0/0 ho_invalid=0 ho_distinct=0 sealed_after_freeze=1 rev=23bd903a03c6b5311c5be46a3c2d51ec896e8b07 C1_R35_CONTROL_PASS=false
```

The revision tree evidence is consistent: `git ls-tree -r --name-only 23bd903a03c6b5311c5be46a3c2d51ec896e8b07 -- .ufo/evidence/round-35/c1/` exited 0 and listed the counter plus these eight panel files; the corresponding listing at `51d3f08073be65d3475cf0286042fc0dbe4c4a7d` was empty. Therefore the receipt itself reproduces exactly at its recorded revision, while the requested base run is an empty-panel measurement. No CRITICAL finding about the v2 control is supported by this result; the blocker is the revision mismatch in the requested comparison.
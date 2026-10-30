# T57D4Controls — documentary review

Axes: exit-status correctness, receipt fidelity, revision identity, non-execution.

## Findings (severity order)

### P2 — controls process reports success despite a failed control

`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-57/controls.sh:88-89` sets `RES=0` on mismatch; lines 118-124 accumulate it, but lines 172-179 only print totals. The final unconditional `echo` supplies a successful process status; there is no final tally-dependent exit. This contradicts line 42's promise that a mismatch stops the round. Counter status is captured at lines 109-112 but is only printed, not an acceptance condition at lines 88-89.

Existing execution evidence (not re-executed): `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3RevControlsDry-receipts/run4/commands.json:134-145` records this command:

```text
bash /fast/scratch/hyaku/tameshi-r57/T57W3RevControlsDry/clone/.ufo/evidence/round-57/controls.sh /fast/scratch/hyaku/tameshi-r57/T57W3RevControlsDry/clone 5e3569969b532310d2b8a3d130901757a3df356b 332becb09a962561377e922ce13d835766087c30 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3RevControlsDry-receipts/run4/controls
```

Its recorded process exit is `0` (commands.json:143; run4/controls.exit:1). Output at `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3RevControlsDry-receipts/run4/controls.stdout:41-45` includes:

```text
CTL_MISMATCH CTL_POS_c1 expected=true actual=false counter_exit=1
CONTROLS_B: 1/2 as pre-registered
```

Recommendation: make overall exit conditional on both phases meeting their expected totals; separately specify/enforce expected counter exit values. Do not reinterpret this historical exit=0 as all controls passing.

Caller boundary: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-57/deciding-run.sh:146-153` independently checks equal numerator/denominator, rejects `CTL_MISMATCH`, checks exit receipts, and checks stdout digests. Therefore this finding does **not** demonstrate deciding-run admission of the failed set. No deciding-run or gate was executed here.

### P2 — retained before receipts mislabel the fallback echo status as counter exit

`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-57/integrate/before-runs.sh:15-16,35-36` uses `counter || echo "counter exit=$? ..."`, then a second echo with `exit=$?`. After a failed counter and successful fallback echo, that second value is the echo/OR-list status, not the counter status. `set -e` does not repair this: the failing command is handled by `||`.

Documentary sweep commands and actual output:

```text
read /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-57/before/c1.stdout:52-56
C1_R57: self=ca48e3c8c8db rev=73648682ebbd rows=0/51 agree=0/51 old49=ok fixed=0 declined=0 thisround=0 panel=pin spot=ok total=58 C1_R57_PASS=false
counter exit=1 (expected: PASS=false)
c1 rev=73648682ebbdcddf36809e2d7a4980004752065d exit=0

read /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-57/before/c2.stdout:11-13
C2_R57: self=a5138acb2248 rev=ba4ed823b99e gate_rows=0 exits=none held=0/0 mutants=0/3 skill_row=0 codes_known=4/4 standing_cell=WRONG:RECEIPT_REV_MISMATCH total=11 C2_R57_PASS=false
counter exit=1 (expected: PASS=false)
c2 rev=ba4ed823b99ea0ce7122e89f6652c8bac5b0c76a exit=0
```

The false verdicts and explicit `counter exit=1` are honestly retained; the final revision-labelled `exit=0` trailers are not truthful counter-exit summaries. For C2 the directly observed status is that of the timeout wrapper, also `1` here. These receipts are contradictory, not evidence of counter success. Preserve historical bytes; document the correction and fix future capture to save status immediately and reuse the saved value. No receipt was altered or regenerated.

## Residual risk and verification gaps

- Dry report `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3RevControlsDry.md:20,98-104` correctly limits run4 to a synthetic-provenance scratch overlay, not C0b certification. Lines 102 and `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3RevControlsDry-receipts/run.py:79-81` disclose another misleading field: terminal `controls_exit` takes the last counter's status, not controls status. The labelled controls receipt is authoritative; runner lines 10-15 capture subprocess returncode directly. The report and its structured `controls.exit=0` agree with that receipt.
- Read-only command `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff 5e3569969b532310d2b8a3d130901757a3df356b adf87899c70d616140a81185a8f9acbbdfb30392 -- .ufo/evidence/round-57/controls.sh .ufo/evidence/round-57/integrate/before-runs.sh .ufo/evidence/round-57/before/c1.stdout .ufo/evidence/round-57/before/c2.stdout` returned no output. A subsequent `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin ls-tree -r adf87899c70d616140a81185a8f9acbbdfb30392 --` with those same four paths also returned no output. Thus these are local review artifacts absent from C0b, not a demonstrated C0b diff. No claim of candidate integration or current admission is supported.
- `read xd://lsp` returned `No such tool`; references/definition/diagnostics were unavailable. Text searches and source reads are literal fallback, not semantic proof. The caller sweep covered round-57 evidence and dry-c1.sh, not every historical fleet artifact.
- No controls, gates, tests, builds, exploit reproduction, credentials, external targets, installations, production edits, delegation, commits, or pushes. Only the two assigned report files were written. Existing historical execution receipts were read, not independently reproduced. Candidate integration remains **UNVERIFIED**; no admission recommendation.

Self-evaluation: accuracy 4 (historical returncodes not independently reproduced); completeness 4 (scoped caller sweep, not fleet-wide); clarity 4 (historical versus local evidence separated); actionability 4 (capture correction specified, intentionally not implemented); conciseness 4 (exact paths and command evidence require repetition). Overall 4.0. Highest-impact improvement is authorized future status capture evidence after a real correction, outside this non-execution assignment.

# ExecC2Oracle — Kill-oracle probes (round 42, wave 1)

Seat: L1Tameshi42.ExecC2Oracle (leaf). Date: 2026-10-25. Lane: /home/vgpnk/Projects/shokunin/tameshi-shokunin.
Measurement context: `--rev 322b5cd32b4319a05340d249ae752d12a9e6b19f --freeze 322b5cd32b4319a05340d249ae752d12a9e6b19f`
(freeze commit). All three runs are `--probe-mutant` control runs: they print `C2_R42_CONTROL`
and are never the deciding measurement (contract `kill_rule`, contract.json:47). No lane file
edited; no tool installed/updated this seat. Probe tools kept at
/tmp/tameshi-r42-ExecC2Oracle-probes/ (sha256 below).

## Oracle under test

`census/measure.py:311-317`:
`oracle()` → any battery error ⇒ `runtime_error`; else any fail ⇒ `killed`; else `survived`.
Battery = 10 fixtures + 3 live sites, each run out-of-process (`run_tool` measure.py:229-260):
exit≠0 or Traceback ⇒ error; unparseable JSON/shape ⇒ error (`unparseable <Exc>`); a site
differing from its declared classification ⇒ fail. Contract `kill_oracle` sentence
(contract.json:46): "killed iff every battery run exits 0 with parseable output and at least one
battery case differs from its declared classification; non-zero exit, Traceback or unparseable
output is runtime_error … not killed; no differing case is survived".

## Probe A — unconditional exception ⇒ runtime_error (matches)

Tool `probe-a-exception.py` (64 B, sha256 `97c7595997ba527a03ec7001f884a233f12d0fafe8242e254dab836542f0b608`):
`import sys; raise RuntimeError('probe-a: unconditional failure')`.

Command:
`python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-42/census/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 322b5cd32b4319a05340d249ae752d12a9e6b19f --freeze 322b5cd32b4319a05340d249ae752d12a9e6b19f --probe-mutant /tmp/tameshi-r42-ExecC2Oracle-probes/probe-a-exception.py`

Output (exit 0):
```
PROBE outcome=runtime_error detail=F01_attr_scratch exit=1 ['RuntimeError: probe-a: unconditional failure']
C2_R42_CONTROL: probe_outcome=runtime_error rev=322b5cd32b4319a05340d249ae752d12a9e6b19f freeze=322b5cd32b4319a05340d249ae752d12a9e6b19f
```
Oracle matches contract: non-zero exit with Traceback ⇒ runtime_error, not killed (run_tool
measure.py:238-239).

## Probe B — control junk-tool.py copy ⇒ killed (matches)

Tool `probe-b-junk.py` = byte-identical copy of `round-42/control/junk-tool.py` (sha256
`99424c38276ada5b0776a5c41a99cca5b51938e1c8f57b7d7348926cf0754a45` = the control receipt's
`tool_sha256`). It mirrors v3's bits with `explicit_out=False, unflagged=False` for every site.

Command: same template, `--probe-mutant /tmp/tameshi-r42-ExecC2Oracle-probes/probe-b-junk.py`.

Output (exit 0):
```
PROBE outcome=killed detail=F01_attr_scratch scratch=0 want 1
C2_R42_CONTROL: probe_outcome=killed rev=322b5cd32b4319a05340d249ae752d12a9e6b19f freeze=322b5cd32b4319a05340d249ae752d12a9e6b19f
```
Oracle matches contract: all runs exit 0, output parseable, ≥1 case differs from declared ⇒ killed.

Depth note — why F01 differs, and a receipt inconsistency:
- v3 (live checkout, rev-pinned, and base all sha256 `095924a7…` = `V3_SHA`) still classifies the
  F01 attr-scratch site as `scratch=0` (v3's known blind spot; v4 fixes it). Verified directly:
  `python3 -I tools/write-path-census-v3.py --file /tmp/tameshi-r42-ExecC2Oracle-probes/f01/F01.py`
  → `…:17 open expected=1 scratch=0 unflagged=1 …`. The junk probe reports exactly those bits
  (with explicit_out/unflagged forced False), so F01 differs from declared `{expected:1, scratch:1,
  explicit_out:0, unflagged:0}` (FIXTURES measure.py:72-92) → first fail = F01.
- The committed control receipt `.ufo/evidence/round-42/control/c2-junk.stdout` does **not** list an
  F01 FAIL (it lists F02…F09 + the three live sites), and the contract prose (contract.json:48) names
  only F02 F03 F05 F06 F07 F08 F09 (omitting F01 *and* F04, while the receipt includes F04). So the
  receipt/prose and the frozen measure's actual behavior already disagreed about F01 (and F04) before
  this probe. The verdict is unaffected (killed either way), but the receipt's "which cases fail"
  detail does not reproduce against the frozen FIXTURES/junk vintage.

## Probe C — `{"sites": "x"}` ⇒ runtime_error (unparseable, matches)

Tool `probe-c-unparseable.py` (51 B, sha256 `df1d11c6b98a56812d1316e28cf6220713a1ec8fad4246d97ec02a93fdd49158`):
`import json, sys; print(json.dumps({"sites": "x"}))`.

Command: same template, `--probe-mutant /tmp/tameshi-r42-ExecC2Oracle-probes/probe-c-unparseable.py`.

Output (exit 0):
```
PROBE outcome=runtime_error detail=F01_attr_scratch unparseable TypeError
C2_R42_CONTROL: probe_outcome=runtime_error rev=322b5cd32b4319a05340d249ae752d12a9e6b19f freeze=322b5cd32b4319a05340d249ae752d12a9e6b19f
```
Oracle matches contract: `sites` is a string, not a list; iteration yields `site['lineno']` TypeError
→ `unparseable TypeError` (run_tool measure.py:250-259) ⇒ runtime_error, not killed.

## Integrity checks (all passed)

- Freeze commit holds the pinned counter: `git -C <lane> ls-tree -r --name-only 322b5cd… -- .ufo/evidence/round-42/` lists `census/measure.py`, `calibration/measure.py`, `contract.json`; blob sha of frozen `census/measure.py` = `3c3727ece033263f9e68ca2601012dc0170c6387cee44f3e7c09ee5744890ff2` = contract counter_sha256 (contract.json:40). Self-pin check (measure.py:371-378) passed on every probe run (no `SETUP` line, exit 0).
- `--rev`/`--freeze` resolve in the lane: `git rev-parse --verify` returned `322b5cd32b4319a05340d249ae752d12a9e6b19f` and `c77c2b7e64d2e356381441ecf94abac03e984606`.
- Lane status clean apart from untracked round-42 evidence/wave dirs (no tracked modifications); nothing was written to the lane checkout except this report.

## Verdict

All three kill-oracle probes reproduce the contract sentence exactly: exception ⇒ runtime_error,
junk-classification-divergence ⇒ killed, unparseable output ⇒ runtime_error. The `--probe-mutant`
path is self-consistent and well-formed (exit 0, PROBE + C2_R42_CONTROL lines). One residual
inconsistency recorded: the committed `c2-junk.stdout` control receipt (and contract prose) do not
fully match the frozen measure's battery failure set (F01 absent from the receipt, F04 absent from the
prose); the outcome label (`killed`) is unaffected.
